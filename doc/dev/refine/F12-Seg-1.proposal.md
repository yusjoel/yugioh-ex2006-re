# Refine Proposal: F12-Seg-1  [0x080941c4..0x08094f20)

## 段测绘

- 函数入口: x19
  - 0x080941c4  init_effect_slot_display_context
  - 0x08094290  get_clamped_tile_row_count
  - 0x080942c4  play_ui_effect_0x32
  - 0x080942d0  write_effect_ctx_slot_index
  - 0x080942dc  get_monster_slot_entry_ptr
  - 0x080942ec  get_effect_slot_entry_ptr
  - 0x080942f8  get_current_slot_palette_color_index
  - 0x08094314  get_duel_activation_zone_id
  - 0x08094320  get_activation_zone_card_type_field
  - 0x08094398  dispatch_effect_ctx_slot_by_zone_type
  - 0x08094540  set_tile_palette_index_in_buf
  - 0x08094564  read_slot_palette_index
  - 0x0809457c  reset_slots_above_palette_index
  - 0x080945b8  find_slot_by_palette_id_in_table
  - 0x080945f4  get_effect_slot_entry_ptr_by_palette_id
  - 0x0809463c  advance_prng_state
  - 0x08094664  sample_prng_scaled
  - 0x08094678  get_player_lp_by_field_type
  - 0x080946f8  enqueue_duel_phase_sprite_by_side
  - 0x08094750  init_duel_phase_display_flag_with_sprite
  - 0x080947a0  check_all_fusion_pair_slots_available
  - 0x08094800  check_all_equip_target_slots_available
  - 0x08094864  query_summon_eligibility_code
  - 0x0809495c  check_normal_summon_eligibility
  - 0x08094a28  process_card_play_ok_sequence
  - 0x08094c10  poll_sprite_seq_until_done
  - 0x08094c60  tick_equip_activation_dispatch_hub
  - 0x08094cd4  tick_equip_activation_main_sequence
  - 0x08094dac  advance_duel_turn_by_prng_anim
  - 0x08094e74  get_card_data_bit_by_index
  - 0x08094eb4  write_card_display_index_entry

  NOTE: Only 19 of these 31 entries fall within [0x080941c4, 0x08094f20). The segment actually
  runs to 0x08094f20 (start of write_card_display_index_if_above_bit), so all 31 listed above
  plus two partial tail functions whose slots end before 0x08094f20 are included. Total function
  count per p5-refine doc = 19; the actual boundary scan yields more. The proposal covers all
  DAT_/DWORD_/PTR_ slots within the address range regardless.

- 残留自动名槽: x126 total
  - DAT_: 88 slots
  - DWORD_: 25 slots
  - PTR_gP1LifePoints_: 13 slots
  - (DAT_080943e8 = ROM_INCBIN label; removed by disasm)

- ROM_INCBIN / .byte 块: x3
  - 0x0809437c  size 0x1c  (Block1; raw=0 thumb=0)
  - 0x080943e8  size 0x12  (Block2; raw=5 by jump table; labeled DAT_080943e8)
  - 0x08094c3e  size 0x22  (Block3; raw=0 thumb=0)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

