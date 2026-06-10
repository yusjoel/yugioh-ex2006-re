import re, json
lines = open('asm/03_equip_chain_hand.s', encoding='utf-8', errors='replace').read().splitlines()
funcs = []
skip_pref = ('LAB_','DAT_','PTR_','UNK_','switchD','DWORD_','jumptable','caseD','jumpTable')
for i, ln in enumerate(lines):
    if not ln.endswith(':'):
        continue
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*:$', ln):
        continue
    name = ln[:-1]
    if name.startswith(skip_pref):
        continue
    # look ahead a few lines for push prologue with addr
    for j in range(i+1, min(i+4, len(lines))):
        mm = re.search(r'push \{.*\}.*@ ([0-9a-fA-F]{8})', lines[j])
        if mm:
            funcs.append((int(mm.group(1), 16), name))
            break
funcs.sort()
print('total func entries:', len(funcs))
# upper bound of file 03
UB = 0x0804020c
LB = 0x08035f54
# split into ~10 segments by function count
N = 10
per = (len(funcs) + N - 1)//N
print('per seg ~', per)
segs = []
for s in range(0, len(funcs), per):
    chunk = funcs[s:s+per]
    start = chunk[0][0]
    # end = next chunk's start, or UB
    nexti = s+per
    end = funcs[nexti][0] if nexti < len(funcs) else UB
    segs.append((start, end, len(chunk)))
for idx,(st,en,c) in enumerate(segs,1):
    print('Seg-%d  0x%05x..0x%05x  %d fn' % (idx, st & 0xfffff, en & 0xfffff, c))
json.dump([[hex(a),n] for a,n in funcs], open('tools/f03funcs.json','w'))
