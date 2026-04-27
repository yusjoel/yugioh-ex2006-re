"""
合并构建最终 codetable.json:
  优先级 (高 → 低): cardname vote > seed > paddle > 空
  反向解码全 ROM 卡名, 与 csv 比对验证完整性
"""
import sys, json, struct, csv
from collections import Counter, defaultdict
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools/jp-decode')
from seed_codetable import build_seed_by_idx

ROM = open('roms/2343.gba', 'rb').read()
CARD_NAMES_TABLE = 0x015BB594
PTR_TABLE        = 0x015F3A5C
NUM_CARDS        = 2098

paddle = json.loads(open('tools/jp-decode/ocr_paddle.json', encoding='utf-8').read())
paddle_by_idx = {int(k): v['pick'] for k, v in paddle['by_idx'].items()}
diff_report = json.loads(open('tools/jp-decode/diff_report.json', encoding='utf-8').read())
cardname_by_idx_raw = {int(k): v for k, v in diff_report['cardname_by_idx'].items()}

seed = build_seed_by_idx()


def char_code_to_glyph_idx(code):
    return ((code & 0xF00) >> 1) | (code & 0x7F)


def read_card_xx(cid):
    ptr_off = struct.unpack_from('<I', ROM, PTR_TABLE + cid*6*4)[0]
    addr = CARD_NAMES_TABLE + ptr_off
    end = ROM.find(b'\x00', addr)
    return ROM[addr:end]


# Build final codetable: cardname > seed > paddle
final = {}
src_count = Counter()
for idx in range(1925):
    if idx in cardname_by_idx_raw:
        final[idx] = cardname_by_idx_raw[idx]
        src_count['cardname'] += 1
    elif idx in seed:
        final[idx] = seed[idx]
        src_count['seed'] += 1
    elif paddle_by_idx.get(idx):
        final[idx] = paddle_by_idx[idx]
        src_count['paddle'] += 1
    else:
        src_count['empty'] += 1

print('=== Final codetable composition ===')
for src, n in src_count.most_common():
    print(f'  {src:10s}: {n:4d} ({100*n/1925:.1f}%)')
print(f'  TOTAL    : {sum(src_count.values())}')


def decode_card(cid):
    xx = read_card_xx(cid)
    if len(xx) % 2 != 0:
        return None, None
    s = []
    has_ascii_path = False
    for i in range(0, len(xx), 2):
        code = (xx[i] << 8) | xx[i+1]
        if code <= 0xEFFF:
            has_ascii_path = True
            s.append(f'<{code:04X}>')
            continue
        idx = char_code_to_glyph_idx(code)
        s.append(final.get(idx, f'[?{idx}]'))
    return ''.join(s), has_ascii_path


# Load csv
csv_names = []
with open('refs/yugioh-card-search/data/card_master.csv', encoding='utf-8') as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        csv_names.append(row[2])
csv_set = set(csv_names)


# Verify: decode all cards + match csv
print('\n=== Verification: decode all cards & match csv ===\n')
exact_match = 0
not_in_csv = 0     # decoded ok but no csv entry
has_unknown = 0    # contains [?N]
empty_xx = 0       # no XX bytes
sjis_path = 0      # has code <= 0xEFFF
total = 0

mismatches = []
for cid in range(1, NUM_CARDS):
    decoded, has_ascii = decode_card(cid)
    if decoded is None:
        continue
    total += 1
    xx = read_card_xx(cid)
    if not xx:
        empty_xx += 1
        continue
    if has_ascii:
        sjis_path += 1
        continue
    if '[?' in decoded:
        has_unknown += 1
        continue
    if decoded in csv_set:
        exact_match += 1
    else:
        # find nearest csv match
        best, ratio = None, 0
        for n in csv_names:
            if abs(len(n) - len(decoded)) > 1:
                continue
            r = SequenceMatcher(None, decoded, n).ratio()
            if r > ratio:
                best, ratio = n, r
        if ratio < 0.8:
            not_in_csv += 1
        else:
            mismatches.append((cid, decoded, best, ratio))

print(f'Total cards processed:      {total}')
print(f'  Exact csv match:          {exact_match} ({100*exact_match/total:.1f}%)')
print(f'  Has unknown [?N]:         {has_unknown}')
print(f'  Has SJIS path bytes:      {sjis_path}')
print(f'  Empty XX:                 {empty_xx}')
print(f'  Not in csv (likely OK):   {not_in_csv}  (ROM 卡 csv 没收录)')
print(f'  Decoded ≠ csv but close:  {len(mismatches)}')
print()
if mismatches[:30]:
    print('Mismatches (decoded vs csv match, ratio):')
    for cid, dec, best, ratio in mismatches[:30]:
        print(f'  cid={cid:4d}  dec={dec!r}  ≠ csv={best!r}  ratio={ratio:.2f}')

# Save final
out = {
    'by_idx': {str(k): v for k, v in final.items()},
    '_meta': {
        'sources': dict(src_count),
        'verification': {
            'total_cards': total,
            'exact_match': exact_match,
            'has_unknown': has_unknown,
            'sjis_path': sjis_path,
            'empty_xx': empty_xx,
            'not_in_csv': not_in_csv,
            'mismatch_close': len(mismatches),
        },
    },
}
with open('tools/jp-decode/codetable.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'\nSaved → tools/jp-decode/codetable.json')
