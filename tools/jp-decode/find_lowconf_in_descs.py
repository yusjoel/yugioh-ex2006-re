"""
搜索 28 个低/中信心 idx 在 card-descriptions.s _xx 中的出现位置。
解析每张卡的 _xx 字段（octal escaped bytes），按 (hi,lo) → idx 解码。
"""
import re
import json
from collections import defaultdict

# 28 个低/中信心 idx (含 group 01-04 ASCII + group 06-10 汉字)
TARGETS = {
    # group 01-02 ASCII 低/中信心
    1: 'guess=、', 2: 'guess=゜', 9: 'guess=◆', 12: 'guess=横线', 16: 'guess=‥', 17: 'guess=”',
    # group 06 中低信心
    326: 'guess=囲', 327: 'guess=妻', 438: 'guess=套', 729: 'guess=詩',
    # group 07
    806: 'guess=今', 851: 'guess=索', 894: 'guess=糸', 922: 'guess=識',
    # group 08
    1056: 'guess=桑', 1080: 'guess=浸', 1088: 'guess=診', 1174: 'guess=川',
    # group 09
    1205: 'guess=麦', 1218: 'guess=縛', 1281: 'guess=只', 1304: 'guess=燕',
    1342: 'guess=譲', 1510: 'guess=緊', 1560: 'guess=喪', 1578: 'guess=父',
    # group 10
    1742: 'guess=諭', 1746: 'guess=愛', 1816: 'guess=塞', 1828: 'guess=異',
    1839: 'guess=業', 1869: 'guess=丨', 1888: 'guess=爻',
}


def decode_octal_string(s):
    """Decode \\366\\223 octal-escaped string to raw bytes."""
    result = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == '0':
                # could be \0 or \0xx — peek
                # standard: \0 in our file is just NUL terminator
                # but octal \012 is also valid
                if i + 2 < len(s) and s[i + 2].isdigit() and s[i + 3:i + 4].isdigit():
                    result.append(int(s[i + 1:i + 4], 8))
                    i += 4
                else:
                    result.append(0)
                    i += 2
            elif nxt.isdigit():
                # octal 1-3 digit
                j = i + 1
                while j < len(s) and j < i + 4 and s[j].isdigit():
                    j += 1
                result.append(int(s[i + 1:j], 8))
                i = j
            elif nxt == 'n':
                result.append(0x0A); i += 2
            elif nxt == 't':
                result.append(0x09); i += 2
            elif nxt == '"':
                result.append(0x22); i += 2
            elif nxt == '\\':
                result.append(0x5C); i += 2
            else:
                i += 2
        else:
            result.append(ord(c))
            i += 1
    return bytes(result)


def code_to_idx(hi, lo):
    if hi >= 0xF0:
        return ((hi & 0xF) << 7) | (lo & 0x7F)
    return None


with open('data/card-descriptions.s', encoding='latin-1') as f:
    txt = f.read()

xx_pattern = re.compile(r'card_desc_(\d+)_xx:\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
cid_to_xx = {}
for m in xx_pattern.finditer(txt):
    cid = int(m.group(1))
    raw = m.group(2)
    bs = decode_octal_string(raw)
    cid_to_xx[cid] = bs

print(f'parsed {len(cid_to_xx)} card xx descriptions')

cid_to_idx_seq = {}
for cid, bs in cid_to_xx.items():
    seq = []
    i = 0
    while i + 1 < len(bs):
        hi, lo = bs[i], bs[i + 1]
        idx = code_to_idx(hi, lo)
        seq.append(idx if idx is not None else (hi, lo))
        i += 2
    cid_to_idx_seq[cid] = seq

idx_to_locs = defaultdict(list)
for cid, seq in cid_to_idx_seq.items():
    for pos, item in enumerate(seq):
        if isinstance(item, int) and item in TARGETS:
            idx_to_locs[item].append((cid, pos))

print('\n=== Hit report ===')
total = 0
for t in sorted(TARGETS.keys()):
    n = len(idx_to_locs[t])
    print(f'  idx={t:5d}  {TARGETS[t]:20s} {n:4d} hit(s)')
    total += n
hit_count = sum(1 for t in TARGETS if idx_to_locs[t])
print(f'\nTotal hits: {total}, idx with >=1 hit: {hit_count}/{len(TARGETS)}')

# Save full data for next step
out = {
    'targets': {
        str(k): {
            'guess_label': v,
            'hit_count': len(idx_to_locs[k]),
            'locations': [{'cid': c, 'pos': p} for c, p in idx_to_locs[k][:50]],  # cap 50 per idx
        }
        for k, v in TARGETS.items()
    },
}

with open('tools/jp-decode/review/lowconf_locations.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('\nwrote tools/jp-decode/review/lowconf_locations.json')

# Also save full idx-seq for rendering step
with open('tools/jp-decode/review/cid_to_idx_seq.json', 'w', encoding='utf-8') as f:
    save = {str(c): [(item if isinstance(item, int) else list(item)) for item in seq]
            for c, seq in cid_to_idx_seq.items()}
    json.dump(save, f, ensure_ascii=False)
print('wrote cid_to_idx_seq.json')
