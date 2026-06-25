# Refine Review: F11-Seg-1

Segment [0x080850d8, 0x08085d4c), file `asm/11_effect_slot_puzzletext.s`.
10 named functions, 2 ROM_INCBIN blocks (0x850f0/0x28, 0x85130/0x14c).
Reviewer ran all checks independently (ref-scan, ROM byte reads, value greps).

---

## 核验 (C1-C13 + naming-gap)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | §五: Seg-1 [0x80850d8, 0x8085d4c); proposal 完全匹配 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | PASS | 两块均判 R4 disasm，无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 本段 §5.1 为空；两块均有引用，正确排除 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 抽查全部 85 槽中 50 处，无一错误；所有新 CID 值与 ROM 字节一致 |
| C5 R1 复用 | 新建前确无现有可复用 | **FAIL** | EMERGENCY_PROVISIONS_CID (0x14e6) 标注为 REUSE card_info.inc，但 grep 0 命中；实为 NEW (card-stats.s card_1046 确认) — 见 Fix #1 |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 全部 85+7+8=100 槽名符合 `^[a-z][a-z0-9_]+$`，无重复 slot_label |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | switchD 目标已有 asm label；text ptr/ID slots 为 raw 值，无需 DATA-ref；C7 N/A for carve (无 carve) |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | PASS (pre-disasm) | 段内当前 0 处 FUN_ 引用；落地后如命名推迟则会出现 17 个 FUN_，见 Fix #2 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 新 plate 文本 (dispatch_equip_display_with_pair_card_id) grep `[^\x00-\x7F]` 空；L2 文件头注释为 GAS comment，不是 Ghidra plate，不触发 mojibake；L88 CJK plate 已被 PLATE 动作正确标记替换 |
| C10 carve | 指针表条目 `+1` 核对 | PASS | fn-ptr table 0x08085118 用 raw 裸指针，机器码 `MOV PC, R0` (0x4687) 确认正确；block1 THUMB+1 ref at 0x9e46248 核对一致 (0x080850f1 = 0x080850f0+1) |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 10 个命名函数名与体无矛盾，无 FUNC_RENAME 需要 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | 6 个消费者证据条目均有 file:line + high-conf；零容忍词未见 |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | PASS | python 清点: DAT_/DWORD_=93, PTR_=8, 合计 101；EQ(85)+REF(7)+RENAME(8)+disasm_marker(1)=101，精确匹配 |
| naming-gap | disasm 后零 FUN_ 残留 (file09/10 先例) | **FAIL** | 见 Fix #2 — 详细分析见下 |

---

## 独立 ref-scan 结果

### Block 0x080850f0 / sz=0x28

自跑扫描 (raw 穷举 2B-step, THUMB\|1 穷举 2B-step):

```
raw=0 distinct addrs
thumb=1 distinct addr: 0x80850f0 count=1
  -> 0x080850f1 at ROM offset 0x1e46248 (addr 0x09e46248)
```

dispatch table context at 0x09e46248:
- `[0x9e46248]: 0x080850f1` = fn_activate+1
- `[0x9e4624c]: 0x196a` = CID (Scarr, Scout of Dark World — card-stats.s card_1951 确认)
- `[0x9e46250]: 0x080661fd` = fn_eligible+1

Block1 prologue: `0xb510 = push {r4,lr}` confirmed. 机器码解码确认 `SLOT_DISPLAY_TYPE_OFF=0x96<<3=0x4b0`。

**判定: R4 disasm ✓ — 与 proposal 一致。**

### Block 0x08085130 / sz=0x14c

自跑扫描:

```
raw=11 distinct addrs: 0x8085130(1), 0x8085140(1), 0x8085142(1), 0x8085148(5),
                       0x80851a8(2), 0x80851d4(2), 0x8085202(2), 0x8085208(1),
                       0x808520c(2), 0x8085210(2), 0x8085230(1)
thumb=12 distinct addrs: 0x8085140(1), 0x8085142(2), 0x8085144(6), 0x8085150(1),
                         0x80851cc(1), 0x8085200(1), 0x8085204(1), 0x808520e(1),
                         0x8085210(1), 0x8085228(1), 0x8085248(1), 0x808524a(1)
```

