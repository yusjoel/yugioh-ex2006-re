# Refine Review: F08-Seg-8a

Reviewer: independent (no Ghidra, no build, no proposal edits)
ROM: roms/2343.gba (SHA1 seed: 9689337d)
Proposal: doc/dev/refine/F08-Seg-8a.proposal.md
Seg-8a range: [0x0806ab0c, 0x0806b56c)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | Seg-8a = Seg-8 首段，与 §三 进度表 Seg-8 (未开始) 对应；无跳号/回头 |
| C2 Rule2 | PASS | 4 个 ROM_INCBIN 全有归宿：§5.1/DISASM/DISASM/DISASM |
| C3 Rule3 | PASS | Block 0x6adb6/0x3e: 独立 ref-scan raw=0 THUMB+1=0 确认 |
| C4 R1 值 | PASS | 22 EQ 槽 + 1 REF 槽全部逐字节核对，与 ROM 完全一致 |
| C5 R1 复用 | PASS | GIANT_GERM_CID=0x1339: grep constants/*.inc 0 命中 -> NEW 正确；21 reuse 值均在 ewram.inc 确认存在 |
| C6 R2 名 | NEEDS_FIX | EQ 槽标签 `gduelvardctxbase_0806b41c` 有打字错误："vard" != "card"，正确应为 `gduelcardctxbase_0806b41c` |
| C7 R3 接通 | PASS | DAT_0806ac24: gas_label=switchD_0806ac1e__switchdataD_0806ac28，数据表已在 asm 结构化为 .word 条目 |
| C8 R5 现名 | PASS | asm/08 Seg-8a 范围内无 FUN_[0-9a-f]{8} 残留 |
| C9 ASCII | PASS | proposal 中 PLATE 操作的所有引号内字符串均为纯 ASCII（proposal 文档本身的中文注释不计） |
| C10 carve | N/A | Seg-8a 无 carve 项 |
| C11 误名 | NEEDS_FIX | CID 核对正确（见下文详情）；但 FUNC_RENAME 收尾清单不完整：缺 CSV sync + 跨模块 plate ripple |
| C12 R6 | PASS | 所有关键槽均有 file:line + high 置信度，无零容忍词 |
| C13 残留 | PASS | Seg-8a 内 31 个自动名槽全部有归宿（28 EQ/REF/RENAME + 3 ROM_INCBIN 入口标签） |

---

## 独立 ref-scan 结果 (Phase 1)

自行运行 python `d.find(struct.pack('<I', addr))` 穷举 raw + THUMB|1：

| 块 | raw 命中 | THUMB+1 命中 | 独立判定 |
|----|---------|-------------|---------|
| 0x6adb6/0x3e | 0 | 0 | §5.1 CONFIRMED |
| 0x6ae18/0x25c | 1 @0x806ae14 | 0 | DISASM R4 CONFIRMED |
| 0x6b098/0x19c | 1 @0x806b094 | 0 | DISASM R4 CONFIRMED |
| 0x6b2a8/0x74 | 1 @0x806b2a4 | 1 @0x89416ca | DISASM R4 CONFIRMED |

Block 0x6b2a8 THUMB+1 @0x89416ca 核对：周边字节 `08 a2 8d 1d d2 20 48 53 a9 b2 06 08 6a 18 ...`，
地址前缀 0x89 属于 FS 压缩资产区，无指针表结构特征，为偶合值，不计真引用。判定正确。

### Block 0x6b2a8 关键裁定（proposal 描述有误但判定正确）

Proposal 在段测绘表中写"本块 IS 该 29 条跳表本体"，此描述不准确：

- 29 条跳转表实体位于 **[0x6b234..0x6b2a8)**（恰好是 0x74 字节），已在 asm/08 lines 15766-15794 结构化为 .word 条目。
- Block 0x6b2a8/0x74 = **[0x6b2a8..0x6b31c)**，读 ROM 字节确认为 THUMB 代码：

```
+000: a1 78 c8 07 c0 0f 21 88 ...   (0x78a1=ldrb r1,[r4,#2]; 0x07c8=lsls r0,r1,#31; ...)
```

所有 29 条跳转表条目均指向此块内部（python 验证全部 `in_block=True`）。

**结论**：block 0x6b2a8 是跳转表的 TARGET CODE stubs，不是 BODY 数据。判定 DISASM R4 **正确**。
描述错误仅影响 proposal 文档可读性，不影响执行正确性，不算独立 NEEDS_FIX 项。

---

## FUNC_RENAME 卡名核 (C11)

### FUNC_RENAME 1: dispatch_germ_momonga_trigger_display_by_state

独立验证 dispatch table fn-ptr-4 处 CID：

- fn+1=0x0806b31d @0x9e45800: CID @0x9e457fc = **0x1339** = Giant Germ (card-stats.s card_0735 slot=0x1339 pw=95178994) -- 确认
- fn+1=0x0806b31d @0x9e45818: CID @0x9e45814 = **0x133a** = Nimble Momonga (card_info.inc L501 NIMBLE_MOMONGA_CID=0x133a) -- 确认
- 函数名中 "neo_daedalus" 与函数体操作的 CID 矛盾，FUNC_RENAME 改名 **正确**。

### FUNC_RENAME 2: dispatch_spear_cretin_activate_if_chain_subtype

独立验证：

- fn+1=0x0806b53d @0x9e436d0: CID @0x9e436cc = **0x133b** = Spear Cretin (card_info.inc L795 SPEAR_CRETIN_CID=0x133b; card-stats.s card_0737 pw=58551308) -- 确认
- fn+1=0x0806b53d @0x9e45830: CID @0x9e4582c = **0x133b** -- 确认

两处 FUNC_RENAME 语义核对均正确，高置信度。

### FUNC_RENAME 收尾清单完整性 (C11 NEEDS_FIX)

Proposal 未提及两项必须操作：

1. **CSV sync 缺失**：doc/dev/naming-proposals.csv 第 2009 行 (0x0806b31c) 和第 2010 行 (0x0806b53c) 的旧函数名需同步更新。proposal 未提及。

2. **跨模块 plate ripple 缺失**：grep 全 asm/*.s 发现：
   - `asm/05_equip_eligibility_a.s:4` 的 plate 文本（submit_equip_lp_indicators_with_bar 的调用者列表）含旧名 `dispatch_neo_daedalus_effect_display_by_state`，需更新为新名。
   - proposal FUNC_RENAME 章节未提及此跨模块修改。

---

## C6 R2 名称错误详情 (NEEDS_FIX)

EQ_SLOTS 表中 DWORD_0806b41c 的槽新标签：

- 常量名: `gDuelCardCtxBase`
- Proposal 槽标签: `gduelvardctxbase_0806b41c`  ← 打字错误 (`vard` != `card`)
- 正确槽标签: `gduelcardctxbase_0806b41c`

---

## 机器码抽查 (C10 + 块验证)

| 块 | 首指令 addr | ROM bytes | 解码 |
|----|-----------|-----------|------|
| 0x6ae18 | 0x806ae18 | `0a 49` | `ldr r1,[pc,#0x28]` (THUMB) -- 代码确认 |
| 0x6b098 | 0x806b098 | `30 1c` | `adds r0,r6,#0` (THUMB) -- 代码确认 |
| 0x6b2a8 | 0x806b2a8 | `a1 78` | `ldrb r1,[r4,#2]` (THUMB) -- 代码确认 |

9 条目跳转表 @0x6adf4..0x6ae14：所有条目验证为 [0x806ae18..0x806b074) 范围内，正确。

---

## 修改清单 (NEEDS_FIX, 共 2 项)

### #1 -- C6 -- 槽标签打字错误

位置: proposal EQ_SLOTS 表 DWORD_0806b41c 行

```
错: gduelvardctxbase_0806b41c
正: gduelcardctxbase_0806b41c
```

Ghidra 脚本中此标签名需同步修正，其他 5 个 gDuelPhaseFlags 槽标签用了 `gduelphaseflags_` 前缀，不受此错影响。

### #2 -- C11 -- FUNC_RENAME 收尾清单补充

Fixer 落地时必须执行（proposal 未提及）：

a. **CSV sync**: 更新 `doc/dev/naming-proposals.csv` 第 2009 行和第 2010 行，将旧名替换为新名：
   - 0x0806b31c: `dispatch_neo_daedalus_effect_display_by_state` -> `dispatch_germ_momonga_trigger_display_by_state`
   - 0x0806b53c: `dispatch_neo_daedalus_placement_check_if_chain_subtype` -> `dispatch_spear_cretin_activate_if_chain_subtype`

b. **跨模块 plate 更新**: `asm/05_equip_eligibility_a.s` line 4 的 plate 文本含旧名 `dispatch_neo_daedalus_effect_display_by_state`，Ghidra 落地后需同步更新该 plate 为新名（Ghidra rename 会更新 bl 指令引用但不更新 plate 散文）。

---

## 其他观察 (不计入 NEEDS_FIX)

- **Block 0x6b2a8 "IS 跳表本体" 描述错误**: proposal 说法不准确（body 是 [0x6b234..0x6b2a8)，已在 asm 结构化），但判定 DISASM R4 正确，不影响执行。
- **switchD_0806ac1e inline 确认**: 位于函数 dispatch_equip_effect_slot_display_by_state_and_card [0x6abec..0x6adb6) 内部 (0x806ac1e < 0x806adb6)，inline 正确。
- **DAT_0806ac20 (0x0201b290) 槽**: 位于 switchD 跳转指令 (0x806ac1e, `.hword 0x4687`) 之后的字面量池内，proposal 将其作为 EQ 槽处理正确；switchD data ptr 是 DAT_0806ac24 (另一槽)，两槽分工清晰。

---

## 状态: NEEDS_FIX(2 items)

**#1 -- C6** -- EQ 槽标签打字错误: `gduelvardctxbase_0806b41c` -> `gduelcardctxbase_0806b41c`

**#2 -- C11** -- FUNC_RENAME 收尾清单缺 CSV sync (naming-proposals.csv 两行) + 跨模块 plate 更新 (asm/05_equip_eligibility_a.s:4)
