# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# LabelDataCrystalRomMap.py  (Jython 2.7 / Ghidra script)
#
# 给 Data Crystal ROM map 揭示的几个数据区打标签：
#   - card_image_index        @ 0x095B5C00  (card_id 0..2098)
#   - cards_ids_array         @ 0x095B7CCC  (internal_card_id -> card_id, 3072 x u16)
#   - card_names_pool         @ 0x095BB594  (cards names base, per Data Crystal)
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
    (0x095B5C00, "card_image_index"),
    (0x095B7CCC, "cards_ids_array"),
    (0x095BB594, "card_names_pool"),
    (0x095F3A5C, "card_name_pointer_table"),
    (0x095FFF6C, "card_effect_text_pool"),
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
    (0x02006E60, "gWinsBase"),
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


def main():
    ok = 0
    for gba_addr, name in LABELS:
        if set_label(gba_addr, name):
            ok += 1
    print("[done] LabelDataCrystalRomMap: %d/%d" % (ok, len(LABELS)))


main()
