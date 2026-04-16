# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ⭐⭐ | **P2-palette** | 卡列表小图 OBJ 256 色调色板 ROM 源未定位 | 候选路径见 `doc/dev/card-list-image-export.md` §"未解决：调色板"；可复用 `doc/temp/palram_state*.bin` 做 diff |
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |

---

## 遗留数据未调查

- ROM `0x001FD568 – 0x0020A500`（~53 KB，被 `card_desc_ptr_table` 269 条文件偏移引用，格式/用途未确认）
