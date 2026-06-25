# Refine Review: F11-Seg-7

> Reviewer: independent
> Proposal: doc/dev/refine/F11-Seg-7.proposal.md
> Module: asm/11_effect_slot_puzzletext.s [0x0808f86c, 0x08090a78)
> (Roadmap boundary 0x0808f7c0; actual code starts at 0x0808f86c per Seg-6 review)
> Date: 2026-06-26

---

## 独立复核步骤

### C13 slot-count 独立核查

Python 扫描 asm lines 22525 (`scan_field_slots_for_equip_chain_node_bitmap_update`) 到
25028 (`build_equip_candidate_score_table` 前一行):

```
DAT_/DWORD_ slots: 108
PTR_gP1LifePoints_ slots: 9
switchd_base_ slots: 0   (NOT in Seg-7 range)
seg6_pool_ slots:    0   (NOT in Seg-7 range)
ROM_INCBIN / .byte code lines: 1   (L24190 -- REFERENCED stub)
Total DAT_+PTR_: 117
```

**Proposal 声称 121 = 108 + 9 + 1 switchd + 3 seg6_pool。** 经独立核查:
- `switchd_base_f818` 在 L22484 (addr 0x0808f818) — 在 0x0808f86c 之前, 属于 Seg-6 领域
- `seg6_pool_cid_con_f7e8` (L22458), `seg6_pool_lpflag_f7f0` (L22462), `seg6_pool_cid_ron_f854` (L22507) — 均在 0x0808f86c 之前, 属于 Seg-6 的 `enqueue_sprite_by_field_copy_count` 函数体

Seg-7 实际自动命名槽数 = **117** (108 DAT_ + 9 PTR_), 而非 121。Proposal 虚报了 4 个 Seg-6 标签。

### C2/C13 缺失槽: DAT_0808f934

Python 独立枚举发现 `DAT_0808f934` (L22632) 在 Seg-7 范围内, **proposal 中完全未提及**:

```
DAT_0808f934 @ 0x0808f934: value = 0x0808f801
```

`0x0808f801` = THUMB+1 函数指针, 指向 `0x0808f800` (Seg-6 的 `enqueue_sprite_by_field_copy_count`
内嵌 switch-case 体第一条指令: `adds r2,r0,#0`). 用途: L22598 `ldr r2, DAT_0808f934` 后作为
`find_equip_chain_node_by_pred` 的谓词回调传入. 全 ROM raw 引用 = 1 (仅此 literal pool 槽).

此槽既不是常量 equate, 也不是 §5.1 孤儿 -- 它是一个有意义的函数指针 RENAME 槽, 应命名为
`ptr_switch_case_body_f934` 或类似 raw-pointer 格式. **C13 未覆盖该槽 = FAIL.**

Proposal 的 108 DAT_ 声称全覆盖, 但实际只处理了 107 个 DAT_ 槽 (漏了 DAT_0808f934).

### C2 缺失代码块: .byte 与未标记 stub

Python 在 L24190 发现:

```
L24190:     .byte  0x00, 0x20, 0x70, 0x47   @ 0x080904ec-0x080904ef
```

独立 ref-scan:
```
0x080904ec THUMB+1 refs: 10  (all in 0x09e40xxx-0x09e42xxx effect node tables)
```

字节解码: `0x2000` = `movs r0,#0`; `0x4770` = `bx lr` -- 这是一个返回 0 的 4-byte THUMB 函数.

L24191-24192 处存在另一个未标记 stub:
```
movs r0,#0x2    @ 0x080904f0
bx lr           @ 0x080904f2
```
```
0x080904f0 THUMB+1 refs: 9  (all in 0x09e3f6xx-0x09e452xx effect node tables)
```

两个 stub 均有大量 THUMB 引用 (分别 10 和 9), 来源为 `find_card_effect_node_entry` 所查的四张
effect node 描述符表 (TYPE0/1/2/3). 两者都是**有引用的代码块** — Rule 2 要求: 有引用 + THUMB opcode
形态 → R4 disasm + createFunction + 命名.

