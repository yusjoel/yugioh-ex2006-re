"""
Phase 0: 调研 data/card-descriptions.s
1. 解析全部 card_desc_NNNN_LANG 的 .ascii bytes
2. _xx 区: 统计所有 byte < 0xF0 的控制码分布
3. en/de/fr/it/es 区: 验证 CP1252 双向 round-trip 是否完整
4. 统计 cid 覆盖情况 (是否每张卡都 6 lang 齐全)
5. 找出 alt-art 共享 (相同 bytes 但不同 cid)
"""
import re
import json
from collections import Counter, defaultdict


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


with open('data/card-descriptions.s', encoding='latin-1') as f:
    txt = f.read()

# 匹配每个 label + .ascii bytes
pattern = re.compile(
    r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"'
)

labels = {}  # (cid, lang) -> bytes
for m in pattern.finditer(txt):
    cid = int(m.group(1))
    lang = m.group(2)
    bs = decode_octal_string(m.group(3))
    labels[(cid, lang)] = bs

print(f'Total labels parsed: {len(labels)}')

# 1. cid 覆盖情况
cid_set = set()
lang_per_cid = defaultdict(set)
for (cid, lang), _ in labels.items():
    cid_set.add(cid)
    lang_per_cid[cid].add(lang)

ALL_LANGS = {'xx', 'en', 'de', 'fr', 'it', 'es'}
print(f'\nUnique cids with labels: {len(cid_set)}')
print(f'Cid range: {min(cid_set)}..{max(cid_set)}')

cids_full = [c for c, ls in lang_per_cid.items() if ls == ALL_LANGS]
cids_partial = [(c, sorted(ALL_LANGS - ls)) for c, ls in lang_per_cid.items() if ls != ALL_LANGS]
print(f'Cids with all 6 langs: {len(cids_full)}')
print(f'Cids with partial langs: {len(cids_partial)}')
if cids_partial[:5]:
    print('  Sample partial:')
    for c, missing in cids_partial[:5]:
        print(f'    cid={c}: missing {missing}')

# 缺失的 cid 区间 (alt-art shared)
all_cids = list(range(0, 2098))
missing_cids = [c for c in all_cids if c not in cid_set]
print(f'\nCids NOT in .s (alt-art shared via pointer table): {len(missing_cids)}')
if missing_cids[:10]:
    print(f'  Sample: {missing_cids[:10]}...')

# 2. _xx 控制码分布
xx_byte_counter = Counter()
xx_total_bytes = 0
xx_control_examples = defaultdict(list)
for (cid, lang), bs in labels.items():
    if lang != 'xx':
        continue
    i = 0
    while i < len(bs):
        b = bs[i]
        xx_total_bytes += 1
        if b < 0xF0:
            xx_byte_counter[b] += 1
            if len(xx_control_examples[b]) < 3:
                # show context: ±3 bytes hex
                ctx_lo = max(0, i - 3)
                ctx_hi = min(len(bs), i + 4)
                ctx = ' '.join(f'{bs[k]:02X}' for k in range(ctx_lo, ctx_hi))
                xx_control_examples[b].append(f'cid={cid} pos={i}: ...{ctx}...')
        i += 1

print(f'\n=== _xx 区控制码分布 ({xx_total_bytes} bytes total) ===')
for b in sorted(xx_byte_counter.keys()):
    cnt = xx_byte_counter[b]
    print(f'  byte=0x{b:02X}  {cnt:6d} occurrences')
    for ex in xx_control_examples[b][:1]:
        print(f'      {ex}')

# 3. 拉丁语区 CP1252 round-trip
print('\n=== EN/DE/FR/IT/ES 区 CP1252 round-trip 验证 ===')
non_cp1252 = defaultdict(list)
total_lang = 0
ok_lang = 0
high_bytes_distribution = Counter()
for (cid, lang), bs in labels.items():
    if lang == 'xx':
        continue
    total_lang += 1
    # try cp1252 → utf-8 → cp1252
    try:
        s = bs.decode('cp1252')
        re_enc = s.encode('cp1252')
        if re_enc == bs:
            ok_lang += 1
        else:
            non_cp1252[lang].append((cid, bs[:60].hex()))
    except Exception as e:
        non_cp1252[lang].append((cid, str(e)))
    # collect high-byte usage
    for b in bs:
        if b >= 0x80:
            high_bytes_distribution[b] += 1

print(f'Lang labels total: {total_lang}, CP1252 round-trip OK: {ok_lang}')
if total_lang != ok_lang:
    print(f'⚠ Failures by lang:')
    for lang, failures in non_cp1252.items():
        print(f'  {lang}: {len(failures)} fail')
        for cid, info in failures[:3]:
            print(f'    cid={cid}: {info}')

print(f'\nHigh bytes (>= 0x80) distribution in lang text (top 20):')
for b, cnt in high_bytes_distribution.most_common(20):
    try:
        ch = bytes([b]).decode('cp1252')
        ch_repr = repr(ch)
    except:
        ch_repr = '<undefined>'
    print(f'  0x{b:02X}: {cnt:6d}  → cp1252 {ch_repr}')

# 4. alt-art 共享 (相同 bytes 但不同 cid 的 _xx)
print('\n=== alt-art 共享检测 (相同 _xx bytes 的 cid 簇) ===')
xx_to_cids = defaultdict(list)
for (cid, lang), bs in labels.items():
    if lang == 'xx' and bs and bs != b'\x00\x00':
        xx_to_cids[bs].append(cid)
shared = {bs: cids for bs, cids in xx_to_cids.items() if len(cids) > 1}
print(f'Distinct non-empty _xx contents: {len(xx_to_cids)}')
print(f'Contents shared by ≥2 cids: {len(shared)}')
if shared:
    sample = list(shared.items())[:5]
    for bs, cids in sample:
        preview = bs[:30].hex()
        print(f'  cids {cids}: {preview}...')

# 5. Summary 写入 JSON
summary = {
    'total_labels': len(labels),
    'cids_present': sorted(cid_set),
    'cids_missing_in_s': missing_cids,
    'cids_partial_lang': [(c, ms) for c, ms in cids_partial],
    'xx_control_codes': {f'0x{b:02X}': xx_byte_counter[b] for b in sorted(xx_byte_counter.keys())},
    'lang_cp1252_roundtrip_ok': ok_lang == total_lang,
    'lang_cp1252_failures': {l: [(c, str(f)) for c, f in fs] for l, fs in non_cp1252.items()},
    'shared_xx_count': len(shared),
}
with open('tools/jp-decode/review/phase0_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print('\nwrote tools/jp-decode/review/phase0_summary.json')
