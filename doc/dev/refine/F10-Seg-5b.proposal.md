# Refine Proposal: F10-Seg-5b  [0x0807ec10..0x0807f730)

Split half: Seg-5b covers the remaining 14 named functions + 2 ROM_INCBIN blocks + 2 already-decoded switchD entries.
Seg-5a is F10-Seg-5.proposal.md.

## Segment Mapping

- Function entries: 14
  - tick_equip_zone15_bitmap_with_sprite_output      @ 0x0807ec10 (line 8878)
  - tick_equip_effect_display_state_machine_alt      @ 0x0807ed04 (line 9009)
  - dispatch_equip_display_by_state_code             @ 0x0807ee74 (line 9173)
  - dispatch_equip_zone_sprite_banisher_or_lp        @ 0x0807efec (line 9332)
  - tick_prng_pair_zone_sprite_by_field_card         @ 0x0807f0a4 (line 9439)
  - enqueue_field_slot_sprite_for_zone11             @ 0x0807f158 (line 9534)
  - enqueue_field_slot_sprite_for_equip_head         @ 0x0807f1ec (line 9610)
  - dispatch_equip_zone_sprite_shape_b_by_state      @ 0x0807f458 (line 9718)
  - submit_equip_slot_lp_indicators_from_bitmap      @ 0x0807f53c (line 9850)
  - find_equip_display_entry_by_card_id              @ 0x0807f5d4 (line 9936)
  - check_card_equip_criteria_by_ext_field6          @ 0x0807f5f0 (line 9961)
  - check_slot_card_equip_criteria_by_state_code     @ 0x0807f618 (line 9991)
  - check_card_equip_display_criteria_match          @ 0x0807f644 (line 10017)
  - get_equip_display_type_code_by_card_id           @ 0x0807f6f0 (line 10104)
- ROM_INCBIN blocks: 2
  - BLK7: 0x7f280, 0x3c  (60B)   -- fn_eligible_flute_summoning_kuriboh (THUMB+1 ref; MOV PC dispatch)
  - BLK8: 0x7f330, 0x128 (296B)  -- Flute of Summoning Kuriboh dispatch sub-stubs (R4 disasm; 1 function body with 6 case sub-stubs)
- switchD entries: 2 (ALREADY DECODED in asm -- no R4 disasm needed)
  - switchD_0807ed22 (tick_equip_effect_display_state_machine_alt, 29 cases, .hword 0x4687 code instr)
  - switchD_0807ee92 (dispatch_equip_display_by_state_code, 29 cases, .hword 0x4687 code instr)
- Auto-name slots: 40 unique addresses (total instances higher due to shared global ptrs)
- NOTE: The decoded jump table for BLK7 (29 x .word entries at 0x7f2bc..0x7f330) is already present as `.word` directives in the asm between enqueue_field_slot_sprite_for_equip_head epilogue and DAT_0807f330.

## Data Block Classification (Rule 2/3) -- ref-scan evidence

| Block         | ref-scan (raw / THUMB+1)           | Judgment  | Rationale |
|---------------|------------------------------------|-----------|-----------|
| BLK7 0x7f280/0x3c  | raw=0, thumb+1=1 @ 0x09e430d0     | R4 disasm | THUMB fn_eligible stub; 1 THUMB+1 ref from FS table entry at 0x09e430c0: [+12]=0x000019ec (Flute of Summoning Kuriboh), [+16]=0x0807f281; contains MOV PC,r0 dispatch (0x4687 at 0x7f2b0); jump table ptr stored in literal pool at 0x7f2b8 = 0x0807f2bc (addr after BLK7) |
| BLK8 0x7f330/0x128 | raw=1 @ 0x7f32c (last .word in decoded jump table), thumb+1=0 | R4 disasm | Pointed to by decoded jump table; ONE function body containing 6 case sub-stubs (case entries 0x7f330/0x7f35e/0x7f376/0x7f404/0x7f43a/0x7f446); single pop {r4,r5}; pop {r1}; bx r1 at 0x7f452; ends at 0x7f458 |

switchD disposition (ALREADY DECODED):
- switchD_0807ed22: asm lines 9026-9027 show `.hword 0x4687` as code instruction (MOV PC,r0 dispatch); full caseD labels present (caseD_80/7e/7d/78/64/65); no R4 action needed.
- switchD_0807ee92: asm lines 9190-9191 show same pattern; caseD labels present; no R4 action needed.

