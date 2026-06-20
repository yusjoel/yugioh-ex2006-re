# Refine Proposal: F09-Seg-10b  [0x79500..0x79e60)

Continuation of F09-Seg-10a. Split boundary 0x79500 = start of apply_equip_activation_for_all_slots_both_players.
This is the FINAL segment of asm/09_equip_lp_display.s (file 09 complete after landing).

---

## 段测绘

- 函数入口 x4 (named, no stale FUN_):
  - 0x79500 apply_equip_activation_for_all_slots_both_players
  - 0x79594 dispatch_equip_slot_activation_seq_by_lp_state
  - 0x797d0 dispatch_equip_slot_sprite_by_zone_flag_and_count
  - 0x79944 tick_neo_daedalus_equip_lp_state
  - (B6 fn_eligible @ 0x7965c, B8 fn_eligible @ 0x79a1c, B9 fn_eligible @ 0x79bdc -- in ROM_INCBIN)

- 残留 DWORD_ 槽 x15 (see EQ_SLOTS)
- PTR_DAT_ x3: PTR_DAT_080796b0 PTR_DAT_08079a68 PTR_DAT_08079c1c
- DAT_ x3: DAT_080796c4 DAT_08079adc DAT_08079c9c
- ROM_INCBIN x5: B6(0x7965c/0x50) B7(0x796c4/0x10c) B8(0x79a1c/0x48) B9(0x79adc/0x13c) B10(0x79c9c/0x1c4)
- Scalar ptr slots (4-byte .word pointing to dispatch tables):
  - 0x080796ac -> PTR_DAT_080796b0
  - 0x08079a64 -> PTR_DAT_08079a68
  - 0x08079c18 -> PTR_DAT_08079c1c

---

## 数据块分类 (Rule 2/3) -- 全部 ref-scan 证据

| 块 | 范围 | size | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|----|------|------|--------------------------|------|------|
| B6 | 0x7965c..0x796ac | 0x50 | thumb=2 @0x9e42098 and @0x9e42200 | R4 disasm fn_eligible | Both refs in 0x09e4xxxx; CID@(0x9e42098-4)=0x179f=ORDER_TO_CHARGE_CID; CID@(0x9e42200-4)=0x17b8=ORDER_TO_SMASH_CID (both REUSE card_info.inc) |
| B7 | 0x796c4..0x797d0 | 0x10c | raw>=1 at 5 unique addrs from PTR_DAT_080796b0 | R4 disasm sub-stubs | PTR_DAT_080796b0 5-entry table raw-refs into B7 |
| B8 | 0x79a1c..0x79a64 | 0x48 | thumb=1 @0x9e45ef0 | R4 disasm fn_eligible | 0x9e45ef0 in 0x09e4xxxx; CID@(0x9e45ef0-4)=0x17c3=FAMILIAR_KNIGHT_CID (REUSE card_info.inc) |
| B9 | 0x79adc..0x79c18 | 0x13c | stubs: raw>=1 at 6 unique addrs; fn_elig: thumb=1 @0x9e42230 | R4 disasm sub-stubs + fn_eligible | PTR_DAT_08079a68 29-entry table raw-refs into B9 stubs; fn_eligible at 0x79bdc from 0x9e42230 in 0x09e4xxxx; CID@(0x9e42230-4)=0x17ca=INFERNO_TEMPEST_CID (NEW) |
| B10 | 0x79c9c..0x79e60 | 0x1c4 | raw>=1 at 9 unique addrs; THUMB 0x79e02 from 0x98355b1 (false positive), 0x79e1c from 0x874a8df (false positive) | R4 disasm sub-stubs | PTR_DAT_08079c1c 32-entry table raw-refs into B10; THUMB refs at 0x9835xxxx and 0x874axxxx are NOT 0x09e4xxxx -> compressed-data artifacts |

---

## 符号化计划

### EQ_SLOTS (data-equate)

