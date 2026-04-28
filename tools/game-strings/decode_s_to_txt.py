"""
Decoder: data/deck-strings.s → text/deck-strings/ja.txt

deck-strings.s = JA UI text 全区段 (0x1DB9C10 ~ 0x1DC4620, 1597 条).
解码 JA bytes → UTF-8, 输出 ja.txt (=NNNNN= header + content).
保留 SD/OPP 名的特殊 label 标注 (=SD_NN= / =OPP_NN= 形式作 alias).
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


# Parse data/deck-strings.s: 收集 (label_or_seq, bytes_with_pad)
src = open('data/deck-strings.s', encoding='utf-8').read()

# 找所有 label + 之后的 .byte / .zero, 直到下一 label
# label 形式: deck_str_xx_00000: / deck_str_xx_sd_NN: / deck_str_xx_opp_NN: / deck_str_xx:
label_pat = re.compile(
    r'^(deck_str_xx(?:_sd_\d+|_opp_\d+|_\d{5}|))?:\s*(?:@\s*(.*))?$',
    re.MULTILINE,
)
lines = src.splitlines()

# 提取每个 entry 的 bytes (含 trailing pad)
entries = []  # list of (kind, name_or_idx, comment, bytes, pad)
cur_label = None
cur_comment = ''
cur_bytes = bytearray()
cur_pad = 0
in_entry = False

bytehex_re = re.compile(r'0x([0-9A-Fa-f]{2})')
zero_re = re.compile(r'^\s*\.zero\s+(\d+)')
byte_re = re.compile(r'^\s*\.byte\s+(.*?)(?:\s*@.*)?$')


def flush(label, comment, data, pad):
    if label is None:
        return
    # data + pad 已分别累积
    entries.append((label, comment, bytes(data), pad))


for line in lines:
    line_strip = line.strip()
    if not line_strip or line_strip.startswith('@'):
        continue
    # label?
    m = re.match(r'^(deck_str_xx(?:_sd_\d+|_opp_\d+|_\d{5})?)\s*:\s*(?:@\s*(.*))?$', line)
    if m:
        # flush previous
        if cur_label is not None:
            flush(cur_label, cur_comment, cur_bytes, cur_pad)
        cur_label = m.group(1)
        cur_comment = (m.group(2) or '').strip()
        cur_bytes = bytearray()
        cur_pad = 0
        continue
    # .byte line: 把 bytes 累积; 若纯 0x00 当 pad
    bm = byte_re.match(line)
    if bm:
        bs = [int(h, 16) for h in bytehex_re.findall(bm.group(1))]
        if all(b == 0 for b in bs):
            cur_pad += len(bs)
        else:
            # 若已经累积了非零, 又出现 \0, 说明字符串内含 \0? 不应发生
            cur_bytes.extend(bs)
        continue
    # .zero N: pad
    zm = zero_re.match(line)
    if zm:
        cur_pad += int(zm.group(1))
        continue

if cur_label is not None:
    flush(cur_label, cur_comment, cur_bytes, cur_pad)

# 第一个 entry 的 label 是 'deck_str_xx' (root), pad 是头部的 .zero 2. 跳过.
print(f'Parsed {len(entries)} entries (incl root)')
real_entries = [e for e in entries if e[0] != 'deck_str_xx']
print(f'Real entries: {len(real_entries)}')

# 写 ja.txt
out_path = OUT_DIR / 'ja.txt'
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'@ text/deck-strings/ja.txt — {len(real_entries)} entries\n')
    f.write('@ JA UI strings (full region 0x1DB9C10 ~ 0x1DC4620, 1597 strings).\n')
    f.write('@ Format:\n')
    f.write('@   =NNNNN= pad=N        (sequential entries, NNNNN = 0..N-1)\n')
    f.write('@   =SD_NN= pad=N        (alias for deck_str_xx_sd_NN, master label)\n')
    f.write('@   =OPP_NN= pad=N\n')
    f.write('@ pad = trailing \\0 byte count (1 or 2 typically).\n\n')
    for label, comment, data, pad in real_entries:
        # 转换 label → header
        if label.startswith('deck_str_xx_sd_'):
            n = int(label[len('deck_str_xx_sd_'):])
            header = f'=SD_{n:02d}= pad={pad}'
        elif label.startswith('deck_str_xx_opp_'):
            n = int(label[len('deck_str_xx_opp_'):])
            header = f'=OPP_{n:02d}= pad={pad}'
        else:
            n = int(label[len('deck_str_xx_'):])
            header = f'={n:05d}= pad={pad}'
        if comment:
            header += f' @ {comment}'
        text = decode_ja(data) if data else ''
        f.write(header + '\n')
        f.write(text)
        if not text.endswith('\n'):
            f.write('\n')
        f.write('\n')

size = os.path.getsize(out_path)
print(f'wrote {out_path} ({size} B)')
