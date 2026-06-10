# Refine Review: F02-Seg-8

**段范围**: `[0x08032e80, 0x08033654)` — 23 fn, file 02 (`asm/02_text_lp_fieldspell.s`)
**Proposal**: `doc/dev/refine/F02Seg8.proposal.md`
**Reviewer**: 独立复核 (自主重跑所有关键验证)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致, 未跳号/回头 | ✅ | Seg-8 直接跟随 Seg-7 (0x32e80=Seg-7 上界), 无跳号; 路线图表格 §三 Seg-8=0x32e80..0x33654 一致 |
| C2 | 所有 ROM_INCBIN/.byte 块有归宿 | ✅ | Proposal 及 grep 验证: 本段无任何 ROM_INCBIN/.byte 块; 跳过 |
| C3 | §5.1 块确 0 引用 | ✅ | 本段无 §5.1 登记; 无 incbin 块需扫引用; 跳过 |
| C4 | 每个 EQ value == ROM 4 字节小端 | ✅ | 自主 Python 逐槽核对: 40 个 EQ 槽 (含 4 个 PTR_gP1LifePoints) 全部 OK, 0 FAIL |
| C5 | 新建常量前无现有同值 | ✅ | 扫全 19 个 constants/*.inc: 5 个新值 (0x000012be/0x00001432/0x000017ee/0x000016df/0x0201c5ec) 无重复 |
| C6 | 槽名格式合规, 无碰撞 | ✅ | 44 个槽名全部匹配 `^[a-z][a-z0-9_]+$`; 无重复; 无现有 asm 碰撞 |
| C7 | carve/全局槽有 USER-label+DATA-ref 计划 | ✅ | 无 REF_SLOTS; 4 个 PTR_gP1LifePoints 已是 DATA-ref 形式, 走 RENAME |
| C8 | plate 引用全用现名, 无残留旧 FUN_ | ✅ | 独立 grep 验证: Seg-8 内唯一 stale 主语 FUN_08032f00 在 L15409 (count_eligible_zone_slots_all_flags 板); P3 全板重写覆盖; 其余 FUN_ (0x080ac584 等) 为 caller 上下文说明, 非 stale 主语 |
| C9 | 所有 plate/EOL 文本纯 ASCII | ✅ | grep 扫 5 个 plate block 及 RENAME EOL 字段: 0 个非 ASCII; 文档 prose 含 CJK 为正常 doc 层, 不入 Ghidra |
| C10 | carve 指针表 +1 (THUMB) | ✅ | 无 carve; 跳过 |
| C11 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | ✅ | **Round-2 验证**: 上轮 C11 修正已全部落实: (1) EQ_NEW 表 L131: GROUND_COLLAPSE_FIELD_CARD_ID=0x1432, slot label check_slot_blocked_ground_collapse_id; (2) EQ_NEW 表 L132: OJAMA_KING_CARD_ID=0x17ee, slot label check_slot_blocked_ojama_king_id; (3) card_info.inc 新增块 L215-216: 两条 .equ 名称正确, 注释含 data.md line/passcode; (4) P2 板 L182: Ground_Collapse_id=0x1432, OjamaKing_id=0x17ee. 残留 "Yami" 仅在消费者证据 L240 描述旧 plate 时以历史注记出现, 不是常量名或 Ghidra 板文本, C11 合规. |
| C12 | 关键槽语义有 file:line + 置信度证据, 无零容忍词 | ✅ | 消费者证据表格有 file:line, 置信度 high/med 标注, 无零容忍词 |
| C13 | 段内所有残留自动名槽都被覆盖 | ✅ | 独立 grep Seg-8: 44 unique DAT_/PTR_ 标签; 与 proposal EQ38+RENAME6=44 完全吻合 |

---

## 状态: PASS

---

## 观察 (非阻塞)

- **EQ 总数描述笔误**: proposal L86 写 "共 37 个 EQ 槽 (33 复用 + 4 新建卡牌 ID + 1 新建全局地址)" — 33+4+1=38, 非 37; 实际 EQ_REUSE 33 行 + EQ_NEW 5 行 = 38 行与 C13 总覆盖一致, 为文档 prose 算术笔误, 不影响落地正确性, fixer 可顺手修正该行数字.

---

## 验证细节 (Round-2 补充)

- **C11 修正落实确认**: grep `Yami|YAMI|Sanctuary|SANCTUARY` proposal → 仅 L240 一处历史注记, 无常量名残留; grep `GROUND_COLLAPSE|OJAMA_KING|ground_collapse|ojama_king` → EQ_NEW 表 (L131/132), card_info.inc 块 (L215/216), 消费者证据 (L240/241), P2 plate (L182) 全部正确.
- **C4/C13 从 Round-1 延续**: 40 EQ ROM 字节核对 100% 通过; 44 槽完全覆盖.
- **C9 plate ASCII 确认**: P1/P2/P3 板文本及所有 RENAME EOL 字段均纯 ASCII; CJK 仅在文档 prose 段.
- **gDuelFieldSpellZoneBase 派生**: gDuelFieldSlots(0x0201c510) + 11*0x14 = 0x0201c5ec ✅.
- **0x000013d4 衍生**: gEquipNodePool(0x0201d9c0) - gDuelFieldSpellZoneBase(0x0201c5ec) = 0x13d4 ✅; 1 raw ref, RENAME 合理.
