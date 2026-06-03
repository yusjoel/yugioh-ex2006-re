#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 all.s 实际行数均衡生成 ~N 段的 split_manifest.tsv 初稿。

策略:
  - 读 ghidra-functions.csv 拿全部函数起始地址 + 名字 (地址序)
  - 读 asm/all.s 建 addr->行号 索引, 求每个函数占的行数
  - 贪心打包: 累计行数达到 target_lines 时, 在「子系统名称发生转变」的函数处切
    (吸附窗口内找 tag 变化点, 找不到就硬切), 保证每段 ~ 均衡且边界落在语义转变
  - 每段文件名 = 序号 + 该段出现最多的 tag

产出 stdout (重定向覆盖 split_manifest.tsv)。生成后人工微调 tag/文件名/边界。
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALL_S = os.path.join(ROOT, "asm", "all.s")
FUNCS = os.path.join(ROOT, "temp", "ghidra-functions.csv")
ADDR_RE = re.compile(r"@\s*([0-9a-fA-F]{8})\b")

N_FILES = int(sys.argv[1]) if len(sys.argv) > 1 else 25


def tag(n):
    n = n.lower()
    if n.startswith("__") or any(k in n for k in ("muldi", "divdi", "udivdi", "reentr", "_fd_", "sbrk", "memcpy", "memset", "strlen", "clz", "ashldi", "lshrdi")):
        return "libc"
    if "pack" in n:
        return "pack"
    if "equip" in n:
        return "equip"
    if any(k in n for k in ("summon", "banlist", "deck", "passcode", "evolution", "fusion")):
        return "cardrules"
    if any(k in n for k in ("sound", "audio", "channel")):
        return "sound"
    if any(k in n for k in ("sprite", "oam", "vram", "palette", "tile", "dispcnt")):
        return "gfx"
    if any(k in n for k in ("render", "draw", "glyph", "font")):
        return "render"
    if any(k in n for k in ("str", "text", "line_buf", "encode", "decode", "char")):
        return "text"
    if any(k in n for k in ("duel", "card_list", "card_select")):
        return "duelscene"
    if any(k in n for k in ("field", "zone", "slot", "monster")):
        return "field"
    if any(k in n for k in ("scene", "menu", "page", "cursor", "input", "tick")):
        return "uiscene"
    return "misc"


def main():
    funcs = []
    with open(FUNCS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            funcs.append((int(r["address"], 16), r["name"]))
    funcs.sort()

    # 规范流: 优先 asm/all.s, 否则从拆分文件反向合并 (复用 split_all_s)
    import split_all_s
    lines, _nl = split_all_s.read_canonical(split_all_s.ALL_S, split_all_s.OUT_DIR, split_all_s.INCLUDES)
    addr_line = {}
    for i, line in enumerate(lines):
        m = ADDR_RE.search(line)
        if m:
            a = int(m.group(1), 16)
            if a not in addr_line:
                addr_line[a] = i

    # 每个函数的行号
    fl = []
    for a, n in funcs:
        if a in addr_line:
            fl.append((a, n, addr_line[a]))
    fl.sort(key=lambda x: x[2])
    total_lines = len(lines)
    target = total_lines / N_FILES

    # 贪心
    SNAP = 8  # 吸附窗口: 达阈值后再看 8 个函数内的 tag 变化点
    boundaries = [0]  # 函数下标
    i = 0
    cur_start_line = fl[0][2]
    while i < len(fl):
        # 找下一个边界
        seg_start_line = fl[boundaries[-1]][2]
        # 从 boundaries[-1]+1 起累计, 超 target 后吸附
        j = boundaries[-1] + 1
        while j < len(fl) and (fl[j][2] - seg_start_line) < target:
            j += 1
        if j >= len(fl):
            break
        # 吸附: 在 [j, j+SNAP) 找 tag 与前一函数不同的点
        best = j
        for k in range(j, min(j + SNAP, len(fl))):
            if tag(fl[k][1]) != tag(fl[k - 1][1]):
                best = k
                break
        else:
            # 向前看也行: [max(j-SNAP,prev+1), j) 找转变
            for k in range(j - 1, max(boundaries[-1] + 1, j - SNAP) - 1, -1):
                if tag(fl[k][1]) != tag(fl[k - 1][1]):
                    best = k
                    break
        boundaries.append(best)
        i = best

    # 段 -> (start_addr, dominant tag)
    segs = []
    bidx = boundaries + [len(fl)]
    for s in range(len(boundaries)):
        lo = bidx[s]
        hi = bidx[s + 1]
        from collections import Counter
        c = Counter(tag(fl[k][1]) for k in range(lo, hi))
        dom = c.most_common(1)[0][0]
        segs.append((fl[lo][0], dom, hi - lo))

    print("# asm/all.s 模块拆分边界定义 (generate_split_manifest.py 生成初稿, 可人工微调)")
    print("# 格式: <start_addr_hex><TAB><filename><TAB><description>")
    print("# 每行覆盖 [start, 下一行 start) 连续地址区间。校验: split_all_s.py --check")
    for idx, (addr, dom, nfn) in enumerate(segs):
        fname = "%02d_%s.s" % (idx, dom)
        print("0x%08x\t%s\t%s 区 (%d fn)" % (addr, fname, dom, nfn))


if __name__ == "__main__":
    main()
