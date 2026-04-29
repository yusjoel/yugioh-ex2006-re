# -*- coding: utf-8 -*-
"""
label_modules.py  --  方法 3 / 命名提案的共享映射表

被以下脚本 import:
    merge_label_refs_to_proposals.py    label name → module
    propagate_label_tags.py             func name 前缀 → module
    rewrite_tags.py                     旧 tag 转新 tag
    (可选) merge_agbcc_fid_to_proposals.py
"""

import re

AUTO_NAME_RE = re.compile(r"^(FUN_|SUB_|thunk_FUN_)[0-9a-fA-F]{8}$")


def is_auto_name(name):
    return bool(AUTO_NAME_RE.match(name or ""))


# -----------------------------------------------------------------------------
# label name → (module_id, prefix)
# 用于把数据 label (如 card_stats_table) 映射到模块语义.
# 顺序敏感: 更具体的规则放前面 (从上到下扫描).
# -----------------------------------------------------------------------------
LABEL_PREFIX_RULES = [
    # 卡数据子模块
    (re.compile(r"^card_stats_table$"),                  "card_stats",  "card_stats"),
    (re.compile(r"^card_passcode"),                      "card_passcode", "card_passcode"),
    (re.compile(r"^card_image_index"),                   "card_image",  "card_image"),
    (re.compile(r"^card_image_palettes$"),               "card_image",  "card_image"),
    (re.compile(r"^card_image_tiles$"),                  "card_image",  "card_image"),
    (re.compile(r"^card_medium_frame"),                  "card_frame",  "card_frame"),
    (re.compile(r"^card_mini_frame"),                    "card_frame",  "card_frame"),
    (re.compile(r"^card_name(s)?(_pointer)?_table$"),    "card_name",   "card_name"),
    (re.compile(r"^card_desc(s)?(_pointer)?_table$"),    "card_desc",   "card_desc"),
    (re.compile(r"^cards_ids_array"),                    "card_ids",    "card_ids"),

    # 字体
    (re.compile(r"^font_jp_"),                           "font_jp",     "font_jp"),
    (re.compile(r"^font_ascii_"),                        "font_ascii",  "font_ascii"),

    # 文件系统
    (re.compile(r"^fs_"),                                "fs",          "fs"),
    (re.compile(r"^file_path_table$"),                   "fs",          "fs"),

    # 卡组 / banlist
    (re.compile(r"^banlist_"),                           "banlist",     "banlist"),
    (re.compile(r"^starter_deck$"),                      "deck",        "starter_deck"),
    (re.compile(r"^file_starter_deck_start$"),           "deck",        "starter_deck"),
    (re.compile(r"^struct_deck_table$"),                 "deck",        "struct_deck"),
    (re.compile(r"^deck_record_table$"),                 "deck",        "deck_record"),

    # 决斗谜题
    (re.compile(r"^duel_puzzle"),                        "duel_puzzle", "duel_puzzle"),

    # game-strings
    (re.compile(r"^game_str_pointer_table$"),            "game_str",    "game_str"),
    (re.compile(r"^game_str_(ja|en|de|fr|it|es)$"),      "game_str",    "game_str"),

    # HUD / Duel field
    (re.compile(r"^hud_"),                               "duel_field",  "hud"),
    (re.compile(r"^duel_field_"),                        "duel_field",  "duel_field"),
    (re.compile(r"^opponent_(top|bottom|palettes)"),     "duel_field",  "duel_field"),
    (re.compile(r"^icon_(tiles|palettes)_base$"),        "duel_field",  "icon"),

    # 卡包 (pack)
    (re.compile(r"^pack_banner"),                        "pack",        "pack_banner"),
    (re.compile(r"^pack_card_list"),                     "pack",        "pack_list"),
    (re.compile(r"^pack_(info|00|0[1-9]|[1-4][0-9])"),   "pack",        "pack"),

    # 玩家姓名输入页
    (re.compile(r"^name_input_state_table$"),            "name_input",  "name_input_page"),
    (re.compile(r"^name_input_"),                        "name_input",  "name_input"),

    # post-banlists / level signature
    (re.compile(r"^level_signature_table$"),             "level_sig",   "level_sig"),

    # ydc
    (re.compile(r"^ydc_limit"),                          "ydc",         "ydc_limit"),
    (re.compile(r"^ydc_theme"),                          "ydc",         "ydc_theme"),
    (re.compile(r"^ydc_all_data$"),                      "ydc",         "ydc"),

    (re.compile(r"^card_desc_pointer_table$"),           "card_desc",   "card_desc"),
    (re.compile(r"^opp(onent)?_card_value"),             "opp_card_value", "opp_card_value"),
]


# 这些 label 是 agbcc 编译器内置 assert 字符串元数据, 不属模块边界
ASSERT_LIKE_LABELS = set([
    "gl_bright_assert",
    "gl_common_c_filename",
    "nns_g2d_assert_anmID",
])


