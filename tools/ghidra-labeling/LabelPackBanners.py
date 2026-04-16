# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# LabelPackBanners.py  (Jython 2.7 / Ghidra script)
#
# 为 pack banner 数据区创建 label:
#   - pack_banner_obj_palette  @ 0x08510440 (256色 OBJ 调色板, 512B)
#   - pack_banner_ptr_table    @ 0x09CCE960 (51 条指针, 204B)
#   - pack_banner_00..50       @ 0x09CCEA2C+ (各 0x800B tile 数据)
#
# 来源: doc/dev/pack-banner-static-analysis.md

from ghidra.program.model.symbol import SourceType
import struct

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass

PACK_COUNT = 51

LABELS = [
    (0x08510440, "pack_banner_obj_palette"),
    (0x09CCE960, "pack_banner_ptr_table"),
]

# 从 ROM 读指针表, 获取各 pack tile 数据地址
def read_pack_pointers():
    """读取指针表, 返回 [(gba_addr, label_name), ...]"""
    mem = currentProgram.getMemory()
    table_addr = toAddr(0x09CCE960)
    result = []
    for i in range(PACK_COUNT):
        addr = table_addr.add(i * 4)
        ptr = mem.getInt(addr) & 0xFFFFFFFF
        result.append((ptr, "pack_banner_%02d" % i))
    return result


def set_label(gba_addr, name):
    st = currentProgram.getSymbolTable()
    addr = toAddr(gba_addr)

    # 检查是否已存在同名
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

    # 从指针表读取各 pack 地址
    pack_ptrs = read_pack_pointers()
    for gba_addr, name in pack_ptrs:
        if set_label(gba_addr, name):
            ok += 1

    total = len(LABELS) + len(pack_ptrs)
    print("[done] LabelPackBanners: %d/%d" % (ok, total))


main()
