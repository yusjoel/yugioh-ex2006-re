# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotatePackUIDialog.py  (Jython 2.7 / Ghidra script)
#
# 深入分析单函数标准流程 (build-pipeline.md §三) 的产物:
#   - text_overlay_create (FUN_080dd53c) 参数签名 (r0=size_packed, r1=flags, r2=text)
#   - pack_ui_show_all_opened_done (FUN_080d6290) 行级 EOL 注释
#
# 前置: LabelDataCrystalRomMap.py + RenameKnownFunctions.py 已跑过
#       (label / rename / plate comment 已就位)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AnnotatePackUIDialog.py
#
# 中文注释 utf-8: 必须 .decode("utf-8") 否则 Java 把 bytes 当 Latin-1 收 mojibake.

from ghidra.program.model.listing import (
    ParameterImpl, Function, CodeUnit
)
from ghidra.program.model.data import (
    UnsignedIntegerDataType, PointerDataType, CharDataType
)
from ghidra.program.model.symbol import SourceType


def u(s):
    """Python 2 str (utf-8 bytes) -> unicode for Java setComment."""
    if isinstance(s, str):
        return s.decode("utf-8")
    return s


def annotate_text_overlay_create():
    """FUN_080dd53c (text_overlay_create) 参数签名."""
    func = getFunctionAt(toAddr(0x080dd53c))
    if func is None:
        print("[skip] text_overlay_create: function not found")
        return False

    name = func.getName()
    if name not in ("FUN_080dd53c", "text_overlay_create"):
        print("[skip] text_overlay_create: unexpected name '%s'" % name)
        return False

    uint_dt = UnsignedIntegerDataType.dataType
    char_ptr = PointerDataType(CharDataType.dataType)

    params = [
        ParameterImpl(
            "size_packed", uint_dt, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl(
            "flags", uint_dt, currentProgram, SourceType.USER_DEFINED),
        ParameterImpl(
            "text", char_ptr, currentProgram, SourceType.USER_DEFINED),
    ]

    try:
        func.replaceParameters(
            Function.FunctionUpdateType.DYNAMIC_STORAGE_FORMAL_PARAMS,
            True,
            SourceType.USER_DEFINED,
            *params
        )
        print("[ok] text_overlay_create params: (size_packed, flags, text)")
        return True
    except Exception as e:
        print("[fail] text_overlay_create replaceParameters: %s" % e)
        return False


# pack_ui_show_all_opened_done (FUN_080d6290) 行级 EOL 注释
# 注: 经典 game_str lookup 链 (12 条 ldr/lsl/add) 不每条都注释,
#     头尾各一条标记进入/退出 lookup 链.
EOL_COMMENTS_080D6290 = [
    (0x080d6290, "pack_ui_show_all_opened_done: 入口"),
    (0x080d6292, "r4 = dialog size = (h=10 << 16) | w=30 = 0x000a001e"),
    (0x080d6294, "r0 = logical string id 0x13f7"),
    (0x080d6296, "r0 = master_row (= 1086 = 'Opened all packs.')"),
    (0x080d629a, "<<< 经典 game_str lookup chain: row -> string addr (lang from gSettings) >>>"),
    (0x080d62b8, "r2 = master[row].offset[lang]"),
    (0x080d62bc, "r2 = STRING_TABLE_BASE + offset = 'Opened all packs.' 字符串地址"),
    (0x080d62be, "r0 = size_packed (0x000a001e), r1 = flags (0), r2 = text"),
    (0x080d62c2, "text_overlay_create(size, 0, 'Opened all packs.')"),
    (0x080d62c8, "FUN_080d55cc(1) -- pack ui helper (TODO: 命名)"),
    (0x080d62ce, "FUN_080d46a8(1) -- pack ui helper (TODO: 命名)"),
    (0x080d62d4, "FUN_080d5184(3) -- pack ui helper (TODO: 命名)"),
    (0x080d62da, "r0 = 8 (next state)"),
    (0x080d62dc, "pack_ui_state[+0x10] = 8  (切 pack 状态机到完成态)"),
    (0x080d62de, "r0 = 1 (return value: success)"),
]


def set_eol_comment(addr_int, txt):
    listing = currentProgram.getListing()
    a = toAddr(addr_int)
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[skip] no codeunit @ 0x%08x" % addr_int)
        return False
    cu.setComment(CodeUnit.EOL_COMMENT, u(txt))
    return True


def annotate_pack_ui_show_all_opened_done():
    n_set = 0
    for addr, txt in EOL_COMMENTS_080D6290:
        if set_eol_comment(addr, txt):
            n_set += 1
    print("[ok] pack_ui_show_all_opened_done EOL comments set: %d / %d"
          % (n_set, len(EOL_COMMENTS_080D6290)))


def main():
    print("=== AnnotatePackUIDialog ===")
    annotate_text_overlay_create()
    annotate_pack_ui_show_all_opened_done()
    print("[done]")


main()
