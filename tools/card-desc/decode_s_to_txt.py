"""
Decoder: data/card-descriptions.s → text/card-desc/{ja,en,de,fr,it,es}.txt

读取现有 .s 的全部 12324 个 label, 解码为 UTF-8 文本, 按 lang 分文件:
  - ja: ROM 自定义 2-byte 编码 → codetable → UTF-8 char
  - en/de/fr/it/es: CP1252 单字节 → UTF-8 char

源文件格式:
  =0001=
  @5高い攻撃力を誇る伝説のドラゴン。

  =0005=
  @5かよわいエルフだが、聖なる力で身を守りとても守備が高い。
"""
import re
import json
import os
from pathlib import Path

OUT_DIR = Path('text/card-desc')
OUT_DIR.mkdir(parents=True, exist_ok=True)


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


# Load codetable
CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

# Trained default idx per char (built by build_char_to_idx.py)
CHAR_DEFAULT_IDX = json.loads(
    open('tools/card-desc/char_to_idx.json', encoding='utf-8').read()
)
# {char: idx, ...}


def decode_ja(bs):
    """Decode JA bytes to UTF-8 string. (hi, lo) pair where hi >= 0xF0 → idx → char.
    Bytes with hi < 0xF0 are treated as raw ASCII (control codes like @7/@5/@4).
    Codetable is strictly 1-to-1 (no duplicates), so no annotation needed."""
    out = []
    i = 0
    while i < len(bs):
        b = bs[i]
        if b >= 0xF0 and i + 1 < len(bs):
            hi, lo = b, bs[i + 1]
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            ch = CT.get(idx)
            if ch is None:
                raise ValueError(f'idx {idx} not in codetable (hi={hi:02X} lo={lo:02X})')
            out.append(ch)
            i += 2
        else:
            out.append(chr(b))
            i += 1
    return ''.join(out)


def decode_lang(bs):
    """CP1252 → UTF-8."""
    return bs.decode('cp1252')


def strip_trailing_nulls(bs):
    return bs.rstrip(b'\x00')


# Parse .s
src = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')

# (cid, lang) → bytes
labels = {}
for m in pat.finditer(src):
    cid = int(m.group(1))
    lang = m.group(2)
    labels[(cid, lang)] = decode_octal_string(m.group(3))

print(f'Parsed {len(labels)} labels from .s')

# 按 lang 分组写出
LANGS = ['ja', 'en', 'de', 'fr', 'it', 'es']
ORIG_LANG = {'ja': ('xx', 'ja'), 'en': ('en',), 'de': ('de',), 'fr': ('fr',), 'it': ('it',), 'es': ('es',)}

for new_lang in LANGS:
    orig = ORIG_LANG[new_lang]
    # Collect entries for this lang, sorted by cid
    entries = sorted(
        [(cid, bs) for (cid, lg), bs in labels.items() if lg in orig],
        key=lambda x: x[0]
    )
    out = OUT_DIR / f'{new_lang}.txt'
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'@ text/card-desc/{new_lang}.txt — {len(entries)} entries\n')
        f.write(f'@ Format: =CID= header (4-digit), then content lines.\n')
        f.write(f'@ Trailing \\0 padding handled by encoder; do NOT add manually.\n\n')
        for cid, bs in entries:
            payload = strip_trailing_nulls(bs)
            if new_lang == 'ja':
                text = decode_ja(payload) if payload else ''
            else:
                text = decode_lang(payload) if payload else ''
            f.write(f'={cid:04d}=\n')
            f.write(text)
            if not text.endswith('\n'):
                f.write('\n')
            f.write('\n')  # blank separator line
    size = os.path.getsize(out)
    print(f'  {out}: {len(entries)} entries, {size:,} B')

print('\ndecode finished')
