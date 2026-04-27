"""查指定 idx 在卡名/卡描述/全 ROM 中的上下文, 帮助判定字符"""
import re
import json
import sys
from collections import defaultdict


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
                result.append(int(s[i + 1:j], 8)); i = j
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c)); i += 1
    return bytes(result)


CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


def code_to_idx(hi, lo):
    if hi >= 0xF0:
        return ((hi & 0xF) << 7) | (lo & 0x7F)
    return None


def render_text(seq, mark_idx):
    out = []
    for i, item in enumerate(seq):
        if item is None:
            continue
        if item == mark_idx:
            out.append(f'【?{item}】')
        else:
            ch = CT.get(item, f'<{item}>')
            out.append(ch if ch else f'<{item}>')
    return ''.join(out)


# 1) 卡描述
src = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|ja):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
cid_seq = {}
for m in pat.finditer(src):
    cid = int(m.group(1))
    bs = decode_octal_string(m.group(3))
    seq = []
    i = 0
    while i + 1 < len(bs):
        idx = code_to_idx(bs[i], bs[i + 1])
        seq.append(idx)
        i += 2
    cid_seq[cid] = seq

# 2) 卡名 (从 ROM 直接读)
import struct
ROM = open('roms/2343.gba', 'rb').read()
PT, CT_NAME = 0x015F3A5C, 0x015BB594


def read_xx(cid):
    ptr = struct.unpack_from('<I', ROM, PT + cid * 24)[0]
    addr = CT_NAME + ptr
    end = ROM.find(b'\x00', addr)
    return ROM[addr:end]


# 3) 全 ROM 搜索
TARGETS = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [1318, 1828]

for tidx in TARGETS:
    print(f'\n========== idx={tidx} ==========')
    # 卡描述
    print('--- card-descriptions hits ---')
    for cid, seq in cid_seq.items():
        if tidx in seq:
            text = render_text(seq, tidx)
            # 截取目标周围
            pos = seq.index(tidx)
            lo = max(0, pos - 8); hi = min(len(seq), pos + 9)
            ctx_seq = seq[lo:hi]
            ctx = ''.join(CT.get(i, f'<{i}>') if i and i != tidx else f'【?{tidx}】' if i == tidx else '?' for i in ctx_seq)
            print(f'  cid={cid:4d}: ...{ctx}...')

    # 卡名
    print('--- card name hits ---')
    hits = 0
    for cid in range(2098):
        try:
            bs = read_xx(cid)
        except:
            continue
        if not bs:
            continue
        # 解码
        seq = []
        i = 0
        while i + 1 < len(bs):
            c = (bs[i] << 8) | bs[i + 1]
            if c >= 0xF000:
                idx = code_to_idx(bs[i], bs[i + 1])
                seq.append(idx); i += 2
            else:
                i += 1
        if tidx in seq:
            ctx = render_text(seq, tidx)
            print(f'  cid={cid:4d}: {ctx}')
            hits += 1
            if hits > 10:
                break

    # 全 ROM (achievement strings 等)
    hi = ((tidx >> 7) & 0xF) | 0xF0
    lo = (tidx & 0x7F) | 0x80
    pat_b = bytes([hi, lo])
    rom_hits = []
    start = 0
    while True:
        p = ROM.find(pat_b, start)
        if p < 0: break
        rom_hits.append(p)
        start = p + 1
    print(f'--- ROM raw hits: {len(rom_hits)} ---')
    # 检查文本邻居
    for p in rom_hits[:8]:
        # 看前后 ±8 byte 解码
        ctx_lo = max(0, p - 16)
        ctx_hi = min(len(ROM), p + 18)
        if (p - ctx_lo) % 2: ctx_lo += 1
        ctx = []
        i = ctx_lo
        while i + 1 < ctx_hi:
            b0, b1 = ROM[i], ROM[i + 1]
            if i == p:
                ctx.append(f'【?{tidx}】'); i += 2
                continue
            if b0 >= 0xF0 and b1 >= 0x80:
                idx2 = ((b0 & 0xF) << 7) | (b1 & 0x7F)
                ch = CT.get(idx2, f'<{idx2}>')
                ctx.append(ch if ch else '?')
            elif b0 == 0:
                ctx.append('§')
            elif b0 < 8:
                ctx.append(f'<c{b0:02X}>')
            else:
                ctx.append(f'?[{b0:02X}{b1:02X}]')
            i += 2
        s = ''.join(ctx)
        # 只输出像文本的 (含至少 5 个有效字符)
        valid = sum(1 for ch in s if ch and len(ch) == 1 and ord(ch) > 0x7F)
        if valid >= 3:
            print(f'  ROM 0x{p:08X}: {s}')
