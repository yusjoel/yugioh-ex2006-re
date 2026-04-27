"""找出 codetable 中字符为单字节 ASCII (0x20-0x7E) 的所有 idx"""
import json

ct = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

ascii_chars_in_ct = []
for idx, ch in sorted(ct.items()):
    if ch and len(ch) == 1 and 0x20 <= ord(ch) <= 0x7E:
        ascii_chars_in_ct.append((idx, ch, ord(ch)))

print(f'Codetable 里映射到 ASCII 字符的 idx: {len(ascii_chars_in_ct)}')
for idx, ch, cp in ascii_chars_in_ct:
    print(f'  idx={idx:4d}: {ch!r} (U+{cp:04X})')

# 检查这些字符是否会作为控制码出现 in raw bytes
print('\n哪些与控制码冲突:')
print('  控制码组合: @4 (0x40 0x34), @5 (0x40 0x35), @7 (0x40 0x37) — 共 3 种')
print('  即: 0x40, 0x34, 0x35, 0x37 这 4 个字节会作为单字节控制码出现')
control_bytes = {0x40, 0x34, 0x35, 0x37}
conflicts = [(idx, ch, cp) for idx, ch, cp in ascii_chars_in_ct if cp in control_bytes]
print(f'\n冲突 idx (会同时被解释为 codetable char 和控制码):')
for idx, ch, cp in conflicts:
    print(f'  idx={idx}: {ch!r} (0x{cp:02X})')
