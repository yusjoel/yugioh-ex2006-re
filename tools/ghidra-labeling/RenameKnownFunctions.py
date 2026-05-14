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

    # --- BATCH 13 (2026-05-05): card_list 渲染/OAM/文字/deck_slot 工具簇 ---
    ("FUN_081021dc", "load_card_list_entry_to_slot",
        "card_list 场景的卡槽数据加载入口. 根据 r0(list_type: 0=全库/1=format/2=其他) "
        "和 r1(card_index) 决定从哪张牌组数据区复制 6 列字段到 IWRAM 0x0202a4d0[+0x6c]. "
        "list_type==0 时按 r1>>5 定位 u32 位图确认该卡已出现; list_type==1 时调用 "
        "get_card_data_format_id 验证 card_index 在 format 范围内; 验证通过后调用 "
        "build_card_list_slot_display_entries 构建槽显示条目, 并循环填写 "
        "read/write_card_list_field_by_row_col 各字段, 最终调用 init_deck_slot_data. "
        "被 FUN_08108f80 (scene_card_list 顶层驱动) 以变化的 card_index 反复调用."),
    ("FUN_0810230c", "reinit_deck_slots_from_card_stats",
        "card_stats 场景下的牌组槽全量重新初始化入口. 无外部参数; 内部 ldr 加载 "
        "0x0202a4d0 (IWRAM card_list 槽基址), r6 = 0x0202a4d0+0x184 (card_stats 源). "
        "先以 copy_bytes_by_halfword(0x0202a4d0+0x6c, 0x02001138, 0x118) 把当前 "
        "card_stats 数据复制到 IWRAM 槽缓冲区, 再调用 reset_all_deck_slots 清空所有 "
        "牌组槽, 接着 populate_deck_slots_from_card_list 按卡列表重建槽内容, 最后循环 "
        "(index 1..3) 对非零槽调用 init_deck_slot_data 单独初始化, 并再次 "
        "copy_bytes_by_halfword 将槽区 0x17 字节属性拷回. "
        "被 FUN_08108fd8 (card_stats 大驱动) 在切入展示模式时调用一次."),
    ("FUN_08104318", "reset_card_list_scroll_offset",
        "card_list 场景的滚动偏移清零工具. 向 IWRAM 0x0202f3c0[+0x32] "
        "(card_list 状态结构体滚动偏移字段, s16) 写入 0, 返回 1. "
        "indeg=8 说明场景中多个初始化/场景切换点均需将滚动复位到顶部. "
        "与 sibling FUN_08104328 (纯 return 1) 形成一对: 08104318 带副作用, 08104328 为空存根."),
    ("FUN_08104328", "return_one_card_list_stub",
        "card_list / scene_duel_puzzle 场景通用的无操作成功占位函数. "
        "仅执行 movs r0,#1; bx lr, 始终返回 1. indeg=10 说明多个场景驱动在需要 "
        "'此步骤成功但无实际工作'时统一调用此桩. "
        "与 sibling reset_card_list_scroll_offset (08104318) 配对: 后者有 strh 副作用, 此函数为纯返回版本."),
    ("FUN_0810432c", "render_card_list_oam_entries",
        "card_list 场景 OAM 条目渲染主循环. 读取 0x0202f3c0[+0x1e] (bit0) 和 "
        "0x0202a4d0[+0x1f] (bit7) 两个标志, 任一置位则跳转到末尾直接返回. "
        "遍历 14 个卡槽, 对每个槽检查 slot_flags[+0x30] 对应位是否激活; "
        "激活时读取 x/y 坐标字段, 叠加行偏移后计算显示坐标, 调用 __divsi3 "
        "将 RGB 分量各调整亮度 (乘以 r7/15), 检查 card_flag bit1 决定高亮色, "
        "最终调用 dispatch_oam_write_by_mode 写入 OAM. "
        "外层循环结束后若 slot_flags!=0 则调用 blend_palette_entry_by_scroll_pos. "
        "被 7 个 card_list 场景驱动以固定节奏调用."),
    ("FUN_08104458", "return_one_card_list_oam_stub",
        "card_list 场景 OAM 渲染链中的无操作成功占位函数. "
        "仅执行 movs r0,#1; bx lr, 始终返回 1. indeg=7, "
        "被与 render_card_list_oam_entries (0810432c) 完全相同的 7 个 caller 调用, "
        "构成'做实际工作的函数 + 无操作存根'配对模式."),
    ("FUN_081044d4", "blend_palette_entry_by_scroll_pos",
        "card_list 场景高亮卡槽的调色板混合计算与写入函数. "
        "从 IWRAM 0x0202f3c0[+0x32] 读取当前滚动偏移 (s16), 超过 0xf 时改用 "
        "0x1e-scroll 做反向插值. 以迭代计数 0..14 从 ROM 调色板表 0x09e315d4 "
        "逐项读出 RGB565 颜色, 将 R/G/B 三分量各自拆分(5/5/5 bit), 乘以插值系数 "
        "r7(0..15)/15 通过 __divsi3 归一化, 重新组合为 RGB565 写入目标缓冲区. "
        "迭代结束后调用 copy_bytes_by_halfword 将 0x20 字节写入 BG 调色板 0x05000340, "
        "并将 0x0202f3c0[+0x32] 递增 (超过 0x1d 时归零). "
        "由 render_card_list_oam_entries 在 slot_flags[+0x30] 非零时作为高亮动画 tick 调用."),
    ("FUN_081065c0", "load_card_frame_tile_to_vram_slot_a",
        "card_list 场景卡框 tile 第一套的 VRAM 加载函数. "
        "从 IWRAM 0x0202a4d0[+0x18] (s16, 当前选中卡框 index) 读取帧索引, "
        "乘以 0x20 (<<5) 计算 ROM 卡框条目偏移, 加上基址 0x09e60600 定位到对应结构体. "
        "随后以 tile_2d_row_copy(r4[0x8], dst=0x06016a80, w=0xc, h=0x2) 将卡框主 "
        "tile 块写入 VRAM BG 区, 再以 copy_bytes_by_halfword(r4[0xc], "
        "dst=0x05000360, 0x20) 将 16 色调色板写入 OBJ 调色板 slot. "
        "与 sibling FUN_081066fc (load_card_frame_tile_to_vram_slot_b) 构成两套 "
        "卡框 tile 加载对, 均被 FUN_081045c4 (bg/vram/palette 场景初始化) 调用."),
    ("FUN_081066fc", "load_card_frame_tile_to_vram_slot_b",
        "card_list 场景卡框 tile 第二套的 VRAM 加载函数. "
        "与 sibling load_card_frame_tile_to_vram_slot_a (081065c0) 结构一致, "
        "但使用固定 ROM 源地址而非动态索引: "
        "tile_2d_row_copy(src=0x09e310b4, dst=0x06016300, w=0x8, h=0x2) 写第二套卡框 tile; "
        "copy_bytes_by_halfword(src=0x09e31794, dst=0x05000300, 0x20) 写对应调色板到 OBJ palette slot 0x18. "
        "均被 FUN_081045c4 (bg/vram/palette 场景初始化) 在 slot_a 之后调用."),
    ("FUN_08106130", "write_vram_bg_tilemap_card_list",
        "card_list 场景 BG tilemap 区域填写函数, 无外部参数. "
        "内部 ldr 加载 VRAM 基址 0x0600e000 存入 r8. "
        "从 IWRAM 0x0202f3c0[+0x26] 读取当前滚动偏移 (s16), 对 8 取模得到像素内偏移 "
        "(r7 = offset % 8), 再除以 8 得到 tile 行偏移. "
        "外层循环遍历 2 行, 内层遍历每行 8 个列组, 计算目标 tilemap 地址: "
        "基址 0x0600e000 + 行号*0x28*0x10 + 列偏移; "
        "以 0xffffa000 (tile_attr 掩码) 构建属性, 对 24 个 halfword 条目调用 strh 写入 tilemap. "
        "由 card_list 场景初始化驱动和文字渲染链中间层各调用一次."),
    ("FUN_081060e4", "render_text_dual_pass_with_shadow",
        "card_list 场景文字双次渲染工具, 产生描边/阴影效果. "
        "接收文字缓冲区指针 r0/r1 和打包参数 r2 (低 16 位=tile_x_offset, 高 8 位=tile_y_offset), "
        "分两次调用 text_render_wrapper: "
        "第一次以 0x8100 或运算后的颜色属性渲染背景层 (阴影色); "
        "第二次以 0x8000 或运算后的颜色属性渲染前景层. "
        "被 render_game_string_line_to_sprite_vram (08105d94) 和 "
        "render_banlist_card_row_text (081061d0) 以相同 (r0=tile_x, r1=tile_y, r2=packed_attr) 模式调用."),
    ("FUN_08105d94", "render_game_string_line_to_sprite_vram",
        "card_list 场景游戏字符串行文字的 sprite VRAM 渲染驱动. "
        "初始化时从 0x0202a4d0[+0x18] 读卡框索引计算 ROM 条目偏移, "
        "从 0x0202f3c0[+0x22] 读 card_type 枚举, 设置 line_buf 状态 (02006ed0[+8] bit1), "
        "选择对应 font_jp_base_table 条目写入 line_buf[+4]. "
        "随后调用 zero_fill_by_halfword 清空 VRAM 0x06000040 起 0x780 字节 sprite 区域, "
        "setup_line_buf_pos_and_font(r0=0x1e, r1=2) 设置位置, "
        "game_str_id_to_row(0x699) 获取主字符串行号, 根据 gSettings.lang 和 "
        "game_str_pointer_table 定位日文字符串指针, "
        "调用 render_text_dual_pass_with_shadow(6, 2, packed_attr, str_ptr). "
        "之后循环遍历 card_list 的所有条目行, 每行 copy_bytes_by_halfword 更新 "
        "line_buf VRAM 基址并调用 render_text_dual_pass_with_shadow + "
        "commit_line_buffer_to_sprite_vram 写入. "
        "被 FUN_08105bfc (card_list 场景完整 BG 初始化) 单次调用."),
    ("FUN_08105964", "query_card_list_slot_validity",
        "根据当前 card_list 展示模式 (0x0202a4d0[+0x18] s16, 值 0..5) 检验传入的 "
        "card_index 是否在有效范围内, 返回 0(无效/越界)、1(有效)、2(有效但格式受限) 三态结果. "
        "通过 6 路 switch 分派: case0 (mode=card) 检查 card_index < format_count; "
        "case1/2 (EX/GB pack) 对 0x0202f3c0[+0x24] (pack_card_count) 范围内的位图检验; "
        "case4/5 类似; default 返回 0. "
        "被 render_banlist_card_row_text (081061d0) 用于决定显示内容."),
    ("FUN_081061d0", "render_banlist_card_row_text",
        "banlist 场景卡片行文字渲染函数. 接收 r0=slot_index (0-based), r1=card_index, "
        "以 r0<<9 计算 VRAM 目标偏移加到 0x06000800 写入 sprite tile 区. "
        "调用 copy_bytes_by_halfword 初始化行缓冲, setup_line_buf_pos_and_font(0x18, 2) 设置字体. "
        "以 query_card_list_slot_validity(state, card_index) 判断有效性: "
        "返回 1 时 r7=8 (显示 -), 返回 2 时 r7=7 (特殊占位). "
        "若 0x0202a4d0[+0x18]==4 (format 模式) 则调用 lookup_card_entry_by_index + "
        "strncpy 写卡名并精确计算居中 x 偏移; "
        "非 format 模式则调用 game_str_id_to_row + 字符串指针表查找日文字符串. "
        "最终调用 render_text_dual_pass_with_shadow 渲染双层文字, 写入 sprite tile."),
    ("FUN_08105f34", "render_card_type_text_row_to_sprite",
        "card_list 场景卡片类型文字行的 sprite VRAM 全量渲染驱动. "
        "根据 0x0202a4d0[+0x18] (s16, 展示模式 0..5) 执行 6 路 switch: "
        "各 case 设置对应的 game_str_id (0x69c..0x06cd) 和显示行数 r6 (4..5), "
        "调用 game_str_id_to_row 获取字符串行号. "
        "初始化时设置 line_buf 状态 (02006ed0[+8] bit1) 并写 font 指针, "
        "zero_fill_by_halfword 清空 VRAM 0x06000040 sprite 区 (0x780 字节), "
        "setup_line_buf_pos_and_font(0x1e, 2). "
        "之后按行数循环调用 render_text_dual_pass_with_shadow + "
        "commit_line_buffer_to_sprite_vram 渲染各行. "
        "随后还渲染 game_str_id 0x69b (卡片属性) 到 VRAM 0x06003800, "
        "最后循环 8 行调用 render_banlist_card_row_text (FUN_081061d0) 渲染具体卡片行. "
        "被两个场景初始化驱动各调用一次."),

    # 2026-05-05: BATCH-14 落地 (topo=274/275/276/277/278/279/280/281/282/284/285/286/287/288/289)
    ("FUN_08105bfc", "init_card_list_sprite_oam_and_bg",
        "card_list 场景完整 sprite/OAM/BG 初始化函数. 从 0x0202a4d0[+0x18] 读当前卡框索引, "
        "从 0x09e60600 查 ROM 卡框条目结构体, 调用 upload_sprite_tiles_and_write_oam 写入 OAM slot; "
        "再以 upload_sprite_tiles_with_palette_blend 上传带调色板混合的 sprite tile. "
        "向 BG2HOFS/BG2VOFS 写入卷轴偏移 (negated), zero_fill_by_halfword 清空 VRAM sprite 区域 "
        "0x0600f000 和 0x0600e000, 并将 OBJ 调色板表 0x05000140 填入 16 色数据. "
        "最后写入 BG tilemap card_list 行与 game_string sprite 行. "
        "被 setup_card_list_scene_bg_regs (FUN_081045c4) 在场景初始化路径末段唯一调用."),
    ("FUN_081045c4", "setup_card_list_scene_bg_regs",
        "card_list 场景 BG 寄存器及场景状态初始化函数. 连续向 BG0CNT/BG1CNT/BG2CNT/BG3CNT "
        "(0x04000008+) 写入 4 个预设控制字 (0x1c02/0x1d09/0x1e8f/0x1f0f), "
        "将 BG0HOFS~BG3VOFS 共 8 个卷轴寄存器全部清零, 并将 BLDALPHA (0x04000052) 写入 0x5001 启用混合. "
        "随后调用 apply_blend_fadeout_flat 执行 fade 动画, 清除 0x0202f3c0[+0x1f] 的 bit6/bit0, "
        "将 gPrng+0x174 写入 0x5001. 接着 zero_fill_by_halfword 清空 5 块 VRAM 区域 "
        "(0x06004000~0x06013fff). 从 gSave 读取 deck_format 字段判断 card_type 格式以初始化 "
        "0x0202f3c0[+0x22] 的游标偏移. 被 dispatch_card_list_scene_state 等多个场景入口调用."),
    ("FUN_081047cc", "clear_dispcnt_blendcnt_and_obj_list",
        "清零 DISPCNT 与 BLDCNT 寄存器并清空场景 OBJ 列表的小函数. "
        "向 DISPCNT (0x04000000) 写 0 关闭所有 BG/OBJ 显示, "
        "向 BLDCNT (0x04000050) 写 0 关闭混合效果, "
        "再调用 init_scene_obj_list 清空 OBJ 列表; 返回固定值 1. "
        "被 dispatch_card_list_scene_state 等 4 个 card_list 场景变体初始化路径调用, "
        "作为每次场景切换前统一的显示/OBJ 复位步骤."),
    ("FUN_08105702", "set_scene_mode_flag",
        "将 r0 写入场景控制块 0x0202f3c0[+0x1f] (scene mode_flags 字段), "
        "通过尾调用 return_zero_from_scene_dispatch 固定返回 0. "
        "调用方 dispatch_card_list_scene_state 在场景状态转换末段调用本函数, "
        "传入经 AND 0x7f 处理过的标志字节, 用于保存模式标志并以返回 0 告知状态机迭代已完成. "
        "函数体仅 2 条指令 (strb + b), 是场景状态机中典型的 set-flag-then-exit 尾调用惯用法."),
    ("FUN_08106588", "copy_card_frame_tile_row_to_vram",
        "将 card_list 场景当前卡框的 tile 行数据复制到 VRAM BG tile 区域的辅助函数. "
        "从 0x0202a4d0[+0x18] (s16) 读取当前选中卡框 index, 乘以 0x20 计算 ROM 条目偏移 "
        "并加基址 0x09e60600 定位卡框结构体, 再从入参 r0 (行号) 计算目标 VRAM 地址 "
        "0x06000800 + row*0x200. 调用 copy_bytes_by_halfword(src=card_frame_entry[0], "
        "dst=vram_row_addr, len=0x600) 写入 tile 数据, 返回 1. "
        "被 dispatch_card_list_scene_state 在场景初始化路径调用, 用于按行刷新卡框 BG tile."),
    ("FUN_08105948", "tick_scene_anim_counter_mod29",
        "对场景动画帧计数器执行模 29 递增的单功能函数. "
        "读取 0x0202f3c0[+0x2a] (s16 动画帧计数器), 加 1 后写回; "
        "若结果超过 0x1d (29) 则归零. "
        "被 caller 0x08105520 (display/window/bg/frame_counter) 每帧调用, "
        "用于驱动需要 29 帧周期的场景动画效果 (如卡框高亮闪烁). "
        "函数体仅 11 条指令, 无调用, 是纯叶子计数器函数."),
    ("FUN_081058c8", "build_palette_row_to_obj_pal_slot",
        "按照当前动画帧计数器 0x0202f3c0[+0x28] 的相位, "
        "为 card_list 场景构建一行调色板数据并写入 OBJ 调色板 slot 0x05000360. "
        "对计数器值 [0xb..0xe] 范围内的每个颜色索引 (0..14), 由 0x09e31754 表查出基准 RGB565 颜色, "
        "按计数器偏移量调整亮度后写入临时缓冲区; 越界索引直接透传原始颜色. "
        "最后调用 copy_bytes_by_halfword 将 16 色 (0x20 字节) 写入 OBJ PAL 0x05000360, "
        "帧计数器加 1 模 0x20 后写回. "
        "被 caller 0x08105520 每帧调用, 实现卡框调色板闪烁动画."),
    ("FUN_0810672c", "write_card_cursor_oam_by_scroll",
        "根据场景当前滚动偏移量计算并写入卡牌游标 OAM 条目的函数. "
        "从 0x0202f3c0[+0x2a] (s16 scroll_phase, 范围 0..29) 读取当前帧相位, "
        "计算高度偏移 y_off = (0xe1 - (phase-15)^2 * 4) / 0xe1, "
        "再从 [+0x26] 读可视行数 visible_rows; 若 visible_rows > 0, "
        "则以 OAM 属性 y_off<<16|0x4 / r2=0x8f18 调用 dispatch_oam_write_by_mode 写入游标 OAM. "
        "随后读 [+0x26] (row_count) 与 get_card_data_format_id 比较, 决定游标 x 位置. "
        "再以 y=0x80-y_off, attr=0x40, x=scroll_x 调用 dispatch_oam_write_by_mode 写第二个 OAM 条目. "
        "被 caller 0x08105520 每帧调用."),
    ("FUN_081065fc", "write_card_slot_oam_all_rows",
        "遍历 card_list 场景所有卡槽行, 为每行卡牌写入 OAM 条目的驱动函数. "
        "外层循环以 r8 (行数上限, 来自 0x0202f3c0[+0x6]) 迭代, "
        "内层从 0x09e605e8 卡框条目数组 (entry_size=0xc bytes) 读取每格参数: "
        "从 [+0x6] 读显示项数 item_count, 从 [+0x2] 读基础 x 偏移, 从 [+0x4] 读 y step. "
        "结合 0x0202f3c0[+0x24] (当前选中 index) 与卡框 mode 标志 "
        "计算每个卡槽的 OAM x/y 坐标, 最终调用 dispatch_oam_write_by_mode 写入. "
        "被 caller 0x08105520 每帧调用."),
    ("FUN_081052aa", "set_card_list_slot_count",
        "将 r0 写入卡片列表控制块 0x0202a4d0[+0x20] (s16 slot_count 字段), "
        "通过尾调用 return_one_from_scene_dispatch 固定返回 1. "
        "调用方 dispatch_card_list_scene_state 在场景状态机的更新 slot 数量分支中调用, "
        "传入当前选中行的列计数值. "
        "函数体仅 3 条指令, 是场景状态机中对称于 set_scene_mode_flag "
        "(设置 mode_flag 并返回 0) 的 set-count-then-return-one 尾调用惯用法."),
    ("FUN_0810573e", "return_zero_from_scene_dispatch",
        "场景状态机分派函数的公共返回 0 出口. 设置 r0=0 后落入 return_one_from_scene_dispatch "
        "的公共栈恢复+返回序列. 与 return_one_from_scene_dispatch (FUN_08105740) "
        "构成对称的 return_zero/return_one 对, 供 dispatch_card_list_scene_state 等场景状态机 "
        "在各分支末尾直接尾跳转. 该模式在 GBA 场景状态机中普遍用于将 "
        "'本帧是否完成转换' 的布尔值返回给驱动循环."),
    ("FUN_08105740", "return_one_from_scene_dispatch",
        "场景状态机分派函数的公共返回 1 出口兼栈恢复序列. "
        "调用方 dispatch_card_list_scene_state 等场景驱动函数以 "
        "push {r4,r5,r6,r7,lr} + push {r5,r6,r7} + sub sp,#0xc 的三段式栈建立帧, "
        "本函数用 add sp,#0xc + pop {r3,r4,r5} + pop {r4,r5,r6,r7} + pop {r1}; bx r1 "
        "将三段完全拆除并跳返. 与 return_zero_from_scene_dispatch (FUN_0810573e) 构成对称对, "
        "set_card_list_slot_count 等短函数直接尾跳本函数以返回 1."),
    ("FUN_081047e8", "dispatch_card_list_scene_state",
        "card_list 场景主状态机分派函数. 读取 0x0202f3c0[+0x1f] bit7 判断场景是否激活; "
        "若未激活则进入 animating counter 路径. "
        "激活时检查 0x0202a4d0[+0x18] (s16 mode) 决定进入新场景初始化还是已激活场景更新两大路径. "
        "初始化路径: 检查 gSave 是否为 pass_input/banlist 模式, 选择合适的 page_state_dispatcher 表, "
        "调用 page_state_dispatcher 后按 flag 决定调用 setup_card_list_scene_bg_regs / "
        "reset_card_list_scroll_offset / write_vram_bg_tilemap_card_list 等完整初始化链. "
        "更新路径: 基于 0x0202f3c0[+0x38] 的 sub_state 字段进行 16 路 switch 分派, "
        "各 case 处理卡牌选择/滚动/确认/取消等交互. "
        "被 FUN_08108940 / FUN_08108da4 / FUN_08108eec 3 个场景驱动调用."),
    ("FUN_08105754", "return_one_scene_stub",
        "仅含 movs r0,#1; bx lr 两条指令的无操作占位函数, 固定返回 1. "
        "被 card_list 场景的 3 个场景变体驱动 (FUN_08108940 / FUN_08108da4 / FUN_08108eec) 共同调用, "
        "根据调用位置推断为场景生命周期中某一阶段的空实现槽 (如 cleanup / finalize). "
        "函数体字节与 return_one_card_list_stub (0x08104328) / return_one_scene_card_list (0x080ff430) "
        "模式完全一致. indeg=3 且 tag 为 scene_card_list."),
    ("FUN_08105758", "query_card_list_max_index",
        "根据当前 card_list 显示模式返回卡牌列表最大有效 index 上限的查询函数. "
        "从 0x0202a4d0[+0x18] (s16 mode, 值 0..5) 读取显示模式: "
        "若 mode==4 (全卡数据库), 调用 get_card_data_format_id 并返回其结果; "
        "若 mode 在 [5..6] 范围 (EX/GB pack), 读 0x0202a4d0[+0x24] (s16 pack_card_count) 并加 0xc 返回; "
        "其余 mode 返回固定值 0x3c (60). "
        "被 FUN_081089d8 (pass_input) 和 FUN_08108da4 (card_list scene) 调用, "
        "用于在滚动/选择时验证 index 是否越界. 纯只读无副作用."),

    # 2026-05-05: BATCH-15 落地 (topo=290/291/292/293/294/295/296/297/298/299/300/301/302/303/304)
    ("FUN_08105784", "check_card_index_in_format_range",
        "验证给定卡牌序号是否在当前卡组列表槽位允许的格式范围内. "
        "入参 r0 为待检卡牌线性序号. 读取 [0x0202a4d0+0x18] 槽类型字段: "
        "若为 4 (CUSTOM 格式) 则调用 get_card_data_format_id 获取格式 ID 并与序号比较; "
        "对其他槽类型则以固定上界 (CARD_LIST_MAX_INDEX=0x3b 或 [ctx+0x24]+0xc) 做范围检查. "
        "由 FUN_08108da4 (deck_edit 状态机) 在初始化时逐条调用以筛选可显示的卡牌条目. "
        "返回 1=序号合法, 0=越界."),
    ("FUN_08106eb4", "return_one_card_list_scene_stub",
        "card_list 场景专用空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "三个调用方 (FUN_081085d0/FUN_08108b38/FUN_0810ad98) 均为 card_list 场景帧调度器, "
        "在特定状态下以此占位代替真实的输入处理器, 返回 1 表示已处理/继续."),
    ("FUN_08106eb8", "return_one_puzzle_card_list_stub",
        "决斗谜题卡牌列表场景专用空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由 scene_duel_puzzle+card_list 双标签场景的帧调度器调用 (FUN_081086f8/FUN_08108c4c/FUN_0810aeb4), "
        "充当特定状态下的无操作输入处理占位符, 返回 1 表示已处理/继续."),
    ("FUN_08108da0", "return_one_deck_edit_stub",
        "deck_edit 页面专用空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由 enter_deck_edit_page (0x08108ac0) 唯一调用, "
        "在 deck_edit 场景状态机的某一分支中作为无操作处理器占位, 返回 1 表示继续."),
    ("FUN_08108f80", "init_card_list_scene_for_deck_slot",
        "为卡牌列表场景执行完整初始化流程, 适用于 deck_edit 页面中某个具体卡组槽位. "
        "向场景上下文 [0x0202a4d0+0x0] 写 2 (场景类型 ID), [+0x4] 写 1 (子模式标志); "
        "检查槽类型 [+0x18]: 若为 4 则 r0=1 否则 r0=0, 连同 [+0x22] 调用 load_card_list_entry_to_slot. "
        "依次调用 reset_card_list_scene_state/card_list_screen_init/reset_card_list_scroll_offset, "
        "最后写 gPrng+0x204 场景调度字 (OR 0x280) 触发状态机切换. 由 enter_deck_edit_page 调用."),
    ("FUN_08108da4", "tick_deck_edit_card_list_frame",
        "deck_edit 场景中卡牌列表页面的每帧驱动函数. "
        "调用 dispatch_card_list_scene_state 执行状态机分派, render_card_list_oam_entries 刷新 OAM. "
        "若 dispatch 返回非零则读 [0x0202a4d0+0x1e] 场景状态字 (5 路 switch): "
        "状态 1-4 各写 slot_type 1-4 至 [ctx+0x18] 并遍历 card_index 调用 check_card_index_in_format_range 筛选首条有效卡牌; "
        "状态 0 执行退出/还原. 返回 0=无转换, 1=完成转换. 由 enter_deck_edit_page 注册为主帧处理器."),
    ("FUN_08108ee8", "return_one_deck_edit_input_stub",
        "deck_edit 页面专用空操作输入处理占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由 enter_deck_edit_page (0x08108ac0) 唯一调用, "
        "注册为 deck_edit 某状态分支的输入处理器占位, 返回 1 表示已处理/继续."),
    ("FUN_08109038", "return_one_puzzle_deck_init_stub",
        "决斗谜题卡牌列表初始化序列中的空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由三个 caller 调用: FUN_081086f8 (scene_duel_puzzle/card_list 帧调度器), "
        "FUN_08108c4c (puzzle deck_edit 场景初始化), FUN_0810aeb4 (与 08106eb8 共享相同 caller 集合). "
        "在 puzzle 场景初始化/帧调度流程中充当初始化已完成/继续的固定占位返回."),
    ("FUN_08108c4c", "init_puzzle_deck_edit_card_list",
        "决斗谜题模式下卡牌列表 (deck_edit) 场景的完整初始化函数. "
        "由 enter_deck_edit_page 在 puzzle 分支调用. 依次调用两个占位存根 (08106eb8/08109038), "
        "return_one_card_list_stub 清理旧状态, init_card_list_display_and_objs 初始化显示对象, "
        "refresh_card_list_slot_display 刷新槽位. "
        "随后从 [0x0202a4d0+0x16] 读谜题选项字节, 将 bit0-4 重新打包到 IWRAM [0x02000000+0x6c30]. "
        "最后调用 init_puzzle_wram_then_copy 并写 gPrng+0x204 (OR 0xfc) 切换场景. 返回 1."),
    ("FUN_08108eec", "tick_deck_edit_name_input_frame",
        "deck_edit 场景中含 name_input 子页面的每帧驱动函数. "
        "调用 dispatch_card_list_scene_state 执行状态分派, render_card_list_oam_entries 刷新 OAM. "
        "若转换发生则读 [0x0202a4d0+0x20] 场景子状态 (s16): "
        "==1 则 return_one_card_list_stub + clear_dispcnt_blendcnt_and_obj_list + gPrng+0x204 OR 0x240 (切换到 name_input); "
        "!=1 则清屏 + 备份 [ctx+0x18] 至 [ctx+0x1a] + gPrng+0x204 OR 0xc0 (切回主列表). "
        "返回 0=无切换, 1=完成切换. 由 enter_deck_edit_page 注册为含 name_input 的分支帧处理器."),
    ("FUN_08108eb8", "init_card_list_scene_bg_with_scroll_reset",
        "card_list 场景背景寄存器初始化函数 (含滚动归零). "
        "调用 setup_card_list_scene_bg_regs 设置 BG 控制寄存器, "
        "然后 reset_card_list_scroll_offset 归零列表滚动偏移. "
        "读 gPrng+0x204 场景调度字, 用掩码 0xffffc03f 清除旧状态域并写入 0x1c0 (0xe0<<1) 作为下一状态编码. "
        "与 08108d70 (写 0x100) 为同族变体, 唯一区别是目标状态值不同. 由 enter_deck_edit_page 调用. 返回 1."),
    ("FUN_08108d70", "init_card_list_scene_bg_for_deck_edit",
        "deck_edit 卡牌列表场景初始化时设置 BG 寄存器与滚动偏移的变体函数. "
        "依次调用 setup_card_list_scene_bg_regs 配置 BG 硬件寄存器, "
        "然后 reset_card_list_scroll_offset 归零滚动, "
        "最后向 gPrng+0x204 写入 0x100 (0x80<<1) 作为下一场景状态编码, 返回 1. "
        "与 08108eb8 结构完全同构, 唯一区别是写入的状态目标值不同 (0x100 vs 0x1c0). 由 enter_deck_edit_page 调用."),
    ("FUN_08108fd4", "return_one_card_info_stub",
        "card_info 显示页面专用空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由 enter_deck_edit_page (0x08108ac0) 唯一调用, "
        "在 deck_edit 状态机中作为 card_info 某分支的无操作处理器占位, 返回 1 表示已处理/继续. "
        "地址紧邻 FUN_08108fd8 (tick_card_info_display_frame), 构成占位+实体对."),
    ("FUN_08108fd8", "tick_card_info_display_frame",
        "card_info 子页面的每帧驱动函数. 由 enter_deck_edit_page 注册为 card_info 分支帧处理器. "
        "调用 tick_card_list_scene_frame 推进场景时序, render_card_list_oam_entries 刷新 OAM, "
        "return_one_scene_card_list 统一帧结束. "
        "若 tick 返回非零则调用 return_one_card_list_stub/init_card_list_display_and_objs/"
        "reinit_deck_slots_from_card_stats, 清零 [0x0202a4d0+0x0], "
        "写 gPrng+0x204 OR 0x180 (0xc0<<1) 返回主列表. 返回 0=展示中, 1=完成退出."),
    ("FUN_08109034", "return_one_card_list_main_stub",
        "card_list 主场景专用空操作占位函数. 函数体仅 movs r0,#1; bx lr. "
        "由三个 card_list/deck_edit/banlist 场景帧调度器调用 (FUN_081085d0/FUN_08108b38/FUN_0810ad98), "
        "与 return_one_card_list_scene_stub (0x08106eb4) 共享完全相同的 caller 集合但地址不同. "
        "在对应场景的某一帧处理分支中作为无需特殊处理返回 1 的占位."),
    ("FUN_08108b38", "init_deck_edit_card_list_scene",
        "deck_edit 场景状态机的 state-0 初始化处理器, "
        "由 enter_deck_edit_page (0x08108ac0) 通过函数指针表 (ROM 0x09e60a8c[0]) 间接调用. "
        "负责零填充 EWRAM 场景上下文 (0x0202f3c0, 256 halfword), "
        "按 gPrng+0x244 的 bit0 决定是否调用 init_card_stats_display_fields 初始化卡片属性显示域, "
        "依次调用 reset_card_list_scene_state/card_list_screen_init/reset_card_list_scroll_offset "
        "完成卡牌列表场景的完整初始化序列, 注册两个无操作占位存根, "
        "清除 gPrng+0x244 的 bit1 标志, 并通过 set_channel_if_changed(6) 切换 BGM 通道. "
        "最终向 gPrng+0x204 写入 OR 0x40 将调度状态推进到 state-1 (tick_deck_edit_card_list_scene), 返回 1."),
    ("FUN_08108cdc", "tick_deck_edit_card_list_scene",
        "deck_edit 场景状态机的 state-1 帧驱动处理器, "
        "由 enter_deck_edit_page 通过函数指针表 (ROM 0x09e60a8c[1]) 间接调用, 每帧运行一次. "
        "调用 tick_card_list_scene_frame/render_card_list_oam_entries 完成帧推进与 OAM 刷新. "
        "若 tick 返回非零则读 [0x0202a4d0+0x2] 场景跳转码: "
        "==1 时重新初始化显示对象并写 gPrng+0x204 OR 0xc0 (state-3); "
        "其他非零值写 OR 0x80 (state-2). 返回 1 表示跳转完成, 0 表示继续."),

    # 2026-05-05: campaign-2 batch (topo=28/29/30/31/32/33/34/35/36/37/38/39/40/41/42)
    ("FUN_08014af0", "calc_bg_screenmap_block_offset",
        "BG screen block byte offset calculator. r0=bg_index [0..3], r1=tile_x [0..63], r2=tile_y [0..63]. "
        "Queries BGxCNT screen_size field via bg0/1/2/3_cnt_get_screen_size, then computes which "
        "screen block the (tile_x, tile_y) coordinate falls in. "
        "screen_size 0=32x32 (1 block), 1=64x32 (2 col blocks), 2=32x64 (2 row blocks), 3=64x64 (4 blocks). "
        "Returns r0 = byte offset {0, 0x800, 0x1000, 0x1800} for the target screen block. "
        "Constants: 0x800 = 1 screen block size (32x32 tiles, 2KB). "
        "Caller apply_bgdt_entry_to_bg calls this twice before write_tile_region_to_bg_screen."),
    ("FUN_08014a50", "get_bg2_char_vram_addr",
        "Reads BG2CNT register (0x0400000C) char_base_block field (bits[3:2]), "
        "returns BG2 char VRAM base address. Formula: addr = 0x06000000 + char_base_block * 0x4000. "
        "No side effects, pure compute. One of four-function sibling cluster: "
        "get_bg0/bg1/bg2/bg3_char_vram_addr. Called by copy_to_bg2_char_tiles and scene init callers."),
    ("FUN_08014c94", "copy_to_bg2_char_tiles",
        "Copies src tile data via bios_cpu_fast_set to BG2 char VRAM. "
        "Asserts src 4-byte aligned (gl_common.c:492) before calling get_bg2_char_vram_addr. "
        "r0=u32* src (4-byte aligned), r1=dst_word_offset [0..0xFFF], r2=word_count [1..0x1000]. "
        "Part of four-function sibling: copy_to_bg0/bg1/bg2/bg3_char_tiles. "
        "Constants: 0x3 = 4-byte alignment mask; BG char area max 16KB = 0x1000 words."),
    ("FUN_08014a70", "get_bg3_char_vram_addr",
        "Reads BG3CNT register (0x0400000E) char_base_block field (bits[3:2]), "
        "returns BG3 char VRAM base address. Formula: addr = 0x06000000 + char_base_block * 0x4000. "
        "No side effects, pure compute. One of four-function sibling cluster: "
        "get_bg0/bg1/bg2/bg3_char_vram_addr. Called only by copy_to_bg3_char_tiles."),
    ("FUN_08014cd4", "copy_to_bg3_char_tiles",
        "Copies src tile data via bios_cpu_fast_set to BG3 char VRAM. "
        "Asserts src 4-byte aligned (gl_common.c:497) before calling get_bg3_char_vram_addr. "
        "r0=u32* src (4-byte aligned), r1=dst_word_offset [0..0xFFF], r2=word_count [1..0x1000]. "
        "Part of four-function sibling: copy_to_bg0/bg1/bg2/bg3_char_tiles. "
        "Constants: 0x3 = 4-byte alignment mask."),
    ("FUN_08014a10", "get_bg0_char_vram_addr",
        "Reads BG0CNT register (0x04000008) char_base_block field (bits[3:2]), "
        "returns BG0 char VRAM base address. Formula: addr = 0x06000000 + char_base_block * 0x4000. "
        "Uses sp-trick to read/restore IO register without net side effect. "
        "One of four-function sibling cluster: get_bg0/bg1/bg2/bg3_char_vram_addr. "
        "Returns r0 = u32 BG0 char VRAM base [0x06000000..0x06007000, step 0x4000, CBB in [0..3]]."),
    ("FUN_08014c14", "copy_to_bg0_char_tiles",
        "Copies src tile data via bios_cpu_fast_set to BG0 char VRAM. "
        "Asserts src 4-byte aligned (gl_common.c:482) before calling get_bg0_char_vram_addr. "
        "r0=u32* src (4-byte aligned), r1=dst_word_offset [0..0xFFF], r2=word_count [1..0x1000]. "
        "Part of four-function sibling: copy_to_bg0/bg1/bg2/bg3_char_tiles. "
        "Constants: 0x3 = 4-byte alignment mask; caller apply_bgdt_entry_to_bg uses this."),
    ("FUN_08014a30", "get_bg1_char_vram_addr",
        "Reads BG1CNT register (0x0400000A) char_base_block field (bits[3:2]), "
        "returns BG1 char VRAM base address. Formula: addr = 0x06000000 + char_base_block * 0x4000. "
        "No side effects, pure compute. One of four-function sibling cluster: "
        "get_bg0/bg1/bg2/bg3_char_vram_addr. Called only by copy_to_bg1_char_tiles."),
    ("FUN_08014c54", "copy_to_bg1_char_tiles",
        "Copies src tile data via bios_cpu_fast_set to BG1 char VRAM. "
        "Asserts src 4-byte aligned (gl_common.c:487) before calling get_bg1_char_vram_addr. "
        "r0=u32* src (4-byte aligned), r1=dst_word_offset [0..0xFFF], r2=word_count [1..0x1000]. "
        "Part of four-function sibling: copy_to_bg0/bg1/bg2/bg3_char_tiles. "
        "Constants: 0x3 = 4-byte alignment mask."),
    ("FUN_080165bc", "apply_bgdt_entry_to_bg",
        "Applies one BGDT (Background Data) resource entry to target BG state struct. "
        "r0=void* bg_dst (target BG state struct with priority/palette/tile_pos fields), "
        "r1=void* bgdt_entry (contains priority/tile_rect/char_data ptr etc). "
        "Writes priority (bits[6:5]) and palette attr to bg_dst[+0x14], tile attr to bg_dst[+0x16]. "
        "Calls write_tile_region_to_bg_screen up to 3 times for screen map regions; "
        "calls calc_bg_screenmap_block_offset before each to handle cross-screen-block offsets. "
        "If entry has char tile data and bg_index valid, dispatches to copy_to_bg0/1/2/3_char_tiles. "
        "Returns fixed 0. Called by apply_gfx_resource_list on 'BGDT' (0x54444742) tag match."),
    ("FUN_0801626c", "write_palt_block_to_vram",
        "Writes PALT (palette) data block to GBA palette VRAM. "
        "r0=void* src_entry (PALT resource entry with type/x/visible/data fields), "
        "r1=void* dst_info. "
        "Checks src_entry[+0x10] signed x>=0 and src_entry[+0x18] bit31 visibility. "
        "src_entry[+0x14] bits[3:0] type: 0-3 -> BG palette 0x05000000; type 4 -> OBJ palette 0x05000200. "
        "Uses bios_cpu_fast_set to write. Returns fixed 0. "
        "Called by apply_gfx_resource_list on 'PALT' (0x544C4150) tag match. "
        "Constants: 0x05000000 = BG palette VRAM base; 0x05000200 = OBJ palette VRAM base."),
    ("FUN_08014c0c", "get_obj_tile_vram_base",
        "Returns constant 0x06010000 (OBJ/sprite tile VRAM base address). "
        "Body: ldr r0, DAT_08014c10; bx lr. Pure constant leaf. "
        "GBA OBJ tile data starts at 0x06010000 (32KB in mode 0-2). "
        "Called only by copy_to_obj_tile_vram to get the write target base."),
    ("FUN_08014e14", "copy_to_obj_tile_vram",
        "Copies src data via bios_cpu_set to OBJ tile VRAM (0x06010000). "
        "Asserts src 4-byte aligned (gl_common.c:524) before calling get_obj_tile_vram_base. "
        "r0=u32* src (4-byte aligned), r1=dst_word_offset [0..0x1FFF], r2=word_count [1..0x2000]. "
        "indeg=4, called by apply_objd_entry_to_sprite and 3 other scene renderers. "
        "Constants: gl_common.c:524 = 0x83<<2 = 0x20C; 0x06010000 = OBJ tile VRAM base."),
    ("FUN_0801695c", "apply_objd_entry_to_sprite",
        "Applies one OBJD (Object Data) resource entry to target sprite/OAM state struct. "
        "r0=void* sprite_dst, r1=void* objd_entry. "
        "Reads data_len([+0xc]) / __udivsi3 / tile_stride([+0xa]) -> row_count -> strh sprite_dst[+0x12]. "
        "Writes tile_attr bits[7:4] (palette) and bits[3:0] (mode) to sprite_dst[+0x14]. "
        "If mode==4 (4bpp indexed) and VRAM target offset valid, calls copy_to_obj_tile_vram. "
        "Returns fixed 0. Called by apply_gfx_resource_list on 'OBJD' (0x444A424F) tag match. "
        "Constants: 'OBJD' = 0x444A424F; mode 4 = 4bpp indexed tile mode."),
    ("FUN_08016a7c", "apply_gfx_resource_list",
        "Iterates a graphics resource entry list, dispatching each entry by 4-byte type tag. "
        "r0=void* list_header ([+0x0]=first entry ptr, [+0xE]=entry_count, [+0xC]=entry_stride). "
        "Supports three types: 'BGDT' (0x54444742) -> apply_bgdt_entry_to_bg; "
        "'OBJD' (0x444A424F) -> apply_objd_entry_to_sprite; 'PALT' (0x544C4150) -> write_palt_block_to_vram. "
        "Returns fixed 0 when list exhausted. indeg=13, called by 5+ scene types "
        "(scene_demo/scene_name_input/palette/demo/fs) as unified BG/OBJ/palette init entry. "
        "Constants: 0x54444742='BGDT'; 0x444A424F='OBJD'; 0x544C4150='PALT'."),

    # 2026-05-05: campaign-1 batch (topo=1/2/8/10/11/13/14/15/16/17/18/19/20/21/25)
    ("FUN_08015194", "fill_gl_palram_buf_0xf0",
        "由 init_gl_palette_slot_flags (FUN_08015160) 在 GL 状态初始化链末尾调用, "
        "负责将调色板 RAM 子区域全部填充为 0xf0 (halfword fill 模式). "
        "实现: sp 作为 src 地址存放填充值 0xf0; bios_cpu_set fill 写入 EWRAM 0x02023490 "
        "起始 0x100 halfword (0x200 字节), 确保调色板条目处于已知默认值状态(非零). "
        "Constants: 0x05000100 = bios_cpu_set 控制字 (bit24=1 fill, len=0x100 halfwords=0x200 bytes)."),
    ("FUN_08015160", "init_gl_palette_slot_flags",
        "被 gl_state_init/name_input_page_tick/demo_shuen_state_machine 等 7 个场景共同调用, "
        "负责将 GL 调色板槽位标记区域 (EWRAM 0x02023490+0x880, 共 32 字节) 全部置为 0xFF, "
        "并将相邻控制字节 (offset 0x8A0) 清零, 最后调用 fill_gl_palram_buf_0xf0 填充调色板 RAM 子区. "
        "触发时机: 每次 GL 层重新初始化或场景切换需要复位调色板槽位状态时调用."),
    ("FUN_080146cc", "update_brightness_fade_flag",
        "由 gl_set_brightness 在设置亮度目标值后调用, 根据亮度状态结构体 (EWRAM 0x02023480) "
        "中的当前值 (offset +0) 和目标值 (offset +1) 符号确定 fade 状态标记并写回 offset +8. "
        "若两个值均 >= 0 则将 +8 的低 2 位清零并置 bit1 (fade 激活); "
        "若任一值 < 0 则置 +8 为 3 (idle/disabled). "
        "副作用: [0x02023480+8] 写入新 flag 字节."),
    ("FUN_08013510", "reset_display_and_gl_state",
        "由 play_ui_effect_3a 及 FUN_08014398 在需要完全重置显示层时调用. "
        "执行顺序: (1) bios_cpu_set 以 0 fill gDemoState (0x02029ec0, 0x94 字节); "
        "(2) 向 DISPCNT 写 0x40 (OBJ 1D 映射, 屏幕显示关闭); "
        "(3) 依次设置 BG0CNT/BG1CNT/BG2CNT/BG3CNT 为固定初始值; "
        "(4) gl_set_brightness (mode=0x3f, bright=-16) 将亮度推向最暗; "
        "(5) gl_state_init 重置 GL 状态结构体; "
        "(6) gl_clear_frame_callbacks 清空帧回调队列. "
        "Constants: DISPCNT=0x0040 / BG0CNT=0x1D00 / BG1CNT=0x1E01 / BG2CNT=0x1F02 / BG3CNT=0x9B0B."),
    ("FUN_08015fc8", "zero_struct_36bytes",
        "被 scene_demo/scene_name_input 初始化器等 13 个调用点使用, "
        "将 r0 传入的指针所指向的 36 字节结构体清零. "
        "实现: 利用栈临时存储 0 (halfword), 以 bios_cpu_set halfword fill 模式将目标地址起 "
        "0x12 个 halfword (36 字节) 填充为 0. 返回 r0=0 (固定). "
        "Constants: 0x01000012 = bios_cpu_set 控制字 (bit24=1 fill, halfword, len=0x12=36 bytes)."),
    ("FUN_08014bcc", "get_bg2_screen_vram_addr",
        "由 assert-wrapper copy_to_bg2_screen_map 在执行 BG2 screen map 拷贝前调用, "
        "读取 BG2CNT 寄存器 (0x0400000C) 的 screen_base_block 字段 (bits [12:8]), "
        "计算并返回 BG2 screen map 在 VRAM 中的实际起始地址. "
        "公式: addr = 0x06000000 + screen_base_block * 0x800. 无副作用, 纯计算返回. "
        "与 get_bg0/bg1/bg3_screen_vram_addr 构成四函数 sibling 簇."),
    ("FUN_08014d94", "copy_to_bg2_screen_map",
        "由 dispatch_bg_screen_map_write 在 bg_index=2 时调用, "
        "将 src 数据经 bios_cpu_set 拷贝到 BG2 的 screen map VRAM 地址. "
        "调用前先检查 src 指针 4 字节对齐, 违规则触发 gl_common.c:513 处的 suppress_assert_report. "
        "对齐通过后: 调 get_bg2_screen_vram_addr 查询 BG2CNT 获得 screen 基址, "
        "加上 dst_offset, 以 bios_cpu_set copy 写入."),
    ("FUN_08014bec", "get_bg3_screen_vram_addr",
        "由 assert-wrapper copy_to_bg3_screen_map 在执行 BG3 screen map 拷贝前调用, "
        "读取 BG3CNT 寄存器 (0x0400000E) 的 screen_base_block 字段 (bits [12:8]), "
        "计算并返回 BG3 screen map 在 VRAM 中的实际起始地址. "
        "公式: addr = 0x06000000 + screen_base_block * 0x800. 无副作用, 纯计算返回. "
        "与 get_bg0/bg1/bg2_screen_vram_addr 构成四函数 sibling 簇."),
    ("FUN_08014dd4", "copy_to_bg3_screen_map",
        "由 dispatch_bg_screen_map_write 在 bg_index=3 时调用, "
        "将 src 数据经 bios_cpu_set 拷贝到 BG3 的 screen map VRAM 地址. "
        "调用前先检查 src 指针 4 字节对齐, 违规则触发 gl_common.c:518 处的 suppress_assert_report. "
        "对齐通过后: 调 get_bg3_screen_vram_addr 查询 BG3CNT 获得 screen 基址, "
        "加上 dst_offset, 以 bios_cpu_set copy 写入."),
    ("FUN_08014b8c", "get_bg0_screen_vram_addr",
        "由 assert-wrapper copy_to_bg0_screen_map 在执行 BG0 screen map 拷贝前调用, "
        "读取 BG0CNT 寄存器 (0x04000008) 的 screen_base_block 字段 (bits [12:8]), "
        "计算并返回 BG0 screen map 在 VRAM 中的实际起始地址. "
        "公式: addr = 0x06000000 + screen_base_block * 0x800. 无副作用, 纯计算返回. "
        "与 get_bg1/bg2/bg3_screen_vram_addr 构成四函数 sibling 簇."),
    ("FUN_08014d14", "copy_to_bg0_screen_map",
        "由 dispatch_bg_screen_map_write 在 bg_index=0 时调用, "
        "将 src 数据经 bios_cpu_set 拷贝到 BG0 的 screen map VRAM 地址. "
        "调用前先以 assert 检查 src 指针 4 字节对齐, 违规则触发 gl_common.c:503 处的 suppress_assert_report. "
        "对齐通过后: 调 get_bg0_screen_vram_addr 查询 BG0CNT 获得 screen 基址, "
        "加上 dst_offset, 以 bios_cpu_set copy 模式写入."),
    ("FUN_08014bac", "get_bg1_screen_vram_addr",
        "由 assert-wrapper copy_to_bg1_screen_map 在执行 BG1 screen map 拷贝前调用, "
        "读取 BG1CNT 寄存器 (0x0400000A) 的 screen_base_block 字段 (bits [12:8]), "
        "计算并返回 BG1 screen map 在 VRAM 中的实际起始地址. "
        "公式: addr = 0x06000000 + screen_base_block * 0x800. 无副作用, 纯计算返回. "
        "与 get_bg0/bg2/bg3_screen_vram_addr 构成四函数 sibling 簇."),
    ("FUN_08014d54", "copy_to_bg1_screen_map",
        "由 dispatch_bg_screen_map_write 在 bg_index=1 时调用, "
        "将 src 数据经 bios_cpu_set 拷贝到 BG1 的 screen map VRAM 地址. "
        "调用前先检查 src 指针 4 字节对齐, 违规则触发 gl_common.c:508 处的 suppress_assert_report. "
        "对齐通过后: 调 get_bg1_screen_vram_addr 查询 BG1CNT 获得 screen 基址, "
        "加上 dst_offset, 以 bios_cpu_set copy 写入."),
    ("FUN_080162dc", "dispatch_bg_screen_map_write",
        "由 write_tile_region_to_bg_screen 调用, 根据 r2 (dst) 的高 20 位是否置位来选择两种写入路径: "
        "(A) r2 高位非零 -- r2 即为原始 VRAM 地址, 直接 bios_cpu_set (src=r0, dst=r2, len=r3); "
        "(B) r2 高位全零 -- r2 为偏移量, r1 为 bg_index [0..3], "
        "分派到 copy_to_bg0/1/2/3_screen_map. "
        "Constants: 0xfff00000 = 高 12 位掩码, 用于判断 r2 是原始地址还是 bg_index+offset."),
    ("FUN_08016344", "write_tile_region_to_bg_screen",
        "由 FUN_080165bc 调用, 将 tileset 描述符 (r6 struct) 中指定的 tile 区域逐行写入 "
        "目标 BG (BG2 或 BG3) 的 screen map. "
        "处理流程: (1) 读取 r6[0xc] (tile 数量/data ptr), 若为 0 则直接返回; "
        "(2) 读 r6[0x15] bit1 选择路径 (普通 tile 序列或含 X 偏移的特殊格式); "
        "(3) 调 bg2_cnt_get_screen_size/bg3_cnt_get_screen_size 确定 screen 宽度; "
        "(4) 按 r6[0x16] 的 width/height 字段计算每行写入范围, "
        "循环调用 dispatch_bg_screen_map_write 写入各行. "
        "BG2/BG3 由 r6[0x14] bits[3:0] 选择. "
        "Confidence: med (r6 struct field layout +0x14/+0x15/+0x16 awaits runtime verify)."),

    # 2026-05-05: campaign-3 batch (topo=43/44/45/55/56/59x3/60/61/62/63/64/65/66)
    # demo loader (exodia/exodia*.LZ5bg assets) + NitroSDK G2D library wrappers
    ("FUN_08013578", "setup_demo_sprite_entry",
        "Called by dispatch_demo_sprite_setup_by_mode (mode=0). "
        "Initialises OAM attr0/attr1/attr2 fields for one demo sprite slot, "
        "then calls apply_gfx_resource_list to commit. "
        "Detects JP BIOS version byte [0x080000ae]>>8 == 0x4a and adjusts tile offset +0x38. "
        "r0=sprite_slot[0..3], r1=x_pos[0..127], r2=palette_idx[0..15], r3=ptr gDemoState field. "
        "Constants: OAM_BIOS_JP_MASK=0x4a / ATTR1_X_MASK=0x7f / ATTR0_PAL_MASK=0xf."),
    ("FUN_08013680", "setup_demo_sprite_entry_alt",
        "Called by dispatch_demo_sprite_setup_by_mode (mode=1 or mode=2). "
        "Structure mirrors setup_demo_sprite_entry (0x08013578) but omits JP BIOS detection branch. "
        "Initialises OAM attr0/attr1/attr2 and calls apply_gfx_resource_list. "
        "Resource list template: 0x09e396c8 (demo/exodia/exodia01_obj.LZncer). "
        "r0=sprite_slot[0..3], r1=x_pos[0..127], r2=palette_idx[0..15], r3=ptr gDemoState field. "
        "Constants: ATTR1_X_MASK=0x7f / ATTR0_PAL_MASK=0xf / ATTR2_MASK=0xffffc07f."),
    ("FUN_08013740", "dispatch_demo_sprite_setup_by_mode",
        "Dispatcher called by scene_demo state machine (FUN_08013bd4) for sprite init. "
        "mode=0 -> setup_demo_sprite_entry (0x08013578); "
        "mode=1 or mode=2 -> setup_demo_sprite_entry_alt (0x08013680); "
        "other mode: epilogue only. "
        "Epilogue unconditionally writes 0 to DISPCNT (0x04000000) via 0xa0<<0x13. "
        "r0=mode[0..2], r1=x_pos, r2=palette_idx, r3=ptr. "
        "Constants: DISPCNT=0x04000000."),
    ("FUN_0801379c", "load_demo_bg_gfx_set0",
        "Called by scene_demo state machine (FUN_08013bd4, case=0). "
        "Loads first BG graphics group: fs_load(r0='demo/exodia/exodia00_1.LZ5bg'), "
        "then two rounds of zero_struct_36bytes + apply_gfx_resource_list for BG0 and BG1. "
        "First apply: priority=3; second apply: tile offset 0xa00 + attr1 bit7 set. "
        "Epilogue strh to DISPCNT (0xa0<<0x13 = 0x04000000). "
        "Constants: BG0_PRIORITY=0x3 / OBJ_VRAM_OFFSET=0xa00 / DISPCNT=0x04000000."),
    ("FUN_08013864", "load_demo_bg_gfx_set1",
        "Called by scene_demo state machine (FUN_08013bd4, case=5). "
        "Symmetric to load_demo_bg_gfx_set0 (0x0801379c); loads second BG group: "
        "fs_load(r0='demo/exodia/exodia01_BG.LZ5bg'), two zero_struct_36bytes + two apply_gfx_resource_list, "
        "plus a third apply for extended resource descriptor DAT_0801393c=0x141e0000. "
        "Difference: second apply uses tile base 0x22 instead of 0xa0<<4. "
        "Epilogue strh to DISPCNT. "
        "Constants: BG_TILE_BASE2=0x22 / DISPCNT=0x04000000 / EXTRA_RESOURCE=0x141e0000."),
    ("FUN_080e88cc", "advance_anim_ctrl_frame",
        "NitroSDK nnsys/g2d/g2d_Animation.c -- animation controller frame advance. "
        "Called by step_anim_ctrl_by_frames (0x080e8d70). "
        "Asserts pAnimCtrl != NULL and pAnimCtrl->pCurrent != NULL (suppress lines 0xf8/0x4d). "
        "Reads [pAnimCtrl+0x14]/[pAnimCtrl+0x18] for sequence type (LOOP=2 / REVERSE=4). "
        "Toggles [pAnimCtrl+0x4] active flag, updates [pAnimCtrl+0x0] frame position "
        "via set_anim_ctrl_position_fwd (FUN_080e90fc). "
        "r0=ptr pAnimCtrl (NNS_G2dAnimController). "
        "Constants: ANIM_TYPE_LOOP=2 / ANIM_TYPE_REVERSE=4 / ANIM_CTRL_ACTIVE_OFFSET=0x4."),
    ("FUN_080e8d70", "step_anim_ctrl_by_frames",
        "NitroSDK nnsys/g2d/g2d_Animation.c -- advance animation controller by N frames. "
        "Called by set_anim_ctrl_position_fwd (0x080e90fc) and FUN_080e957c. "
        "Asserts pAnimCtrl != NULL (suppress line 0x16d), pCurrent != NULL (line 0xb7), "
        "frames >= 0 (line 0x16f). "
        "If [pAnimCtrl+0x8]==1 (active): computes frames * pCurrent->speed (__muldi3) "
        "+ 0x800 rounding, adds to [pAnimCtrl+0xc] (position accumulator). "
        "Returns new [pAnimCtrl+0xc] or 0 if inactive. "
        "r0=ptr pAnimCtrl, r1=s32 frames[0..MAX_INT]. "
        "Constants: ANIM_SPEED_SHIFT=12 / ROUNDING_OFFSET=0x800 / ACTIVE_FLAG=1."),
    ("FUN_080e90fc", "set_anim_ctrl_position_fwd",
        "NitroSDK nnsys/g2d/g2d_Animation.c -- reset animation controller frame pointer to sequence start. "
        "Called by advance_anim_ctrl_frame (0x080e88cc), bind_anim_ctrl_callback (0x080e91a8), FUN_080e9500. "
        "Asserts pAnimCtrl != NULL. Reads [pAnimCtrl+0x10] speed: if speed>0 computes forward base "
        "= pContent + count*8; else base = pContent + totalFrames*8 - 8. "
        "Writes [pAnimCtrl+0x0]=base, [pAnimCtrl+0xc]=0, then calls step_anim_ctrl_by_frames(pAnimCtrl,0). "
        "r0=ptr pAnimCtrl (NNS_G2dAnimController). "
        "Constants: FRAME_SIZE=8 / POSITION_INIT=0."),
    ("FUN_080e91a8", "bind_anim_ctrl_callback",
        "NitroSDK nnsys/g2d/g2d_Animation.c -- bind animation sequence to controller and reset position. "
        "Called by FUN_080e94a4. "
        "Asserts pAnimCtrl != NULL (suppress line 0x260) and pCallBack != NULL. "
        "Stores pCallBack to [pAnimCtrl+0x18] (pCurrent field), "
        "then calls set_anim_ctrl_position_fwd (FUN_080e90fc) to reset frame pointer. "
        "Equivalent to NNS_G2dSetAnimCtrlCurrentAnimSequence. "
        "r0=ptr pAnimCtrl, r1=ptr pCallBack (NNS_G2dAnimSequence). "
        "Constants: ANIM_CTRL_PCURRENT_OFFSET=0x18."),
    ("FUN_080e8bc8", "get_anim_ctrl_current_frame_ptr",
        "NitroSDK nnsys/g2d/g2d_Animation.c -- pure getter returning pAnimCtrl->pCurrent->pContent. "
        "Called by FUN_080e9350. "
        "Asserts pAnimCtrl != NULL (suppress line 0x12f), pCurrent != NULL (line 0x130), "
        "pContent != NULL (line 0x131). "
        "Returns [[pAnimCtrl+0]+0] = pCurrent->pContent via two-level pointer deref. No writes. "
        "r0=ptr pAnimCtrl -> ret ptr (current frame content). "
        "Constants: ANIM_CTRL_PCURRENT_OFFSET=0 / PCURRENT_PCONTENT_OFFSET=0."),
    ("FUN_080eb8a8", "set_nob_cell_position",
        "NitroSDK nnsys/g2d/g2d_NOB_load.c -- set X/Y position of a NOB cell entry. "
        "Called by FUN_080e9350. "
        "Checks [pCell+0]==1 (CELL_TYPE_ACTIVE); if ok: sets [pCell+0x12] bit3 (position valid flag), "
        "writes strh x_pos to [pCell+0xc], strh y_pos to [pCell+0xe]. "
        "Type mismatch triggers suppress_assert_report (line 0x27). "
        "r0=ptr pCell (NNS_G2dNOBCell), r1=u16 x_pos[0..65535], r2=u16 y_pos[0..65535]. "
        "Constants: CELL_TYPE_ACTIVE=1 / CELL_FLAG_POS_SET=0x8 / CELL_X_OFFSET=0xc / CELL_Y_OFFSET=0xe."),
    ("FUN_080eb8e4", "set_nob_cell_frame_idx",
        "NitroSDK nnsys/g2d/g2d_NOB_load.c -- set frame index of a NOB cell entry. "
        "Called by FUN_080e9350. "
        "Checks [pCell+0]==1 (CELL_TYPE_ACTIVE); if ok: sets [pCell+0x12] bit2 (frame-idx valid flag), "
        "writes strh frame_idx to [pCell+0x10]. "
        "Type mismatch triggers suppress_assert_report (line 0x45). "
        "r0=ptr pCell (NNS_G2dNOBCell), r1=u16 frame_idx[0..65535]. "
        "Constants: CELL_TYPE_ACTIVE=1 / CELL_FLAG_FRAME_SET=0x4 / CELL_FRAME_IDX_OFFSET=0x10."),
    ("FUN_080eb978", "init_srt_ctrl_state",
        "NitroSDK nnsys/g2d/g2d_SRTControl.c -- initialise SRT controller scale/rotate/translate fields. "
        "Called by bind_srt_ctrl_data (0x080eb94c). "
        "Asserts pCtrl != NULL (suppress line 0x8f) and type==NNS_G2D_SRTCONTROLTYPE_SRT==1 (line 0x90). "
        "Clears [pCtrl+0] halfword, calls bios_cpu_set fill-0 (control word 0x0100000c) to zero "
        "[pCtrl+4..0xf] (12 bytes), then writes [pCtrl+4]=0x1000 and [pCtrl+8]=0x1000 (scale=1.0 in 4.12). "
        "r0=ptr pCtrl (NNS_G2dSRTControl). "
        "Constants: SRT_SCALE_INIT=0x1000 / SRT_CLEAR_LEN=0xc / NNS_G2D_SRTCONTROLTYPE_SRT=1."),
    ("FUN_080eb94c", "bind_srt_ctrl_data",
        "NitroSDK nnsys/g2d/g2d_SRTControl.c -- bind data pointer to SRT controller and initialise state. "
        "Called by FUN_080e9350 and FUN_080e9400. "
        "Asserts pCtrl != NULL (suppress line 0x77). "
        "Stores pData to [pCtrl+0x0] (data field), then calls init_srt_ctrl_state (FUN_080eb978) "
        "to set scale=0x1000, clear rotate/translate. Equivalent to NNS_G2dInitSRTControl. "
        "r0=ptr pCtrl (NNS_G2dSRTControl), r1=ptr pData. "
        "Constants: SRT_CTRL_DATA_OFFSET=0."),
    ("FUN_080eb7f0", "get_nob_cell_data_ptr",
        "NitroSDK nnsys/g2d/g2d_NOB_load.c -- return pointer to cell entry by slot index. "
        "Called by FUN_080e9350 and FUN_080eb838. "
        "Asserts pCellData != NULL (suppress line 0x51). "
        "Checks slot_index (u16) < pCellData->count (halfword at [pCellData+0]); returns NULL if out of range. "
        "Format flag [pCellData+0x2] bit0: 0 -> stride=8 bytes (lsls slot,#3); 1 -> stride=16 bytes (lsls slot,#4). "
        "Returns [pCellData+0x4] + index*stride. "
        "r0=ptr pCellData (NNS_G2dCellData), r1=u16 slot_index[0..count-1] -> ret ptr (cell entry or NULL). "
        "Constants: CELL_STRIDE_8B=8 / CELL_STRIDE_16B=16 / COUNT_OFFSET=0 / FORMAT_FLAG_OFFSET=2 / DATA_BASE_OFFSET=4."),

    # 2026-05-06: campaign-4 batch (topo=67/68/69/70/71/72/73/74/75/76/77/78/79/80/81)
    ("FUN_080eb918", "set_srt_ctrl_translate",
        "nnsys/g2d/g2d_SRTControl.c -- SRT controller translate write. "
        "Called by apply_cell_anim_frame (0x080e9350) when frame type==6. "
        "Asserts [pCtrl+0x0]==1 (SRT_STATE_ACTIVE, line 0x62); "
        "writes r1 (tx) to [pCtrl+0x4], r2 (ty) to [pCtrl+0x8], "
        "sets [pCtrl+0x12] bit1 (translate-dirty flag). "
        "r0=NNS_G2dSRTControl* pCtrl [active], r1=s16 tx, r2=s16 ty. "
        "Constants: SRT_STATE_ACTIVE=1 / SRT_TRANSLATE_FLAG=0x2 / "
        "SRT_TRANSLATE_X_OFFSET=0x4 / SRT_TRANSLATE_Y_OFFSET=0x8 / SRT_FLAGS_OFFSET=0x12."),
    ("FUN_080e9350", "apply_cell_anim_frame",
        "nnsys/g2d/g2d_CellAnimation.c -- apply current animation frame to CellAnimation controller. "
        "Called by init_cell_anim_with_seq (0x080e94a4) and update paths. "
        "Asserts pCellAnim != NULL (line 0x16), pCellAnim->pCellDataBank != NULL (line 0x17). "
        "Reads current frame ptr via get_anim_ctrl_current_frame_ptr, "
        "calls get_nob_cell_data_ptr -> stores result at [pCellAnim+0x2C]; "
        "calls bind_srt_ctrl_data to init SRT sub-controller at [pCellAnim+0x38]; "
        "dispatch on frame transform type (0/2/6): "
        "type 2 -> set_nob_cell_position; type 6 -> set_srt_ctrl_translate. "
        "r0=NNS_G2dCellAnimation* pCellAnim [non-NULL]. "
        "Constants: CELL_ANIM_CELL_DATA_BANK_OFFSET=0x30 / CELL_ANIM_CURRENT_CELL_OFFSET=0x2C / "
        "CELL_ANIM_SRT_CTRL_OFFSET=0x38."),
    ("FUN_080e94a4", "init_cell_anim_with_seq",
        "nnsys/g2d/g2d_CellAnimation.c -- bind animation sequence to CellAnimation and apply first frame. "
        "Called by bind_cell_anim_to_bank (0x080e9400). "
        "Asserts pCellAnim != NULL (line 0xE5), pAnimSeq != NULL (line 0xE6), "
        "pAnimSeq type == NNS_G2D_ANIMATIONTYPE_CELL (line 0xE8). "
        "Calls bind_anim_ctrl_callback to bind sequence, then apply_cell_anim_frame to write first frame. "
        "Equivalent to NNS_G2dSetCellAnimationSequence. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=NNS_G2dAnimSequence* pAnimSeq. "
        "Constants: ANIM_TYPE_CELL=1."),
    ("FUN_080e90cc", "zero_anim_ctrl_fields",
        "nnsys/g2d/g2d_Animation.c -- zero animation controller sub-struct fields. "
        "Called by init_anim_ctrl (0x080e905c) and FUN_080e90a0. "
        "Asserts pAnimCtrl != NULL (line 0x225=549). "
        "Writes 0 to [pAnimCtrl+0x0], [+0x4], [+0x8] (word each), "
        "and halfword 0 to [pAnimCtrl+0xC]. "
        "r0=NNS_G2dAnimController* pAnimCtrl (caller passes pAnim+0x1C sub-struct). "
        "Constants: ANIM_CTRL_SUB_STRUCT_OFFSET=0x1C."),
    ("FUN_080e905c", "init_anim_ctrl",
        "nnsys/g2d/g2d_Animation.c -- full NNS_G2dAnimController initialisation. "
        "Called by bind_cell_anim_to_bank (0x080e9400). "
        "Asserts pAnimCtrl != NULL (line 0x1F7=503). "
        "Calls zero_anim_ctrl_fields(pAnimCtrl+0x1C), then sets main struct: "
        "[+0x0]=0, [+0x4]=0, [+0x8]=1, [+0xC]=0, [+0x10]=0x1000 (speed), [+0x14]=0, [+0x18]=0. "
        "Equivalent to NNS_G2dInitAnimCtrl. "
        "r0=NNS_G2dAnimController* pAnimCtrl [non-NULL]. "
        "Constants: ANIM_CTRL_DEFAULT_SPEED=0x1000 / ANIM_CTRL_DEFAULT_LOOP_COUNT=1."),
    ("FUN_080e9400", "bind_cell_anim_to_bank",
        "nnsys/g2d/g2d_CellAnimation.c -- main CellAnimation init entry. "
        "Called by game layer 0x08015d30 (fs tag). "
        "Asserts pCellAnim/pCellDataBank/pAnimSeq non-NULL (line 0x87/0x88/0x89 and 0x64/0x65/0x66). "
        "Calls bind_srt_ctrl_data(pCellAnim+0x38), init_anim_ctrl(pCellAnim), "
        "init_cell_anim_with_seq(pCellAnim, pAnimSeq). "
        "Writes pCellDataBank to [pCellAnim+0x30], -1 to [pCellAnim+0x34] (frame counter). "
        "Equivalent to NNS_G2dInitCellAnimation. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=NNS_G2dCellDataBank* pCellDataBank, "
        "r2=NNS_G2dAnimSequence* pAnimSeq. "
        "Constants: CELL_ANIM_SRT_CTRL_OFFSET=0x38 / CELL_ANIM_CELL_DATA_BANK_OFFSET=0x30 / "
        "CELL_ANIM_FRAME_COUNTER_OFFSET=0x34."),
    ("FUN_08015ac4", "alloc_cell_anim_slot",
        "GL/IG2D_Main.c -- allocate next free CellAnmBank slot. "
        "Called by 0x08015d30 (fs tag). "
        "Asserts [0x03000BF8] <= 0x3F (UsedCellAnm < NELEMS(CellAnmBank), line 0x127=295). "
        "Computes slot addr = CellAnmBank + counter*0x54, increments counter, returns ptr. "
        "r0: no input (entry ldr r4,DAT overwrites r0). "
        "Returns NNS_G2dCellAnimation* (allocated slot). "
        "Side effect: [0x03000BF8] += 1. "
        "Constants: IG2D_CELL_ANM_MAX=0x40 / CELL_ANM_ENTRY_SIZE=0x54 / "
        "UsedCellAnm=[0x03000BF8] / CellAnmBank=0x02027D40."),
    ("FUN_080eae5c", "check_vram_location_slot",
        "nnsys/g2d/g2d_Image.c -- check if VRAM location slot[type] is set. "
        "Called by set_img_proxy_vram_location (0x080e9acc) and 2 other image-proxy paths. "
        "Asserts pVramLocation != NULL (line 0x35=53), type <= 2 (line 0x36=54). "
        "Reads pVramLocation->slot[type] = [pVramLocation + type*4]; "
        "returns 1 if non-zero (slot set), 0 if zero (not set). "
        "Uses mvns+rsbs+orrs+lsrs 0x1F idiom for non-zero boolean. "
        "r0=NNS_G2dImageProxy* pVramLocation [non-NULL], r1=u32 type [0..2]. "
        "Constants: NNS_G2D_VRAM_TYPE_3DMAIN=0 / NNS_G2D_VRAM_TYPE_2DMAIN=1 / "
        "NNS_G2D_VRAM_TYPE_2DSUB=2."),
    ("FUN_080e9acc", "set_img_proxy_vram_location",
        "nnsys/g2d/g2d_Image.c -- write VRAM base address into image proxy slot. "
        "Called by load_img_proxy_to_vram (0x080e9de8) and 3 other image load paths. "
        "Asserts pImgProxy != NULL (line 0xC8=200), type <= 2 (line 0x189=393 and 0x20=32), "
        "pImgProxy != NULL (line 0x1F=31). "
        "Calls check_vram_location_slot, then writes baseAddr to [pImgProxy + type*4]. "
        "r0=NNS_G2dImageProxy* pImgProxy [non-NULL], r1=u32 type [0..2], r2=u32 baseAddr. "
        "Constants: NNS_G2D_VRAM_TYPE_MAX=3 / IMG_PROXY_SLOT_STRIDE=4."),
    ("FUN_080e99f0", "check_vram_size_for_type",
        "nnsys/g2d/g2d_Image.c -- validate VRAM offset against type capacity. "
        "Called by load_img_proxy_to_vram (0x080e9de8). "
        "type==0 or 1 -> max 0x300000 (0xC0<<14, 2D MAIN/SUB OBJ VRAM 192KB); "
        "type==2 -> max 0x200000 (0x80<<14, 3D VRAM 128KB); "
        "other type -> returns 0. "
        "Applies -0x10 bias to offset before comparison; returns 1 (valid) or 0 (out of range). "
        "r0=u32 type [0..2], r1=u32 offset (bytes). "
        "Constants: VRAM_2D_SIZE=0x300000 (0xC0<<14) / VRAM_3D_SIZE=0x200000 (0x80<<14)."),
    ("FUN_080e9a18", "check_img_mapping_type",
        "nnsys/g2d/g2d_Image.c -- validate image mapping type compatibility with VRAM target. "
        "Called by load_img_proxy_to_vram (0x080e9de8) and FUN_080ea0a0. "
        "type==0 (3D_MAIN) -> returns 1 immediately (no mapping check). "
        "Otherwise reads [pSrcData+0x8] (mappingType), compares against predefined constants "
        "(0x00100010=NNS_G2D_1D_32K / 0x00200010 / 0x00300010 etc.) with capacity bounds check. "
        "Returns 1 (compatible) or 0 (incompatible). "
        "Equivalent to NNS_G2D internal IsValid1DMappingType_. "
        "r0=NNS_G2dCharacterData* pSrcData, r1=u32 type [0..2]."),
    ("FUN_080e9de8", "load_img_proxy_to_vram",
        "nnsys/g2d/g2d_Image.c -- load character image to OBJ tile VRAM and update image proxy. "
        "Called by game layer 0x08015d30 (fs tag). "
        "Asserts pImgProxy != NULL (line 0x221), pSrcData != NULL (line 0x222). "
        "Validates via check_vram_size_for_type + check_img_mapping_type; "
        "dispatches 32-way switch on [pSrcData+0x2] (mapType) to internal enum 0-5; "
        "calls copy_to_obj_tile_vram to write pixel data, "
        "then set_img_proxy_vram_location to update proxy. "
        "r0=NNS_G2dImageProxy* pImgProxy, r1=u32 dst_word_offset [0..0x1FFF] (saved to r8), "
        "r2=NNS_G2dCharacterData* pSrcData, r3=u32 type [0..2]. "
        "Constants: CHAR_FMT_CHAR=NNS_G2D_CHARACTER_FMT_CHAR / MAP_TYPE_COUNT=32."),
    ("FUN_0801563c", "alloc_nce_buff_slot",
        "GL/IG2D_Main.c -- allocate next free NceBuff (NCE = NNS Cell Entry) slot. "
        "Called by 0x08015b10 (fs tag). "
        "Asserts [0x03000BFC] <= 1 (UsedNceBuff < IG2D_LOAD_ANM_MAX=2, line 0x2F=47). "
        "Computes slot addr = [0x03000C08] + count*(1<<12), increments counter, returns ptr. "
        "r0: no input (entry ldr r4,DAT overwrites r0). "
        "Returns void* (4KB-aligned NceBuff slot). "
        "Side effect: [0x03000BFC] += 1. "
        "Constants: IG2D_LOAD_ANM_MAX=2 / NCE_BUFF_SLOT_SIZE=0x1000 / "
        "UsedNceBuff=[0x03000BFC] / NceBuffBase=[0x03000C08]."),
    ("FUN_08015b04", "invoke_fs_load",
        "GL/IG2D_Main.c area -- thin fs_load wrapper. "
        "Called by 4 G2D resource load paths (FUN_08015b10/b70/bd0/c30, all fs-tagged). "
        "Body: push lr / bl fs_load / pop r1 / bx r1 -- passes all args through, "
        "returns fs_load return value. "
        "r0..r3: forwarded to fs_load unchanged. "
        "Returns: fs_load return value."),
    ("FUN_080eaf28", "relocate_bin_block_ptrs",
        "nnsys/g2d/g2d_Load.c -- relocate internal pointers in a binary block. "
        "Called by FUN_080eb718 (NNS G2D resource file loader) after loading. "
        "Reads [pBlock+0x4] (relative offset table base) + pBlock -> absBase; "
        "writes absBase back to [pBlock+0x4]; "
        "loops i=0..count-1 ([pBlock+0x0]): [absBase+i*4] += pBlock (relative->absolute). "
        "Standard NNS G2D binary block pointer patch-up step. "
        "r0=NNS_G2dBinaryBlockHeader* pBlock. "
        "Loop counter is u16 (lsls/lsrs 0x10 truncation)."),
    # --- campaign-5 batch (batch15-5) ---
    ("FUN_080eaec4", "find_bin_block_by_type",
        "nnsys/g2d/g2d_Load.c line 10 (pBinFileHeader). "
        "Search NNS G2D binary file header for a block by type tag. "
        "r0=NNS_G2dBinaryBlockHeader* pBinFileHeader (non-NULL assert), "
        "r1=u32 type_tag (4-byte magic e.g. 'NANR'/'PLTT'). "
        "Walks block list at [pBinFileHeader+0xc]; compares [block+0x0]==type_tag; "
        "returns block ptr if found, NULL if not found. "
        "indeg=7 (used by g2d_NAN_load / g2d_NCL_load / g2d_NOB_load loaders)."),
    ("FUN_080eaf58", "link_nanr_anim_bank",
        "nnsys/g2d/g2d_NAN_load.c line 38 (pNanrFile). "
        "Validate NANR file and write parsed result to caller-supplied pointer slot. "
        "r0=NNS_G2dBinaryFileHeader* pNanrFile, r1=NNS_G2dAnimBankData** ppAnimBank. "
        "Asserts both ptrs non-NULL; calls find_bin_block_by_type(pNanrFile,'NANR'); "
        "if block found: skips 8-byte block header, calls relocate_nanr_block_ptrs, "
        "writes *ppAnimBank = block+8; returns 1 on success, 0 on failure."),
    ("FUN_080eafb4", "check_anim_block_has_data",
        "NNS G2D anim block utility (leaf, no external writes). "
        "r0=NNS_G2dAnimBlock* pSeqHead: [+0x0]=count(halfword), [+0xc]=first entry ptr. "
        "Iterates count entries (stride 8 bytes); returns 1 if any [entry+0x4]!=0, "
        "else returns 0. Called by relocate_nanr_block_ptrs to validate data after reloc. "
        "Equivalent to NNSi_G2dCheckAnimSequenceValidity_."),
    ("FUN_080eafd4", "load_nanr_anim_bank",
        "nnsys/g2d/g2d_NAN_load.c line 92. "
        "NANR anim file loader top-level entry: validates magic, calls link_nanr_anim_bank. "
        "r0=NNS_G2dBinaryFileHeader* pNanrFile, r1=NNS_G2dAnimBankData** ppAnimBank. "
        "Asserts both non-NULL (line 92/93); verifies [pNanrFile+0]=='NANR' (0x4e414e52) "
        "and [pNanrFile+6] u16 >= 0x100 (version check); then calls link_nanr_anim_bank. "
        "Returns 1=success, 0=failure. "
        "Constants: NANR_SIGNATURE=0x4e414e52, VERSION_MIN=0x100."),
    ("FUN_080eb0f4", "relocate_nanr_block_ptrs",
        "nnsys/g2d/g2d_NAN_load.c line 130. "
        "Patch all relative offsets in a NANR block to absolute pointers. "
        "r0=NNS_G2dAnimBankData* pBlock (block data body, after 8-byte block header). "
        "Patches [pBlock+4],[+8],[+0xc] relative->absolute; "
        "iterates each anim sequence: patches [seq+0xc] and each frame [frame+0x0]; "
        "handles optional ext block at [pBlock+0x14]; "
        "calls check_anim_block_has_data to validate. "
        "Entry uses .hword 0x4657/0x464e/0x4645 (THUMB high-register save encoding)."),
    ("FUN_080eb54c", "load_nclr_pltt_data",
        "nnsys/g2d/g2d_NCL_load.c line 49 (pNclrFile). "
        "NCLR palette file loader: verify magic, find 'PLTT' block, relocate, write *ppPltData. "
        "r0=NNS_G2dBinaryFileHeader* pNclrFile, r1=NNS_G2dPaletteData** ppPltData. "
        "Asserts both non-NULL; verifies magic=='NCLR'(0x4e434c52) or 'NCPR'(0x4e435052); "
        "checks [pNclrFile+6] u16 version>=0x100 and <0x100 for bitdepth; "
        "calls find_bin_block_by_type(pNclrFile,'PLTT')(0x504c5454); "
        "calls relocate_ncl_pltt_data_ptr; *ppPltData=block+8; returns 1/0."),
    ("FUN_080eb6b4", "relocate_ncl_pltt_data_ptr",
        "nnsys/g2d/g2d_NCL_load.c line 151 (pPlttData). "
        "Patch palette data block raw-data relative pointer to absolute address. "
        "r0=NNS_G2dPaletteData* pPlttData. "
        "Asserts pPlttData != NULL; then: [pPlttData+0xc] += pPlttData "
        "(converts pRawData field from relative offset to absolute ptr). "
        "Called by load_nclr_pltt_data after finding PLTT block."),
    ("FUN_080eb6dc", "get_nob_cell_data_offset",
        "nnsys/g2d/g2d_NOB_load.c line 11 (pCellBank). "
        "Compute byte offset of a cell entry in a NOB cell bank by format flag. "
        "r0=NNS_G2dCellBank* pCellBank, r1=u16 cell_idx [0..count-1]. "
        "[pCellBank+0x2] bit0: 0=stride 8 bytes (lsls #3), 1=stride 16 bytes (lsls #4). "
        "Returns [pCellBank+0x4] + cell_idx*stride (absolute address of cell entry). "
        "Equivalent to NNSi_G2dGetCellDataAddress."),
    ("FUN_080eb718", "relocate_nob_exdata_block_ptrs",
        "nnsys/g2d/g2d_NOB_load.c line 28 (pExData). "
        "Relocate internal pointers in a NOB extra-data block. "
        "r0=NNS_G2dBinaryBlockHeader* pExData (non-NULL assert). "
        "Skips 8-byte block header (r0+8) then calls relocate_bin_block_ptrs "
        "to patch all relative offsets to absolute addresses. "
        "Called by relocate_nob_cell_bank_ptrs when [pNcerData+0x14] exdata is present."),
    ("FUN_080eb744", "load_ncer_cell_bank",
        "nnsys/g2d/g2d_NOB_load.c line 41 (pNcerFile). "
        "NCER cell bank loader: verify magic, find 'CBEK' block, relocate, write *ppCellBank. "
        "r0=NNS_G2dBinaryFileHeader* pNcerFile, r1=NNS_G2dCellBank** ppCellBank. "
        "Asserts both non-NULL; verifies magic==0x4e434552 ('NCER'); version>=0x100; "
        "calls find_bin_block_by_type(pNcerFile,0x4345424b 'CBEK'); "
        "calls relocate_nob_cell_bank_ptrs; *ppCellBank=block+8; returns 1/0. "
        "Constants: NCER_SIGNATURE=0x4e434552, CBEK_BLOCK_TYPE=0x4345424b."),
    ("FUN_080eb838", "relocate_nob_cell_bank_ptrs",
        "nnsys/g2d/g2d_NOB_load.c line 110 (pCellData). "
        "Full internal pointer relocation for a NCER cell bank data block. "
        "r0=NNS_G2dCellBank* pNcerData (block body after 8-byte header). "
        "[pNcerData+4]+=pNcerData (cell array base abs); "
        "iterates each cell via get_nob_cell_data_offset: [cell+4]+=r6 (cell data ptr abs); "
        "if [pNcerData+0xc]!=0: abs + patch [ext+4]; "
        "if [pNcerData+0x14]!=0: abs + call relocate_nob_exdata_block_ptrs. "
        "Called by load_ncer_cell_bank."),
    ("FUN_08015674", "alloc_char_data_slot",
        "GL/IG2D_Main.c line 52. "
        "Allocate a 4096-byte char-data buffer slot from IWRAM pool; return its ptr. "
        "No parameters (all state from IWRAM). "
        "IWRAM [0x03000c00] holds current slot count; asserts count<=1 (max 2 slots [0..1]); "
        "returns [0x03002c08] + count*4096 (lsls count,#0xc); increments [0x03000c00]. "
        "Side-effect: [0x03000c00] := old_count+1. "
        "Constants: SLOT_COUNT_PTR=[0x03000c00], CHAR_POOL_BASE=[0x03002c08], SLOT_SIZE=4096."),
    ("FUN_08015b10", "load_nce_cell_bank_from_file",
        "GL/IG2D_Main.c. "
        "Full pipeline: allocate NCE buffer slot, load file from FS, parse cell bank. "
        "r0=NNS_G2dCellBank** ppCellBank (non-NULL assert), r1=const char* pFname (non-NULL). "
        "Calls alloc_nce_buff_slot -> invoke_fs_load(pFname, slot_ptr) -> "
        "load_ncer_cell_bank(slot_ptr, ppCellBank). "
        "Returns loaded data ptr on success, NULL on failure. "
        "Side-effects: IWRAM slot allocated, file DMA'd, *ppCellBank set."),
    ("FUN_08015b70", "load_nanr_anim_bank_from_file",
        "GL/IG2D_Main.c. "
        "Full pipeline: allocate char-data slot, load NANR file from FS, parse anim bank. "
        "r0=NNS_G2dAnimBankData** ppAnimBank (non-NULL assert line 0x1c1), "
        "r1=void** ppCharData (non-NULL assert line 0x1c2). "
        "Calls alloc_char_data_slot -> invoke_fs_load(ppCharData, slot_ptr) -> "
        "load_nanr_anim_bank(slot_ptr, ppAnimBank). "
        "Returns loaded data ptr on success, NULL on failure. "
        "Side-effects: char-data slot allocated ([0x03000c00] +1), file DMA'd, *ppAnimBank set."),
    ("FUN_08015c30", "load_nclr_pltt_data_from_file",
        "GL/IG2D_Main.c. "
        "Full pipeline: load NCLR palette file from FS, parse palette data. "
        "r0=NNS_G2dPaletteData** ppPltData (non-NULL assert line 0x266=614), "
        "r1=const char* pFname (non-NULL assert line 0x267=615). "
        "Calls invoke_fs_load(pFname, NULL) (system-allocated buffer) -> "
        "load_nclr_pltt_data(loaded_ptr, ppPltData). "
        "Returns loaded data ptr on success, NULL on failure. "
        "Side-effects: file loaded to system memory, *ppPltData set."),
    # --- campaign-6 batch ---
    ("FUN_080eb2e8", "fixup_char_block_data_ptr",
        "GL/IG2D_Main.c g2d_NCG_load.c pipeline. "
        "r0=NNS_G2dCharacterData* pCharData (NCGR bin +8, non-NULL assert line 92). "
        "Asserts pCharData != NULL, then adds pCharData base to [pCharData+0x14] "
        "(relative pixel-data offset -> absolute pointer fixup). "
        "Checks [pCharData+0xc] and may skip trailing branch. "
        "Side-effect: [pCharData+0x14] updated from relative offset to absolute address."),
    ("FUN_080eb23c", "parse_ncgr_char_data",
        "GL/IG2D_Main.c g2d_NCG_load.c pipeline. "
        "r0=const void* pNcgrFile (must be non-NULL, magic==0x4E434752 'NCGR'), "
        "r1=NNS_G2dCharacterData** ppCharData (non-NULL). "
        "Validates magic and version, calls find_bin_block_by_type for 'RAHC' (CHAR block), "
        "then calls fixup_char_block_data_ptr and writes result to *ppCharData. "
        "Returns 1=success, 0=fail (bad magic or no CHAR block). "
        "Side-effect: *ppCharData points to fixup'd CHAR data block, or NULL on failure."),
    ("FUN_08015bd0", "load_ncgr_char_data_from_file",
        "GL/IG2D_Main.c line 574-575. "
        "r0=NNS_G2dCharacterData** ppCharData (non-NULL), "
        "r1=const char* pFname (NCGR file path, non-NULL). "
        "Calls invoke_fs_load to load NCGR file into system-allocated buffer, "
        "then calls parse_ncgr_char_data to parse CHAR block into *ppCharData. "
        "Returns file buffer ptr on success, NULL on failure. "
        "Side-effects: FS memory allocated, *ppCharData set to parsed char data."),
    ("FUN_080e9c74", "set_img_proxy_vram_slot",
        "GL/IG2D_Main.c g2d_Image.c line 468-469. "
        "r0=NNS_G2dImageProxy* pProxy (non-NULL), "
        "r1=void* pImg (image data ptr, non-NULL), "
        "r2=NNS_G2dVRamType type [0..2] (0=3D_MAIN, 1=2D_MAIN, 2=2D_SUB). "
        "Asserts all args, calls check_vram_location_slot, "
        "then writes pImg to pProxy[type] (str pImg,[pProxy+type*4]). "
        "Side-effect: NNS_G2dImageProxy VRAM slot[type] set to pImg."),
    ("FUN_08015c90", "copy_pltt_data_to_vram_proxy",
        "GL/IG2D_Main.c line 729-730. "
        "r0=NNS_G2dPaletteData* pSrcData (non-NULL), "
        "r1=u32 vram_offset (added to OBJ palette base 0x05000200), "
        "r2=NNS_G2dVRamType vram_type [0..2], "
        "r3=NNS_G2dImageProxy* pPltProxt (non-NULL). "
        "If r6==1: bios_cpu_fast_set DMA copies palette to OBJ VRAM at 0x05000200+offset; "
        "else assert_false (line 739). "
        "Calls set_img_proxy_vram_slot to update proxy slot. "
        "Side-effects: OBJ palette VRAM written; ImageProxy slot updated."),
    ("FUN_080e9a94", "init_img_proxy_fields",
        "GL/IG2D_Main.c g2d_Image.c line 373. "
        "r0=NNS_G2dImageProxy* pProxy (non-NULL). "
        "Asserts pProxy != NULL, then writes 0xFFFFFFFF (-1) to fields "
        "[pProxy+0x0], [pProxy+0x4], [pProxy+0x8] (3 VRAM slot fields). "
        "Side-effect: all 3 ImageProxy VRAM slots marked invalid (NNS init pattern)."),
    ("FUN_080eb1f4", "get_anim_sequence_ptr_by_index",
        "GL/IG2D_Main.c g2d_NAN_load.c line 203 / g2d_NAN_load.h line 21. "
        "r0=NNS_G2dAnimBankData* pAnimBank (non-NULL), "
        "r1=u16 seqIndex [0..numSequences-1] (high 16 bits truncated). "
        "Asserts pAnimBank != NULL and seqIndex < numSequences, "
        "then returns &pAnimBank->pSequenceArrayHead[seqIndex] (each entry 16 bytes). "
        "Returns NULL on out-of-bounds. "
        "No side-effects (pure address computation)."),
    ("FUN_080e9c38", "init_renderer_img_proxy_fields",
        "GL/IG2D_Main.c g2d_Image.c line 449. "
        "r0=NNS_G2dRendererImageProxy* pProxy (non-NULL). "
        "Asserts pProxy != NULL, then writes 0xFFFFFFFF (-1) to fields "
        "[pProxy+0x8], [pProxy+0xc], [pProxy+0x10] (3 VRAM location slots). "
        "Symmetric sibling to init_img_proxy_fields (0x080e9a94) which covers +0..+8. "
        "Side-effect: RendererImageProxy VRAM slots +8/+c/+10 marked invalid."),
    ("FUN_08015d30", "load_g2d_obj_resource_set",
        "GL/IG2D_Main.c core G2D OBJ resource loader, line 813-874, indeg=6. "
        "r0=void* pOutState, r1=NNS_G2dCellAnimation** ppAnimCtrl (r8 via 0x4689), "
        "r2=G2dObjPathConfig* pPaths {ncer*,nanr*,ncgr*,nclr*}, r3=u32 vramFlags. "
        "Stack args: flag0/flag1/pFilePathTable/flag3/bufSize. "
        "Sequence: init_img_proxy_fields + init_renderer_img_proxy_fields, "
        "load_nce_cell_bank_from_file + load_nanr_anim_bank_from_file, "
        "alloc_cell_anim_slot + get_anim_sequence_ptr_by_index + bind_cell_anim_to_bank per seq, "
        "optional load_ncgr_char_data_from_file + load_img_proxy_to_vram (NCGR path), "
        "optional load_nclr_pltt_data_from_file + copy_pltt_data_to_vram_proxy (NCLR path). "
        "Side-effects: VRAM OBJ tile+palette written; ppAnimCtrl slots bound; ImageProxy set."),
    ("FUN_08013940", "load_demo_obj_resource_by_slot",
        "demo scene OBJ resource loader with slot selection. "
        "r0=u32 slot_index [0..1] (0=exodia01_obj, 1=exodia02_obj). "
        "Reads file path table from ROM constant at 0x09e397d4 (8 paths: 2 slots x 4 files), "
        "indexes by slot_index*16 on stack, then calls load_g2d_obj_resource_set. "
        "Side-effects: gDemoState anim ctrl + ImageProxy initialised; "
        "OBJ Tile VRAM + OBJ Palette VRAM written with exodia file data."),
    ("FUN_0801398c", "load_demo_obj_resource_slot0",
        "demo scene slot-0 OBJ loader stub. "
        "void args. "
        "Fixes r0=0 then calls load_demo_obj_resource_by_slot(0) "
        "to load exodia01_obj {NCER/NANR/NCGR/NCLR} into demo state slot 0. "
        "Returns r0=1 (fixed success flag). "
        "Side-effects: same as load_demo_obj_resource_by_slot(0)."),
    ("FUN_0801399c", "write_bg3_scroll_regs",
        "demo scene BG3 scroll register write helper. "
        "r0=u16 hofs [0..511], r1=u16 vofs [0..511]. "
        "Masks both with 0x1FF, then strh hofs -> BG3HOFS (0x04000018), "
        "strh vofs -> BG3VOFS (0x0400001E). "
        "Called by tick_demo_bg3_hscroll and tick_demo_bg3_vscroll after computing new offsets. "
        "Side-effects: GBA IO regs BG3HOFS and BG3VOFS updated."),
    ("FUN_080139b8", "tick_demo_bg3_hscroll",
        "demo scene per-frame BG3 horizontal scroll updater. "
        "void args. "
        "Reads gDemoState+0x8c bits[23:16] as 8-bit scroll counter, "
        "computes HOFS = counter % 160 (0xa0, GBA screen width), "
        "steps counter bits[8:1] += 2 mod 256 with wrap at 0xa0, "
        "writes back to gDemoState+0x8c, calls write_bg3_scroll_regs(0, hofs). "
        "Side-effects: gDemoState+0x8c updated; BG3HOFS written."),
    ("FUN_08013a10", "tick_demo_bg3_vscroll",
        "demo scene per-frame BG3 vertical scroll updater. "
        "void args. "
        "Reads gDemoState+0x8c bits[23:16], computes VOFS = -(counter % 240) "
        "(0xf0, GBA screen height; rsbs for upward scroll direction), "
        "steps counter bits[8:1] += 2 mod 256 with wrap at 0xf0, "
        "writes back, calls write_bg3_scroll_regs(vofs, 0). "
        "Side-effects: gDemoState+0x8c updated; BG3VOFS written."),
    ("FUN_080e8b6c", "set_cell_anim_sequence_by_index",
        "g2d_Animation.c line 272-273. "
        "r0=NNS_G2dCellAnimation* pAnimCtrl (non-NULL), "
        "r1=u16 seqId [0..numSequences-1] (high 16 bits truncated), "
        "r2=NNS_G2dAnimBankData* pAnimBank (must already be bound). "
        "Asserts pAnimCtrl != NULL and pAnimCtrl->pAnimSequence != NULL, "
        "checks seqId < pAnimBank->numSequences, "
        "then writes &pAnimBank->pSequenceArrayHead[seqId*8] to pAnimCtrl->pAnimSequence (+0). "
        "Returns 1=success, 0=out-of-bounds. "
        "Side-effect: pAnimCtrl active sequence pointer updated."),

    # 2026-05-06: campaign-7 batch (topo=113/114/115/116/117/118/119/120/121/122/123/124/125/126/127)
    ("FUN_080e8f88", "set_cell_anim_sequence_by_idx_guarded",
        "nnsys/g2d/g2d_Animation.c line 0x1a9=425. "
        "Called by step_cell_anim_sequence_guarded (0x080e95ec). "
        "Asserts pCellAnim != NULL (line 425) and pCellAnim->pCurrentCell (+0x18) non-NULL (line 427). "
        "Calls set_cell_anim_sequence_by_index(pCellAnim, sequence_idx); "
        "if return non-zero: clears [pCellAnim+0xc] (reset sequence-changed flag). "
        "r0=NNS_G2dCellAnimation* pCellAnim [non-NULL], r1=u16 sequence_idx. "
        "Returns set_cell_anim_sequence_by_index return value."),
    ("FUN_080e95ec", "step_cell_anim_sequence_guarded",
        "nnsys/g2d/g2d_CellAnimation.c. "
        "Called by dispatch_cell_anim_sequence_step (0x080156e0, D_shared_mid hub indeg=6) and FUN_08015ea4. "
        "Asserts pCellAnim != NULL (g2d_Animation.c:0x143=323), pCellAnim->pCurrentCell (+0x18) non-NULL. "
        "Calls set_cell_anim_sequence_by_idx_guarded(pCellAnim, seq_idx); "
        "if return non-zero: calls apply_cell_anim_frame to apply OAM data. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=u16 sequence_idx. "
        "Returns 0=no frame change, non-zero=frame applied."),
    ("FUN_080156e0", "dispatch_cell_anim_sequence_step",
        "D_shared_mid hub (indeg=6) shared across 5 scenes (scene_demo 0x08013a68/0x0801bb28 + "
        "3 unnamed scene 0x08018260/0x0801a49c/0x0801c5d8). "
        "Body: u16 mask on r1 (lsls/lsrs #0x10) then tail-call step_cell_anim_sequence_guarded (0x080e95ec). "
        "Provides unified entry + width truncation ensuring sequence_idx is u16 for NNS G2D layer. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=u16 sequence_idx. "
        "Returns transparent from step_cell_anim_sequence_guarded."),
    ("FUN_080e957c", "advance_cell_anim_frame_guarded",
        "nnsys/g2d/g2d_CellAnimation.c line 0x122=290. "
        "Called by dispatch_cell_anim_frame_advance (0x0801571c, D_shared_mid hub indeg=6). "
        "Asserts pCellAnim != NULL (line 290), pCellAnim->pCurrentCell (+0x18) non-NULL (line 291), "
        "animation sequence type == NNS_G2D_ANIMATIONTYPE_CELL (line 293). "
        "Calls step_anim_ctrl_by_frames(pCellAnim, frames); "
        "if return non-zero (frame changed): calls apply_cell_anim_frame to update OAM. "
        "Sibling of step_cell_anim_sequence_guarded: this advances frames, that switches sequences. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=s16 frames [0..N]. "
        "Returns 0=no change, non-zero=frame changed."),
    ("FUN_0801571c", "dispatch_cell_anim_frame_advance",
        "D_shared_mid hub (indeg=6) shared across 5 scenes, sibling of dispatch_cell_anim_sequence_step. "
        "Same caller set (scene_demo 0x08013a68/0x0801bb28 + 3 unnamed 0x08018260/0x0801a49c/0x0801c5d8). "
        "Body: 5 instructions, direct call to advance_cell_anim_frame_guarded (0x080e957c), no param transform. "
        "Provides unified public jump point for NNS G2D frame advance. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=s16 frames. "
        "Returns transparent from advance_cell_anim_frame_guarded."),
    ("FUN_08015924", "resolve_bg_affine_param_offset",
        "GL/IG2D_Main.c line 0x180=384. "
        "Called by setup_isd_cell_anim_oam_entry (0x08015954). "
        "Converts BG index (1 or 2) to corresponding affine parameter register byte offset. "
        "r0==1 -> returns 4; r0==2 -> returns 9; other -> assert(0) (IG2D_Main.c:384), returns 0. "
        "Pairs with resolve_isd_affine_matrix_ptr (0x08016108): this returns P-param offset, "
        "that returns matrix data pointer. "
        "r0=u8 bg_index [1..2]. Returns u8 param_offset {4, 9}."),
    ("FUN_08016108", "resolve_isd_affine_matrix_ptr",
        "GL/ISD_Draw.c line 0x8c=140. "
        "Called by setup_isd_cell_anim_oam_entry (0x08015954). "
        "Returns ISD matrix data pointer by affine type code (4 or 9). "
        "r0==4 -> ldr DAT_08016130 (=0x09e587e4) content; r0==9 -> ldr DAT_0801613c (=0x09e587e8) content; "
        "other -> assert(0) (ISD_Draw.c:140), returns 0. "
        "Paired with resolve_bg_affine_param_offset: receives its return value as input. "
        "r0=u8 affine_type {4, 9}. Returns void* affine matrix data ptr."),
    ("FUN_080151b4", "assign_palette_slot_entry",
        "Called by alloc_palette_entry_slot (0x080151d8, palette tag) only. "
        "Establishes bidirectional mapping slot_idx <-> palette_entry in EWRAM palette manager table. "
        "Base 0x02023490: slot_record array at +0x800 (1 byte/entry), palette_map array at +0x880. "
        "Saves old palette_map[palette_entry] into slot_record[slot_idx]; "
        "writes slot_idx into palette_map[palette_entry] (atomic slot occupation record). "
        "r0=u8 slot_idx [0..127], r1=u8 palette_entry [0..31]. Returns void. "
        "Side-effects: [0x02023C90+slot_idx] and [0x02023D10+palette_entry] updated."),
    ("FUN_080151d8", "alloc_palette_entry_slot",
        "GL/IG2D_Main.c palette slot allocator. "
        "Called by setup_isd_cell_anim_oam_entry (0x08015954) and 3 other scene init paths. "
        "Checks [0x02024330] signed byte (slot counter) >= 0; if negative (no slots): returns NULL. "
        "Otherwise: calls assign_palette_slot_entry to record mapping, increments counter, "
        "computes EWRAM palette entry addr (base + slot*8 + 0x400), "
        "bios_cpu_set zero-fills 8 bytes (CPUSET_CTRL=0x05000002), returns entry ptr. "
        "r0=u8 palette_id [0..31]. Returns u8* palette entry ptr or NULL. "
        "Side-effects: [0x02024330] += 1; palette entry zeroed."),
    ("FUN_080e969c", "build_oam_attrs_from_cell_with_affine",
        "Called by setup_isd_cell_anim_oam_entry (0x08015954). "
        "Transforms all cell OAM objects of current NNS_G2dCellAnimation frame via SRT affine "
        "and writes result to output buffer (pDst). "
        "Source: inc/nnsys/g2d/fmt/g2d_Cell_data.h + g2d_Animation_inline.h asserts. "
        "Core loop: reads attr0/attr1/attr2 (3x u16), extracts flip flags and OAM mode, "
        "applies SRT transform via __muldi3 (12.20 fixed-point matrix multiply), "
        "re-encodes transformed X/Y into attr0/attr1. Loop from 0 to min(cell_oam_count, max_limit). "
        "r0=void* pDst_base [0x030007f8 at callsite], r1=u16 max_oam_count [0..128], "
        "r2=NNS_G2dCellData* pCell, r3=NNS_G2dAnimController* pAnimCtrl. "
        "Returns u16 actual OAM count written. "
        "Side-effects: [pDst+i*8] per-entry OAM attr0/attr1 pair written."),
    ("FUN_08015954", "setup_isd_cell_anim_oam_entry",
        "GL/IG2D_Main.c line 0xe3=227. "
        "Called by dispatch_isd_cell_anim_oam_setup (0x08015a8c, D_shared_mid hub indeg=6) and FUN_0801a49c. "
        "Core cell animation OAM initializer: "
        "(1) resolve_bg_affine_param_offset -> affine offset; "
        "(2) resolve_isd_affine_matrix_ptr(offset) -> matrix ptr; "
        "(3) asserts pCell != NULL; "
        "(4) loops alloc_palette_entry_slot to allocate palette slots; "
        "(5) build_oam_attrs_from_cell_with_affine(0x030007f8, max=128, pCell, pAnimCtrl). "
        "Returns u16 OAM entry count. "
        "Side-effects: EWRAM palette slot [0x02024330]+1; OAM buffer [0x030007f8+...] written."),
    ("FUN_08015a8c", "dispatch_isd_cell_anim_oam_setup",
        "D_shared_mid hub (indeg=6) shared across 5 scenes (scene_demo + unnamed scene + 0x08015ea4). "
        "Body 29 instructions: loads stack args (r4-r7 from [sp+0x38..0x54]) into new stack frame, "
        "sets [sp+0x20]=0 (counter init), calls setup_isd_cell_anim_oam_entry, unwinds and returns. "
        "Multi-arg wrapper: repacks caller-supplied stack args and forwards to core init function. "
        "r0=NNS_G2dCellAnimation* pCellAnim, r1=void* pCell, r2=NNS_G2dCellDataBank* pCellBank, "
        "r3=u16 bg_index [1..2]. Returns u16 OAM count transparent from setup_isd_cell_anim_oam_entry."),
    ("FUN_08015718", "read_obj_id_field",
        "Minimal D_shared_mid hub (indeg=6, 2 instructions, 4 bytes). "
        "Body: ldrh r0,[r0,#0x0]; bx lr -- reads first u16 field of object and returns. "
        "Called by FUN_08013a68 (scene_demo) before comparing slot_idx; "
        "receives pointer loaded from gDemoState table by slot offset. "
        "Provides type-safe accessor for object's first u16 field (ID / count / type_code). "
        "r0=void* obj_ptr. Returns u16 first field value."),
    ("FUN_08013a68", "setup_demo_cell_anim_slot",
        "scene_demo cell animation slot initializer. "
        "Called by FUN_08013bd4 (tags: display,bg,demo,fs,settings) only. "
        "Steps: (1) table-lookup gDemoState[slot_idx*4] for cell anim ptr; "
        "(2) read_obj_id_field to assert slot_idx < obj_field (IG2D_Main.c:0x14b=331); "
        "(3) get gDemoState+slot*4+8 anim struct addr; "
        "(4) if frame_or_seq_param==-1: dispatch_cell_anim_frame_advance; "
        "else: dispatch_cell_anim_sequence_step; "
        "(5) assemble stack args and call dispatch_isd_cell_anim_oam_setup for OAM init. "
        "r0=u8 slot_idx [0..slot_count-1], r1=NNS_G2dCellAnimation* pCellAnim, "
        "r2=s16 frame_or_seq_param (-1=frame advance, else=seq_idx lsls*0xc), r3=s16 second_param. "
        "Constants: gDemoState=0x02029ec0."),
    ("FUN_080147d8", "gl_set_blend2_level",
        "GL/GL_Common.c -- blend2 coefficient setter, symmetric sibling of gl_set_brightness. "
        "Called by gl_fade_in (0x080148d0), gl_fade_out (0x080148e0), and 11 other window/display/scene callers (indeg=13). "
        "Asserts blend1_level+0x10<=0x20 and blend2_level<=0x10 (GL_Common.c line 0x10a=266, 0x10b=267). "
        "Writes blend2_level to [gl_state+0x8] bits[11:2] (mask 0xFFFFFC03, shift 10); "
        "saves blend1_level to [gl_state+0x1]; old [gl_state+0x1] -> [gl_state+0x0]; "
        "writes blend_target to [gl_state+0x2]; calls update_brightness_fade_flag(blend1_level). "
        "r0=u8 blend_target [0..255], r1=s8 blend1_level [-16..16], r2=u8 blend2_level [0..16]. "
        "Constants: GL_STATE_BASE=0x02023480 / BLEND2_MASK=0xFFFFFC03 / BLEND2_SHIFT=10."),
    # --- campaign-8 batch (2026-05-06) ---
    ("FUN_08013af4", "apply_demo_window_fade_in_step",
        "Called by tick_demo_scene_state_machine (0x08013bd4) caseD_4/caseD_6 to execute one fade-in step "
        "for the demo window animation. Accepts current_frame r0 and max_frames r1; "
        "if equal (fade done): configures WININ/WINOUT/WIN0H/WIN0V registers and calls gl_set_brightness(0x3f,0) + gl_set_blend2_level. "
        "Otherwise writes WIN0V vertical range proportional to frame progress. "
        "r0=u8 current_frame [0..max_frames-1], r1=u8 max_frames [1..15]. "
        "Symmetric sibling of apply_demo_window_fade_out_step (0x08013b84). "
        "Side-effects: WININ(0x04000048), WINOUT(0x0400004a), WIN0H(0x04000040), WIN0V(0x04000044), DISPCNT bits[13:5]."),
    ("FUN_08013b84", "apply_demo_window_fade_out_step",
        "Called by tick_demo_scene_state_machine (0x08013bd4) caseD_6 to execute one fade-out step. "
        "Computes window vertical range as (max-cur)*0x50/max and writes to WIN0V; "
        "on completion calls gl_set_brightness(0x3f,-16) + tick_blend_transition_step (0x08014914) + gl_set_blend2_level. "
        "r0=u8 current_frame [0..max_frames-1], r1=u8 max_frames [1..15]. "
        "Symmetric sibling of apply_demo_window_fade_in_step (0x08013af4), direction reversed. "
        "Side-effects: WIN0V(0x04000044), gl_set_brightness(-16), tick_blend_transition_step."),
    ("FUN_08013bd4", "tick_demo_scene_state_machine",
        "Called by FUN_08014398 and play_ui_effect_3a (0x080bcbd4); drives the demo scene (Exodia animation) "
        "per-frame state machine. Reads gDemoState+0x8c bits[22:15] as state_idx (0-9), dispatches via 10-entry jump table: "
        "case0 load BG gfx set0+FS+sprites; case1/2 check blend progress and advance fade-in; "
        "case3/4 step sprite animation frames; case5 load BG gfx set1; case6/7 fade-out window animation; "
        "case8/9 end states. Each case increments state counter and falls through to default (no change). "
        "No parameters (void); all inputs from gDemoState EWRAM struct. "
        "Side-effects: gDemoState+0x8c state field, DISPCNT/BG3CNT/BLDCNT IO registers."),
    ("FUN_0801469c", "clear_demo_sprite_enable_bits",
        "Called by tick_demo_scene_state_machine (0x08013bd4) caseD_4 after blend-done check "
        "to reset sprite-enable bits in gDemoState+0x8. "
        "Three-step operation on same field: (1) ldrb/strb clear bit2 (mask ~0x04); "
        "(2) ldrh/strh clear bits[9:2] (mask 0xfffffc03); "
        "(3) ldr/str clear bits[17:10] and set bit10 (0x400) as sprite-inactive initial state. "
        "No parameters (void); leaf function. "
        "Side-effects: [gDemoState(0x02023480)+0x8] byte/halfword/word."),
    ("FUN_08014914", "tick_blend_transition_step",
        "Called by many scene ticks (indeg=10) including demo scene state machine and name_input_page_tick. "
        "Advances the GL blend-transition state machine one step per frame: "
        "reads gDemoState+0x8 bits[9:2] (cur step) and bits[17:10] (target step); "
        "if equal returns idle; otherwise increments step and dispatches by step-range (0x00/0x40/0x80/0xC0). "
        "0x40/0x00 branches interpolate BLDCNT/BLDY; 0x80/0xC0 branches set BLDY direction coefficient. "
        "No parameters (void). "
        "Side-effects: gDemoState+0x8 step field, BLDCNT(0x04000050), BLDY(0x04000054)."),
    ("FUN_080148f4", "check_blend_transition_done",
        "Called by many scene ticks (indeg=7) including tick_demo_scene_state_machine caseD_1/2/3 and name_input_page_tick. "
        "Reads gDemoState+0x8 bits[9:2] (cur step) and bits[17:10] (target step); "
        "returns 0 if equal (transition complete), 1 if still in progress. Pure read, no side-effects. "
        "Prerequisite check before tick_blend_transition_step (0x08014914): caller waits for 0 before advancing state. "
        "No parameters (void). Returns r0=u8 done_flag {0=done, 1=in-progress}."),
    ("FUN_08014754", "init_blend_transition_params",
        "Called by tick_demo_scene_state_machine caseD_2/3 and 3 other scene ticks (indeg=5). "
        "Initializes gDemoState blend-transition param struct (0x02023480): writes r1/r0/r2/r3 "
        "(blend start/current/end/step) to byte fields +0/+1/+2/+4/+5/+6; clears bits[9:2] of +0x8 "
        "and ORs 0x400; sets +0x8 bit0=1 (active). Out-of-range params trigger suppress_assert_report "
        "(GL/GL_Common.c lines 248/249). High-register convention: r8=r1 via caller mov r8,r1. "
        "r0=u8 blend_target [0..255], r1=s8 blend1_start [0..16], r2=u8 blend2_end [0..16], "
        "r3=u8 blend_step [0..16]. No return (void)."),
    ("FUN_08014838", "init_blend_transition_params_ex",
        "Extended version of init_blend_transition_params (0x08014754); called by tick_demo_scene_state_machine "
        "caseD_3 and 3 other scene ticks (indeg=4). Accepts extra stack param r5=[sp+0x1c] as additional blend channel. "
        "Same purpose: writes r0/r1/r2/r3/r5 to gDemoState+0x0..+0x6 byte fields with history-roll (+1->+0, +5->+4); "
        "clears +0x8 step count and sets active bit. Out-of-range params trigger suppress_assert_report "
        "(GL/GL_Common.c lines 282/283). High-register convention: r8=r0, r9=r1 via caller mov instructions. "
        "r0=u8 blend_target_ch1 [0..255], r1=s8 blend1_start_ch1 [0..16], r2=u8 blend2_end_ch1 [0..16], "
        "r3=u8 blend_step_ch1 [0..16], [sp+0x1c]=u8 blend_extra. No return (void)."),
    ("FUN_0801522c", "copy_sprite_attr_table_to_oam",
        "Called by many scene ticks (indeg=6) including tick_demo_scene_state_machine, name_input_page_tick, "
        "demo_shuen_state_machine. Copies up to 32 sprite attribute entries (8 bytes each) from EWRAM sprite-attr "
        "array (0x02023490+0x880) to EWRAM OAM buffer (0x02023490+slot*8); sentinel=-1 terminates list. "
        "Finally calls bios_cpu_fast_set to zero unused OAM VRAM slots (0x07000000). "
        "No external parameters (void); all addresses computed internally from DAT_080152ac=0x02023490. "
        "Side-effects: EWRAM OAM buffer (0x02023490+) write; bios_cpu_fast_set zero OAM VRAM (0x07000000)."),
    ("FUN_080156c8", "get_title_ex_obj_field8",
        "Called by FUN_0801bb28 (scene_demo) and two scene_title_ex callers (indeg=3). "
        "Body: ldr r0,[r0,#0x8]; bx lr -- simple field getter. "
        "r0=ptr obj (title_ex scene object); returns r0=u32 field8 ([obj+0x8]). "
        "Getter/setter pair with set_title_ex_obj_field8 (0x080156cc) at adjacent address. Pure read, no side-effects."),
    ("FUN_080156cc", "set_title_ex_obj_field8",
        "Called by FUN_0801bb28 (scene_demo) and FUN_080fd678 (scene_title_ex) (indeg=2). "
        "Body: str r1,[r0,#0x8]; bx lr -- simple field setter. "
        "r0=ptr obj (title_ex scene object), r1=u32 value to write to [obj+0x8]. "
        "Getter/setter pair with get_title_ex_obj_field8 (0x080156c8) at adjacent address. "
        "Side-effects: [r0+0x8] := r1."),
    ("FUN_08015728", "compute_bg_affine_matrix_scaled",
        "Called by FUN_08015820 and apply_bg_affine_by_angle_scale (0x08015868) (indeg=2). "
        "Computes BG affine transform matrix PA/PB/PC/PD from angle and x/y scale: "
        "1) bios_div(0x01000000, scale_x/y) for fixed-point reciprocals (8.24); "
        "2) lookup cos(angle)=trig_table[angle+0x40] and sin(angle)=trig_table[angle] (ROM 0x09e399d0, 256 s16 entries); "
        "3) __muldi3(trig_val<<4, inv_scale) -> 8.8 fixed-point affine coefficient; PD=-cos*inv_scale_y. "
        "Results written to output buffer r3: [r3+0]=PA, [r3+4]=PB, [r3+8]=PC, [r3+0xc]=PD. "
        "r0=s32 scale_x, r1=s32 scale_y, r2=s32 angle [0..255], r3=ptr out_matrix. "
        "Returns r0=ptr out_matrix. "
        "Constants: TRIG_TABLE=0x09e399d0, FIXED_ONE=0x01000000."),
    ("FUN_08015868", "apply_bg_affine_by_angle_scale",
        "Called by FUN_0801c668 (BG affine animation driver, indeg=1). "
        "Full BG affine transform write-back entry: asserts bg_index in [2..3] (GBA only BG2/BG3 support affine); "
        "calls compute_bg_affine_matrix_scaled to get PA/PB/PC/PD; shifts each >>4 and writes to "
        "BG2PA/PB/PC/PD hardware registers (0x04000020+bg_index*0x10); computes and writes BG2X/BG2Y reference point. "
        "r0=u8 bg_index [2..3], r1=u8 angle [0..255], r2=s32 scale_x, r3=s32 scale_y, [sp+0x2c]=ptr out_matrix. "
        "Side-effects: BG2PA(0x04000020)/BG2PB/BG2PC/BG2PD and BG2X(0x04000028)/BG2Y written per bg_index offset."),
    ("FUN_0801b7e8", "init_demo_shuen_display_state",
        "Called by play_demo_shuen (0x080bc880) and FUN_0801c254 (indeg=2). "
        "Full display-state reset for the demo shuen (final) scene: "
        "bios_cpu_set fill-zeros gDemoState (EWRAM 0x02029ec0) header; "
        "gl_clear_vram_palram_scroll; writes DISPCNT(0x04000000):=0x40 (BG mode 2); "
        "writes BG0CNT(0x04000008):=0x1d00, BG1CNT(0x0400000a):=0x1e01, "
        "BG2CNT(0x0400000c):=0x1f02, BG3CNT(0x0400000e):=0x9b0b; "
        "gl_set_brightness(0x3f,-16) (full dark for fade-in); gl_state_init; gl_clear_frame_callbacks. "
        "No parameters (void). Returns r0=1 (success). "
        "Constants: DISPCNT=0x04000000, BG0CNT_VAL=0x1d00, BG1CNT_VAL=0x1e01, "
        "BG2CNT_VAL=0x1f02, BG3CNT_VAL=0x9b0b."),
    ("FUN_0801b850", "load_demo_shuen_sprite_gfx",
        "Called by FUN_0801b91c (scene_demo, indeg=1). "
        "Loads a single sprite GFX resource for the demo shuen scene. "
        "Non-APCS input: r8=ptr oam_entry (caller-set, transparent through FUN_0801b91c which has no r8 write). "
        "APCS: r0=u8 sprite_slot [0..1], r1=u8 tile_param_low [0..1], r2=u8 tile_param_high [1..2], "
        "r3=u8 sprite_config [0..0]; stack [sp+0x48]=u8 palette_slot [0..0]. "
        "Reads gDemoState+0x88 for GFX resource handle; calls zero_struct_36bytes(r8) to clear OAM buffer; "
        "configures OAM attr bytes [+0x14/0x17/0x18] for tile shape/priority/palette; "
        "loads ROM GFX resource descriptor (0x09e3cee8) and calls apply_gfx_resource_list. "
        "Constants: GFX_RESOURCE_LIST=0x09e3cee8, OAM_PALETTE_MASK=0xffffc07f, OAM_ENTRY_SIZE=36."),
    ("FUN_0801b91c", "load_shuen_sprite_gfx_guarded",
        "demo_shuen scene sprite GFX load dispatcher (guarded). "
        "Called twice by demo_shuen_state_machine (0x0801bd08) in caseD_0 (INIT step). "
        "r0=u8 skip_flag: if r0==0, shifts params (r1->r0, r2->r1, r3->r2, [sp+0xc]->r3, [sp+0x8]->stack) "
        "then calls load_demo_shuen_sprite_gfx; if r0!=0, skips. "
        "Both actual callsites pass r0=0 so the load path always executes. "
        "Params: r0=skip_flag {0=load, non-0=skip}, r1=tile_param_low [0..1], r2=tile_param_high [0..2], "
        "r3=sprite_config [1..2], [sp+0x8]=5th param, [sp+0xc]=6th param. "
        "Returns void (tail-call via pop {r0}; bx r0). "
        "Side-effects: OAM attr bytes [r8+0..35] zeroed then attr0/1/2 written; apply_gfx_resource_list triggered. "
        "Constants: none (all magic handled by callee)."),
    ("FUN_0801b93c", "load_shuen_bg1_gfx_set",
        "demo_shuen scene BG1 GFX resource loader. "
        "Called by demo_shuen_state_machine (0x0801bd08) caseD_0 with r0=0x09e3cfe8 ('demo/shuen/shuen_bg1.LZ5bg'). "
        "Flow: (1) fs_load(r0, 0) decompresses shuen_bg1.LZ5bg; "
        "(2) zero_struct_36bytes clears first GFX descriptor; configures OAM attr bytes "
        "(attr0+0x14 bits[3:0]=0, attr2+0x18 bits[14:7] cleared via mask 0xffffc07f, priority=3); "
        "first apply_gfx_resource_list writes BG1 resource; "
        "(3) zero_struct_36bytes clears second descriptor; attr bits[3:0]=3, [+0x18]=0xa00 OBJ tile offset; "
        "second apply_gfx_resource_list; (4) strh to DISPCNT (0x04000000) enables display. "
        "Symmetric with load_demo_bg_gfx_set0 (0x0801379c). "
        "Param: r0=ptr file_path (ROM addr pointing to 'demo/shuen/shuen_bg1.LZ5bg'). Returns void. "
        "Constants: BG1_GFX_RESOURCE=0x09e3cfe8, OAM_PRIORITY_MASK=0xffffc07f, "
        "PRIORITY_3=0x3, OBJ_TILE_OFFSET=0xa0<<4, DISPCNT=0x04000000."),
    ("FUN_0801ba04", "load_shuen_obj_resource_by_slot",
        "demo_shuen scene OBJ GFX resource loader by slot index. "
        "Called by load_shuen_obj_resource_slot0 (0x0801ba4c) with r0=0. "
        "Symmetric with load_demo_obj_resource_by_slot (0x08013940): "
        "(1) copies 4 words from ROM resource table 0x09e3cf60 (ldmia + str) to stack struct; "
        "(2) builds load_g2d_obj_resource_set param struct "
        "(r0=gDemoState, r1=gDemoState+4, r2=gDemoState+8, [sp+0]=0, [sp+4]=1, [sp+8]=slot_ptr, "
        "[sp+0xc]=0, [sp+0x10]=0x200); "
        "(3) lsls r0,r0,#4 multiplies slot_index by 16 for resource table offset; "
        "(4) calls load_g2d_obj_resource_set. "
        "Param: r0=u32 slot_index [0..0]. Returns void (tail-call pop {r0}; bx r0). "
        "Side-effects: gDemoState anim ctrl + ImageProxy initialized; "
        "OBJ Tile VRAM + OBJ Palette VRAM written with shuen OBJ data. "
        "Constants: GDEMOSTATE=0x02029ec0, SHUEN_OBJ_RESOURCE_TABLE=0x09e3cf60, "
        "OBJ_RESOURCE_STRIDE=0x10, VRAM_FLAGS=0x200."),
    ("FUN_0801ba4c", "load_shuen_obj_resource_slot0",
        "demo_shuen scene OBJ GFX resource slot0 fixed-param stub. "
        "Symmetric with load_demo_obj_resource_slot0 (0x0801398c): "
        "passes r0=0 to load_shuen_obj_resource_by_slot, then returns fixed r0=1 (load triggered). "
        "Called by play_demo_shuen (0x080bc880) and FUN_0801c254 (0x0801c254). "
        "Entry scan (5 instrs): push {lr} / movs r0,#0 / bl FUN_0801ba04 / movs r0,#1 / pop {r1}. "
        "r0 at entry is clobbered by movs r0,#0 -> no input parameter. "
        "Returns r0=u32 1 (load success/busy). "
        "Side-effects: via load_shuen_obj_resource_by_slot(0): "
        "OBJ Tile VRAM + OBJ Palette VRAM written; gDemoState anim ctrl + ImageProxy initialized."),
    ("FUN_0801ba5c", "write_shuen_bg3_scroll_regs",
        "demo_shuen scene BG3 scroll register writer. "
        "Identical structure to write_bg3_scroll_regs (0x0801399c): "
        "r0=u16 hofs [0..511], r1=u16 vofs [0..511]; each ANDed with 0x1FF (9-bit mask), "
        "then strh written to BG3HOFS (0x04000018) and BG3VOFS (0x0400001e). "
        "Callers: tick_demo_shuen_bg3_hscroll (0x0801ba78) with r0=0, r1=hofs; "
        "FUN_0801bad0 with r0=vofs, r1=0. Leaf function (bx lr). "
        "Side-effects: [BG3HOFS 0x04000018] := r0 & 0x1FF; [BG3VOFS 0x0400001e] := r1 & 0x1FF. "
        "Constants: BG3_SCROLL_MASK=0x1FF, BG3HOFS=0x04000018, BG3VOFS=0x0400001e."),
    ("FUN_0801ba78", "tick_demo_shuen_bg3_hscroll",
        "Per-frame BG3 horizontal scroll updater for demo_shuen scene. "
        "Called by demo_shuen_state_machine (0x0801bd08) each frame. "
        "Reads gDemoState+0x8C bits[23:16] (8-bit scroll counter), computes hofs = counter % 0xA0 (160px), "
        "updates counter bits[8:1] (+= 2, wraps at 256), re-wraps if > 0xA0, "
        "writes back to gDemoState+0x8C, then calls write_shuen_bg3_scroll_regs(0, new_hofs). "
        "Symmetric with tick_demo_bg3_hscroll (0x080139b8). "
        "No input params (r0 clobbered by ldr at entry). Returns void. "
        "Side-effects: [gDemoState+0x8C] bits[8:1] updated; [BG3HOFS 0x04000018] written. "
        "Constants: SCREEN_WIDTH=0xA0, COUNTER_MASK=0xFF, STEP=2."),
    ("FUN_0801bb28", "advance_shuen_cell_anim_frame",
        "Per-sprite demo cell animation frame advance for shuen scene (Shuen/SHU_main.c). "
        "Called by tick_shuen_anim_slots_batch (0x0801bbd4). "
        "r0=u8 anm_id [0..10], r1=s32 playback_step (-1=auto advance, >=0=explicit seq step), "
        "r2=s32 screen_x_fp12, r3=s32 screen_y_fp12. "
        "Validates anm_id via read_obj_id_field; out-of-range triggers suppress_assert_report "
        "(assert: 'anmID < IG2D_GetAnmSequencesCount', file='Shuen/SHU_main.c', line=0xEF). "
        "playback_step==-1: calls dispatch_cell_anim_frame_advance then dispatch_cell_anim_sequence_step; "
        "playback_step>=0: calls dispatch_cell_anim_sequence_step directly with r6 low 16 bits. "
        "Finally calls dispatch_isd_cell_anim_oam_setup to commit OAM attributes. "
        "Returns void. "
        "Side-effects: [gDemoState+0x8+anm_id*4] cell anim ptr advanced; OAM attr0/1/2 + XY written. "
        "Constants: STEP_AUTO=-1, DEFAULT_STEP=1, FAST_STEP=2, SEQ_RANGE_MAX=0xA."),
    ("FUN_0801bbd4", "tick_shuen_anim_slots_batch",
        "Per-frame batch OBJ animation slot updater for demo_shuen scene. "
        "Called by demo_shuen_state_machine (0x0801bd08) each frame. "
        "r0=u32 total_count [0..209]: divided by 11 to get valid slot ceiling. "
        "Copies 40-byte ROM coord table (0x09e3cfbf, 20 pairs) to stack via memcpy. "
        "Loops slot r5 from 0 to min(total_count/11, 19), each iteration calls "
        "advance_shuen_cell_anim_frame(slot=r5, step=-1, x=table[r5*2], y=table[r5*2+1]). "
        "Returns void. "
        "Side-effects: OBJ VRAM/OAM updated for all active sprite slots. "
        "Constants: MAX_SLOTS=0x13, GROUP_SIZE=0xB(11), COORD_TABLE=0x09e3cfbf."),
    ("FUN_0801c2ac", "reset_gl_display_state",
        "Full GL display state reset called at scene transitions. "
        "Called by FUN_0801cf74, FUN_0801cfcc, and play_ui_effect_3b (0x080bc918). "
        "No input params (r0 clobbered by movs r0,#0 at entry). Returns r0=1 (success). "
        "Sequence: (1) bios_cpu_set 32-bit fill-zero EWRAM 0x02029eb0, 192 bytes (48 words); "
        "(2) gl_clear_vram_palram_scroll; "
        "(3) writes DISPCNT(0x04000000)=0x1741 (BG mode 1, OBJ 1D, BG0+BG1+BG2+OBJ on), "
        "BG0CNT(0x04000008)=0x1D81, BG1CNT(0x0400000A)=0x1E82, BG2CNT(0x0400000C)=0x1F8B; "
        "(4) gl_set_brightness(0x3F, -16); (5) gl_state_init; (6) gl_clear_frame_callbacks. "
        "Side-effects: EWRAM 0x02029eb0..0x02029f6f zeroed; DISPCNT/BG0-2CNT written; "
        "VRAM/palette/scroll cleared; GL state and callbacks reset. "
        "Constants: DISPCNT_VAL=0x1741, BG0CNT_VAL=0x1D81, BG1CNT_VAL=0x1E82, BG2CNT_VAL=0x1F8B, "
        "ZERO_FILL_CTRL=0x05000030, BRIGHTNESS_TARGET=0x3F, BRIGHTNESS_STEP=-16."),
    ("FUN_0801c310", "load_vija_bg_gfx_embedded",
        "vija scene BG GFX loader - embedded ROM data variant. "
        "Called by load_vija_bg_gfx_by_mode (0x0801c484) when r0==0. "
        "Copies 16-byte BG resource header from ROM table 0x09e3d834 to stack (ldmia+str x4); "
        "memcpy 8-byte BG params from 0x09e3d844 to stack. "
        "Configures OAM attr fields: [r1+0x14] bits[3:0]=tile_shape, [r1+0x17] bit6=priority(0x40), "
        "[r1+0x18] bits[6:0]=tile_base_idx, [r1+0x18] bits[14:7]=palette_bank<<7. "
        "Calls apply_gfx_resource_list to write demo/vija/BG2_all.LZ BG tiles and palette to VRAM. "
        "Params: r0=u8 tile_group_index [0..12], r1=ptr oam_entry, "
        "r2=u8 tile_shape [0..15], r3=u8 tile_base_idx [0..127], [sp+0]=u8 palette_bank [0..127]. "
        "Returns void. "
        "Symmetric with load_vija_bg_gfx_from_fs (0x0801c3f4). "
        "Constants: VIJA_STATE=0x02029eb0, VIJA_BG_RES_HEADER=0x09e3d834, "
        "VIJA_BG_PARAMS=0x09e3d844, OAM_PRIORITY_BIT=0x40, OAM_TILE_MASK=0xffffc07f."),
    ("FUN_0801c3f4", "load_vija_bg_gfx_from_fs",
        "vija scene BG GFX loader - file system variant. "
        "Called by load_vija_bg_gfx_by_mode (0x0801c484) when r0==1. "
        "Non-APCS input: r8=ptr oam_entry (caller-set; entry .hword 0x4668 = mov r0,r8 overwrites APCS r0). "
        "Calls zero_struct_36bytes(r8) to clear OAM buffer, then fs_load(0x09e3d84c, 0) "
        "to load demo/vija/BG2_all.LZ and demo/vija/wija_obj_all.LZncer from filesystem. "
        "Configures OAM attr: [r1+0x14] bits[3:0]=tile_shape, [r1+0x17] bits[5:0]=0 (clears priority+flip), "
        "[r1+0x18] bits[6:0]=tile_base_idx, [r1+0x18] bits[14:7]=palette_bank<<7, "
        "[r1+0x1b] bit2=1 (OBJ enable). Calls apply_gfx_resource_list. "
        "Params: r8=ptr oam_entry (non-APCS), r2=u8 tile_shape [0..15], "
        "r3=u8 tile_base_idx [0..127], [sp+0x34]=u8 palette_bank [0..127]. Returns void. "
        "Symmetric with load_vija_bg_gfx_embedded (0x0801c310); differs in data source and attr[0x17] handling. "
        "Constants: VIJA_FS_PATH_LIST=0x09e3d84c, OAM_ATTR17_CLEAR_MASK=~0x41, "
        "OAM_TILE_MASK=0xffffc07f, OAM_OBJ_ENABLE_BIT=0x4."),
    ("FUN_0801c484", "load_vija_bg_gfx_by_mode",
        "vija scene BG GFX load dispatcher by mode. "
        "Called by FUN_0801c6b0 (bg, demo, fs) and FUN_0801cb00 (display, palette, demo, fs). "
        "r0=u8 load_mode [0..1]: 0=call load_vija_bg_gfx_embedded (ROM embedded), "
        "1=call load_vija_bg_gfx_from_fs (fs_load), other=no-op return. "
        "Forwards r1..r3 and two stack params to the selected loader unchanged. "
        "No direct VRAM side-effects; all writes performed by callees. "
        "Params: r0=load_mode, r1=u8 tile_group_index [0..3], r2=ptr oam_entry, "
        "r3=u8 tile_base_idx [0..127], [sp+0x10]=u8 palette_bank, [sp+0x14]=u8 extra_param. "
        "Returns void. "
        "Symmetric with load_shuen_sprite_gfx_guarded (0x0801b91c) across scenes."),
    ("FUN_0801c4c0", "load_vija_obj_resource_by_region",
        "vija scene OBJ resource loader selected by JP/US region variant. "
        "Called by load_vija_obj_resource_gated (0x0801c50c). "
        "r0=u8 use_us_variant [0..1]: 0=JP wija_obj_all files, 1=US wija_obj_allUS files. "
        "Copies 8 pointers from ROM table 0x09e3d964 (JP group 4 ptrs + US group 4 ptrs) to stack. "
        "Computes resource descriptor ptr: lsls r0,r0,#4 (stride=16) + add r0,sp+0x14. "
        "Calls load_g2d_obj_resource_set(VIJA_STATE, VIJA_STATE+4, VIJA_STATE+8, 0) "
        "to write NNS G2D OBJ data (CellBank/AnimBank/CharProxy/PaletteProxy) to VRAM. "
        "Returns void. "
        "Symmetric with load_shuen_obj_resource_by_slot (0x0801ba04). "
        "Constants: VIJA_STATE=0x02029eb0, VIJA_OBJ_RES_TABLE=0x09e3d964, "
        "OBJ_RESOURCE_STRIDE=0x10, OBJ_VRAM_FLAGS=0x200."),
    ("FUN_0801c50c", "load_vija_obj_resource_gated",
        "vija scene OBJ resource load entry with JP/US region gate. "
        "Called by FUN_0801cf74, FUN_0801cfcc, and play_ui_effect_3b (0x080bc918). "
        "No input params (void). Returns r0=u8 1 (always success). "
        "Reads ROM header 0x080000ae u16 high byte: if != 0x4a ('J') -> use_us_variant=1; "
        "if JP, checks [0x02006c2c] bits[2:0]: non-zero -> use_us_variant=1, else 0. "
        "Calls load_vija_obj_resource_by_region(use_us_variant). "
        "Side-effects: VRAM OBJ Tile/Palette written (via callee). "
        "Symmetric with load_shuen_obj_resource_slot0 (0x0801ba4c). "
        "Constants: ROM_REGION_CODE_ADDR=0x080000ae, REGION_CODE_JP=0x4a, "
        "GAME_STATE_REGION_FLAGS_OFFSET=0x6c2c, REGION_FLAGS_MASK=0x7."),
    ("FUN_0801c5d8", "drive_vija_obj_cell_anim",
        "vija scene NNS G2D CellAnimation driver (Vija/VIJ_main.c). "
        "Called by FUN_0801c74c and FUN_0801c794 (vija animation state machine). "
        "r0=u8 obj_slot_idx [0..N-1]: validated via read_obj_id_field; "
        "out-of-range triggers suppress_assert_report "
        "('anmID < IG2D_GetAnmSequencesCount', 'Vija/VIJ_main.c', line=0xf2). "
        "r1=s16 anim_cmd: -2=no update (OAM pos refresh only), -1=frame advance (rate 0x1000), "
        ">=0=sequence step to anim_cmd. "
        "r2=s16 x_pos, r3=s16 y_pos (pixel coords, lsls #0xc -> fp12 for OAM). "
        "[sp+0]=s32 extra_oam_param0 [0..0], [sp+4]=s32 extra_oam_param1 [0..0]. "
        "All paths end with dispatch_isd_cell_anim_oam_setup. Returns void. "
        "Side-effects: OAM updated; CellAnim internal state advanced. "
        "Constants: VIJA_STATE=0x02029eb0, ANIM_CMD_NO_UPDATE=-2, "
        "ANIM_CMD_FRAME_ADVANCE=-1, FRAME_ADVANCE_RATE=0x1000."),
    ("FUN_0801c668", "apply_bg2_affine_fixed_angle",
        "Apply rotation+scale affine transform to BG2 at fixed scale with given angle. "
        "Called by tick_bg2_affine_anim_frame (0x0801c694) with angle from frame counter byte. "
        "r0=u8 angle [0..255] (256 steps per revolution). "
        "Builds apply_bg_affine_by_angle_scale param block on stack: "
        "bg_index=2, angle=r0, scale_x=0x40, scale_y=0x40 (1:1 no stretch), "
        "pivot_x = 0x40-0x78+0x28 = -0x10 (left-of-screen rotation center). "
        "Calls apply_bg_affine_by_angle_scale (0x08015868) which writes BG2PA/PB/PC/PD/X/Y. "
        "Returns void. "
        "Side-effects: [0x04000020] BG2PA, [0x04000022] BG2PB, [0x04000024] BG2PC, "
        "[0x04000026] BG2PD, [0x04000028] BG2X, [0x0400002c] BG2Y written."),
    ("FUN_0801c694", "tick_bg2_affine_anim_frame",
        "Per-frame BG2 affine rotation tick for play_ui_effect_3b scene. "
        "Called by FUN_0801cb00 (display, palette, demo, fs) each frame. "
        "No input params (r0 unused; first instruction is ldr r1,DAT). "
        "Reads IWRAM 0x02029eb0+0x90 frame counter byte, increments it (u8 natural wrap), "
        "zero-extends old value (lsls/lsrs #0x18) -> angle, "
        "then calls apply_bg2_affine_fixed_angle(angle). Returns void. "
        "Side-effects: [0x02029eb0+0x90] incremented; BG2 affine regs updated via callee."),
    ("FUN_0801c6b0", "tick_bg_scroll_anim_frame",
        "Per-frame BG scroll and tile animation tick for play_ui_effect_3b scene. "
        "Called by FUN_0801cb00 (display, palette, demo, fs) each frame. "
        "r0=u32 tick_count (frame counter from IWRAM 0x02029eb0, passed by caller). "
        "Triggers update only when tick_count mod 13 == 0; otherwise returns immediately. "
        "On trigger: memcpy 4-byte ROM anim params from 0x09e3d9cf to stack; "
        "increments [0x02029eb0+0x91] sub-frame index AND 0x3 (4-frame cycle [0..3]); "
        "calls load_vija_bg_gfx_by_mode(mode=0) for OBJ/tile update; "
        "writes BG0VOFS (0x04000012) = 4. "
        "Returns void. "
        "Side-effects: [0x02029eb0+0x91] updated; [BG0VOFS 0x04000012] := 4; "
        "OBJ/tile VRAM via load_vija_bg_gfx_by_mode. "
        "Constants: MOD_PERIOD=13, SUB_FRAME_MASK=0x3, BG0VOFS=0x04000012, BG0VOFS_VAL=4."),
    ("FUN_0801c728", "advance_scene_phase_counter",
        "Scene internal 2-level phase counter advance. "
        "Called by FUN_0801c794 (play_ui_effect_3b state machine); return value used for dispatch. "
        "r0=void* pSceneState: byte[2]=phase tick count [0..7], byte[3]=phase index [0..3]. "
        "If byte[2]==7 (phase tick complete): increments byte[3] AND 0x3 (4-phase cycle), clears byte[2]=0. "
        "Else: increments byte[2]. "
        "Returns r0=u8 phase_index = byte[r0+3] [0..3]. "
        "Leaf function (no callees). "
        "Side-effects: [r0+2] and [r0+3] updated."),
    ("FUN_0801c74c", "update_dual_cell_anim_oam_pos",
        "Update two ISD cell animation OAM entries simultaneously. "
        "Called by FUN_0801c794 (play_ui_effect_3b state machine). "
        "r0=u8 base_obj_index [0..7] (bits[2:0] of [r7+4], extracted by caller; 2nd call uses r0+3), "
        "r1=s16 sequence_idx [0..4], r2=s16 x_pos_px, r3=s16 y_pos_px. "
        "Subtracts 0x10 from x and y (center anchor), then calls drive_vija_obj_cell_anim twice: "
        "first with obj_index=2, second with obj_index=base_obj_index+3; same sequence_idx and coords. "
        "[sp+0]=0, [sp+4]=0 for both calls. Returns void. "
        "Side-effects: OAM slots [obj_index=2] and [obj_index=r0+3] updated via drive_vija_obj_cell_anim "
        "-> dispatch_isd_cell_anim_oam_setup."),

    # 2026-05-07: campaign-10 batch (topo=170..265 subset) vija scene + card list + sound + duel core
    ("FUN_0801c794", "tick_vija_obj_anim_slot",
        "vija scene OBJ slot per-frame animation state machine tick. "
        "Called by tick_all_vija_obj_anim_slots (FUN_0801cadc) with stride=8 for each of 5 slot ctrl blocks "
        "at IWRAM 0x02029eb0+0x98+i*8 (i=[0..4]). "
        "r0=u8* slot_ctrl_ptr: byte[0]=phase [0..0x1e], byte[1]=sub-counter/seq-idx. "
        "Outer switch routes by phase; inner switch maps to x-coord variant (0x30/0x50 px). "
        "Active phases (1/0xa/3/0x1e/4/5): interpolate x/y from sub-counter, call drive_vija_obj_cell_anim. "
        "Phase 2: call advance_scene_phase_counter then update_dual_cell_anim_oam_pos. "
        "Phase 5: call drive_vija_obj_cell_anim twice with fixed x=-1, y=0x78, z=0x50, then exit. "
        "Phase 0 and invalid phases: return immediately. "
        "Side-effects: slot_ctrl_ptr byte[0]/byte[1] updated; OAM entry for active slot written. "
        "Constants: PHASE_MAX=0x1e, X_VARIANT_A=0x30, X_VARIANT_B=0x50, SIN_TABLE=0x09e399d0."),
    ("FUN_0801cadc", "tick_all_vija_obj_anim_slots",
        "vija scene batch per-frame tick for all 5 OBJ animation slots. "
        "Loops i=[0..4] over IWRAM 0x02029eb0+0x98 with stride=8, calling tick_vija_obj_anim_slot(ptr) per slot. "
        "No parameters; returns void. "
        "Called by run_vija_scene_state_machine (FUN_0801cb00) in phase 4 (active anim) and phase 7 (transition). "
        "Constants: SLOT_BASE_OFFSET=0x98, SLOT_STRIDE=8, SLOT_COUNT=5."),
    ("FUN_0801cb00", "run_vija_scene_state_machine",
        "vija scene (play_ui_effect_3b) per-frame state machine driver. "
        "No parameters; all state from IWRAM 0x02029eb0. "
        "10-phase dispatch (phases 0-9): "
        "phase 0: init display regs (DISPCNT/BGxCNT), load BG+OBJ gfx, clear palette, init 5 OBJ slots; "
        "phase 1: check blend done, start fade-in; "
        "phase 2/3: advance blend, check affine init; "
        "phase 4: tick_all_vija_obj_anim_slots + tick_bg_scroll_anim_frame + tick_bg2_affine_anim_frame each frame; "
        "phase 5: start fade-out blend; phase 6: tick blend; "
        "phase 7: tick_all_vija_obj_anim_slots + check fade; "
        "phase 8/9: epilogue return 1. "
        "Returns r0=1 (scene done) or r0=0 (scene continue). "
        "Side-effects: DISPCNT/BG0-2CNT/palette VRAM, OAM, IWRAM state fields. "
        "Constants: VIJA_STATE=0x02029eb0, DISPCNT_INIT=0x1741, SLOT_COUNT=5."),
    ("FUN_0801e6f4", "open_card_info_page_from_list",
        "Transition entry called by card_list scene dispatchers (FUN_080c64b8 state=0, FUN_080d2c60 state=0) "
        "when player selects a card in the list to view its info page. "
        "Zero-extends card_id (r0) and origin_page (r1=0) to u16, calls card_list_on_select_to_info_page; "
        "then sets [0x0201afb0+0x0] bit2 (0x4) to mark card_info_page_active_flag. "
        "r0=u16 card_id, r1=u16 origin_page, r2=ptr, r3=ptr. Returns void. "
        "Constants: 0x4=[0x0201afb0+0x0] bit2 = card_info_page_active_flag."),
    ("FUN_0801e850", "fill_card_fs_display_entries",
        "Reads card FS data block (base 0x0201e2b4, stride=0x108, indexed by r0=slot_index) "
        "and fills up to three sub-arrays of display entries (halfword) into the target buffer at r1. "
        "Sub-array counts stored at [r1+0x18], [r1+0x19], [r1+0x1a]; "
        "entries sourced from card_stats_table and mapping table at 0x0201ff60. "
        "Callers: fill_card_fs_display_entries_for_card_list (fixed r1=0x02001138), "
        "FUN_0802752c, FUN_0802803c. "
        "Clears three word fields at r1 before filling (init write cursors). No return value (void). "
        "r0=u8 slot_index [0..1], r1=ptr display_buffer. "
        "Constants: 0x108=card FS data block stride (slot*0x108=slot*33*8)."),
    ("FUN_0801e974", "fill_card_fs_display_entries_for_card_list",
        "Specialized wrapper for fill_card_fs_display_entries (FUN_0801e850) that fixes "
        "the second argument to 0x02001138 (card_list slot display buffer EWRAM address) "
        "and forwards r0 (slot_index) unchanged. "
        "Called by FUN_0802752c to write card FS data into the card_list slot display buffer. "
        "No computation logic; single ldr overwrites r1 then jumps to core function. "
        "r0=u8 slot_index [0..1]. Returns void."),
    ("FUN_0810d0a4", "write_sound_engine_request",
        "Writes a request byte to the IWRAM sound engine management struct (base 0x030050cc) "
        "and clears the adjacent status byte: "
        "[0x030050cc+0x381] := 0 (status/ack byte cleared), [0x030050cc+0x380] := r0 (request_code). "
        "Called by request_sound_engine_code10 (FUN_080f9b40, r0=0x10) and FUN_080f9b4c (transparent r0). "
        "r0=u8 request_code [0..0xff]. Returns void. "
        "Constants: 0x030050cc=sound engine IWRAM struct base; 0x380=request code byte offset; "
        "0x381=status/ack byte offset."),
    ("FUN_080f9b40", "request_sound_engine_code10",
        "Specialized wrapper for write_sound_engine_request (FUN_0810d0a4) with fixed request_code=0x10. "
        "No parameters. Returns void. "
        "Called by scene_duel_puzzle state machine branches (0x080bd06c, 0x080bd334, 0x080bd5fe, "
        "0x080bd812, 0x080cc884, 0x0801ea08 -- 6 callsites), all at blend-fade transition completion nodes. "
        "Body: movs r0,#0x10; bl write_sound_engine_request. "
        "Semantic: trigger sound engine opcode 0x10 at scene-transition checkpoint."),
    ("FUN_080f2c8c", "render_decimal_digits_jp",
        "Renders unsigned integer r3 as decimal digits right-to-left into JP font line buffer. "
        "Per digit: r3 %% 10 via __modsi3, +0x30 -> char code, bl render_glyph_jp_single_layer, "
        "r3 /= 10 via __divsi3, x -= width (width: [0x02006ed0+0x8] bit0 == 0 -> 10px JP; 1 -> 5px ASCII). "
        "Loop until quotient is 0. "
        "r0=u16 x_pos [0..239], r1=u8 y_row [0..31], r2=u16 color_attr, r3=u32 decimal_value. Returns void. "
        "Callers: render_duel_field_zone_info, FUN_080d912c, FUN_080dba64, FUN_080de2bc "
        "(LP/ATK/DEF numeric field rendering, typically called twice: main color + shadow color). "
        "Constants: 0x30=ASCII digit base ('0'); 0x02006ed0+0x8=gSettings character width flag."),
    ("FUN_08037b90", "get_player_deck_flag_bit1",
        "Returns bit1 of the deck status word for the specified player. "
        "r0 bit0 selects player index (0=P1, 1=P2); stride 0x868 locates player struct; "
        "offset +0x11c (=0x8e*2) reads 32-bit status word, lsrs #1 extracts bit1. "
        "r0=u32 packed_player_id (bit0=player index [0..1]). Returns u32 (0 or 1). "
        "Callers: FUN_08037c20 (duel_field, skip-deck-sort check); "
        "get_zone_card_attribute_by_type case_b (conditional return 0/1 based on entity match). "
        "Constants: 0x868=player struct stride, 0x11c=deck_status_word_offset."),
    ("FUN_0802fd60", "find_effect_node_in_zone",
        "Searches the slot chain for a node matching effect_code ([node+0]==r2), "
        "entity_id ([node+4]==r3), and valid zone_type ([node+2]&0xF<=5). "
        "Player slot address: 0x0201c510 + (r0 bit0)*0x868 + r1*20; [slot+0xa]=chain head index. "
        "Node pool: EWRAM 0x0201d9c0, stride 8 bytes. Returns 1 if found, 0 if not. "
        "r0=u32 packed_player_id, r1=u32 slot_index [0..0xb], r2=u16 effect_code, r3=u16 entity_id. "
        "Callers: FUN_08033730 (duel_field effect activation check); "
        "get_zone_card_attribute_by_type case_d (slot 0xb effect presence check). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=20 bytes."),
    ("FUN_0803b618", "get_zone_card_attribute_by_type",
        "Dispatches on zone_type_code (r1, [0xb..0xf]) across 5 cases to read a card attribute for player r0. "
        "case_b (0xb): entity ID match check then get_player_deck_flag_bit1. "
        "case_c (0xc): returns 0 fixed. "
        "case_d (0xd): reads bit field from 0x0201c740 table then calls find_effect_node_in_zone. "
        "case_e (0xe): returns 1 fixed. "
        "case_f (0xf): reads [gP1LifePoints+0x788+slot*2] byte; ==0x40 -> return bit[9]; "
        "==0x80 -> return 0; other -> return 1. "
        "default: reads u16 at [+8] from 0x0201bc54 or 0x0201c510 table. "
        "r0=u32 packed_player_id, r1=u32 zone_type_code [0xb..0xf], r2=u32 slot_or_card_index [0..9]. "
        "Returns u16 card attribute value. "
        "Constants: 0x868=player stride; 0x0201c740=gP1CardZone base; 0x12a1=case_d field offset; "
        "0x788=case_f LifePoints offset; 0x0201bc54=default table base; "
        "0x40=case_f threshold A (bit6); 0x80=case_f threshold B (bit7)."),
    ("FUN_0802fb2c", "find_node_by_value_and_zone_type",
        "Traverses EWRAM node pool (0x0201d9c0, stride 8 bytes) via linked list, "
        "returning first node ptr where [node+0]==value (r1) and [node+2]&0xF==zone_type (r2, [0..5]). "
        "r0=u32 head_index [1..139] (0=empty list -> return NULL). "
        "Node layout: [+0]=u16 value, [+2]=type_byte (low 4 bits=zone_type), [+6]=u16 next_index, stride 8. "
        "Returns u32* node pointer or NULL (0) if not found. "
        "Leaf function (no callees). "
        "Callers: check_node_in_slot_chain (FUN_0802fdc0), FUN_0802fe98, FUN_0802ff34, FUN_0802ff84. "
        "Constants: 0x0201d9c0=node pool base, NODE_STRIDE=8, ZONE_TYPE_MAX=5."),
    ("FUN_0802fdc0", "check_node_in_slot_chain",
        "Computes slot entry address (0x0201c510 + (r0 bit0)*0x868 + r1*20), "
        "reads [slot+0xa] chain head index, then calls find_node_by_value_and_zone_type "
        "with r2=value and r3=zone_type to search EWRAM node pool (0x0201d9c0). "
        "Returns 1 if matching node found, 0 otherwise. "
        "Simplified variant of find_effect_node_in_zone (FUN_0802fd60) -- "
        "that function additionally checks [node+4]==entity_id; this one only does dual-field match. "
        "r0=u32 packed_player_id, r1=u32 slot_index [0..0xb], r2=u16 card_id, r3=u8 zone_type [0..5]. "
        "Returns u32 bool. "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=20 bytes."),
    ("FUN_080eeea8", "get_card_extended_stat_field8",
        "Reads field[8] (u16) from the ROM extended card attribute table for a given card_id. "
        "Sibling of 0x080eedf8..0x080eeed4 cluster; each function differs only in the field index N "
        "in 'adds r0,#N'; this one uses N=8. "
        "card_id <= 0x0fa6 (normal card upper bound 4006) -> returns 0. "
        "Otherwise: row = card_id - 0xfa7; offset = row*11 + 8; reads u16 from ROM table 0x09821e04. "
        "r0=u16 card_id. Returns u16 extended_stat_field8. "
        "Callers: FUN_0804a9dc (card type classifier), check_card_field8_is_normal (FUN_0804ad70). "
        "Constants: 0x0fa6=normal card upper bound, 0x09821e04=extended stat table base, field_stride=11."),
    ("FUN_0804ad70", "check_card_field8_is_normal",
        "Calls get_card_extended_stat_field8 for r0=card_id, subtracts 1, "
        "uses result as 0..11 index into 12-entry switch table. "
        "indices {0,2,4,5,6,7,9,10,11} (field8 in {1,3,5,6,7,8,10,11,12}) -> return 1 (normal). "
        "indices {1,3,8} (field8 in {2,4,9}) -> return 0 (abnormal). "
        "field8=0 (normal card or out-of-range): 0-1=0xffffffff, bhi default -> return 0. "
        "Semantic: field8 in {2,4,9} = abnormal extended types (return 0); all others = normal (return 1). "
        "r0=u16 card_id. Returns bool is_normal_field8. "
        "Callers: check_slot_card_is_equip_type (FUN_08030aa4), multiple 0x0804/0x0805/0x0806 duel scenes."),
    ("FUN_08030aa4", "check_slot_card_is_equip_type",
        "Reads EWRAM duel slot (0x0201c510 + (r0 bit0)*0x868 + r1*20), extracts low 13 bits as card_id. "
        "Compares card_id against whitelist {0x172f, 0x1636, 0x1809, 0x1472}: "
        "match -> call check_node_in_slot_chain(side, slot, 0x1472, 5) and return its result. "
        "No match -> call check_card_field8_is_normal(card_id) for field8 extended type check. "
        "r0=u32 player_side (bit0), r1=u32 slot_idx [0..4]. Returns bool is_equip_type. "
        "Callers: duel_field FUN_08030b0c (card_type==8 guard), 0x080364b0, 0x08050c58, "
        "0x08051318, 0x08091888. "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=20 bytes, "
        "0x172f/0x1809/0x1472=equip/magic card ID whitelist, "
        "0x1636=second ID (=0x172f-0xf9, DAT_08030a6c asm:47150)."),
    ("FUN_08032358", "classify_card_effect_category",
        "Maps card_id (r0) to an effect category code [1..0x17] (23 categories) via multi-level cmp/beq tree. "
        "Hardcoded whitelist includes ~20+ specific card_ids: "
        "0x1348/0x10f5/0x10f3/0x10f1/0x10f2/0x1345/0x1346/0x169f/0x14d1/0x1349/ "
        "0x149c/0x150b/0x159d/0x1477/0x175e/0x187f/0x18ff and others. "
        "card_id not in whitelist -> returns 0. "
        "r0=u16 card_id. Returns u8 effect_category [1..0x17] or 0. "
        "Callers: check_card_matches_active_effect_slot (FUN_0803412c), FUN_0804074c (duel hub), "
        "0x0808db90, 0x080c8f48."),
    ("FUN_0803412c", "check_card_matches_active_effect_slot",
        "Checks if card_id matches the effect category stored in the active effect slot "
        "at gP1LifePoints+0x10d8 (=0x0201D5B8). "
        "Special case: card_id==0x10f4 -> substitute reference card 0x150b for category lookup. "
        "General: call classify_card_effect_category(card_id), compare result against [0x0201D5B8]; "
        "return 1 if equal, 0 if not. "
        "r0=u16 card_id. Returns bool matches_active_effect. "
        "indeg=13; core predicate used by duel rule engine across 0x0803xx/0x0805xx/0x0809xx and hub FUN_0804074c. "
        "Constants: 0x10f4=special card needing proxy; 0x150b=proxy reference card; "
        "0x0201D5B8=active effect slot category address (gP1LifePoints+0x10d8)."),
    ("FUN_0802f434", "count_slot_equip_list_matches",
        "Reads [slot+0xa] equip chain head from EWRAM slot "
        "(0x0201c510 + (r0 bit0)*0x868 + r1*20); returns 0 if chain is empty. "
        "Otherwise traverses 8-byte node list (base 0x0201d9c0) counting nodes matching "
        "r2/r9 (ref_card_id_a) and r3/r8 (ref_card_id_b) multi-field conditions. "
        "Non-APCS inputs: r8=ref_card_id_b, r9=ref_card_id_a (caller-set high registers). "
        "r0=u32 player_side, r1=u32 slot_idx [0..4], r2=u16 ref_card_id_a, r3=u16 ref_card_id_b. "
        "Returns u32 match_count. "
        "Callers: FUN_0802f3e0 (direct upstream count-path selector), "
        "0x080364b0/0x080352b0 (duel rule core). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x14b0=equip node pool offset "
        "(gDuelFieldSlots+0x14b0=0x0201D9C0), slot+0xa=u16 chain head, node_stride=8."),
    # --- batch #11 (campaign-11, topo 266-286) ---
    ("FUN_080eedf8", "get_card_extended_stat_field6",
        "Reads field6 (u16) from ROM extended card stat table for given card_id. "
        "card_id <= 0x0fa6 (normal card upper bound 4006) -> returns 0 immediately. "
        "Otherwise: row = card_id - 0xfa7; byte_offset = (row*11 + 6)*2; "
        "reads u16 at 0x09821e04 + byte_offset. "
        "Member of the field5/field6/field7/field8/field9 getter cluster in same translation unit; "
        "functions differ only in the 'adds r0,#N' constant; this function has N=6. "
        "Callers compare return value against 0x16(22)/0x17(23), suggesting field6 encodes an "
        "extended card attribute type code (e.g. spell/trap subclass). "
        "r0=u16 card_id. Returns u16 extended_stat_field6 (0 if card_id <= 0x0fa6). "
        "Constants: 0x0fa6=normal card id upper bound, 0x09821e04=extended stat table base, "
        "stride=11 fields/row, field_index=6."),
    ("FUN_080eee24", "get_card_extended_stat_field7",
        "Reads field7 (u16) from ROM extended card stat table for given card_id. "
        "card_id <= 0x0fa6 -> returns 0. "
        "Otherwise: row = card_id - 0xfa7; byte_offset = (row*11 + 7)*2; "
        "reads u16 at 0x09821e04 + byte_offset. "
        "Member of the field5..field9 getter cluster; this function has N=7 in 'adds r0,#N'. "
        "Caller 0x08030b70 compares return value against r4 (equality check), "
        "suggesting field7 is used for card subtype matching queries. "
        "r0=u16 card_id. Returns u16 extended_stat_field7 (0 if card_id <= 0x0fa6). "
        "Constants: 0x0fa6=normal card id upper bound, 0x09821e04=extended stat table base, "
        "stride=11, field_index=7."),
    ("FUN_080eee50", "get_card_extended_stat_field5",
        "Reads field5 (u16) from ROM extended card stat table for given card_id. "
        "card_id <= 0x0fa6 -> returns 0. "
        "Otherwise: row = card_id - 0xfa7; byte_offset = (row*11 + 5)*2; "
        "reads u16 at 0x09821e04 + byte_offset. "
        "Member of the field5..field9 getter cluster; this function has N=5 in 'adds r0,#N'. "
        "Directly called by bool wrapper check_card_field5_is_nonzero (0x0804ad48); "
        "caller 0x08037b34 compares return value against r8 (<), implying field5 is a "
        "numeric count/score attribute. "
        "r0=u16 card_id. Returns u16 extended_stat_field5 (0 if card_id <= 0x0fa6). "
        "Constants: 0x0fa6=normal card id upper bound, 0x09821e04=extended stat table base, "
        "stride=11, field_index=5."),
    ("FUN_080eee7c", "get_card_extended_stat_field9",
        "Reads field9 (u16) from ROM extended card stat table for given card_id. "
        "card_id <= 0x0fa6 -> returns 0. "
        "Otherwise: row = card_id - 0xfa7; byte_offset = (row*11 + 9)*2; "
        "reads u16 at 0x09821e04 + byte_offset. "
        "Member of the field5..field9 getter cluster; this function has N=9 in 'adds r0,#N'. "
        "Caller 0x0803026c compares result against 0x1; callers 0x08032654/0x0803279c compare "
        "against 0x2, suggesting field9 is a small-integer enum code (e.g. card rank or class flag). "
        "r0=u16 card_id. Returns u16 extended_stat_field9 (0 if card_id <= 0x0fa6). "
        "Constants: 0x0fa6=normal card id upper bound, 0x09821e04=extended stat table base, "
        "stride=11, field_index=9."),
    ("FUN_0804ad48", "check_card_field5_is_nonzero",
        "Bool wrapper for get_card_extended_stat_field5. "
        "Calls get_card_extended_stat_field5(card_id); if result > 0 returns 1, else returns 0. "
        "Direct bool layer over the field5 getter; no extra parameters. "
        "Adjacent sibling FUN_0804ad5c applies similar conversion for field8 (but inverted: ==0->1). "
        "indeg=135; all callers consume result with 'cmp r0,#0; beq/bne' for boolean filtering. "
        "r0=u16 card_id [0..0x1770]. Returns bool (u32): 1 if field5>0, 0 if field5==0 or card_id<=0x0fa6. "
        "Constants: none new (card_id passed through to get_card_extended_stat_field5)."),
    ("FUN_080364b0", "check_slot_card_effect_eligibility",
        "Checks whether the card in player_side:slot_idx qualifies for effect activation. "
        "Guards: card_id != 0, slot_idx <= 4, [0x0201B750]==0 (phase lock), [slot+0x8]!=0. "
        "If guards pass, compares card_id against ~10 specific magic/trap card ID whitelist, "
        "then calls check_card_matches_active_effect_slot / count_slot_equip_list_matches / "
        "check_slot_card_is_equip_type / FUN_0803279c / FUN_08032654; "
        "accumulates results into r7 via OR. "
        "Returns 0 (not eligible), 2 (equip chain hit), or 3 (special effect hit). "
        "Sibling FUN_08036674 handles a separate card ID whitelist; both share the same caller set. "
        "r0=u32 player_side, r1=u32 slot_idx [0..4]. Returns u32 eligibility_flags. "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=20 bytes, "
        "0x0201b290=gDuelPhaseFlags base, 0x4C0=phase flag offset, "
        "0x1709/0x13cd/0x12a8/0x164e/0x17d3/0x1814/0x181a=whitelist card IDs, "
        "0x10f4=proxy card ID for check_card_matches_active_effect_slot, "
        "0x1693=count_slot_equip_list_matches ref_card_id, "
        "0x1667=FUN_0803279c param, 0x17a1=FUN_08032654 param."),
    ("FUN_08036658", "query_slot_effect_eligibility_nonzero",
        "9-instruction thin wrapper over check_slot_card_effect_eligibility. "
        "Calls check_slot_card_effect_eligibility(r0, r1, r2), then tests "
        "(result & (r2+1)) > 0: returns 1 if any masked bit is set, 0 otherwise. "
        "Normalizes the multi-value eligibility result to a bool using a caller-supplied mask. "
        "r2 is the mask-minus-1 value (0 -> mask=1 tests bit0; 1 -> mask=2 tests bit1). "
        "r0=u32 player_side, r1=u32 slot_idx [0..4], r2=u32 result_mask_minus1. "
        "Returns u32 bool (0=mask not hit; 1=mask hit). "
        "Constants: all inherited from check_slot_card_effect_eligibility."),
    ("FUN_08036674", "check_slot_card_fieldspell_eligibility",
        "Sibling of check_slot_card_effect_eligibility sharing the same 4 callers. "
        "Checks player_side:slot_idx card effect eligibility for a smaller card ID whitelist "
        "(only 0x194e and 0x194e+0x75=0x19c3). "
        "Same entry guards: card_id!=0, slot_idx<=4, [0x0201B750]==0, [slot+0x8]!=0. "
        "Reads slot+0x10 equip word and checks bit5/bit1 both 0. "
        "Compares card_id against 0x194e/0x19c3; hit -> returns 3, no hit -> returns 0. "
        "Pure leaf function (no callees). Corresponds to field-spell type card effect check. "
        "r0=u32 player_side, r1=u32 slot_idx [0..4]. Returns u32 eligibility (0 or 3). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, "
        "0x0201b290=gDuelPhaseFlags, 0x4C0=phase flag offset, "
        "0x194e=field-spell card ID 1, 0x19c3=field-spell card ID 2 (=0x194e+0x75)."),
    ("FUN_0803aed0", "resolve_slot_chain_best_target",
        "Locates the best-match node in the equip chain for player_side:slot_idx. "
        "Calls check_slot_card_effect_eligibility and check_slot_card_fieldspell_eligibility, "
        "caches flags on stack. Returns 0 immediately if output_ptr (r2) is NULL. "
        "Otherwise calls get_card_extended_stat_field7 to get a source stat, "
        "then iterates [slot+0xa] equip chain (base 0x0201D9C0, stride=0x14). "
        "For each candidate node checks card_type / equip_word bit5/bit1 / card_id conditions "
        "and numeric stat comparison; tracks the node with the highest stat value. "
        "Writes best_target_value to *r2; returns best node pointer (0 if no match). "
        "r0=u32 player_side, r1=u32 slot_idx [0..4], r2=u32* output_ptr (NULL -> return 0). "
        "Returns u32 result_ptr (0=not found; non-zero=best target node value or fn ptr). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, "
        "0x0201d9c0=gEquipNodePool (=gDuelFieldSlots+0x14b0), node_stride=0x14, "
        "0xb8f80000=card_type sentinel (card_type==0x15E7 gate)."),
    ("FUN_0803b1b0", "compute_slot_zone_eligibility_mask",
        "Queries the zone availability bitmask for player_side:slot_idx. "
        "Main path: calls resolve_slot_chain_best_target(r5,r4,sp); "
        "if *sp (best_target) non-zero, returns 1<<r7 (bit at best-target index). "
        "Secondary path (best_target==0): reads slot card_id vs 0x18c7/0x19ef whitelist, "
        "checks equip_word bit5/bit1 and chain head; if all conditions met, "
        "returns (r4_bit_pos<<r7)|0x78, else returns 1<<r7. "
        "Callers (e.g. 0x08059a78 tags: card_stats/duel_field) use this mask to determine "
        "which field zones are valid for the current effect. "
        "r0=u32 player_side, r1=u32 slot_idx [0..4]. "
        "Returns u32 zone_eligibility_mask (1<<r7 or (1<<r7)|0x78). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, "
        "0x18c7/0x19ef=special effect card ID whitelist, "
        "0x78=0b01111000 (zone flag bits 3..6)."),
    ("FUN_080314d4", "resolve_slot_card_id_for_pair",
        "Reads the effective card_id for pairing checks from gDuelFieldSlots[side][slot_idx]. "
        "r0 low bit = player_side, r1 = slot_index, r2 = default_id (returned if slot is empty). "
        "Extracts low 13 bits (card_id) from slot word[0]. "
        "If card_id == 0x19a6 or 0x19bc (=0x19a6+0x16), checks slot+0x10 bit5/bit1 (pairing "
        "disable flags) and slot+0x8 hword; if flags both 0 and hword != 0, returns paired "
        "substitute ID (0x18f9 for 0x19a6, 0x18f6 for 0x19bc). "
        "Any non-special slot returns original card_id; empty slot returns r2. Read-only. "
        "r0=u8 side_and_flags (bit0=player_side), r1=u16 slot_index [0..0x44], "
        "r2=u32 default_id. Returns u16 effective_card_id. "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, stride 0x14=slot entry, "
        "0x19a6=special card ID A, 0x19bc=0x19a6+0x16=special card ID B, "
        "0x18f9=paired substitute for A, 0x18f6=paired substitute for B."),
    ("FUN_08031564", "check_slot_card_pair_allowed",
        "High-frequency thin dispatch (indeg=14) for pairing validation. "
        "Calls resolve_slot_card_id_for_pair(r0=side, r1=slot_idx, r2=candidate_card_id) to "
        "extract the effective card_id (including special-card substitution), then calls "
        "check_card_pair_allowed(resolved_id, candidate_card_id) for whitelist check. "
        "r2 serves dual purpose: default fallback ID for resolve_slot_card_id_for_pair "
        "and pairing candidate for check_card_pair_allowed. "
        "Returns check_card_pair_allowed result (1=allowed, 0=rejected). Read-only. "
        "r0=u8 side_and_flags (bit0=player_side), r1=u16 slot_index [0..0x44], "
        "r2=u16 candidate_card_id. Returns u32 (1=pair allowed, 0=rejected)."),
    ("FUN_08032548", "test_slot_has_active_card",
        "Ultra-high-frequency utility (indeg=57) called by nearly all duel field logic modules. "
        "Checks whether the specified slot (r0 bit0=player_side, r1=slot_index) is active "
        "and holds the target card (r2=card_id). "
        "Three conditions must all be true to return 1: "
        "(1) slot.word[0] low 13 bits == r2 (exact card_id match); "
        "(2) slot.hword[0x8] != 0 (active field non-zero); "
        "(3) slot.word[0x10] bit5==0 AND bit1==0 (no pairing-disable flags). "
        "Read-only. "
        "r0=u8 side_flags (bit0=player_side), r1=u16 slot_index [0..0x44], "
        "r2=u16 card_id. Returns u32 (1=slot active with card, 0=not). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=0x14 bytes, "
        "slot+0x0=card_id word, slot+0x8=active hword, slot+0x10=flag word (bit5/bit1)."),
    ("FUN_08032654", "count_available_effect_zones",
        "Ultra-high-frequency utility (indeg=59) for effect placement checking. "
        "Counts how many effect zone slots for the given card (r1=card_id) on player side (r0) "
        "are not yet occupied, excluding exclude_slot (r2=-1 means no exclusion). "
        "First calls check_card_field5_is_nonzero(card_id) to determine search region: "
        "  has field5: scans 5 slots at gDuelFieldSlots+0x10a4 offset, "
        "              checks card_id match, pairing flags, active bit, and bitmask (1<<(side*16+slot_idx)); "
        "              counts unoccupied. "
        "  no field5: calls get_card_extended_stat_field9(card_id); if field9==2 checks single "
        "              slot at 0x0201c5d8; else scans gDuelFieldSlots base r3=0..9. "
        "Returns r8 = available effect zone count (non-zero -> effect activation allowed). "
        "r0=u8 side_flags, r1=u16 card_id, r2=s32 exclude_slot [0..0x44 or -1]. "
        "Returns u32 available_count. "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x10a4=effect zone partition offset, "
        "0x0201c5d8=gDuelFieldSlots+0xc8=slot[10], 0x868=player stride, slot_entry=0x14."),
    ("FUN_08034180", "find_paired_zone_entry_for_card",
        "Medium-frequency utility (indeg=12) for paired effect zone lookup. "
        "Checks whether a zone entry paired with the input slot (r0=side, r1=slot_idx) exists. "
        "Steps: (1) verify input slot has a card (card_id != 0), else return 0. "
        "(2) Outer loop (2 iterations) over two effect zone base offsets. "
        "(3) Inner loop (r9=0..9) over 10 slots: checks card_id==0x1368 (target special card), "
        "calls query_slot_effect_eligibility_nonzero for active state, "
        "calls check_slot_card_pair_allowed to verify 0x1368 card pairs with entry slot card, "
        "calls find_effect_node_in_zone to confirm effect node exists. "
        "All conditions met -> returns 1. No match found -> returns 0. Read-only. "
        "r0=u32 side_flags (bit0=player_side, stored in r8), r1=u16 slot_index [0..0x44] (stored in r7). "
        "Returns u32 (1=paired zone entry found, 0=not found). "
        "Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride, slot_entry=0x14, "
        "0x1368=target special card ID, inner loop r9=0..9, outer loop count=2."),
    ("FUN_0803ac04", "query_slot_card_state_code",
        "Queries the combined state code for the card in duel field player_side:slot_idx. "
        "r0=player_side, r1=slot_idx [0..4], r2=mode_flags (-1 = full-scan mode). "
        "Reads card_id (low 13 bits) from gDuelFieldSlots[player][slot_idx]; returns 0 if empty. "
        "Calls check_slot_card_effect_eligibility(player, slot_idx) and "
        "check_slot_card_fieldspell_eligibility(player, slot_idx) for attribute sets A and B. "
        "Calls get_card_extended_stat_field6(card_id) for extended attribute classification. "
        "In a double loop (2 players x 5 slots) scans effect node pool (0x0201d9c0), "
        "matching card ID constants and setting r7 (state code) by match type. "
        "Returns low 16 bits of r7. "
        "r0=u32 player_side (bit0, stored in r10), r1=u32 slot_idx [0..4], "
        "r2=s32 mode_flags (-1=full scan). Returns u16 state_code "
        "(0=empty slot or no match; non-zero=matched state category, e.g. 0xe/0x14/0x2/0x7). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=20, "
        "effect_node_pool=0x0201d9c0."),
    ("FUN_0803abf0", "get_slot_card_state_code",
        "Thin wrapper (indeg=44) calling query_slot_card_state_code with r2=-1 (full-scan mode). "
        "r0=player_side, r1=slot_idx [0..4]; sets r2=-1 via 'movs r2,#1; rsbs r2,r2,#0', "
        "then calls query_slot_card_state_code, truncates result to u16. "
        "High-frequency call site in duel field system; callers use result in slot iteration "
        "loops to compare state_code against card_id or state thresholds. "
        "r0=u32 player_side, r1=u32 slot_idx [0..4]. "
        "Returns u16 state_code (0=empty slot or no match; non-zero=state category). "
        "Constants: wrapper fixes r2=0xFFFFFFFF(-1) as full-mode flag."),
    ("FUN_0803a540", "check_slot_equip_chain_rule",
        "Validates whether a specific slot satisfies equip/chain rules; returns bool. "
        "r0=player_side, r1=card_id, r2=target_side, r3=slot_idx [0..4]. "
        "Calls get_slot_card_state_code(player_side, slot_idx) -> r7 (state_code). "
        "Calls compute_slot_zone_eligibility_mask(player_side, card_id) -> r9 (aux bitmask). "
        "Branches on r7: "
        "  r7==0xd (STATE_EQUIP_TYPE_A): checks player_side==target_side, calls "
        "    test_slot_has_active_card with effect_code_A=0x13a0, on hit reads card [r0+6] ATK. "
        "  r7==0xf (STATE_EQUIP_TYPE_B): similar check with effect_code_B=0x1399. "
        "  other: extracts bits[1..6] from r2, AND with compute_slot_zone_eligibility_mask result. "
        "Returns 1=rule satisfied, 0=not satisfied. Read-only. "
        "r0=u32 player_side (stored r5), r1=u32 card_id (stored r4), "
        "r2=u32 target_side (stored r6), r3=u32 slot_idx [0..4] (MOV r8,r3). "
        "Returns u32 bool. "
        "Constants: gDuelFieldSlots=0x0201c510, STATE_EQUIP_TYPE_A=0xd, STATE_EQUIP_TYPE_B=0xf, "
        "effect_code_A=0x13a0, effect_code_B=0x1399."),
    ("FUN_0803279c", "count_field_copies_of_card",
        "Counts the number of valid on-field copies of card_id across both player sides. "
        "First calls check_card_field5_is_nonzero(card_id); if not applicable, "
        "calls get_card_extended_stat_field9(card_id) for alternate branch. "
        "Main path: double loop player=[0..1] x slot_idx=[0..4] over gDuelFieldSlots, "
        "extracts card_id (word & 0x1FFFF), matches against r9 (entry r0); "
        "on match checks slot+0x10 bit5 (negated), slot+0x8 hword, slot+0x10 bit1 (negated), "
        "and bitmask bit (1<<(player*16+slot_idx)) not set; all conditions met -> r8++. "
        "Returns r8 (u32 count). indeg=117; used by rule engine to enforce uniqueness "
        "limits (e.g. max 1 copy on field). "
        "r0=u16 card_id (MOV r9,r0). Returns u32 count. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20 bytes, "
        "gDuelFieldSlots_side1=0x0201c5d8 (=0x0201c510+0xc8)."),
    ("FUN_0804af60", "check_card_is_gravekeeper",
        "Checks whether card_id belongs to the Gravekeeper card series; returns bool. "
        "Hardcodes two ranges: single card 0x131d (Gravekeeper's Servant) and "
        "consecutive 9 cards 0x1585..0x158d (Gravekeeper's Spy through Gravekeeper's Assailant). "
        "card_id < 0x131d or in gap 0x131e..0x1584 or > 0x158d -> returns 0. "
        "card_id == 0x131d or in [0x1585..0x158d] -> returns 1. "
        "indeg=3 leaf function. "
        "Called in Necrovalley-related effect logic (0x08037e90), slot scan (0x08053cc4), "
        "and 09xx scene effect activation (0x08091888). "
        "r0=u16 card_id (saved to r1 at entry). Returns u32 bool (1=Gravekeeper, 0=not). "
        "Constants: 0x131d=Gravekeeper's Servant, 0x1585=Gravekeeper's Spy (range low), "
        "0x158d=Gravekeeper's Assailant (range high, 9 consecutive cards)."),

    # --- batch #12 (campaign-12, topo 287-?) ---
    ("FUN_08037c9c", "compute_zone_effect_atk_delta",
        "Computes the ATK/DEF buff delta for a specific zone slot (r1=player_side, r2=slot_idx). "
        "Reads card_id from gDuelFieldSlots (0x0201c510) at player_side*0x868 + slot_idx*20; "
        "initialises r9=0(atk), r7=0(def). "
        "If query_slot_effect_eligibility_nonzero(r5,r8) != 0 returns 0 immediately. "
        "Performs large switch on card_id; each case checks [r6+0xc] flag bits, "
        "sets r7=ATK_buff (0x1f4=+500 or 0xc8=+200) and r9=DEF_buff. "
        "Returns packed u32: (s16 atk_delta << 16) | (s16 def_delta & 0xffff). "
        "r0=ptr stack_slot_ptr, r1=u32 player_side [0..1], r2=u32 slot_idx [0..0xa], "
        "r3=u32 player_flag_cmp [0..1], [sp+0]=u32 stack_arg5 [0..9]. "
        "Returns u32 packed (high=atk_delta, low=def_delta; 0=no effect). "
        "Constants: gDuelFieldSlots=0x0201c510, PLAYER_STRIDE=0x868, SLOT_ENTRY_SIZE=20, "
        "ATK_buff_500=0x1f4, ATK_buff_200=0xc8, "
        "card_atk_lookup_base=0x09e3ef74, card_id_range=[0x10f5..0x1346]."),
    ("FUN_0803a658", "classify_equip_target_eligibility",
        "Classifies whether target_slot (r0=player_side, r1=target_slot_idx) can serve as a "
        "valid equip/effect target for source slot (r2=source_side, r3=equipping_slot_idx). "
        "Returns eligibility_type_code [0..6]: 0=not equippable, 1..6=valid equip types. "
        "Main path: reads equip chain head from gDuelFieldSlots+slot*20+0xa, "
        "traverses equip node pool (r12+0x14b0, stride=8): "
        "type_bits[3:0] in [0xa..0xd] -> compare source side/slot -> return 1; "
        "type_bits in [0x6..0x7] -> compare card_id: 0x1280/0x128a/0x1743 -> return 4, "
        "field9==4 -> return 2, FUN_08037c9c -> return 3, equip_chain_rule -> return 5, "
        "FUN_08036b88 -> return 6, else return 1. "
        "Empty chain path (target_slot<=4 only): card_id nonzero -> mask+compute_zone_eligibility_mask "
        "path returns 3; equip_chain_rule -> return 5; else return 0. "
        "r12 is internally loaded from DAT_0803a6c8 (=0x0201c510); not caller-set. "
        "Constants: gDuelFieldSlots=0x0201c510, equip_node_pool=r12+0x14b0, "
        "0x1280/0x128a/0x1743=special card IDs."),
    ("FUN_0802faf4", "find_node_by_value",
        "Traverses EWRAM node pool (0x0201d9c0, stride=8) along a linked list, "
        "returning the first node where [node+0](u16)==value(r1) and [node+2]&0xF (zone_type) in [0..5]. "
        "r0=u16 head_index [0..139] (0=empty list, returns NULL immediately). "
        "Returns u32* matching node ptr, or 0 (NULL) if not found. "
        "Simpler variant of find_node_by_value_and_zone_type: no zone_type equality check, "
        "only zone_type<=5 filter. "
        "Used by check_value_in_slot_chain/check_value_in_effect_context_chain/get_node_entity_id_in_slot. "
        "Constants: gDuelNodePool=0x0201d9c0, node_stride=8, zone_type_mask=0xF, zone_type_max=5."),
    ("FUN_0802fcc0", "check_value_in_effect_context_chain",
        "Checks whether value(r2) exists in the effect activation context chain for (r0,r1). "
        "Reads gDuelEffectCtx (0x0201bb90): compares r0 vs [+0x0](activation_player) and "
        "r1 vs [+0x1c](context_slot_ref); if both match uses side=0 chain, else side=1. "
        "Chain entry at 0x0201bc54 + side*20 + 0xa = chain_head_index. "
        "Calls find_node_by_value(head, r2); returns 1 if found, 0 if not. "
        "r0=u32 query_player, r1=u32 query_slot_ref [0..11], r2=u16 value. "
        "Returns u32 bool (1=value node present, 0=not present). "
        "Constants: gDuelEffectCtx=0x0201bb90, chain_array=0x0201bc54, "
        "activation_player_offset=0, context_slot_ref_offset=0x1c, chain_head_offset=0xa."),
    ("FUN_0802fe60", "get_node_entity_id_in_slot",
        "Locates a node in the equip chain for slot (r0 bit0=side, r1=slot_index) where "
        "[node+0]==r2(value) and zone_type<=5; if found returns [node+4](u16 entity_id), "
        "else returns -1 (0xFFFFFFFF). "
        "Reads chain_head_index from gDuelFieldSlots+side*0x868+slot_idx*20+0xa, "
        "calls find_node_by_value(head, value). "
        "Upgraded variant of check_value_in_slot_chain: returns entity_id instead of bool. "
        "indeg=33; used for effect source entity tracing. "
        "r0=u32 packed_player_id (bit0=side), r1=u32 slot_index [0..11], r2=u16 value. "
        "Returns u16 entity_id extended to u32, or -1 if not found. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20, "
        "chain_head_offset=0xa, entity_id_offset=4."),
    ("FUN_0804c1b8", "get_card_effect_zone_check_sides",
        "Returns 2-bit side_mask indicating which field sides need effect zone occupation check "
        "before placing card_id. bit0=1: check opponent side; bit1=2: check own side; 0=no check. "
        "Implements a hardcoded BST over restricted card IDs. "
        "Caller 0x0805a9a8 tests each bit and calls count_available_effect_zones per side. "
        "r0=u16 card_id. Returns u8 side_mask [0..3]. "
        "Constants: EFFECT_ZONE_CHECK_NONE=0, EFFECT_ZONE_CHECK_OPPONENT=1, "
        "EFFECT_ZONE_CHECK_SELF=2, EFFECT_ZONE_CHECK_BOTH=3."),
    ("FUN_08030de8", "find_zone_descriptor_by_slot_id",
        "Searches all zone tables for the slot matching packed slot_entity_id(r0), "
        "returns packed zone_descriptor (bits[31:24]=zone_type_code, bits[23:16]=slot_idx) "
        "or 0x1000 (sentinel=not found). "
        "Search order: (1) gDuelFieldSlots main field (2 players x 10 slots, stride 0x14); "
        "(2) 5 auxiliary zone arrays (0x0201c4f4/c4fc/c4f0/c4f8/c4ec, each 2-player); "
        "(3) default table (0x0201bc54, stride 0x114). "
        "Each entry compares extracted bits[13..6]<<1|bit[13] against search key r7. "
        "High frequency (indeg=52); used by card_display/card_frame hub functions. "
        "r0=u32 slot_entity_id (bits[13..6] of zone entry word). "
        "Returns u32 zone_descriptor or 0x1000. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "default_zone_table=0x0201bc54, sentinel=0x1000."),
    ("FUN_0804c16c", "check_card_is_zone_pair_restricted",
        "Checks whether card_id is one of two special zone-paired cards (0x12d3 or 0x147e). "
        "These cards share a paired placement restriction: when on field, the paired card "
        "blocks placement in the partner zone. "
        "Returns 1 if card_id==0x12d3 or 0x147e, 0 otherwise. "
        "7-instruction leaf; 9 callers all use 'cmp r0,#0; bne -> special branch'. "
        "r0=u16 card_id. Returns u8 is_zone_pair_restricted (0 or 1). "
        "Constants: CARD_ID_ZONE_PAIR_A=0x12d3(4819), CARD_ID_ZONE_PAIR_B=0x147e(5246)."),
    ("FUN_0802fc90", "check_value_in_slot_chain",
        "Checks whether value(r2) exists in the equip/effect node chain for slot (r0,r1). "
        "Reads chain_head_index from gDuelFieldSlots[side][slot]+0xa, "
        "calls find_node_by_value(head, value); returns 1 if found, 0 if not. "
        "Simplified variant of check_node_in_slot_chain (no zone_type equality param). "
        "indeg=107; core boolean query for duel field effect checking. "
        "r0=u32 packed_player_id (bit0=side), r1=u32 slot_index [0..11], r2=u16 value. "
        "Returns u32 bool (1=value node present in chain, 0=not). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry=20, chain_head_offset=0xa, gDuelNodePool=0x0201d9c0."),
    ("FUN_0802f27c", "count_zone_chain_eligible_cards",
        "Counts nodes in slot(r0,r1) chain satisfying: zone_type<=5, card_id==r2(target_card_id), "
        "status bit clear, and optional eligibility flags (r3=effect_eligible, sp[0]=fieldspell_eligible). "
        "For each node: reverse-maps node zone_type/zone_index back to gDuelFieldSlots to read card_id; "
        "on match checks [gDuelFieldSlots+0x10+slot_offset] bit5; "
        "if player_side matches node low-byte, checks get_card_extended_stat_field6 and "
        "check_card_field5_is_nonzero as additional filters. Counts passing nodes. "
        "r0=u32 packed_player_id, r1=u32 slot_index [0..11], r2=u16 target_card_id, "
        "r3=u32 effect_eligible, sp[0]=u32 fieldspell_eligible. "
        "Returns u32 match_count [0..max_chain_len]. "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, "
        "player_stride=0x868, slot_entry=20, field6_exclude=0x22."),
    ("FUN_0802f394", "count_equip_chain_default_flags",
        "Zero-flags wrapper around count_zone_chain_eligible_cards. "
        "Pushes 0 as sp[0] (fieldspell_eligible=0, disables extended eligibility filters), "
        "forwards r0/r1/r2 (player_side/slot_idx/filter_value) and r3=0. "
        "Used when only simple chain traversal is needed without extra eligibility checks. "
        "Sibling FUN_0802f3a8 passes real eligibility flags computed from "
        "check_slot_card_effect_eligibility+check_slot_card_fieldspell_eligibility. "
        "r0=u32 player_side, r1=u32 slot_idx [0..4], r2=u16 filter_value. "
        "Returns u32 match_count (0=no match). "
        "Constants: inherited from count_zone_chain_eligible_cards."),
    ("FUN_0804b4f4", "get_card_field_summon_restriction",
        "BST over hardcoded restricted card IDs; returns field-summon restriction type. "
        "0=no restriction (normal card), 1=type A (must check count_field_copies_of_card), "
        "2=type B (alternative flag path). "
        "Coverage: card_id in [0x100c..0x18c2] region (BST leaf boundaries). "
        "All 18 callers use 'cmp r0,#1; beq -> call count_field_copies_of_card'. "
        "r0=u16 card_id. Returns u8 restriction_type [0..2]. "
        "Constants: FIELD_RESTRICTION_NONE=0, FIELD_RESTRICTION_TYPE1=1, "
        "FIELD_RESTRICTION_TYPE2=2, BST_ROOT=0x14c9."),
    ("FUN_08034298", "check_card_targeted_by_spell_zone_effect",
        "Checks whether card(r0=card_data_ptr_or_id) is under effect of spell/trap zone card 0x1368. "
        "Returns 0 immediately if r1(zone_type_code)==0. "
        "Scans both players' magic/trap slots 5..9 (slot_offset=0x64..0xb4): "
        "(1) card_id bits[12:0]==0x1368; (2) equip_flags bit valid and chain not blocked; "
        "(3) check_card_pair_allowed([sp+0x0], [r4+0xc]); "
        "(4) find_effect_node_in_zone(player, slot, 0x1368, zone_type). "
        "All 4 conditions met -> return 1. No match found -> return 0. Read-only. "
        "r0=u32 card_data_ptr_or_id (saved at [sp+0x0]), r1=u8 zone_type_code [0..5]. "
        "Returns u32 bool (1=targeted by 0x1368 effect, 0=not). "
        "Constants: 0x1368=target special card ID, gDuelFieldSlots=0x0201c510, "
        "player_stride=0x868, slot5_offset=0x64."),
    ("FUN_0805a9a8", "check_card_placement_rules",
        "Comprehensive placement rule validator for card placement request. "
        "Sequentially checks: (1) find_paired_zone_entry_for_card (paired zone conflict); "
        "(2) check_card_field5_is_nonzero + FUN_0802fc90 (continuous effect quota); "
        "(3) find_effect_node_in_zone (effect zone occupation); "
        "(4) get_card_field_summon_restriction (field-dependent summon limit); "
        "(5) get_card_extended_stat_field6/9 (extended attribute filters); "
        "(6) check_card_is_zone_pair_restricted (pair-restriction dual card check); "
        "(7) get_card_effect_zone_check_sides + count_available_effect_zones (side mask check). "
        "Any rule trigger: writes flag to gP1LifePoints-related player state and returns 1. "
        "All rules pass: returns 0. "
        "r8 is caller-set non-APCS player_state_base used for internal state writes. "
        "r0=ptr card_info ([+0]=card_id, [+2]=player_side+zone_index packed, [+3]=flag_bits). "
        "r8=ptr player_state_base (non-APCS, caller-set). "
        "Returns u8 (0=placement allowed, 1=placement blocked). "
        "Side-effect: [gP1LifePoints+0x1d78] may be written 0x14 on block path."),
    ("FUN_0803b2b4", "get_zone_slot_ptr",
        "Zone slot pointer resolver (indeg=59). "
        "Returns EWRAM ptr to zone slot struct for (r0=player_side, r1=zone_type, r2=slot_offset). "
        "zone_type 0xb..0xf: dispatches to 5 fixed EWRAM zone arrays via switch table "
        "(0xb->0x0201c600, 0xc->0x0201c880, 0xd->0x0201c740, 0xe->0x0201c8f8, 0xf->0x0201cab0), "
        "stride = player_side*0x868 + slot_offset*4. "
        "zone_type 0..0xa (default): if r1+r2<=10 uses gDuelFieldSlots main field (stride 20); "
        "else uses 0x0201bc54-0xc4=0x0201bb90 extended zone base. "
        "All paths return r0+r1 (base + offset ptr). "
        "r0=u32 player_side [0..1], r1=u32 zone_type [0..0xf+], r2=u32 slot_offset [0..0xa]. "
        "Returns u32* EWRAM slot ptr. No side effects (pure address compute). "
        "Constants: gDuelFieldSlots=0x0201c510, PLAYER_STRIDE=0x868, "
        "SLOT_ENTRY_SIZE=20, ZONE_ENTRY_SIZE=4."),
    ("FUN_08036c2c", "build_effect_zone_entry",
        "Builds and submits an effect zone entry for player_side(r0), zone_idx(r1) [>=5 only]. "
        "zone_idx<=4 returns 0 immediately (monster zone ignored). "
        "Flow: (1) get_zone_slot_ptr(player_side, zone_idx) -> slot_ptr r4; "
        "(2) alloca 0x18 bytes on stack, zero-fill; "
        "(3) write player_side&1 to buf[+2].bit0 and zone_idx&0x1f to buf[+2].bits[1..5]; "
        "(4) read card_id (bits[0..12]) from slot_ptr and write to buf[+0]; "
        "(5) pack card_id extra fields into buf[+4] (mask 0xffff803f); "
        "(6) clear buf[+3] bits 0x31; "
        "(7) call check_card_placement_rules(buf) and return result. "
        "r0=u32 player_side [0..1], r1=u32 zone_idx [5..10]. "
        "Returns u32 (0=zone_idx<=4 early exit; check_card_placement_rules result otherwise). "
        "Side-effects: stack buf written; check_card_placement_rules may write player state."),
    ("FUN_08080d6c", "read_effect_slot_side_and_type",
        "Reads side flag and type nibble from effect node slot array. "
        "Layout: base[+4].bits[17:15] = slot count N; slot array starts at base+8, stride 2 bytes. "
        "addr = base + r1*2 + 8; extracts bit[0]=side flag and bits[4:1]=type_nibble. "
        "Returns packed u16: low byte = side(0=P1,1=P2), bits[11:8] = type_nibble (4-bit). "
        "93 callers use 'lsls r0,#0x10; lsrs r0,#0x18' to extract type nibble, or "
        "'lsls r1,r0,#0x18; lsrs r1,#0x18' to extract side bit. "
        "r0=ptr effect_node, r1=u8 slot_index [0..N-1]. "
        "Returns u16 packed_fields (low=side, bits[11:8]=type_nibble). "
        "Constants: EFFECT_SLOT_STRIDE=2, EFFECT_NODE_ARRAY_OFFSET=8, "
        "EFFECT_NODE_COUNT_SHIFT=15."),
    ("FUN_08036b88", "find_effect_entry_by_player_zone",
        "Reverse-scans effect entry array (0x0201b590, stride=0x18, count=[gDuelPhaseFlags+0x594]) "
        "for an entry matching player_side(r0/r2) and zone_type(r3). "
        "For each candidate entry: checks [+2].bit0==r10 (player_side) and [+2].bits[1..5]==r9 (zone_type). "
        "Inner loop: calls read_effect_slot_side_and_type(entry, r5) for each sub-slot, "
        "compares packed result against key (slot_idx<<8|player_side). "
        "Returns 1 on first full match, 0 if no match found. Read-only. "
        "r0=u32 player_side [0..1], r1=u32 slot_idx [0..4] (spill to stack), "
        "r2=u32 player_side_copy [0..1] -> r10, r3=u32 zone_type [0..0x1f] -> r9. "
        "Returns u32 bool (1=matching entry found, 0=not found). "
        "Constants: effect_entry_array=0x0201b590, effect_entry_stride=0x18, "
        "gDuelPhaseFlags=0x0201b290, effect_count_offset=0x594."),
    ("FUN_0803a7f0", "build_equip_target_eligibility_table",
        "Builds the equip target eligibility table for slot (r0=player_side, r1=slot_idx [0..9]). "
        "Output: r2=ptr output_table (2 players x 11 slots, u16 per cell, stride 0x16 per player). "
        "Init: zeros all 22 halfwords per player; exits early if slot_idx>9. "
        "Main loop 2 players x 10 slots: reads active bit from gDuelFieldSlots; "
        "active slots in monster zone (slot<=4): call find_paired_zone_entry_for_card (write 7 on hit); "
        "magic/trap zone (slot>4): call find_effect_entry_by_player_zone (write 6 on hit); "
        "then call classify_equip_target_eligibility for precise type code (write 0..6). "
        "r0=u32 player_side [0..1], r1=u32 slot_idx [0..9] (>9 zeros only), "
        "r2=ptr output_table (44+ bytes). Returns void (output via r2 side-effect). "
        "Side-effect: [output_table + player*0x16 + slot*2] := eligibility_type_code for all slots. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20, "
        "row_stride=0x16, output_buf=0x020230c4 (from caller FUN_080c8d30)."),
    ("FUN_080c8d30", "refresh_zone_effect_buff_cache",
        "Reads packed render state from gPageState[+0x210] (0x02023340): "
        "bit7=player_flag, bits[0..6]=mode, bits[8..14]=sub_idx. "
        "Unpacks to player_flag(r0), mode+sub_idx combined(r1), cache_ptr=0x020230c4(r2), "
        "then calls build_equip_target_eligibility_table to recompute all zone ATK/DEF buff deltas "
        "and write into effect_buff_cache. "
        "Called by 4 callers immediately after zone display update or scene transition. "
        "No input parameters (reads all state from gPageState). "
        "Returns build_equip_target_eligibility_table return value (callers discard). "
        "Side-effect: [0x020230c4..] rewritten with fresh zone effect buff values. "
        "Constants: gPageState=0x02023130, render_state_offset=0x210, "
        "effect_buff_cache=0x020230c4."),
    # 2026-05-08: BATCH campaign-13 (duel field count/cost util cluster)
    ("FUN_0802f5b0", "find_equip_chain_node_by_slot_pair",
        "In the equip chain of slot (r0 bit0=player_side, r1=slot_idx), find a node that matches "
        "r2=ref_player and r3=ref_slot. "
        "Flow: read gDuelFieldSlots[player][slot]+0xa = chain_head_index; return 0 if chain empty. "
        "Traverse gDuelNodePool (0x0201d9c0, stride 8): [node+0]=byte(ref_player), "
        "[node+0 high>>8]=byte(ref_slot), [node+2]&0xF=zone_type <= 5 (valid zone). "
        "Hit: return packed(zone_type<<28 | zone_idx<<16); end of chain: return 0. "
        "Caller FUN_0802f680 calls this for all 2x11 slots to find a paired node. "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, player_stride=0x868, "
        "slot_entry_size=0x14, chain_head_offset=0xa, node_stride=8, zone_type_max=5."),
    ("FUN_0802f680", "find_equip_chain_pair_across_field",
        "Search entire duel field (2 players x 10 slots) for a paired equip chain node "
        "matching (r0=player_side, r1=slot_idx). "
        "Flow: outer r5=0..1 (player), inner r4=0..10 (slot index); call "
        "find_equip_chain_node_by_slot_pair(r5, r4, r0, r1) for each slot; "
        "hit: return packed zone descriptor immediately. "
        "Not found after all slots: return DAT=0x0000ffff (sentinel). "
        "Purpose: check if given slot already has a paired node in another slot's equip chain. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_count_per_player=11, sentinel_not_found=0x0000ffff."),
    ("FUN_08032bc8", "count_paired_slots_with_field5",
        "Count slots on player's field satisfying paired+field5-nonzero conditions. "
        "Path A (check_card_field5_is_nonzero != 0): scan monster zone (slots 0..4), "
        "skip r9-specified slot, call check_slot_card_pair_allowed(player, slot, r2, r10) "
        "and [slot+0x8]!=0 -> count++. "
        "Path B (check_card_field5_is_nonzero == 0): scan trap zone (slots 5..10), "
        "skip r9-specified slot, check active bit + card_id>0 + [slot+0x10]>>1 bit clear "
        "+ card_id==r8 -> count++. "
        "Non-APCS inputs: r8=card_id_filter (caller-set); r9=skip_slot (caller-set); "
        "r10=equip_ref (caller-set, passed to check_slot_card_pair_allowed). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry_size=0x14, monster_zone=0..4, trap_zone=5..10."),
    ("FUN_08032c94", "count_paired_slots_with_field5_default",
        "Default wrapper calling count_paired_slots_with_field5 with r2=-1 (0xFFFFFFFF sentinel). "
        "Flow: movs r2,1; rsbs r2,r2,0 -> r2=-1 (0xFFFFFFFF); bl count_paired_slots_with_field5; "
        "return result. r2=-1 means no-filter in check_slot_card_pair_allowed. "
        "Very high frequency (indeg=27); main entry point for count_paired_slots_with_field5. "
        "Constants: sentinel_r2=0xFFFFFFFF (produced by rsbs)."),
    ("FUN_08032e80", "count_monster_slots_by_state",
        "Count monster zone slots (0..4) for player_side where get_slot_card_state_code "
        "returns a value equal to r10. "
        "Flow: r2=(r0&1)*0x868+gDuelFieldSlots; inner r4=0..4; skip if active bit=0 or "
        "[slot+0x8]=card_id=0; call get_slot_card_state_code(r6, r4); compare low 16 bits to r10; "
        "match -> r7++. Return r7=matching slot count. "
        "Non-APCS inputs: r9=slot_filter (caller-set, skip slot where r4==r9); "
        "r10=target_state_code (caller-set, state code to match). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry_size=0x14, monster_zone_count=5."),
    ("FUN_08033188", "count_occupied_monster_zones",
        "Count monster zone slots (0..4) with active bit set (occupied). "
        "Flow: r1=(r0&1)*0x868; r4=gDuelFieldSlots; for r2=4..0 (5 slots): "
        "ldr [gDuelFieldSlots+player_stride+r2*0x14]; lsls*0x13 extracts active bit; "
        "nonzero -> r3++. Return r3=occupied monster slot count. "
        "Very high frequency (indeg=46); fundamental duel field slot count utility. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry_size=0x14, monster_zone_count=5 (r2=4..0), active_bit_shift=0x13."),
    ("FUN_080331bc", "count_occupied_monster_zones_with_effect_bonus",
        "Extend count_occupied_monster_zones by checking gDuelEffectCtx (0x0201bb90) "
        "for an active effect slot; if matching, add 1 to count. "
        "Flow: r4=r0 (player_id saved); bl count_occupied_monster_zones(r4) -> r2 (base count); "
        "read gDuelEffectCtx: [+0x0]=P0_id, [+0x4]=P1_id; "
        "if P0_id==r4, read [gDuelEffectCtx+0xc4] halfword, active bit set -> r2++; "
        "same check for P1_id==r4 at offset 0xd8. Return r2=bonus-adjusted occupied count. "
        "Constants: gDuelEffectCtx=0x0201bb90, ctx_P0_id_offset=0, ctx_P1_id_offset=4, "
        "ctx_slot_c4_offset=0xc4, ctx_slot_d8_offset=0xd8, active_bit_shift=0x13."),
    ("FUN_08033214", "count_monster_slots_by_fnptr",
        "Count monster zone slots (0..4) where r7 function pointer returns nonzero for card_id. "
        "Flow: r4=player_side*0x868+gDuelFieldSlots+0x8; r5=4 (descending 0..4); "
        "for each slot: ldrh [slot+0x8]=card_id; skip if 0; ldr [slot+0] extract card_id bits[12:0]; "
        "bl FUN_0810e5e4 (=bx r7, trampoline calling r7 fnptr, arg r0=card_id); nonzero -> r6++. "
        "Return r6=matching slot count. "
        "Non-APCS input: r7=function_ptr (caller-set, executed via FUN_0810e5e4=bx r7 trampoline). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry_size=0x14, monster_zone_count=5 (r5=4..0), "
        "card_id_offset=0x8, FUN_0810e5e4_trampoline=bx r7."),
    ("FUN_08033e70", "count_hand_cards_by_field6",
        "Count hand cards where get_card_extended_stat_field6(card_id) equals r8. "
        "Flow: read gP1LifePoints+0x14+player_stride = hand count n; return 0 if n==0. "
        "Hand array base: gP1LifePoints+player*0x868+0x83*8 (=gP1LifePoints+player*0x868+0x418). "
        "For i=0..n-1: ldr [base+i*4]=card_word; card_id=bits[12:0]; "
        "call get_card_extended_stat_field6(card_id); compare to r8; hit -> r6++. "
        "Return r6=matching hand card count. "
        "Non-APCS input: r8=target_field6_value (caller-set, extended stat field6 value to match). "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "hand_count_offset=0x14, hand_base_offset=0x83*8=0x418."),
    ("FUN_080370dc", "count_extra_deck_cards_by_id",
        "Count Extra Deck cards for player_side where card_id equals r6 (=r1 low 16 bits). "
        "Flow: r6=r1&0xffff (card_id filter); read gP1LifePoints+player*0x868+0x14=hand_count; "
        "Extra Deck base: gP1LifePoints+player*0x868+0x83*8. "
        "For i=0..count-1: ldr card_word=[base+i*4]; card_id=bits[12:0]; cmp card_id,r6; "
        "hit -> r4++. Return r4=matching count. "
        "Non-APCS note: r1 low 16 bits extracted as card_id filter into r6 at entry "
        "(lsls r1,r1,0x10; lsrs r6,r1,0x10). "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "extra_deck_count_offset=0x14, extra_deck_base_offset=0x83*8=0x418."),
    ("FUN_0803730c", "count_hand_cards_with_field5",
        "Count hand cards where check_card_field5_is_nonzero(card_id) returns true. "
        "Flow: read gP1LifePoints+player*0x868+0x14=hand_count n; return 0 if n==0. "
        "Hand base: gP1LifePoints+player*0x868+0x83*8. "
        "For i=0..n-1: ldr card_word=[base+i*4]; card_id=bits[12:0]; "
        "bl check_card_field5_is_nonzero(card_id); nonzero -> r6++. "
        "Return r6=matching hand card count. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "hand_count_offset=0x14, hand_base_offset=0x83*8=0x418."),
    ("FUN_080373ac", "count_zone_slots_with_card_field5",
        "Count slots in r9/r8-specified 2D zone table where zone flag is 0x40 or 0x80 "
        "and check_card_field5_is_nonzero(card_id) returns true. "
        "r0=player_side [0..1] (bit0, saved to r5); "
        "Non-APCS r9=player_stride multiplier (caller-set); "
        "Non-APCS r8=zone array base (caller-set, points to gP1LifePoints+player*r9+0xba*8). "
        "Inner double loop (player=0..1 x slot=0..count): read zone flag byte; "
        "==0x40 or ==0x80 -> enter check_card_field5_is_nonzero path; hit -> r6++. "
        "Return r6=matching slot count. "
        "Constants: gP1LifePoints=0x0201c4e0, flag_byte_offset=0xf1*8 (0x788), "
        "zone_flag_A=0x40, zone_flag_B=0x80."),
    ("FUN_08038a1a", "compute_lp_cost_by_occupied_monster_zones",
        "Wrap count_occupied_monster_zones_with_effect_bonus and pass result to shared LP cost path. "
        "Flow: ldr r5=[sp+0x3c] (player_side); subs r0,r6,r5 (compute opponent player side); "
        "bl count_occupied_monster_zones_with_effect_bonus(r0); "
        "b LAB_08038d38 (scale by constant and accumulate into r10). "
        "Case branch of FUN_08037ec0 large LP cost dispatch (entry via b LAB_08038d38). "
        "Note: subs r0,r6,r5 with r6=1,r5=0->r0=1; r6=0,r5=0->r0=0; computes opponent side. "
        "Constants: shared_scale_addr=0x08038d38 (count*0xa0=count*160)."),
    ("FUN_08038c02", "compute_lp_cost_by_hand_field6",
        "Wrap count_hand_cards_by_field6, scale count by 5 for LP cost, jump to shared scale path. "
        "Flow: ldr r0=[sp+0x3c] (player_side from caller stack); movs r1,1 (target_field6=1); "
        "bl count_hand_cards_by_field6; lsls r1,r0,2; adds r1,r1,r0 (r1=count*5); "
        "b LAB_08038d98 (multiply r1 by 0x4e=78 and store into r10). "
        "Case branch of FUN_08037ec0 large LP cost dispatch. "
        "Constants: field6_target=1, lp_scale=5, shared_scale_addr=0x08038d98."),
    ("FUN_08038d08", "compute_lp_cost_by_extra_deck_card_id",
        "Wrap count_extra_deck_cards_by_id, scale count by 5 for LP cost, jump to shared scale path. "
        "Flow: ldr r1,DAT=0x1919 (card_id=0x1919); ldr r0=[sp+0x3c] (player_side); "
        "bl count_extra_deck_cards_by_id(player, 0x1919); "
        "lsls r1,r0,2; adds r1,r1,r0 (r1=count*5); "
        "b LAB_08038d98 (multiply by (0x10-1)*4 and accumulate into r10). "
        "Case branch of FUN_08037ec0 large LP cost dispatch. "
        "Constants: card_id_target=0x1919, lp_scale=5, shared_scale_addr=0x08038d98."),
    ("FUN_08038e00", "compute_lp_cost_by_zone_field5_both_players",
        "Call count_zone_slots_with_card_field5 for both players, sum results, "
        "apply LP cost formula (count*5)*0x4e, write to r7[+0x18] and r7[+0x14]. "
        "Flow: bl count_zone_slots_with_card_field5(0)->r4; "
        "bl count_zone_slots_with_card_field5(1)->r0; r4+=r0; r1=r4*5; "
        "r0=(r1*0x10-r1)*4; write to r7[+0x18]; shared path LAB_08038e18 writes r7[+0x14]. "
        "Case branch of FUN_08037ec0 large LP cost dispatch. "
        "Constants: lp_scale_a=5, lp_scale_b=0x4e=78 (total factor=count*390)."),
    ("FUN_0803b4b0", "get_zone_slot_card_ref_by_type",
        "Read zone slot card reference field by zone_type_code (r1) and return packed value. "
        "Switch dispatch (r1-0xb, 5 cases): "
        "0xb: base=0x0201c600+player_side*0x868+r2*4 -> ldr [slot]; "
        "0xc: base=0x0201c880+player_side*0x868+r2*4 -> ldr [slot]; "
        "0xd: base=0x0201c740+player_side*0x868+r2*4 -> ldr [slot]; "
        "0xe: base=0x0201c8f8+player_side*0x868+r2*4 -> ldr [slot]; "
        "0xf: base=0x0201cab0+player_side*0x868+r2*4 -> ldr [slot]; "
        "default (r1+r2<=10): base=gDuelFieldSlots+player_side*0x868+(r1+r2)*20 -> ldr [slot]; "
        "default (r1+r2>10): base=0x0201bc54+player_side*20 -> ldr [slot]. "
        "Return: packed bits[22..16]<<1 | bit[13] (entity/player reference bits). "
        "Sibling FUN_0803b5c0 returns [slot+6] u16 for same switch. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "zone_0b=0x0201c600, zone_0c=0x0201c880, zone_0d=0x0201c740, "
        "zone_0e=0x0201c8f8, zone_0f=0x0201cab0, default_extended=0x0201bc54."),
    ("FUN_0803b5c0", "get_zone_slot_field6_by_type",
        "Read [slot+6] u16 field from EWRAM zone table by zone_type_code (r1) and slot_index (r2). "
        "Logic fully symmetric with get_zone_slot_card_ref_by_type but returns [slot+0x6] halfword. "
        "Switch dispatch (r1 [0xb..0xf]): r1 in [0xb..0xf] -> shared path; "
        "r1>0xf or <0xb -> return 0; "
        "r1+r2>10: read 0x0201bc54+player*20 -> ldrh [+6]; "
        "r1+r2<=10: gDuelFieldSlots+player*0x868+(r1+r2)*20 -> ldrh [+6]. "
        "Return: r0=u16 zone_slot_field6 (0=invalid zone_type or empty slot). "
        "Sibling get_zone_slot_card_ref_by_type reads [slot+0] and extracts packed bits. "
        "Constants: zone_0b=0x0201c600 (shared with get_zone_slot_card_ref_by_type), "
        "sentinel_zone_range=[0xb..0xf], field_offset=6."),
    ("FUN_080cc8c8", "ensure_card_id_cache_entry",
        "Ensure cache entry at 0x0201ff60+r0*2 is filled; if zero, load from hand table and write. "
        "Flow: r4=0x0201ff60+r0*2 (cache slot ptr); ldrh [r4]; nonzero (cached) -> return. "
        "Otherwise: base=gP1LifePoints+r0*4+0x87*32 (=gP1LifePoints+r0*4+0x10e0); "
        "ldrh card_word=[base]; card_id=bits[12:0]; bl internal_card_id_to_card_id(card_id); "
        "lsls/lsrs truncate to 16 bits; strh card_id,[r4] (write cache slot). "
        "No explicit r0 return. "
        "Used to cache current hand/slot card_id for UI display layer, avoiding repeat decode. "
        "Constants: cache_base=0x0201ff60, cache_stride=2 (u16/entry), "
        "gP1LifePoints=0x0201c4e0, hand_base_offset=0x87*32=0x10e0, card_id_mask=0x1fff."),
    ("FUN_080eef0c", "lookup_rom_card_attribute_table_a",
        "Look up card attribute table in ROM (0x09821e04, stride=0x16=11*2 bytes/row) "
        "by card index and return specific field u16 value. "
        "Flow: r1=r0 (card_index); if r1<=0xfa6 (=4006, boundary check) return 0; "
        "else: r1+=0xfffff059 (=r1-0xfa7=row index); "
        "col_offset=(0xb*row+4)*2 (=row*22+8); base=0x09821e04+col_offset; "
        "ldrh [result]; if result==0xffff (sentinel) return 0, else return result. "
        "Sibling FUN_080eef44 uses col_offset=(0xb*row+3)*2=row*22+6. "
        "Constants: table_base=0x09821e04, index_min=0xfa7 (cmp > 0xfa6), "
        "row_stride=0xb*2=22 bytes, col_offset_A=8 (halfword 4 in row), sentinel=0xffff."),

    # 2026-05-08: campaign-14 batch (duel core evaluation/count/equip chain/LP cost cluster)
    ("FUN_0804be38", "get_card_effect_category",
        "Classify card_id (r0) into effect category code via binary tree ID comparisons. "
        "Returns: 0=none, 1=type_B, 3=type_C, 5=type_D, 0xff=type_A. "
        "Pure read-only; no side effects. "
        "Key IDs: 0x161a, 0x128e, 0x1610-0x1617, 0x16de, 0x1624, 0x186a, 0x1817, 0x1983. "
        "Called by get_slot_effect_card_value (returns 0/non-0) and addr 0x0804513c (extracts bit0)."),
    ("FUN_0803149c", "get_slot_effect_card_value",
        "Read gDuelFieldSlots[player_side][slot_idx] word, extract card_id (bits[12:0]), "
        "call get_card_effect_category(card_id). If result==0 return 0; else return slot word[0xc] (effect value field). "
        "r0: packed_side_flags (bit0=player_side [0..1]); r1: slot_idx [0..4]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20 bytes, effect_field_offset=0xc."),
    ("FUN_08032904", "count_zones_by_card_and_mode",
        "Dispatch based on r2 (mode_flags): "
        "mode==0: bl count_field_copies_of_card(card_id); "
        "mode bit0: bl count_available_effect_zones(1-player, card_id, -1) -> accumulate; "
        "mode bit1: bl count_available_effect_zones(player, card_id, -1) -> accumulate. "
        "r0: card_id [0..0x19b7]; r1: player_side [0..1]; r2: mode_flags [0..3]. "
        "Returns r0=count (field copies or available effect zone sum)."),
    ("FUN_0802f3a8", "query_zone_chain_count_with_eligibility",
        "Wrapper around count_zone_chain_eligible_cards that dynamically computes both eligibility flags. "
        "Flow: bl check_slot_card_effect_eligibility(r0,r1)->r6; "
        "bl check_slot_card_fieldspell_eligibility(r0,r1)->sp[0]; "
        "bl count_zone_chain_eligible_cards(player, slot, r8, r6, sp[0]). "
        "r0: player_side [0..1]; r1: slot_idx [0..4]; r8 (non-APCS, caller-set): filter_value. "
        "Returns r0=match_count [0..chain_len]."),
    ("FUN_0803a428", "adjust_slot_score_by_chain_and_zone",
        "Mid-section of AI slot scoring function (~0x08037ec0). Adjusts r7[+0x14] (atk_score) "
        "and r7[+0x18] (def_score) via stack variables and multiple callee results. "
        "Paths: add/subtract sp[0x48..0x58]+r10 delta; zero atk_score if count_field_copies_of_card(0x1951) "
        "and r7[4]==4 or r7[0xc] bit4; double atk_score if count_occupied_monster_zones_with_effect_bonus==2; "
        "halve via query_zone_chain_count_with_eligibility loop; halve via count_available_effect_zones sum loop; "
        "clamp both scores >=0; fall-through to cleanup_slot_score_entry_epilogue. "
        "r7 (non-APCS): slot_score_entry ptr ([+0x14]=atk_score, [+0x18]=def_score). "
        "r10 (non-APCS): auxiliary_score. No APCS params. "
        "Side effects: writes r7[+0x14] and r7[+0x18]."),
    ("FUN_0804b30c", "check_card_id_is_special_summon_type",
        "Check if card_id (r0) falls in special-summon card ID ranges or exact values. "
        "Ranges/IDs checked: 0x18ab..0x18ad, 0x19aa, 0x19ad..0x19ae, 0x19b2, 0x19bb and final fallthrough. "
        "Returns 1=matches special-summon type, 0=no match. "
        "Pure leaf, no side effects. Sibling cluster: get_card_effect_category, FUN_0804b2dc, FUN_0804b1f0. "
        "r0: card_id [0..0x19b7]."),
    ("FUN_08032ef0", "count_monster_slots_by_state_all",
        "Thin wrapper: sets r2=-1 (full-scan, no filter) then calls count_monster_slots_by_state(r0, r1, -1). "
        "r0: player_side [0..1]; r1: state_mask (e.g. 0xd=occupied, 0xf, 0x12). "
        "Returns r0=slot_count. indeg=8. "
        "Constants: r2=-1 fixed (movs r2,#1; rsbs r2,r2,#0)."),
    ("FUN_0803309c", "count_active_slots_with_field6_value",
        "Iterate player (r0 bit0) monster zone slots 0..4; for each active slot (lsls valid bit), "
        "call test_slot_has_active_card(player, slot_idx, r10=effect_code); "
        "if true and slot[+6] halfword == r9 (target_field6_val), increment counter. "
        "r0: player_side [0..1]; r1: effect_code (-> r10 at entry); r2: target_field6_val [0..0xffff] (-> r9). "
        "Returns r0=count [0..5]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, monster_zone_count=5, slot_entry=0x14."),
    ("FUN_0803407c", "eval_slot_target_eligibility_full",
        "Comprehensive slot-target eligibility evaluator. "
        "Calls resolve_slot_card_id_for_pair then multiple query_zone_chain_count_with_eligibility "
        "and count_zones_by_card_and_mode calls using non-APCS r8/r9/r10 params. "
        "Large switch dispatches on card_id for zone count aggregation. "
        "r8 (non-APCS): player_side_or_mode; r9 (non-APCS): target_param; r10 (non-APCS): aux_param. "
        "Returns r0=eligibility_result (0=ineligible; >0=target count/score). indeg=2. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_08038e1e", "apply_slot_score_bonus_by_state",
        "Apply state-based bonus increments to AI scoring stack variables sp[0x54] and sp[0x58]. "
        "Path 1: card_id==0x1782 and sp[0x64] bit0==0: check_value_in_slot_chain(0x1843) -> "
        "count_available_effect_zones -> if >0 write r7[+0x14]=0xbb8. "
        "Path 2: state_code==0xd: count_active_slots_with_field6_value(r1=0x13a0) x2 -> sp[0x54/0x58] += count*124. "
        "Path 3: state_code==0xf: count_available_effect_zones(0x1399) -> sp[0x54] += count*25; "
        "optionally count_monster_slots_by_state_all*0xc8. "
        "Path 4: state_code==0x7: field-copy loop bonus. "
        "r7 (non-APCS): slot_score_entry ptr. No APCS params. "
        "Side effects: [r7+0x14], sp[0x54], sp[0x58]."),
    ("FUN_08034020", "count_hand_cards_by_field6_alt",
        "Count hand cards where get_card_extended_stat_field6(card_id)==r8 (non-APCS). "
        "Alt variant of count_hand_cards_by_field6 (0x08033e70): uses different EWRAM offsets "
        "(hand_count_offset=0x1c vs 0x14; hand_base_offset=0xba*8=0x5d0 vs 0x83*8=0x418). "
        "Flow: gP1LifePoints+0x1c+player*0x868=hand_count; "
        "iterate gP1LifePoints+player*0x868+0x5d0 (hand array, 4 bytes/entry); "
        "extract card_id bits[12:0]; bl get_card_extended_stat_field6; cmp r0,r8; match->counter++. "
        "r0: player_side [0..1]; r8 (non-APCS, caller-set): target_field6_value. "
        "Returns r0=count [0..hand_size]. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "hand_count_offset=0x1c, hand_base_offset=0xba*8=0x5d0, card_entry_size=4."),
    ("FUN_0803a520", "cleanup_slot_score_entry_epilogue",
        "Shared early-exit/epilogue of large slot-scoring function (~0x08037ec0). "
        "Entered when card_id==0 (empty slot) or slot_idx>4 (out-of-range). "
        "Body: add sp,#0x84; pop non-APCS regs; pop callee-saved; pop r0 (return addr); bx r0. "
        "No scoring writes; pure stack cleanup. indeg=3 (three early-exit callers). "
        "Also entered by fall-through from adjust_slot_score_by_chain_and_zone."),
    ("FUN_08032ca4", "count_paired_slots_both_sides",
        "Call count_paired_slots_with_field5(player=0, card_id, -1) and "
        "count_paired_slots_with_field5(player=1, card_id, -1), sum results. "
        "r0: card_id [0..0x19b7]. Returns r0=total_count [0..10]. "
        "Full-field wrapper analogous to count_monster_slots_by_state_all. indeg=9. "
        "Constants: r2=-1 fixed (rsbs #0)."),
    ("FUN_08030048", "find_equip_chain_node_by_pred",
        "Read slot[+0xa] chain head from gDuelFieldSlots[player_side][slot_idx]; return 0 if empty. "
        "Traverse gDuelNodePool (0x0201d9c0) nodes (8 bytes each): for each node call "
        "FUN_0810e5e4 trampoline (bx r6) with (node_ptr, pred_param); if returns nonzero, return node_ptr. "
        "Next via node[+6] halfword. Exhausted: return 0. "
        "r0: player_side [0..1]; r1: slot_idx [0..4]; r3: pred_param (-> r1 in trampoline); "
        "r6 (non-APCS): fn_ptr/id for trampoline. Returns r0=node_ptr or 0. "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, "
        "slot_chain_offset=0xa, node_stride=8, node_next_offset=6."),
    ("FUN_0803b230", "check_slot_zone_bit_eligible",
        "Wrap compute_slot_zone_eligibility_mask(r0, r1) and test if bit r2 is set in result. "
        "Flow: save r2->r4; bl compute_slot_zone_eligibility_mask; "
        "movs r1,#1; lsls r1,r4 (1<<r4); ands r1,r0; >0->return 1, else 0. "
        "r0: player_side [0..1]; r1: card_id [0..0x19b7]; r2: bit_index [0..31]. "
        "Returns r0=bool. indeg=19."),
    ("FUN_0803a9a8", "eval_equip_chain_score_for_slot",
        "Compute AI equip-chain score for gDuelFieldSlots[player_side][slot_idx]. "
        "Check fieldspell eligibility; if 0 return 0. "
        "Base score: get_card_extended_stat_field5(card_id)->r6. "
        "Traverse slot[+0xa] chain nodes; adjust r6 by node type (0..0xa) and equip card IDs "
        "(0x1472/0x1636/0x172f/0x1809). "
        "Second pass: scan both-player slots for field5 conditions; call check_slot_zone_bit_eligible(bit3); "
        "each match: r6--. Returns max(r6, 1). "
        "r0: player_side [0..1]; r1: slot_idx [0..4]; "
        "r8 (non-APCS, caller-set then overwritten internally to current card_id; caller value preserved via push/pop); "
        "r9 (non-APCS, init from r0): player_side_copy; r10 (non-APCS, init from r1): slot_idx_copy. "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, "
        "equip_ids=0x1472/0x1636/0x172f/0x1809."),
    ("FUN_08030a30", "check_slot_card_is_equip_whitelist",
        "Extract card_id (bits[12:0]) from gDuelFieldSlots[player_side][slot_idx]; "
        "compare against whitelist {0x1472, 0x1636, 0x172f, 0x1809}. "
        "On hit: call check_node_in_slot_chain(player_side, slot_idx, 0x1472, 5) and return its bool result. "
        "No hit: return 0. "
        "r0: player_side [0..1]; r1: slot_idx [0..4]. Returns r0=bool. indeg=38. "
        "Stricter variant of check_slot_card_is_equip_type (no field8 fallback). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "equip_ids=0x1472/0x1636/0x172f/0x1809."),
    ("FUN_08038dd4", "compute_lp_cost_by_zone_field5_x100",
        "Call count_zone_slots_with_card_field5(0) and count_zone_slots_with_card_field5(1), "
        "sum both-side counts, multiply by 0x64 (100), write to r7[+0x18] and r7[+0x14] via fall-through. "
        "No APCS params; r7 (non-APCS): slot_score_entry ptr. "
        "Side effects: [r7+0x18] := count*100; [r7+0x14] := count*100 (fall-through). "
        "Sibling variants: FUN_08038dea (x200), compute_lp_cost_by_zone_field5_both_players (x390). "
        "Constants: scale_factor=0x64=100."),
    ("FUN_080eeed4", "get_card_extended_stat_field3",
        "Read ROM extended card attribute table (0x09821e04, 11 halfwords/row) column index 3 "
        "for card_id (r0). If card_id<=0x0fa6 (normal card bound) return 0. "
        "row=card_id-0xfa7; offset=(row*11+3)*2; read u16 from table_base+offset; "
        "0xffff sentinel treated as 0. "
        "Sibling cluster: get_card_extended_stat_field5/6/7/8/9; only N differs (N=3 here). "
        "r0: card_id [0..0x19b7]. Returns r0=u16 extended_stat_field3. "
        "Constants: table_base=0x09821e04, normal_bound=0x0fa6, row_stride=11 halfwords, field_col=3."),
    ("FUN_0802f4e0", "count_active_extended_chain_nodes",
        "Read slot[+0xa] chain head from gDuelFieldSlots[player_side][slot_idx]; traverse gDuelNodePool. "
        "For each node: type=byte[2]&0xf; skip if type<=9. "
        "For type>9: extract player_side and slot_idx from node[0] (byte[0]=player bit0, byte[1]>>8=slot_idx); "
        "navigate to that slot in gDuelFieldSlots; check lsls*0x13 active bit; if nonzero r5++. "
        "Continue via node[+6] next. Returns r5=count of type>9 active chain nodes. "
        "r0: player_side [0..1]; r1: slot_idx [0..4]. indeg=3. "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelNodePool=0x0201d9c0, "
        "node_type_threshold=9, node_next_offset=6, player_stride=0x868."),

    # --- batch #15 (campaign-15, 2026-05-08) ---
    ("FUN_08038dea", "compute_lp_cost_by_zone_field5_x200",
        "Call count_zone_slots_with_card_field5(0) and count_zone_slots_with_card_field5(1), "
        "sum both-side counts, multiply by 0xc8 (200), write to r7[+0x18] and r7[+0x14] via fall-through. "
        "No APCS params; r7 (non-APCS): slot_score_entry ptr. "
        "Side effects: [r7+0x18] := count*200; [r7+0x14] := count*200 (fall-through). "
        "Sibling variants: compute_lp_cost_by_zone_field5_x100 (x100), "
        "compute_lp_cost_by_zone_field5_both_players (x390). "
        "Constants: scale_factor=0xc8=200."),
    ("FUN_08037ec0", "eval_slot_score_entry_full",
        "Full AI slot-score evaluator for one field slot (large function, indeg=3). "
        "r0: player_side [0..1] (-> r6); r1: slot_idx [0..4] (-> r5). "
        "Allocates 0x84 bytes stack; checks slot active, card_id, zone occupancy. "
        "Dispatches to compute_lp_cost_by_* case branches for various card and zone states. "
        "Falls through to adjust_slot_score_by_chain_and_zone then "
        "cleanup_slot_score_entry_epilogue. "
        "Side effects: writes r7[+0x14] (atk_score) and r7[+0x18] (def_score) via callees. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20 bytes."),
    ("FUN_080ca660", "decode_card_image_tiles_to_vram",
        "Decompress and decode card image tile data into VRAM for card display. "
        "Reads tile data source pointer, calls decompression routine, then writes decoded "
        "tile data to VRAM destination. r0: card_id [0..0x19b7]; r1: vram_dest ptr. "
        "Returns void. Side effects: VRAM region at r1 written with decompressed tile data. "
        "Constants: card_tile_table_base=ROM tile index table."),
    ("FUN_0804bf20", "check_card_id_is_equip_set_b",
        "Check if card_id (r0) belongs to equip card set B (second hardcoded ID range/list). "
        "Pure BST leaf over card IDs in set B. Returns 1=member, 0=not member. "
        "Sibling: check_card_id_is_equip_set_a (set A range). "
        "r0: card_id [0..0x19b7]. Returns u32 bool."),
    ("FUN_0804bd78", "check_card_id_is_equip_set_a",
        "Check if card_id (r0) belongs to equip card set A (first hardcoded ID range/list). "
        "Pure BST leaf over card IDs in set A. Returns 1=member, 0=not member. "
        "Sibling: check_card_id_is_equip_set_b (set B range). "
        "r0: card_id [0..0x19b7]. Returns u32 bool."),
    ("FUN_080cae84", "write_card_digit_tiles_to_vram",
        "Write prebuilt digit tile data for card number display into VRAM. "
        "r0: digit_tile_src ptr; r1: vram_dest ptr; r2: tile_count [1..N]. "
        "Iterates tile_count entries, copying digit tile words to VRAM destination. "
        "Returns void. Side effects: VRAM region written with digit tiles. "
        "Constants: tile_word_size=4 bytes per tile entry."),
    ("FUN_080cace8", "zero_card_display_vram_regions",
        "Zero-fill VRAM regions used for card display (card image, digits, name strip). "
        "No APCS params; reads display region base addresses from global state. "
        "Calls bios_cpu_set fill=0 for each subregion. Returns void. "
        "Side effects: card display VRAM zeroed before redraw. "
        "Constants: uses bios_cpu_set fill mode (bit24=1)."),
    ("FUN_080caf68", "render_card_name_to_sprite_vram",
        "Render card name string tiles into sprite VRAM for card name display strip. "
        "r0: card_id [0..0x19b7]; r1: sprite_vram_dest ptr. "
        "Looks up name string, converts characters to tile indices, writes to sprite VRAM. "
        "Returns void. Side effects: sprite VRAM region written with name tile data."),
    ("FUN_08030b70", "check_card_stat_field7_equals",
        "Read card stat field7 for card_id (r0) and compare to r1 (target_value). "
        "Returns 1 if field7==target_value, 0 otherwise. "
        "r0: card_id [0..0x19b7]; r1: target_value [0..0xff]. "
        "Returns u32 bool. Pure read-only leaf. "
        "Constants: card_stat_table_base=ROM card stat table, field7_offset=7."),
    ("FUN_0802fbbc", "count_chain_nodes_by_card_id",
        "Traverse gDuelNodePool from head_index (r0) counting nodes where "
        "card_id (node[+0] low 13 bits) == r1 (target_card_id) and zone_type<=5. "
        "r0: head_index [0..139]; r1: target_card_id [0..0x19b7]. "
        "Returns u32 match_count. "
        "Constants: gDuelNodePool=0x0201d9c0, node_stride=8, zone_type_mask=0xf, zone_type_max=5."),
    ("FUN_0802fc34", "count_slot_chain_nodes_by_card_id",
        "Wrapper: read chain_head from gDuelFieldSlots[player_side][slot_idx]+0xa, "
        "call count_chain_nodes_by_card_id(head, r2). "
        "r0: packed_player_id (bit0=side); r1: slot_idx [0..11]; r2: target_card_id [0..0x19b7]. "
        "Returns u32 match_count (0=chain empty or no match). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, chain_head_offset=0xa."),
    ("FUN_080377b0", "eval_equip_bonus_for_slot",
        "Evaluate equip bonus score for slot (r0=player_side, r1=slot_idx). "
        "Calls eval_equip_chain_score_for_slot and combines with zone eligibility mask. "
        "Returns r0=bonus_score [0..N]. "
        "r0: player_side [0..1]; r1: slot_idx [0..4]. "
        "Constants: gDuelFieldSlots=0x0201c510."),
    ("FUN_080c933c", "map_card_id_to_digit_tile_offset",
        "Map card_id (r0) to the ROM tile offset for card number digit display. "
        "Looks up card number digits from card attribute table, returns byte offset into "
        "digit tile ROM data. r0: card_id [0..0x19b7]. "
        "Returns u32 tile_offset. Pure read-only. "
        "Constants: card_number_table_base=ROM digit tile index table."),
    ("FUN_080cb1cc", "render_large_card_display_by_mode",
        "Top-level dispatcher for large card display rendering. "
        "r0: display_mode [0..N]; r1: card_id [0..0x19b7]. "
        "Dispatches to sub-renderers: decode_card_image_tiles_to_vram, "
        "render_card_name_to_sprite_vram, write_card_digit_tiles_to_vram, etc. "
        "Returns void. Side effects: VRAM and OAM written for card display. "
        "Constants: mode dispatch table in ROM."),
    ("FUN_080f2c4c", "render_decimal_digits_jp_signed",
        "Render signed decimal integer as digit tiles in JP glyph style. "
        "r0: value (s32 signed integer); r1: dest_ptr (sprite VRAM or BG tile dest). "
        "Decomposes value into decimal digits, maps each digit to JP tile index, "
        "writes tiles to dest. Handles sign (negative prefix tile). "
        "Returns void. Side effects: dest_ptr region written with digit tiles. "
        "Constants: JP digit tile base index in glyph tile set."),
    ("FUN_080c7894", "init_bg_vram_for_card_display",
        "Initialize BG VRAM regions for card display screen. "
        "Clears BG tile/map regions, sets palette entries, configures BG control registers "
        "for card image and text display layers. "
        "No APCS params; all addresses from global display state. "
        "Returns void. Side effects: BG VRAM, palette, DISPCNT regs written. "
        "Constants: BG control regs 0x04000008/0x0400000a/0x0400000c/0x0400000e."),
    ("FUN_080c9a10", "write_oam_card_icon_strip",
        "Write OAM entries for card type/attribute icon strip in card display. "
        "r0: oam_base ptr; r1: icon_count [1..N]; r2: start_x [0..239]; r3: start_y [0..159]. "
        "For each icon: compute OAM attr0/attr1/attr2, write to oam_base + index*8. "
        "Returns void. Side effects: OAM region written. "
        "Constants: OAM_ATTR0_Y_MASK=0xff, OAM_ATTR1_X_MASK=0x1ff."),
    ("FUN_080c9374", "write_nibble_palette_rows_to_vram",
        "Write 4bpp nibble palette row data to VRAM for card display tiles. "
        "r0: src_palette_data ptr; r1: vram_dest ptr; r2: row_count [1..N]. "
        "Iterates row_count rows, packing nibble pairs into halfwords, writing to VRAM. "
        "Returns void. Side effects: VRAM tile palette region written. "
        "Constants: nibble_mask=0xf, halfword_shift=4."),
    ("FUN_080c992c", "render_card_type_icon_to_vram",
        "Render card type icon tile into VRAM for card display. "
        "r0: card_type [0..N]; r1: vram_dest ptr. "
        "Looks up type icon tile source from ROM table, copies tile data to vram_dest. "
        "Returns void. Side effects: VRAM region written with type icon tiles. "
        "Constants: card_type_icon_table_base=ROM icon tile table."),
    ("FUN_080c9ac8", "tick_card_icon_anim_step",
        "Advance card icon animation by one step, updating OAM and VRAM tile indices. "
        "r0: anim_state_ptr (struct with frame_counter, tile_idx, oam_ptr). "
        "Increments frame counter; on threshold, advances tile_idx and writes updated "
        "OAM attr2 tile field. Returns void. "
        "Side effects: anim_state frame_counter and tile_idx updated; OAM attr2 written. "
        "Constants: anim_frame_threshold from anim_state struct."),

    # --- batch #16 (campaign-16, 2026-05-08) card display VRAM rendering pipeline ---
    ("FUN_080c9c94", "advance_card_display_effect_step",
        "Advance one step of the card display effect animation (fade/slide/flip). "
        "Called by the card display scene state machine; reads current effect phase from "
        "EWRAM card display state struct, increments phase counter, triggers VRAM/OAM updates. "
        "r0: card_display_state_ptr. Returns void. "
        "Side effects: phase counter incremented; OAM and/or VRAM updated per effect step."),
    ("FUN_080f0720", "test_char_kinsoku_tail",
        "Test whether a character code is a kinsoku tail character (cannot start a line in JP typography). "
        "r0: char_code (u16 JP character code). "
        "Returns 1 if char_code is in the kinsoku tail set (e.g. closing brackets, punctuation), 0 otherwise. "
        "Pure read-only leaf; no side effects. "
        "Constants: kinsoku_tail_table in ROM."),
    ("FUN_080c76c0", "render_jp_string_to_tile_line",
        "Render a JP-encoded string into a BG tile line buffer. "
        "Iterates over characters in the string, calls glyph rasterizer per character, "
        "accumulates glyph nibble rows into the tile line buffer. "
        "r0: str_ptr (JP encoded string); r1: tile_line_buf_ptr; r2: x_start [0..N]; r3: color_attr. "
        "Returns void. Side effects: tile_line_buf written with glyph nibble rows."),
    ("FUN_080f370c", "write_glyph_nibble_rows_to_vram",
        "Write 4bpp glyph nibble rows from a line buffer into BG tile VRAM. "
        "r0: line_buf_ptr (source nibble rows); r1: vram_tile_dest ptr; r2: row_count [1..8]. "
        "Packs nibble pairs into 32-bit tile words and stores to VRAM. "
        "Returns void. Side effects: VRAM tile region written. "
        "Constants: nibble_mask=0xf, tile_word_stride=4."),
    ("FUN_080f37d4", "write_line_buf_to_bg_tile_vram",
        "Write a complete line buffer (packed glyph rows) into BG tile VRAM for one text row. "
        "r0: line_buf_ptr; r1: vram_tile_dest ptr; r2: tile_col_count [1..N]. "
        "Copies tile_col_count 32-bit tile words from line buffer to VRAM destination. "
        "Returns void. Side effects: BG tile VRAM region written. "
        "Constants: tile_word_size=4 bytes."),
    ("FUN_080ce218", "render_card_label_text_to_bg",
        "Render a card label text string into BG tile VRAM for the card info display. "
        "Looks up label string from ROM string table, calls render_jp_string_to_tile_line "
        "then write_line_buf_to_bg_tile_vram to commit rendered glyphs. "
        "r0: label_id [0..N]; r1: bg_tile_dest ptr; r2: x_col [0..29]; r3: y_row [0..23]. "
        "Returns void. Side effects: BG tile VRAM written with label text."),
    ("FUN_080cd9a0", "init_card_palette_and_tile_vram",
        "Initialize palette and tile VRAM regions for the card display screen. "
        "Fills OBJ palette and BG palette with card display colors from ROM palette table; "
        "zero-fills BG tile VRAM region for text layer. "
        "No APCS params (reads display state from globals). Returns void. "
        "Side effects: OBJ palette, BG palette, BG tile VRAM written. "
        "Constants: card_palette_table_base in ROM; bios_cpu_set fill mode."),
    ("FUN_080cf330", "init_card_stat_tile_and_scroll",
        "Initialize BG tile data and scroll registers for the card stat display area. "
        "Writes stat label tile indices into BG map VRAM and sets BG scroll registers "
        "to position the stat area. "
        "No APCS params (reads card_display_state from globals). Returns void. "
        "Side effects: BG map VRAM and BG scroll regs written. "
        "Constants: BG2HOFS=0x04000014, BG2VOFS=0x04000016."),
    ("FUN_080eec54", "resolve_game_str_ptr",
        "Resolve a game string pointer from the ROM string table by string_id. "
        "r0: string_id [0..N]. Returns ptr to null-terminated JP string in ROM. "
        "Reads entry from ROM string pointer table (base address from globals), "
        "returns the stored pointer. Pure read-only; no side effects. "
        "indeg=8. Constants: game_str_table_base in ROM."),
    ("FUN_080cf25c", "render_card_numeric_stat_to_bg",
        "Render a numeric card stat (ATK/DEF/LP) as decimal digits into BG tile VRAM. "
        "Calls resolve_game_str_ptr for the stat label, then render_decimal_digits_jp "
        "to rasterize the numeric value. "
        "r0: stat_type [0..N]; r1: stat_value [0..9999]; r2: bg_tile_dest ptr; r3: x_col [0..29]. "
        "Returns void. Side effects: BG tile VRAM written with decimal digit tiles."),
    ("FUN_080cf3b0", "render_card_stat_label_with_value",
        "Render a card stat label string followed by its numeric value into BG tile VRAM. "
        "Calls render_card_label_text_to_bg for the label, then render_card_numeric_stat_to_bg "
        "for the value. "
        "r0: stat_id [0..N]; r1: stat_value [0..9999]; r2: bg_tile_dest ptr; r3: row [0..23]. "
        "Returns void. Side effects: BG tile VRAM written with label+value tiles."),
    ("FUN_080f5054", "copy_cstr_to_buf",
        "Copy a null-terminated C string (ASCII/JP) from src to dst buffer. "
        "r0: dst_ptr; r1: src_ptr. Copies bytes until null terminator (inclusive). "
        "Returns dst_ptr (r0 unchanged). Leaf function. No side effects beyond dst_ptr region. "
        "Constants: none."),
    ("FUN_080d03b0", "init_choice_label_vram_case1",
        "Initialize BG tile VRAM for choice label display variant case 1 (first option). "
        "Writes tile map entries for the first choice label position in the card choice UI. "
        "No APCS params; reads choice_display_state from globals. Returns void. "
        "Side effects: BG map VRAM written for choice label case 1. "
        "Sibling: init_choice_label_vram_case8."),
    ("FUN_080cceb8", "init_choice_label_vram_case8",
        "Initialize BG tile VRAM for choice label display variant case 8 (eighth option). "
        "Writes tile map entries for the eighth choice label position in the card choice UI. "
        "No APCS params; reads choice_display_state from globals. Returns void. "
        "Side effects: BG map VRAM written for choice label case 8. "
        "Sibling: init_choice_label_vram_case1."),
    ("FUN_080cd33c", "render_card_name_label_to_bg",
        "Render the card name string into BG tile VRAM for the card info name row. "
        "Looks up card name JP string via resolve_game_str_ptr(card_id), "
        "calls render_jp_string_to_tile_line then write_line_buf_to_bg_tile_vram. "
        "r0: card_id [0..0x19b7]; r1: bg_tile_dest ptr; r2: x_col [0..29]; r3: y_row [0..23]. "
        "Returns void. Side effects: BG tile VRAM name row written."),
    ("FUN_080c78bc", "init_card_icon_tile_and_palette",
        "Initialize OBJ tile VRAM and palette for card type/attribute icon display. "
        "Copies icon tile data from ROM to OBJ VRAM, writes palette entries for icon colors. "
        "r0: card_type [0..N]; r1: card_attribute [0..N]. Returns void. "
        "Side effects: OBJ tile VRAM and OBJ palette written for icon display. "
        "Constants: icon_tile_table_base in ROM; OBJ_VRAM_BASE=0x06010000."),
    ("FUN_080c3b50", "render_field_zone_mini_card_tiles",
        "Render mini card tile data for a duel field zone slot into BG tile VRAM. "
        "Reads zone slot card_id, looks up mini card tile source from ROM table, "
        "copies tile data to BG VRAM at the zone position. "
        "r0: player_side [0..1]; r1: zone_slot_idx [0..9]; r2: bg_tile_dest ptr. "
        "Returns void. Side effects: BG tile VRAM written with mini card tile data. "
        "Constants: mini_card_tile_table_base in ROM."),
    ("FUN_080c9eb8", "write_decimal_digits_to_oam",
        "Write decimal digit OAM entries for a numeric value (LP/ATK/DEF) to OAM buffer. "
        "Decomposes r0 into decimal digits, looks up digit tile indices, "
        "writes OAM attr0/1/2 entries for each digit sprite. "
        "r0: value [0..9999]; r1: oam_dest ptr; r2: x_start [0..239]; r3: y_pos [0..159]. "
        "Returns void. Side effects: OAM buffer entries written. "
        "Constants: digit_tile_base_idx in OBJ VRAM tile map."),
    ("FUN_08095b50", "check_player_side_condition",
        "Check whether the player_side condition flag is set for a given slot. "
        "Reads gDuelFieldSlots[player_side][slot_idx] condition byte and tests a specific bit. "
        "r0: player_side [0..1]; r1: slot_idx [0..9]. "
        "Returns 1 if condition bit set, 0 otherwise. Pure read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=20 bytes."),
    ("FUN_080c3790", "get_field_slot_tile_vram_addr",
        "Compute the BG tile VRAM address for a duel field zone slot position. "
        "r0: player_side [0..1]; r1: zone_slot_idx [0..9]. "
        "Returns ptr to BG tile VRAM position for the slot. Pure address compute; no side effects. "
        "Constants: field_tile_map_base, slot_x/y layout table in ROM."),

    # --- batch #17 (campaign-17, 2026-05-08) duel field placement/equip activation chain ---
    ("FUN_080c3840", "blit_field_slot_tile_with_palette_hi",
        "Blit field slot tile VRAM with high-palette data. "
        "Calls get_field_slot_tile_vram_addr(player_id,row,col); if addr==0 returns. "
        "Reads ROM palette table 0x09854df0 (0x90 halfwords), OR-merges hi/lo bytes, writes to VRAM. "
        "r0=u16 player_id [0..1], r1=u16 row, r2=u16 col. Returns void. "
        "Side-effects: VRAM [tile_addr..+0x120] overwritten. "
        "Constants: palette_table=0x09854df0, tile_count=0x90."),
    ("FUN_080333ac", "check_slot_placement_blocked_by_field_effect",
        "Returns 0 if slot placement is blocked by active field effect node (indeg=40), 1 if allowed. "
        "Monster zone path (slot 0..4): traverses gDuelNodePool field-spell chain, checks field6 low bits, "
        "matches Yami(0x1432)/Sanctuary(0x17ee) IDs and direction/effect bits. "
        "Spell/trap path (slot 5..9): uses check_slot_card_is_equip_whitelist + get_node_entity_id_in_slot. "
        "r0=u8 player_id [0..1], r1=u8 slot_idx [0..9]. Returns u32 bool (0=blocked, 1=allowed). "
        "Constants: player_stride=0x868, slot_entry=0x14, Yami_id=0x1432, Sanctuary_id=0x17ee."),
    ("FUN_080c3880", "update_field_slot_tile_display",
        "Update field slot tile display: blit palette or zero-fill based on placement block check. "
        "Calls get_field_slot_tile_vram_addr, stores addr in r7. "
        "slot_idx [0..0xa] and check_slot_placement_blocked_by_field_effect==0: "
        "calls blit_field_slot_tile_with_palette_hi. "
        "slot_idx > 0xa or blocked: if VRAM addr valid, calls zero_fill_by_halfword (0x90 halfwords). "
        "r0=u16 player_id [0..1], r1=u16 slot_idx [0..0xa], r2=u16 extra. Returns void. "
        "Side-effects: VRAM [tile_addr..+0x120] written or zeroed. "
        "Constants: slot_range_max=0xa, tile_size=0x120."),
    ("FUN_0803b960", "check_zone_has_no_field_spell_node",
        "Returns 1 if field spell zone has no effect node for card 0x1679 (zone type 0xb), 0 if blocked. "
        "Calls find_effect_node_in_zone(player_id, zone_type=0xb, card_id=0x1679, mode=2); "
        "inverts result: 0=node present (return 0), non-0=absent (return 1). Leaf function. "
        "r0=u8 player_id [0..1]. Returns u32 bool (1=no node/allowed, 0=node exists/blocked). "
        "Constants: zone_type=0xb, card_id=0x1679, search_mode=2."),
    ("FUN_080904f4", "find_card_effect_node_entry",
        "Binary search for card effect node descriptor by card_id and effect_type. "
        "Reads card_id from [r0+0] (u16), effect_type from [r0+3] bits[5:2] [0..3]. "
        "Dispatches to one of four sorted ROM tables: "
        "type=0->0x09e3f19c(0x2a3 entries), type=1->0x09e430fc(0x187), "
        "type=2->0x09e455bc(0x8e), type=3->0x09e46324(0xb7). "
        "Standard binary search (entry_size=0xc, key=first word). "
        "r0=ptr card_info ([+0]=card_id, [+3] bits[5:2]=type [0..3]). "
        "Returns ptr effect_node_descriptor, or 0 if not found. Pure read-only leaf. "
        "Constants: entry_size=0xc, type_max=3."),
    ("FUN_08090848", "dispatch_card_effect_activation",
        "Lookup effect node then dispatch card effect activation via unicast or broadcast handler. "
        "Calls find_card_effect_node_entry; if node==0 returns 1 (no handler). "
        "If node[+0xc] (unicast handler ptr) non-0: saves card_ptr to global slot 0x0201b714, "
        "calls FUN_0810e5d0 unicast handler, restores slot. "
        "If node[+0x8] non-0: calls FUN_0810e5d4 broadcast over 2 players x 11 zones. "
        "r0=ptr card_info, r1=u32 override_param. Returns u32 (0=success, 1=blocked/no-handler). "
        "Side-effects: [0x0201b714] temp card_ptr; [0x0201b290+0x4bc] zeroed on broadcast path. "
        "Constants: global_card_slot=0x0201b714, player_count=2, zone_count=11."),
    ("FUN_08031390", "resolve_slot_id_to_zone_ptr",
        "Convert slot_id to zone descriptor ptr via two-step lookup. "
        "Calls find_zone_descriptor_by_slot_id(slot_id)->descriptor; "
        "if descriptor==0x4000 (invalid sentinel) returns 0. "
        "Else unpacks descriptor bytes as r0/r1/r2 and calls get_zone_slot_ptr. "
        "r0=u32 slot_id. Returns ptr zone_slot (0 if invalid). Pure read-only. "
        "Constants: invalid_sentinel=0x4000."),
    ("FUN_0804bc90", "get_card_equip_zone_rank",
        "Return equip zone rank value for card_id; used in equip target priority comparison. "
        "Reads field6 and field9 extended stats; if field6==0x16 and field9==1 returns 3. "
        "Otherwise performs card_id BST mapping: special IDs->2, default->1. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 rank (1=normal, 2=special, 3=priority path). "
        "Constants: equip_type_continuous=0x16, equip_type_ritual=0x17."),
    ("FUN_08055930", "get_card_lp_cost_by_id",
        "Return LP cost for equip card entry by card_id lookup in large BST table. "
        "Reads card_id from [r0+0], player_side from [r0+2], flag_bits from [r0+3]. "
        "If field6==0x16 (continuous equip) and count_available_effect_zones==0: returns 0 (free). "
        "Otherwise BST card_id->LP cost value; unmatched card_id->0xfa8 (default cost). "
        "r0=ptr equip_card_entry ([+0]=card_id, [+2]=player_side, [+3]=flags). "
        "Returns u32 lp_cost (0=free). Pure read-only computation. "
        "Constants: equip_type_continuous=0x16, default_cost=0xfa8."),
    ("FUN_08033bb0", "check_slot_available_for_card",
        "Returns 1 if slot is empty and placement is not blocked by field effect; 0 otherwise. "
        "Tests active bit (lsls #0x13) of gDuelFieldSlots[player*0x868+slot*0x14]; "
        "if occupied returns 0. If free calls check_slot_placement_blocked_by_field_effect; "
        "returns its result. Used by find_first_available_monster_slot_for_player inner loop. "
        "r0=u8 player_id [0..1], r1=u8 slot_idx [0..4]. Returns u32 bool (1=available, 0=not). "
        "Constants: active_bit_shift=0x13, gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_0803310c", "count_occupied_all_field_zones",
        "Count all occupied field zone slots (11 total: monster 5 + spell/trap 5 + field 1) for player. "
        "Iterates gDuelFieldSlots[player*0x868..+11*0x14] testing active bit (lsls #0x13) per slot; "
        "nonzero->count++. Also checks gP1LifePoints[+0x10d0] bonus flag and [0x0201bb90] turn data "
        "for +1/+2 bonus conditions. "
        "r0=u8 player_id [0..1]. Returns u32 count (0..13). Pure read-only. "
        "Constants: zone_count=11, active_bit_shift=0x13, player_stride=0x868, slot_entry=0x14."),
    ("FUN_08033bf4", "find_first_available_monster_slot_for_player",
        "Find first available monster zone slot for player_id; returns slot ptr or -1. "
        "If count_field_copies_of_card(0x16df)>0 and count_occupied_all_field_zones>4: returns -1 (full). "
        "Iterates node_pool_base 0x09e3ef60 (slots 0..4); "
        "calls check_slot_available_for_card(player_id, slot+5); hit->returns (node+5) ptr. "
        "r0=u8 player_id [0..1]. Returns ptr monster_slot_entry (-1=no available slot). Pure read-only. "
        "Constants: special_card=0x16df, max_zones=5, node_pool_base=0x09e3ef60."),
    ("FUN_0805aea4", "apply_card_equip_activation",
        "Full equip card activation flow: placement rules -> LP check -> slot alloc -> effect dispatch. "
        "Calls check_card_placement_rules; if fails returns 0. "
        "If partner non-0: compares get_card_equip_zone_rank for both cards; rank_self<rank_partner->fail. "
        "Calls get_card_lp_cost_by_id; if LP insufficient writes [gP1LifePoints+0x1d78]=0x17, returns 0. "
        "On success: find_first_available_monster_slot_for_player, updates card[2] zone_bits, "
        "calls dispatch_card_effect_activation; returns its result. "
        "r0=ptr card_info, r1=ptr partner_card_info (0=none). Returns u32 dispatch result. "
        "Side-effects: [gP1LifePoints+0x1d78]:=0x17 on fail; card[+2] zone_bits updated. "
        "Constants: special_equip_id=0x19a3, player_stride=0x868, lp_fail_flag=0x17."),
    ("FUN_0805a238", "check_spell_zone_slot_face_down",
        "Returns 1 if spell/trap zone slot_idx [5..10] is face-down, 0 otherwise. "
        "Out-of-range (slot_idx-5 > 5): returns 0. "
        "Reads gDuelFieldSlots[player*0x868+slot*0x14+0x40] word, extracts bit1 (facedown bit). "
        "r0=u8 player_id [0..1], r1=u8 slot_idx [5..10]. Returns u32 bool. Leaf, pure read. "
        "Constants: spell_zone_start=5, slot_entry=0x14, facedown_bit=bit1, player_stride=0x868."),
    ("FUN_0803026c", "get_card_equip_target_zone_cost",
        "Return zone cost/eligibility value for equip target selection by card_id and zone_bits. "
        "Calls get_card_extended_stat_field9; if field9==1 returns 1 (special pass). "
        "Large BST over card_id: 0x1774/0x158a/0x15fc etc->1; unmatched->0 (ineligible). "
        "r0=u16 card_id [0..0x1fff], r1=u16 zone_bits. Returns u32 (1=eligible, 0=ineligible). Pure read. "
        "Constants: special_field9=1."),
    ("FUN_0805a86c", "check_equip_card_can_target_partner",
        "Validate equip card (r0) can legally target partner card (r1). "
        "If partner non-0: compare get_card_equip_zone_rank for both; rank_self<rank_partner->reject; "
        "rank<=1->reject; check_spell_zone_slot_face_down->reject if face-down. "
        "If partner==0: rank<=1->reject. "
        "Final: get_card_equip_target_zone_cost(card_id, zone_bits)->0->reject. "
        "r0=ptr equip_card_info, r1=ptr partner_card_info (0=none). Returns u32 bool (1=can target). "
        "Side-effects: [gP1LifePoints+0x1d78]:=0x16 on block path. "
        "Constants: rank_threshold=1."),
    ("FUN_08033c9c", "check_field_spell_placement_allowed",
        "Returns 1 if field spell card_id can be placed for player; 0 if blocked. "
        "If get_card_extended_stat_field9(card_id)==2 (dual field): checks count_field_copies_of_card(0x16df), "
        "reads gDuelFieldSlots active bit, calls count_occupied_all_field_zones; >4->return 0. "
        "Else: calls find_first_available_monster_slot_for_player; <0->return 0. "
        "r0=u8 player_id [0..1], r1=u16 card_id [0..0x1fff]. Returns u32 bool. Pure read. "
        "Constants: field9_dual_field=2, full_zone_threshold=4, special_card=0x16df."),
    ("FUN_0804c014", "check_card_is_equip_set_c",
        "equip set C classifier: third sibling alongside check_card_id_is_equip_set_a (0x0804bd78) "
        "and check_card_id_is_equip_set_b (0x0804bf20). "
        "BST whitelist over card_id: hits 0x114f/0xfe0/0x168f/0x179c etc->return 1; else->return 0. "
        "Called by check_card_zone_activation_blocked in continuous equip (field6==0x16) path. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool. Leaf, no side-effects. "
        "Constants: set_c_ids={0xfe0, 0x114f, 0x168f, 0x179c}."),
    ("FUN_0805a570", "check_card_zone_activation_blocked",
        "Comprehensive gate: returns 1 if equip/field-spell card activation is blocked, 0 if allowed. "
        "Reads card_id/player_side/flag_bits from stack buf r0. card_id==0->return 1. "
        "field6==0x16 path: check_card_is_equip_set_c; check_field_spell_placement_allowed; "
        "check_equip_card_can_target_partner; find_effect_node_in_zone; "
        "check_card_is_zone_pair_restricted; check_value_in_slot_chain; count_available_effect_zones. "
        "Final: apply_card_equip_activation. Any fail->return 1. "
        "r0=ptr card_activation_entry ([+0]=card_id, [+2]=player+slot, [+3]=flags), "
        "r1=u32 override_flag [0..1]. Returns u32 bool. "
        "Side-effects: [gP1LifePoints+0x1d78]:=0x14 on block; apply_card_equip_activation side-effects. "
        "Constants: active_flag=0x16."),
    ("FUN_0805b164", "invoke_equip_zone_activation_check",
        "Build equip card activation entry on stack and call check_card_zone_activation_blocked. "
        "Allocates 0x18 bytes stack buf; memset to 0; strh card_id->[buf+0]; "
        "sets [buf+2] bit0=player_id&1 (player_side); writes zone_code=0x16 to [buf+2] bits[5:0]; "
        "reads gDuelFieldSlots[player*0x868+slot*4+0x0201c600] node word into [buf+4]. "
        "Calls check_card_zone_activation_blocked(buf, 0). Returns its result. "
        "r0=u8 player_id [0..1], r1=u16 slot_idx [0..4], r2=u16 card_id [0..0x1fff]. "
        "Returns u32 (1=blocked, 0=allowed). "
        "Constants: buf_size=0x18, zone_code_equip=0x16, node_base=0x0201c600."),

    # --- batch #18 (campaign-18, 2026-05-08) duel field equip/placement validator chain ---
    ("FUN_0804a9dc", "map_field8_to_card_type_category",
        "Maps extended_stat field8 raw value [0..15] to internal card type category code [0..9]. "
        "Calls get_card_extended_stat_field8(card_id); if >15 returns 0 (unknown). "
        "Mapping: 0->0, 1->1, 2->3, 3->3, 4->2, 5->2, 6->1, 7->1, 8->1, 9->0, "
        "10->4, 11->5, 12->6, 13->7, 14->8, 15->9. "
        "Called by check_slot_card_is_equip_type (0x08030b2c) and check_card_has_equip_placement_type "
        "to determine if a card belongs to equip/magic/trap category for placement rules. "
        "r0=u16 card_id [0..0x1fff]. Returns u8 card_type_category [0..9] (0=unknown). "
        "indeg=15."),
    ("FUN_0804b81c", "get_card_special_group_code",
        "Performs large BST over card_id to assign one of 6 special group codes [0..5]. "
        "Group 0=no match/unrestricted, groups 1..5=specific card families "
        "(e.g. 0x17c4/0x1758=group 2, range 0x1585-0x1117=group 1, 0x19cd/0x19ca=group 4). "
        "Called by check_card_has_equip_placement_type when map_field8 result is not in [2,3], "
        "as secondary classification. Pure read-only; no side effects. "
        "r0=u16 card_id [0..0x1fff]. Returns u8 special_group_code [0..5] (0=no match). "
        "indeg=3."),
    ("FUN_0804ba58", "check_card_has_equip_placement_type",
        "Returns 1 if card_id satisfies equip/special placement type condition, 0 otherwise. "
        "First calls map_field8_to_card_type_category: 0->return 0; in [2,3]->return 1 directly; "
        "else calls get_card_special_group_code and treats result>0 as 1. "
        "Used by 20 callers to quickly filter whether a card is allowed into the equip zone "
        "before placement. r0=u16 card_id [0..0x1fff]. Returns u32 bool. "
        "indeg=20, class C. "
        "Constants: category_ritual_or_fusion=[2,3]."),
    ("FUN_0804c18c", "check_card_is_field_spell_type_b",
        "Checks if card_id falls in field_spell type-B ranges: "
        "[0x1497..0x149a] or [0x17ad..0x17ae]. Returns 1 if hit, 0 otherwise. "
        "Leaf function; no callees. Called by check_field_spell_b_placeable (0x080309fc) "
        "as final eligibility gate. Sibling: get_card_effect_zone_check_sides (0x0804c1b8, "
        "returns side_mask vs this returning bool). "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool. indeg=1, class E. "
        "Constants: FIELD_SPELL_B_RANGE1=[0x1497..0x149a], FIELD_SPELL_B_RANGE2=[0x17ad..0x17ae]."),
    ("FUN_080309fc", "check_field_spell_b_placeable",
        "Three-condition chain to check whether field_spell type-B card_id can be placed. "
        "(1) check_value_in_slot_chain(player=0, slot=0xb, value=0x1407) non-zero -> return 1 (blocked); "
        "(2) check_card_targeted_by_spell_zone_effect(card_id, -1) non-zero -> return 1 (blocked); "
        "(3) check_card_is_field_spell_type_b(card_id) -> return its result. "
        "All three pass means placement allowed (returns 0). "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=blocked, 0=placeable). "
        "indeg=2, class E. "
        "Constants: FIELD_SPELL_ZONE=0xb, field_spell_b_effect_id=0x1407."),
    ("FUN_0803b910", "check_lp_exceeds_spell_copy_threshold",
        "Checks whether current player LP exceeds threshold set by copy count of card 0x132c on field. "
        "First calls check_card_targeted_by_spell_zone_effect(card_id, -1): if blocked return 0. "
        "Then count_field_copies_of_card(0x132c) -> copy_count; "
        "threshold = copy_count * 132 (via lsls/subs/lsls/adds/lsls shift sequence); "
        "reads gP1LifePoints + player_side*0x868 for current LP; LP>threshold -> return 1. "
        "r0=u16 card_id [0..0x1fff]; r1=u32 player_side [0..1]. "
        "Returns u32 bool (1=LP exceeds threshold and not blocked, 0=blocked or LP insufficient). "
        "indeg=4. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, copy_card=0x132c, scale=132."),
    ("FUN_0802fb6c", "find_node_by_value_zone_entity",
        "Traverses gDuelNodePool (0x0201d9c0, stride=8) from head_index, returning the first node where "
        "[node+0](u16)==r1(card_id), [node+2]&0xF(zone_type) in [1..2], "
        "[node+2]&0xF0==0 (upper flags clear), and if r2>=0 then [node+4](u16 entity_id)==r2. "
        "r2<0 acts as wildcard (skip entity_id check). "
        "r0=u16 head_index [0..139]; r1=u16 card_id; r2=s32 entity_id (-1=wildcard). "
        "Returns u32* matching node ptr, or 0 (NULL) if not found. Read-only leaf. "
        "indeg=3. "
        "Constants: gDuelNodePool=0x0201d9c0, node_stride=8, zone_type_range=[1..2], flag_mask=0xF0."),
    ("FUN_0802fdf4", "check_slot_has_node_by_card_id",
        "Reads chain head index from gDuelFieldSlots[player_side][slot_idx]+0xa; "
        "calls find_node_by_value_zone_entity(head, card_id, -1) (wildcard entity). "
        "Returns 1 if matching node found, 0 otherwise. "
        "r2=card_id is moved to r3 at entry; r1 is set to -1 for wildcard entity search. "
        "Called by check_field_spell_group_placeable and check_field_spell_card_placeable_strict "
        "to test whether a specific effect is already present in a slot chain. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..11]; r2=u16 card_id. "
        "Returns u32 bool. indeg=10, class D. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, chain_head_offset=0xa."),
    ("FUN_0803b9f4", "check_field_spell_card_placeable_strict",
        "Strict 7-condition check: can player place special field-spell card. "
        "Conditions (all must pass for return 1): "
        "(1) gP1LifePoints+side*0x868+0x11c bit20 == 0; "
        "(2) count_available_effect_zones(player, 0x13ff, -1) != 0; "
        "(3) count_field_copies_of_card(0x12b1) == 0; "
        "(4) check_slot_has_node_by_card_id(player, FIELD_SPELL_ZONE, 0x15ad) == 0; "
        "(5) find_effect_node_in_zone(player, FIELD_SPELL_ZONE, 0x1679, 1) == 0; "
        "(6) check_value_in_slot_chain(player, FIELD_SPELL_ZONE, 0x1578) == 0; "
        "(7) count_available_effect_zones(player, 0x1972, -1) != 0. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=placeable, 0=any condition blocks). "
        "indeg=6, class D. "
        "Constants: FIELD_SPELL_ZONE=0xb, gP1LifePoints=0x0201c4e0, player_stride=0x868."),
    ("FUN_0803b980", "check_field_spell_group_placeable",
        "Combined check: can player place field-spell group card. "
        "If count_field_copies_of_card(0x135d)>0: calls check_field_spell_card_placeable_strict(player); "
        "if strict check fails return 0. "
        "Then sequential checks (any non-zero -> return 0): "
        "check_slot_has_node_by_card_id(player, FIELD_SPELL_ZONE, 0x15ad); "
        "find_effect_node_in_zone(player, FIELD_SPELL_ZONE, 0x1679, mode=1); "
        "check_value_in_slot_chain(player, FIELD_SPELL_ZONE, 0x1578); "
        "count_available_effect_zones(player, 0x1972, -1). "
        "All pass -> return 1. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=placeable, 0=blocked). "
        "indeg=4, class E. "
        "Constants: FIELD_SPELL_ZONE=0xb, group_card=0x135d."),
    ("FUN_0804ba90", "check_card_not_equip_placement_type",
        "Negated wrapper of check_card_has_equip_placement_type with card_id 0x17c4 special exemption. "
        "If card_id==0x17c4: return 0 (exempt, treated as non-equip-type). "
        "Otherwise: call check_card_has_equip_placement_type; result==0->return 1, else->return 0. "
        "I.e. returns 1 when card is NOT equip/special placement type. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool. "
        "indeg=2, class E. "
        "Constants: exempt_id=0x17c4."),
    ("FUN_08033730", "check_slot_card_can_be_equipped",
        "Determines whether the monster in slot (target_player, slot_idx) can be equipped by equip_player. "
        "Reads card_id from gDuelFieldSlots low 13 bits; returns 0 if card_id==0 or slot_idx>4. "
        "count_field_copies_of_card(0x13f2)>0 -> return 0. "
        "If equip_player != target_player: find_effect_node_in_zone(target, slot_idx, 0x13eb, equip_player); "
        "absent -> return 0. "
        "check_value_in_slot_chain twice: 0x16a4 (equip_lock_A) and 0x12d1 (equip_lock_B). "
        "Special: card_id==0x1900 extra VRAM bit flag check. All pass -> return 1. "
        "r0=u32 equip_player_side [0..1]; r1=u32 target_player_side [0..1]; r2=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=equippable, 0=not). Read-only. "
        "indeg=53, class C. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "field_lock_card=0x13f2, equip_blocker=0x13eb, lock_A=0x16a4, lock_B=0x12d1, special=0x1900."),
    ("FUN_08033688", "check_slot_equip_eligibility",
        "Whitelist pre-filter layer before check_slot_card_can_be_equipped. "
        "Reads card_id from gDuelFieldSlots[target_side][slot_idx] low 13 bits; "
        "BST whitelist over special IDs: "
        "0x14f9 -> extra unoccupied check -> return 0; "
        "0x1836 -> extra bit-flag check -> return 0; "
        "0x1670/0x19ee -> other special logic -> return 0. "
        "No whitelist hit: call check_slot_card_can_be_equipped(equip_player, target_player, slot_idx). "
        "r8 (non-APCS, caller-set): u32 equip_player_side (loaded via .hword 0x4684 = mov r4,r8 at entry); "
        "r1=u32 target_player_side [0..1]; r2=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=equippable, 0=not or blocked by whitelist). "
        "indeg=6, class D. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "whitelist_ids=0x14f9/0x1836/0x1670/0x19ee."),
    ("FUN_080337f0", "check_equip_cards_share_field7",
        "Checks that two cards share the same extended_stat field7 and equip conditions are met. "
        "Reads gDuelFieldSlots[target_side][slot_idx]+0x40 word; bit5 != 0 -> return 0 (slot flagged). "
        "If equip_player != target_player: check [slot+0x38] != 0. "
        "Reads slot_card_id (low 13 bits from slot+0x30 word); "
        "BST whitelist: 0x17e9/0x1521/0x1798 or range [0x1874-1..0x1874]. "
        "Calls get_card_extended_stat_field7 twice (equip_card_id from r8, slot_card_id); "
        "equal -> return 1, else -> return 0. "
        "r8 (non-APCS, caller-set): u16 equip_card_id (via .hword 0x468c = mov r4,r8); "
        "r1=u32 target_player_side [0..1]; r2=u32 equip_player_side [0..1]; r3=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=field7 match and equip conditions met, 0=not). "
        "indeg=6, class D. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, bit5_flag_offset=0x40."),
    ("FUN_0803352c", "check_monster_slot_accepts_card",
        "Checks if gDuelFieldSlots[player_side][slot_idx] can accept a new card placement. "
        "Tests bit19 (lsls #0x13): occupied path checks entity state (0x0201bb90) and "
        "check_slot_placement_blocked_by_field_effect; if pass return 1. "
        "Empty slot path: checks gP1LifePoints+side*0x868+0x10a0 bit0 and "
        "check_slot_placement_blocked_by_field_effect; if pass return 1. "
        "Called by count_available_monster_slots (indeg=73) and find_first_placeable_monster_slot. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]. Returns u32 bool (1=accepts, 0=not). "
        "indeg=7, class D. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, entity_state=0x0201bb90, "
        "lp_flag_offset=0x10a0."),
    ("FUN_080335b8", "count_available_monster_slots",
        "Counts monster zone slots [0..4] for player_side that accept new card placement. "
        "Loops slot_idx 0..4 calling check_monster_slot_accepts_card(player, slot_idx); counts returns of 1. "
        "If count_field_copies_of_card(0x16df)>0: clamps valid_count by "
        "max(0, 5 - count_occupied_all_field_zones). "
        "Ultra-high-frequency: indeg=73, class C; used by placement and equip logic. "
        "r0=u32 player_side [0..1]. Returns u32 available_count [0..5]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "special_card=0x16df, monster_zone_count=5."),
    ("FUN_08033654", "find_first_placeable_monster_slot",
        "Reads from ROM slot-order table at 0x09e3ef4c (5 entries x 4 bytes); "
        "for each slot_idx calls check_monster_slot_accepts_card(player, slot_idx); "
        "returns first slot_idx that returns 1. All 5 fail -> returns -1 (0xFFFFFFFF). "
        "Variant sibling of count_available_monster_slots: finds index vs counts. "
        "r0=u32 player_side [0..1]. Returns s32 slot_idx [0..4] or -1. "
        "indeg=5, class D. "
        "Constants: slot_order_table=0x09e3ef4c, table_count=5."),
    ("FUN_08033634", "get_first_placeable_monster_slot",
        "Two-step wrapper: calls count_available_monster_slots(player); if 0 return -1. "
        "If >0: calls find_first_placeable_monster_slot(player) and passes through result. "
        "Callers get combined 'has available slot + first slot index' in one call. "
        "r0=u32 player_side [0..1]. Returns s32 slot_idx [0..4] or -1. "
        "indeg=17, class D."),
    ("FUN_080a4490", "eval_equip_targets_for_card",
        "Evaluates equip card (r1=equip_card_id) target availability for player (r0=player_side). "
        "Returns tri-state: 0=no target; 1=target available; 3=all-target mode. "
        "count_field_copies_of_card(0x13f2)>0 -> return 0. "
        "Loops slot 0..4: check_slot_equip_eligibility (r8=equip_player non-APCS); "
        "on hit: match field6/field7 (r9/r10 counters) + check_slot_placement_blocked_by_field_effect. "
        "Post-loop: field_blocked=1 path returns 3 or 0 by r2/r10; "
        "field_blocked=0 path: get_first_placeable_monster_slot<=0->return 0; r10>2->return 1. "
        "r0=u32 player_side [0..1]; r1=u16 equip_card_id [0..0x1fff]. "
        "Returns u8 equip_eval_result (0=not equippable, 1=equippable, 3=all-target). "
        "indeg=1, class E. "
        "Constants: field_lock_card=0x13f2."),
    ("FUN_0804c6cc", "get_paired_card_id_by_variant",
        "Maps input card_id to its paired card_id via 6-entry switch. "
        "Subtracts 0x164a from card_id to get variant_index; if outside [0..5] return 0. "
        "Switch: 0->0x165c, 1->0x165d, 2->0x165e, 3->0x165f, 4->0x1660, 5->0x1661. "
        "I.e. card_id 0x164a..0x164f each maps to associated pair ID 0x165c..0x1661. "
        "Out-of-range returns 0. "
        "r0=u16 card_id [0..0x1fff] (typically 0x164a..0x164f). "
        "Returns u16 paired_card_id (0x165c..0x1661) or 0. "
        "indeg=5, class D. "
        "Constants: variant_base=0x164a, paired_base=0x165c, variant_count=6."),

    # --- batch #19 (campaign-19, 2026-05-08) duel field equip activation/scan cluster ---
    ("FUN_080338b8", "count_equip_placements_with_chain_check",
        "Count legal equip-card placement slots for equip_card r0, optionally checking equip chain pairing. "
        "Entry guard: count_field_copies_of_card(0x13f2); if >0 return 0 (duplicate blocked). "
        "Double loop player=0..1 x slot_idx=0..4 over gDuelFieldSlots: "
        "(1) check active bit (lsls #0x13); (2) call check_slot_equip_eligibility; "
        "(3) if r10 in range [..0x164f] and r2!=0 enter chain pairing path: "
        "traverse existing equip nodes, call get_paired_card_id_by_variant + "
        "find_equip_chain_node_by_slot_pair; on hit call check_equip_cards_share_field7 and count++. "
        "Returns total legal placement count (0=cannot place). "
        "r0=u16 card_id [0..0x1fff]; r2=u32 chain_check_flag [0=skip, 1=check]; "
        "r8 (non-APCS, caller-set)=u32 equip_player_side [0..1]; "
        "r10 (non-APCS, caller-set)=u32 target_slot_idx [0..4]. "
        "Returns u32 count [0..10]. Read-only. "
        "Constants: card_id_guard=0x13f2, slot_range_max=0x164f, "
        "gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14."),
    ("FUN_080a4648", "check_player_can_place_card",
        "Check whether player can place at least one card in the monster zone. "
        "Fast path: get_first_placeable_monster_slot(player) >= 0 -> return 1. "
        "Slow path: iterate slot 0..4; if mode_flag>0 call check_slot_card_can_be_equipped, "
        "else call check_slot_equip_eligibility; on slot pass call "
        "check_slot_placement_blocked_by_field_effect; unblocked -> return 1. "
        "All fail -> return 0. "
        "r0=u32 player_side [0..1]; r1=s32 mode_flag (>0=can_be_equipped, <=0=equip_eligibility). "
        "Returns u32 bool (1=can place, 0=no available slot). Read-only. "
        "Constants: slot_count=5 [0..4], gDuelFieldSlots=0x0201c510."),
    ("FUN_0804b164", "check_card_id_is_normal_summon_type",
        "Check whether card_id belongs to the normal-summon card ID whitelist via BST interval checks. "
        "Pure leaf; no callees. Main interval [0x13cb..0x194e] with sub-intervals; "
        "extra single IDs: 0x18f9, 0x1981, 0x19a6, 0x19b4, 0x19ef. "
        "Returns 1 if in any whitelist range, 0 otherwise. "
        "Called by AI placement hub (FUN_080a46a0) as card-type filter before normal-summon check. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=normal-summon type). "
        "Constants: whitelist_max=0x194e, extra_ids=0x18f9/0x1981/0x19a6/0x19b4/0x19ef."),
    ("FUN_080a4574", "check_equip_slot_has_field_spell_target",
        "Check whether a valid Field Spell target card exists in the equip slots for player (r0), slot (r1). "
        "Guard 1: count_available_monster_slots(player)==0 -> return 0. "
        "Guard 2: eval_equip_bonus_for_slot(player, slot_idx) <= 4 -> return 0. "
        "Main scan: read gP1LifePoints+0x14+player*0x868 count; traverse descending (r4=count-1..0) "
        "over 0x0201c8f8 zone array; compare card_id low 13 bits to 0x197f (target Field Spell ID); "
        "hit: call find_effect_node_in_zone(player, zone=0xb); found -> return 1. "
        "All fail -> return 0. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=field spell target present). Read-only. "
        "Constants: FIELD_SPELL_ZONE=0xb, target_card_id=0x197f, "
        "gP1LifePoints=0x0201c4e0, player_stride=0x868, zone_array=0x0201c8f8."),
    ("FUN_08032e20", "count_equip_slots_meeting_atk_threshold",
        "Count monster-zone slots for player (r0 bit0) matching target_card_id (r12, non-APCS) "
        "and atk >= atk_threshold (r2). "
        "Slot iteration: slot_entry stride=0x14 starting at +0x64 (slot 5). "
        "Per slot: (1) card_id low 13 bits == r12; (2) slot[+0x10] bit5==0 and bit1==0; "
        "(3) ldrh[slot+0x8]!=0; (4) slot[+0xc] >= r2 (atk_threshold). All pass -> r5++. "
        "Pure leaf; no callees. "
        "r0=u32 player_side [0..1]; r2=u32 atk_threshold; "
        "r12 (non-APCS, caller-set)=u16 target_card_id [0..0x1fff]. "
        "Returns u32 count [0..5]. Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry=0x14, equip_zone_base_offset=0x64, flag_bit5=0x20, flag_bit1=0x2."),
    ("FUN_08033610", "count_monster_slots_accepting_card",
        "Count monster zone slots [0..4] for player (r0) that accept new card placement. "
        "Loops slot_idx 0..4 calling check_monster_slot_accepts_card(player, slot_idx); "
        "counts returns of 1. Returns r5=total accepting slot count [0..5]. "
        "Counting sibling of count_available_monster_slots (which only checks presence). "
        "Called by check_equip_card_activation_valid and check_banisher_of_light_activatable. "
        "r0=u32 player_side [0..1]. Returns u32 count [0..5]. "
        "Constants: slot_count=5 [0..4]."),
    ("FUN_080a45f4", "check_equip_card_activation_valid",
        "Determine whether a special-summon-type equip card can be legally activated for player (r0, slot r1). "
        "Three-guard chain: (1) count_field_copies_of_card(0x13f2)>0 -> return 0; "
        "(2) count_monster_slots_accepting_card(player)==0 -> return 0; "
        "(3) eval_equip_bonus_for_slot(player,slot_idx) <= 4 -> return 0. "
        "Bonus classification: 5..6 -> mode=1 (weak); >6 -> mode=2 (strong). "
        "Final: call count_equip_slots_meeting_atk_threshold(player, card_id=0x19b2, mode); "
        "if >0 return 1, else return 0. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=valid, 0=invalid). Read-only. "
        "Constants: guard_card_id=0x13f2, atk_threshold_card=0x19b2, "
        "equip_bonus_threshold=4, mode_weak=1, mode_strong=2."),
    ("FUN_080a46a0", "eval_card_placement_flags_for_ai",
        "AI placement decision core: evaluates card_id (r4, non-APCS) for player (r5, non-APCS), "
        "returns placement suggestion flag-set r6. "
        "Non-APCS inputs via .hword mov instructions: r4=card_id, r5/r8=player_side, r10=slot_data. "
        "Main flow: (1) card_id==0 or check_card_field5_is_nonzero fail -> return 0; "
        "(2) check_card_targeted_by_spell_zone_effect; (3) check_lp_exceeds_spell_copy_threshold; "
        "(4) count_field_copies_of_card(0x135d) guard; "
        "(5) large card_id BST dispatch: calls check_field_spell_card_placeable_strict / "
        "check_field_spell_group_placeable / eval_equip_targets_for_card / "
        "count_available_monster_slots / count_equip_placements_with_chain_check / "
        "check_player_can_place_card / check_equip_card_activation_valid / "
        "count_paired_slots_with_field5_default; accumulates results via orrs r6; "
        "(6) return r6. "
        "r5 (non-APCS)=u32 player_side [0..1]; r4 (non-APCS)=u16 card_id [0..0x1fff]; "
        "r8 (non-APCS)=u32 player_side copy; r10 (non-APCS)=u32 slot_data; "
        "sp[0]=u32 additional_flag. "
        "Returns u32 placement_flags (0=do not place). "
        "Side-effects: [gP1LifePoints+0x1d78] := 0x10/0x11/0x17/0xb on block paths. "
        "Constants: gDuelFieldSlots=0x0201c510, gP1LifePoints=0x0201c4e0, "
        "player_stride=0x868, FIELD_SPELL_ZONE=0xb, guard_card_id=0x135d."),
    ("FUN_080a4694", "eval_card_placement_flags_default",
        "One-parameter wrapper of eval_card_placement_flags_for_ai (FUN_080a46a0) "
        "with fixed chain_check_flag r2=1 (standard check). "
        "Body: push lr; movs r2,#0x1; bl eval_card_placement_flags_for_ai; pop bx. "
        "Callers avoid manually setting r2. "
        "r0=u32 pass-through player_side [0..1]; r1=u32 pass-through param. "
        "Returns u32 placement_flags (same as eval_card_placement_flags_for_ai). "
        "Side-effects: same as eval_card_placement_flags_for_ai. "
        "Constants: chain_check_flag=1 (fixed)."),
    ("FUN_080313dc", "get_equip_card_set_code_for_slot",
        "Read the equip card set_code for slot (r0=player_side bit0, r1=slot_idx). "
        "Flow: locate gDuelFieldSlots[player][slot_idx] (stride 0x14); extract card_id low 13 bits; "
        "if not equip set A (check_card_id_is_equip_set_a) -> return 0. "
        "If active flag 0xa5600000: if slot_idx<=4 call find_equip_chain_pair_across_field(player,slot_idx); "
        "result lsls #0x10 == 0xffff0000 (no pair) -> return 0; "
        "else return ldrh[slot+0xc] (set_code). "
        "Not active: return ldrh[slot+0xc] directly. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]. "
        "Returns u16 set_code (0=invalid or no pair). Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, "
        "active_flag=0xa5600000, no_pair_sentinel=0xffff0000, set_code_offset=0xc."),
    ("FUN_080a533c", "check_equip_slot_pair_can_activate",
        "Check whether the equip-card pair at slot (r0=player, r1+r2=slot) can activate. "
        "Guard: (r1+r2)>4 -> return 0. "
        "Read current player bit0 from 0x0201e4d0, call check_slot_card_can_be_equipped. "
        "If equippable and active (lsls #0x13 == 0x85e00000): call count_available_monster_slots; "
        "if 0: player mismatch -> return 0; else call check_slot_placement_blocked_by_field_effect. "
        "Set_code dispatch: read 0x0201e4d0 word, extract set_code (lsls #0x9 lsrs #0x11); "
        "compare to 0xfdf / 0xfe9 paths; call get_equip_card_set_code_for_slot + "
        "check_slot_card_pair_allowed; success -> return 0x800; else -> return 0. "
        "r0=u32 player_side [0..1]; r1=u32 base_slot_idx [0..4]; r2=u32 slot_offset [0..4]; "
        "r9 (non-APCS, caller-set)=u32 match_threshold. "
        "Returns u32 (0=cannot activate, 0x800=can activate). Read-only. "
        "Constants: slot_max=4, active_flag=0x85e00000, "
        "set_code_a=0xfdf, set_code_b=0xfe9, state_base=0x0201e4d0, success=0x800."),
    ("FUN_080a3a80", "scan_activatable_equip_slots_init",
        "Initialize equip activation state struct (0x0201e4d0) then scan all field slots for "
        "an activatable equip pair. "
        "Init: byte[0] := (r0&1) | (old & ~0x2) (player bit0); word[0] updated with r1 high byte; "
        "byte[0x12] |= 0x2 (activate-phase flag); byte[0x8] := 0. "
        "Double loop player=0..1 x slot_idx=0..4: call check_equip_slot_pair_can_activate(p,s,0); "
        "non-0 -> return 1 immediately. All fail -> return 0. "
        "r0=u32 player_side [0..1]; r1=u32 card_context (low 15 bits written to state struct). "
        "Returns u32 bool (1=at least one activatable equip pair found, 0=none). "
        "Side-effects: [0x0201e4d0] byte/word/byte[0x12]/byte[0x8] updated. "
        "Constants: state_base=0x0201e4d0, player_mask=0x7fff, activate_flag=0x2, "
        "player_loop=[0..1], slot_loop=[0..4]."),
    ("FUN_08031184", "find_slot_idx_by_set_code",
        "Search player (r0 bit0) hand/slot list for a slot matching set_code r1; return its index. "
        "Reads count from gP1LifePoints+0x10+player*0x868; "
        "iterates gP1LifePoints+player*0x868+0x98*4 (offset 0x260) array: "
        "extracts low 13 bits (set_code) per slot word via (lsls #0x2 lsrs #0x18)*2 + (lsls #0x12 lsrs #0x1f); "
        "matches against r1 -> return index r3. "
        "Not found -> return -1 (rsbs #0). "
        "r0=u32 player_side [0..1]; r1=u16 target_set_code [0..0x1fff]. "
        "Returns s32 slot_idx [0..count-1] or -1. Read-only. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "count_offset=0x10, base_offset=0x98*4=0x260."),
    ("FUN_080324b4", "find_equip_slot_by_card_id",
        "Search player (r0 bit0) equip zone slots [5..9] for first slot with card_id==r1. "
        "Iteration: gDuelFieldSlots+player*0x868+0x64 (slot 5 base), stride 0x14; r4 starts at 5. "
        "Per slot: card_id low 13 bits != 0, ldrh[slot+0x8]!=0, card_id==r1 -> return r4 (5..9). "
        "All fail -> return -1. "
        "r0=u32 player_side [0..1]; r1=u16 target_card_id [0..0x1fff]. "
        "Returns s32 slot_idx [5..9] or -1. Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "equip_zone_offset=0x64 (slot 5), equip_zone_count=5, sentinel=-1."),
    ("FUN_08033088", "check_toon_world_equip_present",
        "Check whether equip zone of player (r0) contains card_id=0x12be (Toon World). "
        "Calls find_equip_slot_by_card_id(player, 0x12be): found -> slot in [5..9] (positive); "
        "not found -> -1. "
        "mvns r0,r0: positive -> negative; -1 -> 0. lsrs r0,r0,#0x1f: negative -> 1; 0 -> 0. "
        "Result: found (Toon World present) -> 1; not found -> 0. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=Toon World equip present). "
        "Constants: target_card_id=0x12be (DAT_08033098)."),
    ("FUN_080a57b8", "check_equip_slot_pair_can_activate_alt",
        "Alternate variant of check_equip_slot_pair_can_activate for set_code 0x1895/0x19a6. "
        "Guards: current player bit0 ([0x0201e4d0] byte bit0)==r4 and r5=(r1+r2)<=4. "
        "Active check: lsls #0x13 on gDuelFieldSlots slot. "
        "count_available_monster_slots: if 0 and player mismatch -> return 0; "
        "else check_slot_placement_blocked_by_field_effect. "
        "Set_code dispatch: 0x1895 -> pair_code=0x1522 (DAT_080a5838); "
        "0x19a6 -> pair_code=0x18f9 (DAT_080a5850); "
        "call check_slot_card_pair_allowed(player, slot, pair_code); success -> return 0x800; else 0. "
        "r0=u32 player_side [0..1]; r1=u32 base_slot_idx [0..4]; r2=u32 slot_offset [0..4]. "
        "Returns u32 (0=cannot activate, 0x800=can activate). Read-only. "
        "Constants: state_base=0x0201e4d0, set_code_c=0x1895, set_code_d=0x19a6, "
        "pair_1895=0x1522, pair_19a6=0x18f9, success=0x800."),
    ("FUN_080a3d0c", "scan_activatable_equip_slots_alt",
        "Symmetrical alternate variant of scan_activatable_equip_slots_init; "
        "calls check_equip_slot_pair_can_activate_alt (FUN_080a57b8, set_code 0x1895/0x19a6). "
        "Same init sequence for 0x0201e4d0: player bit0, r1 high byte, byte[0x12]|=0x2, byte[0x8]:=0. "
        "Double loop player=0..1 x slot_idx=0..4: "
        "call check_equip_slot_pair_can_activate_alt(p,s,0); non-0 -> return 1. "
        "All fail -> return 0. "
        "r0=u32 player_side [0..1]; r1=u32 card_context. "
        "Returns u32 bool (1=alt activatable pair found, 0=none). "
        "Side-effects: same as scan_activatable_equip_slots_init. "
        "Constants: state_base=0x0201e4d0, player_loop=[0..1], slot_loop=[0..4]."),
    ("FUN_080a3c2c", "check_banisher_of_light_activatable",
        "Check whether equip card 0x1332 (Banisher of the Light) can be activated. "
        "Guard: count_field_copies_of_card(0x1332)>0 -> return 0 (duplicate blocked). "
        "Init 0x0201e4d0 state struct (same sequence as scan_activatable_equip_slots_init). "
        "BST dispatch on card_id (r4=r1): "
        "0x19a3->fnptr=0x080a839d loop_count=3; 0x19a4->fnptr=0x080a840d loop_count=3; "
        "0x19c8->fnptr=0x080a8479 loop_count=2; else->loop_count=0. "
        "Outer loop slot_idx=0..10: call FUN_0810e5e4 trampoline (bx fnptr)(player,slot,0); "
        "slot<=4 and hit -> r8|=1 (flag); loop_count--. "
        "loop_count==0: if r8 set or count_monster_slots_accepting_card>0 -> return 1; else 0. "
        "r0=u32 player_side [0..1]; r1=u32 card_id_context [0..0x1fff]. "
        "Returns u32 bool (1=activatable, 0=not). "
        "Side-effects: [0x0201e4d0] struct fields updated. "
        "Constants: guard_card_id=0x1332, state_base=0x0201e4d0, slot_loop=0..10, "
        "set_A=0x19a3, set_B=0x19a4, set_C=0x19c8."),
    ("FUN_080a3dac", "check_equip_set_activatable_for_player",
        "Determine whether player (r0) has any activatable equip card pair on the field. "
        "Flow: count_available_monster_slots(player)->r10; "
        "count_field_copies_of_card(0x13f2)>0 -> return 0. "
        "Load 3-word slot_order_table from ROM (0x09e47898) to stack via ldmia/stmia. "
        "Double loop outer idx=0..2 x inner slot=0..4: "
        "read card_id r9 from sp[idx*4] (slot_order ROM word); "
        "compare gDuelFieldSlots[player][slot] card_id to r9; hit: "
        "check_slot_card_can_be_equipped -> check_slot_placement_blocked_by_field_effect; "
        "unblocked -> r10++. "
        "Symmetric scan for opponent slots. "
        "Final: r10>3 -> return 1; else 0 (if sp[0x10] unset -> return 0). "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=activatable pair present). Read-only. "
        "Constants: guard_card_id=0x13f2, slot_order_table=0x09e47898, "
        "gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_0803bc24", "check_spell_zone_slot_placeable",
        "Comprehensive check: is the spell/trap zone available for placement for player (r0)? "
        "Phase 1: count_available_effect_zones(1-r0, 0xa4<<5=0x1480, -1); "
        "non-0 (opponent has available zones) -> skip to return 0 path. "
        "Phase 2: count_field_copies_of_card(0x159d); >0 -> return 0. "
        "Both guards pass -> return 1 (zone placeable). "
        "Side path: DAT_0203e2a0[+8]==r2 (slot context match): "
        "gP1LifePoints+0x1d4c state check + play_ui_effect(0x31) / play_ui_effect(0x32) UI triggers. "
        "Special path LAB_0803bd04: reads 0x0201b870+0x300 byte bit7, calls check_player_side_condition. "
        "indeg=29; used as gate in placement/equip activation chains. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=zone placeable, 0=blocked). "
        "Side-effects: play_ui_effect(0x31)/play_ui_effect(0x32) triggered conditionally. "
        "Constants: count_available_effect_zones_param=0x1480, guard_card_id=0x159d, "
        "gP1LifePoints=0x0201c4e0, ui_sfx_occupied=0x31, ui_sfx_blocked=0x32."),

    # --- batch #20 (campaign-20, 2026-05-08) duel core spell/equip activation eval cluster ---
    ("FUN_080a422c", "classify_spell_card_activation_type",
        "Maps card_id to spell activation type code: 0=normal/unsupported, 1=equip, 2=field_spell, "
        "3=special_field. Multi-branch BST; key boundaries 0x16c6/0x1487/0x16cb/0x18b4/0x19ca. "
        "Leaf function, bx lr exit. "
        "r0=u16 card_id [0..0x1fff]. Returns u8 activation_type [0..3]."),
    ("FUN_0808da68", "find_effect_record_index_by_id",
        "Binary search on ROM effect record table (0x09e5a128, 0x132 entries, 8 bytes each) "
        "for effect_id (r0). Returns table index [0..0x131] if found, -1 if not found. "
        "r0=u16 effect_id. Returns s32 index (-1=not found). Leaf, pure read-only. "
        "Constants: table_base=0x09e5a128, entry_count=0x132, entry_size=8."),
    ("FUN_0808dab0", "dispatch_effect_handler_by_card_id",
        "Look up card_id (r1) in ROM effect record table (0x09e5a128); read fn ptr at [+4]; "
        "call via FUN_0810e5d4 trampoline. Clears gEffectContext+0xc before call; "
        "reads that field as return value after. "
        "100+ callsites; central spell/trap effect dispatch entry. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 handler_result (from gEffectContext+0xc). "
        "Side-effects: gEffectContext+0xc cleared then written by handler. "
        "Constants: effect_table=0x09e5a128, gEffectContext=0x0201e4f0, result_field_offset=0xc."),
    ("FUN_0803bb04", "check_field_spell_neo_daedalus_placeable",
        "Check whether player (r0) can place Neo Daedalus family field spell. "
        "Checks gP1LifePoints[side*0x868+0x11c] bit21; count_field_copies_of_card(0x147f/0x12b1) > 0 -> 0; "
        "check_slot_has_node_by_card_id(player, 0xb, 0x15ad) nonzero -> 0; "
        "find_effect_node_in_zone(player, 0xb, 0x1679, 1) nonzero -> 0. All pass -> return 1. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=placeable, 0=blocked). "
        "Constants: FIELD_SPELL_ZONE=0xb, gP1LifePoints+0x11c=field_state_word."),
    ("FUN_0803bb7c", "check_field_spell_neo_daedalus_group_placeable",
        "Check whether player (r0) can place Neo Daedalus field spell group card. "
        "count_available_effect_zones(player, 0x13ff, -1) nonzero -> return 0; "
        "else call check_field_spell_neo_daedalus_placeable and forward result. "
        "85 callsites; core gate for duel field spell activation. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=placeable, 0=blocked). "
        "Constants: effect_zone_id=0x13ff, FIELD_SPELL_ZONE=0xb."),
    ("FUN_080a42b0", "eval_spell_card_activation_placeable",
        "Comprehensive check whether player (r0) can activate spell card (r1=card_id). "
        "Steps: classify_spell_card_activation_type -> check_value_in_slot_chain(0x14a0) -> "
        "check_field_spell_neo_daedalus_group_placeable -> check_spell_zone_slot_placeable -> "
        "count_available_monster_slots; dispatches loop or dispatch_effect_handler_by_card_id. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 bool (1=activatable, 0=blocked). "
        "Constants: chain_check_id=0x14a0, player_stride=0x868, gDuelFieldSlots=0x0201c510."),
    ("FUN_08037a2c", "count_valid_monster_pair_slots",
        "Count monster zone slots for player (r0) satisfying check_card_pair_allowed. "
        "r8=target_card_id is non-APCS caller-set implicit input. "
        "Iterates [gP1LifePoints+side*0x868+0xc] monster slots; lsls/lsrs #19 extracts card_id. "
        "r0=u32 player_side [0..1]; r8 (non-APCS, caller-set)=u16 target_card_id [0..0x1fff]. "
        "Returns u32 count [0..5]. Pure read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, monster_count_offset=0xc, slot_entry=0x14."),
    ("FUN_080a3eb4", "eval_equip_card_placeable_for_player",
        "Evaluate whether player (r0) can activate equip spell (r10=equip_card_id, non-APCS). "
        "count_available_monster_slots -> count_field_copies_of_card(0x13f2) > 0 -> return 0; "
        "dual-side 5-slot loop check_slot_card_can_be_equipped + check_slot_placement_blocked_by_field_effect; "
        "call count_valid_monster_pair_slots for pairing check. "
        "r0=u32 player_side [0..1]; r10 (non-APCS, caller-set)=u16 equip_card_id [0..0x1fff]. "
        "Returns u32 bool (1=placeable, 0=blocked). "
        "Constants: lockdown_card_id=0x13f2, gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_08032fa4", "count_unpaired_slots_for_card",
        "Count player (r0) slots 0..10 satisfying check_slot_card_pair_allowed "
        "AND find_paired_zone_entry_for_card==0 (unpaired). "
        "Used to evaluate available unpaired target slots before ritual/fusion activation. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 count [0..10]. Pure read-only. "
        "Constants: slot_range=[0..10], player_stride=0x868."),
    ("FUN_080a4134", "check_ritual_fusion_pairable_slots_exist",
        "Check whether player (r0) field has unpaired slots for ritual/fusion card (r1=card_id). "
        "Branches on card_id (0x15f9/0x15fa/0x15fb/0x15b0/0x15b3/0x15b4/0x1947/0x194b/0x1953/0x1954) "
        "and calls count_unpaired_slots_for_card once or twice; any nonzero -> return 1. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 bool (1=pairable slot exists, 0=none)."),
    ("FUN_080a40bc", "check_equip_target_monster_placeable",
        "Check whether player (r0) can place equip spell on a target monster slot. "
        "gP1LifePoints+0x11c bit17 equip lock -> check_value_in_slot_chain(0xb, 0x12f3) nonzero -> return 0; "
        "count_field_copies_of_card(0x13f2) > 0 -> return 0; "
        "5-slot loop check_slot_card_can_be_equipped; r7 > 1 -> return 1. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=can place, 0=blocked). "
        "Constants: FIELD_SPELL_ZONE=0xb, lock_chain_id=0x12f3, lockdown_card_id=0x13f2."),
    ("FUN_080339d8", "count_equippable_slots_for_card",
        "Count across both players' 5 monster slots satisfying check_slot_card_can_be_equipped "
        "for equip_card_id (r0). r10=slot_key non-APCS (encodes (player_byte<<8)|slot_byte, exclude self); "
        "result accumulated in r8. "
        "Pre-check: count_field_copies_of_card(0x13f2) > 0 -> return 0. "
        "r0=u32 equip_card_id [0..0x1fff]; r10 (non-APCS, caller-set)=u32 slot_key. "
        "Returns u32 count [0..10] via r8. "
        "Constants: lockdown_card_id=0x13f2, gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_080a3fc8", "eval_equip_card_multi_target_placeable",
        "Evaluate whether equip spell (r8=equip_card_id, non-APCS) has more than one legal target "
        "for player (r0). count_equippable_slots_for_card <= 1 -> return 0. "
        "Dual-layer scan both players' 5 slots: check_slot_card_can_be_equipped + slot[+8] equip check "
        "+ card type comparison. "
        "r0=u32 player_side [0..1]; r8 (non-APCS, caller-set)=u16 equip_card_id [0..0x1fff]. "
        "Returns u32 bool (1=multi-target available, 0=single or none). "
        "Constants: slot_range=[0..4], player_range=[0..1], gDuelFieldSlots=0x0201c510."),
    ("FUN_0803b1a4", "resolve_best_target_slot_for_equip",
        "Thin wrapper: calls resolve_slot_chain_best_target with r2=0 (best_target mode). "
        "3-instruction function body. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]. "
        "Returns u32 result_ptr (0=not found; nonzero=best target). "
        "Constants: mode=0 (best_target resolve mode)."),
    ("FUN_080a43c8", "eval_spell_equip_target_availability",
        "Evaluate whether equip spell activation (r0=player, r1=card_id) has legal targets. "
        "Pre-gates: check_field_spell_neo_daedalus_group_placeable == 0 -> return 0; "
        "check_spell_zone_slot_placeable == 0 -> return 0. "
        "Main path: iterate 5 slots calling resolve_best_target_slot_for_equip; "
        "r12++ (single target) / r9++ (multi target). "
        "Monster slot path: dispatch_effect_handler_by_card_id x2 (mode 0/1). "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 bool (1=target exists, 0=none). "
        "Constants: FIELD_SPELL_ZONE=0xb, chain_check_id=0x14a0, player_stride=0x868."),
    ("FUN_08032ccc", "count_equipped_paired_slots_for_player",
        "Count player (r0) spell zone slots satisfying check_slot_card_pair_allowed "
        "AND slot[+8] nonzero (equipped). "
        "r8=slot_count_upper non-APCS (loop upper bound); r10=target_card_id non-APCS. "
        "Iterates slots 0..9. "
        "r0=u32 player_side [0..1]; r8 (non-APCS)=u32 slot_count_upper; "
        "r10 (non-APCS)=u16 target_card_id [0..0x1fff]. "
        "Returns u32 count [0..9]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_equip_offset=0x8."),
    ("FUN_080a80a8", "check_slot_equip_target_eligible",
        "Check whether monster slot (r12=base_slot_idx, non-APCS) is a valid equip target for player (r0). "
        "Reads gSpellContext+0 (0x0201e4d0) bit0 (player_bit) and extracts equip_card_id; "
        "gSpellContext+8 == 0: BST on equip_card_id to get expected field7, compare via "
        "get_card_extended_stat_field7; triple filter: check_slot_zone_bit_eligible + "
        "count_available_monster_slots + check_slot_placement_blocked_by_field_effect. "
        "Pass -> return 0x800 (valid flag). "
        "r0=u32 player_side [0..1]; r12 (non-APCS, caller-set)=u32 base_slot_idx [0..4]. "
        "Returns u32 (0x800=eligible, 0=not). "
        "Constants: gSpellContext=0x0201e4d0, gDuelFieldSlots=0x0201c510, valid_return=0x800."),
    ("FUN_080a4058", "init_spell_activation_context",
        "Initialize spell activation context (gSpellContext=0x0201e4d0) for player (r0). "
        "Writes player_side to bit0, card_id to bits[22:8], sets bit1 of [+0x12], clears [+0x8]. "
        "Loops slots 0..4 calling check_slot_equip_target_eligible; any nonzero -> return 1. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 bool (1=eligible slot found, 0=none). "
        "Side-effects: gSpellContext fields updated. "
        "Constants: gSpellContext=0x0201e4d0, player_bit=bit0, slot_range=[0..4]."),
    ("FUN_0804b350", "check_card_id_in_fusion_target_range",
        "Check whether card_id (r0; entry adds r1,r0,#0 captures it) is in fusion target ID ranges. "
        "BST ranges: [0x17c7..0x17c9], single 0x152e, [0x18b2..0x18b3]. "
        "Leaf function, bx lr. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=in fusion target range, 0=not). "
        "Constants: range1=[0x17c7..0x17c9], single=0x152e, range2=[0x18b2..0x18b3]."),
    ("FUN_0802f1f8", "count_slot_chain_copies_of_card",
        "Count nodes in slot (r0=player, r1=slot_idx) equip chain matching card_id (r2). "
        "Reads [slot+0xa] chain head; traverses nodes; zone_type_byte > 5 -> skip; "
        "reverse-lookup gDuelFieldSlots card_id and compare to r2; match -> r5++. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..11]; r2=u16 target_card_id [0..0x1fff]. "
        "Returns u32 count [0..chain_len]. Pure read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, node_pool=0x0201D9C0, player_stride=0x868."),

    # --- batch #21 (campaign-21, 2026-05-08) duel field equip activation eval cluster ---
    ("FUN_080a5498", "check_equip_slot_pair_can_activate_full",
        "Core equip slot pair activation checker. "
        "Guards: (r1+r2)<=4; reads [0x0201e4d0] activation state, gDuelFieldSlots. "
        "Dispatches on set_code (0x112e/0x128c/0x1758/0x1895/0x19a6) to specialized sub-checks; "
        "default path: check_slot_card_can_be_equipped + check_slot_placement_blocked_by_field_effect. "
        "r0=u32 player_side [0..1]; r1=u32 base_slot_idx [0..4]; r2=u32 slot_offset [0..4]. "
        "Returns u32 (0x800=can activate, 0=cannot). Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, state_base=0x0201e4d0, "
        "success=0x800, set_code_sphinx=0x112e, set_code_sphinx_teleia=0x128c, "
        "set_code_ra=0x1758, set_code_c=0x1895, set_code_d=0x19a6."),
    ("FUN_080a5714", "check_equip_slot_can_activate_with_context",
        "check_equip_slot_pair_can_activate_full looser variant with count-list prohibition check. "
        "Entry: r4=(r1+r2)<=4 guard; reads [0x0201e4d0+8] count; "
        "count==0: (A) count_available_monster_slots==0 and player bit0 mismatch -> return 0; "
        "(B) else check_slot_placement_blocked_by_field_effect. "
        "count>0: scan [state+0xc] prohibition pair list; hit (player,slot) -> return 0. "
        "Tail-calls check_equip_slot_pair_can_activate_full(r0, r1, r2). "
        "Non-APCS: r8 saves slot_offset at entry (.hword 0x4690 = mov r8,r2) for tail-call restore. "
        "r0=u32 player_side [0..1]; r1=u32 base_slot_idx [0..4]; r2=u32 slot_offset [0..4]. "
        "Returns u32 (0x800=can activate, 0=cannot). Read-only. "
        "Constants: state_base=0x0201e4d0, gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_080a3ae8", "scan_equip_activation_for_player",
        "Scan all field equip slots for player and return 1 if any activatable slot exists. "
        "Init: writes player_side bit0 to [0x0201e4d0] byte0, player<<8 bitmask to dword, "
        "byte[0x12]|=0x2, byte[0x8]:=0. "
        "Double loop player=[0..1] x slot=[0..4]: call check_equip_slot_can_activate_with_context(p,s,0); "
        "hit -> return 1 immediately. "
        "All fail: if r10==0 and count_available_monster_slots(player)==0 -> return 0; else return 1. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=activatable slot exists, 0=none). "
        "Side-effects: [0x0201e4d0+0x0] byte:=player_side; [0x0201e4d0] dword bits[23:8]:=player<<8; "
        "[0x0201e4d0+0x12] byte|=0x02; [0x0201e4d0+0x8] byte:=0. "
        "Constants: state_base=0x0201e4d0, player_stride=0x868, ff8000ff_mask=0xff8000ff."),
    ("FUN_080312ec", "find_slot_idx_by_card_id_in_player_zones",
        "Linear scan gDuelFieldSlots[side*0x868+slot*0x14] for card_id match; return slot index or -1. "
        "Entry: r0=player_side (bit0), r1=card_id. "
        "Extracts zone_type (lsls #2/lsrs #0x18) and side_bit (lsls #0x12/lsrs #0x1f) per slot; "
        "match bits[12:0]==r1 -> return slot_idx. "
        "Not found -> return -1 (rsbs). "
        "indeg=21; used by duel_field hub to locate card slot index by card_id. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns s32 slot_index [0..count-1] or -1. Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14."),
    ("FUN_080a3b50", "get_equip_activation_mode_by_card_id",
        "Pure leaf: map card_id to equip activation mode_code. "
        "card_id==0x17c6 -> return 2; card_id==0x19a5 -> return 3; else -> return 1. "
        "Result written by caller scan_equip_activation_with_mode to [0x0201e4d0+8]. "
        "r0=u16 card_id [0..0x1fff]. Returns u8 mode_code [1..3]. Leaf, pure read-only. "
        "Constants: card_id_mode2=0x17c6, card_id_mode3=0x19a5."),
    ("FUN_080a3b74", "scan_equip_activation_with_mode",
        "scan_equip_activation_for_player precise variant with extra card_id mode initialization. "
        "Entry: call get_equip_activation_mode_by_card_id(r1) -> mode_code; "
        "write to [0x0201e4d0]: byte0:=player_side, dword bits[23:8]:=player<<8, "
        "byte[0x12]|=0x2, byte[0x8]:=mode_code. "
        "Double loop player=[0..1] x slot=[0..4]: call check_equip_slot_pair_can_activate_full(p,s,s_off); "
        "hit and player==r7 and slot<=4: call check_slot_placement_blocked_by_field_effect; "
        "pass -> r9:=1. Any slot: r6-- (available count). "
        "Final: r6<=0 and r10==0 and count_available_monster_slots==0 -> return 0; else return 1. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Returns u32 bool (1=activatable, 0=not). "
        "Side-effects: [0x0201e4d0+0x0/0x12/0x8] written as described. "
        "Constants: state_base=0x0201e4d0, mask=0xff8000ff."),
    ("FUN_080a3d74", "check_banisher_pair_activation_allowed",
        "Check if banisher card pair can be activated for player. "
        "Guard 1: count_field_copies_of_card(0x1332)>0 -> return 0 (Banisher already on field). "
        "Guard 2: count_valid_monster_pair_slots(player, 0x15a3)==0 -> return 0 (Ectoplasmer absent). "
        "Then: call scan_activatable_equip_slots_alt; return its result. "
        "r0=u32 player_side [0..1]. Returns u32 bool (1=allowed, 0=blocked). "
        "confidence: med (indirect scan via scan_activatable_equip_slots_alt). "
        "Constants: banisher_card_id=0x1332, pair_card_id=0x15a3."),
    ("FUN_080a4af4", "eval_equip_target_slot_flags",
        "Large equip target slot flag evaluator; reads gDuelFieldSlots[slot_idx] card_id and "
        "checks multiple special card IDs to determine activation flags. "
        "Paths: LAB_080a50b0 -> scan_equip_activation_for_player(player); "
        "LAB_080a50ba -> scan_equip_activation_with_mode(player, card_id). "
        "Various card_id checks (0x112e/0x128c/0x1758/0x1895/0x19a6) dispatch specialized sub-checks; "
        "each success writes [gDuelFieldSlots+0x1d78] phase code (0x10/0x11/0x17). "
        "Returns r7=accumulated activation flags. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, duel_phase_code_offset=0x1d78, "
        "set_code_sphinx=0x112e, set_code_sphinx_teleia=0x128c, set_code_ra=0x1758."),
    ("FUN_08095fe0", "eval_spell_activation_flags_by_zone",
        "Large equip/spell card activation condition evaluator; dispatches by equip_type (field6). "
        "Entry: reads gDuelFieldSlots[player][slot] card_id; checks active_player (duel_state+4) bit0 XOR player; "
        "mismatch -> return 0. "
        "check_card_targeted_by_spell_zone_effect: hit -> [gDuelFieldSlots+0x1c58]:=0x10. "
        "check_lp_exceeds_spell_copy_threshold: hit -> [gDuelFieldSlots+0x1c58]:=0x17. "
        "Reads [state+0x1bd4] zone_phase_code; code==3 -> LAB_080961a8; "
        "code==2/4 -> get_card_extended_stat_field6 -> equip_type dispatch: "
        "0x16 -> check_field_spell_placement_allowed -> invoke_equip_zone_activation_check -> "
        "check_zone_has_no_field_spell_node -> check_field_spell_b_placeable; "
        "0x17 -> check_field_spell_placement_allowed -> invoke_equip_zone_activation_check; "
        "else -> check_card_has_equip_placement_type -> eval_equip_target_slot_flags. "
        "Tail: check_card_is_equip_set_c -> invoke_equip_zone_activation_check; "
        "check_card_field5_is_nonzero + check_value_in_slot_chain(0x1407) Non-Aggression guard. "
        "indeg=1. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..10]; r2=u32 result_ptr. "
        "Returns u32 flags (0=cannot activate; nonzero=condition met). "
        "Side-effects: [gDuelFieldSlots+0x1c58]:=0x10/0x17; [gDuelFieldSlots+0x1d78]:=0x0c/0x0d/0x0f. "
        "Constants: gDuelFieldSlots=0x0201c510, duel_state=0x0201e2a0, equip_type_A=0x16, equip_type_B=0x17."),
    ("FUN_0804ae2c", "check_card_stat_field8_is_8",
        "Bool wrapper: get_card_extended_stat_field8(card_id)==8 -> return 1; else -> return 0. "
        "Sibling cluster: check_card_stat_field8_is_6 (0x0804ae04), FUN_0804ae18 (==7). "
        "indeg=3. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=field8==8, 0=not). Leaf."),
    ("FUN_0809058c", "check_card_has_activatable_effect_node",
        "Stack-allocates 0x18-byte context, writes card_id + 0x30 flags, "
        "calls find_card_effect_node_entry; returns 1 if node found, 0 if not. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool. "
        "Constants: EFFECT_QUERY_FLAG_ACTIVE_SEARCHABLE=0x30, context_size=0x18."),
    ("FUN_0804c05c", "check_card_id_is_equip_blocker",
        "Pure leaf: whitelist {0x149c, 0x1232, 0x1517} -> return 1; else -> return 0. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=equip blocker, 0=not). Leaf, no side-effects. "
        "Constants: equip_blocker_a=0x149c (Beast Soul Swap), equip_blocker_b=0x1232, equip_blocker_c=0x1517."),
    ("FUN_0805a3e0", "eval_equip_activation_for_slot",
        "Context-struct based equip slot activation evaluator. "
        "Reads card_id/player_side/slot_type from stack context_struct r0; "
        "calls check_card_has_activatable_effect_node -> check_card_id_is_equip_blocker -> "
        "check_card_stat_field8_is_8; accumulates flags to [context+2]. "
        "Writes [gDuelFieldSlots+0x1d78]:=0x04 on inner path. "
        "r0=ptr context_struct ([+0]=card_id, [+2]={player_side,slot_type}, [+4]=zone_flags). "
        "Returns u32 bool (1=activatable, 0=blocked). "
        "Side-effects: [gDuelFieldSlots+0x1d78]:=0x04; [context+2] flags accumulated. "
        "Constants: gDuelFieldSlots=0x0201c510, duel_phase_code_offset=0x1d78."),
    ("FUN_0805a280", "setup_equip_context_for_slot_activation",
        "Assembles 0x18-byte context_struct on stack from gDuelFieldSlots, then delegates activation check. "
        "Entry: memset 0x18 bytes; reads gDuelFieldSlots[player][slot] card_id low 13 bits -> [sp+0] hword; "
        "card_id==0 -> return 0. "
        "Writes r1 bit0 (player_id) to [sp+2] bit0; slot_idx bits<<1 to [sp+2] bits[6:1]; "
        "zone_type<<1|side_bit to [sp+4] bits[13:6]. "
        "Checks gDuelFieldSlots[player][slot][+8] active_hword: ==0 -> check_card_zone_activation_blocked; "
        "!=0 -> eval_equip_activation_for_slot. "
        "r0=u32 player_side_primary [0..1]; r1=u32 player_id [0..1]; r2=u32 slot_idx [0..4]. "
        "Returns u32 bool (1=activatable, 0=not). "
        "Side-effects: [sp..sp+0x18] stack context_struct (destroyed on return). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14."),
    ("FUN_0805a354", "setup_equip_context_for_zone_activation",
        "Simplified setup_equip_context_for_slot_activation variant with fixed slot_type=0x16. "
        "Allocates 0x18-byte stack context, reads gDuelFieldSlots[player][slot] card_id; "
        "writes player_id bit0, fixed zone_code=0x16 to [sp+2]; passes result_ptr r2 to "
        "check_card_zone_activation_blocked. "
        "Called by eval_zone_activation_flags_for_player (0x08096864) on zone 0xb path. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..4]; r2=u32 result_ptr. "
        "Returns u32 bool (1=activatable, 0=not). "
        "Constants: gDuelFieldSlots=0x0201c510, zone_code_fixed=0x16, player_stride=0x868."),
    ("FUN_0803b738", "read_player_field_slot_word_by_zone",
        "Jump-table dispatch on zone_type [0xb..0xf]: returns gDuelFieldSlots[side*0x868+fixed_offset] word. "
        "zone 0xb->offset 0x18, 0xc->0x10, 0xd->0x14, 0xe->0x1c, 0xf->0x0c. "
        "Default path: zone_type*20 offset, extracts card_id low 13 bits, returns 1 if nonzero else 0. "
        "r0=u32 player_side [0..1]; r1=u32 zone_type [0xb..0xf]; r2=u32 slot_offset [0..4]. "
        "Returns u32 slot_word or 1/0. Read-only. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "zone_0xb_off=0x18, zone_0xc_off=0x10, zone_0xd_off=0x14, zone_0xe_off=0x1c, zone_0xf_off=0x0c."),
    ("FUN_080968f4", "check_zone_slot_card_activatable",
        "Calls read_player_field_slot_word_by_zone; zone 0xd/0xc checks [gLP+0x1d00]; "
        "zones 0xe/0xf -> return 2. Returns mode_code: 0=blocked, 2=activatable. "
        "r0=u32 player_side [0..1]; r1=u32 zone_type [0xb..0xf]; r2=u32 slot_offset [0..4]. "
        "Returns u32 mode_code (0=blocked, 2=activatable). Read-only. "
        "Constants: DUEL_ACTIVATION_FLAG_OFFSET=0x1d00, MODE_ACTIVATABLE=2, "
        "gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_08096864", "eval_zone_activation_flags_for_player",
        "Evaluates zone_type r2 activation flags for player r0/r1. "
        "zone 0xb: LP threshold guard + setup_equip_context_for_zone_activation; "
        "zones [0xc..0xf]: check_zone_slot_card_activatable; "
        "else: setup_equip_context_for_slot_activation. "
        "Returns flags (bit3=0x8=zone activatable). "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..10]; r2=u32 zone_type [0xb..0xf or other]. "
        "Returns u32 flags (0=no activation; 0x8=zone activatable). "
        "Constants: ACTIVE_ZONE_PLAYER_FIELD_OFFSET=0x1d64, FLAG_ZONE_ACTIVATABLE=0x8, "
        "gDuelFieldSlots=0x0201c510."),
    ("FUN_0804ae04", "check_card_stat_field8_is_6",
        "Bool wrapper: get_card_extended_stat_field8(card_id)==6 -> return 1; else -> return 0. "
        "Sibling cluster: check_card_stat_field8_is_8 (0x0804ae2c), FUN_0804ae18 (==7). "
        "indeg=16. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 bool (1=field8==6, 0=not). Leaf."),
    ("FUN_08032d1c", "count_equip_set_activatable_slots_for_player",
        "Count equip zone slots [5..0xa] for player satisfying set_code match. "
        "Non-APCS: r8=count_accumulator, r9=set_code_guard, r10=target_set_code (all caller-set). "
        "Loops slot_idx 5..10 (stride 0x14): call get_equip_card_set_code_for_slot(player, slot); "
        "result>0 and matches guard conditions -> r8++. "
        "Returns r8 (accumulated count) via r0. "
        "r0=u32 player_side [0..1]; r8 (non-APCS)=u32 initial_count; "
        "r9 (non-APCS)=u32 set_code_guard; r10 (non-APCS)=u32 target_set_code. "
        "Returns u32 count via r0. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot5_card_off=0x64, "
        "slot5_state_off=0x74, slot_entry_size=0x14."),

    # batch #22: duel slot activation/eligibility eval cluster (20 functions)
    ("FUN_08034358", "check_slot_field_action_eligibility",
        "Checks if gDuelFieldSlots[player_side][slot_idx] meets field action eligibility. "
        "Verifies slot is occupied (card_id bit9 != 0), else return 0. "
        "Checks slot[+0x10] bit21: bit21==1 -> if gDuelActivation[+4]==player_side write "
        "[gP1LifePoints+side*0x868+0x1d48]=0x3 return 0; "
        "bit21==0 -> run checks: check_slot_card_effect_eligibility / "
        "check_slot_card_fieldspell_eligibility / check_value_in_slot_chain(x3) / "
        "query_zone_chain_count_with_eligibility / count_equip_chain_default_flags / "
        "find_paired_zone_entry_for_card / count_available_effect_zones. "
        "All pass return 1, any fail return 0. indeg=6. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, "
        "activation_base=0x0201e2a0."),
    ("FUN_0803ba98", "check_field_spell_last_warrior_placeable",
        "Checks if player field allows placing Last Warrior from Another Planet (0x12b1) related field spell. "
        "Reads gP1LifePoints[player_side*0x868+0x11c] bit20; bit20==1 -> return 0 (already restricted). "
        "Else: count_available_effect_zones(player, 0x13ff=Jam Breeding Machine, -1) nonzero -> return 0; "
        "count_field_copies_of_card(0x12b1=Last Warrior) nonzero -> return 0; "
        "find_effect_node_in_zone(player, 0xb, 0x1679=Judgement of Pharaoh, 1) nonzero -> return 0. "
        "All pass return 1. indeg=3. "
        "r0=u32 player_side [0..1]. Returns u32 0/1. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, field_state_offset=0x11c, "
        "bit20=0x100000, 0x12b1=Last Warrior, 0x13ff=Jam Breeding Machine, "
        "0x1679=Judgement of Pharaoh."),
    ("FUN_080345e0", "check_field_spell_slot_placeable",
        "Checks if gDuelFieldSlots[player_side][slot_idx] allows placing a field spell. "
        "Reads slot+0x8 (equip chain head); nonzero -> return 0 (slot occupied by equip chain). "
        "Then three gate checks: (1) check_slot_field_action_eligibility(player, slot); "
        "(2) check_field_spell_last_warrior_placeable(player); "
        "(3) check_field_spell_neo_daedalus_group_placeable(player). "
        "Any 0 -> return 0. "
        "On pass checks card_id range (Archfiend range 0x164a..0x164f etc.) for extra pair constraints. "
        "Final pass return 1. indeg=3. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot+0x8=equip_chain_head."),
    ("FUN_080346c4", "check_slot_monster_activation_eligible",
        "Multi-condition monster activation eligibility check for gDuelFieldSlots[player_side][slot_idx]. "
        "Reads slot[flags] bit22 (occupation flag); bit22==0 -> return 0. "
        "Checks bit23; bit23==1 -> proceed to activation path. "
        "bit23==0: reads slot[+0x30] flags extracting bit5/bit1 with slot+0x8 equip chain head "
        "for multi-condition filtering. "
        "On pass branches by card_id: 0x1723=Twinheaded Beast, 0x14d5=Tyrant Dragon etc. "
        "Final pass return 1, fail return 0. indeg=2. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gP1LifePoints ptr, player_stride=0x868, slot_offset=slot_idx*0x14+0x40, "
        "bit22=occupation, bit23=summoned_flag."),
    ("FUN_08035280", "exit_slot_activation_with_state_write",
        "Checks if gDuelActivation[+4] equals r5 (caller-saved player_side); "
        "if match writes 0x13 (activation_fail_code) to gP1LifePoints+0x1d78. "
        "Returns 0 regardless of write. "
        "Dedicated activation-fail exit for check_slot_full_activation_eligibility (FUN_08034a58): "
        "called via tail-branch b FUN_08035280 from multiple sites inside FUN_08034a58. "
        "indeg=1. No APCS params (uses caller r5). Returns u32 0. "
        "Constants: gDuelActivation=0x0201e2a0, activation_player_offset=+4, "
        "0x1d78=activation_state_offset, activation_fail_code=0x13."),
    ("FUN_08033cf8", "check_player_has_equip_type_in_slots",
        "Scans player (r0 bit0) 5 monster zone slots (slot_idx 0..4), "
        "checks if any slot has equip-type card (field8==6). "
        "Per slot: (1) card_id low 13 bits nonzero; "
        "(2) ldrh slot+0x8 (equip_chain_head) nonzero; "
        "(3) check_card_stat_field8_is_6(card_id) true. "
        "All three satisfied -> return 1 immediately. "
        "Leaf function (check_card_stat_field8_is_6 is named callee). indeg=3. "
        "r0=u32 player_side [0..1]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, "
        "slot_count=5 [0..4], slot+0x8=equip_chain_head."),
    ("FUN_08035988", "check_slot_field_spell_chain_eligible",
        "Checks field-chain equip eligibility for slot (player_side=r0, slot_idx=r1). "
        "Calls check_slot_card_fieldspell_eligibility for eligibility flags. "
        "Computes slot address from player_side bit0 and slot_idx; "
        "reads slot[+0x10] flags extracting bit5/bit1 with slot+0x8 (equip_chain_head) for triple filter. "
        "On pass branches by slot card_id: "
        "0x147d=Zombyra, 0x127d..0x1283=Toon range, 0x154a=Toon Dark Magician Girl etc.; "
        "each branch calls check_card_matches_active_effect_slot / find_equip_chain_node_by_slot_pair. "
        "indeg=4. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot+0x10=flags_word, bit5/bit1=restriction_flags."),
    ("FUN_08035b24", "check_field_spell_trap_chain_eligible",
        "Checks trap-chain eligibility for player (r0 bit0) field spell zone slots. "
        "Scans 5 slots (r6=0..4) from gDuelFieldSlots+player*0x868. "
        "Per slot: card_id low 13 bits nonzero; "
        "slot[+0x10] bit5/bit1 dual filter pass; "
        "card_id==0x13cd=The Legendary Fisherman -> "
        "calls check_card_matches_active_effect_slot(0x10f4=Umi). "
        "No match in 5 slots -> return 0. indeg=2. "
        "r0=u32 player_side [0..1]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "0x13cd=The Legendary Fisherman, 0x10f4=Umi."),
    ("FUN_08032dac", "count_equip_zone_slots_matching_card",
        "Counts slots in player (r0 bit0) equip zone (slot 5..10, offset +0x64) matching all conditions. "
        "r1=target_card_id (saved to r8), r2=ref_value (saved to r12). "
        "Per slot (stride 0x14, 6 slots): "
        "(1) card_id low 13 bits == r8; "
        "(2) slot[+0x10] bit5==0 and bit1==0; "
        "(3) ldrh [slot+0x8] (equip_chain_head) != 0; "
        "(4) slot[+0xc] >= r12. "
        "All satisfied -> r6++. Returns hit count. indeg=1. "
        "r0=u32 player_side [0..1]; r1=u32 target_card_id; r2=u32 ref_value. Returns u32 count. "
        "Non-APCS: r8=target_card_id (caller-saved from r1), r12=ref_value (caller-saved from r2). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "equip_zone_base=+0x64, slot_count=6 [0..5]."),
    ("FUN_08034a58", "check_slot_full_activation_eligibility",
        "Comprehensive activation eligibility check for gDuelFieldSlots[player_side][slot_idx]. "
        "Core composite function for field activation decisions (200+ instructions). "
        "Entry: push callee-save regs + sub sp,#0x40 (0x40-byte frame); "
        "reads slot card_id and slot[+0x10] flags; "
        "slot+0x10 bit24 nonzero -> b exit_slot_activation_with_state_write (fail exit). "
        "Calls in sequence: find_paired_zone_entry_for_card / eval_slot_score_entry_full / "
        "check_slot_card_effect_eligibility / check_slot_card_fieldspell_eligibility / "
        "query_zone_chain_count_with_eligibility (multiple) / "
        "count_equip_chain_default_flags (x3) / "
        "count_field_copies_of_card / count_available_effect_zones. "
        "Exits via exit_slot_activation_with_state_write writing activation state then returns 0. "
        "indeg=2. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "gDuelActivation=0x0201e2a0, 0x1d48=activation_field, 0x1d78=second_activation_field."),
    ("FUN_080349b0", "check_slot_card_activatable",
        "Checks if card in gDuelFieldSlots[player_side][slot_idx] is activatable. "
        "Reads slot card_id and slot+0x8 (equip_chain_head); card_id==0 -> return 0 (empty slot). "
        "slot+0x6 (chain_field) nonzero: branch by card_id: "
        "0x12b4=Total Defense Shogun -> reads slot[+0x10] bit5 as activation flag; "
        "0x1956=EHero Rampart Blaster -> bit5 inverted and calls count_occupied_monster_zones; "
        "other -> return 0. "
        "slot+0x6==0: calls check_slot_monster_activation_eligible; "
        "if returns 0 calls check_slot_full_activation_eligibility. indeg=8. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "0x12b4=Total Defense Shogun, 0x1956=Elemental Hero Rampart Blaster."),
    ("FUN_08035ba4", "check_player_field_spell_chain_eligible",
        "Checks if player (r0) has activation eligibility in field spell chain. "
        "Calls check_slot_field_spell_chain_eligible(r0); if returns 0 -> return 0. "
        "If nonzero, calls check_field_spell_trap_chain_eligible(1-r4=opponent); "
        "if opponent returns 0 -> return 1 (player eligible, no opponent conflict). "
        "If opponent also nonzero -> return 0. "
        "Result: player has field chain eligibility AND opponent has no conflict -> 1; else 0. "
        "indeg=6. "
        "r0=u32 player_side [0..1]. Returns u32 0/1."),
    ("FUN_08030b0c", "check_slot_card_is_monster_type",
        "Reads card_id from gDuelFieldSlots[player_side][slot_idx], "
        "calls map_field8_to_card_type_category for type code "
        "(0=Normal Monster, 7=Ritual/Effect subset, 8=Equip). "
        "type==0 or ==7 -> return 1; "
        "type==8 -> calls check_slot_card_is_equip_type(player, slot) and returns inverted result; "
        "other types (2..6 etc.) -> return 0. "
        "Determines if slot card is activatable Monster or specific effect card rather than pure equip spell. "
        "indeg=9. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 0/1. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "card_type_normal=0, card_type_ritual_sub=7, card_type_equip=8."),
    ("FUN_0802f61c", "count_equip_slots_with_active_chain",
        "Counts slots in player (r0 bit0) where all three hold: "
        "(1) slot occupied (card_id bit9 != 0); "
        "(2) slot+0x8 (equip_chain_head) != 0; "
        "(3) count_equip_chain_default_flags(player, slot_idx, r1=chain_filter) nonzero. "
        "r1 saved to r9 at entry via .hword 0x4689 (mov r9,r1); "
        "restored to r2 at each callee call via .hword 0x464a (mov r2,r9). "
        "indeg=6. "
        "r0=u32 player_side [0..1]; r1=u32 chain_filter. Returns u32 count. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry=0x14, slot_count=5 [0..4]."),
    ("FUN_0804aea0", "check_card_is_archfiend_type",
        "Checks if card_id (r0) belongs to the Archfiend card group. "
        "Series of card_id range/single-value comparisons: "
        "0x107f=B.Skull Dragon, 0x10ab=Wicked Mirror, 0x127f=Toon Summoned Skull, "
        "0x12b5=Beast of Talwar, 0x13e3=Archfiend of Gilfer, 0x14b7=Lesser Fiend, "
        "0x14da=Fiend Skull Dragon, 0x1661-0x1666 range, 0x1692=Skull Archfiend of Lightning etc. "
        "Any match return 1, else return 0. Leaf function (bx lr). indeg=7. "
        "r0=u32 card_id. Returns u32 0/1."),
    ("FUN_0804b048", "check_card_is_amazoness_type",
        "Checks if card_id (r0) belongs to the Amazoness card group. "
        "Whitelist comparisons: "
        "0x14ab=Amazoness Chain Master, 0x14a6=Amazoness Archers, "
        "0x14af=Amazoness Fighter, 0x14b0=Amazoness Paladin, 0x160f=Amazoness Tiger etc. "
        "Any match return 1, else return 0. Pure leaf function (bx lr). indeg=1. "
        "r0=u32 card_id. Returns u32 0/1."),
    ("FUN_0803a958", "get_slot_field5_score",
        "Extracts field5 score (sp+0x14 offset) from eval_slot_score_entry_full result array. "
        "Builds 0x24-byte frame (sub sp,#0x24); "
        ".hword 0x466a (mov r2,sp) passes stack top as result buffer pointer; "
        "r0=player_side and r1=slot_idx forwarded directly to eval_slot_score_entry_full; "
        "result array written to sp+0x4..sp+0x24; returns sp+0x14 (index=4, field5). "
        "5-instruction body. Numbered sibling cluster with adjacent functions extracting "
        "different fields from same eval_slot_score_entry_full result. "
        "indeg=41. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]. Returns u32 field5_score. "
        "Constants: sp+0x14=score_field5_offset (entry index 4), "
        "eval_slot_score_entry_full result array base at sp+0x4."),
    ("FUN_080366f0", "check_slot_fieldspell_eligible_by_side",
        "Small wrapper: takes (r0=player_side, r1=slot_idx, r2=target_player_side), "
        "calls check_slot_card_fieldspell_eligibility(r0, r1) for eligibility flags, "
        "then ANDs result with (r2+1) and checks > 0. "
        "Returns 1 if slot has fieldspell eligibility AND (eligibility_flags & (r2+1)) != 0. "
        "Compact selector used at multiple duel sites to check if specific side has field spell activation right. "
        "indeg=10. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]; r2=u32 target_player_side [0..1]. "
        "Returns u32 0/1."),
    ("FUN_0802f3e0", "query_slot_effect_eligibility_with_equip_fallback",
        "Selects path based on card_id (r2) field6 value: "
        "field6==0x17 (Union type) -> computes player_side XOR r3 nonzero as r2 flag, "
        "calls check_slot_fieldspell_eligible_by_side(r0, r1, r2); "
        "other field6 -> computes r2 flag similarly, "
        "calls query_slot_effect_eligibility_nonzero(r0, r1, r2). "
        "If above result==0 -> calls count_slot_equip_list_matches(r0, r1, card_id, r3) "
        "and returns equip count. indeg=3. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]; "
        "r2=u32 card_id; r3=u32 filter_value. Returns u32 count_or_flag. "
        "Constants: field6_union_type=0x17."),
    ("FUN_080332f0", "count_slots_matching_card_pair",
        "Counts player (r0 bit0) 5 slots (slot_idx 0..4) satisfying all: "
        "(1) slot occupied (card_id bit9 != 0); "
        "(2) slot+0x8 (equip_chain_head) == r1 (target_chain_head); "
        "(3) slot+0x6 (chain_field) == r2 (target_chain_field). "
        "All satisfied -> counter++. Returns hit count. "
        "Pure leaf scan function. indeg=3. "
        "r0=u32 player_side [0..1]; r1=u32 target_chain_head; r2=u32 target_chain_field. "
        "Returns u32 count. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, "
        "slot_count=5 [0..4], slot+0x8=equip_chain_head, slot+0x6=chain_field."),

    # batch=23
    ("FUN_080352b0", "eval_slot_activation_eligibility_full",
        "当 duel 场地需要判断某一卡槽 (player_side, slot_idx) 上的卡是否可以激活效果时, "
        "由上层 hub (FUN_0803495c / eval_zone_activation_flags_for_player 簇) 调用. "
        "函数依次执行多层筛选: (1) 同时调用 check_slot_card_effect_eligibility 和 "
        "check_slot_card_fieldspell_eligibility 获取效果/魔法场地资格掩码; "
        "(2) 以 FIELD_SPELL_ZONE=0xb 检查当前槽的 field spell 链; "
        "(3) 按卡 ID 范围 (0x15ff/0x1505/0x1644/0x1958 等特定 id) 分支查询装备/效果链, "
        "调用 query_zone_chain_count_with_eligibility / count_equip_chain_default_flags / "
        "query_slot_effect_eligibility_with_equip_fallback; "
        "(4) 针对 Amazoness/Archfiend 类卡调用 count_available_effect_zones; "
        "(5) 按 equip 列表匹配 count_slot_equip_list_matches 及 get_slot_field5_score 做阈值判断. "
        "副作用: 无 VRAM/IWRAM 写入; 纯读取 gDuelFieldSlots. indeg=11, class D. "
        "返回 0=不可激活, 1=可激活. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "FIELD_SPELL_ZONE=0xb, slot_entry=0x14."),

    ("FUN_08033d44", "check_any_slot_fieldspell_zone_eligible",
        "当需要判断某一玩家侧 (r0 bit0) 是否存在至少一个合法的场地魔法区位时调用. "
        "函数遍历 gDuelFieldSlots 5 个卡槽 (slot_idx 0..4), 对每槽: "
        "(1) 检查 [slot+0] bit9 是否置位 (槽有卡); "
        "(2) 检查 [slot+0x8] equip_chain_head 非零; "
        "(3) 调用 compute_slot_zone_eligibility_mask 取掩码并 AND 0x7, 非零即返回 0 (找到合法区位). "
        "所有槽均不满足则返回 1. 纯读操作, 无副作用. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry=0x14 (20 bytes), slot_count=[0..4]."),

    ("FUN_08033294", "count_slots_with_chain_field_match",
        "当上层需要统计某玩家侧满足双条件的卡槽数量时调用: "
        "条件 A (r1 非零时) 要求 [slot+0x8] equip_chain_head 非零; "
        "条件 B (r2 非零时) 要求 [slot+0x6] chain_field 非零. "
        "函数遍历 gDuelFieldSlots 中该玩家的 5 个卡槽 (slot_idx 0..4), "
        "对每个有卡 ([slot+0] bit9 置位) 的槽: 若条件 A/B 均满足则计数 r5++. "
        "返回命中计数. 纯叶子函数, 无副作用. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, "
        "slot+0x8=equip_chain_head, slot+0x6=chain_field."),

    ("FUN_08035bc8", "eval_slot_fieldspell_activation_full",
        "当判断卡槽上的 field spell 是否可以激活时由 FUN_0803495c 调用. "
        "函数首先调用 check_slot_card_fieldspell_eligibility 和 "
        "check_slot_field_spell_chain_eligible 获取 field spell 基础资格; "
        "若后者为 0 则直接返回 0. "
        "再调用两次 query_zone_chain_count_with_eligibility "
        "(使用卡 ID 0x1561 和 0x1852) 检查区域链. "
        "若无链记录, 则检查 [slot+0] bit5 (chain_lock) 和 [slot+0x8] (equip_chain_head) 双重条件; "
        "然后按对侧对应槽的卡 ID 进行详细分支分别走不同子路径. "
        "返回 0=不可激活, 1/2=不同激活级别. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "0x1561/0x1852=zone chain filter codes, FIELD_SPELL_ZONE=0xb."),

    ("FUN_0803495c", "eval_slot_activation_guard_full",
        "当上层 zone eval 循环 (indeg=9) 需要综合判断某玩家侧 (r0) 某 slot (r1) "
        "是否可激活卡效果时调用. "
        "函数首先调用 check_slot_card_activatable 做基础可激活检查; 失败则返回 0. "
        "通过后依次尝试 check_player_field_spell_chain_eligible 和 "
        "eval_slot_fieldspell_activation_full 做 field spell 专项检查; 任意通过则返回 1. "
        "若两者均失败, 则遍历 5 个卡槽, 对每槽调用 eval_slot_activation_eligibility_full "
        "(FUN_080352b0) 进行全量效果资格判断. 全部失败返回 0. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_count=[0..4]."),

    ("FUN_08096264", "setup_equip_slot_activation_entry",
        "当 zone eval 主循环确定某卡槽需要建立装备激活记录时调用 (indeg=1). "
        "函数接受 player_side/slot_idx/zone_slot, 首先检查 slot_idx<=4; "
        "读取 gDuelState[+0x4] 判断当前激活玩家侧; "
        "若是对侧则调用 check_card_field5_is_nonzero 确认卡有效, "
        "确认 equip_chain_head 非零且 check_card_id_is_equip_blocker 通过. "
        "在 EWRAM 区域 (r8 非 APCS 传递的节点地址 + 0x18 字节 memset 清零) 构建激活条目: "
        "写入 card_id/player_side bit/zone_code/属性位; "
        "最终调用 eval_equip_activation_for_slot 返回激活结果 (0x8=可激活). "
        "Constants: gDuelFieldSlots=0x0201c510, gDuelState=0x0201e2a0, "
        "ACTIVATION_FLAG=0x8, DUEL_ZONE_ACTIVATION_OFFSET=0x1d48, buf_size=0x18."),

    ("FUN_08096954", "dispatch_zone_effect_by_slot",
        "当 zone eval 路径需要对卡槽 (r0=player_side, r1=slot_idx) 派发效果处理时调用 (indeg=2). "
        "函数极简: 将 r1 (slot_idx) 移到 r2 位置, 再将常量 0xfffe 作为 r1 传入 "
        "dispatch_effect_handler_by_card_id; "
        "若返回非零则返回 0x8 (可激活标志), 否则返回 0. "
        "0xfffe 为通配效果 ID, 对应通用激活判断路径. "
        "Constants: EFFECT_ID_GENERIC=0xfffe, ACTIVATION_FLAG=0x8."),

    ("FUN_0809678c", "eval_zone_activation_flags_by_type",
        "当 zone eval 主循环需要对单个 zone_type (r1) 的卡槽计算激活标志位时调用 (indeg=1). "
        "根据 zone_type 三路分支: "
        "(A) zone==0xb (FIELD_SPELL_ZONE): 读 gP1LifePoints[player*0x868+0xc] 做 LP 阈值比较, "
        "调用 setup_equip_context_for_zone_activation, 成功则 r6|=0x8; "
        "(B) zone_type in [0xc..0xf]: 调用 check_zone_slot_card_activatable 取 u16 标志, "
        "再调 dispatch_zone_effect_by_slot OR 进 r6; "
        "若玩家为对侧且 slot==0xd 则 r6|=0x1000; "
        "(C) 其他: 调用 setup_equip_context_for_slot_activation. "
        "返回 r6 (激活标志复合值). "
        "Constants: FIELD_SPELL_ZONE=0xb, ACTIVE_ZONE_PLAYER_FIELD_OFFSET=0x1d64, "
        "FLAG_ZONE_ACTIVATABLE=0x8, FLAG_DUAL_ZONE=0x1000."),

    ("FUN_0805b0cc", "build_zone_activation_entry_blocked",
        "当需要构建一个装备激活条目并检查其是否被阻断时调用 (indeg=3). "
        "函数在栈上分配 0x18 字节缓冲区, memset 清零; "
        "将 r2(card_id) 写入 [buf+0]; "
        "设置 [buf+2] bit0=player_side&1 和 bits[5:0]=zone_code; "
        "设置 [buf+3] |= 0x40; "
        "读取 gDuelFieldSlots[player*0x868+slot*20] 的 node word 提取属性字段写入 [buf+4]; "
        "最终调用 check_card_zone_activation_blocked(buf, 0). 返回其结果. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, buf_size=0x18, "
        "slot_entry=0x14, OAM_attr_mask_1=0xffff803f, OAM_attr_mask_2=0xfffff03f."),

    ("FUN_0805b034", "build_zone_activation_entry_equip",
        "当需要构建一个装备类型激活条目并对其做 eval_equip_activation_for_slot 判定时调用 (indeg=1). "
        "函数结构与 build_zone_activation_entry_blocked (FUN_0805b0cc) 几乎完全对称, "
        "区别在于最终调用的是 eval_equip_activation_for_slot 而非 check_card_zone_activation_blocked, "
        "用于判断装备魔法槽的激活合法性. "
        "栈分配 0x18 字节, memset 清零; 写入 card_id/player_bit/zone_code/attr; "
        "调用 eval_equip_activation_for_slot(buf, 0); 返回其结果. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, buf_size=0x18, "
        "OAM_attr_mask_1=0xffff803f, OAM_attr_mask_2=0xfffff03f."),

    ("FUN_0809650c", "setup_equip_slot_activation_entry_alt",
        "FUN_08096264 (setup_equip_slot_activation_entry) 的结构对称变体, "
        "被 FUN_08096b3c dispatch hub 的另一 case 分支调用 (indeg=1). "
        "同样接受 player_side/slot_idx/zone_slot 三个参数, "
        "首先调用 find_paired_zone_entry_for_card 判断是否已有配对条目; "
        "若已配对且玩家侧与 gDuelState[+0x4] 匹配, 则写 [gP1LifePoints+0x1d48]:=0x10. "
        "无配对时继续判断后 memset 清零缓冲区并构建激活条目, "
        "调用 eval_equip_activation_for_slot. "
        "然后进入扩展路径: 检查 get_card_extended_stat_field6 == 0x16/0x17, "
        "调用 build_zone_activation_entry_blocked / build_zone_activation_entry_equip 做额外 block 检查. "
        "Constants: gDuelState=0x0201e2a0, gDuelFieldSlots=0x0201c510, "
        "ACTIVATION_FLAG=0x8, DUEL_ZONE_OFFSET=0x1d48, buf_size=0x18."),

    ("FUN_08096b3c", "dispatch_zone_activation_by_state",
        "duel field zone 激活评估的主 dispatch hub (indeg=5, class D). "
        "入口读取 gP1LifePoints[+0x1d50] (zone state 标志), 若为 0 则返回 0. "
        "否则读 gP1LifePoints[+0x1d4c] (zone state 类型 1..10), 减 1 后查跳表 (10 个 case): "
        "case 1=单 monster zone; "
        "case 2/3=多 zone 类型按 slot_idx 分 4 组分别调 setup_equip_slot_activation_entry / "
        "setup_equip_slot_activation_entry_alt / eval_zone_activation_flags_by_type; "
        "case 4/5/7/9=场地/trap/magic zone 特殊路径; case 6/8/10=其他路径. "
        "Constants: gP1LifePoints 偏移: 0x1d4c=zone_type, 0x1d50=zone_state, "
        "FLAG_DUAL_ZONE=0x1000, FLAG_ACTIVATABLE=0x8."),

    ("FUN_080c89a8", "query_player_slot_activation_bitmask",
        "当 FUN_080c4220 (duel field display 更新) 需要知道某玩家所有卡槽的激活可能性时调用 (indeg=2). "
        "函数遍历 7 个槽 (r4=0..6), 对每槽从 gDuelZoneDisplay (0x0202317c) 读取 slot_id (halfword), "
        "然后调用 dispatch_zone_activation_by_state (FUN_08096b3c, r1=slot_id, r2=r4) 取激活标志; "
        "若标志 bit11 (0x800) 置位则将 r4 对应 bit 置入返回掩码 r5. "
        "最终返回 r5=7bit 掩码 (bit N = slot N 可激活). "
        "Constants: gDuelZoneDisplay=0x0202317c, FLAG_SLOT_ACTIVATABLE_BIT=0x800 (bit11), "
        "slot_count=[0..6]."),

    ("FUN_080c38cc", "render_field_slot_card_tile",
        "当 duel field 需要在 BG tile map 上渲染一个卡槽的卡牌小图标时调用 (indeg=5, class D). "
        "函数参数通过非 APCS 高寄存器传递 (r8=player_side 等), "
        "栈 sp[0x24]=card_mini_frame_flag, sp[0x28]=use_card_image_flag. "
        "首先调用 get_field_slot_tile_vram_addr 取目标 VRAM 地址. "
        "若 use_card_image_flag==0, 调用 update_field_slot_tile_display 直接清空槽. "
        "否则按 card_mini_frame_flag 决定数据源; "
        "读取 tile_data 后循环以 halfword 形式复制 0x120 字节 (144 个 halfword = 卡牌缩略图) 到 VRAM 目标地址. "
        "Constants: tile_copy_count=0x90=144 halfwords, ROM_VERSION_BYTE_ADDR=0x080000ae, "
        "EWRAM_FLAGS=0x02000000+0x6c2c."),

    ("FUN_080c4220", "refresh_player_field_slot_tiles",
        "当 duel field 场地需要整体刷新某玩家所有卡槽的 BG tile 显示时调用 (indeg=6, class D). "
        "函数接受 player_side (r0) 和一个 halfword (r1, 传入槽 header 值), "
        "首先读取 gP1LifePoints[player*0x868+0xc] 的 zone count (max 7). "
        "外层循环 r4=0..r8 (max slot count), 对每槽: "
        "检查 gDuelState[+0x4] (对侧 player) 或调 get_player_deck_flag_bit1 确认是否对侧; "
        "若是对侧则 r6=1 (有卡), 否则从 gDuelZoneSlotData (0x02023180) 读 zone halfword 判断是否有卡. "
        "然后调用 render_field_slot_card_tile (FUN_080c38cc) 渲染每槽. "
        "内层结束后继续对 slot [4..6] 调 update_field_slot_tile_display 清空魔法/陷阱槽. "
        "最后写入 gDuelZoneSlotHeader (0x02023130+0x4c+player*2) 一个 halfword, "
        "并调用 query_player_slot_activation_bitmask (FUN_080c89a8) 取激活掩码写入辅助区域. "
        "Constants: gDuelState=0x0201e2a0, gP1LifePoints LP_ZONE_COUNT_OFFSET=0xc, "
        "gDuelZoneSlotData=0x02023180, gDuelZoneSlotHeader=0x02023130, "
        "gDuelFieldSlots=0x0201c600, player_stride=0x868, ACTIVATABLE_MASK_SHIFT=5."),

    ("FUN_080c39fc", "render_field_zone_card_tile_by_type",
        "当需要根据 zone_type (slot_idx r1 = 0xc/0xd/0xe/0xf 的特殊 zone) "
        "渲染对应的卡牌小图标 tile 时调用 (indeg=4, tags: card_frame card_ids). "
        "函数获取 get_field_slot_tile_vram_addr 定位 VRAM 目标; 然后按 zone_type 分支: "
        "zone 0xc -> 若 card_id (r4) 非零从 gDuelFieldSlots[player][FUSION_ZONE?] 读卡属性 "
        "(含 JP flag 检查) 后确定 tile 源; "
        "zone 0xd -> 若有卡读 gDuelSpecialZone_0x0201c740 (magic slot 数组) 确定 mini frame tile; "
        "zone 0xe -> 与 0xd 类似, 读 gDuelSpecialZone2_0x0201c8f4; "
        "zone 0xf -> 先调 get_zone_card_attribute_by_type 取属性, 再读 gDuelSpecialZone3_0x0201caac; "
        "若无卡(r4==0)则调 update_field_slot_tile_display 清空. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "gDuelSpecialZone_0xc=0x0201c740, gDuelSpecialZone_0xe=0x0201c8f4, "
        "gDuelSpecialZone_0xf=0x0201caac, ROM_VERSION_BYTE=0x080000ae, "
        "EWRAM_FLAGS=0x02000000+0x6c2c, JP_FLAG_BYTE=0x4a."),

    ("FUN_080c4d04", "redraw_all_field_slot_tiles",
        "当 duel field 场地需要完整重绘所有 zone 和 slot 的卡牌 tile 时调用 (indeg=1, class D). "
        "函数外层循环 r7=0..1 (两个玩家), 内层循环 r6=0..4 (5 个主要 slot): "
        "对每 (player, slot) 组合, 读取 gDuelAnimState (0x0202334e) 和 gDuelAnimFlags (0x02023350) "
        "合成 zone_mask, 再通过 get_zone_card_attribute_by_type / get_zone_slot_field6_by_type / "
        "get_zone_slot_card_ref_by_type + ensure_card_id_cache_entry 获取每槽卡 ID; "
        "调用 render_field_slot_card_tile (FUN_080c38cc) 渲染主 slot. "
        "外层结束后遍历 slot 5..10 同样渲染. "
        "最后对 4 个特殊 zone (0xc/0xd/0xe/0xf) 各调 render_field_zone_card_tile_by_type "
        "(FUN_080c39fc). 最终对两个玩家各调 refresh_player_field_slot_tiles (FUN_080c4220) "
        "完成 header/tile 同步. "
        "Constants: gDuelAnimState=0x0202334e, gDuelAnimFlags=0x02023350, "
        "player_stride=0x868, gDuelFieldSlots=0x0201c510."),

    ("FUN_080c36a8", "write_palette_tile_row_to_vram",
        "当 duel field 显示初始化或场地 BG 重建时调用 (indeg=1, tags: vram palette scene_duel_field). "
        "函数从 ROM 数据表 (0x09e49254/0x09e49258) 和 VRAM base 0x0600e800 开始, "
        "以 r7=0..1 (两行或两层) / r2=0..0x15 (列, 22 列) 的双层循环, "
        "每次读取两个 ROM word (palette_index 和 tile_index), "
        "将 tile_index<<5 | palette_offset 合成 halfword 写入 VRAM BG tile map. "
        "外层 r7==1 时, tile_index 在 0..8 范围内加 0xC00 以选择第二套 tile 集. "
        "循环结束后以 copy_bytes_by_halfword 将 palette 数据 (0x100 halfwords, 0x200 bytes) "
        "从 ROM (0x08510460) 复制到 BG palette (0x05000020). "
        "Constants: VRAM_BG_TILE_MAP=0x0600e800, BG_PALETTE_VRAM=0x05000020, "
        "ROM_PALETTE_SRC=0x08510460, ROM_TILE_TABLE_A=0x09e49254, ROM_TILE_TABLE_B=0x09e49258, "
        "TILE_SET_MASK=0xC00, col_count=0x15 (22 cols), row_count=2, "
        "palette_copy_size=0x100 halfwords=0x200 bytes."),

    ("FUN_080ee3a8", "apply_palette_offset_to_tile_row",
        "当 scene_duel_field 需要对一段 BG tile 数据按调色板偏移进行修改时调用 (indeg=5, class D). "
        "函数从栈 sp[0x28] 读取 tile_count (外层循环次数), "
        "以 r4=tile_count (递减) 和 r5=src_ptr (halfword 步进) 构成内层 tile 遍历循环. "
        "对每个 halfword tile entry: "
        "检查 [src] & 0x3ff (tile index field) 非零才处理; "
        "读 sp[0x4] (palette_mask) 与 tile_value OR, "
        "再将 [src] & 0xf000 (palette bank) 加上 r6 (palette_offset lsl 0xc) 合成新 tile halfword 写入 dst [r3+]. "
        "用于将 duel field BG tile 行的调色板索引批量替换为指定 palette_bank, 实现高亮/变色效果. "
        "Constants: TILE_INDEX_MASK=0x3ff, PALETTE_BANK_MASK=0xf000, "
        "PALETTE_FIELD_MASK=0xf0000000 (sp[4] palette_mask)."),

    ("FUN_080ca4f4", "upload_player_icon_gfx_to_vram",
        "当 duel field scene 需要将某玩家的 LP/图标数字 tile 数据和调色板上传到 VRAM 时调用 "
        "(indeg=1, tags: vram palette scene_duel_field). "
        "函数根据 player_side (r0) 与当前激活玩家 (gDuelState[+0x4] XOR 1) 是否匹配, "
        "在两个 VRAM 目标地址间选择 (0x0600fb80=player 1 位置, 0x0600f840=player 2 位置). "
        "以 r4 (tile_row start = 0x1CE 或 0x1D7) / r3 (步进) 为基准, "
        "外层循环 r3=3..0 (3 次) 写入 3 列 tile halfword 到 BG tile map. "
        "然后读 gDuelState 判断当前玩家, 根据是否对侧从 icon_palettes_base (ROM) "
        "选择 +0x20 偏移的调色板, 以 copy_bytes_by_halfword 复制 0x40 字节到 "
        "BG_PAL_VRAM (0x05000180). "
        "若当前玩家==对侧, 还从 icon_tiles_base (ROM asset 0x0600bae0 或 0x0600b9c0) "
        "+ player offset 复制 0x120 字节 icon tile. "
        "Constants: gDuelState=0x0201e2a0, BG_TILE_MAP_P1=0x0600fb80, "
        "BG_TILE_MAP_P2=0x0600f840, BG_PALETTE_ICON=0x05000180, "
        "ICON_TILE_SIZE=0x120 bytes, PALETTE_COPY_SIZE=0x40 bytes, "
        "tile_row_start_local=0x1CE, tile_row_start_remote=0x1D7."),

    # 2026-05-09: campaign-24 batch (topo=539-560, 20 functions)
    ("FUN_080ca5f8", "write_lp_digit_tiles_to_vram",
        "按 player_id (r0) 与 EWRAM 对手 ID (0x0201e2a0+4 XOR 1) 比对, "
        "选择 VRAM 基地址 (LP_VRAM_BASE=0x0600f000) 的目标区域 (P1 偏移 +8, P2 偏移 0x448), "
        "将 LP 数值 (r1, clamp 至 99999) 逐位分解为十进制数字, "
        "以 strh 循环写入 5 个 tile 索引 halfword (tile base index 0x134=0x9a*2). "
        "由 play_ui_effect_0e / FUN_080ca8ec / FUN_0801ec9c 调用. "
        "Constants: LP_VRAM_BASE=0x0600f000, LP_DIGIT_AREA_OFFSET_P2=0x448, "
        "LP_DIGIT_AREA_OFFSET_P1=+8, TILE_IDX_BASE=0x134, LP_MAX=99999, "
        "EWRAM_GAME_CTX=0x0201e2a0."),
    ("FUN_080ca8ec", "init_duel_field_tile_indices",
        "在 duel field 初始化流程中被 init_duel_field_vram_layout (indeg=8) 调用, "
        "向 VRAM 两块 tile 索引区写入连续递增 tile 编号序列, "
        "以及向 palette VRAM 区写入带高位 OR 掩码 (0xe000) 的 tile 属性 halfword. "
        "双层嵌套循环填充两组 tile 区 (各 6 行 x 4 列), 再以第三组循环写入 palette 属性. "
        "无外部参数 (void). "
        "Constants: VRAM_TILE_AREA_A=DAT_080caac4, VRAM_TILE_AREA_B=DAT_080caad0, "
        "TILE_ATTR_PAL_MASK=0xe000, row_stride=0x40 bytes."),
    ("FUN_080f7e0c", "resolve_aob_pattern_entry_ptr",
        "来自 system/s_opdobj.c line 188. "
        "给定 AOB 上下文指针 (r0) 和图案编号 (r1, u16), "
        "验证图案编号 < AOB_PTNSECT_HEADER->PtnNum (越界触发 suppress_assert_report), "
        "计算对应图案数据指针并写入 [ctx+0x4]. "
        "由 init_aob_ctx_from_ptnsect / init_aob_ctx_with_anm_entry / FUN_080f7f08 调用. "
        "Constants: ASSERT_FILE=system/s_opdobj.c, ASSERT_LINE=0xbc(188), AOB_ENTRY_SIZE=4."),
    ("FUN_080f7e48", "init_aob_ctx_with_anm_entry",
        "来自 system/s_opdobj.c line 207. "
        "给定 AOB ctx (r0), 动画编号 (r1, u16), 初始化标志 (r2, u8), "
        "验证动画编号 < AOB_ANMSECT_HEADER->AnmNum, "
        "写动画入口地址到 [ctx+0x8], 根据 [ctx+0x13] bit3/bit4 决定是否调用 "
        "resolve_aob_pattern_entry_ptr 初始化图案指针, 并设置帧步进量 [ctx+0xc/0xd/0xe]. "
        "被 14 个调用方共享 (duel field LP / UI effect 3b/38 / palette vram 路径). "
        "Constants: AOB_FLAG_HAS_PATTERN=0x8, AOB_FLAG_HAS_FRAME_DIV=0x10, "
        "ASSERT_LINE=0xcf(207)."),
    ("FUN_080f7da4", "init_aob_ctx_from_ptnsect",
        "来自 system/s_opdobj.c. AOB 对象生命周期初始化入口, 被 14 个调用方共享. "
        "清零 ctx 前 0x14 字节 (zero_fill_halfword_wrapper), 写入 p_ptnsect 到 [ctx+0x0], "
        "从 mode_param 分离 tile_count (bits[31:16] -> [ctx+0x10]) 与 ptn_mode (bits[3:0] -> [ctx+0x12]), "
        "检测图案数量 > 0x10 设 AOB_FLAG_LARGE (bit7), 写 init_flag 到 bit6, "
        "最后调用 resolve_aob_pattern_entry_ptr(ctx, 0) 设置初始图案指针. "
        "Constants: AOB_CTX_SIZE_HALF=0x14, AOB_LARGE_TILE_THRESHOLD=0x10, "
        "AOB_FLAG_LARGE=0x80, AOB_FLAG_INIT=0x40."),
    ("FUN_080c879c", "init_duel_field_lp_aob_ctx",
        "在 duel field 初始化 hub (init_duel_field_vram_layout) 的唯一调用下, "
        "将 LP 表盘背景 tile 复制到 VRAM (5 次 tile_2d_row_copy), "
        "初始化 AOB ctx (init_aob_ctx_from_ptnsect), 根据 EWRAM 对手 ID 决定动画方向 "
        "(init_aob_ctx_with_anm_entry, anm_no 0 或 1), 再拷贝两组 tile 完成 LP 区域布局. "
        "写 [r4+0x13] bit0=1 标记 AOB ctx 已激活. "
        "Constants: PTR_gP1LifePoints, ANM_NO_OPPONENT=0, ANM_NO_SELF=1."),
    ("FUN_080cc904", "init_duel_field_vram_layout",
        "duel field 场地 VRAM 完整初始化 hub, 被 play_demo_shuen / play_ui_effect_3b/3a / "
        "FUN_0801fec0 等 8 个调用方共享. "
        "依次: (1) zero_fill_by_halfword 清空 VRAM OBJ tile 区; "
        "(2) store_ewram_ctx_ptr_and_clear_mode_flags; (3) reset_display_and_obj_vram; "
        "(4) apply_blend_fadeout_flat; (5) reset_all_bg_scroll_regs_and_shadows; "
        "(6) 设置 gPrng[0xba*2]=1; (7) 配置 BG0-3CNT 四寄存器; "
        "(8) 复制多组 tile/screen 数据; (9) init_duel_field_lp_aob_ctx; "
        "(10) 条件性复制 tile; (11) write_palette_tile_row_to_vram; "
        "(12) init_duel_field_tile_indices + redraw_all_field_slot_tiles; (13) strh DISPCNT. "
        "Constants: BG0CNT=0x1f08, BG1CNT=0x1f09, BG2CNT=0x1d82, BG3CNT=0x1c0b."),
    ("FUN_080cca38", "tick_duel_field_fadeout_step",
        "在 duel field 状态机收尾步骤中被 8 个 caller 调用 "
        "(play_demo_shuen / play_ui_effect_3b/3a / FUN_0801fec0 等). "
        "先将 EWRAM 标志字节 [0x02023345] bit1 置 1 (激活淡出信号), "
        "然后以步进量 2 调用 tick_blend_step_by_delta 推进混合淡出过渡. "
        "无参数; 返回 tick_blend_step_by_delta 的返回值 (0=进行中, 1=完成). "
        "Constants: EWRAM_FLAG_ADDR=0x02023345, BLEND_STEP_DELTA=2, FLAG_BIT1=0x2."),
    ("FUN_080cca5c", "tick_duel_field_fadein_step",
        "与 tick_duel_field_fadeout_step (0x080cca38) 构成对称函数对, 被 10 个 caller 共享. "
        "先将 EWRAM 标志字节 [0x02023345] bits[1:0] 同时清零 (ands ~0x3=0xFC), "
        "然后以步进量 2 调用 start_blend_fadein_with_target 开始混合淡入过渡. "
        "无参数; 返回 start_blend_fadein_with_target 的返回值. "
        "Constants: EWRAM_FLAG_ADDR=0x02023345, BLEND_STEP_DELTA=2, FLAG_CLEAR_MASK=0xFC."),
    ("FUN_080bc7e0", "blend_palette_entry_toward_target",
        "给定 BGR555 调色板条目指针 (r0), 目标颜色 (r1, u16), 混合步数 (r2, u16, clamp 至 0x10), "
        "对 R/G/B 各 5 bit 分量执行线性插值混合 (delta*blend_steps/16), 写回 PAL RAM. "
        "由 banner_anim_state_machine / play_ui_effect_04 / FUN_080bd0a8 等 8 个 caller 调用. "
        "Constants: COMPONENT_MASK=0x1f, BLEND_DIVISOR=16, "
        "PAL_VRAM_BASE=0x05000200, BLEND_MAX_STEPS=0x10."),
    ("FUN_080be600", "tick_banner_pack_state_machine",
        "pack 场景 banner 状态机驱动器, 读取 gBannerState[+0x10] (当前状态 0-4), "
        "通过 switch 跳转到 5 个子状态处理函数, 协调 pack 开包 banner 动画全流程 "
        "(含 display/window/blend/palette/vram). "
        "唯一调用方: play_ui_effect (0x0801ef94, scene_pack). "
        "Constants: gBannerState_OFFSET=0x10, CASE_COUNT=5, OBJ_PAL_HIGH_MASK=0xe000."),
    ("FUN_080c0760", "write_card_image_oam_grid",
        "将卡图 tile 以 5x4 网格形式写入 OAM, 被 play_ui_effect_33/34 调用. "
        "根据 r0 (tile_offset_sign, 0 或 1) 计算 OAM attr bit7 (0x400 掩码), "
        "对 5 行 x 4 列 OAM 条目循环调用 write_oam_entry_with_tile_inc, "
        "每行 tile 步进 0x20, 每列 attr 步进 4. "
        "r1 在入口第一条指令 (rsbs r1,r0,#0) 被覆盖, 不是独立参数. "
        "Constants: GRID_COLS=4, GRID_ROWS=5, TILE_ROW_STEP=0x20, ATTR_STEP=4, "
        "OAM_ATTR_MASK=0x400."),
    ("FUN_080f5668", "tick_blend_step_with_bldcnt",
        "被 play_ui_effect_33/34 调用, 设置 BLDCNT (0x04000050) = r1, "
        "累加 r0 (delta) 到 gPrng+0x200 bits[5:0] (blend step 计步字节, clamp 至 0x1f), "
        "写 BLDY (0x04000054) = current_step; step > 0x1e 返回 1 (完成), 否则返回 0. "
        "Constants: BLDCNT=0x04000050, BLDY=0x04000054, "
        "gPrng_BLEND_STEP_OFFSET=gPrng+0x200, BLEND_STEP_MAX_ACTIVE=0x1e, "
        "BLEND_STEP_CLAMP=0x1f, BLEND_STEP_FIELD_MASK=0x3f."),
    ("FUN_080f0db4", "init_line_buf_with_jp_font_flag",
        "被 draw_card_name_to_bg_tile_vram / draw_card_atkdef_label_to_vram 调用, "
        "是 card stats 区域文字渲染的字体初始化路径. "
        "调用 setup_line_buf_pos_and_font (r0=x_pos, r1=font_type) 建立 line buffer 渲染状态, "
        "然后对 EWRAM [0x02006ed0+0x14] bit7 置 1, 标记启用 JP 字体扩展渲染模式. "
        "Callsite 固定传入 r0=0xe / r1=0x2. "
        "Constants: EWRAM_FONT_CTX=0x02006ed0, FLAG_JP_EXT=0x80."),
    ("FUN_080c0180", "draw_card_atkdef_label_to_vram",
        "从 card_stats_table 按 card_idx (r0) 读取 ATK (offset 3) / DEF (offset 4), "
        "调用 init_line_buf_with_jp_font_flag (r0=0xe, r1=2) 建立 JP 字体上下文, "
        "检查 ATK 有效性后选择渲染路径: 等级文字 (lookup_level_glyph_index + render_card_level_text_to_buf) "
        "或 ATK/DEF 数字 (render_atk_def_digits_to_buf), "
        "最后调用 write_line_buf_to_bg_tile_vram 写入 BG tile VRAM. "
        "唯一调用方: FUN_080c05b4 (card image 显示页 hub). "
        "Constants: CARD_STATS_FIELD_ATK=3, CARD_STATS_FIELD_DEF=4, "
        "INVALID_STAT_SENTINEL=0xffff, ENTRY_STRIDE=0xb."),
    ("FUN_080bff34", "repack_nibbles_with_palette_offset",
        "将 r0 (nibble_packed, u16, 含 4 个 nibble 调色板索引) 的每个 nibble "
        "加上 r1 (palette_offset, u8) 后截断至 nibble, 重新打包为 16 位输出. "
        "由 render_card_image_to_vram 4 次调用, 用于卡图调色板索引批量偏移. "
        "纯叶子函数, 无外部副作用. "
        "Constants: NIBBLE_MASK=0x0f0f, UPPER_NIBBLE_MASK=0xf0."),
    ("FUN_080bff6c", "render_card_image_to_vram",
        "从 ROM 卡图数据表按 card_idx (r0) 和 VRAM 目标槽位 (r1) 加载卡图 tile 和调色板到 VRAM. "
        "4 次调用 repack_nibbles_with_palette_offset 转换调色板索引后写入 PAL RAM (0x05000200), "
        "再将 tile 数据复制到 BG VRAM (0x060148c0 + slot_offset); "
        "外层循环 11 行 x 0x4f halfword. 唯一调用方: FUN_080c05b4. "
        "Constants: VRAM_CARD_TILE_BASE=0x060148c0, PAL_RAM_BASE=0x05000200, "
        "TILE_ROW_HALFWORDS=0x4f, OUTER_LOOP_COUNT=0xa."),
    ("FUN_080c00f0", "draw_card_name_to_bg_tile_vram",
        "渲染卡牌名称到 BG tile VRAM. 唯一调用方: FUN_080c05b4 (card image 显示页 hub). "
        "调用 init_line_buf_with_jp_font_flag (r0=0xe, r1=2) 建立 JP 字体上下文, "
        "读 EWRAM 字体方向标志选择字体基址, "
        "调用 render_card_name_to_line_buf (card_idx) 渲染到 line buffer, "
        "检查 card_stats_table type 字段 (offset 6, 与 0x16 比较) 选择竖排/横排字体映射表, "
        "最后调用 write_line_buf_to_bg_tile_vram 写入 VRAM. "
        "Constants: CARD_STATS_TYPE_FIELD=6, CARD_TYPE_VERTICAL_LIMIT=0x16."),
    ("FUN_080c0204", "write_nibble_to_bg_tile_cell",
        "在 BG tile VRAM 指定二维坐标 (tile_x=r0, tile_y=r1) 写入单个 nibble (r2=palette_nibble, r3=vram_row_base). "
        "将坐标转换为 VRAM halfword 地址 (VRAM_BASE=0x06010000, 行步进 0x400 halfword), "
        "根据 tile_y 奇偶确定写高/低 nibble, 修改 halfword 后写回. "
        "被 write_nibble_sequence_to_bg_tiles 两次调用. "
        "Constants: VRAM_BG_TILE_BASE=0x06010000, TILE_ROW_STRIDE=0x400, "
        "NIBBLE_HIGH_MASK=0xff00, NIBBLE_LOW_MASK=0x00ff."),
    ("FUN_080c0274", "write_nibble_sequence_to_bg_tiles",
        "从 packed nibble 字节数组 (r2) 中逐字节读取双 nibble, "
        "对每个非零 nibble 调用 write_nibble_to_bg_tile_cell 写入对应 BG tile VRAM 坐标. "
        "外层循环 8 槽 (r7: 0..7), 内层循环 nibble 序列 (r8, 步进 -1), "
        "坐标由 r0 (packed: lo16=tile_x_even [6..80], hi16=inner_row_base [5..6]) 和 r1 (vram_row_param) 驱动. "
        "被 FUN_080c0310 和 FUN_080c05b4 调用. "
        "Constants: OUTER_LOOP_COUNT=8, NIBBLE_LOW_MASK=0x0f, NIBBLE_HIGH_MASK=0xf0."),
    # 2026-05-09: batch #25 (campaign-25) landing (topo=561-582, 20 functions)
    ("FUN_080c0310", "write_nibble_row_pair_to_bg_tiles",
        "BG tile VRAM nibble dual-row writer: 4x bl write_nibble_sequence_to_bg_tiles, "
        "stride 0x20 per row, 2x2 tile block. VRAM base 0x06010000 (DAT_080c03e8). "
        "Caller: render_card_display_with_type_gfx (ATK/DEF nibble rows)."),
    ("FUN_080c0394", "copy_card_frame_nibbles_to_palette_vram",
        "Card frame nibble tile copy to OBJ/BG VRAM by palette offset. "
        "r1>>11=type selects 0x06010000 BG or 0x05000200 PAL VRAM. "
        "Tail-jumps to LAB_080c0598 (no independent return). Caller: render_card_display_with_type_gfx."),
    ("FUN_080c05b4", "render_card_display_with_type_gfx",
        "Full card display render: card image + ATK/DEF nibble tiles + name label + type icon. "
        "Reads card_stats_table[card_id*11]. Dispatches on card_type 0x16/0x17 (fusion/ritual frame). "
        "Callers: play_ui_effect_33, play_ui_effect_34."),
    ("FUN_080f55fc", "clamp_blend_counter_to_target",
        "Converge gPrng+0x200 blend counter (low 6 bits) toward r0 target. "
        "If current>target: subtract delta, mask 0x3f. Else: clear and set negative 0x40. "
        "Callers: play_ui_effect_33, play_ui_effect_34."),
    ("FUN_080c2d24", "blit_card_frame_tile_row_to_vram",
        "Copy card_medium_frame_tile_data row to OBJ VRAM 0x06010000+r1*0x20. "
        "Checks DAT_080000ae flag 0x4a for field_spell frame variant. "
        "Calls tile_2d_row_copy(dest, 0, 8, 6). 5 callers: play_ui_effect_20/21/23/25/0c."),
    ("FUN_080c8bf0", "build_slot_activation_mask_for_player",
        "Build slot activation bitmask at 0x020230c0+3 for current player. "
        "Only runs when player_state==3 (duel phase check). "
        "Loops slot 0..4 calling eval_slot_activation_guard_full; clears mask if gPrng+0x1d10==-1."),
    ("FUN_080f70c4", "push_oam_entry_to_aob_slot",
        "Write OAM attr0/1/2 (from r2 ptr) to AOB slot array at gPrng+0x1bc, then increment slot write ptr. "
        "Skips if slot ptr byte==0x80 (full). Slot stride 8 bytes (lsls r1,#3)."),
    ("FUN_080f8000", "render_aob_frame_to_oam",
        "Render AOB animation object current frame to OAM buffer and copy tile data to VRAM 0x06010000. "
        "16-case shape/color dispatch; calls copy_bytes_by_halfword + push_oam_entry_to_aob_slot. "
        "11 callers including play_ui_effect_37/38/3b."),
    ("FUN_080f7f08", "tick_aob_frame_counter",
        "Advance AOB frame counter (aob+0xc/0xd/0x12/0x13), resolve new ptn entry on frame change. "
        "Returns 0 if uninitialized (bit5 of aob+0x12), 1 on normal tick. "
        "Shared by same 11 callers as render_aob_frame_to_oam."),
    ("FUN_080c2ddc", "write_digit_oam_column_with_scroll",
        "Decimal decompose r4 via __modsi3/__divsi3 (base 10), write each digit OAM entry. "
        "Digit tile base 0x70, x step -0xc per digit (right to left). "
        "Optional gPrng+0x20c bit1 x-jitter via r3 scroll_flag. Caller: render_decimal_number_to_oam."),
    ("FUN_080c2e58", "render_decimal_number_to_oam",
        "Count decimal digits of r1, compute OAM x_base (r5*100+digit_count*6+0x52), "
        "then call write_digit_oam_column_with_scroll. Caller: render_card_number_oam_by_player."),
    ("FUN_080c2eac", "render_card_number_oam_by_player",
        "Select OAM tile orientation by player side comparison (0x0201fe60+3/4 vs 0x0201e2a0+4^1). "
        "flip_sign: 0xae (flip) or 0x4a (normal). Calls render_decimal_number_to_oam. "
        "r0=oam_x_base [0x200..0x208], r1=oam_y_base. Caller: render_dual_card_number_oam_columns."),
    ("FUN_080c305c", "render_dual_card_number_oam_columns",
        "Call render_card_number_oam_by_player twice with r0=0x200 then r0=0x208 (two digit columns). "
        "r1=oam_y same for both calls. Caller: play_ui_effect_0c."),
    ("FUN_08096e14", "init_duel_zone_target_slot_refs",
        "Init duel_field zone slot ref cache in gP1LifePoints+0x1d68 area. "
        "Calls get_zone_slot_ptr 3x; extracts card_id bits[12:0]; sets active flag at +0x1d54=1. "
        "11 callers in duel_field scene."),
    ("FUN_080c6800", "transform_zone_oam_coords_by_player",
        "Mirror OAM coords (r2=x, r3=y) by player_id vs ctx.current_player^1; 16-case zone_type switch. "
        "Returns packed (y<<16|x). Pure calc, no external writes. "
        "Callers: render_duel_field_slot_oam_grid, compute_card_sprite_oam_coords_by_zone."),
    ("FUN_080c35ac", "resolve_zone_oam_base_coords_by_type",
        "Lookup OAM base coords from DAT_080c35e8 table by zone_type [0..15] and player_id. "
        "16-case switch; returns packed (y<<16|x). Pure query. "
        "11 callers including play_ui_effect_15/10/play_card_zoom_in."),
    ("FUN_080c8aa8", "render_duel_field_slot_oam_grid",
        "Iterate all duel_field zone slots (type 0..10 + b..f), compute OAM coords via "
        "resolve_zone_oam_base_coords_by_type + transform_zone_oam_coords_by_player, "
        "write OAM via write_oam_entry_from_packed_args. void input. Caller: play_ui_effect_03."),
    ("FUN_080c57c4", "compute_card_sprite_oam_coords_by_zone",
        "Compute card sprite OAM coords by zone (player_id r5, zone_type r1, zone_idx r2). "
        "Calls resolve_zone_oam_base_coords_by_type; applies y offset by card_type [1/3/5]. "
        "Loops activation mask bits. Returns void. 3 wrapper callers."),
    ("FUN_080c6240", "tick_card_sprite_oam_step_a",
        "Call compute_card_sprite_oam_coords_by_zone, increment ctx+0x2a counter, "
        "return 1 if counter>3 (done) else 0 (continue). void input. Caller: FUN_080c65b0."),
    ("FUN_080f7528", "write_tile_rows_to_vram_by_mode",
        "Conditional copy/zero OBJ VRAM rows: src==0 calls zero_fill_by_halfword per row, "
        "src!=0 calls copy_bytes_by_halfword. Row stride 0x400 (OBJ 2D mode). "
        "r2>>0xb=halfword stride, [sp+0x18]=col offset. Callers: FUN_080c5b78, FUN_080dc4ec."),

    # 2026-05-09: batch #26 (campaign-26, topo=583-604, 19 functions)
    ("FUN_080c5b78", "dispatch_duel_field_zone_oam_by_type",
        "Dispatches OAM update for a single duel field zone slot by zone_type. "
        "Reads gPrng+0x214 halfword to extract zone_type [0..0xd]; "
        "16-way jump table routes each type to a dedicated OAM write sub-function. "
        "No APCS input (all state from gPrng+0x214). Returns void. "
        "Called by init_duel_field_card_sprite_vram (080c6184) and setup_zone_oam_entry_by_field_slot (080c5444). "
        "Constants: gPrng_zone_halfword=gPrng+0x214, zone_type_max=0xd."),
    ("FUN_080c6184", "init_duel_field_card_sprite_vram",
        "Initialize card sprite VRAM for a duel field slot: "
        "copies tile data to VRAM 0x06013800 via write_tile_rows_to_vram_by_mode, "
        "copies palettes to PAL VRAM 0x05000280 and 0x050002a0, "
        "calls dispatch_duel_field_zone_oam_by_type to configure OAM, "
        "updates slot_phase counter at ctx+0x2a. "
        "r0=u16 player_id [0..1]. Returns void. "
        "Side-effects: OBJ VRAM 0x06013800, PAL VRAM 0x05000280/0x050002a0, OAM updated. "
        "Constants: VRAM_CARD_SPRITE=0x06013800, PAL_A=0x05000280, PAL_B=0x050002a0."),
    ("FUN_080c6268", "tick_card_sprite_oam_step_b",
        "OAM animation second step for duel field card sprite. "
        "Reads gPrng+0x210 packed halfword; extracts player_flag (bit15), "
        "x_coord (bits[14:8]), y_coord (bits[6:0]); writes OAM entry. "
        "r0=void. Returns void. Caller: tick_card_sprite_oam_phase_dispatch (080c65b0). "
        "Constants: gPrng_oam_word=gPrng+0x210, player_flag_bit=15, x_bits=[14:8], y_bits=[6:0]."),
    ("FUN_080c6490", "tick_card_sprite_oam_step_c",
        "OAM animation third step for duel field card sprite; symmetric to tick_card_sprite_oam_step_a. "
        "Increments ctx+0x2a step counter; returns 1 when counter > 3 (done), else 0 (continue). "
        "r0=void. Caller: tick_card_sprite_oam_phase_dispatch (080c65b0). "
        "Constants: step_done_threshold=3."),
    ("FUN_080c65b0", "tick_card_sprite_oam_phase_dispatch",
        "4-phase card sprite OAM state machine: "
        "phase 0=fadein (tick_card_sprite_oam_step_a), "
        "phase 1=card_info (tick_card_sprite_oam_step_b), "
        "phase 2=vram_refresh (init_duel_field_card_sprite_vram), "
        "phase 3=fadeout (tick_card_sprite_oam_step_c). "
        "Reads phase index from ctx+0x28; advances phase on step completion. "
        "r0=void. Returns void."),
    ("FUN_080c6638", "resolve_zone_data_ptr_by_oam_word",
        "Decode packed OAM halfword and return zone data pointer via 16-way zone_type dispatch. "
        "Reads gPrng+0x210 (oam_word); extracts zone_type [0..0xd]; "
        "jump table returns pointer to zone data block for each type. "
        "Pure lookup; no side-effects. "
        "r0=void. Returns u32* zone_data_ptr. "
        "Constants: gPrng_oam_word=gPrng+0x210, zone_type_max=0xd."),
    ("FUN_080c64b8", "dispatch_duel_zone_pair_to_oam",
        "Calls resolve_zone_data_ptr_by_oam_word twice, compares the two zone data pointers; "
        "if they differ, calls sync_state_and_init_sprite to commit the OAM update. "
        "r0=void. Returns void. "
        "Caller: tick_card_sprite_oam_phase_dispatch (080c65b0) in card_info phase. "
        "Constants: zone comparison drives sprite sync trigger."),
    ("FUN_080c5444", "setup_zone_oam_entry_by_field_slot",
        "Read gPrng+0x210 OAM halfword; dispatch on zone_type via DAT_080c54a8 16-entry table; "
        "write OAM slots 0x70fb/0x70fc/0x70fd with computed attr0/1/2. "
        "r0=void. Returns void. "
        "Caller: dispatch_duel_field_zone_oam_by_type; used in duel field OAM init path. "
        "Constants: gPrng_oam_word=gPrng+0x210, OAM_SLOT_A=0x70fb, OAM_SLOT_B=0x70fc, OAM_SLOT_C=0x70fd, "
        "zone_dispatch_table=DAT_080c54a8."),
    ("FUN_08096ecc", "zero_duel_lp_display_counters",
        "Clear two duel LP display animation counters. "
        "Writes 0 to gP1LifePoints+0x1d4c and gP1LifePoints+0x1d5c (str r2=0 twice). "
        "No APCS input; leaf function (bx lr). Returns void. "
        "Callers: FUN_080b70ac (duel_field init chain), play_ui_effect_03 (0x080cca80). "
        "Side-effects: [gP1LifePoints+0x1d4c]:=0; [gP1LifePoints+0x1d5c]:=0. "
        "Constants: gP1LifePoints=0x0201c4e0, field_A_offset=0x1d4c, field_B_offset=0x1d5c."),
    ("FUN_0802cf98", "tick_scene_blend_fadeout_step",
        "Execute one blend fadeout step. "
        "Reads BLDCNT (0x04000050), ORs BLD_SRC_ALL mask 0x1f00, writes back to enable full-screen blend source. "
        "Then calls tick_blend_step_by_delta(delta=4) to advance blend counter. "
        "r0=void. Returns void. "
        "Caller: FUN_0802cfd4 (tick_scene_blend_fade_sequence) phase 0 branch. "
        "Side-effects: [BLDCNT 0x04000050] |= 0x1f00; blend counter += 4 via callee. "
        "Constants: BLDCNT=0x04000050, BLD_SRC_ALL=0x1f00, blend_delta=4."),
    ("FUN_0802cfb4", "tick_scene_blend_fadein_step",
        "Execute one blend fadein step and detect completion. "
        "Calls start_blend_fadein_with_target(target=4); if returns 0 (in progress) returns 0. "
        "On completion: writes 0 to BLDCNT (0x04000050) to disable blend, returns 1. "
        "r0=void. Returns u32 done_flag (0=in progress, 1=complete). "
        "Caller: FUN_0802cfd4 (tick_scene_blend_fade_sequence) phase 1 branch. "
        "Side-effects: [BLDCNT 0x04000050]:=0 on completion. "
        "Constants: BLDCNT=0x04000050, target=4."),
    ("FUN_0802cfd4", "tick_scene_blend_fade_sequence",
        "Fadeout-fadein state machine for scene blend transition. "
        "Reads phase_state from 0x02023360+0x118; phase 0: calls tick_scene_blend_fadeout_step; "
        "phase 1: calls tick_scene_blend_fadein_step; advances phase on completion. "
        "Always returns 0. r0=void. "
        "Caller: frame_counter-driven state machine hub. "
        "Constants: phase_state_addr=0x02023360+0x118."),
    ("FUN_080c55dc", "init_zone_oam_ctx_by_type",
        "Zero-fill EWRAM OAM context buffer at 0x0201ff30 (0x2c halfwords). "
        "Sets ctx_valid bit0=1 in context header. "
        "16-way zone_type dispatch to initialize type-specific OAM fields. "
        "r0=void. Returns void. "
        "Caller: setup_zone_oam_entry_by_field_slot and related OAM init path. "
        "Side-effects: [0x0201ff30..+0x58]:=0; ctx valid bit set; OAM type fields written. "
        "Constants: ctx_base=0x0201ff30, ctx_size=0x2c halfwords, valid_bit=bit0."),
    ("FUN_0802cba0", "init_jp_font_linebuf_for_render",
        "Initialize JP font line buffer for card name rendering. "
        "Calls setup_line_buf_with_font_and_align(font_id=0x1a, width=0x28); "
        "writes JP font direction flags to EWRAM; "
        "clears PAL VRAM region 0x050001e0 (palette slot for text rendering). "
        "r0=void. Returns void. "
        "Caller: render_card_name_format_to_line (0x0802c30c) and related result_screen functions. "
        "Side-effects: line buffer state updated; [0x050001e0..] zeroed. "
        "Constants: font_id=0x1a, width=0x28, PAL_TEXT_VRAM=0x050001e0."),
    ("FUN_0802cc08", "commit_glyph_linebuf_to_sprite_vram_with_index",
        "Clear OBJ VRAM 0x06008020 (0x8200 halfwords zero-fill), "
        "commit line buffer glyphs to sprite VRAM, "
        "then write tile index sequence (0,1..25,0,0,0) x40 loops into OAM index table. "
        "r0=void. Returns void. "
        "Caller: result_screen card name rendering pipeline. "
        "Side-effects: OBJ VRAM 0x06008020 zeroed; tile index table written. "
        "Constants: OBJ_VRAM_BASE=0x06008020, zero_fill_count=0x8200 halfwords, "
        "tile_seq_len=26 (0+1..25+0+0+0), loop_count=0x28."),
    ("FUN_080f5a98", "upload_pack_vram_and_palette",
        "Upload pack banner VRAM and palette data: "
        "4x copy_bytes_by_halfword: BG PAL -> 0x05000000, BG tile -> 0x06004000, "
        "OBJ PAL -> 0x05000200, OBJ tile -> 0x06010000. "
        "Clears palette[0] entry (transparent) at BG PAL base. "
        "r0=u32 src_ptr (ROM pack data block). Returns void. "
        "Side-effects: BG PAL 0x05000000, BG tile 0x06004000, OBJ PAL 0x05000200, OBJ tile 0x06010000. "
        "Constants: BG_PAL=0x05000000, BG_TILE=0x06004000, OBJ_PAL=0x05000200, OBJ_TILE=0x06010000."),
    ("FUN_08031348", "find_lp_entry_by_flag_and_type",
        "Linear scan of gP1LifePoints+4 array (step=4, max 0xff entries) for an entry matching "
        "flag bit0 == r0, entry_type (low 13 bits of halfword at [entry+0x10e0]) == 1, "
        "and valid_mark bit7 of [entry+0x10e0+1] set. "
        "Returns 1 if matching entry found, 0 if not found. "
        "r0=u32 flag_value [0..1]. Returns u32 found_flag. "
        "Callers: FUN_08020db4, FUN_08020fa8, FUN_0802c358 (result_screen LP record display). "
        "Constants: array_step=4, field_offset=0x10e0, max_count=0xff, type_value=1, valid_bit7=1."),
    ("FUN_0802c30c", "render_card_name_format_to_line",
        "Lookup card name and format-render to a display line. "
        "Calls card_name_lookup_by_internal_id(r3=card_internal_id) to get name ptr; "
        "calls expand_format_text_to_buf(name, r2=fmt_args, sp_buf, 0x100) to expand into 256-byte stack buf; "
        "calls text_render_wrapper(r5=dst_buf, r6=line_idx, text_buf, flags=0x8008) for first pass; "
        "calls text_render_wrapper again with extra_flags=7 for second pass (shadow/highlight). "
        "Returns low 10 bits of [gPrng+0x6ed0+0xe] halfword as render_width. "
        "r0=ptr dst_buf, r1=u16 line_idx [0..0x401], r2=ptr fmt_args, r3=u16 card_internal_id. "
        "Returns u16 render_width (bits[9:0] of gPrng+0x6ed0[0xe]). "
        "Caller: FUN_0802c358 (result_screen). "
        "Constants: stack_buf_size=0x100, render_flags=0x8008, extra_flags=7, "
        "width_field_offset=0xe, width_mask=0x3ff."),
    ("FUN_080f51ac", "expand_card_name_escape_to_buf",
        "Scan format string for percent-c escape sequence (0x25 0x63), "
        "read 3 decimal digit characters, call internal_card_id_to_card_id + "
        "select_charset_then_load_name + append_text_to_buf_end to append the card name. "
        "r0=ptr fmt_str, r1=ptr out_buf. Returns void. "
        "Caller: expand_format_text_to_buf (format engine). "
        "Constants: ESCAPE_PERCENT=0x25, ESCAPE_C=0x63, digit_count=3."),

    # --- batch #27 (campaign-27, 2026-05-09) ---
    ("FUN_08094e74", "get_card_data_bit_by_index",
        "Return the 1-bit flag at the given index from the ROM card-data table. "
        "r0=card_data_index [0..0x72]: index<=0x34 -> direct word read from EWRAM table at "
        "0x0201b1b0 stride-4; index>0x34 -> compute word-row via (index-0x36)>>5, "
        "read from table_b base (0x0201b1b0+0xd4), extract bit via lsrs+ands. "
        "Returns r0=bit_value [0..1]. No side effects. "
        "Callers: result_screen, card_image, game_str, duel_field clusters. "
        "Constants: table_base_a=0x0201b1b0, stride=4, max_idx_a=0x34, "
        "table_base_b=0x0201b1b0+0xd4, row_shift=5, offset_a=0x36, offset_b=0x17."),
    ("FUN_0802c238", "render_game_text_decimal_to_line",
        "Format a game_str record as decimal text and render it to a display line. "
        "Steps: (1) load str_id_offset from sp+0x58, add base 0x0c1c, call game_str_id_to_row; "
        "(2) look up game_str_pointer_table with font-variant correction from settings[0x6c2c] bits[2:0]; "
        "(3) call expand_format_decimal_to_buf; (4) call count_bytes_until_null for width; "
        "(5) four passes of text_render_wrapper (flags 0x8008, 0x7, r8-saved, sp+0x5c). "
        "Returns r0=render_width bits[9:0] from gPrng+0x6ed0[0xe]. "
        "Constants: str_base_offset=0x0c1c, settings_addr=0x02000000+0x6c2c, "
        "font_variant_mask=0x7, render_flags_1=0x8008, render_flags_2=0x7, "
        "width_field=gPrng+0x6ed0+0xe, width_mask=0x3ff."),
    ("FUN_080e3258", "get_duel_puzzle_count",
        "Return the hardcoded total count of duel puzzles: movs r0,#0x32 -> bx lr. "
        "0x32=50, matching the 50 built-in duel puzzles. No parameters. No side effects. "
        "Called by find_puzzle_slot_by_id as loop bound and by scene_duel_puzzle callers "
        "as upper limit. Constants: DUEL_PUZZLE_COUNT=0x32 (=50)."),
    ("FUN_080e325c", "find_puzzle_slot_by_id",
        "Linear search in the duel puzzle table for an entry matching puzzle_id. "
        "r0=puzzle_id [0..0x31]. r5=table_base=0x09e5e9cc, stride=0xc (12 bytes/entry). "
        "Loop: call get_duel_puzzle_count() for upper bound (50); compare ldrh [r5] with r6; "
        "match -> return r4 (slot index); no match -> r5+=0xc, r4++. "
        "Returns s32: slot_index [0..0x31] if found, -1 (rsbs) if not found. No side effects. "
        "Constants: PUZZLE_TABLE_BASE=0x09e5e9cc, PUZZLE_ENTRY_STRIDE=0xc, NOT_FOUND=-1."),
    ("FUN_0802c358", "render_card_name_escape_to_line",
        "Expand and render the card name (escape form) for a given card_id to a display line, "
        "then dispatch to sub-scene rendering via 16-entry switchD. "
        "r0=card_id [0x2711..0x2744] (saved to r9; r8/r10 init to 0). "
        "Steps: (1) r9+0x3e8 -> game_str_id_to_row; (2) font-variant from settings[0x6c2c]; "
        "(3) expand_card_name_escape_to_buf to sp+8; (4) two text_render_wrapper passes "
        "(flags 0x8008, 0x5); (5) read render_width from gPrng+0x6ed0[0xe]; "
        "(6) switchD keyed on r9-0x2711. Tail-jumps into sub-scene; no direct return. "
        "Constants: game_str_base=0x3e8, settings_addr=0x02000000+0x6c2c, "
        "render_flags_1=0x8008, render_flags_2=5, switch_adjust=-0x2711."),
    ("FUN_0802cc68", "init_card_name_result_screen",
        "Fully initialize the card-name result screen: validate card_id range, "
        "configure VRAM/BG registers, upload tiles and palette, init font buffer, render card name. "
        "r0=card_id [0x2711..0x2744]; validated as r0-0x2711 in [0..0x33], else return 0. "
        "Steps: clear DISPCNT, reset_display_and_obj_vram, store_ewram_ctx_ptr_and_clear_mode_flags, "
        "set BG0-3CNT, reset_all_bg_scroll_regs_and_shadows, upload_pack_vram_and_palette, "
        "zero_fill_by_halfword (VRAM regions), copy_bytes_by_halfword (tiles/palette), "
        "load_pack_tile_and_map_to_vram, setup_line_buf_pos_and_font, init_jp_font_linebuf_for_render, "
        "render_card_name_escape_to_line, commit_glyph_linebuf_to_sprite_vram_with_index. "
        "Returns 1 on success, 0 if card_id out of range. "
        "Side effects: DISPCNT=0, BG0CNT=0x5, BG1CNT=0x104, BG2CNT=0x8208, BG3CNT=0x407, VRAM/PAL. "
        "Constants: DISPCNT=0x04000000, card_id_adjust=-0x2711, max_adjusted=0x33, "
        "gPrng_slot_offset=0x174, VRAM_BG=0x06004000, PAL_BASE=0x05000220."),
    ("FUN_080c6e9c", "decode_zone_oam_word_to_cursor_fields",
        "Unpack a zone OAM descriptor word into player/zone_type/sub_idx fields and dispatch "
        "to the matching zone cursor-position handler via 16-entry switchD. "
        "r0=packed_oam_word (low16: bit7=player_id, bits[6:0]=zone_type; bits[31:24]=sub_idx). "
        "r1=secondary_param (saved to r8, passed to switchD cases). "
        "Reads gDuelFieldCtx[0x0201e2a0+4] for player-flip flag; may swap r8. "
        "Tail-jumps into switchD; no direct return. "
        "Called by apply_zone_cursor_step (0x080c716c) on mode_flag bit path. "
        "Constants: player_bit=0x80, zone_type_mask=0x7f, sub_idx_shift=24, "
        "duel_field_ctx=0x0201e2a0, zone_type_max=0xf, jump_table=DAT_080c6ef8."),
    ("FUN_080c4cd4", "check_lp_threshold_for_zone_slot",
        "Check whether the LP value of a given player slot meets a threshold. "
        "r0 bit0=player_id [0..1]; r1 low16=threshold [0..0xFFFF]. "
        "Reads gP1LifePoints[player_id*0x868+0xc] halfword. "
        "Returns: 0 if slot empty/zero, 1 if LP < threshold, 2 if LP >= threshold. "
        "No side effects (pure read). Called by decode_zone_oam_word_to_slot_fields case 5. "
        "Constants: gP1LifePoints=0x0201C4E0, player_stride=0x868, lp_slot_offset=0xc."),
    ("FUN_080c6b04", "decode_zone_oam_word_to_slot_fields",
        "Unpack a zone OAM descriptor word into player/zone_type/sub_idx fields and dispatch "
        "to the matching zone slot handler via 16-entry switchD; symmetric to "
        "decode_zone_oam_word_to_cursor_fields but focused on slot position decoding and LP checks. "
        "r0=packed_oam_word; r1=secondary_param (saved to r8). "
        "Reads gDuelFieldCtx[0x0201e2a0+4] for flip flag. Some switchD cases call "
        "check_lp_threshold_for_zone_slot. Tail-jumps via switchD; no direct return. "
        "Constants: player_bit=0x80, zone_type_mask=0x7f, sub_idx_shift=24, "
        "duel_field_ctx=0x0201e2a0, zone_type_max=0xf."),
    ("FUN_080c707c", "check_zone_card_id_cache_valid",
        "Check whether the card-ID cache for the zone described by the OAM word is valid (non-empty). "
        "r0=packed_oam_word (same format as decode_zone_oam_word_to_cursor_fields). "
        "Steps: resolve_zone_data_ptr_by_oam_word, unpack player/zone_type/tile fields, "
        "check gDuelFieldCtx flip, handle special zone 0xd (LP word check), "
        "call get_zone_card_attribute_by_type and ensure_card_id_cache_entry. "
        "Returns 1 if valid card ID cached, 0 otherwise. "
        "Side effects: ensure_card_id_cache_entry may write EWRAM card-ID cache. "
        "Constants: player_bit=0x80, zone_type_mask=0x7f, tile_shift=24, "
        "player_stride=0x868, lp_offset=0x10, gDuelFieldCtx=0x0201e2a0."),
    ("FUN_080cc618", "sort_zone_oam_entries_to_vram",
        "Collect active zone OAM sprite entries from gPrng sprite table into a stack buffer, "
        "sort them with qsort, then write back to OAM mirror at 0x030001fc. "
        "No parameters. Steps: alloc sp-=0x600; read count from gPrng+0x1bc+0x400; "
        "collect 9-byte entries (ldmia+str/strb) to sp buffer; "
        "qsort(sp_buf, count, 0xc, compare_fn=0x080cc5f5); "
        "write back 6 bytes/entry via copy_bytes_by_halfword to OAM[entry*8]. "
        "Side effects: writes [0x030001fc+entry*8] for each active OAM entry. "
        "Constants: gPrng_sprite_table=gPrng+0x1bc, count_offset=0x400, "
        "entry_copy_size=9, qsort_stride=0xc, oam_target=0x030001fc, write_bytes=6, "
        "sp_frame=0x600."),
    ("FUN_080c699c", "set_zone_oam_coords_by_player",
        "Transform zone OAM coordinates via transform_zone_oam_coords_by_player and write the "
        "result into the OAM sprite entry, then refresh the OAM sort buffer. "
        "r0=src_x, r1=src_y, r2=zone_type [0..0xF], r3=extra_flags. "
        "write_mode: r2==0 -> mode=0x6 (player 0), else mode=0x2. "
        "Combines transformed x/y + mode + (r3<<0xc) + 0x2300 (OAM type base) into strh. "
        "Calls sort_zone_oam_entries_to_vram to flush OAM mirror. "
        "Side effects: via callee writes OAM sprite table and OAM mirror. "
        "Constants: mode_player0=0x6, mode_default=0x2, oam_type_base=0x2300."),
    ("FUN_08096974", "get_lp_display_anim_counter",
        "Return the LP display animation counter value from gP1LifePoints+0x1d4c. "
        "4-instruction leaf: load gP1LifePoints (0x0201C4E0), add offset 0x1d4c, ldr word, bx lr. "
        "No parameters. No side effects. "
        "Field named 'duel LP display animation counter_A' by zero_duel_lp_display_counters (0x08096ecc). "
        "All callers use cmp r0,#0x1 to gate subsequent logic on animation state. "
        "Constants: gP1LifePoints=0x0201C4E0, field_offset=0x1d4c."),
    ("FUN_080f6144", "write_oam_entry_attr_pairs",
        "Write two attr halfword pairs into a gPrng sprite table entry. "
        "r0=packed_xy_low (>>0xb -> entry_index), r1=packed_attr_hi (hi16=attr1_x, lo16=attr1_y), "
        "r2=packed_attr2 (hi16=attr2_hi, lo16=attr2_lo). "
        "Writes: [entry+6]=r1>>16, [entry+0xe]=r1&0xFFFF, [entry+0x16]=r2>>16, [entry+0x1e]=r2&0xFFFF. "
        "Pure leaf, no bl calls. "
        "Constants: gPrng=0x03000040, sprite_table_offset=0xde*2=0x1bc, entry_shift=0xb, "
        "attr1_x_off=6, attr1_y_off=0xe, attr2_hi_off=0x16, attr2_lo_off=0x1e."),
    ("FUN_080f72e8", "write_oam_sprite_entry_by_flip_mode",
        "Write OAM attr pairs to a gPrng sprite table entry with per-flip-mode x/y offset, "
        "then increment entry counters. "
        "r0=packed_xy (lo16=x, hi16=y), r1=packed_attr (hi16=attr_hi, lo16=sub_type), "
        "r2=attr2_hi_packed (saved r9), r3=attr2_lo_packed/flip_mode (saved r10). "
        "Guards: sprite count >= 0x80 or sub_type==0x20 -> early exit. "
        "16-case switchD on flip_mode adjusts x/y by +-4/8/0x10/0x20 pixels per case. "
        "Calls write_oam_entry_attr_pairs then strb-increments two count bytes. "
        "Side effects: gPrng sprite table attr fields written; two count bytes incremented. "
        "Constants: MAX_SPRITE_COUNT=0x80, SPRITE_COUNT_OFFSET=0x400, "
        "X_MASK=0x1ff, TILE_STRIDE_OFFSET=0x401."),

    # 2026-05-09: BATCH-28 落地 (campaign-28, topo=626..647)
    ("FUN_080bf2d0", "draw_number_digits_to_oam",
        "将十进制数值分解为各位数字并写入 OAM 影子缓冲区 (用于 LP/数值显示). "
        "r1 = number (待渲染的十进制整数, [0..8000] LP 值); r2 = player_flag {0,1} (保存到 r8). "
        "Y 位置: gBannerState[+0x14] * 8 + 0x70 = 屏幕 Y 坐标. "
        "X 起始: 基于 gBannerState[+0x14] * 8 + 0x70 区间 (r6), 每位数字向左偏移 0xc 像素. "
        "digit tile = 0x204 + digit * 2 (tile 基址 0x81*4=0x204 起, 每个数字占 2 tile). "
        "flag 字段: 读 DAT_0x0201e2a0[+0x4] bit0 XOR 1 -> 若非零则 r1 |= 0x80 (palette 或 flip bit). "
        "循环: r5 % 10 = 当前最低位数字 -> 写入 OAM; r5 /= 10; 重复直到 r5 == 0. "
        "最后再写一次末位确保 0 不被跳过. 调用 write_oam_entry_from_packed_args (已命名) 写入 OAM. "
        "唯一 caller: play_ui_effect_0e (0x080bf394, vram/scene_duel_field/duel_field). "
        "Constants: gBannerState (0x0201fec0)[+0x14]: Y/X 位置参数 byte; "
        "DAT_080bf368 = gBannerState; DAT_080bf36c = 0x0201e2a0 (struct); "
        "0x204 = 0x81*4: digit tile 基址; 0xc: 每个数字 X 间距; 0x70: Y 基准偏移; "
        "0x80: palette/flip flag bit; 0xa: 十进制 mod/div 基数; "
        "0x202: 某 OAM attr 常量 (DAT_080bf390)."),
    ("FUN_080fa4d8", "return_void_noop",
        "发布版空操作占位函数. 函数体仅一条 bx lr 指令, 不接受任何参数, 无任何副作用, 无返回值. "
        "在所有 4 个调用点均紧跟在 suppress_display_output (0x080fa4cc) 之后, "
        "两次 bl 连续出现于 play_ui_effect_2f (0x080c1e9c), "
        "FUN_080eda30 (sio), FUN_080f4c14 (dma/sys/display), FUN_080f7708 (display/palette). "
        "调用前未见 r0..r3 专门设置, 属于 Type B 零参数页面处理器占位 "
        "(区别于 suppress_assert_report 0x080fa4dc 的 4 参数消音器). "
        "与地址相邻的 return_void_handler (0x080fa4d4) 及 suppress_assert_report (0x080fa4dc) 构成同簇."),
    ("FUN_080fa4cc", "suppress_display_output",
        "发布版 4 参数空输出函数. 函数体: push {r0,r1,r2,r3} 将所有 APCS 入参压栈, "
        "add sp,#0x10 立即弹出, bx lr 返回. 等效于接收 4 个参数后立即丢弃, 无任何输出或副作用. "
        "调用方包括 banlist/settings 初始化 (0x08017a24, r0=ptr, r1=pixel_offset), "
        "play_ui_effect_2f (0x080c1e9c, r0=ptr, r3=context), "
        "FUN_080eb4d4 / FUN_080ed550 (游戏各模块循环内 r0=ptr 传入). "
        "用于在 release build 中消音调试输出 (类似 printf/log stub). "
        "与 suppress_assert_report (0x080fa4dc) 同为发布版 noop 族."),
    ("FUN_080f5928", "start_blend_fade_with_evy",
        "启动 alpha 混合淡入/淡出序列并推进一步. r0 = delta (带符号偏移量, 每帧步进值). "
        "函数入口: 写入 BLDCNT = 0x3fbf (所有层参与 B 混合模式), 设置混合效果启动条件. "
        "读取 gPrng+0x200 处的 blend_step 字节 (6-bit 字段 [5:0]), "
        "将 (step + r0) & 0x3f 写回该字节. "
        "若新 step 超过 0x1e (30), 则截断到 0x1f (31, 最大值). "
        "同时将 gPrng+0x200 处的 6-bit step 值写入 BLDY (0x04000054) 作为 EVY 系数. "
        "返回 1 = 序列已完成 (step >= 0x1f), 0 = 序列进行中. "
        "与 advance_blend_evy_step (0x080f59a0) 为同 caller 兄弟对: "
        "前者负责设置 BLDCNT 并启动, 后者负责单独推进 step 不写 BLDCNT. "
        "Constants: BLDCNT (0x04000050): blend control register; "
        "DAT_080f598c = 0x3fbf: BLDCNT 初始化值 (所有 BG + OBJ 均参与 B-blend); "
        "BLDY (0x04000054): blend Y coefficient (EVY); "
        "gPrng+0x200: blend_step 字节 (6-bit [5:0] = EVY 值); "
        "0x1e (30): 完成阈值; 0x1f (31): 截断上界; 0x3f: 6-bit 掩码."),
    ("FUN_080f59a0", "advance_blend_evy_step",
        "推进 alpha 混合淡变步骤, 不重设 BLDCNT. r0 = delta (目标 EVY 值方向的偏移量). "
        "读取 gPrng+0x200 处的 blend_step 字节 (6-bit 字段 [5:0]), 若当前 step > delta: "
        "  将 step 减少到 (step - delta) & 0x3f, 写回字节; 写入 BLDY = step. "
        "否则 (step <= delta): 将 step 清零 ([5:0]=0), 调用 disable_blend_and_clear_step 关闭混合并重置, "
        "  返回 1 = 序列结束. "
        "与 start_blend_fade_with_evy (0x080f5928) 为兄弟对: 前者设 BLDCNT 并首次推进, "
        "本函数仅推进 step 不写 BLDCNT (适用于已启动后的逐帧 tick). "
        "两个函数共享相同 caller 对 (0x0802d4bc, FUN_080bd0a8). "
        "Constants: gPrng+0x200: blend_step 字节 (6-bit [5:0]); "
        "BLDY (0x04000054): EVY 混合系数寄存器; "
        "0x3f: 6-bit 掩码; 0x40: 掩码基数 (~0x40 清第 6 位); "
        "disable_blend_and_clear_step: 混合关闭函数."),
    ("FUN_080f6074", "write_obj_affine_scale_diagonal",
        "将 OBJ affine 矩阵写入 OAM 影子缓冲区 (仅对角缩放, 无旋转). "
        "r0 低 21 位经 lsls/lsrs 提取后 >>11 = OBJ slot 索引; r1 = PA (X 轴缩放 Q8); r2 = PD (Y 轴缩放 Q8). "
        "通过 gPrng+0x1bc 取得 OBJ 影子缓冲区基址, 加 slot_idx*8 字节得到目标 affine entry. "
        "写入: [entry+0x6]=r1 (PA), [entry+0xe]=0 (PB=0), [entry+0x16]=0 (PC=0), [entry+0x1e]=r2 (PD). "
        "PB=PC=0 意味着无旋转, 仅 X/Y 独立缩放. "
        "对应 GBA OAM affine 格式: 每 8 字节一个 halfword 参数, 跨 4 个 OAM 连续 entry. "
        "2 个 caller: FUN_080f6adc (indeg=1, scene_duel_puzzle 解谜界面 OBJ scale 设置), "
        "FUN_080f6ec8 (scene_pack, pack 卡牌 OBJ scale 设置). "
        "Constants: gPrng+0x1bc: OBJ 影子缓冲区链表头指针 (0xde<<1=0x1bc); "
        "PA (offset+0x6), PB (offset+0xe), PC (offset+0x16), PD (offset+0x1e): GBA OAM affine 参数."),
    ("FUN_080f609c", "write_obj_affine_rot_scale",
        "计算旋转+缩放 OBJ affine 矩阵并写入 OAM 影子缓冲区. "
        "r0: u8 slot_index [0..N-1], ldrb 传入; 入口 lsls #0x10 + lsrs #0xb = slot*32 (entry 步长 0x20). "
        "r1 = scale 系数 Q8; r2 = 旋转角度索引 [0..127] (128 步正弦表). "
        "函数从 rom_sin_table_q8 (128-entry Q8 正弦表) 查 3 个相位: "
        "sin(r2 & 0x7f) -> PA 基值; sin((r2+0x20) & 0x7f) -> PB 基值; sin((r2+0x40) & 0x7f) -> PD 基值. "
        "各乘以 r1 (scale) 后算术右移 8 位得到 Q8 affine 系数. strh 写入 entry 偏移 0x6/0xe/0x16/0x1e. "
        "PC 取与 PB 对称位置. "
        "与 write_obj_affine_scale_diagonal (0x080f6074) 为兄弟对: 本函数带旋转, 后者无旋转. "
        "5 个 caller 均属 scene_pack 包裹/卡牌 zoom 动画流. "
        "Constants: gPrng+0x1bc (0xde<<1): OBJ 影子缓冲区基址指针; "
        "rom_sin_table_q8 (0x09e5f8f0): 128-entry Q8 正弦表 (已命名); "
        "0x7f: 角度 mod 128 掩码; 0x20: 四分之一周期偏移 (128/4=32=0x20); "
        "PA/PB/PC/PD 偏移: 0x6/0xe/0x16/0x1e (GBA OAM affine 格式)."),
    ("FUN_080f6adc", "write_pack_obj_attr_by_dir",
        "根据方向码调整屏幕坐标并将 OBJ sprite 写入 OAM 影子缓冲区 (pack/puzzle 场景用). "
        "r0 = 打包坐标 (高 16 bit = y, 低 16 bit = x); r1 低 16 = dir_code (方向/角度离散码); "
        "r2 低 16 = 附加参数 (保存栈上备用); r3 = affine 参数. "
        "函数首先验证 gPrng+0x1bc 对应 slot 的 availability 字节 (0x80 = 满, 直接退出); "
        "若可用则根据 dir_code (0x0/0x40/0x80/0xc0/0x4040/0x8000/0x8080/0x80c0 等离散值) "
        "对 (x, y) 各减 4/8/16/32 像素以居中对齐不同旋转角度下的 sprite. "
        "随后写入 OAM attr0 (y & 0xff | 0x300 affine 双尺寸标志), attr1 (x & 0x1ff | affine_idx<<9), attr2 (从 slot 复制). "
        "调用 write_obj_affine_scale_diagonal (0x080f6074) 写入缩放矩阵. "
        "最后递增两个使用计数字节 (buf_base+r8 和 buf_base+0x401). "
        "唯一 caller: FUN_080bcc6c (blend/window/display/palette, banner 场景 OBJ 状态机). "
        "Constants: gPrng+0x1bc (0xde<<1): OBJ 影子缓冲区基址; "
        "gPrng+0x400+slot: slot 可用标志 (0x80=满); "
        "DAT_080f6b5c = 0xfffffe00: attr1 X 坐标掩码 (~0x1ff); "
        "DAT_080f6cc8 = 0x401: slot 使用计数偏移; 0xc0<<2 = 0x300: OBJ affine double-size 标志位."),
    ("FUN_080f68ec", "write_pack_obj_attr_by_dir_split",
        "根据方向码调整坐标并写入 OBJ sprite OAM 属性 (pack 场景, r3 高低 16 分别处理变体). "
        "与 write_pack_obj_attr_by_dir (0x080f6adc) 结构相同: prologue / 方向码 dispatch / OAM attr0-2 写入 / affine 子调用. "
        "关键差异: 本函数将 r3 拆为高 16 (lsrs r5,r3,#0x10 @ 080f6924 -> scale_hi) 和低 16 (r3 直接用), "
        "0x080f6adc 取 r3 整体. 5 个 caller 均属 pack 场景初始化/状态机: "
        "FUN_080bd0a8 (display/palette/frame_counter), FUN_080bd3f4 (display/palette/frame_counter), "
        "FUN_080d46a8 (untag), FUN_080d5470 (palette/scene_pack), FUN_080d933c (palette/pack). "
        "Constants: gPrng+0x1bc (0xde<<1): OBJ 影子缓冲区基址; "
        "gPrng+0x400+slot: slot 可用标志 (0x80=满); "
        "DAT_080f696c = 0xfffffe00: attr1 X 坐标掩码; "
        "0x4040/0x8000/0x8080/0x80c0: 方向码枚举; "
        "0x300 (0xc0<<2): OBJ affine double-size 标志位."),
    ("FUN_080f6ccc", "write_pack_obj_attr_by_dir_stacked",
        "根据方向码调整坐标并写入 OBJ sprite OAM 属性 (pack 场景, r3 双 16-bit 均入栈变体). "
        "与 write_pack_obj_attr_by_dir (0x080f6adc) / write_pack_obj_attr_by_dir_split (0x080f68ec) 三函数对称结构. "
        "本变体特点: sub sp,#0x8 (额外 8 字节栈帧, 其他变体为 4 字节); "
        "r3 的高低 16 位分别保存到 sp+0 和 sp+4 (两个独立栈参数槽): "
        "r3[31:16]=affine_ctrl (0x8000|counter*8), r3[15:0]=scale_ramp [0..0x20]. "
        "方向码 dispatch 与前两变体相同 (0x0/0x40/0x80/0xc0/0x4040/0x8000/0x8080/0x80c0); "
        "像素偏移调整 (4/8/16/32px) 也相同. 结束时同样写 attr0/attr1/attr2 并调用 affine 写入. "
        "6 个 caller: play_ui_effect_21 (场景通用 UI), play_card_zoom_in (卡牌 zoom 动画), "
        "FUN_080c4edc (card_ids/duel_field), FUN_080d0150 (scene_pack), FUN_080d71f4 (scene_pack). "
        "Constants: gPrng+0x1bc (0xde<<1): OBJ 缓冲区基址; "
        "DAT_080f6d50 = 0xfffffe00: attr1 X 坐标掩码; "
        "DAT_080f6d58 = 0x4040: 方向码枚举之一; 0xc0<<2=0x300: OBJ affine 双尺寸标志."),
    ("FUN_080bcc6c", "dispatch_banner_anim_tick_by_state",
        "banner 动画帧状态机 tick 分派器. 读取 gBannerState[+0x11] (byte, 状态索引 [0..8]), "
        "超出范围则跳转到默认 handler (LAB_080bd09c). 在范围内则以 state*4 查找跳转表 "
        "(switchD_080bcc8e__switchdataD_080bcc98, 9 个 entry: 0x080bccbc..0x080bd080), "
        "通过 bx 跳入对应 handler. 每个 case 处理一种 banner 动画阶段 (初始化/过渡/显示/退出等). "
        "case 0 (0x080bccbc): 进一步判断 r2 (= gBannerState 基址) [+0x1/+0x2] 字段决定子 case. "
        "3 个 caller 均属相同 banner/display/palette/vram 场景 (FUN_080bd0a8, FUN_080bd3f4, FUN_080bd660), "
        "均为 banner 状态机的外层 tick 循环调用本函数推进一帧. "
        "Constants: gBannerState (0x0201fec0): banner 全局状态结构基址; "
        "gBannerState[+0x11]: 主状态索引 [0..8]; 0x8 = 最大合法状态; "
        "switchD_080bcc8e__switchdataD_080bcc98: 9-entry 跳转表; "
        "r7 = 0x18 / r5 = 0x30: 参数常量 (传递给 sub-handler)."),
    ("FUN_080cc694", "compute_duel_zone_dir_for_player",
        "计算决斗场地指定玩家的区域方向状态码. r0 = player_side [1..2] (1=玩家1, 2=玩家2). "
        "通过 gP1LifePoints 表 (stride=0x868) 索引当前玩家的 zone 子结构, 读取 zone_type 字段 "
        "(位于 player_struct + 0x2c + team_flag*0x868). 若 zone_type == 8 (特殊类型): "
        "直接按 player_side 返回 1 (r6==1) 或 2 (r6==2). "
        "否则扫描 gPrng+0x23f (gPrng+0x23f..0x23f+count, byte 数组), 统计值为 1 的项数 (dir 加减). "
        "再扫描 gPrng+0x241 (gPrng+0x241..+count), 同样统计. "
        "将 count 值与 gPrng+0x240 bit0<<7 组合形成方向因子, "
        "若结果 > 1 -> 返回 1 (正向); < -1 -> 返回 2 (反向); == 0 则检查 gPrng+0x240 bit6 "
        "决定返回 0 (停止) 或 3 (中性). "
        "3 个 caller (FUN_080bd0a8, FUN_080bd3f4, FUN_080bd660) 均为 banner/display 场景帧 tick 函数. "
        "Constants: gP1LifePoints (0x0201c4e0): 玩家结构数组基址 (stride=0x868); "
        "0x868: 玩家结构步长; 0x2c: zone_info 偏移; "
        "gPrng+0x23f (DAT=0x23f): zone byte 数组起点; gPrng+0x241 (DAT=0x241): 第二数组起点; "
        "gPrng+0x240: 方向标志字节; "
        "返回值: 0=停止/中性待定, 1=正向, 2=反向, 3=中性激活."),
    ("FUN_080bd0a8", "dispatch_banner_scene_tick_by_state",
        "banner/pack 场景主帧状态机 tick 分派器. 读取 gBannerState[+0x10] (byte, 主场景状态索引 [0..8]), "
        "超出范围则跳转 switchD_080bd0c8__caseD_7 (默认处理). "
        "在范围内则以 state*4 查找 9-entry 跳转表 "
        "(switchD_080bd0c8__switchdataD_080bd0d4, entry: 0x080bd0f8..0x080bd3ac), "
        "通过 bx 跳入对应 case handler. "
        "与 dispatch_banner_anim_tick_by_state (0x080bcc6c) 对称: "
        "0x080bcc6c 读 gBannerState[+0x11] (sub-state), 本函数读 gBannerState[+0x10] (main-state). "
        "两函数配合构成双层状态机. "
        "入口: .hword 0x4647=mov r7,r8; movs r0,#0x18 -> r8=0x18; movs r5,#0x30 初始化参数常量. "
        "唯一 caller: play_ui_effect (0x0801ef94) - 游戏顶层 UI 效果循环调用本函数推进每帧. "
        "case 0 (0x080bd0f8): 执行 copy_bytes_by_halfword 复制数据, 读取场景 type 字段 gPrng+0x3d0. "
        "Constants: gBannerState (0x0201fec0): banner 全局状态结构基址; "
        "gBannerState[+0x10]: 主场景状态索引 [0..8]; "
        "0x18 / 0x30: case handler 初始参数常量 (r8 / r5); "
        "switchD_080bd0c8__switchdataD_080bd0d4: 9-entry 跳转表."),
    ("FUN_080c678c", "update_zone_oam_card_count_tag",
        "根据玩家场地区域卡牌数量更新 OAM entry 中的 tag/count 字段. "
        "无 APCS 参数 (r0 入口立即被内部 ldr 覆盖). "
        "读取 0x02023130 + 0x84*4 = 0x02023340 处的 OAM 区域 byte (r6=ldrb at offset). "
        "提取 bit[6:0] 检查是否 == 0xb (zone_type_deck 或特定区域代码); 若否跳转 (不操作). "
        "若是 (zone_type==0xb): 读 gP1LifePoints 基址, 用 player_id (0 or 1) * 0x868 + 0xc "
        "索引玩家 zone 牌数子结构; 读 [r5+0]=当前区域卡牌数 (0..6 范围); 若 > 6 则退出; "
        "若 == 0: 将 bit7 of player_id 构成高位 attr0 组合 (player_flag | 0x0b), strh 写回 OAM entry. "
        "调用 resolve_zone_data_ptr_by_oam_word: 将 OAM word 解析为 zone_data 指针, "
        "确认 bit13==0 后再次更新 attr (lsls r1,r4,#7 | 0xb | (count-1)<<8) strh 写回 OAM entry. "
        "3 个 caller: FUN_0801ec9c (card_frame/duel_field), "
        "FUN_080bede4 (palette/vram/duel_field), play_ui_effect_10. "
        "Constants: DAT_0x02023130: OAM 影子缓冲区 (duel_field 区域 OAM 基址); "
        "0x84*4=0x210: OAM entry 索引偏移; "
        "gP1LifePoints (0x0201c4e0): 玩家结构基址; 0x868: 玩家 stride; 0xc: zone 子结构偏移; "
        "0xb: zone_type 枚举 (卡组/特定决斗区域); [0..6]: 区域最大卡牌数."),
    ("FUN_080f64dc", "write_obj_attr_256color_affine",
        "将 OBJ sprite 属性写入 OAM 影子缓冲区 (256 色调色板模式 + affine 旋转缩放). "
        "r0 低 16 bit = x [0..239], 高 16 bit = y [0..159] (packed 屏幕坐标); "
        "r1 = obj_size_attr 字节 [0..0xff] (bit7 映射 attr1 size 字段, callsite=0x80 表 64x64); "
        "r2 低 16 bit = tile_idx [0..1023]; r3 = affine_slot_idx [0..31] (attr1[13:9] affine 参数组). "
        "通过 gPrng+0x1bc 取 OBJ 影子缓冲区基址, 以 slot_idx 字节 (gPrng+0x400 区域) 定位 entry. "
        "若 slot 不可用 (0x80), 直接返回. 可用时: "
        "attr0 = y[7:0] | (r1 & 0xff00) | 0x2000 (bit13=256色模式); "
        "attr1 = x[8:0] | r1_size_flag | affine_slot_idx; attr2 = r6 (tile_idx); "
        "写入 entry 偏移 0x0/0x2/0x4. 递增 entry 的使用计数字节 (entry+0x400). "
        "与 write_obj_attr_packed (0x080f61e4) 和 write_obj_attr_with_priority (0x080f6578) 同簇. "
        "本函数在 attr0 ORs 0x2000 (256-color), 其他变体使用 16-color 或不同 mode 位. "
        "唯一 caller: play_ui_effect_10 (0x080c25ac, card_ids/duel_field, "
        "作为 effect 10 的 OBJ 写入). "
        "Constants: gPrng+0x1bc (0xde<<1): OBJ 影子缓冲区链表头; "
        "gPrng+0x400+slot: slot 使用计数 (0x80=满); "
        "DAT_080f656c = 0xfffffe00: X 坐标 attr1 掩码 (~0x1ff); "
        "0x2000 = bit13: OBJ 256-color palette 模式标志."),
    # --- batch #29 (campaign-29) ---
    ("FUN_0803b3a8", "get_zone_slot_entity_ref_by_type",
        "根据 zone_type_code (r1) 通过 switch-dispatch 读取指定区域格的 entity_ref 字段, 并提取关键位段后返回. "
        "Switch 覆盖 type_code 0xb..0xf (5 cases) 和 default (r1+r2<=10 / >10 两路), "
        "与已命名兄弟 get_zone_slot_card_ref_by_type (0x0803b4b0) 结构完全对称 -- "
        "后者返回 [slot+0], 本函数同样返回 [slot+0] 但经 lsls/lsrs 提取 bits[22..16]<<1 | bit[13] (entity/player reference bits). "
        "入口: r3=player_id (bit0), r4=zone_type_code, r2=slot_idx; "
        "通过 gDuelFieldSlots 多基地址 (0x0201c510/0x0201c600/0x0201c740/0x0201c880/0x0201c8f8/0x0201cab0/0x0201bc54) 计算 slot 指针. "
        "被 11 个高层牌局函数调用, 是 zone slot entity 读取的公共出口. "
        "Constants: player_stride=0x868, zone_0b=0x0201c600, zone_0c=0x0201c880, "
        "zone_0d=0x0201c740, zone_0e=0x0201c8f8, zone_0f=0x0201cab0, default_extended=0x0201bc54."),
    ("FUN_080c1f10", "tick_pack_banner_3d_state_machine",
        "pack banner 3D 动画状态机, 每帧由 play_ui_effect_3d (唯一 caller) 调用. "
        "读 gBannerState[+0x11] (u8 phase [0..6]) 通过 switch-dispatch 驱动 7 个子状态; phase 超出 6 则返回 0 (done). "
        "case 0: 拷贝调色板到 0x05000260 via copy_bytes_by_halfword, "
        "根据 [gPrng+0x6c2c] bit[4:0]*3<<10 写 tile_2d_row_copy 到 VRAM 0x06014000, "
        "调 disable_blend_and_clear_step, 写 WINOUT=0x1f3f/WIN1H=0/WININ=0xff, 读 DISPCNT 置 bit15 (0x8000) 后写回. "
        "case 1: 从 BLDY 读/写递增 gBannerState[+0x12] 最多 7 次后 phase++. "
        "case 2/3: 调 blend_palette_entry_toward_target 做调色板渐变, 循环写 OAM 3 entries (r6=0..2, tile_id 0x48c0/0x40c0), 计时 0xf 帧后 phase++. "
        "case 4: 循环写 OAM 3 entries (不调 blend), 计时 0x1f 帧后 phase++. "
        "case 5: 写 BLDY = 8 - gBannerState[+0x12], 递增计时最多 7 后 phase++. "
        "case 6: 调 disable_blend_and_clear_step, 读 DISPCNT ands 0x7fff, 写回, phase++. "
        "返回 1=进行中 / 0=完成. "
        "Constants: gBannerState=0x0201fec0, BLDY=0x04000054, WINOUT=0x0400004a, DISPCNT=0x04000000, "
        "tile_vram=0x06014000, pal_src=0x05000260, gPrng_offset=0x6c2c, OAM_tile_a=0x48c0, OAM_tile_b=0x40c0."),
    ("FUN_080c21a0", "tick_pack_banner_3d_state_machine_alt",
        "pack banner 3D 动画状态机变体, 与 tick_pack_banner_3d_state_machine (0x080c1f10) 共享同一 caller (play_ui_effect_3d) "
        "和相同 gBannerState 相位结构 (7 states, [+0x11] phase / [+0x12] sub-tick), "
        "但使用不同的 ROM 资源基地址: 调色板来自 0x0991767c (vs 0x09912e3c) / 0x0991be9c (vs 0x09912e5c). "
        "case 0 同样拷贝调色板 + tile_2d_row_copy + disable_blend_and_clear_step + 写 WINOUT/WIN1H/WININ/DISPCNT. "
        "case 1: 读 BLDY 写 gBannerState[+0x12] 递增计时. "
        "case 2: 调 blend_palette_entry_toward_target + OAM 3 entries 循环 (tile 0x48c0/0x40c0). "
        "case 3: blend + OAM loop. case 4: 纯 OAM loop 无 blend. "
        "case 5: BLDY = 8 - step 淡出. case 6: disable_blend_and_clear_step + DISPCNT &= ~0x8000. "
        "返回 1=进行中 / 0=完成. "
        "Constants: gBannerState=0x0201fec0, BLDY=0x04000054, WINOUT=0x0400004a, "
        "OAM_tile_a=0x48c0, OAM_tile_b=0x40c0, pal_src_a=0x0991767c, pal_src_b=0x0991be9c."),
    ("FUN_080f67f4", "write_oam_entry_with_slot_check",
        "向 OAM 写入一个精灵条目, 但仅当 gPrng 指向的 slot 尚未被标记为 '已写' 时才写入. "
        "入口打包参数 r0 low16=sprite_x, r0 hi16=sprite_y, r1=OAM_attr1, r2=OAM_attr0_low8 (颜色模式等), r3=OAM_attr2 (tile/priority). "
        "内部流程: 从 gPrng+0x1bc (=gPrng+0xde*2) 读出 u8 slot_id; "
        "若 slot_id==0x80 则跳过写入 (slot 未激活); "
        "否则以 slot_id*8 为偏移计算 OAM entry 地址, 将 attr0/attr1/attr2 分别 strh 到 [slot+0]/[slot+2]/[slot+4], "
        "再将 slot_id++ 写回 gPrng+slot*8 (即 OAM 写入计数+1). "
        "被 10 个调用者使用, 是区域动画 OAM 写入的核心出口. "
        "Constants: gPrng=0x03000040, slot_offset=0xde*2=0x1bc, sentinel=0x80, "
        "OAM_entry_size=8, attr0_mask=0xfffffe00, attr1_mask=0x000001ff."),
    ("FUN_080c124c", "render_card_zoom_oam_sprite_grid",
        "为卡牌缩放/展示 UI 效果计算并写入 OAM sprite 网格. "
        "由 play_ui_effect_25 和 play_ui_effect_23 调用, 处理 pack UI 场景中卡牌放大动画的 OAM 布局. "
        "入口: r0=player_side / r1=base_y_or_param / r2=tile_ptr_base / r3=packed (low16=clamp_max [0..0x3e7], hi16=sign_flag). "
        "计算动画帧所需的 sprite 网格尺寸 (通过 __divsi3 / __modsi3 反复计算行列数), "
        "对每个子精灵调用 write_oam_entry_from_packed_args 及 write_oam_entry_with_slot_check (FUN_080f67f4) 完成 OAM 写入. "
        "关键常量: clamp_max=0x3e7 (最大列数), step=10 (% 10 折行), OAM tile pair 0x061a/0x0215 (pack banner OAM 属性). "
        "函数体含 __divsi3/__modsi3 调用, 是计算量较重的 OAM layout 函数."),
    ("FUN_080c2990", "write_zone_pair_oam_with_coords",
        "解包两个 zone OAM 描述字, 分别调用 resolve_zone_oam_base_coords_by_type 获取各自基础坐标, "
        "再计算相对位移后调用 write_oam_entry_with_slot_check (FUN_080f67f4) 写入 OAM. "
        "函数处理'一对 zone 指示器'的 OAM 布局: zone0 和 zone1 各有 player/zone_type/sub_idx 三字段 (分别从 r0/r1/r2 解包). "
        "坐标后处理: 双向各加 4, 再根据 gDuelActivation[+4] 与 player_id 比较结果决定 y 偏移 +24 或 -24 "
        "(配合 OAM attr 0x2488/0x248c 选择 flip 模式). "
        "被 play_ui_effect_0b 和 FUN_080c8c58 调用, 是 duel zone 动画配对高亮的核心写入函数. "
        "Constants: gDuelActivation=0x0201e2a0, OAM_attr_normal=0x2488, OAM_attr_flip=0x248c, "
        "OAM_y_offset=0x18, coord_x_pad=4."),
    ("FUN_080bdbb4", "tick_pack_banner_state_machine_b",
        "pack banner 子状态机 B, 驱动 pack banner 淡入/OAM 动画序列. "
        "读 gBannerState[+0x10] (u8 phase [0..4]) 通过 switch-dispatch 5 cases 执行. "
        "case 0: 从 [gPrng+0x6c2c] 读出 player bit[4:0] 计算 tile VRAM 地址 0x06014000 偏移, "
        "copy_bytes_by_halfword 拷贝调色板 (src 0x098c9064 to 0x05000260, 0x20 halfwords), "
        "tile_2d_row_copy 写 VRAM, disable_blend_and_clear_step, 写 BLDCNT=0xbf40 / BLDALPHA=0, "
        "清 gBannerState[+0x11], phase++. "
        "case 1: 直接 phase++. "
        "case 2: blend_palette_entry_toward_target (淡入, step=[+0x11]*2, max=0x20), "
        "OAM 2 entries loop (tile 0x40c0, x=0x4c, y 每次+0x40), 计时 0x1f 帧后 phase++. "
        "case 3: 计时后触发 sync_state_and_init_sprite (code=0x23) + phase++. "
        "case 4: 直接 phase++. "
        "默认 (phase>4): disable_blend_and_clear_step 后返回 0. "
        "返回 1=进行中 / 0=完成. "
        "Constants: gBannerState=0x0201fec0, BLDCNT=0x04000050, BLDALPHA=0x04000052, "
        "pal_src=0x098c9064, pal_dst=0x05000260, tile_vram=0x06014000, OAM_tile=0x40c0, OAM_attr=0xc0c0, x_base=0x4c."),
    ("FUN_080bda7c", "tick_pack_banner_state_machine_a",
        "pack banner 子状态机 A, 与 tick_pack_banner_state_machine_b (0x080bdbb4) 结构完全对称, "
        "同为 play_ui_effect_0b 唯一调用路径的两个变体之一. "
        "使用不同 ROM palette 地址: case 0 copy_bytes_by_halfword src=0x098cc0a4 (vs B 的 0x098c9064); "
        "case 2 blend 源=0x098c9064 (两者共用). "
        "switch 覆盖 phase [0..4]: "
        "case 0 = palette+tile init+BLDCNT/BLDALPHA+phase++; "
        "case 1 = 直接 phase++; "
        "case 2 = blend + OAM 2 entries (tile 0x40c0, x=0x4c, y 每次+0x40); "
        "case 3 = 计时后 gBannerState[+0x10]++ (32+1=0x21 帧触发 sync_state_and_init_sprite); "
        "case 4 = 直接 phase++. default = disable_blend + return 0. "
        "Constants: gBannerState=0x0201fec0, BLDCNT=0x04000050, BLDALPHA=0x04000052, "
        "pal_init_src=0x098cc0a4, pal_blend_src=0x098c9064, pal_dst=0x05000260, "
        "tile_vram=0x06014000, OAM_tile=0x40c0, x_base=0x4c."),
    ("FUN_080c6a20", "write_zone_slot_oam_descriptor",
        "根据 zone_type_code 更新 gDuelFieldCtx (0x02023130) 中对应 slot 的 OAM 描述字段, "
        "并调用 render_duel_field_zone_info 重绘区域信息. "
        "入口: r0=player_bit (bit0 用于 player) [0..1], r1=zone_type_code [0..0xf]; "
        "r2 由内部 ldr DAT 加载 gDuelFieldCtx 基址, 非外部参数. "
        "switch 覆盖 zone_type [0..0xf]: "
        "case 0..4 (type 0..4) -> r5=0, r4=zone_type; "
        "case 5..9 (type 5..9) -> r5=5, r4=zone_type-5; "
        "case 0xa (type 0xa) -> r5=zone_type, r4=0; "
        "case 0xb (type 0xb) -> 额外读取 gDuelFieldCtx[+0x4c+player*2] 更新 LP counter halfword, 再调 refresh_player_field_slot_tiles. "
        "default 路径: 从 r8 读 player_bit, 拼接 player/zone/sub_idx 位字段写入 gDuelFieldCtx[+0x84*4=0x210] halfword, "
        "再调 render_duel_field_zone_info (r0=packed, r1=zone_type, r2=lp_count). "
        "Constants: gDuelFieldCtx=0x02023130, slot_lp_offset=0x4c, zone_flag_offset=0x84*4=0x210."),
    ("FUN_080c4ca0", "clear_ui_effect_state_flags",
        "清除 gUIEffectState 中两个标志位, 供 dispatch_ui_effect_by_card_type (0x080c4350) "
        "在判定卡牌类型超出正常范围后调用以重置 UI 效果状态. "
        "操作: (1) 读 r4+0x19 字节, ands ~0x2 (bit1 清零), 写回; "
        "(2) 读 [gP1LifePoints+0x215] 字节 (=gDuelFieldCtx+0x215 偏移), ands ~0x5 (bit0/bit2 清零), 写回; "
        "(3) 返回 r0=0. "
        "r4 为函数外部保存的 gUIEffectState 基址 (callee-save, 由调用者在 prologue 通过 ldr r4, DAT = gUIEffectState 加载). "
        "被 dispatch_ui_effect_by_card_type 在卡牌类型>4 时调用. "
        "Constants: gUIEffectState=0x02023110, flag_offset_a=0x19, flag_bit_a=0x2, "
        "gDuelFieldCtx=0x02023130, field_offset_b=0x215, flag_bit_b=0x5."),
    ("FUN_080c4350", "dispatch_ui_effect_by_card_type",
        "读取 gUIEffectState[+0x4] halfword (当前卡牌 slot_ref), "
        "调用 ensure_card_id_cache_entry 确保卡牌信息已缓存, "
        "再读 gUIEffectState[+0x6] halfword 作为第二个卡牌引用. "
        "若 [+0x0] 类型字段 > 4, 调用 clear_ui_effect_state_flags 后返回; "
        "否则以类型值 [0..4] 为 key 通过 switch-dispatch 分发到 5 个卡牌展示子状态机 "
        "(地址表 PTR_DAT_080c4390: case 0..4 分别指向 0x080c43a4/0x080c462c/0x080c48a2/0x080c4a24/0x080c4c58). "
        "返回值转发子状态机 r0: 0=完成, 1=继续/进行中. "
        "被 play_ui_effect (0x0801ef94) 作为某一 UI effect case 调用, 是卡牌展示动画的顶层 dispatcher. "
        "Constants: gUIEffectState=0x02023110, card_type_max=4, dispatch_table=PTR_DAT_080c4390."),
    ("FUN_080c4edc", "run_ui_effect_card_pair_state_machine",
        "以 gUIEffectState[0] card_type [0..4] 为 key 进行 switch-dispatch, "
        "分别驱动 5 个卡牌配对展示子状态机. "
        "入口: r1=gUIEffectState[0x19] u8 flag (由 caller 0x0801f0a6 ldrb 传入, mov r9,r1 保存); "
        "r0 由内部 ldr DAT_080c4f04 覆盖为 0x02023114 (gUIEffectState+4); "
        "r9-4 = gUIEffectState 基址, 读 [0] halfword 作 switch key. "
        "返回 0=完成/1=继续, 转发子状态机 r0. "
        "case 0: 解包 gUIEffectState+4 packed word (player/zone_type/sub_idx), "
        "调用 resolve_zone_oam_base_coords_by_type 两次获取两张卡的坐标, "
        "再调用 load_card_list_small_image x2 加载缩略图, 最后 build_slot_activation_mask_for_player. "
        "case 1..4: 类似模式, 各自处理不同的卡牌对或坐标组合. "
        "被 play_ui_effect (0x0801ef94) 作为 UI effect 的子状态机入口调用. "
        "Constants: gUIEffectState=0x02023110, gUIEffectState_card_ref1=0x02023114, "
        "gUIEffectState_card_ref2=0x02023118, card_type_max=4."),
    ("FUN_080bd660", "tick_duel_puzzle_banner_state_machine",
        "驱动 duel puzzle (场景 scene_duel_puzzle) 的 banner 状态机, 每帧由 play_ui_effect (0x0801ef94) 调用. "
        "读 gBannerState[+0x10] (u8 phase [0..8]) 驱动 switch 9 cases. "
        "case 0: 置 gDuelFieldCtx[+0x21e] bit0, 从 [gPrng+0x6c2c] 读 bit[4:0] 计算 player side, "
        "以 side*3<<11 得 tile 偏移加 ROM 基址 (0x098f6104), "
        "copy_bytes_by_halfword 拷贝调色板 (src 0x098f60e4 to 0x05000260, 0x20 halfwords), "
        "tile_2d_row_copy 写 VRAM 0x06014000 (0x18 tiles x 8 rows), phase++. "
        "case 1 (sin 动画): 每帧从 rom_sin_table_q8 读 OAM y 坐标 (sin[gBannerState[+0x12]]*0x70/256), "
        "循环写 3 OAM entries (tile 0xc0 attr), 计时 0x20 帧 phase++. "
        "case 2..7: 各阶段推进 OAM 动画 (垂直摆动 / 写 gBannerState[+0x8]). "
        "case 8: 切换下一动画 via sync_state_and_init_sprite + compute_duel_zone_dir_for_player 判 player. "
        "default: 置 gBannerState[+0x19] bit1 反转, return 0. "
        "返回 1=进行中 / 0=完成. "
        "Constants: gBannerState=0x0201fec0, rom_sin_table_q8=0x09e5f8f0, "
        "tile_src=0x098f60e4, VRAM=0x06014000."),
    ("FUN_080c8fd8", "init_window_regs_for_campaign_banner",
        "为 campaign banner 场景设置 GBA 窗口和混合寄存器初值. "
        "写入 WIN0H=WIN1H=0x50c8 (left=0x50, right=0xc8), WIN0V=WIN1V=0x1878 (top=0x18, bottom=0x78), "
        "WININ=0x3f1f (all effects in window), WINOUT=0x1f; "
        "读 DISPCNT 置 bit14|bit15 (Window display enable) 后写回; 写 BLDCNT=0x0088 (blend enable). "
        "最后返回 1. 被 play_ui_effect_06 (0x080c91e0) 唯一调用, "
        "是 campaign banner 显示初始化序列的第一步 (配对后续 tick_campaign_banner_slide_state_machine). "
        "Constants: WIN0H=0x04000040, WIN1H=0x04000042, WIN0V=0x04000044, WIN1V=0x04000046, "
        "WININ=0x04000048, WINOUT=0x0400004a, BLDCNT=0x04000050, DISPCNT=0x04000000, "
        "win_h=0x50c8, win_v=0x1878, winin=0x3f1f, winout=0x1f, bldcnt=0x0088, dispcnt_mask=0xc000."),
    ("FUN_080c9030", "tick_campaign_banner_slide_state_machine",
        "campaign banner 滑入/滑出动画状态机, 每帧由 play_ui_effect_06 (0x080c91e0) 调用. "
        "读 [0x020230c0+1] (u8 phase) 进行 4-case dispatch (0/1/2/3). "
        "phase 0: 写 BLDY=0x1f (全黑); "
        "phase 1: 每帧 WIN0V.y_top 递减 (0xc*step/2, 中心点移动), 读 [0x020230c0+2] 累计 8 次后 phase++. "
        "phase 2: 拷贝 campaign_inner_image 到 BG VRAM 0x06009000 (size=0xb4*32=0x1680 bytes via copy_bytes_by_halfword), "
        "再写 WININ=0x3f1f / WINOUT=0x8c8c / WIN0V, 读 [0x020230c0+2] 累计 8 次后 phase++. "
        "phase 3: 同 phase 1 方向逆滑, 每帧 WIN0H y_bot 递增直到 [+2]>=8 后 phase++. "
        "default (phase>3): 返回 1 (busy, 未完成状态). "
        "返回 0=完成 / 1=进行中. "
        "Constants: campaign_state=0x020230c0, WIN0H=0x04000040, WIN0V=0x04000044, "
        "BLDY=0x04000054, WININ=0x04000048, WINOUT=0x0400004a, "
        "campaign_inner_image=0x0985d720, VRAM=0x06009000."),
    # --- batch #30 (campaign-30) ---
    ("FUN_080c91bc", "reset_blend_control_regs",
        "当 play_ui_effect_06 (case 0x06 UI 效果子状态机) 调用本函数时, 执行如下操作: "
        "读 BLDCNT (0x04000050) 并与掩码 0x9fff AND 清除 blend 模式字段[15:13]; "
        "将 BLDCOEF (0x04000052) 与 BLDALPHA (0x04000054) 均写为 0, 关闭 alpha 混合系数. "
        "副作用目的: 禁用 GBA 图层混合效果, 使画面回到正常直通模式. "
        "函数固定返回 1, 供调用方判断操作是否已执行. "
        "Constants: BLDCNT=0x04000050, MASK_9FFF=0x9fff (清除 BLDCNT[15:13]=blend mode), "
        "BLDCOEF=+2, BLDALPHA=+4 (相对 BLDCNT 偏移)."),
    ("FUN_080bd3f4", "tick_banner_display_state_machine",
        "由 play_ui_effect (0x0801ef94) 调用. "
        "读取 gBannerState (0x0201feC0, 偏移 +0x10 字节) 作为 switch 索引 [0..8], 共 9 个 case (case 4..7 合并为同一分支). "
        "每个 case 执行对应帧阶段操作: case 0 设置 VRAM/palette 标志并拷贝调色板数据, 按 LP 状态选择 tile 源; "
        "case 1 更新 banner 贴图行偏移并调 tile_2d_row_copy; 后续 case 逐步完成 banner 动画帧推进. "
        "函数通过 high-register callee-save (.hword 0x4647=mov r7,r0; .hword 0x4680=mov r8,r0) "
        "保存 gBannerState 指针和输入参数供 switch 各分支复用. "
        "Constants: gBannerState=0x0201feC0, VRAM_BG_BASE=0x06014000, "
        "PALETTE_SRC_0=0x05000260, ROM_PALETTE_A=0x098db0c4, ROM_PALETTE_B=0x098ed0e4."),
    ("FUN_0803bc58", "check_card_play_condition_eligible",
        "检查给定卡牌播放/效果条件是否满足. "
        "r0 为来自调用方的索引 (从 FUN_080c9f50 传入 ldr r0,[r0,#0x4] 的值). "
        "首先检查 gBannerState 相关结构体 (0x0201bcc0 + 0x80c/0x808 偏移) 是否均为 0; "
        "若非 0 则直接返回 0 (不满足). "
        "通过后检查 gP1LifePoints 结构中对应玩家的 LP 字段, 激活状态字段, 以及特定状态码; "
        "还会调用 check_player_side_condition 判断玩家阵营条件. "
        "最终返回 0 (不满足) 或 1 (满足). "
        "Constants: BASE=0x0201bcc0, OFFSET_STATE_A=0x80c, OFFSET_STATE_B=0x808, "
        "gP1LifePoints=0x0201c4e0, LP_OFFSET_PLAYER=0x1ce8, LP_OFFSET_ACTIVE=0x1d10, "
        "LP_OFFSET_TARGET=0x1d4c."),
    ("FUN_080c9f50", "render_card_view_scene_by_lp_time",
        "由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 和 FUN_080ca42c 调用. "
        "首先检查 gP1LifePoints+0x1d08 是否非零 (LP 存在); 若为零直接跳到函数末尾. "
        "然后调用 check_card_play_condition_eligible (FUN_0803bc58) 判断卡牌播放条件; 不满足则跳转. "
        "满足后, 从 LP 结构读取时间字段 (gP1LifePoints+r8*4+0x214), "
        "除以 0x3c (60) 得到分钟 r5 和秒数 r7, "
        "再调用各卡牌渲染子程序 (render_jp_string_to_tile_line 等) 将卡牌信息绘制到 BG tile VRAM. "
        "函数使用 r8/r9 作为 high-register callee-save 参数别名. "
        "Constants: gP1LifePoints=0x0201c4e0, OFFSET_LP_CHECK=0x1d08, TIME_DIV=0x3c (60), "
        "gPrng=0x03000040, TIME_LAYOUT=0x00660028."),
    ("FUN_080cd250", "init_field_bg_tile_vram_layout",
        "由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. "
        "函数入口将 r0 低 16 位 (r5=u16_lo) 和高 16 位 (r4=u16_hi) 分别提取作为 palette index 和 tile 偏移参数. "
        "首先 zero_fill_by_halfword 清零 BG tile VRAM 区域 (0x06014000, 0x80<<0x7=0x4000 halfword = 0x8000 字节); "
        "然后依次调用 copy_bytes_by_halfword (0x05000260 palette) 和三次 tile_2d_row_copy 将 card tile 数据从 ROM 复制到 VRAM. "
        "之后读取状态结构体的 palette/tile 字段, 计算 OBJ palette index 并循环写入 BG tile 中调色板编号字段. "
        "Constants: VRAM_BG_BASE=0x06014000, PALETTE_SRC=0x05000260, "
        "ROM_TILE_SRC_A=0x0988aad8, ROM_TILE_SRC_B=0x0988a7d8, ROM_TILE_SRC_C=0x0988ab58, "
        "STATE_BASE=0x0201f440, PALETTE_IDX_MASK=0xfffff00f, LOOP_END=5."),
    ("FUN_080cea50", "render_card_entry_jp_labels_to_bg",
        "由 FUN_080c7ea0 (window/vram/display/card_data 全标签主控) 独占调用 (indeg=1). "
        "初始化 JP 文字渲染缓冲区 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); "
        "读取状态结构体 (0x0201f440 + 0x0a16) 的 bit[0..2] 判断当前语言/模式标志, 选择对应的 font_jp_base_table 条目; "
        "然后循环遍历 card entry 表 (0x0201e4f0, 每条 4 字节, r5 in [0..3]) "
        "逐条调用 render_jp_string_to_tile_line 将 JP 文字渲染到 BG tile 缓冲; "
        "完成后调用 write_line_buf_to_bg_tile_vram 将缓冲写入 BG tile VRAM. "
        "Constants: STATE_BASE=0x0201f440, OFFSET_LANG_FLAG=0x0a16, "
        "CARD_ENTRY_TABLE=0x0201e4f0, VRAM_BG=0x06014000, LOOP_RANGE=[0..3]."),
    ("FUN_080cf7d4", "render_card_stat_tiles_to_vram",
        "由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. "
        "首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x80<<7=0x4000 halfword); "
        "读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的 bit[0]/bit[1] 判断是否需要渲染. "
        "若条件不满足直接跳至末尾. "
        "满足后: 读 r4 (入口参数) 作为 stat 值, 计算显示行列位置 (modsi3/divsi3 各 1 次, 除数 0xa=10), "
        "调用 copy_bytes_by_halfword 拷贝调色板数据两次 (来自 ROM 0x09850c5c/0x0984ee2c 到 0x05000260/0x05000280), "
        "然后 tile_2d_row_copy 拷贝 tile 数据到 VRAM (0x06010000), "
        "调用 setup_line_buf + render_jp (game_str) 渲染统计数字字符到 BG tile; "
        "最后 write_line_buf_to_bg_tile_vram 写回 VRAM. "
        "函数使用 r8/r9/r10 为 callee-save 别名. "
        "r0: s32 stat_value (caller1 080c7a74 从卡牌 ATK/DEF 字段传入; caller2 080c80da 固定传 0). "
        "Constants: VRAM_BG_CLEAR=0x06014000, STATE_BASE=0x0201f440, "
        "PAL_DST_A=0x05000260, PAL_SRC_A=0x09850c5c, PAL_DST_B=0x05000280, PAL_SRC_B=0x0984ee2c, "
        "TILE_VRAM_BASE=0x06010000, STAT_ROWS=0x13, STAT_COLS=0xa."),
    ("FUN_080cff50", "init_field_slot_tile_attrs",
        "由 FUN_080c7950 (vram/card_stats) 和 FUN_080c7ea0 (window/vram/display/card) 调用. "
        "入口将 r0 低 16 位提取为 r4 (palette_index), 高 16 位提取为 r5 (tile_offset). "
        "首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x4000 halfword). "
        "读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的两个标志位决定是否执行后续写入; 若均为 0 则跳过. "
        "满足后: 将 palette_index 写入状态字段 0x0a0c (halfword, 通过掩码 0x7fff/0xffff8000 保留低 15 位), "
        "将 tile_offset (r5) 写入状态字段 0x0a0d byte (bit[6:0], mask 0x7f). "
        "最后固定写入状态字段 0x0a01 := 7. "
        "r0: u32 packed_params (低 16 位=palette_index [0..0x7fff], 高 16 位=tile_offset [0..0x7f]). "
        "Constants: VRAM_BG_BASE=0x06014000, STATE_BASE=0x0201f440, "
        "OFFSET_FLAG_A=0x0a17, OFFSET_FLAG_B=0x0a18, MASK_15BIT_LO=0x7fff, STATE_DONE=7."),
    ("FUN_080cffd4", "render_duel_zone_card_detail_to_vram",
        "由 FUN_080c7ea0 (window/vram/display/card_data/duel_field 全标签主控) 独占调用 (indeg=1). "
        "综合执行以下操作: (1) 读状态字段 (0x0201f440+0x0a0c) 的卡牌 ID (15 位), "
        "调用 ensure_card_id_cache_entry 确保卡牌数据已缓存; "
        "(2) 读下一个槽位 ID, 调用 find_zone_descriptor_by_slot_id 和 get_zone_slot_ptr 获取区域插槽指针; "
        "(3) 读插槽中卡牌 face_down bit, 与 0x4020 合并存入 sp+4; "
        "(4) 初始化 JP 文字行缓冲 (setup_line_buf_with_font_and_align); "
        "(5) 设置语言模式 flag (font_jp_base_table 查找); "
        "(6) render_jp_string_to_tile_line 渲染卡牌名称 JP 文字; "
        "(7) write_line_buf_to_bg_tile_vram 写 BG tile VRAM; "
        "(8) 两次 load_card_list_small_image 加载小图; "
        "(9) render_large_card_display_by_mode 渲染大卡图. "
        "Constants: STATE_BASE=0x0201f440, OFFSET_CARD_SLOT=0x0a0c, "
        "FLAG_FACE_DOWN=0x4020, VRAM_BG=0x06014000, gP1LifePoints_BASE=0x02023130."),
    ("FUN_080d04dc", "render_jp_two_line_text_to_bg_vram",
        "由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). "
        "与 080ccfe4 结构完全对称: 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); "
        "设置语言模式标志 (STATE+0x8 bit[1..2]); 从 font_jp_base_table 取字体基址; "
        "以 STATE_DATA (0x0201f441) 为源, 调用 render_jp_string_to_tile_line 两次 (循环 r6 in [0..1]), "
        "每次偏移 0x200 字节 (0x80*4); 完成后 write_line_buf_to_bg_tile_vram 刷新到 BG tile VRAM (0x06014000). "
        "函数使用 r8/r9 callee-save high-register 别名, 由 .hword 0x4657/464e/4645/4682 搬移. "
        "Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, "
        "VRAM_BG=0x06014000, FONT_SIZE=0x200, LOOP_RANGE=[0..1]."),
    ("FUN_080ca160", "render_lp_zone_digit_oam_row",
        "由 FUN_080c7ea0 (window/vram/display/card) 和 FUN_080ca42c (card_data/card_frame/..) 调用. "
        "函数在结构体 0x0201e2a0 中循环查找 slot.id == 0; "
        "比较键 r10 由函数内部 movs r0,#0; mov r10,r0 设置为 0 (非 caller-set). "
        "每次命中 (slot.id==0) 后: 调用 write_oam_entry_from_packed_args 写一个 OAM 精灵条目; "
        "然后三次调用 write_decimal_digits_to_oam 分别在 OAM 偏移 0x74/0x6c/0x64 写入 3 组十进制数字 (来自 r4 计算的 data 地址). "
        "最终跳到 LAB_080ca266 结束. "
        "Constants: STRUCT_BASE=0x0201e2a0, gP1LifePoints=0x0201c4e0, "
        "OAM_SHAPE_SIZE=0xc4<<0xf|0xe0, DIGIT_OAM_OFF_A=0x74, DIGIT_OAM_OFF_B=0x6c, DIGIT_OAM_OFF_C=0x64, "
        "DATA_STRIDE=0x868, ZONE_ENTRY_STRIDE=0xec, LOOP_KEY=0."),
    ("FUN_080ccfe4", "render_jp_two_line_text_to_bg_vram_alt",
        "由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). "
        "与 080d04dc 结构完全对称: 初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); "
        "设置语言模式标志 (STATE+0x8 bit[1..2]); 从 font_jp_base_table 取字体基址; "
        "以 STATE_DATA (0x0201f441) 为源调用 render_jp_string_to_tile_line 两次 (循环 r6 in [0..1], 步进 0x200 字节); "
        "完成后 write_line_buf_to_bg_tile_vram 刷新到 BG tile VRAM (0x06014000). "
        "两函数共用同一 STATE_BASE (0x02006ed0) / STATE_DATA (0x0201f441) / VRAM / 字体配置, "
        "仅写入的 STATE 字段偏移略有差异. "
        "Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, "
        "VRAM_BG=0x06014000, FONT_SIZE=0x200, LOOP_RANGE=[0..1]."),
    ("FUN_080cda6c", "render_jp_label_row_with_tile_count",
        "由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). "
        "初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); "
        "设置语言模式 (STATE_BASE+0x8); 从 font_jp_base_table 取字体基址; "
        "调用 render_jp_string_to_tile_line 一次; 调用 write_line_buf_to_bg_tile_vram 将 JP 文字写入 VRAM. "
        "随后检查状态字段 (STATE_BASE+0x0a16/0x0a17 双标志), 若均为 0: "
        "计算 tile 行列位置 (asrs r0,r4,#3 行; ands r4,r7=#7 列), 将 tile_pos halfword 写入 STATE_BASE+0x0a03; "
        "另外读状态字段 +0x0a0d (palette/tile nibble), 递增 nibble 字段并写回; "
        "最终将 tile_row_count 写入 STATE_BASE+0x0a03-1 (base_ptr-1 字节). "
        "Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, "
        "OFFSET_FLAG_A=0x0a16, OFFSET_FLAG_B=0x0a17, OFFSET_TILE_POS=0x0a03, OFFSET_NIBBLE=0x0a0d, "
        "VRAM_BG=0x06014000, TILE_MASK=0x7."),
    ("FUN_080cd870", "render_jp_label_row_with_tile_pos",
        "由 FUN_080c7ea0 (window/vram/display/card 全标签主控) 独占调用 (indeg=1). "
        "与 080cda6c 结构高度对称, 但末尾使用直接行列计算而非 nibble 循环. "
        "初始化 JP 行缓冲 (setup_line_buf_with_font_and_align: font=0x17, width=0x10, mode=1, align=2); "
        "设置语言模式 (STATE+0x8); 从 font_jp_base_table 取字体基址; "
        "调用 render_jp_string_to_tile_line; 调用 write_line_buf_to_bg_tile_vram 写 BG VRAM. "
        "然后检查状态字段 (STATE+0x0a16/0x0a17 双标志), 若均为 0: "
        "将 render 返回值 r4-1 作为 tile_width 写入 STATE+0x0a03 halfword; "
        "再计算 tile_row (r4+0x10 除以 8) 和 tile_col (r4+0x10 & 7), "
        "若有余则 tile_row+1, 最终写入 STATE+0x0a02 byte. "
        "Constants: STATE_BASE=0x02006ed0, STATE_DATA=0x0201f441, "
        "OFFSET_TILE_WIDTH=0x0a03, OFFSET_TILE_ROW=0x0a02, VRAM_BG=0x06014000, "
        "OFFSET_FLAG_A=0x0a16, OFFSET_FLAG_B=0x0a17, TILE_ALIGN=8."),
    ("FUN_080ce7f0", "zero_fill_card_label_vram_if_ready",
        "由 FUN_080c7950 (vram/card_stats/font_jp) 和 FUN_080c7ea0 (window/vram/display/card) 调用. "
        "首先 zero_fill_by_halfword 清零 BG tile VRAM (0x06014000, 0x80<<7=0x4000 halfword). "
        "读取状态结构体 (0x0201f440 + 0x0a17/0x0a18) 的双标志: 若任一非零则跳到 LAB_080cea22 (早期退出). "
        "若均为零则进入主循环 (r6 in [0..?]): 从 card entry 表 (0x0201e4f0 + r6*4) 读取 game_str_id (13 位), "
        "调用 resolve_game_str_ptr 解析字符串指针; "
        "若字符串第一字节为 0 (空串) 则清除 entry.flag[0x11] bit[6]; "
        "否则调用渲染路径 (LAB_080ce86c) 将字符串内容写入 BG VRAM 对应区域. "
        "函数使用 r8/r9 callee-save (.hword 0x4682/4689). "
        "Constants: VRAM_BG_BASE=0x06014000, STATE_BASE=0x0201f440, "
        "OFFSET_FLAG_A=0x0a17, OFFSET_FLAG_B=0x0a18, "
        "CARD_ENTRY_TABLE=0x0201e4f0, ENTRY_FLAG_OFF=0x11, STR_ID_MASK=0x1fff."),

    # 2026-05-10: campaign-31 batch #31 (topo=695-708)
    ("FUN_080c7530", "write_card_list_oam_row_strip",
        "indeg=10 (8 card-list display callers). "
        "Writes one row of card icon OAM entries into the sprite table. "
        "r0=oam_start_slot [0..255], r1=y_pixel, r2=x_start_pixel, r3=card_row_count (lo16). "
        "Inner loop: 7 sub-slots (r7=0..6) per row, each calls write_oam_entry_from_packed_args; "
        "X offset accumulated per slot (+2 or +4 px step). "
        "r4=width flag (1/2/4, from remaining row count); "
        "r6=palette/attr word (0x8040/0x8080/0x4040 etc, from slot r7 and width r4). "
        "After each row of 7 slots, updates X origin r5 and decrements row count. "
        "Returns void; all side-effects via write_oam_entry_from_packed_args. "
        "Constants: STRIP_SLOTS=7; WIDTH_4=0x4, WIDTH_2=0x2, WIDTH_1=0x1; "
        "PAL_0x8040=0x00008040, PAL_0x8080=0x00008080, PAL_0x4040=0x00004040."),
    ("FUN_080c7ea0", "dispatch_card_display_state_by_mode",
        "indeg=1, caller: FUN_080c82e4 (card all-tag display master tick). "
        "Reads gFontState (0x0201f440) + 0x0a1a offset (16-bit word); "
        "extracts bits[14..8] low-7-bits via lsls/lsrs 0x17/0x18 as mode index, upper bound 6. "
        "Dispatches to 7 independent case functions via switchD_080c7ebe jump table. "
        "No direct side-effects; all effects delegated to case callees. "
        "Constants: MODE_MAX=6; DISPLAY_MODE_OFFSET=0x0a1a; "
        "jump table: 7 entries at 0x080c7ecc..0x080c7ee4."),
    ("FUN_080cf9f4", "render_card_name_jp_to_bg_tile_vram",
        "indeg=1, caller: FUN_080c7ea0 (card display state dispatch). "
        "Renders card name JP text to BG tile VRAM. "
        "Steps: (1) setup_line_buf_with_font_and_align(font=0x17, width=0x10, mode=1, align=2); "
        "(2) reads gFontState+0x0a03 x-offset and global lang flags (0x02006c2c+0x6c2c, mask 0x7 and 0x2) "
        "to determine render language mode, writes back to gFontState+0x8; "
        "(3) selects font base ptr from font_jp_base_table, writes to gFontState+0x4; "
        "(4) sets gFontState+0x15 bit6; "
        "(5) render_jp_string_to_tile_line (start=(2,2), palette=0xc, src=DAT_080cfab8=0x0201f441); "
        "(6) computes tile row count from render width (r4+0x30 asrs #3), "
        "writes to gFontState+0x0a02; "
        "(7) conditionally strb tile_row (only if gFontState+0x0a16=gFontState+0x0a17=0); "
        "(8) write_line_buf_to_bg_tile_vram to BG VRAM 0x06014000. "
        "Constants: FONT_ID=0x17; WIDTH=0x10; TILE_ROW_OFFSET=0x0a02; "
        "FLAG_A=0x0a16; FLAG_B=0x0a17; VRAM_BG=0x06014000."),
    ("FUN_080ce078", "init_card_info_display_with_jp_label",
        "indeg=2, callers: FUN_080c7950 (card_stats/font_jp) and FUN_080c7ea0 (display master). "
        "Initializes all VRAM/palette resources for card info display area and renders JP label. "
        "r0 packed: lo16=x_tile_col, hi16=y_tile_row, each [0..31]. "
        "Steps: (1) zero_fill_by_halfword BG tile VRAM 0x06014000 (0x4000 halfwords); "
        "(2) reads gFontState+0x0a17 JP flag bit0 and +0x0a18 flag, "
        "if both 0: copies gFontState+0x0a10 word; "
        "(3) copy_bytes_by_halfword palette A (ROM 0x09850c5c -> OBJ pal 0x05000260, 0x20 hw); "
        "(4) copy_bytes_by_halfword palette B (ROM 0x0984e30c -> OBJ pal 0x05000280, 0x20 hw); "
        "(5) tile_2d_row_copy 6 rows from ROM 0x0984de8c to BG VRAM 0x06013000; "
        "(6) tile_2d_row_copy 1 row to BG VRAM 0x06013800; "
        "(7) setup_line_buf_with_font_and_align(font=0x17, w=0x10, mode=1, align=2), "
        "game_str_id_to_row + game_str_pointer_table, text_render_wrapper, "
        "write_line_buf_to_bg_tile_vram JP label; "
        "(8) strb 0x6 to gFontState+0x0a15 (done flag). "
        "Constants: VRAM_BG=0x06014000; OBJ_PAL_A=0x05000260; OBJ_PAL_B=0x05000280; "
        "VRAM_TILE_A=0x06013000; VRAM_TILE_B=0x06013800; "
        "ROM_PAL_A=0x09850c5c; ROM_PAL_B=0x0984e30c; ROM_TILE=0x0984de8c; "
        "DONE_FLAG=6; FONT_ID=0x17."),
    ("FUN_080cd138", "render_card_list_oam_row_by_lp_counter",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Computes OAM Y from gFontState+0x0a03 card_row_count byte: Y=(10-count/2)*8. "
        "Calls write_card_list_oam_row_strip(r0=0x30, r1=Y, r2=0x1fc, r3=count). "
        "Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch: "
        "(0) checks gPrng+0x148 bits[7:6] (mask 0xc0): if nonzero, decrements "
        "gFontState+0x0a14 halfword by 1, calls sync_state_and_init_sprite(0); "
        "(1) checks gPrng+0x148 bit0: if nonzero, reads LP from gP1LifePoints+0x3d40, "
        "writes gFontState+0x0a14 halfword (1-LP_val), calls sync_state_and_init_sprite(0x24); "
        "bit1 nonzero: calls sync_state_and_init_sprite(2); "
        "(2) state>=2: nibble loop increment on gFontState+0x0a1b/0x0a1c byte pair; "
        "returns 1 if nibble>0x1f else 0. "
        "Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; "
        "STATE_OFFSET=0x0a18; LP_OFFSET=0x0a14; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; "
        "LP_ADDR=gP1LifePoints+0x3d40; BITS_LP=0xc0."),
    ("FUN_080cd5ec", "render_card_list_oam_row_by_nibble_rotate",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. "
        "Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. "
        "state=0: reads gPrng+0x148, tests bit5(0x20)/bit4(0x10)/bit0 in sequence; "
        "each path executes nibble-decrement mod-16 loop on gFontState+0x0a0e byte "
        "until corresponding bit in gFontState+0x0a02 is hit; "
        "on success writes gFontState+0x0a14 halfword -1 or +1, calls sync_state_and_init_sprite(0). "
        "state=1: reads gPrng+0x148 bit0 -> LP update (gP1LifePoints+0x3d40, strh 1-halfword). "
        "state>=2: nibble loop increment on 0x0a1b/0x0a1c (same logic as 080cd138). "
        "Key difference from 080cd138: state=0 uses nibble rotation (0x0a0e nibble mask 0xf, "
        "subs #1 & 0xf) rather than LP counter decrement. "
        "Constants: OAM_SLOT=0x30; Y_BASE=10; NIBBLE_OFFSET=0x0a0e; "
        "MASK_BIT5=0x20; MASK_BIT4=0x10; MASK_BIT0=0x01."),
    ("FUN_080cd94c", "render_card_list_oam_row_by_flag_check",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Shortest of the 8 sibling functions: no nibble rotate, no LP write. "
        "Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. "
        "Reads gPrng+0x148 (=gPrng+0xa4*2) low 2 bits: "
        "if bit0=1 or bit1=1, calls sync_state_and_init_sprite(0x24), returns 1; "
        "else returns 0. "
        "Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; "
        "FLAG_OFFSET=gPrng+0x148; MASK_BITS12=0x3; SYNC_OP=0x24."),
    ("FUN_080cdd70", "render_card_list_oam_row_by_lp_nibble",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. "
        "Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. "
        "state=0: reads gPrng+0x148; bit5=0x20: nibble-decrement on gFontState+0x0a0e (mod 16), "
        "on hit writes gFontState+0x0a14 halfword-1, sync_state_and_init_sprite(0); "
        "bit4=0x10: nibble-increment, writes halfword+1; "
        "bit0=0x1: writes gFontState+0x0a0e bits[3:0] (nibble) to gP1LifePoints+0x3d40, "
        "increments gFontState+0x0a18 bits[9:16], sync_state_and_init_sprite(0x24); "
        "bit1=0x2: compares gP1LifePoints+0x1cf4 word, on match sync_state_and_init_sprite(1) "
        "returns 1, else sync_state_and_init_sprite(2). "
        "state=1: nibble increment on 0x0a1b/0x0a1c, may also increment 0x0a18 bits[23:16]. "
        "state>=2: returns 0. "
        "Constants: OAM_SLOT=0x30; NIBBLE_OFFSET=0x0a0e; LP_FIELD=0x0a02; "
        "LP_ADDR=gP1LifePoints+0x3d40; CMP_ADDR=gP1LifePoints+0x1cf4."),
    ("FUN_080cdf6c", "find_next_occupied_slot_in_main_list",
        "indeg=1, caller: FUN_080ce428 (card list OAM row by slot advance). "
        "Searches card main slot list (gFontState+0x0a06 halfword array) for next occupied slot. "
        "r0=current_slot_id [0..5] (saved to r8 as loop sentinel). "
        "Loop: increments slot_id modulo 6 via __modsi3; checks gFontState+0x0a10 flag word "
        "bit corresponding to slot; if set (occupied), scans gFontState+0x0a06 halfword list "
        "to confirm slot_id not already present. Returns r0=next occupied slot_id [0..5]. "
        "Pure read: no VRAM/OAM side-effects. "
        "Constants: SLOT_COUNT=6; FLAG_WORD_OFFSET=0x0a10; "
        "SLOT_LIST_OFFSET=0x0a06; SLOT_TABLE_OFFSET=0x0a0e."),
    ("FUN_080cdff4", "find_next_occupied_slot_in_secondary_list",
        "indeg=1, caller: FUN_080ce428 (card list OAM row by slot advance). "
        "Symmetric to find_next_occupied_slot_in_main_list (0x080cdf6c) but operates on "
        "secondary slot table (gFontState+0x0a0e halfword table). "
        "r0=current_slot_id [0..5] (saved to r8 as sentinel). "
        "Loop: decrements slot_id via __modsi3(mod 6) in reverse; "
        "checks gFontState+0x0a10 flag word bit; "
        "on hit, scans gFontState+0x0a06 list to confirm non-duplicate. "
        "Returns r0=next occupied slot_id [0..5]. Pure read; no side-effects. "
        "Key difference from 0x080cdf6c: search table=+0x0a0e, compare list=+0x0a06 "
        "(roles swapped relative to main-list variant). "
        "Constants: SLOT_COUNT=6; FLAG_WORD_OFFSET=0x0a10; "
        "SEC_TABLE_OFFSET=0x0a0e; CMP_LIST_OFFSET=0x0a06."),
    ("FUN_080ce428", "render_card_list_oam_row_by_slot_advance",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Differs from the other 7 sibling functions: adds extra Y offset from "
        "gFontState+0x0a04 halfword on top of base Y=(10-count/2)*8, then calls "
        "write_card_list_oam_row_strip. "
        "After the icon row: 5-iteration loop writes cursor sprites via "
        "write_oam_entry_from_packed_args (OAM slot base 0x32, x=0x32 stepped). "
        "Then reads gPrng+0x148 flags for four-way dispatch: "
        "(1) bit4=1: calls find_next_occupied_slot_in_main_list, "
        "strh result to gFontState+0x0a14, sets gFontState+0x0a18 bit9, "
        "sync_state_and_init_sprite(0); "
        "(2) bit5=1: calls find_next_occupied_slot_in_secondary_list, same state update; "
        "(3) bit0=1: increments gFontState+0x0a0e nibble (bits[23:16]+1 & 0xff), "
        "copy_bytes_by_halfword ROM 0x0984e30c -> OBJ pal 0x05000280 (0x20 hw), "
        "builds LP bit-set from gFontState+0x0a06, writes to gP1LifePoints+0x3d40, "
        "sync_state_and_init_sprite(0x24); (4) else: no-op. "
        "Constants: Y_EXTRA_OFFSET=0x0a04; OAM_CURSOR_LOOP=5; OAM_CURSOR_X=0x32; "
        "FLAG_MAIN=0x10; FLAG_SEC=0x20; FLAG_LP=0x01; "
        "ROM_PAL=0x0984e30c; OBJ_PAL=0x05000280."),
    ("FUN_080cf52c", "render_card_list_oam_row_by_stat_display",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. "
        "Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. "
        "state=0: reads gPrng+0x148; "
        "bit5=0x20: increments gFontState+0x0a0e halfword bits[23:16] nibble (mod 256), "
        "calls render_card_numeric_stat_to_bg, sync_state_and_init_sprite(0); "
        "bit1=0x2: sync_state_and_init_sprite(2); "
        "bit0=0x1: reads LP offset from gFontState+0x0a0e/0x0a06, "
        "writes to gP1LifePoints+0x3d40, increments gFontState+0x0a18 bits[9:16] nibble, "
        "sync_state_and_init_sprite(0x24). "
        "state=1: nibble increment on gFontState+0x0a1b/0x0a1c, "
        "if >0x1f also increments gFontState+0x0a18 bits[23:16], writes back. "
        "state>=2: returns 1. "
        "Key distinguisher: only sibling containing render_card_numeric_stat_to_bg callee "
        "(card ATK/DEF stat refresh path). "
        "Constants: OAM_SLOT=0x30; STATE_OFFSET=0x0a18; "
        "NIBBLE_B_OFFSET=0x0a1b; NIBBLE_C_OFFSET=0x0a1c; STAT_NIBBLE_OFFSET=0x0a0e."),
    ("FUN_080d029c", "render_card_list_oam_row_by_lp_init",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Nearly identical structure to render_card_list_oam_row_by_lp_counter (0x080cd138). "
        "Computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip. "
        "Reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. "
        "state=0: reads gPrng+0x148 with mask 0x30 (bit4/5, vs 0xc0 in 080cd138); "
        "nonzero: decrements gFontState+0x0a14 halfword by 1, calls sync_state_and_init_sprite(0). "
        "state=1: reads LP from gP1LifePoints+0x3d40, writes gFontState+0x0a14 halfword (1-LP_val), "
        "sets state word bit9, calls sync_state_and_init_sprite(0x24) or (2). "
        "state>=2: nibble loop on 0x0a1b/0x0a1c; returns 1 if >0x1f else 0. "
        "Key difference from 080cd138: gPrng+0x148 check mask=0x30 (bit4/5) not 0xc0. "
        "Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; "
        "STATE_OFFSET=0x0a18; LP_OFFSET=0x0a14; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; LP_MASK=0x30."),
    ("FUN_080d0640", "render_card_list_oam_row_by_slot_nibble",
        "indeg=1, caller: FUN_080c82e4 (card display master tick). "
        "Same skeleton as render_card_list_oam_row_by_lp_init (0x080d029c): "
        "computes OAM Y from gFontState+0x0a03, calls write_card_list_oam_row_strip; "
        "reads gFontState+0x0a18 bits[23:16]=slot_state, three-way dispatch. "
        "state=0: reads gPrng+0x148 bits[7:6] (mask 0xc0). "
        "state=1: LP counter update (gP1LifePoints+0x3d40). "
        "state>=2: reads nibble pair from gFontState+0x0a1b (nibble_A, byte) "
        "and +0x0a1c (nibble_B, byte), increments nibble_A; "
        "if nibble_A>0x1f returns 1 else 0. "
        "Key difference from 080cd138: after nibble_A increment, "
        "applies OR bit1 to nibble_B (flag nibble B logic). "
        "Constants: OAM_SLOT=0x30; Y_BASE=10; OAM_ATTR=0x1fc; "
        "STATE_OFFSET=0x0a18; NIBBLE_A=0x0a1b; NIBBLE_B=0x0a1c; LP_MASK=0xc0."),

    # 2026-05-10: campaign-32 batch #32 (topo=709-722)
    ("FUN_080c7638", "dispatch_card_list_oam_row_by_card_type",
        "Card-list OAM row render dispatcher; 10-case jump table keyed on "
        "gFontState[0x0a01]-1 (range [0..9]). Reads card_type byte, subtracts 1, "
        "bounds-checks against 9, then branches via table at 0x080c7660. "
        "case 1 -> render_card_list_oam_row_by_pack_slot; "
        "case 3 -> render_card_list_oam_row_by_cursor_slot; "
        "case 4 -> render_card_list_oam_row_by_dual_slot; "
        "case 5 -> render_card_list_oam_row_by_rarity_flag; "
        "case 6 -> render_card_list_oam_row_by_type_icon; "
        "case 7 -> render_card_list_oam_row_by_pack_column; "
        "case 8 -> render_card_list_oam_row_by_cost_bar; "
        "case 9 -> render_card_list_oam_row_by_single_slot; "
        "case 10 -> render_card_list_oam_row_by_anim_frame. "
        "Out-of-range -> default exit. No direct IO writes; side effects in callees. "
        "caller: FUN_080c82e4 (card display master tick). "
        "Constants: FONT_STATE_BASE=0x0201f440; CARD_TYPE_OFFSET=0x0a01; "
        "JUMP_TABLE=0x080c7660 (10 entries)."),
    ("FUN_080cf6d8", "find_next_occupied_slot_forward",
        "Forward circular search for next occupied slot in card-list slot bitmap. "
        "r0=start_slot_idx [0..9]; returns r0=found_slot_idx. "
        "Reads gFontState[0x0a10] word; tests bit(r2) for each slot. "
        "Increments r2 each iteration; wraps at 10 via __modsi3. "
        "If wrapped back to anchor returns r4 or r4+10 based on wrap_flag. "
        "No external writes; read-only query. "
        "caller: render_card_list_oam_row_by_stat_state (0x080cfbdc) bit4 path. "
        "Constants: SLOT_BITMASK_OFFSET=0x0a10; SLOT_COUNT=10."),
    ("FUN_080cf754", "find_next_occupied_slot_backward",
        "Backward circular search for next occupied slot in card-list slot bitmap. "
        "Symmetric sibling of find_next_occupied_slot_forward (0x080cf6d8). "
        "r0=start_slot_idx [0..9]; returns r0=found_slot_idx (decreasing direction). "
        "Reads gFontState[0x0a10] word; r2-- each iteration; wraps 0->9. "
        "No external writes; read-only query. "
        "caller: render_card_list_oam_row_by_stat_state (0x080cfbdc) bit5/0xc0 paths. "
        "Constants: SLOT_BITMASK_OFFSET=0x0a10; SLOT_COUNT=10."),
    ("FUN_080cfbdc", "render_card_list_oam_row_by_stat_state",
        "Card-list OAM row render branch for stat_state variant. "
        "indeg=1; caller: FUN_080c82e4 (card display master tick). "
        "Reads gFontState[0x0a03] row_count -> OAM Y; gFontState[0x0a04] x_base; "
        "gFontState[0x0a0e] slot_nibble bits[23:16]; gFontState[0x0a18] state_val bits[23:16]. "
        "Four-way dispatch on state_val: "
        "state=0: writes 4 OAM strips (write_oam_entry_from_packed_args, attr0=0x32, slot=0x60); "
        "then checks gPrng[0x148] bit4(0x10)->find_next_occupied_slot_forward+nibble write+sync; "
        "bit5(0x20)->find_next_occupied_slot_backward+nibble write+sync; "
        "bits6-7(0xc0)->mod20+find_next_occupied_slot_backward+sync; "
        "bit0(0x01)->write gP1LifePoints+0x148+sync. "
        "state=1: nibble_B/C update loop (gFontState[0x0a1b/0x0a1c]). "
        "Side effects: [gFontState+0x0a0e] nibble bits[11:4] updated; "
        "[gFontState+0x0a18] state bits updated; [gP1LifePoints+0x148] written (state=0 bit0). "
        "Constants: SLOT_NIBBLE_OFFSET=0x0a0e; STATE_OFFSET=0x0a18; "
        "OAM_STRIP_COUNT=4; ATTR0_STRIP=0x32; OAM_SLOT=0x60; WRAP_MODULO=0x14."),
    ("FUN_080cedd0", "render_card_list_oam_row_by_jp_type",
        "Card-list OAM row render branch for JP font row type. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) for a matching case. "
        "Reads gFontState[0x0a03] JP row count; OAM Y = (10 - row/2) * 8. "
        "Checks gFontState[0x0a17] bit0 (active flag); if 0 branches to shared exit LAB_080cf0b0. "
        "When active: reads gFontState[0x0a02] strip index; calls write_card_list_oam_row_strip "
        "(slot=0x30, x=0x1fc). Reads gFontState[0x0a18] bits[23:16]=state_val; "
        "four-way dispatch (state 0/1/2/3) for JP card name render frame phases. "
        "No APCS inputs; all values loaded from DAT addresses internally. "
        "Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; FLAG_OFFSET=0x0a17; "
        "STRIP_IDX_OFFSET=0x0a02; STATE_OFFSET=0x0a18; OAM_SLOT=0x30; X_BASE=0x1fc."),
    ("FUN_080d05e4", "render_card_list_oam_row_by_pack_slot",
        "Card-list OAM row render branch for pack_slot variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 1. "
        "Reads gFontState[0x0a03] JP row count; OAM Y = (10-row/2)*8. "
        "Reads gFontState[0x0a1b] bits[1:0] pack_slot state [0..1]; if >1 skips write. "
        "For state 0..1: reads gFontState[0x0a0e] halfword*2 as x_base, "
        "subtracts 0x17, adds gFontState[0x0a04] halfword for Y. "
        "Calls write_oam_entry_from_packed_args (slot=0x60, attr0=0x34). "
        "No APCS inputs. "
        "Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; "
        "SLOT_STATE_OFFSET=0x0a1b [0..1]; X_BASE_OFFSET=0x0a0e; "
        "Y_ADJ_OFFSET=0x0a04; ATTR0=0x34; OAM_SLOT=0x60."),
    ("FUN_080cdba8", "render_card_list_oam_row_by_dual_slot",
        "Card-list OAM row render branch for dual_slot variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 4. "
        "Uses two __divsi3 calls (divisor=0xc8=200) to convert gFontState[0x0201fe4e] "
        "halfword bits[23:16] into x_div/y_div coordinates. "
        "OAM Y base = y_coord+0x1c. Reads gFontState[0x0a1b] bits[1:0] slot_state. "
        "slot_state<=1: extracts gPrng[0x148] bit4 flip_bit; calls "
        "write_oam_entry_from_packed_args (slot=0x60) and write_oam_entry_with_slot_check "
        "(attr2=0x1000/0x2000/0x3000) for 3 OAM entries. "
        "slot_state>1: extended path with up to 6 extra OAM entries. "
        "No APCS inputs; gFontState base loaded internally via r10. "
        "Sibling of render_card_list_oam_row_by_single_slot (divisor=0xb8, Y+0x2a). "
        "Constants: CARD_REG_OFFSET=0x0201fe4e; DIVISOR=0xc8; OAM_Y_BASE=+0x1c; "
        "SLOT_STATE_OFFSET=0x0a1b; OAM_SLOT=0x60; FLIP_BIT=bit4 of gPrng[0x148]; "
        "ATTR2_A=0x1000; ATTR2_B=0x2000; ATTR2_C=0x3000."),
    ("FUN_080ced0c", "render_card_list_oam_row_by_cursor_slot",
        "Card-list OAM row render branch for cursor_slot variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 3. "
        "Reads gFontState[0x0a03] row count; OAM Y = (10-row/2)*8. "
        "Reads gFontState[0x0a1b] bits[1:0] slot_state; if >1 exits. "
        "Checks gFontState[0x0a1c] bit0 cursor active flag; if 0 checks cursor max. "
        "When active: reads gFontState[0x0a0e] halfword+r5 as Y coord (attr0=0x88); "
        "calls write_oam_entry_from_packed_args (slot=0x60). "
        "If cursor Y exceeds max: calls write_oam_entry_with_slot_check (attr2=0x4000) for overflow row. "
        "No APCS inputs. "
        "Constants: FONT_STATE_BASE=0x0201f440; ROW_OFFSET=0x0a03; "
        "SLOT_STATE_OFFSET=0x0a1b [0..1]; ACTIVE_FLAG_OFFSET=0x0a1c bit0; "
        "CURSOR_MAX_OFFSET=0x0a10; ATTR0_CURSOR=0x88; ATTR2_OVERFLOW=0x4000; OAM_SLOT=0x60."),
    ("FUN_080cf490", "render_card_list_oam_row_by_anim_frame",
        "Card-list OAM row render branch for animation frame variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 10 (last case). "
        "Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword as x_base. "
        "Loop r4=0..5: calls write_oam_entry_from_packed_args 6 times for strip OAM "
        "(attr0 incremented by 0x20 per step, attr1=0xe0<<0x11+tile_col, attr2=0x81<<7=0x4080). "
        "After loop: checks gFontState[0x0a1b] bits[1:0]; if <=1 extracts "
        "gPrng[0x148] bits[3:2] (range [0..3]) as delta, computes anim frame Y=0x58-delta, "
        "calls write_oam_entry_with_slot_check (attr2=0x1000). "
        "Writes one trailing write_oam_entry_from_packed_args (attr2=0). "
        "No APCS inputs. "
        "Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; STRIP_COUNT=6; "
        "SLOT_STATE_OFFSET=0x0a1b; PRNG_DELTA_MASK=bits[3:2] of gPrng[0x148] [0..3]; "
        "ATTR2_ANIM=0x1000; OAM_SLOT=0x60."),
    ("FUN_080cfad0", "render_card_list_oam_row_by_rarity_flag",
        "Card-list OAM row render branch for rarity_flag variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 5. "
        "Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword x_base. "
        "Reads gFontState[0x0a18] word bits[23:8] (mask=0xff<<9): "
        "0x200 -> rarity_level=3; 0x400 -> rarity_level=4; default -> 4. "
        "Calls write_card_list_oam_row_strip (slot=0x30). "
        "Main loop r6=0..19 (20 iterations): calls write_oam_entry_from_packed_args; "
        "uses __modsi3 (mod 10) and __divsi3 (div 10) for column wrap coordinates. "
        "No APCS inputs. "
        "Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; "
        "RARITY_FIELD_OFFSET=0x0a18 bits[23:8]; "
        "RARITY_A=0x200 r7=3; RARITY_B=0x400 r7=4; STRIP_LOOP_COUNT=20; "
        "OAM_SLOT_STRIP=0x30; DIVISOR_COLS=10."),
    ("FUN_080d0150", "render_card_list_oam_row_by_pack_column",
        "Card-list OAM row render branch for pack_column variant (scene_pack). "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 7. "
        "Reads gPrng[0x148] as frame count r6; reads gFontState[0x0a18] bits[23:16] "
        "as pack_col_count [0..2]; divisor = 2-pack_col_count [1..2]. "
        "First __divsi3: col_offset = r6 / (2-pack_col_count). "
        "Checks col_offset against threshold 3 (cmp r0,#3; bgt) for mod-8 check. "
        "Second __divsi3: computes second-dimension column coordinate. "
        "Outputs OAM row position via shared tail. No direct OAM write in body. "
        "No APCS inputs; r8 loaded internally from DAT. "
        "Constants: PACK_COL_OFFSET=0x0a18 bits[23:16] [0..2]; "
        "PRNG_FRAME_OFFSET=gPrng+0x148; DIVISOR_MAX=2; MOD_THRESHOLD=3."),
    ("FUN_080ce2f4", "render_card_list_oam_row_by_type_icon",
        "Card-list OAM row render branch for type_icon variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 6. "
        "Reads gFontState[0x0a03] row count; gFontState[0x0a04] halfword x_base. "
        "Reads gFontState[0x0a18] bits[23:8] (mask 0xff<<9): 0 -> icon_base=4; nonzero -> 3. "
        "Reads gFontState[0x0a1b] bits[1:0] slot_state. "
        "slot_state<=1: iterates up to slot_count (gFontState[0x0a10] halfword bits[23:16]) "
        "icons; each icon: calls write_oam_entry_from_packed_args "
        "(slot=0x40, attr0=0x1e, tile_x=(slot_idx+1)*2+x_base). "
        "slot_state>1: writes extra OAM entry (attr1=0xc0<<1). "
        "No APCS inputs. "
        "Constants: ROW_OFFSET=0x0a03; X_BASE_OFFSET=0x0a04; "
        "TYPE_FIELD_OFFSET=0x0a18 bits[23:8]; SLOT_COUNT_OFFSET=0x0a10 bits[23:16]; "
        "SLOT_STATE_OFFSET=0x0a1b [0..1]; ATTR0_ICON=0x1e; OAM_SLOT=0x40."),
    ("FUN_080cd454", "render_card_list_oam_row_by_single_slot",
        "Card-list OAM row render branch for single_slot variant. "
        "Sibling of render_card_list_oam_row_by_dual_slot (0x080cdba8); "
        "called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 9. "
        "Same callee set (__divsi3 x2, write_oam_entry_from_packed_args x2, "
        "write_oam_entry_with_slot_check x3+). "
        "Key differences from dual_slot: divisor=0xb8=184 (vs 0xc8=200); "
        "OAM Y base = y_coord+0x2a=42 (vs +0x1c=28); "
        "extra condition fields at DAT+0x0a14/0x0a18/0x0a1c determine 4th OAM entry "
        "(write_oam_entry_from_packed_args attr2=0x80). "
        "gFontState base loaded internally into r10; no APCS inputs. "
        "Constants: CARD_REG_OFFSET=0x0201fe4e; DIVISOR=0xb8; OAM_Y_BASE=+0x2a; "
        "SLOT_STATE_OFFSET=0x0a1b; ATTR2_EXTRA=0x80; OAM_SLOT=0x60."),
    ("FUN_080cd0dc", "render_card_list_oam_row_by_cost_bar",
        "Card-list OAM row render branch for cost_bar variant. "
        "Called by dispatch_card_list_oam_row_by_card_type (0x080c7638) case 8. "
        "Nearly byte-identical to render_card_list_oam_row_by_pack_slot (0x080d05e4); "
        "differs only in literal pool constants (different DAT offsets). "
        "Reads gFontState[0x0a03] row count; OAM Y=(10-row/2)*8. "
        "Reads gFontState[0x0a1b] bits[1:0] slot_state [0..1]; if >1 skips. "
        "For state 0..1: reads gFontState[0x0a0e] halfword*2 as x_index (lsls #1); "
        "subtracts 0x17, adds gFontState[0x0a04] halfword for Y adjust. "
        "Calls write_oam_entry_from_packed_args (slot=0x60, attr0=0x34). No APCS inputs. "
        "Constants: ROW_OFFSET=0x0a03; SLOT_STATE_OFFSET=0x0a1b [0..1]; "
        "X_INDEX_OFFSET=0x0a0e; Y_ADJUST_OFFSET=0x0a04; ATTR0=0x34; OAM_SLOT=0x60."),

    # 2026-05-10: campaign-33 batch #33 (topo=723-736)
    ("FUN_080c82e4", "tick_card_list_display_master",
        "Card-list display master tick; called once per frame by tick_card_list_scene_frame (0x080c8688). "
        "Reads gFontState+0x0a17 byte, combines bits to form mode index r4=(bit0<<7)|(bits[7:1]). "
        "r4=0: call dispatch_card_list_oam_row_by_card_type (10-case card-type OAM row dispatch); "
        "r4=1: call dispatch_card_display_state_by_mode (7-case display mode dispatch); "
        "r4>=2: read gFontState+0x0a01 card_type byte, enter 14-entry switchD table at 0x080c8384, "
        "call corresponding render_card_list_oam_row_by_* sibling. "
        "No direct IO/VRAM writes; all side effects in callees. "
        "Constants: FONT_STATE_BASE=0x0201f440; STATE_BYTE_OFFSET=0x0a17; "
        "CARD_TYPE_OFFSET=0x0a01; SWITCH_TABLE=0x080c8384 (14 entries)."),
    ("FUN_080c7ba8", "render_card_list_face_row_by_mode",
        "Card-list face tile row renderer; called by tick_card_list_scene_frame (0x080c8688). "
        "Reads gFontState+0x0a18 word; extracts bits[24:15] via lsls #0xf/lsrs #0x18 -> mode [0..2]. "
        "mode=0: iterate row_count rows, write 3 strh tile entries per row to VRAM 0x0600f020+offset; "
        "tile IDs: top=0x013f, mid=0x0141, bot=0x01a2/0x01a3. "
        "mode=1: reverse layout variant, tile IDs 0x01a3/0x01a1/0x0143. "
        "mode=2: third variant. "
        "Side effects: [gFontState+0x0a18] row counter updated; "
        "[0x0600f000+offset]/[0x0600f00a+offset] strh tile IDs written (BG VRAM). "
        "Constants: FONT_STATE_BASE=0x0201f440; MODE_OFFSET=0x0a18; "
        "TILE_TOP=0x013f; TILE_MID=0x0141; TILE_BOT=0x01a2; VRAM_BASE=0x0600f020."),
    ("FUN_080c7af8", "copy_card_frame_tiles_by_type",
        "Copy ROM card frame tile data to OBJ VRAM, then computed-goto to per-type inline tile data. "
        "Called by tick_card_list_scene_frame (0x080c8688). "
        "Step 1: copy_bytes_by_halfword(dst=0x0600a7c0, src=0x09889fd8, count=0x120 bytes) -> write frame tiles. "
        "Step 2: read gFontState+0x0a01 card_type [0..13]; out-of-range -> return r0=1. "
        "Step 3: lsls r0,#2 -> index into PTR_PTR_080c7b2c (14-entry table); "
        ".hword 0x4687 = mov pc,r0 (THUMB computed-goto) -> jump to inline case segment. "
        "Side effects: [0x0600a7c0..0x0600a8df] OBJ VRAM written; per-case inline VRAM writes. "
        "Constants: VRAM_FRAME=0x0600a7c0; ROM_TILE_SRC=0x09889fd8; COPY_SIZE=0x120; "
        "CARD_TYPE_OFFSET=gFontState+0x0a01 [0..13]; JUMP_TABLE=0x080c7b30 (14 entries)."),
    ("FUN_080c841c", "render_card_list_face_row_by_mode_alt",
        "Card-list face tile row renderer, alt variant of render_card_list_face_row_by_mode (0x080c7ba8). "
        "Called by tick_card_list_scene_frame (0x080c8688); structure fully symmetric to 0x080c7ba8. "
        "Same mode extraction (lsls #0xf/lsrs #0x18 -> mode [0..2]), same tile IDs (0x013f/0x0141/0x01a2/0x01a3). "
        "Key difference: VRAM base 0x0600f00a (mode=0) vs 0x0600f000 (mode=1/2) "
        "vs 0x080c7ba8 which uses 0x0600f020 -- renders a different horizontal tile column. "
        "Side effects: [gFontState+0x0a18] row counter; [0x0600f00a+offset]/[0x0600f000+offset] strh writes. "
        "Constants: FONT_STATE_BASE=0x0201f440; MODE_OFFSET=0x0a18; "
        "VRAM_BASE_M0=0x0600f00a; VRAM_BASE_M12=0x0600f000."),
    ("FUN_080c8688", "tick_card_list_scene_frame",
        "Card-list scene per-frame tick; called by scene dispatch hub (FUN_0801e984). "
        "Step 1: check gP1LifePoints+0x1d08 (LP existence); 0 -> skip init, go to sort path. "
        "Step 2: read gPrng+0x214 low 31 bits, bl __divsi3(divisor=0x3c=60); "
        "quotient > 0xb3=179 -> update gFontState+0x0222: clear bits[3:2] (AND ~0xd), set bit2 (OR 0x4). "
        "Step 3: read gFontState+0x0a18 combo word, call FUN_0810e5c8 (card image load check). "
        "Step 4: if FUN_0810e5c8 nonzero: clear gFontState+0x0a1b bit0, +0x0a1c bit1, +0x0222+r3 bit1, +0x0215 bit0. "
        "Step 5: bl sort_zone_oam_entries_to_vram. "
        "Step 6: bl tick_card_list_display_master (0x080c82e4). Returns r0=1 (frame_processed). "
        "Constants: LP_EXIST_OFFSET=0x1d08; gPrng+0x214; DIVISOR=0x3c; THRESHOLD=0xb3; "
        "FONT_BYTE_OFFSET=0x0222; OAM_ROW_OFFSET=0x0a17."),
    ("FUN_08094540", "set_tile_palette_index_in_buf",
        "Write palette index into EWRAM tile attribute buffer entry. "
        "r0=tile_slot [0..255]; r1=palette_index (u8, written to halfword bits[15:8]). "
        "Guard: slot > 255 -> return without write. "
        "Target halfword addr: [0x0201e4f0 + 0x410 + 2*slot]. "
        "Operation: ldrh -> ands 0x1f (keep bits[4:0] = tile index) -> OR (r1<<8) -> strh. "
        "No return value (void); side effect only. "
        "Called by duel_field tile attr init callers (indeg=5). "
        "Constants: BUF_BASE=0x0201e4f0; TILE_ATTR_OFFSET=0x410; TILE_IDX_MASK=0x1f; PAL_SHIFT=8."),
    ("FUN_08094290", "get_clamped_tile_row_count",
        "Read tile_row_phase from [0x0201e4f0+0x4] and clamp to valid display offset range. "
        "Caller: check_field_scroll_phase_ready (0x080d25e0) and FUN_080d2ef4. "
        "Clamp rules: value <= 5 -> return 0; "
        "[6..37] -> return value-6 [0..31]; "
        "[38..71] -> return value-39; "
        ">71 -> return min(value, [0x0201e4f0+0xc]). "
        "Leaf function (bx lr); no side effects (pure read). "
        "Constants: STATE_BASE=0x0201e4f0; TILE_ROW_PHASE_OFFSET=0x4; "
        "RANGE1_MAX=5; RANGE2=[6..37]; RANGE3=[38..71]."),
    ("FUN_080d25e0", "check_field_scroll_phase_ready",
        "Check if duel field scroll animation phase satisfies advance condition. "
        "Called by FUN_080d136c / FUN_080d2ef4 / FUN_080d4478. "
        "Reads [0x0201e4f0+0x4] (phase_counter); dispatches by range: "
        "[0..5]: return 0 (too early). "
        "[6..37]: read scroll_flag [0x02020160+0x2e40]; if 0 -> return 0, else -> return 1. "
        "[38..71]: same scroll_flag + compare against get_clamped_tile_row_count (0x08094290); "
        "if scroll_flag < clamped_count -> return 0, else -> return 1. "
        "[>71]: return 1 (phase complete). "
        "Returns 1=ready_to_advance / 0=not_ready. Callee: get_clamped_tile_row_count. "
        "Constants: PHASE_BASE=0x0201e4f0; PHASE_OFFSET=0x4; "
        "SCROLL_FLAG_ADDR=0x02024fa0 (=0x02020160+0x2e40)."),
    ("FUN_080d0784", "check_zone_slot_attr_visible",
        "Check if duel field zone slot card attribute satisfies visibility condition (indeg=14). "
        "r0=slot_index; computes gDuelCtx+0x24+slot*0x28 (stride 5*8=0x28). "
        "Reads card_type byte at [addr+0]; reads phase_counter [0x0201e4f0+0x4] and "
        "active_zone_card [0x0201e2a0+0x4]. "
        "phase_counter==4: if card_type==active_zone_card -> return 0 (not visible). "
        "Otherwise: bl get_zone_card_attribute_by_type(card_type, attr_type=0xf). "
        "Returns 1=attribute satisfied (visible) / 0=not satisfied. Read-only; no side effects. "
        "Constants: DUEL_CTX=0x02020160; CARD_TYPE_OFFSET=0x24; STRUCT_STRIDE=0x28; "
        "PHASE_BASE=0x0201e4f0; ACTIVE_ZONE_BASE=0x0201e2a0; ATTR_TYPE=0xf."),
    ("FUN_080d3830", "render_zone_slot_card_icon_tile",
        "Render card icon tile for duel field zone slot to OBJ VRAM (indeg=4). "
        "r0=slot_index; reads gDuelCtx+0x2f53 card_status byte; "
        "extracts bits[7:5] (high 3) and bits[4:0] (low 5); "
        "if combined==0 -> direct write to OAM addr (zero-vector path). "
        "Else: copy slot card metadata (9 words via ldmia/stmia); "
        "compute slot_mod5 = slot_index % 5 (bl __modsi3); "
        "VRAM row offset = (slot_mod5*4 + 0x1e0) << 5; "
        "bl tile_2d_row_copy(src, row=0, width=4, height=2) -> write 4x2 icon block to OBJ VRAM 0x06010000. "
        "No return value (void); side effects: OBJ VRAM 0x06010000+row_offset written. "
        "Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_MASK=0x1f; "
        "STRIDE=0x28; MOD_DIVISOR=5; TILE_VRAM=0x06010000; TILE_WIDTH=4; TILE_HEIGHT=2."),
    ("FUN_080d08a4", "render_zone_card_detail_panel",
        "Full render pipeline for duel field selected zone card detail panel (indeg=2). "
        "8 sequential steps: "
        "(1) copy_bytes_by_halfword(dst=0x0600b0e0, src=0x0988ad78, size=0x3e0) -> BG tile frame; "
        "(2) copy_bytes_by_halfword(dst=0x05000160, src=0x0988b158, size=0x40) -> OBJ palette; "
        "(3) setup_line_buf_with_font_and_align(font=0x1b, align=2, flag=1, param=0) -> JP font; "
        "(4) read gDuelCtx+0x6c2c+0x2e40 bits[2:0] (card_attr) -> update card_info_ctx+0x8/+0x4; "
        "(5) text_render_wrapper x2 -> render two JP card name lines; "
        "(6) zero_fill_by_halfword(0x0600bc00, 0x6c0) + commit_line_buffer_to_sprite_vram -> sprite VRAM; "
        "(7) tile_2d_row_copy x10+ for card frame sub-regions; "
        "(8) game_str_id_to_row x3 + measure_string_pixel_width -> centered card description. "
        "No APCS input (void); callee-save r7/r6/r5 via .hword 0x4657/464e/4645. "
        "Constants: BG_TILE_DST=0x0600b0e0; PAL_DST=0x05000160; SPRITE_BUF=0x0600bc00; "
        "FONT_ID=0x1b; CARD_ATTR_OFFSET=gDuelCtx+0x6c2c+0x2e40; GAME_STR_ID=0x3e9."),
    ("FUN_080cad78", "render_zone_card_jp_text_panel",
        "Render duel field zone card JP text panel (card name + description); indeg=1. "
        "r0=card_str_base [0..N] (JP string lookup index). "
        "Step 1: bl zero_card_display_vram_regions -> clear old display. "
        "Step 2: copy_bytes_by_halfword(dst=0x06006340, src=0x0984f5cc, size=0x600) -> BG tile frame. "
        "Step 3: setup_line_buf_with_font_and_align(0x20, 2, 1, 2) -> JP font config. "
        "Step 4: read gDuelCtx+0x6c2c card_attr bits[2:0], update card_info_ctx+0x8/+0x4/+0x15. "
        "Step 5: card_str_variant = (r0+1) & 0xff | 0x8000; game_str page base = 0x3e8. "
        "Step 6: bl game_str_id_to_row -> text_render_wrapper (first JP line). "
        "Step 7: same for second JP line (text_render_wrapper r2=7). "
        "Step 8: bl commit_line_buffer_to_sprite_vram -> commit to OBJ tile VRAM. "
        "Constants: FONT_ID=0x20; CARD_ATTR_OFFSET=gDuelCtx+0x6c2c; "
        "GAME_STR_PAGE=0x3e8; DISPLAY_FLAG=0x8000; LINE2_OFFSET=7."),
    ("FUN_080d0818", "dispatch_zone_card_display_by_mode",
        "Duel field zone slot card display dispatcher by mode (indeg=5). "
        "r0=slot_index; r1=display_mode [0..1]. "
        "Step 1: compute gDuelCtx+0x24+slot*0x28 -> read card_status/card_attr/card_type bytes. "
        "Step 2: build OAM_attr0 halfword and strh to stack temp slot. "
        "Step 3: .hword 0x4684=mov r12,r0 saves slot_index; ldmia/stmia copies 9 slot words to stack. "
        "Step 4: strh 0 to [0x02023130+8] -> clear display_pending_flag. "
        "Step 5: compare r1 (display_mode): "
        "mode=0 -> if slot card_id matches gDuelCtx active_card_id: "
        "bl render_zone_card_jp_text_panel(r0=1); else bl render_large_card_display_by_mode. "
        "mode=1 -> bl render_zone_card_jp_text_panel(r0=1). "
        "No return value (void). "
        "Constants: DUEL_CTX=0x02020160; SLOT_STRIDE=0x28; CARD_STATUS_OFFSET=0x24; "
        "DISPLAY_FLAG_ADDR=0x02023130+8; MODE_LARGE=0; MODE_JP=1."),
    ("FUN_080d2c60", "tick_zone_card_detail_view",
        "4-state machine tick for duel field zone card detail view (indeg=1). "
        "Called by FUN_080d2ef4 (duel scene outer state machine). "
        "Reads [gDuelCtx+0x2f4e] view_state byte; dispatches: "
        "state=0 (fade-in): bl tick_duel_field_fadein_step; on done: open_card_info_page_from_list, "
        "set gFontState+0x0222 bit4, strh [WIN0H=0x04000004]=0x28f0, increment view_state. "
        "state=1 (card info page): bl tick_card_info_page_by_state; on done: increment view_state. "
        "state=2 (rebuild field): read slot card_id, bl init_duel_field_vram_layout, "
        "bl render_zone_card_detail_panel (0x080d08a4), bl check_zone_slot_attr_visible (0x080d0784), "
        "bl dispatch_zone_card_display_by_mode (0x080d0818), apply_palette_offset_to_tile_row, "
        "write WIN0H/WIN0V/WININ, increment view_state; return 1. "
        "state=3 (fade-out): bl tick_duel_field_fadeout_step; on done: clear gFontState+0x0222 bits[4:0], "
        "increment view_state; return 1. "
        "other: write [gDuelCtx+0x2f4e]=0 (reset), return 0. "
        "Returns r0: 1=state_advanced / 0=waiting_or_reset. "
        "Constants: DUEL_CTX=0x02020160; VIEW_STATE_OFFSET=0x2f4e; WIN0H=0x04000004; "
        "WIN0H_VAL=0x28f0; CARD_PAGE_BUF1=0x0203eeb0; CARD_PAGE_BUF2=0x02029eb0."),
    # --- batch #34 (campaign-34) ---
    ("FUN_080d1bb4", "dispatch_zone_card_anim_by_type",
        "Called by tick_zone_card_anim_state (0x080d2390) at phase=2 and by FUN_080d4268 directly. "
        "Extracts bits[7:5] from gDuelCtx+0x2f53 as card_high, bits[4:0] from gDuelCtx+0x2f54 shifted left 3, "
        "ORs to form type_combined [0..6]; if >6 jumps to LAB_080d21ce (error path). "
        "Indexes PTR_DAT_080d1c10 (7-entry function pointer table), loads target into r8, tail-calls via bx r8. "
        "Side effects: indirect VRAM/OAM writes through 7 sub-handlers. "
        "Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_OFFSET=0x2f54; "
        "CARD_WORD_OFFSET=0x2f58; JUMP_TABLE_PTR=0x080d1c0c; TYPE_COUNT=7; "
        "TYPE_MASK_HIGH=bits[7:5]; TYPE_MASK_LOW=0x1f."),
    ("FUN_080d2390", "tick_zone_card_anim_state",
        "Uniquely called by advance_zone_card_anim (0x080d3820). "
        "Core state-machine tick for duel field zone card slot display. "
        "Reads phase byte [0x020230ad] (0=idle-check, 1=loading, 2=active/render). "
        "phase=1: promote to 2, return 1. "
        "phase=0: check gPrng+0x148 bit6/bit7/bit5/bit4/bit2 card attr flags; "
        "conditionally call sync_state_and_init_sprite or write gDuelCtx+0x2f54/0x2f51/0x2f4d fields. "
        "phase=2: call dispatch_zone_card_anim_by_type. "
        "All paths return r0=1 (frame-processed). "
        "Constants: DUEL_CTX=0x02020160; SCENE_PHASE_ADDR=0x020230ad; PRNG_CARD_FLAGS=gPrng+0x148; "
        "FLAG_BIT6=0x40; FLAG_BIT7=0x80; FLAG_BIT5=0x20; FLAG_BIT4=0x10; FLAG_BIT2=0x2; "
        "ATTR_OFFSET1=0x2f54; ATTR_OFFSET2=0x2f51; ATTR_OFFSET3=0x2f4d."),
    ("FUN_080d3820", "advance_zone_card_anim",
        "2-instruction stub called by FUN_080d2ef4 at zone card slot type=1 branch. "
        "bl tick_zone_card_anim_state (0x080d2390) to advance the slot animation state machine, "
        "then b exit_zone_tick_frame (0x080d3828) to pop FUN_080d2ef4 frame and return to its caller. "
        "Inherits r0=1 (frame-processed) from tick_zone_card_anim_state unchanged. "
        "GBA inline exit-stub pattern: single operation then shared pop+bx exit."),
    ("FUN_080d3826", "signal_zone_tick_done",
        "Shared 'return done' exit stub for FUN_080d2ef4 (duel zone card slot state dispatcher). "
        "FUN_080d2ef4 branches here (b FUN_080d3826, not bl) from at least 11 sites to signal "
        "'this frame slot processing complete'. "
        "movs r0,#0x1 sets return value = 1 (done), then falls through to exit_zone_tick_frame (0x080d3828) "
        "to pop FUN_080d2ef4 frame and return to FUN_080cc340 (which interprets r0=1 as non-busy). "
        "Constants: DONE=1."),
    ("FUN_080d2a08", "dispatch_zone_card_anim_by_type_alt",
        "Called by FUN_080d2ef4 at zone card attr-code=6 branch. "
        "Symmetric partner of dispatch_zone_card_anim_by_type (0x080d1bb4) using different row-offset field. "
        "Extracts bits[7:5] from gDuelCtx+0x2f53 and bits[4:0] from gDuelCtx+0x2f54 shifted left 3 "
        "to form type_combined [0..6]; if >6 jumps to LAB_080d2c54 (error path). "
        "Uses gDuelCtx+0x2f56 (vs 0x2f58 in primary) for row offset, validates zone index from gDuelCtx+0x2f4f. "
        "Indexes PTR_DAT_080d2aa0 (7-entry table), tail-calls via bx r8. "
        "Side effects: VRAM/OAM writes through 7 sub-handlers (INCBIN 0x080d2abc..0x080d2c54). "
        "Constants: DUEL_CTX=0x02020160; CARD_STATUS_OFFSET=0x2f53; CARD_LOW_OFFSET=0x2f54; "
        "ROW_OFFSET=0x2f56; ZONE_OFFSET=0x2f4f; JUMP_TABLE_PTR=0x080d2a9c; TYPE_COUNT=7; LOW_MASK=0x1f."),
    ("FUN_080d3828", "exit_zone_tick_frame",
        "Shared frame exit stub for FUN_080d2ef4 (duel zone card slot state dispatcher). "
        "FUN_080d2ef4 enters via 'b FUN_080d3828' (preserving current r0) from multiple paths. "
        "3 instructions: pop {r4,r5,r6,r7} restores FUN_080d2ef4 callee-saves; "
        "pop {r1} retrieves saved LR; bx r1 returns to FUN_080d2ef4 caller with r0 unchanged. "
        "r0 on entry = 0 (busy/waiting) or 1 (done/advanced), set by caller before branching here. "
        "FUN_080d3826 (signal_zone_tick_done) fall-through -> here; "
        "advance_zone_card_anim (0x080d3820) tail-jumps here. "
        "Standard THUMB 'shared function exit' pattern matching FUN_080d2ef4 push {r4,r5,r6,r7,lr}."),

    # batch #35 (campaign-35) -----------------------------------------------
    ("FUN_080d1088", "render_zone_card_anim_oam_frame",
        "Synthesizes type_combined from gDuelCtx+0x2f53/0x2f54 (bits[7:5]<<3 | bits[4:0]&0x1f); "
        "if type_combined==0 exits (null path). Otherwise reads gDuelCtx+0x2f58 (card zone type [0..5]) "
        "and branches into 4 OAM write paths (type 0->LAB_080d117e, 1->LAB_080d120c, 2->LAB_080d122c, "
        "3->LAB_080d1250). Each path reads gPrng+0x83*4 halfword bits[7:4] % 3 or & 1 to generate anim "
        "frame offset, then calls write_oam_entry_from_packed_args. LAB_080d1280 reads gDuelCtx+0x2f56 "
        "halfword bits[12:5] as zone slot encoding for OAM Y coordinate (read-only). "
        "Called by render_zone_card_anim_dual_pass (0x080d1b2c) as first render pass. "
        "Side effects: OAM writes via write_oam_entry_from_packed_args + write_oam_entry_with_slot_check. "
        "Constants: gDuelCtx=0x02020160, status_offset=0x2f53, low_offset=0x2f54, word_offset=0x2f58, "
        "slot_encode_offset=0x2f56 (read-only), gPrng anim_seed_offset=0x83*4=0x20c, oam_size=0x80."),
    ("FUN_080d0c7c", "render_zone_card_anim_oam_frame_alt",
        "Alt variant of render_zone_card_anim_oam_frame (0x080d1088). Same: reads gDuelCtx+0x2f53/0x2f54 "
        "to synthesize type_combined. Difference: if type_combined!=0, applies 'subs r1,r0,#5' (minus-5 "
        "offset) then checks r1>0 to enter multi-column OAM write logic (LAB_080d0cf6) with col_count=0x10 "
        "and col_step=0x54. Called by render_zone_card_anim_dual_pass (0x080d1b2c) as fallback when "
        "type_combined>5. Side effects: OAM writes via write_oam_entry_from_packed_args. "
        "Constants: gDuelCtx=0x02020160, status_offset=0x2f53, low_offset=0x2f54, word_offset=0x2f58, "
        "col_count=0x10, col_step=0x54."),
    ("FUN_080d07cc", "check_zone_anim_id_in_table",
        "Linear search in gDuelCtx+0x2e00 (gDuelCtx+0xb8*0x40) halfword array for entry matching r0. "
        "Array length read from gDuelCtx+0x2e40 (gDuelCtx+0xb9*0x40). Compares each [gDuelCtx+0x2e00+i*2] "
        "with r4 (=r0 input); sets r5=1 on match. Returns r5 (1=found, 0=not_found). "
        "Called exclusively by render_zone_card_anim_oam_with_base (0x080d136c). "
        "Side effects: read-only. "
        "Constants: gDuelCtx=0x02020160, anim_table_base=0x2e00 (0xb8*0x40), "
        "count_offset=0x2e40 (0xb9*0x40), entry_size=2."),
    ("FUN_0804ae18", "check_card_stat_field8_is_7",
        "Bool wrapper: calls get_card_extended_stat_field8(card_id); returns 1 if result==7, else 0. "
        "Sibling cluster with check_card_stat_field8_is_6 (0x0804ae04) and check_card_stat_field8_is_8 "
        "(0x0804ae2c); all called from equip/effect eligibility chains. "
        "Side effects: none. Constants: field8_target=7."),
    ("FUN_0804bb6c", "check_card_is_equip_target_eligible",
        "Given card_id, determines whether the card can be targeted by an equip spell (i.e. monster "
        "meets equip conditions). Steps: (1) check_card_stat_field8_is_7(card_id): field8==7 -> return 0 "
        "(fusion-exclusive excluded). (2) BST exclusion of specific card_id ranges and individual IDs: "
        "upper limit 0x18e0 (0xc7*0x20); low range excludes 0x15fc/0x1729/0x16ec and others. "
        "(3) get_card_special_group_code(card_id): special_group==2 or ==4 -> return 0. "
        "All checks pass -> return 1. Core filter for equip card placement chain. "
        "Side effects: none. "
        "Constants: field8_7_exclude=7, upper_card_id=0x18e0 (0xc7*0x20), "
        "excluded_ids=0x15fc/0x1729/0x16ec/0x18c9/0x1987/0x19ce/0x19ef, special_group_2/4=excluded."),
    ("FUN_0803bba4", "eval_equip_placement_full_check",
        "Full equip placement feasibility check for (player_side, card_id, use_toon_flag) triple. "
        "Chain: (1) check_card_is_equip_target_eligible(card_id): not eligible -> return 0. "
        "(2) check_card_has_equip_placement_type(card_id): no type -> special case path. "
        "(3) use_toon_flag (r2)==0 -> return 0. "
        "(4) check_card_stat_field8_is_6(card_id): not 6 -> return 0. "
        "(5) check_toon_world_equip_present(player_side): 0 -> return 0; nonzero -> return 1. "
        "Special case: card_id==0x160f -> count_paired_slots_with_field5_default; "
        "range [0x160f-5..0x164f] -> get_paired_card_id_by_variant + count_paired_slots. "
        "indeg=10. Side effects: none. "
        "Constants: equip_special_id=0x160f, paired_range_hi=0x164f, paired_range_lo=0x160a."),
    ("FUN_08037568", "check_zone_slot_equip_eligible_alt",
        "Alt variant of check_zone_slot_equip_eligible (0x08037434); structure fully symmetric, "
        "difference is zone table base: gDuelFieldP1_base=0x0201cab0 (vs 0x0201c8f8). "
        "Reads [player*0x868+slot_idx*4] slot word, extracts card_id bits[12:0], runs same "
        "five-step equip check chain. indeg=3. Side effects: none. "
        "Constants: zone_base=0x0201cab0, player_stride=0x868, slot_entry=4."),
    ("FUN_08031294", "find_hand_slot_idx_by_set_code_alt",
        "Iterates gP1LifePoints[player*0x868+0x1c] count and gP1LifePoints[player*0x868+0x5d0] "
        "array (entry_size=4), extracts set_code encoding (lsls #2/lsrs #0x18 + lsls #0x12/lsrs #0x1f) "
        "and compares with r1; returns slot index on match or -1 if not found. "
        "Alt variant of find_hand_slot_idx_by_set_code (count_offset=0x14, base=0x418); "
        "this function uses count_offset=0x1c / array_offset=0xba*8=0x5d0. "
        "Confirmed by PASSED count_hand_cards_by_field6_alt (0x08034020) using same offsets. "
        "Side effects: read-only. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, count_offset=0x1c, "
        "array_offset=0xba*8=0x5d0, entry_size=4."),
    ("FUN_08033a6c", "count_slots_equippable_by_state_code",
        "Counts zone slots across both players that can accept an equip card with the given state_code. "
        "Guard: count_field_copies_of_card(0x13f2)>0 -> return 0 (card 0x13f2 on field blocks). "
        "Main loop: player=[0,1] x slot=[0..4] over gDuelFieldSlots (0x0201c510), tests bit19=occupied; "
        "if player==r8 (target side) or slot[+8]!=0, calls get_slot_card_state_code(player, slot_idx) "
        "and compares with sp[0]=r1; on match calls check_slot_card_can_be_equipped; increments r9. "
        "Returns r9 (count). Called only by check_zone_slot_equip_eligible (0x08037434) at "
        "card_id==0x15b4 path with state_code=1. Side effects: read-only. "
        "Constants: guard_card_id=0x13f2, gDuelFieldSlots=0x0201c510, player_stride=0x868, "
        "slot_entry=0x14, slot_count=5."),
    ("FUN_08037434", "check_zone_slot_equip_eligible",
        "Reads zone slot [zone_player_id_bit0*0x868+slot_idx*4] from gDuelFieldP0 (0x0201c8f8), "
        "extracts bits[12:0] as card_id, runs full equip feasibility check. "
        "r0 (player_side) for toon_world/slot_chain sub-functions; r1 (zone_player_id) bit0 for zone "
        "table row select; r2 (slot_index [0..4]) as slot offset. "
        "Check chain: (1) check_card_is_equip_target_eligible(card_id). "
        "(2) check_card_has_equip_placement_type(card_id): fail -> eval_equip_placement_full_check. "
        "(3) lsls r0,r0,#0x11 (equip lock bit): set -> return 0. "
        "(4) check_card_stat_field8_is_6(card_id): not 6 -> eval_equip_placement_full_check. "
        "(5) check_toon_world_equip_present(player_side): 0 -> return 0. "
        "Special: card_id==0x14fc -> count_paired_slots; card_id==0x1578 -> gP1LifePoints flag bit. "
        "indeg=21, C_util_high. Side effects: none. "
        "Constants: zone_base_P0=0x0201c8f8, player_stride=0x868, slot_entry=4, bit_lock_shift=0x11, "
        "special_id_0x14fc, special_id_0x1578, equip_check_value=0xb, "
        "gP1LifePoints_bit17_offset=0x8e*2=0x11c."),
    ("FUN_0803123c", "find_hand_slot_idx_by_set_code",
        "Gets hand card count from gP1LifePoints[player*0x868+0x14], iterates "
        "gP1LifePoints[player*0x868+0x418] hand array (entry_size=4), extracts set_code encoding "
        "(lsls #2/lsrs #0x18 + lsls #0x12/lsrs #0x1f) and compares with r1; returns slot index on "
        "match or -1 (rsbs) if not found. Sibling of find_slot_idx_by_set_code (0x08031184, "
        "count_offset=0x10, base=0x260); differs in count_offset=0x14 / base=0x418. "
        "indeg=43, C_util_high. Side effects: read-only. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, count_offset=0x14, "
        "array_offset=0x83*8=0x418, entry_size=4."),
    ("FUN_08094398", "dispatch_effect_ctx_slot_by_zone_type",
        "Reads effect slot entry from gEffectContext+0x10 (=0x0201e500) at [+r0*4], then reads "
        "halfword from attr_table [0x0201e900+r0*2] and extracts bits[4:0] (zone_type). "
        "If zone_type-0xb in [0..4] (zone_type in [0xb..0xf], 5 valid values), jumps via 5-entry "
        "table at 0x080943d0; otherwise error path (r6=1, LAB_080943e4). "
        "Sole caller: render_zone_card_anim_oam_with_base (0x080d136c) at 0x080d170e. "
        "Side effects: indirect (by jump table handlers). "
        "Constants: gEffectContext=0x0201e4f0, slot_table=0x0201e500, "
        "attr_table=0x0201e900 (=0x0201e500+0x400), jump_table=0x080943d0, "
        "zone_type_valid_range=[0xb..0xf] (5 entries)."),
    ("FUN_080d136c", "render_zone_card_anim_oam_with_base",
        "Base-r9 variant of render_zone_card_anim_oam_frame: prologue loads gDuelCtx "
        "(DWORD_080d13ac=0x02020160) internally into r9 via '.hword 0x4689=mov r9,r1'; "
        "does not consume APCS r1 parameter. All gDuelCtx field reads use 'add r0,r9' with fixed "
        "offsets (0x2f53/0x2f54/0x2f57/0x2f58). Also calls check_zone_anim_id_in_table (0x080d07cc) "
        "and dispatch_effect_ctx_slot_by_zone_type (0x08094398). Void, no APCS params. "
        "Side effects: OAM writes via write_oam_entry_from_packed_args; "
        "[gDuelCtx+0x2e42+slot*2] := 0 via strh at 0x080d157c (slot=modsi3(zone_slot,5)). "
        "Constants: gDuelCtx=0x02020160, base_offsets={0x2f53,0x2f54,0x2f57,0x2f58}, "
        "r9=gDuelCtx (internal load)."),
    ("FUN_080d1b2c", "render_zone_card_anim_dual_pass",
        "Zone card animation two-pass OAM render wrapper. Entry reads gDuelCtx+0x2f51 bit4: "
        "if set, returns immediately (animation inactive). Otherwise calls in sequence: "
        "render_zone_card_anim_oam_frame (0x080d1088) and render_zone_card_anim_oam_with_base "
        "(0x080d136c) for two OAM write passes. Then re-evaluates type_combined from "
        "gDuelCtx+0x2f53/0x2f54: if <=5 and gDuelCtx+0x2f58 type also satisfies condition, "
        "calls render_zone_card_anim_oam_frame_alt (0x080d0c7c) as third path. "
        "Called exclusively by FUN_080d2ef4. Side effects: OAM writes (through three sub-functions). "
        "Constants: gDuelCtx=0x02020160, active_flag_offset=0x2f51, active_bit=bit4=0x10."),
    ("FUN_080942d0", "write_effect_ctx_slot_index",
        "Single write: stores r0 into gEffectContext+0x8 (effect slot index field). "
        "3 instructions (ldr+str+bx lr). Called by effect activation chains when binding target slot. "
        "Side effects: [gEffectContext+0x8] := r0. "
        "Constants: gEffectContext=0x0201e4f0, slot_index_offset=0x8."),
    ("FUN_080d2690", "dispatch_zone_card_anim_by_subtype",
        "Reads gDuelCtx+0x2f4e (subtype byte); if >6, jumps to error path (LAB_080d29f4, clears byte). "
        "Otherwise uses subtype*4 to index PTR_PTR_080d26b8 (7-entry function pointer table at "
        "0x080d26bc), loads target function pointer into r7, and tail-calls via '.hword 0x4687=bx r7'. "
        "7 cases cover handlers at 0x080d26d8..0x080d29f4. Complements dispatch_zone_card_anim_by_type "
        "(0x080d1bb4) which dispatches on type_combined; this dispatches on subtype. "
        "Called exclusively by FUN_080d2ef4. Side effects: indirect (by sub-handlers). "
        "Constants: gDuelCtx=0x02020160, subtype_offset=0x2f4e, jump_table=0x080d26bc, "
        "handler_count=7."),
    ("FUN_080d2634", "update_zone_anim_queue_entry",
        "Finds and updates matching entry in gDuelCtx+0x2dfe animation queue array. "
        "Queue length read from gDuelCtx+0x2e40 (0xb9*0x40); iterates entries (entry_size=2). "
        "r1==0 (clear mode): finds [entry+2]==r4, clears [entry+2] to 0, sets r3=1. "
        "r1!=0 (shift mode): copies [entry+2] to [entry+0]. "
        "After loop, if r3!=0: gDuelCtx+0x2e40 -= 1 (decrements queue length). "
        "Returns r3 (operation success flag). Called exclusively by FUN_080d2ef4. "
        "Side effects: [gDuelCtx+0x2dfe+i*2+2] := 0 (conditional clear); "
        "[gDuelCtx+0x2e40] -= 1 (conditional decrement). "
        "Constants: gDuelCtx=0x02020160, queue_base_offset=0x2dfe, count_offset=0x2e40, "
        "entry_size=2."),
    ("FUN_080d3dc4", "compare_zone_slot_card_stat_pair_win",
        "Third variant of compare_zone_slot_card_stat_pair sibling cluster. Symmetric structure; "
        "difference: 'success' path returns +9 (movs r0,#9) rather than a negative code; "
        "invisible path still returns -4. Compares r1 against 0x16/0x17; on mismatch ('win' case) "
        "at LAB_080d3e10 computes return value from card_stats_table via multi-level index "
        "add r0,r8/r9/r10 and stores to [r5]. This variant returns the 'win' status code (positive). "
        "Side effects: [r5] := 0x9 (stack-local slot write, not external EWRAM). "
        "Constants: win_code=0x9, no_vis_code=-4, sentinel_16=0x16, sentinel_17=0x17."),
    ("FUN_080d3d28", "compare_zone_slot_card_stat_pair_alt",
        "Alt variant of compare_zone_slot_card_stat_pair (0x080d3c8c). Fully symmetric structure: "
        "zero-extends r0/r1, loops 2x calling check_zone_slot_attr_visible, ldmia/stmia batch "
        "24 bytes, compares r1 with 0x16/0x17. Difference: uses different DAT constants "
        "(DAT_080d3d64=0x02020160) and different result code assignments: "
        "r1==0x16 -> rsbs r0=-1; r1==0x17 -> rsbs r0=-2 (vs 0x080d3c8c which returns -2/-3). "
        "Invisible path returns -4 identically. One of the three-member sibling cluster. "
        "Side effects: stack-local temporaries only, no external EWRAM/VRAM. "
        "Constants: same as compare_zone_slot_card_stat_pair."),
    ("FUN_080d3c8c", "compare_zone_slot_card_stat_pair",
        "Compares card stats of two zone slots (r0, r1 each u16 slot index, zero-extended) and "
        "returns a result code. Internal: r8=gDuelCtx, r9=card_stats_table, r10=internal DAT. "
        "Main loop 2x (r7=0,1): calls check_zone_slot_attr_visible for each slot; if visible, "
        "reads stat word (slot_id*5*8+base) via ldmia batch copy 24 bytes; compares original r1 "
        "with 0x16/0x17: 0x16 -> rsbs r0=-2; 0x17 -> rsbs r0=-3; else continue; "
        "visibility fail -> rsbs r0=-4. Sibling cluster with FUN_080d3d28 / FUN_080d3dc4; "
        "differs only in return code constants (-2/-3 vs -1/-2 vs +9). "
        "Side effects: ldmia/stmia batch writes to stack-local (not external). "
        "Constants: gDuelCtx=0x02020160, slot_stride=5*8=40, loop_count=2, "
        "sentinel_16=0x16, sentinel_17=0x17."),

    # batch #36 (campaign-36) -----------------------------------------------
    ("FUN_080d3b6c", "compare_zone_slot_visibility_pair",
        "Checks visibility relationship of two zone slots and returns a sort key. "
        "Called by sort_zone_slots_by_stat_insertion (0x080d403c) and "
        "sort_zone_slots_by_stat_quicksort (0x080d4148) as comparator during sort phase. "
        "r0, r1 each u16 slot_index (zero-extended via lsls/lsrs #0x10). "
        "Calls check_zone_slot_attr_visible for slot_a first; if not visible returns 1 (sort last). "
        "Then checks slot_b; if not visible jumps to LAB_080d3be4 returns -1. "
        "Both visible: reads card_stats from gDuelCtx (0x02020160) at stride=0x28, "
        "looks up compare_table (0x09832604) via ldrh, returns difference as compare key. "
        "Side effects: read-only (gDuelCtx + ROM table). "
        "Constants: gDuelCtx=0x02020160, card_stats_stride=0x28, compare_table=0x09832604."),
    ("FUN_080d3bf0", "compare_zone_slot_stat_with_type_alt",
        "Zone slot comparator with card type correction; returns sort key for zone sort pipeline. "
        "Called by sort_zone_slots_by_stat_insertion (0x080d403c) and "
        "sort_zone_slots_by_stat_quicksort (0x080d4148). "
        "Symmetric with compare_zone_slot_card_stat_pair (0x080d3c8c): push {r4-r7, lr}, "
        "high-reg save (0x4657/0x464e/0x4645); calls check_zone_slot_attr_visible for each slot; "
        "both visible: ldmia batch read 24 bytes card_stats; if r1 (slot_b raw)==0x16 returns -2; "
        "if 0x17 returns -3; else computes difference via card_stats_table. "
        "Invisible path returns -4 or 0x18. Side effects: read-only (IWRAM gDuelCtx + ROM). "
        "Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3e9c, "
        "card_type_range=[0x16..0x17], slot_stride=0x28."),
    ("FUN_080d3e50", "compare_zone_slot_card_stat_with_atk",
        "Zone slot comparator with ATK/DEF value correction; returns sort key. "
        "Called by sort_zone_slots_by_stat_insertion (0x080d403c) and "
        "sort_zone_slots_by_stat_quicksort (0x080d4148). "
        "Symmetric with compare_zone_slot_card_stat_pair cluster; difference: uses additional "
        "ATK/DEF offset tables (0x09e4f310 for type 0x16, 0x09e4f32c for type 0x17, "
        "0x09e4f2ac fallback). r5 loop_count=0 init; invisible path returns 0x18. "
        "End: r0=sp[0x2c]-r7[0x4] difference returned. "
        "Side effects: read-only (IWRAM/ROM). "
        "Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3e9c, "
        "atk_table_16=0x09e4f310, atk_table_17=0x09e4f32c, fallback=0x09e4f2ac, "
        "slot_stride=0x28, loop_count=2."),
    ("FUN_080d3f4c", "compare_zone_slot_card_stat_with_level",
        "Zone slot comparator with level/position offset correction; returns sort key. "
        "Called by sort_zone_slots_by_stat_insertion (0x080d403c) and "
        "sort_zone_slots_by_stat_quicksort (0x080d4148). "
        "Symmetric with compare_zone_slot_card_stat_with_atk but uses different table pointer "
        "(PTR_card_stats_table@080d3f94). r3=0 init; invisible path returns 0x27 (sentinel). "
        "Type [0x16..0x17] paths query 0x09e4f310/0x09e4f32c + sp[0x38] cache; "
        "0x17 path also reads 0x09e4f2ac[+0x5c] accumulated offset. "
        "End: r0=sp[0x2c]-r7[0x4] difference. Side effects: read-only. "
        "Constants: gDuelCtx=0x02020160, card_stats_table=PTR@080d3f94, "
        "atk_table_16=0x09e4f310, atk_table_17=0x09e4f32c, fallback_table=0x09e4f2ac, "
        "return_invisible=0x27."),
    ("FUN_080d403c", "sort_zone_slots_by_stat_insertion",
        "Insertion sort on zone slot id list; sorts slots by card stat descending. "
        "Called by sort_zone_slots_by_stat_quicksort (0x080d4148) as base case when count<=6. "
        "r0=slot_list_ptr (u16* array, 2 bytes/entry), r1=slot_count. "
        "Standard insertion sort: outer i=0..n-2; inner calls FUN_0810e5d0 (card stat comparator) "
        "for each pair; on swap: ldrh/strh exchange 2-byte slot ids. "
        "r9 (high-reg alias for gPrng+0x808 sliding ptr) used for compare table access; "
        "LAB_080d4100 performs strh swap on two halfwords. "
        "Side effects: strh writes to [gPrng+0x808+r6*2] and [gPrng+0x808+sp[0x4]] (slot id swap). "
        "Constants: gDuelCtx=0x02020160, queue_base=0x0201bcc0, queue_offset=0x808, "
        "swap_size=2, compare_fn=FUN_0810e5d0."),
    ("FUN_080d4148", "sort_zone_slots_by_stat_quicksort",
        "Quicksort on zone slot id list; sorts slots by card stat descending. "
        "Called by setup_zone_slot_sorted_view (0x080d4268); self-recursive. "
        "r0=slot_list_ptr (u16* array), r1=slot_count saved to sp[0x8]. "
        "count<=6 delegates to sort_zone_slots_by_stat_insertion (0x080d403c); "
        "else selects pivot arr[count/2+count%2], swaps with arr[0], partitions via "
        "FUN_0810e5d0 comparator, then recurses on left/right subarrays. "
        "High-regs r7/r6/r5/r8/r9/r10 callee-saved via .hword 0x4657/0x464e/0x4645. "
        "Side effects: strh slot id swaps in-place in slot_list_ptr array. "
        "Constants: insertion_threshold=6, compare_fn=FUN_0810e5d0."),
    ("FUN_080d4268", "setup_zone_slot_sorted_view",
        "Initializes zone slot sort and triggers card icon rendering. "
        "Called by tick_zone_card_list_state_machine (0x080d4478) when state==2. "
        "No explicit input params (r0-r3 overwritten by internal loads). "
        "Flow: (1) reads gDuelCtx+0x2f52 halfword bits[12:5] (0xff<<5 mask) for active slot count; "
        "if 0 goes to sort path; else reads gDuelCtx+0x2f57/0x2f58 for type_combined and compares "
        "with count: if count<type_combined clears VRAM 0x0601f000+i*2 (strh 0). "
        "(2) reads 0x2f57/0x2f58/0x2f53/0x2f54 type_combined2; if >0 calls "
        "dispatch_zone_card_anim_by_type. (3) loop calls render_zone_slot_card_icon_tile and "
        "load_card_list_small_image for each slot. "
        "(4) clears gDuelCtx+0x2f54 bits[12:5] and 0x2f56, calls dispatch_zone_card_display_by_mode. "
        "Side effects: strh writes VRAM 0x0601f000 (zero loop); "
        "gDuelCtx+0x2f54 &= 0xffe01fff; gDuelCtx+0x2f56 &= 0xffffe01f."),
    ("FUN_080d4478", "tick_zone_card_list_state_machine",
        "Single-frame update of zone card list display state machine. "
        "Called by tick_zone_card_list_view (0x080d2ef4) in zone main loop. "
        "Reads gDuelCtx+0x2f4d byte as state and dispatches: "
        "state=0: checks gPrng+0xa4*2 bit6 flag, calls check_field_scroll_phase_ready if needed, "
        "then writes gDuelCtx+0x2f54 bits[12:5]=0x60|0x20 and exits; "
        "state=1: calls setup_zone_slot_sorted_view (0x080d4268); "
        "state=2: calls setup_zone_slot_sorted_view. "
        "All paths write gDuelCtx+0x2f4d (state advance) and return 1 fixed. "
        "Side effects: strb gDuelCtx+0x2f4d (state); strh gDuelCtx+0x2f54 (display bits); "
        "strb gDuelCtx+0x2f51 bit1 (display enable). "
        "Constants: gDuelCtx=0x02020160, state_offset=0x2f4d, display_offset=0x2f54, "
        "gPrng_flag=0xa4*2=0x148, flag_bit6=0x40, flag_bit7=0x80, flag_bit5=0x20."),
    ("FUN_080d2ef4", "tick_zone_card_list_view",
        "Single-frame update of zone card list view; dispatches to sub-systems by gDuelCtx state. "
        "Called by invert_zone_tick_result (0x080cc340) in zone tick main loop. "
        "No explicit params; all state from gDuelCtx global. "
        "Flow: (1) reads gDuelCtx+0x2f53/0x2f54 type_combined (bits[7:5]<<3 | bits[4:0]); "
        "if >0 and <=5 calls dispatch_zone_card_anim_by_subtype + signal_zone_tick_done, "
        "clears gDuelCtx+0x2f54 bits (& 0xffffe01f), calls signal_zone_tick_done again. "
        "(2) type=4: calls dispatch_zone_card_anim_by_subtype; "
        "type=5: calls tick_zone_card_detail_view -> signal; "
        "type=6: calls dispatch_zone_card_anim_by_type_alt -> signal. "
        "(3) other: if gDuelCtx+0x2f54 bits[12:5] set calls render_zone_card_anim_dual_pass; "
        "type=1: advance_zone_card_anim; final calls exit_zone_tick_frame + "
        "tick_zone_card_list_state_machine (0x080d4478). "
        "Side effects: strh gDuelCtx+0x2f54 &= 0xffffe01f (multiple); "
        "signal_zone_tick_done/exit_zone_tick_frame indirect effects."),
    ("FUN_080cc340", "invert_zone_tick_result",
        "Bool-invert wrapper around tick_zone_card_list_view; propagates result upward. "
        "Called by tick_zone_display_frame (0x080cc528) in zone frame tick dispatcher. "
        "Body: push {lr}; bl tick_zone_card_list_view (FUN_080d2ef4); "
        "cmp r0,#0 beq LAB_080cc34e -> r0==0 returns 1 (pending); "
        "r0!=0 returns 0 (done). Converts tick_zone_card_list_view result "
        "(nonzero=done/exit) to 'is_pending' semantics (0=done, 1=continue). "
        "Side effects: none (only propagates return value). "
        "Constants: none."),
    ("FUN_080cc208", "tick_zone_detail_render_step",
        "Renders zone card detail panel and advances state counter. "
        "Called by tick_zone_display_frame (0x080cc528) in zone frame tick. "
        "Body: push {lr}; bl render_zone_card_detail_panel (no params); "
        "ldr gDuelCtx+0x2f4d; ldrb state; adds #1; strb state+1; movs r0,#1; pop bx. "
        "Fixed return 1. Side effects: strb gDuelCtx+0x2f4d (state counter +1). "
        "Constants: gDuelCtx=0x02020160, state_offset=0x2f4d."),
    ("FUN_080cc228", "tick_zone_detail_panel_by_anim_state",
        "Dispatches zone detail panel single-frame tick by animation type state. "
        "Called by tick_zone_display_frame (0x080cc528) in zone frame total dispatcher. "
        "Reads gDuelCtx+0x2f53/0x2f54 type_combined (bits[7:5]<<3 | bits[4:0]); "
        "type>0 and <=5 selects ROM ptr table 0x0988b434; type==0 selects 0x0988b178. "
        "Reads gDuelCtx+0x2f4d as sub_state; if sub_state in [0..6]: "
        "computes VRAM row 0x0600f00a+((8-sub_state)<<6), calls apply_palette_offset_to_tile_row "
        "twice (palette row writes); sub_state++ strb; returns 0. "
        "If sub_state>6: reads gDuelCtx+0x2f55/0x2f56 type_combined2 for second dispatch: "
        "0->dispatch_zone_card_display_by_mode; nonzero->same with check_zone_slot_attr_visible. "
        "Side effects: strb gDuelCtx+0x2f4d (+1); VRAM 0x0600f00a palette row writes. "
        "Constants: gDuelCtx=0x02020160, VRAM_base=0x0600f00a, table_hi=0x0988b434, "
        "table_lo=0x0988b178, sub_state_offset=0x2f4d."),
    ("FUN_080cc354", "tick_zone_field_info_panel",
        "Single-frame update of zone field info panel: animation tile writes and field info render. "
        "Called by tick_zone_display_frame (0x080cc528). "
        "Reads gPrng+0x1886*2 tile control bits: bit7=flip flag (r9), bits[6:0]=r7, bits[14:8]=r6. "
        "Reads gDuelCtx+0x2f53/0x2f54 type_combined; selects ROM table 0x0988b434 or 0x0988b178. "
        "Reads gDuelCtx+0x2f4d sub_state: "
        "0->double loop strh #0 clearing VRAM 0x0600f00a block; "
        "1..6->calls apply_palette_offset_to_tile_row twice per step; "
        "7->calls render_duel_field_zone_info + copy_bytes_by_halfword "
        "(0x050002e0 <- 0x0985329c, 0x20 bytes). Each case sub_state++ strb. Returns 0 or 1. "
        "Side effects: strb gDuelCtx+0x2f4d; strh VRAM 0x0600f00a area (zero or palette); "
        "OBJ PAL 0x050002e0 += 0x20 bytes (state 7 path). "
        "Constants: gDuelCtx=0x02020160, state_offset=0x2f4d, VRAM_base=0x0600f00a, "
        "OBJ_PAL_dst=0x050002e0, pal_src=0x0985329c."),
    ("FUN_080cc528", "tick_zone_display_frame",
        "Top-level zone display frame tick dispatcher; selects one sub-system per frame "
        "based on gDuelCtx animation state. Called by FUN_0801e984 (scene main dispatcher). "
        "Flow: (1) checks gP1LifePoints+0x1d08 (LP alive); if nonzero reads gPrng+0x85*4 "
        "random value, divides by 0x3c=60; if quotient>0xb3=179 sets gPrng+0x23130+0x222 bits |= 0x4. "
        "(2) reads gDuelCtx+0x2f4c (animation selector) and dispatches: "
        "0->sort_zone_oam_entries_to_vram + advance state; "
        "1->tick_zone_detail_render_step (0x080cc208); "
        "2->tick_zone_detail_panel_by_anim_state (0x080cc228); "
        "3..6->tick_zone_field_info_panel (0x080cc354); "
        "7->invert_zone_tick_result (0x080cc340). "
        "(3) calls sort_zone_oam_entries_to_vram at end. Returns 0 or 1. "
        "Side effects: strb gDuelCtx+0x2f4c (selector advance); "
        "strb gDuelCtx+0x2f4d; strb gPrng bits (random LP effect); "
        "gDuelCtx+0x2f51 &= ~2; gDuelCtx+0x2f52 &= ~5. "
        "Constants: gDuelCtx=0x02020160, selector_offset=0x2f4c, "
        "gP1LifePoints_LP_offset=0x1d08, gPrng_rand_offset=0x85*4=0x214, "
        "rand_threshold=0xb3=179, rand_div=0x3c=60, LP_flag_offset=0x23130+0x222."),
    ("FUN_08093598", "play_card_ok_ui_effect",
        "Plays UI sound effect for card confirm/OK action. "
        "Called by FUN_08094a28 (card/duel_field/prng scene dispatcher) and FUN_08094cd4 "
        "after card confirm/select operation. "
        "Body: push {lr}; movs r0,#0x31=49 (UI effect ID); bl play_ui_effect; pop {r1}; bx r1. "
        "Thin wrapper around play_ui_effect with fixed effect_id=0x31=49. "
        "Side effects: triggers sound effect ID 49 via play_ui_effect (indirect). "
        "Constants: CARD_OK_EFFECT_ID=0x31=49."),
    ("FUN_0801f3d4", "return_void_noop_stub",
        "No-op stub; executes bx lr immediately and returns. "
        "Called by enqueue_sprite_attr_record (0x0803bd2c) as 'entry committed' notification "
        "placeholder after writing four halfword sprite attributes. "
        "Identical single-instruction bx lr structure to return_void_noop (0x080fa4d8, batch #28). "
        "In release build this callback is optimized to empty. "
        "Address-adjacent siblings: FUN_0801f3d8 (movs r0,#0; bx lr), "
        "FUN_0801f3dc (bx lr), FUN_0801f3e4 (movs r0,#1; bx lr). "
        "Side effects: none."),
    ("FUN_0803bd2c", "enqueue_sprite_attr_record",
        "Writes four halfword sprite attributes (x, y, w, h) to IWRAM sprite attr queue "
        "at current write slot and advances write pointer. "
        "Called from 135 callsites across card image/OAM/menu/number-OAM rendering. "
        "First checks [0x0201e2a0+8]==3 (scene-switching/paused) and exits if true. "
        "Then reads write_ptr=[0x0201bcc0+0x808]; if >0xff (queue full) exits. "
        "Writes: strh r5(x)->[entry+0x8]; strh r6(y)->[entry+0xa]; "
        "strh r2(w)->[entry+0xc]; strh r3(h)->[entry+0xe]. "
        "Calls return_void_noop_stub (0x0801f3d4) as 'entry committed' notification; "
        "then write_ptr += 1. All four params zero-extended via lsls/lsrs #0x10. "
        "Side effects: strh [queue_entry+0x8..0xe] four fields; [queue_write_ptr] += 1. "
        "Constants: state_base=0x0201e2a0, queue_base=0x0201bcc0, queue_offset=0x808, "
        "capacity_max=0xff, entry_stride=8, pause_state=3."),
    ("FUN_080ed858", "write_sprite_row_to_vram_buffer",
        "Writes one row of sprite halfword data to VRAM display buffer; "
        "supports two row-count modes (<=6 single-channel / >6 dual-channel). "
        "Called by submit_sprite_row_data (0x08095498, indeg=14) and FUN_0802826e / "
        "FUN_08027c98 (player_profile) / FUN_080fa7e4 (font_jp). "
        "r0=dst_offset (saved to r8 via .hword 0x4680=mov r8,r0); r1=row_count (r7=row_count). "
        "Checks [0x03000000+0x18] (display ready flag); if 0 skips. "
        "If r7=(r1+1)/2 <=6: writes strh [gPrng+0x1c0+stride*r6] for each row. "
        ">6: same per-row writes but also toggles IME (0x04000208) off/on around gPrng+0x464 "
        "count update and sets gPrng+0x584 flag byte. "
        "Side effects: strh gPrng+0x464 region (<=6 path); "
        "IME toggle + str gPrng+0x46c count + strb gPrng+0x584 (>6 path). "
        "Constants: gPrng=EWRAM_base, display_ready=0x03000000+0x18, IME=0x04000208, "
        "buf_base=0x1c0, count_offset=0x46c, flag_offset=0x584."),
    ("FUN_080953c4", "dispatch_sprite_row_write_by_type",
        "Dispatches sprite row write request to appropriate path by sprite type code. "
        "Called by submit_sprite_row_data (0x08095498) and FUN_080954e8 (duel_field/font_jp). "
        "r0=sprite_type_raw [2..0x1f]; r1=direction [0..1] (saved as r2=type); "
        "r2=channel_or_mode (0 -> special branch). "
        "subs r0,#2 -> base offset; cmp #0x1d bhi -> default bx lr; "
        "lsls #2; ldr switch_table; computed-goto via 0x4687=mov pc,r7. "
        "Switch table 0x080953dc: 30 entries, two case targets. "
        "case 0x08095454: r2!=0 -> r10+r2*0xc0*4; lsls r3,#0xd; asrs #0x1c bits[18:15] "
        "inc/dec by direction; ands #0xf; lsls #0xf; ands+orrs r0,r3; str to 0x0201b870+channel*0x300. "
        "Side effects: str [0x0201b870+channel*0x300+offset] bits[18:15] modified. "
        "Constants: sprite_table_base=0x0201b870, channel_stride=0x300, "
        "switch_table=0x080953dc, entry_count=30."),
    ("FUN_08095498", "submit_sprite_row_data",
        "Assembles sprite row data into 256-byte stack buffer then submits to write pipeline. "
        "Called by indeg=14 scene dispatchers (card_data/duel_field/font_jp etc). "
        "r0=sprite_id (u16 zero-extend, stored to sp[0]); r1=row_offset (s16, -1 skips header); "
        "r2=src_data_ptr (u16* source); r3=halfword_count (0 skips copy). "
        "sub sp,#0x100 allocates 256-byte frame. "
        "If r1!=-1: strh row_offset -> sp[2]; r5=2, else r5=1. "
        "If r3>0: copy_bytes_by_halfword(sp+r5*2, src, r3); r5 += ceil(r3/2). "
        "Then: bl dispatch_sprite_row_write_by_type(sprite_id, 1); "
        "bl write_sprite_row_to_vram_buffer(sp, r5*2). "
        "Side effects: sp[0]=sprite_id; sp[2]=row_offset (conditional); "
        "sp[r5*2..] from src_data_ptr; indirect: dispatch_sprite_row_write_by_type + "
        "write_sprite_row_to_vram_buffer effects. "
        "Constants: SKIP_OFFSET=-1, stack_buf_size=0x100=256."),

    # --- batch #37 (campaign-37, 2026-05-10) topo 783-802 ---
    ("FUN_08095380", "pack_sprite_row_attr_words",
        "Packs four halfword fields (x_pos/y_pos/palette/flags) into two 32-bit sprite-row "
        "attribute words and submits them via submit_sprite_row_data with count=6. "
        "r0[15:0] | r1[15:0]<<16 forms first attr word; second attr word is built from sp[4] "
        "ANDed with DAT_080953bc, ORed with r2[15:0], ANDed with DAT_080953c0, ORed with r3[15:0]. "
        "Passes r1=-1 (full mask) and r2+2 (stride+2) to submit_sprite_row_data(base_ptr,-1,stride+2,6). "
        "Called by 5 card-display/duel-field callers as unified sprite row attribute merge entry. "
        "r0=u16 x_or_slot_word [0..0xffff]; r1=u16 y_or_attr_high [0..0xffff]; "
        "r2=u16 palette_or_stride [0..0xffff]; r3=u16 flags_or_tile [0..0xffff]; "
        "sp+4=u32 base_attr_word. Returns void (submit_sprite_row_data return transparent). "
        "Constants: submit count=6, stride=r2+2, AND masks DAT_080953bc/DAT_080953c0."),
    ("FUN_080c2880", "init_field_slot_aob_ctx_b",
        "Initialises duel_field slot AOB (animation object) context structure at 0x0201fe60 "
        "for dispatch_card_display_op case 0x0b. "
        "Writes r1[7:0]<<3 into [base+4][10:3] (palette field), r0 to [base+8], r2 to [base+c]. "
        "Calls init_aob_ctx_from_ptnsect([base+0x48], ptnsect_id, r1_dat, 1), then sets "
        "[base+0x5b] bit0 (init done). Reads gP1LifePoints[0x1ce8] vs (gDuelActivation[4]^player_id) "
        "to select anm_entry param (2 or 3) for init_aob_ctx_with_anm_entry. "
        "Clears high bits of [base+0]/[base+2] via AND mask. "
        "r0=ptr arg0 [0..0x03ffffff]; r1=u8 palette_slot [0..0xff]; r2=ptr arg2. Returns void. "
        "Constants: base_struct=0x0201fe60, mask=0xfffff807, gDuelActivation=0x0201e2a0."),
    ("FUN_080c3d00", "init_field_slot_ctx_zoom",
        "Initialises duel_field card zoom display context (DAT_080c3d1c, 0x1c halfwords=0x38 bytes) "
        "for dispatch_card_display_op case 0x1a (card zoom-in scene). "
        "Calls zero_fill_by_halfword(base, 0x1c), then writes r0 to [base+4] and r1 to [base+8]. "
        "r0=ptr ctx_src (zoom source descriptor); r1=ptr ctx_dst (zoom target descriptor). "
        "Returns void. "
        "Constants: base_struct=DAT_080c3d1c, zero_len=0x1c halfwords (0x38 bytes)."),
    ("FUN_080c8904", "refresh_all_zone_slot_tile_display",
        "Iterates all duel field zone slots for both players and refreshes tile display state; "
        "called as final sub-step of dispatch_card_display_op case 0x24. "
        "Outer loop r5=[0..1] (player_id); inner loop slot_type [0..4] then [5..10]. "
        "For each slot calls get_zone_slot_entity_ref_by_type; if null calls "
        "update_field_slot_tile_display(player, slot, 0). "
        "No APCS params (all data from globals). Returns void. "
        "Constants: gDuelZoneDisplay=0x02023130, slot_type_lo=[0..4], slot_type_hi=[5..10]."),
    ("FUN_080bc794", "init_field_slot_aob_ctx_a",
        "Initialises duel_field slot AOB context structure (DAT_080bc7d4, zero_len=0x6c halfwords=0xd8 bytes) "
        "for dispatch_card_display_op cases 0x01 and 0x21. "
        "Calls zero_fill_by_halfword(base, 0x6c), writes r0->[base+4], r1->[base+8], "
        "r2 (via mov r8,r2 / mov r0,r8)->[base+c]. Sets [base+0] bit0 (init done). "
        "Reads gP1LifePoints player bit, ORs 0x4, writes to external ctrl byte. "
        "r0=ptr arg_data; r1=ptr arg_target; r2=ptr arg_extra (saved via r8). Returns void. "
        "Constants: base_struct=DAT_080bc7d4, zero_len=0x6c halfwords=0xd8 bytes, player_flag_bit=0x4."),
    ("FUN_080c291c", "write_zone_oam_entry_with_flip",
        "Reads zone_type[2:0] and sub_idx[7:3] from slot struct (0x0201fe60), "
        "forms zone_oam_key = sub_idx<<5 | zone_type. "
        "If key nonzero selects r1 as flip param, else r0; writes to [base+0x10] and [base+0x14]. "
        "Reconstructs OAM coord from two bytes and writes to [base+0x18]. "
        "Sets ctrl bit2 at 0x02023345. Corresponds to dispatch_card_display_op case 0x0c. "
        "r0=u32 oam_param_a; r1=u32 oam_param_b; r2=u8 sub_packed [0..0xff]. Returns void. "
        "Constants: base_struct=0x0201fe60, ctrl_byte=0x02023345, zone_key_mask=sub_idx<<5|zone_type[2:0]."),
    ("FUN_080c4ea0", "init_field_slot_aob_ctx_c",
        "Initialises third variant of duel_field slot AOB context (DAT_080c4ed0, 0x1c halfwords=0x38 bytes) "
        "for dispatch_card_display_op case 0x19. "
        "Calls zero_fill_by_halfword(base, 0x1c), writes r0->[base+4], r1->[base+8]. "
        "Sets [base+0x19] bit1 (init_flag=0x2). "
        "Reads gP1LifePoints player bit, ORs 0x4, writes to external ctrl byte. "
        "r0=ptr arg_data; r1=ptr arg_target. Returns void. "
        "Constants: base_struct=DAT_080c4ed0, zero_len=0x1c halfwords, init_flag=0x2."),
    ("FUN_080c412c", "render_field_slot_card_tile_by_id",
        "Decodes packed slot descriptor (r0) to player_id/zone_type/sub_idx, "
        "calls get_field_slot_tile_vram_addr to find VRAM slot, reads cached card_id at +0x120. "
        "If cache empty: calls internal_card_id_to_card_id(r1) and writes result to cache, "
        "then calls ensure_card_id_cache_entry. Finally calls render_field_slot_card_tile. "
        "Corresponds to dispatch_card_display_op case 0x1b. "
        "r0=u32 slot_descriptor (bit0=player_id, bits[5:1]=zone_type, bits[13:6]=sub_idx); "
        "r1=u16 card_id_raw [0..0x1fff]. Returns void. "
        "Constants: VRAM_cache_offset=0x120 (0x90*2)."),
    ("FUN_080c2840", "write_field_slot_activation_mask",
        "Zero-fills field slot activation state structure (DAT_080c287c, 0x5c halfwords=0xb8 bytes) "
        "then writes two bit-fields from r0: r0[4:0]<<3 -> [base+3][5:3], r0[21:19]&0x7 -> [base+4][2:0]. "
        "Called in dispatch_card_display_op case 0x09 after build_slot_activation_mask_for_player. "
        "r0=u32 packed_slot_data (output of build_slot_activation_mask_for_player, "
        "effective bits [4:0] and [21:19]). Returns void. "
        "Constants: base_struct=DAT_080c287c, zero_len=0x5c halfwords=0xb8 bytes, "
        "mask_lo=0x1f (bit[4:0]), mask_hi=0x7 (bit[21:19])."),
    ("FUN_080c8f48", "init_card_effect_aob_ctx",
        "Initialises card-effect AOB context (DAT_080c8fb4, 0x4c halfwords=0x98 bytes) "
        "for dispatch_card_display_op case 0x06. "
        "Calls zero_fill_by_halfword(base, 0x4c), then classify_card_effect_category(r0) "
        "to get effect category byte. Writes category<<1 into gDuelActivation halfword bits[2:1]. "
        "Calls init_aob_ctx_from_ptnsect([base+0x38], ...). Sets [base+0x4b] bit0 (init done). "
        "Reads gP1LifePoints[0x1ce8] vs (gDuelActivation[4]^1) to select anm_entry param. "
        "r0=u16 card_id [0..0x1fff]. Returns void. "
        "Constants: base_struct=DAT_080c8fb4, zero_len=0x4c halfwords=0x98 bytes, "
        "gDuelActivation=0x0201e2a0, category_mask=0xff."),
    ("FUN_080c786c", "zero_card_name_vram_buf",
        "Clears 32KB card name VRAM buffer (DAT_080c7888) via zero_fill_by_halfword(base, 0x4000). "
        "Called by copy_game_text_to_card_name_vram before writing text tiles. "
        "Writes ctrl ready flag 0x0b to external ctrl byte after clearing. "
        "No APCS params (all addresses loaded from DAT). Returns void. "
        "Constants: vram_buf=DAT_080c7888, zero_len=0x4000 halfwords=0x8000 bytes (32KB), ctrl_val=0x0b."),
    ("FUN_080c7950", "copy_game_text_to_card_name_vram",
        "Writes game string to card name VRAM buffer for dispatch_card_display_op case 0x31. "
        "Calls zero_card_name_vram_buf to clear 32KB, then resolve_game_str_ptr(r1) twice "
        "(validity check and pointer fetch); if valid calls copy_cstr_to_buf(vram_base+1, str_ptr). "
        "r0=u32 zone_descriptor [0..0xffffffff]; r1=u16 game_str_id [0..0xd7ea]; "
        "r2=u32 extra_flags [0..2]. Returns void. "
        "Constants: vram_base=DAT_080c7984, vram_offset=+1 (skip first halfword)."),
    ("FUN_08094314", "get_duel_activation_zone_id",
        "Three-instruction leaf: ldr ptr from DAT_0809431c, ldr [ptr+0xc], bx lr. "
        "Returns current activated zone ID from global duel activation state structure. "
        "No APCS params. Returns u32 zone_id. Pure read, no side effects. "
        "Callers: build_field_zone_display_state (0x080cbf58), "
        "FUN_080bb414 (duel_field zone activation), FUN_08057c28. "
        "Constants: ptr=DAT_0809431c, zone_id_offset=0xc."),
    ("FUN_080cbf58", "build_field_zone_display_state",
        "Builds complete duel field zone display state for dispatch_card_display_op case 0x32. "
        "Zero-fills gDuelZoneState (0x02020160, 0x2f5c halfwords=0x5eb8 bytes). "
        "Extracts zone_id from r0[7:0], writes <<13 into [base+0x2f50][20:13], sets [base+0x2f51] bit0, "
        "sets ctrl [0x02023345] bit2. Calls get_duel_activation_zone_id, decodes zone class bits, "
        "writes [base+0x2f57]/[base+0x2f58] zone category fields. "
        "Inner loop: for each slot calls ensure_card_id_cache_entry + find_zone_descriptor_by_slot_id "
        "+ eval_slot_score_entry_full; reads ATK/DEF/level from card_stats_table via ldmia/stmia. "
        "r0=u8 zone_descriptor [0..0xff]. Returns void. "
        "Constants: gDuelZoneState=0x02020160, gDuelActivation=0x0201e2a0, zero_len=0x2f5c halfwords."),
    ("FUN_080c40e0", "init_field_slot_aob_ctx_d",
        "Initialises fourth variant of duel_field slot AOB context (DAT_080c4120, 0x1c halfwords=0x38 bytes) "
        "for dispatch_card_display_op case 0x18. "
        "Calls zero_fill_by_halfword(base, 0x1c), writes r0->[base+4], r1->[base+8], "
        "r2 (via mov r8,r2 / mov r0,r8)->[base+c]. Sets [base+0x19] bit0 (init_flag=0x1). "
        "Reads gP1LifePoints player bit, ORs 0x4, writes to external ctrl byte. "
        "r0=ptr arg_data; r1=ptr arg_target; r2=ptr arg_extra (three-arg variant via r8). Returns void. "
        "Constants: base_struct=DAT_080c4120, zero_len=0x1c halfwords, init_flag=0x1."),
    ("FUN_080c89e8", "update_zone_activation_display_state",
        "Updates per-player zone activation display state for all 11 slot types; "
        "called in dispatch_card_display_op case 0x03 after write_zone_slot_oam_descriptor. "
        "Outer loop r6=[0..1] (player_id); inner slot_type [0..10]: "
        "calls dispatch_zone_activation_by_state(is_active, slot_type, 0); "
        "if return bit11 (0x800) set, accumulates bit into r5 bitmask. "
        "Writes final bitmask to gDuelZoneCtrl (0x020230c0) [+0x30+player*4]; "
        "calls query_player_slot_activation_bitmask to refresh related fields. "
        "No APCS params (all from globals). Returns void. "
        "Constants: gDuelZoneCtrl=0x020230c0, FLAG_ACTIVATABLE=0x800, slot_type_range=[0..10]."),
    ("FUN_08094678", "get_player_lp_by_field_type",
        "Reads player LP/stat value from gP1LifePoints by player_id and field_type code. "
        "r0=u32 player_bit_packed (bit0=player_id); r1=u8 field_type [0xc..0xf]. "
        "Dispatches: 0xc->[+0x18], 0xd->[+0x10], 0xe->[+0x14], 0xf->[+0x1c] "
        "relative to player_id*0x868 base. Returns 0 for type outside [0xc..0xf]. "
        "Called by dispatch_card_display_op case 0x14; return used as zone_type param for "
        "render_field_zone_card_tile_by_type. Pure read, no side effects. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, type_range=[0xc..0xf]."),
    ("FUN_0801ec9c", "dispatch_card_display_op",
        "Core card display operation dispatcher (indeg=114). "
        "r0=op_code [1..0x3d] (subs#1; cmp#0x3c); dispatches via 61-entry jump table 0x0801ecc4. "
        "Case handlers (sample): 0x01/0x21=init_field_slot_aob_ctx_a, 0x03=write_zone_slot_oam_descriptor+"
        "update_zone_activation_display_state, 0x06=init_card_effect_aob_ctx, "
        "0x09=build_slot_activation_mask_for_player+write_field_slot_activation_mask, "
        "0x0b=init_field_slot_aob_ctx_b, 0x0c=write_zone_oam_entry_with_flip, "
        "0x0d=write_lp_digit_tiles_to_vram, 0x14=get_player_lp_by_field_type+render_field_zone_card_tile_by_type, "
        "0x18=init_field_slot_aob_ctx_d, 0x19=init_field_slot_aob_ctx_c, "
        "0x1a=init_field_slot_ctx_zoom, 0x1b=render_field_slot_card_tile_by_id, "
        "0x1c=init_field_slot_aob_ctx_a (case alias), 0x24=refresh_duel_field+refresh_zone_effect_buff_cache+"
        "refresh_all_zone_slot_tile_display, 0x31=copy_game_text_to_card_name_vram, "
        "0x32=build_field_zone_display_state. "
        "r1/r2/r3=op args (transparent to callee). Returns 1=done or 0=default/invalid. "
        "Constants: jump_table=0x0801ecc4, op_range=[1..0x3d]."),
    ("FUN_0809355c", "invoke_card_display_op_0x31",
        "Lightweight thunk: sets r0=0x31, r1=0x0b, r2=0, r3=0, then calls "
        "dispatch_card_display_op (0x0801ec9c). "
        "Hardcodes op 0x31 (copy_game_text_to_card_name_vram) with sub_param r1=0x0b. "
        "Called by process_card_play_ok_sequence (0x08094a28) and FUN_080954e8 (duel field sprite refresh). "
        "No APCS params. Returns u32 result transparent from dispatch_card_display_op (1=done, 0=invalid). "
        "Constants: op_code=0x31, sub_param=0x0b."),
    ("FUN_08094a28", "process_card_play_ok_sequence",
        "State-machine for 'play card OK' UI sequence. "
        "Calls play_card_ok_ui_effect; if nonzero returns 0 (busy). "
        "Reads gP1LifePoints[0x1d1c] phase code: 1=draw_phase path, 2=LP compare path, else done. "
        "Main path: reads [gP1LifePoints+0x2c] spell/trap/monster phase state (3/4/7), "
        "calls enqueue_sprite_attr_record with attr 0x8006/0x8007/0x8008/0x8005. "
        "Calls pack_sprite_row_attr_words (0x08095380) to submit sprite row. "
        "If [gDuelActivation+offset]!=1: calls invoke_card_display_op_0x31 (0x0809355c). "
        "Increments gP1LifePoints[0x1d1c] (phase counter). Returns 0=done, 1=busy. "
        "Constants: phase_offset=0x1d1c, sprite_attr_spell=0x8006, sprite_attr_trap=0x8007, "
        "sprite_attr_monster=0x8008, sprite_attr_alt=0x8005."),
    # --- batch #38 (campaign-38, 2026-05-10) ---
    ("FUN_080abb90", "reset_sprite_attr_record_flags",
        "Resets flag fields in the sprite attr record struct at 0x0201e4d0. "
        "Loads struct ptr from DAT_080abbcc; r0 is overwritten at entry (void input). "
        "Clears bits in [+0x13] (AND 0x01 keep bit0), clears bit1 in [+0x14] (AND 0xFD), "
        "applies mask 0xFFFFFE01 to [+0x14] halfword and word, "
        "applies mask to [+0x16] halfword; then ORs 0x30 (bit4+bit5) into [+0x12] byte "
        "to mark record as committed/done. Leaf; called by FUN_080954e8 after sprite attr "
        "sequence processing to prevent double-submission. Returns void. "
        "Constants: struct_base=0x0201e4d0, keep_mask=0x01, clear_bit1=0xFD, "
        "wide_mask_0=0xFFFFFE01 (DAT_080abbd0), wide_mask_1=0xFFFE01FF (DAT_080abbd4), "
        "done_bits=0x30."),
    ("FUN_08085320", "submit_lp_bar_sprite_row_by_type",
        "Submits one LP bar display row to the sprite row queue based on current duel state. "
        "r0=u16 x_coord [0..0xFFFF] (low 16 bits via lsls/lsrs); "
        "r1=u32 lp_bar_param (width/type field written to sprite row buffer). "
        "Path A: if gP1LifePoints+0x1d08 LP data ptr is valid and player_id matches, "
        "writes x_coord/lp_bar_param to sp buffer, calls "
        "submit_sprite_row_data(type=0x9, y=-1, sp, count=6). "
        "Path B: if gDuelCtx+0x4d0 LP bar count=0 and extra condition met, "
        "writes LP bar width/count fields then calls submit_sprite_row_data. "
        "r4=x_coord, r5=lp_bar_param. 32 duel_field callers. Returns void (b LAB, no r0). "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, lp_data_offset=0x1d08, "
        "gDuelCtx=0x0201b290, lp_bar_count_offset=0x4d0 (0x9a<<3), type=0x9, row_count=6."),
    ("FUN_080909e0", "check_card_effect_node_active",
        "Checks whether the given card has an active effect node with nonzero activation count. "
        "Calls find_card_effect_node_entry(card_entry); if node not found returns 0. "
        "If found, reads [node+0x4] activation count; converts to bool via "
        "(rsbs #0 | orrs) then lsrs #0x1f to extract sign bit as final flag. "
        "r0=ptr card_entry; returns r0=u32 is_active (1=active, 0=inactive or missing). "
        "No side effects. Called by dispatch_card_effect_by_stat_type as precondition check. "
        "Constants: effect_node_active_offset=0x4."),
    ("FUN_0805b2a4", "dispatch_card_effect_by_stat_type",
        "Dispatches card effect processing based on card stat type fields and special card IDs. "
        "r0=ptr card_entry (saved to r7). "
        "Step 1: checks [r7+0x4] bit1 (processed_bit=0x2); if set returns 0 (already handled). "
        "Step 2: calls check_card_effect_node_active; if node missing returns 0. "
        "Step 3: checks [r7+0x4] bit2 (alt_path_bit=0x4); if clear jumps to large branch LAB_0805b3c2. "
        "Step 4: calls get_card_extended_stat_field9; matches field9 [2..3] range. "
        "Step 5: checks [r7+0x3] AND 0x30 (stat3_bits); if card_id==0x1909 returns 0 (special skip). "
        "Whole function is pure read; all exit paths are movs r0,#0 or movs r0,#1. "
        "Called by FUN_080954e8 (duel scene main loop). Returns u32 should_continue (0=skip, 1=proceed). "
        "Constants: processed_bit=0x2, alt_path_bit=0x4, stat3_bits=0x30, "
        "card_id_special=0x1909, field9_range=[2..3]."),
    ("FUN_0801f3b0", "read_prng_entry_flag_clear",
        "Reads a flag byte at gPrng+0x1c0[+0x584] and returns the inverted bit0 as a bool. "
        "No APCS input (first two instructions overwrite r0 and r1). "
        "Computes gPrng + (0xe0<<1)=0x1c0, dereferences the word there as a pointer, "
        "then adds offset 0x584 (DAT_0801f3cc), reads a byte, and returns "
        "bics r0(=1),r1 -> 1 if bit0 is clear, 0 if bit0 is set. "
        "Result is 'flag_is_clear' boolean. Leaf; called by FUN_080954e8 (prng tagged). "
        "No side effects (read-only). "
        "Constants: gPrng_offset=0x1c0 (0xe0<<1), entry_offset=0x584, flag_bit=0x1."),
    ("FUN_080a1968", "commit_lp_display_row_to_sprite",
        "Initialises LP display state fields then submits one LP bar sprite row. "
        "No APCS input (entry overwrites r2 with PTR_gP1LifePoints). "
        "Writes [gP1LifePoints+0x1d88]:=1 (active), [+0x1d94]:=0, [+0x1d84]:=0. "
        "Checks player_id match (eors#1 XOR); if match and LP data valid, "
        "calls copy_bytes_by_halfword(src, sp, len=0x10) then "
        "submit_sprite_row_data(type=0x1e, y=-1, sp, count=0x12). "
        "Clears [0x0201b870+0x301] bit0/bit1 (AND 0xFC), sets [gP1LifePoints+0x1d84]:=1 (done). "
        "Called by setup_lp_display_row_with_data (0x080a1a38) and FUN_080a1a00. Returns void. "
        "Constants: gP1LifePoints=0x0201c4e0, active_flag_offset=0x1d88, zero_offset=0x1d94, "
        "data_offset=0x1d84, copy_len=0x10, type=0x1e, row_count=0x12."),
    ("FUN_080a1a38", "setup_lp_display_row_with_data",
        "Writes caller-provided LP bar display params to gP1LifePoints state area "
        "then triggers sprite row submission. "
        "r0=u32 lp_val_a (written to gP1LifePoints+0x1d6c); "
        "r1=u32 lp_val_b (written to +0x1d70); "
        "r2=ptr src_data; r3=u32 copy_count [0..8] (clamped to 8 via cmp#8/ble). "
        "Calls copy_bytes_by_halfword(r2, gP1LifePoints+0x1d74, r3*2), "
        "then commit_lp_display_row_to_sprite(). Returns void. "
        "Constants: gP1LifePoints=0x0201c4e0, val_a_offset=0x1d6c, val_b_offset=0x1d70, "
        "data_offset=0x1d74, max_copy_count=8."),
    ("FUN_08095b3c", "get_lp_display_state_word",
        "Reads and returns the 32-bit LP display state control word from "
        "gP1LifePoints+0x1d0c. No APCS input (entry overwrites r0). "
        "4-instruction leaf: ldr gP1LifePoints, ldr 0x1d0c offset, adds, ldr [r0], bx lr. "
        "Non-zero return enables LP display update in caller FUN_080954e8; "
        "zero means no update needed this frame. No side effects. "
        "Constants: gP1LifePoints=0x0201c4e0, state_offset=0x1d0c."),
    ("FUN_0803bde4", "write_sprite_attr_record_entry",
        "Writes four halfword sprite attributes into fixed slots in gSpriteAttrBuf "
        "and marks the slot as filled. "
        "r0=u16 attr0, r1=u16 attr1, r2=u16 attr2, r3=u16 attr3. "
        "Loads gSpriteAttrBuf (0x0201b870) into r12; "
        "writes attr0 to [base+0x304] (0xc1*4), attr1 to [+0x306], "
        "attr2 to [+0x308] (0xc2*4), attr3 to [+0x30a]; "
        "ORs 0x4 into [base+0x300] (0xc0*4) to set filled bit; "
        "writes 0 to [base+0x30c] (0xc3*4) to clear attr3 pad byte. "
        "Calls return_void_noop_stub as commit callback. Returns void. "
        "Constants: gSpriteAttrBuf=0x0201b870, flags_offset=0x300, filled_bit=0x4, "
        "attr_offsets=[0x304,0x306,0x308,0x30a,0x30c]."),
    ("FUN_0804a76c", "increment_lp_bar_display_counter",
        "Increments the LP bar display counter in gDuelCtx and initialises animation "
        "state on first increment. No APCS input (entry overwrites r4 with gDuelCtx). "
        "Checks gDuelCtx+0x4d0 (active flag); if nonzero returns immediately. "
        "Reads gP1LifePoints+0x1d08 LP data ptr; if nonzero checks player_id match. "
        "On player mismatch: writes halfword=1 to sp, calls "
        "submit_sprite_row_data(type=0xa, y=-1, sp, count=2). "
        "On match or LP ptr null: increments gDuelCtx+0x4c4; "
        "if counter first becomes 1: clears [+0x4cc] and [+0x580], increments [+0x4c8]. "
        "indeg=64. Returns void. "
        "Constants: gDuelCtx=0x0201b290, active_flag_offset=0x4d0, counter_offset=0x4c4, "
        "anim_offset=0x4cc, anim2_offset=0x580, seq_counter_offset=0x4c8, type=0xa, row_count=2."),
    ("FUN_080310d0", "find_slot_idx_in_dual_list_by_id",
        "Searches two player slot lists sequentially for an entry matching a target ID; "
        "returns its logical index. "
        "r0=u32 player_side [0..1]; r1=u16 target_id [0..0x1FFF] (low 13 bits matched). "
        "Base: gP1LifePoints+0x10e0 (0x87<<5). Outer loop r4=[0..1] (lists); "
        "inner loop r3=[0..0x7e] (127 entries, 8 bytes each). "
        "Each entry: ldrh, extract low 13 bits (lsls#0x13/lsrs#0x13), cmp with target. "
        "Hit: returns r1 = r6 XOR r4 (player_side XOR list_idx). "
        "Miss: returns 0. Pure read; no side effects. "
        "Constants: gP1LifePoints=0x0201c4e0, base_offset=0x10e0 (0x87<<5), "
        "entry_size=8, entry_count=0x7f, id_bits=13."),
    ("FUN_0803b8b0", "write_field_slot_bit_by_player",
        "Performs a single bit set or clear on the slot flags word for a given player and slot. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]; "
        "r2=u32 bit_pos [0..31]; r3=u32 set_flag (0=clear BIC, nonzero=set OR). "
        "Target address: gP1LifePoints + player_side*0x868 + slot_idx*0x14 + 0x40. "
        "Reads flags word, applies (1<<bit_pos) OR or BIC, writes back. "
        "indeg=11; called by duel_field and card_data callers. Returns void. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "slot_entry_size=0x14, flags_offset=0x40."),
    ("FUN_0804a970", "set_field_slot_bit_with_sprite_update",
        "Conditionally writes a slot flag bit and enqueues a sprite attr update when "
        "the bit value changes. "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]; "
        "r2=u32 bit_pos [0..31]; r3=u32 set_flag [0..1]. "
        "Reads gP1LifePoints[player*0x868+slot*0x14+0x40] flags word, extracts bit at bit_pos; "
        "if current == set_flag skips (no-op). Otherwise calls "
        "write_field_slot_bit_by_player(player, slot, bit_pos, set_flag) then "
        "enqueue_sprite_attr_record(oam_y, slot_idx, bit_pos, set_flag) "
        "with oam_y=0x2a (player=0) or 0x802a (player!=0). "
        "indeg=29; core shared path for slot flag updates. Returns void. "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, "
        "slot_entry_size=0x14, flags_offset=0x40, oam_y_p0=0x2a, oam_y_p1=0x802a."),
    ("FUN_0804c76c", "submit_slot_card_sprite_row_entry",
        "Looks up a duel slot index, packs card sprite attributes and submits a display row. "
        "r0=u32 player_side [0..1]; r1=u32 card_id [0..0xFFFF]; "
        "r2=u16 slot_idx [0..0xFFFF] (0 triggers dynamic find via find_slot_idx_in_dual_list_by_id); "
        "r3=u32 slot_data_word (written to gDuelCtx slot struct +0x14 in alternate path). "
        "Main path: checks gP1LifePoints+0x1d08 LP ptr and player_id match; "
        "packs 6 halfword sprite attrs to sp buf, calls "
        "submit_sprite_row_data(type=0x14, y=-1, sp, count=0xc). "
        "Alt path: finds gDuelCtx+0x480 or 0x488 slot ptr, "
        "calls zero_fill_by_halfword(0x18 bytes), packs card_id/slot fields, "
        "increments active count halfword. Returns void. "
        "Constants: gDuelCtx=0x0201b290, p0_slot_offset=0x480, p1_slot_offset=0x488, "
        "slot_entry_size=0x18, sprite_type=0x14, row_count=0xc."),
    ("FUN_0804a870", "decrement_lp_bar_display_counter",
        "Symmetric counterpart of increment_lp_bar_display_counter (0x0804a76c); "
        "decrements gDuelCtx+0x4c4 by 1 (subs #1) instead of incrementing. "
        "No APCS input (entry overwrites r4 with gDuelCtx). "
        "Checks gDuelCtx+0x4d0 active flag; if nonzero returns. "
        "Reads gP1LifePoints+0x1d08 LP ptr and player_id; on mismatch "
        "writes halfword=3 to sp, calls submit_sprite_row_data(type=0xa, y=-1, sp, count=2). "
        "On match or LP ptr null: decrements [gDuelCtx+0x4c4]. "
        "No extra initialisation when counter reaches 0 (unlike increment variant). "
        "indeg=67. Returns void. "
        "Constants: gDuelCtx=0x0201b290, active_flag_offset=0x4d0, counter_offset=0x4c4, "
        "sprite_type=0xa, row_count=2."),
    ("FUN_08094eb4", "write_card_display_index_entry",
        "Writes or updates one entry in the card display index array at 0x0201b1b0. "
        "r0=u32 index [0..0x7F]; r1=u32 value. "
        "If index <= 0x34 (52): direct path writes r1 to [0x0201b1b0+index*4]. "
        "If index > 0x34: extended path computes sub_idx=(index-0x35), "
        "locates word in 32-slot bitfield at [0x0201b1b0+0xd4+word_slot*4], "
        "applies (1<<bit_pos) OR if value!=0, BIC if value==0. "
        "indeg=10; leaf. Returns void (bx lr). "
        "Constants: array_base=0x0201b1b0, direct_max_index=0x34, "
        "extended_base_offset=0xd4, extended_slot_bits=32."),
    ("FUN_08094f3c", "write_card_display_index_with_bit_offset",
        "Wrapper that queries a card data bit then adds a base offset to form the "
        "final display index before writing. "
        "r0=ptr card_entry; r1=u32 base_offset [0..0x7F]. "
        "Calls get_card_data_bit_by_index(card_entry, bit_selector); "
        "computes index = bit_result + base_offset; "
        "calls write_card_display_index_entry(card_entry, index). "
        "indeg=27; called by card_data/card_frame/duel_field callers. Returns void. "
        "Side effect: write_card_display_index_entry applied to computed index."),
    ("FUN_08094f70", "update_card_display_index_by_type_rules",
        "Applies field6/field9 type rules to update card display index array entries. "
        "r0=ptr card_entry (saved to r4); r1=s32 active_count (saved to r6; "
        "caller FUN_08095a18 passes [gP1LifePoints+0x310]; <=0 skips sub-condition checks). "
        "Checks card_side XOR flip_status vs current player_id [0x0201e2a0+4]; "
        "mismatch: skips all. "
        "If field6 (get_card_extended_stat_field9/field6) == 0x17 (23): "
        "calls write_card_display_index_entry(0x3a, 1); if [r0+0x3] AND 0x30 == 0, "
        "calls write_card_display_index_with_bit_offset(0x21, 1); "
        "checks field9: if field9==1 returns early. "
        "If field6 == 0x16 (22): similar path "
        "write_card_display_index_entry(0x39,1) + write_card_display_index_with_bit_offset(0x1f,1). "
        "Final: write_card_display_index_with_bit_offset(0x20 or 0x22, 1). "
        "Called only by FUN_080954e8. Returns void. "
        "Constants: player_id_ptr=0x0201e2a0, field6_type_23=0x17, field6_type_22=0x16, "
        "field9_threshold=1, index_A=0x3a, index_B=0x39, index_C=0x21, "
        "index_D=0x1f, index_E=0x20, index_F=0x22."),
    ("FUN_0804a7f8", "increment_lp_bar_counter_no_player",
        "Similar to increment_lp_bar_display_counter (0x0804a76c) but takes no player_side "
        "parameter and writes halfword=2 (vs 1) on player mismatch. "
        "No APCS input (entry: push {lr}; ldr r3, gDuelCtx). "
        "Checks gDuelCtx+0x4d0 active flag; if nonzero returns. "
        "Checks gP1LifePoints+0x1d08 LP ptr and player_id [0x0201e2a0+4] XOR 1; "
        "on mismatch: writes halfword=2 to sp, "
        "calls submit_sprite_row_data(type=0xa, y=-1, sp, count=2). "
        "On match or LP null: increments gDuelCtx+0x4c4; "
        "if counter becomes 1: increments gDuelCtx+0x4c8. "
        "Missing 0x4cc/0x580 clear steps present in 0x0804a76c. indeg=4. Returns void. "
        "Constants: gDuelCtx=0x0201b290, active_flag_offset=0x4d0, counter_offset=0x4c4, "
        "seq_offset=0x4c8, type=0xa, row_count=2, mismatch_halfword=2."),
    ("FUN_080ed674", "check_prng_anim_frame_slot_occupied",
        "Checks whether a player's target animation frame slot is already occupied in "
        "the gPrng frame table. "
        "r0=u32 player_id [0..1]. "
        "Loads gPrng+0x1c0 frame table ptr; locates player entry at +0x5a0+player*14. "
        "Reads frame byte, adds 6, masks to low 8 bits, ORs 0xb000 to form OAM attr r5. "
        "Loops (r6+6)/6+3 iterations over circular index (player+i) & 0x3f: "
        "reads each halfword from frame table, masks with 0xf0ff, compares to r5; "
        "on hit returns 1 (slot occupied). After loop returns 0 (free). "
        "No side effects. Called by FUN_080ed6fc (prng tag). "
        "Constants: gPrng=0x03000040, frame_ptr_offset=0x1c0, table_offset=0x5a0, "
        "entry_stride=14, frame_mask=0xFF, oam_base=0xb000, attr_mask=0xf0ff, slot_wrap=0x3f."),
    # --- batch #39 (campaign-39) 2026-05-10 ---
    ("FUN_080ed6fc", "dequeue_prng_anim_entry",
        "prng anim queue dequeue. r0=ptr 6-byte anim data src. "
        "Reads gPrng+0x592 frame counter (halfword); if 0 returns 0. "
        "Otherwise sets gPrng+0x58c active flag=1, decrements counter, "
        "branches by type tag (high byte mask 0xF0): "
        "0x90=single channel, 0xA0=dual channel, 0xB0=multi-segment. "
        "0x90 path: copy_bytes_by_halfword writes 6 bytes to dest buffer, "
        "increments gPrng+0x59c slot counter. 0xA0/0xB0 paths similar but different offsets. "
        "All paths clear gPrng+0x58c at exit. Returns 0 (queue empty) or non-zero (slots*2). "
        "Callers: FUN_080954e8/FUN_080fa570/FUN_080fae24 (prng tag). "
        "Constants: gPrng=PTR_gPrng_080ed76c, frame_counter_offset=0x592, "
        "active_flag_offset=0x58c, slot_counter_offset=0x59c, type_mask=0xF0, "
        "TYPE_SINGLE=0x90, TYPE_DUAL=0xA0, TYPE_MULTI=0xB0."),
    ("FUN_080954e8", "step_prng_anim_frame",
        "Per-frame prng animation step. When busy_flag (base 0x0201b870 + 0x300) bit0==0, "
        "calls dequeue_prng_anim_entry to advance one queue entry. "
        "If dequeue returns non-zero: calls read_prng_entry_flag_clear to clear slot flag, "
        "then queries get_lp_display_state_word; if 0 jumps to switch case 0, "
        "otherwise loads gP1LifePoints+0x1d0c LP data and dispatches. "
        "Indeg=1 (game loop hub FUN_08094dac). No APCS input (entry: ldr r4,DAT then base+0x300). "
        "Returns void (b switchD jumps to case handler at exit). "
        "Constants: base=0x0201b870, busy_flag_offset=0x300 (0xc0<<2), bit0=busy_bit."),
    ("FUN_0804f0e4", "flush_sprite_row_queue_partial",
        "Compacts sprite row anim queue and flushes processed entries. "
        "Base=0x0201b290 (DAT_0804f1cc); count at +0x488 (0x91<<3); write_ptr at +0x480 (0x90<<3). "
        "While read_ptr < depth: copy_bytes_by_halfword copies 0x18-byte entries from src to dst, "
        "updates write_ptr, increments frame index until 0xf cap. "
        "After cap: phase 2 compacts tail entries forward, decrements [base+0x488] by processed count. "
        "Finally clears [base+0x490] and [base+0x494] flags. "
        "No APCS input (entry ldr r1,DAT_0804f1cc loads base; .hword 0x464f/0x4646 callee-save). "
        "Returns 1 if write_ptr!=0 (entries processed) else 0. "
        "Side effects: strh base+0x480, str base+0x488, str 0 to base+0x490 and base+0x494, "
        "multiple copy_bytes_by_halfword writes (0x18 bytes each). "
        "Caller: FUN_0804f2e0 (card_frame/duel_field/game_str). "
        "Constants: base=0x0201b290, write_ptr_offset=0x480, count_offset=0x488, "
        "max_row=0xf, entry_stride=0x18."),
    ("FUN_0804daf6", "reset_sprite_row_queue_tail",
        "Resets sprite row queue tail control fields at end of animation sequence. "
        "Base=0x0201b290: clears +0x48c, sets +0x498=1, clears +0x49c. "
        "Reads halfword at +0x4b6 (0x8b<<3 - 0x18) and writes it to +0x4b8 "
        "(prev frame X position propagates to current frame X). "
        "Clears +0x4d0 (0x9a<<3), +0x518, and +0x580 (0xb0<<3). "
        "No APCS input (ldr r1,DAT_0804db44=0x0201b290; .hword 0x4698/0x46a1/0x46aa restore r8/r9/r10). "
        "Returns 1 (movs r0,#1 fixed success code at @0804db32). Leaf, no bl. "
        "Caller: FUN_0804d1e4 (batch-internal, terminal-state cleanup). "
        "Constants: base=0x0201b290, off_48c=0x48c, off_498=0x498, off_49c=0x49c, "
        "off_4b6=0x4b6, off_4b8=0x4b8, off_4d0=0x4d0, off_518=0x518, off_580=0x580."),
    ("FUN_0804d1e4", "dispatch_sprite_row_anim_by_state",
        "Sprite row anim state machine dispatcher. Reads state code (word) at base 0x0201b290 + 0x494. "
        "If state>0xe: calls reset_sprite_row_queue_tail to force reset. "
        "States [0..0xe] index jump table PTR_DAT_0804d258 (15 cases: init/fade-in/play/fade-out/end). "
        "If state==0 jumps to LAB_0804d220 (r7=0 idle); else computes source entry pointer "
        "from base+0x498*3<<3 + 0xba<<2, dispatches via PTR_DAT. "
        "No APCS input (.hword 0x4657/0x464e/0x4645 = mov r15/r14/r13 callee-save; ldr r2 loads base). "
        "Returns case_result: state>0xe path=reset_sprite_row_queue_tail return (1); state==0 r7=0; "
        "other cases handler-defined. Both known callers FUN_0804f2ee/FUN_0804f3da b after bl, "
        "so semantically void to caller. "
        "Callers: FUN_0804f2e0 (card_frame/duel_field), FUN_0804f34c. "
        "Constants: base=0x0201b290, state_offset=0x494 (0x92<<3), entry_stride=0xba<<2=0x2e8."),
    ("FUN_0804c958", "init_card_sprite_row_entry",
        "Initializes one sprite row entry (0x18-byte OAM attribute block). "
        "Memsets target struct to 0 (0x18 bytes), then writes r0 (card_id) as first halfword. "
        "Unpacks r1 (attr_packed u16) into OAM attr0/attr1/attr2 fields: "
        "bit31->attr0[1] flip_y; bits[29:27]->attr1[5:4] priority/size; "
        "bits[23:16]>>6->attr1[7:6] shape; bits[20:21]->attr2[5:4] palette; bits[15:9]->attr2[6] tile. "
        "Then checks active slot count at base 0x0201b290 + 0x4cc; if >0 iterates slots calling "
        "dispatch_card_effect_activation; on activation calls submit_slot_card_sprite_row_entry. "
        "r0=u16 card_id [0..0x172f] (game total card upper bound; 13-bit field static cap 0x1fff); "
        "r1=u16 attr_packed [0..0xffff]. Returns void (bx r0). "
        "3 callers from FUN_08095ba8/FUN_08095ca0/FUN_08095d84 (duel_field). "
        "Constants: base=0x0201b290, slot_count_offset=0x4cc, attr_mask_1ff=0x1FF, "
        "attr_mask_803f=0xFFFF803F, entry_size=0x18."),
    ("FUN_0804caf0", "init_card_sprite_row_entry_alt",
        "Alternate variant of init_card_sprite_row_entry (0x0804c958), structurally symmetric. "
        "Same memset+OAM unpack logic, same callees (dispatch_card_effect_activation + "
        "submit_slot_card_sprite_row_entry). "
        "Key difference: this variant saves r1 (truncated attr_packed) at sp[0x18] "
        "before memset and restores afterwards (vs v1 which uses r10 callee-save alias). "
        "r0=u16 card_id [0..0x172f]; r1=u16 attr_packed (truncated, stored at sp[0x18] then reused). "
        "Returns void (bx r0). 3 callers identical to v1 (FUN_08095ba8/FUN_08095ca0/FUN_08095d84). "
        "Caller selection: alt is invoked when r1 is built by multiple `orrs r0,r1` "
        "merging multiple halfword fields (wider packed attr); v1 is invoked when r1 comes from "
        "a single ldrh of one 16-bit field. "
        "Constants: base=0x0201b290, slot_count_offset=0x4cc, attr_mask_1ff=0x1FF, "
        "attr_mask_803f=0xFFFF803F, entry_size=0x18."),
    ("FUN_08043054", "enqueue_sprite_attr_with_mode",
        "Core OAM sprite attribute enqueue primitive (indeg=74). Packs 5 params and calls "
        "enqueue_sprite_attr_record to write OAM buffer. "
        "r0=u32 palette_mode (0=default 0x36, non-zero=ext 0x8036 from DAT_08043088); "
        "r1=u8 sprite_type [0..0xff] (OAM group/type, callee-save r5); "
        "r2=u16 x_pos [0..0x3ff]; r3=u16 y_pos [0..0x1ff]; sp[0x10]=u16 extra_attr [0..0xffff]. "
        "Builds OAM attr1 word as (r5<<24)|((r3<<24)>>8), then calls enqueue_sprite_attr_record "
        "(x=r2, y=r3, extra=r4). Returns void (bx r0 transparent forwarding). "
        "74 callers cover nearly all sprite submission points in duel_field; "
        "single bottom-level OAM write convergence point. "
        "Constants: default_palette=0x36, ext_palette=0x8036, attr_pack: type_field=bits[23:16] of r1."),
    ("FUN_0804a484", "enqueue_sprite_attr_type11",
        "Wrapper around enqueue_sprite_attr_with_mode with sprite_type fixed at 0xb (11), indeg=81. "
        "r0=u32 palette_mode (forwarded); r1=u16 x_pos [0..0x3ff]; r2=u16 y_pos [0..0x1ff]; "
        "r3=u16 extra_attr [0..0xffff]. "
        "Truncates r1/r2/r3 to u16, pushes r3 onto sp[0x0] (callee 5th arg sp[0x10]), "
        "injects r1=0xb (SPRITE_TYPE_CARD), then bl enqueue_sprite_attr_with_mode. "
        "Returns void (bx r0 transparent). 81 callers (superset of 74-caller core) cover most "
        "card position sprites in duel_field; type=0xb corresponds to standard field card sprite layer. "
        "Constants: SPRITE_TYPE_CARD=0xb."),
    ("FUN_080486b0", "enqueue_sprite_attr_by_sign",
        "Selects OAM attr2 palette by sign of r0, then calls enqueue_sprite_attr_record. "
        "r0<0 (negative=active/occupied slot): movs r0,#0x30 (PALETTE_ACTIVE); size=1; attr3=0; "
        "calls enqueue_sprite_attr_record. "
        "r0>=0: default attr2=0x30; if r0==0 keep, if r0>0 load DAT_080486e0=0x8030 (PALETTE_EXT); "
        "calls enqueue_sprite_attr_record. "
        "r0=s32 slot_state (sign-determined palette select); r1=u16 y_pos [0..0xffff]. "
        "Returns void (transparent forwarding). 10 callers including FUN_08049014/FUN_080490b4 "
        "(duel_field) and batch-mate FUN_0808e5c4. "
        "Constants: PALETTE_ACTIVE=0x30, PALETTE_EXT=0x8030, SIZE_FIELD=1."),
    ("FUN_08048750", "enqueue_sprite_attr_clamped",
        "Clamps r1 (count) into [0..0xffff] then selects OAM attr and calls enqueue_sprite_attr_record. "
        "r1==0: jumps to LAB_08048774 returning without enqueue (count 0 no render). "
        "r1>0xffff (DAT_08048778): clamps to 0xffff. "
        "Attr select: r0==0 uses 0x25 (single sprite), r0!=0 uses DAT_0804877c=0x8025 (extended). "
        "Calls enqueue_sprite_attr_record with attr2=2, attr3=0, r1=clamped count, r3=r0_copy. "
        "r0=u32 attr_mode (0=0x25, non-zero=0x8025); r1=u32 count [0..0xffff, clamped] (0=no-op). "
        "Returns void. 13 callers including FUN_0805635c (duel_field), FUN_080572b8 (multi-tag), "
        "FUN_0808e5c4 (batch-internal via 0x080486b0 chain). "
        "Constants: CLAMP_MAX=0xffff, ATTR_SINGLE=0x25, ATTR_EXT=0x8025, SIZE=2."),
    ("FUN_0808e5c4", "render_field_card_copy_count",
        "Counts copies of one card on field and renders the count as sprites. "
        "Fixed CARD_BASE=0x132c (DAT_0808e5fc) for query target. "
        "Step 1: count_field_copies_of_card(base) returns r4; if r4<=0 returns. "
        "Step 2: r0=-1, r1=base, calls enqueue_sprite_attr_by_sign to submit one active marker sprite "
        "(palette=0x30). Step 3: loops r4 times calling enqueue_sprite_attr_clamped "
        "(r0=card_ptr, r1=0x1f4=COUNT_SPRITE_Y), decrementing r4 to 0. "
        "r0=ptr card_ptr (saved to r6 then forwarded to enqueue_sprite_attr_clamped). "
        "Returns void (bx r0). 5 callers: FUN_0804a334, FUN_0807fde8, FUN_08095ca0, "
        "FUN_080abbd8, FUN_080abe54. "
        "Constants: CARD_BASE=0x132c, COUNT_SPRITE_Y=0x1f4 (0xfa<<1)."),
    ("FUN_0804adc8", "check_card_type_is_spell",
        "Checks whether a card's type category is Spell (3). "
        "Calls map_field8_to_card_type_category (0x0804a9dc) to map stat_field8 to a category code [0..N]. "
        "If category==3 (TYPE_SPELL) sets r1=1, else r1=0; returns r1. "
        "r0=u16 card_id [0..0x172f] (forwarded to map_field8_to_card_type_category; "
        "callers extract from gDuelFieldSlots low 13 bits via lsls/lsrs #0x13). "
        "Returns u32 bool (1=Spell, 0=non-Spell). Pure query, no side effects. "
        "Indeg=25, C_util_high; callers in duel_field/card_frame contexts decide effect/render path. "
        "Constants: TYPE_SPELL=3."),
    ("FUN_08045268", "enqueue_sprite_attr_with_shape",
        "Selects OAM shape attr by r0 then calls enqueue_sprite_attr_record after splitting r3 "
        "into x/y. r0==0 uses 0x3a (shape A); r0!=0 uses DAT_08045294=0x803a (shape B). "
        "r1 (u8 after lsls/lsrs 0x18): OAM auxiliary field (type or palette low byte), "
        "ORed with 0x100 (TYPE_FLAG=0x80<<1) before forwarding as r1. "
        "r3: high 16 bits = y_pos [0..0x1ff], low 16 bits = x_pos [0..0x3ff]; split via lsls/lsrs. "
        "Note: r2 is NOT an APCS input; entry `adds r3,r2` saves r2 as xy_packed, then "
        "@0804527a `movs r2,#0x80 / lsls #0x1` overwrites r2 with internal TYPE_FLAG=0x100. "
        "Caller-passed r2 is unread (entry-instruction-param-clobber pattern). "
        "Returns void (transparent forwarding). 8 callers including FUN_0804559c (duel_field), "
        "FUN_0808e45c/FUN_0808e770/FUN_0808e85c (batch-internal/duel_field). "
        "Constants: ATTR_SHAPE_A=0x3a, ATTR_SHAPE_B=0x803a, TYPE_FLAG=0x100."),
    ("FUN_0808e85c", "scan_field_slots_for_equip_sprite",
        "Scans both player field slots (gDuelFieldSlots, 9 slots/side) for cards matching equip "
        "criteria and submits sprites. "
        "r0=ptr card_ptr_p0; r1=u8 player0_id [0..1] (.hword 0x4689=mov r9,r1); "
        "r2=ptr card_ptr_p1 (.hword 0x4682=mov r10,r2). "
        "Outer loop counter sp[0x4] iterates 0..1; "
        "inner loop slot_idx 1..9 (cmp r6,#0x9, ble); "
        "uses [gDuelFieldSlots_B + slot*0x14].lsls #0x13 to test active bit; "
        "if matches active_mask 0x9b080000 (bits [26,23,22,20,19] all set on slot word), "
        "tests further flag bits and conditionally calls enqueue_sprite_attr_with_shape (0x08045268). "
        "Outer loop selects player side (sp[0x4] & 1). Returns void. "
        "5 callers: FUN_080440b8, FUN_08047218, FUN_08047f50, FUN_08048020, FUN_08048364 (duel_field). "
        "Constants: gDuelFieldSlots_B=0x0201c520, gDuelFieldSlots_A=0x0201c510, "
        "player_stride=0x868, slot_stride=0x14, MAX_SLOT=9, active_mask_word=0x9b080000."),
    ("FUN_0802f930", "find_equip_target_for_card_slot",
        "Finds the equip-link target for a given card slot in gDuelFieldSlots. "
        "r0=u32 player_key (low bit0=player_id; ands r2,r0 masks to bit0; .hword 0x4692=mov r10,r2). "
        "r1=u8 slot_idx [0..4] (slot_stride 0x14 * slot_idx + player_id*0x868 + base). "
        "Reads [slot+0xa] (halfword, current card state); if 0 returns 0xffff (no target). "
        "Else extracts stat_field8 (lsls/lsrs 0x1c); only values 0xa or 0xb enter lookup flow. "
        "Computes equip card player+slot product, filters via check_card_stat_field8_is_8, "
        "confirms chain pair via find_equip_chain_pair_across_field. "
        "Final check: if lsrs[slot.field]+0x5 bit0==1 (equip_active) AND "
        "lsrs[target.field]+0x1 bit0==1 (not_reversed), returns target_slot_ptr; else 0xffff. "
        "Returns ptr target_slot or 0xffff (DAT_0x0002f9f8). Pure query. "
        "7 callers including FUN_08047218, FUN_0804888c (duel_field). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "equip_field8_A=0xa, equip_field8_B=0xb, slot_state_offset=0xa, NO_TARGET=0xffff."),
    ("FUN_08033b18", "count_equip_slots_matching_whitelist",
        "Counts player field equip slots that pass a whitelist filter. "
        "r0=ptr player_id_ptr (r7 alias); r1=ptr card_ptr (r9, .hword 0x4689=mov r9,r1); "
        "r2=u32 start_count [0..0xb] (r6 alias, accumulator initial value); "
        "r3=u32 allow_face_down [0..1] (r8 alias, .hword 0x4680=mov r8,r3). "
        "Iterates gDuelFieldSlots[player*0x868 + slot*0x14] for r8 slots from slot=0: "
        "tests active bit (lsls #0x13) -- skip if 0; "
        "for slot<=4 calls check_slot_card_is_equip_whitelist(player_id, slot_idx); "
        "if passes, checks halfword [slot+0x8] under allow_face_down condition. "
        "Increments r2 on match. Returns u32 matched_count (>= start_count). "
        "Pure query. 5 callers including FUN_080acc30/FUN_080bb0f8/FUN_080bb414 (duel_field) "
        "and FUN_08033b08 (batch-internal wrapper). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "active_bit_shift=0x13, max_slot_guard=4."),
    ("FUN_08033b08", "count_equip_slots_active_only",
        "Wrapper that calls count_equip_slots_matching_whitelist (0x08033b18) with fixed args "
        "(r1=0 card_ptr null, r2=0 start_count, r3=1 allow_face_down=true). "
        "Forwards r0 (player_id_ptr) unchanged. Returns total active equip slot count for the player. "
        "Pure read-only forwarding. 12 callers including FUN_08030500 (batch-internal), "
        "FUN_08064880, FUN_0809bf60, FUN_080ad974 (duel_field)."),
    ("FUN_08030500", "map_card_id_to_anim_type",
        "Maps a card ID (halfword from r2 struct +0) to an animation type enum [0..6] "
        "via a large binary-search dispatch tree (DAT compares + beq/bgt/blt branches). "
        "All known card IDs partitioned across 6 return labels: "
        "LAB_08030874 -> r0=1 (DEFAULT); LAB_0803084c -> r0=4 (SPELL extended); "
        "LAB_08030850 -> calls count_equip_slots_active_only, returns 6 if >0 else 0 (EQUIP); "
        "LAB_08030838 -> calls read_effect_slot_side_and_type, returns 2 if slot_type>4 else 0 (EXTRA); "
        "LAB_08030866 -> reads attr field, returns 1 or 0 if in range [0x1f..0x21]; "
        "LAB_08030884 -> r0=0 (NO_ANIM). "
        "r0=ptr slot_ptr (r2 saved; reads halfword [r0+0]=card_id). "
        "Returns u32 anim_type [0..6]. "
        "Callers: FUN_08036870 (batch-internal C_util_high indeg=37), FUN_0805d118, FUN_080b40d8. "
        "Constants: NO_ANIM=0, DEFAULT=1, EXTRA=2, SPELL=4, EQUIP=6."),
    ("FUN_08036870", "check_card_equip_eligible_for_slot",
        "Determines whether a given equip card is eligible to attach to a target field slot "
        "(indeg=37, C_util_high). "
        "r0=ptr card_ptr (r5); r1=ptr slot_ptr (r7); r2=u8 target_slot_idx [0..9] (r4); "
        "r3=u8 player_id [0..1] (r9, .hword 0x4699=mov r9,r3). "
        "Phase 1: extracts field5 from card_ptr[+2] (lsls #0x1a / lsrs #0x1b, bits[6:2]); "
        "subs 5 then truncates to u16; if >5 enters Phase 2. "
        "Phase 2: when field5 is in [0..5], stores a flag in r8 (.hword 0x4680=mov r8,r0). "
        "Reads halfword slot_ptr[+0x8] zone state; if 0 jumps to LAB_08036978 (special). "
        "Reads slot[+0] word (lsls/lsrs #0x13 strips active bit) as card_type, compares to "
        "DAT_080368dc=0x150c (TYPE_A) and DAT_080368e0=0x1645 (TYPE_B). "
        "TYPE_A path: validates equip chain via find_equip_chain_pair_across_field. "
        "TYPE_B path: similar but with player_id non-zero check. "
        "LAB_08036938: if r8!=0 AND slot_idx<=4 AND slot[+0x8]!=0 calls "
        "query_zone_chain_count_with_eligibility; if >0 calls map_card_id_to_anim_type and "
        "check_slot_card_is_equip_whitelist; combined result returns 0 (eligible) or 1 (not). "
        "Returns u32 bool (0=eligible, 1=not eligible). Pure query (callees all read-only). "
        "Callers: FUN_080369a4, FUN_0804640c, FUN_08047990, FUN_0804f440, FUN_0804f550. "
        "Constants: FIELD5_EQUIP_TYPE_MIN=5, TYPE_A=0x150c, TYPE_B=0x1645, "
        "slot_state_offset=0x8, EQUIP_SLOT_MAX=4."),
    # --- batch #40 (campaign-40) 2026-05-10 ---
    ("FUN_080369a4", "check_equip_eligibility_via_request_buf",
        "Equip request constructor: builds 24-byte equip request record on stack, "
        "fills (player_id, card_id, zone_type, extra) triple plus extension bits, "
        "then forwards to check_card_equip_eligible_for_slot for actual eligibility test. "
        "r0=u32 player_id [0..1] (bit0 XOR 1 -> [buf+2] bit0); r1=u32 slot_idx [0..0x14] "
        "(equip_chain slot, forwarded to callee); r2=u16 card_id [0..0x172f] "
        "(strh [buf+0]); r3=u32 zone_type [0..0x1f] (low 5 bits lsls #1 -> [buf+2] bits[5..1]); "
        "sp[0x30]=u32 extra_param (forwarded to callee 4th arg). "
        "Returns u32 eligibility (0=not eligible, !=0=eligible). "
        "Callers: FUN_0804686e/FUN_08046974/FUN_08046e44/FUN_08046fe4 (FUN_08046bd0 cluster, "
        "duel_field), FUN_08068596 (effect trigger pre-filter), FUN_0809dde4 (card frame). "
        "No external side effects, only stack-local buffer. "
        "Constants: BUF_SIZE=0x18, EXTRA_PARAM_SP_OFFSET=0x30."),
    ("FUN_080300d4", "check_zone_card_special_state_by_field5",
        "Zone slot special state checker by field5 dispatch: reads card_record [r0+2] low 4 bits "
        "(field5) and dispatches: field5 in [6..9] checks gDuelFieldSlots active_bit at "
        "slot[+0]&0x10000; field5 in [0xa..0xd] does card_id table-match on "
        "0x14b2/0x1243/0x1103/0x137d/0x17b7/0x14fc/0x16a2/0x184b followed by "
        "gP1LifePoints+0x40 bit5 check. "
        "r0=ptr<CardEntry> (reads [+0]=card_id, [+2] low 4=field5); "
        "r1=u32 r6_payload (returned on hit at LAB_080301cc as fallback value). "
        "Returns u32 (0=miss, 1=hit with non-branch return, r6=branch hit return). "
        "Callers: FUN_0804659c, FUN_08046bd0 (duel_field, batch). "
        "No side effects, reads gDuelFieldSlots@0x0201c510 + gP1LifePoints+0x40 only. "
        "Constants: gDuelFieldSlots=0x0201c510, BIT5_MASK=0x20, "
        "FIELD5_RANGE_A=[6..9], FIELD5_RANGE_B=[0xa..0xd]."),
    ("FUN_0804adf0", "check_card_field8_is_9",
        "Simple equality wrapper around get_card_extended_stat_field8: calls callee, "
        "compares result to 9, returns 1 if equal else 0. r0=u16 card_id [0..0x172f] "
        "(forwarded to get_card_extended_stat_field8). Returns u32 bool (1=field8==9, 0=else). "
        "indeg=44, all 16 callers use cmp r0,#0 + beq/bne (standard bool test) in "
        "duel_field equip/effect chains. 5-instruction leaf wrapper, no side effects. "
        "Sibling pattern check_card_field<N>_is_<value> (e.g. check_card_field5_is_nonzero #162). "
        "Constants: FIELD8_TARGET=9."),
    ("FUN_0808f3b0", "scan_field_slots_for_attached_sprite_by_id",
        "Double-loop field scanner for card 0x14bf (DAT_0808f44c=0xa5f80000=0x14bf<<19): "
        "outer i=[0..1] (player side), inner j=[5..9] (monster + spell zone). "
        "When [slot+0]>>19 == 0x14bf AND [slot+0x40] bit5+bit1 both 0, calls "
        "enqueue_sprite_attr_with_shape (PROGRESS #681) to submit decorative sprite. "
        "r0=u32 card_field_bit13 [0..1] -> r10 (callee-save alias for enqueue 1st arg); "
        "r1=u32 sprite_kind_id [=1, fixed across 4 callers] -> r9. Returns void. "
        "All 4 callers (FUN_08047218/FUN_08047f50/FUN_08048020/FUN_08048364, duel_field) "
        "build r0 via lsls#0x12+lsrs#0x1f and r1=#1. "
        "Constants: TARGET_CARD_ID=0x14bf, slot_base=gDuelFieldSlots, "
        "stride_player=0x868, stride_slot=0x14, slot_attr_offset=0x40."),
    ("FUN_0802f6e4", "find_node_packed_by_card_id_in_dual_lists",
        "Dual-player chain scanner: in gDuelFieldSlots@0x0201c510 both player sides (i=[0..1]), "
        "scans node pool@0x0201d9c0 (stride 8) following chain head [+0xa], looking for first "
        "node where [+0]==r8_low AND [+1]==r5. On hit and r4==0 returns "
        "([ctx+0x1c]<<8) | [ctx+0]; on hit and r4!=0 returns "
        "([ctx+0x20]>>8 << 16) | [ctx+4]. No match returns 0xffff. "
        "r0=u8 ref_id_lo [0..0xff] -> r8 (callee-save alias); r1=u8 ref_id_hi [0..0xff] -> r5; "
        "r2=ptr<DuelStateExt> ctx_ptr -> r3 (sub #0xc4 then ldrb-indexed read). "
        "Returns u32 packed (combined fields on hit, 0xffff on miss). "
        "Single caller FUN_0804559c (duel_field, equip dispatcher). "
        "No side effects, reads gDuelFieldSlots/node_pool/ctx_ptr only. "
        "Constants: NODE_POOL=0x0201d9c0, slot_base=0x0201bc54, MISS_SENTINEL=0xffff."),
    ("FUN_0805b1f0", "apply_equip_activation_via_packed_attr",
        "Equip activation record constructor: allocates 24-byte stack record, memset 0, "
        "unpacks 8 bit fields from r0 packed_attr to record offsets: sign bit -> [+2] bit0; "
        "bits[24..23] -> [+3] bits[6..7]; bits[20..18] -> [+3] bits[5..4]; "
        "bits[15..11] -> [+2] bits[2..7]; bits[31..26] -> [+2..3]. "
        "r1 (u16 entity_id, 9 bits) lsls #6 -> [+4] mask 0xffff803f. r2 -> sp[0x14] "
        "(callee 4th arg). Then bl apply_card_equip_activation. "
        "r0=u32 card_attr_packed; r1=u16 entity_id [0..0xffff]; r2=u32 extra_payload. "
        "Returns u32 (decided by apply_card_equip_activation). "
        "Direct callee of FUN_0804c910 (this batch) when r1!=0; also called by "
        "FUN_08096f20/FUN_08096f40/FUN_08099e0c/FUN_0809d5f4 (duel_field/card_frame). "
        "Constants: BUF_SIZE=0x18, ENTITY_SHIFT=6, ATTR_MASK=0xffff803f."),
    ("FUN_0804c910", "apply_equip_activation_with_id_lookup",
        "Equip activation entry wrapper with optional id lookup: when r1 (entity_id u16) is 0, "
        "uses r0 sign_bit + r0 low 13 bits (mask 0x1fff) to call find_slot_idx_in_dual_list_by_id "
        "(PROGRESS #658) to resolve actual entity_id, then forwards to "
        "apply_equip_activation_via_packed_attr (this batch 0x0805b1f0). When r1!=0 skips lookup. "
        "If callee returns 0 returns 0 (failure short-circuit) else returns 1. "
        "r0=u32 card_attr_packed (sign_bit + mask 0x1fff used for lookup); "
        "r1=u16 entity_id [0..0xffff] (==0 triggers lookup); r2=u32 extra_payload (forwarded). "
        "Returns u32 success (0=fail, 1=ok). indeg=61, 5 known callers all duel_field "
        "(FUN_080432bc/FUN_08043714/FUN_080439e0/FUN_08043d90/FUN_080440b8). "
        "Constants: ID_MASK=0x1fff, SIGN_SHIFT=0x1f."),
    ("FUN_0808f938", "refresh_opponent_field_slots_for_card_attached",
        "Opponent-side field scanner: r0=player_id, opp_side=1-r0. Scans opponent 5 monster "
        "slots (j=[5..9]). For each: test_slot_has_active_card filter; reads [slot+0x40] >>4 & "
        "opp_side. ==0 simple path: enqueue_sprite_attr_with_shape. !=0: parses attr bits "
        "(lsls #0x2/#0x12) + apply_equip_activation_via_packed_attr (batch); on hit calls "
        "set_field_slot_bit_with_sprite_update(side,slot,4,1) + enqueue. "
        "r0=u32 player_id [0..1]. Returns void. "
        "Single caller FUN_080487dc (duel_field, batch). "
        "Side effects: enqueue_sprite_attr_with_shape, set_field_slot_bit_with_sprite_update, "
        "apply_equip_activation_via_packed_attr. "
        "Constants: PRE_TEST_CARD=0x159b, slot_attr_offset=0x40, BIT5_OPP_SHIFT=4."),
    ("FUN_080487dc", "submit_lp_change_indicator_with_chain_check",
        "LP change indicator submitter with triple chain check gate: combines amount r1 "
        "(clamped to 0xffff) + player r0 into sprite attr record via enqueue_sprite_attr_record "
        "+ submit_lp_bar_sprite_row_by_type for LP bar display. "
        "Three pre-checks: if r2!=0 AND check_value_in_slot_chain(player,0xb,0x1805) hit, "
        "OR check_value_in_slot_chain(player,0xb,0x1850) hit, OR "
        "count_available_effect_zones returns 0 -> skip submit, return 0. "
        "On hit: calls FUN_0808f938 (refresh_opponent_field_slots, batch) + "
        "submit_lp_bar_sprite_row_by_type. Returns 1 on success. "
        "r0=u32 player_id [0..1]; r1=u16 amount [0..0xffff] (0=skip); "
        "r2=u32 chain_check_flag (!=0 enables 0x1805 check); r3=u32 enqueue_payload -> r7. "
        "Returns u32 success (0=skip/blocked, 1=submitted). 16 callers all duel_field. "
        "Constants: CHAIN_KEY_A=0x1805, CHAIN_KEY_B=0x1850, EFFECT_ZONE_KEY=0x18c4, "
        "ATTR_PLAYER0=0x25, ATTR_PLAYER1=0x8025, AMOUNT_CLAMP=0xffff."),
    ("FUN_0802ff10", "check_zone_card_id_in_node_pool",
        "Zone slot card_id existence check wrapper: reads gP1LifePoints+0x10e2 "
        "(DAT_0802ff30=0x10e2) at slot_idx*4 to extract card_id halfword, then calls "
        "find_node_by_value (PROGRESS #183) to check node pool. Returns 1 on hit, 0 on miss. "
        "r0=u32 slot_idx [0..0xb]. Returns u32 bool. 7-instruction leaf wrapper. "
        "Callers: FUN_0804559c (duel_field, batch), FUN_0805e3a8 (effect trigger). "
        "No side effects (pure read of gP1LifePoints+0x10e2 zone state table + node pool). "
        "Constants: ZONE_STATE_OFFSET=0x10e2, slot_stride=4."),
    ("FUN_08048674", "enqueue_sprite_attr_for_zone_card_id_lookup",
        "Zone-slot card_id lookup + sprite enqueue wrapper: indexes "
        "gP1LifePoints+0x10e0 with slot_idx (lsls #2) to read card_attr halfword, extracts "
        "low 13 bits (lsls/lsrs #0x13) as card_id. Selects OAM attr1: r0==0 -> 0x2e, "
        "r0!=0 -> 0x802e (DAT_080486ac). Forwards to enqueue_sprite_attr_record. "
        "r0=u32 attr_select_flag (0/non-zero); r1=u16 y_pos [0..0xffff]; "
        "r2=u32 slot_idx [0..0xb]. Returns void (transparent forward). "
        "indeg=40, all callers in duel_field. Sibling family with "
        "enqueue_sprite_attr_by_sign (#677) + enqueue_sprite_attr_with_shape (#681). "
        "Constants: ZONE_TABLE=0x10e0, ATTR1_DEFAULT=0x2e, ATTR1_EXT=0x802e, "
        "CARD_ID_BITS=13."),
    ("FUN_0803009c", "find_zone_node_by_card_id_match",
        "Zone-slot chain node finder: reads [r0+0xa] chain head, then scans node pool "
        "@0x0201d9c0 (stride 8) calling FUN_0810e5e4(node, r6=cmp_key) on each, returns first "
        "matching node pointer. Empty chain or no hit returns 0. "
        "r0=ptr<DuelFieldSlot> slot_ptr; r1=u32 r7_payload (callee-save alias unused in body); "
        "r2=u32 cmp_key -> r6 (forwarded to FUN_0810e5e4 r1). "
        "Returns ptr<Node> on hit, 0 on miss. Single caller FUN_0804559c (duel_field, batch). "
        "No side effects, pure read of node pool + chain head. "
        "Constants: NODE_POOL=0x0201d9c0, chain_head_offset=0xa, node_stride=8."),
    ("FUN_0804559c", "dispatch_card_effect_sprite_render_by_card_id",
        "Central dispatcher for sprite attr submission by card_id and effect state: "
        "decodes 8 bit fields from r0 (sp[0x10] equality flag, sp[0x14] field5==0xe test, "
        "sp[0x18] bit15, sp[0x1c] bit14), reads card_id 13bit from [r1+0]>>0x13 -> r6, "
        "decodes r2 into 4 bit flags. Body is large card_id binary search tree "
        "(0x1591/0x1342/0xfd6/0x10dd/0x1185/0x11e4/0x133a/0x1333/0x17b7/0x17af/0x1881/0x19d7+) "
        "with branches to LAB_080457cc/LAB_08045ab4/LAB_0804XX completing "
        "enqueue_sprite_attr_record + submit_lp_bar_sprite_row_by_type submission. "
        "r0=u32 card_attr_packed; r1=ptr<CardRecord> card_record_ptr; r2=u32 flags. "
        "Returns u32 (1 on success paths, 0 on miss/fail). "
        "4 callers all duel_field (FUN_08047218/FUN_08047f50/FUN_08048020/FUN_08048364). "
        "Constants: CARD_ID_SHIFT=0x13, FIELD5_EQUIP=0xe, BUF_SIZE=0x24."),
    ("FUN_08046bd0", "dispatch_card_effect_zone_action_by_card_id",
        "Central dispatcher for zone-level card actions by card_id: extracts card_id_13bit "
        "from [r0+0]&0x1fff -> r8. Decodes r3 bit fields (bit3 inverted -> r1, bit1/bit10/bit2 "
        "-> sp[0x10..0x18]). Body is 30+ card_id binary search tree "
        "(0x1625/0x1468/0x12d3/0x1366/0x150e/0x17b7/0x17af/0x1881/0x19d7/0x15e6+) with branches "
        "to LAB_08046f08/LAB_08047114/LAB_08046f00/LAB_08046db8/LAB_08047012. "
        "Some paths self-recurse, others jump to FUN_08047114/FUN_080470a4. "
        "r0=ptr<CardRecord>; r1=u32 player_side [0..1] (5 callers build via mov r9/r8 or r5); "
        "r2=u32 slot_idx [0..0xb]; r3=u32 flags_bitfield. "
        "Returns u32 (path-dependent: success/fail outcomes). "
        "5 callers all duel_field (FUN_08047218/FUN_08047f50/FUN_08048020/FUN_08048268/"
        "FUN_08048364), sibling dispatcher to FUN_0804559c (this batch). "
        "Constants: CARD_ID_MASK=0x1fff, SP_FRAME=0x1c."),
    ("FUN_08047218", "handle_card_effect_zone_eligibility_by_field6",
        "Card effect zone eligibility handler dispatched by field6: calls "
        "get_card_extended_stat_field6, then dispatches: field6==0x16 -> "
        "query_slot_effect_eligibility_nonzero (equip chain); field6==0x17 -> "
        "check_slot_fieldspell_eligible_by_side; field6<=4 -> "
        "count_equip_chain_default_flags + find_equip_target_for_card_slot then self-recurse "
        "(tail call); field6 in [0xe..0xf] -> sprite branch via FUN_0804559c (batch) + "
        "enqueue_sprite_attr_record. Also reads [gP1LifePoints+0x40+slot*0xc] bit2 + chain "
        "index check, then FUN_0804adf0 (batch, field8==9). "
        "r0=u32 player_side [0..1] -> r9; r1=u32 slot_idx [0..0xb] -> r10; "
        "r2=u32 flag_bit [0..1]; r3=u32 sub_type_bits [0..1] -> sp[0x4]; "
        "sp[0x44]=u16 card_id_arg [0..0x172f] (passed to get_card_extended_stat_field6). "
        "Returns u32 result (1=success, 0=failure). "
        "Callers: FUN_08046bd0 (batch, dispatch sub-flow), FUN_08047724 "
        "(duel_field, equip trigger wrapper). "
        "Constants: FIELD6_EQUIP=0x16, FIELD6_FIELDSPELL=0x17, FIELD6_RECURSE_MAX=4, "
        "FIELD6_SPRITE_LO=0xe, FIELD6_SPRITE_HI=0xf."),
    ("FUN_08036ac0", "check_slot_card_eligible_for_special_action",
        "Slot card eligibility check for special action: r0=player_id, r1=slot_idx, r2=card_id. "
        "Steps: (1) card_id==0 -> return 0; (2) slot in [5..9] -> "
        "check_card_field5_is_nonzero, hit -> SUCCESS; (3) get_card_extended_stat_field9==3 -> "
        "slot in [5..0xa] active_bit check at gDuelFieldSlots+8; (4) field9!=3 -> match against "
        "5 special card_ids (0x13ea/0x1231/0x1238/0x1514/0x1980), on hit do active_bit + "
        "[+0x10] bit1 check. Returns u32 bool (1=eligible, 0=not). "
        "r0=u32 player_id [0..1]; r1=u32 slot_idx [0..0xb]; r2=u16 card_id [0..0x172f]. "
        "5 callers all duel/effect (FUN_08051a08/FUN_0805b990/FUN_0805f088/FUN_0807076c/"
        "FUN_080acc30, mostly duel_field). "
        "No side effects, reads gDuelFieldSlots only. "
        "Constants: SLOT_RANGE_LO=5, SLOT_RANGE_HI=9, FIELD9_SPECIAL=3, "
        "SPECIAL_CARDS=[0x13ea,0x1231,0x1238,0x1514,0x1980]."),
    ("FUN_0802f550", "find_zone_chain_node_by_card_id_pair",
        "Slot chain node finder by card_id pair (zone_type>9 path): in "
        "gDuelFieldSlots[player_bit0][slot_idx]+0xa chain head, scans node pool "
        "@0x0201d9c0 (stride 8) for first node where [+2]&0xF>9 (zone_type out of range) "
        "AND [+0]==r0_low AND [+1]==r1_high. Returns 1 on hit, 0 on empty/miss. "
        "r0=u8 ref_id_lo [0..0xff]; r1=u8 ref_id_hi [0..0xff]; "
        "r2=u32 player_id [0..1] (bit0); r3=u32 slot_idx [0..0xb]. "
        "Returns u32 bool. 7 callers (FUN_0804888c/FUN_08051670/FUN_08052020/FUN_080521a0/"
        "FUN_08053af8 + 2 others, mostly duel_field). "
        "No side effects, pure read. Sibling 0x0802f5b0 find_equip_chain_node_by_slot_pair "
        "checks zone_type<=5 (in-range) - this checks zone_type>9 (out-of-range), forming dual. "
        "Constants: NODE_POOL=0x0201d9c0, slot_base=0x0201c510, ZONE_TYPE_MIN=10."),
    ("FUN_0802fd00", "find_chain_node_by_dual_halfword",
        "Slot chain node finder by dual halfword keys (zone_type<=5 path): in "
        "gDuelFieldSlots[player_bit0][slot_idx]+0xa chain head, scans node pool "
        "@0x0201d9c0 (stride 8) for first node where [+2]&0xF<=5 (zone_type in legal range) "
        "AND [+0]==r2 (halfword 1) AND [+4]==r3 (halfword 2). Returns chain index on hit, 0 on miss. "
        "r0=u32 player_id [0..1]; r1=u32 slot_idx [0..0xb]; r2=u16 ref_halfword_1; "
        "r3=u16 ref_halfword_2. "
        "Returns u32 chain_index (current idx on hit, 0 on miss). "
        "2 callers: FUN_0802ecbc (equip main), FUN_08043240 (batch wrapper). "
        "No side effects, pure read. Near-identical structure to sibling 0x0802fd60 "
        "find_effect_node_in_zone (returns bool 1/0 vs idx). "
        "Constants: NODE_POOL=0x0201d9c0, slot_base=0x0201c510, ZONE_TYPE_MAX=5."),
    ("FUN_08043240", "enqueue_sprite_attr_for_chain_node_match",
        "Chain-node match + sprite attr enqueue wrapper: calls "
        "find_chain_node_by_dual_halfword (this batch 0x0802fd00). On hit (chain_idx!=0): "
        "selects attr1 by r4 (player_id): r4==0 -> 0x38, r4!=0 -> 0x8038 (DAT_08043270). "
        "Encodes r5 (slot_idx) + chain_idx into r1 via lsls/orrs/lsrs. Calls "
        "enqueue_sprite_attr_record(attr1, packed, 0, 0). On miss skips enqueue. "
        "r0=u32 player_id [0..1] -> r4 (selects attr1); r1=u32 slot_idx [0..0xb] -> r5; "
        "r2=u16 ref_halfword_1 (forwarded); r3=u16 ref_halfword_2 (forwarded). Returns void. "
        "9 callers all duel-related (FUN_08044e30/FUN_080490b4/FUN_08057138/FUN_08067750/"
        "FUN_08076b1c+, mostly duel_field). "
        "Side effects: find_chain_node_by_dual_halfword (read), enqueue_sprite_attr_record "
        "(on hit). OAM attr1 sibling family 0x38/0x8038 vs 0x3a/0x803a (#681). "
        "Constants: ATTR1_PLAYER0=0x38, ATTR1_PLAYER1=0x8038."),
    ("FUN_08045240", "enqueue_sprite_attr_with_xy_split",
        "Sprite attr enqueue wrapper with xy-split: splits r2 (32-bit packed_xy = "
        "y_high<<16 | x_low) into x_pos (low 16 lsls/lsrs #0x10) and y_pos (high 16). "
        "Selects attr1 by r0: r0==0 -> 0x3a, r0!=0 -> 0x803a (DAT_08045264). Truncates "
        "r1 (lsls/lsrs #0x18) to low 8 bits. Calls "
        "enqueue_sprite_attr_record(attr1, r1_byte, x_pos, y_pos). "
        "r0=u32 attr_select_flag; r1=u32 attr_aux_byte [0..0xff]; "
        "r2=u32 packed_xy (lo 16=x_pos[0..0x1ff], hi 16=y_pos[0..0x3ff]). Returns void. "
        "25 callers all duel_field (FUN_080432bc/FUN_08043d90/FUN_08044e30/FUN_0805847c/"
        "FUN_08058f90+). Sibling enqueue_sprite_attr_with_shape (#681, 0x08045268) is structural "
        "twin + extra OR 0x100 (TYPE_FLAG); this is bare-split version. "
        "Constants: ATTR1_DEFAULT=0x3a, ATTR1_EXT=0x803a, AUX_BYTE_BITS=8, OAM_TYPE_A=0xa."),
    # campaign-41 batch #41
    ("FUN_080431ac", "enqueue_equip_slot_sprite_attr",
        "Enqueues OAM sprite attr for an equip card slot. "
        "Checks equip chain validity via check_value_in_slot_chain; if chain exists, "
        "builds OAM attr1 from slot_idx|0x100 and calls enqueue_sprite_attr_record "
        "with sprite base 0x8037. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u16 equip_slot_ref; r3=u8 flag (via r8). Returns void. "
        "35 callers, all duel_field related. "
        "Constants: OAM_ATTR1_BASE=0x8037, OAM_VISIBLE_BIT=0x100."),
    ("FUN_0808ea28", "enqueue_paired_slot_sprite_attrs_for_player",
        "Iterates all slot pairs for a player (player*2 rows, up to 11 slots per row). "
        "For each pair, calls check_slot_card_pair_allowed; if non-zero, reads slot attrs "
        "and calls enqueue_sprite_attr_with_mode (mode=3) to write OAM. "
        "Also calls enqueue_equip_slot_sprite_attr for equip chain slots. "
        "r0=u32 player_data_ptr; r1=u8 player_id [0..1]; "
        "r2=u8 col_idx [0..10]; r3=u8 row_count [0..1]. Returns void. "
        "Callers: FUN_08044e30 (duel_field), FUN_0806c368. "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, mode=3."),
    ("FUN_0804543c", "enqueue_equip_card_sprite_attr_for_slot",
        "Checks if the card on the given player slot belongs to equip set B "
        "(check_card_id_is_equip_set_b). If yes, selects OAM attr (0x3c or 0x803c) "
        "based on r2 threshold and player_id, then calls enqueue_sprite_attr_record. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=s16 threshold (ble -> 0x3c, else 0x803c). Returns void. "
        "5 callers, all duel_field related. "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "OAM_ATTR_DEFAULT=0x3c, OAM_ATTR_FLIP=0x803c."),
    ("FUN_08045314", "enqueue_effect_card_slot_sprite_attr",
        "Gets effect category for card on player slot (get_card_effect_category) "
        "and compares with effect card value (get_slot_effect_card_value). "
        "Selects OAM attr (0x3c default or DAT_080453fc) based on zone_col and zone_row, "
        "then calls enqueue_sprite_attr_record and/or enqueue_sprite_attr_with_mode. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u8 zone_col [0..9]. Returns void. "
        "5 callers, all duel_field. "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "OAM_DEFAULT=0x3c, mode_values=0x12/0x22."),
    ("FUN_08043128", "enqueue_equip_chain_slot_sprite_attr",
        "Finds equip chain node via find_equip_chain_node_by_slot_pair. "
        "If node exists, builds OAM attr1 (base 0x8037, high bits 0xa000) "
        "and calls enqueue_sprite_attr_record to enqueue equip chain slot sprite. "
        "r0=u8 player_id [0..1]; r1=u8 slot_a [0..9]; "
        "r2=u32 packed_slot_pair (hi byte=slot_b, lo byte=equip_ref); "
        "r3=u8 equip_type. Returns void. "
        "7 callers, duel_field related. "
        "Constants: OAM_SPRITE_BASE=0x8037, OAM_ATTR_HIGH=0xa000."),
    ("FUN_0804317c", "enqueue_equip_chain_all_slots_for_pair",
        "Iterates all player (0..1) x slot (0..10) combinations and calls "
        "enqueue_equip_chain_slot_sprite_attr for each pair to refresh all equip chain "
        "slot OAM sprite attributes. "
        "r0=u8 side_a [0..1]; r1=u8 side_b [0..1]. Returns void. "
        "Called only by FUN_08044e30 (duel_field hub). "
        "Inner loop: slot [0..10]; outer loop: player [0..1]."),
    ("FUN_08032a8c", "find_best_slot_for_card_by_player",
        "Scans monster zone (slots 0..4) if card field5 is nonzero, otherwise trap zone "
        "(slots 5..10). In monster path calls check_slot_card_pair_allowed and checks "
        "[slot+0x8]; in trap path compares card_id and checks active_bit and [slot+0x10] "
        "bit flags. Returns best slot ATK value (ldrh [slot+0x4]) or 0 if not found. "
        "r0=u8 player_id [0..1]; r1=ptr slot_ref. Returns u16 best_atk_value. "
        "Called only by find_best_slot_atk_across_players. "
        "Constants: gDuelFieldSlots=0x0201c510, equip_zone_offset=0x10a4, "
        "player_stride=0x868, slot_entry_size=0x14."),
    ("FUN_08032b98", "find_best_slot_atk_across_players",
        "Calls find_best_slot_for_card_by_player twice (player=0 then player=1) "
        "on the same slot_ref and returns the larger ATK value. "
        "If player=0 result is 0 returns player=1 result; "
        "if player=1 result is 0 or smaller, returns player=0 result. "
        "r0=ptr slot_ref. Returns u16 best_atk_value (0 if neither found). "
        "Called by populate_effect_node_snapshot."),
    ("FUN_0805b5f0", "populate_effect_node_snapshot",
        "Batch-fills a snapshot struct (r0 ptr) with effect zone node pointers and "
        "chain entries. Clears [r7+0x18], then calls find_effect_node_in_zone (x6) "
        "and check_value_in_slot_chain (x5) to write [r7+0x0..0x2c]. "
        "If count_field_copies_of_card>0, also calls find_best_slot_atk_across_players "
        "and conditionally overwrites [r7+0x10/0x14]. "
        "Then scans slot pairs and calls find_paired_zone_entry_for_card / "
        "count_occupied_monster_zones. "
        "r0=ptr effect_snapshot. Returns void. "
        "Callers: FUN_0805b990, FUN_0805bc48. "
        "Constants: zone_id=0xb, chain_check_const=0xc240, type_codes=1/2."),
    ("FUN_0803670c", "query_slot_card_type_eligibility",
        "Routes eligibility check based on card field6 (get_card_extended_stat_field6): "
        "field6==0x17 (field spell) -> reads byte[+0x2] bit0 for side and calls "
        "check_slot_fieldspell_eligible_by_side; "
        "field6==0x16 (equip/continuous) -> calls query_slot_effect_eligibility_nonzero; "
        "other types in zone_col 5..9 -> check_card_field5_is_nonzero then same. "
        "r0=ptr card_slot_entry; r1=u8 player_id [0..1]; r2=u8 zone_col [0..9]. "
        "Returns u8 eligible_flag (1=eligible, 0=not). "
        "74 callers (C_util_high). "
        "Constants: FIELD_SPELL=0x17, EQUIP_CONTINUOUS=0x16, zone_col_range=[5..9]."),
    ("FUN_0804640c", "check_slot_equip_placement_valid",
        "Comprehensive check whether equip card can be placed on slot (player, zone_col). "
        "Steps: (1) read slot card_id, reject if zero; "
        "(2) query_slot_card_type_eligibility; "
        "(3) if zone_col!=0 call check_card_equip_eligible_for_slot; "
        "(4) if card_id==0x169f check side match; "
        "(5) check byte[slot+0x4] bit4; "
        "(6) if card_id==0x1258 check gP1LifePoints+offset bit2. "
        "r0=ptr duel_field_base; r1=u8 player_id [0..1]; r2=u8 zone_col [0..9]. "
        "Returns u8 valid_flag (1=placeable, 0=not). "
        "Called only by build_equip_placement_valid_bitmap. "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "equip_zone_offset=0x10a4, card_id_169f=0x169f, card_id_1258=0x1258."),
    ("FUN_08046538", "build_equip_placement_valid_bitmap",
        "Iterates all player (0..1) x slot (0..10) combinations. "
        "For each, calls check_slot_equip_placement_valid and ORs result bit "
        "(1<<(player*16+slot)) into internal bitmap r8. "
        "Returns accumulated valid placement bitmap. "
        "r0=ptr duel_field_ptr; r1=u32 equip_mask; r2=u8 player_side [0..1]. "
        "Returns u32 valid_placement_bitmap. "
        "Called by update_equip_target_bitmap_for_field (indeg=25, duel_field). "
        "Bitmap formula: 1<<(player_id*16+slot_idx); slot [0..10], player [0..1]."),
    ("FUN_0804659c", "check_slot_equip_target_eligibility",
        "Checks if slot meets equip target conditions. "
        "Reads stack param 5 (extra_param); uses zone_flags bit1 to set extra_flag. "
        "Gets entity ref via get_zone_slot_entity_ref_by_type. "
        "Routes by field6: 0x16->query_slot_effect_eligibility_nonzero, "
        "0x17->check_slot_fieldspell_eligible_by_side. "
        "Also requires count_equip_chain_default_flags!=0 and "
        "find_equip_target_for_card_slot to succeed. "
        "r0=ptr card_slot_ptr; r1=u8 player_id [0..1]; "
        "r2=u8 zone_flags [0..0xF] (bit1=extra_flag trigger); "
        "r3=u8 zone_col [0..9]; sp+0x34=u32 extra_param. "
        "Returns u8 eligible_flag (1=eligible, 0=not). "
        "Callers: FUN_08047724, FUN_08046538. "
        "Constants: EQUIP_CONT=0x16, FIELD_SPELL=0x17, zone_flags_bit1=0x2."),
    ("FUN_08043644", "enqueue_sprite_attrs_for_card_chain_list",
        "Reads linked list head from slot [+0xa]; if non-zero, traverses chain. "
        "For each entry, reads byte[+0x2] bits[3:0] and compares with chain_type_filter. "
        "On match, calls enqueue_equip_slot_bitmap_update with [entry+0x0], [entry+0x1] "
        "and [entry+0x6] halfword. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u8 chain_type_filter [0..15]. Returns void. "
        "Called only by FUN_08044e30 (duel_field hub). "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "chain_entry_base=0x0201d9c0, link_field_offset=0xa, entry_size=8."),
    ("FUN_08044e30", "update_duel_field_slot_sprite_state",
        "Full sprite state update for a duel field slot (player_id, slot_idx, side_flag). "
        "Compares gP1LifePoints+offset control word bit5 against side_flag; exits if mismatch. "
        "Reads card_id (low 13 bits), calls set_field_slot_bit_with_sprite_update, "
        "then dispatches by slot_idx<=4 vs >4 to sub-paths calling enqueue_effect_card_slot_sprite_attr, "
        "enqueue_equip_card_sprite_attr_for_slot, enqueue_equip_slot_sprite_attr, "
        "enqueue_equip_chain_all_slots_for_pair, enqueue_sprite_attrs_for_card_chain_list, "
        "enqueue_paired_slot_sprite_attrs_for_player. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; r2=u8 side_flag [0..1]. "
        "Returns void. "
        "Callers: FUN_08044dcc, FUN_0805b990 (both duel_field). "
        "Constants: player_stride=0x868, ctrl_offset=0x40, card_id_shift=0x13, "
        "monster_zone_max=4."),
    ("FUN_08047724", "update_equip_target_bitmap_for_field",
        "Builds and updates equip target valid bitmap for current duel field state. "
        "Phase 1: iterates player=0..1 x slot=0..4, calls count_equip_chain_default_flags, "
        "writes bits to internal bitmap r9; calls build_equip_placement_valid_bitmap "
        "and stores in sp[0x10]. "
        "Phase 2: iterates player=0..1 x slot=0..10, filters spells via "
        "check_card_type_is_spell, dispatches by zone_type (0xb/0xd); "
        "calls scan_equip_zone_candidates_with_snapshot, count_field_copies_of_card, "
        "check_slot_equip_target_eligibility per slot. "
        "Finally writes combined sprite flags to gP1LifePoints+0x10d4 control field "
        "and calls increment_lp_bar_display_counter. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u8 zone_flags [0x0..0xF]; r3=u8 side_flags [0..2]. Returns void. "
        "25 callers (C_util_high, all duel_field). "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "equip_ctrl_offset=0x10d4, aux_offset=0x1ce8, "
        "chain_flags_param=0x1825, chain_entry_base=0x0201e1c8."),
    ("FUN_0804790c", "prepare_slot_ctx_for_equip_bitmap",
        "Initializes target struct (memset 0x18 bytes to zero), writes r1 (halfword) "
        "to [sp_buf+0x0], reads byte[r2+0x2] bit1 and merges into [r2+0x2], "
        "then calls update_equip_target_bitmap_for_field (zone_flags=0xe, side_flags=2). "
        "r0=u8 player_id [0..1]; r1=u16 slot_ref; r2=ptr card_slot_ptr. Returns void. "
        "Callers: enqueue_equip_slot_bitmap_update and 4 duel_field callers. "
        "Constants: memset_size=0x18, zone_flags=0xe, side_flags=0x2, bit1_mask=0x2."),
    ("FUN_0804794c", "enqueue_equip_slot_bitmap_update",
        "Computes slot bitmask 1<<(player*16+slot), then XORs player_id with r2 "
        "(player_xor_flag) and calls prepare_slot_ctx_for_equip_bitmap. "
        "Returns 1 if bitmap & slot_bit is nonzero, else 0. "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u8 player_xor_flag [0..1]; r3=ptr card_slot_ptr. "
        "Returns u8 slot_in_bitmap (1=in valid bitmap, 0=not). "
        "43 callers (C_util_high, all duel_field). "
        "Bitmap formula: 1<<(player_id*16+slot_idx)."),
    ("FUN_0805b990", "scan_equip_zone_candidates_with_snapshot",
        "Calls populate_effect_node_snapshot to fill stack snapshot struct (sp+0x0, 0x48 bytes). "
        "Then iterates player=0..1 x slot=0..9; for each slot with card_id!=0, "
        "runs check_card_is_zone_pair_restricted, check_card_field8_is_normal, "
        "handles special card ID rules, and dispatches monster (slot<=4) vs "
        "magic/trap (slot>4) sub-paths. On match calls "
        "update_duel_field_slot_sprite_state to refresh OAM. "
        "r0=ptr duel_field_ctx; r1=u8 slot_idx [0..0xa]; "
        "r2=u8 zone_flags [0..0xF]. Returns void. "
        "Callers: FUN_08047724, FUN_0806d960, FUN_08090218. "
        "Constants: player_stride=0x868, gDuelFieldSlots=0x0201c510, "
        "monster_zone_max=4, snapshot_size=0x48."),
    ("FUN_0804a334", "render_monster_slot_card_with_lp_bar",
        "Full display sequence for the card on the first available monster slot "
        "for a player: (1) reads field6/field9; if field6==0x16 and field9==2, "
        "calls enqueue_equip_slot_bitmap_update (slot=0xa, r2=0); "
        "(2) calls render_field_card_copy_count; "
        "(3) if slot has card, calls enqueue_sprite_attr_type11 (r1=0x198a); "
        "(4) calls submit_lp_bar_sprite_row_by_type (slot_key=0xa). "
        "r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9]; "
        "r2=u8 player_flag [0..1]. Returns void. "
        "Callers: FUN_0806c828, FUN_08095d84 (duel_field). "
        "Constants: player_stride=0x868, gDuelFieldSlots_offset=0x0201c600, "
        "FIELD6_EQUIP=0x16, FIELD9_TYPE2=0x2, slot_key=0xa, sprite_tile=0x198a."),
    # campaign-42 batch #42
    ("FUN_08095d84", "dispatch_lp_bar_animation_step",
        "LP bar animation state machine single-frame dispatcher. "
        "Reads state word at gP1LifePoints+0x1d60 (offset 0xeb<<5) and dispatches: "
        "state=0: calls render_monster_slot_card_with_lp_bar, writes result to +0x1d74, advances state; "
        "state=1: sets state to 2, skips render; "
        "other: r3!=0 -> init_card_sprite_row_entry_alt, r1==0 -> init_card_sprite_row_entry. "
        "Clears pending flag at gP1LifePoints+0x1d54 on exit. "
        "r0=u32 anim_mode [0..2]; r1=u32 use_alt_entry [0..1]; r2=ptr row_entry_ptr. Returns void. "
        "Callers: FUN_0804ce78, FUN_08085d4c, trigger_lp_bar_animation_if_ready (r0=1,r1=0,r2=0). "
        "Constants: state_offset=0x1d60, result_offset=0x1d74, pending_flag_offset=0x1d54."),
    ("FUN_08095ca0", "trigger_lp_bar_animation_if_ready",
        "Gate function for LP bar animation. "
        "Reads gP1LifePoints+0x1d44; if equal to 0x0fee, calls "
        "dispatch_lp_bar_animation_step(r0=1, r1=0, r2=0) and jumps to shared tail LAB_08095d32. "
        "Otherwise (LAB_08095ccc): writes 1 to 0x0201b290+0x9a*8 (sprite buffer flag); "
        "reads [gP1LifePoints+0x1d68], calls render_field_card_copy_count; "
        "if r0!=0 calls init_card_sprite_row_entry_alt else init_card_sprite_row_entry; "
        "writes 0 to [gP1LifePoints+0x1d54] (pending flag clear). "
        "r0=u32 player_bit_field (bit0=player_id [0..1]). Returns void. "
        "Callers: FUN_0804ce78, FUN_08085d4c. "
        "Constants: trigger_sentinel=0x0fee, sprite_buf_flag_addr=0x0201b290+0x4d0."),
    ("FUN_08093390", "trigger_card_display_op31_if_not_active",
        "Guard for card display slot activation. "
        "Reads state at 0x0201e2a0+0x8+slot_index*4; if state==1 (already active) returns immediately. "
        "Otherwise calls dispatch_card_display_op(op=0x31, r1=0, r2=display_param, r3=0). "
        "r0=u32 slot_index [0..N-1]; r1=u32 display_param (forwarded as r2 to dispatch). Returns void. "
        "indeg=119 (C_util_high). Callers: FUN_080563cc and 118 others."),
    ("FUN_080942dc", "get_monster_slot_entry_ptr",
        "Pure leaf. Reads active slot count from 0x0201e4f0+0x8, "
        "computes next-write address as base+0x10+count*4, and returns it. "
        "No parameters (r0-r3 unused at entry). Returns ptr to monster_slot_array[count]. "
        "indeg=26 (C_util_high). Callers: FUN_08057874, FUN_080598d8, FUN_08059b4c and others. "
        "Constants: monster_slot_base=0x0201e4f0, count_offset=0x8, entries_offset=0x10."),
    ("FUN_0809463c", "advance_prng_state",
        "LCG single-step advance. Reads 32-bit seed from gP1LifePoints+0x1ce0 (offset 0xe7<<5), "
        "computes new_seed = seed * 0x343fd + 0x269ec3 (standard C rand() parameters), "
        "writes new_seed back, then extracts bits[16..30] via (new_seed<<1)>>17 "
        "as 15-bit pseudo-random output. "
        "No input parameters (r0 overwritten at entry). Returns u16 prng_value [0..0x7fff]. "
        "Callers: sample_prng_scaled, FUN_0809457c, check_slot_palette_nonzero. "
        "Constants: seed_offset=0x1ce0, LCG_mul=0x343fd, LCG_inc=0x269ec3."),
    ("FUN_08094664", "sample_prng_scaled",
        "Wrapper around advance_prng_state for range-scaled random sampling. "
        "Calls advance_prng_state to get 15-bit prng value, multiplies by r0 (upper_bound), "
        "then shifts right 0xf (divides by 32768) to yield uniform integer in [0..upper_bound-1]. "
        "r0=u32 upper_bound [1..0x7fff]. Returns u32 random_index [0..upper_bound-1]. "
        "indeg=34. Callers: FUN_08031668, FUN_08031d44, FUN_08037c20 and others. "
        "Side effect: advances LCG seed at gP1LifePoints+0x1ce0."),
    ("FUN_08094564", "read_slot_palette_index",
        "Pure leaf. Reads palette index for a monster slot from "
        "0x0201e4f0+0x410+slot_index*2 (halfword), extracts high byte (>>8) and returns it. "
        "r0=u32 slot_index [0..N-1]. Returns u8 palette_index [0..255]. "
        "Callers: FUN_0809457c, check_slot_palette_nonzero. "
        "Constants: monster_slot_base=0x0201e4f0, palette_subarray_offset=0x410 (=0x82<<3)."),
    ("FUN_080ade34", "check_slot_palette_nonzero",
        "Boolean wrapper around read_slot_palette_index. "
        "Returns 1 if palette_index > 0 (slot occupied/active), 0 if empty. "
        "r0=u32 slot_index [0..N-1]. Returns u32 is_active [0..1]. "
        "Callers: find_first_empty_slot_for_card_type, find_random_empty_slot_excluding_card_id, "
        "find_slot_by_card_type_and_player, FUN_080ae050."),
    ("FUN_080ade8c", "find_random_empty_slot_excluding_card_id",
        "Two-phase scan over monster_slot array (0x0201e4f0). "
        "Phase 1: iterates all slots; for each slot with check_slot_palette_nonzero==0 (empty), "
        "reads card_id from 0x0201e500+idx*4 bits[18..0]; if card_id != target, increments r5 (eligible count). "
        "Phase 2: if r5>0, calls sample_prng_scaled(r5) to pick random offset, "
        "then re-scans to find the N-th eligible empty slot and returns its index. "
        "Returns -1 if no eligible slot found. "
        "r0=u32 card_id [0..0x7ffff] (exclude slots matching this ID). "
        "Returns i32 slot_index [0..N-1] or -1. "
        "Callers: FUN_080ae050."),
    ("FUN_080adf8c", "check_special_card_activation_eligible",
        "Activation eligibility check for specific special card IDs. "
        "Compares r0 (card_id) against hardcoded set {0x1366, 0x137d, 0x15e6}; "
        "on match reads slot card_id from 0x0201e500+r1*4 bits[18..0], "
        "then compares against {0x1596, 0x13c3, 0x1914}. "
        "For 0x1914: calls count_equipped_paired_slots_for_player for both players; "
        "if either has equipped pair returns 0 (ineligible). "
        "r0=u32 card_id [0..0x7fff]; r1=u32 slot_index [0..N-1]. "
        "Returns u32 eligible [0..1]. "
        "Callers: FUN_080ae050. "
        "Constants: special_ids={0x1366,0x137d,0x15e6}, pair_ids={0x1596,0x13c3,0x1914}."),
    ("FUN_08032f7c", "count_slot_card_pair_allowed_for_card",
        "Iterates slots 0..10 for player r0, calls check_slot_card_pair_allowed(player, slot_idx, card_id) "
        "for each, and counts allowed slots. Returns count [0..11]. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. "
        "Callers: FUN_080ac584, FUN_080acc30, check_compound_pair_activation_eligible, "
        "check_any_pair_slot_available_for_card, FUN_080b76e4."),
    ("FUN_080af914", "check_any_pair_slot_available_for_card",
        "Dual slot availability check for a card. "
        "First calls count_valid_monster_pair_slots(player, card_id & 0xffff); "
        "if non-zero returns 1. "
        "Then calls count_slot_card_pair_allowed_for_card(player, card_id); "
        "if non-zero returns 1. Returns 0 if both are zero. "
        "r0=u32 player_side [0..1]; r1=u32 card_id_packed (low 16 bits = card_id). "
        "Returns u32 any_slot_available [0..1]. "
        "Callers: FUN_080ac584, FUN_080acc30, FUN_080ae050, FUN_080bbf38."),
    ("FUN_080eef9c", "get_card_type_bits_by_internal_id",
        "Converts internal card_id to standard card_id via internal_card_id_to_card_id, "
        "then reads byte at card_attr_table (0x02000006) + card_id*2+1, "
        "masks low 2 bits (ands #0x3), and returns card type enum "
        "(0=monster, 1=spell, 2=trap, 3=other). "
        "r0=u16 internal_card_id [0..0xffff]. Returns u32 card_type_bits [0..3]. "
        "Callers: FUN_0807ed04, FUN_0807ee74, FUN_080ae050, FUN_080b58e8, FUN_080b70ac."),
    ("FUN_08037b34", "count_monster_slots_with_field5_ge_threshold",
        "Iterates all monster zone cards for player r0 "
        "(count at gP1LifePoints+player*0x868+0xc, entries at +0x120 subarray). "
        "For each card calls get_card_extended_stat_field5; "
        "if return >= threshold (r1, saved in r8) increments counter. "
        "Returns match_count. "
        "r0=u32 player_side [0..1]; r1=u32 field5_threshold [0..255] (known callsite: 7). "
        "Uses non-APCS r8 for threshold (mov r8,r1 via .hword 0x4688). "
        "Callers: FUN_080ae050 (with r1=7). "
        "Constants: player_stride=0x868, monsters_offset=0xc, subarray_offset=0x120 (=0x90<<1)."),
    ("FUN_080af534", "check_card_id_in_eligible_set",
        "Pure leaf. Binary-search-style comparison tree checking if r0 (card_id) "
        "belongs to a predefined whitelist including: "
        "0x14ac, 0x130c, 0x10f4, 0x12ac, 0x1302, 0x140e, 0x134a, 0x1468, 0x147c, "
        "0x1645, 0x15ee, 0x1636, 0x1770, 0x166c, 0x172c, 0x1855, 0x185c, 0x1992 and others. "
        "LAB_080af696 path returns 1; LAB_080af68c path returns (r1==0 ? 1 : 0); "
        "LAB_080af69a returns 0. "
        "r0=u32 card_id [0..0x7fff]; r1=u32 mode_flag [0..1]. "
        "Returns u32 eligible [0..1]. "
        "indeg=7. Callers: FUN_080ae050, FUN_080af6a0, FUN_080af72c, FUN_080b5348, FUN_080b54c0."),
    ("FUN_080adf40", "find_slot_by_card_type_and_player",
        "Linear scan over monster_slot array (0x0201e4f0, count at [+0xc]). "
        "For each slot with check_slot_palette_nonzero==0 (empty): "
        "reads slot data word from 0x0201e500+idx*4, extracts bits[18..0] as card_type "
        "and bit[13] (via lsrs#0x12) as player_id; "
        "if both match r1 (card_type) and r0 (player_id) returns slot index. "
        "Returns -1 if not found. "
        "r0=u32 player_id [0..1]; r1=u32 card_type [0..0x7ffff]. "
        "Returns i32 slot_index [0..N-1] or -1. "
        "Callers: FUN_080ae050."),
    ("FUN_080ade48", "find_first_empty_slot_for_card_type",
        "Linear scan over monster_slot array (0x0201e4f0, count at [+0xc]). "
        "For each slot with check_slot_palette_nonzero==0 (empty): "
        "reads slot data from 0x0201e500+idx*4, extracts bits[18..0] card_type; "
        "if matches r0 returns slot index. "
        "Returns -1 if not found. "
        "Differs from find_slot_by_card_type_and_player: no player check. "
        "r0=u32 card_type [0..0x7ffff]. "
        "Returns i32 slot_index [0..N-1] or -1. "
        "Callers: FUN_080ae050."),
    ("FUN_08031a84", "count_zone_card_pair_allowed_for_card",
        "Iterates all monster zone cards for player r0 "
        "(count at gP1LifePoints+player*0x868+0x10). "
        "For each card reads card_id (bits[18..0]) and calls "
        "check_card_pair_allowed(card_id, r1); if allowed increments counter. "
        "Returns match_count. "
        "r1 (card_id threshold) saved in r8 via .hword 0x4688 = mov r8,r1. "
        "r0=u32 player_side [0..1]; r1=u16 card_id [0..0xffff]. "
        "Callers: check_compound_pair_activation_eligible. "
        "Constants: player_stride=0x868, zone_count_offset=0x10."),
    ("FUN_080af8cc", "check_compound_pair_activation_eligible",
        "Four-fold compound pairing activation check; returns 1 if any condition met. "
        "Sequentially calls: "
        "(1) count_zone_card_pair_allowed_for_card(player, card_id & 0xffff); "
        "(2) count_valid_monster_pair_slots(player, card_id & 0xffff); "
        "(3) count_extra_deck_cards_by_id(player, card_id); "
        "(4) count_slot_card_pair_allowed_for_card(player, card_id_packed). "
        "Returns 0 only if all four are zero. "
        "r0=u32 player_side [0..1]; r1=u32 card_id_packed (low 16 bits = card_id). "
        "Returns u32 any_condition_met [0..1]. "
        "Callers: FUN_080a3130, FUN_080acc30, FUN_080ae050."),
    ("FUN_080abf64", "eval_zone_slot_score_for_player",
        "Computes score entry for zone slot r1 of player r0, writing into score_out (r2). "
        "Slot base = 0x0201c510 + (player_id&1)*0x868 + slot_index*0x14. "
        "If slot[+0x8] halfword != 0: calls eval_slot_score_entry_full directly. "
        "Else reads card_id from slot[0], checks slot[+0x11] bit7 (activation flag): "
        "if active: temporarily writes slot[+0x8], calls eval_slot_score_entry_full, restores; "
        "if not active: calls get_card_extended_stat_field5; "
        "field5<=4 -> score_out[0x14]=0x4b0, score_out[0x18]=0x708; "
        "field5>4 -> score_out[0x14]=0x834. "
        "Writes score_out[0x00/0x04/0x08/0x10/0x14/0x18]. "
        "r0=u32 player_bit_field (bit0=player_id [0..1]); r1=u32 card_slot_index [0..N-1]; "
        "r2=ptr score_out. Returns void. "
        "Uses non-APCS high registers: r8=base addr (0x0201c510), r12=1 (constant). "
        "Callers: FUN_080ac004, FUN_080ae050, FUN_080aef1c, FUN_080aefc4, FUN_080af070. "
        "Constants: zone_base=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "score_low_threshold=4, score_A=0x4b0, score_B=0x708, score_C=0x834."),

    # 2026-05-13: campaign-43 batch #43 (topo=856..913, 20 fns)
    ("FUN_08033370", "count_active_cards_in_zone_by_player",
        "Iterates first 4 zone slots of gDuelFieldSlots for the given player_side, "
        "counts slots where bit9 is set (active) and slot[+6] card_id matches target_card_id. "
        "r0=u32 player_side [0..1]; r1=u16 target_card_id. Returns u32 count [0..4]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "active_bit=bit9, loop_count=4."),
    ("FUN_080aec7a", "exit_slot_search_with_result",
        "Shared epilogue thunk for find_empty_slot_for_card_id_dispatch (FUN_080ae050). "
        "Body is pure callee-restore epilogue: add sp,#0x2c + pop r8/r9/r10 via .hword 0x46xx "
        "+ pop {r4..r7} + pop {r1}; bx r1. "
        "Called by FUN_080ae050 when a valid slot (>=0) is found (5 callsites). "
        "No independent business logic; mirrors the push/sub-sp prologue of FUN_080ae050."),
    ("FUN_080ae050", "find_empty_slot_for_card_id_dispatch",
        "Uses r1 (card_id) as key via multi-range BST + linear search to find an empty field slot. "
        "Checks [0x0201e4f0+0xc] global activation state; if 0 skips main body. "
        "Dispatches by card_id range: calls check_compound_pair_activation_eligible, "
        "find_first_empty_slot_for_card_type, find_slot_by_card_type_and_player, "
        "find_random_empty_slot_excluding_card_id. "
        "On slot found (>=0) calls exit_slot_search_with_result (FUN_080aec7a) to return. "
        "Side effect: [0x0201afe0] = r0 (card_slot_ptr, current card processing ctx). "
        "r0=ptr card_slot_ptr; r1=u16 card_id; r2=u32 player_side [0..1]. "
        "Returns s32 slot_index (>=0) or -1."),
    ("FUN_080aece4", "fill_effect_slots_up_to_count",
        "Loops calling find_empty_slot_for_card_id_dispatch (FUN_080ae050) to fill up to "
        "max_count effect slots, then calls write_effect_ctx_slot_index + set_tile_palette_index_in_buf "
        "for each found slot (palette index = loop counter r4). "
        "Triggered by init_effect_slot_display_context (FUN_080941c4) for card effect type [0x7..0x26]. "
        "Side effects: [gP1LifePoints+0x1d40]=r4 (final slot count); "
        "[0x0201afe0]=card_slot_ptr (via FUN_080ae050). "
        "r0=ptr card_slot_ptr; r1=u16 card_id_a; r2=u16 card_id_b; r3=u32 max_count [0..N]. "
        "Returns u32 actual_filled_count [0..max_count]. "
        "Constants: gP1LifePoints+0x1d40 = effect_slot_count_field."),
    ("FUN_080aec8c", "activate_effect_slot_for_card",
        "Activates a single effect slot for one card: calls dispatch_effect_handler_by_card_id; "
        "if non-zero writes [0x0201afe0]=card_slot_ptr, calls find_empty_slot_for_card_id_dispatch "
        "to get slot r4, then write_effect_ctx_slot_index(r4) + set_tile_palette_index_in_buf(r4,1) "
        "+ [gP1LifePoints+0x1d40]=1. "
        "Triggered by init_effect_slot_display_context for card_type==6 or 0x49. "
        "r0=ptr card_slot_ptr; r1=u16 card_id; r2=u32 context_param. "
        "Returns s32 slot_index (>=0) or -1. "
        "Side effects: [0x0201afe0]=card_slot_ptr; [gP1LifePoints+0x1d40]=1."),
    ("FUN_080aed4c", "fill_effect_slots_up_to_count_with_equip_cap",
        "Symmetric to fill_effect_slots_up_to_count (FUN_080aece4) but adds special handling "
        "when r8 (card_id_b) == 0x18e0 (0xc7*0x20): calls count_equip_slots_active_only(1-r7) "
        "and uses its result to further cap max_count. "
        "Triggered by init_effect_slot_display_context for card effect type [0x28..0x47]. "
        "Side effects: [gP1LifePoints+0x1d40]=r4 (final count); [0x0201afe0]=card_slot_ptr. "
        "r0=ptr card_slot_ptr; r1=u32 player_side_or_ref; r2=u16 card_id_b; r3=u32 max_count. "
        "Returns u32 actual_filled_count. "
        "Constants: 0x18e0=special_card_id_threshold; gP1LifePoints+0x1d40=effect_slot_count_field."),
    ("FUN_080941c4", "init_effect_slot_display_context",
        "Effect slot display context init hub (indeg=39). "
        "Saves r0..r3 to r6/r5/r7/r8, loads gEffectDisplayCtx (0x0201e4f0): "
        "writes [+0x0]=card_slot_ptr, [+0x4]=card_type, [+0x8]=0; "
        "zero-fills [+0x10..+0x20f] and [+0x410..+0x50f]. "
        "Dispatches by card_type: type==6 or 0x49 -> activate_effect_slot_for_card; "
        "type [7..37] -> fill_effect_slots_up_to_count (max=type-6); "
        "type [0x28..0x47] -> fill_effect_slots_up_to_count_with_equip_cap (max=type-0x27); "
        "type > 0x49 -> [gP1LifePoints+0x1d40]=0x161c; "
        "default -> dispatch_effect_handler_by_card_id + dispatch_card_display_op(0x32). "
        "r0=ptr card_slot_ptr; r1=u32 card_type; r2=u32 player_side_or_ref; r3=u32 extra_param. "
        "Returns void. "
        "Constants: gEffectDisplayCtx=0x0201e4f0, zero_fill_1=0x200 bytes, "
        "zero_fill_2=0x100 bytes, 0x161c=special_count_value."),
    ("FUN_08097150", "dispatch_to_effect_handler_by_card_type",
        "Linear scans ROM effect handler table (DAT_0809717c=0x09e47560) "
        "with entry stride=0x10, up to 0x11 (17) entries. "
        "Matches r1 (card_type) against entry[+0x0]; on match reads handler ptr at [+0xc+offset] "
        "and calls FUN_0810e5d4(r5, r4, r6, r3). "
        "r0=ptr context_ptr; r1=u16 card_type; r2=u32 sub_param. Returns void. "
        "Callers: dispatch_effect_slot_by_display_state (state==2 path), FUN_080bb414."),
    ("FUN_08095ec4", "dispatch_effect_slot_by_display_state",
        "Reads [gP1LifePoints+0x1d60] (0xeb<<5) display state; dispatches 0/1/2: "
        "state==0: trigger_card_display_op31_if_not_active(r6, 0x114); "
        "state==1: init_effect_slot_display_context(r6, 6, r7) then state++; "
        "state==2: reads monster slot fields via get_monster_slot_entry_ptr x3, "
        "calls dispatch_to_effect_handler_by_card_type, clears [gP1LifePoints+0x1d54]=0. "
        "r1=u32 context_ptr (saved as r6); r2=u32 sub_param. Returns void. "
        "Side effects: [gP1LifePoints+0x1d60]+=1 (state 0/1); [gP1LifePoints+0x1d54]=0 (state 2). "
        "Caller: FUN_08085d4c (effect slot display update driver)."),
    ("FUN_080933c8", "invoke_card_display_op_0x31_with_params",
        "4-instruction thunk: reorders r0/r1 as dispatch_card_display_op args. "
        "Fixed op=0x31 (copy_game_text_to_card_name_vram), sub1=0x2. "
        "Actual call: dispatch_card_display_op(0x31, 0x2, r0_in, r1_in). "
        "Sibling of invoke_card_display_op_0x31 (0x0809355c) which uses fixed 4-arg form. "
        "r0=ptr card_slot_ptr (becomes dispatch r2); r1=u32 sub_param (becomes dispatch r3). "
        "Callers: FUN_0804ce78 (card name display), FUN_08085d4c (effect slot render)."),
    ("FUN_0804394c", "enqueue_zone_card_sprite_attr_by_slot",
        "Reads gDuelFieldSlots[player_side][slot_idx]; if bit9 set (slot occupied), "
        "builds OAM sprite attr and calls enqueue_sprite_attr_record. "
        "OAM_ATTR0_BASE=0x8035 (Y_pos[7:0]=0x35, bit15=1, 4bpp square shape). "
        "slot offset = slot_idx*0x14; player offset = (player_side&1)*0x868. "
        "slot[+8] halfword: 0 -> flip_flag=1, non-zero -> flip_flag=0. "
        "Calls enqueue_sprite_attr_record(0x8035, slot_idx_masked, flip_flag, 4). "
        "r0=u32 player_side [0..1]; r1=u32 slot_idx [0..10]. Returns void. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "OAM_ATTR0_BASE=0x8035, OAM_count=4."),
    ("FUN_08095ba8", "init_equip_card_sprite_row_entry",
        "Initializes OAM sprite row entry for an equip card. "
        "Reads player_bit from [gP1LifePoints+0x1d68], base_slot_a from [+0x1d6c], "
        "slot_b from [+0x1d70]; slot_idx = slot_a + slot_b. "
        "If slot[+0x38]==0 (not yet rendered): calls enqueue_zone_card_sprite_attr_by_slot. "
        "Else: builds OAM attr0 word and calls init_card_sprite_row_entry_alt or "
        "init_card_sprite_row_entry (fallback). "
        "Clears [gP1LifePoints+0x1d54]=0 at end. "
        "r0=u32 context_extra (saved to r8 via .hword 0x4680=mov r8,r0). Returns void. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, "
        "slot_rendered_offset=0x38; gP1LifePoints offsets 0x1d44/0x1d48/0x1d54/0x1d68/0x1d6c/0x1d70. "
        "Callers: FUN_0804ce78, FUN_08085d4c (equip card display sequence)."),
    ("FUN_08096988", "write_card_display_ctx_fields",
        "Leaf function (bx lr). Writes 5 gP1LifePoints fields for card display context init. "
        "Side effects: [gP1LifePoints+0x1d4c]=r0 (display_key); "
        "[+0x1d7c]=0; [+0x1d58]=0; [+0x1d54]=0; "
        "[+0x1d64]=[gDuelActivation+4] (copy activation slot ref). "
        "r0=u32 display_key (card_id or display area id). Returns void. "
        "Constants: gP1LifePoints, gDuelActivation=0x0201e2a0; "
        "offsets 0x1d4c/0x1d7c/0x1d58/0x1d54/0x1d64. "
        "indeg=6; all callers are card_frame+card_ids context."),
    ("FUN_080af940", "check_effect_zone_available_for_player",
        "Checks if specified player side has any available effect zone slot. "
        "Reads gP1LifePoints[player_side&1 * 0x868 + 0xc] (zone count); "
        "if > 6 returns 1 (full). Otherwise calls count_available_effect_zones(player_side, 0x1387, -1). "
        "count > 0 -> return 0 (slot available); count == 0 -> return 1 (no slot). "
        "r0=u32 player_side [0..1]. Returns u32: 0=available, 1=no slot. "
        "Constants: player_stride=0x868, zone_count_offset=0xc, zone_limit=6, "
        "zone_id=0x1387, quota=-1. "
        "Callers: FUN_080b499c, FUN_080baed0, FUN_080bb9b8 (duel_field activation eval)."),
    ("FUN_0805bc48", "check_card_normal_summon_eligible_full",
        "Multi-condition normal summon eligibility check for card r1 (card_id), player r0. "
        "Entry: populate_effect_node_snapshot; check_card_is_zone_pair_restricted -> return 0 if restricted. "
        "Branches on get_card_extended_stat_field6==0x17 (compound) or not, "
        "checks field9==2/3/4, check_card_field5_is_nonzero, find_effect_node_in_zone. "
        "Also checks count_occupied_monster_zones_with_effect_bonus>=3 -> "
        "count_available_effect_zones(player, DAT=0x1955, -1)==0 -> return 0. "
        "End: slot[+2] & 0x303e==0x201c && count_field_copies_of_card(0x17b9)>0 -> "
        "FUN_0803088c (non-type-0xe slot summon check). "
        "r0=u32 player_side [0..1]; r1=u16 card_id. Returns u32: 1=eligible, 0=not. "
        "Constants: field6_compound=0x17, zone_limit=3, 0x1302=specific_card, "
        "0x303e/0x201c=status_mask/value, 0x17b9=card_id_check."),
    ("FUN_08037a8c", "find_zone_slot_idx_allowed_for_card",
        "Scans gDuelFieldSlots for player_side, returns first slot index where "
        "check_card_pair_allowed(slot_card_id, target_card_id) passes. "
        "Zone count upper bound from gP1LifePoints[side*0x868+0xc]. "
        "Slot card_id extracted as low 13 bits (lsls/lsrs #0x13). "
        "r0=u32 player_side [0..1]; r1=u16 target_card_id. Returns s32 slot_idx (>=0) or -1. "
        "indeg=8. Constants: player_stride=0x868, zone_count_offset=0xc, slot_pool_offset=0x120."),
    ("FUN_0804c38c", "classify_card_id_summon_category",
        "Large BST: classifies card_id r0 into 3 summon/effect categories. "
        "Returns 0 = no category (not in any known range), "
        "1 = category-1 (primary range including up to 0x1631), "
        "2 = category-2 (special subset e.g. 0x19c0/0x19d7). "
        "Used by check_effect_slot_summon_path_eligible (FUN_0803088c) to decide activation path. "
        "r0=u16 card_id [0..0x1fff]. Returns u32 category [0..2]. "
        "Constants: upper_bound=0x1631, special_card=0x1488; "
        "exit labels: LAB_0804c6be->1, LAB_0804c6c2->2, LAB_0804c6c6->0."),
    ("FUN_0803088c", "check_effect_slot_summon_path_eligible",
        "Iterates effect slot group pointed to by r0; skips slots with type==0xe "
        "(bits[23:16] from read_effect_slot_side_and_type). "
        "After loop: calls classify_card_id_summon_category on slot[+0x0] (card_id). "
        "category==1 -> return 1 (eligible); "
        "category==2 -> checks specific card_ids (0x1534/0x133b/0x1449/0x1452 etc.) "
        "and slot[+3] bit4/5 (0x10/0x20 summon flags) -> return 0 or 1; "
        "category==0 -> return 0. "
        "r0=ptr effect_slot_group (contains [+0]=card_id, [+3]=flags, [+4]=slot_count). "
        "Returns u32: 1=normal-summon-path eligible, 0=not. "
        "Constants: type_skip=0xe; summon path card_ids: 0x1534/0x133b/0x1449/0x1452/0x19c0 etc."),
    # --- batch #44 (campaign-44) ---
    ("FUN_080b499c", "check_normal_summon_eligible_for_slot",
        "Full eligibility check for normal summon of a single card slot, with summon target init on pass. "
        "r0=player_id [0..1]; r1=slot_ptr ([r1+0]=card_id); r2=mode_flag [0..1]. "
        "Scans gDuelCardMain (0x0201b290+0xc0<<2) for matching card_id+mode_flag entry: "
        "found -> path B (equip activation via find_zone_slot_idx_allowed_for_card); "
        "not found -> path A: check_card_field5_is_nonzero + check_card_normal_summon_eligible_full. "
        "Both paths write [gP1LifePoints+0x1d64]:=player_id and call init_duel_zone_target_slot_refs. "
        "Returns u32: 1=eligible+initialized, 0=not eligible. "
        "Constants: gDuelCardMain=0x0201b290+0x300, gDuelEffectZones=0x0201c510, player_stride=0x868."),
    ("FUN_080bb3dc", "check_normal_summon_eligible_for_any_effect_zone",
        "Scans up to 0xce effect zone entries (base=0x09e48918, stride=8) for player r0. "
        "For each entry: check_card_field5_is_nonzero; if valid call check_normal_summon_eligible_for_slot(player, entry, 0). "
        "Returns u32: 1=any effect zone card passes normal summon eligibility, 0=none. "
        "r0=u32 player_id [0..1]. "
        "Constants: effect_zone_base=0x09e48918, max_entries=0xce, entry_stride=8."),
    ("FUN_080b4ba8", "check_normal_summon_eligible_any_slot",
        "Checks whether player r0 has any card slot or effect zone satisfying normal summon eligibility. "
        "Writes r0 to [0x0201afe0] (current player ptr). "
        "Iterates gDuelCardMain (0x09e478d0) up to 0xdd slots (stride=8): "
        "calls check_normal_summon_eligible_for_slot(player, slot, 0) per slot; returns 1 on first pass. "
        "Falls back to check_normal_summon_eligible_for_any_effect_zone(player). "
        "Returns u32: 1=eligible slot exists, 0=none. "
        "r0=u32 player_id [0..1]. Constants: player_ptr=0x0201afe0, gDuelCardMain=0x09e478d0, max_slots=0xdd."),
    ("FUN_08085430", "build_sprite_row_from_zone_state",
        "Builds one sprite row from zone state data and submits it. "
        "r0=player_id [0..1]: selects sprite type (0->0xb, 1->0xc). "
        "Reads [gP1LifePoints+0x1d08] guard word: 0 -> skip. "
        "Reads gDuelCardBase+0x4cc for dest row buf ptr; reads byte array at +0x4d4 and word array at +0x4f4; "
        "packs byte+low16+high16 per slot (6 bytes each) into dest buf. "
        "Calls submit_sprite_row_data with sprite_count from row header and stride per slot. "
        "Returns void. "
        "Constants: gP1LifePoints=0x0201c4e0, state_guard_off=0x1d08, gDuelCardBase=0x0201b290."),
    ("FUN_0801f238", "copy_game_text_if_raw",
        "Copies a game string to dest buf r0: if r1 is a raw string ID (high 15 bits == 0, "
        "mask 0xFFFE0000 & r1 == 0) calls resolve_game_str_ptr(r1) then strcpy; "
        "otherwise uses r1 directly as pointer for strcpy. "
        "r0=u8* dest; r1=u32 str_handle (raw ID or resolved ptr). Returns void. "
        "Side effects: writes NUL-terminated string to [r0..]. "
        "Constants: RAW_ID_MASK=0xFFFE0000."),
    ("FUN_0801f25c", "append_game_text_if_raw",
        "Appends a game string to end of dest buf r0 (strcat variant of copy_game_text_if_raw). "
        "If r1 high 15 bits == 0 calls resolve_game_str_ptr(r1) then strcat; "
        "otherwise uses r1 directly as pointer for strcat. "
        "r0=u8* dest (existing content); r1=u32 str_handle. Returns void. "
        "Side effects: appends NUL-terminated string to [r0 end..]. "
        "Constants: RAW_ID_MASK=0xFFFE0000."),
    ("FUN_08085a50", "build_field_action_text_by_zone_type",
        "Builds field action description string into dest buf r0 based on active zone type code. "
        "Zeroes [r4] (dest buf first byte); reads [gDuelCardBase+0x4cc] ctrl word: 0 -> empty string. "
        "Reads type byte at +0x4d4 as switch key (r3-1, upper bound 0x1d, 30 cases). "
        "Each case calls copy_game_text_if_raw(r4, str_id) for zone-specific string. "
        "Tail (caseD_11): if [r4+0] non-empty appends separator (0x09e3f14c) via append_game_text_if_raw; "
        "then appends fixed tail str_id=0x10d. Returns void. "
        "Constants: gDuelCardBase=0x0201b290, ctrl_off=0x4cc, type_off=0x4d4, tail_id=0x10d."),
    ("FUN_08094800", "check_all_equip_target_slots_available",
        "Checks whether all equip target slots are available for player r0. "
        "First calls count_available_effect_zones(player, 0x1468, -1): 0 -> return 0. "
        "Then calls find_equip_slot_by_card_id 4 times with IDs 0x1497/0x1498/0x1499/0x149a: "
        "any returns < 0 -> return 0. All non-negative -> return 1. "
        "r0=u32 player_id [0..1]. Returns u32: 1=all slots available, 0=at least one unavailable. "
        "Constants: effect_zone_id=0x1468, equip_slot_ids=0x1497..0x149a."),
    ("FUN_080947a0", "check_all_fusion_pair_slots_available",
        "Checks whether all 5 fusion pair slots are valid for player r0. "
        "Calls count_valid_monster_pair_slots 5 times with IDs 0x0fb7/0x0fb8/0x0fb9/0x0fba/0x0fbb. "
        "Any returns 0 -> return 0 immediately. All non-zero -> return 1. "
        "r0=u32 player_id [0..1]. Returns u32: 1=all 5 fusion pair slots valid, 0=at least one invalid. "
        "Constants: fusion_slot_ids=0x0fb7..0x0fbb."),
    ("FUN_08094864", "query_summon_eligibility_code",
        "Returns the highest-priority summon eligibility code for player r0 (priority 0..9). "
        "Checks in order: opponent field non-empty->2; check_all_fusion_pair_slots_available->3; "
        "check_all_equip_target_slots_available->4; check_node_in_slot_chain series->5/6/7/8/9; "
        "hand empty ([gP1LifePoints+0x28+player*0x868]==0)->1; else->0. "
        "r0=u32 player_id [0..1]. Returns u32 code [0..9] (0=cannot summon, 1=hand empty, "
        "2=opponent occupied, 3=fusion, 4=equip, 5-9=chain states). "
        "Constants: gP1LifePoints=0x0201c4e0, player_stride=0x868, hand_off=0x28, field_off=0x20."),
    ("FUN_0809495c", "check_normal_summon_eligibility",
        "Checks and updates summon eligibility state for both players each frame. "
        "Reads [gP1LifePoints+0x1d08] guard; if non-zero checks [+0x1ce8] vs [gDuelSettings+0x4]^1: "
        "match -> return 0 (already handled). "
        "Calls query_summon_eligibility_code for player 0 and 1; writes results to "
        "[gP1LifePoints+0x2c+player*0x868] (summon code fields). "
        "Both 0 -> check [+0x10dc]; at least one non-zero -> write [+0x1cfc]/[+0x10dc] and return 1. "
        "r0..r3: no APCS inputs. Returns u32: 0=no change, 1=new summon state detected. "
        "Constants: gP1LifePoints=0x0201c4e0, gDuelSettings=0x0201e2a0, player_stride=0x868."),
    ("FUN_080854b8", "scan_equip_target_slots_for_card",
        "Scans equip target slot list to determine if card r0 (card_id) has any valid equip target. "
        "r1=slot_ptr (start). Reads byte per slot from gDuelCardBase+0x4d4; byte-1 as switch key "
        "(switchD_080854da, 30 cases); each case checks r4 (card_id) against allowed equip target range. "
        "Match -> return 1 (caseD_d); no match -> slot_counter++; all checked -> return 0. "
        "r0=u32 card_id; r1=ptr slot_ptr. Returns u32: 1=valid target found, 0=none. "
        "Constants: gDuelCardBase=0x0201b290, slot_byte_base_off=0x4d4."),
    ("FUN_08085838", "scan_all_zones_for_equip_target",
        "Scans all field zones of both players for a valid equip target. "
        "Outer loop r6=[0..1] (player), inner r5=[0..0xa] (slot stride 0x14): "
        "reads gDuelCardSlots (0x0201c510) slot field5 (bits 13..0); if non-zero calls "
        "setup_equip_context_for_slot_activation; if valid calls scan_equip_target_slots_for_card. "
        "Second pass scans gDuelEffectZones (0x0201c600) with r1 (equip_flag) via "
        "setup_equip_context_for_zone_activation + scan_equip_target_slots_for_card. "
        "Returns u32: 1=found, 0=not found. "
        "r0=u32 player_id [0..1]; r1=u32 equip_flag. "
        "Constants: gDuelCardSlots=0x0201c510, gDuelEffectZones=0x0201c600, player_stride=0x868."),
    ("FUN_08085d4c", "dispatch_field_display_state_by_type",
        "Dispatches field display handling based on display type code read from gDuelCardBase+0x578. "
        "Reads [gDuelCardBase+0x57c] as ctrl value (r4); reads type code [+0x578]: "
        ">0x32 -> caseD_3 return 1 (skip). Otherwise indexes switchD_08085d70 (51 entries). "
        "case 0: check_normal_summon_eligibility; case 1: scan_all_zones_for_equip_target + "
        "check_normal_summon_eligible_any_slot + invoke display op; case 0xa: write_card_display_ctx_fields; "
        "case 0x14: build_sprite_row_from_zone_state; default: return 1. "
        "r0..r3: no APCS inputs. Returns u32: 0=busy (action taken), 1=done/skip. "
        "Constants: gDuelCardBase=0x0201b290, type_off=0x578, ctrl_off=0x57c, type_limit=0x32."),
    ("FUN_0804f0c2", "clear_sprite_row_queue_overflow_flag",
        "Clears sprite row queue overflow flag word and returns 1. "
        "Loads gSpriteRowBase (0x0201b290) + 0x93<<3 (=0x498); stores 0 to that address. "
        "Restores frame (add sp,#0x2c + callee-restore) and returns r0=1. "
        "Called by dispatch_sprite_row_queue_by_state when state_code > 0x67 (overflow). "
        "Also serves as default fallback for dispatch table indices 8..0x67. "
        "r0..r3: no APCS inputs. Returns u32: 1 (fixed). "
        "Side effects: [0x0201b290+0x498] := 0."),
    ("FUN_0804db50", "dispatch_sprite_row_queue_by_state",
        "Dispatches sprite row queue processing based on current state code. "
        "Reads [gSpriteRowBase+0x480] read-ptr to compute row stride; "
        "reads state code [+0x49c]: >0x67 -> call clear_sprite_row_queue_overflow_flag; "
        "else index dispatch table PTR_DAT_0804dbb8 (indices 0..7=8 handlers, 8..0x67=overflow fallback). "
        "r0..r3: no APCS inputs. Returns u32 passthrough from dispatched handler. "
        "Side effects: sub-handlers may modify gSpriteRowBase internal state fields. "
        "Constants: gSpriteRowBase=0x0201b290, read_ptr_off=0x480, state_code_off=0x49c, limit=0x67."),
    ("FUN_0808e600", "enqueue_equip_chain_sprites_for_zones",
        "Scans both players effect zones for active equip chain cards and enqueues OBJ sprite attrs. "
        "Entry: checks [gP1LifePoints+0x10d0] bit0 + [+0x1d28]<=8 -> return 0 (cooldown). "
        "Outer r5=[0..1] (player); inner scans gDuelActivation effect zone list (5 slots per player): "
        "test_slot_has_active_card; checks field5 bitmask and chain flags; "
        "count_equip_chain_default_flags + eval_slot_target_eligibility_full; on pass: "
        "builds OBJ attr word and calls enqueue_sprite_attr_with_mode(slot, zone_idx, attr, 0x9). "
        "On hits: enqueue_sprite_attr_by_sign + prepare_slot_ctx_for_equip_bitmap. "
        "r0..r3: no APCS inputs. Returns u32: 1=enqueued, 0=none. "
        "Constants: gP1LifePoints=0x0201c4e0, gDuelActivation=0x0201e1c8, attr_mode=0x9."),
    ("FUN_0808fe84", "apply_equip_activation_from_zone_scan",
        "Scans both players effect zones for card_type=0x18b2 (equip card type) and applies activation. "
        "r8=0/r9=gP1LifePoints/r10=1 manage two-player scan; inner r7=[0..4] (zone slot index). "
        "Reads slot [+0] bit13..0 (card_type); filters card_type==0x18b2 and valid slot. "
        "Calls apply_equip_activation_with_id_lookup then enqueue_sprite_attr_with_xy_split per match. "
        "r0..r3: no APCS inputs. Returns u32: 1=found and activated, 0=none. "
        "Side effects: writes EWRAM equip state; enqueues OBJ sprite attrs. "
        "Constants: gDuelEffectZones=0x0201c510, target_card_type=0x18b2, player_stride=0x868."),
    ("FUN_08094f20", "write_card_display_index_if_above_bit",
        "Conditionally writes card display index entry only if target_index > current bit value. "
        "r0=ptr card_entry; r1=u32 target_index [0..0xFF]. "
        "Calls get_card_data_bit_by_index(r0, r1) -> r0; if r1 > r0 calls write_card_display_index_entry(r4, r5). "
        "Returns void. indeg=7. Used by 5 hub callers to ensure only higher-priority index is written. "
        "Side effects: if r1>bit_value: write_card_display_index_entry(card_entry, target_index)."),
    ("FUN_08095084", "write_monster_zone_display_indices",
        "Scans both players monster zones, scores each slot and writes display indices via "
        "write_card_display_index_if_above_bit (0x08094f20). "
        "Phase 1: iterates gDuelEffectZones 5 slots (stride 0x14): "
        "reads slot field5 (bit 13..0); if non-zero: stmia into collect buf, r8++; "
        "get_slot_field5_score(player, idx) -> write_card_display_index_if_above_bit(0, score); "
        "check_slot_placement_blocked_by_field_effect -> r10++. "
        "Phase 2 (r8>=3): check_card_pair_allowed for each slot pair -> "
        "any >=2 pairs valid: write_card_display_index_entry(0x3b, 1). "
        "r8==5: write index=0x3c; r10==5: write index=0x3d. "
        "r0..r3: no APCS inputs. Returns void. "
        "Constants: gDuelSettings=0x0201e2a0, gDuelEffectZones=0x0201c510, player_stride=0x868."),
    ("FUN_0805bcf0", "check_card_special_summon_eligible_full",
        "Multi-layer special summon eligibility check for card_slot_ptr r0. "
        "Entry: check_card_field5_is_nonzero, check_card_field8_is_normal (both must pass). "
        "Then: find_zone_descriptor_by_slot_id, get_card_field_summon_restriction, "
        "count_field_copies_of_card (0x148e/0x14da/0x166c), check_value_in_slot_chain, "
        "count_occupied_monster_zones_with_effect_bonus>=3 -> count_available_effect_zones==0 -> 0. "
        "For zone_type [5..0xa]: bl check_card_normal_summon_eligible_full; "
        "then count_field_copies_of_card(0x159d) + check_effect_slot_summon_path_eligible. "
        "End: slot[+2] & 0x303e==0x201c -> count_field_copies_of_card(0x17b9)->eligible. "
        "r0=ptr card_slot_ptr (slot[+0]=card_id, slot[+2]=flags, slot[+4]=zone_bits). "
        "Returns u32: 1=special-summon eligible, 0=not. "
        "indeg=3: FUN_0809f21c, FUN_080ad974, FUN_080bae6c."),
    ("FUN_080bae6c", "check_card_summon_eligible_by_field6",
        "Determines player_side and zone_id from get_card_extended_stat_field6 value "
        "(0x16 -> zone_id=0x17d4; 0x17 -> zone_id=0x17c6; default -> zone_id=0x1771). "
        "Calls count_available_effect_zones(player_side, zone_id, -1); "
        "if count > 0 returns 1 (slot available); "
        "else falls back to check_card_special_summon_eligible_full (FUN_0805bcf0). "
        "r0=ptr card_slot_ptr. Returns u32: 1=summon eligible, 0=not. "
        "Constants: field6_vals=0x16/0x17, zone_ids=0x17d4/0x17c6/0x1771, quota=-1. "
        "Callers: FUN_080b499c, FUN_080baed0 (duel_field activation eval chain)."),
    # --- campaign-45 batch #45 ---
    ("FUN_0808ec08", "scan_field_slots_for_graveyard_equip_activation",
        "Called by FUN_08090218 (duel_field main control) as one step in equip-chain activation scanner sequence. "
        "Iterates 2 players x 10 slots (player 0..1, slot 0..9), reads card_id (bits[12:0]) from each slot, "
        "compares with constant 0x1403 (Graveyard zone card ID); also checks [slot+0xc] chain pointer is non-zero. "
        "When conditions met, constructs OAM attr (flip/priority/coord fields) then calls "
        "apply_equip_activation_with_id_lookup to attempt equip effect activation. "
        "Sets flag and returns 1 if any slot activates, else 0. "
        "Side effect: injects activation record into equip chain. "
        "r0=void (entry movs r0,#0 confirms no APCS input). "
        "Returns u32 found_flag (0=no activation, 1=at least one triggered). "
        "Constants: base=gP1LifePoints+0x1ce8, card_id=0x1403 (Graveyard zone). "
        "Callers: FUN_08090218."),
    ("FUN_080486e4", "enqueue_equip_zone_sprite_by_side",
        "Called by 17 callers (indeg=17) including duel_field-tagged functions. "
        "Selects OAM attr base by player_id (r0): 0x2f for r0==0 (P1, no flip), "
        "0x802f for r0!=0 (P2, H-flip bit set). "
        "Truncates slot_idx (r1) to u16, then calls enqueue_sprite_attr_record to write "
        "one equip-zone sprite record to sprite attribute buffer. "
        "Pure side-effect function, no return value. "
        "r0=u8 player_id [0..1], r1=u16 slot_idx [0..9]. Returns void. "
        "Constants: OAM_P1=0x2f, OAM_P2=0x802f (bit15=H-flip). "
        "Callers: FUN_080440b8, FUN_08044618, FUN_080576b0, FUN_08084738, FUN_0808f608."),
    ("FUN_08049e44", "enqueue_equip_slot_sprite_with_card_check",
        "Called by 3 duel_field callers (FUN_0804a2c8, FUN_0804a2e4, FUN_0804a30c). "
        "Receives equip zone slot ref ptr (r3), extracts card_id bits[12:0], "
        "calls count_field_copies_of_card to check same-name count on field; "
        "sets field_copy_flag if >0. Then calls check_card_field8_is_9 (r0=card_id). "
        "Combines both check results to build OAM attr fields (palette/flip/coord), "
        "calls enqueue_sprite_attr_record to write to sprite buffer. "
        "Conditionally calls scan_field_slots_for_equip_sprite for further slot scan. "
        "r0=u8 player_id [0..1], r1=u8 slot_col [0..9], r2=u16 card_id [0..0x1fff], "
        "r3=ptr slot_entry. Returns u32 oam_attr_or_zero (0=not written). "
        "Prologue: .hword 0x4680=mov r8,r0, .hword 0x4689=mov r9,r1 (callee-save). "
        "Callers: FUN_0804a2c8, FUN_0804a2e4, FUN_0804a30c."),
    ("FUN_0804a2c8", "submit_equip_slot_sprite_zone11",
        "Called by 6 callers (indeg=6) including duel_field. "
        "Thin wrapper for enqueue_equip_slot_sprite_with_card_check (FUN_08049e44): "
        "hard-codes r1=0xb (zone 11, special equip zone slot index), "
        "passes through caller r0(player_id), r2(slot_col), r3(zone_ptr), plus stack 5th arg. "
        "Returns void; callee return value discarded by epilogue pop+bx. "
        "r0=u8 player_id [0..1], r1=u16 slot_col (overwritten to 0xb internally), "
        "r2=u16 card_id [0..0x1fff], r3=ptr zone_ptr. "
        "Constants: zone11_idx=0xb. "
        "Callers: FUN_08067c0c, FUN_08068990, FUN_08069260, FUN_0807b0c8, FUN_0808f608."),
    ("FUN_0808f608", "scan_chain_nodes_for_equip_zone_sprite",
        "Called by FUN_08090218 (duel_field main control) as one phase in equip-chain activation scan. "
        "Iterates 2 players x 11 slots (player=r9, slot 0..10), "
        "calls check_node_in_slot_chain(card_id=0x123b, zone=0xb, type=2) for each slot. "
        "If node found, reads [slot_entry+0xa] availability; if valid, calls "
        "find_slot_idx_by_card_id_in_player_zones to locate equip target slot. "
        "When target valid: calls enqueue_equip_zone_sprite_by_side (FUN_080486e4) for flip sprite, "
        "then submit_equip_slot_sprite_zone11 (FUN_0804a2c8) for equip-zone sprite. "
        "Finally calls enqueue_sprite_attr_for_chain_node_match for match-marker sprite. "
        "r0=void (entry movs r0,#0 / mov r9,r0 confirms no APCS input). "
        "Returns u32 activation_flag (0=none, non-zero=at least one node matched). "
        "Constants: card_id=0x123b, zone=0xb, type=2, base=0x0201c5ec. "
        "Callers: FUN_08090218."),
    ("FUN_08043274", "enqueue_equip_chain_sprite_by_side",
        "Called by FUN_0804348c (equip-chain list scanner). Leaf function writing equip-chain sprite attr. "
        "Receives player_id (r0), row_byte (r1 via stack r[0x10]), col_byte (r3), plus two extra bytes r1/r2. "
        "Selects OAM base attr by player: 0x38 for P1 (no flip), 0x8038 for P2 (H-flip). "
        "Merges row/col bytes (lsls+orrs) then truncates to u16; combines with OAM base and slot_col, "
        "calls enqueue_sprite_attr_record to write to sprite attribute buffer. "
        "r0=u8 player_id [0..1], r1=u8 row_byte, r2=u8 col_byte, r3=u16 slot_col [0..9], "
        "[sp+0x10]=u16 extra_slot [0..9]. Returns void. "
        "Constants: OAM_P1=0x38, OAM_P2=0x8038 (bit15=H-flip). "
        "Callers: FUN_0804348c."),
    ("FUN_0804348c", "scan_equip_chain_list_for_sprite_update",
        "Called by FUN_08090218 (duel_field main control); key scanner for equip-chain sprite update. "
        "Traverses equip-chain linked list (base 0x0201d9c0), reads [node+0x6] as next-node ID. "
        "Extracts low 4 bits of [node+0x2] for card type: 0xa (equip) or 0x6 (spell) enters sprite path. "
        "Reads target slot card_id, locates in gDuelFieldSlots (0x0201c510); "
        "checks slot has valid card and activation flag ([slot+0x10] bit5) is clear. "
        "If conditions met: calls check_slot_zone_bit_eligible / get_card_extended_stat_field7 for extra validation, "
        "then calls enqueue_equip_chain_sprite_by_side (FUN_08043274) to write sprite. "
        "Terminates when [node+0x6]==0. "
        "r0=u8 player_id [0..1], r1=u8 slot_idx [0..10]. Returns void. "
        "Prologue: .hword 0x4682=mov r10,r0, .hword 0x4689=mov r9,r1. "
        "Constants: chain_list=0x0201d9c0, gDuelFieldSlots=0x0201c510, type_equip=0xa, type_spell=0x6. "
        "Callers: FUN_08090218."),
    ("FUN_080325dc", "check_card_equip_eligibility_in_field",
        "Called by 6 callers (indeg=6) including duel_field and FUN_08032960. "
        "Receives slot_entry ptr (r0), performs multi-layer equip eligibility check: "
        "(1) check_card_field8_is_normal; (2) reads [slot+0x34] for existing equip bind; "
        "(3) count_field_copies_of_card(card_id=0x166c) checks same-name field limit; "
        "(4) if [slot+0x8] non-zero, check_value_in_slot_chain(card_id=0x12bf, zone=0xb); "
        "(5) get_card_field_summon_restriction; if type==1 checks 0x148e and 0x14da copies; "
        "(6) check_card_targeted_by_spell_zone_effect. Returns 1 if all pass, 0 on any failure. "
        "r0=ptr slot_entry ([+0x10]=field8, [+0x34]=equip_bind, [+0x8]=chain_flag). "
        "Returns u32 eligible (0=not equippable, 1=equippable). No write side effects. "
        "Constants: card_ids=0x166c/0x12bf/0x148e/0x14da, zone=0xb. "
        "Callers: FUN_08032960, FUN_08048020, FUN_08048364, FUN_08099aac, FUN_08099e0c."),
    ("FUN_08032960", "count_equip_eligible_slots_for_player",
        "Called by FUN_08032a6c (both-players wrapper) and FUN_080490b4 (duel_field). "
        "Receives card_id (r1; saved to r8 via .hword 0x4688=mov r8,r1) and player_id (r0 low bit). "
        "Scans 5 monster-zone slots for given player (gDuelFieldSlots + player*0x868 + 0x10a4 + slot*0x14, slot 0..4). "
        "For each slot: extracts card_id bits[12:0] and compares with r8; "
        "checks [slot+0x10] active flags (bit5, bit1); computes bitmask (1<<(player*16+slot)). "
        "Calls check_card_equip_eligibility_in_field (FUN_080325dc) for qualifying slots. "
        "Returns count of eligible slots. Pure query, no write side effects. "
        "r0=u8 player_id [0..1], r1=u16 card_id [0..0x1fff]. Returns u32 eligible_slot_count. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14, zone_offset=0x10a4. "
        "Callers: FUN_08032a6c, FUN_080490b4."),
    ("FUN_08032a6c", "count_equip_eligible_slots_both_players",
        "Called by FUN_0808db90 (duel_field). "
        "Calls count_equip_eligible_slots_for_player (FUN_08032960) twice: "
        "first with r0=0 (P1), then with r0=1 (P2). "
        "Accumulates both results and returns total eligible slot count across both players. "
        "r0 (slot_ref ptr) passed as r1 to both callee invocations. "
        "Pure aggregate wrapper, no write side effects. "
        "r0=ptr slot_ref (passed as r1 to count_equip_eligible_slots_for_player). "
        "Returns u32 total_eligible_slot_count (P1+P2 sum). "
        "Callers: FUN_0808db90."),
    ("FUN_080454c0", "enqueue_effect_zone_pair_sprite_scan",
        "Called by FUN_08064760 (duel_field) and FUN_0808db90 (duel_field). "
        "Receives slot_id (r0), writes base sprite via enqueue_sprite_attr_record(mode=0x14, side=slot_id&0xffff, type=1, extra=0). "
        "Loads global field-state ptr (DAT_08045524), calls check_card_matches_active_effect_slot "
        "and check_card_pair_allowed to check pairing eligibility. "
        "If pair valid: iterates inner loop over candidate slots, "
        "writing pair sprites via enqueue_sprite_attr_record / enqueue_sprite_attr_with_mode. "
        "r0=u16 slot_id [0..0xffff]. Returns void. "
        "Constants: sprite_type=0x14, state_ptr=DAT_08045524. "
        "Callers: FUN_08064760, FUN_0808db90."),
    ("FUN_0808db90", "dispatch_equip_pair_sprites_by_state",
        "Called by FUN_08090218 (duel_field main control); combines equip-pair state check and sprite refresh. "
        "Scans 2 players (base 0x0201c5d8, stride 0x868), for each slot: "
        "reads card_id (bits[12:0]), checks [slot+0x8] availability, [slot+0x10] bit1 equip-bind flag. "
        "If slot has card and is unbound: calls count_equip_eligible_slots_both_players (FUN_08032a6c); "
        "if >0 records to r12. After loop: if r8==0 (no target), calls classify_card_effect_category; "
        "if category differs from [gP1LifePoints+0x10d8], calls enqueue_effect_zone_pair_sprite_scan (FUN_080454c0). "
        "r0=void (entry movs r0,#0 / mov r8,r0 confirms no APCS input). "
        "Returns u32 stage_done (0=continue, 1=stage complete). "
        "Constants: slot_base=0x0201c5d8, player_stride=0x868, state_addr=gP1LifePoints+0x10d8. "
        "Callers: FUN_08090218."),
    ("FUN_0808ee80", "enqueue_active_card_shape_sprites_in_zone",
        "Called by FUN_08049014 (duel_field) as last step in effect-zone sprite combined submission. "
        "Receives player_side (r0), iterates slots 0..4 (counter r4=0..4). "
        "For each slot calls test_slot_has_active_card(card_id=0x144d, player=r0, slot=r4). "
        "If active card found: calls enqueue_sprite_attr_with_shape(player=r0, slot=r4, mode=1) "
        "to write shape sprite to attribute buffer. Pure side-effect function, no return value. "
        "r0=u8 player_side [0..1]. Returns void. "
        "Constants: card_id=0x144d, slot_range=0..4, shape_mode=1. "
        "Callers: FUN_08049014."),
    ("FUN_08049014", "submit_effect_zone_lp_and_shape_sprites",
        "Called by 13 callers (indeg=13) including duel_field. "
        "Receives player_side (r7=r0) and effect_count (r4=r1). "
        "Returns immediately if effect_count==0. "
        "Computes opponent_side=1-player_side (r6), calls count_available_effect_zones(opponent_side, slot_id=0x1256, -1). "
        "If zones available: calls enqueue_sprite_attr_by_sign(opponent_side, r8 sign_value) for sign sprite, "
        "then submit_lp_change_indicator_with_chain_check(player_side, effect_count, 1, r12) for LP indicator. "
        "Otherwise: caps effect_count, selects OAM attr by player (0x24 P1 / 0x8024 P2), "
        "calls enqueue_sprite_attr_record for base sprite, submit_lp_bar_sprite_row_by_type(type=0x11), "
        "and enqueue_active_card_shape_sprites_in_zone (FUN_0808ee80). "
        "r0=u8 player_side [0..1], r1=u16 effect_count [0..0xffff]. Returns void. "
        "Prologue: .hword 0x464f=mov r7,r0; no non-APCS high-reg inputs. "
        "Constants: OAM_P1=0x24, OAM_P2=0x8024, slot_id=0x1256, lp_row_type=0x11. "
        "Callers: FUN_080655ec, FUN_08067160, FUN_0806a884, FUN_0806b31c, FUN_0806b56c (+ 8 more)."),
    ("FUN_0808ed98", "scan_field_slots_for_card_pair_sprite_update",
        "Called by FUN_08090218 (duel_field main control); large field sprite scanner. "
        "Iterates 2 players x 10 slots (player 0..1, slot 0..9), base gP1LifePoints+0xffffe358. "
        "For each slot: reads word[0], extracts bits[19:0] and compares with constant 0x28a0 (card_id/type check), "
        "checks [slot+0xc] chain pointer. If conditions met: "
        "calls enqueue_sprite_attr_with_xy_split for XY-split sprite; "
        "checks [slot+0x8] bit5/bit1 inverted logic combination; "
        "if inner condition met: calls enqueue_sprite_attr_for_zone_card_id_lookup, "
        "then submit_effect_zone_lp_and_shape_sprites (FUN_08049014). "
        "r0=void (entry movs r0,#0; str r0,[sp,#0]; movs r1,#1; mov r10,r1 confirms no APCS input). "
        "Returns u32 found_flag (0=not triggered, 1=at least one slot matched). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, cmp_val=0x28a0. "
        "Callers: FUN_08090218."),
    ("FUN_0808f57c", "scan_equip_chain_slots_for_bitmap_update",
        "Called by FUN_08090218 (duel_field main control); equip-chain bitmap sprite update scanner. "
        "Iterates 2 players (r6=0..1) x 5 slots (r5=0..4), base 0x0201e1c8. "
        "For each (player, slot): calls test_slot_has_active_card(card_id=0x14fc, player=r4=player_xor_6, slot=r5). "
        "If active card found: calls find_equip_chain_pair_across_field(player, slot) to find cross-field pair. "
        "If valid pair returned (!=0xffff): extracts player-side/slot-index from result, "
        "calls enqueue_equip_slot_bitmap_update to write equip-slot bitmap sprite. "
        "r0=void (entry movs r6,#0 / ldr r7,DAT confirms no APCS input). "
        "Returns u32 found_flag (0=no pair, 1=at least one pair updated). "
        "Constants: card_id=0x14fc, state_base=0x0201e1c8, slot_range=0..4, no_pair=0xffff. "
        "Callers: FUN_08090218."),
    ("FUN_0809011c", "scan_slots_for_equip_activation_by_field5",
        "Called by FUN_08090218 (duel_field main control) as one phase of equip activation scanner chain. "
        "Entry saves r0 to r9 (.hword 0x4681=mov r9,r0 -- card_id or global ptr). "
        "Calls check_card_field5_is_nonzero(r9): if non-zero scans monster zone (slot 0..4); "
        "else scans trap zone (slot 5..9). "
        "For each (player 0..1, slot): reads slot card_id (bits[12:0]), compares with r9; "
        "checks [slot+0x8] availability; checks [slot+0x10] bit4 (equip-activation bit). "
        "If conditions met: constructs OAM attr, calls apply_equip_activation_with_id_lookup; "
        "on success calls set_field_slot_bit_with_sprite_update. "
        "r0=u16 card_id [0..0xffff] (saved to r9; callsite 0x08090470 loads 0x1762). "
        "Returns u32 activation_done (0=no activation, 1=activated). "
        "Constants: gDuelFieldSlots=0x0201c510 (DAT_0809020c), player_stride=0x868, bit4=equip_activation_bit. "
        "Callers: FUN_08090218."),
    ("FUN_08043d20", "enqueue_equip_chain_pair_sprite_validated",
        "Called by FUN_08043ea4 and FUN_08043f44 (both duel_field). "
        "Receives encoded params: r0=src (bits[7:0]=src_player [0..1], bits[15:8]=src_slot [0..9]), "
        "r1=dst (bits[7:0]=dst_player [0..1], bits[15:8]=dst_slot [0..9]). "
        "If src_slot==dst_slot: returns immediately (self-reference invalid). "
        "Locates src slot in gDuelFieldSlots (0x0201c510, player*0x868+slot*0x14); "
        "checks [slot+0x8] valid flag (ldrh!=0). "
        "Reads slot[0] bits[12:0] for card_id, compares with 0xa5600000>>19 (=0x12ab type mask). "
        "If match: calls find_equip_chain_pair_across_field; "
        "if pair found (!=0xffff): extracts player/slot fields, "
        "calls enqueue_equip_chain_slot_sprite_attr to write equip-chain slot sprite. Returns void. "
        "r0=u16 src_encoded, r1=u16 dst_encoded. "
        "Constants: gDuelFieldSlots=0x0201c510, card_type_mask=0xa5600000 (0x12ab after shift), no_pair=0xffff. "
        "Callers: FUN_08043ea4, FUN_08043f44."),
    ("FUN_08045298", "enqueue_equip_set_slot_sprite_by_zone_col",
        "Called by 8 callers (indeg=8) including duel_field. "
        "Receives player_id (r0), slot_idx (r1), zone_col (r2). "
        "Locates slot in gDuelFieldSlots (0x0201c510), reads card_id (bits[12:0]). "
        "Calls check_card_id_is_equip_set_a: if not a set-A equip, returns. "
        "If zone_col==0: selects OAM base 0x3b (P1) / 0x803b (P2, H-flip), writes sprite directly. "
        "If zone_col!=0: calls get_equip_card_set_code_for_slot; if non-zero, writes sprite with same OAM base. "
        "Writes via enqueue_sprite_attr_record. Pure sprite-buffer side effect, no return value. "
        "r0=u8 player_id [0..1], r1=u8 slot_idx [0..9], r2=u8 zone_col [0..9]. Returns void. "
        "Constants: OAM_P1=0x3b, OAM_P2=0x803b (bit15=H-flip), gDuelFieldSlots=0x0201c510. "
        "Callers: FUN_080432bc, FUN_08043d90, FUN_0808dc48, FUN_0808dd5c, FUN_0808f2f0 (+ 3 more)."),
    ("FUN_08043d90", "scan_equip_chain_list_for_activation_sprite",
        "Called by FUN_08043ea4 and FUN_08043f44 (both duel_field); sibling of enqueue_equip_chain_pair_sprite_validated (FUN_08043d20). "
        "Receives r0=src_encoded (bits[7:0]=src_player [0..1], bits[15:8]=src_slot [0..9]), "
        "r1=dst_encoded (.hword 0x4688=mov r8,r1), "
        "r9=r0 (.hword 0x4681=mov r9,r0). "
        "If src_slot==r9: returns immediately. "
        "Locates src slot in gDuelFieldSlots; checks [slot+0x8] valid and [slot+0xa] chain node ID. "
        "If [slot+0xa]!=0: traverses equip-chain list at 0x0201d9c0; "
        "reads [node+0x2] low 4 bits for card_type; type 0xa enters sprite-write path. "
        "Reads target slot card_id, compares with 0x118a / 0x118a+0x3f (equip activation range). "
        "If match: calls enqueue_equip_set_slot_sprite_by_zone_col (FUN_08045298). "
        "Then enters activation path: locates another slot, reads card_id; "
        "if card_id==0x118a..0x11c9 and [slot+0xc]==0 (no bound chain): "
        "calls apply_equip_activation_with_id_lookup, on success calls enqueue_sprite_attr_with_xy_split. "
        "r0=u16 src_encoded, r1=u16 dst_encoded. Returns void. "
        "Constants: gDuelFieldSlots=0x0201c510, chain_list=0x0201d9c0, card_id_range=0x118a..0x11c9, type_equip=0xa. "
        "Callers: FUN_08043ea4, FUN_08043f44."),

    # --- batch #46 (campaign-46) ---
    ("FUN_08043ea4", "enqueue_equip_chain_pair_sprite_if_eligible",
        "Check activation bit (bit12) of two equip slots (r0=player_a/r1=slot_a, r2=player_b/r3=slot_b); "
        "if both active, call enqueue_equip_chain_pair_sprite_validated to enqueue dual-slot sprite, "
        "write sprite attr to OAM buffer via enqueue_sprite_attr_record, "
        "then scan activation chain via scan_equip_chain_list_for_activation_sprite. "
        "Entry unpacks u8 player_id and u8 slot_idx via lsls/lsrs. Returns void. "
        "Params: r0=u8 player_id_a [0..1], r1=u8 slot_idx_a [0..4], r2=u8 player_id_b [0..1], r3=u8 slot_idx_b [0..4]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14."),
    ("FUN_08036014", "check_slot_equip_eligibility_by_type",
        "Comprehensive equip eligibility check for a field slot (r0=player_id, r1=slot_idx, r2=flag). "
        "Calls check_slot_card_effect_eligibility then count_zones_by_card_and_mode; "
        "dispatches to different eligibility paths based on card type field attr[0xc..0xf] (type=1/5/6/0xa etc). "
        "Returns 1 if slot can legally equip, 0 otherwise. Shared by 7 duel_field callers. "
        "Params: r0=u8 player_id [0..1], r1=u8 slot_idx [0..4], r2=u8 flag [0..1]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_0804c140", "check_card_id_is_field_zone_special",
        "Leaf function. Checks if card_id (r0) matches one of three special field zone cards: "
        "0x170a, 0x1652 (=0x170a-0xb8), or 0x17d2. Returns 1 if match, 0 otherwise. "
        "Called by check_slot_field_zone_card_eligible to filter special zone cards before equip check. "
        "Params: r0=u16 card_id [0..0x1fff]. "
        "Constants: CARD_ID_FIELD_ZONE_A=0x170a, CARD_ID_FIELD_ZONE_B=0x1652, CARD_ID_FIELD_ZONE_C=0x17d2."),
    ("FUN_08032f00", "count_eligible_zone_slots_for_player",
        "Iterates 5 field slots (slot 0..4, stride 0x14) for given player side (r0=player_id, r2=zone_flag). "
        "For each slot checks: (1) bit12 activation flag nonzero; (2) [slot+0x8] nonzero (valid card); "
        "(3) check_slot_zone_bit_eligible passes. Increments counter if all three pass. "
        "Returns count of eligible slots [0..5]. Called by count_eligible_zone_slots_all_flags with r2=-1. "
        "Params: r0=u8 player_id [0..1], r2=i32 zone_flag (zone bit mask, -1=all). "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14."),
    ("FUN_08032f6c", "count_eligible_zone_slots_all_flags",
        "Thin wrapper around count_eligible_zone_slots_for_player. "
        "Sets r2=-1 (movs r2,#1; rsbs r2,r2,#0 = all-flags) then tail-calls FUN_08032f00. "
        "Counts all eligible zone slots for given player side with all zone bits selected. "
        "Params: r0=u8 player_id [0..1]. Returns r0=u8 count [0..5]. "
        "Constants: ZONE_FLAG_ALL=-1."),
    ("FUN_080363bc", "check_slot_field_zone_card_eligible",
        "Comprehensive field zone card eligibility check for slot (r0=player_id, r1=slot_idx). "
        "Reads slot at 0x0201c510+player*0x868+slot*0x14, checks bit12 activation and [slot+0x10] limit bits (bit5/bit1). "
        "Calls check_card_id_is_field_zone_special to filter special zone cards; "
        "then compares card_id against 0x1826/0x17e4/0x1860 etc. "
        "If conditions met, calls count_eligible_zone_slots_all_flags to verify opposite side has eligible slots. "
        "Returns 1 (eligible) or 0 (ineligible). "
        "Params: r0=u8 player_id [0..1], r1=u8 slot_idx [0..4]. "
        "Constants: CARD_ID_FIELD_A=0x1826, CARD_ID_FIELD_B=0x17e4, CARD_ID_FIELD_C=0x1860, gDuelFieldSlots=0x0201c510."),
    ("FUN_08042b24", "resolve_equip_target_slot_for_enqueue",
        "Equip activation target slot resolution and enqueue. Entry r0=player_id, r1=slot_idx. "
        "Calls check_slot_field_zone_card_eligible; checks bit12 activation; "
        "calls check_slot_equip_eligibility_by_type to find target slot; "
        "calls check_slot_card_is_equip_whitelist. Whitelist path uses find_first_available_monster_slot_for_player; "
        "non-whitelist path uses get_first_placeable_monster_slot. "
        "If valid target (r6!=-1): calls enqueue_equip_slot_bitmap_update (r2=1). "
        "If cross-side slot (r7!=r4): packs player/slot and calls enqueue_equip_chain_pair_sprite_if_eligible. "
        "Returns 1=processed, 0=not processed. "
        "Params: r0=u8 player_id [0..1], r1=u8 slot_idx [0..4]."),
    ("FUN_08047e20", "prepare_equip_slot_ctx_for_bitmap_update",
        "Equip target context init and bitmap update. Entry r0=player_id, r1=slot_idx, r2=extra_flag, r3=flags. "
        "Allocates 0x18-byte stack workspace, clears via memset; writes r3 (halfword) to [sp+0x0]; "
        "reads [r2+0x2] byte, applies bit1 mask, writes back; "
        "computes slot bitmap (1<<(player*0x10+slot_idx)); "
        "calls update_equip_target_bitmap_for_field (zone_flags=0xe, side_flags=0). "
        "Returns 1 if slot bit set in bitmap, 0 otherwise. "
        "Params: r0=u8 player_id [0..1], r1=u8 slot_idx [0..9], r2=u8 extra_flag [0..1], r3=u16 flags. "
        "Constants: MEMSET_SIZE=0x18, ZONE_FLAGS=0xe, SIDE_FLAGS=0x0, BIT1_MASK=0x2."),
    ("FUN_080478fc", "query_equip_target_bitmap_default",
        "Minimal leaf wrapper (5 instructions). Calls update_equip_target_bitmap_for_field with fixed params "
        "r2=0xe (zone_flags) and r3=2 (side_flags=both sides). "
        "Passes through r0=player_id, r1=slot_mask to callee. "
        "indeg=29, highest-frequency equip target bitmap query entry in field code. "
        "Params: r0=u32 player_id, r1=u32 slot_mask. "
        "Constants: ZONE_FLAGS=0xe, SIDE_FLAGS=0x2."),
    ("FUN_08047970", "test_equip_target_slot_in_bitmap",
        "Combines r1=player_id and r2=slot_idx into slot bitmap mask (1<<(r1*0x10+r2)), "
        "then calls query_equip_target_bitmap_default (FUN_080478fc). "
        "Returns 1 if bitmap AND slot_mask nonzero (slot is valid equip target), 0 otherwise. "
        "indeg=19, standard entry for equip feasibility test throughout field code. "
        "Params: r0=u32 bitmap_ctx, r1=u8 player_id [0..1], r2=u8 slot_idx [0..9]."),
    ("FUN_08047f1c", "update_equip_bitmap_with_cross_side_flag",
        "Equip target bitmap update with cross-side flag injection. "
        "Entry r0=bitmap_ctx, r1=player_id_a, r2=slot_idx, r3=zone_flags, [sp+0x10]=side_flags. "
        "Computes slot_mask=1<<(r1*0x10+r2); detects cross-side (r4 XOR r1 nonzero) via eors/rsbs/orrs/asrs pattern; "
        "if cross-side, ORs 0x20000 (bit17) into zone_flags; then calls update_equip_target_bitmap_for_field. "
        "Returns 1 if bitmap hit, 0 otherwise. "
        "Params: r0=u32 bitmap_ctx, r1=u8 player_id_a [0..1], r2=u8 slot_idx [0..9], r3=u32 zone_flags, [sp+0x10]=u32 side_flags. "
        "Constants: CROSS_SIDE_FLAG=0x20000."),
    ("FUN_0808efa8", "scan_field_for_whitelist_equip_sprite_and_lp",
        "Iterates 2 sides x 5 slots. For each active slot calls check_slot_card_is_equip_whitelist; "
        "if pass, reads opposite-side same-slot equip chain data (bit5/bit1 limit checks); "
        "calls enqueue_sprite_attr_for_zone_card_id_lookup to enqueue zone sprite attr. "
        "When cross-side match found, calls submit_lp_change_indicator_with_chain_check per interval. "
        "Returns 1=found and processed at least one eligible slot, 0=none. "
        "Params: r0=void (entry movs r0,#0 overwrites). "
        "Constants: gDuelFieldBase=0x0201e1c8, player_stride=0x868."),
    ("FUN_0808f9f8", "scan_field_slots_for_equip_bitmap_update",
        "Iterates 2 sides (player 0..1) x monster zone slots (slot 5..9). "
        "For each slot calls test_slot_has_active_card (card_id=0x1624); "
        "if active and get_slot_effect_card_value returns 0 (no extra effect value), "
        "calls enqueue_equip_slot_bitmap_update to enqueue bitmap update. "
        "Returns 1=found and processed, 0=none. Single caller FUN_08090218 (duel_field master). "
        "Params: r0=void (entry movs r6,#0 overwrites). "
        "Constants: BASE_ADDR=0x0201e1c8, CARD_ID_FILTER=0x1624."),
    ("FUN_0808eeb0", "scan_field_slots_for_chain_sprite_enqueue",
        "Iterates 2 sides x 5 slots; checks each slot bit12 activation flag and [slot+0xc] field "
        "value against chain node constant 0xa2680000. For matching slots calls "
        "enqueue_sprite_attr_with_xy_split to enqueue split-XY sprite attr. "
        "Inner loop slot 0..4, outer loop player 0..1. Base addr 0x0201e1c8. "
        "Single caller FUN_08090218 (duel_field master). "
        "Params: r0=void (entry ldr r0,DAT overwrites). "
        "Constants: BASE_ADDR=0x0201e1c8, CHAIN_NODE_MAGIC=0xa2680000, PLAYER_STRIDE=0x868."),
    ("FUN_0808f230", "scan_field_for_equip_priority_slot_update",
        "Iterates 2 sides x 5 slots; calls test_slot_has_active_card (card_id=0x160f) per slot; "
        "among active slots compares [slot+0x4] values (priority/ATK), selects slot with smaller value; "
        "calls enqueue_equip_slot_bitmap_update to update equip bitmap. "
        "Returns 1=found and updated, 0=not processed. Single caller FUN_08090218. "
        "Params: r0=void (entry movs r0,#0 + mov r10,r0 overwrites). "
        "Constants: CARD_ID_TARGET=0x160f, BASE_ADDR=0x0201e1c8, PLAYER_STRIDE=0x868."),
    ("FUN_08037bb4", "check_field_effect_zone_activation_eligible",
        "Checks field effect zone activation eligibility for given player side (r0=player_id). "
        "Logic: (1) call count_available_effect_zones (card=0x137b) for opposite side - return 1 if nonzero; "
        "(2) call count_field_copies_of_card for own side - return 1 if nonzero; "
        "(3) call count_available_effect_zones (card=0x17e7) for opposite side; "
        "(4) if opposite player_id matches stored value at gP1LifePoints+0x1ce8, "
        "call count_field_copies_of_card (card=0x135e). Returns 1 if any condition met, 0 otherwise. "
        "Params: r0=u8 player_id [0..1]. "
        "Constants: CARD_ID_A=0x137b, CARD_ID_B=0x17e7, CARD_ID_C=0x135e, ZONE_FLAG_ALL=-1."),
    ("FUN_0808ffb4", "scan_field_slots_for_equip_sprite_by_chain",
        "Iterates 2 sides x 5 slots; for each active slot checks card_id=0x1817; "
        "calls count_slot_chain_nodes_by_card_id; if nonzero, checks bit5: "
        "bit5=0 calls enqueue_effect_card_slot_sprite_attr (with count param), "
        "then calls enqueue_equip_slot_sprite_attr (r3=1). "
        "Returns 1=processed at least one slot, 0=none. Single caller FUN_08090218. "
        "Params: r0=void (entry movs r0,#0 + mov r8,r0 overwrites). "
        "Constants: CARD_ID_TARGET=0x1817, BASE_ADDR=0x0201e1c8."),
    ("FUN_0808eb68", "find_first_eligible_zone_slot_for_player",
        "Iterates 5 field slots (slot 0..4, stride 0x14) for given player side (r0=player_id). "
        "Checks each slot: (1) bit12 activation flag; (2) [slot+0x8] nonzero (has card); "
        "(3) check_slot_zone_bit_eligible (r2=1). Returns 1 immediately on first match, 0 if none found. "
        "Called by scan_field_slots_for_zone_equip_bitmap_update and FUN_0809a1a4. "
        "Params: r0=u8 player_id [0..1]. "
        "Constants: PLAYER_STRIDE=0x868, BASE_ADDR=0x0201c510, ZONE_FLAG=1."),
    ("FUN_0808ebb8", "scan_field_slots_for_zone_equip_bitmap_update",
        "Iterates 2 sides x 5 slots; calls test_slot_has_active_card (card_id=0x13a4) to confirm active; "
        "if active, calls find_first_eligible_zone_slot_for_player to confirm that side has eligible zone slot; "
        "if eligible, calls enqueue_equip_slot_bitmap_update to enqueue equip bitmap update. "
        "Returns 1=processed, 0=none. Single caller FUN_08090218 (duel_field master). "
        "Params: r0=void (entry movs r6,#0 overwrites). "
        "Constants: CARD_ID_TARGET=0x13a4, BASE_ADDR=0x0201e1c8."),
    ("FUN_080439e0", "apply_slot_equip_activation_with_sprite",
        "Performs equip activation for a field slot (r0=player_id, r1=slot_idx, r2=extra, r3=side_flag) "
        "and updates sprite display. Reads slot card_id (bits[12:0]); checks slot_idx<=4 and activation flag; "
        "builds OAM attr word using bit masks (0xfffffdff/0xffffc3ff/0xffffbfff/0xffff7fff/"
        "0xfffffe00/0xfffeffff/0xfffdffff) to clear old fields then OR in new slot/player/flip bits; "
        "calls enqueue_sprite_attr_record to write OAM buffer. "
        "Based on side_flag calls set_field_slot_bit_with_sprite_update (r3=1); "
        "for specific card_ids (0x1005/0x1048/0x101e/0x1197/0x1868) calls apply_equip_activation_with_id_lookup; "
        "if LP change, calls submit_lp_bar_sprite_row_by_type. Returns 1=success, 0=not processed. "
        "Params: r0=u8 player_id [0..1], r1=u8 slot_idx [0..4], r2=u16 extra_field, r3=u8 side_flag [0..1]. "
        "Constants: OAM_CLEAR_BIT9=0xfffffdff, OAM_CLEAR_BITS14_15=0xffffc3ff, OAM_CLEAR_BIT14=0xffffbfff, "
        "OAM_CLEAR_BIT15=0xffff7fff, OAM_CLEAR_BITS0_8=0xfffffe00, OAM_CLEAR_BIT16=0xfffeffff, "
        "OAM_CLEAR_BIT17=0xfffdffff, CARD_ID_BRANCH_A=0x1005, CARD_ID_BRANCH_B=0x1048, "
        "CARD_ID_BRANCH_C=0x1197, CARD_ID_BRANCH_D=0x1868."),

    # --- batch #47 (campaign-47) 2026-05-14 ---
    ("FUN_080439a0", "invoke_equip_activation_with_zero_flag",
        "Wrapper: writes sp+0=0 then bl apply_slot_equip_activation_with_sprite. "
        "Equivalent to calling apply_slot_equip_activation_with_sprite with side_flag=0 "
        "without requiring caller to clear the stack param. "
        "Called by 5 duel_field callers (FUN_08043c18, FUN_0808df3c, FUN_0809b178, "
        "FUN_0809b7e0, FUN_0809eb54) in sprite refresh phase. "
        "Params: r0=u32 player_side [0..1], r1=u32 slot_idx [0..4], r2=u32 card_info. "
        "Returns r0 passthrough from apply_slot_equip_activation_with_sprite."),
    ("FUN_0808df3c", "scan_all_slots_for_max_equip_match",
        "Called by duel_field master FUN_08090218. "
        "Initializes sp+4 work array (10 words from DAT_0808e054=0x09e3f164). "
        "Double loop player [0..1] x slot [0..9]: reads [slot+0x10] bit5 (equip flag) "
        "and bit0 (position), ANDs with [slot+0x8] mask. On hit compares [slot+0x4] "
        "halfword (ATK/value) with stored max per player. Second nested scan repeats. "
        "Returns 0 if no hit (r7==0), else enters activation path (LAB_0808e068). "
        "Constants: DAT_0808e054=0x09e3f164 (init template), "
        "gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_0808daf0", "find_matching_slot_by_player_zone_card",
        "Called by scan_card_placement_for_activation (FUN_0808fc78) and FUN_0808fbd0. "
        "Searches gDuelFieldSlots (base=0x0201c510, stride=0x868) for a slot matching "
        "r0=player_id, r1=zone_type (bits[5:3]), r2=card_id (bits[14:8]). "
        "Inner loop slot 0..count: reads [slot+2] bit0=player, bits[5:3]=zone_type, "
        "[slot+4] bits[14:8]=card_id. On match enters second scan via 0x488-offset array. "
        "Returns r0=slot_idx (>=0) on hit, r0<0 on miss. Read-only; no external writes. "
        "Params: r0=u32 player_id [0..1], r1=u32 zone_type [0..5], r2=u32 card_id [0..0x1fff]."),
    ("FUN_080316b8", "find_card_pair_in_player_deck_list",
        "Called by 10 duel_field callers. "
        "Searches player deck list (gP1LifePoints+player*0x868+0x10) for a card "
        "that check_card_pair_allowed(entry_card_id, r1) returns nonzero for. "
        "Extracts card_id from [entry+0] bits[12:0] via lsls/lsrs #0x13. "
        "Returns first matching deck list index (>=0), or -1 if not found. "
        "Read-only; no external writes. "
        "Params: r0=u32 player_side [0..1], r1=u32 target_card_id [0..0x1fff]. "
        "Constants: gP1LifePoints base, player_stride=0x868, deck_list_offset=0x10."),
    ("FUN_0808fc78", "scan_card_placement_for_activation",
        "Called exclusively by duel_field master FUN_08090218. "
        "Initializes sp work area (4 words from DAT_0808fcdc=0x09e3f18c). "
        "Iterates 2 players; per slot checks byte[+0]==0x1b (card_type filter), "
        "bit15 of [slot+4] (activation flag), bits[14:8] sub-type to branch: "
        "0x17c7=type_A / 0x17c8=type_B, stores player_id in sp+0 or sp+4+bit*8. "
        "Then calls find_zone_slot_idx_allowed_for_card, find_card_pair_in_player_deck_list, "
        "find_slot_idx_in_dual_list_by_id, FUN_0808daf0, apply_equip_activation_with_id_lookup. "
        "Returns 1=activated at least once, 0=none. "
        "Constants: DAT_0808fcf4=0x17c7, DAT_0808fce0=0x0201b290 (gDuelPhaseFlags)."),
    ("FUN_0804a5a0", "enqueue_sprite_attr_for_card_slot",
        "Called by enqueue_sprite_by_field_copy_count (FUN_0808f7c0). "
        "Extracts low 16 bits of r0 as tile_idx (lsls/lsrs #0x10). "
        "Calls enqueue_sprite_attr_record with fixed attr0=0x58, attr1=tile_idx, attr2=0, shape=0. "
        "Used to enqueue sprite attr for a duel field card slot display. "
        "Params: r0=u16 card_slot_value (low 16 bits = sprite tile_idx [0..0xffff]). "
        "Returns void. "
        "Constants: OAM_ATTR0=0x58 (Y=88, square, normal mode, 4bpp)."),
    ("FUN_0808f7c0", "enqueue_sprite_by_field_copy_count",
        "Called exclusively by duel_field master FUN_08090218. "
        "Calls count_field_copies_of_card(card_id=0x1510): count>0 sets flag=1, else flag=0. "
        "Reads [gP1LifePoints+0x10d0] lsrs #2 ands #1 (bit2). "
        "If flag != stored bit2: calls enqueue_sprite_attr_for_card_slot to enqueue update. "
        "Returns 1=processed, 0=not queued. "
        "Constants: CARD_ID=0x1510, STATE_OFFSET=0x10d0."),
    ("FUN_0808fdc0", "scan_effect_zone_slots_for_equip_activation",
        "Called exclusively by duel_field master FUN_08090218. "
        "Double loop player [0..1] x slot [0..4]; base 0x0201c510+player*0x868+slot*0x14. "
        "Per slot: extracts bits[19:13] (7-bit card type field) and bit31 (activation flag). "
        "Filters card type 0x16da via cmp DAT_0808fe5c. On match: checks [slot+0x8] / [slot+0xc] nonzero. "
        "Constructs OAM attr (bits[22:19] + bit13), calls apply_equip_activation_with_id_lookup "
        "then enqueue_sprite_attr_with_xy_split. Accumulates hit count in r12. "
        "Returns 0=no hit, 1=at least one activation. "
        "Constants: EFFECT_ZONE_OFFSET=0x1ce8, player_stride=0x868, CARD_TYPE_FILTER=0x16da."),
    ("FUN_0808ff44", "scan_slots_for_field_bit4_sprite_update",
        "Called exclusively by duel_field master FUN_08090218. "
        "Double loop player [0..1] x slot [0..4]; reads slot word low 13 bits (card_type). "
        "Filters via mask DAT_0808ffb0=0xba200000 (lsls then cmp). "
        "On match calls set_field_slot_bit_with_sprite_update(player, slot, r2=4, r3=0) "
        "to set bit4 and trigger sprite refresh. Returns 0 always. "
        "Constants: gDuelFieldSlots=0x0201c510, EXTRA_TABLE=0x0201e1c8, CARD_TYPE_MASK=0xba200000."),
    ("FUN_0804a4cc", "check_zone_eligible_with_deck_flag",
        "Called by 8 duel_field callers in activation eligibility chains. "
        "If r1==0: calls check_field_effect_zone_activation_eligible(r0) -> r4; "
        "else r4=r1 directly. Then calls get_player_deck_flag_bit1(r0). "
        "If deck_flag==r4: no update (return). Else enqueues sprite attr record "
        "with attr0=0x51 (player 0) or 0x8051 (player 1), attr1=r4[15:0], attr2=0. "
        "Combines zone eligibility check with sprite update trigger. "
        "Params: r0=u32 player_side [0..1], r1=u32 secondary_check (0=use default, else compare direct). "
        "Constants: OAM_ATTR0_P0=0x51, OAM_ATTR0_P1=0x8051 (DAT_0804a500)."),
    ("FUN_0808f1cc", "scan_field_for_unpaired_equip_slot_update",
        "Called exclusively by duel_field master FUN_08090218. "
        "Double loop player [0..1] x slot [0..4]; base 0x0201e1c8. "
        "Per slot: test_slot_has_active_card(card_id=0x1914). If active: "
        "count_equipped_paired_slots_for_player(0) and (1) - both must be 0. "
        "If both zero: calls enqueue_equip_slot_bitmap_update, returns 1. "
        "Used to trigger equip priority slot refresh when both sides have no pairs. "
        "Returns 1=updated, 0=not processed. "
        "Constants: CARD_ID=0x1914, BASE_ADDR=0x0201e1c8, player_stride=0x1784 (for count call)."),
    ("FUN_0808fa4c", "scan_field_for_extra_deck_equip_slot_update",
        "Called exclusively by duel_field master FUN_08090218. "
        "Symmetric to scan_field_for_unpaired_equip_slot_update; double loop player x slot. "
        "Per active slot (card_id=0x1645): calls count_extra_deck_cards_by_id for 5 card IDs "
        "(0x0fb7/0x0fb8/0x0fb9/0x0fba/0x0fbb). If any count==0: "
        "calls enqueue_equip_slot_bitmap_update, returns 1. "
        "Triggers equip slot refresh when field has fusion material card but extra deck "
        "is missing at least one required material. "
        "Constants: CARD_ID_FIELD=0x1645, EXTRA_IDS=0x0fb7..0x0fbb, BASE_ADDR=0x0201e1c8."),
    ("FUN_0804345c", "enqueue_equip_chain_attrs_for_slot_range",
        "Called by scan_equip_chain_list_by_player_slot (FUN_080435c4) and FUN_0809bdfc. "
        "Unpacks r0=u8 player_a and r1=u8 player_b from bit-packed words. "
        "Double loop r5 [0..1] x r4 [0..4]: calls enqueue_equip_chain_slot_sprite_attr "
        "(r0=player_side, r1=slot_idx, r2=r7, r3=1) 10 times total (2 players x 5 slots). "
        "Returns void. "
        "Params: r0=u8 player_a [0..1], r1=u8 player_b [0..1]."),
    ("FUN_080435c4", "scan_equip_chain_list_by_player_slot",
        "Called exclusively by FUN_08042bd0 (duel_field). "
        "Locates slot in gDuelFieldSlots (0x0201c510, stride=0x868, entry_size=0x14). "
        "Reads [slot+0xa] halfword as equip chain head node ID. "
        "If head==0: if slot_idx<=4, calls enqueue_equip_chain_attrs_for_slot_range. "
        "Else traverses chain: reads [node+2] bits[3:0] card_type; "
        "if type in [0xa..0xd]: reads player/slot from [node+0]/[node+1], next_id from [node+6]; "
        "calls enqueue_equip_chain_slot_sprite_attr then enqueue_equip_slot_bitmap_update. "
        "Returns void. "
        "Params: r0=u32 player_side [0..1], r1=u32 slot_idx [0..9]. "
        "Constants: gDuelFieldSlots=0x0201c510, chain_table=0x0201d9c0, stride=0x868."),
    ("FUN_0804ff9a", "check_card_state_code_eq_11",
        "In dispatch branch of FUN_0804f6c4 (card state hub). "
        "Clears r0, compares r3 (card_state_code) with 0xb (11): "
        "if equal sets r0=1, jumps to shared tail LAB_0804fffe; else r0=0. "
        "Sibling of check_card_state_code_eq_3 (0x0804ffa4) and other state_code stubs. "
        "Params: r3=u32 card_state_code [0..0xffff]. Returns r0: 1 if state_code==0xb, else 0."),
    ("FUN_0804b09c", "check_card_id_in_special_set",
        "Boolean whitelist checker; leaf. "
        "Compares r0=card_id against 4 special IDs: 0x117b / 0x16b9 / 0x17df / 0x18be. "
        "Branch tree: if card_id>0x16b9 check 0x17df and 0x18be; else check 0x16b9/0x16b8 and 0x117b. "
        "Returns 1 if any match, 0 otherwise. "
        "Called by FUN_0804f6c4 (card state hub), FUN_08051cc4, FUN_08052aa8. "
        "Params: r0=u32 card_id [0..0x1fff]. "
        "Constants: CARD_SET={0x117b, 0x16b9 (Nekogal_1), 0x17df (Gemini_Elf), 0x18be (Elemental_Burst)}."),
    ("FUN_0804ffa4", "check_card_state_code_eq_3",
        "In dispatch branch of FUN_0804f6c4 (card state hub). "
        "Symmetric to check_card_state_code_eq_11 (0x0804ff9a); only comparison value differs. "
        "Clears r0, compares r3 (card_state_code) with 0x3: "
        "if equal sets r0=1, jumps to shared tail LAB_0804fffe; else r0=0. "
        "Params: r3=u32 card_state_code [0..0xffff]. Returns r0: 1 if state_code==0x3, else 0."),
    ("FUN_0804ffba", "check_slot_zone_bit3_eligible",
        "In dispatch branch of FUN_0804f6c4 (card state hub). "
        "Reads r4=player_side [0..1] and r7=slot_idx [0..9] from caller frame (non-APCS). "
        "Sets r2=3 (fixed zone_bit), calls check_slot_zone_bit_eligible, "
        "then jumps to shared tail LAB_0804fffe. "
        "Sibling of check_slot_zone_bit1_eligible (0x0804ffd2) and other bit-N variants. "
        "Params: r4=u32 player_side [0..1] (caller-set), r7=u32 slot_idx [0..9] (caller-set). "
        "Returns r0: result of check_slot_zone_bit_eligible."),
    ("FUN_08036450", "check_slot_equip_whitelist_with_monster_space",
        "indeg=14, D_shared_mid. Checks slot meets equip activation conditions. "
        "Steps: (1) compute slot addr in gDuelFieldSlots(0x0201c510, stride=0x868, entry=0x14); "
        "(2) [slot+0] high 13 bits nonzero (has card); (3) [slot+0x8] halfword nonzero; "
        "(4) check_slot_field_zone_card_eligible; (5) check_slot_card_is_equip_whitelist; "
        "(6) find_first_available_monster_slot_for_player (opposite side has space). "
        "Returns 1 if all pass, 0 otherwise. Read-only. "
        "Params: r0=u32 player_side [0..1], r1=u32 slot_idx [0..4]. "
        "Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868."),
    ("FUN_0804ffd2", "check_slot_zone_bit1_eligible",
        "In dispatch branch of FUN_0804f6c4 (card state hub). "
        "Symmetric to check_slot_zone_bit3_eligible (0x0804ffba); only zone_bit differs. "
        "Reads r4=player_side and r7=slot_idx from caller frame (non-APCS). "
        "Sets r2=1 (fixed zone_bit), calls check_slot_zone_bit_eligible, "
        "then jumps to shared tail LAB_0804fffe. "
        "Params: r4=u32 player_side [0..1] (caller-set), r7=u32 slot_idx [0..9] (caller-set). "
        "Returns r0: result of check_slot_zone_bit_eligible."),
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
