# Refine Proposal: F09-Seg-8 REMEDIATION  [0x0807629c..0x0807738c)

**Purpose**: Eliminate all ROM_INCBIN and .byte CODE residuals left by commit 1e38556 in
the Seg-8 range [0x0807629c, 0x0807738c). Two companion .byte DATA literal-pool slots also
require `createDWord` to resolve a Ghidra half-word split artifact.

**Background**: Seg-8 committed as 1e38556 left one ROM_INCBIN block and one .byte CODE block
undisassembled, plus two literal-pool entries improperly encoded as .byte instead of .word.
Seg-1/4/5 remediation commits (e9636e1, 8f8c64f, 867d68b, 9ff948e) serve as precedents.

---

## Section Mapping

- Function entries: Seg-8 range [0x0807629c..0x0807738c) contains 19 already-named functions
  (all named in commit 1e38556). No new function entries.
- Residual ROM_INCBIN blocks: 1 block
  - `ROM_INCBIN 0x768dc, 0x1e` (30 bytes) at asm line 18484
- Residual .byte CODE blocks: 1 block
  - `.byte 0x10, 0x20` at `LAB_08076750` (2 bytes) at asm line 18273
- Residual .byte DATA blocks (literal pool split artifacts): 2 blocks
  - `DAT_08076720:` `.byte 0x31, 0x15` + `movs r0,r0 @ 08076722 0000` (4 bytes total)
  - `DAT_0807677c:` `.byte 0x68, 0x08, 0x00, 0x00` (4 bytes)

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

Exhaustive ref-scan (raw + THUMB|1) at all block addresses, python verified against
`roms/2343.gba`:

| Block | addr / size | raw refs | THUMB+1 refs | Judgment | Evidence |
|---|---|---|---|---|---|
| Block A | 0x080768dc / 0x1e | 0 | 0 | CODE-disasm | Branch target: `beq LAB_080768dc` @ 0x08076866 (asm:18423, hw=0xd039, target=0x080768dc confirmed python); intra-function branch; first HW 0xe00f = `lsrs r0,r4,#0x1f` |
| Block B | 0x08076750 / 0x2 | 0 | 0 | CODE-disasm | Branch target: `beq LAB_08076750` @ 0x0807672e (asm:18272, hw=0xd00f, target=0x08076750 confirmed python); first HW 0x2010 = `movs r0,#0x10` |
| Block C | 0x08076720 / 0x4 | 0 | 0 | DATA-createDWord | `ldr r0, DAT_08076720` @ 0x08076704 (asm:18228, hw=0x4806, pc-rel imm=0x18, target=0x08076720); ROM bytes {0x31,0x15,0x00,0x00} = word 0x00001531; raw=0/thumb=0 as DATA literal (no external .word pointer to this slot addr) |
| Block D | 0x0807677c / 0x4 | 0 | 0 | DATA-createDWord | `ldr r2, DAT_0807677c` @ 0x0807675e (asm:18283, hw=0x4a07, pc-rel imm=0x1c, target=0x0807677c); ROM bytes {0x68,0x08,0x00,0x00} = word 0x00000868; raw=0/thumb=0 as DATA literal |

**raw=0/THUMB+1=0 note for Blocks A and B**: Both are intra-function branch targets reached
via conditional branch (beq) instructions, NOT via .word pointer tables. Zero external pointer
references are expected and correct. The branch encoding is the authoritative evidence of CODE
classification. Ref-scan of 0x080768dd (THUMB+1 of Block A start) = 0 (not in handler table;
`fn_eligible_spell_vanishing` is referenced at 0x9e41b28 as value 0x080767ad = fn start+1,
not the internal sub-stub start).

**Block C split artifact**: Ghidra created a 2-byte `DAT_` data unit at 0x08076720 (covering
only bytes 0x31,0x15) and then decoded the next 2 bytes (0x00,0x00) as code (`movs r0,r0`
@ 0x08076722). This is a Ghidra disassembly artifact: the actual `ldr r0,[pc,#0x18]` at
0x08076704 loads a 4-byte word from 0x08076720, which is 0x00001531. Both halves are data.
`movs r0,r0` at 0x08076722 is never a branch target (raw=0/THUMB+1=0, confirmed python).

---

## Detailed Analysis (per-block)

### Block A: ROM_INCBIN 0x768dc / 0x1e (30 bytes = 15 THUMB instructions)

