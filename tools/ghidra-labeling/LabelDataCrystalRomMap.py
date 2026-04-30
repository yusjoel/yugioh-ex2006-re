# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# LabelDataCrystalRomMap.py  (Jython 2.7 / Ghidra script)
#
# 给 Data Crystal ROM map 揭示的几个数据区打标签：
#   - card_image_index        @ 0x095B5C00  (card_id 0..2098)
#   - cards_ids_array         @ 0x095B7CCC  (internal_card_id -> card_id, 3072 x u16)
#   - card_passcode_table     @ 0x095B94CC  (2098 × u32 加密密码表)
#   - card_names_table        @ 0x095BB594  (cards names base; 旧名 card_names_pool)
#   - card_descs_table        @ 0x095FFF0C  (2098 × 6 lang 描述文本池; 曾用名 card_desc_text_pool / card_effect_text_pool)
#   - card_desc_pointer_table @ 0x0980A508  (2098 × 6 × u32 offset 表; 曾用名 card_desc_data)
#   - card_stats_table        @ 0x098169B8  (5170 × 22 B, 首条 20B 少 zero0 字段)
#   - card_name_pointer_table @ 0x095F3A5C  (12612 x u32 = 2102 x 6 langs)
#   - card_effect_text_pool   @ 0x095FFF6C  (2014 cards x 6 langs description text)
#
# 同时给关联的 EWRAM/IWRAM 地址打标签（以便 Ghidra 反编译可读）：
#   - gSettings              @ 0x02006C2C
#   - gMoneyDp               @ 0x02006C38
#   - gPlayerName            @ 0x02006E48
#   - gP1LifePoints          @ 0x0201C4E0
#   - gP2LifePoints          @ 0x0201CD48
#   - gPlayerNameEntry       @ 0x02029512
#   - gBanlistPasswordBuffer @ 0x02029810
#   - gPrng                  @ 0x03000040
#   - gFrameCounter          @ 0x03000240
#
# 数据来源: refs/datacrystal-um2006/{rom-map,ram-map}.md

from ghidra.program.model.symbol import SourceType

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass

LABELS = [
    # ROM 数据区（GBA 视角地址 = ROM 偏移 + 0x08000000）
    (0x084C76C0, "card_image_palettes"),        # 2331 × 128 B, data/card-image-palettes.s
    (0x08510640, "card_image_tiles"),           # 2331 × 4800 B, data/card-image-tiles.s
    (0x08FBC080, "card_medium_frame_tile_data"), # 2331 × 1536 B, data/card-medium-frame.s
    (0x09326280, "card_mini_frame_tile_data"),  # data/card-mini-frame.s

    # card-mini-frame OBJ 调色板 (data/card-mini-frame-palette.s, ROM 0x1E31554..0x1E31714 = 0x1C0 B)
    # 由 card_list_screen_init (FUN_080fdef4 → FUN_081011c4) 4 次 memcpy 加载到 PALRAM:
    #   pal_128  → PALRAM 0x05000140 (BG colors 160-175) + 0x05000300 (OBJ 128-143)
    #   pal_144  → PALRAM 0x05000320 (OBJ colors 144-159)
    #   pal_main → PALRAM 0x05000200 (OBJ colors 0-127)
    # all.s 字面量池目前以裸 .word 0x09e31554 / 0x09e31594 形式引用 (3 处), 加 label 后符号化
    (0x09E31554, "card_mini_frame_pal_128"),   # 32 B (16 colors, OBJ 128-143)
    (0x09E31574, "card_mini_frame_pal_144"),   # 32 B (16 colors, OBJ 144-159; 0 ref)
    (0x09E31594, "card_mini_frame_pal_gap"),   # 128 B (其他 UI 调色板, 2 处 .word 引用)
    (0x09E31614, "card_mini_frame_pal_main"),  # 256 B (OBJ colors 0-127; 0 ref)

    # HUD 资源 + 决斗外场图块 (ROM 0x18xxxxx, 原拆分边界是静态分析推断的)
    # 加 label 后字面量池 .word 自动变 symbol; 未在 asm 源定义的 name 由 rom_data.inc 生成 .equ
    (0x09850B1C, "hud_life_points_font"),       # LP 数字字体 tile (0xAC0 B)
    (0x098515DC, "hud_phase_highlights_palette"),  # Phase Highlight OBJ palette (0x20 B; ROM 无指针 ref)
    (0x098515FC, "hud_gap_tiles"),              # HUD gap 4bpp tile sheet (0x400 B)
    (0x098519FC, "hud_phases_highlight"),       # Phases Highlight tile (0x3650 B; 末尾 28 B 实为指针表)
    (0x09855030, "duel_field_outer_tile_pointers"),  # 7 × u32 tile image 指针 (6 modes + 1 sentinel)
    (0x0985504C, "campaign_outer_image"),       # Campaign 外场 tile (0x9E0 B)
    (0x09855A2C, "link_outer_image"),           # Link Duel 外场 (0x5E0 B)
    (0x0985600C, "puzzle_outer_image"),         # Duel Puzzle 外场 (0x7E0 B)
    (0x098567EC, "limited_outer_image"),        # Limited Duel 外场 (0xDE0 B)
    (0x098575CC, "theme_outer_image"),          # Theme Duel 外场 (0x9E0 B)
    (0x09857FAC, "survival_outer_image"),       # Survival Mode 外场 (0x7E0 B)
    (0x0985878C, "duel_field_outer_extra_tiles"),    # ~95 tiles 4bpp (tile_pointers sentinel)

    # 外场 palette + 调色板指针表 (每 palette 0x40 B, 2×16色)
    (0x0985936C, "duel_field_outer_palette_pointers"),  # 7 × u32
    (0x09859388, "campaign_outer_palette"),
    (0x098593C8, "link_outer_palette"),
    (0x09859408, "puzzle_outer_palette"),
    (0x09859448, "limited_outer_palette"),
    (0x09859488, "theme_outer_palette"),
    (0x098594C8, "survival_outer_palette"),
    (0x09859508, "duel_field_extra_palette"),   # 2×16色 (palette_pointers sentinel)

    # LP/阶段 Tilemap + 指针表 (每 tilemap 0x4B0 B = 30×20)
    (0x09859548, "hud_phases_tilemap_pointers"),    # 7 × u32
    (0x09859564, "campaign_outer_lp_tilemap"),
    (0x09859A14, "link_outer_lp_tilemap"),
    (0x09859EC4, "puzzle_outer_lp_tilemap"),
    (0x0985A374, "limited_outer_lp_tilemap"),
    (0x0985A824, "theme_outer_lp_tilemap"),
    (0x0985ACD4, "survival_outer_lp_tilemap"),
    (0x0985B184, "hud_phases_map"),             # 0x4B0 B (lp_tilemap sentinel)

    # 外场 Tilemap + 指针表 (每 tilemap 0x4B0 B = 30×20)
    (0x0985B634, "duel_field_outer_tilemap_pointers"),  # 7 × u32
    (0x0985B650, "campaign_outer_tilemap"),
    (0x0985BB00, "link_outer_tilemap"),
    (0x0985BFB0, "puzzle_outer_tilemap"),
    (0x0985C460, "limited_outer_tilemap"),
    (0x0985C910, "theme_outer_tilemap"),
    (0x0985CDC0, "survival_outer_tilemap"),
    (0x0985D270, "duel_field_common_inner_tilemap"),  # 0x4B0 B (outer_tilemap sentinel)

    # 内场图块 (6 modes × 0x1680 B)
    # 代码只字面量池引用 campaign base; 其他 mode 由 base + idx * 0x1680 计算
    (0x0985D720, "campaign_inner_image"),
    (0x0985EDA0, "link_inner_image"),
    (0x09860420, "puzzle_inner_image"),
    (0x09861AA0, "limited_inner_image"),
    (0x09863120, "theme_inner_image"),
    (0x098647A0, "survival_inner_image"),
    (0x09865E20, "unused_inner_image"),  # 第 7 inner tile 变体,0 ref (未实装 mode 推测)
    (0x098674A0, "campaign_inner_palette"),  # 内场 palette base (6 modes × 0x20, base + mode * 0x20 访问)

    # 小图标 (131 个: 玩家 + 对手 + 其他, 暂用 icon_NNN 命名)
    (0x0988CF30, "icon_tiles_base"),     # 131 × 0x120 = 0x9360 B
    (0x09896290, "icon_palettes_base"),  # 131 × 0x20  = 0x1060 B (紧跟 tiles)

    # 对手图形 5-base 指针表（loader 字面量池 @ 0x0802D240..0x0802D250 引用）
    # palette copy 2 @ 0x09B4FE9C 是 copy 1 的冗余副本, 0 ref, 仅 asm/rom.s 文档 label
    (0x09B101AC, "opponent_palettes_base"),       # 7776 B = 27 × 288 (copy 1, 实际被 loader 引用)
    (0x09B1200C, "opponent_top_tiles_base"),      # 221184 B = 27 × 0x2000
    (0x09B4800C, "opponent_top_tilemap_base"),    # 32400 B = 27 × 0x4B0
    (0x09B51CFC, "opponent_bottom_tiles_base"),   # 221184 B = 27 × 0x2000
    (0x09B87CFC, "opponent_bottom_tilemap_base"), # 32400 B = 27 × 0x4B0

    # 日文双字节字库（4 个 charset 变体, 每个 1925 glyph, 8bpp 预解码每像素 1 字节）
    # 索引 = (hi & 0xF) << 7 | (lo & 0x7F) ∈ [0, 1925); narrow=主字形, wide=描边层
    # FUN_080F1884 用 (char_high_bit << 1) | ctx_flag_bit1 在 font_jp_charset_table 选 1 个
    # 验证: cid=1 青眼の白龍 XX 字节 F8F7/F48C/F1A9/FBD9/FE91 → glyph 1143/524/169/1497/1809
    (0x09BAC9A4, "font_jp_main_small"),     # 10×10 narrow main, 192500 B
    (0x09C2B7EC, "font_jp_main_large"),     # 12×12 narrow main, 277200 B
    (0x09BDB998, "font_jp_outline_small"),  # 12×12 wide outline, 277200 B (与 main_small 同 idx 配对)
    (0x09C6F2BC, "font_jp_outline_large"),  # 14×14 wide outline, 377300 B
    (0x09E5F864, "font_jp_charset_table"),  # 4 × (base, stride): (base[0..3], stride[0..3])
    # Shift_JIS code → glyph index 二分查找表（FUN_080F0188 在 code <= 0xEFFF 时使用）
    (0x09BA1524, "font_jp_sjis_lookup_table"),  # 1925 × u16 (sorted SJIS), 3850 B
    (0x09BA2430, "font_jp_sjis_lookup_count"),  # u16 = 1925
    (0x095B5C00, "card_image_index"),
    (0x095B7CCC, "cards_ids_array"),
    (0x095B94CC, "card_passcode_table"),  # 2098 × u32 加密密码表
    (0x095BB594, "card_names_table"),     # 曾用名 card_names_pool; data 源统一叫 _table
    (0x095F3A5C, "card_name_pointer_table"),
    (0x095FFF0C, "card_descs_table"),        # 曾用名 card_desc_text_pool / card_effect_text_pool@0x095FFF6C(错)
    (0x0980A508, "card_desc_pointer_table"), # 2098 × 6 × u32 per-cid offset 表; 曾用名 card_desc_data
    (0x098169B8, "card_stats_table"),      # 5170 × 22 B (首条 20B 少 zero0)

    # game-strings (UI text 6 lang) — 见 doc/dev/data-structure/game-strings.md
    # 1642 行 master pointer table @ 0x08000F40, 每行 24 B = 6 lang × 4 B offset
    # 顺序 [JA, EN, DE, FR, IT, ES]; offset = entry_addr - game_str_ja (BASE)
    # 代码引用: 0x08000F40 ROM 字面量 101 hits, 0x09DB9C10 99 hits

    # logical_id -> master_row 重映射表 (见 game_str_id_to_row 即 FUN_080f4e18 的二分查找)
    # 游戏代码用 16-bit logical_id (如 0x1004) 调 game_str_id_to_row, 返回 master row.
    # arr[0..199] 多为 identity, 高范围 (0x10XX/0x13XX/0x6XX/0x7XX) 为 game-message 类别.
    (0x08000240, "game_str_id_remap_count"),   # u16, 当前 = 0x0673 = 1651
    (0x08000250, "game_str_id_remap_table"),   # 1651 × u16 sorted, 3302 B (0x250..0xF36)

    (0x08000F40, "game_str_pointer_table"),  # master 表, 1642 × 24 B = 39408 B
    (0x09DB9C10, "game_str_ja"),             # JA 区起点 (= STRING_TABLE_BASE)
    (0x09DC4620, "game_str_en"),             # EN 区起点
    (0x09DCF471, "game_str_de"),             # DE 区起点
    (0x09DDB7DE, "game_str_fr"),             # FR 区起点
    (0x09DE7CB7, "game_str_it"),             # IT 区起点
    (0x09DF3C66, "game_str_es"),             # ES 区起点

    (0x09E58D0C, "deck_record_table"),       # = data/opponent-card-values.s; 121×32B = 0xF20 B
                                              # 三段: Opponent(27) + Theme(52) + Limited(42)
                                              # 结构 {u16 deck_id, u16 cv, u16 dup, char path[26]}
                                              # 代码循环上限 r1<=0x78 (FUN_0801f3e8 / FUN_080242c8)

    (0x09E5F6CC, "banlist_master_table"),     # = data/banlists.s 末段; 10 × 8B = 80 B
                                              # {u32 entries_ptr, u32 count}, banlist_default 拆 3 段
                                              # 唯一 caller 字面量池 .word @ 0x080EF00C

    # post-banlists 4 张表 (data/post-banlists-tables.s, ROM 0x1E5F71C..0x1E5F884 = 0x168 B)
    (0x09E5F71C, "level_signature_table"),    # 14 × 20 B (Limited Duel 等级数据? 推测)
                                              # {u16 so_code, char field_a[8], char field_b[8], u16 pad}
                                              # caller: 0x080EF474 base, 0x0801D8A0 / 0x0801D8FC field a/b
    (0x09E5F834, "font_jp_dim_table"),        # 32 B = 4 × {u32, u32} 维度配对
    (0x09E5F854, "font_jp_base_table"),       # 32 B = 8 × u32 ptrs ⭐ HOT 92 ldrs
                                              # ptr[0..3] alt fonts (state-bits 选择), ptr[4..7] font_jp_*
    (0x09E5F874, "font_jp_stride_table"),     # 16 B = 4 × u32 (100/144/144/196 = per-glyph 字节数)

    # 代码内分支标签（非函数入口，用 LAB 命名以便 Ghidra 视为代码标签）
    # 这两处在 wiki 反汇编里是入口/中间点，但 Ghidra 已识别为 LAB_*；
    # 保留 wiki 语义注释即可，不强行重命名。

    # EWRAM
    (0x02006C2C, "gSettings"),
    (0x02006C38, "gMoneyDp"),
    (0x02006C3C, "gDuelPuzzleProgress"),
    (0x02006CC8, "gLimitedDuelProgress"),
    (0x02006D6C, "gThemeDuelScores"),
    (0x02006E48, "gPlayerName"),
    (0x02006E57, "gPlayerIcon"),
    (0x02006E5C, "gUnlockedDuelists"),

    # 对手胜场数组 (27 × 4B, 0x02006E60..0x02006ECC)
    # gWinsBase 是数组起点 label, gWinsKuriboh 是 [0] 元素 label, 同址共存
    (0x02006E60, "gWinsBase"),
    (0x02006E60, "gWinsKuriboh"),
    (0x02006E64, "gWinsScapegoat"),
    (0x02006E68, "gWinsSkullServant"),
    (0x02006E6C, "gWinsWatapon"),
    (0x02006E70, "gWinsWhiteMagicianPikeru"),
    (0x02006E74, "gWinsBatterymanC"),
    (0x02006E78, "gWinsOjamaYellow"),
    (0x02006E7C, "gWinsGoblinKing"),
    (0x02006E80, "gWinsDesFrog"),
    (0x02006E84, "gWinsWaterDragon"),
    (0x02006E88, "gWinsRedEyesDarknessDragon"),
    (0x02006E8C, "gWinsVampireGenesis"),
    (0x02006E90, "gWinsInfernalFlameEmperor"),
    (0x02006E94, "gWinsOceanDragonLord"),
    (0x02006E98, "gWinsHeliosDuoMegiste"),
    (0x02006E9C, "gWinsGilfordTheLegend"),
    (0x02006EA0, "gWinsDarkEradicatorWarlock"),
    (0x02006EA4, "gWinsGuardianExode"),
    (0x02006EA8, "gWinsGoldd"),
    (0x02006EAC, "gWinsElementalHeroErikshieler"),
    (0x02006EB0, "gWinsRavielLordOfPhantasms"),
    (0x02006EB4, "gWinsHorusLv8"),
    (0x02006EB8, "gWinsStronghold"),
    (0x02006EBC, "gWinsSacredPhoenix"),
    (0x02006EC0, "gWinsCyberEndDragon"),
    (0x02006EC4, "gWinsPlayer"),
    (0x02006EC8, "gWinsCopycat"),

    (0x0201C4E0, "gP1LifePoints"),
    (0x0201CD48, "gP2LifePoints"),
    (0x0201FEC0, "gBannerState"),  # banner 出/入场动画状态结构 (EWRAM); +0x10 = u8 main state, +0x11 = u8 sub-counter; 被 banner_anim_state_machine + FUN_080be600 共用
    (0x02029512, "gPlayerNameEntry"),
    (0x02029810, "gBanlistPasswordBuffer"),
    (0x02029EC0, "gDemoState"),  # demo 过场动画状态结构 (EWRAM); +0x88 = fs 解压指针; +0x8c = packed bitfield (bit0=done, bits9..16=main state); +0x8e = u16 sub-state; +0x94 = u32 frame counter; demo_shuen_state_machine 用

    # IWRAM
    (0x03000040, "gPrng"),
    (0x03000240, "gFrameCounter"),
    (0x03005850, "pack_ui_state"),  # pack scene 状态结构 (IWRAM); offset 0x10 = u16 state field
]