Proposal 声称 "No ROM_INCBIN or .byte blocks in this segment" 但 L24190 存在 `.byte` 块且有 10 个
THUMB 引用. **C2 FAIL.**

### C4 ROM 字节核对 (18 槽抽查)

Python `struct.unpack_from("<I")` 对 ROM offset = addr - 0x08000000:

```
EFFECT_ZONE_BITMASK_OFF      0x0808f898: expected=000010d0  ROM=000010d0  OK
EQUIP_CHAIN_STEP_OFF         0x0808f89c: expected=00001d28  ROM=00001d28  OK
SPIRIT_REAPER_CID            0x0808f930: expected=00001596  ROM=00001596  OK
BERSERK_GORILLA_CID          0x0808fc50: expected=000016bf  ROM=000016bf  OK
FALLING_DOWN_CID_SHIFTED     0x0808fb9c: expected=b4d00000  ROM=b4d00000  OK
SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED 0x0808ffb0: expected=ba200000 ROM=ba200000 OK
THE_BLOCKMAN_CID_SHIFTED     0x08090114: expected=c0800000  ROM=c0800000  OK
THEINEN_ACTIVATION_PACKED    0x0808fda4: expected=005017c9  ROM=005017c9  OK
SPHINX_ACTIVATION_INIT_TEMPLATE 0x0808fcdc: expected=09e3f18c ROM=09e3f18c OK
EFFECT_NODE_TABLE_TYPE0_BASE 0x08090520: expected=09e3f19c  ROM=09e3f19c  OK
EFFECT_NODE_TABLE_TYPE0_COUNT 0x08090524: expected=000002a3 ROM=000002a3  OK
EFFECT_NODE_TABLE_TYPE1_BASE 0x08090530: expected=09e430fc  ROM=09e430fc  OK
EFFECT_NODE_TABLE_TYPE1_COUNT 0x08090534: expected=00000187 ROM=00000187  OK
EFFECT_NODE_TABLE_TYPE2_BASE 0x08090540: expected=09e455bc  ROM=09e455bc  OK
EFFECT_NODE_TABLE_TYPE3_BASE 0x0809054c: expected=09e46324  ROM=09e46324  OK
PLAYER_BLOCK_STRIDE          0x0808f924: expected=00000868  ROM=00000868  OK
gDuelFieldSlots              0x0808f92c: expected=0201c510  ROM=0201c510  OK
DISPATCH_ACTIVE_FLAG_OFF     0x080904d0: expected=00001d38  ROM=00001d38  OK
```

C4 全部 18 槽 OK.

### C5 NEW 常量 value-grep (12 值)

