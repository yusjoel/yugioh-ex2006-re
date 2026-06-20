# Refine Proposal: F09-Seg5R  [file 09 Seg-5 REMEDIATION 0x08072d20..0x08074338)

**Purpose**: Eliminate 2 ROM_INCBIN + 10 companion .byte CODE/DATA residual blocks left by
commits fa30373 + 4ba8057 in Seg-5a [0x72d20..0x73a5c) and Seg-5b [0x73a5c..0x74338).
All blocks are CODE continuation paths (bne/beq/bls/bcs branch-taken bodies) or DATA
dispatch-table entry[0] slots within already-disassembled functions. No new functions, no
FS THUMB+1 stubs, no §5.1 orphans.

Precedent: F09-Seg1R.proposal.md + F09-Seg1R2.proposal.md (per-stub DC ordering, pool
createDWord discipline) and F09-Seg4R.proposal.md (bne/bls/beq-taken bodies, dispatch
table entry DATA slots, pool-label-must-not-collide-with-equate-name lesson).

---

## Segment Mapping

- Function range: [0x08072d20, 0x08074338) -- Seg-5 (a+b), all functions already named
- Residual ROM_INCBIN: 0x73218/0x12, 0x73636/0x56
- Residual .byte CODE blocks: 0x73156/0xa, 0x7326c/0x4, 0x7359e/0xa, 0x73732/0x8,
  0x7387a/0xa, 0x73922/0x10, 0x73d30/0xe
- Residual .byte DATA slots: 0x73168/0x4, 0x735b4/0x4, 0x7388c/0x4

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

All ref-scans performed python-exhaustive 2B-step against roms/2343.gba.

### ROM_INCBIN blocks

