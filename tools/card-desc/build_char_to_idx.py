"""
仅扫 data/card-descriptions.s 的 _xx/_ja label, 统计每个 (UTF-8 char) 实际使用的 idx,
取最高频 idx 作为 card-desc encoder 的 char_to_idx. 写入 tools/card-desc/char_to_idx.json.

per-dataset (card-desc / card-names / deck-strings) 各有自己的 char_to_idx, 因为
同一 ASCII 字符 (如 '@') 在 card-desc 是单字节控制码, 在 card-names 可能是 JA-encoded
2-byte (idx=42), 编码语义不同.
"""
import re
import json
from collections import Counter, defaultdict
from pathlib import Path


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


def scan_ascii_label_data(path: Path, label_re: re.Pattern):
    """扫 .s 找 _xx/_ja label 的 .ascii bytes, yield (idx, count)."""
    if not path.exists():
        return
    txt = path.read_text(encoding='latin-1')
    for m in label_re.finditer(txt):
        if m.group(1) not in ('xx', 'ja'):
            continue
        bs = decode_octal_string(m.group(2))
        payload = bs.rstrip(b'\x00')
        i = 0
        while i + 1 < len(payload):
            hi, lo = payload[i], payload[i + 1]
            if hi >= 0xF0:
                idx = ((hi & 0xF) << 7) | (lo & 0x7F)
                yield idx
            i += 2


def scan_byte_lines(path: Path):
    """扫 .s 形如 `.byte 0xXX, 0xXX, ...` 的行 (deck-strings.s 用), yield idx."""
    if not path.exists():
        return
    line_pat = re.compile(r'^\s*\.byte\s+(.*)$', re.MULTILINE)
    bytehex_pat = re.compile(r'0x([0-9A-Fa-f]{2})')
    txt = path.read_text(encoding='latin-1')
    for m in line_pat.finditer(txt):
        bs = bytes(int(h, 16) for h in bytehex_pat.findall(m.group(1)))
        i = 0
        while i + 1 < len(bs):
            hi, lo = bs[i], bs[i + 1]
            if hi >= 0xF0:
                idx = ((hi & 0xF) << 7) | (lo & 0x7F)
                yield idx
            i += 2


# 统计 char → idx 频率 (仅 card-descriptions.s)
char_idx_counter = defaultdict(Counter)

desc_pat = re.compile(r'card_desc_\d+_(xx|ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
for idx in scan_ascii_label_data(Path('data/card-descriptions.s'), desc_pat):
    ch = CT.get(idx)
    if ch:
        char_idx_counter[ch][idx] += 1

# 不做 codetable 兜底: ASCII 字符 ('@', '1', 'a' 等) 在 JA 数据中可能既存在为
# 单字节 0x40/0x31/0x61 控制码, 也存在为 codetable idx (e.g. F0 AA = idx 42 = '@').
# 兜底会破坏现有 ASCII pass-through 语义. 仅根据实际观察到的 (hi >= 0xF0) 出现来填.
# 后果: 若 .txt 编辑加了从未出现的新 JA 字符 → encoder 会显式报错, 须手动补 char_to_idx.

# 取每个 char 最高频 idx
char_to_idx = {}
ambiguous = []
for ch, counts in char_idx_counter.items():
    most_common = counts.most_common(1)[0]
    char_to_idx[ch] = most_common[0]
    if len(counts) > 1:
        ambiguous.append((ch, dict(counts)))

print(f'Total distinct chars: {len(char_to_idx)}')
print(f'Chars with multiple idx variants (in actual data): {len(ambiguous)}')
for ch, cnts in ambiguous[:10]:
    print(f'  {ch!r}: {cnts}')

with open('tools/card-desc/char_to_idx.json', 'w', encoding='utf-8') as f:
    json.dump({ch: idx for ch, idx in char_to_idx.items()}, f, ensure_ascii=False, indent=2)
print('\nwrote tools/card-desc/char_to_idx.json')