def set_label(gba_addr, name):
    st = currentProgram.getSymbolTable()
    addr = toAddr(gba_addr)

    existing = st.getSymbols(name)
    for s in existing:
        if s.getAddress().equals(addr):
            print("[skip] %s @ %s (already exists)" % (name, addr))
            return True

    if RUN_DRY:
        print("[dry] %s @ 0x%08X" % (name, gba_addr))
        return True

    try:
        st.createLabel(addr, name, SourceType.USER_DEFINED)
        print("[ok] %s @ 0x%08X" % (name, gba_addr))
        return True
    except Exception as e:
        print("[fail] %s @ 0x%08X: %s" % (name, gba_addr, e))
        return False


# 历史命名迁移 (old -> new)。每次跑脚本都尝试清理,幂等。
# 原因记录:
#   card_names_pool -> card_names_table: data/card-names.s 注释明确正式名是 _table,
#     _pool 是早期从 Data Crystal wiki 搬来的别名
RENAMES = [
    ("card_names_pool", "card_names_table"),
    # data/card-descriptions.s 命名风格对齐 card-names.s:
    #   pool -> table (实际数据), data -> pointer_table (offset 索引)
    ("card_desc_text_pool", "card_descs_table"),
    ("card_desc_data",      "card_desc_pointer_table"),
    # 命名精细化: 与 duel_field_outer_palette_pointers / _tilemap_pointers 并列
    ("duel_field_outer_pointer_table", "duel_field_outer_tile_pointers"),
    # opponent_card_values 实为 121 条 deck record (含 theme/limited),改 deck_record_table
    ("deck_id_and_data_array", "deck_record_table"),
]