| Block | entry (GBA) | raw | THUMB+1 | Judgment | Evidence |
|---|---|---|---|---|---|
| ROM_INCBIN 0x73218/0x12 | 0x08073218 | 0 | 0 | CODE-disasm | bne LAB_08073218 at 0x0807320a (hw d105) inside trap_dustshoot_dispatch_sub_stubs_31e4; first HW 0x78b9 = ldrb r1,[r7,#2] |
| ROM_INCBIN 0x73636/0x56 | 0x08073636 | 0 | 0 | CODE-disasm | bne LAB_08073636 at 0x08073632 (hw 00d1) inside machine_dup_dispatch_sub_stubs_3628; first HW 0x78a9 = ldrb r1,[r5,#2] |

Note: sub-address 0x08073660 within ROM_INCBIN 0x73636 has THUMB+1=1 at ROM offset 0x66dd88.
That hit is a coincidental bit-pattern in audio/graphics compressed data (0x66dd88 is surrounded
by non-pointer binary; confirmed: 0x66dd84=0x860f080a, 0x66dd8c=0x3a58f596, only 3 GBA-range
values in +/-0x40 window, consistent with compressed asset coincidence). Confidence: high --
not a true function-pointer reference.

### .byte CODE blocks

| Block | entry (GBA) | raw | THUMB+1 | Judgment | Evidence |
|---|---|---|---|---|---|
| 0x73156/0xa | 0x08073156 | 0 | 0 | CODE-disasm | bls LAB_08073156 at 0x08073152 (hw 00d9) in fn_eligible_trap_dustshoot_3140; first HW 0x0080 = lsls r0,r0,#2 (indirect dispatch entry) |
| 0x7326c/0x4 | 0x0807326c | 1 | 0 | CODE-disasm | raw=1 ref from trap_dustshoot_dispatch_table_3168[2] at 0x73170 = .word trap_dustshoot_sub_326c; confirmed expected self-ref from dispatch table; partial-decode stub entry |
| 0x7359e/0xa | 0x0807359e | 0 | 0 | CODE-disasm | bls LAB_0807359e at 0x0807359a (hw 00d9) in fn_eligible_machine_dup_and_league_356c; first HW 0x0080 = lsls r0,r0,#2 |
| 0x73732/0x8 | 0x08073732 | 0 | 0 | CODE-disasm | bcs LAB_08073732 at 0x0807370a (hw d212) in machine_dup_sub_3704; first HW 0xf7d7 = BL_hi |
| 0x7387a/0xa | 0x0807387a | 0 | 0 | CODE-disasm | bls LAB_0807387a at 0x08073876 (see cat_ill_omen fn body); first HW 0x0080 = lsls r0,r0,#2 |
| 0x73922/0x10 | 0x08073922 | 0 | 0 | CODE-disasm | bne LAB_08073922 at 0x08073910 (hw d107) in cat_ill_omen_dispatch_sub_stubs_3900; first HW 0x78ad = ldrb r5,[r5,#2] |
| 0x73d30/0xe | 0x08073d30 | 0 | 0 | CODE-disasm | beq LAB_08073d30 at 0x08073cb8 (hw 3ad0) and 0x08073cc2 (hw 35d0) in reasoning_dispatch_sub_stubs_3bc8; first HW 0x1c20 = adds r0,r4,#0 |

### .byte DATA slots (dispatch table entry[0])

| Block | value (LE) | Judgment | Evidence |
|---|---|---|---|
| 0x73168/0x4 | 0x08073290 | DATA-createDWord | trap_dustshoot_dispatch_table_3168[0]; .byte 0x90,0x32,0x07,0x08 = trap_dustshoot_sub_3290 (label exists line 10871); raw ref from pool_b1_3164 and table traversal |
| 0x735b4/0x4 | 0x0807374c | DATA-createDWord | machine_dup_dispatch_table_35b4[0]; .byte 0x4c,0x37,0x07,0x08 = machine_dup_sub_374c (label exists line 11466); table base ptr at pool_b3_35b0 (0x735b0) refs 0x080735b4 |
| 0x7388c/0x4 | 0x08073a46 | DATA-createDWord | cat_ill_omen_dispatch_table_388c[0]; .byte 0x46,0x3a,0x07,0x08 = cat_ill_omen_sub_3a46 (label exists line 11827); table base ptr at pool_b5_3888 (0x73888) refs 0x0807388c |

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate; reuse existing)

| slot | value | const_name | slot_label | source |
|---|---|---|---|---|
| pool_b4_368c @ 0x7368c | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | pool_b4_368c | REUSE card_info.inc:1496 |

Verification: ROM @ 0x7368c = bytes 1d 01 00 00 -> u32 LE = 0x11d.
card_info.inc:1496: `.equ CARD_DISPLAY_OP31_LP_BAR_SUB, 0x0000011d`. Match: high confidence.
Usage: ldr r1,[pc,#8] at 0x73682 within ROM_INCBIN 0x73636 block -> pool_b4_368c -> r1 = 0x011d,
passed as display_param to trigger_card_display_op31_if_not_active (BL at 0x73684 -> 0x08093390).
Applying equate to pool_b4_368c is an EQ annotation only (no createDWord required; label already .word).

Note: pool_b4_368c label must NOT be renamed to CARD_DISPLAY_OP31_LP_BAR_SUB (Seg-4R lesson:
pool-slot label == equate name causes GAS self-reference error). Label stays pool_b4_368c; equate
is applied via Ghidra createEquate.

### REF_SLOTS (DATA .byte -> .word via createDWord)

| slot | target | gas_label | note |
|---|---|---|---|
| 0x73168 | 0x08073290 | trap_dustshoot_sub_3290 | dispatch table entry[0] for trap_dustshoot_dispatch_table_3168 |
| 0x735b4 | 0x0807374c | machine_dup_sub_374c | dispatch table entry[0] for machine_dup_dispatch_table_35b4 |
| 0x7388c | 0x08073a46 | cat_ill_omen_sub_3a46 | dispatch table entry[0] for cat_ill_omen_dispatch_table_388c |

All target labels already exist in asm (lines 10871, 11466, 11827).
Ghidra fix: clearListing(4B) at each slot, createDWord, export emits .word <label>.

### RENAME_SLOTS (none)

No DAT_/DWORD_ residuals in Seg-5 range (verified by grep). No new sub-stub labels needed
(all CODE blocks are intra-function LAB_ continuations, not new function entries).

### FUNC_RENAME (none)

All containing functions are correctly named from prior Seg-5a/5b passes.

### PLATE (none)

No plate updates required. All containing functions have correct plate text; the CODE block
bodies do not introduce new callee references that would stale existing plates.

---

## Disasm Plan (R4)

### Execution Ordering

Per Seg-1R/Seg-4R precedent: epilogue-first for blocks where shared epilogue is reachable
by multiple paths. Here all blocks branch to already-existing named epilogue LABs (outside the
.byte block ranges), so no special epilogue-first inversion is needed. Process blocks in
address order within each fn_eligible cluster, with DATA createDWord done BEFORE DC to
prevent Ghidra from treating dispatch-table entry[0] slots as code.

Global ordering: DATA createDWords first, then CODE blocks in address order.

---

### Step 1 -- DATA createDWord slots (3 slots)

Execute before any DisassembleCommand to ensure dispatch table entry[0] words are typed
correctly before Ghidra attempts code flow through the table.

```
clearListing(0x08073168, 4)  force_dword -> .word trap_dustshoot_sub_3290
clearListing(0x080735b4, 4)  force_dword -> .word machine_dup_sub_374c
clearListing(0x0807388c, 4)  force_dword -> .word cat_ill_omen_sub_3a46
```

---

### Step 2 -- EQ_SLOT annotation (1 slot)

```
createEquate(0x0807368c, 'CARD_DISPLAY_OP31_LP_BAR_SUB')   @ pool_b4_368c
```

---

### Step 3 -- CODE blocks: DisassembleCommand in address order

#### A1: LAB_08073156 (.byte 0x73156/0xa)

Containing function: fn_eligible_trap_dustshoot_3140 @ 0x08073140.
Reached via: bls LAB_08073156 at 0x08073152 (phase_code-0x62 <= 0x1e -> valid dispatch).

THUMB decode (5 halfwords):
```
0x73156: 0080  lsls r0,r0,#2            ; r0 = (phase_offset-0x62)*4 (table index)
0x73158: 4902  ldr r1,[pc,#8] @ 0x73164 ; r1 = pool_b1_3164 = 0x08073168 = trap_dustshoot_dispatch_table_3168 base
           ; PC=(0x73158+4)&~2 = 0x7315c; addr = 0x7315c+8 = 0x73164 (pool_b1_3164, already in asm)
0x7315a: 1840  adds r0,r0,r1             ; r0 = table_base + index*4
0x7315c: 6800  ldr r0,[r0,#0]           ; r0 = table[phase_offset-0x62]
0x7315e: 4687  mov r15,r0               ; computed indirect jump (stops DC)
```

Pool pool_b1_3164 @ 0x73164 = 0x08073168 (outside block range 0x73156..0x7315f). Already in asm.
No createDWord inside block.

DC plan:
```
clearListing(0x08073156, 0x08073160)  -- 0xa bytes
setTMode(0x08073156)
DisassembleCommand(0x08073156, None, True)
-- stops at mov r15,r0; pad at 0x73160 is pool_b1_3160 (outside block)
```

---

#### B1: ROM_INCBIN 0x73218/0x12

Containing function: trap_dustshoot_dispatch_sub_stubs_31e4 @ 0x080731e4.
Reached via: bne LAB_08073218 at 0x0807320a (count_field_zone_cards_with_field5 returned nonzero).

THUMB decode (9 halfwords):
```
0x73218: 78b9  ldrb r1,[r7,#2]          ; slot[2] = side/player byte
0x7321a: 07c8  lsls r0,r1,#31
0x7321c: 0fc0  lsrs r0,r0,#31           ; r0 = player_side (bit0 of slot[2])
0x7321e: 8839  ldrh r1,[r7,#0]          ; r1 = card_id (slot[0] halfword)
0x73220: 2201  movs r2,#1               ; r2 = 1 (mode param)
0x73222: f02e fd03  BL -> 0x080a1c2c   ; set_lp_display_row_type5(player, card_id, 1)
                  ; hi=0xf02e(46), lo=0xfd03(1283); PC=0x08073226
                  ; target = 0x08073226 + (46<<12) + (1283<<1) = 0x080a1c2c ✓
0x73226: 207f  movs r0,#0x7f            ; return code = 0x7f
0x73228: e03b  b -> 0x08073296          ; b trap_dustshoot_default_32a0? Let me verify
           ; imm8=0x3b=59; target = 0x0807322a + (59<<1) = 0x0807322a + 0x76 = 0x080732a0
           ; trap_dustshoot_default_32a0 @ 0x080732a0 (asm line 10880) -> movs r0,#0; LAB_080732a2
```

Wait: b at 0x73228 (imm8=0x3b=59): target = (0x0807322a) + (59*2) = 0x0807322a + 0x76 = 0x080732a0
= trap_dustshoot_default_32a0. Confidence: high (trap_dustshoot_default_32a0 at 0x080732a0 confirmed asm line 10880).

Literal pools: pool_b2_3210 @ 0x73210 (gP1LifePoints) and pool_b2_3214 @ 0x73214 (PLAYER_BLOCK_STRIDE)
are OUTSIDE block range [0x73218, 0x7322a). No createDWord inside block.

DC plan:
```
clearListing(0x08073218, 0x0807322a)  -- 0x12 bytes
setTMode(0x08073218)
DisassembleCommand(0x08073218, None, True)
-- stops at b @0x73228; 9 instructions decoded
```

---

#### A2: trap_dustshoot_sub_326c entry (.byte 0x7326c/0x4)

Containing function: trap_dustshoot_dispatch_sub_stubs_31e4 (sub-stub cluster).
This is the ENTRY of trap_dustshoot_sub_326c; only the first 4 bytes (2 halfwords) are encoded
as .byte -- the remaining 6 instructions (0x73270..0x7327e) are already decoded.

THUMB decode of 0x7326c..0x7326f (2 halfwords):
```
0x7326c: 78bf  ldrb r7,[r7,#2]          ; slot[2] (same entry pattern as sub_3280/sub_3290)
0x7326e: 07f9  lsls r1,r7,#31           ; isolate bit0 of r7
```

The label trap_dustshoot_sub_326c is already placed at 0x0807326c. Only the .byte block
at the entry needs to be disassembled; Ghidra should then auto-fall-through into the already-
decoded body at 0x73270.

DC plan:
```
clearListing(0x0807326c, 0x08073270)  -- 0x4 bytes
setTMode(0x0807326c)
DisassembleCommand(0x0807326c, None, True)
-- fall-through into already-decoded 0x73270..0x7327e; b @0x7327e stops flow
```

---

#### A3: LAB_0807359e (.byte 0x7359e/0xa)

Containing function: fn_eligible_machine_dup_and_league_356c @ 0x0807356c.
Reached via: bls LAB_0807359e at 0x0807359a (phase_code-0x64 <= 0x1c -> valid dispatch).

THUMB decode (5 halfwords, identical pattern to A1):
```
0x7359e: 0080  lsls r0,r0,#2            ; r0 = (phase_offset-0x64)*4
0x735a0: 4903  ldr r1,[pc,#12] @ 0x735b0 ; r1 = pool_b3_35b0 = 0x080735b4 = machine_dup_dispatch_table_35b4
           ; PC=(0x735a0+4)&~2=0x735a4; addr=0x735a4+12=0x735b0 (pool_b3_35b0, already in asm)
0x735a2: 1840  adds r0,r0,r1
0x735a4: 6800  ldr r0,[r0,#0]
0x735a6: 4687  mov r15,r0               ; computed indirect jump
```

Pool pool_b3_35b0 @ 0x735b0 = 0x080735b4 (outside block range 0x7359e..0x735a7). Already in asm.

DC plan:
```
clearListing(0x0807359e, 0x080735a8)  -- 0xa bytes
setTMode(0x0807359e)
DisassembleCommand(0x0807359e, None, True)
-- stops at mov r15,r0
```

---

#### B2: ROM_INCBIN 0x73636/0x56

Containing function: machine_dup_dispatch_sub_stubs_3628 @ 0x08073628.
Reached via: bne LAB_08073636 at 0x08073632 (check_neo_daedalus_placement_eligible returned nonzero,
i.e., Neo Daedalus IS placeable).

THUMB decode (43 halfwords = 0x56 bytes):
```
0x73636: 78a9  ldrb r1,[r5,#2]          ; slot[2] = player byte
0x73638: 07c8  lsls r0,r1,#31
0x7363a: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x7363c: 8829  ldrh r1,[r5,#0]          ; r1 = card_id
0x7363e: 1c22  adds r2,r4,#0            ; r2 = r4 (zone descriptor or slot context)
0x73640: f01a fa36  BL -> 0x0808dab0    ; dispatch_effect_handler_by_card_id(player, card_id, r4)
           ; hi=0xf01a(26), lo=0xfa36(566); PC=0x08073644
           ; target = 0x08073644 + (26<<12) + (566<<1) = 0x0808dab0 ✓
0x73644: 8168  strh r0,[r5,#10]         ; slot[10] = result halfword
0x73646: 0400  lsls r0,r0,#16           ; shift left to get flags
0x73648: 2800  movs r0,#0               ; (NOTE: r0 already used; this clobbers; Ghidra will have cmp check)
```

Actually wait: 0x73646: 0400 = lsls r0,r0,#16 sets r0; 0x73648: 2800 is NOT movs -- this is the
condition check. Let me re-decode:

```
0x73646: 0400  lsls r0,r0,#16           ; test: shift strh result into flags
0x73648: 2800  cmp r0,#0                ; this is cmp! 0x2800 = cmp r0,#0 (movs r0,#0 = 0x2000)
```

Wait: 0x2800: op=0b0010=movs, rd=(0x2800>>8)&7=0, imm=0x00 -> movs r0,#0. But that would clobber r0.
Actually Ghidra probably knows: 0x73646 does lsls r0,r0,#16; 0x73648 is cmp r0,#0? or movs r0,#0?
Let me re-verify:

From dump: 0x73648: 2800 = 0x0028 byte[0]=0x00, byte[1]=0x28 -> LE = 0x2800.
0x2800 = 0010 1000 0000 0000 = movs/cmp? THUMB: 0010 = rd=(2800>>8)&7=0, so movs r0,imm8=0x00.
But that makes no sense after lsls r0,r0,#16.

Actually re-read: 0x73648 bytes are 0x00 0x28 (from dump showing "2800") -- wait, the dump showed
"0x73648: 2800" meaning the decoded little-endian u16 = 0x2800. But 0x2800:
  - hi byte = 0x28 = 0010 1000 -> upper bits 15-8
  - lo byte = 0x00 -> lower bits 7-0
  So 0x2800 = 0010 1000 0000 0000 = movs r0,#0x00

This IS movs r0,#0. The lsls only set flags; then movs r0,#0 clears r0 for subsequent check.
But wait: after strh result to [r5,#10], then lsls r0,r0,#16 sets CPSR.Z if r0[15:0]==0.
Then 0x7364a: d107 = bne 0x0807365c.

Let me recheck 0x7364a:

```
0x7364a: d107  bne -> 0x0807365c
           ; cond=1(ne), imm8=7; target=(0x0807364c)+(7<<1)=0x0807364c+0xe=0x0807365a? 
```

Hmm. Let me recalculate: target for bne at 0x7364a: PC = 0x7364c; imm8=7; target = 0x7364c+(7*2)=0x7364c+0xe=0x7365a? That contradicts my earlier decode showing target=0x7365c.

PC for conditional branch: PC = instr_addr + 4 = 0x7364a+4 = 0x7364e.

Ah wait: PC for THUMB branch is always instr_addr+4 but for 2-byte instruction it's still +4:
target = (0x0807364e) + (7<<1) = 0x0807364e + 0xe = 0x0807365c ✓

So 0x2800 at 0x73648 must be the condition test, NOT movs:

Re-checking 0x73646..0x73648:
```
0x73646: 0400  lsls r0,r0,#16    ; if r0[15:0]==0 -> Z=1; flags set
-- but 0x73648: 2800 = movs r0,#0 which CLEARS Z!
```

This creates a conflict. Let me look at the actual bytes more carefully:

From dump byte sequence for block 0x73636: a9 78 c8 07 c0 0f 29 88 22 1c ...68 81 00 04 00 28 07 d1...
Position 0x73644-0x73649: offset in block = 0xe..0x13:
  byte[0xe]=0x68, byte[0xf]=0x81, byte[0x10]=0x00, byte[0x11]=0x04, byte[0x12]=0x00, byte[0x13]=0x28

So:
  0x73644: bytes 0x68 0x81 -> LE = 0x8168 = strh r0,[r5,#10] (imm=5*2=10, rn=r5, rd=r0) ✓
  0x73646: bytes 0x00 0x04 -> LE = 0x0400 = lsls r0,r0,#16 ✓
  0x73648: bytes 0x00 0x28 -> LE = 0x2800 = cmp r0,#0? NO: cmp is encoded differently

THUMB cmp: 0010 1 rd imm8 = 0b0010 1 000 0000 0000 = 0x2800. But that's the SAME as movs r0,#0!
Actually NO: THUMB:
  - movs: 0b001 0 0 Rd imm8 -> bit12=0, bit11=0, bit10=0 -> all zeroed
  - cmp: 0b001 0 1 Rd imm8 -> bit11=1

0x2800 = 0010 1000 0000 0000:
  bits 15-11: 0b00101 = CMP (since bit11=1, op=00101 is `cmp rd,imm8` where rd=(hw>>8)&7=0)
  rd = (0x2800 >> 8) & 7 = 0x28 & 7 = 0 = r0
  imm8 = 0x00

So 0x2800 IS `cmp r0,#0`! My earlier decode was wrong (printed it as movs). Confirmed: lsls r0,r0,#16 sets Z if bottom 16 bits of handler result = 0; then cmp r0,#0 checks if r0 (after lsls = high bits only, but lsls replaces r0 with shifted value) is zero; bne 0x7365c if r0 != 0 (handler result was nonzero after shift).

Corrected decode:
```
0x73636: 78a9  ldrb r1,[r5,#2]
0x73638: 07c8  lsls r0,r1,#31
0x7363a: 0fc0  lsrs r0,r0,#31           ; r0 = player_side (bit0)
0x7363c: 8829  ldrh r1,[r5,#0]          ; r1 = card_id
0x7363e: 1c22  adds r2,r4,#0            ; r2 = zone_descriptor (r4 param)
0x73640: f01a fa36  BL dispatch_effect_handler_by_card_id -> 0x0808dab0
0x73644: 8168  strh r0,[r5,#10]         ; slot[10] = handler result (halfword)
0x73646: 0400  lsls r0,r0,#16           ; check if result[15:0] != 0
0x73648: 2800  cmp r0,#0                ; compare shifted result with 0
0x7364a: d107  bne -> 0x0807365c        ; if nonzero -> bne-taken path at 0x7365c
```

NOT-taken path (result == 0, conditions not met):
```
0x7364c: 78ad  ldrb r5,[r5,#2]
0x7364e: 07e8  lsls r0,r5,#31
0x73650: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x73652: 210d  movs r1,#0xd             ; r1 = 0xd (display_param)
0x73654: f01f fe9c  BL trigger_card_display_op31_if_not_active -> 0x08093390
           ; hi=0xf01f(31), lo=0xfe9c(668); PC=0x08073658
           ; target = 0x08073658 + (31<<12) + (668<<1) = 0x08093390 ✓
0x73658: 206e  movs r0,#0x6e            ; return code = 0x6e
0x7365a: e07d  b machine_dup_default_3756 -> 0x08073756
           ; imm11=0x7d=125; target=(0x0807365c)+(125<<1)=0x08073756 ✓ machine_dup_default_3756
```

bne-taken path (result != 0, Neo Daedalus effect applied):
```
0x7365c: 896c  ldrh r4,[r5,#10]         ; r4 = slot[10] (handler result already stored)
0x7365e: 78aa  ldrb r2,[r5,#2]
0x73660: 07d0  lsls r0,r2,#31
0x73662: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x73664: f7bf ffa8  BL count_available_monster_slots -> 0x080335b8
           ; hi=0xf7bf(-65), lo=0xffa8(1960? -> wait hi_off=0x7bf=1983, bit10=1 -> neg
           ; hi_off=0x7bf-0x800=-65; lo_off=0xfa8=4008? No: lo=0xffa8&0x7ff=0x5a8=1448
```

Re-check BL at 0x73664:
bytes from block: at offset 0x2e from block start = 0x73636+0x2e = 0x73664
bytes: bf f7 a8 ff (from block dump: ...f7bf ffa8...)
hi=0xf7bf, lo=0xffa8:
- hi_off = 0xf7bf & 0x7ff = 0x3bf = 959; bit10=(0x3bf>>10)&1=0; positive; hi_off=0x3bf=959? 
  No: 0x3bf = 0b01111011111, bit10=0, so positive: hi_off=0x3bf=-65? 

  Actually: 0xf7bf: bits[10:0] = 0x7bf. 0x7bf = 0b11111011111. bit10=1! So hi_off=0x7bf-0x800=-0x41=-65.

lo=0xffa8: lo_off = 0xffa8 & 0x7ff = 0x5a8 = 1448.

Hmm but 0xffa8 & 0x7ff:
  0xffa8 = 1111 1111 1010 1000; bits[10:0] = 111 1010 1000 = 0x7a8 = 1960. 
  Wait: 0xffa8 & 0x7ff = 0xffa8 & 0b11111111111 = 0b11111010 1000 & 0b11111111111 = 0b11010 1000? 
  Let me just compute: 0xffa8 & 0x7ff = 0xffa8 & 2047:
  0xffa8 = 65448; 65448 & 2047 = 65448 % 2048 = 65448 - 31*2048 = 65448 - 63488 = 1960.
  So lo_off = 1960.

target = (0x08073668) + (-65<<12) + (1960<<1) = 0x08073668 - 0x41000 + 0xF50 = 0x08073668 - 0x400B0 = ?

Wait: -65 * 4096 = -266240 = -0x41000.
0x08073668 - 0x41000 + 0x0F50 = 0x08073668 + (-0x41000 + 0xF50) = 0x08073668 - 0x400B0 = 0x08033558?

That doesn't match expected 0x080335b8. Let me just trust the python computation which showed target=0x080335b8 earlier (verified twice). Python is correct.

The BL targets for 0x73664 and 0x73676 are both 0x080335b8 = count_available_monster_slots.

```
0x73664: f7bf ffa8  BL count_available_monster_slots -> 0x080335b8
0x73668: 4284  cmp r4,r0                ; compare slot[10] vs available_count
0x7366a: da01  bge -> 0x0807366e? wait
```

0xda01: cond=0xa=bge, imm8=1; target=(0x0807366c)+(1<<1)=0x0807366e... 
  But 0x7366a: da01 -> bge; imm8=1; PC=0x7366c; target=0x7366c+2=0x7366e? No: target=PC+(imm8<<1)=0x7366c+2=0x7366e. 

Decode:
0xda01: 0b1101 1010 0000 0001 -> cond=0b1010=bge, imm8=0x01; target=(0x0807366c)+(0x01<<1)=0x08073670.

```
0x73668: 4284  cmp r4,r0                ; cmp slot[10] with available_monster_slots count
0x7366a: da01  bge -> 0x08073670        ; if slot[10] >= count: clip to count
0x7366c: 8968  ldrh r0,[r5,#10]         ; else r0 = slot[10] (use as-is)
0x7366e: e004  b -> 0x0807367a          ; skip clip
0x73670: 78a9  ldrb r1,[r5,#2]
0x73672: 07c8  lsls r0,r1,#31
0x73674: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x73676: f7bf ff9f  BL count_available_monster_slots -> 0x080335b8   ; get fresh count
           ; hi=0xf7bf(-65), lo=0xff9f; lo_off=0x79f? Let me trust python: target=0x080335b8 ✓
0x7367a: 8168  strh r0,[r5,#10]         ; slot[10] = clipped count (or original r0 from ldrh)
0x7367c: 78ad  ldrb r5,[r5,#2]
0x7367e: 07e8  lsls r0,r5,#31
0x73680: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x73682: 4902  ldr r1,[pc,#8] @ 0x7368c ; r1 = pool_b4_368c = CARD_DISPLAY_OP31_LP_BAR_SUB = 0x011d
           ; PC=(0x73682+4)&~2=0x73684; addr=0x73684+8=0x7368c ✓ (pool_b4_368c outside block)
0x73684: f01f fe84  BL trigger_card_display_op31_if_not_active -> 0x08093390
           ; hi=0xf01f(31), lo=0xfe84(644); PC=0x08073688; target=0x08073688+(31<<12)+(644<<1)=0x08093390 ✓
0x73688: 207e  movs r0,#0x7e            ; return code = 0x7e
0x7368a: e065  b LAB_08073758 -> 0x08073758
           ; imm11=0x65=101; target=(0x0807368c)+(101<<1)=0x0807368c+0xca=0x08073756? 
```

b target: imm11=0x65=101; PC=0x0807368c; target=0x0807368c+(101<<1)=0x0807368c+0xca=0x08073756=machine_dup_default_3756 ✓

Pool pool_b4_368c @ 0x7368c (OUTSIDE block range 0x73636..0x7368b). Already in asm. EQ applied in Step 2.

DC plan:
```
clearListing(0x08073636, 0x0807368c)  -- 0x56 bytes
setTMode(0x08073636)
DisassembleCommand(0x08073636, None, True)
-- Ghidra follows both edges of bne at 0x7364a:
   NOT-taken: 0x7364c..0x7365a (b machine_dup_default_3756 stops flow)
   taken:     0x7365c..0x7368a (b LAB_08073758 stops flow)
-- 43 halfwords decoded
```

Note: clearListing stops at 0x7368b inclusive (block end = 0x73636+0x56-1 = 0x7368b).
pool_b4_368c at 0x7368c is OUTSIDE range; not cleared.

---

#### A4: LAB_08073732 (.byte 0x73732/0x8)

Containing function: machine_dup_sub_3704 @ 0x08073704 (sub-stub in machine_dup cluster).
Reached via: bcs LAB_08073732 at 0x0807370a (slot[8] >= slot[10] -> early return path, no
set_code advancement).

THUMB decode (4 halfwords):
```
0x73732: f7d7 f89d  BL decrement_lp_bar_display_counter -> 0x0804a870
           ; hi=0xf7d7, hi_off=0x7d7; bit10=1 -> hi_off=0x7d7-0x800=-0x29=-41
           ; lo=0xf89d, lo_off=0x7ff&0xf89d=0x09d=157
           ; PC=0x08073736; target=0x08073736+(-41<<12)+(157<<1)=0x08073736-0xa9000+0x13a=0x0804a870 ✓
0x73736: 2064  movs r0,#0x64            ; return code = 0x64
0x73738: e00e  b LAB_08073758 -> 0x08073758
           ; imm11=0xe=14; PC=0x0807373a; target=0x0807373a+(14<<1)=0x0807373a+0x1c=0x08073756
           ; = machine_dup_default_3756 (0x73756=movs r0,#0; LAB_08073758 epilogue)
```

b target: 0x08073756 = machine_dup_default_3756 ✓ (asm line 11472).

No literal pools within block range 0x73732..0x73739.

DC plan:
```
clearListing(0x08073732, 0x0807373a)  -- 0x8 bytes
setTMode(0x08073732)
DisassembleCommand(0x08073732, None, True)
-- stops at b machine_dup_default_3756; 4 halfwords decoded
```

---

#### A5: LAB_0807387a (.byte 0x7387a/0xa)

Containing function: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864.
Reached via: bls dispatch branch in fn_eligible_cat_ill_omen_and_owl_of_luck (phase_offset <= limit
-> valid dispatch). Pattern identical to A1/A3.

THUMB decode (5 halfwords):
```
0x7387a: 0080  lsls r0,r0,#2
0x7387c: 4902  ldr r1,[pc,#8] @ 0x73888 ; r1 = pool_b5_3888 = 0x0807388c = cat_ill_omen_dispatch_table_388c
           ; PC=(0x7387c+4)&~2=0x73880; addr=0x73880+8=0x73888 (pool_b5_3888, already in asm)
0x7387e: 1840  adds r0,r0,r1
0x73880: 6800  ldr r0,[r0,#0]
0x73882: 4687  mov r15,r0
```

Pool pool_b5_3888 @ 0x73888 (outside block range 0x7387a..0x73883). Already in asm.

DC plan:
```
clearListing(0x0807387a, 0x08073884)  -- 0xa bytes
setTMode(0x0807387a)
DisassembleCommand(0x0807387a, None, True)
-- stops at mov r15,r0
```

---

#### A6: LAB_08073922 (.byte 0x73922/0x10)

Containing function: cat_ill_omen_dispatch_sub_stubs_3900 (sub-stub cluster).
Reached via: bne LAB_08073922 at 0x08073910 (dispatch_effect_handler_by_card_id returned nonzero,
i.e., cat_ill_omen effect successfully dispatched).

THUMB decode (8 halfwords):
```
0x73922: 78ad  ldrb r5,[r5,#2]
0x73924: 07e8  lsls r0,r5,#31
0x73926: 0fc0  lsrs r0,r0,#31           ; r0 = player_side
0x73928: 215e  movs r1,#0x5e            ; r1 = 0x5e (display_param for LP-bar trigger)
0x7392a: f01f fd31  BL trigger_card_display_op31_if_not_active -> 0x08093390
           ; hi=0xf01f(31), lo=0xfd31(1329); PC=0x0807392e
           ; target = 0x0807392e + (31<<12) + (1329<<1) = 0x08093390 ✓
0x7392e: 207f  movs r0,#0x7f            ; return code = 0x7f
0x73930: e091  b cat_ill_omen_default_3a54 -> 0x08073a54
           ; imm11=0x91=145; PC=0x08073932; target=0x08073932+(145<<1)=0x08073932+0x122=0x08073a54 ✓
```

b target: 0x08073a54 = cat_ill_omen_default_3a54 (asm line 11834) ✓.
No literal pools within block range 0x73922..0x73931.

DC plan:
```
clearListing(0x08073922, 0x08073932)  -- 0x10 bytes
setTMode(0x08073922)
DisassembleCommand(0x08073922, None, True)
-- stops at b cat_ill_omen_default_3a54; 8 halfwords decoded
```

---

#### A7: LAB_08073d30 (.byte 0x73d30/0xe)

Containing function: reasoning_dispatch_sub_stubs_3bc8 (sub-stub cluster within
tick_equip_zone_eligibility_display_state_seq / fn_eligible_reasoning cluster, Seg-5b).
Reached via: beq LAB_08073d30 at 0x08073cb8 (check_card_field5_is_nonzero returned 0)
          AND beq LAB_08073d30 at 0x08073cc2 (check_card_not_equip_placement_type returned 0).
Both beq target this same block (two convergent branch sources).

THUMB decode (7 halfwords):
```
0x73d30: 1c20  adds r0,r4,#0            ; r0 = r4 (player_side param)
0x73d32: 2101  movs r1,#1               ; r1 = 1 (count_limit = 1)
0x73d34: 2200  movs r2,#0               ; r2 = 0 (base_attr = 0)
0x73d36: f7d5 fc61  BL enqueue_equip_zone_sprite_attr_full -> 0x080495fc
           ; hi=0xf7d5(-43), lo=0xfc61(1121+? let me verify lo: 0xfc61&0x7ff=0x461=1121)
           ; PC=0x08073d3a; target=0x08073d3a+(-43<<12)+(1121<<1)=0x08073d3a-0x2b000+0x8c2=0x080495fc ✓
0x73d3a: 207d  movs r0,#0x7d            ; return code = 0x7d
0x73d3c: e01b  b LAB_08073d74 -> 0x08073d74
           ; imm11=0x1b=27; PC=0x08073d3e; target=0x08073d3e+(27<<1)=0x08073d3e+0x36=0x08073d74 ✓
```

b target: LAB_08073d74 @ 0x08073d74 (asm line 12239) = movs r0,#0 epilogue of reasoning dispatch ✓.
No literal pools within block range 0x73d30..0x73d3d.

DC plan:
```
clearListing(0x08073d30, 0x08073d3e)  -- 0xe bytes
setTMode(0x08073d30)
DisassembleCommand(0x08073d30, None, True)
-- stops at b LAB_08073d74; 7 halfwords decoded
```

---

## Carve Plan (R7)

None. No inter-function ROM_INCBIN blocks in Seg-5 range. All ROM_INCBIN blocks are intra-function
branch-taken code paths.

---

## §5.1 Registration (Rule 3) -- 0-ref blocks

None. Every block (ROM_INCBIN and .byte) is reached by an explicit intra-function branch
instruction (bne/beq/bls/bcs) within the same named function. All have confirmed branch-ref.

The THUMB+1 hit at sub-address 0x08073660 inside ROM_INCBIN 0x73636 is classified as a
coincidental compressed-data collision (ROM offset 0x66dd88, audio/graphics binary stream,
no surrounding GBA pointer context). It does NOT constitute a true fn-ptr reference.
This block is classified CODE-disasm (intra-function bne), not §5.1.

---

## New Constants / Globals

**None new.** Only one equate applied:

- pool_b4_368c (0x7368c): CARD_DISPLAY_OP31_LP_BAR_SUB = 0x011d -- REUSE card_info.inc:1496.

All other BL targets (set_lp_display_row_type5, dispatch_effect_handler_by_card_id,
count_available_monster_slots, trigger_card_display_op31_if_not_active,
decrement_lp_bar_display_counter, enqueue_equip_zone_sprite_attr_full) are already named
functions with no pool slots inside the remediated blocks.

---

## Consumer Evidence (R6)

**ROM_INCBIN 0x73218 BL -> set_lp_display_row_type5 (0x080a1c2c)**
- File: asm/13_equip_placement.s, confirmed `set_lp_display_row_type5:` at push {r4,lr} @ 0x080a1c2c
- Params: r0=player_side, r1=card_id (ldrh [r7,#0]), r2=1
- Same BL target as F09-Seg1R B1 (0x6f00a): identical pattern, different return code (0x7f vs 0x63)
- Confidence: high

**ROM_INCBIN 0x73636 BL -> dispatch_effect_handler_by_card_id (0x0808dab0)**
- File: asm/11_effect_slot_puzzletext.s, `dispatch_effect_handler_by_card_id:` push @ 0x0808dab0
- Params: r0=player_side, r1=card_id (ldrh [r5,#0]), r2=r4 (zone descriptor)
- 45+ other call sites in file 09 with identical BL target
- Confidence: high

**ROM_INCBIN 0x73636 BL -> count_available_monster_slots (0x080335b8) x2**
- File: asm/02_text_lp_fieldspell.s, `count_available_monster_slots:` push @ 0x080335b8
- Used twice: first to get limit (cmp r4,r0), second to refresh count after clip (bge path)
- Confidence: high

**LAB_08073732 BL -> decrement_lp_bar_display_counter (0x0804a870)**
- File: asm/05_equip_eligibility_a.s, `decrement_lp_bar_display_counter:` push @ 0x0804a870
- Called when slot[8] >= slot[10] (over limit); same callee as asm/09 line 12215
- Confidence: high

**LAB_08073d30 BL -> enqueue_equip_zone_sprite_attr_full (0x080495fc)**
- File: asm/05_equip_eligibility_a.s, `enqueue_equip_zone_sprite_attr_full:` push @ 0x080495fc
- Pattern r0=player_side, r1=1, r2=0 matches sibling call at asm/09 line 12207 (LAB_08073d24 path)
- Confidence: high

---

## C13-Style Post-Remediation Proof (Zero Residue)

### ROM_INCBIN blocks in Seg-5 [0x72d20, 0x74338):

| Block | Disposition | After |
|---|---|---|
| ROM_INCBIN 0x73218/0x12 | DISASM B1 -> 9 halfwords; b->trap_dustshoot_default_32a0 | GONE |
| ROM_INCBIN 0x73636/0x56 | DISASM B2 -> 43 halfwords + 2-path bne; b->machine_dup_default_3756/LAB_08073758 | GONE |

Post-remediation ROM_INCBIN count in Seg-5: **0**

### .byte CODE blocks in Seg-5 [0x72d20, 0x74338):

| Block | Disposition | After |
|---|---|---|
| .byte 0x73156/0xa | DISASM A1 -> 5 HW; mov r15,r0 stops DC | GONE |
| .byte 0x7326c/0x4 | DISASM A2 -> 2 HW entry; fall-through into decoded body | GONE |
| .byte 0x7359e/0xa | DISASM A3 -> 5 HW; mov r15,r0 stops DC | GONE |
| .byte 0x73732/0x8 | DISASM A4 -> 4 HW; b->machine_dup_default_3756 stops DC | GONE |
| .byte 0x7387a/0xa | DISASM A5 -> 5 HW; mov r15,r0 stops DC | GONE |
| .byte 0x73922/0x10 | DISASM A6 -> 8 HW; b->cat_ill_omen_default_3a54 stops DC | GONE |
| .byte 0x73d30/0xe | DISASM A7 -> 7 HW; b->LAB_08073d74 stops DC | GONE |

### .byte DATA slots in Seg-5 [0x72d20, 0x74338):

| Block | Disposition | After |
|---|---|---|
| .byte 0x73168/0x4 | createDWord -> .word trap_dustshoot_sub_3290 | GONE |
| .byte 0x735b4/0x4 | createDWord -> .word machine_dup_sub_374c | GONE |
| .byte 0x7388c/0x4 | createDWord -> .word cat_ill_omen_sub_3a46 | GONE |

Post-remediation .byte-code residue in Seg-5: **0**
Justified §5.1 orphans: **0**
Remaining .byte DATA: **0** (all 3 createDWord'd to named .word entries)

**Total blocks handled: 12 (2 ROM_INCBIN + 7 .byte CODE + 3 .byte DATA)**
**Target: 0 ROM_INCBIN + 0 .byte-code residue in Seg-5 range**

---

## Ghidra Script Plan (DisassembleF09Seg5R.py)

```python
# Step 1: DATA .byte slots -> createDWord (must be before DC)
force_dword(0x08073168)  # -> .word trap_dustshoot_sub_3290
force_dword(0x080735b4)  # -> .word machine_dup_sub_374c
force_dword(0x0807388c)  # -> .word cat_ill_omen_sub_3a46

# Step 2: EQ annotation
createEquate(0x0807368c, 'CARD_DISPLAY_OP31_LP_BAR_SUB')  # pool_b4_368c REUSE card_info.inc

# Step 3: CODE blocks in address order
# A1: indirect dispatch in fn_eligible_trap_dustshoot_3140
clearListing(0x08073156, 0x08073160)
setTMode(0x08073156)
DisassembleCommand(0x08073156, None, True)

# B1: bne-taken in trap_dustshoot_dispatch_sub_stubs_31e4
clearListing(0x08073218, 0x0807322a)
setTMode(0x08073218)
DisassembleCommand(0x08073218, None, True)

# A2: entry stub trap_dustshoot_sub_326c
clearListing(0x0807326c, 0x08073270)
setTMode(0x0807326c)
DisassembleCommand(0x0807326c, None, True)

# A3: indirect dispatch in fn_eligible_machine_dup_and_league_356c
clearListing(0x0807359e, 0x080735a8)
setTMode(0x0807359e)
DisassembleCommand(0x0807359e, None, True)

# B2: bne-taken in machine_dup_dispatch_sub_stubs_3628
clearListing(0x08073636, 0x0807368c)
setTMode(0x08073636)
DisassembleCommand(0x08073636, None, True)

# A4: bcs-taken in machine_dup_sub_3704
clearListing(0x08073732, 0x0807373a)
setTMode(0x08073732)
DisassembleCommand(0x08073732, None, True)

# A5: indirect dispatch in fn_eligible_cat_ill_omen_and_owl_of_luck
clearListing(0x0807387a, 0x08073884)
setTMode(0x0807387a)
DisassembleCommand(0x0807387a, None, True)

# A6: bne-taken in cat_ill_omen_dispatch_sub_stubs_3900
clearListing(0x08073922, 0x08073932)
setTMode(0x08073922)
DisassembleCommand(0x08073922, None, True)

# A7: beq-taken in reasoning_dispatch_sub_stubs_3bc8
clearListing(0x08073d30, 0x08073d3e)
setTMode(0x08073d30)
DisassembleCommand(0x08073d30, None, True)
```

Notes:
- clearListing ranges are [start, end) exclusive: 0x0807322a = 0x08073218+0x12 (18B), etc.
- B2 clearListing(0x08073636, 0x0807368c): excludes pool_b4_368c at 0x7368c (which is already
  .word typed). If Ghidra clears this anyway, add explicit force_dword(0x0807368c) AFTER DC.
- All DisassembleCommand calls use unrestricted mode (third arg = True) per Seg-1R C2 B1 precedent.
- pool residue watch: all pool .word slots referenced from within the blocks are OUTSIDE their
  respective clearListing ranges. No secondary pool-fix pass should be needed.
- Potential issue: A2 (trap_dustshoot_sub_326c entry at 0x7326c) -- if body at 0x73270 was already
  fully decoded in Ghidra, DC fall-through may auto-confirm. If Ghidra shows the body as data
  (unlikely given prior Seg-5a pass), add explicit DisassembleCommand(0x08073270, ...) step.

---

## Help Requests

None. All 12 blocks classified with high confidence from ROM byte evidence, branch instruction
cross-referencing, BL target reverse-computation, and asm label verification.
