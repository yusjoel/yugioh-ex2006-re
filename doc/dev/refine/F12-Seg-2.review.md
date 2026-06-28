# Refine Review: F12-Seg-2

Segment [0x08094f20, 0x08095ba8), file `asm/12_equip_activation_scan.s`.
15 named functions, 2 ROM_INCBIN blocks (0x95274/0xc0, 0x95b28/0x14).
Reviewer ran all checks independently (ref-scan, ROM byte reads, value greps, C13 slot count).

---

## 独立 ref-scan 结果

### Block1: 0x08095274 / sz=0xc0

Independent scan (raw + THUMB+1, all 2-byte-aligned addresses):

```
raw hits: {0x8095274:2, 0x8095284:1, 0x809528a:1, 0x809528e:1,
           0x8095292:1, 0x809529e:1, 0x80952aa:1, 0x8095304:1, 0x809530a:1}
thumb+1 hits: {} (none)
raw total=10, thumb total=0
```

Jump table at 0x0809524c (10 entries, each 4B):
```
entry[0]: 0x0809530a   entry[1]: 0x0809529e   entry[2]: 0x080952aa
entry[3]: 0x08095292   entry[4]: 0x08095284   entry[5]: 0x0809528a
entry[6]: 0x0809528e   entry[7]: 0x08095274   entry[8]: 0x08095274 (shared)
entry[9]: 0x08095304
```

Dispatch instruction at 0x0809523c: `0x4687` = `mov pc,r0` (raw pointer, not THUMB+1).
Verified: 0x4687 = THUMB-encoded `mov pc, r0` (0x4600 | (1<<7) | 7 = 0x4687).

10 table entries but only **9 unique entry addresses** (entry[7] and [8] both -> 0x8095274).
Proposal disasm plan lists exactly 9 DisassembleCommands. Procedurally correct.

Note on proposal wording: proposal says "10 case blocks" in both the intro text and the disasm
plan title. The accurate count is 9 unique case-block entry points (10 jump-table entries, 2
sharing the same target). The disasm plan itself (9 DCs) is correct; the count description is
misleading but does not affect the outcome.

**Judgment: raw=10 (from jump table), THUMB+1=0 -> R4 disasm CONFIRMED.**

### Block2: 0x08095b28 / sz=0x14

Independent scan (all 2-byte-aligned addresses):

```
raw hits: {} (none)
thumb+1 hits: {} (none)
raw total=0, thumb total=0
```

Fall-through check: preceding function `step_prng_anim_frame` ends at 0x08095b18:
```
0x08095b18: bc70  pop {r4,r5,r6}
0x08095b1a: bc02  pop {r1}
0x08095b1c: 4708  bx r1
0x08095b1e: 0000  .zero 2
```
Explicit pop-bx epilogue. NOT fall-through.

Block2 bytes confirmed:
```
0x08095b28: 4802  ldr r0,[pc,#8]    -> pool @0x08095b34 = 0x0201c4e0 = gP1LifePoints
0x08095b2a: 4903  ldr r1,[pc,#12]   -> pool @0x08095b38 = 0x00001d0c = 0x1d0c
0x08095b2c: 1840  adds r0,r0,r1
0x08095b2e: 2101  movs r1,#1
0x08095b30: 6001  str r1,[r0,#0]    -> [gP1LifePoints+0x1d0c] := 1
0x08095b32: 4770  bx lr
```

**Judgment: raw=0, THUMB+1=0, not fall-through -> §5.1 CONFIRMED.**

---

## ROM 字节核对 (C4 EQ 值)

47 slots verified (all PASS):

