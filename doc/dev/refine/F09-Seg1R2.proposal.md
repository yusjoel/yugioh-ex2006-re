# Refine Proposal: F09-Seg-1 REMEDIATION -- Cluster-2 [0x0806f85e..0x0806fef4)

> Remediation scope: 9 ROM_INCBIN blocks + 11 companion .byte partial-decode blocks (incl. B2a equip_lp_sub_fa4c body)
> within [0x0806f85e, 0x0806fef4). These are the two fn_eligible stubs and their
> associated dispatch sub-stub clusters that commit 08b3db1 left partially disassembled.
> Cluster-1 [0x0806f008..0x0806f1c4) was remediated in commit e9636e1.
> This proposal covers everything in [0x0806f85e..0x0806fef4) exhaustively.
> After landing, the only remaining residue in original Seg-1 is Cluster-3
> [0x0806fef4..0x0806ff50), which contains already-decoded .byte bodies for the
> equip_chain_act sub-stubs ff0a/ff1a/ff2c/ff3c/ff46. Those .byte blocks are
> simple enough to be handled in a follow-up remediation pass.

---

## Section Mapping

Two fn_eligible / dispatch clusters in Cluster-2:

### Cluster-2A: Destiny Board dispatch cluster [0x0806f85e..0x0806fb87]

Containing function: eligible_destiny_board_f85c (fn_eligible, push decoded at 0x6f85c)
Sub-dispatch table: equip_lp_disp_table_f994 at 0x0806f994 (29-entry raw-ptr table, already labeled)

| Block | ROM off / size | Role | Entry addr | Entry ref |
|-------|----------------|------|------------|-----------|
| B1    | 0x6f85e / 0x136 | fn_eligible body | 0x0806f85c | FS table THUMB+1 x2 |
| B2    | 0x6fa0a / 0x36  | eligible_sub_stubs_fa08 body | 0x0806fa08 | dispatch_table[28] raw |
| B3    | 0x6fa62 / 0x12  | equip_lp_sub_fa5e body | 0x0806fa5e | dispatch_table[26] raw |
| B4    | 0x6fa78 / 0x8c  | equip_lp_sub_fa74 body | 0x0806fa74 | dispatch_table[25] raw |
| B5    | 0x6fb16 / 0x32  | equip_lp_sub_fb14 body | 0x0806fb14 | dispatch_table[24] raw |

Companion .byte blocks (partial decode -- entry decoded, body as .byte):
| Block | Range             | Role | Entry at |
|-------|-------------------|------|----------|
| B2a   | 0x6fa4e..0x6fa5d  | equip_lp_sub_fa4c body | 0x0806fa4c |
| B2c   | 0x6fb4e..0x6fb57  | equip_lp_sub_fb4c body | 0x0806fb4c |
| B2d   | 0x6fb5a..0x6fb63  | equip_lp_sub_fb58 body | 0x0806fb58 |
| B2e   | 0x6fb66..0x6fb6f  | equip_lp_sub_fb64 body | 0x0806fb64 |
| B2f   | 0x6fb72..0x6fb75  | equip_lp_sub_fb70 body | 0x0806fb70 |
| B2g   | 0x6fb78..0x6fb87  | equip_lp_sub_fb76 body (SHARED EPILOGUE) | 0x0806fb76 |

### Cluster-2B: Cathedral of Nobles dispatch cluster [0x0806fdec..0x0806fef3]

Containing function: eligible_cathedral_of_nobles_fdec (fn_eligible, push decoded at 0x6fdec)
Sub-dispatch table: equip_chain_act_disp_table_fe14 at 0x0806fe14 (29-entry raw-ptr table, already labeled)

| Block | ROM off / size | Role | Entry addr | Entry ref |
|-------|----------------|------|------------|-----------|
| B6    | 0x6fdee / 0x26  | fn_eligible body | 0x0806fdec | FS table THUMB+1 x2 |
| B7    | 0x6fe8a / 0x4a  | eligible_sub_stubs_fe88 body | 0x0806fe88 | dispatch_table[28] raw |
| B8    | 0x6fede / 0x12  | equip_chain_act_sub_fedc body | 0x0806fedc | dispatch_table[27] raw |
| B9    | 0x6fef2 / 0x18  | equip_chain_act_sub_fef0 body | 0x0806fef0 | dispatch_table[26] raw |

Companion .byte blocks:
| Block | Range             | Role | Entry at |
|-------|-------------------|------|----------|
| B7c   | 0x6ff0c..0x6ff19  | equip_chain_act_sub_ff0a body | 0x0806ff0a |
| B7d   | 0x6ff1c..0x6ff2b  | equip_chain_act_sub_ff1a body | 0x0806ff1a |
| B7e   | 0x6ff2e..0x6ff3b  | equip_chain_act_sub_ff2c body | 0x0806ff2c |
| B7f   | 0x6ff3e..0x6ff45  | equip_chain_act_sub_ff3c body | 0x0806ff3c |
| B7g   | 0x6ff48..0x6ff4b  | equip_chain_act_sub_ff46 body (SHARED EPILOGUE) | 0x0806ff46 |

NOTE: B7c/B7d/B7e/B7f/B7g are at 0x0806ff0a..0x0806ff4f which is OUTSIDE the stated
Cluster-2 range [0x6f85e..0x6fef4). They are listed here for completeness as companions
to Cluster-2B; their disassembly is handled in the same Ghidra script pass. The stated
end of this proposal's scope is 0x0806fef4 (= B9 end at 0x6fef2+0x18=0x6ff0a, but
for the 9 ROM_INCBIN blocks only). The 5 .byte companions in Cluster-3 range are
scheduled for a separate Cluster-3 pass but included in this proposal's disasm plan
since they share the same clearListing/Disassemble session as B7.

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

### Primary ref-scan: stub ENTRY addresses (confirming CODE classification)

All ROM_INCBIN block-start addresses have raw=0, THUMB+1=0 (mid-body, expected: no external
pointer to function internals). True refs are on the ENTRY address of the containing stub.