**Containing function**: `fn_eligible_spell_vanishing` @ 0x080767ac, specifically the
sub-stub `spell_vanishing_sub_6818` @ 0x08076818.

**Reaching branch**: `beq LAB_080768dc @ 08076866 39d0` (hw=0xd039; imm8=0x39;
target = 0x08076866+4+0x39*2 = 0x080768dc confirmed).

**Decoded instructions** (python decoded, all THUMB16):
```
0x080768dc: 0fe0  lsrs r0,r4,#0x1f
0x080768de: 1a10  subs r0,r2,r0
0x080768e0: 0fe1  lsrs r1,r4,#0x1f
0x080768e2: 1a51  subs r1,r2,r1
0x080768e4: 4011  ands r1,r2
0x080768e6: 4642  mov r2,r8           @ r8 = PLAYER_BLOCK_STRIDE (set by .hword 0x46c1 @ 0x08076840)
0x080768e8: 434a  muls r2,r1
0x080768ea: 1c11  adds r1,r2,#0x0
0x080768ec: 19c9  adds r1,r1,r7      @ r7 = gP1FieldArrayCBase (set by adds r7,r3,r6 @ 0x08076846)
0x080768ee: 18c9  adds r1,r1,r3      @ r3 = FIELD_ARRAY_C_TO_COUNT_NEG_OFF (ldr @ 0x08076874)
0x080768f0: 2201  movs r2,#0x1
0x080768f2: f7cd  BL_prefix (off_hi=0x7cd, signed=-51)
0x080768f4: fe57  BL_suffix (off_lo=0x657)
                  -> BL target = 0x080768f2+4 + (-51<<12) + (0x657<<1) = 0x080445a4
                     = dispatch_equip_zone_sprite_banisher_by_field_count
                       (asm/04_card_zone_sprite.s:9609)
0x080768f6: 207e  movs r0,#0x7e
0x080768f8: e000  b 0x080768fc      -> b LAB_080768fc (shared pop/bx epilogue, already decoded)
```

**BL target verification**: hw1=0xf7cd (prefix, off_hi=0x7cd), hw2=0xfe57 (suffix, off_lo=0x657).
22-bit combined offset = (0x7cd << 11) | 0x657 = 0x3e6e57; sign-extend from bit21
(bit21 set) -> -102825; target = 0x080768f2+4 + (-102825)*2 = 0x080445a4 (confirmed python).
`dispatch_equip_zone_sprite_banisher_by_field_count` @ 0x080445a4 confirmed in
`asm/04_card_zone_sprite.s` line 9609 (`push {r4,r5,r6,lr} @ 080445a4 70b5`).

**Semantics**: Block A is the beq-taken path of `spell_vanishing_sub_6818`'s inner loop.
When the ldrh-loaded halfword matches the compare, this path:
(1) computes opponent side's zone_hand_count pointer
    (gP1FieldArrayCBase + opp*PLAYER_BLOCK_STRIDE + FIELD_ARRAY_C_TO_COUNT_NEG_OFF);
(2) calls `dispatch_equip_zone_sprite_banisher_by_field_count(player_id, hand_count_ptr, 1)`;
(3) returns 0x7e via shared epilogue at LAB_080768fc.
Confidence: high (all register sources traced back to prior instructions in same function;
BL target verified in asm/04).

**Internal literal pool**: None. Exhaustive python scan of all 15 instructions finds no
`ldr r,[pc,#imm]` within 0x080768dc..0x080768f9. No `createDWord` needed inside the
ROM_INCBIN range.

**Fall-through**: `b LAB_080768fc` at last instruction. `LAB_080768fa` and `LAB_080768fc`
are already decoded in asm (lines 18485-18493). No label conflict.

---

### Block B: .byte 0x10,0x20 at LAB_08076750 (2 bytes = 1 THUMB instruction)

**Containing function**: `fn_eligible_mustering_dark_scorpions` @ 0x080765b0.

**Reaching branch**: `beq LAB_08076750 @ 0807672e d00f` (hw=0xd00f; imm8=0x0f;
target = 0x0807672e+4+0x0f*2 = 0x08076750 confirmed python).

**Decoded instruction**: bytes {0x10, 0x20} = halfword 0x2010 =
`movs r0,#0x10` (hi3=001, op=00, rd=0, imm8=0x10). Confidence: high.

