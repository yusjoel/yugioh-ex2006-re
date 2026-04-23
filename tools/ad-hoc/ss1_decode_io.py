"""解析 ss1 快照的 IO 寄存器（DISPCNT / BGxCNT），打印活 charblock / 色深 / OBJ mode。

输入：doc/temp/ss1_s{N}_io.bin（96 B），同目录 oam.bin（1 KB）
输出：stdout 文本报告
"""
import pathlib, struct, sys

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
STATES = ["s0", "s1", "s3"]  # s2 视觉重复跳过


def decode_dispcnt(io: bytes):
    d = struct.unpack_from('<H', io, 0)[0]
    mode = d & 0x7
    obj_map_1d = bool(d & 0x40)
    bg_enable = [bool(d & (1 << (8 + i))) for i in range(4)]
    obj_enable = bool(d & 0x1000)
    return dict(mode=mode, obj_map_1d=obj_map_1d, bg_enable=bg_enable, obj_enable=obj_enable, raw=d)


def decode_bgcnt(io: bytes, bg: int):
    # BG0CNT @ 0x08, step 2
    b = struct.unpack_from('<H', io, 0x08 + bg * 2)[0]
    prio = b & 0x3
    char_base = (b >> 2) & 0x3                  # charblock 0..3
    mosaic = bool(b & 0x40)
    color_8bpp = bool(b & 0x80)
    screen_base = (b >> 8) & 0x1F               # screenblock 0..31
    screen_size = (b >> 14) & 0x3
    return dict(prio=prio, char_base=char_base, color_8bpp=color_8bpp,
                screen_base=screen_base, screen_size=screen_size, raw=b)


def obj_char_base(mode: int) -> int:
    # 0x06010000 for BG modes 0-2, 0x06014000 for 3-5
    return 0x06014000 if mode >= 3 else 0x06010000


def report(state: str):
    io = (ROOT / f"doc/temp/ss1_{state}_io.bin").read_bytes()
    oam = (ROOT / f"doc/temp/ss1_{state}_oam.bin").read_bytes()
    d = decode_dispcnt(io)
    print(f"=== state {state} ===")
    print(f"DISPCNT={d['raw']:04X}  mode={d['mode']}  OBJ1D={d['obj_map_1d']}  "
          f"BG={d['bg_enable']}  OBJ={d['obj_enable']}")
    for bg in range(4):
        if d['bg_enable'][bg]:
            c = decode_bgcnt(io, bg)
            char_addr = 0x06000000 + c['char_base'] * 0x4000
            screen_addr = 0x06000000 + c['screen_base'] * 0x800
            bpp = 8 if c['color_8bpp'] else 4
            print(f"  BG{bg}  CNT={c['raw']:04X}  prio={c['prio']}  {bpp}bpp  "
                  f"char=cb{c['char_base']}@{char_addr:08X}  "
                  f"screen=sb{c['screen_base']}@{screen_addr:08X}  "
                  f"size={c['screen_size']}")
    obj_base = obj_char_base(d['mode'])
    print(f"  OBJ    tile_base=0x{obj_base:08X}")

    # OAM 128 entries * 8 B (attr0/1/2 + affine)
    active_sprites = 0
    tile_refs = {}          # (palbank, tile_idx) -> count
    for i in range(128):
        a0, a1, a2 = struct.unpack_from('<HHH', oam, i * 8)
        obj_mode = (a0 >> 8) & 0x3            # 0=normal 1=semi 2=window
        disable = bool(a0 & 0x0200)
        shape = (a0 >> 14) & 0x3
        size_bits = (a1 >> 14) & 0x3
        tile_idx = a2 & 0x3FF
        palbank = (a2 >> 12) & 0xF
        # "visible": not disabled AND coord within screen
        if a0 & 0x0100:                        # rotation/scale bit
            disable = False                   # different flag semantics
        if disable:
            continue
        active_sprites += 1
        tile_refs[(palbank, tile_idx)] = tile_refs.get((palbank, tile_idx), 0) + 1
    print(f"  OAM: {active_sprites} active sprites, {len(tile_refs)} distinct (palbank,tile_idx)")
    # show top-5 palbanks used
    from collections import Counter
    palbank_cnt = Counter()
    for (pb, _), c in tile_refs.items():
        palbank_cnt[pb] += c
    print(f"  palbanks in use: {dict(sorted(palbank_cnt.items()))}")
    # range of tile idx
    idxs = [ti for (_, ti) in tile_refs.keys()]
    if idxs:
        print(f"  tile idx range: {min(idxs)}..{max(idxs)}")
    print()


for s in STATES:
    report(s)
