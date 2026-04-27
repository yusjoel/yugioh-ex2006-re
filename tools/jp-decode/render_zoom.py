"""
高清放大渲染 idx 207 和 idx 291 周围字符对比, 字号大便于人眼判断字形细节.
"""
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, 'tools/jp-decode')
from seed_codetable import build_seed_by_idx
seed = build_seed_by_idx()

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 14   # 12*14 = 168 px
GW = W * SCALE
GH = H * SCALE

font = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 36)
font_lab = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 18)

def render_strip(idx_list, title, fname):
    """Render given idx_list as horizontal strip with big labels."""
    n = len(idx_list)
    cell_w = GW + 30
    cell_h = GH + 90
    img = Image.new('RGB', (cell_w*n + 20, cell_h + 50), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((20, 8), title, fill=(60, 60, 100), font=font_lab)
    for i, item in enumerate(idx_list):
        if isinstance(item, tuple):
            idx, hint = item
        else:
            idx, hint = item, ''
        x0 = 20 + i*cell_w
        y0 = 40
        # idx label
        draw.text((x0 + 10, y0), f'idx={idx}  hi/lo=F{(idx>>7)+0:X}/{0x80|(idx&0x7F):02X}',
                  fill=(80, 80, 80), font=font_lab)
        # glyph
        gx = x0 + 10
        gy = y0 + 22
        draw.rectangle([gx-2, gy-2, gx+GW+1, gy+GH+1], fill=(255,255,255), outline=(150,150,150), width=2)
        for y in range(H):
            for x in range(W):
                if ROM[BASE + idx*W*H + y*W + x]:
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            img.putpixel((gx+x*SCALE+dx, gy+y*SCALE+dy), (0,0,0))
        # known/inferred char
        ch_str = ''
        color = (200, 200, 200)
        if idx in seed:
            ch_str = seed[idx]; color = (30, 110, 30); tag = '(seed)'
        elif hint:
            ch_str = hint
            color = (180, 30, 30) if '✓' in hint else (60, 60, 180)
            tag = ''
        else:
            tag = '?'
        if ch_str:
            cw = draw.textlength(ch_str.replace('?', '').replace('✓', ''), font=font)
            draw.text((x0 + (cell_w - cw)//2, gy + GH + 6), ch_str, fill=color, font=font)
    img.save(fname)
    print(f'wrote {fname}  ({img.size})')

# Strip 1: idx 207 ± neighbors (含 seed 已知 ろ ゎ わ ゐ ゑ を ん | ァ? | ア ィ イ)
strip1 = [
    (203, 'ゐ (seed)'),
    (204, 'ゑ (seed)'),
    (205, 'を (seed)'),
    (206, 'ん (seed)'),
    (207, '? (推断 ァ)'),
    (208, 'ア (seed)'),
    (209, 'ィ (seed)'),
    (210, 'イ (seed)'),
]
render_strip(strip1, 'idx 207 周围 (推断 ァ 小a片假名 vs ?)',
             'tools/jp-decode/review/zoom_idx207.png')

# Strip 2: idx 291 ± neighbors (含 seed ヰ ヱ ヲ ン | ヴ | ? | α β γ)
strip2 = [
    (287, 'ヱ (seed)'),
    (288, 'ヲ (seed)'),
    (289, 'ン (seed)'),
    (290, 'ヴ ✓'),
    (291, '? (推断 ヶ)'),
    (292, 'α ✓'),
    (293, '? (推断 β)'),
    (294, '? (推断 γ)'),
]
render_strip(strip2, 'idx 291 周围 (推断 ヶ 小ke片假名 vs ?)',
             'tools/jp-decode/review/zoom_idx291.png')
