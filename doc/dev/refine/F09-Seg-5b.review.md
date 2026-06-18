# Refine Review: F09-Seg-5b [0x08073a5c..0x08074338)

Reviewer: refine-reviewer (independent). Date: 2026-06-19.

---

## 核验 (C1-C13)

| #   | 检查                                 | 结果 | 备注 |
|-----|--------------------------------------|------|------|
| C1  | 段范围与 §五 路线图一致, 无跳号/回头   | OK   | Seg-5a landed fa30373 at [0x08072d20,0x08073a5c); Seg-5b is [0x08073a5c,0x08074338): consecutive, no gap, no overlap. Proposal lists exactly 4 blocks (B7-B10). Block 0x73900 cleanly moved to Seg-5a; only footnote references remain in Seg-5b. |
| C2  | 每个 ROM_INCBIN 块都有归宿           | OK   | 4 ROM_INCBIN confirmed in asm lines 11328/11361/11723/11754 (0x73b1c/0x30, 0x73bc8/0x1bc, 0x73fde/0x2e, 0x74080/0x178). All 4 classified R4 disasm. No silent residuals. |
| C3  | §5.1 块确 0 引用 (自己重跑)          | OK   | §5.1 = 0. All 4 blocks have confirmed refs (see C3 detail below). No block was wrongly assigned §5.1. |
| C4  | EQ value == ROM 4 字节小端           | OK   | All 25 EQ slots verified by python read: 19 REUSE + 2 NEW all match ROM exactly. 4 REF slots verified as 0x0201c4e0 (gP1LifePoints). |
| C5  | 新建 constants 前确无现有可复用      | OK   | RELOAD_CID=0x16d9: grep 0 hits across all constants/*.inc. DISTURBANCE_STRATEGY_CID=0x15aa: grep 0 hits. Both confirmed new. REUSE constants (REASONING_CID=0x159a line 1190, REVERSAL_QUIZ_CID=0x15a5 line 1023, MIND_WIPE_CID=0x17f3 line 1231) verified present in card_info.inc. ewram.inc constants (gEquipChainSlotRefs/PLAYER_BLOCK_STRIDE/gDuelPhaseFlags/gDuelFieldSlots/EQUIP_PHASE_FRAME_OFF/P1LP_BLOCK2_OFF_1CE8) all verified present. |
| C6  | 槽名 ^[a-z][a-z0-9_]+$ 无碰撞      | OK   | RENAME labels: reasoning_dispatch_sub_stubs_3bc8, reversal_quiz_dispatch_sub_stubs_4080. Both lowercase alphanumeric+underscore, start with [a-z], no collision. NEW const names RELOAD_CID/DISTURBANCE_STRATEGY_CID follow SCREAMING_SNAKE but are constants not labels. |
| C7  | carve/全局槽有 USER-label + DATA-ref  | OK   | No carve in Seg-5b. REF_SLOTS (4x gP1LifePoints): label rename action described (eliminate DWORD_ def label). Accepted. |
| C8  | plate 引用全用现名, 无残留旧 FUN_    | OK   | Exhaustive grep of asm/09 lines 11207-12011: FUN_08071d64 appears once at absolute line 11952 in the plate of enqueue_spirit_zone_sprite_type11. dispatch_spirit_monster_zone_sprite_by_card_id confirmed at 0x08071d64 (asm line 7246: push {r4,r5,r6,r7,lr} @ 08071d64). PLATE fix is correct. The second grep hit FUN_08074708 at line 11988 is in apply_equip_activation_for_zone_slot_sprite (0x08074338, Seg-6 start) -- out of scope, correctly excluded. Note: proposal's stated "line 11513" is incorrect (actual absolute line is 11952), but the functional fix is correct and unambiguous. |
| C9  | ASCII: plate/EOL 文本纯 ASCII       | OK   | python byte-scan of asm lines 11207-12011: zero bytes > 0x7f. All plate/EOL comments are pure ASCII. (Non-ASCII in proposal.md is CJK section headers in doc/, expected and acceptable.) |
| C10 | carve 指针表条目 +1 核对             | N/A  | No carve planned. Dispatch table entries are raw (non-THUMB) code pointers -- correctly not +1. THUMB+1 pointers in FS handler tables (B7: 0x08073b1d, B9: 0x08073fe1) confirmed by ROM read. |
| C11 | 误名: 函数体全局 vs 函数名矛盾       | OK   | FUNC_RENAME=0. No contradictions identified. |
| C12 | 关键槽语义有 file:line + 置信度      | OK   | R6 evidence provided: RELOAD_CID asm line 11368 (DWORD_08074210) with card-stats.s line 18657 confirmation, confidence high. DISTURBANCE_STRATEGY_CID asm line 11370 (DWORD_08074214) with card-stats.s line 15563, confidence high. B7/B9 CIDs confirmed via ROM read at FS table entries. |
| C13 | 段内所有残留自动名槽 100% 覆盖       | OK   | Independent python count of DWORD_/DAT_ label definitions in asm lines 11207-12011: 27 slots exactly. Union: 19 EQ_REUSE + 2 EQ_NEW + 4 REF + 2 RENAME = 27. All within [0x08073a5c, 0x08074338). No unclassified slots, no double-count. |

---

## Ref-scan 详情 (C3 自主复核)

**B7** (0x08073b1c, fn_eligible_reasoning, 0x30 bytes):
- Entry 0x08073b1c: raw=0, THUMB+1=2.
- Legitimate ref: 0x09e412b8 (4-byte aligned, in FS handler table, CID @-4 = 0x159a Reasoning). Confirmed.
- Second "hit" 0x081bf29e: alignment mod 4 = 2, not a valid code pointer. False positive in FS data.
- FS table verified: ROM[0x09e412b8] = 0x08073b1d (THUMB+1); ROM[0x09e412b4] = 0x159a. Both confirmed.
- Classification: R4 disasm. CORRECT.

**B8** (0x08073bc8, reasoning sub-stubs, 0x1bc bytes):
- Entry 0x08073bc8: raw=1 (from dispatch table last entry at 0x08073bc4). Confirmed.
- THUMB+1 refs: 0. Confirmed.
- Internal dispatch table (0x08073b4c..0x08073bc8, 31 entries = 0x7c bytes):
  - 9 unique targets, all with 1+ raw ref from table. All classified as code. Confirmed.
  - Note: proposal states "0x78 bytes, 30 entries" -- actual is 0x7c bytes, 31 entries (off-by-1 in docs). Does NOT affect disasm action.
- Extra raw hit at 0x08073d22 from 0x09fc231e: alignment mod 4 = 2. False positive.
- Classification: R4 disasm. CORRECT.

**B9** (0x08073fde, fn_eligible_reversal_quiz, 0x2e bytes):
- 2-byte align pad at 0x08073fde (0x0000 confirmed); fn_elig starts at 0x08073fe0.
- Entry 0x08073fe0: raw=0, THUMB+1=1.
- Legitimate ref: 0x09e41378 (4-byte aligned, in FS handler table). Confirmed.
- FS table verified: ROM[0x09e41378] = 0x08073fe1; ROM[0x09e41374] = 0x15a5 (Reversal Quiz). Confirmed.
- Extra raw hits at 0x08074006 from 0x09eb746d (mod4=1) and 0x09eb8976 (mod4=2). Both false positives.
- Literal pool: 0x08074004=0x0201b290 (gDuelPhaseFlags), 0x08074008=0x0807400c (B10 table ptr). Confirmed.
- Classification: R4 disasm. CORRECT.

**B10** (0x08074080, reversal quiz sub-stubs, 0x178 bytes):
- Entry 0x08074080: raw=1 (from B9 dispatch table last entry at 0x0807407c). Confirmed.
- THUMB+1 refs: 0. Confirmed.
- Internal dispatch table (0x0807400c..0x08074080, 29 entries = 0x74 bytes):
  - 6 unique targets (0x08074080/0x080740e8/0x08074114/0x08074148/0x080741e4 + default 0x080741ee x24). Confirmed.
  - Last entry at 0x0807407c = 0x08074080 (self-ptr). Confirmed.
- Extra raw hits: 0x080740ba x6 from 0x09ecec... (alignment OK but [-4]=0x06074004 = VRAM addr, not a CID+fn_ptr handler entry; false positives in FS data). 0x080740fc from 0x09e93b0e (mod4=2, false positive). 0x08074104 from 0x08b401dc (in compressed FS blob, surrounding values not structured code pointers). 0x08074116 from 0x081af641 (mod4=1, false positive).
- Classification: R4 disasm. CORRECT.

---

## 文档小瑕疵 (不影响落地)

1. **B7 literal pool 描述地址错误** (disasm plan section line 116): 写"0x08073b44=0x46876800 (opcode word, part of fn body), 0x08073b44=gDuelPhaseFlags" -- 0x46876800 实际在 0x08073b40 (fn body code), 不是 0x08073b44. 分类表 (行37) 已正确写 "0x08073b44=0x0201b290 (gDuelPhaseFlags)". disasm action plan (createDWord at 0x08073b44/0x08073b48) 正确. 不影响落地。

2. **B8 dispatch table 大小** (line 118): 写 "0x08073b4c..0x08073bc4 (0x78 bytes, 30 .word entries)", 实际应为 0x08073b4c..0x08073bc8 (0x7c bytes, 31 entries). 末条目 0x08073bc4=0x08073bc8 确实存在且 proposal 在入口列表中正确标注 "0x08073bc8(x1 self-ref)". 不影响落地。

3. **PLATE 行号** (line 107): 写 "Line 11513" 但实际 FUN_08071d64 在 asm/09 绝对行 11952. 功能描述正确, 不影响落地.

---

## 状态: PASS

所有 C1-C13 核验通过。上述 3 处为 proposal 文档内部的记录瑕疵，不影响 fixer 落地动作的正确性（ROM 值、ref-scan 分类、EQ/RENAME/REF 动作、PLATE 修复目标均已独立验证正确）。

---

## Reviewer Verdict: F09-Seg-5b = PASS
