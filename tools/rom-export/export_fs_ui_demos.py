#!/usr/bin/env python3
"""
合成渲染 demo cutscene 的 cells + 动画关键帧（任务 C3）。

== 输入（A1 + A2 产物）==
  fs-decompressed/demo/exodia/exodia01_obj.{nanr,ncer,ncgr,nclr}
  fs-decompressed/demo/exodia/exodia02_obj.{nanr,ncer,ncgr,nclr}（+ _dup{1,2} 副本）
  fs-decompressed/demo/shuen/shuen_obj.{nanr,ncer,ncgr,nclr}
  fs-decompressed/demo/vija/wija_obj_all{,_dup1}.{nanr,ncer,ncgr,nclr}
  fs-decompressed/demo/vija/wija_obj_allUS{,_dup1}.{nanr,ncer,ncgr,nclr}

== 输出 ==
  graphics/images/fs-ui/demo_<asset>_cell_NN.png       每个 cell 合成图
  graphics/images/fs-ui/demo_<asset>_all_cells.png     cell 网格概览
  graphics/images/fs-ui/demo_<asset>_seq_S_frame_F.png 各 NANR 序列关键帧
  graphics/images/fs-ui/demo_<asset>_seq_S_timeline.png 每序列的时间轴拼图
  graphics/images/fs-ui/_demo_index.json               总索引

== NANR 说明 ==
- 本渲染仅支持 element_type=INDEX (0) 与 INDEX_T (2) 两类 frame content
- INDEX: frame content = u16 cellIdx + u16 pad → 直接复用 cell 图
- INDEX_T: 额外 s16 tx/ty → cell 绘制时叠加 translate
- INDEX_SRT (1)：暂不支持 rotate+scale，fallback 到 INDEX_T 只用 tx/ty

== 任务范围 ==
本脚本不做 BG 背景合成（依赖 .LZ5bg，任务 A3 未解）。仅前景 sprite 层。

用法:
    python tools/rom-export/export_fs_ui_demos.py
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


IN_DIR = Path("fs-decompressed")
OUT_DIR = Path("graphics/images/fs-ui")

# (asset_id, ncgr, nclr, ncer, nanr)
ASSETS: list[tuple[str, str, str, str, str]] = [
    ("exodia01",       "demo/exodia/exodia01_obj.ncgr",      "demo/exodia/exodia01_obj.nclr",
                        "demo/exodia/exodia01_obj.ncer",     "demo/exodia/exodia01_obj.nanr"),
    ("exodia02",       "demo/exodia/exodia02_obj.ncgr",      "demo/exodia/exodia02_obj.nclr",
                        "demo/exodia/exodia02_obj.ncer",     "demo/exodia/exodia02_obj.nanr"),
    ("shuen",          "demo/shuen/shuen_obj.ncgr",          "demo/shuen/shuen_obj.nclr",
                        "demo/shuen/shuen_obj.ncer",         "demo/shuen/shuen_obj.nanr"),
    ("wija_all",       "demo/vija/wija_obj_all.ncgr",        "demo/vija/wija_obj_all.nclr",
                        "demo/vija/wija_obj_all.ncer",       "demo/vija/wija_obj_all.nanr"),
    ("wija_allUS",     "demo/vija/wija_obj_allUS.ncgr",      "demo/vija/wija_obj_allUS.nclr",
                        "demo/vija/wija_obj_allUS.ncer",     "demo/vija/wija_obj_allUS.nanr"),
    ("wija_allUS_dup1","demo/vija/wija_obj_allUS_dup1.ncgr", "demo/vija/wija_obj_allUS_dup1.nclr",
                        "demo/vija/wija_obj_allUS_dup1.ncer","demo/vija/wija_obj_allUS_dup1.nanr"),
]


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not IN_DIR.is_dir():
        print(f"ERROR: {IN_DIR} 不存在", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index: list[dict] = []

    for asset_id, ncgr_rel, nclr_rel, ncer_rel, nanr_rel in ASSETS:
        paths = [IN_DIR / r for r in (ncgr_rel, nclr_rel, ncer_rel, nanr_rel)]
        if not all(p.exists() for p in paths):
            missing = [r for r, p in zip((ncgr_rel, nclr_rel, ncer_rel, nanr_rel), paths) if not p.exists()]
            print(f"  SKIP {asset_id}: 缺 {missing}", file=sys.stderr)
            continue

        fmt, palette = load_nclr_palette(paths[1].read_bytes())
        pxfmt, tiles_px = load_ncgr_tiles(paths[0].read_bytes())
        cells = load_ncer_cells(paths[2].read_bytes())
        sequences = load_nanr_sequences(paths[3].read_bytes())

        # 渲染每个 cell 到独立 PNG
        cell_imgs: list[tuple[str, bytes, int, int]] = []
        per_cell_meta = []
        for i, cell in enumerate(cells):
            rgba, W, H, ox, oy = render_cell_rgba(cell, tiles_px, palette)
            if W == 0 or H == 0:
                per_cell_meta.append({"cell": i, "empty": True, "num_oam": cell["num_oam"]})
                continue
            p = OUT_DIR / f"demo_{asset_id}_cell_{i:02d}.png"
            save_png_rgba(p, W, H, rgba)
            cell_imgs.append((f"c{i}", rgba, W, H))
            per_cell_meta.append({
                "cell": i,
                "png": str(p.relative_to(OUT_DIR)).replace("\\", "/"),
                "WxH": [W, H], "origin": [ox, oy], "num_oam": cell["num_oam"],
            })

        if cell_imgs:
            gg, gw, gh = render_grid(cell_imgs, per_row=8)
            save_png_rgba(OUT_DIR / f"demo_{asset_id}_all_cells.png", gw, gh, gg)

        # 渲染每个 NANR 序列的 timeline
        seq_meta = []
        for si, seq in enumerate(sequences):
            frame_imgs: list[tuple[str, bytes, int, int]] = []
            for fi, frame in enumerate(seq["frames"]):
                cell_idx = frame.get("cell", -1)
                if cell_idx < 0 or cell_idx >= len(cells):
                    continue
                tx = frame.get("tx", 0)
                ty = frame.get("ty", 0)
                rgba, W, H, _, _ = render_cell_rgba(cells[cell_idx], tiles_px, palette,
                                                     extra_offset=(tx, ty))
                if W == 0 or H == 0:
                    continue
                frame_imgs.append((f"f{fi}", rgba, W, H))
                # 仅保存首帧和尾帧作为 "key frame"，中间帧仅进时间轴
                if fi == 0 or fi == seq["num_frames"] - 1:
                    p = OUT_DIR / f"demo_{asset_id}_seq_{si}_frame_{fi:02d}.png"
                    save_png_rgba(p, W, H, rgba)

            if frame_imgs:
                gg, gw, gh = render_grid(frame_imgs, per_row=min(len(frame_imgs), 8))
                save_png_rgba(OUT_DIR / f"demo_{asset_id}_seq_{si}_timeline.png", gw, gh, gg)

            seq_meta.append({
                "seq": si, "num_frames": seq["num_frames"],
                "loop_start": seq["loop_start"],
                "element_type": seq["element_type"],
                "play_mode": seq["play_mode"],
                "frame_cells": [f.get("cell", -1) for f in seq["frames"]],
            })

        index.append({
            "asset": asset_id,
            "ncgr": ncgr_rel, "nclr": nclr_rel, "ncer": ncer_rel, "nanr": nanr_rel,
            "palette_fmt": fmt, "tile_fmt": pxfmt,
            "num_cells": len(cells), "num_sequences": len(sequences),
            "cells": per_cell_meta,
            "sequences": seq_meta,
        })
        print(f"  [{asset_id}] cells={len(cells)} seqs={len(sequences)} "
              f"rendered_cells={len(cell_imgs)} pal={fmt} tiles={pxfmt}")

    (OUT_DIR / "_demo_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[export_fs_ui_demos] {len(index)} demo assets → {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
