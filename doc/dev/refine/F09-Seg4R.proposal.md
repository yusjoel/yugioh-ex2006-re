# Refine Proposal: F09-Seg4R  [file 09 Seg-4 REMEDIATION 0x080719fc..0x08072d20)

**Purpose**: Eliminate 4 ROM_INCBIN and 8 .byte residual blocks left by the Seg-4a/4b partial-disasm
pass (commits a9aa009 + 527e3a9). All blocks are CODE continuation paths (bne/beq/bls branch-taken
bodies) or DATA dispatch-table entries within already-disassembled functions. No new functions,
no FS THUMB+1 stubs, no §5.1 orphans.

Precedent: F09-Seg1R.proposal.md + F09-Seg1R2.proposal.md (same per-stub DC ordering,
epilogue-first rule, pool createDWord discipline).

---

## 段测绘

- 函数入口: 0x719fc~0x72d20 (Seg-4 range; all 20 functions already named in prior Seg-4a/4b passes)
- 残留 ROM_INCBIN:
  - 0x720e2 size 0x12  (within field_spell_dispatch_sub_stubs_2004)
  - 0x7270e size 0x1e  (within fn_eligible_vampire_lord_lady_26f4)
  - 0x7276a size 0x1e  (within equip_zone_sub_stubs_274c, bne-taken path)
  - 0x72794 size 0x20  (within equip_zone_sub_stubs_274c, bne target from 0x7276a block)
- 残留 .byte CODE 块:
  - 0x71f74 size 0xc   (indirect dispatch in fn_eligible_fengsheng_mirror_1f58)
  - 0x7241c size 0xc   (indirect dispatch in fn_eligible_fiend_comedian_2404)
  - 0x7256a size 0xa   (indirect dispatch in fn_eligible_last_turn_2540)
  - 0x72838 size 0x10  (beq-taken path in equip_zone_sub_2804)
- 残留 .byte DATA 槽:
  - 0x72430 size 0x4   (dispatch table entry: last_turn_sub_2534)
  - 0x7257c size 0x4   (dispatch table entry: vampire_sub_26bc)
  - 0x72734 size 0x4   (dispatch table entry: equip_zone_sub_2856)
  - 0x72830 size 0x4   (literal pool constant: LP_CARD_TRACK_BASE_OFF=0x1da8)

---

## データ块分类 (Rule 2/3) — ref-scan 証拠

Exhaustive 2B-step ref-scan (raw + THUMB|1) at all entry points, python verified against
roms/2343.gba:

