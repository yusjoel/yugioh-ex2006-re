# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ⭐⭐ | **P2-palette** | 卡列表小图 OBJ 256 色调色板 ROM 源未定位 | 候选路径见 `doc/dev/card-list-image-export.md` §"未解决：调色板"；可复用 `doc/temp/palram_state*.bin` 做 diff |
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |

---

## 内嵌文件系统（2026-04-17 新识别）

ROM 内有 Konami 自写的文件系统（NNS g2d 资源 + .ydc 卡组 + .ydq 谜题 + .LZ5bg 背景），基址 `0x1E64684`，共 `0x70420` 字节（339 个文件）。

- ✓ 索引表已结构化：`data/fs-tables.s`（`offset_table` + `size_table`, 2716 B）
- ✓ 解析器已完成：`tools/ad-hoc/nns_extract.py` 解压 63 个 NNS 资源到 `doc/temp/nns_out/`

**后续可做的 FS 数据区拆分（按优先级）**：

| 优先级 | 扩展名 | 数量 | 目标 |
|---|---|---|---|
| ⭐⭐ | `.LZnclr` | 18 | P2-palette 问题的直接依赖：定位各调色板在 PALRAM 中的使用点 |
| ⭐ | `.ydc` / `.ydq` | ~230 / 35 | 现已被 `opponent-decks.s`、`duel-puzzles.s` 部分覆盖，可升级为统一 FS 层 |
| ⭐ | `.LZ5bg` | 26 | 格式未解析（Konami 私有 BG 压缩，压缩头 `0x01`） |
| ⭐ | NNS `.LZn*` tile/cell/anim | 45 | NCGR/NCER/NANR 数据解析 + PNG 渲染，需 palette 对齐 |

---

## 遗留数据未调查

- ROM `0x001FD568 – 0x0020A500`（~53 KB，被 `card_desc_ptr_table` 269 条文件偏移引用，格式/用途未确认）
- ~~ROM `0x1E58D0C` `deck_id_and_data_array`~~：核实后是项目已有 `data/opponent-card-values.s` (`0x1E58D0E`, 27×32B) 的同一段；wiki 的 "(opponent_id << 16)" stride 注释是 `lsr r4,0x16` (= r4>>22) 的误读，实际 stride 是 32B。无需拆分。

---

## 数据 crystal 跟进事项（来自 2026-04-17 拆分）

- ~~**card-names.s 双重偏差**~~：✓ 已修复（2026-04-17）：
  - 起点改为 `0x15BB594` (含 cid=0 6 langs 占位 12B)
  - lang 顺序改为 `XX/EN/DE/FR/IT/ES`（XX 在最前）
  - 验证：byte-identical SHA1 一致；Blue-Eyes XX = `f8 f7 f4 8c f1 a9 fb d9 fe 91` (5 字符对，匹配 JP "青眼の白龍" 5 字)
  - 注：`card-effect-text.s` 是相反的 `EN/DE/FR/IT/ES/XX`（XX 在最后），与 card-names 不同

## 后续研究

- **XX 编码反向工程**：每字符 2 字节自定义编码，含义未知。已在 `refs/yugioh-card-search/` 引入日文五十音排序卡表作为对照数据，待解码（可能是 sort key / 假名压缩）。
- ~~**Ghidra label 脚本未跑**~~：✓ 已落地（21 标签 + 5 函数名），all.s 已重导出，71 处新符号引用。详见 `doc/dev/datacrystal-cross-reference.md`。
