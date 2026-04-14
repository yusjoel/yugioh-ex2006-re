"""
批量导出《游戏王 EX2006》(BY6E, roms/2343.gba) 全部卡牌详情页大卡图为 PNG。

对应 PLAN.md P1-5。依据 doc/dev/p1-phase-b2-findings.md 的逆向结论：
  - tile 基址 0x08510640，ROM 文件偏移 0x00510640
  - 每张卡占 4800 字节，布局为 10×10 tiles × 8×8 像素 = 80×80
  - 6bpp 自写压缩（每 6 ROM bytes → 8 像素）
  - 索引表 0x095B5C00（ROM 0x015B5C00），每条 u16 LE
  - 字节偏移 = (card_id × 2 + flag) × 2；BY6E 的 flag=1
  - 调色板 0x084C76C0（ROM 0x004C76C0），256 色 BGR555
  - 解码后 6bit 索引 + 0x10 得到最终调色板索引

用法：
    python tools/rom-export/export_card_images.py [--flag 1] [--gray]

输出目录：graphics/card-images/（已 .gitignore）
文件命名：card_{card_id:04d}_tb{tile_block:04d}.png
      另：每个 tile_block 唯一数据只解码一次，异画卡共享同一 tile_block
      的情况下，会产出多个文件名指向同一图像（用软拷贝策略：第二个及以后
      直接跳过，在清单 manifest.csv 记录共享关系）。
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

from PIL import Image

ROM_PATH = Path("roms/2343.gba")
OUT_DIR = Path("graphics/card-images")
STATS_BASE_ROM = 0x018169B6   # card-stats.s 起始 ROM 偏移
STATS_STRIDE = 22             # 每条记录字节数
EN_NAMES_BASE_ROM = 0x015BB5AC  # 欧洲卡名表 ROM 起始（每卡 5 个 CP1252 字符串）

# ROM 中三段原始数据的精确范围（byte-identical 要求）
PALETTES_ROM_START = 0x004C76C0
PALETTES_ROM_END   = 0x00510440  # 2331 × 128 B = 0x48D80
TILES_ROM_START    = 0x00510640
TILES_ROM_END      = 0x00FBC080  # 2331 × 4800 B = 0xAABA40
INDEX_ROM_START    = 0x015B5C00
INDEX_ROM_END      = 0x015B94CC  # 7270 × u16 = 0x38CC（6846 实条目 + 424 FFFF 填充）

BLOB_DIR = Path("graphics/card-images-rom")       # bin 根目录（已 .gitignore graphics/）
PAL_BLOB_DIR = BLOB_DIR / "palettes"              # 2331 × 128 B
TILE_BLOB_DIR = BLOB_DIR / "tiles"                # 2331 × 4800 B
INDEX_S_PATH = Path("data/card-image-index.s")    # 索引表 .s（显式 .hword）
PAL_S_PATH = Path("data/card-image-palettes.s")   # 调色板 incbin 列表
TILE_S_PATH = Path("data/card-image-tiles.s")     # tile incbin 列表

NUM_TILE_BLOCKS = 2331                             # tile_block 0..2330 全覆盖
PAL_ENTRY_SIZE = 128                               # 64 × BGR555
TILE_ENTRY_SIZE = 4800                             # 与 STRIDE 同值（6bpp，10×10 tiles）

# 常量（均来自 findings）
TILE_BASE_ROM = 0x00510640
INDEX_TABLE_ROM = 0x015B5C00
PALETTE_BASE_ROM = 0x004C76C0  # 每张卡 64 色 (128 bytes) 调色板基址
PALETTE_STRIDE = 128           # 每张卡 64 × BGR555 = 128 字节
STRIDE = 4800                  # 每张卡字节数
NUM_ITER = 800                 # 第一循环次数，每次 6 bytes → 8 像素
PAL_OFFSET = 0x10              # 第二循环：raw_6bit + 0x10（此处用于游戏内 256 色调色板的偏移；6bit+0x10 映射到卡图自身 64 色调色板的 0x10..0x4F 区间，我们用 tile_block 级独立调色板时直接用 raw_6bit 索引）
TILE_COLS = 10
TILE_ROWS = 10
TILE_PIX = 8

# 索引表扫描：最大 card_id 上限（findings 实测表末在 index 6845 处，
# 即 card_id 3422/flag=1。取 3423 为硬上限；超过会读到表尾无关字节）
MAX_CARD_ID_SCAN = 3423


def load_palette(rom: bytes, tile_block: int) -> list[tuple[int, int, int]]:
    """读取指定 tile_block 的 64 色调色板（BGR555 → RGB888）。

    假设：每张卡独立 64 色调色板存于 0x4C76C0 起，stride 128 bytes。
    游戏运行时 FUN_080ee010 会将其拷入 VRAM BG palette[0x10..0x4F]。
    解码后 raw_6bit 直接索引本 64 色表。
    """
    pal_off = PALETTE_BASE_ROM + tile_block * PALETTE_STRIDE
    pal_raw = rom[pal_off:pal_off + PALETTE_STRIDE]
    palette: list[tuple[int, int, int]] = []
    for i in range(64):
        v = pal_raw[i * 2] | (pal_raw[i * 2 + 1] << 8)
        v &= 0x7FFF  # 忽略 bit15
        r = (v & 0x1F) << 3
        g = ((v >> 5) & 0x1F) << 3
        b = ((v >> 10) & 0x1F) << 3
        palette.append((r, g, b))
    return palette


def card_id_to_slot(rom: bytes, card_id: int) -> int:
    """从 card-stats.s 取第 card_id 条记录的 slot_id（+2 偏移 u16 LE）。"""
    off = STATS_BASE_ROM + card_id * STATS_STRIDE + 2
    return rom[off] | (rom[off + 1] << 8)


def build_slot_to_en_name(_rom: bytes) -> dict[int, str]:
    """解析 data/card-names.s 的 `card_name_XXXX:  @ <EN>  (pw ...)` 标签行。
    比按字节扫描可靠得多（tools/rom-export/export_card_data.py 生成时已按 slot 对齐）。
    """
    import re
    result: dict[int, str] = {}
    path = Path("data/card-names.s")
    if not path.exists():
        return result
    pat = re.compile(r"^card_name_([0-9A-Fa-f]{4}):\s*@\s*(.+?)\s*(?:\(pw\s+\d+\))?\s*$")
    with path.open("r", encoding="cp1252", errors="replace") as fp:
        for line in fp:
            m = pat.match(line.rstrip("\r\n"))
            if m:
                slot = int(m.group(1), 16)
                name = m.group(2).strip()
                result[slot] = name
    return result


def sanitize(s: str) -> str:
    keep = []
    for ch in s:
        if ch.isalnum() or ch in "-_":
            keep.append(ch)
        elif ch == " ":
            keep.append("_")
    return "".join(keep)[:40]


def scan_index_table(rom: bytes, flag: int) -> list[tuple[int, int]]:
    """扫描索引表，返回 [(card_id, tile_block), ...]（仅非 FFFF 项）。"""
    entries: list[tuple[int, int]] = []
    for card_id in range(MAX_CARD_ID_SCAN):
        byte_off = (card_id * 2 + flag) * 2
        off = INDEX_TABLE_ROM + byte_off
        tb = rom[off] | (rom[off + 1] << 8)
        if tb != 0xFFFF:
            entries.append((card_id, tb))
    return entries


def decode_6bpp(rom_slice: bytes) -> bytes:
    """把 4800 bytes 6bpp 数据解为 6400 个 6bit 索引值（0..63）。"""
    out = bytearray(NUM_ITER * 8)
    for i in range(NUM_ITER):
        off = i * 6
        W0, W1, W2 = struct.unpack_from("<HHH", rom_slice, off)
        out[i * 8 + 0] = W0 & 0x3F
        out[i * 8 + 1] = (W0 >> 6) & 0x3F
        out[i * 8 + 2] = ((W0 >> 12) & 0xF) | ((W1 & 0x3) << 4)
        out[i * 8 + 3] = (W1 >> 2) & 0x3F
        out[i * 8 + 4] = (W1 >> 8) & 0x3F
        out[i * 8 + 5] = ((W1 >> 14) & 0x3) | ((W2 & 0xF) << 2)
        out[i * 8 + 6] = (W2 >> 4) & 0x3F
        out[i * 8 + 7] = (W2 >> 10) & 0x3F
    return bytes(out)


def arrange_tiles(pixels_6bit: bytes) -> bytes:
    """把按 tile 顺序存储的 6400 像素重排为 80×80 行优先图。"""
    W = TILE_COLS * TILE_PIX
    H = TILE_ROWS * TILE_PIX
    out = bytearray(W * H)
    for tile_idx in range(TILE_COLS * TILE_ROWS):
        tx = tile_idx % TILE_COLS
        ty = tile_idx // TILE_COLS
        base_src = tile_idx * 64
        base_dst_y = ty * TILE_PIX
        base_dst_x = tx * TILE_PIX
        for py in range(TILE_PIX):
            src_row = base_src + py * TILE_PIX
            dst_row = (base_dst_y + py) * W + base_dst_x
            out[dst_row:dst_row + TILE_PIX] = pixels_6bit[src_row:src_row + TILE_PIX]
    return bytes(out)


def render_png(pixels_6bit: bytes, palette: list[tuple[int, int, int]], gray: bool) -> Image.Image:
    """6bit → RGB PNG（彩色用共享调色板，灰度用 ×4 放大）。"""
    W = TILE_COLS * TILE_PIX
    H = TILE_ROWS * TILE_PIX
    if gray:
        img = Image.frombytes("L", (W, H), bytes(p << 2 for p in pixels_6bit))
        return img
    # 彩色：raw_6bit 直接索引 64 色卡图专属调色板
    rgb = bytearray(W * H * 3)
    for i, p in enumerate(pixels_6bit):
        r, g, b = palette[p & 0x3F]
        rgb[i * 3] = r
        rgb[i * 3 + 1] = g
        rgb[i * 3 + 2] = b
    return Image.frombytes("RGB", (W, H), bytes(rgb))


def read_tb(rom: bytes, card_id: int, flag: int) -> int | None:
    """索引表读取；FFFF 返回 None。"""
    off = 0x015B5C00 + (card_id * 2 + flag) * 2
    v = rom[off] | (rom[off + 1] << 8)
    return None if v == 0xFFFF else v


def decode_and_arrange(rom: bytes, tb: int) -> bytes:
    src = TILE_BASE_ROM + tb * STRIDE
    if src + STRIDE > len(rom):
        raise ValueError(f"tile_block {tb} src=0x{src:X} 超出 ROM")
    return arrange_tiles(decode_6bpp(rom[src:src + STRIDE]))


def dump_rom_blobs(rom: bytes) -> None:
    """按 tile_block 拆分导出 2331 × palette + 2331 × tile 为独立 bin。

    同时生成 data/card-image-palettes.s 和 data/card-image-tiles.s 两个
    包装 .s，顺序 .incbin 全部小 bin 文件（asm/all.s 用 .include 引用）。
    """
    PAL_BLOB_DIR.mkdir(parents=True, exist_ok=True)
    TILE_BLOB_DIR.mkdir(parents=True, exist_ok=True)

    for tb in range(NUM_TILE_BLOCKS):
        pal_off = PALETTES_ROM_START + tb * PAL_ENTRY_SIZE
        tile_off = TILES_ROM_START + tb * TILE_ENTRY_SIZE
        (PAL_BLOB_DIR / f"tb{tb:04d}.bin").write_bytes(
            rom[pal_off:pal_off + PAL_ENTRY_SIZE])
        (TILE_BLOB_DIR / f"tb{tb:04d}.bin").write_bytes(
            rom[tile_off:tile_off + TILE_ENTRY_SIZE])

    # 生成 palettes.s
    pal_lines = [
        "@ 卡牌大图调色板序列（由 tools/rom-export/export_card_images.py 生成）",
        f"@ ROM 范围: 0x{PALETTES_ROM_START:X} - 0x{PALETTES_ROM_END:X}  "
        f"({NUM_TILE_BLOCKS} × {PAL_ENTRY_SIZE} B = {NUM_TILE_BLOCKS * PAL_ENTRY_SIZE} B)",
        "@ 每 tile_block 一段 64 色 BGR555 调色板。",
        "",
    ]
    for tb in range(NUM_TILE_BLOCKS):
        pal_lines.append(
            f'    .incbin "graphics/card-images-rom/palettes/tb{tb:04d}.bin"')
    PAL_S_PATH.write_text("\n".join(pal_lines) + "\n", encoding="utf-8")

    # 生成 tiles.s
    tile_lines = [
        "@ 卡牌大图 tile 数据序列（由 tools/rom-export/export_card_images.py 生成）",
        f"@ ROM 范围: 0x{TILES_ROM_START:X} - 0x{TILES_ROM_END:X}  "
        f"({NUM_TILE_BLOCKS} × {TILE_ENTRY_SIZE} B = {NUM_TILE_BLOCKS * TILE_ENTRY_SIZE} B)",
        "@ 每 tile_block 一张 80×80 6bpp 图（10×10 tiles × 8×8，4800 B）。",
        "",
    ]
    for tb in range(NUM_TILE_BLOCKS):
        tile_lines.append(
            f'    .incbin "graphics/card-images-rom/tiles/tb{tb:04d}.bin"')
    TILE_S_PATH.write_text("\n".join(tile_lines) + "\n", encoding="utf-8")

    print(f"写入 {PAL_BLOB_DIR}/ 下 {NUM_TILE_BLOCKS} 个 tb*.bin"
          f" ({NUM_TILE_BLOCKS * PAL_ENTRY_SIZE} B 总计)")
    print(f"写入 {TILE_BLOB_DIR}/ 下 {NUM_TILE_BLOCKS} 个 tb*.bin"
          f" ({NUM_TILE_BLOCKS * TILE_ENTRY_SIZE} B 总计)")
    print(f"写入 {PAL_S_PATH} ({NUM_TILE_BLOCKS} 条 incbin)")
    print(f"写入 {TILE_S_PATH} ({NUM_TILE_BLOCKS} 条 incbin)")


def write_index_source(rom: bytes) -> None:
    """生成 data/card-image-index.s —— 显式 .hword 配带注释（card_id/slot/卡名）。"""
    slot_to_name = build_slot_to_en_name(rom)
    import struct as _struct

    # 读取原始 ROM 索引表
    raw = rom[INDEX_ROM_START:INDEX_ROM_END]
    total_u16 = len(raw) // 2
    vals = _struct.unpack(f"<{total_u16}H", raw)
    # entries[i] 对应 (card_id, flag) where i = card_id*2 + flag
    # 前 6846 条为有效数据（其中仍有 FFFF 占位），后 424 条全部 FFFF
    n_real = 6846  # 6846 = 3423 × 2（card_id 0..3422，每卡 flag=0/1 两条）
    n_pad = total_u16 - n_real  # 424

    out_lines = [
        "@ 卡牌大图索引表（由 tools/rom-export/export_card_images.py 自动生成）",
        f"@ ROM 范围: 0x{INDEX_ROM_START:X} - 0x{INDEX_ROM_END:X}  "
        f"({INDEX_ROM_END - INDEX_ROM_START} B = {total_u16} × u16)",
        "@",
        "@ 结构：每个 card_id 占 2 条 u16（flag=0 OCG / flag=1 TCG），",
        "@ 值为 tile_block（=> 大图 ROM 偏移 = 0x00510640 + tile_block × 4800；",
        "@ 调色板 ROM 偏移 = 0x004C76C0 + tile_block × 128）。",
        "@ 0xFFFF 表示该 card_id 在此 flag 下无大图。",
        "@ card_id 是 data/card-stats.s 的 0-indexed 数组下标；1..2080 为正式卡，",
        "@ 2081..2097 为 Token，0 为占位记录，2098+ 为未使用/表 B 数据。",
        "",
        "    .section .rodata",
        "    .balign 2",
        "    .global card_image_index",
        "card_image_index:",
        "",
    ]

    for card_id in range(n_real // 2):  # 0..3422
        tb0 = vals[card_id * 2]
        tb1 = vals[card_id * 2 + 1]

        # 生成一行 .hword
        def fmt(v: int) -> str:
            return "0xFFFF" if v == 0xFFFF else f"0x{v:04X}"

        # 注释
        slot = card_id_to_slot(rom, card_id) if card_id < 5170 else 0
        name = slot_to_name.get(slot, "") if slot else ""
        name_part = f" {name}" if name else ""
        c_note = ""
        if card_id == 0:
            c_note = "  @ [占位] "
        elif 1 <= card_id <= 2080:
            c_note = f"  @ [正式卡{card_id:04d}] slot=0x{slot:04X}{name_part}"
        elif 2081 <= card_id <= 2097:
            c_note = f"  @ [Token{card_id - 2080:02d}] slot=0x{slot:04X}{name_part}"
        elif 2098 <= card_id <= 3422:
            c_note = f"  @ [表B {card_id:04d}] slot=0x{slot:04X}{name_part}"
        else:
            c_note = f"  @ card_id={card_id}"

        out_lines.append(f"    .hword {fmt(tb0)}, {fmt(tb1)}{c_note}")

    # 填充段
    out_lines.append("")
    out_lines.append(f"    @ === 保留/填充区：{n_pad} × 0xFFFF ({n_pad * 2} B) ===")
    out_lines.append(f"    .fill {n_pad * 2}, 1, 0xFF")
    out_lines.append("")
    out_lines.append("card_image_index_end:")
    out_lines.append("")

    INDEX_S_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_S_PATH.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"写入 {INDEX_S_PATH} ({total_u16} entries, {INDEX_ROM_END - INDEX_ROM_START} B)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="导出卡牌详情页大卡图（6bpp）。card_id 1..2097，"
                    "OCG (flag=0) 与 TCG (flag=1) 两版一致时无后缀，不一致时分别加 _ocg / _tcg。")
    parser.add_argument("--gray", action="store_true", help="输出灰度（跳过调色板）")
    parser.add_argument("--only", type=int, default=None, help="只处理指定 card_id（调试用）")
    parser.add_argument("--start", type=int, default=0, help="起始 card_id（默认 0；0 对应占位记录 tb=0，用途未知但数据有效）")
    parser.add_argument("--end", type=int, default=2097, help="末尾 card_id 含（默认 2097）")
    parser.add_argument("--no-png", action="store_true", help="跳过 PNG 导出，仅生成 bin 与 .s")
    parser.add_argument("--no-blobs", action="store_true", help="跳过 bin 与 .s 生成，仅导出 PNG")
    args = parser.parse_args()

    if not ROM_PATH.exists():
        print(f"ERROR: ROM not found at {ROM_PATH}", file=sys.stderr)
        return 1
    rom = ROM_PATH.read_bytes()

    if not args.no_blobs:
        print("=== 导出 ROM 原始数据块 + 索引 .s ===")
        dump_rom_blobs(rom)
        write_index_source(rom)
        print()

    if args.no_png:
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    card_ids = [args.only] if args.only is not None else list(range(args.start, args.end + 1))

    # 缓存 tile_block → PNG 渲染（避免重复解码 + 避免重复 I/O）
    rendered: dict[tuple[int, bool], Image.Image] = {}  # (tb, gray) → Image

    def get_image(tb: int) -> Image.Image:
        key = (tb, args.gray)
        if key not in rendered:
            pixels = decode_and_arrange(rom, tb)
            pal = load_palette(rom, tb) if not args.gray else []
            rendered[key] = render_png(pixels, pal, args.gray)
        return rendered[key]

    # 统计
    tb_used: set[int] = set()
    n_written = 0
    n_both_ffff = 0
    n_single = 0
    n_same = 0
    n_diff = 0

    manifest_rows: list[tuple[int, str, str, str]] = []  # cid, fn_ocg, fn_tcg, fn_shared

    for cid in card_ids:
        tb0 = read_tb(rom, cid, 0)  # OCG 日版
        tb1 = read_tb(rom, cid, 1)  # TCG 非日版

        if tb0 is None and tb1 is None:
            n_both_ffff += 1
            manifest_rows.append((cid, "", "", ""))
            continue

        if tb0 == tb1:
            # 两版相同 → 无后缀
            tb = tb0  # == tb1
            fn = f"card_{cid:04d}.png"
            get_image(tb).save(OUT_DIR / fn, optimize=True)
            tb_used.add(tb)
            n_written += 1
            n_same += 1
            manifest_rows.append((cid, "", "", fn))
        elif tb0 is not None and tb1 is not None:
            # 两版都存在但不同 → 双文件
            fn_ocg = f"card_{cid:04d}_ocg.png"
            fn_tcg = f"card_{cid:04d}_tcg.png"
            get_image(tb0).save(OUT_DIR / fn_ocg, optimize=True)
            get_image(tb1).save(OUT_DIR / fn_tcg, optimize=True)
            tb_used.update([tb0, tb1])
            n_written += 2
            n_diff += 1
            manifest_rows.append((cid, fn_ocg, fn_tcg, ""))
        else:
            # 单版存在
            fn_ocg = fn_tcg = ""
            if tb0 is not None:
                fn_ocg = f"card_{cid:04d}_ocg.png"
                get_image(tb0).save(OUT_DIR / fn_ocg, optimize=True)
                tb_used.add(tb0)
            if tb1 is not None:
                fn_tcg = f"card_{cid:04d}_tcg.png"
                get_image(tb1).save(OUT_DIR / fn_tcg, optimize=True)
                tb_used.add(tb1)
            n_written += 1
            n_single += 1
            manifest_rows.append((cid, fn_ocg, fn_tcg, ""))

        if cid % 200 == 0:
            print(f"  进度 {cid}/{args.end}  (已写 {n_written})")

    # 清单
    manifest_path = OUT_DIR / "manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as fp:
        fp.write("card_id,file_ocg,file_tcg,file_shared,slot_id_hex,tb_ocg,tb_tcg\n")
        for cid, fn_ocg, fn_tcg, fn_shared in manifest_rows:
            slot = card_id_to_slot(rom, cid)
            tb0 = read_tb(rom, cid, 0)
            tb1 = read_tb(rom, cid, 1)
            fp.write(
                f"{cid},{fn_ocg},{fn_tcg},{fn_shared},{slot:04X},"
                f"{'' if tb0 is None else tb0},{'' if tb1 is None else tb1}\n"
            )

    print()
    print(f"===== 导出统计 (card_id {args.start}..{args.end}) =====")
    print(f"两版相同（无后缀）   : {n_same}")
    print(f"两版不同（双文件）   : {n_diff}")
    print(f"仅单版存在（单文件） : {n_single}")
    print(f"两版都 FFFF（跳过）  : {n_both_ffff}")
    print(f"共写 PNG            : {n_written}")
    print(f"独立 tile_block 数  : {len(tb_used)}")

    # tile_block 覆盖率分析
    if tb_used:
        max_tb = max(tb_used)
        all_tbs = set(range(max_tb + 1))
        missing = sorted(all_tbs - tb_used)
        print(f"tile_block 值域: 0..{max_tb}")
        print(f"理论连续数:      {max_tb + 1}")
        print(f"实际使用数:      {len(tb_used)}")
        print(f"未被使用数:      {len(missing)}")
        if missing and len(missing) <= 50:
            print(f"缺失 tile_block: {missing}")
        elif missing:
            print(f"缺失 tile_block (前 50): {missing[:50]} ...")
    print(f"PNG 输出：{OUT_DIR.resolve()}")
    print(f"清单文件：{manifest_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