| slot addr | proposed value | ROM actual | result |
|-----------|---------------|------------|--------|
| 0x0809501c | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x08095020 | 0x000012c4 | 0x000012c4 | OK |
| 0x08095024 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095028 | 0x00001ce8 | 0x00001ce8 | OK |
| 0x08095080 | 0x00001ce8 | 0x00001ce8 | OK |
| 0x0809507c | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095188 | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x0809518c | 0x00000868 | 0x00000868 | OK |
| 0x08095190 | 0x0201c510 | 0x0201c510 | OK |
| 0x08095204 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095208 | 0x00001d4c | 0x00001d4c | OK |
| 0x0809520c | 0x00001d50 | 0x00001d50 | OK |
| 0x0809521c | 0x00001d50 | 0x00001d50 | OK |
| 0x08095240 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095244 | 0x00001d5c | 0x00001d5c | OK |
| 0x08095248 | 0x0809524c | 0x0809524c | OK |
| 0x08095344 | 0x00001d54 | 0x00001d54 | OK |
| 0x0809535c | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095360 | 0x00001d58 | 0x00001d58 | OK |
| 0x0809537c | 0x00001d54 | 0x00001d54 | OK |
| 0x080953bc | 0xffff0000 | 0xffff0000 | OK |
| 0x080953c0 | 0x0000ffff | 0x0000ffff | OK |
| 0x080953d8 | 0x080953dc | 0x080953dc | OK |
| 0x0809546c | 0x0201b870 | 0x0201b870 | OK |
| 0x08095490 | 0x0201b870 | 0x0201b870 | OK |
| 0x08095494 | 0xfff87fff | 0xfff87fff | OK |
| 0x08095528 | 0x0201b870 | 0x0201b870 | OK |
| 0x08095530 | 0x00001d0c | 0x00001d0c | OK |
| 0x08095638 | 0x0201b872 | 0x0201b872 | OK |
| 0x08095778 | 0x00001d64 | 0x00001d64 | OK |
| 0x080958a8 | 0x00001d84 | 0x00001d84 | OK |
| 0x08095a44 | 0x000010e1 | 0x000010e1 | OK |
| 0x08095a60 | 0x0000030f | 0x0000030f | OK |
| 0x08095910 | 0x00000301 | 0x00000301 | OK |
| 0x0809590c | 0x0000030d | 0x0000030d | OK |
| 0x08095984 | 0x0000030e | 0x0000030e | OK |
| 0x080958cc | 0x000002ff | 0x000002ff | OK |
| 0x08095788 | 0x000002fe | 0x000002fe | OK |
| 0x08095b48 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095b4c | 0x00001d0c | 0x00001d0c | OK |
| 0x08095b94 | 0x0201b870 | 0x0201b870 | OK |
| 0x08095b98 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08095b9c | 0x00001d08 | 0x00001d08 | OK |
| 0x08095ba0 | 0x00001ce8 | 0x00001ce8 | OK |
| 0x08095ba4 | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x08095608 | 0x0201b870 | 0x0201b870 | OK |
| 0x0809560c | 0x0201e2a0 | 0x0201e2a0 | OK |

C4 PASS (47 slots, 0 failures).

---

## C5 dedup 详细

### NEW constants VALUE grep (independent)

| const_name | value | grep hits | ruling |
|-----------|-------|-----------|--------|
| NEGATE_ATTACK_CID | 0x000012c4 | 0 hits | NEW OK |
| LP_EQUIP_STATE_B_OFF | 0x00001d50 | 0 hits | NEW OK |
| LP_DISPLAY_STATE_OFF | 0x00001d0c | 0 hits | NEW OK |
| LP_PLAYER_SIDE_CACHE_OFF | 0x00001d64 | 0 hits | NEW OK |
| LP_EQUIP_DISPLAY_FLAG_OFF | 0x00001d84 | 0 hits | NEW OK |
| LP_ACTIVATION_TYPE_ARRAY_BASE_OFF | 0x000010e1 | 0 hits | NEW OK |
| SPRITE_ROW_BUSY_BYTE_OFF | 0x00000301 | 0 hits | NEW OK |
| SPRITE_ROW_ENTRY_30D_OFF | 0x0000030d | 0 hits | NEW OK |
| SPRITE_ROW_ENTRY_30E_OFF | 0x0000030e | 0 hits | NEW OK |
| SPRITE_ROW_ENTRY_30F_OFF | 0x0000030f | 0 hits | NEW OK |
| SPRITE_ATTR_BYTE_2FE_OFF | 0x000002fe | 0 hits | NEW OK |
| SPRITE_ATTR_BYTE_2FF_OFF | 0x000002ff | 0 hits | NEW OK |
| gSpriteAttrBufData | 0x0201b872 | 0 hits | NEW OK |
| **SPRITE_HIGH_HALF_MASK** | **0xffff0000** | **1 hit** (EQUIP_CHAIN_SENTINEL, duel_field.inc:272) | **Domain-distinct OK** |
| SPRITE_ROW_BITS18_15_CLEAR_MASK | 0xfff87fff | 0 hits | NEW OK |
| SPRITE_ROW_DISPATCH_TABLE | 0x080953dc | 0 hits | NEW OK |
| **SPRITE_LOW_HALF_MASK** | **0x0000ffff** | **6 direct hits** | **Domain-distinct OK** |

SPRITE_HIGH_HALF_MASK (0xffff0000): the existing EQUIP_CHAIN_SENTINEL=0xffff0000 is a linked-list
terminator for gEquipChainSlotRefs. SPRITE_HIGH_HALF_MASK is a bit-mask applied to sprite attr
words in pack_sprite_row_attr_words to clear the low 16 bits before ORing y-coordinate. The two
uses (chain list sentinel vs sprite attr packing) are domain-distinct. New constant is justified
per the domain-exception policy (feedback_c5_offset_value_collision_scope).

