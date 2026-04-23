"""对每个非平凡 VRAM tile 在 ROM 里做 stride-1 exact 搜索（bytes.find 循环）。
结果归属到未知段。
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

def in_unknown(off):
    for s, sz in UNKNOWN_SEGMENTS:
        if s <= off < s + sz:
            return (s, sz)
    return None


def is_trivial(t):
    if len(set(t)) <= 1: return True
    if len(set(t)) == 2:
        flips = sum(1 for i in range(1, len(t)) if t[i] != t[i-1])
        if flips <= 2: return True
    return False


# 汇总所有非平凡 VRAM tile
STATES = ["s0", "s1", "s3"]
vram_tiles = {}                           # tile_bytes -> set of state@off
ZERO32 = b"\x00" * 32
for state in STATES:
    v = (ROOT / f"doc/temp/ss1_{state}_vram.bin").read_bytes()
    for i in range(0, len(v), 32):
        t = v[i:i+32]
        if t == ZERO32 or is_trivial(t): continue
        vram_tiles.setdefault(t, set()).add(f"{state}@0x{i:x}")
print(f"[*] 非平凡 VRAM tile 种类: {len(vram_tiles)}")

# 针对每个 tile，在 ROM 里做 stride-1 搜索，最多 5 次
hits_in_unknown = []
for tile, refs in vram_tiles.items():
    off = 0
    all_hits = []
    while len(all_hits) < 5:
        i = ROM.find(tile, off)
        if i < 0: break
        all_hits.append(i)
        off = i + 1
    unknown_matches = [(h, in_unknown(h)) for h in all_hits if in_unknown(h)]
    if unknown_matches:
        hits_in_unknown.append((tile, refs, all_hits, unknown_matches))

print(f"\n[*] 非平凡 tile 在未知段有 stride-1 匹配的: {len(hits_in_unknown)}")
for tile, refs, all_hits, umatches in hits_in_unknown[:30]:
    print(f"  tile {tile[:8].hex()}... refs={sorted(refs)[:2]} "
          f"all_hits={[hex(h) for h in all_hits]} "
          f"unknown={[(hex(o), hex(seg[0])) for o, seg in umatches]}")
