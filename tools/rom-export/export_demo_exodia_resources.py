# -*- coding: utf-8 -*-
"""
export_demo_exodia_resources.py

把 demo/exodia 资源块 (ROM 0x09e396b8..0x09e398dc, 548B) 从 rom.s line733 的大 raw
.incbin blob 里结构化导出为 data/demo-exodia-resources.s。

该块布局 (batch-1 demo scene 簇的 R3 指针目标):
  0x09e396b8  desc A (16B 二进制, NNS g2d 资源描述符, setup_demo_sprite_entry 用)
  0x09e396c8  desc B (12B, setup_demo_sprite_entry_alt 用)
  0x09e396d4  obj 路径字符串池 (8 × 0x20, exodia01/02_obj 的 NCER/NANR/NCGR/NCLR)
  0x09e397d4  指针表 (8 word -> 上面 8 串, load_demo_obj_resource_by_slot 用)
  0x09e397f4  断言文件名 "Exodia/EXO_main.c"
  0x09e39808  断言表达式 "anmID < IG2D_GetAnmSequencesCount(...)"
  0x09e39844  BG 路径 exodia00_1/00_2/01_BG/01/02 (.LZ5bg, tick_demo_scene_state_machine 用)

byte-identical: 脚本逐字段读 ROM 原始字节, .asciz+.zero / .byte / .word<label> 汇编回同字节。

用法: python tools/rom-export/export_demo_exodia_resources.py
"""
import os

ROM = os.path.join(os.path.dirname(__file__), "..", "..", "roms", "2343.gba")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo-exodia-resources.s")
VBASE = 0x08000000
BLOCK_START = 0x09e396b8
BLOCK_END   = 0x09e398dc

# 字段表 (addr, kind, label[, extra]); kind: 'bin' len / 'str' / 'ptrtable' count
FIELDS = [
    (0x09e396b8, "bin", "demo_sprite_resource_desc",     16),
    (0x09e396c8, "bin", "demo_sprite_alt_resource_desc",  12),
    (0x09e396d4, "str", "demo_path_exodia01_obj_ncer"),
    (0x09e396f4, "str", "demo_path_exodia01_obj_nanr"),
    (0x09e39714, "str", "demo_path_exodia01_obj_ncgr"),
    (0x09e39734, "str", "demo_path_exodia01_obj_nclr"),
    (0x09e39754, "str", "demo_path_exodia02_obj_ncer"),
    (0x09e39774, "str", "demo_path_exodia02_obj_nanr"),
    (0x09e39794, "str", "demo_path_exodia02_obj_ncgr"),
    (0x09e397b4, "str", "demo_path_exodia02_obj_nclr"),
    (0x09e397d4, "ptrtable", "demo_obj_resource_ptr_table", 8),
    (0x09e397f4, "str", "demo_cell_anim_assert_file"),
    (0x09e39808, "str", "demo_cell_anim_assert_expr"),
    (0x09e39844, "str", "demo_path_exodia00_1_bg"),
    (0x09e39864, "str", "demo_path_exodia00_2_bg"),
    (0x09e39884, "str", "demo_path_exodia01_bg"),
    (0x09e398a4, "str", "demo_path_exodia01"),
    (0x09e398c0, "str", "demo_path_exodia02"),
]


def main():
    rom = open(ROM, "rb").read()

    def rd(addr, n):
        off = addr - VBASE
        return rom[off:off + n]

    # 地址 -> label (供指针表解析)
    addr2label = {a: f[2] for a, *f in [(x[0],) + tuple(x) for x in FIELDS]}
    addr2label = {f[0]: f[2] for f in FIELDS}

    # 计算每字段结束 = 下一字段起始 (最后一个到 BLOCK_END)
    ends = {}
    for i, f in enumerate(FIELDS):
        ends[f[0]] = FIELDS[i + 1][0] if i + 1 < len(FIELDS) else BLOCK_END

    lines = []
    w = lines.append
    w("@ ============================================================================")
    w("@ demo/exodia 资源块 (ROM 0x%08x..0x%08x, %dB)" % (BLOCK_START, BLOCK_END, BLOCK_END - BLOCK_START))
    w("@ 由 tools/rom-export/export_demo_exodia_resources.py 生成 —— 勿手改。")
    w("@ 从 rom.s line733 raw .incbin blob 切出; byte-identical。")
    w("@ batch-1 demo scene 簇 (0x13510..0x14398) 的 R3 资源指针目标。")
    w("@ ============================================================================")
    w("")

    for f in FIELDS:
        addr, kind, label = f[0], f[1], f[2]
        end = ends[addr]
        total = end - addr
        w("%s:                              @ 0x%08x" % (label, addr))
        if kind == "bin":
            n = f[3]
            bs = rd(addr, n)
            for i in range(0, n, 8):
                chunk = bs[i:i + 8]
                w("    .byte  " + ", ".join("0x%02x" % b for b in chunk))
            # bin 之后若有到 end 的填充 (本块 bin 紧邻无填充)
            pad = total - n
            if pad > 0:
                w("    .zero  %d" % pad)
        elif kind == "str":
            bs = rd(addr, total)
            z = bs.index(0)
            s = bs[:z].decode("ascii")
            w('    .asciz "%s"' % s)
            pad = total - (z + 1)
            if pad > 0:
                w("    .zero  %d" % pad)
        elif kind == "ptrtable":
            cnt = f[3]
            for i in range(cnt):
                tgt = int.from_bytes(rd(addr + i * 4, 4), "little")
                lbl = addr2label.get(tgt)
                if lbl is None:
                    raise SystemExit("ptrtable @0x%08x[%d] -> 0x%08x 无对应 label" % (addr, i, tgt))
                w("    .word  %s" % lbl)
        w("")

    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("[ok] wrote %s (%dB block)" % (OUT, BLOCK_END - BLOCK_START))


if __name__ == "__main__":
    main()
