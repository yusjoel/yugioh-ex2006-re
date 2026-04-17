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
- ~~ROM `0x1E58D0C` `deck_id_and_data_array`~~：核实后是项目已有 `data/opponent-card-values.s` (`0x1E58D0E`, 27×32B) 的同一段；wiki 的 "(opponent_id << 16)" stride 注释是 `lsr r4,0x16` (= r4>>22) 的误读，实际 stride 是 32B。无需拆分。

---

## 数据 crystal 跟进事项（来自 2026-04-17 拆分）

- ⭐ **card-names.s 双重偏差**（byte-identical 不受影响，但语义不准）：
  1. **起始晚 0x18 字节**：应自 `0x15BB594` 起（含 cid=0 6 langs 占位槽 24 B），项目自 `0x15BB5AC` 起。
  2. **lang 顺序错位**：实际 ROM 顺序是 `XX/EN/DE/FR/IT/ES`（lang_id 0=XX），项目假设 `EN/DE/FR/IT/ES/XX`。
     结果：项目每张卡的"XX"标签实际对应**下一张唯一卡**的 XX 串。
  
  修复步骤：重写 `export_card_data.py`（处理 cid=0 空槽 + 修正 LANG_NAMES 顺序为 `XX/EN/DE/FR/IT/ES`）+ 调整 `asm/rom.s` 兜底 `.incbin` 大小。验证以指针表 `data/card-name-pointer-table.s` 为基准。
- ~~**Ghidra label 脚本未跑**~~：✓ 已落地（21 标签 + 5 函数名），all.s 已重导出，71 处新符号引用。详见 `doc/dev/datacrystal-cross-reference.md`。
