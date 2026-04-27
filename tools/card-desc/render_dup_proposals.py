"""
基于视觉判读, 给每对重复 char 的 LOW-freq idx 提议正确字符.
分 2 页渲染让用户确认.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 22

# (low_idx, current_char (错), proposed (绿), 信心 H/M/L, hint)
PROPOSALS = [
    # Page 1 batch
    (588, '1', '旧', 'H', 'kyū, ku-row (丨+日)'),
    (27,  '[', '{', 'M', '左花括号 (vs 21=[)'),
    (28,  ']', '}', 'M', '右花括号'),
    (1282, 'o', '即', 'M', 'soku 或 卯 (uncertain)'),
    (1883, 'キ', '?', 'L', '复杂字, 待用户'),
    (3,   '・', '·', 'M', 'mid-dot 变体'),
    (683, '主', '潔', 'H', 'kessō (氵+丰+刀+糸)'),
    (33,  '二', '−', 'M', '一横, 应是 minus 或 _'),
    (574, '体', '?', 'L', '亻+? 不确定'),
    (1088,'判', '診', 'H', '言+多, 应是 診断 (revert)'),
    (1170,'占', '点', 'H', 'ten (占+灬)'),
    (36,  '古', '?', 'L', 'ASCII 区, 不确定'),
    (1828,'合', '累', 'M', '田+? 应是 累計 (uncertain)'),
    (631, '字', '緊', 'M', '臣+又+糸'),
    (1318,'室', '富', 'H', 'fu (宀+一+口+田)'),
    (725, '屍', '戸', 'H', 'to (一+尸)'),
    # Page 2 batch
    (1879,'山', '崎', 'H', 'saki (山+寺-like)'),
    (1004,'川', '順', 'H', 'jun (川+頁)'),
    (1102,'推', '雑', 'M', 'zatsu 或 推 (uncertain)'),
    (730, '支', '鼓', 'H', 'tsuzumi (士+口+支)'),
    (1390,'日', '由', 'M', 'yu 或 申 / 甲'),
    (37,  '早', '?', 'L', 'ASCII 区, glyph 像 早 但位置错'),
    (426, '果', '課', 'H', 'ka (言+果)'),
    (507, '欠', '歓', 'H', 'kan (雚+欠), 681 才是真欠'),
    (580, '求', '救', 'H', 'kyū (求+攵)'),
    (1902,'真', '貞', 'H', 'tei (卜+貝)'),
    (569, '石', '詰', 'H', 'tsu (言+吉)'),
    (1856,'竜', '電', 'H', 'den (雨+田+乚)'),
    (1444,'篤', '驚', 'M', 'kyō 或 篤 (uncertain)'),
    (1604,'粉', '紛', 'M', 'fun (糸+分)'),
    (1152,'精', '績', 'M', 'seki (糸+責)'),
    (656, '葉', '?', 'L', '艹+三+木, defer'),
    # Page 3 batch
    (1773,'葉', '?', 'L', 'defer'),
    (1904,'藤', '?', 'L', '类似 藤, defer'),
    (1559,'西', '漂', 'H', '高频实际是 漂! 1139 才是真西'),
    (1737,'言', '訳', 'H', 'yaku (言+尺)'),
    (1329,'貝', '貯', 'H', 'cho (貝+丁)'),
    (1399,'貝', '?', 'L', '第 3 个 貝, defer'),
    (987, '足', '戦', 'M', 'sen 或其他'),
    (1003,'通', '巡', 'H', 'jun (辶+巛)'),
    (1499,'道', '迫', 'H', 'haku (辶+白)'),
    (1537,'重', '載', 'M', 'sai 或 戴'),
    (852, '錯', '鎖', 'M', 'sa (金+鎖右半)'),
    (1884,'防', '倣', 'M', 'hō 或 訪'),
    (1154,'青', '晴', 'M', 'hare (日+青)'),
    (18,  '！', '"', 'H', '右双引号 (上方 2 短斜线)'),
]

print(f'Total proposals: {len(PROPOSALS)}')

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_big = ImageFont.truetype(font_path, 36)
font_md = ImageFont.truetype(font_path, 22)
font_sm = ImageFont.truetype(font_path, 16)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


CONFIDENCE_COLOR = {
    'H': (40, 130, 40),    # 高: 绿
    'M': (200, 130, 30),   # 中: 橙
    'L': (140, 80, 80),    # 低: 暗红
}

PER_PAGE = 16
COLS = 4
CELL_W = 460
CELL_H = 360

n_pages = (len(PROPOSALS) + PER_PAGE - 1) // PER_PAGE
for page in range(n_pages):
    start = page * PER_PAGE
    end = min(start + PER_PAGE, len(PROPOSALS))
    batch = PROPOSALS[start:end]
    rows = (len(batch) + COLS - 1) // COLS
    img_w = CELL_W * COLS + 40
    img_h = CELL_H * rows + 80
    img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((20, 12), f'Codetable 重复 char 提议 第 {page+1}/{n_pages} 页 (共 {len(PROPOSALS)})',
              fill=(40, 40, 80), font=font_md)
    draw.text((20, 44), '左: ROM 实际 glyph (24x).  右上红: 当前(错).  右下: 提议 (绿=高信心 / 橙=中 / 暗红=低/?)',
              fill=(80, 80, 100), font=font_sm)

    for i, (idx, cur, prop, conf, hint) in enumerate(batch):
        row = i // COLS
        col = i % COLS
        x0 = 20 + col * CELL_W
        y0 = 70 + row * CELL_H
        draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
        draw.text((x0 + 14, y0 + 8), f'idx={idx} ({conf})', fill=(60, 60, 200), font=font_md)

        glyph_box = W * SCALE
        gx0 = x0 + 14
        gy0 = y0 + 50
        draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                       fill=(255, 255, 255), outline=(140, 140, 140))
        draw_glyph(img, idx, gx0, gy0)

        rx0 = gx0 + glyph_box + 20
        draw.text((rx0, gy0 + 8), '当前:', fill=(180, 60, 30), font=font_sm)
        draw.text((rx0, gy0 + 28), cur, fill=(180, 60, 30), font=font_big)
        draw.text((rx0, gy0 + 95), '提议:', fill=CONFIDENCE_COLOR[conf], font=font_sm)
        draw.text((rx0, gy0 + 115), prop, fill=CONFIDENCE_COLOR[conf], font=font_big)
        # hint
        draw.text((x0 + 14, y0 + CELL_H - 35), hint[:32], fill=(60, 60, 60), font=font_sm)

    out = Path(f'tools/card-desc/dup_proposals_page{page+1}.png')
    img.save(out)
    print(f'wrote {out}')
