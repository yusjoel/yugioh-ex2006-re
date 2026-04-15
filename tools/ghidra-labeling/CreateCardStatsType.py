# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# CreateCardStatsType.py  (Jython 2.7 / Ghidra script)
#
# TG.1 + TG.3
#   - 建 enum: AttrCode / RaceCode / SubtypeCode / SpSubCode
#   - 建 struct: CardStats (22 B, uint16 x 11) / DeckEntry (4 B)
#   - 应用到:
#       0x098169B6  CardStats[5170]
#       0x09E5FA58  DeckEntry[... (struct decks)]  // 6 个 Structure Decks
#       0x09E5F884  uint16[...]  (starter_deck, 终止 0x0000)
#       0x09E6468E  uint16[...]  (opponent decks 区整体)
#       0x09CCCA90  byte[2048]   (font_ascii_8x8)
#       0x095B5C00  uint16[14540/2] (card_image_index)
#
# 约束: Ghidra 内置 Jython 2.7。不要用 f-string / pathlib。
#
# @category Ygo-ex2006

from ghidra.program.model.data import (
    CategoryPath, DataTypeConflictHandler, EnumDataType, StructureDataType,
    UnsignedShortDataType, ByteDataType, ArrayDataType,
)
from ghidra.program.model.symbol import SourceType


CATEGORY = CategoryPath("/ygo_ex2006")

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def get_dtm():
    return currentProgram.getDataTypeManager()


def ensure_category(dtm):
    if dtm.getCategory(CATEGORY) is None:
        dtm.createCategory(CATEGORY)


def add_or_replace(dtm, dt):
    if RUN_DRY:
        print("[dry/type] would add/replace %s/%s" % (CATEGORY, dt.getName()))
        return dt  # 未登记; 后续仅用于 apply_array 的打印
    existing = dtm.getDataType(CATEGORY, dt.getName())
    if existing is not None:
        dtm.remove(existing, monitor)
    return dtm.addDataType(dt, DataTypeConflictHandler.REPLACE_HANDLER)


def build_enum(dtm, name, size_bytes, entries):
    e = EnumDataType(CATEGORY, name, size_bytes)
    for k, v in entries:
        e.add(k, v)
    return add_or_replace(dtm, e)


def build_structs(dtm, attr_enum, race_enum, subtype_enum, spsub_enum):
    cs = StructureDataType(CATEGORY, "CardStats", 0)
    u16 = UnsignedShortDataType.dataType
    cs.add(u16, 2, "zero0",   "+00 恒 0 (首条哑元除外)")
    cs.add(u16, 2, "slot_id", "+02 卡槽编号")
    cs.add(u16, 2, "copy",    "+04 异画索引 0..3")
    cs.add(u16, 2, "flags",   "+06 1=正常, 0=哑元, 3=?")
    cs.add(u16, 2, "atk",     "+08 攻击力")
    cs.add(u16, 2, "def_",    "+0A 守备力")
    cs.add(u16, 2, "level",   "+0C 星数")
    cs.add(race_enum,    2, "race",    "+0E RACE_*")
    cs.add(attr_enum,    2, "attr",    "+10 ATTR_*")
    cs.add(subtype_enum, 2, "subtype", "+12 SUBTYPE_*")
    cs.add(spsub_enum,   2, "spsub",   "+14 SPSUB_*")
    cs_dt = add_or_replace(dtm, cs)

    de = StructureDataType(CATEGORY, "DeckEntry", 0)
    de.add(u16, 2, "packed", "so_code<<2 | qty (0..3)")
    de.add(u16, 2, "pad",    "恒 0")
    de_dt = add_or_replace(dtm, de)
    return cs_dt, de_dt


def addr(hex_str):
    return currentProgram.getAddressFactory().getAddress(hex_str)


def clear_range(start, length):
    end = start.add(length - 1)
    listing = currentProgram.getListing()
    listing.clearCodeUnits(start, end, False)


def apply_array(data_addr, element_dt, count, label=None):
    length = element_dt.getLength() * count
    if RUN_DRY:
        print("[dry/apply] %s @ %s  x%d  (%d B) label=%s" % (
            element_dt.getName(), data_addr, count, length, label))
        return
    clear_range(data_addr, length)
    arr = ArrayDataType(element_dt, count, element_dt.getLength())
    createData(data_addr, arr)
    if label is not None:
        createLabel(data_addr, label, True, SourceType.USER_DEFINED)
    print("[apply] %s @ %s  x%d  (%d B)" % (element_dt.getName(), data_addr, count, length))