# 需要从 Ghidra 彻底删除的错误 label (地址或名字错)。幂等。
# 原因记录:
#   card_effect_text_pool @ 0x095FFF6C 地址错 0x60 字节,实际应为
#     card_desc_text_pool @ 0x095FFF0C (data/card-descriptions.s:29)。
#     asm/all.s 0x095FFF6C 0 引用证实该地址不是任何字面量池目标。
REMOVALS = [
    (0x095FFF6C, "card_effect_text_pool"),
    # 旧 file_opponent_card_values_start: 数据文件起点回退到 0x09E58D0C 后该 label 错位 2B
    (0x09E58D0E, "file_opponent_card_values_start"),
    # 旧 file_game_strings_* 系列 label (与 game_str_* 同址重复, 清掉旧的)
    (0x09DC4620, "file_game_strings_en_start"),
    (0x09DC4620, "file_game_strings_start"),
    (0x09DCF471, "file_game_strings_de_start"),
    (0x09DDB7DE, "file_game_strings_fr_start"),
    (0x09DE7CB7, "file_game_strings_it_start"),
    (0x09DF3C66, "file_game_strings_es_start"),
]


def apply_renames():
    st = currentProgram.getSymbolTable()
    for old_name, new_name in RENAMES:
        syms = list(st.getSymbols(old_name))
        if not syms:
            continue
        for s in syms:
            if RUN_DRY:
                print("[dry-rename] %s @ %s -> %s" % (old_name, s.getAddress(), new_name))
                continue
            try:
                s.setName(new_name, SourceType.USER_DEFINED)
                print("[rename] %s @ %s -> %s" % (old_name, s.getAddress(), new_name))
            except Exception as e:
                print("[rename-fail] %s: %s" % (old_name, e))


def apply_removals():
    st = currentProgram.getSymbolTable()
    for gba_addr, name in REMOVALS:
        addr = toAddr(gba_addr)
        target = None
        for s in st.getSymbols(name):
            if s.getAddress().equals(addr):
                target = s
                break
        if target is None:
            continue
        if RUN_DRY:
            print("[dry-remove] %s @ 0x%08X" % (name, gba_addr))
            continue
        try:
            target.delete()
            print("[remove] %s @ 0x%08X" % (name, gba_addr))
        except Exception as e:
            print("[remove-fail] %s @ 0x%08X: %s" % (name, gba_addr, e))


def main():
    apply_removals()
    apply_renames()
    ok = 0
    for gba_addr, name in LABELS:
        if set_label(gba_addr, name):
            ok += 1
    print("[done] LabelDataCrystalRomMap: %d/%d" % (ok, len(LABELS)))


main()
