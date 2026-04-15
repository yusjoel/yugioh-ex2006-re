# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ⭐⭐ | **P2-palette** | 卡列表小图 OBJ 256 色调色板 ROM 源未定位 | 候选路径见 `doc/dev/card-list-image-export.md` §"未解决：调色板"；可复用 `doc/temp/palram_state*.bin` 做 diff |
| ⭐⭐ | **T-COINFLIP** | Coinflip 界面图形（Top Bar / Coin & Box / Flipping Anim / "Coin Toss Selection" Text）+ tilemap/palette | 地址齐备，见 `doc/um06-romhacking-resource/opponents-coinflip-screen.md`；照 opponents 管线抄 |
| ⭐⭐ | **T-THEME** | Theme Duel 大图 27 对手 × Top/Bottom + palette | 地址 `0x1A1DFAC` 起；同上 |
| ⭐ | **T4** | 主菜单 4bpp 背景（`0x1CF009C`）+ 8bpp 图标（`0x1CF8B94`）；禁卡密码界面图形（`0x1E22874` tilemap, `0x1E314B4` palette） | 先调查 8bpp 解码与尺寸 |
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |
| 🔧 | **T5** | 标题画面 LZ77（`0x1EC33DC`） | 需专门解压工具 |

---

## Ghidra 反向标注

已完成首轮 TG.1–TG.4：`doc/dev/ghidra-function-names.md` + `tools/ghidra-labeling/`。

- [ ] **TG.4-next**（候选）：从已命名函数 XREF 继续爬：
  - `FUN_080ee010` → `load_bg_palette_for_card`（`card_image_decode_wrapper` 内调用）
  - `FUN_0801e640` → `card_list_on_select_to_info_page`（`card_info_page_enter_with_card_id` 的 caller）
  - `FUN_080f0cc0` → `clear_text_line_buffer`（`render_card_description_text` 内）
  - `FUN_080f21e8` → `layout_string_row`（`text_render_wrapper` 的唯一调用目标）
- [ ] **TG.5**（待定）：把 `data/card-names.s` 的 2036 条 `card_name_XXXX` 标签也导进去（当前仅顶层锚点）

---

## 遗留音频/数据未调查

- ROM `0x1844727 – 0x1854FFF`（~70 KB 未知段）
- ROM `0x1832602 – 0x183885B`（~25 KB，含 0xFFFF 哨兵和重复模式）
- ROM `0x01FD568 – 0x01FFFFF`（~150 KB 描述文本压缩，指针表目标）
