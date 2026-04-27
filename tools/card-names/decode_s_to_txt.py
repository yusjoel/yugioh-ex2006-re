"""
Decoder: data/card-names.s → text/card-names/{ja,en,de,fr,it,es}.txt + pointer-table.txt

读取现有 .s 全部 12324 个 master label, 解码为 UTF-8 文本按 lang 分文件.
另外 parse pointer table → text/card-names/pointer-table.txt (cid → master_cid).

源文件结构 (data/card-names.s):
  card_names_table:
    card_name_0001_xx: .ascii "..."
    card_name_0001_en: .ascii "Blue-Eyes White Dragon\\0\\0"
    ...
  card_name_pointer_table:
    name_offsets 0001    @ Blue-Eyes White Dragon
    name_offsets 0001    @ Blue-Eyes White Dragon (alt-art)
"""
import re
import json
import os
from pathlib import Path

OUT_DIR = Path('text/card-names')
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


CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


def decode_ja(bs):
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
    return bs.decode('cp1252')


def strip_trailing_nulls(bs):
    return bs.rstrip(b'\x00')


# Parse .s — 1) labels, 2) pointer table
src = open('data/card-names.s', encoding='latin-1').read()

# 1. (cid, lang) → bytes
label_pat = re.compile(r'card_name_(\d+)_(xx|ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
labels = {}
for m in label_pat.finditer(src):
    cid = int(m.group(1))
    lang = m.group(2)
    labels[(cid, lang)] = decode_octal_string(m.group(3))
print(f'Parsed {len(labels)} labels from .s')

# 2. master comments: from `card_name_NNNN:  @ Master Name`
master_comment = {}
mc_pat = re.compile(r'^card_name_(\d+):\s*@\s*(.*)$', re.MULTILINE)
for m in mc_pat.finditer(src):
    master_comment[int(m.group(1))] = m.group(2).strip()

# 3. Pointer table
pt_start = src.find('card_name_pointer_table:')
assert pt_start >= 0, 'card_name_pointer_table not found'
pt_section = src[pt_start:]
pt_pat = re.compile(r'name_offsets\s+(\d+)\s*@\s*(.*)$', re.MULTILINE)
pt_entries = []
for m in pt_pat.finditer(pt_section):
    label_cid = int(m.group(1))
    comment = m.group(2).strip()
    pt_entries.append((label_cid, comment))
print(f'Parsed {len(pt_entries)} pointer table entries')
assert len(pt_entries) == 2098, f'expected 2098, got {len(pt_entries)}'


# 写出 6 lang txt
LANGS = ['ja', 'en', 'de', 'fr', 'it', 'es']
ORIG_LANG = {'ja': ('xx', 'ja'), 'en': ('en',), 'de': ('de',), 'fr': ('fr',), 'it': ('it',), 'es': ('es',)}

for new_lang in LANGS:
    orig = ORIG_LANG[new_lang]
    entries = sorted(
        [(cid, bs) for (cid, lg), bs in labels.items() if lg in orig],
        key=lambda x: x[0]
    )
    out = OUT_DIR / f'{new_lang}.txt'
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'@ text/card-names/{new_lang}.txt — {len(entries)} entries\n')
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
            f.write('\n')
    size = os.path.getsize(out)
    print(f'  {out}: {len(entries)} entries, {size:,} B')

# 写 pointer-table.txt
pt_out = OUT_DIR / 'pointer-table.txt'
with open(pt_out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('@ Pointer Table mapping: cid → master_cid (4 digits each)\n')
    f.write('@ Each cid in [0, 2097] maps to a master_cid that has actual label data.\n')
    f.write('@ When cid != master_cid, this is alt-art / shared name.\n')
    f.write('@ Format: cid master_cid english_name_comment\n')
    f.write('@\n')
    for cid, (master_cid, comment) in enumerate(pt_entries):
        f.write(f'{cid:04d} {master_cid:04d} {comment}\n')
print(f'  {pt_out}: {len(pt_entries)} entries')

print('\ndecode finished')
