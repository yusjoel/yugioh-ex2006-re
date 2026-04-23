#!/usr/bin/env python3
"""
批量解压 63 个 BIOS LZ77 压缩的 NNS 容器（.LZn{anr,cer,cgr,clr}）。

== 输入 ==
  直接从 ROM（roms/2343.gba）读取 FS 表与数据区。
  （亦可从已修复的 fs/ 目录读，bug #12 已修；此脚本保留 ROM 直读以最大化独立性。）

  过滤扩展名：.LZnanr × 14, .LZncer × 14, .LZncgr × 17, .LZnclr × 18
  合计 63 个，全部 BIOS LZ77 (magic=0x10，SWI 0x11/0x12 可解)。

== 输出 ==
  fs-decompressed/<orig-path>/<stem>.{nanr,ncer,ncgr,nclr}
  例: demo/exodia/exodia01_obj.LZnanr
      → fs-decompressed/demo/exodia/exodia01_obj.nanr
  重名时追加 `_dup{N}` 后缀（与 export_fs_files.py 一致）。
  解压后**剥去 4 字节 Konami wrapper**，输出纯 NNS 文件。

== 格式 ==
  LZ77 流解压后开头 4 字节是 Konami 私有 wrapper：
    byte 0       : 0x00 (type)
    bytes 1..3   : u24 LE = total_size（含 wrapper 自身，= 解压后长度）
  其后是 NNSG2dBinaryFileHeader + 数据块：
    [0..4 ) magic (LE: RNAN/RECN/RGCN/RLCN — 反转 ASCII 'NANR'/'NCER'/'NCGR'/'NCLR')
    [4..6 ) byteOrder 0xFEFF
    [6..8 ) version (major<<8|minor)
    [8..12) fileSize (= NNS 长度 = 总长 - 4 字节 wrapper)
    [12..14) headerSize = 0x10
    [14..16) dataBlocks

== 验证 ==
  - 解压后总长 == wrapper.total_size
  - 剥去 wrapper 后前 4 B == 期望 magic（按扩展名）
  - NNS 头 fileSize 字段 == (解压总长 - 4)

== FS 对齐（重要） ==
  ROM FS 表：
    paths_table  @ 0x01E6118C  339 × 32 B       (339 条 null 终止 ASCII 路径)
    offsets      @ 0x01E63BE8  339 × u32        (FID 0..338 的 FS 相对偏移)
    sizes        @ 0x01E64134  340 × u32        (多 1 个 szs[339])
    FS_BASE      @ 0x01E64684  (FID 1..338 数据起点)

  正确映射: path[i] ↔ FID[i+1]
    - offs[0]=0, szs[0]=0x70350 = FS 根 meta（不对应任何数据 FID）
    - FID 1..338 的数据在 FS_BASE..FS_BASE+0x70350 内 tight-pack
    - FID 339 (orphan): path[338]="titleEx/title_obj_s.LZnclr"
      数据在 FS_BASE + 0x70350 = 0x01ED49D4，长度 szs[339] = 208 B
      位于 FS 尾段外（见任务 D2）

  `tools/rom-export/export_fs_files.py` 历史版本误用 path[i] ↔ FID[i]（shift=0），
  致 52/63 个 .LZn* 文件名与实际内容不匹配。已于 bug #12 修复；fs/ 现 100% 对齐。
  本脚本保留直读 ROM 的路径，独立于 fs/ 修复状态，易于单独运行验证。

== 产物接入 ==
  fs-decompressed/ 由 build 重建，加入 .gitignore，不入库。
  不改 asm/rom.s（解压产物不参与 byte-identical build）。

用法:
    python tools/rom-export/export_nns_unpacked.py
"""
from __future__ import annotations

import os
import struct
import sys
from pathlib import Path


ROM_PATH = Path("roms/2343.gba")
OUT_DIR = Path("fs-decompressed")

# FS table 地址（见 export_fs_files.py 与 nns-format-notes.md §10）
FS_BASE = 0x01E64684
FS_SIZE = 0x00070350  # 声称的 FS 大小；实际尾部还有 208 B 第 339 号文件
FS_TABLES = 0x01E63BE8
PATHS_BASE = 0x01E6118C
PATHS_END = 0x01E63BE8
NUM_PATHS = 339
# 逻辑 FID 范围：1..NUM_FIDS（FID 0 是 FS 根 meta，无数据）
NUM_FIDS = 339  # 含孤儿 FID 339 (szs[339]=0xD0, 位于 FS_BASE+0x70350)

