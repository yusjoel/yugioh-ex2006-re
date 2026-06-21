# Refine Proposal: F09-Seg-1 REMEDIATION -- Cluster-1 [0x0806f008..0x0806f1c4)

> Remediation scope (THIS proposal): 5 residual ROM_INCBIN blocks + 2 companion .byte
> partial-decode blocks within Cluster-1 sub-stub group [0x0806f008..0x0806f1c4).
> Only the first instruction of each stub was decoded by commit 08b3db1; bodies remain
> as ROM_INCBIN/.byte (Rule 2 violation, same containing functions).
> Background: commit 08b3db1 landed Seg-1 but left these blocks undisassembled.
> Precedent: Seg-7/8/9a each fully disassembled their stubs using per-stub DisassembleCommand.
>
> NOTE -- Seg-1 has TWO additional clusters to be remediated in follow-up proposals:
>   Cluster-2 = region 0x6f85e..0x6fef2: 9 more ROM_INCBIN blocks
>     (0x6f85e/0x136, 0x6fa0a/0x36, 0x6fa62/0x12, 0x6fa78/0x8c, 0x6fb16/0x32,
>      0x6fdee/0x26, 0x6fe8a/0x4a, 0x6fede/0x12, 0x6fef2/0x18)
>     plus ~11 companion .byte code bodies (same partial-decode pattern).
>   These are deferred to F09-Seg1R2 (Cluster-2) proposals per incremental remediation strategy.
>   Full Seg-1 range [0x0806e76c..0x0806ff50) remediation is complete only after all clusters done.

---

## Section Mapping

The 5 ROM_INCBIN blocks are all within the sub-stub cluster at 0x0806f008..0x0806f1c3,
which is function-internal to the dispatch group anchored by `equip_disp_table_f03c` at 0x0806f03c.

Containing functions / stubs:

| Block | ROM off / size | Containing stub | Entry addr | Entry in asm |
|-------|----------------|-----------------|------------|--------------|
| B1    | 0x6f00a / 0x32 | eligible_creature_swap_f008 (fn_eligible) | 0x0806f008 | push decoded |
| B2a   | 0x6f07a / 0x22 | equip_disp_sub_f078 | 0x0806f078 | ldr decoded |
| B2b   | 0x6f0ae / 0x12 | equip_disp_sub_f0ac | 0x0806f0ac | movs decoded |
| B2c   | 0x6f0ce / 0xb2 | equip_disp_sub_f0cc | 0x0806f0cc | ldrb decoded |
| B2d   | 0x6f18a / 0x3a | equip_disp_sub_f188 | 0x0806f188 | ldrb decoded |

Two companion .byte blocks (NOT ROM_INCBIN but same Rule 2 violation):

| Block | Range | Containing stub |
|-------|-------|-----------------|
| B2e   | 0x6f056..0x6f065 (.byte 16B) | eligible_sub_stubs_f054 body |
| B2f   | 0x6f068..0x6f077 (.byte 16B) | equip_disp_sub_f066 body |

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

### Primary: entry-address ref-scan (confirming CODE classification)

For each ROM_INCBIN block, the critical ref-scan is on the stub ENTRY address, not the
mid-body ROM_INCBIN start. Mid-body start addresses have raw=0/thumb=0 (expected: no
external pointer to function internals).

| Block | Entry addr | Entry raw hits | Entry THUMB+1 hits | Judgment |
|-------|-----------|----------------|-------------------|----------|
| B1    | 0x0806f008 | raw=1 @ ROM 0x806d7 (misaligned, size-check context) | THUMB+1=1 @ ROM 0x1e40958 | DISASM (fn_eligible) |
| B2a   | 0x0806f078 | raw=1 @ ROM 0x6f048 (equip_disp_table_f03c entry[3]) | THUMB+1=0 | DISASM (raw dispatch) |
| B2b   | 0x0806f0ac | raw=1 @ ROM 0x6f044 (equip_disp_table_f03c entry[2]) | THUMB+1=0 | DISASM (raw dispatch) |
| B2c   | 0x0806f0cc | raw=1 @ ROM 0x6f040 (equip_disp_table_f03c entry[1]) | THUMB+1=0 | DISASM (raw dispatch) |
| B2d   | 0x0806f188 | raw=1 @ ROM 0x6f03c (equip_disp_table_f03c entry[0]) | THUMB+1=0 | DISASM (raw dispatch) |