| slot | value | const_name | source | slot_label |
|------|-------|------------|--------|------------|
| DWORD_08079588 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | EQ_gEquipZoneCountTable |
| DWORD_0807958C | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | EQ_PLAYER_STRIDE |
| DWORD_08079590 | 0x0201c510 | gDuelFieldSlots | ewram.inc | EQ_gDuelFieldSlots |
| DWORD_080795B8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | EQ_gDuelPhaseFlags |
| DWORD_08079640 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | EQ_PLAYER_STRIDE |
| DWORD_08079644 | 0x0201c510 | gDuelFieldSlots | ewram.inc | EQ_gDuelFieldSlots |
| DWORD_0807985C | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | EQ_PLAYER_STRIDE |
| DWORD_08079860 | 0x0201c510 | gDuelFieldSlots | ewram.inc | EQ_gDuelFieldSlots |
| DWORD_08079898 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | EQ_gDuelPhaseFlags |
| DWORD_0807989C | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQ_EQUIP_PHASE_FRAME_OFF |
| DWORD_08079938 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | EQ_PLAYER_STRIDE |
| DWORD_0807993C | 0x0201c510 | gDuelFieldSlots | ewram.inc | EQ_gDuelFieldSlots |
| DWORD_08079940 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQ_EQUIP_PHASE_FRAME_OFF |
| DWORD_08079970 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | EQ_gDuelPhaseFlags |
| DWORD_080799C0 | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | card_info.inc | EQ_CARD_DISPLAY_OP31_LP_BAR_SUB |

EQ count: 15 slots. All REUSE.

C5 dedup evidence:
- CARD_DISPLAY_OP31_LP_BAR_SUB=0x11d: grep card_info.inc -> CARD_DISPLAY_OP31_LP_BAR_SUB = 0x0000011d; REUSE confirmed
- EQUIP_PHASE_FRAME_OFF=0x4a4: ewram.inc confirmed
- PLAYER_BLOCK_STRIDE=0x868: grep ewram.inc:250 -> PLAYER_BLOCK_STRIDE = 0x868; REUSE confirmed (5 slots at 0x7958c/0x79640/0x7985c/0x79938; slot_label EQ_PLAYER_STRIDE retained)
- All other values: confirmed in ewram.inc

### REF_SLOTS (USER-label + DATA-ref)

Scalar ptr-to-table slots (current label: raw .word with addr comment):

| slot | value | label_after | note |
|------|-------|-------------|------|
| 0x080796ac | 0x080796b0 | ptr_to_PTR_DAT_080796b0 | self-ptr before B7 dispatch table; PTR_DAT_080796b0 has 5 entries |
| 0x08079a64 | 0x08079a68 | ptr_to_PTR_DAT_08079a68 | self-ptr before B9 dispatch table; PTR_DAT_08079a68 has 29 entries |
| 0x08079c18 | 0x08079c1c | ptr_to_PTR_DAT_08079c1c | self-ptr before B10 dispatch table; PTR_DAT_08079c1c has 32 entries |

PTR_DAT_ and DAT_ labels (already named by Ghidra, will get post-disasm function labels):

| slot | existing_label | action |
|------|---------------|--------|
| PTR_DAT_080796b0 | PTR_DAT_080796b0 | rename post-disasm: B7 5-entry dispatch table |
| DAT_080796c4 | DAT_080796c4 | rename post-disasm: start of B7 sub-stubs |
| PTR_DAT_08079a68 | PTR_DAT_08079a68 | rename post-disasm: B9 29-entry dispatch table |
| DAT_08079adc | DAT_08079adc | rename post-disasm: start of B9 sub-stubs |
| PTR_DAT_08079c1c | PTR_DAT_08079c1c | rename post-disasm: B10 32-entry dispatch table |
| DAT_08079c9c | DAT_08079c9c | rename post-disasm: start of B10 sub-stubs |

### FUNC_RENAME (误名订正)

No function renames needed. All 4 named functions have accurate semantics confirmed by body inspection.

tick_neo_daedalus_equip_lp_state: plate comment says "Called via effect node function pointer table (Sub-type B, fn-ptr at ROM 0x09e42218)" -- verified: 0x09e42218 is in 0x09e4xxxx; no rename needed.

### PLATE (R5)

No plate changes for Seg-10b named functions. Disassembled block functions will receive plates post-disasm.

---

## 新增 constants / 全局

One new constant needed in card_info.inc:

1. INFERNO_TEMPEST_CID = 0x000017ca
   - Card name: Inferno Tempest (passcode 14391920; data/card-stats.s slot=0x17CA confirmed by prior work)
   - Consumer: B9 fn_eligible at 0x79bdc; THUMB+1 ref from 0x9e42230; CID@(0x9e42230-4)=0x17ca (python verified); confidence high
   - grep card_info.inc 0x17ca -> 0 hits; grep INFERNO_TEMPEST -> 0 hits; NEW confirmed
   - Placement: after FAMILIAR_KNIGHT_CID = 0x000017c3 (or in sequence with other 0x17xx CIDs)

