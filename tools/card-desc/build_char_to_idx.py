"""
扫原始 .s 的 _xx label, 为每个 (UTF-8 char) 统计实际使用的 (hi,lo) → idx,
取最高频 idx 作为 encoder 的 char_to_idx. 写入 char_to_idx.json.

控制字节 ASCII (@, 4, 5, 7) 不走 codetable, 单独标记为 None.
重复 codetable entry 中, 选最常用的 idx (其他 idx 即使 char 相同也忽略).
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
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c))
            i += 1
    return bytes(result)


CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

orig_path = r'C:\Users\yushj\AppData\Local\Temp\orig_card_descs.s'
txt = open(orig_path, encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')

# 统计每个 char 在 _xx 实际使用的 idx 频率
char_idx_counter = defaultdict(Counter)
for m in pat.finditer(txt):
    if m.group(2) != 'xx':
        continue
    bs = decode_octal_string(m.group(3))
    payload = bs.rstrip(b'\x00')
    i = 0
    while i + 1 < len(payload):
        hi, lo = payload[i], payload[i + 1]
        if hi >= 0xF0:
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            ch = CT.get(idx)
            if ch:
                char_idx_counter[ch][idx] += 1
            i += 2
        else:
            # 单字节控制码 (40 NN 模式), 跳过本对的非对齐 1 字节
            # 实际上 _xx 中控制码 始终是 40 NN 对齐的 2 字节 (0x40, 0x34/0x35/0x37)
            # 所以这里 i+=2 跳过整对
            i += 2

# 取每个 char 最高频 idx
char_to_idx = {}
ambiguous = []
for ch, counts in char_idx_counter.items():
    most_common = counts.most_common(1)[0]
    char_to_idx[ch] = most_common[0]
    if len(counts) > 1:
        ambiguous.append((ch, dict(counts)))

print(f'Total distinct chars used in _xx: {len(char_to_idx)}')
print(f'Chars with multiple idx variants: {len(ambiguous)}')
for ch, cnts in ambiguous[:20]:
    print(f'  {ch!r}: {cnts}')

with open('tools/card-desc/char_to_idx.json', 'w', encoding='utf-8') as f:
    # 写成 idx → char 形式 (JSON key 必须 string, 这里用 char 作 key)
    json.dump({ch: idx for ch, idx in char_to_idx.items()}, f, ensure_ascii=False, indent=2)
print('\nwrote tools/card-desc/char_to_idx.json')