Python 精确 grep against constants/*.inc (.equ 行, 按值不按名):

```
BERSERK_GORILLA_CID       0x000016bf: 0 exact hits  OK
FALLING_DOWN_CID_SHIFTED  0xb4d00000: 0 hits         OK
SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED 0xba200000: 0 hits OK
THE_BLOCKMAN_CID_SHIFTED  0xc0800000: 0 hits         OK
THEINEN_ACTIVATION_PACKED 0x005017c9: 0 hits         OK
SPHINX_ACTIVATION_INIT_TEMPLATE 0x09e3f18c: 0 hits   OK
EFFECT_NODE_TABLE_TYPE0_BASE 0x09e3f19c: 0 hits      OK
EFFECT_NODE_TABLE_TYPE0_COUNT 0x000002a3: 0 hits     OK
EFFECT_NODE_TABLE_TYPE1_BASE 0x09e430fc: 0 hits      OK
EFFECT_NODE_TABLE_TYPE1_COUNT 0x00000187: 0 EXACT hits OK
  (proposal 正确: 0x1874/0x1875/0x1877/0x187f 等为不同值的 substring 误命中; 精确 0x00000187 不存在)
EFFECT_NODE_TABLE_TYPE2_BASE 0x09e455bc: 0 hits      OK
EFFECT_NODE_TABLE_TYPE3_BASE 0x09e46324: 0 hits      OK
```

C5 全部 12 NEW 常量按值 0 命中. **C5 PASS.**

### CID 与 card-stats.s 核对

```
BERSERK_GORILLA_CID   0x16bf: card-stats.s card_1410 slot=0x16BF pw=39168895  CONFIRMED
FALLING_DOWN CID      0x169a: card-stats.s card_1382 slot=0x169A pw=32919136  CONFIRMED (0xb4d00000>>19=0x169a)
SOUL_ABSORB BONE CID  0x1744: card-stats.s card_1519 slot=0x1744 pw=63012333  CONFIRMED (0xba200000>>19=0x1744)
THE_BLOCKMAN CID      0x1810: card-stats.s card_1689 slot=0x1810 pw=48115277  CONFIRMED (0xc0800000>>19=0x1810)
THEINEN CID           0x17c9: card-stats.s card_1624 slot=0x17C9 pw=87997872  CONFIRMED
```

### Effect node table 大小一致性

```
TYPE0: base=0x09e3f19c  count=0x2a3  entry_size=0xc  end=0x09e41140  (gap to TYPE1: 0x1fbc)
TYPE1: base=0x09e430fc  count=0x187  entry_size=0xc  end=0x09e44350  (gap to TYPE2: 0x126c)
TYPE2: base=0x09e455bc  count=0x8e   entry_size=0xc  end=0x09e45c64  (gap to TYPE3: 0x6c0)
TYPE3: base=0x09e46324  count=0xb7   entry_size=0xc  end=0x09e46bb8
```

Tables are NOT adjacent (gaps exist between each). The counts (from `ldr r2, DAT_..` for TYPE0/1
and `movs r2,#0x8e/0xb7` for TYPE2/3) match ROM-read values exactly. SPHINX_ACTIVATION_INIT_TEMPLATE
at 0x09e3f18c is 0x10 bytes before TYPE0 (4 words of 0xffffffff = empty template). **Table base/count
values all correct.** C5 PASS for these.

### FUNC_RENAME 验证: 0x080905e8

ASM body read at L24337-24372 (`set_equip_activation_state_by_mode_alt` 现名):

- Takes 3 args: r0=card_ptr(r4), r1=param1(r5), r2=param2(r6)
- Calls `find_card_effect_node_entry(card_ptr)`
- Checks `[node+0x8]` (target ptr, not state bit): NULL → return 1
- **ONLY** clears `[gDuelPhaseFlags+0x4bc]` = 0; does NOT set it to 1 first
- Calls `invoke_r3(r4, r5, r6)` (3 args)
- **Zero writes to state/mode bits**; no "mode" parameter exists

Sibling comparison confirms:
- `invoke_effect_node_handler_2arg` (0x080905c0): checks `[node+0xc]`, calls `invoke_r2` (2 args)
- Target (0x080905e8): checks `[node+0x8]`, only clears flag, calls `invoke_r3` (3 args)
- `invoke_effect_node_with_active_flag_3arg` (0x08090624): checks `[node+0x8]`, **SETS** flag=1
  before invoke AND clears on both paths (symmetric fence), calls `invoke_r3` (3 args)

Old name "set_equip_activation_state_by_mode_alt" is wrong (no state set, no mode parameter).
New name "invoke_effect_node_handler_3arg" is accurate (3 args, dispatches via node[+0x8]).
The "_3arg" suffix correctly describes arg count (r4/r5/r6 passed to invoke_r3). **C11 PASS for FUNC_RENAME.**

### C8 stale FUN_ 核对 (6 地址抽查)

All proposed current-name labels verified in respective files:

```
submit_lp_change_indicator_with_chain_check  asm/04 L18841  OK (diff -1 from stated 18842)
dispatch_equip_field_update_by_anim_state    asm/05 L13420  OK (diff -1)
set_equip_activation_state_by_mode           asm/05 L17731  OK (diff -1)
commit_serial_spell_effect_node              asm/10 L2235   OK (diff -1)
invoke_effect_action_with_temp_card_id       asm/10 L24153  OK (diff -1)
find_matching_slot_by_player_zone_card       asm/11 L18578  OK (diff -1)
dispatch_equip_field_scan_sequence           asm/11 L23831  OK
invoke_count_zone_pair_hits_full_range       asm/11 L24582  OK (diff -1)
build_equip_candidate_score_table            asm/11 L25029  OK
run_equip_spell_display_state_machine        asm/12 L12316  OK (diff -1)
dispatch_equip_effect_by_slot_state          asm/13 L6553   OK (diff -1)
dispatch_equip_lp_delta_by_slot_status       asm/13 L6670   OK (diff -1)
apply_lp_delta_if_slot_active                asm/13 L7832   OK (diff -1)
invoke_r2                                    asm/23 L15343  OK
invoke_r3                                    asm/23 L15348  OK (diff -1)
invoke_r8                                    asm/23 L15363  OK (diff -5)
```

All 16 current-name labels exist. Line-number diffs of -1 are systematic (off-by-one between proposal
and asm file — harmless for fixer execution). **C8 PASS** (current names verified correct).

### C9 非 ASCII 核对

Python scan L22525-L25028:
- L24653: CJK plate for `count_effect_node_activations_by_zone` — proposal provides ASCII replacement. PRESENT but planned for replacement.
- L24961: CJK plate for `scan_equip_chain_nodes_for_bitmap_update` — proposal provides ASCII replacement. PRESENT but planned for replacement.
- L25028: CJK plate for `build_equip_candidate_score_table` at segment boundary (next segment, outside Seg-7) — NOT in Seg-7 scope.

The two CJK plates within Seg-7 are correctly identified by the proposal and ASCII replacements are
provided. The ASCII replacements themselves contain only ASCII characters (verified by inspection).
**C9 PASS** (proposal correctly identifies and resolves the 2 CJK plates in scope).

### C11 추가 미명 확인 (5개 함수 spot-check)

- `scan_card_placement_for_activation` (0x0808fc78): body initializes 4-word sp buffer from
  SPHINX_ACTIVATION_INIT_TEMPLATE, loops over CHAIN_NODE_CARD_ARR_OFF entries checking slot type
  0x1b (SPHINX/THEINEN card slot), builds OAM attr with THEINEN_ACTIVATION_PACKED. Name is accurate.
- `dispatch_equip_field_scan_sequence` (0x08090218): body is a chain of ~30 scanner calls; returns 1
  on first hit or 0 if all pass. Name accurate.
- `find_card_effect_node_entry` (0x080904f4): binary search across 4 effect node tables by type bits
  and card_id. Name accurate.
- `count_zone_pair_hits_with_fn_ptr` (0x0809078c): loops r4=0..10 calling fn_ptr(r4) and counting
  nonzero results. Name accurate.
- `apply_equip_lp_delta_by_node_flag` (0x08090988): reads node[+0x4] activation count and
  bit5/bit2 flags. Proposal says "LP delta commit by bit5/bit2 flags" -- consistent.

No additional misnomers detected. **C11 PASS** for spot-checked functions.

### REF_SLOTS (C6/C7 check)

9 PTR_gP1LifePoints_ slots → all renamed to `ptr_lp_xxxx`. This is the RENAME convention
(GAS label pointing to a literal pool entry holding `gP1LifePoints` address). No createDWordWithRef
needed. Consistent with Seg-5/6 handling. **C6/C7 PASS.**

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | 路线图 "Seg-7: 0x808f7c0..0x8090a78"; proposal 声明与路线图一致; Seg-6 review 确认实际代码从 0x808f86c 开始 (0x808f7c0 是 Seg-6 最后一个函数); 无跳号/回头 |
| C2 Rule2 | ❌ | L24190: `.byte 0x00,0x20,0x70,0x47` @0x080904ec 有 10 个 THUMB 引用 (effect node 表); 另 0x080904f0 已反汇编但无函数标签, 有 9 个 THUMB 引用; proposal 声称 "0 .byte blocks" 但两者均为有引用的代码桩, 需 disasm+createFunction+命名 |
| C3 Rule3 | ✅ | 无 §5.1 块; SPHINX_ACTIVATION_INIT_TEMPLATE (0x09e3f18c) raw=1 thumb=0 — 确认有引用; 两个 stub 也有引用, 均非 §5.1 |
| C4 R1 值 | ✅ | 18 槽抽查全部与 ROM LE-word 一致 (含 3 个 CID_SHIFTED + THEINEN_PACKED + SPHINX_TEMPLATE + 4 effect node 表 base/count + PLAYER_BLOCK_STRIDE等) |
| C5 R1 复用 | ✅ | 12 NEW 常量按值 grep constants/*.inc 全部 0 精确命中; TYPE1_COUNT=0x187 proposal 正确分析 0x1874 为 substring 误命中; CID 均有 card-stats.s slot= 行确认 |
| C6 R2 名 | ✅ | 9 ptr_lp_ 标签格式 `ptr_lp_[0-9a-f]{4}` 符合约定; 无格式冲突; 新常量名均符合 `^[A-Z][A-Z0-9_]+$` 格式 |
| C7 R3 接通 | ✅ | 无实际 REF 槽 (PTR_gP1LifePoints_ 作 RENAME, 不需 createDWordWithRef); 无 carve |
| C8 R5 现名 | ✅ | 16 个 stale FUN_ 抽查 6 个: 全部在对应文件找到当前标签定义; 行号 diff -1 为系统性偏移, 不影响执行 |
| C9 ASCII | ✅ | 2 个 CJK 板注释 (L24653/L24961) proposal 均提供了 ASCII 替换文本; 替换文本本身仅含 ASCII; L25028 CJK 属 Seg-8 范围 |
| C10 carve | ✅ | 无 carve; 无 fn-ptr+1 条目 |
| C11 误名 | ✅ | FUNC_RENAME 0x080905e8 正确 (body 无状态写入, 有 3 参数 invoke); spot-check 5 个函数无其他误名 |
| C12 R6 | ✅ | 关键槽均有 asm/11 file:line 证据 + card-stats.s slot= 确认 + conf: high 标注; 无零容忍词 |
| C13 残留 | ❌ | 实际 Seg-7 有 108 DAT_ + 9 PTR_ = 117 槽; proposal 虚报 121 (含 Seg-6 领域的 4 个标签); **DAT_0808f934 (@0x0808f934 值=0x0808f801) 完全未被 proposal 提及** — 1 个 DAT_ 槽漏覆盖; 实际覆盖 107/108 DAT_ + 9/9 PTR_ |

---

## 状态: NEEDS_FIX

---

## 修改清单 (逐条可执行)

### #1 — C2 — 为 0x080904ec 和 0x080904f0 两个有引用 stub 添加 disasm+命名

**问题**: `dispatch_equip_field_scan_sequence` (ends 0x080904ea) 与 `find_card_effect_node_entry`
(starts 0x080904f4) 之间存在 8 字节代码区域:

- `0x080904ec-0x080904ef`: 4 bytes `.byte 0x00,0x20,0x70,0x47` = `movs r0,#0; bx lr` (返回 0)
  — 10 个 THUMB 引用来自 0x09e40c00/18/30/48/1188/11a0/2190/21a8/2910/2c58 (effect node TYPE0/1 表)
- `0x080904f0-0x080904f3`: 已反汇编 (`movs r0,#2; bx lr`, 返回 2) 但无函数标签
  — 9 个 THUMB 引用来自 0x09e3f628/4260/3618/3900/3f90/4380/44a0/4500/5250 (effect node TYPE0/1/2 表)

**操作**:

1. 在 proposal §三 DISASM_PLAN 中添加两个 stub:
   - `stub_return_0_effect_node_result @ 0x080904ec` (4 bytes): DisassembleCommand 0x080904ec/4;
     createFunction; 建议名 `return_effect_node_result_0` (返回常量 0)
   - `stub_return_2_effect_node_result @ 0x080904f0` (4 bytes): clearListing+setTMode 可能已不需要
     (已经反汇编); createFunction; 建议名 `return_effect_node_result_2` (返回常量 2)

2. 两个函数均需 plate comment (说明它们是 effect node 回调的常量返回 stub; indeg=10 和 indeg=9).

3. 这两个地址应加入 CSV sync (2 new fn rows).

**注**: 两函数是纯常量返回 stub (无参数, 直接 bx lr). 在 effect node 表中作为 `fn_activate` 或
`fn_eligible` 字段的空实现/默认值. 命名时可参考 file 10 类似 stub 命名模式.

---

### #2 — C13 — 补充 DAT_0808f934 的处置方案

**问题**: `DAT_0808f934` (@0x0808f934, value=0x0808f801) 在 Seg-7 范围内 (L22632), 但 proposal
完全未提及, 导致 C13 覆盖缺口.

**解码**:
- 值 `0x0808f801` = THUMB+1 函数指针, 指向 `0x0808f800` (Seg-6 `enqueue_sprite_by_field_copy_count`
  内嵌 switch case 体的第一条指令 `adds r2,r0,#0 @ 0808f800`)
- 用途: L22598 `ldr r2, DAT_0808f934` → 传给 `find_equip_chain_node_by_pred` 作谓词回调
- 全 ROM raw 引用 = 1 (仅此 literal pool 槽)

**操作**: 在 proposal §三 EQ/REF_SLOTS 区域添加一条新的 RENAME 处置:

```
| 0x0808f934 | ptr_case_body_f934 | .word 0x0808f801 | RENAME: raw fn-ptr to switch-case body in Seg-6 enqueue_sprite_by_field_copy_count; used as pred callback in find_equip_chain_node_by_pred |
```

EOL comment: `"switch case body fn-ptr for find_equip_chain_node_by_pred callback"`

此槽的值是一个 hardcoded 内部代码地址 (Seg-6 fn 内部), 无法用公共符号表示, raw label 处理合理.
总 RENAME 计数从 9 增至 10 (9 PTR_gP1LP_ + 1 raw fn-ptr).

---

### #3 — C13 count 修正 — 删除虚报的 4 个 Seg-6 标签

**问题**: Proposal C13 Coverage Statement 声称 "121 auto-name labels" 包含:
- 1 `switchd_base_f818` (实际在 L22484 = 0x0808f818, Seg-6 territory)
- 3 `seg6_pool_*` (实际在 L22458/22462/22507, Seg-6 territory)

这 4 个标签均在 Seg-6 的最后一个函数 `enqueue_sprite_by_field_copy_count` (0x0808f7c0) 的函数体内,
地址均 < 0x0808f86c (Seg-7 代码起点).

**操作**: 将 proposal §五 C13 Coverage Statement 更正为:

```
实际 Seg-7 自动命名槽: 108 DAT_ + 9 PTR_ = 117 (不含 Seg-6 的 switchd_base_f818 和 3 个 seg6_pool_ 标签)
+ 新增 1 DAT_0808f934 (fix #2 补充) → 总处理 108 DAT_ + 9 PTR_ = 117 槽 (100%)
```

---

## Reviewer Verdict: F11-Seg-7 = NEEDS_FIX(3 items)
