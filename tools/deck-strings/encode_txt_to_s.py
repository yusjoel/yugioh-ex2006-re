"""
Encoder: text/deck-strings/ja.txt → data/deck-strings.s

输出与原 export_deck_strings.py 相同的 .s 结构:
  deck_str_xx_sd:
    .byte 0xXX, ...   (7 SD JA names)
    ...
    .incbin "roms/2343.gba", 0x1DBF081, 0x2CDF
  deck_str_xx_opp:
    .byte 0xXX, ...   (25 OPP JA names)
    ...
    .incbin "roms/2343.gba", 0x1DC1EF1, 0x272F
"""
import re
import json
from pathlib import Path

SRC = Path('text/deck-strings/ja.txt')
OUT = Path('data/deck-strings.s')

# ROM 偏移常数 (与 export_deck_strings.py 同步)
SD_START = 0x1DBF01A
SD_GAP_START = 0x1DBF081
SD_GAP_LEN = 0x2CDF
OPP_START = 0x1DC1D60
OPP_GAP_START = 0x1DC1EF1
OPP_GAP_LEN = 0x272F

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
            out.append(hi)
            out.append(lo)
        else:
            cp = ord(ch)
            if cp > 0xFF:
                raise ValueError(f'char {ch!r} (U+{cp:04X}) not in char_to_idx, not ASCII')
            out.append(cp)
    return bytes(out)


def parse_txt(path):
    """parse =SD_NN= pad=N / =OPP_NN= pad=N entries → list[(kind, idx, pad, text)]."""
    content = open(path, encoding='utf-8').read()
    pat = re.compile(r'^=(SD|OPP)_(\d+)=\s*pad=(\d+)\s*\n', re.MULTILINE)
    matches = list(pat.finditer(content))
    out = []
    for i, m in enumerate(matches):
        kind = m.group(1)
        idx = int(m.group(2))
        pad = int(m.group(3))
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[body_start:body_end].rstrip('\n')
        out.append((kind, idx, pad, body))
    return out


entries = parse_txt(SRC)
sd = [e for e in entries if e[0] == 'SD']
opp = [e for e in entries if e[0] == 'OPP']
print(f'SD: {len(sd)} entries')
print(f'OPP: {len(opp)} entries')
assert len(sd) == 7 and len(opp) == 25
assert sorted(e[1] for e in sd) == list(range(7))
assert sorted(e[1] for e in opp) == list(range(25))

sd.sort(key=lambda e: e[1])
opp.sort(key=lambda e: e[1])


def fmt_byte_line(indent, data):
    return indent + '.byte ' + ', '.join(f'0x{b:02X}' for b in data)


lines = []
lines.append('@ 卡组名字符串表')
lines.append('@ 由 tools/deck-strings/encode_txt_to_s.py 从 text/deck-strings/ja.txt 生成')
lines.append('@')
lines.append(f'@ ROM 文件偏移范围: 0x{SD_START:X} ~ 0x1DFC852')
lines.append('@ 字符串表基址（文件偏移）: 0x1DB9C10')
lines.append('@')
lines.append('@ 6 lang: XX(JA)/EN/DE/FR/IT/ES; 当前 .s 仅 JA 部分, 其他 5 lang 在 game-strings 区')
lines.append('@ 各语言分两组：SD (7 条) + OPP (25 条)')
lines.append('')
lines.append('@ ========================================================')
lines.append('@ JA - 预组/初始卡组名')
lines.append(f'@ ROM 偏移: 0x{SD_START:X} ~ 0x{SD_GAP_START:X}  ({SD_GAP_START - SD_START} 字节)')
lines.append('@ ========================================================')
lines.append('deck_str_xx_sd:')
lines.append('')

for kind, idx, pad, text in sd:
    name_en = SD_NAMES[idx]
    lines.append(f'\t@ {name_en}')
    data = encode_ja(text)
    if data:
        lines.append(fmt_byte_line('\t', data))
    if pad > 0:
        lines.append(fmt_byte_line('\t', b'\0' * pad))
    lines.append('')

lines.append(f'\t.incbin "roms/2343.gba", 0x{SD_GAP_START:X}, 0x{SD_GAP_LEN:X}')
lines.append('')
lines.append('@ ========================================================')
lines.append('@ JA - 对手卡组名')
lines.append(f'@ ROM 偏移: 0x{OPP_START:X} ~ 0x{OPP_GAP_START:X}  ({OPP_GAP_START - OPP_START} 字节)')
lines.append('@ ========================================================')
lines.append('deck_str_xx_opp:')
lines.append('')

for i, (kind, idx, pad, text) in enumerate(opp):
    name_en = OPP_NAMES[idx]
    lines.append(f'\t@ {name_en}')
    data = encode_ja(text)
    if data:
        lines.append(fmt_byte_line('\t', data))
    if pad > 0:
        lines.append(fmt_byte_line('\t', b'\0' * pad))
    if i < len(opp) - 1:
        lines.append('')

lines.append(f'\t.incbin "roms/2343.gba", 0x{OPP_GAP_START:X}, 0x{OPP_GAP_LEN:X}'
             f'  @ 间隙：直到游戏文本开始（0x{OPP_GAP_START + OPP_GAP_LEN - 1:X}）')
lines.append('')
lines.append('@ 后续内容见 data/game-strings.s（0x1DC4620 起）')

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')
print(f'wrote {OUT}')
