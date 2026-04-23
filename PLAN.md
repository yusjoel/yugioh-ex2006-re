# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |

---

## 内嵌文件系统深化

主骨架已全部打通（339 文件全量解包 + byte-identical，详见 `doc/dev/fs-export-and-ocg-tcg.md`）。
余下深化任务按优先级：

| 优先级 | 范围 | 目标 |
|---|---|---|
| ⭐ | `.LZ5bg` BGDT/DFPL 内部字段 | 逆 BG tile pixel 格式 + screen layout 映射；用于 C1 title BG 层 |
| ⭐ | C1 title 画面 BG 合成 | 用 `.gbtn` 补 BG 层；当前 C1 仅 OBJ |
| ⭐ | `.ydc` 语义解码（B1 第二阶段） | 解 3 种 4B key（`4f57443f`/`7f217741`/`39a7cf42`）含义、body `so_code*4\|qty` 编码验证、tail 字段用途（LV2_kaeru 等含非零数据）|
| ⭐ | `.ydc` loader 追溯 | 反编译定位 OCG/TCG flag 选 FID 的具体函数；顺便可取代 ghidra 未命名 |
| — | FS 尾段 B 区 2 KB pointer table | 追 consumer 反推 C struct；覆盖率收益仅 ~0.006% |

---

## 后续研究

- **XX 编码反向工程**：每字符 2 字节自定义编码，含义未知。已在 `refs/yugioh-card-search/` 引入日文五十音排序卡表作为对照数据，待解码（可能是 sort key / 假名压缩）。
