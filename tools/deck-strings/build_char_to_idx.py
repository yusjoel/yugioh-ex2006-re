"""扫 data/deck-strings.s 的 .byte JA bytes, 构建 char_to_idx."""
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


line_pat = re.compile(r'^\s*\.byte\s+(.*?)\s*$', re.MULTILINE)
bytehex_pat = re.compile(r'0x([0-9A-Fa-f]{2})')

txt = Path('data/deck-strings.s').read_text(encoding='utf-8')
char_idx_counter = defaultdict(Counter)
for m in line_pat.finditer(txt):
    bs = bytes(int(h, 16) for h in bytehex_pat.findall(m.group(1)))
    i = 0
    while i + 1 < len(bs):
        hi, lo = bs[i], bs[i + 1]
        if hi >= 0xF0:
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            ch = CT.get(idx)
            if ch:
                char_idx_counter[ch][idx] += 1
        i += 2

char_to_idx = {}
for ch, counts in char_idx_counter.items():
    char_to_idx[ch] = counts.most_common(1)[0][0]

print(f'Total distinct chars in deck-strings: {len(char_to_idx)}')

OUT = Path('tools/deck-strings/char_to_idx.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(char_to_idx, f, ensure_ascii=False, indent=2)
print(f'wrote {OUT}')