SPRITE_LOW_HALF_MASK (0x0000ffff): 6 existing constants share value 0xffff -- SLOT_CARD_EMPTY,
LP_ROW_TYPE8_ALL_SLOTS_MASK, EQUIP_ACTIVATION_CNT_CAP, UNINIT_GUARD_FFFF, OAM_ATTR0_HIDDEN,
EQUIP_SLOT_SCORE_CAP. All are domain-distinct from sprite attr low-half packing. New constant
is justified. Proposal's description acknowledging existing hits is accurate.

### REUSE claims verified

All REUSE entries verified by value-grep. Confirmed hits include:
gDuelCardCtxBase, PLAYER_BLOCK_STRIDE, gDuelFieldSlots, ACTIVATION_STATE_C_OFF,
ELIGIB_ACT_TYPE_OFF, ELIGIB_STATE_CTRL_OFF, ELIGIB_ACT_COUNT_OFF, gSpriteAttrBuf,
gEquipZoneRankState, gEquipChainEntryBase, gEffectEntryArray, gDuelPhaseFlags,
GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF, EQUIP_SLOT_SUBSTATE_OFF, EFFECT_ENTRY_COUNT_OFF,
LP_BAR_ANIM_STATE_OFF, SPRITE_ROW_ENTRY_DATA_OFF, CHAIN_NODE_CARD_ARR_OFF,
SPRITE_ROW_ANIM_CTL_OFF, P1LP_BLOCK2_OFF, P1LP_BLOCK2_OFF_1CE8 -- all CONFIRMED.

C5 PASS (domain-conflict notes documented, no false NEW claims).

---

## C13 残留核对

Independent python scan of Seg-2 [0x08094f20, 0x08095ba8):

```
DAT_  slots: 99
DWORD_ slots: 10
PTR_  slots: 13
Total: 122
```

PTR_ breakdown (13 total):
- PTR_gP1LifePoints_ x11: 0x8095024, 0x809507c, **0x809552c**, 0x8095774, 0x8095868, 0x80958a4, 0x8095a40, 0x8095af8, 0x8095b20, 0x8095b48, 0x8095b98
- PTR_PTR_ x1: 0x8095248 (in REF_SLOTS)
- PTR_DAT_ x1: 0x809524c (covered by REF user-label at 0x8095248)

Proposal coverage mapping:
- EQ_SLOTS: ~110 entries (DAT_ and DWORD_)
- REF_SLOTS: 0x8095248 (PTR_PTR_) -- user-label creates equip_confirm_case_jump_table at 0x809524c, which effectively renames PTR_DAT_0809524c
- RENAME_SLOTS: 13 entries (10 PTR_gP1LifePoints_ + 3 DWORD_gP1LifePoints + 7 DWORD_others -- wait, see below)

**CONFIRMED C13 GAP #1: PTR_gP1LifePoints_0809552c (0x0809552c)**
ROM[0x0809552c] = 0x0201c4e0 (gP1LifePoints). Used at LAB_0809551e inside
step_prng_anim_frame: `ldr r0, PTR_gP1LifePoints_0809552c`. This slot is NOT listed
in RENAME_SLOTS (proposal lists 13 entries but counts PTR_PTR_08095248 and PTR_DAT_0809524c
toward the "13 PTR_gP1LifePoints_" total, masking this omission). Needs:
RENAME_SLOTS: 0x0809552c PTR_gP1LifePoints_0809552c -> gp1lp_ptr_9552c.

**CONFIRMED C13 GAP #2: DAT_08095550 (0x08095550)**
ROM[0x08095550] = 0x08095554. This pool word (used at LAB_08095544 in step_prng_anim_frame
second switchD: `ldr r1, DAT_08095550; adds r0,r0,r1; ldr r0,[r0]; mov pc,r0`) holds
the base address of the second dispatch table `switchD_0809554c__switchdataD_08095554` (30
entries). NOT listed in any proposal table (EQ_SLOTS, REF_SLOTS, or RENAME_SLOTS).
Needs REF_SLOTS entry: 0x08095550 / gas_label=switchD_0809554c__switchdataD_08095554 /
slot_label=sprite_row_tbl2_95550. (The GAS label is already present in the asm file.)

