#!/usr/bin/env python3
"""
重建 title 画面的多语言 OBJ 层渲染（任务 C1）。

== 输入 ==
  fs-decompressed/titleEx/title_obj_{e,f,g,i,j,s}.{nanr,ncer,ncgr,nclr}
  实际发现 6 种语言，不含 P（葡萄牙）。

  fs-decompressed/titleEx/title_obj_s.nclr 来自 FS 尾部 0x1ED49D4（FID 339 orphan，见任务 A1）。

== 输出 ==
  graphics/images/fs-ui/title_<lang>_cell_NN.png    每个 cell 合成图
  graphics/images/fs-ui/title_<lang>_all_cells.png  cell 网格概览
  graphics/images/fs-ui/title_<lang>_seq_S.png      每个 NANR 序列的时间轴
  graphics/images/fs-ui/_title_index.json           索引

== 任务范围 ==
本脚本不做 BG 背景合成（依赖 `.LZ5bg`，任务 A3 未解）。仅 OBJ 前景层。
完整 title 画面 = BG (.LZ5bg) + 本输出（OBJ）的叠加，需 A3 解出 LZ5bg 后补全。

用法:
    python tools/rom-export/export_fs_ui_titles.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nns_lib import (  # noqa: E402
    load_nclr_palette, load_ncgr_tiles, load_ncer_cells, load_nanr_sequences,
    render_cell_rgba, render_grid, save_png_rgba,
)


IN_DIR = Path("fs-decompressed/titleEx")
OUT_DIR = Path("graphics/images/fs-ui")

LANGS = ["e", "f", "g", "i", "j", "s"]


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not IN_DIR.is_dir():
        print(f"ERROR: {IN_DIR} 不存在", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index: list[dict] = []

    for lang in LANGS:
        asset = f"title_obj_{lang}"
        ncgr = IN_DIR / f"{asset}.ncgr"
        nclr = IN_DIR / f"{asset}.nclr"
        ncer = IN_DIR / f"{asset}.ncer"
        nanr = IN_DIR / f"{asset}.nanr"
        missing = [p.name for p in (ncgr, nclr, ncer, nanr) if not p.exists()]
        if missing:
            print(f"  SKIP {asset}: 缺 {missing}", file=sys.stderr)
            continue

        fmt, palette = load_nclr_palette(nclr.read_bytes())
        pxfmt, tiles_px = load_ncgr_tiles(ncgr.read_bytes())
        cells = load_ncer_cells(ncer.read_bytes())
        sequences = load_nanr_sequences(nanr.read_bytes())

        cell_imgs: list[tuple[str, bytes, int, int]] = []
        per_cell = []
        for i, cell in enumerate(cells):
            rgba, W, H, ox, oy = render_cell_rgba(cell, tiles_px, palette)
            if W == 0 or H == 0:
                per_cell.append({"cell": i, "empty": True, "num_oam": cell["num_oam"]})
                continue
            p = OUT_DIR / f"title_{lang}_cell_{i:02d}.png"
            save_png_rgba(p, W, H, rgba)
            cell_imgs.append((f"c{i}", rgba, W, H))
            per_cell.append({
                "cell": i,
                "png": str(p.relative_to(OUT_DIR)).replace("\\", "/"),
                "WxH": [W, H], "origin": [ox, oy], "num_oam": cell["num_oam"],
            })

        if cell_imgs:
            gg, gw, gh = render_grid(cell_imgs, per_row=8)
            save_png_rgba(OUT_DIR / f"title_{lang}_all_cells.png", gw, gh, gg)

        seq_meta = []
        for si, seq in enumerate(sequences):
            frame_imgs: list[tuple[str, bytes, int, int]] = []
            for fi, frame in enumerate(seq["frames"]):
                cell_idx = frame.get("cell", -1)
                if not (0 <= cell_idx < len(cells)):
                    continue
                tx = frame.get("tx", 0)
                ty = frame.get("ty", 0)
                rgba, W, H, _, _ = render_cell_rgba(cells[cell_idx], tiles_px, palette,
                                                     extra_offset=(tx, ty))
                if W == 0 or H == 0:
                    continue
                frame_imgs.append((f"f{fi}", rgba, W, H))

            if frame_imgs:
                gg, gw, gh = render_grid(frame_imgs, per_row=min(len(frame_imgs), 8))
                save_png_rgba(OUT_DIR / f"title_{lang}_seq_{si}.png", gw, gh, gg)

            seq_meta.append({
                "seq": si, "num_frames": seq["num_frames"],
                "loop_start": seq["loop_start"],
                "element_type": seq["element_type"],
                "play_mode": seq["play_mode"],
                "frame_cells": [f.get("cell", -1) for f in seq["frames"]],
            })

        index.append({
            "lang": lang, "asset": asset,
            "palette_fmt": fmt, "tile_fmt": pxfmt,
            "num_cells": len(cells), "num_sequences": len(sequences),
            "cells": per_cell, "sequences": seq_meta,
            "bg_note": "BG layer pending task A3 (.LZ5bg reverse)",
        })
        print(f"  [title_{lang}] cells={len(cells)} seqs={len(sequences)} "
              f"rendered_cells={len(cell_imgs)} pal={fmt} tiles={pxfmt}")

    (OUT_DIR / "_title_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[export_fs_ui_titles] {len(index)}/6 languages → {OUT_DIR}/")
    print("  (BG 层待 A3 解 .LZ5bg 后补全)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