ref-scan validation:
```python
import struct
rom = open("roms/2343.gba", "rb").read()
for blk_off, sz in [(0x7f280, 0x3c), (0x7f330, 0x128)]:
    a = blk_off + 0x08000000
    print(f"0x{blk_off:07x}: raw={rom.count(struct.pack('<I',a))} thumb+1={rom.count(struct.pack('<I',a|1))}")
```
Results: BLK7: raw=0, thumb+1=1; BLK8: raw=1, thumb+1=0

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

REUSE from existing constants:

| slot addr  | value      | action | const_name                   | source |
|------------|------------|--------|------------------------------|--------|
| 0x7ec94    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7ecec    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f05c    | 0x000004a4 | REUSE  | EQUIP_PHASE_FRAME_OFF        | ewram.inc L437 |
| 0x7f064    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f09c    | 0x00001332 | REUSE  | BANISHER_OF_THE_LIGHT_CID    | card_info.inc L452 |
| 0x7f0a0    | 0x000004a4 | REUSE  | EQUIP_PHASE_FRAME_OFF        | ewram.inc L437 |
| 0x7f0d8    | 0x000004a4 | REUSE  | EQUIP_PHASE_FRAME_OFF        | ewram.inc L437 |
| 0x7f13c    | 0x000004a4 | REUSE  | EQUIP_PHASE_FRAME_OFF        | ewram.inc L437 |
| 0x7f144    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f1e4    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f278    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f488    | 0x00001ce8 | REUSE  | P1LP_BLOCK2_OFF_1CE8         | ewram.inc L276 |
| 0x7f490    | 0x000004a4 | REUSE  | EQUIP_PHASE_FRAME_OFF        | ewram.inc L437 |
| 0x7f4c0    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f50c    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f5bc    | 0x00000868 | REUSE  | PLAYER_BLOCK_STRIDE          | ewram.inc L251 |
| 0x7f65c    | 0x000019ef | REUSE  | EHERO_ERIKSHIELER_CID        | card_info.inc L381 |
| 0x7f6d8    | 0x000018a6 | REUSE  | EHERO_AVIAN_CID              | card_info.inc L213 |
| 0x7f6dc    | 0x000018a7 | REUSE  | EHERO_BURSTINATRIX_CID       | card_info.inc L922 |
| 0x7f6e0    | 0x000018a8 | REUSE  | EHERO_CLAYMAN_CID            | card_info.inc L1257 |
| 0x7f6e4    | 0x000018f9 | REUSE  | EHERO_BUBBLEMAN_CID          | card_info.inc L688 |
| 0x7f714    | 0x000019ef | REUSE  | EHERO_ERIKSHIELER_CID        | card_info.inc L381 (dup) |

NEW equates:

| slot addr  | value        | action | const_name                     | note |
|------------|--------------|--------|--------------------------------|------|
| 0x7f510    | 0x000005cc   | NEW    | ZONE_ENTRY_OFFSET_5CC          | base+offset for zone slot entry in dispatch_equip_zone_sprite_shape_b_by_state; 0 grep hits by value in constants/; add to ewram.inc or equip_display.inc |
| 0x7f5ec    | 0x09e59e14   | NEW    | EQUIP_DISPLAY_ROM_TABLE_BASE   | ROM read-only table of 86 equip display entries (stride 8B, max_idx=0x55); 0 grep hits in constants/; 1 ROM ref; add to equip_display.inc |
| 0x7f658    | 0x0000157e   | NEW    | FGD_CID                        | F.G.D. (Five-God Dragon, pw=99267150; card_1157 slot=0x157E); check_card_equip_display_criteria_match special case; 0 grep hits by value; add to card_info.inc |
| 0x7f710    | 0x0000157e   | REUSE  | FGD_CID                        | dup slot same value (get_equip_display_type_code_by_card_id) |

C5 dedup proof:
- 0x000005cc: grep -rn "0x000005cc" constants/ -> 0 hits (NEW confirmed)
- 0x09e59e14: grep -rn "0x09e59e14" constants/ -> 0 hits (NEW confirmed)
- 0x0000157e: grep -rn "0x0000157e" constants/ -> 0 hits (NEW confirmed); grep "FGD\|Five.God" -> 0 hits