Mid-body ref-scan (0 raw, 0 THUMB+1 for all 5 block start addresses -- expected):
- 0x0806f00a: raw=0, THUMB+1=0
- 0x0806f07a: raw=0, THUMB+1=0
- 0x0806f0ae: raw=0, THUMB+1=0
- 0x0806f0ce: raw=0, THUMB+1=0
- 0x0806f18a: raw=0, THUMB+1=0

### B1 additional evidence: FS handler table THUMB+1

ROM @ 0x1e40958 contains 0x0806f009 (= eligible_creature_swap_f008 + 1 = THUMB+1 ptr).
Entry layout at 0x1e4094c (6 DWORDs):
  +0x00: 0x08057471  (fn_ptr0)
  +0x04: 0x00000000  (NULL)
  +0x08: 0x0000142a  (CID = Creature Swap, conf:high file:roms/2343.gba@0x1e40954)
  +0x0c: 0x0806f009  (fn_eligible+1 = eligible_creature_swap_f008+1)
  +0x10: 0x080508cd  (fn_activate+1)
  +0x14: 0x0805ec41  (fn_ptr3)
CID 0x142a confirmed: data/card-stats.s "card_0910" pw=31036355 = Creature Swap. conf:high.

### Dispatch table at 0x0806f03c (raw ptr refs for B2a/b/c/d)

6-entry table (6x .word = 0x18 bytes, already labeled equip_disp_table_f03c):
  [0] 0x0806f03c: 0x0806f188 -> equip_disp_sub_f188 (B2d entry)
  [1] 0x0806f040: 0x0806f0cc -> equip_disp_sub_f0cc (B2c entry)
  [2] 0x0806f044: 0x0806f0ac -> equip_disp_sub_f0ac (B2b entry)
  [3] 0x0806f048: 0x0806f078 -> equip_disp_sub_f078 (B2a entry)
  [4] 0x0806f04c: 0x0806f066 -> equip_disp_sub_f066 (B2f entry, .byte partial)
  [5] 0x0806f050: 0x0806f054 -> eligible_sub_stubs_f054 (B2e entry, .byte partial)

All dispatch table entries are RAW code pointers (not THUMB+1). Confirmed CODE.

---

## Instruction-level decode summary (Phase 2 evidence)

### B1 (eligible_creature_swap_f008 body, 0x0806f00a..0x0806f03b)

