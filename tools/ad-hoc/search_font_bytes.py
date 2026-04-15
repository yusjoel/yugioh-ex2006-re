"""Search ROM for exact byte pattern of rendered sprite tiles."""
import pathlib

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
vram = (ROOT / "doc/temp/vram_state3.bin").read_bytes()
rom = (ROOT / "roms/2343.gba").read_bytes()

def find_all(data, needle, max_hits=10):
    idx = 0
    out = []
    while True:
        i = data.find(needle, idx)
        if i < 0: break
        out.append(i)
        idx = i + 1
        if len(out) >= max_hits: break
    return out

BASE = 0x10000  # sprite tile VRAM offset
# search each tile's 32 bytes in ROM (raw)
for t in [1, 2, 3, 4, 6, 10, 14, 20]:
    off = BASE + t * 32
    tile = vram[off:off+32]
    if tile == b'\x00' * 32:
        print(f"tile {t}: empty")
        continue
    hits = find_all(rom, tile, 5)
    print(f"tile {t} @0x0601{t*32:04X} first8={tile[:8].hex()}: {len(hits)} ROM hits {[hex(0x08000000+h) for h in hits]}")

# also try sub-strings (longer unique runs)
print("\n-- sub-pattern search (first non-empty row of each tile) --")
for t in [2, 3, 4, 6]:
    off = BASE + t * 32
    tile = vram[off:off+32]
    # find rows with data
    for r in range(8):
        row = tile[r*4:r*4+4]
        if row != b'\x00\x00\x00\x00':
            # search for this 4-byte row (too short likely) so also take 8 bytes window
            window = tile[r*4:r*4+8] if r < 7 else tile[r*4:r*4+4]
            hits = find_all(rom, window, 3)
            print(f"tile {t} row {r} bytes={window.hex()}: {len(hits)} hits")
            break