Also: BLK7 CID 0x000019ec (Flute of Summoning Kuriboh) NEW -- NOT in constants, needed for fn name:
- grep -rn "0x000019ec" constants/ -> 0 hits
- Add: `.equ FLUTE_SUMMONING_KURIBOH_CID, 0x000019ec  @ The Flute of Summoning Kuriboh (pw=20065322; card_2070 slot=0x19EC)`

### REF_SLOTS (USER-label + DATA-ref)

| slot addr  | target value  | gas_label              | slot_label                 | note |
|------------|---------------|------------------------|----------------------------|------|
| 0x7ec2c    | 0x0201b290    | gDuelPhaseFlags        | DAT_0807ec2c               | ewram.inc L353 |
| 0x7ec98    | 0x0201c510    | gDuelFieldSlots        | DAT_0807ec98               | ewram.inc L314 |
| 0x7ecf0    | 0x0201c8f8    | gP1HandSlotArray       | DAT_0807ecf0               | ewram.inc L334 |
| 0x7ed24    | 0x0201b290    | gDuelPhaseFlags        | DAT_0807ed24               | ewram.inc L353 |
| 0x7ee94    | 0x0201b290    | gDuelPhaseFlags        | DAT_0807ee94               | ewram.inc L353 |
| 0x7f008    | 0x0201b290    | gDuelPhaseFlags        | DWORD_0807f008             | ewram.inc L353 |
| 0x7f068    | 0x0201b290    | gDuelPhaseFlags        | DWORD_0807f068             | ewram.inc L353 |
| 0x7f0c0    | 0x0201b290    | gDuelPhaseFlags        | DWORD_0807f0c0             | ewram.inc L353 |
| 0x7f1e8    | 0x0201c510    | gDuelFieldSlots        | DWORD_0807f1e8             | ewram.inc L314 |
| 0x7f27c    | 0x0201c510    | gDuelFieldSlots        | DWORD_0807f27c             | ewram.inc L314 |
| 0x7f48c    | 0x0201b290    | gDuelPhaseFlags        | DWORD_0807f48c             | ewram.inc L353 |
| 0x7f5c0    | 0x0201c510    | gDuelFieldSlots        | DWORD_0807f5c0             | ewram.inc L314 |

PTR_NAMED slots (already use gP1LifePoints -- skip):
- 0x7f060 DWORD_0807f060
- 0x7f140 DWORD_0807f140
- 0x7f484 DWORD_0807f484

switchD literal pool slots (jump table base addresses -- skip, already decoded labels):
- 0x7ed28 DAT_0807ed28 -> .word 0x0807ed2c (already has switchD_0807ed22__switchdataD_0807ed2c label)
- 0x7ee98 DAT_0807ee98 -> .word 0x0807ee9c (already has switchD_0807ee92__switchdataD_0807ee9c label)

### RENAME_SLOTS (pure rename + EOL)

No standalone DWORD/DAT slots without semantic decode needed.

### FUNC_RENAME (misnomer corrections)

None identified in Seg-5b. All 14 named functions have semantics consistent with their names.

### PLATE (R5) -- C8 stale FUN_ substitution

The following plates contain stale FUN_ references that must be replaced with current names:

| plate location (line) | stale FUN_         | current name                               | confidence |
|-----------------------|--------------------|--------------------------------------------|------------|
| find_equip_display_entry_by_card_id plate (L9929-9935) | FUN_0807f644 | check_card_equip_display_criteria_match | high (same file) |
| check_card_equip_criteria_by_ext_field6 plate (L9954-9958) | FUN_0807f644 | check_card_equip_display_criteria_match | high |
| check_card_equip_criteria_by_ext_field6 plate (L9956) | FUN_0807f800 | check_equip_slot_criteria_by_ext_field6_any | high (same file L10274) |
| check_slot_card_equip_criteria_by_state_code plate (L9984-9990) | FUN_0807f848 | check_equip_slot_criteria_by_state_code_any | high (same file L10316) |
| check_slot_card_equip_criteria_by_state_code plate (L9986) | FUN_0807f8f0 | find_first_equip_slot_criteria_by_state_code | high (same file L10412) |
| get_equip_display_type_code_by_card_id plate (L10103) | FUN_0807f7bc | fill_equip_criteria_display_code_array | high (same file L10236) |
| get_equip_display_criteria_code_by_card_and_slot plate (Seg-6 start L10142) | FUN_0807f7bc | fill_equip_criteria_display_code_array | high |

