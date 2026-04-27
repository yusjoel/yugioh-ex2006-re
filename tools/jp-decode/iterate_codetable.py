"""
迭代收敛 codetable.
priority: seed > user_confirmed > cardname-vote > paddle
"""
import sys, json, struct, csv
from collections import Counter, defaultdict
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools/jp-decode')
from seed_codetable import build_seed_by_idx
from user_confirmed import USER_CONFIRMED

ROM = open('roms/2343.gba', 'rb').read()
PT, CT = 0x015F3A5C, 0x015BB594

paddle = json.loads(open('tools/jp-decode/ocr_paddle.json', encoding='utf-8').read())
paddle_by_idx = {int(k): v['pick'] for k, v in paddle['by_idx'].items()}
seed = build_seed_by_idx()

csv_names = []
with open('refs/yugioh-card-search/data/card_master.csv', encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for row in r: csv_names.append(row[2])
csv_set = set(csv_names)

def cti(c): return ((c & 0xF00) >> 1) | (c & 0x7F)
def read_xx(cid):
    ptr = struct.unpack_from('<I', ROM, PT + cid*24)[0]
    addr = CT + ptr; end = ROM.find(b'\x00', addr)
    return ROM[addr:end]


def build_table_from_vote(votes):
    """seed > user_confirmed > vote > paddle."""
    out = {}
    for idx in range(1925):
        if idx in seed: out[idx] = seed[idx]
        elif idx in USER_CONFIRMED: out[idx] = USER_CONFIRMED[idx]
        elif idx in votes and votes[idx]: out[idx] = votes[idx].most_common(1)[0][0]
        elif paddle_by_idx.get(idx): out[idx] = paddle_by_idx[idx]
    return out


def decode_card(cid, table):
    xx = read_xx(cid)
    if len(xx) % 2 != 0: return None, None
    s, idx_seq = [], []
    for i in range(0, len(xx), 2):
        code = (xx[i]<<8) | xx[i+1]
        if code <= 0xEFFF: return None, None
        idx = cti(code); idx_seq.append(idx)
        s.append(table.get(idx, '?'))
    return ''.join(s), idx_seq


def run_round(prev_table, threshold=0.7, prev_votes=None):
    votes = defaultdict(Counter) if prev_votes is None else prev_votes
    matched = 0
    for cid in range(1, 2098):
        dec, idx_seq = decode_card(cid, prev_table)
        if dec is None or '?' in dec or len(dec) < 2: continue
        best, ratio = None, 0
        for n in csv_names:
            if len(n) != len(dec): continue
            r = SequenceMatcher(None, dec, n).ratio()
            if r > ratio: best, ratio = n, r
        if best and ratio >= threshold:
            matched += 1
            for idx, ch in zip(idx_seq, best):
                votes[idx][ch] += 1
    return votes, matched


# Init
init_table = {}
for idx in range(1925):
    if idx in seed: init_table[idx] = seed[idx]
    elif idx in USER_CONFIRMED: init_table[idx] = USER_CONFIRMED[idx]
    elif paddle_by_idx.get(idx): init_table[idx] = paddle_by_idx[idx]

votes = defaultdict(Counter)
for round_n in range(1, 6):
    prev_table = build_table_from_vote(votes) if round_n > 1 else init_table
    votes, matched = run_round(prev_table, threshold=0.7, prev_votes=votes)
    table = build_table_from_vote(votes)
    
    src = Counter()
    for idx in range(1925):
        if idx in seed: src['seed'] += 1
        elif idx in USER_CONFIRMED: src['user'] += 1
        elif idx in votes and votes[idx]: src['cardname'] += 1
        elif paddle_by_idx.get(idx): src['paddle'] += 1
        else: src['empty'] += 1
    
    exact = 0; total = 0; unknown = 0
    for cid in range(1, 2098):
        dec, _ = decode_card(cid, table)
        if dec is None: continue
        total += 1
        if '?' in dec: unknown += 1; continue
        if dec in csv_set: exact += 1
    print(f'Round {round_n}: matched={matched}  user={src["user"]}  cardname={src["cardname"]}  '
          f'empty={src["empty"]}  exact_csv={exact}/{total} ({100*exact/total:.1f}%)')

out = {
    'by_idx': {str(k): v for k, v in table.items()},
    '_meta': {
        'priority': 'seed > user_confirmed > cardname-vote > paddle',
        'sources': dict(src),
        'verify': {'total': total, 'exact_csv': exact, 'unknown': unknown},
    },
}
with open('tools/jp-decode/codetable.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'\nSaved → tools/jp-decode/codetable.json')

# Spot-check
for cid in [1, 2, 3, 5, 16, 21, 22, 37, 88, 220]:
    dec, _ = decode_card(cid, table)
    print(f'  cid={cid:4d}  {dec!r}')
