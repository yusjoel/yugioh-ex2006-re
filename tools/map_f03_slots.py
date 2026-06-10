import re, json
lines = open('asm/03_equip_chain_hand.s', encoding='utf-8', errors='replace').read().splitlines()
# segment boundaries (start addr) from previous mapping
seg_bounds = [0x35f54,0x36a78,0x37128,0x37904,0x3a7f0,0x3b3a8,0x3bba4,0x3c774,0x3d91c,0x3efcc,0x4020c]
# build mapping of addr per line: any line with '@ 08XXXXXX'
def line_addr(ln):
    m = re.search(r'@ ([0-9a-fA-F]{8})(?:\s|$)', ln)
    if m:
        return int(m.group(1),16) & 0xfffff
    return None

# count auto-name label definitions per segment, and ROM_INCBIN
# We track current addr by scanning; label defs (DAT_/DWORD_/PTR_/UNK_) carry their addr on same line or next
auto_defs = []  # (addr, name)
incbins = []    # (addr, directive)
cur = None
for i,ln in enumerate(lines):
    a = line_addr(ln)
    if a is not None:
        cur = a
    # auto-name label definition
    m = re.match(r'^((?:DAT|DWORD|PTR|UNK|PTR_DAT)_[0-9a-fA-F]{8}):', ln)
    if m:
        # addr from name
        addr = int(m.group(1).split('_')[-1],16) & 0xfffff
        auto_defs.append((addr, m.group(1)))
    if 'ROM_INCBIN' in ln or re.search(r'\.incbin', ln):
        incbins.append((cur if cur else 0, ln.strip()[:80]))

def seg_of(addr):
    for s in range(10):
        if seg_bounds[s] <= addr < seg_bounds[s+1]:
            return s+1
    return None

from collections import Counter
cnt = Counter()
for addr,name in auto_defs:
    sg = seg_of(addr)
    if sg: cnt[sg]+=1
print('=== auto-name slot counts per seg ===')
for s in range(1,11):
    print('Seg-%d: %d slots' % (s, cnt[s]))
print('total auto-name defs:', len(auto_defs))
print()
print('=== ROM_INCBIN / .incbin in file 03 ===')
for addr,d in incbins:
    print('0x%05x  %s  (Seg-%s)' % (addr, d, seg_of(addr)))
print('total incbin lines:', len(incbins))
