"""遍历 ss1 VRAM 所有 32B tile，到 ROM (stride 32) 做 exact 匹配，输出每 tile 命中列表。

输入：
  doc/temp/ss1_s{0,1,3}_vram.bin
  roms/2343.gba

输出：
  doc/temp/ss1_tile_hits.csv
    列: state, vram_off, tile_hex_first8, n_hits, rom_offs...
"""
import pathlib, sys, csv

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
STATES = ["s0", "s1", "s3"]

print(f"[*] ROM size = {len(ROM):#x}")

# stride-32 index: rom[i:i+32] -> [rom_offs...]
print("[*] 构建 ROM stride-32 索引...")
rom_idx: dict[bytes, list[int]] = {}
ZERO32 = b"\x00" * 32
for i in range(0, len(ROM) - 31, 32):
    chunk = ROM[i:i + 32]
    if chunk == ZERO32:
        continue
    rom_idx.setdefault(chunk, []).append(i)
print(f"[*] ROM 非零 32B 去重种类 = {len(rom_idx):,}")

# stride-16 补丁索引（少量；用于处理 palette 偏移后 tile 起点非 32 对齐的情况）
# 暂不启用，先看 stride-32 覆盖率

hits_csv = ROOT / "doc/temp/ss1_tile_hits.csv"
f = hits_csv.open("w", newline="", encoding="utf-8")
w = csv.writer(f)
w.writerow(["state", "vram_off", "tile_first8_hex", "tile_last8_hex", "n_hits", "rom_offs_hex"])

summary = {}
for state in STATES:
    vram = (ROOT / f"doc/temp/ss1_{state}_vram.bin").read_bytes()
    matched = 0
    unmatched = 0
    empty = 0
    total = 0
    for vo in range(0, len(vram), 32):
        tile = vram[vo:vo + 32]
        if tile == ZERO32:
            empty += 1
            continue
        total += 1
        offs = rom_idx.get(tile)
        if offs:
            matched += 1
            # 最多记 8 个 ROM 命中，超出以 "+N" 标注
            shown = offs[:8]
            extra = "" if len(offs) <= 8 else f"+{len(offs)-8}"
            w.writerow([
                state, f"0x{vo:05X}", tile[:8].hex(), tile[-8:].hex(),
                len(offs), ";".join(f"0x{o:08X}" for o in shown) + extra,
            ])
        else:
            unmatched += 1
            w.writerow([state, f"0x{vo:05X}", tile[:8].hex(), tile[-8:].hex(), 0, ""])
    summary[state] = dict(total=total, matched=matched, unmatched=unmatched, empty=empty)
    print(f"[{state}] total non-empty={total}  matched={matched}  unmatched={unmatched}  empty={empty}")

f.close()
print(f"[*] 写出: {hits_csv}")
