"""扫每个未知 ROM 段，以 32B 步长检测段内 ROM tile 是否出现于任意 ss1 VRAM 状态。
连续出现的 32B 块 = 一个"被 VRAM 引用的 tile sheet"。

输出：doc/temp/ss1_unknown_scan.txt
- 每个未知段内的匹配段（ROM 起止 + 长度 + 涉及的状态）
"""
import pathlib, struct

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

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

# 构建 VRAM tile 集合（按 32B 取，跨所有状态）
STATES = ["s0", "s1", "s3"]
vram_tiles: dict[bytes, set[str]] = {}
ZERO32 = b"\x00" * 32


def is_trivial(t: bytes) -> bool:
    """过滤单字节重复（实心填充 tile）和只有 2 字节交替的 tile。"""
    if len(set(t)) <= 1:
        return True
    # 只含 2 种字节、且交替 (即 ABABAB...)
    if len(set(t)) == 2:
        # 粗略：只要非零变化点少，基本是纯色/线
        first = t[0]
        flips = sum(1 for i in range(1, len(t)) if t[i] != t[i - 1])
        if flips <= 2:
            return True
    return False


for state in STATES:
    v = (ROOT / f"doc/temp/ss1_{state}_vram.bin").read_bytes()
    for i in range(0, len(v), 32):
        t = v[i:i + 32]
        if t == ZERO32 or is_trivial(t):
            continue
        vram_tiles.setdefault(t, set()).add(f"{state}@{i:#x}")

print(f"[*] VRAM tile 种类（非零, 32B）: {len(vram_tiles)}")

out_lines = []
total_matched_bytes = 0
for seg_start, seg_size in UNKNOWN_SEGMENTS:
    out_lines.append(f"\n### UNKNOWN segment 0x{seg_start:08X} size 0x{seg_size:X} ({seg_size:,} B)")
    # 段内 32B 对齐位置（考虑起点偏移）
    # 32B 对齐起点 ≥ seg_start
    base = (seg_start + 31) & ~31
    end = seg_start + seg_size
    # 收集段内所有对齐到 32B 的 tile 是否在 VRAM
    marks = []             # list of (rom_off, is_match)
    for off in range(base, end - 31, 32):
        tile = ROM[off:off + 32]
        if tile in vram_tiles:
            marks.append((off, True, vram_tiles[tile]))
        else:
            marks.append((off, False, None))

    # 求最长连续 True 段（允许至多 K=0 个 False gap）
    clusters = []
    i = 0
    while i < len(marks):
        if marks[i][1]:
            j = i
            while j + 1 < len(marks) and marks[j + 1][1]:
                j += 1
            # cluster from marks[i] to marks[j]
            n = j - i + 1
            if n >= 1:
                clusters.append((marks[i][0], marks[j][0] + 32, n,
                                [m for _, _, m in marks[i:j+1] if m]))
            i = j + 1
        else:
            i += 1
    # 汇报：至少 2 tile 的簇全列；1 tile 的簇只统计
    single_cnt = sum(1 for c in clusters if c[2] == 1)
    multi = [c for c in clusters if c[2] >= 2]
    out_lines.append(f"  内部 32B 对齐块 {(end - base) // 32} 个；其中 VRAM 命中 {sum(c[2] for c in clusters)}")
    out_lines.append(f"    多 tile 簇: {len(multi)}（含 {sum(c[2] for c in multi)} tile）；单 tile 散点: {single_cnt}")
    for a, b, n, hits in multi:
        total_matched_bytes += (b - a)
        # 采样 3 个状态引用
        hit_preview = sorted(set().union(*hits[:3]))[:5]
        out_lines.append(f"    cluster 0x{a:08X}-0x{b:08X}  {n:3d} tiles  "
                         f"({b - a} B)  e.g. {hit_preview}")

out_lines.append(f"\n### 合计多-tile 簇覆盖未知段字节数: {total_matched_bytes:,} B")

print("\n".join(out_lines))
(ROOT / "doc/temp/ss1_unknown_scan.txt").write_text("\n".join(out_lines), encoding="utf-8")
