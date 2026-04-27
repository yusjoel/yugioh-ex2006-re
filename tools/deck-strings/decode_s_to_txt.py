"""
Decoder: data/deck-strings.s → text/deck-strings/ja.txt

deck-strings.s 当前仅含 JA SD/OPP 名 (其他 5 lang 在 game-strings 区).
解码 32 条 (SD 7 + OPP 25) JA 名为 UTF-8.
"""
import re
import json
import os
from pathlib import Path

OUT_DIR = Path('text/deck-strings')
OUT_DIR.mkdir(parents=True, exist_ok=True)

CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


def decode_ja(bs):
    out = []
    i = 0
    while i < len(bs):
        b = bs[i]
        if b >= 0xF0 and i + 1 < len(bs):
            hi, lo = b, bs[i + 1]
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            ch = CT.get(idx)
            if ch is None:
                raise ValueError(f'idx {idx} not in codetable')
            out.append(ch)
            i += 2
        else:
            out.append(chr(b))
            i += 1
    return ''.join(out)


def parse_byte_lines(section: str):
    """从一段文本中解析所有 .byte 行的 bytes (扁平合并). 返回连续 bytes."""
    line_pat = re.compile(r'^\s*\.byte\s+(.*?)\s*$', re.MULTILINE)
    bytehex_pat = re.compile(r'0x([0-9A-Fa-f]{2})')
    out = bytearray()
    for m in line_pat.finditer(section):
        for h in bytehex_pat.findall(m.group(1)):
            out.append(int(h, 16))
    return bytes(out)


def split_by_null(bs):
    """按 0x00 切分 (空字符串保留, 但末尾若有连续 \\0 全部归到最后一条 pad)."""
    entries = []
    cur = bytearray()
    i = 0
    while i < len(bs):
        if bs[i] == 0:
            # 累积 trailing pad
            pad_start = i
            while i < len(bs) and bs[i] == 0:
                i += 1
            pad = i - pad_start
            entries.append((bytes(cur), pad))
            cur = bytearray()
        else:
            cur.append(bs[i])
            i += 1
    if cur:
        entries.append((bytes(cur), 0))
    return entries


# Parse data/deck-strings.s
src = open('data/deck-strings.s', encoding='utf-8').read()

# 找 SD 区 (deck_str_xx_sd: 到下一 .incbin)
sd_m = re.search(r'deck_str_xx_sd:\s*\n(.+?)\.incbin', src, re.DOTALL)
opp_m = re.search(r'deck_str_xx_opp:\s*\n(.+?)\.incbin', src, re.DOTALL)
assert sd_m and opp_m

sd_bytes = parse_byte_lines(sd_m.group(1))
opp_bytes = parse_byte_lines(opp_m.group(1))
print(f'SD bytes: {len(sd_bytes)}, OPP bytes: {len(opp_bytes)}')

sd_entries = split_by_null(sd_bytes)
opp_entries = split_by_null(opp_bytes)
print(f'SD entries: {len(sd_entries)} (expect 7)')
print(f'OPP entries: {len(opp_entries)} (expect 25)')
assert len(sd_entries) == 7
assert len(opp_entries) == 25


# 写 ja.txt
out_path = OUT_DIR / 'ja.txt'
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'@ text/deck-strings/ja.txt — 32 entries (SD: 7, OPP: 25)\n')
    f.write(f'@ Format: =KIND_NN= header, then JA name on next line.\n')
    f.write(f'@ Trailing \\0 padding handled by encoder; do NOT add manually.\n\n')
    for i, (data, pad) in enumerate(sd_entries):
        text = decode_ja(data) if data else ''
        f.write(f'=SD_{i:02d}= pad={pad}\n')
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')
        f.write('\n')
    for i, (data, pad) in enumerate(opp_entries):
        text = decode_ja(data) if data else ''
        f.write(f'=OPP_{i:02d}= pad={pad}\n')
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')
        f.write('\n')

size = os.path.getsize(out_path)
print(f'wrote {out_path} ({size} B)')
