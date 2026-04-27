"""检查 6 lang payload 是否含不可打印 byte (除 \\0 padding)"""
import re


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


txt = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
problems = {l: [] for l in ['xx', 'en', 'de', 'fr', 'it', 'es']}
for m in pat.finditer(txt):
    cid = int(m.group(1))
    lang = m.group(2)
    bs = decode_octal_string(m.group(3))
    payload = bs.rstrip(b'\x00')
    bad = [b for b in payload if (b < 0x20 and b != 9) or b == 0x7F]
    if bad:
        problems[lang].append((cid, sorted(set(bad))))

for lang, ps in problems.items():
    print(f'{lang}: {len(ps)} entries with unprintable bytes')
    for cid, bad in ps[:3]:
        print(f'  cid={cid}: bytes={[hex(b) for b in bad]}')
