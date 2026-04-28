"""
渲染 24 个无 SJIS 映射的汉字 (疑 paddle OCR 把日文新字体识为简体/异体).
每页 6 个, 共 4 页. 每格: 码表当前字符 + ROM 实际 glyph + 提议日文新字体对比.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 24

# (idx, current_ch, proposed_ch_or_question, hint)
ITEMS = [
    (523,  '库', '庫',  'kura (warehouse), 庫 = 广+車'),
    (599,  '竞', '競',  'kyō (compete), 立+口+兄 ×2'),
    (617,  '鄉', '郷',  'kyō (village), 郷 是 鄉 的日文新字体'),
    (656,  '薰', '薫',  'kun (fragrance), 薰 vs 薫'),
    (775,  '较', '較',  'kaku (compare), 車+交'),
    (811,  '捆', '?',   'paddle 给 捆, 待确认'),
    (817,  '查', '査',  'sa (investigate), 査 是 查 的日文新字体'),
    (1113, '营', '営',  'ei (manage), 但 idx 361 已是 営 → 此 idx 应别字'),
    (1219, '聪', '聡',  'sō (clever), 聡 是 聰 新字体'),
    (1305, '值', '値',  'chi (value), 値 是 值 新字体'),
    (1359, '滇', '?',   'paddle 给 滇 (云南古称), 卡名上下文待查'),
    (1473, '恼', '悩',  'nō (vex), 悩 是 惱 新字体'),
    (1529, '晚', '晩',  'ban (evening), 晩 是 晚 新字体'),
    (1616, '编', '編',  'hen (compile), 編 是 编 繁体/新字'),
    (1625, '步', '歩',  'ho (walk), 歩 是 步 新字体'),
    (1680, '每', '毎',  'mai (every), 毎 是 每 新字体'),
    (1757, '亲', '親',  'shin (parent), 亲 = 立+木 (简), 親 = 立+木+見'),
    (1766, '摇', '揺',  'yō (shake), 揺 是 摇 新字体'),
    (1791, '攔', '欄?', 'ran (railing), 攔=扌+闌 / 欄=木+闌'),
    (1811, '虑', '慮',  'ryo (consider), 慮 是 虑 繁体'),
    (1838, '歷', '歴',  'reki (history), 歴 是 歷 新字体 (用户已 user_confirmed=歷)'),
    (1851, '劳', '労',  'rō (labor), 労 是 劳 新字体'),
    (1860, '錄', '録',  'roku (record), 録 是 錄 新字体'),
    (1866, '桦', '?',   'paddle 给 桦 (桦树), 待查'),
]


font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_md = ImageFont.truetype(font_path, 22)
font_sm = ImageFont.truetype(font_path, 16)
font_big = ImageFont.truetype(font_path, 36)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


# Layout: 每行 1 个 item; 列: idx 信息 | ROM glyph | 当前 char (font 渲染) | 提议 char (font 渲染)
ROW_H = 360
GLYPH_BOX = W * SCALE  # 288
LEFT_INFO_W = 240
COL_W = GLYPH_BOX + 60
ITEMS_PER_PAGE = 6

n_pages = (len(ITEMS) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
img_w = LEFT_INFO_W + COL_W * 3 + 40
img_h = ROW_H * ITEMS_PER_PAGE + 80

OUT_DIR = Path('tools/card-desc')

for page in range(n_pages):
    start = page * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, len(ITEMS))
    batch = ITEMS[start:end]
    page_h = ROW_H * len(batch) + 80

    img = Image.new('RGB', (img_w, page_h), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((20, 14),
              f'24 个无 SJIS 映射汉字  第 {page+1}/{n_pages} 页 — paddle OCR 嫌疑误识 (简体/繁体)',
              fill=(40, 40, 80), font=font_md)
    draw.text((20, 44),
              '左: idx 信息  | 中: ROM 实际 glyph | 右上 (红): 码表当前字符 | 右下 (绿): 提议日文体',
              fill=(80, 80, 100), font=font_sm)

    for row, (idx, cur, prop, hint) in enumerate(batch):
        y0 = 80 + row * ROW_H

        # 左: 信息
        draw.text((20, y0 + 30), f'idx {idx}', fill=(60, 60, 200), font=font_md)
        draw.text((20, y0 + 60),
                  f'当前: {cur} (U+{ord(cur):04X})',
                  fill=(180, 60, 30), font=font_sm)
        draw.text((20, y0 + 85),
                  f'提议: {prop}' + (f' (U+{ord(prop):04X})' if len(prop) == 1 else ''),
                  fill=(40, 130, 40), font=font_sm)
        # hint 多行 wrap
        words = hint
        draw.text((20, y0 + 115), words, fill=(60, 60, 60), font=font_sm)

        # 中: ROM glyph (24x)
        gx0 = LEFT_INFO_W + 10
        gy0 = y0 + 30
        draw.rectangle([gx0 - 2, gy0 - 2, gx0 + GLYPH_BOX + 1, gy0 + GLYPH_BOX + 1],
                       fill=(255, 255, 255), outline=(120, 120, 140), width=2)
        draw_glyph(img, idx, gx0, gy0)
        draw.text((gx0, gy0 + GLYPH_BOX + 6),
                  f'idx {idx} ROM glyph (12x12, 24x scale)',
                  fill=(60, 60, 60), font=font_sm)

        # 右上: 当前 codetable char (大字渲染)
        cx2 = gx0 + COL_W
        draw.rectangle([cx2 - 2, y0 + 30 - 2, cx2 + GLYPH_BOX + 1, y0 + 30 + GLYPH_BOX//2 - 2],
                       fill=(255, 245, 245), outline=(180, 60, 30), width=2)
        draw.text((cx2 + 30, y0 + 50), '当前码表:', fill=(180, 60, 30), font=font_sm)
        draw.text((cx2 + GLYPH_BOX//2 - 25, y0 + 80), cur, fill=(180, 60, 30), font=font_big)

        # 右下: 提议 char
        draw.rectangle([cx2 - 2, y0 + 30 + GLYPH_BOX//2 + 4, cx2 + GLYPH_BOX + 1, y0 + 30 + GLYPH_BOX + 1],
                       fill=(245, 255, 245), outline=(40, 130, 40), width=2)
        draw.text((cx2 + 30, y0 + 30 + GLYPH_BOX//2 + 24), '提议日文体:', fill=(40, 130, 40), font=font_sm)
        if len(prop) == 1:
            draw.text((cx2 + GLYPH_BOX//2 - 25, y0 + 30 + GLYPH_BOX//2 + 56),
                      prop, fill=(40, 130, 40), font=font_big)
        else:
            draw.text((cx2 + 50, y0 + 30 + GLYPH_BOX//2 + 56),
                      prop, fill=(120, 80, 40), font=font_md)

    out = OUT_DIR / f'non_sjis_kanji_page{page+1}.png'
    img.save(out)
    print(f'wrote {out}  ({img_w}x{page_h})')

print(f'\nTotal: {len(ITEMS)} idx, {n_pages} pages')
