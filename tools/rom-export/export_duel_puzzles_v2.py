#!/usr/bin/env python3
"""
决斗题目 `.ydq` 导出 v2：直接从 ROM FS 表读 35 个 `puzzle/*.ydq`。

== 变更（vs v1 `export_duel_puzzles.py`）==
v1 按旧 ROM 区段 0x01EB90D8..0x01EC33D9 顺序读（FS 重构后此区已被打散进 fs-payload），
现在从 FS 表直接定位 35 个 .ydq 文件。v1 已从 export_all.py 剔除。

== FS 对齐 ==
path[i] ↔ FID[i+1]（正确映射，已于 bug #12 在 `export_fs_files.py` 修复）。
本脚本直读 ROM，独立于 fs/ 目录状态。

== 输入 ==
  roms/2343.gba 内 FS 表 + 路径表
  35 个 `.ydq` 路径: path[270..304] = "puzzle/001_kaeru.ydq" ... "puzzle/035_ijigen.ydq"
  每个 .ydq = INI 格式（CRLF 行尾），4 字节对齐填充

== 格式 ==
  标准 sections: [DUEL QUESTION] / [Player0] / [Player1] / [Equipment] / [END]
  Keys: Phase, PlayerLP[01], CardIn{Game,Hand,Deck,Fusion,Grave,Exclude}[01]_NNN(_{Face,Turn})?
  Values: 卡号\\t//\\t<SJIS 编码卡名>
  （高字节 0x80+ 是 Shift-JIS 双字节字符；`\\t` = 0x09；`//` 是分隔符）

== 输出 ==
  data/duel-puzzles-v2.s
    - 标签 `duel_puzzles_v2:`
    - 按 path[270..304] 顺序依次发射 35 个题目字节
    - 每题目以 label `duel_puzzle_NNN_<name>:` 开头
    - 字节级精确（含 trailing null padding），可 `.include` 替换 fs-payload.s 中的
      35 条 .incbin（需手写路径映射；留作后续 refactor）

用法:
    python tools/rom-export/export_duel_puzzles_v2.py
"""
from __future__ import annotations

import os
import struct
import sys
from pathlib import Path


ROM_PATH = Path("roms/2343.gba")
OUT_PATH = Path("data/duel-puzzles-v2.s")

FS_BASE = 0x01E64684
FS_TABLES = 0x01E63BE8
PATHS_BASE = 0x01E6118C
PATHS_END = 0x01E63BE8
NUM_PATHS = 339


def read_paths(rom: bytes) -> list[str]:
    raw = rom[PATHS_BASE:PATHS_END]
    paths: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == 0:
            i += 1
            continue
        end = raw.find(b"\x00", i)
        paths.append(raw[i:end].decode("ascii"))
        i = end + 1
    return paths


def read_fs_tables(rom: bytes) -> tuple[list[int], list[int]]:
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0]
            for i in range(NUM_PATHS)]
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_PATHS * 4 + i * 4)[0]
           for i in range(NUM_PATHS + 1)]
    return offs, szs


def asm_escape_line(raw: bytes) -> str:
    """ASCII 行转 .ascii 字面量内容（不含引号），高字节用 \\xXX。"""
    parts = []
    for b in raw:
        if b == 0x22:
            parts.append('\\"')
        elif b == 0x5C:
            parts.append("\\\\")
        elif b == 0x09:
            parts.append("\\t")
        elif 0x20 <= b < 0x7F:
            parts.append(chr(b))
        else:
            parts.append(f"\\{b:03o}")  # GAS: \ooo 八进制
    return "".join(parts)


def sanitize_label(s: str) -> str:
    """puzzle/001_kaeru.ydq → duel_puzzle_001_kaeru"""
    name = Path(s).stem  # 001_kaeru
    return f"duel_puzzle_{name}"


