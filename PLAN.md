# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ~~⭐⭐~~ | ~~**P2-palette**~~ | ~~卡列表小图 OBJ 256 色调色板 ROM 源未定位~~ | ✓ **2026-04-19 完成**：card-mini-frame 有 OBJ + BG 两套调色板（ROM 0x09E31614 / 0x08510460），模块已从 `card-list-images` 重命名。详见 `doc/dev/card-mini-frame-export.md` |
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |

---

## 内嵌文件系统（2026-04-17 识别，2026-04-23 全解）

ROM 内有 Konami 自写的文件系统（NNS g2d 资源 + .ydc 卡组 + .ydq 谜题 + .LZ5bg 背景），
基址 `0x1E64684`，共 `0x70420` 字节（**339** 个文件，含 FID 339 orphan palette）。

- ✓ 索引表已结构化：`data/fs-tables.s`（`offset_table` + `size_table`, 2716 B）
- ✓ 路径表已结构化：`data/file-paths.s`（339 条 null 终止 ASCII）
- ✓ **FS 原始字节全量导出**（2026-04-23 修正后）：`tools/rom-export/export_fs_files.py` →
  `fs/<orig path>` + `data/fs-payload.s`（339 文件 FID 1..339，byte-identical）。
  path[i] ↔ FID[i+1] 正确映射；99 组重名用 `_dupN` 消歧（2-way 为 OCG/TCG 变体，
  exodia02 的 2 组 3-way 经 A4 确认为字节相同冗余发布 bug）。
- ✓ **所有 89 个 LZ77 容器（63 NNS + 26 LZ5bg）已解压**到 `fs-decompressed/`
- ✓ **NNS 解析器**：`export_nns_parsed.py` 解 4 类格式 + 生成 palette/tile PNG，
  共享库 `_nns_lib.py` 供 C 系列渲染脚本复用
- ✓ **UI 静态帧渲染**：
  - C1 title 6 语言 OBJ 层（`title_obj_{e,f,g,i,j,s}`）
  - C2 name/pass input UI cells
  - C3 demo cutscene cells + NANR 序列关键帧
- ✓ **`.LZ5bg` 逆向完成**：并非私有压缩，实为 LZ77 + Konami wrapper + NitroSDK 风格
  `NTBG` 容器（`PALT` / `BGDT` / `DFPL` 三块）。见 `doc/temp/nns-format-notes.md` §9.1。
- ✓ **`.ydc` / `.ydq` 结构化**：215 ydc → `data/ydc-all.s`（header + body + tail），
  35 ydq → `data/duel-puzzles-v2.s`（INI 结构化）；均 byte-identical 可重建。
- ✓ **OCG/TCG flag 代码级确认**（D1）：`0x080000AE` 在 asm 有 24 处引用，14 处规范模板
  `ldrh+lsrs+cmp 'J'+IRAM fallback`。BY6E 游戏代码第 4 字 `'E' ≠ 'J'` → flag=1 (TCG)。
- ✓ **FS 尾段分段**（D2）：`0x1ED4AA4..0x2000000` = 1.17 MB。段 B 2 KB 稀疏 pointer table，
  段 C 1.22 MB 均匀高熵（疑 ROM padding 或 PRNG），推翻 prompt "125 KB NitroSDK 串池" 假设。
- ✓ **历史 bug #12 修复**（2026-04-23）：`export_fs_files.py` 的 path/FID off-by-one 修正，
  fs/ 下 100% 文件名与内容对齐，新增 fs/titleEx/title_obj_s.LZnclr 捕获 FID 339 orphan。

**后续 FS 深化（优先级较低）**：

| 优先级 | 范围 | 目标 |
|---|---|---|
| ⭐ | `.LZ5bg` BGDT/DFPL 内部字段 | 逆 BG tile pixel 格式 + screen layout 映射；用于 C1 title BG 层 |
| ⭐ | C1 title 画面 BG 合成 | 用 `.gbtn` 补 BG 层；当前 C1 仅 OBJ |
| ⭐ | `.ydc` 语义解码（B1 第二阶段） | 解 3 种 4B key（`4f57443f`/`7f217741`/`39a7cf42`）含义、body `so_code*4\|qty` 编码验证、tail 字段用途（LV2_kaeru 等含非零数据）|
| ⭐ | `.ydc` loader 追溯 | 反编译定位 OCG/TCG flag 选 FID 的具体函数；顺便可取代 ghidra 未命名 |
| — | FS 尾段 B 区 2 KB pointer table | 追 consumer 反推 C struct；覆盖率收益仅 ~0.006% |