**Context**: `LAB_08076750:` is labeled in asm (beq target). Following instruction is
`LAB_08076752: ldrh r2,[r4,#0x8] @ 08076752` (already decoded, asm:18274). The
`movs r0,#0x10` sets r0 (bitmask value 0x10) before the `orrs r0,r2` at LAB_08076752
and `strh r0,[r4,#0x8]` at LAB_08076756.

**Fall-through**: Directly into `LAB_08076752` (already decoded). No gap.

---

### Block C: DAT_08076720 -- literal pool split (4 bytes)

**Nature**: `ldr r0, DAT_08076720` at 0x08076704 (asm:18228) loads a 4-byte word.
Ghidra created a 2-byte `DAT_` data unit covering bytes 0x31,0x15 (0x08076720..0x08076721)
and decoded the following 2 bytes 0x00,0x00 as `movs r0,r0` code at 0x08076722.
The true 4-byte word value = 0x00001531 (python verified:
ROM[0x76720..0x76723] = {0x31,0x15,0x00,0x00}).

**Value**: 0x00001531 = slot_id of Dark Scorpion Burglars
(`data/card-stats.s:14445`, `card_1110: @ Dark Scorpion Burglars slot=0x1531 pw=40933924`).

**Existing equate**: `DARK_SCORPION_BURGLARS_CID = 0x00001531` in
`constants/card_info.inc:1476` (conf: high). REUSE.

**Fix**: `createDWord(0x08076720)` absorbs both the 2-byte DAT_ and the fake `movs r0,r0`
into a single 4-byte word unit; eliminates the spurious code at 0x08076722.

---

### Block D: DAT_0807677c -- literal pool 4-byte .byte (4 bytes)

**Nature**: `ldr r2, DAT_0807677c` at 0x0807675e (asm:18283) loads a 4-byte word.
Ghidra created a 4-byte `DAT_` with `.byte` encoding instead of `.word`.
ROM bytes {0x68,0x08,0x00,0x00} = word 0x00000868 (python verified).

**Value**: 0x00000868 = 2152 = PLAYER_BLOCK_STRIDE.

**Existing equate**: `PLAYER_BLOCK_STRIDE = 0x868` in
`constants/ewram.inc:250` (conf: high; 2146 raw refs). REUSE.

**Fix**: `createDWord(0x0807677c)` converts `.byte` encoding to `.word` unit.

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate via Ghidra equate after createDWord)

| slot | value | const_name | source | action |
|---|---|---|---|---|
| DAT_08076720 @ 0x08076720 | 0x00001531 | DARK_SCORPION_BURGLARS_CID | card_info.inc:1476 REUSE | createDWord + setEquate + EOL |
| DAT_0807677c @ 0x0807677c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 REUSE | createDWord + setEquate + EOL |

**Verification**:
- `DARK_SCORPION_BURGLARS_CID`: `constants/card_info.inc:1476`
  `.equ DARK_SCORPION_BURGLARS_CID, 0x00001531`. ROM[0x76720..23]=0x00001531. Match: high.
- `PLAYER_BLOCK_STRIDE`: `constants/ewram.inc:250`
  `.equ PLAYER_BLOCK_STRIDE, 0x868`. ROM[0x7677c..7f]=0x00000868. Match: high.

**EOL comments** (ASCII only, for Ghidra setEOLComment):
- 0x08076720: `DARK_SCORPION_BURGLARS_CID=0x1531: Dark Scorpion Burglars (pw=40933924); card_info.inc:1476`
- 0x0807677c: `PLAYER_BLOCK_STRIDE=0x868: player data block stride (2152B); ewram.inc:250`

### REF_SLOTS

None. Block A and Block B are CODE continuation paths, not data pointer tables.

### RENAME_SLOTS

None. All existing auto-labels (`LAB_080768dc`, `LAB_08076750`) are retained as Ghidra
re-assigns them on disassembly. No new sub-stub function labels needed.

### FUNC_RENAME

None. All 19 functions in Seg-8 are already correctly named.

### PLATE

None. Block A and Block B sub-stubs are intra-function code paths; they do not require
new plate comments. The containing functions (`fn_eligible_spell_vanishing`,
`fn_eligible_mustering_dark_scorpions`) already have plates in asm.

---

## Disasm Plan (R4)

**Execution order**: Block B first (simpler, sets no shared labels for Block A). Then Block A.
Then createDWord for Blocks C and D. EQ_SLOTS applied after createDWord.

### Step 0: setTMode

```
setTMode(0x08076750, THUMB)   @ Block B
setTMode(0x080768dc, THUMB)   @ Block A
```