Note: RECYCLE_CID (0x16d5) and CARD_TYPE_FIELD8_MASK (0xb4f80000) are defined in Seg-10a proposal.
ORDER_TO_CHARGE_CID (0x179f) and ORDER_TO_SMASH_CID (0x17b8) already exist in card_info.inc (verified by grep).

---

## disasm 计划 (R4)

All 5 blocks are R4 disasm (zero ROM_INCBIN residue target).

### B6: fn_eligible shared by Order to Charge (CID=0x179f) and Order to Smash (CID=0x17b8)

Range: [0x7965c, 0x796ac) THUMB
Entry point: 0x7965c (single fn_eligible body)
Sources:
  - THUMB+1 ref at 0x9e42098; CID@(0x9e42098-4)=0x179f=ORDER_TO_CHARGE_CID
  - THUMB+1 ref at 0x9e42200; CID@(0x9e42200-4)=0x17b8=ORDER_TO_SMASH_CID (confirmed via earlier lookup: BIG_WAVE_SMALL/Order to Smash listed in prior analysis)
Both entries point to same fn_eligible (shared implementation).

Procedure:
1. clearListing [0x807965c, 0x80796ac)
2. setTMode 0x807965c
3. DisassembleCommand 0x807965c (single fn body; dispatch table 0x796ac is already decoded after block)
4. createDWord for literal pools in B6

Zero-residue: B6 is 0x50 bytes; single fn_eligible covers full range.

### B7: 5 sub-stubs for equip slot activation dispatch

Range: [0x796c4, 0x797d0) THUMB
5 entry points from PTR_DAT_080796b0 (5-entry table):
  0x796c4 0x7970e 0x79734 0x79760 0x797c4

Procedure:
1. clearListing [0x80796c4, 0x80797d0)
2. setTMode 0x80796c4
3. DisassembleCommand per unique entry point IN ADDRESS ORDER:
   0x80796c4, 0x807970e, 0x8079734, 0x8079760, 0x80797c4
4. createDWord for literal pools between stubs

Zero-residue: 5 stubs cover [0x796c4..0x797d0).

### B8: fn_eligible for Familiar Knight (CID=0x17c3)

Range: [0x79a1c, 0x79a64) THUMB
Entry point: 0x79a1c (fn_eligible body)
Source: THUMB+1 ref at 0x9e45ef0; CID@(0x9e45ef0-4)=0x17c3=FAMILIAR_KNIGHT_CID (REUSE)

Procedure:
1. clearListing [0x8079a1c, 0x8079a64)
2. setTMode 0x8079a1c
3. DisassembleCommand 0x8079a1c
4. createDWord for literal pools

Zero-residue: B8 is 0x48 bytes; single fn_eligible.
Note: dispatch table PTR_DAT_08079a68 points into B9, not B8. B8 contains only the Familiar Knight fn_eligible.

### B9: 6 sub-stubs + fn_eligible for Inferno Tempest (CID=0x17ca)

Range: [0x79adc, 0x79c18) THUMB
Entry points:
  Sub-stubs (raw-ref from PTR_DAT_08079a68 29-entry table):
    0x79adc 0x79af8 0x79b62 0x79b80 0x79bb4 0x79bd0(default, raw=24)
  fn_eligible (THUMB+1 from 0x9e42230):
    0x79bdc (CID=0x17ca=INFERNO_TEMPEST_CID NEW)

B9 structure: 6 sub-stubs in [0x79adc..0x79bdb], fn_eligible in [0x79bdc..0x79c18).

Procedure:
1. clearListing [0x8079adc, 0x8079c18)
2. setTMode 0x8079adc
3. DisassembleCommand per unique entry point IN ADDRESS ORDER:
   0x8079adc, 0x8079af8, 0x8079b62, 0x8079b80, 0x8079bb4, 0x8079bd0, 0x8079bdc
4. createDWord for literal pools

Zero-residue: 7 entry points (6 stubs + 1 fn_eligible) cover [0x79adc..0x79c18).

### B10: 9 sub-stubs for Neo-Daedalus equip LP sequence

Range: [0x79c9c, 0x79e60) THUMB
9 entry points from PTR_DAT_08079c1c (32-entry table; 4 unique non-default targets + default):
  0x79c9c 0x79cd4 0x79d24 0x79d74 0x79da4 0x79dc0 0x79dd8 0x79df0 0x79e4e(default, raw=24)

Note: THUMB refs 0x79e02|1 (from 0x98355b1) and 0x79e1c|1 (from 0x874a8df) are NOT 0x09e4xxxx -> compressed-data false positives. 0x79e02 and 0x79e1c are expected to be mid-instruction bytes or literal pool entries within sub-stubs; verify post-disasm that they fall within decoded instructions.