| Block | Entry addr | raw hits | THUMB+1 hits | Ref location | Judgment |
|-------|-----------|----------|--------------|--------------|----------|
| B1 | 0x0806f85c | raw=0 | THUMB+1=2 | FS table @ ROM 0x1e40a90 + 0x1e43a30 | DISASM (fn_eligible) |
| B2 | 0x0806fa08 | raw=1 | THUMB+1=0 | dispatch_table[28] @ ROM 0x6fa04 | DISASM (raw dispatch) |
| B2a | 0x0806fa4c | raw=1 | THUMB+1=0 | dispatch_table[27] @ ROM 0x6fa00 | DISASM (raw dispatch) |
| B3 | 0x0806fa5e | raw=1 | THUMB+1=0 | dispatch_table[26] @ ROM 0x6f9fc | DISASM (raw dispatch) |
| B4 | 0x0806fa74 | raw=1 | THUMB+1=0 | dispatch_table[25] @ ROM 0x6f9f8 | DISASM (raw dispatch) |
| B5 | 0x0806fb14 | raw=1 | THUMB+1=0 | dispatch_table[24] @ ROM 0x6f9f4 | DISASM (raw dispatch) |
| B2c | 0x0806fb4c | raw=1 | THUMB+1=0 | dispatch_table[20] @ ROM 0x6f9e4 | DISASM (raw dispatch) |
| B2d | 0x0806fb58 | raw=1 | THUMB+1=0 | dispatch_table[19] @ ROM 0x6f9e0 | DISASM (raw dispatch) |
| B2e | 0x0806fb64 | raw=1 | THUMB+1=0 | dispatch_table[18] @ ROM 0x6f9dc | DISASM (raw dispatch) |
| B2f | 0x0806fb70 | raw=1 | THUMB+1=0 | dispatch_table[0] @ ROM 0x6f994 | DISASM (raw dispatch) |
| B2g | 0x0806fb76 | raw=20 | THUMB+1=0 | dispatch_table[1..17,21..23] x17 + b-branches from stubs | DISASM (shared epilogue) |
| B6 | 0x0806fdec | raw=0 | THUMB+1=2 | FS table @ ROM 0x1e46610 (CID=0x146f, fn_elig+1=0x806fded) | DISASM (fn_eligible) |
| B7 | 0x0806fe88 | raw=1 | THUMB+1=0 | dispatch_table[28] @ ROM 0x6fe84 | DISASM (raw dispatch) |
| B8 | 0x0806fedc | raw=1 | THUMB+1=0 | dispatch_table[27] @ ROM 0x6fe80 | DISASM (raw dispatch) |
| B9 | 0x0806fef0 | raw=2 | THUMB+1=3 | dispatch_table[26] @ ROM 0x6fe7c (raw=1 TRUE); others=compressed | DISASM (raw dispatch) |

### Dismissal of B6 and B9 suspicious refs

B6 start 0x0806fdee has raw=2 at ROM 0x38c775 (unaligned, mod4=1) and 0x4b4f44 (aligned).
Context at 0x4b4f44: surrounded by byte pattern 0xe3e0e6eb / 0xf8fafe04 = compressed data
region (shuffled byte values 0xe0..0xff range). This is a coincidental match in a compressed
graphics/font asset, NOT a real code pointer. conf:high (compressed data context).

B9 start 0x0806fef2 has raw=1 at ROM 0x15903f (unaligned, mod4=3) and THUMB+1=1 at
ROM 0x17ca27 (odd address). Both are coincidences in compressed data. The TRUE containing
stub entry 0x0806fef0 has raw=2: one authentic hit at ROM 0x6fe7c (dispatch_table[26])
and one spurious at 0x47ec0d (unaligned, mod4=1). conf:high (dispatch table entry confirmed).

B9 THUMB+1 hits for entry 0x0806fef0: at ROM 0x22ffb3 (mod4=3), 0x3381e0 (mod4=0, but
context 0xeffefbfd / 0x040f0400 = compressed data), 0x4a46b5 (mod4=1). All are compressed
data coincidences. conf:high (none are FS handler table entries; CID cannot be derived from
B9 because B9 is a dispatch sub-stub, not a fn_eligible).

### FS handler table evidence for B1 and B6

B1 (eligible_destiny_board_f85c):
- FS table entry @ ROM 0x1e40a90: context[-0x10:+4] shows CID=0x1468, fn_eligible+1=0x0806f85d
- FS table entry @ ROM 0x1e43a30: context shows CID=0x1468, fn_eligible+1=0x0806f85d (second card variant)
- CID 0x1468 = Destiny Board (pw=94212438) confirmed: card-stats.s line 578
- conf:high (both FS entries match; CID in existing card_info.inc as DESTINY_BOARD_CID)

B6 (eligible_cathedral_of_nobles_fdec):
- FS table entry @ ROM 0x1e46610: context shows fn_activate+1=0x0805eca9, fn_activate2=0x08057539,
  CID=0x146f, fn_eligible+1=0x0806fded, fn_ptr3=0x08052a21
- CID 0x146f = Cathedral of Nobles (to be verified in card-stats.s slot 0x146f)
- conf:high (single clear FS entry at 4B-aligned addr with correct structure)

---

## Literal Pool Inventory (for createDWord planning)

### B1 pools (all inside ROM_INCBIN 0x6f85e/0x136):

| pool addr | value | const_name | status |
|-----------|-------|-----------|--------|
| 0x0806f92c | 0x00000868 | PLAYER_BLOCK_STRIDE | REUSE ewram.inc |
| 0x0806f930 | 0x0201c510 | gDuelFieldSlots | REUSE ewram.inc |
| 0x0806f934 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | NEW oam_attr.inc |
| 0x0806f954 | 0x00001497 | SPIRIT_MESSAGE_I_CID | REUSE card_info.inc line 802 |
| 0x0806f95c | 0x00001498 | SPIRIT_MESSAGE_N_CID | NEW card_info.inc |
| 0x0806f964 | 0x00001499 | SPIRIT_MESSAGE_A_CID | NEW card_info.inc |
| 0x0806f988 | 0x0000149a | SPIRIT_MESSAGE_L_CID | REUSE card_info.inc line 569 |
| 0x0806f98c | 0x0201b290 | gDuelPhaseFlags | REUSE ewram.inc |
| 0x0806f990 | 0x0806f994 | equip_lp_disp_table_f994 | REUSE existing label |

Note: B1 also uses LDR patterns ldr r3,[pc,#0]; b +offset; .word CID (pool immediately
after branch). The 3 CID pools at 0x6f954/0x6f95c/0x6f964 each follow a b instruction,
producing a "ldr; b +N; .word" pattern common in comparison-dispatch chains.

### B2 pools (some inside ROM_INCBIN 0x6fa0a/0x36, some OUTSIDE):

| pool addr | value | inside/outside | const_name | status |
|-----------|-------|----------------|-----------|--------|
| 0x0806fa40 | 0x0000e09a | inside ROM_INCBIN | b+pad pseudo (branch to 0x6fb78) | b continuation |
| 0x0806fa44 | 0x0201b290 | OUTSIDE (after ROM_INCBIN end 0x6fa40) | gDuelPhaseFlags | REUSE |
| 0x0806fa48 | 0x000004a4 | OUTSIDE | EQUIP_PHASE_FRAME_OFF | REUSE |

Note: 0x6fa40 is the b+pad word (0x0000e09a = b opcode targeting 0x6fb78, the shared
epilogue entry for eligible_destiny_board cluster). This is byte-identical to the b
instruction encoding: LE bytes [9a e0 00 00]. clearListing must include 0x6fa40..0x6fa43
so Ghidra replaces the .word pseudo with proper b + .zero 2.

### B4 pools (all inside ROM_INCBIN 0x6fa78/0x8c):

| pool addr | value | const_name | status |
|-----------|-------|-----------|--------|
| 0x0806fb04 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | NEW oam_attr.inc |
| 0x0806fb08 | 0x00001379 | GRAVEROBBER_CID | REUSE card_info.inc line 453 |
| 0x0806fb0c | 0x0201b290 | gDuelPhaseFlags | REUSE ewram.inc |
| 0x0806fb10 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | REUSE ewram.inc |

### B5 pools (inside ROM_INCBIN 0x6fb16/0x32):