def extract_summary(blob: bytes) -> str:
    """从 INI 提取 Phase / PlayerLP0 / PlayerLP1 做行内注释。"""
    info: dict[str, str] = {}
    for line in blob.split(b"\r\n"):
        for key in (b"Phase=", b"PlayerLP0=", b"PlayerLP1="):
            if line.startswith(key):
                k = key.rstrip(b"=").decode("ascii")
                v = line[len(key):].decode("latin-1", errors="replace")
                # 控制字符转义
                v_clean = "".join(
                    c if 0x20 <= ord(c) < 0x7F else f"\\x{ord(c):02X}"
                    for c in v
                )
                info[k] = v_clean
    parts = []
    if "Phase" in info:
        parts.append(f"Phase={info['Phase']}")
    if "PlayerLP0" in info:
        parts.append(f"LP0={info['PlayerLP0']}")
    if "PlayerLP1" in info:
        parts.append(f"LP1={info['PlayerLP1']}")
    return ", ".join(parts)


def emit_puzzle_asm(label: str, rom_off: int, blob: bytes, summary: str) -> list[str]:
    """为一个 .ydq 生成结构化 asm 行。bytes 级精确（含 padding null）。"""
    lines: list[str] = []
    lines.append(f"")
    lines.append(f"@ ---- {label} @ ROM 0x{rom_off:07X}, {len(blob)} B ----")
    if summary:
        lines.append(f"@ {summary}")
    lines.append(f"{label}:")

    # 去掉 trailing null padding（0..3 字节），单独发射
    stripped = blob.rstrip(b"\x00")
    pad = len(blob) - len(stripped)

    # 按 CRLF 拆行发射 .ascii
    text_lines = stripped.split(b"\r\n")
    for idx, tl in enumerate(text_lines):
        content = asm_escape_line(tl)
        # 末行若为空 & 没剩余就不加 CRLF
        is_last = (idx == len(text_lines) - 1)
        if not is_last:
            content_with_crlf = content + "\\r\\n"
            if content_with_crlf:
                lines.append(f'\t.ascii "{content_with_crlf}"')
        else:
            if content:
                lines.append(f'\t.ascii "{content}"')

    # trailing padding
    if pad:
        lines.append(f"\t.byte {', '.join(['0x00'] * pad)}  @ {pad}-byte align pad")

    return lines


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

    ydq_indices = [i for i, p in enumerate(paths) if p.endswith(".ydq")]
    if len(ydq_indices) != 35:
        print(f"WARN: 预期 35 个 .ydq，实得 {len(ydq_indices)}", file=sys.stderr)

    out: list[str] = []
    out.append("@ ============================================================")
    out.append("@ Duel Puzzle Data v2  (DUEL QUESTION templates, INI style)")
    out.append(f"@ {len(ydq_indices)} puzzles from FS path[270..304] (shift=+1 aligned)")
    out.append("@ CRLF line endings, 4-byte aligned with trailing 0x00 pad")
    out.append("@")
    out.append("@ Generated by tools/rom-export/export_duel_puzzles_v2.py")
    out.append("@ NOT included in byte-identical build: fs/puzzle/*.ydq filenames")
    out.append("@ are currently off-by-one (task #12). Re-link after FS fix.")
    out.append("@ ============================================================")
    out.append("")
    out.append("duel_puzzles_v2:")

    total_bytes = 0
    for pi in ydq_indices:
        fid = pi + 1  # shift=+1 correct mapping
        off = offs[fid]
        sz = szs[fid]
        abs_off = FS_BASE + off
        blob = rom[abs_off : abs_off + sz]
        if len(blob) != sz:
            raise RuntimeError(f"{paths[pi]}: 读取 {len(blob)} B ≠ 声明 {sz}")
        if not blob.startswith(b"[DUEL QUESTION]\r\n"):
            raise RuntimeError(f"{paths[pi]}: 非标准 INI 头")
        label = sanitize_label(paths[pi])
        summary = extract_summary(blob)
        out.extend(emit_puzzle_asm(label, abs_off, blob, summary))
        total_bytes += sz

    out.append("")
    out.append(f"@ Total: {len(ydq_indices)} puzzles, {total_bytes:,} B")
    out.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(out), encoding="ascii")
    print(
        f"[export_duel_puzzles_v2] {len(ydq_indices)} puzzles, "
        f"{total_bytes:,} B → {OUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
