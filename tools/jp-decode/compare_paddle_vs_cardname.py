"""
比对 PaddleOCR 汉字区结果 vs 卡名 vote 结果, 列出差异。

流程:
1. 用 seed (ASCII+假名) + PaddleOCR (汉字) 解码全 ROM 卡名
2. 与 csv 日文卡名 fuzzy 匹配 (Levenshtein-like)
3. 对匹配的卡: 用 csv 真名按字符位置回填 → 累积 idx → 字符 投票
4. 与 PaddleOCR 对比, 列出汉字区 (idx >= 290) 差异
"""
import sys, json, struct, csv
from collections import Counter, defaultdict
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools/jp-decode')
from seed_codetable import build_seed_by_idx

# Constants
ROM = open('roms/2343.gba', 'rb').read()
CARD_NAMES_TABLE = 0x015BB594
PTR_TABLE        = 0x015F3A5C
NUM_CARDS        = 2098

# Load OCR results
paddle = json.loads(open('tools/jp-decode/ocr_paddle.json', encoding='utf-8').read())
paddle_by_idx = {int(k): v['pick'] for k, v in paddle['by_idx'].items()}

seed = build_seed_by_idx()


def char_code_to_glyph_idx(code):
    """For code > 0xEFFF (XX encoding)."""
    return ((code & 0xF00) >> 1) | (code & 0x7F)


def read_card_xx_bytes(cid):
    ptr_off = struct.unpack_from('<I', ROM, PTR_TABLE + cid*6*4)[0]
    addr = CARD_NAMES_TABLE + ptr_off
    end = ROM.find(b'\x00', addr)
    return ROM[addr:end]


def xx_bytes_to_idx_seq(xx):
    """Convert XX byte stream to glyph_idx sequence (skip non-XX bytes)."""
    if len(xx) % 2 != 0:
        return None
    seq = []
    for i in range(0, len(xx), 2):
        hi, lo = xx[i], xx[i+1]
        code = (hi << 8) | lo
        if code <= 0xEFFF:
            return None  # SJIS path - skip these cards for now
        idx = char_code_to_glyph_idx(code)
        seq.append(idx)
    return seq


def decode_with_seed_and_paddle(idx_seq):
    """Best-effort decode: seed first, fallback to paddle, '?' if both fail."""
    s = []
    for idx in idx_seq:
        if idx in seed:
            s.append(seed[idx])
        elif paddle_by_idx.get(idx):
            s.append(paddle_by_idx[idx])
        else:
            s.append('?')
    return ''.join(s)


# Load csv (Japanese card names)
csv_names = []
with open('refs/yugioh-card-search/data/card_master.csv', encoding='utf-8') as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        csv_names.append(row[2])


def find_best_csv_match(decoded, max_dist=2):
    """Find csv name with smallest edit distance to decoded.
       Skip if decoded contains '?' (unknown). Returns (name, ratio) or None."""
    if '?' in decoded or len(decoded) < 2:
        return None
    best = None
    best_ratio = 0.0
    for name in csv_names:
        if abs(len(name) - len(decoded)) > max_dist:
            continue
        ratio = SequenceMatcher(None, decoded, name).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = name
    return (best, best_ratio) if best else None


# Process all cards
print('Decoding & matching cards...')
matched_cards = []   # list of (cid, idx_seq, csv_name)
skipped = 0
unmatched = 0
for cid in range(1, NUM_CARDS):  # skip cid=0 (placeholder)
    xx = read_card_xx_bytes(cid)
    if len(xx) == 0:
        skipped += 1
        continue
    idx_seq = xx_bytes_to_idx_seq(xx)
    if idx_seq is None:
        skipped += 1
        continue
    decoded = decode_with_seed_and_paddle(idx_seq)
    m = find_best_csv_match(decoded)
    if m and m[1] >= 0.7:  # similarity threshold
        csv_name, ratio = m
        if len(csv_name) == len(idx_seq):  # length must match for 1-to-1 alignment
            matched_cards.append((cid, idx_seq, csv_name, ratio, decoded))
        else:
            unmatched += 1
    else:
        unmatched += 1

print(f'Matched (length-aligned): {len(matched_cards)}')
print(f'Unmatched: {unmatched}')
print(f'Skipped (no XX / SJIS path): {skipped}')

# Build cardname-vote table
votes = defaultdict(Counter)
for cid, idx_seq, csv_name, ratio, decoded in matched_cards:
    for idx, ch in zip(idx_seq, csv_name):
        votes[idx][ch] += 1

# Each idx → top-voted character
cardname_by_idx = {}
ambiguous = []  # idx with conflicting votes
for idx, c in votes.items():
    top = c.most_common(2)
    cardname_by_idx[idx] = top[0][0]
    if len(top) > 1 and top[1][1] >= 2:
        ambiguous.append((idx, top))

print(f'\nCard-name covered idx: {len(cardname_by_idx)}')
print(f'Ambiguous (multi-char vote): {len(ambiguous)}')
if ambiguous[:5]:
    print('  Sample ambiguous:')
    for idx, top in ambiguous[:10]:
        print(f'    idx={idx:4d}  votes={top[:3]}')

# Compare paddle vs cardname for KANJI region (idx >= 290)
print(f'\n=== Comparing PaddleOCR vs Card-name vote (汉字区 idx ≥ 290) ===\n')
diffs = []
for idx in sorted(cardname_by_idx):
    if idx < 290:
        continue
    cn = cardname_by_idx[idx]
    pd = paddle_by_idx.get(idx, '')
    if cn != pd:
        diffs.append((idx, pd, cn, votes[idx].most_common(3)))

print(f'Differences: {len(diffs)} / {sum(1 for i in cardname_by_idx if i >= 290)} card-covered kanji idx')
print(f'(PaddleOCR pick != Card-name vote)\n')
print(f'{"idx":>5}  {"paddle":>6}  {"card":>6}  vote_top3')
for idx, pd, cn, top3 in diffs:
    pd_str = repr(pd) if pd else "''"
    print(f'  {idx:4d}  {pd_str:>8}  {cn!r:>6}  {top3}')

# Save full report
out = {
    'paddle_pick_count': len([1 for v in paddle_by_idx.values() if v]),
    'cardname_covered_count': len(cardname_by_idx),
    'kanji_diff_count': len(diffs),
    'diffs_kanji': [
        {'idx': idx, 'paddle': pd, 'cardname': cn,
         'vote_top3': [[c, n] for c, n in top3]}
        for idx, pd, cn, top3 in diffs
    ],
    'cardname_by_idx': cardname_by_idx,
    'matched_cards_count': len(matched_cards),
    'unmatched_count': unmatched,
}
with open('tools/jp-decode/diff_report.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'\nFull report saved → tools/jp-decode/diff_report.json')
