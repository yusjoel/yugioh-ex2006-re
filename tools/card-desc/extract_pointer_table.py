"""
从原 .s 提取 pointer table mapping → text/card-desc/pointer-table.txt

Format (each line):
  cid label_cid comment
  e.g.:
  0000 0000 (dummy)
  0001 0001 Blue-Eyes White Dragon
  0002 0001 Blue-Eyes White Dragon (alt-art)
"""
import re
from pathlib import Path

src = open('data/card-descriptions.s', encoding='latin-1').read()
# 找 pointer table 段
start = src.find('card_desc_pointer_table:')
assert start >= 0
section = src[start:]

pat = re.compile(r'desc_offsets\s+(\d+)\s*@\s*card id:\s*(\d+),\s*(.*)')
entries = []
for m in pat.finditer(section):
    label_cid = int(m.group(1))
    cid = int(m.group(2))
    comment = m.group(3).strip()
    entries.append((cid, label_cid, comment))

print(f'Extracted {len(entries)} pointer table entries')
# 保证 cid 从 0 连续到 2097
cids = [e[0] for e in entries]
assert cids == list(range(2098)), f'Non-continuous cids! min={min(cids)}, max={max(cids)}'

# 统计 alt-art (cid != label_cid)
alt_art = [(c, l) for c, l, _ in entries if c != l]
print(f'Alt-art entries (cid != label_cid): {len(alt_art)}')
print(f'Sample alt-art:')
for c, l in alt_art[:5]:
    print(f'  cid={c} → label_cid={l}')

out = Path('text/card-desc/pointer-table.txt')
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('@ Pointer Table mapping: cid → label_cid (4 digits each)\n')
    f.write('@ Each cid in [0, 2097] maps to a label_cid that has actual data.\n')
    f.write('@ When cid != label_cid, this is alt-art / shared description.\n')
    f.write('@ Format: "<cid> <label_cid> <comment>"\n\n')
    for cid, label_cid, comment in entries:
        f.write(f'{cid:04d} {label_cid:04d}  {comment}\n')

print(f'\nwrote {out}')