Cross-file FUN_ resolution for check_slot_card_equip_criteria_by_state_code plate (asm/10 line 11578):
- FUN_08054d5c -> `check_equip_slot_eligible_by_display_criteria_loop` (asm/06_equip_eligibility_b.s line 3309; addr 0x08054d5c confirmed)
- FUN_080598d8 -> `tick_equip_atk_zone_sprite_display_seq` (asm/06_equip_eligibility_b.s line 15141; addr 0x080598d8 confirmed)
- FUN_0807f848 -> `check_equip_slot_criteria_by_state_code_any` (asm/10 line 11908; addr 0x0807f848 confirmed)
- FUN_0807f8f0 -> `find_first_equip_slot_criteria_by_state_code` (asm/10 line 12004; addr 0x0807f8f0 confirmed)

Full rewrite of asm/10 line 11578 plate line (replacing the stale-FUN_ sentence):
```
@ Called by check_equip_slot_eligible_by_display_criteria_loop (asm/06 0x08054d5c) and tick_equip_atk_zone_sprite_display_seq (asm/06 0x080598d8) (card frame / equip activation check chain) and check_equip_slot_criteria_by_state_code_any / find_first_equip_slot_criteria_by_state_code.
```
(Full ASCII; all 4 stale FUN_ replaced with current names.)

### CJK plate rewrites (C9 -- 2 mojibake plates in Seg-5b range)

The following existing Ghidra plates in asm/10 contain CJK characters (Jython mojibake risk) and must be rewritten to ASCII-only:

**A) tick_equip_effect_display_state_machine_alt (0x0807ed04)** -- asm/10 lines 10592-10593:

Current CJK text (lines 10592-10593):
```
@ 驱动装备卡牌效果显示的 29 步 switch 状态机帧驱动, 与 0807d104 形成同族 sibling.
@ 以 IWRAM[0x0201b290+0x4a0] 状态码减 0x64 作 switch 索引 (0x1c+1=29 case): 0x80 -> lookup_slot_display_value_by_card_id + dispatch_effect_handler_by_card_id; 成功 -> trigger_card_display_op31_if_not_active(0x3a) 返回 0x7e; 失败且非法术 -> trigger_card_display_op31(0xd) 返回 0x78; 失败且是法术 -> 0x0; 0x7e -> init_effect_slot_display_context(player, 6, card_id, display_val) 返回 0x7d; 0x7d -> get_monster_slot_entry_ptr x2 取两侧槽; extract tile_col/flip; render_spell_zone_sprite_with_field_copy_check 返回 0x64; 0x78 -> count_field_cards_pair_allowed_for_card + get_card_type_bits; 如果 count < type_bits 则 set_lp_row_type7_if_opponent_linked; 返回 0x64; 0x64 -> check_card_type_is_spell; 非法术 -> enqueue_lp_counter_sprite_by_player; 返回 0x0.
```

ASCII replacement (preserve full semantic):
```
@ 29-case switch state machine frame driver for equip card effect display (sibling of 0807d104).
@ State code = [IWRAM_BASE+0x4a0] - 0x64; switch index 0..0x1c (29 cases): 0x80 -> lookup_slot_display_value_by_card_id + dispatch_effect_handler_by_card_id; on success -> trigger_card_display_op31_if_not_active(0x3a) return 0x7e; on fail non-spell -> trigger_card_display_op31(0xd) return 0x78; on fail spell -> return 0x0; 0x7e -> init_effect_slot_display_context(player, 6, card_id, display_val) return 0x7d; 0x7d -> get_monster_slot_entry_ptr x2 both sides; extract tile_col/flip; render_spell_zone_sprite_with_field_copy_check return 0x64; 0x78 -> count_field_cards_pair_allowed_for_card + get_card_type_bits; if count < type_bits then set_lp_row_type7_if_opponent_linked; return 0x64; 0x64 -> check_card_type_is_spell; non-spell -> enqueue_lp_counter_sprite_by_player; return 0x0.
```

**B) tick_prng_pair_zone_sprite_by_field_card (0x0807f0a4)** -- asm/10 lines 11021-11022:

