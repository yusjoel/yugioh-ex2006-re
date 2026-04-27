"""
仅扫 data/card-names.s 的 _xx/_ja label, 统计 char → idx, 写
tools/card-names/char_to_idx.json (card-names encoder 专用).

per-dataset 是必要的: '@' 在 card-desc 是单字节控制码, 在 card-names 是 JA-encoded
2-byte (idx=42 = F0 AA). 不能共享一份 char_to_idx.
"""
import re
import json
from collections import Counter, defaultdict
from pathlib import Path


def decode_octal_string(s):
    result = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt.isdigit():
                j = i + 1
                while j < len(s) and j < i + 4 and s[j].isdigit():
                    j += 1
                result.append(int(s[i + 1:j], 8))
                i = j
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c))
            i += 1
    return bytes(result)


CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


pat = re.compile(r'card_name_\d+_(xx|ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')

char_idx_counter = defaultdict(Counter)
txt = Path('data/card-names.s').read_text(encoding='latin-1')
for m in pat.finditer(txt):
    if m.group(1) not in ('xx', 'ja'):
        continue
    bs = decode_octal_string(m.group(2))
    payload = bs.rstrip(b'\x00')
    i = 0
    while i + 1 < len(payload):
        hi, lo = payload[i], payload[i + 1]
        if hi >= 0xF0:
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            ch = CT.get(idx)
            if ch:
                char_idx_counter[ch][idx] += 1
        i += 2

char_to_idx = {}
ambiguous = []
for ch, counts in char_idx_counter.items():
    most_common = counts.most_common(1)[0]
    char_to_idx[ch] = most_common[0]
    if len(counts) > 1:
        ambiguous.append((ch, dict(counts)))

print(f'Total distinct chars in card-names: {len(char_to_idx)}')
print(f'Ambiguous: {len(ambiguous)}')
for ch, cnts in ambiguous[:10]:
    print(f'  {ch!r}: {cnts}')

OUT = Path('tools/card-names/char_to_idx.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(char_to_idx, f, ensure_ascii=False, indent=2)
print(f'\nwrote {OUT}')