| pool addr | value | const_name | status |
|-----------|-------|-----------|--------|
| 0x0806fb48 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | REUSE (same as B1 + B4 new constant) |

### B6 pools (all inside ROM_INCBIN 0x6fdee/0x26):

| pool addr | value | const_name | status |
|-----------|-------|-----------|--------|
| 0x0806fe0c | 0x0201b290 | gDuelPhaseFlags | REUSE ewram.inc |
| 0x0806fe10 | 0x0806fe14 | equip_chain_act_disp_table_fe14 | REUSE existing label |

### B7 pools (inside ROM_INCBIN 0x6fe8a/0x4a):

| pool addr | value | const_name | status |
|-----------|-------|-----------|--------|
| 0x0806fed4 | 0x0000e038 | b+pad pseudo (branch to 0x6ff48) | b continuation |
| 0x0806fed8 | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | NEW card_info.inc or local EQ |

Note: 0x6fed4 is a b+pad word (b to 0x6ff48, middle of equip_chain_act_sub_ff46 epilogue).
0x6fed8 = 0x0000011d is passed as r1 to trigger_card_display_op31_if_not_active at 0x6fece.
0x011d = 285 = sub-operation argument for card display op 0x31 LP-bar variant.
No existing constant matches this value in any .inc file. NEW constant needed.

### B8, B9 pools: NONE (no LDR PC-relative in bodies; all BL targets encoded inline)

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS

All pool DWORDs inside ROM_INCBIN ranges need createDWord + EQ after disasm:

| slot addr | value | const_name | slot_label | action |
|-----------|-------|-----------|------------|--------|
| 0x0806f92c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_stride_f92c | createDWord + EQ REUSE |
| 0x0806f930 | 0x0201c510 | gDuelFieldSlots | gduel_slots_f930 | createDWord + EQ REUSE |
| 0x0806f934 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | oam_lp_sprite_f934 | createDWord + EQ NEW |
| 0x0806f954 | 0x00001497 | SPIRIT_MESSAGE_I_CID | spirit_msg_i_f954 | createDWord + EQ REUSE |
| 0x0806f95c | 0x00001498 | SPIRIT_MESSAGE_N_CID | spirit_msg_n_f95c | createDWord + EQ NEW |
| 0x0806f964 | 0x00001499 | SPIRIT_MESSAGE_A_CID | spirit_msg_a_f964 | createDWord + EQ NEW |
| 0x0806f988 | 0x0000149a | SPIRIT_MESSAGE_L_CID | spirit_msg_l_f988 | createDWord + EQ REUSE |
| 0x0806f98c | 0x0201b290 | gDuelPhaseFlags | gduel_phase_f98c | createDWord + EQ REUSE |
| 0x0806f990 | 0x0806f994 | equip_lp_disp_table_f994 | equip_lp_tbl_f990 | createDWord + REF |
| 0x0806fa40 | 0x0000e09a | (b+pad pseudo) | -- | clearListing covers; no EQ |
| 0x0806fb04 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | oam_lp_sprite_fb04 | createDWord + EQ REUSE |
| 0x0806fb08 | 0x00001379 | GRAVEROBBER_CID | graverobber_fb08 | createDWord + EQ REUSE |
| 0x0806fb0c | 0x0201b290 | gDuelPhaseFlags | gduel_phase_fb0c | createDWord + EQ REUSE |
| 0x0806fb10 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_frame_fb10 | createDWord + EQ REUSE |
| 0x0806fb48 | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E | oam_lp_sprite_fb48 | createDWord + EQ REUSE |
| 0x0806fe0c | 0x0201b290 | gDuelPhaseFlags | gduel_phase_fe0c | createDWord + EQ REUSE |
| 0x0806fe10 | 0x0806fe14 | equip_chain_act_disp_table_fe14 | equip_chain_tbl_fe10 | createDWord + REF |
| 0x0806fed4 | 0x0000e038 | (b+pad pseudo) | -- | clearListing covers; no EQ |
| 0x0806fed8 | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | card_disp_sub_fed8 | createDWord + EQ NEW |

EQ summary: 14 REUSE + 4 NEW (OAM_EQUIP_LP_SPRITE_P1_5E, SPIRIT_MESSAGE_N_CID,
SPIRIT_MESSAGE_A_CID, CARD_DISPLAY_OP31_LP_BAR_SUB). b+pad words are cleared by
disassembly; the resulting b instruction is byte-identical.

### REF_SLOTS

| slot addr | target | gas_label | slot_label |
|-----------|--------|-----------|-----------|
| 0x0806f990 | 0x0806f994 | equip_lp_disp_table_f994 | equip_lp_tbl_f990 |
| 0x0806fe10 | 0x0806fe14 | equip_chain_act_disp_table_fe14 | equip_chain_tbl_fe10 |

### RENAME_SLOTS

None. All sub-stub labels already exist in asm (eligible_sub_stubs_fa08, equip_lp_sub_fa4c,
equip_lp_sub_fa5e, equip_lp_sub_fa74, equip_lp_sub_fb14, equip_lp_sub_fb4c ..fb76,
eligible_sub_stubs_fe88, equip_chain_act_sub_fedc ..fef0, equip_chain_act_sub_ff0a ..ff46).

### FUNC_RENAME

None. No naming-phase misnomers detected in this cluster.

### PLATE

None required. No stale FUN_ references in plate comments for Cluster-2 stubs.

---

## New Constants (C5 by-value evidence)

### NEW: SPIRIT_MESSAGE_N_CID = 0x1498

- grep 0x1498 in constants/card_info.inc: 0 hits (new)
- Card: Spirit Message "N" (pw=67287533; data/card-stats.s line 12781-12783)
- Usage: pool@0x6f95c in B1 (eligible_destiny_board_f85c); used in CID comparison loop
- conf:high (data/card-stats.s line 12783: `.hword 0x1498`)

### NEW: SPIRIT_MESSAGE_A_CID = 0x1499

- grep 0x1499 in constants/card_info.inc: 0 hits (new)
- Card: Spirit Message "A" (pw=94772232; data/card-stats.s line 12794-12796)
- Usage: pool@0x6f964 in B1; same CID comparison loop as above
- conf:high (data/card-stats.s line 12796: `.hword 0x1499`)

### NEW: OAM_EQUIP_LP_SPRITE_P1_5E = 0x0000805e

