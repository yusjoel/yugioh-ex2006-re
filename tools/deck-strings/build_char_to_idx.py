"""扫 data/deck-strings.s 的 .byte JA bytes, 构建 char_to_idx."""
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


# 按 entry (label) 边界分段, 每段内按 2B pair 扫. 因为某些 entry 全局偏移为奇数,
# 但 entry 内部 (data[0,1], data[2,3], ...) 总是配对的.
byte_line_pat = re.compile(r'^\s*\.byte\s+(.*?)(?:\s*@.*)?$')
zero_pat = re.compile(r'^\s*\.zero\s+(\d+)')
label_pat = re.compile(r'^(deck_str_xx[a-z_0-9]*):')
bytehex_pat = re.compile(r'0x([0-9A-Fa-f]{2})')

txt = Path('data/deck-strings.s').read_text(encoding='utf-8')

entries = []  # list of bytearray, 每 entry 一段
cur = bytearray()
for line in txt.splitlines():
    if label_pat.match(line):
        if cur:
            entries.append(cur)
        cur = bytearray()
        continue
    bm = byte_line_pat.match(line)
    if bm:
        for h in bytehex_pat.findall(bm.group(1)):
            cur.append(int(h, 16))
        continue
    zm = zero_pat.match(line)
    if zm:
        cur.extend(b'\x00' * int(zm.group(1)))
if cur:
    entries.append(cur)

print(f'Entries: {len(entries)}')

char_idx_counter = defaultdict(Counter)
for ent in entries:
    # 走 variable-length: hi >= 0xF0 → 2B JA pair; else → 1B ASCII (含 @, 数字, 字母)
    i = 0
    while i < len(ent):
        b = ent[i]
        if b >= 0xF0 and i + 1 < len(ent):
            idx = ((b & 0xF) << 7) | (ent[i + 1] & 0x7F)
            ch = CT.get(idx)
            if ch:
                char_idx_counter[ch][idx] += 1
            i += 2
        else:
            i += 1

char_to_idx = {}
for ch, counts in char_idx_counter.items():
    char_to_idx[ch] = counts.most_common(1)[0][0]

print(f'Total distinct chars in deck-strings: {len(char_to_idx)}')

OUT = Path('tools/deck-strings/char_to_idx.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(char_to_idx, f, ensure_ascii=False, indent=2)
print(f'wrote {OUT}')
