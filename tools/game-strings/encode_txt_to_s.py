"""
Encoder: text/game-strings/{ja,en,de,fr,it,es}.txt → data/game-strings-{lang}.s

按 master pointer table row idx 重组每 lang.
- JA: .byte form, 自定义 2B JA + 1B ASCII control
- 5 lang: .ascii form, CP1252 单字节
- pad 沿用 .ascii 末尾捎带最多 2 个 \\0; 多余用 .zero N
"""
import os
import re
import json
import struct
from pathlib import Path

OUT_DIR = Path('data')

LANG_REGIONS = {
    # name: (region_start, region_end_exclusive)
    'ja': (0x1DB9C10, 0x1DC4620),
    'en': (0x1DC4620, 0x1DCF471),
    'de': (0x1DCF471, 0x1DDB7DE),
    'fr': (0x1DDB7DE, 0x1DE7CB7),
    'it': (0x1DE7CB7, 0x1DF3C66),
    'es': (0x1DF3C66, 0x1DFF9D2),
}

SD_FIRST_ROW = 655
OPP_FIRST_ROW = 1217
N_ROWS = 1642

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

JA_CHAR_TO_IDX = json.loads(
    open('tools/game-strings/char_to_idx.json', encoding='utf-8').read()
)


# --- 解析 txt ---------------------------------------------------------------

# 头格式: =NNNN= pad=N [(empty)] [@ 注释]
#   或:   =JA_EXTRA_NN= pad=N [@ 注释]
HEADER_RE = re.compile(
    r'^=(?P<id>\d{4}|JA_EXTRA_\d{2}|PRE)=[ \t]*pad=(?P<pad>\d+)'
    r'(?:[ \t]*\(empty\))?'
    r'(?:[ \t]*@[^\n]*)?[ \t]*\n',
    re.MULTILINE,
)


def parse_txt(path):
    """返回 list of (kind, num, pad, body_text). kind ∈ {'master','extra'}.
    body_text: header 后到下一 header 的内容, 但去掉 '@ ' / '@' 注释行 (entry 间的章节注释).
    """
    content = open(path, encoding='utf-8', newline='').read()
    matches = list(HEADER_RE.finditer(content))
    out = []
    for i, m in enumerate(matches):
        ident = m.group('id')
        pad = int(m.group('pad'))
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        raw = content[body_start:body_end]
        # 去注释行 ('@ ...' 或纯 '@'); 保留 '@N' 等游戏文本色码
        body_lines = []
        for ln in raw.split('\n'):
            if ln.startswith('@ ') or ln == '@':
                continue
            body_lines.append(ln)
        body = '\n'.join(body_lines).rstrip('\n')
        if ident == 'PRE':
            out.append(('pre', 0, pad, body))
        elif ident.startswith('JA_EXTRA_'):
            out.append(('extra', int(ident[9:]), pad, body))
        else:
            out.append(('master', int(ident), pad, body))
    return out


# --- 编码 -----------------------------------------------------------------

def encode_ja_text(text):
    out = bytearray()
    for ch in text:
        idx = JA_CHAR_TO_IDX.get(ch)
        if idx is not None:
            hi = ((idx >> 7) & 0xF) | 0xF0
            lo = (idx & 0x7F) | 0x80
            out.append(hi)
            out.append(lo)
        else:
            cp = ord(ch)
            if cp > 0xFF:
                raise ValueError(f'JA: char {ch!r} (U+{cp:04X}) not in char_to_idx')
            out.append(cp)
    return bytes(out)


def encode_5lang_text(text):
    return text.encode('cp1252')


def asm_escape_ascii(raw):
    """字节序列 → GAS .ascii 字面量内容 (CP1252 source)."""
    parts = []
    for b in raw:
        if   b == 0x22: parts.append('\\"')
        elif b == 0x5C: parts.append('\\\\')
        elif b == 0x0A: parts.append('\\n')
        elif b == 0x0D: parts.append('\\r')
        elif b == 0x09: parts.append('\\t')
        elif b == 0x00: parts.append('\\0')
        elif 0x20 <= b < 0x7F:  parts.append(chr(b))
        elif 0x80 <= b <= 0x9F:
            try:    parts.append(bytes([b]).decode('cp1252'))
            except (UnicodeDecodeError, ValueError):
                    parts.append(f'\\x{b:02x}')
        elif 0xA0 <= b <= 0xFF: parts.append(chr(b))
        else:                   parts.append(f'\\x{b:02x}')
    return ''.join(parts)


# --- 输出 .s --------------------------------------------------------------

def labels_for_master(lang, row_idx):
    """生成此 row 在该 lang 下的 label 列表 (主标签 + SD/OPP alias)."""
    primary = f'game_str_{lang}_{row_idx:04d}'
    aliases = []
    if SD_FIRST_ROW <= row_idx <= SD_FIRST_ROW + 6:
        n = row_idx - SD_FIRST_ROW
        aliases.append((f'game_str_{lang}_sd_{n:02d}', SD_NAMES[n]))
    if OPP_FIRST_ROW <= row_idx <= OPP_FIRST_ROW + 24:
        n = row_idx - OPP_FIRST_ROW
        aliases.append((f'game_str_{lang}_opp_{n:02d}', OPP_NAMES[n]))
    return primary, aliases


