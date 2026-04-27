"""检查每条记录末尾 \\0 padding 分布"""
import re
from collections import Counter


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


txt = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
labels = {}
for m in pat.finditer(txt):
    labels[(int(m.group(1)), m.group(2))] = decode_octal_string(m.group(3))

print('每条记录末尾 \\0 数量分布 (按 lang):')
for lang in ['xx', 'en', 'de', 'fr', 'it', 'es']:
    pad = Counter()
    for (cid, ln), bs in labels.items():
        if ln != lang:
            continue
        tz = 0
        for b in reversed(bs):
            if b == 0:
                tz += 1
            else:
                break
        pad[tz] += 1
    print(f'  {lang}: {dict(sorted(pad.items()))}')

# 拉丁语区: 是否 总长偶数 且 末尾 ≥1 \0?
print('\n拉丁语区 padding 与总长奇偶性关系:')
for lang in ['en', 'de', 'fr', 'it', 'es']:
    pad_len = Counter()  # (trailing_zeros, total_len_even)
    for (cid, ln), bs in labels.items():
        if ln != lang:
            continue
        tz = 0
        for b in reversed(bs):
            if b == 0:
                tz += 1
            else:
                break
        even = (len(bs) % 2 == 0)
        pad_len[(tz, 'even' if even else 'odd')] += 1
    print(f'  {lang}: {dict(sorted(pad_len.items()))}')

# 解释: padding 是为了 2-byte 对齐到下一条 label
# 即 strip \0 后 数据长度奇 -> 加 1 个 \0 终止 + 1 个 padding (共 2 byte)
#                数据长度偶 -> 加 2 个 \0 (终止 + alignment)
# 等价于: padding 总是把记录长度补到偶数, 然后必有 \0 终止
print('\n验证规则: 去掉所有末尾 \\0 后, 长度必须能被 2 整除 (or 0):')
for lang in ['xx', 'en', 'de', 'fr', 'it', 'es']:
    bad = 0
    for (cid, ln), bs in labels.items():
        if ln != lang:
            continue
        # strip trailing zeros
        stripped = bs.rstrip(b'\x00')
        if len(stripped) % 2 != 0:
            bad += 1
    print(f'  {lang}: {bad} entries with odd payload-length (after strip)')
