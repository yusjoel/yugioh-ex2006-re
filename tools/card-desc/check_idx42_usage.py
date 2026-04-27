"""检查 _xx 中 F0 AA (idx=42) 实际是否出现, 也检查所有 (hi=F0, lo=任意) 命中频率"""
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
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c))
            i += 1
    return bytes(result)


orig_path = r'C:\Users\yushj\AppData\Local\Temp\orig_card_descs.s'
txt = open(orig_path, encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')

# 统计 _xx 中每个 (hi, lo) 字符对的频率
pair_counter = Counter()
for m in pat.finditer(txt):
    if m.group(2) != 'xx':
        continue
    bs = decode_octal_string(m.group(3))
    payload = bs.rstrip(b'\x00')
    i = 0
    while i + 1 < len(payload):
        hi, lo = payload[i], payload[i + 1]
        # 控制码对 (hi=0x40 + 数字) 不算字符对
        if hi == 0x40 and 0x30 <= lo <= 0x39:
            i += 2
            continue
        pair_counter[(hi, lo)] += 1
        i += 2

# 检查 F0 AA (idx=42) 实际出现?
print(f'F0 AA (idx=42) hits in payload: {pair_counter.get((0xF0, 0xAA), 0)}')

# 检查其他冲突字符 idx 的 (hi, lo) 命中
import json
ct = {int(k): v for k, v in json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx'].items()}

# 每个映射到 ASCII 单字符的 idx, 检查它在 _xx 中是否真的被用过
ascii_mapped = []
for idx, ch in sorted(ct.items()):
    if ch and len(ch) == 1 and 0x20 <= ord(ch) <= 0x7E:
        ascii_mapped.append((idx, ch))

print(f'\n=== 所有 ASCII-mapped idx 在 _xx 中的实际出现频率 ===')
print(f'(出现 0 次说明 codetable 把这些 idx 错误指认为 ASCII char, 可以改为全角)')
for idx, ch in ascii_mapped:
    hi = ((idx >> 7) & 0xF) | 0xF0
    lo = (idx & 0x7F) | 0x80
    cnt = pair_counter.get((hi, lo), 0)
    print(f'  idx={idx:4d}  ({ch!r} → {hi:02X} {lo:02X})  hits={cnt}')