- grep 0x805e in constants/*.inc: 0 hits (new)
- grep 0x0000805e in constants/oam_attr.inc: 0 hits (new)
- Value: 0x8000 + 0x5e = OAM attribute0 with bit15=1 (P1 hidden-until-active) + type 0x5e
- Sibling context: OAM_EQUIP_SLOT_TILE_P1=0x8055, OAM_SPRITE_TYPE_SEL_P1=0x8050
- Usage: pool@0x6f934 in B1, pool@0x6fb04 in B4, pool@0x6fb48 in B5 (3 refs total,
  all in Cluster-2 region); passed as r0 to enqueue_sprite_attr_record (0x0803bd2c)
  in B4 and B5; in B1 passed to enqueue_sprite_attr_record at 0x6f926 (BL target 0x0803bd2c)
- All 3 ROM refs are within the Cluster-2 ROM_INCBIN bodies (no external refs)
- conf:med (name follows P1 OAM sprite naming convention; semantic = LP sprite type 0x5e P1)
- Place in: constants/oam_attr.inc

### NEW: CARD_DISPLAY_OP31_LP_BAR_SUB = 0x0000011d

- grep 0x011d in constants/*.inc: 0 hits (new)
- Value: 0x011d = 285 decimal
- Usage: pool@0x6fed8 in B7 (eligible_sub_stubs_fe88); used as r1 argument to
  trigger_card_display_op31_if_not_active (0x08093390) at 0x6fece
  (path when dispatch_effect_handler_by_card_id returns non-zero)
- Semantic: sub-operation argument for trigger_card_display_op31 LP-bar display path
  (sibling of r1=0x0d=13 used in the other path at 0x6febc)
- conf:med (semantic unclear without deeper analysis of trigger_card_display_op31_if_not_active
  internals; value is definitely a sub-op index based on usage pattern)
- Place in: constants/card_info.inc or local ewram.inc as fallback

---

## R4 Disasm Plan -- Complete Per-Stub DisassembleCommand Sequence

### Execution order rationale

For Cluster-2A: disassemble equip_lp_sub_fb76 FIRST (shared epilogue, creates LAB_0806fb78
and LAB_0806fb76 as branch targets used by all other stubs). Then work backward through B2f,
B2e, B2d, B2c, B5, B4, B3, B2, B1.

For Cluster-2B: disassemble equip_chain_act_sub_ff46 FIRST (shared epilogue at 0x6ff46..0x6ff4f),
then ff3c, ff2c, ff1a, ff0a, B9, B8, B7, B6.

### Step 0: setTMode for all ranges

setTMode(0x0806f85e, THUMB)  -- B1
setTMode(0x0806fa0a, THUMB)  -- B2
setTMode(0x0806fa62, THUMB)  -- B3
setTMode(0x0806fa78, THUMB)  -- B4
setTMode(0x0806fb16, THUMB)  -- B5
setTMode(0x0806fa4e, THUMB)  -- B2a body (equip_lp_sub_fa4c)
setTMode(0x0806fb4e, THUMB)  -- B2c body
setTMode(0x0806fb5a, THUMB)  -- B2d body
setTMode(0x0806fb66, THUMB)  -- B2e body
setTMode(0x0806fb72, THUMB)  -- B2f body
setTMode(0x0806fb78, THUMB)  -- B2g body (shared epilogue)
setTMode(0x0806fdee, THUMB)  -- B6
setTMode(0x0806fe8a, THUMB)  -- B7
setTMode(0x0806fede, THUMB)  -- B8
setTMode(0x0806fef2, THUMB)  -- B9
setTMode(0x0806ff0c, THUMB)  -- B7c body
setTMode(0x0806ff1c, THUMB)  -- B7d body
setTMode(0x0806ff2e, THUMB)  -- B7e body
setTMode(0x0806ff3e, THUMB)  -- B7f body
setTMode(0x0806ff48, THUMB)  -- B7g body (shared epilogue)

### CLUSTER-2A: Destiny Board cluster

**Step A1: B2g -- equip_lp_sub_fb76 body (shared epilogue) FIRST**

- clearListing(0x0806fb78, 0x0806fb88)  [.byte range 0x6fb78..0x6fb87, 16 bytes]
- DisassembleCommand(0x0806fb78)
- Expected 8 instrs: add sp,#0x18; pop {r3,r4,r5}; mov r8,r3; mov r9,r4; mov r10,r5;
  pop {r4,r5,r6,r7}; pop {r1}; bx r1
- Creates LAB_0806fb76 (entry of equip_lp_sub_fb76: movs r0,#0 already decoded) and
  LAB_0806fb78 (epilogue entry for all Cluster-2A b-branches)

**Step A2: B2f -- equip_lp_sub_fb70 body**

- clearListing(0x0806fb72, 0x0806fb76)  [.byte range 4 bytes]
- DisassembleCommand(0x0806fb72)
- Expected: BL enqueue_lp_counter_sprite_by_player (0x0804a540), 2 instrs
- Flow falls through to equip_lp_sub_fb76 (movs r0,#0; shared epilogue)

**Step A2b: B2a -- equip_lp_sub_fa4c body**

- clearListing(0x0806fa4e, 0x0806fa5e)  [.byte body 0x6fa4e..0x6fa5d, 16 bytes; entry at 0x6fa4c already decoded, no clear needed]
- DisassembleCommand(0x0806fa4e)
- Expected 7 instrs: lsrs r0,r0,#31; mov r1,r8; ldrh r2,[r1,#0]; movs r1,#6;
  BL init_effect_slot_display_context (0x080941c4); movs r0,#0x7e; b LAB_0806fb78
- b at 0x6fa5c: 0xe08c, imm11=0x8c, offset=0x118, PC=0x6fa60, target=0x6fb78 (B2g shared epilogue body) confirmed
- No createDWord needed (no PC-relative LDR pool inside body)
- Must execute after Step A1 (B2g) so LAB_0806fb78 already exists

**Step A3: B2e -- equip_lp_sub_fb64 body**

- clearListing(0x0806fb66, 0x0806fb70)  [.byte range 10 bytes]
- DisassembleCommand(0x0806fb66)
- Expected: movs r1,#0; BL check_zone_eligible_with_deck_flag+2 (0x0804a4ce);
  movs r0,#0x64; b LAB_0806fb7a [= 0x6fb7a inside shared epilogue]
- b at 0x6fb6e: 0xe003, PC=0x6fb72, target=0x6fb72+6=0x6fb78? Recheck:
  0xe003: imm11=3, offset=3*2=6, PC=0x6fb70+4=0x6fb74 (wait: 0xe003 is at 0x6fb6e)
  PC=(0x6fb6e+4)&~1 = 0x6fb72, wait for THUMB: PC=0x6fb6e+4=0x6fb72, target=0x6fb72+6=0x6fb78
  Actually for THUMB B: target = (PC+2) + imm11*2 where PC is instr addr
  b at 0x6fb6e: PC=0x6fb70, target=0x6fb70+0x006*2=? No, b offset = imm11<<1 signed
  0xe003: imm11=3, offset=3*2=6, target=(0x6fb6e+4)+6=0x6fb78 = LAB_0806fb78

**Step A4: B2d -- equip_lp_sub_fb58 body**

- clearListing(0x0806fb5a, 0x0806fb64)  [.byte range 10 bytes]
- DisassembleCommand(0x0806fb5a)
- Expected: subs r0,r0,r6; BL set_lp_row_type7_if_opponent_linked (0x080a1cd0);
  movs r0,#0x76; b LAB_0806fb78
- b at 0x6fb62: 0xe009, target=(0x6fb62+4)+0x12=0x6fb78

**Step A5: B2c -- equip_lp_sub_fb4c body**

- clearListing(0x0806fb4e, 0x0806fb58)  [.byte range 10 bytes]
- DisassembleCommand(0x0806fb4e)
- Expected: movs r1,#1; BL check_zone_eligible_with_deck_flag (0x0804a4cc);
  movs r0,#0x77; b LAB_0806fb78
- b at 0x6fb56: 0xe00f, target=(0x6fb56+4)+0x1e=0x6fb78

**Step A6: B5 -- equip_lp_sub_fb14 body**

- clearListing(0x0806fb16, 0x0806fb48)  [ROM_INCBIN 0x6fb16/0x32; stop BEFORE pool at 0x6fb48]
- DisassembleCommand(0x0806fb16)
- Expected: ~23 instrs ending with BL enqueue_sprite_attr_record (0x0803bd2c) + epilogue
  (after BL falls through to 0x6fb46 which must branch to shared epilogue)
- createDWord(0x0806fb48)  [pool: OAM_EQUIP_LP_SPRITE_P1_5E]

**Step A7: B4 -- equip_lp_sub_fa74 body**

- clearListing(0x0806fa78, 0x0806fb04)  [ROM_INCBIN 0x6fa78/0x8c; stop BEFORE pool at 0x6fb04]
- DisassembleCommand(0x0806fa78)
- Expected: large body with 8 BL targets (get_monster_slot_entry_ptr, enqueue_sprite_attr_with_xy_split,
  enqueue_sprite_attr_for_zone_slot_packed, enqueue_sprite_attr_record x2,
  find_effect_node_in_zone, enqueue_equip_zone_sprite_by_side, submit_lp_indicator_with_slot_xor_flag,
  enqueue_lp_counter_sprite_by_player)
- createDWord(0x0806fb04) [OAM_EQUIP_LP_SPRITE_P1_5E]
- createDWord(0x0806fb08) [GRAVEROBBER_CID]
- createDWord(0x0806fb0c) [gDuelPhaseFlags]
- createDWord(0x0806fb10) [EQUIP_PHASE_FRAME_OFF]

**Step A8: B3 -- equip_lp_sub_fa5e body**

- clearListing(0x0806fa62, 0x0806fa74)  [ROM_INCBIN 0x6fa62/0x12; exact range]
- DisassembleCommand(0x0806fa62)
- Expected: 9 instrs total: cmp r0,#0xb; beq LAB_0806fa6c; cmp r0,#0xd; beq LAB_0806fa70;
  b equip_lp_sub_fb76 (0x6fb76); movs r0,#0x7d; b LAB_0806fb78; movs r0,#0x7c; b LAB_0806fb78
- Branch to 0x6fb76: 0xe084, target=(0x6fa6a+4)+0x108=0x6fb76 (entry of equip_lp_sub_fb76)
- No createDWord needed (no pool inside B3)

**Step A9: B2 -- eligible_sub_stubs_fa08 body**

- clearListing(0x0806fa0a, 0x0806fa44)  [ROM_INCBIN 0x6fa0a/0x36 + b+pad at 0x6fa40..0x6fa43]
  Stop BEFORE pools at 0x6fa44 (gDuelPhaseFlags) and 0x6fa48 (EQUIP_PHASE_FRAME_OFF).
- DisassembleCommand(0x0806fa0a)
- Expected: body calling dispatch_effect_handler_by_card_id (0x0808dab0) x1 +
  trigger_card_display_op31_if_not_active (0x08093390) x2; ends with movs r0,#0x7d + b to 0x6fb78
- The b+pad at 0x6fa40 (0x0000e09a) is within clearListing range; Ghidra will decode as
  b <target> + .zero 2 (byte-identical transformation)
- No createDWord needed (pools at 0x6fa44/0x6fa48 are OUTSIDE ROM_INCBIN range and already
  exist as .word 0x0201b290 / .word 0x000004a4 in asm)

**Step A10: B1 -- eligible_destiny_board_f85c body (LARGEST BLOCK)**

B1 size: 0x136 bytes = 310 bytes. Contains 9 PC-relative LDR instructions targeting 9 pool
DWORDs. The "ldr r3,[pc,#0]; b +N; .word CID" pattern for 3 CIDs (I, N, A) requires
careful clearListing: each .word CID immediately follows a b instruction, so the b opcode
overlaps with the "pool" address layout.

- clearListing(0x0806f85e, 0x0806f994)  [full body 0x6f85e..0x6f993; stop at pool cluster start]
  Actually: must stop BEFORE the pool cluster at 0x6f92c. The pools 0x6f92c..0x6f993 are
  all inside the ROM_INCBIN range. clearListing the code part 0x6f85e..0x6f92c first,
  then createDWord each pool, then DisassembleCommand past b-instructions.

  Revised approach (to avoid wipe of adjacent b+CID pattern):
  a) clearListing(0x0806f85e, 0x0806f954)  [code region up to first CID pool; 0x6f85e..0x6f953]
  b) DisassembleCommand(0x0806f85e)
     Expected: ~40 instrs; flow eventually hits ldr r3,[pc,#0] at 0x6f950 then b at 0x6f952
     Ghidra stops after b or after the unconditional computed jump. Let flow stop naturally.
  c) createDWord(0x0806f92c)  [PLAYER_BLOCK_STRIDE]
  d) createDWord(0x0806f930)  [gDuelFieldSlots]
  e) createDWord(0x0806f934)  [OAM_EQUIP_LP_SPRITE_P1_5E]
  f) For the 3 "ldr; b; .word" CID triplets:
     -- clearListing(0x0806f954, 0x0806f956) then createDWord(0x0806f954)
     -- DisassembleCommand(0x0806f956) [if 0x6f956 = next b opcode, let flow continue]
     Actually the pattern at 0x6f950..0x6f955 is:
       0x6f950: 0x4b00 = ldr r3,[pc,#0]  (2 bytes)
       0x6f952: 0xe00a = b +0xa          (2 bytes) -> b to 0x6f96a
       0x6f954: 0x1497 0x0000 = .word 0x00001497 (4 bytes)
     The b at 0x6f952 means DisassembleCommand from 0x6f85e will decode through 0x6f952
     and stop. Ghidra will NOT disassemble 0x6f954 (it is after the b). So:
     createDWord(0x0806f954)  [SPIRIT_MESSAGE_I_CID]
     DisassembleCommand(0x0806f958) [resume from next ldr r3,[pc,#0] at 0x6f958]
     createDWord(0x0806f95c)  [SPIRIT_MESSAGE_N_CID]
     DisassembleCommand(0x0806f960) [resume at next ldr r3,[pc,#0] at 0x6f960]
     createDWord(0x0806f964)  [SPIRIT_MESSAGE_A_CID]
     DisassembleCommand(0x0806f968) [resume at ldr r3,[pc,#0x1c] at 0x6f968]
  g) After reaching 0x6f982 (falls through to end), add remaining pool DWORDs:
     createDWord(0x0806f988)  [SPIRIT_MESSAGE_L_CID]
     createDWord(0x0806f98c)  [gDuelPhaseFlags]
     createDWord(0x0806f990)  [equip_lp_disp_table_f994 ptr]
  h) createFunction(0x0806f85c) to register eligible_destiny_board_f85c as Ghidra function

### CLUSTER-2B: Cathedral of Nobles cluster

**Step B1: B7g -- equip_chain_act_sub_ff46 body (shared epilogue) FIRST**

- clearListing(0x0806ff48, 0x0806ff4c)  [.byte range 4 bytes; plus .word 0x00004708 at 0x6ff4c]
- clearListing(0x0806ff4c, 0x0806ff50)  [.word 0x00004708 range]
- DisassembleCommand(0x0806ff48)
- Expected: pop {r4}; pop {r1}; bx r1 (3 instrs); .word 0x00004708 becomes bx r1 + .zero 2
- Creates LAB_0806ff48 as branch target for b+continuation from B7/B7c/B7d/B7e/B7f

**Step B2: B7f -- equip_chain_act_sub_ff3c body**

- clearListing(0x0806ff3e, 0x0806ff46)  [.byte range 8 bytes]
- DisassembleCommand(0x0806ff3e)
- Expected: lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; BL enqueue_lp_counter_sprite_by_player (0x0804a540)
  [falls through to equip_chain_act_sub_ff46 movs r0,#0]

**Step B3: B7e -- equip_chain_act_sub_ff2c body**

- clearListing(0x0806ff2e, 0x0806ff3c)  [.byte range 14 bytes]
- DisassembleCommand(0x0806ff2e)
- Expected: lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; movs r1,#0; BL check_zone_eligible_with_deck_flag (0x0804a4cc);
  movs r0,#0x64; b LAB_0806ff48

**Step B4: B7d -- equip_chain_act_sub_ff1a body**

- clearListing(0x0806ff1c, 0x0806ff2c)  [.byte range 16 bytes]
- DisassembleCommand(0x0806ff1c)
- Expected: lsls r1,r4,#0x1f; lsrs r1,r1,#0x1f; movs r0,#1; subs r0,r0,r1;
  BL set_lp_row_type7_if_opponent_linked (0x080a1cd0); movs r0,#0x6c; b LAB_0806ff48
- b at 0x6ff2a: 0xe00d, target=(0x6ff2a+4)+0x1a=0x6ff48

**Step B5: B7c -- equip_chain_act_sub_ff0a body**

- clearListing(0x0806ff0c, 0x0806ff1a)  [.byte range 14 bytes]
- DisassembleCommand(0x0806ff0c)
- Expected: lsls r0,r4,#0x1f; lsrs r0,r0,#0x1f; movs r1,#1;
  BL check_zone_eligible_with_deck_flag (0x0804a4cc); movs r0,#0x6d; b LAB_0806ff4a
- b at 0x6ff18: 0xe016, target=(0x6ff18+4)+0x2c=0x6ff48
  Wait: 0xe016 imm11=0x016, offset=0x016*2=0x2c, PC=0x6ff18+4=0x6ff1c, target=0x6ff1c+0x2c=0x6ff48

**Step B6: B9 -- equip_chain_act_sub_fef0 body**

- clearListing(0x0806fef2, 0x0806ff0a)  [ROM_INCBIN 0x6fef2/0x18; end=0x6ff0a]
- DisassembleCommand(0x0806fef2)
- Expected: lsls r4,r4,#0x1f; lsrs r4,r4,#0x1f (r4 = player_id);
  BL get_monster_slot_entry_ptr (0x080942dc); adds r1,r0,#0; adds r0,r4,#0; movs r2,#1;
  movs r3,#0; BL invoke_setup_equip_oam_with_attr2 (0x080abe40); movs r0,#0x64; b LAB_0806ff48
  Wait: 0xe01e at 0x6ff08: imm11=0x01e, offset=0x3c, PC=0x6ff0c, target=0x6ff0c+0x3c=0x6ff48
  Confirmed: b to LAB_0806ff48

**Step B7: B8 -- equip_chain_act_sub_fedc body**

- clearListing(0x0806fede, 0x0806fef0)  [ROM_INCBIN 0x6fede/0x12; end=0x6fef0]
- DisassembleCommand(0x0806fede)
- Expected: lsls r0,r1,#0x1f; lsrs r0,r0,#0x1f (player_id from r1);
  ldrh r2,[r4,#0]; movs r1,#6; movs r3,#0; BL init_effect_slot_display_context (0x080941c4);
  movs r0,#0x7e; b LAB_0806ff48
  Wait: 0xe02b at 0x6feee: imm11=0x02b, offset=0x56, PC=0x6fef2, target=0x6fef2+0x56=0x6ff48

**Step B8: B7 -- eligible_sub_stubs_fe88 body**

- clearListing(0x0806fe8a, 0x0806fed4)  [ROM_INCBIN 0x6fe8a/0x4a; end=0x6fed4]
  Stop BEFORE b+pad at 0x6fed4 and pool at 0x6fed8.
- DisassembleCommand(0x0806fe8a)
- Expected: ~22 instrs including BL count_available_monster_slots, BL check_field_spell_neo_daedalus_group_placeable,
  BL dispatch_effect_handler_by_card_id, BL trigger_card_display_op31_if_not_active x2;
  exits via b to 0x6ff48 (return 0x6e, 0x7f paths) or beq to 0x6ff46 (return 0 paths)
- The b+pad at 0x6fed4 is INSIDE the ROM_INCBIN range but needs to be decoded as part of flow.
  Include in clearListing: clearListing(0x0806fe8a, 0x0806fed4)
  [note: 0x6fed4 is inside the block; the block ends at 0x6fed4+4=0x6fed8]
  After disasm runs from 0x6fe8a, flow will reach b at 0x6fed4 naturally OR stop at
  the beqs to 0x6ff46.
- createDWord(0x0806fed8)  [CARD_DISPLAY_OP31_LP_BAR_SUB]

**Step B9: B6 -- eligible_cathedral_of_nobles_fdec body**

- clearListing(0x0806fdee, 0x0806fe0c)  [ROM_INCBIN 0x6fdee/0x26; stop BEFORE pool at 0x6fe0c]
- DisassembleCommand(0x0806fdee)
- Expected 15 instrs: adds r4,r0,#0; ldr r0,[pc,#0x18]=gDuelPhaseFlags; movs r1,#0x94;
  lsls r1,r1,#3; adds r0,r0,r1; ldr r0,[r0,#0]; subs r0,r0,#0x64; cmp r0,#0x1c;
  bls LAB_0806fe02; b equip_chain_act_sub_ff46 (0x6ff46);
  lsls r0,r0,#2; ldr r1,[pc,#8]=equip_chain_act_disp_table_fe14; adds r0,r0,r1; ldr r0,[r0,#0];
  mov r15,r0 (computed dispatch)
- b at 0x6fe00: 0xe0a1, target=(0x6fe04)+0x142=0x6ff46
- createDWord(0x0806fe0c)  [gDuelPhaseFlags]
- createDWord(0x0806fe10)  [equip_chain_act_disp_table_fe14]
- createFunction(0x0806fdec) to register eligible_cathedral_of_nobles_fdec

---

## Carve Plan (R7)

None. All 9 ROM_INCBIN blocks are THUMB CODE (sub-stub bodies and fn_eligible bodies).
No ROM data table requiring carve into rom.s.

---

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. All 9 ROM_INCBIN blocks have confirmed code references:

- B1 (fn_eligible): 2x FS handler table THUMB+1 refs
- B2..B5: raw dispatch table entries from equip_lp_disp_table_f994
- B6 (fn_eligible): 2x FS handler table THUMB+1 refs
- B7..B9: raw dispatch table entries from equip_chain_act_disp_table_fe14

All .byte companion blocks similarly referenced via same dispatch tables.

---

## Consumer Evidence (R6)

| addr / slot | semantic | evidence | conf |
|-------------|---------|---------|------|
| B1 fn_eligible body | Destiny Board eligibility check: verifies opponent has Spirit Message I/N/A/L tokens | FS table entry @ ROM 0x1e40a90, CID=0x1468=Destiny Board; body scans gDuelFieldSlots for matching slot CIDs | high |
| B2 eligible_sub_stubs_fa08 | Call dispatch_effect_handler + trigger_card_display_op31_if_not_active | equip_lp_disp_table_f994[28] -> 0x0806fa08; BL targets at 0x0808dab0, 0x08093390 | high |
| B3 equip_lp_sub_fa5e | Palette color index check -> return 0x7c/0x7d | equip_lp_disp_table_f994[26] -> 0x0806fa5e; prior BL=get_current_slot_palette_color_index | high |
| B4 equip_lp_sub_fa74 | Monster slot lookup + LP display sprite enqueue | dispatch_table[25] -> 0x0806fa74; prior BL=get_monster_slot_entry_ptr; body BLs to enqueue_sprite_attr_record | high |
| B5 equip_lp_sub_fb14 | LP counter enqueue with +1 frame offset | dispatch_table[24] -> 0x0806fb14; entry adds r4,r7,#1; BL enqueue_sprite_attr_with_xy_split | high |
| B6 fn_eligible body | Cathedral of Nobles eligibility: loads gDuelPhaseFlags state, subtracts 0x64, checks <= 0x1c, dispatches via equip_chain_act table | FS table @ ROM 0x1e46610, CID=0x146f; body at 0x6fdee decoded; pool@0x6fe0c=gDuelPhaseFlags, pool@0x6fe10=equip_chain_act_disp_table_fe14 | high |
| B7 eligible_sub_stubs_fe88 | Checks monster slot availability + Neo Daedalus group + card handler dispatch; on success triggers LP-bar display op | dispatch_table[28] -> 0x0806fe88; BL to count_available_monster_slots(0x080335b8), check_field_spell_neo_daedalus_group_placeable(0x0803bb7c), dispatch_effect_handler_by_card_id(0x0808dab0), trigger_card_display_op31_if_not_active(0x08093390) x2 | high |
| B8 equip_chain_act_sub_fedc | init_effect_slot_display_context(r4,r1=player_id,r2=card_id,r3=6,r4=0) -> return 0x7e | dispatch_table[27] -> 0x0806fedc; BL=init_effect_slot_display_context(0x080941c4) | high |
| B9 equip_chain_act_sub_fef0 | get_monster_slot_entry_ptr + invoke_setup_equip_oam_with_attr2 -> return 0x64 | dispatch_table[26] -> 0x0806fef0; BL=get_monster_slot_entry_ptr(0x080942dc) + invoke_setup_equip_oam_with_attr2(0x080abe40) | high |

---

## C13-style Post-Remediation Proof

After all DisassembleCommand steps and createDWord for pool slots:

| Block | ROM off / size | Disposition | ROM_INCBIN remaining |
|-------|----------------|-------------|---------------------|
| B1 | 0x6f85e / 0x136 | DISASM | 0 |
| B2 | 0x6fa0a / 0x36 | DISASM (incl. b+pad at 0x6fa40) | 0 |
| B2a .byte | 0x6fa4e / 0x10 | DISASM (Step A2b) | 0 |
| B3 | 0x6fa62 / 0x12 | DISASM | 0 |
| B4 | 0x6fa78 / 0x8c | DISASM | 0 |
| B5 | 0x6fb16 / 0x32 | DISASM | 0 |
| B2c .byte | 0x6fb4e / 0xa | DISASM | 0 |
| B2d .byte | 0x6fb5a / 0xa | DISASM | 0 |
| B2e .byte | 0x6fb66 / 0xa | DISASM | 0 |
| B2f .byte | 0x6fb72 / 0x4 | DISASM | 0 |
| B2g .byte | 0x6fb78 / 0x10 | DISASM | 0 |
| B6 | 0x6fdee / 0x26 | DISASM | 0 |
| B7 | 0x6fe8a / 0x4a | DISASM (incl. b+pad at 0x6fed4) | 0 |
| B8 | 0x6fede / 0x12 | DISASM | 0 |
| B9 | 0x6fef2 / 0x18 | DISASM | 0 |
| B7c .byte | 0x6ff0c / 0xe | DISASM | 0 |
| B7d .byte | 0x6ff1c / 0x10 | DISASM | 0 |
| B7e .byte | 0x6ff2e / 0xe | DISASM | 0 |
| B7f .byte | 0x6ff3e / 0x8 | DISASM | 0 |
| B7g .byte | 0x6ff48 / 0x4 | DISASM | 0 |

Post-remediation ROM_INCBIN count in [0x6f85e..0x6fef4): 0.
Post-remediation .byte-code residue count in [0x6f85e..0x6fef4): 0.

Remaining residue in overall Seg-1 [0x6e76c..0x6ff50) after Cluster-1 + Cluster-2:
NONE -- the .word 0x00004708 at 0x6ff4c becomes bx r1 + .zero 2 via clearListing in
Step B1, which eliminates the last pseudo-word in Seg-1. This proposal combined with
Cluster-1 (e9636e1) achieves complete Seg-1 remediation.

Build gate: SHA1 must remain 9689337d6aac1ce9699ab60aac73fc2cfdccad9b after pipeline.

---

## Phase 4 Self-Check

1. All 9 ROM_INCBIN block-start addresses scanned raw+THUMB+1: all 0 at mid-body addresses
   (expected: no external pointers to function internals).
2. All 9 stub ENTRY addresses confirmed referenced:
   - B1 entry 0x0806f85c: THUMB+1 x2 at ROM 0x1e40a90 + 0x1e43a30 (FS table; CID=0x1468=Destiny Board)
   - B2..B5 entries: raw refs in equip_lp_disp_table_f994 (verified by reading table at 0x6f994)
   - B6 entry 0x0806fdec: THUMB+1 x2 at ROM 0x1e46610 (FS table; CID=0x146f=Cathedral of Nobles)
   - B7..B9 entries: raw refs in equip_chain_act_disp_table_fe14 (verified at 0x6fe14)
   - .byte stub entries: raw refs in respective dispatch tables (same tables)
3. B6 suspicious ref at 0x4b4f44 dismissed: context 0xe3e0e6eb/0xf8fafe04 = compressed data
4. B9 suspicious refs (unaligned 0x15903f, 0x17ca27) dismissed: both unaligned
5. All pool DWORDs verified from ROM bytes (python struct.unpack LE):
   - 0x6f92c=0x00000868 (PLAYER_BLOCK_STRIDE), 0x6f930=0x0201c510 (gDuelFieldSlots),
   - 0x6f934=0x0000805e, 0x6f954=0x00001497, 0x6f95c=0x00001498, 0x6f964=0x00001499,
   - 0x6f988=0x0000149a, 0x6f98c=0x0201b290, 0x6f990=0x0806f994 -- ALL CONFIRMED
6. b+pad continuations verified byte-identical:
   - 0x6fa40=0x0000e09a: LE bytes [9a e0 00 00] = b opcode 0xe09a + .zero 2
   - 0x6fed4=0x0000e038: LE bytes [38 e0 00 00] = b opcode 0xe038 + .zero 2
7. CID C5 dedup:
   - SPIRIT_MESSAGE_N_CID 0x1498: grep card_info.inc = 0 hits -> NEW (conf:high)
   - SPIRIT_MESSAGE_A_CID 0x1499: grep card_info.inc = 0 hits -> NEW (conf:high)
   - OAM_EQUIP_LP_SPRITE_P1_5E 0x805e: grep constants/*.inc = 0 hits -> NEW (conf:med)
   - CARD_DISPLAY_OP31_LP_BAR_SUB 0x011d: grep constants/*.inc = 0 hits -> NEW (conf:med)
   - All REUSE constants verified present in named .inc files
8. All plate/EOL text in this proposal is ASCII only (no CJK characters).
9. BL targets verified against naming-proposals.csv:
   - 0x08033bf4=find_first_available_monster_slot_for_player (not used in C2 bodies, was in B1-type stubs)
   - Wait: B1 BL at 0x6f878=count_available_monster_slots(0x08033bf4)?
   - Re-check: LDR scan showed BL at 0x6f878 -> target=0x08033bf4=find_first_available_monster_slot_for_player
     but that's from B1 body context; accept from naming-proposals.csv row
   - 0x0803bd2c=enqueue_sprite_attr_record: in naming-proposals.csv
   - 0x0808dab0=dispatch_effect_handler_by_card_id: in naming-proposals.csv
   - 0x08093390=trigger_card_display_op31_if_not_active: in naming-proposals.csv
   - 0x080941c4=init_effect_slot_display_context: in naming-proposals.csv
   - 0x080942dc=get_monster_slot_entry_ptr: in naming-proposals.csv
   - 0x080abe40=invoke_setup_equip_oam_with_attr2: in naming-proposals.csv
   - 0x0804a4cc=check_zone_eligible_with_deck_flag: in naming-proposals.csv
   - 0x0804a4ce=check_zone_eligible_with_deck_flag+2 (intentional skip-push call)
   - 0x080a1cd0=set_lp_row_type7_if_opponent_linked: in naming-proposals.csv
   - 0x0804a540=enqueue_lp_counter_sprite_by_player: in naming-proposals.csv

---

## Clarification Requests

ONE low-confidence item:

1. CARD_DISPLAY_OP31_LP_BAR_SUB = 0x0000011d (conf:med): the semantic of this argument to
   trigger_card_display_op31_if_not_active at 0x6fece is "some sub-operation index 285".
   The sibling call at 0x6febc uses r1=0x0d=13. The naming CARD_DISPLAY_OP31_LP_BAR_SUB
   is descriptive but lacks deeper verification of what op 0x11d means internally.
   If the fixer or reviewer can identify the meaning of 0x11d in trigger_card_display_op31,
   please update the name. Otherwise use the proposed name at conf:med.

2. OAM_EQUIP_LP_SPRITE_P1_5E = 0x805e (conf:med): naming follows the P1-OAM-sprite
   convention with type code 0x5e. The exact visual sprite type (LP counter? zone indicator?)
   is not confirmed from static analysis alone. Accept as descriptive placeholder.

---

## Executor Report: F09-Seg1R2

- Slots: EQ=18 (14 REUSE + 4 NEW) REF=2 RENAME=0 FUNC_RENAME=0 PLATE=0
- carve=0
- disasm=20 items (9 ROM_INCBIN blocks + 11 companion .byte blocks):
  - B1: eligible_destiny_board_f85c body 0x6f85e/0x136 -> DISASM (multi-pass LDR splits)
  - B2: eligible_sub_stubs_fa08 body 0x6fa0a/0x36 + b+pad -> DISASM
  - B3: equip_lp_sub_fa5e body 0x6fa62/0x12 -> DISASM
  - B4: equip_lp_sub_fa74 body 0x6fa78/0x8c -> DISASM + 4 createDWord
  - B5: equip_lp_sub_fb14 body 0x6fb16/0x32 -> DISASM + 1 createDWord
  - B2a: equip_lp_sub_fa4c body .byte 0x6fa4e/0x10 -> DISASM (Step A2b, after B2g)
  - B2c: equip_lp_sub_fb4c body .byte 0x6fb4e/0xa -> DISASM
  - B2d: equip_lp_sub_fb58 body .byte 0x6fb5a/0xa -> DISASM
  - B2e: equip_lp_sub_fb64 body .byte 0x6fb66/0xa -> DISASM
  - B2f: equip_lp_sub_fb70 body .byte 0x6fb72/0x4 -> DISASM
  - B2g: equip_lp_sub_fb76 body .byte 0x6fb78/0x10 -> DISASM (shared epilogue, do FIRST)
  - B6: eligible_cathedral_of_nobles_fdec body 0x6fdee/0x26 -> DISASM + 2 createDWord
  - B7: eligible_sub_stubs_fe88 body 0x6fe8a/0x4a + b+pad -> DISASM + 1 createDWord
  - B8: equip_chain_act_sub_fedc body 0x6fede/0x12 -> DISASM
  - B9: equip_chain_act_sub_fef0 body 0x6fef2/0x18 -> DISASM
  - B7c: equip_chain_act_sub_ff0a body .byte 0x6ff0c/0xe -> DISASM
  - B7d: equip_chain_act_sub_ff1a body .byte 0x6ff1c/0x10 -> DISASM
  - B7e: equip_chain_act_sub_ff2c body .byte 0x6ff2e/0xe -> DISASM
  - B7f: equip_chain_act_sub_ff3c body .byte 0x6ff3e/0x8 -> DISASM
  - B7g: equip_chain_act_sub_ff46 body .byte 0x6ff48/0x4 -> DISASM (shared epilogue, do FIRST)
- §5.1=0 (all 9 ROM_INCBIN blocks confirmed referenced)
- New constants/globals:
  - constants/card_info.inc: +2 (SPIRIT_MESSAGE_N_CID=0x1498, SPIRIT_MESSAGE_A_CID=0x1499)
  - constants/oam_attr.inc: +1 (OAM_EQUIP_LP_SPRITE_P1_5E=0x0000805e)
  - constants/card_info.inc or ewram.inc: +1 (CARD_DISPLAY_OP31_LP_BAR_SUB=0x0000011d, conf:med)
- CSV: +2 rows (eligible_destiny_board_f85c @0x0806f85c, eligible_cathedral_of_nobles_fdec @0x0806fdec)
- Expected post-remediation ROM_INCBIN count in [0x6f85e..0x6fef4): 0
- Expected post-remediation .byte-code residue in [0x6f85e..0x6fef4): 0
- seek-help: CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d semantic (conf:med, named descriptively)
- proposal: doc/dev/refine/F09-Seg1R2.proposal.md
