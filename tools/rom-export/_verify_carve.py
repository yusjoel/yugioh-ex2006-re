# -*- coding: utf-8 -*-
# 核对 assert_carve_block.txt 覆盖字节 == after-demo incbin 长度 (0x1F430), 且字节序列 == ROM。
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
rom = open(os.path.join(ROOT, "roms", "2343.gba"), "rb").read()
blk = os.path.join(ROOT, "tools", "ghidra-labeling", "assert_carve_block.txt")
AFTER_START, AFTER_END = 0x1E398DC, 0x1E58D0C

def unesc(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            out.append(s[i + 1]); i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)

cur = AFTER_START
rebuilt = bytearray()
for l in open(blk, encoding="utf-8"):
    m = re.search(r'\.incbin "roms/2343\.gba", 0x([0-9A-Fa-f]+), 0x([0-9A-Fa-f]+)', l)
    if m:
        off = int(m.group(1), 16); ln = int(m.group(2), 16)
        rebuilt += rom[off:off + ln]
        cur += ln
        continue
    m2 = re.match(r'\s*\.asciz "(.*)"\s*$', l)
    if m2:
        s = unesc(m2.group(1))
        rebuilt += s.encode("ascii") + b"\x00"
        cur += len(s) + 1
print("carve 覆盖结束 off: 0x%X  目标 0x%X  匹配: %s" % (cur, AFTER_END, cur == AFTER_END))
orig = rom[AFTER_START:AFTER_END]
print("重建字节 == 原 ROM 字节: %s (len %d vs %d)" % (bytes(rebuilt) == orig, len(rebuilt), len(orig)))
