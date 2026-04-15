"""VRAM diff state1 vs state3 (font localization)."""
import pathlib

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re/doc/temp")
a = (ROOT / "vram_state1.bin").read_bytes()
b = (ROOT / "vram_state3.bin").read_bytes()
assert len(a) == len(b) == 0x18000

# find all differing byte indices
diffs = [i for i in range(len(a)) if a[i] != b[i]]
print(f"total differing bytes: {len(diffs)}")

# merge adjacent diffs (gap <= 64)
GAP = 64
intervals = []
if diffs:
    start = diffs[0]
    prev = diffs[0]
    for i in diffs[1:]:
        if i - prev <= GAP:
            prev = i
        else:
            intervals.append((start, prev))
            start = i
            prev = i
    intervals.append((start, prev))

print(f"{len(intervals)} merged intervals (gap <= {GAP}):")
intervals.sort(key=lambda x: -(x[1] - x[0]))
for s, e in intervals[:20]:
    size = e - s + 1
    vram_s = 0x06000000 + s
    vram_e = 0x06000000 + e
    region = "BG" if vram_s < 0x06010000 else "OBJ"
    print(f"  VRAM 0x{vram_s:08X}-0x{vram_e:08X} size={size:6d} B  [{region}]")
