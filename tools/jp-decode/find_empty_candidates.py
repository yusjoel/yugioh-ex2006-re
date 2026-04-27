"""
对 61 个出现在卡名的 empty idx, 通过 [?]-pattern matching 找 csv 候选字符。

策略:
- 用当前 codetable 解码每张卡
- 含 [?]-占位的卡: 在 csv 中找其他位置匹配的同长度卡名
- 反推 [?]-位置应该是什么字符
- 累积每个 empty idx 的候选字符
"""
import sys, json, struct, csv
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

ROM = open('roms/2343.gba', 'rb').read()
PT, CT = 0x015F3A5C, 0x015BB594
final = {int(k): v for k, v in json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx'].items()}

csv_names = []
with open('refs/yugioh-card-search/data/card_master.csv', encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for row in r: csv_names.append(row[2])

def cti(c): return ((c & 0xF00) >> 1) | (c & 0x7F)

def decode_with_marker(cid):
    ptr = struct.unpack_from('<I', ROM, PT + cid*24)[0]
    addr = CT + ptr; end = ROM.find(b'\x00', addr)
    xx = ROM[addr:end]
    if len(xx) % 2 != 0: return None, None
    chars = []
    idx_seq = []
    for i in range(0, len(xx), 2):
        c = (xx[i]<<8) | xx[i+1]
        if c <= 0xEFFF: return None, None
        idx = cti(c)
        idx_seq.append(idx)
        chars.append(final.get(idx, None))  # None for unknown
    return chars, idx_seq


# Pattern match: chars (含 None) vs csv 卡名
votes = defaultdict(Counter)
for cid in range(1, 2098):
    chars, idx_seq = decode_with_marker(cid)
    if chars is None: continue
    if all(c is not None for c in chars): continue  # no unknown, skip
    n = len(chars)
    # Find csv candidates: same length, all known positions match
    candidates = []
    for csv_name in csv_names:
        if len(csv_name) != n: continue
        ok = True
        for i, c in enumerate(chars):
            if c is not None and c != csv_name[i]:
                ok = False; break
        if ok: candidates.append(csv_name)
    # Single candidate → strong evidence
    if len(candidates) == 1:
        cand = candidates[0]
        for i, c in enumerate(chars):
            if c is None:
                votes[idx_seq[i]][cand[i]] += 5  # strong vote
    elif 1 < len(candidates) <= 5:
        # Multiple but few: still vote (lighter)
        for cand in candidates:
            for i, c in enumerate(chars):
                if c is None:
                    votes[idx_seq[i]][cand[i]] += 1


# Filter: only idx that have empty in current codetable
empty_idx = [i for i in range(1925) if i not in final or not final[i]]
in_cardname_empty = sorted([i for i in empty_idx if i in votes and votes[i]])
print(f'Total empty: {len(empty_idx)}')
print(f'In-cardname empty (with vote): {len(in_cardname_empty)}')

# Save candidates
out = []
for idx in in_cardname_empty:
    top = votes[idx].most_common(3)
    out.append({'idx': idx, 'top1': top[0][0], 'top1_count': top[0][1],
                'all': [[c, n] for c, n in top]})

with open('tools/jp-decode/empty_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f'\nSample candidates:')
for entry in out[:15]:
    top_str = ' '.join(f'{c}({n})' for c, n in entry['all'])
    print(f'  idx={entry["idx"]:4d}  top1={entry["top1"]!r}  votes=[{top_str}]')
print(f'\nSaved → tools/jp-decode/empty_candidates.json')
