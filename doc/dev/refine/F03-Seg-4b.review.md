# Refine Review: F03-Seg-4b

段范围: `[0x08037ec0, 0x0803a7f0)` — `asm/03_equip_chain_hand.s`
proposal: `doc/dev/refine/F03-Seg-4b.proposal.md`
reviewer: independent (2026-06-11, iter-2 re-review)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致，无跳号/回头 | ✅ | p5-refine-03 roadmap: Seg-4b = [0x37ec0..0x3a7f0)，接 Seg-4a 0x37ec0 无缝；Seg-5 起点 0x3a7f0 明确标出 |
| C2 | 所有 ROM_INCBIN 块有归宿 | ✅ | 唯一 incbin 块 0x39350/0x10ce → R4 disasm（6 子 stub，mov pc,r0 jump table）；无静默保留 |
| C3 | §5.1 块确 0 引用 | N/A | 本段无 §5.1 块，C3 不适用 |
| C4 | EQ value == ROM 4 字节小端 | ✅ | **DAT_08038c84 已修正**：ROM bytes `00 00 18 c6` = LE u32 `0xc6180000` = `0x18c3<<19` (Batteryman AA)；reviewer 独立 Python 验证：`0x18c3<<19=0xc6180000` Match=True；no `.word RESHEF` 残留 |
| C5 | 新建 constants 无现有同值重复 | ✅ | grep constants/*.inc: `BATTERYMAN_AA_CID`/`BATTERYMAN_AA_CID_SHIFTED`/`0xc6180000`/`0x18c3` 均不存在；其余新增常量（LP_COST_{3000,1500}、SCORE_DELTA_NEG_{300,500,700}、SLOT_CARD_EMPTY、HAND_COUNT_TO_SLOT_OFF、FIELD_STATE_OFF、CHAIN_LINK_COUNTER_OFF、EQUIP_PHASE_STATE_OFF）也均无重名 |
| C6 | 槽名合规，无碰撞 | ✅ | **C6 已修正**：0x142d 行 proposed_const 改为 `DARK_MAGICIAN_CID_142D`；注释文字也统一用 `DARK_MAGICIAN_CID_142D`/`DARK_MAGICIAN_CID_0FC9`；无裸 `DARK_MAGICIAN_CID` 出现于可执行表中；全部槽名符合 `^[a-z][a-z0-9_]+$` |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | zone_monster_field_bonus_table (REF×2) + dispatch_equip_node_jump_table (REF×1) 均有 label + DATA-ref 计划 |
| C8 | plate 引用全用现名，无残留 FUN_ | ✅ | **C8 已修正**：§7 PLATE 节现已枚举完整 7 条 FUN_→现名替换映射（asm 行 5895/6148/6287/6399/6423/7420×2），验收标准 grep lines 4335..7634 FUN_ count=0 明确写入；reviewer 独立核实 7 处 FUN_ 均存在且现名正确（FUN_08037ec0→eval_slot_score_entry_full@line4335、FUN_08038dea→compute_lp_cost_by_zone_field5_x200@line6412、FUN_08037c9c→compute_zone_effect_atk_delta@08037c9c、FUN_08036b88→find_effect_entry_by_player_zone@08036b88）|
| C9 | ASCII-only plate/EOL | ✅ | RENAME_SLOTS eol 列全 ASCII；doc 正文 CJK 属 doc/ 范围，不进 Ghidra；无非 ASCII 字符出现于任何 eol/proposed_name 可执行字段 |
| C10 | fn-ptr 表 +1 (THUMB)；carve .word == ROM raw | ✅ | `mov pc,r0` dispatch 维持 CPSR.T，偶地址 THUMB stub 正确；ROM 存 0x08039350 等偶值，`.word eval_equip_node_type_1_to_4`（偶地址，无 +1）匹配；ARMv4T 行为已在 §求助 §5 详述 |
| C11 | FUNC_RENAME 无误名 | ✅ | 15 个函数体操作与函数名一致，FUNC_RENAME=0 |
| C12 | 关键槽语义有 file:line + 置信度 | ✅ | R6 消费者证据节提供 asm/03 行号 + high/med 置信度；zone_monster_field_bonus_table / dispatch_equip_jump_table / gP1HandCountBase / DUEL_ACTIVE_PLAYER_OFF 等关键槽均有 file:line 证据 |
| C13 | 段内所有残留自动名槽 100% 覆盖 | ✅ | asm/03 Seg-4b 范围约 150 个 DAT_/PTR_DAT_ 定义，proposal 全部覆盖（EQ_SLOTS + REF_SLOTS + RENAME_SLOTS 三节合计）；PTR_gP1LifePoints_× 6 已有语义名，proposal 正确列为 REF confirm |

---

## 补充验证 (reviewer 独立复核)

**DAT_08038c84 ROM 字节三重确认**：
```
ROM @ 0x08038c84: bytes = 00 00 18 c6
LE u32             = 0xc6180000
0x18c3 << 19       = 0xc6180000  (Batteryman AA)   MATCH
0x18c6 << 19       = 0xc6300000  (Reshef)          NO MATCH
```

**zone_monster_field_bonus_table entries [7..12] 逐条 ROM 验证**：

| entry | proposal .hword | ROM 匹配 |
|-------|----------------|---------|
| [7]  | 0x1468,0,0x1497,0,0x1498,0,0x1499,0 | ✅ |
| [8]  | 0x149a,0,0xa,0,0x14f9,0,0x154f,0    | ✅ |
| [9]  | 0x1550,0,0x1551,0,0x1730,0,0x1731,0 | ✅ |
| [10] | 0x1670,0,0x1671,0,0x1672,0,0x1288,0 | ✅ |
| [11] | 0x129b,0,0x12b8,0,0xa,0,0x15fb,0    | ✅ |
| [12] | 0x10ef,0,0x17a6,0,0x197b,0,0x1704,0 | ✅ |
| [13] sentinel | 0xffff×8 | ✅ |

entries [0..6] 已在上次 review 验证，本次未退步。结构性注释（`[0..6]=ATK bonuses` vs `[7..12]=CID-encoded`）已在 carve 代码块中明确标注。

**C5 dedup 验证**：`grep -r "BATTERYMAN_AA|0xc6180000|0x18c3" constants/` → 空（Exit 1）。BATTERYMAN_AA_CID / BATTERYMAN_AA_CID_SHIFTED 为全新常量，无冲突。

**C8 FUN_ 映射验证**：reviewer 独立 Python 扫描 asm lines 4335..7634，找到 7 处 FUN_（lines 5895/6148/6287/6399/6423/7420×2），与 proposal 枚举完全一致。FUN_08037ec0@line4335→eval_slot_score_entry_full（现有标签已在 asm/03:4335 确认）；FUN_08038dea@line6399→compute_lp_cost_by_zone_field5_x200（现有标签已在 asm/03:6412 确认）；FUN_08037c9c@line7420→compute_zone_effect_atk_delta（现有标签已在 asm/03:4032, addr=0x08037c9c 确认）；FUN_08036b88@line7420→find_effect_entry_by_player_zone（现有标签已在 asm/03:1679, addr=0x08036b88 确认）。line7634 的 FUN_080c8d30 属 Seg-5 范围，proposal 正确排除。

**C6 无裸 DARK_MAGICIAN_CID**：grep `DARK_MAGICIAN_CID[^_0-9]` 仅命中 Fix iteration 1 说明文字（非可执行指令），EQ 表和注释均已统一为 `DARK_MAGICIAN_CID_142D`/`DARK_MAGICIAN_CID_0FC9`。

---

## 状态: PASS

三项 NEEDS_FIX 均已正确修正，补充 carve 表条目 ROM 验证通过，全项 C1-C13 无新增问题。

---

## 核验方法说明

- **ROM 字节独立核对**：Python `struct.unpack('<I', d[0x8038c84-0x8000000:...])` 直读 `roms/2343.gba`；`0xc6180000` 与 `0x18c3<<19` 算术比对。
- **carve 表 [7..12] 逐条**：Python 读 ROM `0x09e3f094-0x08000000` 偏移处 13×16B，逐行 `struct.unpack('<8H',...)` 与 proposal 值比对，全部 Match=True。
- **C5 常量去重**：PowerShell `grep -r "BATTERYMAN_AA|0xc6180000|0x18c3" constants/` 确认空结果。
- **C6 命名**：grep proposal `DARK_MAGICIAN_CID[^_0-9]` 无可执行表命中。
- **C8 FUN_ scan**：Python 读 asm lines 4334..7634，找到 7 处 FUN_，逐一确认地址→现名映射与 proposal 表一致；grep asm/03 各函数 label 地址确认。