def derive_module_from_label(label):
    """label 名 → (module_id, prefix) 或 (None, None)."""
    if label in ASSERT_LIKE_LABELS:
        return (None, None)
    for pat, mod, prefix in LABEL_PREFIX_RULES:
        if pat.search(label):
            return (mod, prefix)
    return (None, None)


# -----------------------------------------------------------------------------
# 已 Ghidra 命名函数: 名字前缀 → module
# 用于 propagate 把已命名函数当作种子.
# 长前缀优先匹配; 没匹配的函数 (gl_*, cpu_*, bios_*, default 等) 不作种子.
# -----------------------------------------------------------------------------
FUNC_NAME_PREFIX_TO_MODULE = {
    # 直接由 label 派生的模块名复用
    "card_stats":       "card_stats",
    "card_passcode":    "card_passcode",
    "card_image":       "card_image",
    "card_frame":       "card_frame",
    "card_name":        "card_name",
    "card_desc":        "card_desc",
    "card_ids":         "card_ids",
    "card_data":        "card_data",        # 新: card_data_query
    "card_info":        "card_info",        # 新: card_info_page_*
    "card_list":        "card_list",        # 新: card_list_screen_init etc
    "decode_card_image":"card_image",       # decode_card_image_6bpp
    "render_card_desc": "card_desc",        # render_card_description_*
    "render_card_description": "card_desc",
    "internal_card_id": "card_ids",         # internal_card_id_to_card_id

    "font_jp":          "font_jp",
    "font_ascii":       "font_ascii",
    "select_charset":   "font_jp",
    "char_code":        "font_jp",
    "char_width":       "font_jp",
    "measure_string":   "font_jp",
    "get_char_width":   "font_jp",
    "blit_glyph":       "font_jp",
    "render_glyph":     "font_jp",
    "load_glyph":       "font_jp",
    "text_render":      "font_jp",
    "render_string":    "font_jp",
    "commit_line_buffer":"font_jp",

    "fs":               "fs",
    "banlist":          "banlist",
    "starter_deck":     "deck",
    "struct_deck":      "deck",
    "deck_record":      "deck",
    "duel_puzzle":      "duel_puzzle",
    "game_str":         "game_str",
    "hud":              "duel_field",
    "duel_field":       "duel_field",
    "icon":             "duel_field",

    "pack_banner":      "pack",
    "pack_list":        "pack",
    "pack_card_list":   "pack",
    "pack_detail":      "pack",
    "pack_entry":       "pack",
    "pack_name":        "pack",
    "pack_visible":     "pack",
    "pack_ui":          "pack",
    "pack":             "pack",

    "name_input_page":  "name_input",
    "name_input":       "name_input",

    "level_sig":        "level_sig",
    "ydc":              "ydc",
    "opp_card_value":   "opp_card_value",
}


def derive_module_from_func_name(name):
    """
    Ghidra 函数名 → module_id.
    优先匹配最长前缀. e.g.:
      'card_info_page_init_bg0' -> 'card_info'
      'pack_list_bg_setup' -> 'pack'
      'fs_load' -> 'fs'
      'gl_set_brightness' -> None
    """
    if not name:
        return None
    if AUTO_NAME_RE.match(name):
        return None
    sorted_prefixes = sorted(FUNC_NAME_PREFIX_TO_MODULE.keys(),
                             key=lambda p: -len(p))
    for prefix in sorted_prefixes:
        if name == prefix or name.startswith(prefix + "_"):
            return FUNC_NAME_PREFIX_TO_MODULE[prefix]
    return None


# -----------------------------------------------------------------------------
# module_id → 代表 prefix (用于扩散后 proposed_name = "<prefix>_<addr>")
# -----------------------------------------------------------------------------
MODULE_TO_PREFIX = {
    "card_stats":      "card_stats",
    "card_passcode":   "card_passcode",
    "card_image":      "card_image",
    "card_frame":      "card_frame",
    "card_name":       "card_name",
    "card_desc":       "card_desc",
    "card_ids":        "card_ids",
    "card_data":       "card_data",
    "card_info":       "card_info",
    "card_list":       "card_list",
    "font_jp":         "font_jp",
    "font_ascii":      "font_ascii",
    "fs":              "fs",
    "banlist":         "banlist",
    "deck":            "deck",
    "duel_puzzle":     "duel_puzzle",
    "game_str":        "game_str",
    "duel_field":      "duel_field",
    "pack":            "pack",
    "name_input":      "name_input",
    "level_sig":       "level_sig",
    "ydc":             "ydc",
    "opp_card_value":  "opp_card_value",

    # method 4 (路径字符串锚) 引入的新模块
    "demo":            "demo",        # demo/exodia/, demo/shuen/, demo/vija/ (召唤/胜利动画)
    "title_ex":        "title_ex",    # titleEx/ (title screen extension)
    "pass_input":      "pass_input",  # pass_input/ (banlist 密码输入页)
}