Code segment 0x6f00a..0x6f031 (25 instructions):
  0x6f00a: mov r7,r8          (save r8 caller-save via high-reg push)
  0x6f00c: push {r7}          (push r8 via r7 to stack)
  0x6f00e: sub sp,#4          (local frame 1 word)
  0x6f010: adds r5,r0,#0      (r5 = slot_ptr param r0)
  0x6f012: adds r2,r1,#0      (r2 = zone_idx param r1)
  0x6f014: ldr r0,[pc,+0x1c]  (pool@0x6f034 = 0x0201b290 = gDuelPhaseFlags)
  0x6f016: movs r3,#0x94
  0x6f018: lsls r3,r3,#3      (r3 = 0x4a0)  -- wait: 0x94<<3 = 0x4a0
  0x6f01a: adds r1,r0,r3      (r1 = gDuelPhaseFlags + 0x4a0, near EQUIP_PHASE_FRAME_OFF 0x4a4-4)
  0x6f01c: ldr r1,[r1,#0]     (r1 = duel_phase_state value)
  0x6f01e: subs r1,#0x7b      (r1 -= 0x7b = 123)
  0x6f020: adds r4,r0,#0      (r4 = gDuelPhaseFlags base)
  0x6f022: cmp r1,#5          (check state in [0..5])
  0x6f024: bls 0x0806f028     (if in range -> dispatch)
  0x6f026: b 0x0806f1b6       (else -> epilogue, return 0)
  0x6f028: lsls r0,r1,#2      (r0 = idx*4)
  0x6f02a: ldr r1,[pc,+0xc]   (pool@0x6f038 = 0x0806f03c = equip_disp_table_f03c)
  0x6f02c: adds r0,r0,r1      (r0 = table_base + idx*4)
  0x6f02e: ldr r0,[r0,#0]     (r0 = table[idx] = target fn ptr)
  0x6f030: mov r15,r0         (computed jump: PC = table[idx])
Pad: 0x6f032..0x6f033 (0x0000, 2 bytes .zero 2)
Pool DWORDs (inside ROM_INCBIN range):
  0x6f034: 0x0201b290 = gDuelPhaseFlags
  0x6f038: 0x0806f03c = equip_disp_table_f03c

Note: b @ 0x6f026 targets 0x0806f1b6 (shared epilogue). The computed jump at 0x6f030
dispatches to one of 6 sub-stubs via the dispatch table. Flow stops at mov r15,r0.

### B2a (equip_disp_sub_f078 body, 0x0806f07a..0x0806f09b) + continuation b+pad

Code 0x6f07a..0x6f09b (17 instructions):
  0x6f07a: adds r1,r4,r0      (r1 = gDuelPhaseFlags + [offset already in r0])
  0x6f07c: ldr r0,[pc,+0x24]  (pool@0x6f0a4 = 0x0201c4e0 = gP1LifePoints, OUTSIDE incbin)
  0x6f07e: ldr r2,[pc,+0x28]  (pool@0x6f0a8 = 0x00001da8 = LP_CARD_TRACK_BASE_OFF, OUTSIDE)
  0x6f080: adds r0,r0,r2      (r0 = gP1LifePoints + LP_CARD_TRACK_BASE_OFF)
  0x6f082: ldrh r0,[r0,#0]    (r0 = LP track halfword)
  0x6f084: lsrs r0,r0,#8      (r0 = upper byte of LP track)
  0x6f086: str r0,[r1,#0]     (store to equip state field)
  0x6f088: ldrb r3,[r5,#2]    (r3 = slot flags byte[2])
  0x6f08a: lsls r2,r3,#31     (r2 = bit[0] of flags -> bit31)
  0x6f08c: lsrs r1,r2,#31     (r1 = bit[0] of flags = player side)
  0x6f08e: movs r0,#1
  0x6f090: subs r0,r0,r1      (r0 = 1 - side = !side)
  0x6f092: ldrh r1,[r5,#0]    (r1 = slot card set-code)
  0x6f094: lsrs r2,r2,#31     (r2 = side bit again)
  0x6f096: bl set_lp_display_row_type9  (-> 0x080a1cb4)
  0x6f09a: movs r0,#0x7d      (return value 0x7d)
Continuation (OUTSIDE ROM_INCBIN, currently .word 0x0000e08c):
  0x6f09c: b 0x0806f1b8       (b opcode 0xe08c; target = epilogue SP-restore)
  0x6f09e: .zero 2            (pad, 0x0000)
Note: .word 0x0000e08c is byte-identical to b+pad (LE bytes [8c e0 00 00]), but semantically
wrong. DisassembleCommand from 0x6f07a with clearListing to 0x6f09f will fix this.

### B2b (equip_disp_sub_f0ac body, 0x0806f0ae..0x0806f0bf) + continuation b+pad

Code 0x6f0ae..0x6f0bf (9 instructions):
  0x6f0ae: lsls r1,r1,#3      (r1 = state_idx * 8)
  0x6f0b0: adds r0,r4,r1      (r0 = gDuelPhaseFlags + state_idx*8)
  0x6f0b2: ldr r1,[pc,+0x10]  (pool@0x6f0c4 = 0x0201c4e0 = gP1LifePoints, OUTSIDE)
  0x6f0b4: ldr r2,[pc,+0x10]  (pool@0x6f0c8 = 0x00001da8 = LP_CARD_TRACK_BASE_OFF, OUTSIDE)
  0x6f0b6: adds r1,r1,r2
  0x6f0b8: ldrh r1,[r1,#0]    (r1 = LP track halfword)
  0x6f0ba: lsrs r1,r1,#8      (r1 = upper byte)
  0x6f0bc: str r1,[r0,#0]     (store to equip state field)
  0x6f0be: movs r0,#0x7c      (return value 0x7c)
Continuation (OUTSIDE ROM_INCBIN, currently .word 0x0000e07a):
  0x6f0c0: b 0x0806f1b8       (b opcode 0xe07a; bytes [7a e0 00 00] byte-identical to .word)
  0x6f0c2: .zero 2
Pool DWORDs outside range (already in asm, need no createDWord):
  0x6f0c4 = 0x0201c4e0 (gP1LifePoints), 0x6f0c8 = 0x00001da8 (LP_CARD_TRACK_BASE_OFF)

### B2c (equip_disp_sub_f0cc body, 0x0806f0ce..0x0806f17f) + continuation b+pad

Code 0x6f0ce..0x6f17f (89 instructions). Key structure:
  0x6f0ce: lsls r1,r3,#31     (bit[0] of r3 = player side)
  0x6f0d0: lsrs r1,r1,#31
  0x6f0d2: ldr r0,[pc,+0xb0]  (pool@0x6f184 = 0x000004a4 = EQUIP_PHASE_FRAME_OFF, OUTSIDE)
  0x6f0d4: adds r0,r0,r4      (r0 = gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF)
  0x6f0d6: mov r8,r0          (r8 = zone-state ptr)
  0x6f0d8: ldr r2,[r0,#0]     (r2 = zone_state value)
  0x6f0da: adds r0,r5,r0      (r0 = slot_ptr arg)
  0x6f0dc: bl query_slot_card_type_eligibility  (-> 0x0803670c)
  0x6f0e0: cmp r0,#0
  0x6f0e2: bne 0x0806f1b6     (if not eligible -> return 0)
  ... [further eligibility checks via check_slot_equip_whitelist_with_monster_space @0x08036450]
  0x6f142: bl enqueue_sprite_attr_with_mode  (-> 0x08043054, r3=5=mode)
  [str r3,[sp,#0] = 0x9300 (valid: STR r3,[sp,#0]) before bl]
  ... [second enqueue_sprite_attr_with_mode call for P2]
  0x6f17a: bl enqueue_equip_chain_dual_slot_sprite_with_activation_scan  (-> 0x08043f44)
  0x6f17e: movs r0,#0x7b      (return value 0x7b on success)
Continuation (OUTSIDE ROM_INCBIN, currently .word 0x0000e01a):
  0x6f180: b 0x0806f1b8       (b opcode 0xe01a; bytes [1a e0 00 00] byte-identical to .word)
  0x6f182: .zero 2
Fail branches: 0x6f0e2 bne, 0x6f0f6 beq, 0x6f112 bne, 0x6f126 beq all -> 0x0806f1b6 (return 0).
Pool at 0x6f184 = 0x000004a4 (EQUIP_PHASE_FRAME_OFF) already in asm, no createDWord needed.

### B2d (equip_disp_sub_f188 body + shared epilogue, 0x0806f18a..0x0806f1c3)

Code 0x6f18a..0x6f1c3 (29 instructions, includes shared epilogue 0x6f1b6..0x6f1c3):
  0x6f18a: lsls r0,r3,#31     (bit[0] of r3 = player side)
  0x6f18c: lsrs r0,r0,#31
  0x6f18e: ldr r2,[pc,+0x34]  (pool@0x6f1c4 = 0x000004a4 = EQUIP_PHASE_FRAME_OFF, OUTSIDE)
  0x6f190: adds r1,r4,r2      (r1 = gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF)
  0x6f192: ldr r1,[r1,#0]     (r1 = zone state)
  0x6f194: movs r2,#0x15      (sprite type?)
  0x6f196: movs r3,#1
  0x6f198: bl set_field_slot_bit_with_sprite_update  (-> 0x0804a970)
  [P1 path above]
  0x6f19c: ldrb r5,[r5,#2]    (r5 = slot flags byte[2])
  0x6f19e: lsls r1,r5,#31
  0x6f1a0: lsrs r1,r1,#31     (r1 = player side bit)
  0x6f1a2: movs r0,#1
  0x6f1a4: subs r0,r0,r1      (r0 = !side)
  0x6f1a6: movs r3,#0x95
  0x6f1a8: lsls r3,r3,#3      (r3 = 0x4a8)
  0x6f1aa: adds r1,r4,r3      (r1 = gDuelPhaseFlags + 0x4a8)
  0x6f1ac: ldr r1,[r1,#0]     (r1 = P2 zone state)
  0x6f1ae: movs r2,#0x15
  0x6f1b0: movs r3,#1
  0x6f1b2: bl set_field_slot_bit_with_sprite_update  (-> 0x0804a970)  [P2 path]
Shared epilogue (also inside ROM_INCBIN range 0x6f18a..0x6f1c3):
  0x6f1b6: movs r0,#0         (return 0 for all fail-path branches)
  0x6f1b8: add sp,#4          (restore local frame)
  0x6f1ba: pop {r3}           (restore r8 via r3)
  0x6f1bc: mov r8,r3
  0x6f1be: pop {r4,r5,r6,r7}
  0x6f1c0: pop {r1}           (lr into r1)
  0x6f1c2: bx r1              (return)
Pool at 0x6f1c4 = 0x000004a4 already in asm (.word 0x000004a4 @ 0x0806f1c4), no createDWord needed.

### B2e/B2f (.byte partial blocks -- same sub-stubs, companion fixes)

B2e (eligible_sub_stubs_f054 body, 0x6f056..0x6f065, 0x10 bytes .byte):
  0x6f056: adds r1,r2,#0      (r1 = zone_idx param)
  0x6f058: bl dispatch_card_effect_activation  (-> 0x08090848)
  0x6f05c: cmp r0,#0
  0x6f05e: bne 0x0806f062     (if non-zero result -> set return 0x7f)
  0x6f060: b 0x0806f1b6       (else -> return 0)
  0x6f062: movs r0,#0x7f      (return 0x7f on success)
  0x6f064: b 0x0806f1b8       (skip movs r0,#0 in epilogue)

B2f (equip_disp_sub_f066 body, 0x6f068..0x6f077, 0x10 bytes .byte):
  0x6f068: lsls r2,r4,#31     (bit[0] of flags; r4 holds flags byte from ldrb r4,[r5,#2] at 0x6f066)
  0x6f06a: lsrs r0,r2,#31     (r0 = player side)
  0x6f06c: ldrh r1,[r5,#0]    (r1 = slot card set-code)
  0x6f06e: adds r2,r0,#0      (r2 = side)
  0x6f070: bl set_lp_display_row_type9  (-> 0x080a1cb4)
  0x6f074: movs r0,#0x7e      (return 0x7e)
  0x6f076: b 0x0806f1b8       (to epilogue SP-restore)

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS additions from newly-decoded bodies

Two pool DWORDs inside B1 ROM_INCBIN range need EQ symbolization after createDWord:

| slot addr | value | const_name | source file | slot_label | evidence |
|-----------|-------|-----------|-------------|-----------|---------|
| 0x0806f034 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gduel_phase_f034 | eligible_creature_swap_f008: ldr r0,[pc,+0x1c] -> pool@0x6f034; used as base for phase state field reads; same global as other Seg-1 REF slots; conf:high |
| 0x0806f038 | 0x0806f03c | equip_disp_table_f03c | (label in asm) | equip_disp_tbl_f038 | eligible_creature_swap_f008: ldr r1,[pc,+0xc] -> pool@0x6f038; MOV PC,r0 uses this as jump table base; label equip_disp_table_f03c already exists at 0x0806f03c; conf:high |

Notes:
- All pool references from B2a body (0x6f0a4=gP1LifePoints, 0x6f0a8=LP_CARD_TRACK_BASE_OFF) are
  OUTSIDE the ROM_INCBIN range; they are already labeled in the asm as part of the existing
  DWORD_0806f0a0 block. No new EQ slots needed for B2a.
- All pool references from B2b body (0x6f0c4=gP1LifePoints, 0x6f0c8=LP_CARD_TRACK_BASE_OFF)
  are OUTSIDE the ROM_INCBIN range; already in asm. No new EQ slots.
- B2c pool (0x6f184=EQUIP_PHASE_FRAME_OFF) is OUTSIDE range; already in asm.
- B2d pool (0x6f1c4=EQUIP_PHASE_FRAME_OFF) is OUTSIDE range; already in asm.

### REF_SLOTS additions

| slot addr | target | gas_label | slot_label |
|-----------|--------|-----------|-----------|
| 0x0806f034 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_f034 |
| 0x0806f038 | 0x0806f03c | equip_disp_table_f03c | equip_disp_tbl_f038 |

Note: 0x6f038 value 0x0806f03c is a code-address (dispatch table), not an EWRAM global.
The slot_label equip_disp_tbl_f038 uses the existing label as the symbolic reference.

### RENAME_SLOTS

None required. All sub-stub labels (equip_disp_sub_f078, equip_disp_sub_f0ac,
equip_disp_sub_f0cc, equip_disp_sub_f188, eligible_creature_swap_f008) are already named.

The label eligible_sub_stubs_f054 was named in the original Seg-1 pass. It is semantically
a sub-stub (dispatch sub-function), not a fn_eligible. The name mismatch is a minor
inaccuracy but outside remediation scope (no FUNC_RENAME since it's a data label, not
a Ghidra function object). Document only.

### FUNC_RENAME

None. All 20 named functions in Seg-1 verified unchanged.

### PLATE

None required. No stale FUN_ references in Seg-1 plate comments related to these blocks.

---

## Disasm Plan (R4) -- complete per-stub DisassembleCommand sequence

### Recommended execution order (Block2d first to create shared epilogue labels)

**Step 0: setTMode for all ranges** (single pass before any DisassembleCommand):
- setTMode(0x0806f00a, THUMB)
- setTMode(0x0806f056, THUMB)
- setTMode(0x0806f068, THUMB)
- setTMode(0x0806f07a, THUMB)
- setTMode(0x0806f0ae, THUMB)
- setTMode(0x0806f0ce, THUMB)
- setTMode(0x0806f18a, THUMB)

**Step 1: Block2d** (equip_disp_sub_f188 body + shared epilogue)
- clearListing(0x0806f18a, 0x0806f1c4)  [ROM_INCBIN range only; pool at 0x6f1c4 is OUTSIDE]
- DisassembleCommand(0x0806f18a)
- Expected: 29 instructions through bx r1 at 0x6f1c2; auto-creates LAB_0806f1b6 and LAB_0806f1b8
  as branch targets from other blocks. The shared epilogue is part of equip_disp_sub_f188 flow.

**Step 2: Block2c** (equip_disp_sub_f0cc body)
- clearListing(0x0806f0ce, 0x0806f184)  [ROM_INCBIN 0x6f0ce..0x6f17f + b+pad 0x6f180..0x6f183]
- DisassembleCommand(0x0806f0ce)
- Expected: 89 instructions; fail branches resolve to LAB_0806f1b6 (created by Step 1);
  success path ends: movs r0,#0x7b @ 0x6f17e + b 0x806f1b8 @ 0x6f180 + .zero 2 @ 0x6f182.
- Pool at 0x6f184 must NOT be in clearListing range (stop at 0x6f184 exclusive).
- If Ghidra emits .byte for 0x9300 (str r3,[sp,#0]) or 0x4319/431a/4643/4642/4680:
  all are valid THUMB16 opcodes. Ghidra 10 handles these; no special workaround needed.

**Step 3: Block2b** (equip_disp_sub_f0ac body)
- clearListing(0x0806f0ae, 0x0806f0c4)  [ROM_INCBIN 0x6f0ae..0x6f0bf + b+pad 0x6f0c0..0x6f0c3]
- DisassembleCommand(0x0806f0ae)
- Expected: 9 instructions + b + .zero 2; pool at 0x6f0c4..0x6f0cb NOT in clearListing range.

**Step 4: Block2a** (equip_disp_sub_f078 body)
- clearListing(0x0806f07a, 0x0806f0a0)  [ROM_INCBIN 0x6f07a..0x6f09b + b+pad 0x6f09c..0x6f09f]
- DisassembleCommand(0x0806f07a)
- Expected: 17 instructions + b + .zero 2; pool at 0x6f0a0..0x6f0ab NOT in clearListing range.

**Step 5: Block1** (eligible_creature_swap_f008 body, computed-jump stub)
- clearListing(0x0806f00a, 0x0806f032)  [Code only; stop BEFORE pad+pool at 0x6f032]
  Rationale: Do NOT clearListing past 0x6f032 to avoid wiping the pool area unnecessarily.
  The pad bytes 0x6f032..0x6f033 (0x0000) can be handled separately.
- DisassembleCommand(0x0806f00a)
- Expected: 22 instructions through mov r15,r0 @ 0x6f030. Flow stops at computed jump.
  Ghidra will NOT auto-decode 0x6f032..0x6f03b (after computed branch).
- createDWord(0x0806f034)  [creates DWORD/word unit for gDuelPhaseFlags pool]
- createDWord(0x0806f038)  [creates DWORD/word unit for equip_disp_table_f03c pool]
- The 2-byte pad at 0x6f032 (0x0000): Ghidra will emit as .byte 0x00 0x00 or .hword 0x0.
  This is acceptable; byte-identical result is guaranteed.
- Apply REF/EQ symbolization: rename DWORD at 0x6f034 -> gduel_phase_f034 with gDuelPhaseFlags ref;
  rename DWORD at 0x6f038 -> equip_disp_tbl_f038 with equip_disp_table_f03c ref.

**Step 6: Block2e** (eligible_sub_stubs_f054 body, .byte partial)
- clearListing(0x0806f056, 0x0806f066)  [.byte range; 0x6f054 entry instr already decoded]
- DisassembleCommand(0x0806f056)
- Expected: 8 instructions (adds,bl,cmp,bne,b,movs,b); branches to LAB_0806f1b6/LAB_0806f1b8.

**Step 7: Block2f** (equip_disp_sub_f066 body, .byte partial)
- clearListing(0x0806f068, 0x0806f078)  [.byte range; 0x6f066 entry instr already decoded]
- DisassembleCommand(0x0806f068)
- Expected: 7 instructions (lsls,lsrs,ldrh,adds,bl,movs,b); b to LAB_0806f1b8.

### Literal pool createDWord requirements

| addr | value | label | action |
|------|-------|-------|--------|
| 0x0806f034 | 0x0201b290 | gduel_phase_f034 | createDWord (inside B1 ROM_INCBIN range) |
| 0x0806f038 | 0x0806f03c | equip_disp_tbl_f038 | createDWord (inside B1 ROM_INCBIN range) |

All other pool DWORDs (0x6f0a0/a4/a8, 0x6f0c4/c8, 0x6f184, 0x6f1c4) are OUTSIDE the
ROM_INCBIN ranges and already have correct .word entries in the asm. No createDWord needed.

### Pool-fix risk assessment

B2c (0xb2 bytes, 89 instructions) is the largest block. It has no inline pool DWORDs
INSIDE the ROM_INCBIN range (pool at 0x6f184 is outside). All BL targets are in other
modules. Multi-pass pool fix (as needed in Seg-7/8) is not anticipated for B2c, but
if Ghidra re-merges adjacent words after clearListing, run a targeted PoolFix for 0x6f184.

B1 requires createDWord at 0x6f034 and 0x6f038. These are a two-step operation AFTER
DisassembleCommand (which stops at mov r15,r0). Risk: low (only 2 isolated DWORDs).

---

## Carve Plan (R7)

None. All 5 ROM_INCBIN blocks are THUMB CODE. No ROM data table requiring carve into rom.s.

---

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. All 5 ROM_INCBIN blocks have confirmed code references (3 via FS THUMB+1 indirectly
through the fn_eligible stub, 4 directly via dispatch table raw ptrs). No 0-ref orphan blocks.

---

## New Constants / Globals

No new constants required. The 2 pool DWORDs within B1 reference existing symbols:
- gDuelPhaseFlags (0x0201b290): already in ewram.inc, used throughout Seg-1.
- equip_disp_table_f03c (0x0806f03c): existing label from Seg-1 original pass.

---

## Consumer Evidence (R6)

| slot / addr | semantic | consumer | evidence | conf |
|-------------|---------|---------|---------|------|
| 0x6f034 = 0x0201b290 | gDuelPhaseFlags base | eligible_creature_swap_f008: ldr r0 pool@0x6f034; r0 used as base for equip phase state reads via stride | asm/09 line 1258..1260 (entry push), body @ 0x6f014-0x6f01a | high |
| 0x6f038 = 0x0806f03c | equip_disp_table_f03c ptr | eligible_creature_swap_f008: ldr r1 pool@0x6f038; adds r0,r0,r1; ldr r0,[r0,0]; mov r15,r0 -- computed dispatch | asm/09 line 1261-1267 (table .words) | high |
| B1 stub = fn_eligible for Creature Swap | eligibility check for CID=0x142a | FS handler table entry @ ROM 0x1e4094c: CID=0x142a @ +8, fn_eligible+1=0x0806f009 @ +0xc | roms/2343.gba @ 0x1e40954-0x1e40958 | high |
| B2a-d stubs | equip LP display state sub-handlers | equip_disp_table_f03c: 6-entry .word table with raw ptrs to each sub-stub; computed dispatch via MOV PC,r0 | asm/09 lines 1261-1267 | high |

---

## C13-style Post-Remediation Proof

After Ghidra DisassembleCommand steps 1-7 and createDWord for pool slots:

| Block | ROM off / size | Disposition | Post-remediation asm | ROM_INCBIN remaining |
|-------|----------------|-------------|---------------------|---------------------|
| B1    | 0x6f00a / 0x32 | DISASM | 22 instrs + .zero 2 + 2 createDWord .words | 0 |
| B2a   | 0x6f07a / 0x22 | DISASM | 17 instrs (incl. b+.zero from 0x6f09c) | 0 |
| B2b   | 0x6f0ae / 0x12 | DISASM | 9 instrs (incl. b+.zero from 0x6f0c0) | 0 |
| B2c   | 0x6f0ce / 0xb2 | DISASM | 89 instrs (incl. b+.zero from 0x6f180) | 0 |
| B2d   | 0x6f18a / 0x3a | DISASM | 29 instrs (incl. shared epilogue 0x6f1b6..0x6f1c3) | 0 |
| B2e   | .byte 0x6f056/0x10 | DISASM | 8 instrs | 0 |
| B2f   | .byte 0x6f068/0x10 | DISASM | 7 instrs | 0 |

Zero ROM_INCBIN blocks remaining for these 7 items after remediation.
The 3 `.word` pseudo-entries at 0x6f09c/0x6f0c0/0x6f180 that represent b+pad are
replaced by proper THUMB `b` + `.zero 2` (byte-identical transformation).
Build byte-identical check: SHA1 must remain 9689337d6aac1ce9699ab60aac73fc2cfdccad9b.

---

## Clarification Requests

None. All block classifications are high-confidence (code-address dispatch table refs + FS table THUMB+1 for B1).

---

## Self-check

1. All 5 ROM_INCBIN block-start addresses scanned: raw=0, THUMB+1=0 (mid-body, expected).
2. All 5 stub ENTRY addresses verified in dispatch table or FS handler table with file:ROM offset evidence.
3. B1 CID=0x142a confirmed against data/card-stats.s (card_0910 pw=31036355 = Creature Swap). conf:high.
4. Literal pool addresses computed via PC-relative formula and verified against ROM bytes.
5. All branch targets computed and verified: fail paths -> 0x0806f1b6, success paths -> 0x0806f1b8.
6. BL targets verified: set_lp_display_row_type9(0x080a1cb4), dispatch_card_effect_activation(0x08090848),
   query_slot_card_type_eligibility(0x0803670c), check_slot_equip_whitelist_with_monster_space(0x08036450),
   enqueue_sprite_attr_with_mode(0x08043054), enqueue_equip_chain_dual_slot_sprite_with_activation_scan(0x08043f44),
   set_field_slot_bit_with_sprite_update(0x0804a970). All confirmed in naming-proposals.csv.
7. No CJK in any plate/EOL text.
8. Section 5.1 has 0 entries: all blocks confirmed referenced.
9. No new constants required: existing ewram.inc (gDuelPhaseFlags) + existing asm label (equip_disp_table_f03c).
10. Pool DWORDs at 0x6f0a0/0x6f0a4/0x6f0a8 (B2a), 0x6f0c4/0x6f0c8 (B2b), 0x6f184 (B2c), 0x6f1c4 (B2d)
    are all OUTSIDE their respective ROM_INCBIN ranges; no createDWord needed for those.
11. b+pad .words at 0x6f09c/0x6f0c0/0x6f180 verified byte-identical: .word 0x0000e08c emits [8c e0 00 00]
    = ROM bytes [8c e0 00 00]; .word 0x0000e07a -> [7a e0 00 00] matches; .word 0x0000e01a -> [1a e0 00 00] matches.

---

## Executor Report: F09-Seg1R

- Slots: EQ=2 (NEW: gduel_phase_f034, equip_disp_tbl_f038) REF=2 RENAME=0 FUNC_RENAME=0 PLATE=0
- carve=0 disasm=7 items (5 ROM_INCBIN blocks + 2 companion .byte blocks)
  - B1: eligible_creature_swap_f008 body 0x6f00a/0x32 -> DISASM + 2 createDWord
  - B2a: equip_disp_sub_f078 body 0x6f07a/0x22 + b+pad -> DISASM
  - B2b: equip_disp_sub_f0ac body 0x6f0ae/0x12 + b+pad -> DISASM
  - B2c: equip_disp_sub_f0cc body 0x6f0ce/0xb2 + b+pad -> DISASM
  - B2d: equip_disp_sub_f188 body 0x6f18a/0x3a -> DISASM (incl. shared epilogue)
  - B2e: eligible_sub_stubs_f054 body 0x6f056/0x10 .byte -> DISASM
  - B2f: equip_disp_sub_f066 body 0x6f068/0x10 .byte -> DISASM
- §5.1=0 (all 5 ROM_INCBIN blocks confirmed referenced)
- New constants/globals: none (all pool refs use existing gDuelPhaseFlags + equip_disp_table_f03c label)
- Seek-help: none
- Expected post-remediation ROM_INCBIN count for these 5 blocks: 0
- proposal: doc/dev/refine/F09-Seg1R.proposal.md