C13 FAIL (2 missing slots out of 122 total).

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | §五 Seg-2: [0x08094f20, 0x08095ba8); proposal 精确匹配 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | PASS | Block1=R4 disasm; Block2=§5.1; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立重跑: Block2 raw=0/thumb+1=0; 前驱 step_prng_anim_frame 以 pop/pop/bx r1 结尾, 非 fall-through |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立核对 47 槽, 全部一致 |
| C5 R1 复用 | 新建前确无现有可复用 | PASS | SPRITE_HIGH_HALF_MASK 1 hit + SPRITE_LOW_HALF_MASK 6 hits; 均 domain-distinct, 新建合法 |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 槽名全部符合 ^[a-z][a-z0-9_]+$; 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | **FAIL** | DAT_08095550 (0x08095550) 持有第二 dispatch table 地址 0x08095554, 未列入 REF_SLOTS; 无 DATA-ref 计划 (见 Fix #2) |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | PASS | 6 个 stale FUN_ 全部在 PLATE 表中覆盖; FUN_08095a18=LAB_ 已注记; FUN_0804ce78=Seg-3 fn 正确排除 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | grep [^\x00-\x7F] 在 Seg-2 范围 (L1919..L3464) 返回 0 行 |
| C10 carve | 指针表条目 +1 (THUMB) 核对 | PASS | 10 个表条目均为偶数 (raw 地址); dispatch via mov pc,r0 (0x4687, 非 BX, 不切换模式); THUMB-mode RAW ptr dispatch 正确 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 15 个函数名经 ghidra-functions.csv 核对, 与体一致; 无矛盾 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | 10 个消费者证据条目均有 asm/12 file:line + conf:high; 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | **FAIL** | 独立清点 122 槽; proposal 覆盖 119; 2 槽缺失: PTR_gP1LifePoints_0809552c + DAT_08095550 |

---

## 状态: NEEDS_FIX(3 items)

---

## 修改清单 (NEEDS_FIX, 逐条可执行)

### Fix #1 — C13 — PTR_gP1LifePoints_0809552c 遗漏 RENAME_SLOTS

**位置**: RENAME_SLOTS 表缺少一项。

**问题**: 0x0809552c (PTR_gP1LifePoints_0809552c) = 0x0201c4e0 (gP1LifePoints)。
该槽位于 step_prng_anim_frame 内 LAB_0809551e 路径: `ldr r0, PTR_gP1LifePoints_0809552c`。
Proposal 声称 "PTR_gP1LifePoints_: 13 slots" 并列了 13 个 RENAME 条目, 但实际
PTR_gP1LifePoints_ 标签共 11 个, 而其中 PTR_PTR_08095248 / PTR_DAT_0809524c 被错误纳入
计数凑成 13, 导致 0x0809552c 漏计且漏列。

**修改**:
在 RENAME_SLOTS 表新增一行:
```
| 0x0809552c | PTR_gP1LifePoints_0809552c | gp1lp_ptr_9552c |
```
在 disasm 计划 / EQ 表对应位置补注: slot_label `gp1lp_ptr_9552c`, value = gP1LifePoints.

### Fix #2 — C7/C13 — DAT_08095550 遗漏 REF_SLOTS

**位置**: REF_SLOTS 表缺少第二 dispatch table 指针槽。

**问题**: 0x08095550 (DAT_08095550) = 0x08095554, 持有 `switchD_0809554c__switchdataD_08095554`
起始地址 (step_prng_anim_frame 第二 switchD 的 30-entry dispatch table)。
用于 LAB_08095544: `ldr r1, DAT_08095550; adds r0,r0,r1; ldr r0,[r0,#0]; mov pc,r0`。
该槽未列入 EQ_SLOTS / REF_SLOTS / RENAME_SLOTS 任何一张表。

**修改**:
在 REF_SLOTS 表新增一行:
```
| 0x08095550 | 0x08095554 | switchD_0809554c__switchdataD_08095554 | sprite_row_tbl2_95550 | step_prng_anim_frame second switchD dispatch table base; 30 entries, targets caseD groups; conf: high |
```
GAS label `switchD_0809554c__switchdataD_08095554` 已在 asm 文件中作为 Ghidra 导出标签存在,
直接引用即可。

### Fix #3 — 文档说明 — Block1 case 块数描述歧义 (非阻断, 建议同步修正)

**位置**: 数据块分类表 "Block1: 10 case blocks" 及 disasm 计划标题。

**问题**: Jump table 有 10 个条目, 但 entry[7] 和 entry[8] 共享同一入口 0x8095274, 实际
唯一 case 块入口点为 9 个。Proposal disasm 计划正确列出 9 个 DisassembleCommand, 执行
无误; 但标题 "10 case blocks" 与事实不符, 有误导性。

**建议**: 将相关描述改为 "10-entry jump table / 9 unique case-block entry points" 或
类似表述, 避免未来维护混淆。此项不阻断落地。

---

## Reviewer Verdict: F12-Seg-2 = NEEDS_FIX(3 items)
