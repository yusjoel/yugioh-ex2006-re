# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# VerifyTgRun.py  -- 检查 TG.1/TG.2/TG.3/TG.4 的产出是否已落到 Ghidra 工程.

from ghidra.program.model.data import Structure, Array


def check_type(dtm, cat, name):
    from ghidra.program.model.data import CategoryPath
    dt = dtm.getDataType(CategoryPath(cat), name)
    print("  %s/%s : %s" % (cat, name, "OK" if dt is not None else "MISSING"))
    return dt


def check_label_at(addr_hex, expected_names):
    st = currentProgram.getSymbolTable()
    af = currentProgram.getAddressFactory()
    a = af.getAddress(addr_hex)
    syms = list(st.getSymbols(a))
    names = set([s.getName() for s in syms])
    hits = [n for n in expected_names if n in names]
    print("  %s : %s  %s" % (addr_hex, ",".join(sorted(names))[:80], "OK" if hits else "MISS"))
    return len(hits) > 0


def check_function_renamed(old, new):
    st = currentProgram.getSymbolTable()
    old_syms = list(st.getSymbols(old))
    new_syms = list(st.getSymbols(new))
    ok = len(old_syms) == 0 and len(new_syms) >= 1
    print("  %-32s -> %-36s %s" % (old, new, "OK" if ok else "FAIL"))
    return ok


def check_array_type(addr_hex, expected_elem_name, expected_count):
    af = currentProgram.getAddressFactory()
    a = af.getAddress(addr_hex)
    d = currentProgram.getListing().getDataAt(a)
    if d is None:
        print("  %s : NO DATA" % addr_hex)
        return False
    dt = d.getDataType()
    info = "len=%d numElems=%s dt=%s" % (d.getLength(),
                                         getattr(dt, "getNumElements", lambda: "-")(),
                                         dt.getName())
    ok = isinstance(dt, Array) and dt.getDataType().getName() == expected_elem_name \
         and dt.getNumElements() == expected_count
    print("  %s : %s  %s" % (addr_hex, info, "OK" if ok else "MISMATCH"))
    return ok


def main():
    dtm = currentProgram.getDataTypeManager()

    print("== TG.1 types ==")
    check_type(dtm, "/ygo_ex2006", "CardStats")
    check_type(dtm, "/ygo_ex2006", "DeckEntry")
    check_type(dtm, "/ygo_ex2006", "AttrCode")
    check_type(dtm, "/ygo_ex2006", "RaceCode")
    check_type(dtm, "/ygo_ex2006", "SubtypeCode")
    check_type(dtm, "/ygo_ex2006", "SpSubCode")

    print("== TG.3 arrays ==")
    check_array_type("0x098169b6", "CardStats", 5170)
    check_array_type("0x09e5fa58", "DeckEntry", 28)
    check_array_type("0x09ccca90", "byte",      2048)
    check_array_type("0x095b5c00", "ushort",    7270)

    print("== TG.2 labels (spot-check) ==")
    check_label_at("0x098169b6", ["card_stats_table", "card_0000", "file_card_stats_start"])
    check_label_at("0x098169cc", ["card_0001"])
    check_label_at("0x09816cce", ["card_0024"])  # 中段采样
    check_label_at("0x09e6468e", ["deck_kuriboh", "file_opponent_decks_start"])
    check_label_at("0x09e5fa58", ["dragons_roar", "file_struct_decks_start"])
    check_label_at("0x09ccca90", ["font_ascii_8x8"])
    check_label_at("0x095b5c00", ["card_image_index"])
    check_label_at("0x09e65986", ["deck_raviel_lord_of_phantasms"])  # 最后一个对手卡组

    print("== TG.4 function renames ==")
    check_function_renamed("FUN_0801d290", "decode_card_image_6bpp")
    check_function_renamed("FUN_0801e440", "card_info_page_entry")
    check_function_renamed("FUN_080f1b60", "load_glyph_row_pair")
    check_function_renamed("FUN_080f2e4c", "commit_line_buffer_to_sprite_vram")

    print("[done] VerifyTgRun.py")


main()
