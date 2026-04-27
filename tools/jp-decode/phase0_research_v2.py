"""
Phase 0 v2: 修正控制码统计 (按 2-byte 对齐扫描 _xx)
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

pattern = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
labels = {}
for m in pattern.finditer(txt):
    cid = int(m.group(1))
    lang = m.group(2)
    bs = decode_octal_string(m.group(3))
    labels[(cid, lang)] = bs

# 解析 _xx 为 token 流: 字符对 (hi >= 0xF0) | 控制码对 (hi < 0xF0)
# 假设全部 stream 是 2-byte 对齐的
xx_char_pair_count = 0  # hi >= 0xF0
xx_control_pair_count = 0  # hi < 0xF0
xx_odd_length = 0  # 奇数长度 (理论上不应出现)
control_pair_counter = Counter()  # (hi, lo) -> count
control_examples = defaultdict(list)
trailing_zero_padding = Counter()  # 多少个 \0 byte 在末尾

for (cid, lang), bs in labels.items():
    if lang != 'xx':
        continue
    # trailing zero count
    tz = 0
    for b in reversed(bs):
        if b == 0:
            tz += 1
        else:
            break
    trailing_zero_padding[tz] += 1
    # main payload (excluding trailing zeros)
    payload = bs[:len(bs) - tz] if tz > 0 else bs
    if len(payload) % 2 != 0:
        xx_odd_length += 1
        continue
    i = 0
    while i + 1 < len(payload):
        hi, lo = payload[i], payload[i + 1]
        if hi >= 0xF0:
            xx_char_pair_count += 1
        else:
            xx_control_pair_count += 1
            control_pair_counter[(hi, lo)] += 1
            if len(control_examples[(hi, lo)]) < 3:
                ctx_lo = max(0, i - 4)
                ctx_hi = min(len(payload), i + 6)
                ctx = ' '.join(f'{payload[k]:02X}' for k in range(ctx_lo, ctx_hi))
                control_examples[(hi, lo)].append(f'cid={cid} pos={i}: ...{ctx}...')
        i += 2

print(f'_xx 区 (按 2-byte 对齐扫描):')
print(f'  字符对 (hi >= 0xF0):  {xx_char_pair_count}')
print(f'  控制码对 (hi < 0xF0): {xx_control_pair_count}')
print(f'  奇数长度记录:         {xx_odd_length}')

print(f'\n=== 末尾 \\0 padding 分布 ===')
for tz, cnt in sorted(trailing_zero_padding.items()):
    print(f'  trailing {tz} zero(s): {cnt} entries')

print(f'\n=== _xx 控制码对分布 (top 30) ===')
for (hi, lo), cnt in control_pair_counter.most_common(30):
    print(f'  {hi:02X} {lo:02X}  {cnt:5d}')
    for ex in control_examples[(hi, lo)][:1]:
        print(f'      {ex}')

# 也看 5 拉丁语 lang 的控制码
print(f'\n=== 5 lang 区 byte < 0x20 控制字符 ===')
lang_control = defaultdict(Counter)
for (cid, lang), bs in labels.items():
    if lang == 'xx':
        continue
    for b in bs:
        if b < 0x20 or b == 0x7F:
            lang_control[lang][b] += 1
for lang in ['en', 'de', 'fr', 'it', 'es']:
    if lang_control[lang]:
        print(f'  {lang}: {dict(sorted(lang_control[lang].items()))}')
    else:
        print(f'  {lang}: (no control bytes)')