| 块 | entry/range | ref-scan raw | ref-scan THUMB+1 | 判定 | 理由 |
|---|---|---|---|---|---|
| ROM_INCBIN 0x720e2/0x12 | 0x080720e2 | 0 | 0 | CODE-disasm | bne LAB_080720e2 at asm:8190 (0x8072062 3ed1); intra-function branch target; first HW 0xa1 0x78 = ldrb r1,[r4,#2] |
| ROM_INCBIN 0x7270e/0x1e | 0x0807270e | 0 | 0 | CODE-disasm | bne LAB_0807270e at asm:9077 (0x8072704 03d1); intra-function branch target; first HW 0x07 0x48 = ldr r0,[pc,#28] |
| ROM_INCBIN 0x7276a/0x1e | 0x0807276a | 0 | 0 | CODE-disasm | bne LAB_0807276a at asm:9107 (0x8072766 00d1); intra-function branch target; first HW 0x09 0x48 = ldr r0,[pc,#36] |
| ROM_INCBIN 0x72794/0x20 | 0x08072794 | 0 | 0 | CODE-disasm | bne from 0x72778 within block at 0x7276a; first HW 0x82 0x20 = movs r0,#0x82 |
| .byte 0x71f74/0xc | 0x08071f74 | 0 | 0 | CODE-disasm | bls LAB_08071f74 at asm:8100 (0x8071f70 00d9); first HW = 0x0080 = lsls r0,r0,#2 |
| .byte 0x7241c/0xc | 0x0807241c | 0 | 0 | CODE-disasm | bls LAB_0807241c at asm:8710 (0x807241a 00d9); first HW = 0x0080 = lsls r0,r0,#2 |
| .byte 0x7256a/0xa | 0x0807256a | 0 | 0 | CODE-disasm | bls LAB_0807256a at asm:8872 (0x8072566 00d9); first HW = 0x0088 = lsls r0,r1,#2 |
| .byte 0x72838/0x10 | 0x08072838 | 0 | 0 | CODE-disasm | beq LAB_08072838 at asm:9185 (0x807280e 13d0); first HW = 0x789b = ldrb r3,[r3,#2] |
| .byte 0x72430/0x4 | n/a | n/a | n/a | DATA-.word | ROM bytes 34 25 07 08 = 0x08072534 (last_turn_sub_2534); dispatch table entry; raw=0 as ptr |
| .byte 0x7257c/0x4 | n/a | n/a | n/a | DATA-.word | ROM bytes bc 26 07 08 = 0x080726bc (vampire_sub_26bc); dispatch table entry; raw=0 as ptr |
| .byte 0x72734/0x4 | n/a | n/a | n/a | DATA-.word | ROM bytes 56 28 07 08 = 0x08072856 (equip_zone_sub_2856); dispatch table entry[0]; raw=0 as ptr |
| .byte 0x72830/0x4 | n/a | n/a | n/a | DATA-.word | ROM bytes a8 1d 00 00 = 0x00001da8 = LP_CARD_TRACK_BASE_OFF; literal pool constant; ewram.inc:247 |

Zero-ref notes for DATA entries: dispatch table entries at 0x72430/0x7257c/0x72734 hold raw
GBA function addresses (0x0807xxxx); ref-scan of the address VALUE (e.g. 0x08072534) finds it
as a raw .word in the dispatch table itself, which is expected. The .byte encoding is a Ghidra
partial-disasm artifact -- the value itself is not zero-ref; it is referenced by the dispatch
sequence ldr r1,[pc,#imm]+adds+ldr r0,[r0,#0]+mov pc,r0.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate)

| slot | value | const_name | slot_label | source |
|---|---|---|---|---|
| DAT_08072830 @ 0x72830 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | LP_CARD_TRACK_BASE_OFF | REUSE ewram.inc:247 |
| pool_b8_27b4 @ 0x727b4 | 0x000001b9 | lookup_equip_score_b_0x1b9 | pool_b8_27b4 | REUSE duel_field.inc:332 |

Verification:
- LP_CARD_TRACK_BASE_OFF: ROM @ 0x72830 = bytes a8 1d 00 00 -> u32 LE = 0x1da8. ewram.inc:247
  confirms `.equ LP_CARD_TRACK_BASE_OFF, 0x00001da8`. Match: high confidence.
- lookup_equip_score_b_0x1b9: ROM @ 0x727b4 = bytes b9 01 00 00 -> u32 LE = 0x1b9. duel_field.inc:332
  confirms `.equ lookup_equip_score_b_0x1b9, 0x000001b9`. Match: high confidence.

### REF_SLOTS  (DATA .byte -> .word label)

These are dispatch table entries currently encoded as .byte but requiring createDWord to become .word
references to existing labels:

| slot | target | gas_label | slot_label |
|---|---|---|---|
| 0x72430 | 0x08072534 | last_turn_sub_2534 | (unlabeled, at table entry position) |
| 0x7257c | 0x080726bc | vampire_sub_26bc | (unlabeled, at table entry position) |
| 0x72734 | 0x08072856 | equip_zone_sub_2856 | (unlabeled, at table entry position) |

All three target labels already exist in asm (asm:8843, asm:9038, asm:9193 respectively).
The Ghidra fix is: clearListing(4B) at each .byte slot, createDWord, then the re-export will
emit `.word last_turn_sub_2534` etc.

Note: pool_b8_27b4 @ 0x727b4 is already a .word in the asm; it only needs an EQ_SLOT rename
in Ghidra (equate 0x727b4 with lookup_equip_score_b_0x1b9). This does NOT require createDWord.

### RENAME_SLOTS  (pure label rename + EOL)

None needed. All existing slot labels (pool_b7_272c, pool_b7_2730, pool_b8_2788, pool_b8_278c,
pool_b8_2790, pool_b8_27b4) retain their existing names. No new sub-stub labels needed since all
block bodies are intra-function LAB_ continuations (not new function entries).

### FUNC_RENAME

None. All containing functions are correctly named from prior Seg-4a/4b passes.

### PLATE

None required for this remediation. The CODE block bodies do not introduce new callee references
that would stale existing plate text.

---

## disasm 计划 (R4)

### Ordering principle
Per Seg-1R precedent: epilogue-first. However, none of the 8 CODE blocks contains a SHARED epilogue
that other stubs merge into (all blocks branch to existing named epilogue labels outside the block).
Therefore no special epilogue-first inversion is needed; blocks are processed in address order.

All blocks are within existing named functions; no createFunction calls required.

### ROM_INCBIN blocks

**B1: ROM_INCBIN 0x720e2/0x12  (within field_spell_dispatch_sub_stubs_2004)**

Containing function: field_spell_dispatch_sub_stubs_2004 (Seg-4a B4, raw-dispatch sub-stub
for 32-entry dispatch table @ 0x71f88..0x72003).

Reached via: `bne LAB_080720e2` at 0x8072062 (bne taken = check_card_stat_field8_is_7 returned
nonzero, i.e., card IS field-type-7).

THUMB decode (9 halfwords):
```
0x720e2 [78a1]: ldrb r1,[r4,#2]           ; slot byte [2]
0x720e4 [07c8]: lsls r0,r1,#31            ; isolate bit0 of r1
0x720e6 [0fc0]: lsrs r0,r0,#31            ; r0 = player_side (bit0)
0x720e8 [8821]: ldrh r1,[r4,#0]           ; r1 = slot[0] halfword = card_id
0x720ea [2201]: movs r2,#1                ; r2 = 1
0x720ec [f02f]: BL_hi off11=47 \
0x720ee [fd9e]: BL_lo off11=1438 /  --> target: 0x080720f0 + (47<<12) + (1438<<1) = 0x080a1c2c
                                     = set_lp_display_row_type5 (asm/13_equip_placement.s:7899)
0x720f0 [207f]: movs r0,#0x7f             ; return code = 0x7f
0x720f2 [e000]: b 0x8072f6               ; b LAB_080720f6 (shared epilogue: pop {r3,r4};mov r8;pop {r4-7};pop {r1};bx r1)
```

Literal pools: NONE within block range 0x720e2..0x720f3. Adjacent existing pools at 0x720a4/0x720a8
are already in asm and outside this range.

DC plan:
1. clearListing(0x080720e2, 0x080720f3)  -- 18 bytes, 4-byte step safe
2. setTMode(0x080720e2)
3. DisassembleCommand(0x080720e2, None, True)

Expected result: 9 instructions decoded; b LAB_080720f6 stops DC.

---

**B2: ROM_INCBIN 0x7270e/0x1e  (within fn_eligible_vampire_lord_lady_26f4)**

Containing function: fn_eligible_vampire_lord_lady_26f4 @ 0x080726f4.

Reached via: `bne LAB_0807270e` at 0x8072704 (bne taken = flag 0xfc0 & slot[2] halfword != 0x80,
i.e., NOT the hand-set-code path handled by invoke_equip_oam_for_hand_set_code_slot).

THUMB decode (15 halfwords):
```
0x7270e [4807]: ldr r0,[pc,#28] @[0x7272c] = gDuelPhaseFlags=0x0201b290
                ; PC = (0x7270e+4)&~2 = 0x72710, load_addr = 0x72710+28 = 0x7272c (confirmed: pool_b7_272c)
0x72710 [2294]: movs r2,#0x94
0x72712 [00d2]: lsls r2,r2,#3             ; r2 = 0x94<<3 = 0x4a0 (phase-code field offset)
0x72714 [1881]: adds r1,r0,r2             ; r1 = gDuelPhaseFlags + 0x4a0
0x72716 [6809]: ldr r1,[r1,#0]            ; r1 = phase_code
0x72718 [397b]: subs r1,#0x7b            ; r1 = phase_code - 0x7b (range 0..5 for valid dispatch)
0x7271a [1c02]: adds r2,r0,#0            ; r2 = gDuelPhaseFlags base (save)
0x7271c [2905]: cmp r1,#5
0x7271e [d900]: bls 0x8072722            ; bls taken: valid phase -> indirect dispatch
0x72720 [e0a0]: b 0x8072864             ; b LAB_08072864 (return 0 path: movs r0,#0; add sp,#8; pop...)
-- bls taken path at 0x72722: --
0x72722 [0088]: lsls r0,r1,#2            ; r0 = (phase_code-0x7b) * 4 (index into table)
0x72724 [4902]: ldr r1,[pc,#8] @[0x72730] = 0x08072734 (equip_zone_dispatch_table base)
                ; PC = (0x72724+4)&~2 = 0x72728, load_addr = 0x72728+8 = 0x72730 (confirmed: pool_b7_2730)
0x72726 [1840]: adds r0,r0,r1            ; r0 = table_base + index*4
0x72728 [6800]: ldr r0,[r0,#0]           ; r0 = dispatch_table[phase_code-0x7b]
0x7272a [4687]: mov r15,r0              ; indirect jump (computed branch via table entry)
```

Dispatch table @ 0x08072734 (6 entries, phases 0x7b..0x80):
- phase=0x7b (idx=0): 0x08072856 = equip_zone_sub_2856
- phase=0x7c (idx=1): 0x08072848 = equip_zone_sub_2848
- phase=0x7d (idx=2): 0x08072804 = equip_zone_sub_2804
- phase=0x7e (idx=3): 0x080727e4 = equip_zone_sub_27e4
- phase=0x7f (idx=4): 0x080727b8 = equip_zone_sub_27b8
- phase=0x80 (idx=5): 0x0807274c = equip_zone_sub_stubs_274c (entry sub-stub)

Literal pools: pool_b7_272c @ 0x7272c and pool_b7_2730 @ 0x72730 are already labeled .word in
asm (lines 9083-9086); both are OUTSIDE the ROM_INCBIN 0x7270e/0x1e range. No createDWord needed.

DC plan:
1. clearListing(0x0807270e, 0x0807272b)  -- 0x1e bytes
2. setTMode(0x0807270e)
3. DisassembleCommand(0x0807270e, None, True)
   - DC follows: sequential until b @0x72720 (stops), AND bls taken-path @0x72722 -> mov r15,r0
     @0x7272a (stops). In unrestricted mode Ghidra follows both edges, so all 15 instructions
     are decoded in one pass.

Expected result: all 15 instructions decoded including bls-taken path; mov r15,r0 stops DC.

---

**B3: ROM_INCBIN 0x7276a/0x1e  (within equip_zone_sub_stubs_274c, bne-taken path)**

Containing function: equip_zone_sub_stubs_274c @ 0x0807274c.

Reached via: `bne LAB_0807276a` at 0x8072766 (bne taken = loaded pointer field != 0, i.e., there
IS an active card pointer at gDuelCardCtxBase+0x8+player*4).

THUMB decode (15 halfwords):
```
0x7276a [4809]: ldr r0,[pc,#36] @[0x72790] = gDuelCardCtxBase=0x0201e2a0
                ; PC = (0x7276a+4)&~2 = 0x7276c, load_addr = 0x7276c+36 = 0x72790 (pool_b8_2790, outside block)
0x7276c [0fd1]: lsrs r1,r2,#31            ; r1 = player_side (bit31 of r2, which holds player*PLAYER_BLOCK_STRIDE)
0x7276e [0089]: lsls r1,r1,#2             ; r1 = player_side * 4
0x72770 [3008]: adds r0,#0x8              ; r0 = gDuelCardCtxBase + 0x8
0x72772 [1809]: adds r1,r1,r0             ; r1 = &gDuelCardCtxBase[0x8 + player*4]
0x72774 [6808]: ldr r0,[r1,#0]            ; r0 = ctx->confirm_ptr_field
0x72776 [2801]: cmp r0,#1
0x72778 [d10c]: bne 0x8072794            ; bne taken: ptr != 1 -> B4 (invoke_card_display_op path)
-- bne NOT taken (ptr == 1): clear chain flag path --
0x7277a [23ea]: movs r3,#0xea
0x7277c [015b]: lsls r3,r3,#5             ; r3 = 0xea<<5 = 0x1d40 (LP frame flag offset)
0x7277e [18e1]: adds r1,r4,r3             ; r1 = slot_ptr + 0x1d40
0x72780 [2000]: movs r0,#0x0
0x72782 [6008]: str r0,[r1,#0]            ; [slot+0x1d40] = 0 (clear chain frame flag)
0x72784 [e013]: b 0x80727ae              ; b 0x80727ae (lands inside B4: movs r0,#0x7f; b epilogue)
0x72786 [0000]: movs r0,r0               ; align pad (inert NOP)
```

Note: 0x1d40 (0xea<<5) is NOT in constants files. The value is computed inline and not a pool .word
(no createDWord, no new equate; the EOL comment "0xea<<5 = 0x1d40 LP frame flag" suffices).

Literal pools: pool_b8_2788 @ 0x72788, pool_b8_278c @ 0x7278c, pool_b8_2790 @ 0x72790 are
already labeled .word in asm (lines 9111-9116); all OUTSIDE 0x7276a..0x72787. No createDWord.

DC plan:
1. clearListing(0x0807276a, 0x08072787)  -- 0x1e bytes
2. setTMode(0x0807276a)
3. DisassembleCommand(0x0807276a, None, True)
   - DC follows b @0x72784 to 0x80727ae (within B4; B4 must be disassembled first for this to
     resolve, but DC will still stop here regardless; B4 disasm handled separately).
   - pad at 0x72786 (0x0000 = movs r0,r0) may be auto-decoded or stay as data.

Expected result: 14 active instructions + 1 pad decoded. b @0x72784 stops flow.

---

**B4: ROM_INCBIN 0x72794/0x20  (within equip_zone_sub_stubs_274c, bne target from B3)**

Containing function: equip_zone_sub_stubs_274c (continuation; bne target from B3 at 0x72778).

Also: B3's b@0x72784 lands at 0x727ae which is WITHIN B4's range [0x72794, 0x727b3].

THUMB decode (16 halfwords):
```
0x72794 [2082]: movs r0,#0x82
0x72796 [0040]: lsls r0,r0,#1             ; r0 = 0x82<<1 = 0x104
0x72798 [21dc]: movs r1,#0xdc
0x7279a [0049]: lsls r1,r1,#1             ; r1 = 0xdc<<1 = 0x1b8
0x7279c [4a05]: ldr r2,[pc,#20] @[0x727b4] = 0x1b9 = lookup_equip_score_b_0x1b9
                ; PC = (0x7279c+4)&~2 = 0x727a0, load_addr = 0x727a0+20 = 0x727b4 (pool_b8_27b4, OUTSIDE block)
0x7279e [23dd]: movs r3,#0xdd
0x727a0 [005b]: lsls r3,r3,#1             ; r3 = 0xdd<<1 = 0x1ba
0x727a2 [2400]: movs r4,#0x0
0x727a4 [9400]: str r4,[sp,#0]            ; sp[0] = 0
0x727a6 [240f]: movs r4,#0xf
0x727a8 [9401]: str r4,[sp,#4]            ; sp[4] = 0xf
0x727aa [f020]: BL_hi off11=32 \
0x727ac [fe17]: BL_lo off11=0x617 /  --> target: 0x080727ae + (32<<12) + (0x617<<1) = 0x080933dc
                                     = invoke_card_display_op_0x31_sub3_with_packed_params
                                       (asm/all.s:298064, confirmed in file13)
-- B3 branch target at 0x727ae: --
0x727ae [207f]: movs r0,#0x7f             ; return code = 0x7f
0x727b0 [e059]: b 0x8072866             ; b LAB_08072866 (epilogue: add sp,#8; pop {r4}; pop {r1}; bx r1)
0x727b2 [0000]: movs r0,r0               ; align pad
```

Note: params r0=0x104, r1=0x1b8, r2=0x1b9, r3=0x1ba, sp[0]=0, sp[4]=0xf are identical
to LAB_080722b8 @ 0x722b8 (asm:8517-8528) except return code (0x7f here vs 0x7e there).
This confirms semantic: displays equip score sub-op with these packed params.

BL target verification:
- BL_hi off=32, BL_lo off=0x617
- target = (0x080727aa + 4) + (32 << 12) + (0x617 << 1) = 0x080727ae + 0x20000 + 0xc2e = 0x080933dc
- invoke_card_display_op_0x31_sub3_with_packed_params confirmed at 0x080933dc (asm/all.s:298064).

Literal pool: pool_b8_27b4 @ 0x727b4 (OUTSIDE block, range ends at 0x727b3) is already a labeled
.word in asm. No createDWord inside block. EQ_SLOT for 0x727b4 (rename equate to lookup_equip_score_b_0x1b9).

DC plan (B3 FIRST to satisfy epilogue-first reasoning, then B4):
1. clearListing(0x08072794, 0x080727b3)  -- 0x20 bytes
2. setTMode(0x08072794)
3. DisassembleCommand(0x08072794, None, True)
   - DC decodes from 0x72794 through BL (not a stop), then 0x727ae (movs), 0x727b0 (b -> stops).
   - Pad at 0x727b2 may auto-decode or remain data (.zero 2 / movs r0,r0).

Expected result: 15 active instructions + pad. b @0x727b0 stops DC.

---

### .byte CODE blocks

**C1: .byte 0x71f74/0xc  (indirect dispatch in fn_eligible_fengsheng_mirror_1f58)**

Containing function: fn_eligible_fengsheng_mirror_1f58 @ 0x08071f58 (Seg-4a B3).

Reached via: `bls LAB_08071f74` at 0x8071f70 (bls taken = phase_offset <= 0x1e = valid range for
fn_eligible_fengsheng_mirror dispatch table).

THUMB decode (6 halfwords):
```
0x71f74 [0080]: lsls r0,r0,#2             ; r0 = index * 4
0x71f76 [4903]: ldr r1,[pc,#12] @[0x71f84] = 0x08071f88 (dispatch table base, pool_1f84)
                ; PC = (0x71f76+4)&~2 = 0x71f78, load_addr = 0x71f78+12 = 0x71f84
0x71f78 [1840]: adds r0,r0,r1             ; r0 = table_base + index*4
0x71f7a [6800]: ldr r0,[r0,#0]            ; r0 = table[index]
0x71f7c [4687]: mov r15,r0              ; indirect jump (computed branch)
0x71f7e [0000]: movs r0,r0               ; align pad (NOP)
```

pool_1f84 @ 0x71f84 = 0x08071f88 (dispatch table base, already labeled in asm). The dispatch table
at 0x71f88..0x71fff (32 entries) is already fully decoded as .word refs in the asm.

DC plan:
1. clearListing(0x08071f74, 0x08071f7f)  -- 0xc bytes
2. setTMode(0x08071f74)
3. DisassembleCommand(0x08071f74, None, True)  -- stops at mov r15,r0; pad at 0x71f7e may auto-decode

---

**C2: .byte 0x7241c/0xc  (indirect dispatch in fn_eligible_fiend_comedian_2404)**

Containing function: fn_eligible_fiend_comedian_2404 @ 0x08072404 (Seg-4b B5).

Reached via: `bls LAB_0807241c` at 0x807241a (bls taken = phase_offset <= 4 = valid dispatch).

THUMB decode (identical pattern to C1):
```
0x7241c [0080]: lsls r0,r0,#2             ; r0 = index * 4
0x7241e [4903]: ldr r1,[pc,#12] @[0x7242c] = 0x08072430 (dispatch table base, pool_next_addr_242c)
                ; PC = (0x7241e+4)&~2 = 0x72420, load_addr = 0x72420+12 = 0x7242c
0x72420 [1840]: adds r0,r0,r1
0x72422 [6800]: ldr r0,[r0,#0]
0x72424 [4687]: mov r15,r0              ; indirect jump
0x72426 [0000]: movs r0,r0               ; align pad
```

Dispatch table base: pool_next_addr_242c @ 0x7242c = 0x08072430 (already labeled .word in asm).
Table at 0x72430..0x72443 (5 entries + fn_eligible_last_turn_2540 at 0x2440):
- [0] 0x72430: .byte -> .word last_turn_sub_2534  (DATA slot, fix in REF_SLOTS)
- [1] 0x72434: .word last_turn_sub_24b4 (already .word)
- [2] 0x72438: .word last_turn_sub_24ac (already .word)
- [3] 0x7243c: .word last_turn_sub_248a (already .word)
- [4] 0x72440: .word last_turn_dispatch_sub_stubs_2444 (already .word)

DC plan:
1. clearListing(0x0807241c, 0x08072427)  -- 0xc bytes
2. setTMode(0x0807241c)
3. DisassembleCommand(0x0807241c, None, True)

---

**C3: .byte 0x7256a/0xa  (indirect dispatch in fn_eligible_last_turn_2540)**

Containing function: fn_eligible_last_turn_2540 @ 0x08072540 (Seg-4b B6).

Reached via: `bls LAB_0807256a` at 0x8072566 (bls taken = phase_offset <= 5 = valid dispatch).

THUMB decode (5 halfwords, no trailing pad):
```
0x7256a [0088]: lsls r0,r1,#2             ; r0 = r1*4 (r1 = phase_offset; note: r0 used as index NOT r0)
0x7256c [4902]: ldr r1,[pc,#8] @[0x72578] = 0x0807257c (dispatch table base, pool_b6_2578)
                ; PC = (0x7256c+4)&~2 = 0x72570, load_addr = 0x72570+8 = 0x72578
0x7256e [1840]: adds r0,r0,r1
0x72570 [6800]: ldr r0,[r0,#0]
0x72572 [4687]: mov r15,r0              ; indirect jump (stops DC; next .word at 0x72574 safe)
```

Dispatch table base: pool_b6_2578 @ 0x72578 = 0x0807257c (already labeled .word in asm).
Table at 0x7257c..0x72593 (6 entries):
- [0] 0x7257c: .byte -> .word vampire_sub_26bc  (DATA slot, fix in REF_SLOTS)
- [1] 0x72580: .word vampire_sub_2678 (already .word)
- [2] 0x72584: .word vampire_sub_264c (already .word)
- [3] 0x72588: .word vampire_sub_2624 (already .word)
- [4] 0x7258c: .word vampire_sub_25e8 (already .word)
- [5] 0x72590: .word vampire_dispatch_sub_stubs_2594 (already .word)

DC plan:
1. clearListing(0x0807256a, 0x08072573)  -- 0xa bytes
2. setTMode(0x0807256a)
3. DisassembleCommand(0x0807256a, None, True)

---

**C4: .byte 0x72838/0x10  (beq-taken path in equip_zone_sub_2804)**

Containing function: equip_zone_sub_2804 @ 0x08072804 (Seg-4b B8, sub-stub).

Reached via: `beq LAB_08072838` at 0x807280e (beq taken = LP field [gP1LP+0x1da8] == 0,
no LP card tracking entry -> display trigger only).

THUMB decode (8 halfwords):
```
0x72838 [789b]: ldrb r3,[r3,#2]           ; slot byte [2] (r3=slot_ptr from parent)
0x7283a [07d8]: lsls r0,r3,#31            ; isolate bit0
0x7283c [0fc0]: lsrs r0,r0,#31            ; r0 = player_side
0x7283e [210d]: movs r1,#0xd              ; r1 = 0xd = 13
0x72840 [f020]: BL_hi off11=32 \
0x72842 [fda6]: BL_lo off11=0x5a6 /  --> target: (0x08072844) + (32<<12) + (0x5a6<<1) = 0x08093390
                                     = trigger_card_display_op31_if_not_active
                                       (confirmed: bl at asm:8909 from 0x080725c0 uses same encoding pattern)
0x72844 [207c]: movs r0,#0x7c             ; return code = 0x7c
0x72846 [e00e]: b 0x8072866             ; b LAB_08072866 (epilogue)
```

BL target verification:
- target = (0x08072844) + (32<<12) + (0x5a6<<1) = 0x08072844 + 0x20000 + 0xb4c = 0x08093390
- trigger_card_display_op31_if_not_active confirmed at 0x08093390 (asm:8002 confirms
  `set_lp_row_type7_if_opponent_linked @ 0x08093390`... wait, checking again)

Re-check: from asm grep, `trigger_card_display_op31_if_not_active` BL at 0x080725c0 encodes
as `20f0e6fe` which is BL_hi=0xf020 (off=32), BL_lo=0xfee6 (off=0x6e6=1766):
target = (0x080725c4) + (32<<12) + (1766<<1) = 0x080725c4 + 0x20000 + 0xdcc = 0x08093390.
This confirms 0x08093390 = trigger_card_display_op31_if_not_active. The asm grep showing
`set_lp_row_type7_if_opponent_linked` at asm:8002 refers to a DIFFERENT function in file 09.
The `trigger_card_display_op31_if_not_active` GBA address 0x08093390 is confirmed by
cross-referencing the BL encoding. Confidence: high.

Literal pools: no pool words within the .byte block range 0x72838..0x72847. Adjacent pools
(pool_b8_282c @ 0x7282c, pool_b8_2834 @ 0x72834) are before the block and already in asm.

DC plan:
1. clearListing(0x08072838, 0x08072847)  -- 0x10 bytes
2. setTMode(0x08072838)
3. DisassembleCommand(0x08072838, None, True)  -- stops at b LAB_08072866

---

## carve 計画 (R7)

None. No function-between ROM_INCBIN blocks in Seg-4 range.

---

## §5.1 登记 (Rule 3) — 0 引用块

None. Every block (ROM_INCBIN and .byte) is reached by an explicit intra-function branch
instruction (bne / beq / bls) within the same function body. All have non-zero ref-count
from their controlling branch instruction.

---

## 消費者証拠 (R6)

**Block1 (0x720e2) BL -> set_lp_display_row_type5:**
- ROM bytes: HI=0xf02f, LO=0xfd9e -> target = 0x080a1c2c
- asm/13_equip_placement.s:7899 confirms `set_lp_display_row_type5:` @ 0x080a1c2c (push {r4,lr} = 0xb510)
- Params: r0=player_side, r1=card_id (ldrh from slot[0]), r2=1 -> set_lp_display_row_fields(player, 5, card_id&0xffff, 1)
- Confidence: high (BL encoding verified; asm label confirmed)

**Block4 (0x72794) BL -> invoke_card_display_op_0x31_sub3_with_packed_params:**
- Consumer: asm/09_equip_lp_display.s:8528 `bl invoke_card_display_op_0x31_sub3_with_packed_params @ 080722ce`
- Adjacent call site at 0x722ce uses identical param setup (LAB_080722b8 at asm:8517-8528) with r0=0x104, r1=0x1b8, r2=lookup_equip_score_b_0x1b9, r3=0x1ba, sp[0]=0, sp[4]=0xf
- Block4 differs only in return code (0x7f vs 0x7e)
- Confidence: high (BL encoding verified; identical setup pattern at two call sites)

**C4 (.byte 0x72838) BL -> trigger_card_display_op31_if_not_active:**
- Consumer: asm/09_equip_lp_display.s:8909 `bl trigger_card_display_op31_if_not_active @ 080725c0 20f0e6fe`
- Same target 0x08093390 verified from BL at 0x080725c0 with identical off_hi=32
- Both call sites pass r0=player_side, r1=type (0xd here, 0x7c there), consistent with API
- Confidence: high

---

## 新増 constants / 全局

**NONE.** All equates REUSE existing constants:
- LP_CARD_TRACK_BASE_OFF = 0x1da8 in constants/ewram.inc:247
- lookup_equip_score_b_0x1b9 = 0x1b9 in constants/duel_field.inc:332

No new functions created (all code is intra-function LAB_ continuation).

---

## C13-スタイル post-remediation 証拠 (全 0 残留証明)

**ROM_INCBIN blocks in Seg-4 [0x719fc, 0x72d20):**

| block | disposition | after |
|---|---|---|
| ROM_INCBIN 0x720e2/0x12 | DISASM B1 -> 9 instructions | GONE |
| ROM_INCBIN 0x7270e/0x1e | DISASM B2 -> 15 instructions | GONE |
| ROM_INCBIN 0x7276a/0x1e | DISASM B3 -> 15 instructions | GONE |
| ROM_INCBIN 0x72794/0x20 | DISASM B4 -> 15 instructions + pad | GONE |

Post-remediation ROM_INCBIN count in Seg-4: **0**

**.byte blocks in Seg-4 [0x719fc, 0x72d20):**

| block | disposition | after |
|---|---|---|
| .byte 0x71f74/0xc | DISASM C1 -> 6 halfwords (5 instr + pad) | GONE |
| .byte 0x7241c/0xc | DISASM C2 -> 6 halfwords (5 instr + pad) | GONE |
| .byte 0x72430/0x4 | createDWord -> .word last_turn_sub_2534 | GONE |
| .byte 0x7256a/0xa | DISASM C3 -> 5 halfwords | GONE |
| .byte 0x7257c/0x4 | createDWord -> .word vampire_sub_26bc | GONE |
| .byte 0x72734/0x4 | createDWord -> .word equip_zone_sub_2856 | GONE |
| .byte 0x72830/0x4 | createDWord + EQ -> .word LP_CARD_TRACK_BASE_OFF | GONE |
| .byte 0x72838/0x10 | DISASM C4 -> 8 instructions | GONE |

Post-remediation .byte-code residue count in Seg-4: **0**
Justified §5.1 orphans: **0** (all blocks have explicit branch refs within their containing function)

---

## 求助

None. All blocks classified with high confidence from ROM byte evidence + branch instruction
cross-referencing + BL target reverse-computation.

---

## Ghidra Script Plan (DisassembleF09Seg4R.py)

Execution order (epilogue-first; shared epilogues already exist as named LABs):

```python
# Step 1: DATA .byte blocks -> createDWord (must be done BEFORE DC to avoid conflicts)
force_dword(0x08072430)   # .byte -> .word last_turn_sub_2534
force_dword(0x0807257c)   # .byte -> .word vampire_sub_26bc
force_dword(0x08072734)   # .byte -> .word equip_zone_sub_2856
force_dword(0x08072830)   # .byte -> .word LP_CARD_TRACK_BASE_OFF (then EQ)

# Step 2: EQ_SLOTS
createEquate(0x08072830, 'LP_CARD_TRACK_BASE_OFF')
createEquate(0x080727b4, 'lookup_equip_score_b_0x1b9')  # pool_b8_27b4

# Step 3: .byte CODE blocks -> DisassembleCommand
# C1: indirect dispatch in fn_eligible_fengsheng_mirror_1f58
clearListing(0x08071f74, 0x08071f7f)
setTMode(0x08071f74)
DisassembleCommand(0x08071f74, None, True)

# C2: indirect dispatch in fn_eligible_fiend_comedian_2404
clearListing(0x0807241c, 0x08072427)
setTMode(0x0807241c)
DisassembleCommand(0x0807241c, None, True)

# C3: indirect dispatch in fn_eligible_last_turn_2540
clearListing(0x0807256a, 0x08072573)
setTMode(0x0807256a)
DisassembleCommand(0x0807256a, None, True)

# C4: beq-taken path in equip_zone_sub_2804
clearListing(0x08072838, 0x08072847)
setTMode(0x08072838)
DisassembleCommand(0x08072838, None, True)

# Step 4: ROM_INCBIN blocks -> DisassembleCommand (address order)
# B1: bne-taken path in field_spell_dispatch_sub_stubs_2004
clearListing(0x080720e2, 0x080720f3)
setTMode(0x080720e2)
DisassembleCommand(0x080720e2, None, True)

# B2: bne-taken path in fn_eligible_vampire_lord_lady_26f4
clearListing(0x0807270e, 0x0807272b)
setTMode(0x0807270e)
DisassembleCommand(0x0807270e, None, True)

# B3: bne-taken path in equip_zone_sub_stubs_274c (B3 before B4: B4 needed first?)
# B4 contains 0x727ae which B3 branches to; but B3's b@0x72784->0x727ae is a forward ref
# that Ghidra resolves after B4 is disassembled. Process B3 first (it stops at b), then B4.
clearListing(0x0807276a, 0x08072787)
setTMode(0x0807276a)
DisassembleCommand(0x0807276a, None, True)

# B4: bne target from B3 + 0x7f return path
clearListing(0x08072794, 0x080727b3)
setTMode(0x08072794)
DisassembleCommand(0x08072794, None, True)
```

Note on pool residue: the only pool word inside the remediated ranges that might need
attention is pool_b8_27b4 @ 0x727b4. This word is OUTSIDE all ROM_INCBIN blocks (at 0x727b4,
after ROM_INCBIN 0x72794/0x20 which ends at 0x727b3). It is already a properly labeled .word
in the asm; only its equate annotation needs updating via EQ_SLOT in Step 2.

**Potential issue**: DC for B3 may leave 0x72786 (0x0000 pad) as a movs r0,r0 NOP instruction.
This is byte-identical and acceptable. If Ghidra leaves it as data, a `.zero 2` in the asm
is also byte-identical.

**Potential issue**: B2 dispatch table entry[0] at 0x72734 must be force_dword BEFORE B2 DC
to prevent Ghidra from treating it as code. Handled in Step 1 above.
