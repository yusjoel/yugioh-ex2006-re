# Refine Review: F07-Seg-3

ROM range: `0x0805e358..0x0805f1cc`  
Module: `asm/07_equip_effect_chain.s` (L5214..~L7250)  
Reviewed: 2026-06-14 (iter-1) / iter-2 re-review: 2026-06-14

---

## 核验 (C1-C13) — iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | 段范围 0x5e358..0x5f1cc 与 §五路线图 Seg-3 一致; 地址序, 未跳号回头 |
| C2 Rule2 | PASS | 4 个 ROM_INCBIN 块全部分配到 DISASM; 0 静默保留 |
| C3 Rule3 | PASS | 独立重跑 ref-scan: 所有 11 sub-fn 均有 THUMB+1 命中在 0x09e4xxxx handler table; §5.1=0 |
| C4 R1 值 | PASS | 全部 25 个 EQ/REF/RENAME 槽的 4 字节值逐一 python 核对 ROM, 全部一致 |
| C5 R1 复用 | PASS | REVIVAL_JAM_CID=0x13c7 和 RED_MOON_BABY_CID=0x1415 在 card_info.inc grep=0 命中 (新建正确); 所有声称复用常量在对应 inc 文件确认存在 |
| C6 R2 名 | PASS | 11 个 disasm 函数名全部改为 verb-first check_ 开头; 逐一验证 `^[a-z][a-z0-9_]+$` 全部通过; 无 cid_ 前缀残留; 无重复 label |
| C7 R3 接通 | PASS | 16 REF 槽均有全局 label (ewram.inc: gDuelFieldSlots/gEquipChainSlotRefs/gP1LifePoints/gP1ZoneHandCount), DATA-ref 计划完整 |
| C8 R5 现名 | PASS | 段内 FUN_ 出现仅在 PLATE 表的 stale→replacement 记录和证据注释中, 不在 Ghidra 写入文本中; 2 个 plate 替换目标确认 |
| C9 ASCII | PASS | Seg-3 范围 L5214..L7250 无非 ASCII 字符; 求助/注释段无 CJK |
| C10 carve | N/A | 无 fn-ptr .word 槽需要 carve; REF 槽全部使用 ewram.inc 全局 label |
| C11 误名 | PASS | 现有 34 个命名函数无函数名与函数体矛盾情况 |
| C12 R6 | PASS | Block1 fn2 语义已订正: "returns 1 if type_field in [6..8], else returns 0 (including type_field > 8 which branches to movs r0,#0)"; 旧错误表述 "nonzero if > 8" 已完全消除; 求助节 L316 亦明确说明 bgt->movs r0,#0 (return 0). 置信度高 |
| C13 残留 | PASS | 段内 DAT_(24) + DWORD_(16) + PTR_(5) = 45 个自动名槽; EQ(24)+REF(16)+RENAME(5)=45, 完全覆盖, 无遗漏 |

---

## 状态: PASS

iter-1 NEEDS_FIX(2 items) 全部解决:

- **#1 (C6/R1)**: 11 个 disasm 函数名已全部改为 verb-first `check_<object>_for_cid_<hex>` 形式; 逐一核验 `^[a-z][a-z0-9_]+$` + 动词开头 + 无 cid_ 前缀 + 无碰撞, 全部 PASS。
- **#2 (C12/R6)**: Block1 fn2 (`check_equip_type_bits_range6_8_for_cid_13fa`) 语义已订正; 提案 L182/L183 明确 bgt@0x805e780→movs r0,#0 (返回 0), 正确语义 "type_field in [6..8] 返回 1, 否则 (含 >8) 返回 0"; 旧错误主张已消除。

---

## 独立复核证据摘要 (iter-1, 保留)

**ref-scan (独立重跑)**:

| 块 | sub-fn | THUMB+1 ref | handler table CID | 核验结果 |
|---|---|---|---|---|
| Block1 0x5e744 | fn1@0x5e744 | 0x9e43948 | 0x13f9 (Fairy Box) | OK |
| Block1 0x5e744 | fn2@0x5e778 | 0x9e407c8 | 0x13fa (Torrential Tribute) | OK |
| Block2 0x5ed4a | fn1@0x5ed4c | 0x9e439c0 | 0x144e (unassigned) | OK |
| Block3 0x5ed8e | fn1@0x5ed90 | 0x9e439f0 + 0x9e47020 | 0x1450 + 0x1855 | OK |
| Block3 0x5ed8e | fn2@0x5edc0 | 0x9e43a08 (THUMB+1 only) | 0x1451 (Dancing Fairy) | OK; raw ref @0x824c74a NOT 4B-aligned, foreign code |
| Block3 0x5ed8e | fn3@0x5edf0 | 0x9e40a38 | 0x1460 (Meteor of Destruction) | OK |
| Block4 0x5ee9c | fn1@0x5ee9c | 0x9e43a38 | 0x1468 (Destiny Board) | OK |
| Block4 0x5ee9c | fn2@0x5eeb8 | 0x9e46618 | 0x146f (Cathedral of Nobles) | OK |
| Block4 0x5ee9c | fn3@0x5eee4 | 0x9e40ae0 | 0x1472 (Embodiment of Apophis) | OK |
| Block4 0x5ee9c | fn4@0x5ef10 | 0x9e40b10 | 0x1475 (Makiu) | OK |
| Block4 0x5ee9c | fn5@0x5ef4c | 0x9e46648 | 0x147f (Jowgen the Spiritualist) | OK |

**fn boundary verification**: Block1 (fn1/fn2 exits via bx lr 0x4770), Block3 (fn1/fn2/fn3 exit bx lr), Block4 (fn1-5 exit pop{r1}/bx r1 = 0xbc02/0x4708). All boundary sizes match proposal.

**LP threshold check**: @0x5ee1c = 0xBB8 = 3000 decimal. Confirmed.

**BEQ/BNE distinction**: Block3 fn1 byte+31 = 0xd1 (BNE), fn2 byte+31 = 0xd0 (BEQ). Confirmed.