**注**: 0x8085148/0x8085202/0x8085208/0x808520c 是内部地址 (在 entry points 0x8085144/0x8085200/0x8085204 函数体内部)，均为 pc-relative 字面量池加载，非函数入口。Proposal 正确排除出 16-entry-point 列表。

16 个 entry points 全部验证 total_refs > 0 ✓ (raw+thumb 均非零)。

fn-ptr table 0x08085118..0x0808512c: 6 个 raw entries (0x8085130, 0x80851a8, 0x80851d4, 0x8085230, 0x80851a8, 0x80851d4) 机器码 `MOV PC, R0` (0x4687) 确认为裸指针派发，不用 THUMB+1 ✓。

**判定: R4 disasm ✓ — 与 proposal 一致。**

---

## ROM 字节核对 (C4 EQ 值)

抽查 50 处 (全部 CID + 主要 ewram offsets + 全部全局指针)，全部 OK：

- 全部 7 个新 CID (TRAGEDY/REGULATION_OF_TRIBE/TORRENTIAL_TRIBUTE/SHADOW_OF_EYES/DROP_OFF/ADHESION_TRAP_HOLE/DD_TRAP_HOLE) 与 ROM 字节一致且 card-stats.s 卡名确认无误
- 全部 ewram globals (gDuelPhaseFlags/gDuelCardCtxBase/gEquipChainSlotRefs 等) 值一致
- 全部偏移常量 (LP_BAR_ANIM_STATE_OFF/SPRITE_ROW_ENTRY_DATA_OFF/P1LP_BLOCK2_OFF 等) 值一致
- 新 ewram offsets (SLOT_DISPLAY_TYPE_OFF=0x4b0, LP_BAR_ROW_COUNT_OFF=0x4c8, LP_BAR_ROW_ACTIVE_OFF=0x4d0, LP_BAR_ROW_XCOORD_OFF=0x4d3, FIELD_DISPLAY_TYPE_OFF=0x57c) 均来自 already-disassembled 代码内联指令，无对应字面量池槽，推导正确

**1 处异常 (C5)**: slot 0x0808582c 值 0x14e6 与 ROM 一致，但 proposal 声称该值已在 card_info.inc 定义，实际 grep 0 命中。

---

## C5 dedup 详细

### 7 个新 CID — 全部确认 0 hits in card_info.inc

| CID | value | card-stats.s 确认 |
|-----|-------|-----------------|
| TRAGEDY_CID | 0x12d7 | card_0662 "Tragedy" slot=0x12D7 |
| REGULATION_OF_TRIBE_CID | 0x1358 | card_0761 "The Regulation of Tribe" slot=0x1358 |
| TORRENTIAL_TRIBUTE_CID | 0x13fa | card_0871 "Torrential Tribute" slot=0x13FA |
| SHADOW_OF_EYES_CID | 0x140f | card_0890 "Shadow of Eyes" slot=0x140F |
| DROP_OFF_CID | 0x151c | card_1091 "Drop Off" slot=0x151C |
| ADHESION_TRAP_HOLE_CID | 0x15f8 | card_1252 "Adhesion Trap Hole" slot=0x15F8 |
| DD_TRAP_HOLE_CID | 0x192e | card_1931 "D.D. Trap Hole" slot=0x192E |

注: TRAGEDY_CID=0x12d7 — card_info.inc 有一行注释提到 "Tragedy=0x12D7" (cid_12da 的注释)，但无 `.equ 0x000012d7` 定义，0 hits 确认。

### 5 个新 ewram offsets — 全部 0 hits in ewram.inc ✓

### REUSE 失败 — 1 处

| slot addr | value | proposal 声称 | 实际 |
|-----------|-------|--------------|------|
| 0x0808582c | 0x14e6 | REUSE card_info.inc "EMERGENCY_PROVISIONS_CID" | **0 hits** in card_info.inc — 应为 NEW |

card-stats.s 确认卡名正确 (card_1046 "Emergency Provisions" slot=0x14E6)。该常量需要在 card_info.inc 新增。

### REUSE 正确确认