Procedure:
1. clearListing [0x8079c9c, 0x8079e60)
2. setTMode 0x8079c9c
3. DisassembleCommand per unique entry point IN ADDRESS ORDER:
   0x8079c9c, 0x8079cd4, 0x8079d24, 0x8079d74, 0x8079da4, 0x8079dc0, 0x8079dd8, 0x8079df0, 0x8079e4e
4. createDWord for literal pools
5. Verify 0x79e02 and 0x79e1c fall within decoded instruction ranges (not gaps)

Zero-residue: 9 stubs cover [0x79c9c..0x79e60).

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 5 blocks have confirmed references (R4 disasm).

B10 THUMB false positives (0x98355b1, 0x874a8df) are compressed-data artifacts; the real refs to B10 are from PTR_DAT_08079c1c (raw). Not §5.1.

---

## 消费者证据 (R6)

| 槽 | 语义 | file:line | 置信度 |
|----|------|-----------|--------|
| DWORD_08079588 = 0x0201e1c8 | gEquipZoneCountTable: player toggle base used to XOR player selection in activation loop | asm/09 line 23925-23927: ldr r4,[r1,#0x0]; eors r4,r0 (r0=loop counter XOR into r4) | high |
| DWORD_08079590 = 0x0201c510 | gDuelFieldSlots: equip slot array base for slot[player*0x868+slot*0x14+0x6] | asm/09 line 23984: .word 0x0201c510 | high |
| DWORD_080799C0 = 0x11d | CARD_DISPLAY_OP31_LP_BAR_SUB: trigger_card_display_op31_if_not_active opcode param 0x11d | asm/09 line 24377: ldr r1,[DWORD_080799c0]; bl trigger_card_display_op31_if_not_active | high |
| B6 fn_eligible | Shared eligibility check for Order to Charge (0x179f) and Order to Smash (0x17b8); both in card_info.inc | ref-scan 0x9e42098 CID=0x179f; 0x9e42200 CID=0x17b8; python ROM read confirmed | high |
| B9 fn_eligible @ 0x79bdc | fn_eligible for Inferno Tempest (0x17ca); embedded at offset +0x100 from B9 start | ref-scan 0x9e42230 THUMB+1=0x08079bdd; CID@(0x9e42230-4)=0x17ca | high |

---

## C8 stale FUN_ 扫描

Scanned asm/09_equip_lp_display.s lines 23913..24501 (Seg-10b range):
- grep FUN_ in [0x79500..0x79e60): 0 hits. No stale FUN_ names.
- Confirmed: all named functions in 10b use semantic names.

Also confirmed no non-ASCII CJK characters in Seg-10b asm lines (C8 mojibake scan: 0 violations).

---

## C13 残留 100% 覆盖 (Seg-10b proof)

Total auto-name slots in [0x79500..0x79e60):
- DWORD_ x15 (all EQ)
- PTR_DAT_ x3: PTR_DAT_080796b0 PTR_DAT_08079a68 PTR_DAT_08079c1c (post-disasm rename)
- DAT_ x3: DAT_080796c4 DAT_08079adc DAT_08079c9c (post-disasm rename)
- Scalar ptr .word x3: 0x080796ac 0x08079a64 0x08079c18 (REF)

Sum: 15 EQ + 3 PTR_DAT + 3 DAT + 3 scalar = 24 slots total.

All 15 DWORD_: 100% EQ assigned.
All 3 PTR_DAT_ + 3 DAT_: post-disasm rename.
All 3 scalar ptr: REF (ptr-to-table).
Coverage: 24/24 = 100%.

---

## Executor Report: F09-Seg-10a + F09-Seg-10b (combined)

- Slots: EQ=44 (29+15) REF=6 (3+3 ptr) RENAME=0 FUNC_RENAME=0 PLATE=0
- carve=0 disasm=5+5=10 ranges (B1-B10 all R4) §5.1=0
- 新增 constants/全局: RECYCLE_CID=0x16d5 (card_info.inc, Seg-10a), CARD_TYPE_FIELD8_MASK=0xb4f80000 (card_info.inc, Seg-10a), INFERNO_TEMPEST_CID=0x17ca (card_info.inc, Seg-10b)
- 求助: none
- proposals: doc/dev/refine/F09-Seg10.proposal.md + doc/dev/refine/F09-Seg10b.proposal.md
