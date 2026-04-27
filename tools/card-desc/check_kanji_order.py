"""
扫 codetable 汉字区 (idx 305+) 找疑点:
1. 重复 char (整个 codetable 内 char 重复)
2. 简体字 (Chinese simplified, 不应在日文 ROM)
3. 位置可疑 (前后字 on-yomi 不连续)
"""
import json
from collections import Counter

ct = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

# 1. 全 codetable 重复检查
char_counter = Counter()
for idx, ch in ct.items():
    if ch and len(ch) >= 1:
        char_counter[ch] += 1
dups = {ch: cnt for ch, cnt in char_counter.items() if cnt > 1}
print(f'=== Codetable 重复 char: {len(dups)} ===')
if dups:
    char_idxs = {}
    for idx, ch in ct.items():
        if ch in dups:
            char_idxs.setdefault(ch, []).append(idx)
    for ch, idxs in sorted(char_idxs.items()):
        print(f'  {ch!r}: idx={idxs}')

# 2. 简体/旧字体疑点 (常见简体字符 vs 日文 shin-jitai)
SIMPLIFIED_HINTS = {
    '报': '報',  # Chinese simplified → Japanese
    '銳': '鋭',  # 旧字体 → 新字体
    '閱': '閲',
    '绿': '緑',
    '橫': '横',
    '荣': '栄',
    '颜': '顔',
    '兴': '興',
    '欢': '歓',
    '战': '戦',
    '时': '時',
    '场': '場',
    '门': '門',
    '问': '問',
    '间': '間',
    '关': '関',
    '开': '開',
    '会': None,  # 会 在日文也用 (会う)
    '决': '決',
    '冲': '沖',
    '净': '浄',
    '凉': '涼',
    '减': '減',
    '凤': '鳳',
    '击': '撃',
    '击': '擊',
    '击': '撃',
    '别': '別',
    '剑': '剣',
    '动': '動',
    '务': '務',
    '势': '勢',
    '勋': '勲',
    '医': None,  # 医 是日文新字体
    '区': None,  # 区 是日文新字体
    '历': '歴',
    '压': None,  # 圧 是日文新字体, 压 是中文简体
    '压': '圧',
    '叶': '葉',
    '号': None,  # 号 是日文新字体
    '吓': '嚇',
    '员': None,  # 员 是日文? 实际是 員 简体
    '员': '員',
    '听': '聴',
    '吗': '嗎',
    '咏': '詠',
    '响': '響',
    '哑': '唖',
    '哲': None,
    '唤': '喚',
    '商': None,
    '啰': '囉',
    '啵': None,
    '啸': '嘯',
    '喷': '噴',
    '嘱': '囑',
    '团': '団',  # 注: 団 是日文新字体, 但 团 是中文
    '园': None,  # 園/园 - 园是中文简体
    '围': '囲',
    '园': '園',
    '图': '図',
    '国': '国',  # 同形
    '圆': '円',
    '圣': '聖',
    '块': '塊',
    '坚': '堅',
    '执': '執',
    '坛': '壇',
    '坝': '壩',
    '坞': '塢',
}

print(f'\n=== 简体字/旧字体疑点 ===')
for idx in sorted(ct.keys()):
    ch = ct[idx]
    if ch in SIMPLIFIED_HINTS and SIMPLIFIED_HINTS[ch] is not None:
        print(f'  idx={idx:4d}: {ch!r} ← 应为 {SIMPLIFIED_HINTS[ch]!r}')

# 3. 列出 305..600 全部, 让用户视觉扫一眼
print(f'\n=== idx 305..600 一览 (用户可扫一眼检查 五十音順) ===')
for i in range(305, 601):
    if i in ct:
        print(f'  {i:4d}: {ct[i]!r}', end='')
        if (i - 304) % 6 == 0:
            print()
print()