Current CJK text (lines 11021-11022):
```
@ 驱动 prng 抽样后渲染卡牌配对 zone 精灵的三步帧状态机.
@ 以 IWRAM[0x0201b290+0x4a0] 状态码路由: 0x80 -> increment_lp_bar_display_counter; 写 [IWRAM+0x4a4]=0 (COUNTER_OFFSET 重置); 返回 0x7f; 0x7f -> 读 [IWRAM+0x4a4] 计数器; 若 > 1 返回 0x7e (等待); 否则 sample_prng_scaled 取随机索引; 读 gP1LifePoints[player*0x868+0x18+rand_offset] card_id, 调用 render_pair_zone_sprites_if_field_card_present(opponent, card_id_bits13, 0, 1); 返回 0x7f; 0x7e -> decrement_lp_bar_display_counter; 返回 0x0. 副作用: 写 IWRAM COUNTER_OFFSET; LP bar 计数器 +1/-1; 渲染配对 zone 精灵.
```

ASCII replacement (preserve full semantic):
```
@ 3-step frame state machine for rendering paired-zone sprites after prng sampling.
@ Routes on [IWRAM_BASE+0x4a0]: 0x80 -> increment_lp_bar_display_counter; write [IWRAM+0x4a4]=0 (COUNTER_OFFSET reset); return 0x7f; 0x7f -> read [IWRAM+0x4a4] counter; if > 1 return 0x7e (wait); else sample_prng_scaled for random index; read gP1LifePoints[player*0x868+0x18+rand_offset] card_id; call render_pair_zone_sprites_if_field_card_present(opponent, card_id_bits13, 0, 1); return 0x7f; 0x7e -> decrement_lp_bar_display_counter; return 0x0.
@ Side effects: write IWRAM COUNTER_OFFSET; LP bar counter +1/-1; render paired-zone sprites.
```

All plate text must remain ASCII. No CJK in plate/EOL.

## Disasm Plan (R4)

### BLK7: fn_eligible_flute_summoning_kuriboh  [0x0807f280..0x0807f2bc)  60B

FS entry at 0x09e430c0: [+12]=0x000019ec (FLUTE_SUMMONING_KURIBOH_CID), [+16]=0x0807f281 (THUMB+1).
Contains push {r4,r5,lr} at 0x7f280; MOV PC,r0 dispatch at 0x7f2b0; literal pool word at 0x7f2b8 = 0x0807f2bc (jump table address AFTER BLK7).

Function name: fn_eligible_flute_summoning_kuriboh

Disasm action: DisassembleCommand(addr=0x0807f280, THUMB) -- single stub.

NOTE: The jump table at 0x7f2bc..0x7f330 (29 x .word entries) is ALREADY DECODED in the asm as `.word` directives in the switch table for dispatch_equip_zone_sprite_shape_b_by_state. No additional action needed for the jump table itself.

### BLK8: Flute of Summoning Kuriboh dispatch sub-stubs  [0x0807f330..0x0807f458)  296B

ONE function body (29-case switch via MOV PC,r0 from BLK7). 6 real case entry points + 1 default:
- 0x0807f330: case state 0x80 (state_reset_path)
- 0x0807f35e: case state 0x7e
- 0x0807f376: case state 0x7d
- 0x0807f404: case state 0x7c
- 0x0807f43a: case state 0x78
- 0x0807f446: case state 0x64 (return 0x64)
- 0x0807f44c: default (return 0x0)

Single return sequence at 0x7f452: pop {r4,r5}; pop {r1}; bx r1.
Function name: dispatch_flute_summoning_kuriboh_by_state_code

Disasm action: DisassembleCommand(addr=0x0807f330, THUMB) -- single function.
Then createFunction at 0x0807f330.

## New Constants / Globals Needed

Add to `constants/card_info.inc`:
```asm
.equ FGD_CID,                     0x0000157e  @ F.G.D. (Five-God Dragon, pw=99267150; card_1157 slot=0x157E); check_card_equip_display_criteria_match / get_equip_display_type_code special case; conf: high
.equ FLUTE_SUMMONING_KURIBOH_CID, 0x000019ec  @ The Flute of Summoning Kuriboh (pw=20065322; card_2070 slot=0x19EC); BLK7 fn_eligible; conf: high
```

Add to `constants/equip_display.inc` (new file) or `constants/ewram.inc`:
```asm
.equ ZONE_ENTRY_OFFSET_5CC,       0x000005cc  @ zone slot entry base offset in dispatch_equip_zone_sprite_shape_b_by_state; gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x5cc; 5 ROM refs; conf: med
.equ EQUIP_DISPLAY_ROM_TABLE_BASE, 0x09e59e14 @ ROM read-only equip display entry table; 86 entries stride 8B [cid(u16), criteria0(u16), criteria1(u16), criteria2(u16)]; 1 ROM ref (find_equip_display_entry_by_card_id); conf: high
```

