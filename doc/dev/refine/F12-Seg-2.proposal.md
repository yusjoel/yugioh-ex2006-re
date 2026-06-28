# Refine Proposal: F12-Seg-2  [0x08094f20..0x08095ba8)

## 段测绘

- 函数入口: x15
  - 0x08094f20  write_card_display_index_if_above_bit
  - 0x08094f3c  write_card_display_index_with_bit_offset
  - 0x08094f58  write_spell_activation_type_display_bit
  - 0x08094f70  update_card_display_index_by_type_rules
  - 0x08095084  write_monster_zone_display_indices
  - 0x08095194  count_nonzero_results_in_zone_matrix
  - 0x080951cc  play_equip_ui_effect_3_with_state_gate
  - 0x08095220  dispatch_equip_confirm_phase_by_step
  - 0x08095348  tick_equip_confirm_slot_by_step
  - 0x08095380  pack_sprite_row_attr_words
  - 0x080953c4  dispatch_sprite_row_write_by_type
  - 0x08095498  submit_sprite_row_data
  - 0x080954e8  step_prng_anim_frame
  - 0x08095b3c  get_lp_display_state_word
  - 0x08095b50  check_player_side_condition

- 残留自动名槽: 122 slots total
  - DAT_: 99 slots
  - DWORD_: 10 slots
  - PTR_gP1LifePoints_: 11 slots (PTR_PTR_08095248 x1 and PTR_DAT_0809524c x1 are separate; true PTR_gP1LifePoints_ count = 11, NOT 13)

  All verified by python ROM read (value = little-endian 4 bytes at vaddr-0x08000000).

- ROM_INCBIN / .byte 块: x2
  - 0x08095274  size 0xc0  (Block1: 10-entry jump table / 9 unique case-block entry points (entries[7]/[8] both -> 0x08095274); raw=2 for 0x8095274)
  - 0x08095b28  size 0x14  (Block2: THUMB helper; raw=0, thumb+1=0)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

ref-scan script (run per methodology):
```python
import struct
rom = open("roms/2343.gba","rb").read()
for block_start, size in [(0x08095274, 0xc0), (0x08095b28, 0x14)]:
    for off in range(0, size, 2):
        a = block_start + off
        for v in (a, a|1):
            c = rom.count(struct.pack("<I", v))
            if c: print(hex(v), c)
```

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08095274 sz=0xc0 | raw: 0x8095274=2, 0x8095284=1, 0x809528a=1, 0x809528e=1, 0x8095292=1, 0x809529e=1, 0x80952aa=1, 0x8095304=1, 0x809530a=1; THUMB+1=0 for all | R4 disasm | Jump table PTR_DAT_0809524c (10 entries, 9 unique entry points) references all case-block entry addresses as RAW pointers; dispatch via MOV PC,r0 (.hword 0x4687 = THUMB-encoded MOV PC, r0). 0x8095274 appears twice because table entries[7] and [8] both point there (shared case 7+8). Bytes are valid THUMB code (case dispatch stubs). R4 disasm required; no createFunction for any case block (they are jump targets within dispatch_equip_confirm_phase_by_step, not standalone functions). |
| 0x08095b28 sz=0x14 | raw=0, THUMB+1=0 (all 2-byte-aligned addrs scanned; no refs found) | §5.1 | THUMB code confirmed: 4802 4903 1840 2101 6001 4770 = ldr r0,[pc,#8]; ldr r1,[pc,#12]; adds r0,r0,r1; movs r1,#1; str r1,[r0,#0]; bx lr; pool: gP1LifePoints=0x0201c4e0, 0x1d0c. NOT fall-through: preceding function step_prng_anim_frame ends 0x08095b18: pop {r4,r5,r6} (bc70); pop {r1} (bc02); bx r1 (4708); .zero 2 (0000) -- explicit pop-bx epilogue, not fall-through. Zero full-ROM refs -> §5.1 registration, ROM_INCBIN preserved. |

Block1 case-block decoding (10 case blocks; PTR_DAT_0809524c entry mapping):
```
Table entry -> case entry addr -> semantics:
[0] -> 0x809530a  ldr r1,[pc,#28]={0x1d68}; adds r0,r4,r1; ldr r0,[r0]; ldr r2,[pc,#24]={0x1d6c}; adds r1,r4,r2; ldr r3,[r1]; adds r1,r3,#0; subs r1,#0x0b; movs r2,#1; rsbs r2,r2,r0; bl init_lp_bar_slot_entry_from_state(0x80941c4); ldr r0,[pc,#12]={0x1d54}; adds r1,r4,r0; b 0x8095338
[1] -> 0x809529e  movs r0,#1; movs r1,#1; movs r2,#0; bl 0x80a5f38(tick_equip_target_selection_display_seq path); b epilogue
[2] -> 0x80952aa  ldr r2,[pc,#32]={0x1d6c}; adds r0,r4,r2; ldr r2,[r0]; cmp r2,#0x0b; cmp/blo/bhi branches; ldr r1,[pc,#16]={0x1d68}; adds r0,r4,r1; ldr r1,[r0]; movs r0,#0; bl 0x8095ec4(dispatch_effect_slot_by_display_state); b epilogue
[3] -> 0x8095292  movs r0,#1; movs r1,#0; movs r2,#1; bl 0x80a5f38; b epilogue
[4] -> 0x8095284  bl 0x8095d44(init_lp_bar_slot_entry_from_state); b epilogue
[5] -> 0x809528a  movs r0,#0; b 0x8095294 (falls through to case[3] after first insn)
[6] -> 0x809528e  movs r0,#0; b 0x80952f2 (shared path movs r1,#0; movs r2,#0; then bl 0x80a5f38)
[7] -> 0x8095274  ldr r1,[pc,#8]={0x1d5c}; adds r0,r4,r1; ldrh r0,[r0,#0]; bl 0x8095e6e(apply_slot_equip_activation_if_lp_anim_phase); b epilogue
[8] -> 0x8095274  (same entry as [7], shared case 7+8)
[9] -> 0x8095304  bl 0x8095f4c(tick_lp_bar_anim_step_display); b epilogue
```
Post-block epilogue at 0x8095334: ldr r2,{0x1d54}; adds r1,r1,r2; movs r0,#0; str r0,[r1,#0]; pop {r4}; pop {r0}; bx r0.
Additional shared path 0x8095338: stores callee result to [gP1LifePoints+0x1d54].

Pool words inside Block1:
- 0x8095280: 0x00001d5c (ELIGIB_ACT_TYPE_OFF -- ewram.inc:421 REUSE)
- 0x80952cc: 0x00001d6c (ELIGIB_ANIM_STATE_OFF -- ewram.inc:423 REUSE)
- 0x80952d0: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF -- ewram.inc:422 REUSE)
- 0x8095328: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF REUSE)
- 0x809532c: 0x00001d6c (ELIGIB_ANIM_STATE_OFF REUSE)
- 0x8095330: 0x00001d54 (ELIGIB_STATE_CTRL_OFF -- ewram.inc:419 REUSE)
(No new constants needed from Block1 pool words; all already in ewram.inc.)

