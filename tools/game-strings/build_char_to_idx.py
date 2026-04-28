"""扫 text/game-strings/ja.txt 收集所有 JA 字符, 选 codetable 中 idx 构建 char_to_idx.

每个字符可能对应多个 idx (重复 glyph), 选最常用的.
ASCII control bytes (< 0x80) 不进 char_to_idx (encoder 直接 ord(ch)).
"""
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

# 反向: char → list of idx
ch_to_all_idx = defaultdict(list)
for idx, ch in CT.items():
    if ch:
        ch_to_all_idx[ch].append(idx)

# 扫 ja.txt 收集字符 + 频率
src = Path('text/game-strings/ja.txt').read_text(encoding='utf-8')

# 跳过 header (=NNNN= 头) 行, 只扫正文
counter = Counter()
for line in src.splitlines():
    if not line:
        continue
    if line.startswith('='):
        continue  # entry header
    if line.startswith('@ ') or line == '@':
        continue  # comment line (注: '@N' 是游戏文本色码, 非注释)
    for ch in line:
        # 不按 cp 截断: codetable 中可能有 ASCII (idx 40 = '&'), 必须能查到 idx
        # → 编码成 2B JA pair (而非 1B raw 0x26).
        counter[ch] += 1

# 为每个字符选 idx (codetable 已去重为 1-to-1).
# 不在 codetable 的字符 (如 ja.txt 中孤例 \x9e 0x8a 的 raw 字节透传) 跳过 — 由 encoder
# 走 raw byte 分支 (out.append(cp)) 直接写字节, 不需 char_to_idx 表.
char_to_idx = {}
for ch, freq in counter.items():
    candidates = ch_to_all_idx.get(ch)
    if not candidates:
        # raw byte 透传, 跳过 (encoder 处 cp <= 0xFF 直接写)
        continue
    char_to_idx[ch] = candidates[0]

print(f'Total distinct chars in game-strings JA: {len(char_to_idx)}')

OUT = Path('tools/game-strings/char_to_idx.json')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(char_to_idx, f, ensure_ascii=False, indent=2)
print(f'wrote {OUT}')