C5 dedup proof (all new, grep by value = 0 hits):
- 0x0000157e: 0 hits confirmed
- 0x000019ec: 0 hits confirmed
- 0x000005cc: 0 hits confirmed
- 0x09e59e14: 0 hits confirmed

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. Both BLK7 and BLK8 have ROM references:
- BLK7 THUMB+1: 1 ref (FS table at 0x09e430d0)
- BLK8 raw: 1 ref (decoded .word at 0x0807f32c pointing to 0x0807f330)

## Consumer Evidence (R6) -- key slot semantics

| slot           | value       | consumer / evidence                                                          | confidence |
|----------------|-------------|-------------------------------------------------------------------------------|------------|
| 0x7f09c/1332   | 0x1332      | asm/10 line 9402: `bl count_field_copies_of_card` with r0=0x1332; plate "CARD_ID_BANISHER=0x1332 (Banisher of the Light)"; card_info.inc BANISHER_OF_THE_LIGHT_CID=0x1332 | high |
| 0x7f488/1ce8   | 0x1ce8      | asm/10 line 9724: `ldr r0,[DWORD_0807f488]` = 0x1ce8; plate "OFFSET_0x1ce8=0x1ce8"; ewram.inc P1LP_BLOCK2_OFF_1CE8=0x1ce8 | high |
| 0x7f510/5cc    | 0x5cc       | asm/10 line 9814: `DWORD_0807f510` loaded as r4; used as `adds r0,r2,r4` then `ldr r0,[r0,#0x0]` to read zone slot entry ptr; plate "ZONE_ENTRY_OFFSET=0x5cc"; 5 ROM refs | med |
| 0x7f5ec/9e59e14 | 0x09e59e14 | asm/10 line 9939: `ldr r0,DAT_0807f5ec` = table base; find_equip_display_entry_by_card_id iterates 86 entries; plate "TABLE_BASE=0x09e59e14"; 1 ROM ref | high |
| 0x7f658/157e   | 0x157e      | asm/10 lines 10021-10023: `cmp r4,r0` where r0=0x157e; matched against card_id; plate "CARD_ID_A=0x157e"; card-stats.s card_1157 slot=0x157E = F.G.D. | high |
| 0x7f65c/19ef   | 0x19ef      | asm/10 line 10024-10026: `cmp r4,r0` where r0=0x19ef; card_info.inc EHERO_ERIKSHIELER_CID | high |
| BLK7 CID 19ec  | 0x19ec      | FS entry 0x09e430c0+12 = 0x000019ec; card-stats.s card_2070 slot=0x19EC = The Flute of Summoning Kuriboh | high |

## Seek Help / Blocked

None. All blocks have confirmed consumers. ZONE_ENTRY_OFFSET_5CC=0x5cc is marked med confidence due to limited ROM ref count (5 refs); the structural evidence (used as base+offset into gP1LifePoints) is clear.

---

## Seg-5b Summary Counts

- EQ slots: 26 (22 REUSE + 4 NEW including FGD_CID first occurrence, ZONE_ENTRY_OFFSET_5CC, EQUIP_DISPLAY_ROM_TABLE_BASE, FLUTE_SUMMONING_KURIBOH_CID)
- REF slots: 12 (all REUSE existing globals)
- RENAME slots: 0
- FUNC_RENAME: 0
- PLATE: 9 (C8 stale FUN_ substitutions: 5 in-file + 1 cross-file line-11578 full-rewrite with 4 resolved names; C9 ASCII rewrites: 2 CJK mojibake plates replaced with ASCII-only content)
- carve: 0
- disasm blocks: 2 (BLK7: 1fn fn_eligible, BLK8: 1fn dispatch body)
- switchD: 2 (already decoded, no action)
- section 5.1: 0
- new constants: 5 (FGD_CID, FLUTE_SUMMONING_KURIBOH_CID, ZONE_ENTRY_OFFSET_5CC, EQUIP_DISPLAY_ROM_TABLE_BASE in Seg-5b; + the Seg-5a new constants for a combined 11 new from both halves)
