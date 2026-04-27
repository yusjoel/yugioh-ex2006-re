"""逐 (cid, lang) 对比 encoder 输出 vs 原 .s 解析的字节"""
import re
import sys
sys.path.insert(0, 'tools/card-desc')

# Re-parse original .s
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

# Backup
import shutil
shutil.copy('data/card-descriptions.s', r'C:\Users\yushj\AppData\Local\Temp\new_card_descs.s')

# Read original (we don't have it anymore — restore via git stash? actually we backed it up)
import os
orig_path = r'C:\Users\yushj\AppData\Local\Temp\orig_card_descs.s'
if not os.path.exists(orig_path):
    # try git show
    import subprocess
    r = subprocess.run(['git', 'show', 'HEAD:data/card-descriptions.s'], capture_output=True)
    open(orig_path, 'wb').write(r.stdout)

orig_txt = open(orig_path, encoding='latin-1').read()
new_txt = open(r'C:\Users\yushj\AppData\Local\Temp\new_card_descs.s', encoding='latin-1').read()

pat_orig = re.compile(r'card_desc_(\d+)_(xx|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
pat_new = re.compile(r'card_desc_(\d+)_(ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')

orig_labels = {}
for m in pat_orig.finditer(orig_txt):
    cid, lang = int(m.group(1)), m.group(2)
    if lang == 'xx':
        lang = 'ja'  # 兼容
    orig_labels[(cid, lang)] = decode_octal_string(m.group(3))

new_labels = {}
for m in pat_new.finditer(new_txt):
    cid, lang = int(m.group(1)), m.group(2)
    new_labels[(cid, lang)] = decode_octal_string(m.group(3))

print(f'Orig labels: {len(orig_labels)}')
print(f'New labels:  {len(new_labels)}')

# 对比
mismatches = []
for key in orig_labels:
    if key not in new_labels:
        mismatches.append((key, 'missing in new'))
        continue
    o = orig_labels[key]
    n = new_labels[key]
    if o != n:
        mismatches.append((key, f'len {len(o)} vs {len(n)}'))

print(f'\nMismatches: {len(mismatches)}')
for key, info in mismatches[:20]:
    print(f'  {key}: {info}')
    o = orig_labels.get(key, b'')
    n = new_labels.get(key, b'')
    print(f'    orig: {o[:32].hex()}...({len(o)})')
    print(f'    new:  {n[:32].hex()}...({len(n)})')

# Per-lang mismatch summary
from collections import Counter
mismatch_by_lang = Counter()
for (cid, lang), _ in mismatches:
    mismatch_by_lang[lang] += 1
print(f'\nMismatch by lang: {dict(mismatch_by_lang)}')
