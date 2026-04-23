"""未知段内 stride-4 扫描：对段内每 4B 对齐 offset，取 32B 作为潜在 tile，
如在 VRAM（非平凡 tile 集）命中即记录。再求连续 +32 的最大运行。

输出：
  doc/temp/ss1_unknown_v2.txt —— 按段列出 matched runs
"""
import pathlib

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

UNKNOWN_SEGMENTS = [
    (0x004C7638, 0x88), (0x01832602, 0x1E51A), (0x01865E20, 0x1680),
    (0x01867560, 0x26510), (0x0188F8D0, 0x6B00), (0x01896730, 0x279A7C),
    (0x01B8FB8C, 0x13CF04), (0x01CCD290, 0x16D0), (0x01CE822C, 0xD6DEE),
    (0x01DFF9D2, 0x31B82), (0x01E31714, 0x275FA), (0x01E5906E, 0x1B8E),
    (0x01E5E618, 0x918), (0x01E5F6CC, 0x1B8), (0x01E5F8EA, 0x16E),
    (0x01E5FD84, 0x1408), (0x01ED49D4, 0x12B62C),
]


def is_trivial(t):
    if len(set(t)) <= 1: return True
    if len(set(t)) == 2:
        flips = sum(1 for i in range(1, len(t)) if t[i] != t[i - 1])
        if flips <= 2: return True
    return False


STATES = ["s0", "s1", "s3"]
vram_tiles: dict[bytes, set[str]] = {}
ZERO32 = b"\x00" * 32
for state in STATES:
    v = (ROOT / f"doc/temp/ss1_{state}_vram.bin").read_bytes()
    for i in range(0, len(v), 32):
        t = v[i:i + 32]
        if t == ZERO32 or is_trivial(t):
            continue
        vram_tiles.setdefault(t, set()).add(f"{state}@0x{i:x}")
print(f"[*] 非平凡 VRAM tile 种类: {len(vram_tiles)}")

out_lines = []
total_run_bytes = 0
for seg_start, seg_size in UNKNOWN_SEGMENTS:
    seg_end = seg_start + seg_size
    # stride-4 扫描段内 4B 对齐 offset
    base = (seg_start + 3) & ~3
    # 收集每个 4B 对齐 offset 处：该 32B tile 是否在 vram_tiles
    pos = []
    for off in range(base, seg_end - 31, 4):
        tile = ROM[off:off + 32]
        if tile in vram_tiles:
            pos.append(off)
    if not pos:
        continue
    # 求连续 +32 run（相邻 pos 差正好 32）
    runs = []
    cur = [pos[0]]
    for p in pos[1:]:
        if p == cur[-1] + 32:
            cur.append(p)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [p]
    if len(cur) >= 2:
        runs.append(cur)

    if runs:
        out_lines.append(f"\n### UNKNOWN segment 0x{seg_start:08X} size 0x{seg_size:X}")
        for run in runs:
            a = run[0]
            b = run[-1] + 32
            n = len(run)
            total_run_bytes += (b - a)
            # 预览 VRAM 引用
            t0 = ROM[a:a + 32]
            refs = sorted(vram_tiles[t0])
            out_lines.append(f"  run 0x{a:08X}-0x{b:08X}  {n:3d} tiles  ({b - a} B)  "
                             f"first_refs={refs[:2]}")
print("\n".join(out_lines))
print(f"\n>>> 合计 runs 字节: {total_run_bytes:,} B")
(ROOT / "doc/temp/ss1_unknown_v2.txt").write_text(
    "\n".join(out_lines) + f"\n\n>>> 合计 runs: {total_run_bytes:,} B\n",
    encoding="utf-8")
