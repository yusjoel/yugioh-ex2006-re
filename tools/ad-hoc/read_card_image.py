#!/usr/bin/env python3
"""
read_card_image.py - 从 ROM 读取卡图压缩块并导出 PNG

用法:
    python tools/read_card_image.py <GBA地址> [<GBA地址2> ...]

示例:
    python tools/read_card_image.py 0x09001234
    python tools/read_card_image.py 0x09001234 0x09005678

说明:
    - GBA 地址格式：0x08xxxxxx 或 0x09xxxxxx
    - 自动检测压缩格式（LZ77=0x10, Huffman=0x20, RLE=0x30）
    - LZ77: 直接解压并渲染为 PNG（需要调色板，默认用灰阶）
    - 其他格式：仅输出压缩头信息和原始字节预览

ROM 文件: roms/2343.gba（固定路径，从项目根目录运行）
"""

import sys
import os
import struct

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ROM_PATH = os.path.join(_REPO_ROOT, 'roms', '2343.gba')
OUT_DIR  = os.path.join(_REPO_ROOT, 'output', 'card_images')

GBA_ROM_BASE  = 0x08000000
GBA_ROM2_BASE = 0x09000000
ROM_SIZE      = 0x2000000  # 32 MB


def gba_addr_to_offset(addr: int) -> int:
    if GBA_ROM_BASE <= addr < GBA_ROM_BASE + ROM_SIZE:
        return addr - GBA_ROM_BASE
    if GBA_ROM2_BASE <= addr < GBA_ROM2_BASE + ROM_SIZE:
        return (addr - GBA_ROM2_BASE) + ROM_SIZE
    raise ValueError(f"地址 0x{addr:08X} 不在 ROM 范围内（0x08000000–0x0BFFFFFF）")


def read_rom(rom: bytes, offset: int, length: int) -> bytes:
    return rom[offset:offset + length]


def lz77_decompress(data: bytes) -> bytes:
    """BIOS LZ77 (SWI 0x11/0x12) 解压，magic byte = 0x10"""
    if data[0] != 0x10:
        raise ValueError(f"非 LZ77 魔数：0x{data[0]:02X}")
    decomp_size = struct.unpack_from('<I', data)[0] >> 8
    out = bytearray()
    pos = 4  # 跳过4字节头
    while len(out) < decomp_size:
        if pos >= len(data):
            break
        flags = data[pos]; pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= decomp_size:
                break
            if pos >= len(data):
                break
            if flags & (1 << bit):
                # 反向引用
                if pos + 1 >= len(data):
                    break
                b0, b1 = data[pos], data[pos + 1]; pos += 2
                length = ((b0 >> 4) & 0xF) + 3
                disp   = ((b0 & 0xF) << 8) | b1
                start  = len(out) - disp - 1
                for i in range(length):
                    out.append(out[start + i])
            else:
                out.append(data[pos]); pos += 1
    return bytes(out[:decomp_size])


def save_png_gray(pixels: bytes, width: int, height: int, path: str):
    """保存灰阶 PNG（不依赖 Pillow）"""
    import zlib, struct as st

    def png_chunk(name: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(name + data) & 0xFFFFFFFF
        return st.pack('>I', len(data)) + name + data + st.pack('>I', crc)

    raw_rows = b''
    for y in range(height):
        raw_rows += b'\x00' + pixels[y * width:(y + 1) * width]
    compressed = zlib.compress(raw_rows, 9)

    ihdr_data = st.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0)
    png = (
        b'\x89PNG\r\n\x1a\n'
        + png_chunk(b'IHDR', ihdr_data)
        + png_chunk(b'IDAT', compressed)
        + png_chunk(b'IEND', b'')
    )
    with open(path, 'wb') as f:
        f.write(png)
    print(f"  已保存: {path}")


def analyze_address(rom: bytes, gba_addr: int):
    print(f"\n{'='*60}")
    print(f"GBA 地址: 0x{gba_addr:08X}")
    try:
        offset = gba_addr_to_offset(gba_addr)
    except ValueError as e:
        print(f"  错误: {e}")
        return
    print(f"ROM 文件偏移: 0x{offset:08X} ({offset})")

    header = read_rom(rom, offset, 16)
    print(f"头部字节（前16）: {header.hex(' ')}")

    magic = header[0]
    if magic in (0x10, 0x20, 0x30):
        names = {0x10: 'LZ77', 0x20: 'Huffman', 0x30: 'RLE'}
        decomp_size = struct.unpack_from('<I', header)[0] >> 8
        print(f"压缩格式: BIOS {names[magic]} (magic=0x{magic:02X})")
        print(f"解压后大小: {decomp_size} 字节 ({decomp_size/1024:.1f} KB)")

        if magic == 0x10:
            # LZ77 解压并保存
            chunk_size = min(decomp_size * 3, len(rom) - offset)  # 估算压缩块大小
            chunk = read_rom(rom, offset, chunk_size)
            try:
                pixels = lz77_decompress(chunk)
                print(f"解压成功: {len(pixels)} 字节")
                os.makedirs(OUT_DIR, exist_ok=True)

                # BG2 256色，tiles 1-36，每 tile 64 字节（8×8 px）
                # 猜测尺寸：tiles 1-36 = 36 tiles = 3列×12行 = 24×96 px
                # 但解压大小可能包含调色板+tiles
                # 直接以 raw 字节存为灰阶图（近似）
                total_tiles = len(pixels) // 64
                w_tiles = 8  # 估算：8 tiles 宽
                h_tiles = total_tiles // w_tiles
                if h_tiles * w_tiles * 64 <= len(pixels) and h_tiles > 0:
                    w_px = w_tiles * 8
                    h_px = h_tiles * 8
                    # 重组 tile 数据为线性像素
                    flat = bytearray(w_px * h_px)
                    for t in range(w_tiles * h_tiles):
                        tx, ty = t % w_tiles, t // w_tiles
                        tile = pixels[t * 64:(t + 1) * 64]
                        for py in range(8):
                            for px in range(8):
                                flat[(ty * 8 + py) * w_px + tx * 8 + px] = tile[py * 8 + px]
                    fname = os.path.join(OUT_DIR, f"card_{gba_addr:08X}.png")
                    save_png_gray(bytes(flat), w_px, h_px, fname)
                else:
                    # 直接线性存储
                    side = int(len(pixels) ** 0.5)
                    fname = os.path.join(OUT_DIR, f"card_{gba_addr:08X}_raw.png")
                    save_png_gray(pixels[:side * side], side, side, fname)
            except Exception as e:
                print(f"  解压失败: {e}")
        else:
            print(f"  （{names[magic]} 解压暂不支持，仅输出头信息）")
    else:
        # 非标准压缩格式，检查是否为原始 4bpp/8bpp 图像
        print(f"  非 BIOS 压缩格式（magic=0x{magic:02X}）")
        print(f"  前 64 字节（raw）: {read_rom(rom, offset, 64).hex(' ')}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if not os.path.exists(ROM_PATH):
        print(f"ROM 文件不找到: {ROM_PATH}")
        sys.exit(1)

    with open(ROM_PATH, 'rb') as f:
        rom = f.read()
    print(f"ROM 已加载: {len(rom)} 字节 ({len(rom)//1024//1024} MB)")

    for arg in sys.argv[1:]:
        try:
            addr = int(arg, 16) if arg.startswith('0x') or arg.startswith('0X') else int(arg)
        except ValueError:
            print(f"无效地址: {arg}")
            continue
        analyze_address(rom, addr)


if __name__ == '__main__':
    main()
