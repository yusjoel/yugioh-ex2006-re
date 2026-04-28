"""
codetable.json: 把所有半角 ASCII 字符 (cp 0x21-0x7E) 转全角 (cp + 0xFEE0).

原因: paddle OCR 把全角 'ａ-ｚ' / 'Ａ-Ｚ' / '０-９' 等误识别成半角形.
而 ROM 中相同 idx 实际是全角 glyph. 修正 codetable 后:
  - decoder: F0 ED → idx 109 → 'ｌ' (全角, 而非 'l' 半角)
  - encoder: 'ｌ' 走 char_to_idx → JA 2-byte; 'l' (不在 char_to_idx) → 1-byte ASCII pass-through
区分清晰, 1-byte 控制码 vs 2-byte JA pair 不再歧义.

少数 idx 全角已被占 (e.g. idx 91 = 'Ｔ', idx 1832 paddle 给 'T') → 用 Math Bold (𝐀-𝐳, 𝟎-𝟗) 唯一替代, 保 codetable 1-to-1.

不动 user_confirmed.py 中已经手工设的全角.
"""
import sys, io
if sys.stdout.encoding.lower() not in ('utf-8', 'utf_8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json

CT_PATH = 'tools/jp-decode/codetable.json'
ct = json.loads(open(CT_PATH, encoding='utf-8').read())

# 第一遍: 收集已有的全角 ASCII (作 occupied 集)
occupied_full = set()
for ch in ct['by_idx'].values():
    if ch and len(ch) == 1 and 0xFF01 <= ord(ch) <= 0xFF5E:
        occupied_full.add(ch)

# Math Bold (U+1D400-) substitution — 用于全角已占的次重复, 保持 1-to-1
def to_math_bold(cp):
    """半角 0-9/A-Z/a-z → Math Bold (4 byte UTF-8) 唯一占位."""
    if 0x30 <= cp <= 0x39:  # 0-9 → 𝟎-𝟗 (U+1D7CE-)
        return chr(0x1D7CE + (cp - 0x30))
    if 0x41 <= cp <= 0x5A:  # A-Z → 𝐀-𝐙 (U+1D400-)
        return chr(0x1D400 + (cp - 0x41))
    if 0x61 <= cp <= 0x7A:  # a-z → 𝐚-𝐳 (U+1D41A-)
        return chr(0x1D41A + (cp - 0x61))
    return None  # 非字母数字, 无 math 变体


# 第二遍: 半角→全角; 若全角已被其他 idx 占用 → 用 Math Bold 唯一替代 (避免 codetable 重复)
new_by_idx = {}
changed_full = []
changed_math = []
skipped = []
for idx_str, ch in ct['by_idx'].items():
    if ch and len(ch) == 1:
        cp = ord(ch)
        if 0x21 <= cp <= 0x7E:
            full_ch = chr(cp + 0xFEE0)
            if full_ch in occupied_full:
                math_ch = to_math_bold(cp)
                if math_ch is not None and math_ch not in occupied_full:
                    new_by_idx[idx_str] = math_ch
                    changed_math.append((int(idx_str), ch, math_ch))
                    occupied_full.add(math_ch)
                else:
                    # 没有 math 变体 (非字母数字) 或 math 也已占 → 留半角
                    skipped.append((int(idx_str), ch, full_ch))
                    new_by_idx[idx_str] = ch
            else:
                new_by_idx[idx_str] = full_ch
                changed_full.append((int(idx_str), ch, full_ch))
                occupied_full.add(full_ch)
            continue
    new_by_idx[idx_str] = ch

print(f'Changed {len(changed_full)} entries (半角 → 全角):')
for idx, old, new in sorted(changed_full)[:10]:
    print(f'  idx={idx}: {old!r} → {new!r}')
if len(changed_full) > 10:
    print(f'  ... + {len(changed_full)-10} more')
print(f'\nChanged {len(changed_math)} entries (全角占, 用 Math Bold 替代):')
for idx, old, new in sorted(changed_math):
    print(f'  idx={idx}: {old!r} → {new!r}')
if skipped:
    print(f'\nSkipped {len(skipped)} entries (无 math 变体, 留半角):')
    for idx, half, full in sorted(skipped):
        print(f'  idx={idx}: {half!r}')

ct['by_idx'] = new_by_idx

# Also update by_char if present
if 'by_char' in ct:
    new_by_char = {new_by_idx[k]: int(k) for k in new_by_idx if new_by_idx[k]}
    ct['by_char'] = {k: v for k, v in new_by_char.items()}

with open(CT_PATH, 'w', encoding='utf-8') as f:
    json.dump(ct, f, ensure_ascii=False, indent=2)
print(f'\nwrote {CT_PATH}')
