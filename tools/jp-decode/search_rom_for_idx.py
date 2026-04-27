"""
对 20 个 0-hit idx，全 ROM 搜索 (hi,lo) 字节对。
过滤伪命中：要求 P 位置至少前/后一个邻居也是有效 JP char_code（hi >= 0xF0 且 lo >= 0x80），
或前后是特定控制码（0x01-0x05 = 换行/空格 markers）。
然后用当前 codetable 解码 ±15 byte 上下文。
"""
import json
import re
from collections import defaultdict


ZERO_HIT = {
    9: 'guess=◆', 12: 'guess=横线', 16: 'guess=‥', 17: 'guess=”',
    327: 'guess=妻', 851: 'guess=索', 1088: 'guess=診', 1174: 'guess=川',
    1218: 'guess=縛', 1281: 'guess=只', 1304: 'guess=燕', 1342: 'guess=譲',
    1510: 'guess=緊', 1578: 'guess=父', 1742: 'guess=諭', 1746: 'guess=愛',
    1816: 'guess=塞', 1828: 'guess=異', 1839: 'guess=業', 1869: 'guess=丨',
}


def idx_to_code(idx):
    hi = ((idx >> 7) & 0xF) | 0xF0
    lo = (idx & 0x7F) | 0x80
    return hi, lo


def code_to_idx(hi, lo):
    if hi >= 0xF0 and lo >= 0x80:
        return ((hi & 0xF) << 7) | (lo & 0x7F)
    return None


CONTROL_CODES = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07}


def is_jp_pair(b0, b1):
    """字节对像日文 char_code"""
    return b0 >= 0xF0 and b1 >= 0x80


def is_text_neighbor(rom, p):
    """位置 p 是否像文本上下文：前后字节对至少一个是合法 JP char_code 或控制码"""
    # check pair at p-2
    has_left = False
    if p >= 2:
        b0, b1 = rom[p - 2], rom[p - 1]
        if is_jp_pair(b0, b1) or b0 in CONTROL_CODES or (b0 == 0x00 and b1 == 0x00):
            has_left = True
    # check pair at p+2
    has_right = False
    if p + 3 < len(rom):
        b0, b1 = rom[p + 2], rom[p + 3]
        if is_jp_pair(b0, b1) or b0 in CONTROL_CODES or (b0 == 0x00 and b1 == 0x00):
            has_right = True
    return has_left or has_right


def decode_context(rom, p, ctx_pairs=12, target_idx=None):
    """从 p 开始解码 ±ctx_pairs 个字符对"""
    out = []
    start = p - ctx_pairs * 2
    end = p + (ctx_pairs + 1) * 2
    start = max(0, start)
    end = min(len(rom), end)
    # 对齐到偶数偏移（相对 p）
    if (p - start) % 2 != 0:
        start += 1

    i = start
    while i + 1 < end:
        b0, b1 = rom[i], rom[i + 1]
        is_target = (i == p)
        if b0 in CONTROL_CODES:
            # 控制码占 2 字节（小端 u16），按 1 字节 marker 解码
            if b0 == 0x00 and b1 == 0x00:
                out.append('§')  # null terminator marker
                i += 2
                continue
            else:
                out.append(f'<c{b0:02X}>')
                i += 2
                continue
        idx = code_to_idx(b0, b1)
        if is_target:
            out.append(f'【?{target_idx}】')
        elif idx is not None:
            ch = ct.get(idx, f'<{idx}>')
            out.append(ch if ch else f'<{idx}>')
        else:
            out.append(f'?[{b0:02X}{b1:02X}]')
        i += 2
    return ''.join(out)


# Load codetable
ct = json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx']
ct = {int(k): v for k, v in ct.items()}

# Load ROM
rom = open('roms/2343.gba', 'rb').read()
print(f'ROM size: {len(rom):,} B')

# Known text regions (skip code/graphics zones to reduce noise)
# card_descs_table: 0x15FFF0C - 0x180A508
# card name table region: ~0x15BB594 - ?
# Not strict; we'll use the neighbor heuristic
TEXT_REGIONS = [
    (0x15A0000, 0x1820000),  # generous range covering card names + descriptions
    (0x1B00000, 0x1E00000),  # other text regions (game strings, deck names?)
]

def in_text_region(p):
    for lo, hi in TEXT_REGIONS:
        if lo <= p < hi:
            return True
    return False


report = []
for tidx in sorted(ZERO_HIT.keys()):
    hi, lo = idx_to_code(tidx)
    pat = bytes([hi, lo])
    matches = []
    start = 0
    while True:
        p = rom.find(pat, start)
        if p < 0:
            break
        # require even alignment (since text is 2-byte units, but offset depends on stream start)
        # we don't know the alignment a priori; the heuristic is: at this p, both neighbor pairs
        # at p-2 and p+2 are also valid JP/control bytes
        if is_text_neighbor(rom, p) and in_text_region(p):
            matches.append(p)
        start = p + 1

    report.append(f'\n=== idx={tidx} ({ZERO_HIT[tidx]}) hi={hi:02X} lo={lo:02X} → {len(matches)} text-like hits ===')
    for p in matches[:8]:
        ctx = decode_context(rom, p, ctx_pairs=15, target_idx=tidx)
        report.append(f'  ROM 0x{p:08X}: ...{ctx}...')

text = '\n'.join(report)
print(text)
with open('tools/jp-decode/review/zerohit_rom_search.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('\nwrote tools/jp-decode/review/zerohit_rom_search.txt')
