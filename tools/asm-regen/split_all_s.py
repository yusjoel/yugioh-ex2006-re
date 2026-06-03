#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把单体反汇编流拆成 asm/*.s 多模块文件（按 split_manifest.tsv 定义的连续地址区间）。

设计要点（见 doc/dev/methodology/build-pipeline.md §七）:
  - manifest 以【函数起始地址】为 key（不是行号）-> 再生成后只要函数边界没移动就能重套。
  - 每个输出文件 = 一段连续 [start, next_start) 地址区间（≈ 原编译单元）。
    byte-identical 由「按地址序 .include 等价于文本拼接」保证。
  - 切割点取在函数 plate 注释块之前（向上吞掉 label + 连续以 @ 开头的注释行），
    使 plate 注释跟随它所属的函数。
  - 每个非首文件开头注入 3 行 header（@ ==== 名 ====, @ 描述, 当前 mode）。mode 指令零
    字节，纯为可读 + 可独立汇编；正确性本由 one-assembly-unit 的状态延续保证。

规范流（canonical stream）来源，按优先级:
  1. asm/all.s 存在（Ghidra 再生成 + inject_modes 产出的单体）-> 直接用
  2. 否则从已入库的 asm/*.s 拆分文件【反向合并】（剥掉注入 header）重建
  => all.s 删除后，阶段 B「改 manifest 重切」仍可工作，无需保留 all.s。

用法:
  python tools/asm-regen/split_all_s.py            # 拆分（自动选规范流来源）
  python tools/asm-regen/split_all_s.py --check     # 只校验 manifest 边界命中
  python tools/asm-regen/split_all_s.py --merge OUT # 反向合并 -> 写单体到 OUT（如 asm/all.s）
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALL_S = os.path.join(ROOT, "asm", "all.s")
MANIFEST = os.path.join(ROOT, "tools", "asm-regen", "split_manifest.tsv")
OUT_DIR = os.path.join(ROOT, "asm")
INCLUDES = os.path.join(OUT_DIR, "includes.inc")
INC_REL = "asm"  # .include 前缀

LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:\s*$")
COMMENT_RE = re.compile(r"^\s*@")
MODE_RE = re.compile(r"^\.(thumb|arm)\s*$")
ADDR_RE = re.compile(r"@\s*([0-9a-fA-F]{8})\b")
MARKER_RE = re.compile(r"^@ ==== .+ ====$")
INC_LINE_RE = re.compile(r'^\s*\.include\s+"%s/(.+?)"\s*$' % re.escape(INC_REL))

INC_BANNER = ["@ 由 tools/asm-regen/split_all_s.py 自动生成，勿手改。",
              "@ 模块边界定义见 tools/asm-regen/split_manifest.tsv。", ""]


def detect_nl(text):
    return "\r\n" if "\r\n" in text[:65536] else "\n"


def load_manifest(path):
    entries = []
    with open(path, encoding="utf-8") as f:
        for ln, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                sys.exit("manifest 第 %d 行字段不足 (需 addr<TAB>filename[<TAB>desc]): %r" % (ln, line))
            addr = int(parts[0].strip(), 16)
            fname = parts[1].strip()
            desc = parts[2].strip() if len(parts) >= 3 else ""
            entries.append((addr, fname, desc))
    return entries


def strip_injected_header(lines):
    """剥掉一个非首拆分文件开头注入的 header（marker + desc? + mode）。返回正文 lines。"""
    if not lines or not MARKER_RE.match(lines[0]):
        return lines  # 没有注入 header（可能是首文件或手工流）
    i = 1
    while i < len(lines) and COMMENT_RE.match(lines[i]) and not MARKER_RE.match(lines[i]):
        i += 1  # 跳过 desc 注释行
    if i < len(lines) and MODE_RE.match(lines[i]):
        i += 1  # 跳过注入的 mode 行
    return lines[i:]


def read_canonical(all_path, out_dir, includes_path):
    """返回 (lines, nl)。优先读 all.s；否则从拆分文件反向合并。"""
    if os.path.exists(all_path):
        with open(all_path, encoding="utf-8", newline="") as f:
            text = f.read()
        nl = detect_nl(text)
        lines = text.split(nl)
        if lines and lines[-1] == "":
            lines = lines[:-1]
        print("[规范流] 读 asm/all.s (%d 行)" % len(lines))
        return lines, nl
    # 反向合并
    if not os.path.exists(includes_path):
        sys.exit("asm/all.s 不存在且 %s 也不存在，无法重建规范流" % os.path.relpath(includes_path, ROOT))
    with open(includes_path, encoding="utf-8", newline="") as f:
        inc_text = f.read()
    nl = detect_nl(inc_text)
    order = []
    for line in inc_text.split(nl):
        m = INC_LINE_RE.match(line)
        if m:
            order.append(m.group(1))
    if not order:
        sys.exit("includes.inc 中没有解析到任何 .include 行")
    merged = []
    for idx, fname in enumerate(order):
        p = os.path.join(out_dir, fname)
        with open(p, encoding="utf-8", newline="") as f:
            sub = f.read().split(nl)
        if sub and sub[-1] == "":
            sub = sub[:-1]
        if idx > 0:
            sub = strip_injected_header(sub)
        merged.extend(sub)
    print("[规范流] 反向合并 %d 个拆分文件 -> %d 行" % (len(order), len(merged)))
    return merged, nl


def index_addr_lines(lines):
    idx = {}
    for i, line in enumerate(lines):
        m = ADDR_RE.search(line)
        if m:
            a = int(m.group(1), 16)
            if a not in idx:
                idx[a] = i
    return idx


def find_cut(lines, addr, addr_idx):
    if addr not in addr_idx:
        return None
    i = addr_idx[addr]
    cut = i
    while cut - 1 >= 0:
        prev = lines[cut - 1]
        if LABEL_RE.match(prev) or COMMENT_RE.match(prev):
            cut -= 1
        else:
            break
    return cut


def mode_prefix_at(lines, upto):
    mode = ".arm"
    for line in lines[:upto]:
        if MODE_RE.match(line):
            mode = "." + MODE_RE.match(line).group(1)
    return mode


def compute_cuts(lines, entries):
    addr_idx = index_addr_lines(lines)
    cuts = []
    missing = []
    for addr, fname, desc in entries:
        c = find_cut(lines, addr, addr_idx)
        if c is None:
            missing.append((addr, fname))
        cuts.append((c, addr, fname, desc))
    if missing:
        print("以下 manifest 地址在规范流中找不到对应指令行:", file=sys.stderr)
        for addr, fname in missing:
            print("  0x%08x  %s" % (addr, fname), file=sys.stderr)
        sys.exit(1)
    for k in range(1, len(cuts)):
        if cuts[k][0] <= cuts[k - 1][0]:
            sys.exit("manifest 顺序错误: %s (行 %d) 不在 %s (行 %d) 之后" %
                     (cuts[k][2], cuts[k][0], cuts[k - 1][2], cuts[k - 1][0]))
    return cuts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", default=ALL_S)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--check", action="store_true", help="只校验边界命中，不写文件")
    ap.add_argument("--merge", metavar="OUT", help="反向合并拆分文件写单体到 OUT，不拆分")
    args = ap.parse_args()

    lines, nl = read_canonical(args.all, args.out, INCLUDES)

    if args.merge:
        with open(args.merge, "w", encoding="utf-8", newline="") as f:
            f.write(nl.join(lines))
            f.write(nl)
        print("[写] %s (%d 行)" % (args.merge, len(lines)))
        return

    entries = load_manifest(args.manifest)
    if not entries:
        sys.exit("manifest 为空")
    cuts = compute_cuts(lines, entries)

    if args.check:
        print("manifest OK: %d 段, 全部边界命中" % len(cuts))
        for c, addr, fname, desc in cuts:
            print("  行 %7d  0x%08x  %s" % (c + 1, addr, fname))
        return

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    inc_lines = list(INC_BANNER)
    n = len(cuts)
    for i in range(n):
        start = cuts[i][0]
        end = cuts[i + 1][0] if i + 1 < n else len(lines)
        fname = cuts[i][2]
        desc = cuts[i][3]
        body = lines[start:end]
        out_lines = []
        if i == 0:
            if start > 0:
                body = lines[0:end]  # preamble 并入首文件
        else:
            out_lines.append("@ ==== %s ====" % fname)
            if desc:
                out_lines.append("@ %s" % desc)
            out_lines.append(mode_prefix_at(lines, start))
        out_lines.extend(body)
        with open(os.path.join(args.out, fname), "w", encoding="utf-8", newline="") as f:
            f.write(nl.join(out_lines))
            f.write(nl)
        inc_lines.append('\t.include "%s/%s"' % (INC_REL, fname))
        print("[写] asm/%-32s 行 %7d..%-7d (%d 行)" % (fname, start + 1, end, end - start))

    with open(INCLUDES, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(inc_lines))
        f.write(nl)
    print("[写] %s (%d 个 .include)" % (os.path.relpath(INCLUDES, ROOT), n))


if __name__ == "__main__":
    main()
