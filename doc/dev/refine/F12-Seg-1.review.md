# Refine Review: F12-Seg-1

Segment [0x080941c4, 0x08094f20), file `asm/12_equip_activation_scan.s`.
31 named functions, 3 ROM_INCBIN blocks (0x9437c/0x1c, 0x943e8/0x12, 0x94c3e/0x22).
Reviewer ran all checks independently (ref-scan, ROM byte reads, value greps, C13 slot count).

---

## 独立 ref-scan 结果

### Block1: 0x0809437c / sz=0x1c

Independent scan (raw + THUMB+1, all 2-byte-aligned addresses):

```
raw hits:  {} (none)
thumb+1:   {} (none)
raw total=0  thumb total=0
```

Fall-through check: preceding function `get_activation_zone_card_type_field` ends at 0x0809437a
with bytes `08 47` = `bx r1` (unconditional branch/return). NOT fall-through.
Block1 first byte: `0x4905` = `ldr r1,[pc,#20]` (valid THUMB opcode).
Block1 last instruction before pool: `0x4770` = `bx lr` (return).
Pool word at 0x08094394: `0x0201e4f0` = gEquipEffectZoneBase confirmed.

**Judgment: 0 refs, not fall-through -> §5.1 CONFIRMED. Proposal R4 disasm + §5.1 classification is correct.**

### Block2: 0x080943e8 / sz=0x12

Independent scan:

```
raw hits:  {0x80943e8:1, 0x80943ec:1, 0x80943f0:1, 0x80943f4:1, 0x80943f8:1}
thumb+1:   {} (none)
raw total=5  thumb total=0
```

All 5 raw refs come from the 5-entry jump table at 0x080943d0 inside `dispatch_effect_ctx_slot_by_zone_type`.
Dispatch instruction at 0x080943c6: `0x4687` = `mov pc, r0` (raw pointer, not THUMB+1). Correct.

Block2 decoded (all 5 case blocks verified):
```
0x080943e8: movs r6,#0x02; b 0x080943fa   (verified)
0x080943ec: movs r6,#0x04; b 0x080943fa   (verified)
0x080943f0: movs r6,#0x08; b 0x080943fa   (verified)
0x080943f4: movs r6,#0x10; b 0x080943fa   (verified)
0x080943f8: movs r6,#0x20                  (fall-through to 0x080943fa) (verified)
```