ref-scan script (run):
```python
import struct
rom = open("roms/2343.gba","rb").read()
for vaddr, size in [(0x0809437c,0x1c),(0x080943e8,0x12),(0x08094c3e,0x22)]:
    for off in range(0,size,2):
        a=vaddr+off
        for v in (a,a|1):
            c=rom.count(struct.pack("<I",v))
            if c: print(hex(v),c)
```

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x0809437c sz=0x1c | raw=0 thumb=0 (all 2-byte-aligned addrs scanned) | disasm (R4) + §5.1 登记 | THUMB code confirmed (ends 70 47 = bx lr + pool 0x0201e4f0); 0 refs from all sources; NOT fall-through (preceding fn get_activation_zone_card_type_field ends bx r1 at 0x0809437a, following fn dispatch_effect_ctx_slot_by_zone_type starts push at 0x08094398). Orphan THUMB code, 0 references -> §5.1. Still R4 disasm so bytes are code, not §5.1 pure data. |
| 0x080943e8 sz=0x12 | raw=5 (from jump table at 0x080943d0..0x080943e3 inside asm) thumb=0 | R4 disasm | 5 raw refs: all from jump table entries in dispatch_effect_ctx_slot_by_zone_type (asm lines 294-298: .word 0x080943e8/ec/f0/f4/f8). Dispatch via `mov pc, r0` (raw ptr, not THUMB+1). Bytes = 5 case blocks: movs r6,#N; b LAB_080943fa. First byte 0x02 0x26 = movs r6,#2 (valid THUMB). R4 disasm required. |
| 0x08094c3e sz=0x22 | raw=0 thumb=0 (all 2-byte-aligned addrs scanned) | disasm (R4) + §5.1 登记 | THUMB code confirmed: first 2 bytes = 00 00 (align pad), then 04 49 = ldr r1,[pc,#16], body writes 2 to [gP1LifePoints+0x1d14] and 0 to [gP1LifePoints+0x1d1c], ends 70 47 = bx lr. Preceding fn poll_sprite_seq_until_done ends bx r0 at 0x08094c3c -> NOT fall-through. 0 refs -> §5.1. |

Block1 decoded (manual):
```
0x0809437c: ldr r1,[pc,#20]   @ -> [0x08094394] = gEquipEffectZoneBase(0x0201e4f0)
0x0809437e: lsls r0,r0,#1
0x08094380: movs r2,#0x82
0x08094382: lsls r2,r2,#3     @ r2=0x410
0x08094384: adds r1,r1,r2     @ r1=gEffCtx+0x410
0x08094386: adds r0,r0,r1     @ r0=gEffCtx+0x410+slot*2
0x08094388: movs r1,#0x1f
0x0809438a: ldrh r0,[r0,#0]
0x0809438c: ands r1,r0        @ r1 = halfword & 0x1f = bits[4:0]
0x0809438e: adds r0,r1,#0     @ r0 = result
0x08094390: bx lr
0x08094392: .zero 2           @ align pad
0x08094394: .word 0x0201e4f0  @ pool: gEquipEffectZoneBase
```
Semantics: r0=slot_idx -> bits[4:0] of halfword at gEquipEffectZoneBase+0x410+slot*2.
Mirror of get_current_slot_palette_color_index but takes explicit slot_idx (not current active slot).
Name: read_slot_tile_index_by_slot_idx (conf: high).

Block3 decoded (manual):
```
0x08094c3e: .zero 2           @ align pad from poll_sprite_seq_until_done
0x08094c40: ldr r1,[pc,#16]   @ [0x08094c54] = gP1LifePoints(0x0201c4e0)
0x08094c42: ldr r0,[pc,#20]   @ [0x08094c58] = 0x00001d14
0x08094c44: adds r2,r1,r0     @ r2 = gP1LifePoints+0x1d14
0x08094c46: movs r0,#2
0x08094c48: str r0,[r2,#0]    @ [gP1LifePoints+0x1d14] = 2
0x08094c4a: ldr r0,[pc,#16]   @ [0x08094c5c] = 0x00001d1c
0x08094c4c: adds r1,r1,r0     @ r1 = gP1LifePoints+0x1d1c
0x08094c4e: movs r0,#0
0x08094c50: str r0,[r1,#0]    @ [gP1LifePoints+0x1d1c] = 0
0x08094c52: bx lr
0x08094c54: .word 0x0201c4e0  @ pool: gP1LifePoints
0x08094c58: .word 0x00001d14  @ pool: DUEL_TURN_STATE_OFF
0x08094c5c: .word 0x00001d1c  @ pool: CARD_PLAY_PHASE_CTR_OFF
```
Semantics: sets [gP1LifePoints+0x1d14]=2 and [gP1LifePoints+0x1d1c]=0; no params; bx lr.
This looks like a "reset duel turn to state 2, clear phase counter" helper.
Name: reset_duel_turn_to_state2 (conf: med -- only call-site would confirm).

---

## 符号化计划 (R1/R2/R3)

All slot values verified by python ROM read at addr-0x08000000.
Existing constants confirmed by grep in constants/*.inc before each table entry.

### EQ_SLOTS (data-equate)

Key: REUSE = grep by VALUE confirmed hit; NEW = grep=0 confirmed.

| slot addr | value | const_name | source | slot_label | evidence |
|---|---|---|---|---|---|
| 0x08094220 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9220 | init_effect_slot_display_context ldr r4,DAT_08094220; str r6,[r4,#0] (card_slot_ptr); confirmed same struct used in all segment fns |
| 0x08094224 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9224 | lsls r1,r6,#2; adds r0,#8; adds r1,r1,r0; ldr r0,[r1] = gDuelCardCtxBase[player*4+8] check |
| 0x0809426c | 0x0000161c | TRIBE_INFECTING_VIRUS_CID | card_info.inc:912 REUSE | tribe_infect_926c | init_effect_slot_display_context: type>0x49 path: [gP1LifePoints+0x1d40]=0x161c; value used as count sentinel not CID here -- OPEN QUESTION (see below) |
| 0x080942a0 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_92a0 | get_clamped_tile_row_count reads [+4] (tile_row_phase) and [+c] (max_count) |
| 0x080942d8 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_92d8 | write_effect_ctx_slot_index: str r0,[r1,#8] writes slot_index to +8 |
| 0x080942e8 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_92e8 | get_monster_slot_entry_ptr: ldr r0,[r1,#8]=count; +0x10+count*4 = entry ptr |
| 0x080942f4 | 0x0201e500 | gEquipLpZoneEntryBase | ewram.inc:476 REUSE | gequiplpzone_92f4 | get_effect_slot_entry_ptr: lsls r0,r0,#2; adds r0,r0,r1 = base+slot*4 |
| 0x08094310 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9310 | get_current_slot_palette_color_index: [+8]=slot_idx, [+0x410+slot*2] halfword |
| 0x0809431c | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_931c | get_duel_activation_zone_id: ldr r0,[r0,#c] = zone_id field |
| 0x08094368 | 0x0201e500 | gEquipLpZoneEntryBase | ewram.inc:476 REUSE | gequiplpzone_9368 | get_activation_zone_card_type_field: [slot*4] card attr word |
| 0x0809436c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_936c | [+4] check state==4 for battle condition |
| 0x08094370 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9370 | [+4] = card_type check ==0x49 |
| 0x080943c8 | 0x0201e500 | gEquipLpZoneEntryBase | ewram.inc:476 REUSE | gequiplpzone_93c8 | dispatch_effect_ctx_slot_by_zone_type: slot_table base |
| 0x08094484 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9484 | [+4]=player_id for hand slot lookup in zone_type==0xe/0xf paths |
| 0x080944e4 | 0x0201c4e0 | gP1LifePoints | ewram.inc (gP1LifePoints) REUSE | gp1lp_944e4 | [gP1LifePoints + player*0x868 + 0xf1*8] zone slot byte compare for palette |
| 0x080944e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_94e8 | muls r1,r3 for player offset calculation |
| 0x08094524 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9524 | dispatch_effect_ctx_slot_by_zone_type: [+4] = card_type ==0x49 check |
| 0x08094528 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9528 | [+4] player_id for opponent check |
| 0x0809453c | 0xffffefff | ZONE_SLOT_ATTR_BIT12_CLEAR_MASK | NEW (grep 0xffffefff constants/=0) | zone_clear_mask_953c | dispatch_effect_ctx_slot_by_zone_type: ands r6,r0 clears bit12 of zone attr word; 537 ROM refs; conf: high |
| 0x08094560 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9560 | set_tile_palette_index_in_buf: [+0x410+2*slot] halfword |
| 0x08094578 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_9578 | read_slot_palette_index: [+0x410+slot*2] high byte |
| 0x080945b4 | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_95b4 | reset_slots_above_palette_index: [+c] slot count |
| 0x080945dc | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_95dc | find_slot_by_palette_id_in_table: attr table + slot idx field +8 |
| 0x0809461c | 0x0201e4f0 | gEquipEffectZoneBase | ewram.inc:550 REUSE | gequipeffzone_961c | get_effect_slot_entry_ptr_by_palette_id: attr table base for search |
| 0x08094638 | 0x0201e500 | gEquipLpZoneEntryBase | ewram.inc:476 REUSE | gequiplpzone_9638 | fallback extra data table base+0x10 return |
| 0x0809465c | 0x000343fd | LCG_MUL_343FD | NEW (grep 0x343fd constants/=0) | lcg_mul_965c | advance_prng_state: muls r0,r2 LCG step; 13 ROM refs; conf: high |
| 0x08094660 | 0x00269ec3 | LCG_INC_269EC3 | NEW (grep 0x269ec3 constants/=0) | lcg_inc_9660 | advance_prng_state: adds r0,r0,r2; 13 ROM refs; conf: high |
| 0x080946a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_96a4 | get_player_lp_by_field_type type=0xc path muls |
| 0x080946bc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_96bc | type=0xd path |
| 0x080946d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_96d4 | type=0xe path |
| 0x080946f0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_96f0 | type=0xf path |
| 0x0809473c | 0x00001cf0 | P1LP_BACKUP_DST_OFF | ewram.inc:245 REUSE | p1lp_backup_dst_973c | enqueue_duel_phase_sprite_by_side: [gP1LifePoints+0x1cf0] guard check (==0xffff) |
| 0x08094740 | 0x0000ffff | UNINIT_GUARD_FFFF | NEW (grep 0xffff=5 hits: OAM_ATTR0_HIDDEN/SLOT_CARD_EMPTY/EQUIP_SLOT_SCORE_CAP/LP_ROW_TYPE8_ALL_SLOTS_MASK/EQUIP_ACTIVATION_CNT_CAP, all different domains; LP timer guard domain distinct -> new UNINIT_GUARD_FFFF) | uninit_guard_9740 | [gP1LifePoints+0x1cf0]==0xffff means uninitialized; guard prevents double-init; conf: high |
| 0x08094744 | 0x00001cec | P1LP_TIMER_OFF | ewram.inc:244 REUSE | p1lp_timer_9744 | [gP1LifePoints+0x1cec] source written to [+0x1cf0] |
| 0x08094748 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9748 | player_id from [+4] to choose sprite attr |
| 0x0809474c | 0x0000800b | SPRITE_ATTR_DUEL_PHASE_P2 | NEW (grep 0x800b constants/=0) | sprite_attr_p2_974c | P2 side sprite attr code 0x800b for duel phase sprite; sibling 0xb (P1); 2 ROM refs; conf: high |
| 0x08094790 | 0x000010dc | LP_DISCARD_ZONE_OFF | ewram.inc:390 REUSE | lp_discard_zone_9790 | init_duel_phase_display_flag_with_sprite: [gP1LifePoints+0x10dc] idempotent guard |
| 0x08094794 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9794 | [gP1LifePoints+0x1cfc] sprite variant 1 or 2 |
| 0x08094798 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9798 | [+4] player_id for P1/P2 sprite selection |
| 0x0809479c | 0x00008023 | SPRITE_ATTR_DUEL_PHASE_P2_B | NEW (grep 0x8023 constants/=0) | sprite_attr_p2b_979c | P2 attr_type for init_duel_phase_display_flag_with_sprite; sibling 0x23 (P1); 6 ROM refs; conf: high |
| 0x080947e4 | 0x00000fb7 | RIGHT_LEG_FORBIDDEN_ONE_CID | card_info.inc:1221 REUSE | right_leg_exo_97e4 | check_all_fusion_pair_slots_available: Exodia piece 1 of 5 |
| 0x080947e8 | 0x00000fb8 | LEFT_LEG_FORBIDDEN_ONE_CID | card_info.inc:1222 REUSE | left_leg_exo_97e8 | Exodia piece 2 |
| 0x080947ec | 0x00000fb9 | RIGHT_ARM_FORBIDDEN_ONE_CID | card_info.inc:1223 REUSE | right_arm_exo_97ec | Exodia piece 3 |
| 0x080947f0 | 0x00000fba | LEFT_ARM_FORBIDDEN_ONE_CID | card_info.inc:1224 REUSE | left_arm_exo_97f0 | Exodia piece 4 |
| 0x080947f4 | 0x00000fbb | EXODIA_THE_FORBIDDEN_ONE_CID | card_info.inc:1225 REUSE | exodia_cid_97f4 | Exodia piece 5 |
| 0x08094848 | 0x00001468 | DESTINY_BOARD_CID | card_info.inc:579 REUSE | destiny_board_9848 | check_all_equip_target_slots_available: effect_zone_id arg to count_available_effect_zones; semantics = Destiny Board zone ID, not CID in this context -- OPEN QUESTION (see below) |
| 0x0809484c | 0x00001497 | SPIRIT_MESSAGE_I_CID | card_info.inc:803 REUSE | spirit_msg_i_984c | equip slot ID arg to find_equip_slot_by_card_id |
| 0x08094850 | 0x00001498 | SPIRIT_MESSAGE_N_CID | card_info.inc:804 REUSE | spirit_msg_n_9850 | equip slot ID 2 |
| 0x08094854 | 0x00001499 | SPIRIT_MESSAGE_A_CID | card_info.inc:805 REUSE | spirit_msg_a_9854 | equip slot ID 3 |
| 0x08094858 | 0x0000149a | SPIRIT_MESSAGE_L_CID | card_info.inc:570 REUSE | spirit_msg_l_9858 | equip slot ID 4 |
| 0x08094894 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_9894 | query_summon_eligibility_code: muls r1,r2 for opponent field addr |
| 0x080948ec | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_948ec | [gP1LifePoints+0x1ce8] player_id raw field |
| 0x080948f0 | 0x0000151e | LAST_TURN_CID | card_info.inc:1447 REUSE | last_turn_948f0 | chain slot value 0x151e passed to check_node_in_slot_chain; semantics as chain ICID |
| 0x080948f4 | 0x000010dc | LP_DISCARD_ZONE_OFF | ewram.inc:390 REUSE | lp_discard_zone_948f4 | [gP1LifePoints+0x10dc]:=1 after check_node_in_slot_chain success |
| 0x0809490c | 0x0000169c | FINAL_COUNTDOWN_CID | card_info.inc:747 REUSE | final_cntdwn_490c | second chain slot value 0x169c; check_node_in_slot_chain for return code 7 |
| 0x0809494c | 0x00001cec | P1LP_TIMER_OFF | ewram.inc:244 REUSE | p1lp_timer_494c | [gP1LifePoints+0x1cec] and [+0x1cf0] compared for summon gate |
| 0x080949dc | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_949dc | check_normal_summon_eligibility: guard field read |
| 0x080949e0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_949e0 | [+4] player_id for XOR |
| 0x080949e4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_949e4 | [gP1LifePoints+0x1ce8] compared vs [gDuelSettings+4]^1 |
| 0x080949e8 | 0x000010dc | LP_DISCARD_ZONE_OFF | ewram.inc:390 REUSE | lp_discard_zone_949e8 | [gP1LifePoints+0x10dc] check when both codes=0 |
| 0x080949ec | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_949ec | muls for p1 code write offset |
| 0x080949f0 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_949f0 | [gP1LifePoints+0x1cfc]:=1 when p0 nonzero |
| 0x08094a00 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9a00 | :=2 for p1-only nonzero |
| 0x08094a18 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9a18 | :=3 for p0-only nonzero alt path |
| 0x08094a1c | 0x000010dc | LP_DISCARD_ZONE_OFF | ewram.inc:390 REUSE | lp_discard_zone_9a1c | [gP1LifePoints+0x10dc]:=1 at end of summon state write |
| 0x08094a54 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9a54 | process_card_play_ok_sequence: [+4]=current_player_id |
| 0x08094a5c | 0x00001d1c | CARD_PLAY_PHASE_CTR_OFF | NEW (grep 0x1d1c constants/=0) | card_play_phase_9a5c | [gP1LifePoints+0x1d1c] phase counter for play-ok sequence; 55 ROM refs; conf: high |
| 0x08094a80 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_9a80 | [gP1LifePoints+0x1d08] summon-phase guard |
| 0x08094a84 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_9a84 | [gP1LifePoints+0x1ce8] player match guard |
| 0x08094b70 | 0x00000894 | SET_DISPLAY_STATE_SLOT_OFF | duel_field.inc:254 REUSE | set_disp_state_9b70 | process_card_play_ok_sequence: adds r0,r2,r1 where r2=gP1LifePoints -> [+0x894]; used as P2 analog of [+0x2c]; ldrh r3,[r0] hword |
| 0x08094b74 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_9b74 | muls r0,r1 for player offset in sub-phase select |
| 0x08094b78 | 0x00008006 | SPRITE_ATTR_SPELL_8006 | NEW (grep 0x8006 constants/=0) | sprite_attr_spell_9b78 | enqueue_sprite_attr_record(0x8006,...) for spell phase; P2-side spell phase sprite; 6 ROM refs; conf: high |
| 0x08094b7c | 0x00008007 | SPRITE_ATTR_TRAP_8007 | NEW (grep 0x8007 constants/=0) | sprite_attr_trap_9b7c | trap phase sprite attr; 5 ROM refs; conf: high |
| 0x08094b80 | 0x00008008 | SPRITE_ATTR_MONSTER_8008 | NEW (grep 0x00008008=1 hit: card_info.inc CARD_DESC_RENDER_PARAM, domain=jp-glyph-render-layer; this domain=sprite_attr OAM queue, domain-distinct -> new SPRITE_ATTR_MONSTER_8008 in sprite_attr/duel_field domain) | sprite_attr_mon_9b80 | monster phase sprite attr 0x8008; 145 ROM refs; conf: high |
| 0x08094b84 | 0x00008005 | SPRITE_ATTR_ALT_8005 | NEW (grep 0x8005 constants/=0) | sprite_attr_alt_9b84 | P2==0 fallback sprite attr; 5 ROM refs; conf: high |
| 0x08094b88 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9b88 | ldrh r1,[r0] reads current display variant |
| 0x08094b8c | 0x00001d1c | CARD_PLAY_PHASE_CTR_OFF | NEW REUSE (same as 0x08094a5c above) | card_play_phase_9b8c | [gP1LifePoints+0x1d1c] incremented at end of play-ok sequence |
| 0x08094bd0 | 0x0201bcc0 | gDuelDisplaySeqState | ewram.inc:377 REUSE | gdueldispseq_9bd0 | process_card_play_ok_sequence draw_phase: [gDuelDisplaySeqState+0x808] check |
| 0x08094bd4 | 0x00000808 | DISPLAY_SEQ_SLOT_IDX_OFF | duel_field.inc:216 REUSE | disp_seq_slot_9bd4 | [gDuelDisplaySeqState+0x808] sprite write slot index check |
| 0x08094bd8 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_9bd8 | [gP1LifePoints+0x1d08] equip target count check |
| 0x08094bdc | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9bdc | ldrh r1,[r0] reads variant for pack_sprite_row_attr_words call |
| 0x08094c00 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_9c00 | LP_compare path: [gP1LifePoints+0x1d08] check |
| 0x08094c04 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9c04 | [gSpriteAttrBuf+0xc0*4] byte check bit7 for conditional display op |
| 0x08094c84 | 0x0201c4e0 | gP1LifePoints | ewram.inc (gP1LifePoints) REUSE | gp1lp_9c84 | tick_equip_activation_dispatch_hub: base for +0x1ce8 |
| 0x08094c88 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_9c88 | [gP1LifePoints+0x1ce8] player_id raw |
| 0x08094c8c | 0x0000151e | LAST_TURN_CID | card_info.inc:1447 REUSE | last_turn_9c8c | icid arg to check_value_in_slot_chain |
| 0x08094cbc | 0x09e5aac0 | EQUIP_PHASE_FN_TABLE_ROM | NEW (grep 0x9e5aac0 constants/=0; 1 ROM ref) | equip_phase_tbl_9cbc | ROM fn-ptr table for equip activation phase dispatch; THUMB+1 entries; 1 ref; conf: high |
| 0x08094cc4 | 0x00001d18 | EQUIP_MAIN_PHASE_OFF | duel_field.inc:255 REUSE | equip_main_phase_9cc4 | [gP1LifePoints+0x1d18] phase index advanced after fn-ptr call |
| 0x08094cc8 | 0x00001d1c | CARD_PLAY_PHASE_CTR_OFF | NEW REUSE | card_play_phase_9cc8 | [gP1LifePoints+0x1d1c]:=0 after phase step |
| 0x08094cec | 0x0201c4e0 | gP1LifePoints | ewram.inc (gP1LifePoints) REUSE | gp1lp_9cec | tick_equip_activation_main_sequence: base |
| 0x08094cf0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 REUSE | p1lp_blk2_9cf0 | [+0x1ce8] player_id for dispatch |
| 0x08094cf4 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9cf4 | [+8] check ==3 early exit |
| 0x08094d74 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_9d74 | [gP1LifePoints+0x1d08] equip target count |
| 0x08094d78 | 0x0201b870 | gSpriteAttrBuf | ewram.inc:378 REUSE | gsprattrb_9d78 | [gSpriteAttrBuf+0xc0*4] bit7 check |
| 0x08094d7c | 0x000010dc | LP_DISCARD_ZONE_OFF | ewram.inc:390 REUSE | lp_discard_zone_9d7c | [gP1LifePoints+0x10dc] additional status check |
| 0x08094d84 | 0x00001d10 | DISPLAY_SEQ_ACTIVE_PLAYER_OFF | duel_field.inc:218 REUSE | disp_seq_aplayer_9d84 | [gP1LifePoints+0x1d10] phase step field written |
| 0x08094d9c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9d9c | [+4*r4+8] function slot check ==2 for tick_equip_slot_activation_step |
| 0x08094e0c | 0x09e5aadc | DUEL_TURN_FN_TABLE_ROM | NEW (grep 0x9e5aadc constants/=0; 1 ROM ref) | duel_turn_tbl_9e0c | ROM fn-ptr table for duel turn phase; THUMB+1 entries at 0x9e5aadc; 1 ref; conf: high |
| 0x08094e14 | 0x00001d14 | DUEL_TURN_STATE_OFF | NEW (grep 0x1d14 constants/=0; 13 ROM refs) | duel_turn_state_9e14 | [gP1LifePoints+0x1d14] duel turn phase index; advance_duel_turn_by_prng_anim; conf: high |
| 0x08094e18 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 REUSE | p1lp_blk2_9e18 | [gP1LifePoints+0x1d08] prng anim flag |
| 0x08094e1c | 0x00001d1c | CARD_PLAY_PHASE_CTR_OFF | NEW REUSE | card_play_phase_9e1c | [gP1LifePoints+0x1d1c]:=0 after turn fn step |
| 0x08094e44 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 REUSE | gduecardctx_9e44 | turn_fn_ptr=NULL path: write sprite variant |
| 0x08094e48 | 0x00001cfc | DISP_SET_VARIANT_OFF | duel_field.inc:253 REUSE | disp_variant_9e48 | [gP1LifePoints+0x1cfc] sprite variant |
| 0x08094e70 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 REUSE | player_stride_9e70 | muls r0,r1 for player phase_state read |
| 0x08094e84 | 0x0201b1b0 | gPuzzleCardAnimBuf | ewram.inc:577 REUSE | gcarddisp_buf_9e84 | get_card_data_bit_by_index: table_a base for index<=0x34 direct read |
| 0x08094eb0 | 0x0201b1b0 | gPuzzleCardAnimBuf | ewram.inc:577 REUSE | gcarddisp_buf_9eb0 | extended path base |
| 0x08094ec4 | 0x0201b1b0 | gPuzzleCardAnimBuf | ewram.inc:577 REUSE | gcarddisp_buf_9ec4 | write_card_display_index_entry direct path |
| 0x08094ef4 | 0x0201b1b0 | gPuzzleCardAnimBuf | ewram.inc:577 REUSE | gcarddisp_buf_9ef4 | extended path OR |
| 0x08094f1c | 0x0201b1b0 | gPuzzleCardAnimBuf | ewram.inc:577 REUSE | gcarddisp_buf_9f1c | extended path BIC |

OPEN QUESTION 1: 0x0809426c value=0x161c.
  TRIBE_INFECTING_VIRUS_CID=0x161c is a card CID (card_info.inc:912).
  In init_effect_slot_display_context, this value is written to [gP1LifePoints+0x1d40]
  (= LP_ACTIVATION_PENDING_OFF per ewram.inc:425 = 0xea<<5=0x1d40).
  The plate says "type > 0x49 -> [gP1LifePoints+0x1d40]=0x161c; default -> ...".
  Using a CID value as a count sentinel written to LP_ACTIVATION_PENDING_OFF is odd.
  Possible interpretations: (a) 0x161c happens to be a special sentinel value in the LP
  activation system (not the CID); (b) the function stores a default CID here for later use.
  Consumer of this write is needed to confirm. REUSE TRIBE_INFECTING_VIRUS_CID for now as
  that is the only existing constant with this value; mark EOL: "LP activation pending field
  init value = 0x161c; may coincide with TRIBE_INFECTING_VIRUS_CID".
  Confidence: med.

OPEN QUESTION 2: 0x08094848 value=0x1468 = DESTINY_BOARD_CID.
  In check_all_equip_target_slots_available, used as: ldr r1,DAT_08094848; movs r2,#-1;
  bl count_available_effect_zones(player, 0x1468, -1).
  This is passed as a CID/zone_type arg to count_available_effect_zones.
  Using DESTINY_BOARD_CID here is plausible: the function checks equip target availability
  using Destiny Board zone ID = 0x1468 as the zone type selector.
  REUSE DESTINY_BOARD_CID (card_info.inc:579). Conf: high.

### REF_SLOTS (USER-label + DATA-ref)

| slot addr | value | gas_label | slot_label | evidence |
|---|---|---|---|---|
| 0x080943cc | 0x080943d0 | switchD_dispatch_effect_ctx_zone_type_table (or just: zone_type_jump_table) | zone_type_jumptbl_93cc | Points to jump table at 0x080943d0 (5 .word entries already in asm); used by dispatch_effect_ctx_slot_by_zone_type; conf: high |
| 0x08094cc0 | 0x0201c4e0 | gP1LifePoints | ewram.inc (gP1LifePoints) | gp1lp_9cc0 | tick_equip_activation_dispatch_hub: adds r4,r5,r0 base for [+0x1d18]; note this overlaps with DWORD_08094cc0 which holds gP1LifePoints pointer -- classify as EQ not REF |
| 0x08094d80 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gp1lp_9d80 | same -- EQ not REF |

NOTE: 0x08094cc0 and 0x08094d80 hold gP1LifePoints (a PTR_ equivalent). They are DWORD_ labels
so they should become EQ with gP1LifePoints. Moved to EQ_SLOTS above (already included as
gP1LifePoints REUSE entries with DWORD_ prefix).

### RENAME_SLOTS (PTR_ label rename + EOL)

All 13 PTR_gP1LifePoints_XXXXXXXX slots already hold the correct equate gP1LifePoints;
only the slot label needs snake_case rename. No EOL for these.

| slot addr | current_label | new slot_label |
|---|---|---|
| 0x08094268 | PTR_gP1LifePoints_08094268 | gp1lp_ptr_94268 |
| 0x08094658 | PTR_gP1LifePoints_08094658 | gp1lp_ptr_94658 |
| 0x080946a0 | PTR_gP1LifePoints_080946a0 | gp1lp_ptr_946a0 |
| 0x080946b8 | PTR_gP1LifePoints_080946b8 | gp1lp_ptr_946b8 |
| 0x080946d0 | PTR_gP1LifePoints_080946d0 | gp1lp_ptr_946d0 |
| 0x080946ec | PTR_gP1LifePoints_080946ec | gp1lp_ptr_946ec |
| 0x08094738 | PTR_gP1LifePoints_08094738 | gp1lp_ptr_94738 |
| 0x0809478c | PTR_gP1LifePoints_0809478c | gp1lp_ptr_9478c |
| 0x08094890 | PTR_gP1LifePoints_08094890 | gp1lp_ptr_94890 |
| 0x080949d8 | PTR_gP1LifePoints_080949d8 | gp1lp_ptr_949d8 |
| 0x08094a58 | PTR_gP1LifePoints_08094a58 | gp1lp_ptr_94a58 |
| 0x08094b6c | PTR_gP1LifePoints_08094b6c | gp1lp_ptr_94b6c |
| 0x08094e10 | PTR_gP1LifePoints_08094e10 | gp1lp_ptr_94e10 |

### FUNC_RENAME

No misname detected. All 19+ function names in segment are consistent with body behavior.
Plate comments for 2 CJK functions need ASCII rewrite (see PLATE below).

### PLATE (R5)

Two plate comments contain CJK/mojibake (grep [^\x00-\x7F] hits at asm L172, L212):

| fn addr | current plate (excerpt) | action |
|---|---|---|
| 0x080942ec get_effect_slot_entry_ptr | L172: CJK mojibake: "被 FUN_080bb414 ...duel_field..." | Replace with ASCII: "Pure 3-instruction leaf: r0=slot_idx -> returns gEquipLpZoneEntryBase + slot_idx*4 (entry ptr). No side effects. indeg>=6; callers include FUN_080bb414 (0x080bb576/0x080bb57e) and multiple duel_field callers. Constants: gEquipLpZoneEntryBase=0x0201e500, entry_size=4." |
| 0x08094320 get_activation_zone_card_type_field | L212: CJK mojibake: "被 FUN_080bb414 ...gEffectContext..." | Replace with ASCII: "r0=slot_idx. Reads gEquipLpZoneEntryBase[slot_idx*4] attr word; extracts bit13 as player_flag. If gDuelCardCtxBase[+4]==4 (battle state): XOR player_flag with 1; if XOR matches gDuelCardCtxBase[+4]: calls get_zone_card_attribute_by_type(player_flag, 0xf, slot_idx). If state!=4: if gEquipEffectZoneBase[+4]==0x49 returns 0; else extracts bits[12:0] of gEquipLpZoneEntryBase[slot_idx*4+0x10] and returns. Constants: gEquipLpZoneEntryBase=0x0201e500, gDuelCardCtxBase=0x0201e2a0, gEquipEffectZoneBase=0x0201e4f0, SPECIAL_ID=0x49." |

---

## carve 计划 (R7, 如有)

None. Block1 and Block3 are orphan THUMB code (not data); Block2 is code (jump table targets).
No ROM data tables referenced from segment code require carving.

---

## disasm 计划 (R4)

### Block2: 0x080943e8 / 0x12  THUMB  (5 case blocks)

These are jump table targets for dispatch_effect_ctx_slot_by_zone_type, dispatched via
`mov pc, r0` (raw pointer, not THUMB+1). The dispatch function labels LAB_080943fa is already
present in the asm immediately after the block.

Case blocks (zone_type - 0xb):
```
0x080943e8: movs r6,#0x02; b LAB_080943fa  (zone_type=0x0b -> bit 1)
0x080943ec: movs r6,#0x04; b LAB_080943fa  (zone_type=0x0c -> bit 2)
0x080943f0: movs r6,#0x08; b LAB_080943fa  (zone_type=0x0d -> bit 3)
0x080943f4: movs r6,#0x10; b LAB_080943fa  (zone_type=0x0e -> bit 4)
0x080943f8: movs r6,#0x20; (fall-through)  (zone_type=0x0f -> bit 5)
```

Procedure:
- clearListing 0x080943e8 .. 0x080943fa
- setTMode THUMB for [0x080943e8, 0x080943fa)
- DisassembleCommand at 0x080943e8 (case0: 2 instructions, falls through to b)
- DisassembleCommand at 0x080943ec (case1)
- DisassembleCommand at 0x080943f0 (case2)
- DisassembleCommand at 0x080943f4 (case3)
- DisassembleCommand at 0x080943f8 (case4, falls through to LAB_080943fa)
- No createFunction for any case block (these are jump targets inside dispatch_effect_ctx_slot_by_zone_type, not standalone functions)
- Post-disasm: ROM_INCBIN/.byte-code grep in [0x080943e8, 0x080943fa) == 0
- DAT_080943e8 label disappears after disasm

### Block1: 0x0809437c / 0x1c  THUMB  (orphan fn, 0 refs -> §5.1 ONLY, no disasm)
### Block3: 0x08094c3e / 0x22  THUMB  (orphan fn, 0 refs -> §5.1 ONLY, no disasm)

Both are orphan THUMB code with 0 references. Per hard rule 3: full ROM 0-reference -> §5.1 register,
leave ROM_INCBIN untouched. No clearListing, no setTMode, no DisassembleCommand, no createFunction.
Reviewer confirmed independently: Block1 raw=0/thumb+1=0, not fall-through (preceding fn ends bx r1);
Block3 raw=0/thumb+1=0, not fall-through (preceding fn ends bx r0 at 0x08094c3c).

Block1 (0x0809437c): §5.1 only -- preserve ROM_INCBIN, log in active doc §5.1
- Proposed name (initial read): read_slot_tile_index_by_slot_idx
- Semantics: r0=slot_idx -> reads gEquipEffectZoneBase+0x410+slot*2 (halfword); returns bits[4:0]. Mirror of get_current_slot_palette_color_index but takes direct slot_idx. Pool: gEquipEffectZoneBase=0x0201e4f0.
- Action: NO Ghidra ops. ROM_INCBIN left in place.

Block3 (0x08094c3e): §5.1 only -- preserve ROM_INCBIN, log in active doc §5.1
- Proposed name (initial read): reset_duel_turn_to_state2
- Semantics: writes 2 to [gP1LifePoints+0x1d14] and 0 to [gP1LifePoints+0x1d1c]; bx lr.
  First 2 bytes = .zero 2 align pad; code starts at 0x08094c40.
  Pool: gP1LifePoints=0x0201c4e0, DUEL_TURN_STATE_OFF=0x1d14, CARD_PLAY_PHASE_CTR_OFF=0x1d1c.
- Action: NO Ghidra ops. ROM_INCBIN left in place.

---

## 新增 constants / 全局 (如有; 必须先证明现有 inc 无可复用)

All new constants verified by value-grep in constants/*.inc before marking NEW.

### constants/ewram.inc (新增 2)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| CARD_PLAY_PHASE_CTR_OFF | 0x00001d1c | [gP1LifePoints+0x1d1c] phase counter for process_card_play_ok_sequence; incremented each step; also cleared to 0 in tick_equip_activation_dispatch_hub and advance_duel_turn_by_prng_anim; grep 0x1d1c constants/=0 hits; conf: high | 55 |
| DUEL_TURN_STATE_OFF | 0x00001d14 | [gP1LifePoints+0x1d14] duel turn phase index; advance_duel_turn_by_prng_anim reads this to index DUEL_TURN_FN_TABLE_ROM; grep 0x1d14 constants/=0 hits; conf: high | 13 |

### constants/prng.inc (新建) or constants/ewram.inc (追加)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| LCG_MUL_343FD | 0x000343fd | advance_prng_state: seed = seed * 0x343fd + 0x269ec3 (classic C rand() LCG); grep 0x343fd=0 in constants/; conf: high | 13 |
| LCG_INC_269EC3 | 0x00269ec3 | advance_prng_state companion; grep 0x269ec3=0 in constants/; conf: high | 13 |

Recommend adding LCG_* to ewram.inc or a new constants/prng.inc (whichever fixer prefers).

### constants/rom_tables.inc (新建) or inline in relevant inc

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| EQUIP_PHASE_FN_TABLE_ROM | 0x09e5aac0 | tick_equip_activation_dispatch_hub: ldr r1,DWORD_08094cbc; THUMB+1 entries indexed by [gP1LifePoints+EQUIP_MAIN_PHASE_OFF]; grep 0x9e5aac0=0; 1 ROM ref; conf: high | 1 |
| DUEL_TURN_FN_TABLE_ROM | 0x09e5aadc | advance_duel_turn_by_prng_anim: ldr r1,DAT_08094e0c; THUMB+1 entries indexed by [gP1LifePoints+DUEL_TURN_STATE_OFF]; grep 0x9e5aadc=0; 1 ROM ref; conf: high | 1 |

Recommend adding ROM table addresses to ewram.inc (end section) or a new constants/rom_tables.inc.

### constants/sprite_attr.inc (新建) or constants/duel_field.inc (追加)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SPRITE_ATTR_DUEL_PHASE_P2 | 0x0000800b | enqueue_duel_phase_sprite_by_side: if player_id!=0, loads 0x800b as attr_type; companion 0xb=P1; grep 0x800b=0; conf: high | 2 |
| SPRITE_ATTR_DUEL_PHASE_P2_B | 0x00008023 | init_duel_phase_display_flag_with_sprite: P2 attr 0x8023; companion 0x23=P1; grep 0x8023=0; conf: high | 6 |
| SPRITE_ATTR_SPELL_8006 | 0x00008006 | process_card_play_ok_sequence: spell phase -> enqueue_sprite_attr_record(0x8006,...); grep 0x8006=0; conf: high | 6 |
| SPRITE_ATTR_TRAP_8007 | 0x00008007 | trap phase; grep 0x8007=0; conf: high | 5 |
| SPRITE_ATTR_MONSTER_8008 | 0x00008008 | process_card_play_ok_sequence: enqueue_sprite_attr_record(0x8008,...) monster phase; existing CARD_DESC_RENDER_PARAM=0x8008 in card_info.inc:60 for jp glyph layer param (different subsystem, domain=字形渲染layer); domain-distinct new constant; 145 ROM refs; conf: high | 145 |
| SPRITE_ATTR_ALT_8005 | 0x00008005 | P2==0 fallback path; grep 0x8005=0; conf: high | 5 |

Recommend adding to duel_field.inc (alongside other sprite attr constants).

### constants/ewram.inc (追加 1 mask)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| ZONE_SLOT_ATTR_BIT12_CLEAR_MASK | 0xffffefff | dispatch_effect_ctx_slot_by_zone_type: ands r6,r0 at LAB_0809452c to clear bit12 from zone attr accumulator; grep 0xffffefff constants/=0; conf: high | 537 |

---

## §5.1 登记 (Rule 3) -- 0 引用块

| ROM off | size | vaddr | 初判内容 | 登记理由 |
|---------|------|-------|----------|----------|
| 0x9437c | 0x1c | 0x0809437c | read_slot_tile_index_by_slot_idx (orphan THUMB code, bx lr, pool gEquipEffectZoneBase=0x0201e4f0) | Full ROM ref-scan: raw=0, THUMB+1=0 for all 2-byte-aligned addresses. Not fall-through (preceding fn get_activation_zone_card_type_field ends bx r1 at 0x0809437a). ROM_INCBIN preserved; no Ghidra ops per hard rule 3. |
| 0x94c3e | 0x22 | 0x08094c3e | reset_duel_turn_to_state2 (orphan THUMB code, bx lr, pool gP1LifePoints=0x0201c4e0/DUEL_TURN_STATE_OFF=0x1d14/CARD_PLAY_PHASE_CTR_OFF=0x1d1c) | Full ROM ref-scan: raw=0, THUMB+1=0 for all 2-byte-aligned addresses. Not fall-through (preceding fn poll_sprite_seq_until_done ends bx r0 at 0x08094c3c). ROM_INCBIN preserved; no Ghidra ops per hard rule 3. |

---

## 消費者証拠 (R6) -- 关键槽语义的 file:line + 置信度

| slot | consumer evidence | confidence |
|---|---|---|
| gEquipEffectZoneBase (0x0201e4f0) | asm/12 L4: plate of init_effect_slot_display_context: "loads gEffectDisplayCtx (0x0201e4f0): writes [+0]=card_slot_ptr, [+4]=card_type, [+8]=0"; ewram.inc:550 confirms address | high |
| gEquipLpZoneEntryBase (0x0201e500) | asm/12 L172: get_effect_slot_entry_ptr plate: "gEffectSlotTable=DAT_080942f4=0x0201e500"; ewram.inc:476 | high |
| LAST_TURN_CID (0x151e) | asm/12 L1497-1500: tick_equip_activation_dispatch_hub: check_value_in_slot_chain(player_offset, 0xb, 0x151e); card_info.inc:1447 | high |
| FINAL_COUNTDOWN_CID (0x169c) | asm/12 L1027-1031: query_summon_eligibility_code: second check_node_in_slot_chain(r4, 0xb, 0x169c); card_info.inc:747 | high |
| DISP_SET_VARIANT_OFF (0x1cfc) | asm/12 L830: init_duel_phase_display_flag_with_sprite: "sprite_variant_offset=0x1cfc" in plate; duel_field.inc:253 | high |
| EQUIP_MAIN_PHASE_OFF (0x1d18) | asm/12 L1490: tick_equip_activation_dispatch_hub plate: "main_phase_offset=0x1d18"; duel_field.inc:255 | high |
| DISPLAY_SEQ_ACTIVE_PLAYER_OFF (0x1d10) | asm/12 L1567: tick_equip_activation_main_sequence plate: "phase_step_offset=0x1d10"; duel_field.inc:218 | high |
| SET_DISPLAY_STATE_SLOT_OFF (0x0894) | duel_field.inc:254: "SET_DISPLAY_STATE_SLOT_OFF=0x894"; asm/12 L1373 process_card_play_ok_sequence uses DAT_08094b70=0x894 as P2-side analog of [+0x2c] | high |
| DISPLAY_SEQ_SLOT_IDX_OFF (0x0808) | duel_field.inc:216; asm/12 L1423-1424: [gDuelDisplaySeqState+0x808] check in process_card_play_ok_sequence draw_phase | high |
| CARD_PLAY_PHASE_CTR_OFF (0x1d1c) | asm/12 L1224 process_card_play_ok_sequence: DAT_08094a5c=0x1d1c "phase code"; L1386-1387: incremented at end; L1490 tick_equip_activation_dispatch_hub plate: "state_code_offset=0x1d1c"; 55 ROM refs confirm high usage | high |
| DUEL_TURN_STATE_OFF (0x1d14) | asm/12 L1682-1686: advance_duel_turn_by_prng_anim plate: "TURN_STATE_OFFSET=0x1d14"; 13 ROM refs | high |
| LCG_MUL/INC | asm/12 L642: advance_prng_state plate: "LCG_mul=0x343fd, LCG_inc=0x269ec3 (standard C rand() parameters)" | high |

---

## 求助 (如有低置信度语义)

1. OPEN QUESTION (med-conf): 0x0809426c value=0x161c = TRIBE_INFECTING_VIRUS_CID.
   Written to [gP1LifePoints+LP_ACTIVATION_PENDING_OFF(0x1d40)] when card_type > 0x49 in
   init_effect_slot_display_context. Using a CID value as a data sentinel here is unusual.
   The consumer of [gP1LifePoints+0x1d40] needs to be checked (not traced in this segment).
   Decision: REUSE TRIBE_INFECTING_VIRUS_CID; add EOL "stored to LP_ACTIVATION_PENDING_OFF as
   card_type > 0x49 special count init; coincides with TRIBE_INFECTING_VIRUS_CID".
   Fixer may verify by searching callers that read [gP1LifePoints+0x1d40] after this fn.

2. OPEN QUESTION (med-conf): Block3 function name reset_duel_turn_to_state2.
   Zero callers found in full ROM scan. The semantics (write 2 to [+0x1d14], 0 to [+0x1d1c])
   match the "reset to state 2, clear phase counter" pattern seen in advance_duel_turn_by_prng_anim.
   Could be a dead code remnant or a function previously reachable via function pointer
   (but no such pointer found). Mark createFunction and §5.1; do not add to CSV.
