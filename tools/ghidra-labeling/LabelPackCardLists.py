# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# LabelPackCardLists.py  (Jython 2.7 / Ghidra script)
#
# 为 pack 卡牌列表 + 信息表创建 label:
#   - pack_XX_card_list    @ 各 pack 卡牌列表起始 (从信息表指针动态读取)
#   - pack_info_table      @ 0x09E5E2E8 (51 条 x 16B = 816B)
#
# 来源: doc/dev/pack-card-list-analysis.md (TBD)
# 数据范围: 0x09E5ABFC ~ 0x09E5E618

from ghidra.program.model.symbol import SourceType

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass

PACK_COUNT = 51
PACK_INFO_TABLE_ADDR = 0x09E5E2E8
PACK_INFO_SIZE = 16

LABELS = [
    (PACK_INFO_TABLE_ADDR, "pack_info_table"),
]


def read_pack_card_list_pointers():
    """从信息表读取各 pack 卡牌列表指针。"""
    mem = currentProgram.getMemory()
    result = []
    for i in range(PACK_COUNT):
        addr = toAddr(PACK_INFO_TABLE_ADDR + i * PACK_INFO_SIZE + 12)
        ptr = mem.getInt(addr) & 0xFFFFFFFF
        if 0x08000000 <= ptr <= 0x0A000000:
            result.append((ptr, "pack_%02d_card_list" % i))
    return result


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

    # 固定 label
    for gba_addr, name in LABELS:
        if set_label(gba_addr, name):
            ok += 1

    # 从信息表读取各 pack 卡牌列表地址
    card_list_ptrs = read_pack_card_list_pointers()
    for gba_addr, name in card_list_ptrs:
        if set_label(gba_addr, name):
            ok += 1

    total = len(LABELS) + len(card_list_ptrs)
    print("[done] LabelPackCardLists: %d/%d" % (ok, total))


main()
