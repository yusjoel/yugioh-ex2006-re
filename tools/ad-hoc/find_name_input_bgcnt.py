#!/usr/bin/env python3
"""Find functions in asm/all.s that write the name_input-page BGxCNT set:
  BG1CNT = 0x1D8C  (immediates: prio=0 + CBB=3 + 8bpp → low byte 0x8C)
  BG2CNT = 0x1E8D
  BG3CNT = 0x1F8F

Strategy: find functions that contain movs/mov with immediates #0x8C, #0x8D, #0x8F
in close proximity AND reference at least one of the BGxCNT addresses.
"""
import re
from pathlib import Path

SRC = Path('asm/all.s').read_text(errors='replace').splitlines()

# Function starts: "FUN_XXXXXXXX:"
fun_re = re.compile(r'^(FUN_[0-9a-f]{8}):')

# Find function boundaries
fun_bounds = []  # (name, start_line, end_line_exclusive)
current = None
for i, line in enumerate(SRC):
    m = fun_re.match(line)
    if m:
        if current is not None:
            fun_bounds.append((current[0], current[1], i))
        current = (m.group(1), i)
if current is not None:
    fun_bounds.append((current[0], current[1], len(SRC)))

# Pre-compile patterns
immediates = {
    '8C': re.compile(r'mov\w*\s+r[0-7],#0x8c\b'),
    '8D': re.compile(r'mov\w*\s+r[0-7],#0x8d\b'),
    '8F': re.compile(r'mov\w*\s+r[0-7],#0x8f\b'),
    '1F40': re.compile(r'0x1f40\b|0x00001f40\b|#0x1f40'),
}
bgcnt_addrs = re.compile(r'0x0*0400000[08ace]\b|\.word  0x0400000[8a-f]|0x0*040000008')

candidates = []
for name, s, e in fun_bounds:
    body = '\n'.join(SRC[s:e])
    has_8c = bool(immediates['8C'].search(body))
    has_8d = bool(immediates['8D'].search(body))
    has_8f = bool(immediates['8F'].search(body))
    has_1f40 = bool(immediates['1F40'].search(body))
    has_bgcnt = bool(bgcnt_addrs.search(body))
    hits = sum([has_8c, has_8d, has_8f])
    if hits >= 2 or has_1f40:
        candidates.append((name, s, e-s, has_8c, has_8d, has_8f, has_1f40, has_bgcnt))

candidates.sort(key=lambda x: (-sum(x[3:7]), -x[7]))

print(f'Total functions: {len(fun_bounds)}; candidates ({len(candidates)}):')
print(f'{"function":22s}  size   8C 8D 8F 1F40 bgCNTaddr')
for row in candidates[:30]:
    name, s, size, c, d, f, word1f40, bgcnt = row
    print(f'{name:22s}  {size:4d}   {int(c)}  {int(d)}  {int(f)}   {int(word1f40)}    {int(bgcnt)}')