LZN_EXTS = (".LZnanr", ".LZncer", ".LZncgr", ".LZnclr")

# 期望的 NNS magic（落盘后 LE 反转）
EXPECTED_MAGIC = {
    ".LZnanr": b"RNAN",  # 'NANR' Cell Animation
    ".LZncer": b"RECN",  # 'NCER' Cell Resource
    ".LZncgr": b"RGCN",  # 'NCGR' Character Graphics
    ".LZnclr": b"RLCN",  # 'NCLR' Color (Palette)
}


def lz77_decompress(data: bytes) -> bytes:
    """BIOS LZ77 (SWI 0x11/0x12) 解压，magic byte = 0x10。"""
    if not data or data[0] != 0x10:
        raise ValueError(f"非 LZ77 魔数: 0x{data[0]:02X}" if data else "空输入")
    decomp_size = struct.unpack_from("<I", data)[0] >> 8
    out = bytearray()
    pos = 4
    while len(out) < decomp_size:
        if pos >= len(data):
            break
        flags = data[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= decomp_size:
                break
            if pos >= len(data):
                break
            if flags & (1 << bit):
                if pos + 1 >= len(data):
                    break
                b0, b1 = data[pos], data[pos + 1]
                pos += 2
                length = ((b0 >> 4) & 0xF) + 3
                disp = ((b0 & 0xF) << 8) | b1
                start = len(out) - disp - 1
                for i in range(length):
                    out.append(out[start + i])
            else:
                out.append(data[pos])
                pos += 1
    return bytes(out[:decomp_size])


def read_paths(rom: bytes) -> list[str]:
    raw = rom[PATHS_BASE:PATHS_END]
    paths: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == 0:
            i += 1
            continue
        end = raw.find(b"\x00", i)
        if end < 0:
            break
        paths.append(raw[i:end].decode("ascii"))
        i = end + 1
    if len(paths) != NUM_PATHS:
        raise RuntimeError(f"expected {NUM_PATHS} paths, got {len(paths)}")
    return paths


def read_fs_tables(rom: bytes) -> tuple[list[int], list[int]]:
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0]
            for i in range(NUM_PATHS)]
    # szs 比 offs 多 1 个（存尾部 orphan 文件的大小）
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_PATHS * 4 + i * 4)[0]
           for i in range(NUM_PATHS + 1)]
    return offs, szs


def build_fid_table(paths: list[str], offs: list[int], szs: list[int]) -> list[tuple[str, int, int]]:
    """返回 [(path, fs_offset, size)] × NUM_FIDS，对应逻辑 FID 1..NUM_FIDS。

    映射: FID i 的 path = paths[i-1]
    - FID 1..338: (off, sz) = (offs[i], szs[i])
    - FID 339 (orphan): off = offs[338] + szs[338] = FS_SIZE = 0x70350; sz = szs[339]
    """
    entries: list[tuple[str, int, int]] = []
    for fid in range(1, NUM_FIDS + 1):
        path = paths[fid - 1]
        if fid < NUM_PATHS:
            off = offs[fid]
            sz = szs[fid]
        else:  # orphan FID 339
            off = offs[NUM_PATHS - 1] + szs[NUM_PATHS - 1]
            sz = szs[NUM_PATHS]
        entries.append((path, off, sz))
    return entries


def disambiguate(rel: str, counter: dict[str, int]) -> str:
    """重名时给第 N 次出现（N≥1）追加 _dup{N} 后缀。与 export_fs_files.py 一致。"""
    n = counter.get(rel, 0)
    counter[rel] = n + 1
    if n == 0:
        return rel
    p = Path(rel)
    stem = p.stem
    suffix = p.suffix
    new_name = f"{stem}_dup{n}{suffix}"
    return str(p.parent / new_name).replace("\\", "/")


