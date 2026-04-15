# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ImportProjectLabels.py  (Jython 2.7 / Ghidra script)
#
# TG.2  把项目 .s 里的 label 批量打到 Ghidra.
#
# 策略分两类:
#   A. 已知 stride / 已知 base 的规则数组, 脚本里硬编码 (无需解析源码).
#      - card-stats.s: card_XXXX @ 0x098169B6 + i*22  (5170 条)
#      - (struct-decks / font / card-image-index / starter-deck 由 CreateCardStatsType.py 打)
#   B. 顶层 label, 从 .s 文件头注释里抄 ROM 范围.
#      - card-names / banlists / game-strings / opponent-card-values / deck-strings /
#        card-image-palettes / card-image-tiles
#   C. 顶层 + 25 个对手卡组 (扫注释 "GBA地址: 0xXXXXXXXX" + 下一行 label).
#
# 用法: 在 Ghidra 里 Script Manager 里运行. 必要时配合 RUN_DRY=True 预览.
#
# Jython 限制: 不要用 f-string / pathlib / walrus / type hints.
#
# @category Ygo-ex2006

import os
import re

from ghidra.program.model.symbol import SourceType


RUN_DRY = False  # True=仅打印, False=实际 createLabel
# 允许 headless -postScript 传 "dry" 强制开启
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


# 仓库根 (脚本放在 ghidra_scripts/ 下, 根在上一级)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__ if '__file__' in dir() else os.getcwd() + '/ghidra_scripts/x')))
# Ghidra 脚本常常没有 __file__; 退而用 ghidra_script source file
try:
    SOURCE_FILE = getSourceFile().getAbsolutePath()
    REPO_ROOT = os.path.dirname(os.path.dirname(SOURCE_FILE))
except Exception:
    pass


def af():
    return currentProgram.getAddressFactory()


def place_label(rom_abs, name):
    """rom_abs 是 0x09xxxxxx 形式的 GBA 运行时地址."""
    a = af().getAddress("0x%08X" % rom_abs)
    if RUN_DRY:
        print("[dry] %s  %s" % (a, name))
        return
    try:
        createLabel(a, name, True, SourceType.USER_DEFINED)
    except Exception as e:
        print("[fail] %s %s: %s" % (a, name, e))


# -----------------------------------------------------------------------------
# A. card-stats.s: 5170 条 card_XXXX label
# -----------------------------------------------------------------------------
def place_card_stats_labels():
    base = 0x098169B6
    count = 5170
    stride = 22
    for i in range(count):
        place_label(base + i * stride, "card_%04X" % i)
    print("[A] card-stats: %d labels" % count)


# -----------------------------------------------------------------------------
# B. 顶层 label (只打一锚点)
# -----------------------------------------------------------------------------
# 精简: 所有文件级锚点由 scan_top_from_comments() 通过 .s 头 "ROM range/偏移" 解析,
# 这里只保留因文件头信息缺失需要硬编码的少数特例.
TOP_LABELS = [
    # (name, gba_addr)
    # 目前无硬编码项.
]


def place_top_labels():
    for name, addr in TOP_LABELS:
        # 动态读 .s 文件注释会更稳, 这里先允许人工覆盖上表.
        place_label(addr, name)
    print("[B] top labels: %d" % len(TOP_LABELS))


# -----------------------------------------------------------------------------
# B'. 从 .s 文件头注释 "ROM range: 0xXXXX ~ 0xYYYY" 自动抓顶层 label.
# -----------------------------------------------------------------------------
# "偏移" utf-8 = E5 81 8F E7 A7 BB; "：" utf-8 = EF BC 9A
ROM_RANGE_RE = re.compile(
    r"ROM\s*(?:range|offset|\xe5\x81\x8f\xe7\xa7\xbb)\s*[:\xef\xbc\x9a]?\s*0x([0-9A-Fa-f]+)")


def scan_top_from_comments():
    """扫 data/*.s 文件头前 10 行, 找 ROM range / ROM 偏移, 给文件起点打个 label."""
    data_dir = os.path.join(REPO_ROOT, "data")
    if not os.path.isdir(data_dir):
        print("[warn] data/ not found at %s" % data_dir)
        return
    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith(".s"):
            continue
        path = os.path.join(data_dir, fname)
        f = open(path, "r")
        try:
            head = []
            for _ in range(12):
                line = f.readline()
                if not line:
                    break
                head.append(line)
        finally:
            f.close()
        blob = "".join(head)
        m = ROM_RANGE_RE.search(blob)
        if not m:
            continue
        rom_off = int(m.group(1), 16)
        gba = 0x08000000 + rom_off
        # 生成 label 名: 去掉 .s, 破折号变下划线, 加前缀 file_
        stem = fname[:-2].replace("-", "_")
        place_label(gba, "file_%s_start" % stem)
    print("[B'] scanned data/*.s file headers")


# -----------------------------------------------------------------------------
# C. opponent-decks.s: 扫 "GBA地址: 0xXXXXXXXX" 再跟 "deck_xxx:"
# -----------------------------------------------------------------------------
# "GBA地址" 在源文件里是 utf-8 (E4 B8 80 ...); 用正则的字节串直接匹配.
GBA_COMMENT_RE = re.compile(r"GBA\s*\xe5\x9c\xb0\xe5\x9d\x80\s*[:\xef\xbc\x9a]?\s*0x([0-9A-Fa-f]+)")
LABEL_RE       = re.compile(r"^([a-z_][a-z0-9_]*):\s*(?:@.*)?$")


def place_opponent_decks():
    path = os.path.join(REPO_ROOT, "data", "opponent-decks.s")
    if not os.path.isfile(path):
        print("[warn] opponent-decks.s not found")
        return
    pending_addr = None
    count = 0
    f = open(path, "r")
    try:
        for line in f:
            m1 = GBA_COMMENT_RE.search(line)
            if m1:
                pending_addr = int(m1.group(1), 16)
                continue
            m2 = LABEL_RE.match(line)
            if m2 and pending_addr is not None:
                name = m2.group(1)
                place_label(pending_addr, name)
                pending_addr = None
                count += 1
    finally:
        f.close()
    print("[C] opponent decks: %d labels" % count)


# -----------------------------------------------------------------------------
def main():
    print("[ImportProjectLabels] REPO_ROOT = %s  DRY=%s" % (REPO_ROOT, RUN_DRY))
    place_card_stats_labels()   # 5170
    place_top_labels()          # 少量硬编码
    scan_top_from_comments()    # 每个 data/*.s 一个锚点
    place_opponent_decks()      # 25
    print("[done] ImportProjectLabels.py")


main()