NOTE: The proposal's semantic case description (zone_type mapping) has an ordering error.
The actual jump table at 0x080943d0 is: entry[0]=0x80943e8(#2), entry[1]=0x80943f4(#10),
entry[2]=0x80943ec(#4), entry[3]=0x80943f0(#8), entry[4]=0x80943f8(#20).
So zone_type=0x0c (index 1) dispatches to 0x80943f4 (movs r6,#0x10), NOT to 0x80943ec.
The proposal has cases 1..3 in wrong order. However, the DISASM PLAN (listing all 5
DisassembleCommand calls at the correct addresses) is procedurally correct.

**Judgment: 5 raw refs, all from jump table -> R4 disasm CONFIRMED. Procedure correct.**

### Block3: 0x08094c3e / sz=0x22

Independent scan:

```
raw hits:  {} (none)
thumb+1:   {} (none)
raw total=0  thumb total=0
```

Fall-through check: preceding function `poll_sprite_seq_until_done` ends at 0x08094c3c
with bytes `00 47` = `bx r0` (unconditional return). NOT fall-through.
Block3 first 2 bytes (0x08094c3e): `00 00` = .zero 2 align pad. Entry at 0x08094c40: `0x4904` = `ldr r1,[pc,#16]` (valid THUMB). Pool at 0x08094c54: `0x0201c4e0` = gP1LifePoints (confirmed; note: p5-refine doc §五 preview table mistakenly shows `0201e4d4` -- ROM bytes confirm `0201c4e0`).

**Judgment: 0 refs, not fall-through -> §5.1 CONFIRMED. Proposal R4 disasm + §5.1 classification is correct.**

---

## ROM 字节核对 (C4 EQ 值)

All 38 sampled slots verified correct:

| slot addr | proposed value | ROM actual | result |
|-----------|---------------|------------|--------|
| 0x08094220 | 0x0201e4f0 | 0x0201e4f0 | OK |
| 0x08094224 | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x0809426c | 0x0000161c | 0x0000161c | OK |
| 0x0809453c | 0xffffefff | 0xffffefff | OK |
| 0x0809465c | 0x000343fd | 0x000343fd | OK |
| 0x08094660 | 0x00269ec3 | 0x00269ec3 | OK |
| 0x0809474c | 0x0000800b | 0x0000800b | OK |
| 0x0809479c | 0x00008023 | 0x00008023 | OK |
| 0x08094740 | 0x0000ffff | 0x0000ffff | OK |
| 0x08094a5c | 0x00001d1c | 0x00001d1c | OK |
| 0x08094cbc | 0x09e5aac0 | 0x09e5aac0 | OK |
| 0x08094cc4 | 0x00001d18 | 0x00001d18 | OK |
| 0x08094e0c | 0x09e5aadc | 0x09e5aadc | OK |
| 0x08094e14 | 0x00001d14 | 0x00001d14 | OK |
| 0x08094b78 | 0x00008006 | 0x00008006 | OK |
| 0x08094b7c | 0x00008007 | 0x00008007 | OK |
| 0x08094b80 | 0x00008008 | 0x00008008 | OK |
| 0x08094b84 | 0x00008005 | 0x00008005 | OK |
| 0x08094848 | 0x00001468 | 0x00001468 | OK |
| 0x0809484c | 0x00001497 | 0x00001497 | OK |
| 0x080947e4 | 0x00000fb7 | 0x00000fb7 | OK |
| 0x080947e8 | 0x00000fb8 | 0x00000fb8 | OK |
| 0x080947ec | 0x00000fb9 | 0x00000fb9 | OK |
| 0x080947f0 | 0x00000fba | 0x00000fba | OK |
| 0x080947f4 | 0x00000fbb | 0x00000fbb | OK |
| 0x080948f0 | 0x0000151e | 0x0000151e | OK |
| 0x0809490c | 0x0000169c | 0x0000169c | OK |
| 0x080944e4 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x080944e8 | 0x00000868 | 0x00000868 | OK |
| 0x08094cc0 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08094bd0 | 0x0201bcc0 | 0x0201bcc0 | OK |
| 0x08094bd4 | 0x00000808 | 0x00000808 | OK |
| 0x0809473c | 0x00001cf0 | 0x00001cf0 | OK |
| 0x08094744 | 0x00001cec | 0x00001cec | OK |
| 0x08094943 + 9 | 0x00001cec | 0x00001cec | OK |
| 0x080943cc | 0x080943d0 | 0x080943d0 | OK |
| 0x08094d80 | 0x0201c4e0 | 0x0201c4e0 | OK |
| 0x08094c54 | 0x0201c4e0 | 0x0201c4e0 | OK (Block3 pool) |

All values confirmed. C4 PASS.

---

## C5 dedup 详细

### NEW constants grep-by-VALUE results (independent grep of constants/*.inc)

| const_name | value | grep result | ruling |
|-----------|-------|------------|--------|
| ZONE_SLOT_ATTR_BIT12_CLEAR_MASK | 0xffffefff | **0 hits** | NEW OK |
| LCG_MUL_343FD | 0x000343fd | **0 hits** | NEW OK |
| LCG_INC_269EC3 | 0x00269ec3 | **0 hits** | NEW OK |
| EQUIP_PHASE_FN_TABLE_ROM | 0x09e5aac0 | **0 hits** | NEW OK |
| DUEL_TURN_FN_TABLE_ROM | 0x09e5aadc | **0 hits** | NEW OK |
| SPRITE_ATTR_DUEL_PHASE_P2 | 0x0000800b | **0 hits** | NEW OK |
| SPRITE_ATTR_DUEL_PHASE_P2_B | 0x00008023 | **0 hits** | NEW OK |
| SPRITE_ATTR_SPELL_8006 | 0x00008006 | **0 hits** | NEW OK |
| SPRITE_ATTR_TRAP_8007 | 0x00008007 | **0 hits** | NEW OK |
| **SPRITE_ATTR_MONSTER_8008** | **0x00008008** | **1 HIT: card_info.inc:60 CARD_DESC_RENDER_PARAM** | **C5 FAIL** |
| SPRITE_ATTR_ALT_8005 | 0x00008005 | **0 hits** | NEW OK |
| CARD_PLAY_PHASE_CTR_OFF | 0x00001d1c | 0 hits (rom_data.inc partial match not exact) | NEW OK |
| DUEL_TURN_STATE_OFF | 0x00001d14 | 0 hits (rom_data.inc partial match not exact) | NEW OK |

For UNINIT_GUARD_FFFF (0x0000ffff): grep returns 5 hits (OAM_ATTR0_HIDDEN/SLOT_CARD_EMPTY/EQUIP_SLOT_SCORE_CAP/LP_ROW_TYPE8_ALL_SLOTS_MASK/EQUIP_ACTIVATION_CNT_CAP). Proposal text says "not as named constant" which is inaccurate. However, all existing 0xffff constants are in different domains (OAM attr / card slot sentinel / score cap / row mask / counter cap). The LP timer initialization guard domain is distinct. Decision: NEW is justified per domain-exception policy, but proposal text must be corrected to say "5 hits, all different domains" rather than "not as named constant".

### REUSE claims verified

| const_name | value | grep result |
|-----------|-------|------------|
| gEquipEffectZoneBase | 0x0201e4f0 | ewram.inc:550 HIT |
| gDuelCardCtxBase | 0x0201e2a0 | ewram.inc:218 HIT |
| gEquipLpZoneEntryBase | 0x0201e500 | ewram.inc:476 HIT |
| PLAYER_BLOCK_STRIDE | 0x00000868 | ewram.inc:251 HIT |
| TRIBE_INFECTING_VIRUS_CID | 0x0000161c | card_info.inc:912 HIT |
| P1LP_BACKUP_DST_OFF | 0x00001cf0 | ewram.inc:245 HIT |
| P1LP_TIMER_OFF | 0x00001cec | ewram.inc:244 HIT |
| RIGHT_LEG_FORBIDDEN_ONE_CID | 0x00000fb7 | card_info.inc:1221 HIT |
| LEFT_LEG_FORBIDDEN_ONE_CID | 0x00000fb8 | card_info.inc:1222 HIT |
| RIGHT_ARM_FORBIDDEN_ONE_CID | 0x00000fb9 | card_info.inc:1223 HIT |
| LEFT_ARM_FORBIDDEN_ONE_CID | 0x00000fba | card_info.inc:1224 HIT |
| EXODIA_THE_FORBIDDEN_ONE_CID | 0x00000fbb | card_info.inc:1225 HIT |
| DESTINY_BOARD_CID | 0x00001468 | card_info.inc:579 HIT |
| SPIRIT_MESSAGE_I_CID | 0x00001497 | card_info.inc:803 HIT (reviewer verified) |
| SPIRIT_MESSAGE_N_CID | 0x00001498 | card_info.inc:804 HIT (reviewer verified) |
| SPIRIT_MESSAGE_A_CID | 0x00001499 | card_info.inc:805 HIT (reviewer verified) |
| SPIRIT_MESSAGE_L_CID | 0x0000149a | card_info.inc:570 HIT (reviewer verified) |
| LAST_TURN_CID | 0x0000151e | card_info.inc:1447 HIT |
| FINAL_COUNTDOWN_CID | 0x0000169c | card_info.inc:747 HIT |
| gP1LifePoints | 0x0201c4e0 | ewram.inc HIT |
| DISP_SET_VARIANT_OFF | 0x00001cfc | duel_field.inc:253 HIT |
| EQUIP_MAIN_PHASE_OFF | 0x00001d18 | duel_field.inc:255 HIT |
| DISPLAY_SEQ_ACTIVE_PLAYER_OFF | 0x00001d10 | duel_field.inc:218 HIT |
| SET_DISPLAY_STATE_SLOT_OFF | 0x00000894 | duel_field.inc:254 HIT |
| DISPLAY_SEQ_SLOT_IDX_OFF | 0x00000808 | duel_field.inc:216 HIT |
| gDuelDisplaySeqState | 0x0201bcc0 | ewram.inc:377 HIT |
| P1LP_BLOCK2_OFF | 0x00001d08 | ewram.inc:243 HIT |
| P1LP_BLOCK2_OFF_1CE8 | 0x00001ce8 | ewram.inc:276 HIT |
| LP_DISCARD_ZONE_OFF | 0x000010dc | ewram.inc:390 HIT |
| gSpriteAttrBuf | 0x0201b870 | ewram.inc:378 HIT |
| gPuzzleCardAnimBuf | 0x0201b1b0 | ewram.inc:577 HIT |

All REUSE claims verified by value-grep. Only SPRITE_ATTR_MONSTER_8008 fails.

---

## C13 残留核对

Independent python count of segment [0x080941c4, 0x08094f20):

- DAT_ slots: **88** (including DAT_080943e8 = Block2 ROM_INCBIN label)
- DWORD_ slots: **25**
- PTR_gP1LifePoints_ slots: **13**
- **Total: 126**

Proposal coverage:
- EQ_SLOTS: 109 entries (87 DAT_ + all 25 DWORD_ -- see note: 3 DWORD_ slots are in REF_SLOTS)
- Wait: 109 EQ + 3 REF (0x80943cc, 0x8094cc0, 0x8094d80) = 112 for DAT_+DWORD_ minus block2
- Block2 (DAT_080943e8 removed by disasm): 1
- RENAME_SLOTS: 13 PTR_

Total covered: 109 + 3 + 1 + 13 = 126 = all auto-named slots. C13 PASS.

Note: 0x08094cc0 and 0x08094d80 appear in REF_SLOTS but proposal note says "EQ not REF". These should be in EQ_SLOTS (they are literal pool words holding gP1LifePoints pointer). This is an organizational inconsistency but does not cause a coverage gap.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | §五: Seg-1 [0x080941c4, 0x08094f20); proposal 完全匹配。实际 fn 数=31 (§五 估计 19 是近似值, 不影响 C1) |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | PASS | Block1=R4 disasm+§5.1; Block2=R4 disasm; Block3=R4 disasm+§5.1; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立重跑: Block1 raw=0/thumb=0; Block3 raw=0/thumb=0; 两者前驱函数均以 bx r0/bx r1 结尾, 非 fall-through |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 抽查 38 槽全部一致; Block3 pool 0x0201c4e0=gP1LifePoints (p5-refine doc 预览表 0x0201e4d4 有误, ROM 字节纠正) |
| C5 R1 复用 | 新建前确无现有可复用 | **FAIL** | SPRITE_ATTR_MONSTER_8008 (0x00008008): 独立 grep 返回 1 hit = card_info.inc:60 CARD_DESC_RENDER_PARAM; proposal 声称 grep=0 错误. 另: UNINIT_GUARD_FFFF grep 有 5 hits, proposal 描述 "not as named constant" 措辞不准确 (见 Fix #1) |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 全部 109 EQ 槽名符合 ^[a-z][a-z0-9_]+$, 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | REF_SLOTS 3 项均有 label 规划; 0x80943cc (jump table ptr) 有 ldr 代码引用; 0x8094cc0/0x8094d80 作为 literal pool 由 ldr 自动建引用; 无独立 carve (Block1/3 是孤儿代码非数据表) |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | PASS | 新 plate 文本 (get_effect_slot_entry_ptr, get_activation_zone_card_type_field) 中 FUN_080bb414 是当前仍未命名函数 (在 asm/02/12/15 中均以 FUN_ 形式存在), 非 stale 残留; 两个 CJK 旧 plate 将被 ASCII 替换 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 全部 4 个新 plate 文本经 grep [^\x00-\x7F] 确认纯 ASCII; 现 asm 中非 ASCII 仅 L2(文件头 GAS comment, 非 Ghidra plate) / L172 / L212, 后两者在 proposal 中被 ASCII 替换计划覆盖 |
| C10 carve | 指针表条目 +1 (THUMB) 核对 | PASS | Block2 dispatch via mov pc,r0 (0x4687), raw ptr; 表条目均为裸地址无 +1 ✓ |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 31 个函数名检查无矛盾; Block1 read_slot_tile_index_by_slot_idx 与体一致; Block3 reset_duel_turn_to_state2 与体一致 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | 12 个消费者证据条目均有 asm file:line + confidence; 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | PASS | python 清点: DAT_=88 / DWORD_=25 / PTR_=13 = 126; proposal 三表并集 109+3+1(block2)+13=126 精确匹配 |

---

## 修改清单 (NEEDS_FIX)

### Fix #1 — C5 — SPRITE_ATTR_MONSTER_8008: 必须文档化 domain 区分

**位置**: EQ 表 slot 0x08094b80 + 新增 constants 表 SPRITE_ATTR_MONSTER_8008

**问题**: 独立 grep `0x8008` / `0x00008008` 在 constants/*.inc 返回 **1 hit**:
```
constants/card_info.inc:60: .equ CARD_DESC_RENDER_PARAM, 0x00008008
```
Proposal 声称 "grep 0x8008 constants/=0 -- but 145 ROM refs, check" 是**错误**的。

**分析**: CARD_DESC_RENDER_PARAM 用于 render_glyph_jp 层参数 (字形渲染 layer id), SPRITE_ATTR_MONSTER_8008 用于 enqueue_sprite_attr_record 的 sprite attr 参数 (精灵 OAM 属性类型). 两者调用不同子系统, 是 domain 区分的合法碰撞 (参照 feedback_c5_offset_value_collision_scope, 同值异域可独立建常量).

**修改**:
1. 在 EQ 表 slot 0x08094b80 的 `source` 列改为:
   `NEW (grep 0x00008008=1 hit: card_info.inc CARD_DESC_RENDER_PARAM, 域=字形渲染layer; 本域=sprite_attr OAM队列, domain distinct -> new SPRITE_ATTR_MONSTER_8008 in sprite_attr/duel_field domain)`
2. 在新增 constants 表 SPRITE_ATTR_MONSTER_8008 行 evidence 改为:
   `process_card_play_ok_sequence: enqueue_sprite_attr_record(0x8008,...) monster phase; existing CARD_DESC_RENDER_PARAM=0x8008 in card_info.inc for jp glyph layer param (different subsystem); domain-distinct new constant; 145 ROM refs; conf: high`
3. Fixer 落地时在适当 inc 文件中新建 `.equ SPRITE_ATTR_MONSTER_8008, 0x00008008` (推荐 duel_field.inc 中 sprite attr 区段)

### Fix #2 (informational, 不阻断) — C5 — UNINIT_GUARD_FFFF grep 描述措辞

**位置**: EQ 表 slot 0x08094740

**问题**: Proposal 说 "grep 0xffff constants/=many hits for other CIDs, but not as named constant" 措辞不准确. 实际已有 5 个具名常量: OAM_ATTR0_HIDDEN / SLOT_CARD_EMPTY / EQUIP_SLOT_SCORE_CAP / LP_ROW_TYPE8_ALL_SLOTS_MASK / EQUIP_ACTIVATION_CNT_CAP 均为 0x0000ffff.

**结论**: NEW 决定正确 (LP timer 初始化哨兵域与上述域均不同), 措辞须订正为 "grep 0xffff=5 hits, all different domains (OAM/card-slot/score/row-mask/counter-cap); LP timer guard domain is distinct -> new UNINIT_GUARD_FFFF".

**是否阻断**: 不阻断 (决定正确, 仅措辞需要更新). Fixer 可在修 Fix #1 时一并订正.

---

## OPEN QUESTION 裁定

**OQ1 (0x161c sentinel REUSE)**: TRIBE_INFECTING_VIRUS_CID = 0x0000161c 在 card_info.inc:912 确认存在. REUSE 合法. 写到 [gP1LifePoints+LP_ACTIVATION_PENDING_OFF] 的语义 (CID 作为初始值而非计数器) 确属不寻常, 但这是运行时语义问题, 不影响符号化决策. EOL 注记计划合理. **裁定: REUSE 通过.**

**OQ2 (Block3 §5.1 无 CSV row)**: Block3 (reset_duel_turn_to_state2) 全 ROM 0 引用已独立确认, 不能被调用, 故不写 CSV row 正确. **裁定: 无 CSV row 合规.**

---

## 其他观察 (不阻断)

1. **Block2 case 描述顺序错误**: Proposal 把 zone_type dispatch 顺序写错 (case1 应为 0x80943f4 -> #0x10, 而非 0x80943ec -> #0x04). 但 disasm **过程** (5 个 DisassembleCommand 的正确地址) 无误, 不影响落地结果.

2. **0x08094cc0 / 0x08094d80 分类**: 应属 EQ_SLOTS (字面量池持有 gP1LifePoints 指针), 但被放入 REF_SLOTS 且 note 自相矛盾 ("EQ not REF" vs 在 REF 表中). C13 总覆盖无缺口, 不阻断.

3. **fn 数注记**: Proposal 头部 NOTE 说 "Only 19 of these 31 entries fall within [0x080941c4, 0x08094f20)" 是错误的, 实际 31 个函数全部在范围内. C1 只看边界不看数量, 不阻断.

---

## 状态: NEEDS_FIX(1 blocking item)

Fix #1 (C5 SPRITE_ATTR_MONSTER_8008 文档化 domain 区分) 为阻断项.
Fix #2 (措辞) 为轻量非阻断, 建议与 Fix #1 合并修订.

## Reviewer Verdict: F12-Seg-1 = NEEDS_FIX(1 item)