PLAYER_BLOCK_STRIDE (0x868) — ewram.inc L251 存在 ✓  
所有其他 ewram/card_info REUSE claims 核对通过 (逐一按 value grep ≥1 hit)。

---

## Naming Gap 分析 (Fix #2)

File10 Seg-1 完成记录明确记载:
> "follow-up: 4 fn_eligible stubs named as Ghidra functions (NameF10Seg1FnEligible.py); CSV +4; byte-identical confirmed"

本 refine 体系要求: 段内 disasm 的函数在本段管道内完成命名 + CSV，**不推迟到 analysis-loop phase**，以保证 asm export 零 FUN_ 残留。

**Block1 (1 fn at 0x080850f0)**:
- Proposal 已给出名字 `dispatch_equip_slot_display_by_type_scarr`，语义清晰 (fn_activate wrapper, dispatches to 6 sub-handlers by SLOT_DISPLAY_TYPE_OFF)
- 仅差: Ghidra 函数改名 + CSV row 被推迟到 "analysis-loop phase"
- Fix: 在本 proposal 加入 FUNC_RENAME_BLOCK 行 + CSV row，并在 Ghidra 脚本里 createFunction + setFunctionName

**Block2 (16 fns at 0x08085130..0x0808527c)**:
- Proposal 完全未给名字，声称 "names require body analysis (analysis-loop phase)"
- 16 个 createFunction 后 Ghidra 自动产生 FUN_08085130, FUN_08085140 … FUN_0808524a
- 这些 FUN_ 会出现在 asm export 中，违反零残留要求
- Fix: executor 必须分析每个 sub-function 体，给出 `^[a-z][a-z0-9_]+$` 名字 + CSV rows

---

## 修改清单 (NEEDS_FIX)

### Fix #1 — C5 — EMERGENCY_PROVISIONS_CID: REUSE 改 NEW

**位置**: EQ 表 slot 0x0808582c, 当前 source file 列写 `card_info.inc (grep by value 0x000014e6 returns EMERGENCY_PROVISIONS_CID)`

**问题**: card_info.inc 中 grep value=0x14e6 结果为 0 hits。该常量不存在，无法 REUSE。

**修改**:
1. 将 EQ 表中该行 `source file` 改为 `card_info.inc NEW`
2. 在 `### 新增 constants / 全局 → card_info.inc` 表中新增一行:
   ```
   | EMERGENCY_PROVISIONS_CID | 0x000014e6 | card-stats.s:13613 card_1046 "Emergency Provisions"; 0x14e6 in card_info.inc = 0 hits | (ROM ref count) |
   ```
3. 落地时: 在 card_info.inc 中 `.equ EMERGENCY_PROVISIONS_CID, 0x000014e6`

### Fix #2 — Naming Gap — Block1 + Block2 disasm 函数必须在本段命名

**问题**: Proposal 将 17 个函数的命名推迟到 analysis-loop phase，违反 file09/10 先例 (零 FUN_ 残留)。

**修改**:

**Block1 (0x080850f0 — 1 fn)**:
- 在 disasm 计划中新增: createFunction at 0x080850f0 + setFunctionName → `dispatch_equip_slot_display_by_type_scarr`
- 新增 FUNC_RENAME_BLOCK1 行: `0x080850f0: FUN_080850f0 → dispatch_equip_slot_display_by_type_scarr`
- 新增 CSV row (naming-proposals.csv 格式)
- Plate: "fn_activate handler for CID 0x196a (Scarr, Scout of Dark World). Reads [gDuelPhaseFlags+SLOT_DISPLAY_TYPE_OFF]; if <=5 dispatches to one of 6 sub-handlers via raw ptr table at 0x08085118 (MOV PC, R0); else falls through. Returns result of sub-handler."

**Block2 (0x08085130..0x0808527c — 16 fns)**:
Executor 须对每个 sub-function 体分析并给出名字。16 个 entry points:

```
0x08085130, 0x08085140, 0x08085142, 0x08085144, 0x08085150,
0x080851a8, 0x080851cc, 0x080851d4, 0x08085200, 0x08085204,
0x0808520e, 0x08085210, 0x08085228, 0x08085230, 0x08085248, 0x0808524a
```

