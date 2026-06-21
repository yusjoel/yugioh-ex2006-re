# Refine Review: F10-Seg-5b

Segment: [0x0807ec10, 0x0807f730)
Proposal: `doc/dev/refine/F10-Seg-5b.proposal.md`
Reviewer: independent (no trust in proposal conclusions)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五路线图一致 | OK | Seg-5a [0x7db20,0x7ec10) commit 9404095; 5b [0x7ec10,0x7f730) 紧接; Seg-6 [0x7f730,...) 下一; 无跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | OK | BLK7 0x7f280/0x3c -> R4 disasm (THUMB+1=1); BLK8 0x7f330/0x128 -> R4 disasm (raw=1); 2 switchD 已 decoded 无 incbin; 共 2 incbin 全处理 |
| C3 Rule3 | §5.1 块 0 引用核实 | N/A | proposal §5.1=0; BLK7 thumb+1=1 / BLK8 raw=1; 均有引用 -> 无需 §5.1 |
| C4 R1 值 | EQ value == ROM 4B小端 | OK | 全部 26 个 EQ 槽独立 python 核对 ROM 字节, 0 FAIL |
| C5 R1 复用 | 4 NEW 前无现有同值 | OK | 0x5cc=0 hits / 0x09e59e14=0 hits / 0x157e=0 hits / 0x19ec=0 hits; 22 REUSE 均 grep 确存在 |
| C6 R2 名 | 函数名 + 新常量名合规 | OK | fn_eligible_flute_summoning_kuriboh / dispatch_flute_summoning_kuriboh_by_state_code / FGD_CID / FLUTE_SUMMONING_KURIBOH_CID / ZONE_ENTRY_OFFSET_5CC / EQUIP_DISPLAY_ROM_TABLE_BASE 均 ^[a-z][a-z0-9_]+$ 或 ^[A-Z][A-Z0-9_]+$; 无碰撞 |
| C7 R3 接通 | carve=0; REF_SLOTS 12 个均有 gDuelPhaseFlags/gDuelFieldSlots/gP1HandSlotArray USER-label | OK | 3 个全局已在 ewram.inc 定义; 12 REF slot 值 ROM 独立核对全部通过 |
| C8 R5 现名 | plate stale FUN_ 覆盖完整性 | FAIL | 见 NEEDS_FIX #1: 2 个跨文件 FUN_ (FUN_08054d5c / FUN_080598d8) 指向 asm/06_equip_eligibility_b.s (非 asm/05_*.s); 均已命名; 提案引导 fixer grep 错误文件; 需更正为正确文件与现名 |
| C9 ASCII | plate/EOL 纯 ASCII | FAIL | 见 NEEDS_FIX #2: asm 10 Seg-5b 内存在 2 处 CJK mojibake plate (line 10592-10593 tick_equip_effect_display_state_machine_alt; line 11021-11022 tick_prng_pair_zone_sprite_by_field_card); proposal 未列入 ASCII 重写计划 |
| C10 carve | carve=0; BLK8 跳转表已 decoded .word | OK | 0x7f2bc..0x7f330 共 29 个 .word 已在 asm 中; BLK8 raw=1 来自 0x7f32c 处 .word 0x0807f330 ✅ |
| C11 误名 | 14 fn 名语义与函数体无矛盾 | OK | 无 FUNC_RENAME |
| C12 R6 | 关键槽有 file:line + 置信度 | OK | 6 个关键槽均有 asm 行号 + conf 标注; 无零容忍词 |
| C13 残留 | 段内 44 个 DAT_/DWORD_ 槽全部覆盖 | OK | 独立 python 清点: 26 EQ + 12 REF + 3 PTR_named_skip (gP1LifePoints 已符号化) + 2 switchD pool skip + 1 BLK8_base (DAT_0807f330 由 disasm 消除) = 44; 无遗漏, 无双计 |

---

## 追加核验 (disasm 专项)

### BLK7 fn_eligible_flute_summoning_kuriboh [0x0807f280..0x0807f2bc)

- ref-scan 独立复核: raw=0, THUMB+1=1 @ ROM[0x09e430d0]=0x0807f281 ✅
- FS entry 0x09e430c0: [+12]=0x000019ec (CID=FLUTE_SUMMONING_KURIBOH_CID), [+16]=0x0807f281 (BLK7 THUMB+1) ✅
- CID 距离 fn_eligible ptr: -4 字节 (fn_ptr@[+16] vs CID@[+12]); 该表 stride=0x18; 与活动文档 "-0xc" 描述不同但不影响正确性 (两种 FS 表格式不同)
- ROM[0x7f2b0]=0x4687 (MOV PC,r0) ✅; ROM[0x7f2b8]=0x0807f2bc (jump table ptr) ✅
- card-stats.s card_2070: "The Flute of Summoning Kuriboh slot=0x19EC" ✅

### BLK8 dispatch_flute_summoning_kuriboh_by_state_code [0x0807f330..0x0807f458)

