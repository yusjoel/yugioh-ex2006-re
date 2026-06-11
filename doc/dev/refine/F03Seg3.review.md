# Refine Review: F03Seg3

段范围: [0x08037128, 0x08037904), file 03_equip_chain_hand.s
13 named fn + 1 unlabeled fn at 0x0803777c
Proposal: doc/dev/refine/F03Seg3.proposal.md
Reviewer date: 2026-06-11 (Round 1) / 2026-06-11 (Round 2)

---

## 核验 (C1-C13) — Round 2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段边界与 §五 路线图一致 | PASS | roadmap Seg-3 = 0x37128..0x37904, 与 proposal 一致; 未跳号 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块有归宿 | PASS | Seg-3 无 ROM_INCBIN 块; 仅 .zero 0x2 对齐 pad |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无独立数据块 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 37 个 DAT_/DWORD_ 槽全量核对 (Round 1 完成); 未改动, 无回归 |
| C5 R1 复用 | 新建常量前无现有可复用 | PASS | 同 Round 1; fixer 未改常量定义 |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$ | **PASS** | 0 处 _gP1LP 残留; 全 65 个 slot_label 纯小写; 13 个 _lp_ptr 槽全部就位 (1 EQ + 12 REF) |
| C7 R3 接通 | fn-ptr 槽有 USER-label + DATA-ref 计划 | PASS | 同 Round 1 |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | PASS | 同 Round 1 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 16 个代码块全量扫描: 0 个非 ASCII 字符; 非 ASCII 仅在 proposal 中文注释散文行 |
| C10 carve | fn-ptr DAT_08037884 = 0x0803777d | PASS | 同 Round 1 (ref-scan 2 处, Seg-3 + Seg-4) |
| C11 误名 | 函数名无 FUNC_RENAME 遗漏 | PASS | 同 Round 1 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | 同 Round 1; 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽全覆盖 | PASS | 49 个 (37 DAT_/DWORD_ + 12 PTR_gP1LifePoints) 全覆盖; 同 Round 1 |

---

## Round 2 独立核验结果

### C6 重跑 (核心修正项)

- `_gP1LP` 后缀残留: **0 处** (全文搜索, 无命中)
- `_lp_ptr` 槽 label: **13 处** (表格 last-cell 提取)
  - EQ 表: `count_graveyard_entries_by_card_id_lp_ptr` (line 96) — DWORD_0803716c, gP1LifePoints 常量
  - REF 表 (12 个 PTR_gP1LifePoints_*): 全部改为 `<func>_lp_ptr` 格式
- 全 65 个 slot_label 均符合 `^[a-z][a-z0-9_]+$`

### replace_all 误改检查

- `PTR_gP1LifePoints_` 出现 27 次: 12 处槽清单 (目标名保留) + 12 处 REF 表 slot 列 + 1 处 section header + 1 处 RENAME_SLOTS 备注 + 1 处 Executor Report = 正确, 无误改
- Executor Report 行 (`12 PTR_gP1LifePoints + 1 fn-ptr`) 完整保留, 未被替换为 `_lp_ptr`
- REF 表地址列与 Round 1 一致: 12 个 PTR 地址 (0x080371f4 .. 0x080378d8) 全部正确

### C9 全量扫描

- 16 个代码块 (`(三连反引号)...(三连反引号)` 内容): **0 个非 ASCII**
- 非 ASCII 570 字符均在 proposal 中文注释行 (section title / prose), 不写入 Ghidra

---

## 状态: PASS

修改清单: 无 (Round 1 唯一 NEEDS_FIX 项 C6 已完全修复, 无新问题引入)

---

## 非阻塞备注 (继承自 Round 1, 供 fixer 参考)

1. Executor Report 行 "EQ=36 (reuse 24 + new 12)" 与头部 "EQ=36 (reuse 25 + new 11)" 计数约定差异: 不影响功能正确性。
2. duel_field.inc FIELD_ARRAY_C_TO_COUNT_NEG_OFF 注释 "2 raw refs" 偏低 (全 ROM 实际 ~10 处): 建议 fixer 改为准确值, 非阻塞。