---

## 遗留数据未调查

- ~~ROM `0x001FD568 – 0x0020A500`（~53 KB，被 `card_desc_ptr_table` 269 条文件偏移引用）~~：
  ✓ **2026-04-22 破解**：此"53KB 区"实际是 **card-descriptions pool 的一部分**（ROM `0x15FFF0C` 起的大文本池）。用户指出关键假设（pool 起点 `0x15FFF0C` + lang 顺序 XX/EN/DE/FR/IT/ES）后，验证 Section C 269 条指针加 ET 基址后精确落在 pool 内字符串起点（前一字节全是 null）。进一步发现 Section C 实为 **270 u32** (45 cards × 6 lang)，最末 u32 高 2B 与 card-stats[0].zero0 字节重叠。已合并 `card-effect-text.s` + `card-descriptions.s` 为单一 `card-descriptions.s`（2.14 MB），用 `desc_offsets <cid>` 宏 + label 减法统一表达 2098 卡 × 6 lang offset 表。
- ~~ROM `0x1E58D0C` `deck_id_and_data_array`~~：核实后是项目已有 `data/opponent-card-values.s` (`0x1E58D0E`, 27×32B) 的同一段；wiki 的 "(opponent_id << 16)" stride 注释是 `lsr r4,0x16` (= r4>>22) 的误读，实际 stride 是 32B。无需拆分。

---

## 数据 crystal 跟进事项

- ~~**card-names.s 双重偏差**~~：✓ 已修复（2026-04-17）：
  - 起点改为 `0x15BB594` (含 cid=0 6 langs 占位 12B)
  - lang 顺序改为 `XX/EN/DE/FR/IT/ES`（XX 在最前）
  - 验证：byte-identical SHA1 一致；Blue-Eyes XX = `f8 f7 f4 8c f1 a9 fb d9 fe 91` (5 字符对，匹配 JP "青眼の白龍" 5 字)

- ~~**card-name-pointer-table 真实大小**~~：✓ 已修复（2026-04-22）：原以为 12,612 u32（2102 cards），实际是 **12,588 u32 (2098 cards)**；末尾 24 u32 (cid=2098..2101) 不是合法 name offsets，而是 card-descriptions pool 的前 96 字节（cid=0 dummy 12B + cid=1 XX 84B）。表尾修正为 `0x15FFF0C`，末卡 cid=2097 = Fluffy Token。

- ~~**card-effect-text 合并**~~：✓ 完成（2026-04-22）：
  - 原 `card-effect-text.s` (2 MB, 起 `0x15FFF6C`) + `card-descriptions.s` (起 `0x1800000`) 合并为单一 `card-descriptions.s`，起点 **`0x15FFF0C`**（原以为 `0x15FFF6C`，往前 96 字节才是真实 pool 起点）
  - lang 顺序 **XX/EN/DE/FR/IT/ES**（与 card-names 一致；旧 `card-effect-text.s` 的 "EN/DE/FR/IT/ES/XX" 是错误理解）
  - Section B + C 合并为统一 `card_desc_data`（12,588 u32 = 2098 cards × 6 lang），与 `card_name_pointer_table` 完全同构（都是 per-cid 6-lang offset 表）
  - 用宏 `desc_offsets <cid>` + label 减法表达，异画卡共享 master cid 的 labels
  - 字节重叠：Card 38 XX null / Section B u32[0] / Section A pad 共享 4 B；Section C 最末 u32 高 2B / card_stats[0].zero0 共享 2 B
  - 删除 `tools/rom-export/export_card_effect_text.py` 和 `data/card-effect-text.s`

## 后续研究

- **XX 编码反向工程**：每字符 2 字节自定义编码，含义未知。已在 `refs/yugioh-card-search/` 引入日文五十音排序卡表作为对照数据，待解码（可能是 sort key / 假名压缩）。
- ~~**Ghidra label 脚本未跑**~~：✓ 已落地（21 标签 + 5 函数名），all.s 已重导出，71 处新符号引用。详见 `doc/dev/datacrystal-cross-reference.md`。