### Step 1: Block B -- .byte 0x10,0x20 at LAB_08076750

```
clearListing(0x08076750, 0x08076752)    @ 2 bytes only; stop before LAB_08076752 (already decoded)
DisassembleCommand(0x08076750, None, True)
```

Expected output: `movs r0,#0x10 @ 08076750 1020`
The label `LAB_08076750` already exists as a branch target and will be preserved or
re-assigned on disassembly. Fall-through to `LAB_08076752: ldrh r2,[r4,#0x8]`
(already decoded, no conflict).

**Risk**: None. Single instruction, 2 bytes, no pool.

### Step 2: Block A -- ROM_INCBIN 0x768dc/0x1e

```
clearListing(0x080768dc, 0x080768fa)    @ 0x1e bytes; stop before LAB_080768fa (already decoded)
DisassembleCommand(0x080768dc, None, True)
```

Expected output: 15 THUMB instructions (lsrs, subs x2, ands, mov, muls, adds x3, movs,
BL pair, movs, b). The auto-label `LAB_080768dc` will be re-assigned.
Fall-through: `b LAB_080768fc` at 0x080768f8 auto-resolves to existing `LAB_080768fc`
(already decoded at asm:18487). No conflict.

**Risk**: Low. No internal literal pool. BL target
`dispatch_equip_zone_sprite_banisher_by_field_count` is in a different module (asm/04)
and already named. Ghidra resolves the bl reference automatically.

If Ghidra stops before `b LAB_080768fc` (very unlikely for a b.n +0 offset):
run additional `DisassembleCommand(0x080768f8, None, True)` for the final b instruction only.

### Step 3: Block C -- createDWord at DAT_08076720

```
clearListing(0x08076720, 0x08076724)    @ 4 bytes (covers .byte 0x31,0x15 AND fake movs r0,r0)
createDWord(0x08076720)
@ setEquate: apply DARK_SCORPION_BURGLARS_CID to slot 0x08076720
@ setEOLComment: "DARK_SCORPION_BURGLARS_CID=0x1531: Dark Scorpion Burglars (pw=40933924); card_info.inc:1476"
```

Expected asm output:
```
DWORD_08076720:
    .word  DARK_SCORPION_BURGLARS_CID     @ 08076720 31150000
```

**Pool label collision check**: `DARK_SCORPION_BURGLARS_CID` is a `.equ` constant name in
`constants/card_info.inc`; the Ghidra slot label will be `DWORD_08076720`. No collision
between equate name and slot label. Verified: no Ghidra code/data label named
`DARK_SCORPION_BURGLARS_CID` exists in the asm.

### Step 4: Block D -- createDWord at DAT_0807677c

```
clearListing(0x0807677c, 0x08076780)    @ 4 bytes
createDWord(0x0807677c)
@ setEquate: apply PLAYER_BLOCK_STRIDE to slot 0x0807677c
@ setEOLComment: "PLAYER_BLOCK_STRIDE=0x868: player data block stride (2152B); ewram.inc:250"
```

Expected asm output:
```
DWORD_0807677c:
    .word  PLAYER_BLOCK_STRIDE            @ 0807677c 68080000
```

**Pool label collision check**: `PLAYER_BLOCK_STRIDE` is a `.equ` constant name in
`constants/ewram.inc`; slot label will be `DWORD_0807677c`. No collision.

---

## Carve Plan

None. No inter-function data tables in Seg-8 residuals. Both code blocks (A, B) are
intra-function continuation paths, not standalone dispatch tables requiring rom.s carve.

---

## New Constants / Globals

None. All constants used are already present in constants/:
- `DARK_SCORPION_BURGLARS_CID = 0x1531`: `constants/card_info.inc:1476`
- `PLAYER_BLOCK_STRIDE = 0x868`: `constants/ewram.inc:250`
- `SPELL_VANISHING_CID = 0x16a6`: `constants/card_info.inc:1033` (reference; no new slot)

**C5 by-value verification**:
- 0x00001531: grep `constants/*.inc` -> 1 hit `card_info.inc:1476`. REUSE confirmed.
- 0x00000868: grep `constants/*.inc` -> 1 hit `ewram.inc:250` PLAYER_BLOCK_STRIDE. REUSE confirmed.

---

## Section 5.1 Register (Rule 3) -- zero-ref orphan blocks

None. All four residual blocks have consuming references (conditional branch or ldr pc-rel).
No zero-reference orphans exist in the Seg-8 remediation scope.