# -----------------------------------------------------------------------------
# 路径字符串一级目录 → module
# 用于方法 4: fs_load(path, ...) 调用点的字符串锚定 caller 模块
# -----------------------------------------------------------------------------
PATH_PREFIX_TO_MODULE = {
    "demo":        "demo",
    "titleEx":     "title_ex",
    "name_input":  "name_input",
    "pass_input":  "pass_input",
    "puzzle":      "duel_puzzle",
}


def derive_module_from_path(path):
    """'titleEx/bg3.LZ5bg' -> 'title_ex'."""
    if not path:
        return None
    if "/" in path:
        first = path.split("/", 1)[0]
        return PATH_PREFIX_TO_MODULE.get(first)
    return PATH_PREFIX_TO_MODULE.get(path)


# Tag 形式约定 (单 token, 无 key:value, 无括号):
#   模块直接命中  -> '<module>'              e.g. 'font_jp', 'card_stats'
#   模块扩散      -> 'via_<module>'          e.g. 'via_game_str'
#   IO family    -> 语义化 family 名         e.g. 'palette', 'vram', 'bg', 'sprite'
#   FID tramp    -> 'tramp_<func>'           e.g. 'tramp_calloc'
#
# 注: 旧 'io_pal;reg_PALRAM+0x0' 形式已废弃, IO 信息只保留 family 级语义 tag,
#     具体寄存器名 (reg_*) 全部丢弃 (信息冗余于 family, 可从 Ghidra 重导).

IO_FAMILY_RENAME = {
    "io_pal":     "palette",
    "io_vram":    "vram",
    "io_bg":      "bg",
    "io_win":     "window",
    "io_display": "display",
    "io_blend":   "blend",
    "io_dma":     "dma",
    "io_obj":     "sprite",
    "io_snd":     "sound",
    "io_timer":   "timer",
    "io_input":   "input",
    "io_sio":     "sio",
    "io_sys":     "sys",
    "io_io":      "io",  # PropagateIOTagsViaCallGraph 用 'io' 兜底
}

# 反查: 哪些是 IO family tag (新格式) — 用于 rewrite/propagate 跳过
IO_FAMILY_TAGS = set(IO_FAMILY_RENAME.values())

# 全部 module_id 集合 (用于 tag 解析时识别哪些 token 是模块名)
ALL_MODULES = set(MODULE_TO_PREFIX.keys())


# -----------------------------------------------------------------------------
# 场景大类划分 (用于 cluster_scenes_via_callgraph.py 阶段 1)
#
# SCENE_MODULES: "场景内部"模块, 函数有边界, 互相调用频繁.
#   作种子, 沿 callgraph 双向 BFS 扩散.
# UTILITY_MODULES: "通用工具"模块, 横切多个场景被广泛调用.
#   作 BFS 边界——遇到则停止, 不污染 scene 扩散.
# 二者互斥, 任意 module 必须分一类.
# -----------------------------------------------------------------------------
SCENE_MODULES = set([
    "demo",          # 战斗动画 (exodia/shuen/vija)
    "title_ex",      # 标题屏扩展
    "name_input",    # 玩家名字输入页
    "pass_input",    # banlist 密码输入页
    "pack",          # 卡包浏览/购买
    "pack_banner",   # (现已合并到 pack)
    "card_info",     # 卡牌详情页
    "card_list",     # 卡牌列表页
    "duel_puzzle",   # 决斗谜题
    "duel_field",    # 决斗场地 (HUD/外场)
])

UTILITY_MODULES = set([
    "font_jp", "font_ascii",     # 字体渲染
    "game_str",                   # i18n 字符串
    "fs",                         # 文件系统
    "banlist",                    # 禁卡表数据
    "card_stats",                 # 卡数据
    "card_image",                 # 卡图
    "card_frame",                 # 卡边框
    "card_name", "card_desc",     # 卡名/描述
    "card_ids", "card_data",      # 卡 ID 映射
    "card_passcode",              # 卡密码
    "level_sig",                  # Limited Duel 等级签名
    "ydc",                        # Yu-Gi-Oh Duel Console (限定/主题)
    "opp_card_value",             # 对手卡价值
    "deck",                       # starter/struct deck 数据
])

# Sanity: 二者无交集且并集 ⊆ ALL_MODULES
assert not (SCENE_MODULES & UTILITY_MODULES), \
    "SCENE/UTILITY overlap: %s" % (SCENE_MODULES & UTILITY_MODULES)
_uncategorized = ALL_MODULES - SCENE_MODULES - UTILITY_MODULES
if _uncategorized:
    # 不强制——某些 module (e.g. pack_banner) 已合并, 容许存在
    pass


# 已 Ghidra 命名但不属任何 module 的函数, 若名字以这些前缀开头则视为 utility
# (图层 helper / BIOS / CPU op / BG 寄存器解码 / 默认 stub)
HELPER_NAME_PREFIXES = (
    "gl_", "cpu_", "bios_",
    "bg0_", "bg1_", "bg2_", "bg3_",
    "default",
)


def is_helper_name(name):
    if not name or is_auto_name(name):
        return False
    for p in HELPER_NAME_PREFIXES:
        if name == p or name.startswith(p):
            return True
    return False
