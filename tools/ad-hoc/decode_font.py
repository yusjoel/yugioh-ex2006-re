"""Decode 1bpp 8x8 font glyphs from ROM at 0x09ccca90 and render ASCII samples."""
import pathlib
rom = (pathlib.Path(r"E:/Workspace/yugioh-ex2006-re/roms/2343.gba")).read_bytes()
FONT_ROM = 0x09ccca90 - 0x08000000  # ROM file offset

def glyph(ch):
    off = FONT_ROM + ch * 8
    return rom[off:off+8]

# Display ASCII 32..127 as 8x8 bitmaps. Try MSB-first first.
def render(bytes8, msb_first=True):
    rows = []
    for b in bytes8:
        if msb_first:
            pixels = [(b >> (7-i)) & 1 for i in range(8)]
        else:
            pixels = [(b >> i) & 1 for i in range(8)]
        rows.append(''.join('#' if p else '.' for p in pixels))
    return rows

# Print a few known characters
TEST = [ord(c) for c in "AHWhengScardGraveyard 0123!?"]
for ch in TEST:
    g = glyph(ch)
    print(f"\nchar 0x{ch:02X} '{chr(ch)}' bytes={g.hex()}")
    for r in render(g, msb_first=True):
        print(f"  {r}")
