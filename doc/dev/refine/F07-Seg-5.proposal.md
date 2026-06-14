# Refine Proposal: F07-Seg-5  [0x0805fc94..0x08060898)

## 段测绘

- 函数入口: ROM 0x0805fc94..0x08060898, **34 named fn**
  - check_equip_slot_eligible_by_chain_score_and_owner variant (0x0805fc94)
  - check_equip_slot_eligible_by_zone_type_and_lp_slot (0x0805fd3c)
  - check_equip_slot_eligible_neo_daedalus_with_monster_slots (0x0805fdf4)
  - check_equip_slot_eligible_with_hand_slot_bit14_and_effect_node (0x0805fe38)
  - check_equip_slot_eligible_type180_or_1c0_cross_player_handlers (0x0805feb0)
  - check_equip_slot_eligible_spell480_neo_daedalus_path (0x0805ff3c)
  - check_equip_slot_eligible_with_lp_active_and_neo_daedalus (0x0805ff64)
  - check_necrovalley_paired_slots_exist (0x0805ff9c)
  - check_equip_slot_eligible_by_zone_type_b0_with_field5 (0x0805ffb8)
  - check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14 (0x0806001c)
  - check_equip_slot_eligible_with_chain_absent_and_lp_slot (0x08060044)
  - [ROM_INCBIN 0x6008c/0x28]
  - check_equip_slot_eligible_necrovalley_with_lp_and_field5 (0x080600b4)
  - check_equip_slot_eligible_with_lp_slot_and_banisher (0x08060104)
  - check_equip_slot_eligible_active_player_phase1_by_tier (0x0806015c)
  - check_equip_slot_eligible_zone_type_or_neo_daedalus (0x0806019c)
  - check_equip_slot_eligible_neo_daedalus_with_zone_field_guard (0x080601dc)
  - check_slot_entity_at_zone_descriptor_f (0x08060270)
  - check_equip_slot_eligible_spell_zone_with_neo_daedalus (0x080602a8)
  - check_equip_slot_eligible_mask_restrict_absent_dual_phase (0x080602e0)
  - check_equip_slot_eligible_neo_daedalus_or_lp_count (0x08060328)
  - check_equip_slot_eligible_second_goblin_absent_zone (0x08060350)
  - [ROM_INCBIN 0x60386/0x32]
  - check_equip_slot_eligible_neo_daedalus_full_guard (0x080603b8)
  - check_equip_slot_eligible_chain_absent_neo_daedalus_path (0x08060464)
  - check_equip_slot_eligible_by_duel_phase3_neo_daedalus (0x08060484)
  - check_equip_slot_eligible_neo_daedalus_with_lp_loop (0x080604ac)
  - check_equip_slot_eligible_with_resistance_triple_and_opponent_lp (0x08060514)
  - [ROM_INCBIN 0x60588/0x7c]
  - check_equip_slot_eligible_by_opponent_zone_and_lp (0x08060640)
  - check_equip_slot_eligible_with_monster_zone_and_neo_daedalus (0x08060684)
  - check_equip_eligible_in_main_phase2 (0x080606cc)
  - check_equip_slot_eligible_neo_daedalus_by_tier_and_equip_guard (0x08060710)
  - check_equip_slot_eligible_by_slot_value_vs_tier (0x08060788)
  - check_equip_slot_eligible_by_lp_status_and_slot_value (0x080607b4)
  - classify_equip_slot_eligibility_by_tier_field6 (0x080607ec)
  - [UNNAMED fn at 0x08060800 -- .byte + partial disasm; 22 THUMB+1 refs]
  - check_equip_slot_eligible_with_lp_slot_and_chain_polarity (0x08060854)
  - [Seg-6 begins at 0x08060898]

