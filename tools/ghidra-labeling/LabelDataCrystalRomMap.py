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
    (0x095B5C00, "card_image_index"),
    (0x095B7CCC, "cards_ids_array"),
    (0x095B94CC, "card_passcode_table"),  # 2098 × u32 加密密码表
    (0x095BB594, "card_names_table"),     # 曾用名 card_names_pool; data 源统一叫 _table
    (0x095F3A5C, "card_name_pointer_table"),
    (0x095FFF0C, "card_descs_table"),        # 曾用名 card_desc_text_pool / card_effect_text_pool@0x095FFF6C(错)
    (0x0980A508, "card_desc_pointer_table"), # 2098 × 6 × u32 per-cid offset 表; 曾用名 card_desc_data
    (0x098169B8, "card_stats_table"),      # 5170 × 22 B (首条 20B 少 zero0)
    (0x09E58D0C, "deck_id_and_data_array"),  # = data/opponent-card-values.s (-2B); 27×32B
                                              # wiki 标注的 << 16 stride 是 lsr r4,0x16 误读

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
    (0x02029512, "gPlayerNameEntry"),
    (0x02029810, "gBanlistPasswordBuffer"),

    # IWRAM
    (0x03000040, "gPrng"),
    (0x03000240, "gFrameCounter"),
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
]

# 需要从 Ghidra 彻底删除的错误 label (地址或名字错)。幂等。
# 原因记录:
#   card_effect_text_pool @ 0x095FFF6C 地址错 0x60 字节,实际应为
#     card_desc_text_pool @ 0x095FFF0C (data/card-descriptions.s:29)。
#     asm/all.s 0x095FFF6C 0 引用证实该地址不是任何字面量池目标。
REMOVALS = [
    (0x095FFF6C, "card_effect_text_pool"),
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