Block2 semantic (§5.1 orphan):
```
0x8095b28: ldr r0,[pc,#8]   -> pool @ 0x8095b34 = gP1LifePoints (0x0201c4e0)
0x8095b2a: ldr r1,[pc,#12]  -> pool @ 0x8095b38 = 0x00001d0c (LP_DISPLAY_STATE_OFF -- NEW)
0x8095b2c: adds r0,r0,r1    -> r0 = gP1LifePoints + 0x1d0c
0x8095b2e: movs r1,#1
0x8095b30: str r1,[r0,#0]   -> [gP1LifePoints+0x1d0c] := 1
0x8095b32: bx lr
pool: gP1LifePoints=0x0201c4e0, 0x1d0c
```
Semantics: writes 1 to [gP1LifePoints+0x1d0c] (LP display state control word).
Name candidate: set_lp_display_state_active (conf: high, semantics match get_lp_display_state_word counterpart).
Action: §5.1 registration ONLY, ROM_INCBIN preserved, no Ghidra ops.

---

## 符号化计划 (R1/R2/R3)

All slot values verified by python ROM read (vaddr - 0x08000000).
All REUSE entries verified by grep in constants/*.inc by VALUE before marking.
All NEW entries verified by grep returning 0 hits in constants/*.inc.

### EQ_SLOTS (data-equate)

Key: REUSE = grep by VALUE confirmed hit in constants/; NEW = grep=0 confirmed.

| slot addr | value | const_name | source | slot_label | evidence |
|---|---|---|---|---|---|
| 0x0809501c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9501c | update_card_display_index_by_type_rules: ldr r5,[r1,#4]=player_id check at L1984 |
| 0x08095020 | 0x000012c4 | NEGATE_ATTACK_CID | NEW (grep 0x12c4 constants/=0; card-stats.s slot=0x12c4 pw=14315573 "Negate Attack"; 8 ROM refs) | negate_atk_cid_95020 | update_card_display_index_by_type_rules: cmp r2,r0 when card_id == 0x12c4 -> reads [gP1LifePoints+0x1ce8] XOR 1 (player side check for Negate Attack effect rule); conf: high |
| 0x08095024 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | update_card_display_index_by_type_rules: PTR_gP1LifePoints_08095024 |
| 0x08095028 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_95028 | [gP1LifePoints+0x1ce8] player_raw XOR for Negate Attack check |
| 0x08095080 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_95080 | update_card_display_index_by_type_rules field6==0x16 path player XOR check |
| 0x0809507c | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_0809507c |
| 0x08095188 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_95188 | write_monster_zone_display_indices: ldr r2,[r7,#4]=player_id |
| 0x0809518c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE (value 0x868 hits PLAYER_BLOCK_STRIDE) | player_stride_9518c | write_monster_zone_display_indices: muls r0,r1 player offset |
| 0x08095190 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 REUSE | gduelfieldslots_95190 | write_monster_zone_display_indices: ldr base for slot scan [+0]=slot_field5 |
| 0x08095204 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (DWORD_ -> EQ, see RENAME) | DWORD_08095204 in play_equip_ui_effect_3_with_state_gate |
| 0x08095208 | 0x00001d4c | ACTIVATION_STATE_C_OFF | duel_field.inc:220 REUSE | act_state_c_95208 | [gP1LifePoints+0x1d4c] equip slot status; ldr r1 then adds r0,r2,r1; ldr r1,[r0] check !=0 |
| 0x0809520c | 0x00001d50 | LP_EQUIP_STATE_B_OFF | NEW (grep 0x1d50 constants/=0; 7 ROM refs) | lp_equip_b_9520c | play_equip_ui_effect_3_with_state_gate: [gP1LifePoints+0x1d50] secondary equip state flag; cmp==0 (beq skip), then set [+0x1d50]:=1 and dispatch_card_display_op(3,0,0,0); conf: high |
| 0x0809521c | 0x00001d50 | LP_EQUIP_STATE_B_OFF | NEW REUSE (same) | lp_equip_b_9521c | LAB_08095210: str r1,[r0] where r1=0 -> clear [gP1LifePoints+0x1d50] |
| 0x08095240 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (DWORD_ -> EQ, see RENAME) | DWORD_08095240 |
| 0x08095244 | 0x00001d5c | ELIGIB_ACT_TYPE_OFF | ewram.inc:421 REUSE | eligib_act_type_95244 | dispatch_equip_confirm_phase_by_step: [gP1LifePoints+0x1d5c] step value; subs r0,#1; cmp r0,#9; bls dispatch |
| 0x08095344 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc:419 REUSE | eligib_state_ctrl_95344 | dispatch_equip_confirm_phase_by_step LAB_08095334: str 0 to [gP1LifePoints+0x1d54] when step out of range |
| 0x0809535c | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (DWORD_ -> EQ, see RENAME) | DWORD_0809535c |
| 0x08095360 | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc:420 REUSE | eligib_act_cnt_95360 | tick_equip_confirm_slot_by_step: [gP1LifePoints+0x1d58] confirm pending flag; cmp==0 -> return 0 |
| 0x0809537c | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc:419 REUSE | eligib_state_ctrl_9537c | tick_equip_confirm_slot_by_step: [gP1LifePoints+0x1d54] check after step; if==0 clears [+0x1d58] |
| 0x080953bc | 0xffff0000 | SPRITE_HIGH_HALF_MASK | NEW (grep 0xffff0000 constants/=0 -- duel_field.inc:272 EQUIP_CHAIN_SENTINEL=0xffff0000 exists; DIFFERENT domain: here = AND mask to clear low 16 bits of sprite attr word; domain conflict -> new constant SPRITE_HIGH_HALF_MASK) | sprite_hi_mask_953bc | pack_sprite_row_attr_words: ands r1,r4 at 0x08095398 clears low 16 bits of r1 before ORing y-coord; mask=0xffff0000; conf: high (sprite packing, NOT equip chain sentinel) |
| 0x080953c0 | 0x0000ffff | SPRITE_LOW_HALF_MASK | NEW (grep 0xffff constants/: 5 hits in card_info.inc (CARD_STAT_ROW_ATTR2_BASE_A etc.) and ewram.inc (UNINIT_GUARD_FFFF), all different domains; this domain = low-halfword sprite attr mask; new SPRITE_LOW_HALF_MASK) | sprite_lo_mask_953c0 | pack_sprite_row_attr_words: ands r1,r5 at 0x0809539e clears high 16 bits; conf: high |
| 0x080953d8 | 0x080953dc | SPRITE_ROW_DISPATCH_TABLE | NEW (grep 0x080953dc constants/=0; 1 ROM ref; self-referential dispatch table in dispatch_sprite_row_write_by_type) | sprite_row_tbl_953d8 | dispatch_sprite_row_write_by_type: switch table of 30 entries (2 targets: 0x08095454 / 0x0809548e) at 0x080953dc; conf: high |
| 0x0809546c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9546c | dispatch_sprite_row_write_by_type caseD_2 r2!=0 path: adds r2,r2,r0 where r0=0xc0<<2=0x300 stride |
| 0x08095490 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95490 | caseD_2 r2==0 path (LAB_08095470) |
| 0x08095494 | 0xfff87fff | SPRITE_ROW_BITS18_15_CLEAR_MASK | NEW (grep 0xfff87fff constants/=0; 2 ROM refs) | sprite_bits1815_mask_95494 | dispatch_sprite_row_write_by_type: ands r0,r3 clears bits[18:15] of sprite row word before ORing new direction bits; conf: high |
| 0x08095528 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95528 | step_prng_anim_frame: base for busy_flag [+0xc0*4=0x300] |
| 0x08095530 | 0x00001d0c | LP_DISPLAY_STATE_OFF | NEW (grep 0x1d0c constants/=0; 7 ROM refs) | lp_disp_state_95530 | step_prng_anim_frame: [gP1LifePoints+0x1d0c] LP display state control word; ldr r0,[r0+r2] -> b LAB_08095b12 dispatch; also read by get_lp_display_state_word; conf: high |
| 0x08095608 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95608 | step_prng_anim_frame caseD_2: [gSpriteAttrBuf+0x300] busy byte ORed with 1 |
| 0x0809560c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9560c | caseD_2: [gDuelCardCtxBase+4]=player_id for slot index lookup |
| 0x0809561c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9561c | caseD_3: adds base+0xc0*4 then ORs bit0 |
| 0x08095634 | 0x0201e4d0 | gEquipZoneRankState | ewram.inc:441 REUSE | gequipzonerank_95634 | caseD_15: bl copy_bytes_by_halfword(gEquipZoneRankState, gSpriteAttrBuf+2, 0x18) |
| 0x08095638 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW (0x0201b872; grep 0x0201b872 constants/=0; 8 ROM refs; gSpriteAttrBuf+2 = halfword at offset 2 into sprite buf; consistently paired with gEquipZoneRankState as copy destination) | gsprattrb_p2_95638 | caseD_15: dst = gSpriteAttrBuf+2 for halfword copy; conf: high |
| 0x08095644 | 0x0201e4d0 | gEquipZoneRankState | ewram.inc:441 REUSE | gequipzonerank_95644 | caseD_16 (b LAB_080959b2): same copy src |
| 0x08095648 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (same 0x0201b872) | gsprattrb_p2_95648 | caseD_16 copy dst |
| 0x0809565c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9565c | caseD_17: ORs bit1 into busy byte [+0x300] |
| 0x08095674 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95674 | caseD_9: ldrh r0,[r2,#2]/r3[6]/r2[4] sprite row fields |
| 0x0809568c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9568c | caseD_a: ldrh r0,[r0,#2] sprite type field |
| 0x08095708 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95708 | caseD_c: clears [gDuelPhaseFlags+ELIGIB_RESULT_OFF=0x584] and [+0x58c] and [+0x590]; ORs 0x10 into [gSpriteAttrBuf+0x300] |
| 0x0809570c | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc:359 REUSE | effect_cnt_9570c | [gDuelPhaseFlags+0x594]=0 clear in caseD_c |
| 0x08095710 | 0x0000058c | EQUIP_SLOT_SUBSTATE_OFF | ewram.inc:538 REUSE | equip_substate_95710 | [gDuelPhaseFlags+0x58c]=0 clear |
| 0x08095714 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95714 | caseD_c continued: ORs 0x10 into [gSpriteAttrBuf+0x300] |
| 0x08095718 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_95718 | caseD_b: ldrh r4,[r2,#0] source halfword |
| 0x0809571c | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc:405 REUSE | lp_bar_anim_9571c | caseD_b+c: [gDuelPhaseFlags+0x4cc] as offset for str r4 |
| 0x08095720 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc:411 REUSE | sprite_row_data_95720 | caseD_b: [gDuelPhaseFlags+0x4d4] byte array base |
| 0x08095724 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | ewram.inc:447 REUSE | chain_node_arr_95724 | caseD_b: [gDuelPhaseFlags+0x4f4] card ptr array |
| 0x08095738 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95738 | caseD_d: ORs 0x20 into [gSpriteAttrBuf+0x300] |
| 0x08095770 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_95770 | caseD_e: ldrh r0,[r4,#0]/r1[2]/r2[4] entry fields; r4=gSpriteAttrBuf+2 |
| 0x08095778 | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | NEW (grep 0x1d64 constants/=0; 25 ROM refs) | lp_playerside_9578 | caseD_e: [gP1LifePoints+0x1d64] written = [gDuelCardCtxBase+4] XOR 1; copy of activation player_side cached for LP display; conf: high |
| 0x0809577c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9577c | caseD_e: ldr r0,[r0,#4]=current_player_id for XOR |
| 0x08095780 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95780 | caseD_e: [gDuelPhaseFlags+GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF=0x584] :=1 |
| 0x08095784 | 0x00000584 | GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF | duel_field.inc:97 REUSE (value 0x584; NOTE: ewram.inc also mentions ELIGIB_RESULT_OFF=0x584 but duel_field.inc:97 GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF is the same value -- same memory offset, gDuelPhaseFlags+0x584; use duel_field.inc def) | gprng_disp_flag_95784 | caseD_e: str 1 -> [gDuelPhaseFlags+0x584] display-ready |
| 0x08095788 | 0x000002fe | SPRITE_ATTR_BYTE_2FE_OFF | NEW (grep 0x2fe constants/=0; 98 ROM refs) | sprite_byte_2fe_95788 | caseD_e/11: adds r4,r4,r2 where r2=DAT_088=0x2fe -> byte field at gSpriteAttrBuf+2+0x2fe=gSpriteAttrBuf+0x300 -- actually 0x0201b872+0x2fe=0x0201bb70 (a byte within gSpriteAttrBuf that receives ORed bits); conf: high |
| 0x080957a0 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_957a0 | caseD_12: ldrh r5,[r1,#2]; lsls r0,r5,#1; adds r0,r0,r5; lsls r0,r0,#3 -> sprite offset |
| 0x080957a4 | 0x0201b590 | gEffectEntryArray | ewram.inc:358 REUSE | geffectentry_957a4 | caseD_12: adds r0,r0,r2; r2=gEffectEntryArray -> base+entry_offset |
| 0x080957b4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_957b4 | caseD_13: adds r0,r1 where r1=0x594 -> gDuelPhaseFlags+EFFECT_ENTRY_COUNT_OFF |
| 0x080957b8 | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc:359 REUSE | effect_cnt_957b8 | caseD_13: [gDuelPhaseFlags+0x594] = effect entry count |
| 0x080957bc | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_957bc | caseD_13: ldrh r1,[r1,#2] |
| 0x080957dc | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_957dc | caseD_14: ldrh r0[2]/r2[6]/r3[4]/r2[c]/r5[a]/r4[8] entry fields for submit_slot_card_sprite_row_entry |
| 0x08095810 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95810 | caseD_f: ldr+adds -> [gDuelPhaseFlags+0x594] = sprite_id from gSpriteAttrBuf |
| 0x08095814 | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc:359 REUSE | effect_cnt_95814 | caseD_f |
| 0x08095818 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95818 | caseD_f: ldrh r0,[r2,#2] source sprite_id |
| 0x0809581c | 0x0000058c | EQUIP_SLOT_SUBSTATE_OFF | ewram.inc:538 REUSE | equip_substate_9581c | caseD_f: [gDuelPhaseFlags+0x58c]:=0 |
| 0x0809582c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9582c | caseD_10: adds r1,r1,r5 where r5=0xc0*4=0x300; ORs 0x20 |
| 0x08095864 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_95864 | caseD_11: ldrh r0[0]/r1[2]/r2[4] entry; init_duel_zone_target_slot_refs args |
| 0x0809586c | 0x00001d64 | LP_PLAYER_SIDE_CACHE_OFF | NEW REUSE (same 0x1d64) | lp_playerside_9586c | caseD_11: [gP1LifePoints+0x1d64]:=[gDuelCardCtxBase+4] XOR 1 (same pattern as caseD_e) |
| 0x08095870 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_95870 | caseD_11: [+4] player_id XOR |
| 0x08095874 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95874 | caseD_11: [gDuelPhaseFlags+0x584]:=1 |
| 0x08095878 | 0x00000584 | GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF | duel_field.inc:97 REUSE | gprng_disp_flag_95878 | caseD_11 [gDuelPhaseFlags+0x584]:=1 |
| 0x0809587c | 0x000002fe | SPRITE_ATTR_BYTE_2FE_OFF | NEW REUSE | sprite_byte_2fe_9587c | caseD_11: adds r4,r4,r2 where r2=0x2fe -> byte at gSpriteAttrBuf+2+0x2fe |
| 0x0809589c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9589c | caseD_1e: [gDuelCardCtxBase+4]=player_id arg to setup_lp_display_row_with_data |
| 0x080958a0 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_958a0 | caseD_1e: ldrh r1,[r2,#2]; adds r2,#4 source for setup_lp_display_row_with_data |
| 0x080958a4 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_080958a4 |
| 0x080958a8 | 0x00001d84 | LP_EQUIP_DISPLAY_FLAG_OFF | NEW (grep 0x1d84 constants/=0; 7 ROM refs) | lp_equip_disp_958a8 | caseD_1e: str 1 to [gP1LifePoints+0x1d84] after setup_lp_display_row_with_data; display tracking flag; conf: high |
| 0x080958c4 | 0x0201e288 | gEquipChainEntryBase | ewram.inc:391 REUSE | gequipchain_958c4 | caseD_1f: bl copy_bytes_by_halfword(gEquipChainEntryBase, gSpriteAttrBuf+2, 0x10) |
| 0x080958c8 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_958c8 | caseD_1f: dst for copy |
| 0x080958cc | 0x000002ff | SPRITE_ATTR_BYTE_2FF_OFF | NEW (grep 0x2ff constants/=0; 198 ROM refs) | sprite_byte_2ff_958cc | caseD_1f: adds r4,r4,r0 where r0=0x2ff -> byte at gSpriteAttrBuf+2+0x2ff=gSpriteAttrBuf+0x301 receives ORed bits; conf: high |
| 0x08095904 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95904 | caseD_1c: base [+2] halfword as sprite_id; [+0xc4*4] = sprite_id; [+0x301] ORed 0x10 |
| 0x08095908 | 0x0201b590 | gEffectEntryArray | ewram.inc:358 REUSE | geffectentry_95908 | caseD_1c: adds r0,r0,r1 -> gEffectEntryArray + sprite_id*24 |
| 0x0809590c | 0x0000030d | SPRITE_ROW_ENTRY_305_OFF | NEW (grep 0x30d constants/=0; 28 ROM refs; gSpriteAttrBuf+0x30d = control byte within sprite entry) | sprite_entry_30d_9590c | caseD_1c: strb r0,[r1,#0] -> [gSpriteAttrBuf+0x30d]:=0 (clear byte); conf: high |
| 0x08095910 | 0x00000301 | SPRITE_ROW_BUSY_BYTE_OFF | NEW (grep 0x301 constants/=0; 157 ROM refs; gSpriteAttrBuf+0x301 = main busy/status byte; OR target in many cases) | sprite_busy_95910 | caseD_1c: adds r4,r4,r5; ldrb r1,[r4,#0]; ORs 0x10 -> [gSpriteAttrBuf+0x301] |
| 0x08095938 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95938 | caseD_1d: adds r2,r1,r3 where r3=0x301 -> [gSpriteAttrBuf+0x301] ORed 0x20 |
| 0x0809593c | 0x00000301 | SPRITE_ROW_BUSY_BYTE_OFF | NEW REUSE | sprite_busy_9593c | caseD_1d |
| 0x08095940 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95940 | caseD_1d: [gDuelPhaseFlags+0x494] = count * 24 + gEffectEntryArray |
| 0x08095944 | 0x00000494 | SPRITE_ROW_ANIM_CTL_OFF | ewram.inc:435 REUSE | sprite_anim_ctl_95944 | [gDuelPhaseFlags+0x494] sprite type index |
| 0x0809597c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9597c | caseD_1a: [+2] ldrh; [+0xc4*4] = sprite_id; copy to gEffectEntryArray+idx*24; [+0x30e] strb 0 |
| 0x08095980 | 0x0201b590 | gEffectEntryArray | ewram.inc:358 REUSE | geffectentry_95980 | caseD_1a: effect entry base |
| 0x08095984 | 0x0000030e | SPRITE_ROW_ENTRY_30E_OFF | NEW (grep 0x30e constants/=0; 19 ROM refs; gSpriteAttrBuf+0x30e = control byte adjacent to 0x30d) | sprite_entry_30e_95984 | caseD_1a: strb 0 -> [gSpriteAttrBuf+0x30e] clear; conf: high |
| 0x08095988 | 0x00000301 | SPRITE_ROW_BUSY_BYTE_OFF | NEW REUSE | sprite_busy_95988 | caseD_1a: [gSpriteAttrBuf+0x301] ORed 0x4 |
| 0x080959bc | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_959bc | caseD_1b: [gSpriteAttrBuf+0x301] ORed 0x8; [gDuelPhaseFlags+0x494] stride |
| 0x080959c0 | 0x00000301 | SPRITE_ROW_BUSY_BYTE_OFF | NEW REUSE | sprite_busy_959c0 | caseD_1b |
| 0x080959c4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_959c4 | caseD_1b |
| 0x080959c8 | 0x00000494 | SPRITE_ROW_ANIM_CTL_OFF | ewram.inc:435 REUSE | sprite_anim_ctl_959c8 | caseD_1b |
| 0x08095a38 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95a38 | caseD_18: entry fields; [+0xc4*4]=sprite_id; copy to gEffectEntryArray+stride |
| 0x08095a3c | 0x0201b590 | gEffectEntryArray | ewram.inc:358 REUSE | geffectentry_95a3c | caseD_18 |
| 0x08095a40 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_08095a40 |
| 0x08095a44 | 0x000010e1 | LP_ACTIVATION_TYPE_ARRAY_BASE_OFF | NEW (grep 0x10e1 constants/=0; 9 ROM refs; from asm L6872 plate comment "type_field_offset=0x10e1"; in caseD_18: r1=gP1LifePoints + field_bits*4 + 0x10e1 -> byte array base for per-slot activation type flags) | lp_act_type_base_95a44 | caseD_18: orrs bit7 -> per-slot activation type byte at gP1LifePoints+0x10e1+field_slot*4; conf: high |
| 0x08095a5c | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95a5c | LAB_08095a48: [gSpriteAttrBuf+0x30f]:=0; [gSpriteAttrBuf+0x301] ORed 0x40 |
| 0x08095a60 | 0x0000030f | SPRITE_ROW_ENTRY_30F_OFF | NEW (grep 0x30f constants/=0; 18 ROM refs; gSpriteAttrBuf+0x30f = control byte at +3 from 0x30c cluster) | sprite_entry_30f_95a60 | [gSpriteAttrBuf+0x30f]:=0 clear; conf: high |
| 0x08095a64 | 0x00000301 | SPRITE_ROW_BUSY_BYTE_OFF | NEW REUSE | sprite_busy_95a64 | [gSpriteAttrBuf+0x301] ORed 0x40 |
| 0x08095a9c | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 REUSE | gphaseflag_95a9c | caseD_19: [gDuelPhaseFlags+0x94*8=0x4a0]:=0 clear state; [+0x90*8=0x480] count check |
| 0x08095aa0 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_95aa0 | caseD_19: copy dst for ldrh->copy_bytes_by_halfword 0x30 bytes |
| 0x08095ac0 | 0x0201b870+2 | gSpriteAttrBuf_p2 | NEW REUSE (0x0201b872) | gsprattrb_p2_95ac0 | LAB_08095aa4: copy_bytes_by_halfword(gEffectEntryArray+idx*24, gSpriteAttrBuf+2, 0x18) |
| 0x08095ad4 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95ad4 | caseD_7: ldrh r0[2]/r1[4]/r2[6]/r3[8] -> write_sprite_attr_record_entry args |
| 0x08095aec | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95aec | caseD_8: adds r1,r1,r5 where r5=0x300; ORs 0x8 into [gSpriteAttrBuf+0x300] |
| 0x08095af8 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_08095af8 |
| 0x08095afc | 0x00001d0c | LP_DISPLAY_STATE_OFF | NEW REUSE | lp_disp_state_95afc | caseD_1: ldr r3,[pc,#8]={0x1d0c}; adds r0,r0,r3; b LAB_08095b12 -> writes 1 to [gP1LifePoints+0x1d0c] |
| 0x08095b20 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_08095b20 |
| 0x08095b24 | 0x00001d0c | LP_DISPLAY_STATE_OFF | NEW REUSE | lp_disp_state_95b24 | caseD_4: after pack_sprite_row_attr_words, [gP1LifePoints+0x1d0c]:=1 |
| 0x08095b48 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_08095b48 |
| 0x08095b4c | 0x00001d0c | LP_DISPLAY_STATE_OFF | NEW REUSE | lp_disp_state_95b4c | get_lp_display_state_word: ldr r0,[r0+r1] returns [gP1LifePoints+0x1d0c] |
| 0x08095b94 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_95b94 | check_player_side_condition: [gSpriteAttrBuf+0xc0*4=0x300] ldr r0; lsls r0,#0xd; asrs r3,r0,#0x1c -> extracts bits[18:15] |
| 0x08095b98 | 0x0201c4e0 | gP1LifePoints | ewram.inc REUSE | (PTR_ -> EQ, see RENAME) | PTR_gP1LifePoints_08095b98 |
| 0x08095b9c | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_95b9c | check_player_side_condition: [gP1LifePoints+0x1d08] flag check |
| 0x08095ba0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_95ba0 | [gP1LifePoints+0x1ce8] player_id XOR check |
| 0x08095ba4 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_95ba4 | [gDuelCardCtxBase+4]=player_id for XOR |

### REF_SLOTS (USER-label + DATA-ref)

| slot addr | value | gas_label | slot_label | evidence |
|---|---|---|---|---|
| 0x08095248 | 0x0809524c | equip_confirm_case_jump_table (or: dispatch_equip_confirm_switch_table) | eq_confirm_jumptbl_95248 | PTR_PTR_08095248 points to jump table PTR_DAT_0809524c (10 x .word entries); used by dispatch_equip_confirm_phase_by_step; conf: high |
| 0x08095550 | 0x08095554 | switchD_0809554c__switchdataD_08095554 | sprite_row_tbl2_95550 | DAT_08095550 holds base address of step_prng_anim_frame second switchD 30-entry dispatch table at 0x08095554; used at LAB_08095544: ldr r1,DAT_08095550; adds r0,r0,r1; ldr r0,[r0,#0]; mov pc,r0; GAS label already present in asm file; conf: high |

NOTE: PTR_DAT_0809524c (the jump table itself at 0x0809524c) is already labeled as a data block in the asm (10 .word entries, already structured). The jump table entries are raw (not THUMB+1) pointers confirmed by ref-scan. No additional REF slot needed for the table entries themselves.

### RENAME_SLOTS (PTR_/DWORD_ label rename)

All PTR_gP1LifePoints_* and DWORD_ slots holding gP1LifePoints (0x0201c4e0) get snake_case rename. The actual value becomes EQ gP1LifePoints (already in ewram.inc).

| slot addr | current_label | new slot_label |
|---|---|---|
| 0x08095024 | PTR_gP1LifePoints_08095024 | gp1lp_ptr_95024 |
| 0x0809507c | PTR_gP1LifePoints_0809507c | gp1lp_ptr_9507c |
| 0x08095204 | DWORD_08095204 | gp1lp_ptr_95204 |
| 0x08095240 | DWORD_08095240 | gp1lp_ptr_95240 |
| 0x0809535c | DWORD_0809535c | gp1lp_ptr_9535c |
| 0x080958a4 | PTR_gP1LifePoints_080958a4 | gp1lp_ptr_958a4 |
| 0x08095a40 | PTR_gP1LifePoints_08095a40 | gp1lp_ptr_95a40 |
| 0x08095af8 | PTR_gP1LifePoints_08095af8 | gp1lp_ptr_95af8 |
| 0x08095b20 | PTR_gP1LifePoints_08095b20 | gp1lp_ptr_95b20 |
| 0x08095b48 | PTR_gP1LifePoints_08095b48 | gp1lp_ptr_95b48 |
| 0x08095774 | PTR_gP1LifePoints_08095774 | gp1lp_ptr_95774 |
| 0x08095868 | PTR_gP1LifePoints_08095868 | gp1lp_ptr_95868 |
| 0x0809552c | PTR_gP1LifePoints_0809552c | gp1lp_ptr_9552c |
| 0x08095b98 | PTR_gP1LifePoints_08095b98 | gp1lp_ptr_95b98 |

Also DWORD_ holding non-gP1LifePoints values (already captured in EQ_SLOTS above):
| 0x08095208 | DWORD_08095208 | act_state_c_95208 |
| 0x0809520c | DWORD_0809520c | lp_equip_b_9520c |
| 0x0809521c | DWORD_0809521c | lp_equip_b_9521c |
| 0x08095244 | DWORD_08095244 | eligib_act_type_95244 |
| 0x08095344 | DWORD_08095344 | eligib_state_ctrl_95344 |
| 0x08095360 | DWORD_08095360 | eligib_act_cnt_95360 |
| 0x0809537c | DWORD_0809537c | eligib_state_ctrl_9537c |

### FUNC_RENAME

No function name in Seg-2 is contradicted by function body semantics. All 15 function names are consistent with their behavior.

### PLATE (R5) -- stale FUN_ subscriptions

7 stale FUN_ references found in Seg-2 ASM (grep [^\x00-\x7F] = 0; no non-ASCII).

| fn addr | stale ref | real name | action |
|---|---|---|---|
| 0x08094f58 write_spell_activation_type_display_bit | L1949: "FUN_0804154c (caseD_44)" | tick_spell_equip_zone_display_seq | Substring replace FUN_0804154c -> tick_spell_equip_zone_display_seq in plate |
| 0x08094f70 update_card_display_index_by_type_rules | L1971: "FUN_08095a18" (is a LAB_ label, not a function; refers to code inside step_prng_anim_frame switchD_caseD_18); "FUN_080954e8" | step_prng_anim_frame | Replace "FUN_080954e8" -> "step_prng_anim_frame"; remove "FUN_08095a18" / replace with "step_prng_anim_frame (caseD_18)" |
| 0x08095194 count_nonzero_results_in_zone_matrix | L2250: "FUN_080a2ad0" | tick_equip_target_selection_display_seq | Replace FUN_080a2ad0 -> tick_equip_target_selection_display_seq |
| 0x080953c4 dispatch_sprite_row_write_by_type | L2476: "FUN_080954e8" | step_prng_anim_frame | Replace FUN_080954e8 -> step_prng_anim_frame |
| 0x080954e8 step_prng_anim_frame | L2603: "FUN_08094dac" | advance_duel_turn_by_prng_anim | Replace FUN_08094dac -> advance_duel_turn_by_prng_anim |
| 0x08095b3c get_lp_display_state_word | L3402: "FUN_080954e8" | step_prng_anim_frame | Replace FUN_080954e8 -> step_prng_anim_frame |
| 0x08095ba8 init_equip_card_sprite_row_entry | L3464: "FUN_0804ce78" | dispatch_card_eligibility_state_machine | Replace FUN_0804ce78 -> dispatch_card_eligibility_state_machine |

NOTE: init_equip_card_sprite_row_entry at 0x08095ba8 is the first function of Seg-3; however its plate comment references a stale FUN_ that is visible inside Seg-2's address range in the asm file (L3464 is in the grep range). The plate is on the function at 0x08095ba8 which starts Seg-3, so the Seg-2 fixer should NOT modify this plate -- it belongs to Seg-3. Removing it from this list.

Revised PLATE list (Seg-2 plates only, functions [0x08094f20, 0x08095ba8)):
| fn addr | stale ref | corrected name | action |
|---|---|---|---|
| 0x08094f58 | FUN_0804154c | tick_spell_equip_zone_display_seq | setPlateComment substring replace |
| 0x08094f70 | FUN_080954e8 | step_prng_anim_frame | setPlateComment substring replace; also remove FUN_08095a18 / note it is a LAB_ in step_prng_anim_frame body |
| 0x08095194 | FUN_080a2ad0 | tick_equip_target_selection_display_seq | setPlateComment substring replace |
| 0x080953c4 | FUN_080954e8 | step_prng_anim_frame | setPlateComment substring replace |
| 0x080954e8 | FUN_08094dac | advance_duel_turn_by_prng_anim | setPlateComment substring replace |
| 0x08095b3c | FUN_080954e8 | step_prng_anim_frame | setPlateComment substring replace |

Total PLATE: 6 plate repairs.

---

## carve 计划 (R7, 如有)

None. No ROM data tables referenced from segment code require carving into rom.s.

---

## disasm 计划 (R4)

### Block1: 0x08095274 / 0xc0  THUMB  (10-entry jump table / 9 unique case-block entry points)

These are RAW-pointer jump targets for dispatch_equip_confirm_phase_by_step, dispatched via
`mov pc, r0` (.hword 0x4687 = THUMB-encoded MOV PC, r0 -- which treats the table entries as
raw pointers, not THUMB+1). All 10 cases jump back to epilogue at 0x08095334+ or shared path
at 0x8095338.

The block spans 0x08095274..0x08095333 (0xc0 bytes). Case boundaries:
```
0x08095274  Case[7+8]: ldr+ldrh+bl+b  (4 insns + .zero + pool)
0x08095284  Case[4]:   bl+b            (2 insns)
0x0809528a  Case[5]:   movs+b          (2 insns, falls to case[3]+1)
0x0809528e  Case[6]:   movs+b          (2 insns, falls to shared path)
0x8095290   [shared b target for case6]
0x8095292   Case[3]+[6-fall]: movs+movs+movs+bl+b
0x809529e   Case[1]:   movs+movs+movs+bl+b
0x80952aa   Case[2]:   larger sequence with cmp/b tree
0x8095304   Case[9]:   bl+b
0x809530a   Case[0]:   ldr+adds+ldr+ldr+adds+ldr+adds+subs+movs+rsbs+bl+ldr+adds+b+.zero+pool*3
```

Procedure:
- clearListing 0x08095274 .. 0x08095334 (entire block)
- setTMode THUMB for [0x08095274, 0x08095334)
- DisassembleCommand at 0x08095274  (case[7+8])
- DisassembleCommand at 0x08095284  (case[4])
- DisassembleCommand at 0x0809528a  (case[5])
- DisassembleCommand at 0x0809528e  (case[6])
- DisassembleCommand at 0x08095292  (case[3], includes shared fall-through from case[5]+[6])
- DisassembleCommand at 0x0809529e  (case[1])
- DisassembleCommand at 0x80952aa   (case[2])
- DisassembleCommand at 0x8095304   (case[9])
- DisassembleCommand at 0x809530a   (case[0])
- createDWord on each pool word inside block (0x8095280, 0x80952cc, 0x80952d0, 0x8095328, 0x809532c, 0x8095330)
- No createFunction for any case block (jump targets inside dispatch_equip_confirm_phase_by_step, not standalone)
- Post-disasm: ROM_INCBIN/.byte-code grep in [0x08095274, 0x08095334) == 0

Pool words in Block1 already use REUSE constants (ELIGIB_ACT_TYPE_OFF/ELIGIB_ANIM_STATE_OFF/
ELIGIB_SPRITE_CTRL_OFF/ELIGIB_STATE_CTRL_OFF -- all in ewram.inc). No new equates needed from
these pool words (they are already named from Seg-1 Seg-7 work).

### Block2: 0x08095b28 / 0x14  THUMB  (orphan fn, 0 refs -> §5.1 ONLY, no disasm)

---

## 新增 constants / 全局 (必须先证明现有 inc 无可复用)

All new constants verified by VALUE grep in constants/*.inc returning 0 hits before marking NEW.

### constants/card_info.inc (新增 1)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| NEGATE_ATTACK_CID | 0x000012c4 | card-stats.s: card_0648 "Negate Attack" slot=0x12C4 pw=14315573; update_card_display_index_by_type_rules: special player-side XOR path when card_id==0x12c4 (Negate Attack effect display rule); grep 0x12c4 card_info.inc=0; conf: high | 8 |

### constants/ewram.inc (新增 8 offsets)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| LP_EQUIP_STATE_B_OFF | 0x00001d50 | play_equip_ui_effect_3_with_state_gate: [gP1LifePoints+0x1d50] secondary equip slot state flag; if==0: set to 1 then dispatch_card_display_op(3,0,0,0); if nonzero: check if busy then return 1 waiting. Adjacent to ACTIVATION_STATE_C_OFF=0x1d4c(+4) and ELIGIB_STATE_CTRL_OFF=0x1d54(+4). grep 0x1d50 constants/=0; conf: high | 7 |
| LP_DISPLAY_STATE_OFF | 0x00001d0c | step_prng_anim_frame: b LAB_08095b12 path writes 1 to [gP1LifePoints+0x1d0c] (LP display control); get_lp_display_state_word: returns [gP1LifePoints+0x1d0c]; caseD_1 and caseD_4 also write 1 to this field. grep 0x1d0c constants/=0; conf: high | 7 |
| LP_PLAYER_SIDE_CACHE_OFF | 0x00001d64 | step_prng_anim_frame caseD_e and caseD_11: [gP1LifePoints+0x1d64] := [gDuelCardCtxBase+4] XOR 1 (inverted player_id copy); init_zone_activation_display_fields plate (L5402) confirms "[+0x1d64]:=[0x0201e2a0+4]"; used as player_side cache for LP display; grep 0x1d64 constants/=0; conf: high | 25 |
| LP_EQUIP_DISPLAY_FLAG_OFF | 0x00001d84 | caseD_1e: str 1 to [gP1LifePoints+0x1d84] after setup_lp_display_row_with_data completes; an equip LP display active flag; grep 0x1d84 constants/=0; conf: high | 7 |
| LP_ACTIVATION_TYPE_ARRAY_BASE_OFF | 0x000010e1 | caseD_18: r1 = gP1LifePoints + field_slot*4 + 0x10e1 -> ORs bit7 into per-slot activation type byte; asm L6872 plate comment confirms "type_field_offset=0x10e1"; grep 0x10e1 constants/=0; conf: high | 9 |

### constants/ewram.inc (新增 4 gSpriteAttrBuf offsets)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SPRITE_ROW_BUSY_BYTE_OFF | 0x00000301 | gSpriteAttrBuf+0x301 = primary busy/status byte for sprite row; target of ORs (0x4, 0x8, 0x10, 0x20, 0x40) in cases D_1a/1b/1c/1d/1f+LAB; 157 ROM refs confirms heavy usage; grep 0x301 constants/=0; conf: high | 157 |
| SPRITE_ROW_ENTRY_30D_OFF | 0x0000030d | gSpriteAttrBuf+0x30d = control byte cleared to 0 in caseD_1c before activating effect entry; adjacent cluster byte; grep 0x30d constants/=0; conf: high | 28 |
| SPRITE_ROW_ENTRY_30E_OFF | 0x0000030e | gSpriteAttrBuf+0x30e = control byte cleared to 0 in caseD_1a; grep 0x30e constants/=0; conf: high | 19 |
| SPRITE_ROW_ENTRY_30F_OFF | 0x0000030f | gSpriteAttrBuf+0x30f = control byte cleared to 0 in LAB_08095a48; grep 0x30f constants/=0; conf: high | 18 |

### constants/ewram.inc (新增 3 gSpriteAttrBuf byte offsets -- small cluster)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SPRITE_ATTR_BYTE_2FE_OFF | 0x000002fe | gSpriteAttrBuf+2+0x2fe = gSpriteAttrBuf+0x300 relative byte; ORed with direction bits in caseD_e/11; step_prng_anim_frame adds r4,r4,r2 where r4=gSpriteAttrBuf+2, r2=0x2fe; 98 ROM refs; grep 0x2fe constants/=0; conf: high | 98 |
| SPRITE_ATTR_BYTE_2FF_OFF | 0x000002ff | gSpriteAttrBuf+2+0x2ff relative byte; ORed with control bits in caseD_1f; 198 ROM refs; grep 0x2ff constants/=0; conf: high | 198 |

### constants/ewram.inc (新增 1 gSpriteAttrBuf+2 global alias)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| gSpriteAttrBufData | 0x0201b872 | gSpriteAttrBuf+2 = halfword start of actual sprite attribute data (fields after the 2-byte type header); consistently used as copy destination/source alongside gEquipZoneRankState/gEquipChainEntryBase; 8 ROM refs; grep 0x0201b872 constants/=0; conf: high |  8 |

### constants/duel_field.inc or constants/ewram.inc (新增 2 pack_sprite_row_attr_words masks)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SPRITE_HIGH_HALF_MASK | 0xffff0000 | pack_sprite_row_attr_words: ands r1,r4 at 0x08095398 = clear low 16 bits of sprite attr word in packing operation; domain = sprite row attribute packing, NOT equip chain sentinel (EQUIP_CHAIN_SENTINEL=0xffff0000 in duel_field.inc:272 is a DIFFERENT use: list terminator for gEquipChainSlotRefs); register context (r4=loaded mask, ands with r1 to form high half) confirms packing domain; value conflict documented; new constant in duel_field.inc; conf: high | 2 |
| SPRITE_ROW_BITS18_15_CLEAR_MASK | 0xfff87fff | dispatch_sprite_row_write_by_type caseD_2: ands r0,r3 clears bits[18:15] of existing sprite row word before ORing new direction field ((new_dir&0xf)<<15); grep 0xfff87fff constants/=0; conf: high | 2 |

### constants/duel_field.inc (新增 2 sprite dispatch table)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SPRITE_ROW_DISPATCH_TABLE | 0x080953dc | dispatch_sprite_row_write_by_type: self-referential switch table (30 entries, 2 targets: caseD_2/caseD_4); DAT_080953d8 holds address; grep 0x080953dc constants/=0; 1 ROM ref; conf: high | 1 |

---

## §5.1 登记 (Rule 3) -- 0 引用块

| ROM off | size | vaddr | 初判内容 | 登记理由 |
|---------|------|-------|----------|----------|
| 0x95b28 | 0x14 | 0x08095b28 | set_lp_display_state_active (orphan THUMB code; ldr r0,[pc,#8]=gP1LifePoints; ldr r1,[pc,#12]=0x1d0c; adds r0,r0,r1; movs r1,#1; str r1,[r0,#0]; bx lr; pool: gP1LifePoints/LP_DISPLAY_STATE_OFF=0x1d0c) | Full ROM ref-scan: raw=0, THUMB+1=0 for all 2-byte-aligned addresses. NOT fall-through: preceding function step_prng_anim_frame ends with pop/pop/bx r1 explicit epilogue at 0x08095b18..0x08095b1c. ROM_INCBIN preserved; no Ghidra ops per hard rule 3. |

---

## 消費者証拠 (R6) -- 关键槽语义的 file:line + 置信度

| slot | consumer evidence | confidence |
|---|---|---|
| gDuelFieldSlots (0x0201c510) | asm/12 L2247: DAT_08095190=0x0201c510 "gDuelFieldSlots"; ewram.inc:314 confirms; write_monster_zone_display_indices scans [gDuelFieldSlots+player*0x868+slot*0x14] | high |
| LP_EQUIP_STATE_B_OFF (0x1d50) | asm/12 L2307 DWORD_08095208 adjacent L2330 DWORD_0809520c=0x1d50; play_equip_ui_effect_3_with_state_gate reads/writes [gP1LifePoints+0x1d50] as secondary equip slot state; adjacent ACTIVATION_STATE_C_OFF=0x1d4c (+4) and ELIGIB_STATE_CTRL_OFF=0x1d54 (+4) sandwich this field | high |
| LP_DISPLAY_STATE_OFF (0x1d0c) | asm/12 L3402: get_lp_display_state_word plate "state_offset=0x1d0c"; L2641 DAT_08095530=0x1d0c used in step_prng_anim_frame to dispatch lp anim; 7 ROM refs | high |
| LP_PLAYER_SIDE_CACHE_OFF (0x1d64) | asm/12 L3038 DAT_0809586c=0x1d64; asm/12 L5402 plate init_zone_activation_display_fields: "[+0x1d64]:=[0x0201e2a0+4]"; 25 ROM refs | high |
| LP_EQUIP_DISPLAY_FLAG_OFF (0x1d84) | asm/12 L3069 DAT_080958a8=0x1d84; caseD_1e: setup_lp_display_row_with_data then str 1 to [gP1LifePoints+0x1d84]; 7 ROM refs | high |
| LP_ACTIVATION_TYPE_ARRAY_BASE_OFF (0x10e1) | asm/12 L6872 plate fill_slot_activation_state_array: "type_field_offset=0x10e1"; asm/12 L3278 DAT_08095a44=0x10e1 caseD_18; L7152 plate same usage | high |
| SPRITE_ROW_BUSY_BYTE_OFF (0x301) | asm/12 L3121 DAT_08095910=0x301; multiple cases OR different bits (0x4/8/10/20/40) into [gSpriteAttrBuf+0x301]; 157 ROM refs | high |
| NEGATE_ATTACK_CID (0x12c4) | asm/12 L2061 DAT_08095020=0x12c4; card-stats.s L8439 "card_0648: Negate Attack slot=0x12C4"; update_card_display_index_by_type_rules: cmp r2,r0 when card_id=0x12c4 then XOR player_side | high |
| gSpriteAttrBufData (0x0201b872) | asm/12 L2744 DAT_08095638=0x0201b872; copy_bytes_by_halfword dst; consistently used as halfword-offset start of gSpriteAttrBuf data fields (+2 from type header); 8 ROM refs | high |
| SPRITE_HIGH_HALF_MASK (0xffff0000) | asm/12 L2472 DAT_080953bc=0xffff0000; pack_sprite_row_attr_words: ands r1,r4 at L2454 clears low half before shift-OR; domain-distinct from EQUIP_CHAIN_SENTINEL (gEquipChainSlotRefs terminator, duel_field.inc:272) | high |

---

## 求助 (如有低置信度语义)

No BLOCKED items. All constants have high-confidence semantics from direct consumer evidence.

OPEN QUESTION (med-conf): SPRITE_ATTR_BYTE_2FE_OFF (0x2fe) naming:
  In caseD_e: `ldr r4, DAT_08095770 = gSpriteAttrBuf+2`; `ldr r2, DAT_08095788 = 0x2fe`; `adds r4,r4,r2` -> r4 = gSpriteAttrBuf+2+0x2fe = gSpriteAttrBuf+0x300. This then has `strb r0,[r4,#0]` for the direction bits. But gSpriteAttrBuf+0x300 is also described as the "busy_flag_offset=0x300" in the step_prng_anim_frame plate (L2603). So 0x2fe is an offset from gSpriteAttrBuf+2 (=gSpriteAttrBufData) to reach the same +0x300 location. This is slightly indirect naming. I name it SPRITE_ATTR_BYTE_2FE_OFF as the offset from the +2 base to reach the +0x300 busy byte area. Conf: med on naming convention (value semantics are clear, naming of +2-base offsets is design choice).

OPEN NOTE: gSpriteAttrBuf+0x300 appears both as `0xc0*4` computed in code and as `gSpriteAttrBufData + 0x2fe` via DAT slots. The existing ewram.inc describes `gSpriteAttrBuf+0x300=filled_flags` but no constant exists. This proposal does not create a SPRITE_ROW_STRIDE_OFF constant for 0x300 (=0xc0<<2) as it is always computed inline. Fixer may choose to add it if desired.
