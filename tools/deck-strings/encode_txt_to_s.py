"""
Encoder: text/deck-strings/ja.txt → data/deck-strings.s

deck-strings.s = JA UI text 全区段 (0x1DB9C10 ~ 0x1DC4620, 1597 条).
ja.txt 中 SD/OPP 名作 alias label 标注 (=SD_NN=, =OPP_NN=) 替代 sequential idx.
"""
import re
import json
from pathlib import Path

SRC = Path('text/deck-strings/ja.txt')
OUT = Path('data/deck-strings.s')

JA_START = 0x1DB9C10
JA_END = 0x1DC4620
LEADING_PAD = 2  # 区段开头 2 字节 \0 (固定)

SD_NAMES = [
    'Starter Deck', "Dragon's Roar", 'Zombie Madness', 'Blazing Destruction',
    'Fury From the Deep', "Warrior's Triumph", "Spellcaster's Judgement",
]
OPP_NAMES = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'REDD', 'Vampire Genesis', 'Infernal Flame Emperor', 'Ocean Dragon Lord',
    'Helios Duo Megiste', 'Gilford the Legend', 'Dark Eradicator Warlock',
    'Guardian Exode', 'Goldd', 'Electrum', 'Raviel', 'Horus', 'Stronghold',
    'Sacred Phoenix', 'Cyber End Dragon',
]


char_to_idx = json.loads(
    open('tools/deck-strings/char_to_idx.json', encoding='utf-8').read()
)


def encode_ja(text):
    out = bytearray()
    for ch in text:
        idx = char_to_idx.get(ch)
        if idx is not None:
            hi = ((idx >> 7) & 0xF) | 0xF0
            lo = (idx & 0x7F) | 0x80
            out.append(hi); out.append(lo)
        else:
            cp = ord(ch)
            if cp > 0xFF:
                raise ValueError(f'char {ch!r} (U+{cp:04X}) not in char_to_idx')
            out.append(cp)
    return bytes(out)


def parse_txt(path):
    """Parse =NNNNN= / =SD_NN= / =OPP_NN= entries.
    Returns: list of (label_str, pad, text)."""
    # newline='' 防 Windows 文本模式把 \r\n 译成 \n (会吃掉数据中字面 \r)
    content = open(path, encoding='utf-8', newline='').read()
    # 注意: 用 [ \t] 而非 \s, 避免 \n 被吞 (会让 body 第一行 (以 @ 开头) 被误认 comment)
    pat = re.compile(
        r'^=(SD_\d+|OPP_\d+|\d{5})=[ \t]*pad=(\d+)(?:[ \t]*@[^\n]*)?[ \t]*\n',
        re.MULTILINE,
    )
    matches = list(pat.finditer(content))
    out = []
    for i, m in enumerate(matches):
        label_id = m.group(1)
        pad = int(m.group(2))
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[body_start:body_end].rstrip('\n')
        out.append((label_id, pad, body))
    return out


entries = parse_txt(SRC)
print(f'Parsed {len(entries)} entries from {SRC}')

# 校验: 应有 1597 entries (NNNNN_seq + 32 named)
assert len(entries) == 1598, f'expected 1598, got {len(entries)}'

# 验证 sequential idx 连续 + named labels 完整
seq_ids = [int(e[0]) for e in entries if e[0].isdigit()]
sd_ids = [int(e[0][3:]) for e in entries if e[0].startswith('SD_')]
opp_ids = [int(e[0][4:]) for e in entries if e[0].startswith('OPP_')]
print(f'Sequential: {len(seq_ids)}, SD: {len(sd_ids)}, OPP: {len(opp_ids)}')
assert sorted(sd_ids) == list(range(7))
assert sorted(opp_ids) == list(range(25))

# 字节大小检查
total_bytes = LEADING_PAD
for label, pad, text in entries:
    data = encode_ja(text)
    total_bytes += len(data) + pad
print(f'Encoded total bytes: {total_bytes} (expected {JA_END - JA_START} = {JA_END - JA_START}B)')


def fmt_byte_line(indent, data):
    return indent + '.byte ' + ', '.join(f'0x{b:02X}' for b in data)


lines = []
lines.append('@ JA UI 字符串表 (历史名 deck-strings, 实为 JA 全 UI text)')
lines.append('@ 由 tools/deck-strings/encode_txt_to_s.py 从 text/deck-strings/ja.txt 生成')
lines.append('@')
lines.append(f'@ ROM 偏移: 0x{JA_START:X} ~ 0x{JA_END:X}  ({JA_END-JA_START} 字节, 1597 条)')
lines.append(f'@ STRING_TABLE_BASE = 0x{JA_START:X}')
lines.append('@')
lines.append('@ Pointer table SD/OPP slot[5] = JA pointer:')
lines.append('@   SD: 0x4CAC, 7 槽 × 24B → deck_str_xx_sd_NN')
lines.append('@   OPP: 0x815C, 25 槽 × 24B → deck_str_xx_opp_NN')
lines.append('')
lines.append('@ ============================================================')
lines.append('deck_str_xx:')
lines.append('')
lines.append(f'\t.zero {LEADING_PAD}')
lines.append('')

for label, pad, text in entries:
    if label.startswith('SD_'):
        n = int(label[3:])
        lname = f'deck_str_xx_sd_{n:02d}'
        comment = SD_NAMES[n]
    elif label.startswith('OPP_'):
        n = int(label[4:])
        lname = f'deck_str_xx_opp_{n:02d}'
        comment = OPP_NAMES[n]
    else:
        n = int(label)
        lname = f'deck_str_xx_{n:05d}'
        comment = ''
    if comment:
        lines.append(f'{lname}:  @ {comment}')
    else:
        lines.append(f'{lname}:')
    data = encode_ja(text)
    for k in range(0, len(data), 16):
        lines.append(fmt_byte_line('\t', data[k:k+16]))
    if pad == 1:
        lines.append('\t.byte 0x00')
    elif pad >= 2:
        lines.append(f'\t.zero {pad}')
    lines.append('')

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')
print(f'wrote {OUT}')
