"""
对 13 个有 hit 的低/中信心 idx，从 card-descriptions.s 中 dump 出现位置的上下文（前后 12 字），
用当前 codetable 解码非目标字符，目标 idx 显示为 [?TARGET]。
"""
import json
import re
from collections import defaultdict


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


# Load codetable
ct = json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx']
ct = {int(k): v for k, v in ct.items()}

# Load card xx
with open('data/card-descriptions.s', encoding='latin-1') as f:
    txt = f.read()

xx_pattern = re.compile(r'card_desc_(\d+)_xx:\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
cid_to_seq = {}
for m in xx_pattern.finditer(txt):
    cid = int(m.group(1))
    bs = decode_octal_string(m.group(2))
    seq = []
    i = 0
    while i + 1 < len(bs):
        idx = code_to_idx(bs[i], bs[i + 1])
        seq.append(idx if idx is not None else None)
        i += 2
    cid_to_seq[cid] = seq

# Targets (drop those with 0 hits — handled separately by re-render)
TARGETS = {
    1: '、', 2: '゜', 1560: '喪',
    326: '囲', 438: '套', 729: '詩',
    806: '今', 894: '糸', 922: '識',
    1056: '桑', 1080: '浸', 1205: '麦',
    1888: '爻',
}


def render_text(seq, target_idx, mark_pos):
    """Decode seq to Japanese text. Mark target at mark_pos with [?T:guess]."""
    out = []
    for i, idx in enumerate(seq):
        if idx is None:
            out.append('?')
            continue
        if i == mark_pos:
            out.append(f'【?{idx}】')
            continue
        ch = ct.get(idx, f'<{idx}>')
        out.append(ch if ch else f'<{idx}>')
    return ''.join(out)


# For each target, dump up to 5 cards' descriptions with target highlighted
report = []
for tidx in sorted(TARGETS.keys()):
    locs = []
    for cid, seq in cid_to_seq.items():
        for pos, item in enumerate(seq):
            if item == tidx:
                locs.append((cid, pos))
    if not locs:
        continue

    report.append(f'\n=== idx={tidx} (我猜 {TARGETS[tidx]}) — {len(locs)} hits ===')
    # Dedup by cid (some cards have multiple occurrences)
    seen_cid = set()
    samples = []
    for cid, pos in locs:
        if cid in seen_cid and len(samples) >= 3:
            continue
        if len(samples) >= 5:
            break
        seen_cid.add(cid)
        samples.append((cid, pos))

    for cid, pos in samples:
        seq = cid_to_seq[cid]
        # ±15 char window
        lo = max(0, pos - 15)
        hi = min(len(seq), pos + 16)
        context = render_text(seq[lo:hi], tidx, pos - lo)
        report.append(f'  cid={cid:4d} (idx pos {pos}/{len(seq)}): ...{context}...')

text = '\n'.join(report)
print(text)
with open('tools/jp-decode/review/lowconf_contexts.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('\nwrote tools/jp-decode/review/lowconf_contexts.txt')