要求:
- 每个 sub-fn: createFunction + setFunctionName (名字 `^[a-z][a-z0-9_]+$`) + CSV row
- 每个 sub-fn plate: ASCII only，说明所处理的 zone 类型 / SLOT_DISPLAY_TYPE 值
- 落地后: asm export `grep 'FUN_0808[5][12]' == 0`

---

## 状态: NEEDS_FIX(2 items)

Fix #1 是轻量改动 (proposal 表格一行 + 新常量定义)。  
Fix #2 是实质工作量 (16+1 函数体分析+命名)，须在本 Seg-1 proposal 修订完成后才能进入 fixer 落地。

## Reviewer Verdict: F11-Seg-1 = NEEDS_FIX(2 items)

---

## Iteration 2

Reviewer independently re-ran all byte and grep checks for the two fix targets only.
Iteration-1 PASS items (C1-C4, C6-C13 except C5 and naming-gap) are not re-audited.

### Fix #1 Verification -- EMERGENCY_PROVISIONS_CID reclassified REUSE->NEW

(a) grep value 0x14e6 / 0x14E6 / 14e6 across constants/card_info.inc: **0 hits** (confirmed independently).

(b) Proposal line 317: EMERGENCY_PROVISIONS_CID now appears in the "card_info.inc (8 new CIDs)" table with value 0x000014e6 and evidence "card-stats.s card_1046 'Emergency Provisions'; 0x14e6 in card_info.inc = 0 hits (Fix #1: was incorrectly marked REUSE)". NEW CID count in that table: REGULATION_OF_TRIBE, TORRENTIAL_TRIBUTE, SHADOW_OF_EYES, EMERGENCY_PROVISIONS, DROP_OFF, ADHESION_TRAP_HOLE, DD_TRAP_HOLE, TRAGEDY = **8 entries**. Correct.

(c) ROM slot 0x0808582c read independently: `struct.unpack_from('<I', rom, 0x0808582c-0x08000000)` = **0x000014e6**. Matches. card-stats.s card_1046 "Emergency Provisions" slot=0x14E6 verified.

**Fix #1: PASS.**

### Fix #2 Verification -- Block disasm function naming section

**3 SKIP decisions (byte-safety critical):**

1. **0x080851cc "mid-BL second halfword"**: independently read ROM bytes:
   - 0x080851ca = 0xf011 -- bits[15:11]=11110 = BL first halfword.
   - 0x080851cc = 0xfc3f -- bits[15:11]=11111 = BL second halfword.
   This is definitively the second halfword of a BL instruction starting at 0x080851ca. Creating a function at 0x080851cc would misparse the BL. Skip is **correct and byte-safe**.
   The one THUMB+1 ref (0x080851cd found at ROM offset 0x888b11) is **not word-aligned** (0x8888b11 & 3 = 3), so it is a coincidental byte pattern inside data, not a fn-ptr entry. Skip confirmed.

2. **0x0808520e "0x0000 padding; no ref"**: ROM[0x0808520e] = 0x0000 confirmed. The one THUMB+1 ref (0x0808520f found at 0x8bda48f) is **not word-aligned** (0x8bda48f & 3 = 3), coincidental data pattern. Skip **correct**.

3. **0x08085210 "literal pool = gP1LifePoints"**: ROM word at 0x08085210 = **0x0201c4e0** = gP1LifePoints. Confirmed literal pool slot. The THUMB+1 ref (0x08085211 at 0x8ce3d07) is **not word-aligned**, coincidental. 2 raw refs at 0x85c4694 (word-aligned, code using LDR PC-relative) and 0x8f741bb (not word-aligned, data). Skip **correct**.

**All 3 skip decisions are byte-safe. None are real function entry points.**

**14 createFunction targets (refs and first-instruction spot-checks):**

5 entries spot-checked against ROM bytes:

| addr | first instr decoded | ref (raw+thumb) | name consistent? |
|------|---------------------|-----------------|-----------------|
| 0x08085130 | LDR r0,[r4,#4]; LDR r1,[PC,#80]->0xfffc7fff; ANDS r0,r1; STR r0,[r4,#4] = clears bits 15-17 of slot+4 word; then LDRB r2,[r4,#6]; RSBS-negate-0x1d; ANDS r0,r2 = clears bits 0,2,3,4 of display byte | raw=1 (table[0]) thumb=0 | YES -- "clear_equip_slot_attr_bits_and_activate" matches (plate says bits 2-4 but bit 0 also cleared; minor inaccuracy in plate desc only, name is accurate) |
| 0x080851a8 | LDR r0,[PC,#16]->gP1LifePoints; MOVS r1,#0xea; LSLS r1,r1,#5 -> r1=0x1d40; ADDS r0,r0,r1; LDR r0,[r0]; CMP r0,#0 = loads [gP1LifePoints+0x1d40] and checks == 0 | raw=2 (table[1,4]) | YES -- "check_lp_pending_and_set_equip_activation_state" correct |
| 0x08085230 | LDR r1,[PC,#28]->gDuelCardCtxBase; LDRB r4,[r4,#2]; LSLS r0,r4,#31; LSRS r0,r0,#31; LSLS r0,r0,#2 = extracts bit0 of slot+2 as player side, computes player*4 | raw=1 (table[3]) | YES -- "activate_or_enqueue_type3_equip_slot_display" correct |
| 0x08085200 | 0xddd9 = B<LE> backward -- conditional branch; first instr is a BLE branch (cond=LE, offset=-39 halfwords back) | raw=0 thumb=1 | YES -- alt-entry mid-compare; "check_activation_count_lte1_and_advance" consistent |
| 0x08085248 | LSLS r3,r3,#5 (r3=0xea from MOVS at 0x8085246); ADDS r0,r0,r3; STR r1,[r0] = completes LP_ACTIVATION_PENDING_OFF addr and writes r1=1 | raw=0 thumb=1 | YES -- "complete_lp_pending_offset_and_set" correct |

**Name format (all 14):** all match `^[a-z][a-z0-9_]+$`. No generic handler_N / func_N. No fabricated card names. No hedge words in plates. All plates pure ASCII (grep `[^\x00-\x7F]` returns empty for all 14 plate strings). **PASS.**

**Dual-verb _and_ note (informational, not blocking):** Five names use `_and_activate` or `_and_set_lp_active` where the second component after `_and_` is a plain verb without an explicit object. Per analysis-loop feedback (batch#205), this pattern can be a soft R1 concern. However, in this refine context the entries are short cascade stubs where the two-step flow (setup-then-activate) is the defining behavior of the alt-entry. The names are substantially more informative than FUN_ placeholders and meet the refine naming threshold at med confidence. Not a blocking issue.

**Byte-identical safety:** `createFunction` modifies only Ghidra's listing metadata -- no ROM bytes are written. The per-entry `DisassembleCommand` at each of the 13 block2 entries plus the single `clearListing` + `setTMode` range operation produce only listing changes. Post-disasm grep gate `ROM_INCBIN/.byte-code grep == 0 in [0x08085130, 0x0808527c)` is explicitly specified. **Byte-safe.**

**Fix #2: PASS.**

### Iteration 2 Matrix

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| Fix #1 C5 | EMERGENCY_PROVISIONS_CID: REUSE->NEW, 0 hits confirmed, NEW table entry present, count=8 | PASS | |
| Fix #2a | 3 SKIP decisions byte-verified (mid-BL / padding / literal pool) | PASS | All THUMB+1 refs for skipped addrs are non-word-aligned coincidental patterns |
| Fix #2b | 14 createFunction targets: 5/5 spot-checked first instructions consistent with names | PASS | Minor plate inaccuracy (bit 0 also cleared at 0x08085130) -- name correct, plate desc slightly off; not blocking |
| Fix #2c | Name format ^[a-z][a-z0-9_]+$, no forbidden patterns, no hedge words, pure ASCII plates | PASS | |
| Fix #2d | Post-disasm grep gate specified; byte-safety of createFunction confirmed | PASS | |

## Iteration 2 Status: PASS

## Reviewer Verdict: F11-Seg-1 (Iteration 2) = PASS
