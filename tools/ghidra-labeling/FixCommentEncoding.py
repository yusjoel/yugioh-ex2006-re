# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixCommentEncoding.py  (Jython 2.7 / Ghidra script)
#
# 一次性修复历史 plate / pre / post / EOL / repeatable / function 注释里的 mojibake.
#
# 起因 (2026-04-30):
#   过去脚本 (RenameKnownFunctions.py 等) 在 Jython 中以 utf-8 bytes (Python 2 str)
#   形式调 cu.setComment(...) / func.setComment(...). Java 把 bytes 当 Latin-1
#   收成 String, 每个 utf-8 字节对应一个 char => 存进 .rep 全是 mojibake.
#
#   修复算法: 对每条注释, 用 latin-1 重新编码再 utf-8 解码. 如果产出有效 unicode
#   且与原文不同, 写回. 否则保留 (避免破坏纯 ASCII / 已是正确 unicode 的注释).
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat FixCommentEncoding.py [dry]

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


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def try_fix_mojibake(s):
    """
    s: unicode (Java String -> Python unicode in Jython).
    若 s 是 'utf-8 bytes 被 Latin-1 解读' 形式, 修回正确 unicode.
    返回 (new_s, did_change). 失败 (原文已正确 / 不是 mojibake / 解码失败) 则 (s, False).
    """
    if s is None:
        return (None, False)
    # 全 ASCII: 不可能是 mojibake
    try:
        s.encode("ascii")
        return (s, False)
    except UnicodeEncodeError:
        pass
    # 试 latin-1 -> utf-8
    try:
        b = s.encode("latin-1")
    except UnicodeEncodeError:
        # 含非 latin-1 字符 (如已是正确中文): 不是 mojibake
        return (s, False)
    try:
        new = b.decode("utf-8")
    except UnicodeDecodeError:
        return (s, False)
    if new == s:
        return (s, False)
    return (new, True)


def main():
    listing = currentProgram.getListing()
    fm = currentProgram.getFunctionManager()
    addr_set = currentProgram.getMemory()

    n_total = 0
    n_changed = 0
    n_unchanged = 0
    by_kind = {name: [0, 0] for _, name in COMMENT_KINDS}  # [total, changed]
    by_kind["func_repeatable"] = [0, 0]

    samples = []  # (kind, addr, old, new)

    # CodeUnit 注释
    for ctype, kname in COMMENT_KINDS:
        try:
            it = listing.getCommentAddressIterator(ctype, addr_set, True)
        except Exception as e:
            print("[warn] iterator(%s): %s" % (kname, e))
            continue
        while it.hasNext():
            addr = it.next()
            cu = listing.getCodeUnitAt(addr)
            if cu is None:
                continue
            old = cu.getComment(ctype)
            if not old:
                continue
            n_total += 1
            by_kind[kname][0] += 1
            new, changed = try_fix_mojibake(old)
            if not changed:
                n_unchanged += 1
                continue
            n_changed += 1
            by_kind[kname][1] += 1
            if len(samples) < 6:
                samples.append((kname, "0x%08x" % addr.getOffset(),
                                old[:80], new[:80]))
            if not RUN_DRY:
                cu.setComment(ctype, new)

    # Function repeatable
    funcs = fm.getFunctions(True)
    while funcs.hasNext():
        func = funcs.next()
        old = func.getComment()
        if not old:
            continue
        n_total += 1
        by_kind["func_repeatable"][0] += 1
        new, changed = try_fix_mojibake(old)
        if not changed:
            n_unchanged += 1
            continue
        n_changed += 1
        by_kind["func_repeatable"][1] += 1
        if not RUN_DRY:
            func.setComment(new)

    mode = "[dry]" if RUN_DRY else "[done]"
    print("%s FixCommentEncoding" % mode)
    print("  total comments scanned : %d" % n_total)
    print("  changed (fixed)        : %d" % n_changed)
    print("  unchanged              : %d" % n_unchanged)
    print("  by kind (total / fixed):")
    for k in ["plate", "pre", "post", "eol", "repeatable", "func_repeatable"]:
        t, c = by_kind[k]
        print("    %-15s : %4d / %4d" % (k, t, c))
    if samples:
        print("  samples (前 6 条):")
        for kname, a, oldv, newv in samples:
            try:
                # safe display: encode latin-1 then ignore
                old_disp = oldv.encode("ascii", "replace")
                new_disp = newv.encode("utf-8")
                print("    [%s %s] %s -> %s" % (kname, a, old_disp, new_disp))
            except Exception:
                print("    [%s %s] (encoding error)" % (kname, a))


main()