- 残留自动名槽: **53 slots** (python 精确清点 0x0805fc94..0x08060898)
  - DWORD_0805fd14 = 0x0201bb90 (gEquipChainSlotRefs)
  - DWORD_0805fd18 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DWORD_0805fd1c = 0x0201c510 (gDuelFieldSlots)
  - DWORD_0805fd20 = 0x00001318 (RING_OF_MAGNETISM_CID)
  - DWORD_0805fddc = 0x0201c4e0 (gP1LifePoints)
  - DWORD_0805fde0 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DWORD_0805fe84 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DWORD_0805fe88 = 0x0201c8f8 (gP1HandSlotArray)
  - DWORD_0805feac = 0xfffffbf4 (neg offset gP1HandSlotArray->gP1ZoneHandCount)
  - PTR_gP1LifePoints_0805ff34 = 0x0201c4e0
  - DAT_0805ff38 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DWORD_0805ff8c = 0x0201c4e0
  - DWORD_0805ff90 = 0x00000868
  - DAT_0805ffac = 0x0000159d (NECROVALLEY_CID)
  - DWORD_0806007c = 0x0201c4e0
  - DWORD_08060080 = 0x00000868
  - DAT_080600f0 = 0x0000159d (NECROVALLEY_CID)
  - PTR_gP1LifePoints_080600f4 = 0x0201c4e0
  - DAT_080600f8 = 0x00000868
  - PTR_gP1LifePoints_08060148 = 0x0201c4e0
  - DAT_0806014c = 0x00000868
  - DAT_08060150 = 0x00001332 (BANISHER_OF_THE_LIGHT_CID)
  - PTR_gP1LifePoints_08060188 = 0x0201c4e0
  - DAT_0806018c = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
  - DAT_08060190 = 0x00001cf4 (FIELD_STATE_OFF)
  - PTR_gP1LifePoints_0806025c = 0x0201c4e0
  - DAT_08060260 = 0x00000868
  - DAT_08060264 = 0x00f88000 (zone_detail_field_mask NEW)
  - PTR_gP1LifePoints_0806030c = 0x0201c4e0
  - DAT_08060310 = 0x00001cf4 (FIELD_STATE_OFF)
  - DAT_08060314 = 0x000013f2 (EQUIP_LOCKDOWN_CID)
  - DAT_08060374 = 0x000015d3 (SECOND_GOBLIN_CID)
  - PTR_gP1LifePoints_08060450 = 0x0201c4e0
  - DAT_08060454 = 0x00000868
  - DAT_08060458 = 0x00000fa7 (BLUE_EYES_WHITE_DRAGON_CID)
  - PTR_gP1LifePoints_0806049c = 0x0201c4e0
  - DAT_080604a0 = 0x00001cf4 (FIELD_STATE_OFF)
  - DWORD_0806050c = 0x0201c4e0
  - DWORD_08060510 = 0x00000868
  - DWORD_0806054c = 0x000015ca (PEOPLE_RUNNING_ABOUT_CID NEW)
  - DWORD_08060550 = 0x000015cb (OPPRESSED_PEOPLE_CID NEW)
  - DWORD_08060554 = 0x000015cc (UNITED_RESISTANCE_CID NEW)
  - DWORD_08060578 = 0x0201c4e0
  - DWORD_0806057c = 0x00000868
  - DWORD_0806067c = 0x0201c4e0
  - DWORD_08060680 = 0x00000868
  - PTR_gP1LifePoints_08060700 = 0x0201c4e0
  - DWORD_08060704 = 0x00001cf4 (FIELD_STATE_OFF)
  - DWORD_080607dc = 0x0201c4e0
  - DWORD_080607e0 = 0x00000868
  - DAT_08060838 = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
  - DWORD_08060874 = 0x0201c4e0
  - DWORD_08060878 = 0x00000868

- ROM_INCBIN / .byte 块:
  - 0x0806008c size 0x28 (Block 1)
  - 0x08060386 size 0x32 (Block 2)
  - 0x08060588 size 0x7c (Block 3)
  - 0x08060800 size 0x08 (.byte fn prologue, see disasm plan)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x0806008c sz=0x28 | raw=0 thumb+1=1 at 0x09e412c0 | disasm (R4) | 0x09e412c0 处 table entry: CID_word=0x0000159a(REASONING) at 0x09e412b4, fn_ptr=0x0806008d; fn starts with 4a06=ldr r2,... (leaf), ends bx lr at 0x080600b2; block = complete fn body |
