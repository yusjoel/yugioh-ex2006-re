# Refine Review: F03Seg1

Segment: [0x08035f54, 0x08036a78), 13 fn, file 03 refine 第 4 文件
第 2 轮 review (fixer 模式 A C5 修正后)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | roadmap p5-refine-03-equip-chain-hand.md §五 Seg-1 [0x35f54..0x36a78) 完全吻合 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | OK | 本段 0 个 incbin 块，无需处理 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 无 §5.1 登记；无 incbin，跳过 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 35 新建 card_info 槽 + 6 ewram/duel_field 槽全部 python struct.unpack 核对通过 (FAIL=0) |
| C5 R1 复用 | 新建 constants 前无同值可复用，无孤儿 | OK | gEffectEntryArray/DUEL_EFFECT_COUNT_OFF 已删除，grep 返回 0；现有 35 新 CID 在 card_info.inc grep 无同名/同值重复 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`，无碰撞 | OK | 84 个 slot label 格式合规，无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label+DATA-ref 计划 | OK | REF=0，无 carve，不适用 |
| C8 R5 现名 | plate 引用全用现名，无残留旧 FUN_ | INFO | 现有 4 条 pre-existing plate（行4/751/1265/1425）含 FUN_（FUN_0803c814/0803ca70/0803279c/08032654/08036674 等，均已命名）；proposal 声称新写 13 条 plate 无 FUN_；fixer 落地后须 grep 段范围函数 plate FUN_==0 验收 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 3 条 RENAME EOL 文本 python 逐字符核验全 ASCII；proposal plate 章节声称 ASCII；fixer 落地验收 |
| C10 carve | 指针表 +1 核对 | OK | 无 carve，不适用 |
| C11 误名 | CID 常量与 card-stats.s 完全吻合 | OK | 35 个新 CID 逐一 ROM bytes 核对全部通过；无新误名 |
| C12 R6 | 关键槽有 file:line + 置信度证据 | OK | 消费者证据表覆盖所有关键槽，均有 asm 行号与置信度 |
| C13 残留 | 段内所有残留自动名槽被覆盖 | OK | grep asm/03_equip_chain_hand.s 段范围内 DAT_/PTR_ = 84；EQ(81)+RENAME(3)=84，精确覆盖 |

---

## 补注：card_info.inc 条数文本不一致 (文档内自洽问题)

proposal 第 274 行写 "共 32 条"，第 318 行写 "32 (excluding 2 reused)"，但 `.equ` 实际块中含 35 个有值常量定义（不含 2 条 "already exists" 行）。Executor Report 第 381 行正确列出 35 个名字。

**功能内容无误**：35 条 `.equ` 全部 ROM bytes 核对通过 (FAIL=0)；35 个名称在现有 card_info.inc 中无重复。"32" 系 proposal 摘要文本计数错误，不影响落地。fixer 模式 B 落地时应将 "共 32 条" 改为 "共 35 条"、"32 (excluding 2 reused)" 改为 "35 (excluding 2 reused)"，或直接以实际 `.equ` 块为准无需保留该行。

此项**不阻塞 PASS**（功能 `.equ` 内容已验证正确）。

---

## 状态: PASS

---

## 附：本轮独立核验摘要

- C5 孤儿清理: grep "gEffectEntryArray\|DUEL_EFFECT_COUNT_OFF" proposal = 0 (已删除)
- C4 ROM bytes 本轮重核: 35 个新建 card_info.inc CID 全部 struct.unpack('<I') 匹配 (OK=35, FAIL=0)
- C4 ewram/duel_field: gDuelPhaseFlags x3 + PHASE_LOCK_FLAG_OFF + EQUIP_SLOT_CARD_ID_RANGE_MAX + NODE_POOL_TO_SLOT_STATE_OFF 全部 ROM 验证通过
- C5 去重: card_info.inc grep 35 新名均无冲突
- C13: asm grep 段范围 auto-label = 84; EQ(81)+RENAME(3) = 84
- C11: FUN_0803279c = count_field_copies_of_card (asm/02 line 14337), FUN_08032654 = count_available_effect_zones (asm/02 line 14165) 均已命名
- card_info.inc 条数文本: proposal "32" 与实际 `.equ` 块 35 条不符；功能内容正确，为文档摘要笔误