def emit_data_lines(data, pad, form):
    """生成一个 entry 的 data + pad 输出行 (无 label, 仅数据).
    form ∈ {'byte', 'ascii'}."""
    lines = []
    if form == 'ascii':
        # 5 lang: 把最多 2 个 \\0 捎进 .ascii, 多余用 .zero
        nulls_in_ascii = min(pad, 2)
        if data or nulls_in_ascii:
            payload = data + b'\x00' * nulls_in_ascii
            lines.append(f'\t.ascii "{asm_escape_ascii(payload)}"')
        rest = pad - nulls_in_ascii
        if rest == 1:
            lines.append('\t.byte 0x00')
        elif rest >= 2:
            lines.append(f'\t.zero {rest}')
        if not data and not pad:
            pass  # 0-byte entry, pad=0, 罕见
    elif form == 'byte':
        # JA: data 用 .byte, pad 用 .byte/.zero
        for k in range(0, len(data), 16):
            chunk = data[k:k + 16]
            lines.append('\t.byte ' + ', '.join(f'0x{b:02X}' for b in chunk))
        if pad == 1:
            lines.append('\t.byte 0x00')
        elif pad >= 2:
            lines.append(f'\t.zero {pad}')
    else:
        raise ValueError(f'unknown form {form}')
    return lines


def write_lang_s(lang, entries, form, region_start, region_end):
    out_path = OUT_DIR / f'game-strings-{lang}.s'
    region_size = region_end - region_start

    # 统计 master entries (1642) + extras + pre (leading pad)
    pre_entries = [e for e in entries if e[0] == 'pre']
    master_entries = [e for e in entries if e[0] == 'master']
    extra_entries = [e for e in entries if e[0] == 'extra']
    assert len(master_entries) == N_ROWS, \
        f'{lang}: 期望 {N_ROWS} master rows, 实 {len(master_entries)}'
    assert len(pre_entries) <= 1, f'{lang}: 最多 1 个 PRE entry'
    leading_pad = pre_entries[0][2] if pre_entries else 0

    lines = []
    lines.append(f'@ data/game-strings-{lang}.s')
    if lang == 'ja':
        lines.append(f'@ JA UI strings (game-strings JA col, ROM 0x{region_start:X}-0x{region_end:X})')
    else:
        lines.append(f'@ {lang.upper()} game strings (ROM 0x{region_start:X}-0x{region_end:X})')
    lines.append('@ Generated by tools/game-strings/encode_txt_to_s.py (master pointer table-driven)')
    lines.append('@')
    lines.append(f'@ Region size: {region_size} B; 1642 master rows')
    if extra_entries:
        lines.append(f'@ + {len(extra_entries)} JA-only extras (Death Message tail)')
    lines.append('@')
    lines.append('@ Labels:')
    lines.append(f'@   game_str_{lang}_NNNN          master row 0000..1641')
    lines.append(f'@   game_str_{lang}_sd_NN         alias for SD[0..6] (master row 655..661)')
    lines.append(f'@   game_str_{lang}_opp_NN        alias for OPP[0..24] (master row 1217..1241)')
    if lang == 'ja':
        lines.append(f'@   game_str_ja_extra_NN          JA-only Death Message tail (00..08)')
    lines.append('')
    lines.append(f'game_str_{lang}:')
    lines.append('')

    total_bytes = 0

    # 区段头 leading pad
    if leading_pad > 0:
        lines.append(f'@ region leading pad ({leading_pad} B), before row 0 ptr')
        if leading_pad == 1:
            lines.append('\t.byte 0x00')
        else:
            lines.append(f'\t.zero {leading_pad}')
        lines.append('')
        total_bytes += leading_pad

    for kind, num, pad, body in master_entries:
        primary, aliases = labels_for_master(lang, num)
        lines.append(f'{primary}:')
        for ali_name, ali_comment in aliases:
            lines.append(f'{ali_name}:  @ {ali_comment}')
        # encode body
        if lang == 'ja':
            data = encode_ja_text(body)
        else:
            data = encode_5lang_text(body)
        lines.extend(emit_data_lines(data, pad, form))
        lines.append('')
        total_bytes += len(data) + pad

    # JA extras
    for kind, num, pad, body in extra_entries:
        lines.append(f'game_str_ja_extra_{num:02d}:')
        data = encode_ja_text(body)
        lines.extend(emit_data_lines(data, pad, form))
        lines.append('')
        total_bytes += len(data) + pad

    if total_bytes != region_size:
        raise ValueError(
            f'{lang}: 编码总字节 {total_bytes} != 区段大小 {region_size} '
            f'(差 {total_bytes - region_size} B)'
        )

    # 5 lang 的 .ascii 内容含 CP1252 高字节, 必须用 cp1252 编码写文件 (GAS 把每字节字面读取).
    # JA 的 .byte form 全 ASCII 安全, 用 utf-8 也行, 这里统一 cp1252 (header 已无非 ASCII).
    file_encoding = 'cp1252'
    with open(out_path, 'w', encoding=file_encoding, newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'  {lang}: {len(master_entries)} master + {len(extra_entries)} extras '
          f'= {total_bytes} B -> {out_path}')


def main():
    print('Encoding 6 lang txt → 6 .s files')
    for lang, (rs, re_) in LANG_REGIONS.items():
        src = Path(f'text/game-strings/{lang}.txt')
        if not src.exists():
            print(f'  [SKIP] {lang}: {src} not found')
            continue
        entries = parse_txt(src)
        form = 'byte' if lang == 'ja' else 'ascii'
        write_lang_s(lang, entries, form, rs, re_)


if __name__ == '__main__':
    main()
else:
    main()