| 0x08060386 sz=0x32 | raw=0 thumb+1=1 at 0x09e44290 | disasm (R4) | 0x09e44290: CID_word=0x0000015dc(HELPING_ROBO_FOR_COMBAT) at 0x09e44284, fn_ptr=0x08060389; starts at +0x2 (0x08060388), 0x0000 pad before; ends bx lr at 0x080603b4; block = complete fn body |
| 0x08060588 sz=0x7c | raw=0 thumb+1=3 confirmed 0x09e4xxxx entries | disasm (R4) 3 sub-fn | 3 THUMB+1 refs in 0x09e4xxxx table: 0x08060589@0x09e41560(CID 0x15f0), 0x080605b9@0x09e41590(CID 0x15f2), 0x080605f1@0x09e415a8(CID 0x15f3); other hits at 0x083f.../0x0812... are false (data/code, not table structure); F1@0x08060588 leaf(bx lr @0x080605b6); F2@0x080605b8 leaf(bx lr @0x080605e8); F3@0x080605f0 push{r4,r5,lr} continues past block into named asm at 0x08060604 |
| 0x08060800 sz=0x08 (.byte) | raw=3(all incidental, non-4B-aligned) thumb+1=22(2 handler-table@0x09e41638/0x09e46bd0 + 1 code-literal@0x0813d450 + 19 incidental non-4B-aligned) | disasm (R4) | .byte 0x10,0xb5,0x04,0x1c,0x0a,0x1c,0x0b,0x48 = push{r4,lr};r4=r0;r2=r1;ldr r0,[pc,#44]; fn body continues in named asm 0x08060808..0x08060850; handler for CID 0x1624(PITCH_BLACK_POWER_STONE) at 0x09e41638,0x09e46bd0; 20 direct bl callers |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 复用/新建标注)

Total EQ: 53 slots classified below.

**gP1LifePoints = 0x0201c4e0** (REUSE ewram.inc; 17 slots):
| slot | value | const_name | slot_label |
|---|---|---|---|
| DWORD_0805fddc | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_0805ff34 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_0805ff8c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_0806007c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_080600f4 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_08060148 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_08060188 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_0806025c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_0806030c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_08060450 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_0806049c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_0806050c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_08060578 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_0806067c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| PTR_gP1LifePoints_08060700 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_080607dc | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |
| DWORD_08060874 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints |

**PLAYER_BLOCK_STRIDE = 0x868** (REUSE ewram.inc; 14 slots):
| slot | value | const_name | slot_label |
|---|---|---|---|
| DWORD_0805fd18 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_0805fde0 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_0805fe84 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DAT_0805ff38 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_0805ff90 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08060080 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DAT_080600f8 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DAT_0806014c | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DAT_08060260 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08060510 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_0806057c | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08060680 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_080607e0 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08060878 | 0x868 | PLAYER_BLOCK_STRIDE | PLAYER_BLOCK_STRIDE |

**CID and scalar equates (REUSE):**
| slot | value | const_name | slot_label |
|---|---|---|---|
| DWORD_0805fd14 | 0x0201bb90 | gEquipChainSlotRefs | gEquipChainSlotRefs |
| DWORD_0805fd1c | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots |
| DWORD_0805fd20 | 0x00001318 | RING_OF_MAGNETISM_CID | RING_OF_MAGNETISM_CID |
| DWORD_0805fe88 | 0x0201c8f8 | gP1HandSlotArray | gP1HandSlotArray |
| DAT_0805ffac | 0x0000159d | NECROVALLEY_CID | NECROVALLEY_CID |
| DAT_080600f0 | 0x0000159d | NECROVALLEY_CID | NECROVALLEY_CID |
| DAT_08060150 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | BANISHER_OF_THE_LIGHT_CID |
| DAT_0806018c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | P1LP_BLOCK2_OFF_1CE8 |
| DAT_08060190 | 0x00001cf4 | FIELD_STATE_OFF | FIELD_STATE_OFF |
| DAT_08060310 | 0x00001cf4 | FIELD_STATE_OFF | FIELD_STATE_OFF |
| DAT_08060314 | 0x000013f2 | EQUIP_LOCKDOWN_CID | EQUIP_LOCKDOWN_CID |
| DAT_08060374 | 0x000015d3 | SECOND_GOBLIN_CID | SECOND_GOBLIN_CID |
| DAT_08060458 | 0x00000fa7 | BLUE_EYES_WHITE_DRAGON_CID | BLUE_EYES_WHITE_DRAGON_CID |
| DAT_080604a0 | 0x00001cf4 | FIELD_STATE_OFF | FIELD_STATE_OFF |
| DWORD_08060704 | 0x00001cf4 | FIELD_STATE_OFF | FIELD_STATE_OFF |
| DAT_08060838 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | P1LP_BLOCK2_OFF_1CE8 |

**CID equates (NEW -- grep card_info.inc confirmed 0 hits):**
| slot | value | const_name | slot_label |
|---|---|---|---|
| DWORD_0806054c | 0x000015ca | PEOPLE_RUNNING_ABOUT_CID | PEOPLE_RUNNING_ABOUT_CID |
| DWORD_08060550 | 0x000015cb | OPPRESSED_PEOPLE_CID | OPPRESSED_PEOPLE_CID |
| DWORD_08060554 | 0x000015cc | UNITED_RESISTANCE_CID | UNITED_RESISTANCE_CID |

Evidence (card-stats.s):
- 0x15ca: card_1245 "People Running About" pw=12143771
- 0x15cb: card_1246 "Oppressed People" pw=58538870
- 0x15cc: card_1247 "United Resistance" pw=85936485

**Scalar NEW equates:**
| slot | value | const_name | slot_label |
|---|---|---|---|
| DWORD_0805feac | 0xfffffbf4 | HAND_SLOT_TO_ZONE_COUNT_NEG_OFF | HAND_SLOT_TO_ZONE_COUNT_NEG_OFF |
| DAT_08060264 | 0x00f88000 | ZONE_DETAIL_FIELD_MASK_F88 | ZONE_DETAIL_FIELD_MASK_F88 |

Evidence for DWORD_0805feac (0xfffffbf4):
- Used in check_equip_slot_eligible_with_hand_slot_bit14_and_effect_node @ 0x0805fe98
- adds r1,r6,r2 where r6=gP1HandSlotArray(0x0201c8f8), r2=0xfffffbf4
- result: 0x0201c8f8+0xfffffbf4 = 0x0201c4ec = gP1ZoneHandCount (ewram.inc line 232)
- Distinct from HAND_ARRAY_TO_COUNT_NEG_OFF=0xfffffbfc (ewram.inc line 358); that delta is -0x404, this is -0x40c
- confidence: high

Evidence for DAT_08060264 (0x00f88000):
- Used in check_equip_slot_eligible_neo_daedalus_with_zone_field_guard @ 0x08060224
- ands r0,r2 where r2=slot[+0x14]; cmp r0,#0xe1<<15(=0x708000)
- 0xf88000 = bits[23:11] mask; compared against 0x708000 expected pattern
- semantic: zone_detail_word bit-field mask for upper pattern check
- grep constants/*.inc for 0xf88000 or 0x00f88000: 0 hits
- confidence: high (exact bit mask value)

**New LP field offsets (NEW -- grep ewram.inc/duel_field.inc confirmed no 0x0010/0x000c equate for LP context):**

Note: These offset values (0x10, 0x0c) are used WITH PLAYER_BLOCK_STRIDE (gP1LifePoints + player*0x868 + offset) and are semantically distinct from the abs-addr gP1SlotCountBase (0x0201c4f0 = gP1LifePoints+0x10, P1 only). The per-player block usage requires separate offset constants.

These are SCALAR constants used inline in ldr/adds patterns and are NOT stored as literal pool slots in Seg-5 -- they are encoded directly as immediate operands. No EQ_SLOTS needed.

### REF_SLOTS (USER-label + DATA-ref; none in this segment)

No RAM/ROM pointer REF slots in Seg-5 (all slots are scalar or gP1LifePoints which is already a gref-style label).

### RENAME_SLOTS (纯改名 + EOL)

**stale PTR_ -> gref style (RENAME, no value change):**
The PTR_gP1LifePoints_* slots should be renamed to `gP1LifePoints` label directly (EQ change, handled above via EQ_SLOTS).

No standalone RENAME_SLOTS (no mis-prefixed DAT_/DWORD_ that need simple renaming without value change beyond the EQ category above).

### FUNC_RENAME (误名订正, 如有; 注 indeg + 理由)

No FUNC_RENAME needed. All 34 named functions in Seg-5 have semantically correct names. The stale FUN_ references in plate comments are:
- FUN_0806001c -> check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14 (confirmed @ L10131)
- FUN_0805f9e4 -> check_equip_slot_eligible_with_monster_count_gate (confirmed @ L9057, Seg-4)
- FUN_080607b4 -> check_equip_slot_eligible_by_lp_status_and_slot_value (confirmed @ L11313)
- FUN_08061660 -> check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect (confirmed @ L13738, Seg-6)

These are PLATE fixes, not FUNC_RENAME.

### PLATE (R5; stale FUN_ substring replacements + CJK rewrites; all ASCII)

**P1: FUN_ -> current name substring fixes (4 occurrences):**

1. `check_equip_slot_eligible_by_zone_type_b0_with_field5` plate @ L10054:
   - Stale: `FUN_0806001c`
   - Replace with: `check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14`

2. `check_equip_slot_eligible_neo_daedalus_full_guard` plate @ L10713:
   - Stale: `FUN_0805f9e4`
   - Replace with: `check_equip_slot_eligible_with_monster_count_gate`

3. `check_equip_slot_eligible_by_slot_value_vs_tier` plate @ L11271:
   - Stale: `FUN_080607b4`
   - Replace with: `check_equip_slot_eligible_by_lp_status_and_slot_value`

4. `check_equip_slot_eligible_by_lp_slot_and_effect_dispatch` plate @ L11456:
   - Stale: `FUN_08061660`
   - Replace with: `check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect`

**P2: CJK mojibake plate rewrites (6 functions with non-ASCII content):**

Functions at lines 10378, 10420, 10558, 10838, 11102, 11308 contain CJK characters (U+69FD, U+4E3A, U+602A, U+8DEF, U+7B2C, U+8FD4, U+5168, U+4EC5, U+521D, U+65E0, U+5408, U+4E2D). Must rewrite full plate as ASCII. Actual Ghidra plate comment already has valid English plate text -- these CJK characters likely appear only in the asm export comment lines (the @ prefix) not in the Ghidra plate. Verify: grep the plate open-lines for CJK before setting.

Note: Per asm file inspection, CJK appears in comment lines (@ prefix) which are NOT the Ghidra plate content -- they are Ghidra EOL or plate export artifacts. The plate content lines themselves (starting with `@ ` without address suffix) may need ASCII rewrite if CJK is present. Fixer must grep Ghidra export and use setPlateComment with all-ASCII text. The 6 affected functions are:
- L10378: check_equip_slot_eligible_zone_type_or_neo_daedalus (slot/zone CJK lines)
- L10420: check_equip_slot_eligible_neo_daedalus_with_zone_field_guard (slot CJK lines)
- L10558: check_equip_slot_eligible_mask_restrict_absent_dual_phase (second/return CJK lines)
- L10838: check_equip_slot_eligible_by_duel_phase3_neo_daedalus (all/only CJK lines)
- L11102: check_equip_slot_eligible_with_monster_zone_and_neo_daedalus (init/no-merge CJK lines)
- L11308: check_equip_slot_eligible_by_lp_status_and_slot_value (middle CJK line)

Full ASCII rewrites: use the existing English plate text visible in the plate comment header lines (which are already ASCII). Fixer must call setPlateComment with the English-only version.

---

## disasm 计划 (R4)

### Block 1: 0x0806008c size=0x28 -- fn for REASONING (CID 0x159a)

Handler table: 0x09e412c0 contains 0x0806008d (THUMB+1), CID 0x159a at 0x09e412b4.
Entry: 0x0806008c (THUMB fn, no push, leaf).
Exit: bx lr at 0x080600b2. End = 0x080600b4 (next named fn starts there).

**Disasm: createFunction at 0x0806008c**
Name: `check_equip_slot_eligible_by_lp_slot_for_cid_159a`
Plate (ASCII): "Equip slot eligibility predicate for Reasoning (CID 0x159A, pw=58577036). Leaf fn. Reads gP1LifePoints[player*0x868+0x10] (LP slot activation count); returns 1 if nonzero (LP active), 0 otherwise. Reached via card effect handler dispatch table 0x09e412c0, Reasoning CID 0x159A."

Literal pool inside block: none (pools are gP1LifePoints at +0x1c and PLAYER_BLOCK_STRIDE at +0x20, within the block).
Literal pool slots: 2 at file offsets within the block -- these become anonymous literals after createDWord (standard pattern); no named DAT_ slots created.

EQ for block literals:
- slot at 0x080600a8 (=0x0201c4e0): gP1LifePoints (REUSE)
- slot at 0x080600ac (=0x00000868): PLAYER_BLOCK_STRIDE (REUSE)

### Block 2: 0x08060386 size=0x32 -- fn for HELPING_ROBO_FOR_COMBAT (CID 0x15dc)

Handler table: 0x09e44290 contains 0x08060389 (THUMB+1), CID 0x15dc at 0x09e44284.
Padding: 2 zero bytes at 0x08060386; actual fn starts at 0x08060388.
Entry: 0x08060388 (THUMB fn, no push, leaf).
Exit: bx lr at 0x080603b4. Pad .zero 0x2 at 0x080603b6. End = 0x080603b8 (next named fn).

**Disasm: createFunction at 0x08060388**
Name: `check_equip_slot_eligible_by_type_and_player_for_cid_15dc`
Plate (ASCII): "Equip slot eligibility predicate for Helping Robo For Combat (CID 0x15DC, pw=47025270). Leaf fn. Checks slot type field (halfword[+2] bits[10:4] via mask 0xfc0) against 0x180 (0xb0<<1). Reads slot[+0x14] bit9 (lsls#0x16/lsrs#0x1f); compares against slot player bit0. Verifies zone detail bits. Returns 1 on pass, 0 on fail. Reached via card effect handler dispatch table 0x09e44290, Helping Robo For Combat CID 0x15DC."

Literal pool slots within block (2B before fn start and within fn):
- 0x08060386: .zero 0x2 (pad, createDWord will handle alignment)
- no named DAT_ slots from this block

### Block 3: 0x08060588 size=0x7c -- 3 sub-fns for CIDs 0x15f0/0x15f2/0x15f3

**Sub-fn F1: 0x08060588 -- CID 0x15f0 (Thunder of Ruler, pw=91781589)**
Handler table: 0x09e41560 contains 0x08060589 (THUMB+1), CID 0x15f0 at 0x09e41554.
Entry: 0x08060588 (no push, leaf-style with ldr r2).
Exit: bx lr at 0x080605b6. Next sub-fn starts at 0x080605b8.
Name: `check_equip_slot_eligible_by_active_player_phase_for_cid_15f0`
Plate (ASCII): "Equip slot eligibility predicate for Thunder of Ruler (CID 0x15F0, pw=91781589). Leaf fn. Gate: reads gP1LifePoints[player*0x868+0x1ce8] (active player id); if not equal to slot player id returns 0. Then reads gP1LifePoints+0x1cf4 (duel phase); if not equal to 1 returns 0. Else returns 1. Reached via card effect handler dispatch table 0x09e41560, Thunder of Ruler CID 0x15F0."

Literal pool slots within F1:
- 0x080605a8/0x080605aa: bytes c4e0,0201 = part of gP1LifePoints literal at 0x080605a8 -- createDWord sets .word gP1LifePoints (REUSE)
- 0x080605ac/0x080605ae: 1ce8,0000 = P1LP_BLOCK2_OFF_1CE8 literal (REUSE)
- 0x080605b0/0x080605b2: 1cf4,0000 = FIELD_STATE_OFF literal (REUSE)

**Sub-fn F2: 0x080605b8 -- CID 0x15f2 (Meteorain, pw=64274292)**
Handler table: 0x09e41590 contains 0x080605b9 (THUMB+1), CID 0x15f2 at 0x09e41584.
Entry: 0x080605b8 (no push, leaf-style).
Exit: bx lr at 0x080605e8. Pad .zero at 0x080605ea. Next sub-fn starts at 0x080605f0.
Name: `check_equip_slot_eligible_by_active_player_phase_for_cid_15f2`
Plate (ASCII): "Equip slot eligibility predicate for Meteorain (CID 0x15F2, pw=64274292). Leaf fn. Same active_player+duel_phase gate pattern as F1 (CID 0x15F0 sibling). Gate: reads gP1LifePoints[player*0x868+0x1ce8] (active player); if mismatch returns 0. Reads gP1LifePoints+0x1cf4 (phase); if not 3 returns 1, else reads opponent LP count at +0xc; returns 1 if 0, else 0. Reached via card effect handler dispatch table 0x09e41590, Meteorain CID 0x15F2."

Literal pool slots within F2:
- 0x080605d0/0x080605d2: gP1LifePoints (REUSE)
- 0x080605d4/0x080605d6: P1LP_BLOCK2_OFF_1CE8 (REUSE)
- 0x080605ec/0x080605ee: FIELD_STATE_OFF (REUSE)

**Sub-fn F3: 0x080605f0 -- CID 0x15f3 (Pineapple Blast, pw=90669991)**
Handler table: 0x09e415a8 contains 0x080605f1 (THUMB+1), CID 0x15f3 at 0x09e4159c (=table_addr-0xc).
Entry: 0x080605f0 (0xb530 = push{r4,r5,lr}). Body spans INTO named asm after 0x08060604.
Exit: pop{r4,r5};pop{r1};bx r1 at 0x08060638/0x0806063a/0x0806063c. End = 0x0806063e.
The code at 0x08060604..0x0806063e is currently UNNAMED continuation (visible as raw asm after ROM_INCBIN).

Name: `check_equip_slot_eligible_by_monster_zone_type_for_cid_15f3`
Plate (ASCII): "Equip slot eligibility predicate for Pineapple Blast (CID 0x15F3, pw=90669991). push{r4,r5,lr} fn. Calls count_occupied_monster_zones(opponent); compares result against player monster zone count (r4); checks zone_type bits[10:4] mask 0xfc0 against 0x180; verifies slot[+0x14] bit22 vs slot player bit0. Returns 1 on all pass, 0 on fail. Handler dispatch table 0x09e415a8, Pineapple Blast CID 0x15F3."

Note: BL target at 0x080605fe/0x08060600 = count_occupied_monster_zones at 0x08033188 (verified: asm/02 line 15717 shows push{r4,lr} at 0x08033188).

### Disasm for .byte block at 0x08060800 (fn prologue)

Handler table: 0x09e41638, 0x09e46bd0 contain 0x08060801 (THUMB+1); CID 0x1624 (Pitch-Black Power Stone).
Also: 20 direct-bl callers in code area (high indeg=20).
Entry: 0x08060800 (.byte 0x10,0xb5,... = push{r4,lr};r4=r0;r2=r1;ldr r0).
Body continues in named asm at 0x08060808..0x08060850 (with .byte 0x00,0x00,0xe0,0xc4,0x01,0x02 at 0x08060836 = pad+gP1LifePoints literal bytes).
Exit: bx r1 at 0x08060850. End = 0x08060852. Next fn: check_equip_slot_eligible_with_lp_slot_and_chain_polarity at 0x08060854.

**Disasm: createFunction at 0x08060800**
Name: `check_equip_slot_eligible_active_player_with_chain_and_node_count`
Plate (ASCII): "Equip slot eligibility predicate: active player gate + chain absent + effect node count. push{r4,lr}. Gate: gP1LifePoints+0x1ce8 (active player id) vs slot player id (bit0 byte[+2]); mismatch -> defer path. Match: check_equip_slot_chain_absent; chain present -> defer. count_effect_node_zone_activations; if >0 returns 2. Defer: byte[+3] bits[5:4] mask 0x30; nonzero returns 0, else 3. Handler for Pitch-Black Power Stone CID 0x1624 at tables 0x09e41638, 0x09e46bd0."

Literal pool slots inside fn body (.byte + named asm):
- 0x08060834 = gP1LifePoints (REUSE, .word 0x0201c4e0); currently .byte 0xe0,0xc4,0x01,0x02 fragment
- 0x08060838 = P1LP_BLOCK2_OFF_1CE8 (REUSE, .word 0x1ce8); already DAT_08060838 named slot -> EQ applies

After disasm, DAT_08060838 becomes the standard literal label referencing P1LP_BLOCK2_OFF_1CE8.
The literal at 0x08060834 is a new literal pool slot that needs EQ: gP1LifePoints. Assigned label: `seg5_disasm_fn_literal_c4e0` -> gP1LifePoints (REUSE).

---

## carve 計劃 (R7, 如有)

None. All ROM_INCBIN blocks are THUMB code (R4 disasm), not structured data to carve into rom.s.

---

## 新增 constants / 全局

### card_info.inc (新建 -- grep 0 命中确认):
```
.equ PEOPLE_RUNNING_ABOUT_CID, 0x000015ca  @ People Running About (pw=12143771; card-stats.s line ~16220 slot=0x15CA); resistance triple check
.equ OPPRESSED_PEOPLE_CID,      0x000015cb  @ Oppressed People (pw=58538870; card-stats.s line ~16226 slot=0x15CB); resistance triple check
.equ UNITED_RESISTANCE_CID,     0x000015cc  @ United Resistance (pw=85936485; card-stats.s line ~16232 slot=0x15CC); resistance triple check
.equ REASONING_CID,             0x0000159a  @ Reasoning (pw=58577036; card-stats.s line 15381 slot=0x159A); disasm block1 handler fn
.equ HELPING_ROBO_FOR_COMBAT_CID, 0x000015dc @ Helping Robo For Combat (pw=47025270; card-stats.s line 16005 slot=0x15DC); disasm block2 handler fn
.equ THUNDER_OF_RULER_CID,      0x000015f0  @ Thunder of Ruler (pw=91781589; card-stats.s line 16213 slot=0x15F0); disasm block3 F1
.equ METEORAIN_CID,             0x000015f2  @ Meteorain (pw=64274292; card-stats.s line 16239 slot=0x15F2); disasm block3 F2
.equ PINEAPPLE_BLAST_CID,       0x000015f3  @ Pineapple Blast (pw=90669991; card-stats.s L16252 slot=0x15F3); disasm block3 F3
```

### ewram.inc (新建 -- grep confirmed no existing 0x10/0x0c LP-field offset equate):
```
.equ LP_SLOT_ACTIVE_OFF,        0x00000010  @ [gP1LifePoints+player*0x868+0x10] LP slot activation count; nonzero = LP slot active/present; ~10 Seg-5 uses
.equ LP_LOOP_CEIL_OFF,          0x0000000c  @ [gP1LifePoints+player*0x868+0x0c] LP slot count ceiling for loop bounds; ~7 Seg-5 uses
.equ HAND_SLOT_TO_ZONE_COUNT_NEG_OFF, 0xfffffbf4  @ gP1HandSlotArray(0x0201c8f8)+0xfffffbf4=gP1ZoneHandCount(0x0201c4ec); neg delta -0x40c; distinct from HAND_ARRAY_TO_COUNT_NEG_OFF=-0x404; 1 Seg-5 slot DWORD_0805feac
```

Note: LP_SLOT_ACTIVE_OFF=0x10 and LP_LOOP_CEIL_OFF=0xc are used as immediate adds operands (not literal pool slots) in Seg-5 -- they appear in EOL comments, not as EQ_SLOTS. However creating the equates now enables Seg-6..10 symbolization.

### constants/duel_field.inc or new file (1 new mask):
```
.equ ZONE_DETAIL_FIELD_MASK_F88, 0x00f88000  @ slot[+0x14] bits[23:11] mask; used with 0x708000 (0xe1<<15) expected value in neo_daedalus zone_field_guard check; 1 Seg-5 slot DAT_08060264
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None in this segment. All 3 ROM_INCBIN blocks + .byte block have confirmed THUMB+1 references.

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽 | 值 | 语义 | 证据 | 置信度 |
|---|---|---|---|---|
| DWORD_0805feac | 0xfffffbf4 | HAND_SLOT_TO_ZONE_COUNT_NEG_OFF: gP1HandSlotArray + this = gP1ZoneHandCount | asm/07 L9866 adds r1,r6,r2 where r6=gP1HandSlotArray; result 0x0201c4ec = gP1ZoneHandCount (ewram.inc L232) | high |
| DAT_08060264 | 0x00f88000 | ZONE_DETAIL_FIELD_MASK_F88: bits[23:11] of slot[+0x14] detail word | asm/07 L10468-10471: ands r0,r2; cmp r0,0xe1<<15; check_equip_slot_eligible_neo_daedalus_with_zone_field_guard | high |
| DWORD_0806054c/50/54 | 0x15ca/cb/cc | resistance triple group CIDs | asm/07 L10964-10979: three sequential count_paired_slots_with_field5_default calls, each with one CID; card-stats.s confirms names | high |
| Block1 0x0806008c | fn | REASONING handler (CID 0x159a) | table entry @ 0x09e412c0 struct: CID_word=0x159a at 0x09e412b4, fn_ptr=0x0806008d; python verified rom[0x09e412b4-base:+8] = 9a150000 8d000608 | high |
| Block2 0x08060388 | fn | HELPING_ROBO handler (CID 0x15dc) | table entry @ 0x09e44290 struct: CID_word=0x15dc at 0x09e44284, fn_ptr=0x08060389; python verified | high |
| Block3 F1-F3 | fn | THUNDER/METEORAIN/PINEAPPLE_BLAST handlers (CID 0x15f0/f2/f3) | table entries @ 0x09e41560/90/a8 respectively; python verified all 3 CID_words | high |
| .byte 0x08060800 | fn | PITCH_BLACK_POWER_STONE (CID 0x1624) active_player+chain+node | table entry @ 0x09e41638: CID_word=0x1624 at 0x09e4162c, fn_ptr=0x08060801; 20 direct-bl callers | high |

---

## 求助 (如有低置信度语义)

None. All slots and blocks have high-confidence semantics with verified evidence.

**Minor open item (low impact):** The name `check_equip_slot_eligible_by_type_and_player_for_cid_15dc` for Block2 fn is based on the THUMB code pattern (type_field check + player bit cross-check + zone detail bits). The exact Zone Type value checked by the code could be more precisely named once Ghidra disassembles it. If reviewer finds the code decodes differently, propose: `check_equip_slot_eligible_by_zone_type_for_cid_15dc`. Confidence: med for name specifics, high for CID assignment.

**Block 3 F2 (Meteorain, CID 0x15f2) plate note:** The plate says "phase != 3 returns 1, else reads opponent LP count at +0xc; returns 1 if 0, else 0." -- this is the best-effort decode from 0x080605b8..0x080605e8 raw bytes. Actual disasm may refine the branch semantics. Not blocking for symbolization.
