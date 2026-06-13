# Refine Review: F05-Seg-7

## 段信息

- ROM 范围: `0x0804ffba..0x08050e40`
- asm 文件: `asm/05_equip_eligibility_a.s`
- 函数数: 24
- 实际 .word 槽数: **73** (从 asm 文件精确计数)
- proposal: `doc/dev/refine/F05-Seg-7.proposal.md`

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-6 结束 0x4ffba, Seg-7 起始 0x4ffba, 严格地址序 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块有归宿 | OK | Seg-7 内无 ROM_INCBIN/.byte 块，独立 grep 确认 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 无孤儿块，段内全为代码+函数内 literal pool |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 独立 python 核对 46 个槽值，全部匹配 |
| C5 R1 复用 | 新建 constants 前无同值碰撞 | OK | 22 新 CID 均未在 card_info.inc 出现; 0x1281 碰撞 RELINQUISHED_CID -> RENAME (正确); 0x1cb8 碰撞 DUEL_ACTIVE_PLAYER_OFF (不同 base: 0x0201e198 vs 0x0201e1c8) -> RENAME (正确) |
| C6 R2 名 | 槽名格式合法, 无碰撞 | OK | 50 个 slot label 全通过 `^[a-z][a-z0-9_]+$`, 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | 无 REF_SLOT 需求; PTR_gP1LifePoints_08050510 已正确命名 (ROM 值 0x0201c4e0 = gP1LifePoints 验证通过) |
| C8 R5 现名 | plate 引用全用现名 | OK | Seg-7 范围内 FUN_ 正好 3 处 (FUN_080538e8/FUN_080af120/FUN_0809078c), 均在 PLATE 节列出，CSV 中现名核对正确 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 3 个 RENAME EOL 文本均纯 ASCII; proposal 文档头部的 CJK 是 doc/ 内容, 不进 Ghidra |
| C10 carve | 指针表条目 +1 核对 | N/A | Seg-7 无独立指针表; DAT_08050510 为 PTR_gP1LifePoints, 已正确命名 |
| C11 误名 | 函数名与函数体无矛盾 | OK | 24 函数体操作与函数名一致; proposal 指出 eval_equip_slot_score_by_card_state plate 有 "state_code" 措辞误差, 已计划订正, 不影响函数名 |
| C12 R6 | 关键槽语义有 file:line + 置信度, 无零容忍词 | OK | iter-2 修正: DAT_08050d40 EOL 改为 `low-conf sentinel used in TRIANGLE_ECSTASY_SPARK (0x1840) branch; slot[0]<<19 exact semantics not decoded`; Rationale 节及 R6 消费者证据同步改为 `0x7f280000 >> 19 = 0x0fe5, not 0x1840 directly`; 无错误移位等式, 纯 ASCII |
| C13 残留 | 段内所有残留自动名槽被覆盖 | OK | iter-2 修正: 头部 `74 total` 改 `73 total`, 与 PTR=1+DAT=66+DWORD=6=73 自洽; 覆盖完整性不受影响 |

---

## 状态: PASS (iter-2)

---

## 修改清单

iter-2 全部解决, 无遗留项。

---

## 独立复核证据摘要

1. **ROM 字节核对**: 独立用 `python struct.unpack_from('<I', rom, addr-0x08000000)` 核对全部 46 个已声明槽值 (Group A 21 + Group B 20 + 3 RENAME + PTR 1 + Group C 6 + Group D 22 = 73 个, 全部 OK)。
2. **ref-scan**: 段内无 ROM_INCBIN/.byte, 无需 §5.1 登记。
3. **C5 碰撞扫描**: grep `card_info.inc` 22 个新 CID 值全部不存在 (无碰撞); 0x1281 碰撞已用 RENAME 处理。
4. **C8 FUN_ 扫描**: asm 行 15410-17669 内搜索 `FUN_[0-9a-f]{8}` 得到 3 处, 均在 proposal PLATE 节列出。
5. **CID 卡名验证**: 18 个命名 CID 全部在 `data/card-stats.s` 找到对应 `slot=0xXXXX` 条目; 4 个 cid_xxxx 值在 card-stats.s 中确认无对应条目 (未分配)。
6. **DUEL_ACTIVE_PLAYER_OFF 基址**: gP1LifePoints+0x1cb8=0x0201e198, gDuelFieldSlots+0x1cb8=0x0201e1c8=gEquipZoneCountTable, 两者地址不同, RENAME 策略正确。
7. **fn-ptr 验证**: DAT_08050ff4 (Seg-8 范围, 在 R6 节被引用) ROM 值 0x080502b1 = eval_equip_slot_score_by_card_state+1 (THUMB), 引用链正确。
8. **0x7f280000 sentinel 数学错误**: `(0x1840 << 19) & 0xFFFFFFFF = 0xC2000000 != 0x7f280000`; `0x7f280000 >> 19 = 0x0fe5`。

---

## Reviewer Verdict: F05-Seg-7 = PASS
