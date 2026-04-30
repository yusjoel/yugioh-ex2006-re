# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ExportComments.py  (Jython 2.7 / Ghidra script)
#
# 导出 Ghidra 工程内所有 USER_DEFINED 注释 (plate / pre / post / EOL / repeatable)
# 与函数 repeatable comment, 写到 temp/ghidra-comments.csv.
#
# 用途:
#   - 把"深入分析过的函数/数据"的人工注释从 .rep 二进制工程导成纯文本
#   - 不在 Ghidra 内的 reviewer 也能看到; 也作为分析备份 (避免 .rep 损坏丢失)
#   - 每次给函数加 plate comment 后跑一次, diff 检查
#
# CSV 格式:
#   address, kind, owner_name, comment
#     kind: plate / pre / post / eol / repeatable / func_repeatable / data_repeatable
#     owner_name: 函数名/数据 label/空 (取决于 kind)
#     comment: 多行用 \n 转义保留 (CSV quote 处理)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat ExportComments.py
#
# 只读: 不 createFunction / 不 setName / 不 setComment.

import os
import sys

from ghidra.program.model.listing import CodeUnit


COMMENT_KINDS = [
    (CodeUnit.PLATE_COMMENT,      "plate"),
    (CodeUnit.PRE_COMMENT,        "pre"),
    (CodeUnit.POST_COMMENT,       "post"),
    (CodeUnit.EOL_COMMENT,        "eol"),
    (CodeUnit.REPEATABLE_COMMENT, "repeatable"),
]


def repo_root():
    """ghidra-labeling/ 上面两层就是仓库根."""
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def safe_csv(s):
    """Jython 2.7: 显式 unicode 处理, 否则 ASCII codec 在中文上炸."""
    if s is None:
        return ""
    if isinstance(s, unicode):
        s = s.encode("utf-8")
    elif not isinstance(s, str):
        s = str(s)
    if s == "":
        return ""
    if "," in s or '"' in s or "\n" in s or "\r" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def get_owner_name(addr_int, listing, sym_table, fm):
    """优先函数名; 否则取该地址 USER_DEFINED label; 否则 ''."""
    addr = currentProgram.getAddressFactory().getAddress("0x%x" % addr_int)
    if addr is None:
        return ""
    func = fm.getFunctionContaining(addr)
    if func is not None and func.getEntryPoint().getOffset() == addr_int:
        return func.getName()
    sym = sym_table.getPrimarySymbol(addr)
    if sym is not None:
        return sym.getName()
    return ""


def main():
    root = repo_root()
    out_dir = os.path.join(root, "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_path = os.path.join(out_dir, "ghidra-comments.csv")
    # binary mode: write utf-8 bytes (Jython 2.7 文本模式默认 ASCII 会炸中文)
    fcsv = open(out_path, "wb")
    fcsv.write("address,kind,owner_name,comment\n")

    listing = currentProgram.getListing()
    sym_table = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()

    n_total = 0
    n_by_kind = {name: 0 for _, name in COMMENT_KINDS}
    n_by_kind["func_repeatable"] = 0

    # --- 1) CodeUnit-level comments (plate/pre/post/eol/repeatable) ---
    # getCommentAddressIterator(comment_type, addr_set, forward) 返回所有有该类型 comment 的地址
    addr_set = currentProgram.getMemory()
    for ctype, kname in COMMENT_KINDS:
        try:
            it = listing.getCommentAddressIterator(ctype, addr_set, True)
        except Exception as e:
            print("[warn] getCommentAddressIterator(%s) failed: %s" % (kname, e))
            continue
        while it.hasNext():
            addr = it.next()
            cu = listing.getCodeUnitAt(addr)
            if cu is None:
                continue
            comment = cu.getComment(ctype)
            if not comment:
                continue
            addr_int = addr.getOffset() & 0xFFFFFFFF
            owner = get_owner_name(addr_int, listing, sym_table, fm)
            fcsv.write("0x%08x,%s,%s,%s\n" % (
                addr_int, kname, safe_csv(owner), safe_csv(comment)))
            n_total += 1
            n_by_kind[kname] += 1

    # --- 2) Function repeatable comment (Function.getComment / setComment) ---
    funcs = fm.getFunctions(True)
    while funcs.hasNext():
        func = funcs.next()
        c = func.getComment()
        if not c:
            continue
        addr_int = func.getEntryPoint().getOffset() & 0xFFFFFFFF
        fcsv.write("0x%08x,func_repeatable,%s,%s\n" % (
            addr_int, safe_csv(func.getName()), safe_csv(c)))
        n_total += 1
        n_by_kind["func_repeatable"] += 1

    fcsv.close()

    print("[done] ExportComments")
    print("  total comments exported : %d" % n_total)
    for k in ["plate", "pre", "post", "eol", "repeatable", "func_repeatable"]:
        print("    %-15s : %d" % (k, n_by_kind[k]))
    print("  -> %s" % out_path)


main()