---

## Consumer Evidence (R6) -- key slot semantics

| slot | consumer | evidence | confidence |
|---|---|---|---|
| Block A (0x080768dc) | `spell_vanishing_sub_6818` loop body (beq @ 0x08076866) | asm:18423 `beq LAB_080768dc @ 08076866 39d0` | high |
| Block A BL target 0x080445a4 | `dispatch_equip_zone_sprite_banisher_by_field_count` | asm/04_card_zone_sprite.s:9609 `push {r4,r5,r6,lr} @ 080445a4 70b5` | high |
| Block B (0x08076750) | `fn_eligible_mustering_dark_scorpions` (beq @ 0x0807672e) | asm:18272 `beq LAB_08076750 @ 0807672e d00f` | high |
| DAT_08076720 = 0x1531 | `mustering_dark_scorpions_sub_66d8` compare @ 0x08076706 | asm:18229 `cmp r2,r0 @ 08076706 8242` after `ldr r0,DAT_08076720` | high |
| DAT_0807677c = 0x868 | `mustering_dark_scorpions_sub_66d8` multiply @ 0x08076760 | asm:18284 `muls r1,r2 @ 08076760 5143` after `ldr r2,DAT_0807677c` | high |

---

## CID Identification (fn_eligible stubs)

**fn_eligible_spell_vanishing** (Block A containment context):
- THUMB+1 ref of `fn_eligible_spell_vanishing` (0x080767ac+1=0x080767ad) found at
  ROM 0x1e41b28 (addr 0x09e41b28). Entry layout at 0x9e41b24 (0x18-byte entries,
  python verified):
  - +0x00: 0x000016a6 = CID (Spell Vanishing)
  - +0x04: 0x080767ad = fn_eligible_spell_vanishing+1 (THUMB ptr)
  - +0x08..+0x14: fn_activate+1, fn_effect+1, etc.
- CID 0x16a6 = Spell Vanishing: `data/card-stats.s:18124`
  `card_1393: @ Spell Vanishing slot=0x16A6 pw=29735721`. Confirmed.
- `SPELL_VANISHING_CID = 0x16a6` already in `constants/card_info.inc:1033`. No new constant.

**Note on fn_ptr-0xc**: The file 09 doc Section 1 states "fn_eligible block CID is at
fn_ptr address -0xc". For this table (0x09e41xxx, 0x18-byte entries), fn_eligible+1 is at
entry_start+0x04 (not +0x0c). The CID is at entry_start = fn_eligible_ptr_in_table - 0x04
= 0x9e41b28 - 0x04 = 0x9e41b24. CID = 0x16a6 confirmed from python readout;
passcode matches data/card-stats.s. This table uses a different entry layout from the
file07 Seg-5 pattern (where fn_eligible was at +0x0c). The CID identification here is
determined by direct python inspection of the table entry, not from the -0xc formula.

---

## C13-Style Post-Remediation Clean Sweep

Post-remediation, Seg-8 range [0x0807629c, 0x0807738c):

| Residual type | Before | After | How |
|---|---|---|---|
| ROM_INCBIN blocks | 1 (0x768dc/0x1e) | 0 | DisassembleCommand(0x080768dc) -> 15 instrs |
| .byte CODE blocks | 1 (0x08076750/0x2) | 0 | DisassembleCommand(0x08076750) -> movs r0,#0x10 |
| .byte DATA literals (literal pool split) | 2 (DAT_08076720, DAT_0807677c) | 0 | createDWord -> .word |
| stale FUN_ in range | 0 | 0 | grep verified: 0 hits in asm lines 17601..20013 |
| Section 5.1 orphan blocks | 0 | 0 | n/a |

**Expected target**: Zero ROM_INCBIN, zero .byte residual in Seg-8 range post-remediation.
Build + byte-identical SHA1 9689337d verification required after fixer applies all steps.

**Scope note**: The movs r0,r0 @ 08076722 (fake code artifact from Block C split) will be
absorbed by createDWord(0x08076720) and will NOT appear in the post-remediation asm.

---

## Queries

None. All blocks have deterministic classification with high-confidence evidence.
- Block A: 15 THUMB instructions fully decoded by python; BL target verified in asm/04.
- Block B: 1 THUMB instruction (movs r0,#0x10); no ambiguity.
- Block C: Ghidra literal-pool split artifact; createDWord restores correct .word.
- Block D: Literal pool 4-byte value; createDWord restores correct .word.
