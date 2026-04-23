"""读 ss1_tile_hits.csv，按"canonical rom_off"聚类，过滤出落在未知段的图形簇。

规则：
- 每 tile 选一个 "canonical ROM offset"：优先匹配已知图形段里的，
  没命中已知段则取最小 rom_off。
- 相邻 tile 若 `canon_off[i+1] == canon_off[i] + 32` 归一簇（簇内 tile 必然连续来自同一 ROM 段）。
- 与 data-analysis-coverage.md 的 17 个未分析段相交：列出落在未知段的 cluster。
"""
import pathlib, csv, bisect, collections

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")

# 未分析段 (start, size) —— 从 data-analysis-coverage.md 手抄
UNKNOWN_SEGMENTS = [
    (0x004C7638, 0x88),
    (0x01832602, 0x1E51A),
    (0x01865E20, 0x1680),
    (0x01867560, 0x26510),
    (0x0188F8D0, 0x6B00),
    (0x01896730, 0x279A7C),
    (0x01B8FB8C, 0x13CF04),
    (0x01CCD290, 0x16D0),
    (0x01CE822C, 0xD6DEE),
    (0x01DFF9D2, 0x31B82),
    (0x01E31714, 0x275FA),
    (0x01E5906E, 0x1B8E),
    (0x01E5E618, 0x918),
    (0x01E5F6CC, 0x1B8),
    (0x01E5F8EA, 0x16E),
    (0x01E5FD84, 0x1408),
    (0x01ED49D4, 0x12B62C),
]
UNKNOWN_SEGMENTS.sort()
UNKNOWN_STARTS = [s for s, _ in UNKNOWN_SEGMENTS]


def in_unknown_segment(off: int) -> tuple[int, int] | None:
    """返回所属未知段的 (start, size) 或 None。"""
    i = bisect.bisect_right(UNKNOWN_STARTS, off) - 1
    if i < 0:
        return None
    s, sz = UNKNOWN_SEGMENTS[i]
    if s <= off < s + sz:
        return (s, sz)
    return None


def pick_canonical(offs: list[int]) -> int:
    """从匹配列表中挑一个 canonical offset：优先落在未知段的，其次最小。"""
    for o in offs:
        if in_unknown_segment(o) is not None:
            return o
    return min(offs)


csv_path = ROOT / "doc/temp/ss1_tile_hits.csv"
rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))

# 按 state 分组
by_state = collections.defaultdict(list)      # state -> [(vram_off, canon_off, n_hits, first8)]
for r in rows:
    if int(r["n_hits"]) == 0:
        continue
    offs_str = r["rom_offs_hex"].split(";")
    offs = []
    for o in offs_str:
        o = o.split("+")[0]
        if o:
            offs.append(int(o, 16))
    canon = pick_canonical(offs)
    by_state[r["state"]].append((
        int(r["vram_off"], 16), canon, int(r["n_hits"]), r["tile_first8_hex"], len(offs)))

# 对每 state 聚类：按 canon_off 排序，相邻 +32 归簇
report_lines = []
clusters_unknown_all = []
for state, tiles in by_state.items():
    tiles.sort(key=lambda t: t[1])
    clusters = []
    current = [tiles[0]]
    for t in tiles[1:]:
        prev_canon = current[-1][1]
        if t[1] == prev_canon + 32:
            current.append(t)
        else:
            clusters.append(current)
            current = [t]
    clusters.append(current)

    report_lines.append(f"\n=== state {state}: {len(clusters)} clusters ===")
    for cl in clusters:
        first_canon = cl[0][1]
        last_canon = cl[-1][1] + 32
        seg = in_unknown_segment(first_canon)
        unknown_tag = ""
        if seg:
            # 整簇都落在未知段?
            all_in = all(in_unknown_segment(t[1]) == seg for t in cl)
            unknown_tag = f"  [UNKNOWN seg @0x{seg[0]:08X}, size 0x{seg[1]:X}]" if all_in else "  [partial UNKNOWN]"
            if all_in:
                clusters_unknown_all.append((state, first_canon, last_canon, cl))
        if len(cl) >= 4 or seg is not None:         # 簇 >= 4 tile 或落未知段才打印
            vram_range = f"VRAM 0x{cl[0][0]:05X}-0x{cl[-1][0]:05X}"
            n_hit_min = min(t[2] for t in cl)
            n_hit_max = max(t[2] for t in cl)
            report_lines.append(
                f"  cluster ROM 0x{first_canon:08X}-0x{last_canon:08X}  "
                f"{len(cl):3d} tiles  {vram_range}  hits/tile={n_hit_min}..{n_hit_max}"
                f"{unknown_tag}"
            )

out = ROOT / "doc/temp/ss1_cluster_report.txt"
out.write_text("\n".join(report_lines) + "\n\n=== clusters_in_unknown ===\n" +
               "\n".join(f"{s} 0x{a:08X}-0x{b:08X} {len(cl)} tiles" for s, a, b, cl in clusters_unknown_all),
               encoding="utf-8")
print("".join(report_lines[:80]))
print(f"\n... full report: {out}")
print(f"\nclusters fully in UNKNOWN segments: {len(clusters_unknown_all)}")
for s, a, b, cl in clusters_unknown_all:
    print(f"  [{s}] ROM 0x{a:08X}-0x{b:08X}  {len(cl):3d} tiles")