- ref-scan 独立复核: raw=1 @ 0x7f32c (.word 0x0807f330 已 decoded), THUMB+1=0 ✅
- 函数大小 0x128=296B; 0x7f330+0x128=0x7f458 ✅
- 实际 epilogue (ROM 字节): 0x7f450=0xbc70 (pop {r4,r5,r6}), 0x7f452=0xbc02 (pop {r1}), 0x7f454=0x4708 (bx r1)
  - Proposal 描述 "pop {r4,r5}" 有误 -- 实际是 pop {r4,r5,r6}; 但函数边界和大小均正确; 此为 descriptive 误差, 不影响 disasm 计划
- BLK8 中 6 个 case 入口地址均在 [0x7f330,0x7f458) 内; 29 个 jump table 条目全部覆盖 ✅

### switchD 验证

- switchD_0807ed22 @ 0x7ed22: .hword 0x4687 已是 code (非 data); caseD 标签已存在; DAT_0807ed28 -> .word 0x0807ed2c (switchD data 地址已标) ✅
- switchD_0807ee92 @ 0x7ee92: 同上 ✅
- 两者均在 5b 范围 [0x7ec10,0x7f730) 内; proposal 正确认定已 decoded, 无 R4 动作 ✅

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 -- C8 -- 跨文件 FUN_ 现名及搜索文件错误

**问题**: proposal 说 "mark for Seg-5b fixer to grep asm/05_*.s"; 实际地址在 asm/06_equip_eligibility_b.s; 且两个函数均已命名。

**修改**:

在 proposal PLATE 节的跨文件说明中:
- `FUN_08054d5c` -> 现名 `check_equip_slot_eligible_by_display_criteria_loop` (asm/06_equip_eligibility_b.s line 3309)
- `FUN_080598d8` -> 现名 `tick_equip_atk_zone_sprite_display_seq` (asm/06_equip_eligibility_b.s line 15141)

Fixer 落地时: 将 asm/10_equip_effect_dispatch.s line 11578 中的 `FUN_08054d5c` 和 `FUN_080598d8` 替换为上述现名 (ASCII, 无空格)。

涉及的 plate 行:
```
@ Called by FUN_08054d5c and FUN_080598d8 (card frame / equip activation check chain) and FUN_0807f848/0807f8f0.
```
应改为:
```
@ Called by check_equip_slot_eligible_by_display_criteria_loop and tick_equip_atk_zone_sprite_display_seq (card frame / equip activation check chain) and check_equip_slot_criteria_by_state_code_any/find_first_equip_slot_criteria_by_state_code.
```
(全 ASCII; FUN_0807f848 -> check_equip_slot_criteria_by_state_code_any; FUN_0807f8f0 -> find_first_equip_slot_criteria_by_state_code; 均在 asm/10 已命名)

### #2 -- C9 -- 2 处 CJK mojibake plate 需 ASCII 重写

**问题**: Seg-5b 范围内 asm 文件存在 2 处现有 CJK 编码 plate, proposal 未列入 ASCII 重写计划。

**修改**: Fixer 须在落地 Ghidra 脚本中对以下 2 个函数重写 plate comment (纯 ASCII):

**A) tick_equip_effect_display_state_machine_alt (0x0807ed04)** -- asm line 10592-10593:
- 现状: CJK 汉字 plate
- 须改写为 ASCII-only plate (函数已有 Constants 节 ASCII 内容可保留; 只需将 CJK 描述行改为 English 或删去)

**B) tick_prng_pair_zone_sprite_by_field_card (0x0807f0a4)** -- asm line 11021-11022:
- 现状: CJK 汉字 plate
- 须改写为 ASCII-only plate

建议 ASCII 替换文本:

For tick_equip_effect_display_state_machine_alt:
```
@ 29-case switch state machine frame driver for equip card effect display (sibling of 0807d104).
@ Reads state=[IWRAM+0x4a0]-0x64, routes: 0x80->lookup+dispatch_effect_by_card_id; 0x7e->init_display_ctx; 0x7d->get_monster_slot_entry_ptr pair; 0x78->count_field_cards_pair; 0x64->check_card_type_is_spell.
```

For tick_prng_pair_zone_sprite_by_field_card:
```
@ 3-step frame state machine for rendering paired-zone sprite after prng sampling.
@ Routes on [IWRAM+0x4a0]: 0x80->increment_lp_bar_display_counter + reset [IWRAM+0x4a4]=0; 0x7f->sample_prng + render_pair_zone_sprites; 0x7e->decrement_lp_bar_display_counter.
```

---

## 自检

- Review 文档本身 (本文件) 的中文说明为 doc/ 内容, 允许 CJK。
- 引用的 plate 文本均照搬 ASCII (含建议改写内容均为 ASCII)。
- 未动 Ghidra / 未写 .py / 未 build / 未 commit / 未改 proposal。