def strip_lz_prefix(name: str) -> str:
    """file.LZnanr → file.nanr"""
    stem, dot, ext = name.rpartition(".")
    if not dot or ext not in {"LZnanr", "LZncer", "LZncgr", "LZnclr"}:
        raise ValueError(f"不识别的扩展名: {name}")
    return f"{stem}.{ext[2:]}"


def validate(nns: bytes, total_size: int, expected_magic: bytes, src_path: str) -> None:
    if len(nns) < 16:
        raise ValueError(f"{src_path}: NNS 部分仅 {len(nns)} B，太短")
    magic = nns[:4]
    if magic != expected_magic:
        raise ValueError(
            f"{src_path}: magic 不匹配，期望 {expected_magic!r}，实际 {magic!r}"
        )
    file_size_field = struct.unpack_from("<I", nns, 8)[0]
    if file_size_field != len(nns):
        raise ValueError(
            f"{src_path}: NNS fileSize={file_size_field} ≠ 实际 {len(nns)} B"
        )
    # wrapper total_size == 解压总长 (= NNS 长度 + 4)
    if total_size != len(nns) + 4:
        raise ValueError(
            f"{src_path}: wrapper total={total_size} ≠ NNS+4={len(nns) + 4}"
        )


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not ROM_PATH.exists():
        print(f"ERROR: ROM 不存在: {ROM_PATH}", file=sys.stderr)
        return 1
    rom = ROM_PATH.read_bytes()

    paths = read_paths(rom)
    offs, szs = read_fs_tables(rom)

    # 完整性检查：FID 0 是根 meta
    if offs[0] != 0 or szs[0] != FS_SIZE:
        raise RuntimeError(
            f"FID 0 不是 FS 根 meta: off=0x{offs[0]:X} sz=0x{szs[0]:X}"
        )

    fid_table = build_fid_table(paths, offs, szs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    counter: dict[str, int] = {}
    # 用完整 FID 列表（而非仅 .LZn*）构造计数器，保证 dup 编号与 export_fs_files.py 一致
    for path, _, _ in fid_table:
        if not any(path.endswith(e) for e in LZN_EXTS):
            counter.setdefault(path, 0)
            counter[path] += 1

    # 重置计数器，边写边数
    write_counter: dict[str, int] = {}
    # 先把非 .LZn* 的重名次数累计（为了 _dup 编号与 export_fs_files 对齐）
    # —— 其实更简单的做法：按 FID 顺序遍历，所有路径都参与 disambiguate，
    # 只对 .LZn* 实际落盘。
    dup_counter: dict[str, int] = {}

    ok = 0
    total_in = 0
    total_out = 0
    for fid, (path, off, sz) in enumerate(fid_table, start=1):
        rel = disambiguate(path, dup_counter)
        if not any(path.endswith(e) for e in LZN_EXTS):
            continue
        ext = "." + path.rsplit(".", 1)[-1]
        expected = EXPECTED_MAGIC[ext]

        abs_off = FS_BASE + off
        blob = rom[abs_off : abs_off + sz]
        if len(blob) != sz:
            raise RuntimeError(
                f"FID {fid} {path}: 读取 {len(blob)} B ≠ 声明 {sz} B"
            )
        d = lz77_decompress(blob)

        # 剥 4 字节 Konami wrapper
        if len(d) < 4 or d[0] != 0x00:
            raise ValueError(
                f"FID {fid} {path}: wrapper byte0={d[0]:#x}（期望 0x00）"
            )
        total_size_u24 = d[1] | (d[2] << 8) | (d[3] << 16)
        if total_size_u24 != len(d):
            raise ValueError(
                f"FID {fid} {path}: wrapper u24 total={total_size_u24} ≠ 解压长 {len(d)}"
            )
        nns = d[4:]
        validate(nns, total_size_u24, expected, f"FID {fid} {path}")

        # 输出路径
        out_rel = strip_lz_prefix(Path(rel).name)
        dst = OUT_DIR / Path(rel).parent / out_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(nns)

        ok += 1
        total_in += sz
        total_out += len(nns)

    ratio = total_in / total_out if total_out else 0
    print(
        f"[export_nns_unpacked] {ok}/63 .LZn* files → {OUT_DIR}/ "
        f"— LZ77 in {total_in:,} B → NNS out {total_out:,} B (ratio {ratio:.2%})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
