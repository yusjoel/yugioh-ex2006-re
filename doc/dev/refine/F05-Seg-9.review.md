# Refine Review: F05-Seg-9

Seg range: ROM `0x08051cc4..0x08052df8`, asm `05_equip_eligibility_a.s` lines ~19855-22387.
Split: Seg-9a `0x08051cc4..0x080525d0` / Seg-9b `0x080525d0..0x08052df8`.
ROM: `roms/2343.gba`.  Reviewer ran all checks independently.

---

## iter-2 re-review (2026-06-13)

iter-1 NEEDS_FIX(4) 项已由 fixer mode A 修订。重核如下。

### #1 (C13 边界泄漏) 复核

独立 python 验证:

- 8 个 Seg-10 槽 (0x08052e4c/e50/e54/ebc/ec0/f04/f44/f48) 地址全部 >= 0x08052df8 (verified True x8)。
- 独立计数 asm lines 19855-22387 内 DAT_/DWORD_ label 定义: **117** (python script, 与 proposal 一致)。
- 117 个 labels 中无一 addr >= 0x08052df8 (outside count = 0)。
- 算术自洽: 66 structural + 19 CID-reuse + 27 CID-new + 4 zone-mask RENAME + 1 cid_13b0 RENAME = **117**。
- Executor Report 已更新为 `EQ=112 (66 structural + 19 CID-reuse + 27 CID-new) RENAME=5`; EQ+RENAME=117。

**结论: #1 已修复, C13 PASS。**

### #2 (new CID 计数 27 vs 28) 复核

- 提案 "New Constants" 代码块独立计数 `.equ` 条目: **27** (SUMMONED_SKULL_CID 至 PHOTON_GENERATOR_UNIT_CID)。
- `cid_13b0` 为 RENAME 槽, 未列入 new EQ 块 (正确)。
- Segment Survey 表: "27 new CIDs | 27 | EQ new" (已修正)。
- C13 reconciliation: "EQ new CIDs: 27 slots" (已修正)。
- Executor Report: "27 CID-new" (已修正)。

**结论: #2 已修复。**

### #3 (CID-reuse 19 vs 18) 复核

- 提案 "Existing CID constants (19 slots, 18 unique values)" 节标题已修正。
- C13 reconciliation: "Total existing CID reuse slots: 2 + 17 = 19" (已修正)。
- Executor Report: "19 CID-reuse" (已修正)。
- 独立计数: 0x0fc9 x2 + 17 其他 unique = 19 slots, 18 unique values (python 验证)。

**结论: #3 已修复。**

### #4 (passcode 注释) 复核

独立核对 `data/card-stats.s`:

| 常量 | 提案 pw | card-stats.s | 匹配 |
|------|---------|--------------|------|
| MINEFIELD_ERUPTION_CID (0x18d6) | 85519211 | 85519211 | PASS |
| DOUBLE_ATTACK_CID (0x18cb) | 34187685 | 34187685 | PASS |
| MULTIPLY_CID (0x12c5) | 40703222 | 40703222 | PASS |

slot_id 值均经 python ROM 读取确认 (0x08052494=0x18d6, 0x08052bb8=0x18cb, 0x08051d40=0x12c5)。

**结论: #4 已修复。**

---

## 核验 (C1-C13) -- iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致, 未跳号/回头 | PASS | Seg-8 (6c92afe 已落), Seg-9 正确接续 |
| C2 Rule2 | ROM_INCBIN/.byte 块 | PASS | 段内 ROM_INCBIN=0, .byte=0 (grep 确认) |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 段内无 ROM_INCBIN, 无须 ref-scan |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | structural slots + 3 pw slots python ROM 读取逐一匹配; 4 packed mask python verified (0x9e380000>>19=0x13c7 等) |
| C5 R1 复用 | 新建常量无同值碰撞 | PASS | 27 new CID 值在 constants/*.inc 无碰撞; 5 RENAME label 无名称碰撞 |
| C6 R2 名 | 槽名格式合规无碰撞 | PASS | 5 RENAME label (`revival_jam_zone_mask`/`cathedral_of_nobles_zone_mask`/`transcendent_wings_zone_mask`/`mine_golem_zone_mask`/`cid_13b0`) 均符合 `^[a-z][a-z0-9_]+$` |
| C7 R3 接通 | carve/全局槽 USER-label + DATA-ref | N/A | 无 carve/disasm; RENAME 为 literal pool 原地 rename |
| C8 R5 现名 | 无残留 stale FUN_ (plate/EOL) | PASS | Seg-9 asm 范围 grep: 2 处 FUN_ 均在 plate 替换计划中 (invoke_count_zone_pair_hits_full_range + check_equip_slot_eligible_by_setcode_activation_and_zone_pair); proposal 文档内 FUN_ 引用均为记录性文字, 非写入 Ghidra 的 plate/EOL 内容 |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | asm Seg-9 范围 0 non-ASCII; proposal doc 第 360 行含 U+2014 em dash 为 doc 本身散文 (非 Ghidra plate/EOL 内容), 不违 C9 |
| C10 carve | fn-ptr +1 | N/A | Seg-9 全 .word 槽 0 个 THUMB fn-ptr (+1) |
| C11 误名 | 函数名与函数体一致 | PASS | 24 fn 名 `check_equip_slot_eligible_by_*`; 函数体均操作 gDuelFieldSlots+PLAYER_BLOCK_STRIDE; 无误名信号 |
| C12 R6 | 关键槽有 file:line + 置信度证据 | PASS | gEquipChainSlotRefs (asm 21293-21300 + 21487-21492), revival_jam_zone_mask (asm 21475-21479 + python 0x9e380000>>19=0x13c7), chain_list 3 偏移槽证据完整; 全标 high confidence |
| C13 残留 | 段内所有 DAT_/DWORD_ 槽 100% 覆盖 | PASS | python 独立计数 117, 算术自洽 66+19+27+5=117, 无 Seg-10 槽泄漏 |

---

## 状态: PASS

iter-1 NEEDS_FIX(4) 全部解决。C1-C13 全部 PASS。

---

## iter-1 修改清单 (已解决, 存档)

### #1 -- C13 -- 8 个 Seg-10 槽混入 (已修复)
DWORD_08052e4c/e50/e54/ebc/ec0/f04/f44/f48 (addr >= 0x08052df8) 已从 Seg-9 列表删除; 总数修正 125->117; structural 修正 73->66。

### #2 -- C13 -- new CID 计数 28->27 (已修复)
cid_13b0 归 RENAME, 不列入 new EQ 块; 相关 3 处文字已修正。

### #3 -- C12 -- CID-reuse 节标题 18->19 (已修复)
0x0fc9 占 2 槽; 节标题和 Executor Report 已修正为 19 slots / 18 unique values。

### #4 -- C4 -- 3 个 passcode 注释错误 (已修复)
MINEFIELD_ERUPTION=85519211 / DOUBLE_ATTACK=34187685 / MULTIPLY=40703222 均已订正并核 card-stats.s 确认。
