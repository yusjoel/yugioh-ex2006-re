#!/usr/bin/env python3
"""从 refs/gba-ghidra-loader/ 的 GBALoader.java 提取 MMIO 寄存器定义,
生成 constants/gba_io.inc。

loader 里 mapIO() 的模式:
    addr = flatAPI.toAddr(0x4000000);
    flatAPI.createLabel(addr, "DISPCNT", true);
    flatAPI.setEOLComment(addr, "LCD Control");
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOADER_JAVA = REPO / "refs/gba-ghidra-loader/src/main/java/gba/GBALoader.java"
OUT = REPO / "constants/gba_io.inc"


def extract(java_text):
    """简单状态机: 每行看是否新 toAddr 或 createLabel, 跟踪 last_addr / last_name。"""
    addr_re = re.compile(r'flatAPI\.toAddr\(\s*(0x[0-9A-Fa-f]+)\s*\)')
    label_re = re.compile(r'flatAPI\.createLabel\(\s*addr\s*,\s*"([^"]+)"\s*,\s*true\s*\)')
    comment_re = re.compile(r'flatAPI\.setEOLComment\(\s*addr\s*,\s*"([^"]+)"\s*\)')

    last_addr = None
    pending = None  # (addr, name) waiting for EOLComment
    out = []
    for line in java_text.splitlines():
        m = addr_re.search(line)
        if m:
            if pending is not None:
                out.append((pending[0], pending[1], ""))
                pending = None
            last_addr = int(m.group(1), 16)
            continue
        m = label_re.search(line)
        if m and last_addr is not None:
            pending = (last_addr, m.group(1))
            continue
        m = comment_re.search(line)
        if m and pending is not None:
            out.append((pending[0], pending[1], m.group(1)))
            pending = None
    if pending is not None:
        out.append((pending[0], pending[1], ""))
    return out


SECTIONS = [
    (0x04000000, 0x0400005F, "LCD I/O"),
    (0x04000060, 0x040000AF, "Sound"),
    (0x040000B0, 0x040000FF, "DMA"),
    (0x04000100, 0x0400011F, "Timer"),
    (0x04000120, 0x040001FF, "Serial / Keypad / JOY Bus"),
    (0x04000200, 0x040003FF, "Interrupt / Waitstate / Power-Down"),
]


def section_of(addr):
    for lo, hi, name in SECTIONS:
        if lo <= addr <= hi:
            return name
    return "Other"


def main():
    java = LOADER_JAVA.read_text(encoding="utf-8")
    entries = extract(java)
    entries.sort(key=lambda e: e[0])

    # 按 section 分组
    grouped = {}
    for addr, name, comment in entries:
        sec = section_of(addr)
        grouped.setdefault(sec, []).append((addr, name, comment))

    lines = [
        "@ =============================================================================",
        "@ GBA MMIO 寄存器符号常量",
        "@ 数据来源: refs/gba-ghidra-loader/src/main/java/gba/GBALoader.java (mapIO)",
        "@ 生成脚本: tools/gen_gba_io_inc.py (据 GBALoader.java 自动提取)",
        "@",
        "@ 用法: 代码里 .word <名字> / ldr rN, =<名字>,GAS 会 .equ 替换成对应 MMIO 地址",
        "@ =============================================================================",
        "",
    ]

    name_w = max(len(n) for _, n, _ in entries)
    name_w = max(name_w, 12)

    for sec in ["LCD I/O", "Sound", "DMA", "Timer",
                "Serial / Keypad / JOY Bus",
                "Interrupt / Waitstate / Power-Down", "Other"]:
        if sec not in grouped:
            continue
        lines.append("@ -----------------------------------------------------------------------------")
        lines.append("@ %s" % sec)
        lines.append("@ -----------------------------------------------------------------------------")
        for addr, name, comment in grouped[sec]:
            com = ("  @ " + comment) if comment else ""
            lines.append(".equ %-*s 0x%08X%s" % (name_w, name + ",", addr, com))
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[gen] %d entries -> %s" % (len(entries), OUT.relative_to(REPO)))


if __name__ == "__main__":
    main()
