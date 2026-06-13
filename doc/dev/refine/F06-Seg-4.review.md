# Refine Review: F06-Seg-4

Segment: `0x08055440..0x080565e8`, 22 fn, `asm/06_equip_eligibility_b.s`
Reviewer: independent re-scan (no trust in proposal conclusions)
Iteration: 3 (iter-2 NEEDS_FIX(2): #4 UMI_CARD_ID / #5 cid_12c6; fixer mode A applied; re-reviewed here)

---

## 独立复核方法 (iter-3)

- ROM 字节: `struct.unpack_from('<I', rom, addr-0x08000000)` 逐槽核验 (iter-1 完成, iter-3 补核 fix #4/#5)
- 残留 slot 计数: python regex `^(DAT_|DWORD_|PTR_)[0-9a-fA-F]{8}:` grep asm/06 范围 [4427..7216] (iter-1 完成)
- C5 (所有新建 CID): python 逐值 grep constants/card_info.inc — **本轮独立重跑** (55 个全核)
- C8: asm/06 lines 4427-7216 FUN_ 穷举 — iter-2 PASS, 本轮不变
- fix #4/#5: ROM 字节 + card_info.inc 行号 + proposal 两处改写 逐条核验

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | PASS | 0x55440..0x565e8; 前 Seg-3 已完成 (roadmap Seg-4 ⬜→进行中) |
| C2 | 所有 ROM_INCBIN/.byte 块有归宿 | PASS | 段内无 ROM_INCBIN/.byte |
| C3 | §5.1 块 0 引用确认 | N/A | 无数据块 |
| C4 | 每个 EQ value == ROM 4 字节小端 | PASS | 全 153 槽 python 核验 (iter-1); fix #4/#5 iter-3 再验 ✓ |
| C5 | 新建 constants 无现有重复值 | PASS | 55 新建 CID 全核 0 命中; fix #4 UMI_CARD_ID 复用; fix #5 cid_12c6 复用 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 所有 RENAME/DWORD_ 标签符合格式; 无重复 |
| C7 | carve/全局槽 USER-label + DATA-ref | PASS | fn-ptr 0x08055770=0x080525d1 (+1 THUMB 已验) |
| C8 | plate 无残留 `FUN_` (Seg-4 行范围内) | PASS | P4 双替换 + P2 全段重写 覆盖 line 6830/7169; line 7214 属 Seg-5 不计 |
| C9 | plate/EOL 纯 ASCII | PASS | P1-P5 plate 全 ASCII (iter-1 核验) |
| C10 | 指针表条目 +1 (THUMB) | PASS | 0x08055770 = 0x080525d1 (低位=1) ✓ |
| C11 | 误名检查 FUNC_RENAME | PASS | 22 fn 无误名 |
| C12 | R6 关键槽语义有 file:line + 置信度 | PASS | 各关键槽均有 asm/06 行号证据 |
| C13 | 段内残留 slot 100% 覆盖 | PASS | 149 DAT_/DWORD_ + 4 PTR_ = 153 全覆盖 (0x08055770 同时出现在 EQ_SLOTS/REF_SLOTS 各一次, 合并后 153 槽) |

---

## iter-3 两项 fix 核验

### Fix #4 (C5 UMI_CARD_ID): RESOLVED

- proposal EQ_SLOTS L116: `0x080558e4 | DAT_080558e4 | 0x000010f4 | UMI_CARD_ID | card_info.inc 复用 (line 145)` ✓
- ROM 字节: `struct.unpack('<I', rom[0x558e4:0x558e8]) == (0x000010f4,)` ✓
- card_info.inc line 145: `.equ UMI_CARD_ID, 0x000010f4` ✓
- 新建 CID 表 (55 个) 不含 0x10f4 ✓

### Fix #5 (C5 cid_12c6): RESOLVED

- proposal EQ_SLOTS L190: `0x08055f80 | DAT_08055f80 | 0x000012c6 | cid_12c6 | card_info.inc 复用 (line 886)` ✓
- ROM 字节: `struct.unpack('<I', rom[0x55f80:0x55f84]) == (0x000012c6,)` ✓
- card_info.inc line 886: `.equ cid_12c6, 0x000012c6` ✓
- 新建 CID 表 (55 个) 不含 0x12c6 ✓

---

## C5 独立穷举 (iter-3 自主 re-scan)

python 逐值 grep constants/card_info.inc 对全部 55 新建 CID (50 具名 + 5 gap):

```
0x10e7, 0x10f8, 0x1190, 0x11cf, 0x1294, 0x12c3, 0x12de, 0x12fd, 0x12ff,
0x1321, 0x1388, 0x1393, 0x1470, 0x14a7, 0x14b6, 0x14be, 0x14ea, 0x14fd,
0x1519, 0x153f, 0x156a, 0x1599, 0x15a5, 0x15b5, 0x15f1, 0x1617, 0x1634,
0x166c, 0x1685, 0x169d, 0x16a6, 0x1712, 0x1741, 0x175a, 0x1775, 0x179e,
0x17a3, 0x17a7, 0x17bc, 0x17f4, 0x1844, 0x184e, 0x1851, 0x188e, 0x18cc,
0x1908, 0x190e, 0x1916, 0x192b, 0x1932, 0x1975, 0x19af, 0x19b6, 0x19d5, 0x19e2
```

结果: **0 命中** — 所有 55 值不在 card_info.inc 中。C5 PASS。

注: 0x1599 (CARD_SHUFFLE_CID) 在本段新建, 同段第二槽 0x08055ff0 复用该新建常量 (非复用现有);
card_info.inc 中确无 0x1599 (grep 验证)。

---

## C8 独立穷举 (iter-2 结论沿用)

asm/06 lines 4427-7216 FUN_ 穷举:
- line 6830 (P4): `FUN_0805715c` + `FUN_08059be0` → P4 substring replace 两处 ✓
- line 7169 (P2): `FUN_08057430` → P2 full rewrite 消除 ✓
- line 7214 (P3): `FUN_08057430` → addr=0x080565e8=Seg-5 起点, 不属 Seg-4 ✓

落地后 Seg-4 自身 plate 内 FUN_ 数 = 0. C8 PASS.

---

## 附注 (不影响 PASS)

### N1 — 段头标题已更正 (iter-2 N1 修复确认)

`### card_info.inc 新建 CID (55 个)` 标题已由 fixer 更正为 55. ✓

### N2 — 0x1388 双用 (已确认无 C5 冲突)

LP_COST_5000=0x1388 (slot DAT_08055c58) vs lookup_equip_card_score_cid_1388 (gap CID, slot DAT_08055f74)
vs EQUIP_SLOT_CARD_ID_RANGE_MAX (duel_field.inc line 189): 三者同值异域, 豁免 C5。

### N3 — 153 槽计数

槽地址 0x08055770 同时出现在 EQ_SLOTS (L107, fn-ptr 行) 和 REF_SLOTS (L250, 详细定义); 合并
计 1 次 = 153 槽 (EQ 146 + REF 5 + RENAME 3 - 重复 1 = 153). 与 proposal 总览一致。

### N4 — 22 score RENAME 中性标签合理

BST 分支返回值 0x1a5..0x1cf 无统一枚举语义, RENAME-only 处理合理。

### N5 — 概述表 "CID 复用=17" 为过期数字

proposal 槽分类总览 "EQ -- CID 复用 (card_info.inc) | 17" 与实际 EQ_SLOTS 表不符:
EQ_SLOTS 中标注 "card_info.inc 复用" 的行共 36 条 (35 来自已有 card_info.inc + 1 同段内
CARD_SHUFFLE_CID 二次引用). "17" 系早期草稿遗留, 未随 iter 迭代更新.
此数字不影响任何技术操作 (EQ_SLOTS 逐行映射正确), 仅为文档描述不一致. 不阻塞 PASS.

---

## iter-1/2 三项已关闭 fix (历史存档)

### Fix #1 (C5 LP_COST_1500 重建→复用): RESOLVED (iter-2)
### Fix #2 (C5 LP_COST_3000 重建→复用): RESOLVED (iter-2)
### Fix #3 (C8 P4 plate 遗漏 FUN_08059be0): RESOLVED (iter-2)

---

## 状态: PASS

---

## Reviewer Verdict: F06-Seg-4 = PASS
