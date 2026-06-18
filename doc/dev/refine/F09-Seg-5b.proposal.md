# Refine Proposal: F09-Seg-5b  [0x08073a5c..0x08074338)

## Splitting rationale
Continuation of Seg-5 split at function boundary 0x08073a5c.
See F09-Seg-5a.proposal.md for B1-B5 details.

## 段测绘

### 函数入口 x8
- 0x08073a5c  test_equip_target_slot_by_zone_descriptor_match  (push {r4,lr})
- 0x08073ab0  enqueue_lp_counter_sprite_by_mode_and_player     (push {r4,lr})
- 0x08073d84  tick_equip_zone_sprite_and_lp_counter_state      (push {r4,r5,r6,r7,lr})
- 0x08073e94  enqueue_zone_sprite_type5_from_slot              (push {lr})
- 0x08073eb0  tick_equip_zone_eligibility_display_state_seq    (push {r4,r5,r6,r7,lr})
- 0x080741f8  tick_equip_lp_counter_display_state_seq          (push {r4,r5,r6,r7,lr})
- 0x08074318  enqueue_spirit_zone_sprite_type11                (push {lr})

Note: enqueue_hand_spell_sprite_by_set_code_match ends before Seg-5b at 0x08073863.
     B6 dispatch table at 0x0807388c (last entry of B5's literal-pool-referenced table).
     tick_equip_zone_sprite_and_lp_counter_state begins at 0x08073d84 (after B8 ends at 0x08073d84).

### ROM_INCBIN blocks x4
| Block | Start      | Size  | End        | Classification |
|-------|-----------|-------|-----------|----------------|
| B7    | 0x08073b1c | 0x30  | 0x08073b4c | R4 disasm: fn_eligible Reasoning (CID 0x159a) stub + literal pool; dispatch table at 0x08073b4c -> B8 |
| B8    | 0x08073bc8 | 0x1bc | 0x08073d84 | R4 disasm: dispatch sub-stubs (Reasoning card zone handlers; 8 stubs + default) |
| B9    | 0x08073fde | 0x2e  | 0x0807400c | R4 disasm: fn_eligible Reversal Quiz (CID 0x15a5) stub + literal pool; dispatch table at 0x0807400c -> B10 |
| B10   | 0x08074080 | 0x178 | 0x080741f8 | R4 disasm: dispatch sub-stubs (Reversal Quiz zone handlers; 4 stubs + default) |

### 残留自动名槽 x27
(See EQ_SLOTS/REF_SLOTS/RENAME_SLOTS tables below -- 27 total)

## 数据块分类 (Rule 2/3)

| 块  | ref-scan (raw / THUMB+1)                          | 判定   | 理由                                                          |
|-----|---------------------------------------------------|--------|---------------------------------------------------------------|
| B7  | raw=0 / entry 0x08073b1c THUMB+1=2 (at 0x09e412b8) | R4 disasm | FS handler table ref at 0x09e412b8 stores 0x08073b1d (THUMB+1); value at CID slot (ref-0x4) = 0x0000159a (Reasoning, card-stats.s line 15381). Literal pool at 0x08073b44=0x0201b290 (gDuelPhaseFlags) and 0x08073b48=0x08073b4c (ptr to B8 dispatch table). THUMB opcode at 0x08073b1c: 0x4647b5f0 (push {r4,r5,r6,r7,lr} + .hword 0x4647). |
| B8  | entry 0x08073bc8 raw=1 (at 0x08073bc4 dispatch table self-ptr) / THUMB+1=0 | R4 disasm | Entry raw refs from B7 dispatch table (0x08073b4c-0x08073bc4) confirm code; sub-stubs 0x08073c0c/0x08073c50/0x08073c58/0x08073d42/0x08073d48/0x08073d58/0x08073d6a each have 1 raw ref from dispatch table; 0x08073d74 (default) has 23 raw refs. All refs in 0x08073b4c..0x08073bc4 range = runtime dispatch table. |
| B9  | raw=0 / entry 0x08073fe0 THUMB+1=1 (at 0x09e41378) | R4 disasm | Block starts at 0x08073fde with 2-byte align pad (0x0000), fn_elig starts at 0x08073fe0. FS handler table ref at 0x09e41378 stores 0x08073fe1 (THUMB+1); value at CID slot (ref-0x4=0x09e41374) = 0x000015a5 (Reversal Quiz, card-stats.s line 15524). Literal pool at 0x08074004=0x0201b290 and 0x08074008=0x0807400c (ptr to B10 dispatch table). |
| B10 | entry 0x08074080 raw=1 (at 0x0807407c dispatch table self-ptr) / THUMB+1=0 | R4 disasm | Entry raw refs from B9 dispatch table (0x0807400c-0x0807407c) confirm code; sub-stubs 0x080740e8/0x08074114/0x08074148/0x080741e4 each have 1 raw ref; 0x080741ee (default) has 24 raw refs. All refs in 0x0807400c..0x0807407c range = runtime dispatch table. |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

| 槽                          | 値           | const_name                   | 来源/C5 dedup                                  |
|-----------------------------|--------------|------------------------------|------------------------------------------------|
| DWORD_08073aac              | 0x0201bb90   | gEquipChainSlotRefs          | REUSE ewram.inc (grep 0x0201bb90 ewram.inc -> hit line 316) |
| DWORD_08073ae4              | 0x00000868   | PLAYER_BLOCK_STRIDE          | REUSE ewram.inc line 250                       |
| DWORD_08073b18              | 0x00000868   | PLAYER_BLOCK_STRIDE          | REUSE ewram.inc line 250 (dup slot)            |
| DWORD_08073da8              | 0x0201b290   | gDuelPhaseFlags              | REUSE ewram.inc line 352                       |
| DWORD_08073e8c              | 0x00000868   | PLAYER_BLOCK_STRIDE          | REUSE ewram.inc line 250                       |
| DWORD_08073e90              | 0x0201c510   | gDuelFieldSlots              | REUSE ewram.inc line 313                       |
| DWORD_08073ed8              | 0x0201b290   | gDuelPhaseFlags              | REUSE ewram.inc line 352 (dup slot)            |
| DWORD_08073f0c              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF        | REUSE ewram.inc line 435                       |
| DWORD_08073f98              | 0x00001ce8   | P1LP_BLOCK2_OFF_1CE8         | REUSE ewram.inc line 275                       |
| DWORD_08073f9c              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF        | REUSE ewram.inc line 435 (dup slot)            |
| DWORD_08073fa0              | 0x00000868   | PLAYER_BLOCK_STRIDE          | REUSE ewram.inc line 250                       |
| DWORD_08073fa4              | 0x0201b290   | gDuelPhaseFlags              | REUSE ewram.inc line 352                       |
| DWORD_08074210              | 0x000016d9   | RELOAD_CID                   | NEW: Reload (card-stats.s line 18657 slot=0x16D9). grep 0x16d9 card_info.inc -> 0 hits |
| DWORD_08074214              | 0x000015aa   | DISTURBANCE_STRATEGY_CID     | NEW: Disturbance Strategy (card-stats.s line 15563 slot=0x15AA). grep 0x15aa card_info.inc -> 0 hits |
| DWORD_0807422c              | 0x000017f3   | MIND_WIPE_CID                | REUSE card_info.inc line 1231                  |
| DWORD_08074250              | 0x0201b290   | gDuelPhaseFlags              | REUSE ewram.inc line 352                       |
| DWORD_080742ac              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF        | REUSE ewram.inc line 435                       |
| DWORD_080742b4              | 0x00000868   | PLAYER_BLOCK_STRIDE          | REUSE ewram.inc line 250                       |
| DWORD_080742b8              | 0x000017f3   | MIND_WIPE_CID                | REUSE card_info.inc line 1231 (dup slot)       |
| DWORD_080742d4              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF        | REUSE ewram.inc line 435                       |
| DWORD_0807430c              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF        | REUSE ewram.inc line 435                       |

EQ total Seg-5b: EQ_REUSE=19, EQ_NEW=2 (RELOAD_CID, DISTURBANCE_STRATEGY_CID); 21 EQ total.

### REF_SLOTS (USER-label + DATA-ref)

Note: DWORD_08073ae0 and DWORD_08073b14 both have `.word gP1LifePoints` (already symbolized in
asm content), but their LABEL is still `DWORD_08073ae0` / `DWORD_08073b14`. These need the
definition label renamed to match the content. Same for DWORD_08073f94 and DWORD_080742b0.

| 槽                              | target        | gas_label        | slot_label action                               |
|---------------------------------|---------------|------------------|-------------------------------------------------|
| DWORD_08073ae0                  | gP1LifePoints | gP1LifePoints    | rename label DWORD_08073ae0 -> (no label needed; already .word gP1LifePoints; eliminate the DWORD_ def label) |
| DWORD_08073b14                  | gP1LifePoints | gP1LifePoints    | same: eliminate DWORD_ def label                |
| DWORD_08073f94                  | gP1LifePoints | gP1LifePoints    | same: eliminate DWORD_ def label                |
| DWORD_080742b0                  | gP1LifePoints | gP1LifePoints    | same: eliminate DWORD_ def label                |

REF total Seg-5b: 4 (all gP1LifePoints -- label already points to correct value, only def label needs removing)

### RENAME_SLOTS (auto-name -> semantic label)

| 槽             | addr       | new_label                                       | EOL_ascii                                          |
|----------------|-----------|--------------------------------------------------|---------------------------------------------------|
| DAT_08073bc8   | 0x08073bc8 | reasoning_dispatch_sub_stubs_3bc8               | Reasoning CID=0x159a dispatch sub-stubs            |
| DAT_08074080   | 0x08074080 | reversal_quiz_dispatch_sub_stubs_4080           | Reversal Quiz CID=0x15a5 dispatch sub-stubs        |

RENAME total Seg-5b: 2

### FUNC_RENAME (if any)

None identified.

### PLATE (R5)

| fn                            | addr       | action                                                                             |
|-------------------------------|-----------|------------------------------------------------------------------------------------|
| enqueue_spirit_zone_sprite_type11 | 0x08074318 | Substring replace: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id (stale auto-name found at asm line 11513 in plate comment). Confidence: high -- grep asm/09 for FUN_08071d64 shows line 11513 only; function was named in Seg-3. |

C8 stale FUN_ scan (Seg-5b lines 10769-11534):
- Line 11513: FUN_08071d64 in plate of enqueue_spirit_zone_sprite_type11 -> handled above
- Line 11549: FUN_08074708 and FUN_0807479c in plate of apply_equip_activation_for_zone_slot_sprite
  (0x08074338, Seg-6 -- out of scope for Seg-5b; leave for Seg-6 processing)

## disasm 计划 (R4)

### B7: fn_eligible_reasoning @ 0x08073b1c (block 0x08073b1c/0x30, end 0x08073b4c)
- FS handler ref: 0x09e412b8 stores 0x08073b1d (THUMB+1); CID at ref-0x4=0x09e412b4 = 0x0000159a (Reasoning)
- Block content: push {r4,r5,r6,r7,lr} + .hword 0x4647 (nop), fn body (0x24 bytes), literal pool
- Literal pool: 0x08073b44=0x46876800 (opcode word, part of fn body), 0x08073b44=gDuelPhaseFlags, 0x08073b48=0x08073b4c (ptr to B8 dispatch table)
- Action: setTMode(0x08073b1c); DisassembleCommand(0x08073b1c..0x08073b4c); createDWord for pool at 0x08073b44/0x08073b48
- Dispatch table 0x08073b4c..0x08073bc4 (0x78 bytes, 30 .word entries): label as reasoning_dispatch_table_3b4c
  entries: 0x08073d6a(x1), 0x08073d58(x1), 0x08073d48(x1), 0x08073d74(x23 default), 0x08073d42(x1), 0x08073c58(x1), 0x08073c50(x1), 0x08073c0c(x1), 0x08073bc8(x1 self-ref)

### B8: reasoning_dispatch_sub_stubs @ 0x08073bc8 (block 0x08073bc8/0x1bc, end 0x08073d84)
- Sub-stub entry points (from dispatch table): 0x08073bc8, 0x08073c0c, 0x08073c50, 0x08073c58, 0x08073d42, 0x08073d48, 0x08073d58, 0x08073d6a
- Default stub at 0x08073d74: opcode 0x2000 (movs r0,#0); return 0
- Action: clearListing(0x08073bc8..0x08073d84); setTMode; DisassembleCommand per entry
- Labels: reasoning_sub_3bc8, reasoning_sub_3c0c, reasoning_sub_3c50, reasoning_sub_3c58,
          reasoning_sub_3d42, reasoning_sub_3d48, reasoning_sub_3d58, reasoning_sub_3d6a,
          reasoning_default_3d74

### B9: fn_eligible_reversal_quiz @ 0x08073fe0 (block 0x08073fde/0x2e, end 0x0807400c)
- Block starts at 0x08073fde with 2-byte align pad (0x0000); fn_elig starts at 0x08073fe0
- FS handler ref: 0x09e41378 stores 0x08073fe1 (THUMB+1); CID at ref-0x4=0x09e41374 = 0x000015a5 (Reversal Quiz)
- Literal pool: 0x08074004=0x0201b290 (gDuelPhaseFlags), 0x08074008=0x0807400c (ptr to B10 dispatch table)
- Action: setTMode(0x08073fe0); DisassembleCommand(0x08073fe0..0x0807400c); createDWord for pool words
- Dispatch table 0x0807400c..0x0807407f (0x74 bytes, 29 .word entries): label as reversal_quiz_dispatch_table_400c
  entries: 0x080741e4(x1), 0x080741ee(x24 default), 0x08074148(x1), 0x08074114(x1), 0x080740e8(x1), 0x08074080(x1 self-ref)

### B10: reversal_quiz_dispatch_sub_stubs @ 0x08074080 (block 0x08074080/0x178, end 0x080741f8)
- Sub-stub entry points (from dispatch table): 0x08074080, 0x080740e8, 0x08074114, 0x08074148, 0x080741e4
- Default stub at 0x080741ee: opcode 0x2000 (movs r0,#0); 0xb002 (add sp,#8); 0xbcf0 (pop ...); return 0
- Action: clearListing(0x08074080..0x080741f8); setTMode; DisassembleCommand per entry
- Labels: reversal_quiz_sub_4080, reversal_quiz_sub_40e8, reversal_quiz_sub_4114,
          reversal_quiz_sub_4148, reversal_quiz_sub_41e4, reversal_quiz_default_41ee

## carve 计划 (R7)

No inter-function ROM data tables requiring rom.s carve in Seg-5b. All 4 blocks are code (R4 disasm). The dispatch tables (0x08073b4c, 0x0807400c) are function-internal data linked from preceding literal pools; they can remain in asm/09 with structural labels.

## 新增 constants / 全局

File: constants/card_info.inc (append)
- RELOAD_CID = 0x16d9          @ Reload (card-stats.s line 18657 slot=0x16D9 pw=22589918); tick_equip_lp_counter_display_state_seq BST; grep 0x16d9 card_info.inc -> 0 hits
- DISTURBANCE_STRATEGY_CID = 0x15aa @ Disturbance Strategy (card-stats.s line 15563 slot=0x15AA pw=77561728); tick_equip_lp_counter_display_state_seq BST; grep 0x15aa card_info.inc -> 0 hits

(REASONING_CID=0x159a already in card_info.inc line 1190; REVERSAL_QUIZ_CID=0x15a5 already in card_info.inc line 1023; MIND_WIPE_CID=0x17f3 already in card_info.inc line 1231)

## §5.1 登记 (Rule 3) -- 0 引用块

None in Seg-5b. All 4 blocks have confirmed code refs:
- B7: THUMB+1 ref at 0x09e412b8 (FS handler table CID=0x159a Reasoning)
- B8: raw refs from B7 dispatch table (0x08073b4c region)
- B9: THUMB+1 ref at 0x09e41378 (FS handler table CID=0x15a5 Reversal Quiz)
- B10: raw refs from B9 dispatch table (0x0807400c region)
(Block 0x73900/0x15c formerly listed as B6 is now in Seg-5a as B6; see F09-Seg-5a.proposal.md)

## 消費者证据 (R6)

### RELOAD_CID (0x16d9)
- asm/09_equip_lp_display.s line 11368 (DWORD_08074210): `ldr r0, DWORD_08074210; cmp r1,r0`
  Function tick_equip_lp_counter_display_state_seq (0x080741f8) at entry: ldrh r1,[r3+0] = card_id;
  BST compares card_id vs 0x16d9 (RELOAD_CID), 0x15aa (DISTURBANCE_STRATEGY_CID), 0x17f3 (MIND_WIPE_CID).
  Function plate comment confirms: CARD_ID_RELOAD=0x16d9. Confidence: high.

### DISTURBANCE_STRATEGY_CID (0x15aa)
- asm/09_equip_lp_display.s line 11370 (DWORD_08074214): `ldr r0, DWORD_08074214; cmp r1,r0`
  Same function tick_equip_lp_counter_display_state_seq; BST branch. Plate comment confirms:
  CARD_ID_DISTURBANCE_STRATEGY=0x15aa. card-stats.s line 15563 confirms slot. Confidence: high.

### fn_eligible_reasoning (B7 CID=0x159a)
- FS table at 0x09e412b8: value=0x08073b1d (THUMB+1 of 0x08073b1c); CID at 0x09e412b4=0x0000159a.
  card_info.inc line 1190: REASONING_CID=0x159a; card-stats.s line 15381. Confidence: high.

### fn_eligible_reversal_quiz (B9 CID=0x15a5)
- FS table at 0x09e41378: value=0x08073fe1 (THUMB+1 of 0x08073fe0); CID at 0x09e41374=0x000015a5.
  card_info.inc line 1023: REVERSAL_QUIZ_CID=0x15a5; card-stats.s line 15524. Confidence: high.

### dispatch table sub-stubs semantics (B8, B10)
- B8 dispatch table at 0x08073b4c: indexed by zone/card type field. Sub-stubs each implement a
  specific zone-type eligibility check for Reasoning (draws until non-monster -> any monster zone).
  B7 fn body (0x08073b1c) performs: extract zone_type_field -> dispatch via table -> return result.
  Evidence: B7 stub structure mirrors B1/B3 patterns in Seg-5a. Confidence: high (structural).
- B10 dispatch table at 0x0807400c: same pattern for Reversal Quiz (select a card type at random).
  B9 fn body same structure. Confidence: high (structural).

## C8 stale FUN_ scan

grep FUN_ in Seg-5b lines 10769-11534:
- Line 11513: FUN_08071d64 in enqueue_spirit_zone_sprite_type11 plate -- PLATE fix planned above
- No other stale FUN_ in Seg-5b named functions (lines 10769-11517)

Seg-6 function apply_equip_activation_for_zone_slot_sprite plate (line 11549) has FUN_08074708 and
FUN_0807479c -- out of Seg-5b scope; leave for Seg-6.

## C13 残留 100% 覆盖证明 (Seg-5b)

Total auto-name slots in Seg-5b [0x08073a5c..0x08074338): 27

Classification union:
- EQ_SLOTS (REUSE): 19 slots -> DWORD_08073aac/ae4/b18/da8/e8c/e90/ed8/f0c/f98/f9c/fa0/fa4
                                + DWORD_0807422c/74250/742ac/742b4/742b8/742d4/7430c = 19
- EQ_SLOTS (NEW): 2 slots -> DWORD_08074210 (RELOAD_CID), DWORD_08074214 (DISTURBANCE_STRATEGY_CID)
- REF_SLOTS: 4 slots -> DWORD_08073ae0/b14/3f94/742b0 (all gP1LifePoints; label rename only)
- RENAME_SLOTS: 2 slots -> DAT_08073bc8, DAT_08074080
  (DAT_08073900 moved to Seg-5a B6; see F09-Seg-5a.proposal.md)

21 EQ + 4 REF + 2 RENAME = 27. Coverage complete. No unclassified slots.

## 求助

None. All semantics confirmed with file:line evidence.
