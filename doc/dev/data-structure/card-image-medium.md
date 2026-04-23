# 中卡图（对战场 OBJ/BG 32×48 8bpp）

用于对战场等屏幕的中等尺寸卡 sprite，未压缩 8bpp tiles。

---

## 参数

| 项目 | 值 |
|------|-----|
| tile 数据基址 | `0x00FBC080`（GBA `0x08FBC080`） |
| tile 数据结束 | `0x01326280`（= 0x00FBC080 + 2331 × 1536） |
| stride | **1536 字节 / 卡** |
| 像素尺寸 | **32 × 48**（4 × 6 tiles） |
| tile 内部格式 | 8×8 像素 × 8bpp（64 字节 / tile，未压缩） |
| tile_block 数 | 2331（与 big / mini 共享） |
| 索引表 | `0x015B5C00`（与 big / mini 共享） |
| 索引访问 | `tile_block = u16[0x015B5C00 + (card_id × 2 + flag) × 2]` |
| 加载函数 | `FUN_080c2d24`（`asm/all.s` L230236） |
| VRAM 目标（主路径） | OBJ `0x06010000` |
| VRAM 目标（备选） | BG `0x06006340` / `0x06008020`（多屏复用） |

### 索引

与 big / mini 共享同一索引表，同一 OCG/TCG `flag` 机制（见 `card-image-big.md` §索引与 card_id）。

---

## tile 地址公式

```
tile_rom = 0x00FBC080 + tile_block × 1536
```

stride 由加载函数计算为 `tb × 3 × 512 = tb × 1536`（`FUN_080c2d24` 汇编 `lsls r1, r1, #0x9` 即 ×512，前面已 ×3）。

---

## 加载函数（`FUN_080c2d24` 摘要）

```asm
FUN_080c2d24(card_id [u16], oam_slot [u16]):
    ldr  r6, =0x095B5C00    ; INDEX_TABLE
    lsls r2, r3, #0x1       ; r2 = card_id * 2
    ldr  r0, =0x080000AE    ; region byte
    ldrh r0, [r0]
    lsrs r0, r0, #0x8       ; 取高字节
    cmp  r0, #0x4A          ; 'J' ?
    ...                      ; 日版走 flag=0 分支（含 EWRAM 0x02006C2C 位 7 检查）
    ...                      ; 非日版走 flag=1
    orrs r2, r4             ; r2 = card_id*2 | flag
    lsls r0, r2, #0x1
    adds r0, r6, r0         ; 索引表字节偏移
    ldrh r2, [r0]           ; tile_block = u16[INDEX_TABLE + (card_id*2+flag)*2]
    lsls r1, r2, #0x1
    adds r1, r1, r2         ; r1 = tb * 3
    lsls r1, r1, #0x9       ; r1 = tb * 3 * 512 = tb * 1536
    ldr  r0, =0x08FBC080    ; TILE_BASE
    adds r4, r1, r0         ; tile_ptr = base + tb * 1536
    lsls r0, r5, #0x5       ; r0 = oam_slot * 32
    ldr  r1, =0x06010000    ; OBJ VRAM
    adds r5, r0, r1         ; vram_dst
    ; ... 复制 24 tile 到 OBJ
```

---

## 导出覆盖

覆盖 card_id 0..2097（与 big / mini 共享索引），导出 PNG 数量与 big 同（2331 独立 tile_block）。

---

## 相关文件

| 文件 | 内容 |
|------|------|
| `data/card-medium-frame.s` | 结构化汇编（label + 2331 条 `.incbin`） |
| `graphics/bin/card-medium-frame/tiles/tb{0000..2330}.bin` | tile 原始数据 |
| `graphics/images/card-medium-frame/card_{0000..2097}[_ocg\|_tcg].png` | PNG 预览 |
| `tools/rom-export/export_card_medium_frame.py` | 导出脚本 |