def main():
    dtm = get_dtm()
    ensure_category(dtm)

    attr_entries = [
        ("ATTR_LIGHT", 1), ("ATTR_DARK", 2), ("ATTR_WATER", 3),
        ("ATTR_FIRE", 4),  ("ATTR_EARTH", 5), ("ATTR_WIND", 6),
        ("ATTR_DIVINE", 7), ("ATTR_SPELL", 8), ("ATTR_TRAP", 9),
    ]
    race_entries = [
        ("RACE_DRAGON", 1),  ("RACE_ZOMBIE", 2),  ("RACE_FIEND", 3),
        ("RACE_PYRO", 4),    ("RACE_SEA_SERPENT", 5), ("RACE_ROCK", 6),
        ("RACE_MACHINE", 7), ("RACE_FISH", 8),    ("RACE_DINOSAUR", 9),
        ("RACE_INSECT", 10), ("RACE_BEAST", 11),  ("RACE_BEAST_WARRIOR", 12),
        ("RACE_PLANT", 13),  ("RACE_AQUA", 14),   ("RACE_WARRIOR", 15),
        ("RACE_WINGED_BEAST", 16), ("RACE_FAIRY", 17), ("RACE_SPELLCASTER", 18),
        ("RACE_THUNDER", 19), ("RACE_REPTILE", 20), ("RACE_DIVINE_BEAST", 21),
        ("RACE_SPELL", 22),  ("RACE_TRAP", 23),
    ]
    subtype_entries = [
        ("SUBTYPE_NORMAL", 0),        ("SUBTYPE_EFFECT", 1),
        ("SUBTYPE_FUSION", 2),        ("SUBTYPE_FUSION_EFFECT", 3),
        ("SUBTYPE_RITUAL", 4),        ("SUBTYPE_RITUAL_EFFECT", 5),
        ("SUBTYPE_TOON", 6),          ("SUBTYPE_SPIRIT", 7),
        ("SUBTYPE_UNION", 8),         ("SUBTYPE_TOKEN", 9),
        ("SUBTYPE_SPELL_CARD", 13),   ("SUBTYPE_TRAP_CARD", 14),
    ]
    spsub_entries = [
        ("SPSUB_NORMAL", 0), ("SPSUB_COUNTER", 1),    ("SPSUB_FIELD", 2),
        ("SPSUB_EQUIP", 3),  ("SPSUB_CONTINUOUS", 4), ("SPSUB_QUICK_PLAY", 5),
        ("SPSUB_RITUAL", 6),
    ]

    attr_e    = build_enum(dtm, "AttrCode",    2, attr_entries)
    race_e    = build_enum(dtm, "RaceCode",    2, race_entries)
    subtype_e = build_enum(dtm, "SubtypeCode", 2, subtype_entries)
    spsub_e   = build_enum(dtm, "SpSubCode",   2, spsub_entries)

    card_stats_dt, deck_entry_dt = build_structs(dtm, attr_e, race_e, subtype_e, spsub_e)

    print("[ok] types created in %s" % CATEGORY)

    # ---- 应用 ----
    # CardStats[5170] @ 0x098169B6
    apply_array(addr("0x098169B6"), card_stats_dt, 5170, label="card_stats_table")

    # Structure Decks: 顶层 table @ 0x09E5FD54，共 6 条 deck 数据在 0x09E5FA58..0x09E5FD54
    # 6 个 deck 的入口地址（注释里给的 GBA 地址）:
    struct_decks = [
        ("dragons_roar",            "0x09E5FA58", 28),
        ("zombie_madness",          "0x09E5FAC8", 28),
        ("molten_destruction",      "0x09E5FB38", 31),
        ("fury_from_the_deep",      "0x09E5FBB4", 32),
        ("warriors_triumph",        "0x09E5FC34", 36),
        ("spellcasters_judgement",  "0x09E5FCC4", 36),
    ]
    for name, a, slots in struct_decks:
        apply_array(addr(a), deck_entry_dt, slots, label=name)
    createLabel(addr("0x09E5FD54"), "struct_deck_table", True, SourceType.USER_DEFINED)

    # font_ascii_8x8 @ 0x09CCCA90, 2048 B
    apply_array(addr("0x09CCCA90"), ByteDataType.dataType, 2048, label="font_ascii_8x8")

    # card_image_index @ 0x095B5C00, (0x15B94CC - 0x15B5C00)/2 = 7270 u16
    apply_array(addr("0x095B5C00"), UnsignedShortDataType.dataType, 7270,
                label="card_image_index")

    # starter_deck / opponent decks 仅打顶层 label（变长 + 0x0000 终止，数组无法一次性确定）
    createLabel(addr("0x09E5F884"), "starter_deck", True, SourceType.USER_DEFINED)
    createLabel(addr("0x09E6468E"), "opponent_decks_start", True, SourceType.USER_DEFINED)

    print("[done] CreateCardStatsType.py")


main()
