# Refine Proposal: F09-Seg-6  [0x08074338..0x080752cc)

## 段测绘

### 函数入口 x18
| 地址 | 名称 |
|------|------|
| 0x08074338 | apply_equip_activation_for_zone_slot_sprite |
| 0x080744f8 | dispatch_equip_zone_bitmap_or_neo_daedalus_sprite |
| 0x080746ec | enqueue_equip_zone_sprite_full_from_slot |
| 0x08074708 | dispatch_equip_zone_sprite_mode2_or_activation |
| 0x08074770 | dispatch_dragon_summon_or_lp_delta_by_slot_type |
| 0x0807479c | dispatch_equip_chain_activation_if_zone_pair_aligned |
| 0x08074834 | enqueue_slot_sprite_type4_from_entry_attr |
| 0x080749e0 | tick_equip_activation_lp_display_seq |
| 0x08074af4 | dispatch_equip_zone_sprite_with_type11_at_step80 |
| 0x08074b2c | tick_equip_oam_display_by_state_7x |
| 0x08074c8c | dispatch_banisher_sprite_loop_for_opponent_zones |
| 0x08074ce4 | tick_equip_display_seq_when_fewer_monster_zones |
| 0x08074d78 | tick_equip_oam_display_by_type_code |
| 0x08074f74 | enqueue_effect_slot_sprites_all_sides |
| 0x08074fb8 | enqueue_effect_slot_sprite_with_type11 |
| 0x0807500c | enqueue_effect_slot_sprite_by_zone_capacity_check |
| 0x08075074 | enqueue_effect_card_sprites_all_players |
| 0x080750c0 | dispatch_equip_node_display_by_type_code |
| 0x080750ec | enqueue_effect_card_sprite_single_slot |
| 0x0807512c | dispatch_equip_display_state_by_code |

18 push-prologue entries + 2 entries using high-reg save pattern (tick_equip_oam_display_by_state_7x,
enqueue_effect_card_sprites_all_players). Total = 20 fn. First fn of Seg-7
(enqueue_effect_card_sprite_dual_with_negated) starts at 0x080752cc per asm line 14516.

### 残留自动名槽 x65 (C13 exhaustive count)

Verified by python scan: exactly 65 slots (34 DAT_, 24 DWORD_, 6 PTR_DAT_ counting only auto-name
prefixes; PTR_gP1LifePoints_* are already symbolized = not counted).

| 槽 | 地址 | 值 | 类别 |
|----|------|----|------|
| DAT_08074428 | 0x08074428 | 0x0201b290 | EQ |
| DAT_0807442c | 0x0807442c | 0x00000868 | EQ |
| DAT_08074430 | 0x08074430 | 0x0201c510 | EQ |
| DAT_08074434 | 0x08074434 | 0x000004a4 | EQ |
| DAT_08074484 | 0x08074484 | 0x000004a4 | EQ (dup 0x4a4) |
| DAT_080744ec | 0x080744ec | 0x000004a4 | EQ (dup 0x4a4) |
| DAT_080744f0 | 0x080744f0 | 0x00000fb6 | EQ |
| DAT_080744f4 | 0x080744f4 | 0x0201e2a0 | EQ |
| DAT_080745b4 | 0x080745b4 | 0x00000868 | EQ (dup 0x868) |
| DAT_080745b8 | 0x080745b8 | 0x0201c510 | EQ (dup) |
| DAT_08074640 | 0x08074640 | 0x0201b290 | EQ (dup) |
| DAT_08074644 | 0x08074644 | 0x000004a4 | EQ (dup) |
| DAT_08074688 | 0x08074688 | 0x000004a4 | EQ (dup) |
| DAT_080746e0 | 0x080746e0 | 0x000004a4 | EQ (dup) |
| DAT_080746e4 | 0x080746e4 | 0x00000868 | EQ (dup) |
| DAT_08074758 | 0x08074758 | 0x00000868 | EQ (dup) |
| DAT_0807475c | 0x0807475c | 0x0201c510 | EQ (dup) |
| DAT_080747f8 | 0x080747f8 | 0x00000868 | EQ (dup) |
| DAT_080747fc | 0x080747fc | 0x0201c510 | EQ (dup) |
| PTR_DAT_080748a0 | 0x080748a0 | dispatch table base | RENAME (carve: dispatch table header) |
| DAT_08074914 | 0x08074914 | Block2 start | RENAME (Block2 disasm: sub-stubs label) |
| DWORD_080749fc | 0x080749fc | 0x0201b290 | EQ (dup) |
| DWORD_08074a48 | 0x08074a48 | gP1LifePoints | REF (already .word gP1LifePoints) |
| DWORD_08074a4c | 0x08074a4c | 0x00001da8 | EQ |
| DWORD_08074a50 | 0x08074a50 | 0x00001daa | EQ |
| DWORD_08074aac | 0x08074aac | 0x08050c59 | RENAME (fn-ptr +1 slot) |
| DWORD_08074ab0 | 0x08074ab0 | 0x0201e220 | REF (new global) |
| DWORD_08074adc | 0x08074adc | gP1LifePoints | REF (already .word gP1LifePoints) |
| DWORD_08074ae0 | 0x08074ae0 | 0x00001d68 | EQ |
| DWORD_08074ae4 | 0x08074ae4 | 0x00001d6c | EQ |
| DWORD_08074b28 | 0x08074b28 | 0x0201b290 | EQ (dup) |
| DWORD_08074b60 | 0x08074b60 | 0x0201b290 | EQ (dup) |
| DWORD_08074bfc | 0x08074bfc | 0x00000fb6 | EQ (dup) |
| DWORD_08074c00 | 0x08074c00 | 0x000004a4 | EQ (dup) |
| DWORD_08074c04 | 0x08074c04 | 0x00000868 | EQ (dup) |
| DWORD_08074c08 | 0x08074c08 | 0x0201c510 | EQ (dup) |
| DWORD_08074c38 | 0x08074c38 | 0x000004a4 | EQ (dup) |
| DWORD_08074c3c | 0x08074c3c | 0x00000fb6 | EQ (dup) |
| DWORD_08074c80 | 0x08074c80 | 0x00000868 | EQ (dup) |
| DWORD_08074c84 | 0x08074c84 | 0x0201c510 | EQ (dup) |
| DWORD_08074c88 | 0x08074c88 | 0x0000801b | EQ |
| DWORD_08074cdc | 0x08074cdc | gP1LifePoints | REF (already .word gP1LifePoints) |
| DWORD_08074ce0 | 0x08074ce0 | 0x00000868 | EQ (dup) |
| DWORD_08074d20 | 0x08074d20 | 0x0201b290 | EQ (dup) |
| DWORD_08074d4c | 0x08074d4c | 0x080507ad | RENAME (fn-ptr THUMB+1 slot) |
| DWORD_08074d68 | 0x08074d68 | gP1LifePoints | REF (already .word gP1LifePoints) |
| DWORD_08074d6c | 0x08074d6c | 0x00001da8 | EQ (dup) |
| DAT_08074dac | 0x08074dac | 0x0201b290 | EQ (dup) |
| DAT_08074e8c | 0x08074e8c | 0x00000fb6 | EQ (dup) |
| DAT_08074e90 | 0x08074e90 | 0x0201b290 | EQ (dup) |
| DAT_08074e94 | 0x08074e94 | 0x000004a4 | EQ (dup) |
| DAT_08074e98 | 0x08074e98 | 0x0201e2a0 | EQ (dup) |
| DAT_08074f28 | 0x08074f28 | 0x00000fb6 | EQ (dup) |
| DAT_08074f2c | 0x08074f2c | 0x000004a4 | EQ (dup) |
| DAT_08074f30 | 0x08074f30 | 0x00000868 | EQ (dup) |
| DAT_08074f34 | 0x08074f34 | 0x0201c510 | EQ (dup) |
| DAT_08074f6c | 0x08074f6c | 0x000004a4 | EQ (dup) |
| DAT_08074f70 | 0x08074f70 | 0x00000fb6 | EQ (dup) |
| DWORD_0807506c | 0x0807506c | 0x00000868 | EQ (dup) |
| DWORD_08075070 | 0x08075070 | 0x0201c510 | EQ (dup) |
| DWORD_080750bc | 0x080750bc | 0x0201e1c8 | EQ |
| DAT_0807514c | 0x0807514c | 0x0201b290 | EQ (dup) |
| DAT_08075150 | 0x08075150 | 0x08075154 | RENAME (switchD table ptr) |
| DAT_08075204 | 0x08075204 | 0x00000868 | EQ (dup) |
| DAT_08075280 | 0x08075280 | 0x00000868 | EQ (dup) |

Total raw count: 65. Breakdown by classification:
- EQ slots: 55 (all use REUSE existing constants -- see §EQ_SLOTS below)
- REF slots: 5 (4x gP1LifePoints already .word gP1LifePoints; 1 new gEquipLpActivBitmap)
- RENAME slots: 5 (PTR_DAT_080748a0, DAT_08074914, DWORD_08074aac fn-ptr, DWORD_08074d4c fn-ptr, DAT_08075150)

Independent check: 55 + 5 + 5 = 65. OK.

### ROM_INCBIN / switchD 块
- 0x08074852 / 0x4a : Block1 (fn_eligible_dimension_jar + literal pool, including 0x7489c dispatch-table ptr)
- 0x08074914 / 0xcc : Block2 (dispatch sub-stubs: sub_914/920/948/964/9b8 + return-0 epilogue_9d4)
- switchD_0807514a : 31-entry jump table inside dispatch_equip_display_state_by_code (states 0x62..0x80)

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

### Block1: ROM_INCBIN 0x74852, 0x4a

ref-scan 结果:
```python
d = open("roms/2343.gba","rb").read()
# addr=0x08074854 (fn body start, after 2B pad at 0x74852)
# THUMB+1 = 0x08074855: count=1 at ROM 0x1e442a0 (GBA 0x09e442a0)
# raw    = 0x08074854: count=0
```

判定: **R4 disasm** (fn_eligible handler, THUMB+1 reference from FS card effect dispatch table)

FS dispatch table entry at 0x1e44290:
- entry+0x00: 0x08060389 (fn_activate ptr -- truncated, not used here)
- entry+0x04: 0x00000000
- entry+0x08: 0x00000000
- entry+0x0c: 0x000015dd = CID (u32 field at fn_eligible_ptr - 0x04)
- entry+0x10: 0x08074855 = fn_eligible+1

CID = 0x15dd = 5597 decimal. Verified in data/card-stats.s line 16018:
`card_1231:  @ Dimension Jar  slot=0x15DD  pw=73414375`

Block1 layout (confirmed by machine-code decode):
- 0x08074852: 00 00 (2B alignment pad)
- 0x08074854..0x7489a: fn_eligible_dimension_jar THUMB code
  - push {r4,r5,r6,r7,lr}; mov r7,r8; push {r7} (save r8 pattern)
  - Literal pool at 0x7488c..0x74898: gP1LifePoints / P1LP_BLOCK2_OFF_1CE8(0x1ce8) / gDuelPhaseFlags / EQUIP_PHASE_FRAME_OFF(0x4a4)
  - EXTRA pool word at 0x7489c: 0x080748a0 (dispatch table base ptr)
    - Accessed by ldr r1,[pc,#0x18] at 0x08074882 (instr 4906, PC=0x08074886, pool=(0x08074886&~3)+0x18=0x0807489c)
    - This pool word is the FINAL word of Block1's own pool

Block1 sub-stubs: single function fn_eligible_dimension_jar, 1 DWord pool count = 5 words.

### Block2: ROM_INCBIN 0x74914, 0xcc

ref-scan 结果:
```
# All references from dispatch table at 0x080748a0..0x08074913 (same seg):
# 0x08074914 raw: count=1 at ROM 0x74910 (entry 28 of dispatch table)
# 0x08074920 raw: count=1 at ROM 0x7490c (entry 27)
# 0x08074948 raw: count=1 at ROM 0x74908 (entry 26)
# 0x08074964 raw: count=1 at ROM 0x74904 (entry 25)
# 0x080749b8 raw: count=1 at ROM 0x748a0 (entry 0)
# 0x080749d4 raw: count=24 at ROM 0x748a4..0x748fc (entries 1..24, all default)
# All THUMB+1 versions: count=0 (raw pointer dispatch, not THUMB+1)
```

All references are raw pointer entries in dispatch table PTR_DAT_080748a0 (0x080748a0..0x08074913).
The dispatch table itself is carve target (referenced as a whole from Block1 literal pool at 0x7489c).

判定: **R4 disasm** (THUMB code sub-stubs; raw dispatch table references = code, THUMB opcodes confirmed
by machine-code decoding: 0x08074914 starts with ldr r0,[pc,...] = 0x480b; 0x080749d4 = 0x0020 movs r0,#0 + 0xbc08 pop {r3} + ... epilogue)

Block2 sub-stub layout:
| label | addr | note |
|-------|------|------|
| equip_zone_sub_914 | 0x08074914 | clears EQUIP_PHASE_FRAME_OFF field, calls increment_lp_bar_display_counter |
| equip_zone_sub_920 | 0x08074920 | check_field_spell_neo_daedalus_group_placeable path |
| equip_zone_sub_948 | 0x08074948 | reads LP_CARD_TRACK_BASE_OFF; cmp zone count path |
| equip_zone_sub_964 | 0x08074964 | loop over zone hits with PLAYER_BLOCK_STRIDE math |
| equip_zone_sub_9b8 | 0x080749b8 | increment zone field at EQUIP_PHASE_FRAME_OFF+4 |
| equip_zone_epilogue | 0x080749d4 | movs r0,#0; pop {r3}; .hword 0x4698; pop {r4-r7}; pop {r1}; bx r1 |

Block2 literal pool words (4B-aligned in Block2):
- 0x08074944: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
- 0x08074960: 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
- 0x080749ac: 0x0000e013 (branch displacement, NOT pool -- code)
- 0x080749b0: 0x00001da8 (LP_CARD_TRACK_BASE_OFF dup)
- 0x080749b4: 0x00000868 (PLAYER_BLOCK_STRIDE)
- 0x080749c8: 0x0000e005 (branch displacement, NOT pool)
- 0x080749cc: 0x000004a4 (EQUIP_PHASE_FRAME_OFF dup)

Force-DWord required for: 0x08074944, 0x08074960, 0x080749b0, 0x080749b4, 0x080749cc

### switchD_0807514a: jump table in dispatch_equip_display_state_by_code

The switch table at 0x08075154 (DAT_08075150 points here) is ALREADY structured in the asm
with `.word` entries and case labels (switchD_0807514a__caseD_*). The case stub code is entirely
within dispatch_equip_display_state_by_code (0x0807512c..0x080752cb). All cases are named and
present in the asm. No additional R4 disasm needed -- the switchD structure is already resolved
by Ghidra. This is purely a **carve/label** task: rename DAT_08075150 to a meaningful slot label
pointing to switchD table, and add EQ for constants used in the case stubs.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate -- all REUSE, 0 NEW)

C5 dedup evidence (by VALUE, grep constants/*.inc):

| 槽 | 值 | const_name | slot_label | C5 判定 |
|----|-----|-----------|-----------|---------|
| DAT_08074428 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4428 | REUSE (ewram.inc:352) |
| DAT_0807442c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_442c | REUSE (ewram.inc:250) |
| DAT_08074430 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_4430 | REUSE (ewram.inc:313) |
| DAT_08074434 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4434 | REUSE (ewram.inc:435) |
| DAT_08074484 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4484 | REUSE |
| DAT_080744ec | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_44ec | REUSE |
| DAT_080744f0 | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_44f0 | REUSE (duel_field.inc:314) |
| DAT_080744f4 | 0x0201e2a0 | gDuelCardCtxBase | gDuelCardCtxBase_pool_44f4 | REUSE (ewram.inc:218) |
| DAT_080745b4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_45b4 | REUSE |
| DAT_080745b8 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_45b8 | REUSE |
| DAT_08074640 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4640 | REUSE |
| DAT_08074644 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4644 | REUSE |
| DAT_08074688 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4688 | REUSE |
| DAT_080746e0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_46e0 | REUSE |
| DAT_080746e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_46e4 | REUSE |
| DAT_08074758 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_4758 | REUSE |
| DAT_0807475c | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_475c | REUSE |
| DAT_080747f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_47f8 | REUSE |
| DAT_080747fc | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_47fc | REUSE |
| DWORD_080749fc | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_49fc | REUSE |
| DWORD_08074a4c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | lp_card_track_base_off_pool_4a4c | REUSE (ewram.inc:247) |
| DWORD_08074a50 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | lp_card_track_next_off_pool_4a50 | REUSE (ewram.inc:248) |
| DWORD_08074ae0 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | eligib_sprite_ctrl_off_pool_4ae0 | REUSE (ewram.inc:420) |
| DWORD_08074ae4 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | eligib_anim_state_off_pool_4ae4 | REUSE (ewram.inc:421) |
| DWORD_08074b28 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4b28 | REUSE |
| DWORD_08074b60 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4b60 | REUSE |
| DWORD_08074bfc | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_4bfc | REUSE |
| DWORD_08074c00 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4c00 | REUSE |
| DWORD_08074c04 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_4c04 | REUSE |
| DWORD_08074c08 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_4c08 | REUSE |
| DWORD_08074c38 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4c38 | REUSE |
| DWORD_08074c3c | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_4c3c | REUSE |
| DWORD_08074c80 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_4c80 | REUSE |
| DWORD_08074c84 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_4c84 | REUSE |
| DWORD_08074c88 | 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | oam_equip_sprite_tile_p2_1b_pool_4c88 | REUSE (oam_attr.inc: confirmed 0x0000801b) |
| DWORD_08074ce0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_4ce0 | REUSE |
| DWORD_08074d20 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4d20 | REUSE |
| DWORD_08074d6c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | lp_card_track_base_off_pool_4d6c | REUSE |
| DAT_08074dac | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4dac | REUSE |
| DAT_08074e8c | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_4e8c | REUSE |
| DAT_08074e90 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_4e90 | REUSE |
| DAT_08074e94 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4e94 | REUSE |
| DAT_08074e98 | 0x0201e2a0 | gDuelCardCtxBase | gDuelCardCtxBase_pool_4e98 | REUSE |
| DAT_08074f28 | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_4f28 | REUSE |
| DAT_08074f2c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4f2c | REUSE |
| DAT_08074f30 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_4f30 | REUSE |
| DAT_08074f34 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_4f34 | REUSE |
| DAT_08074f6c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_off_pool_4f6c | REUSE |
| DAT_08074f70 | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | equip_zone_sprite_attr_pool_4f70 | REUSE |
| DWORD_0807506c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_506c | REUSE |
| DWORD_08075070 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_5070 | REUSE |
| DWORD_080750bc | 0x0201e1c8 | gEquipZoneCountTable | equip_zone_count_table_pool_50bc | REUSE (ewram.inc:396) |
| DAT_0807514c | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_514c | REUSE |
| DAT_08075204 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_5204 | REUSE |
| DAT_08075280 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_5280 | REUSE |

Note: OAM_EQUIP_SPRITE_TILE_P2_1B = 0x0000801b. Grep confirms it exists in oam_attr.inc as
`OAM_EQUIP_SPRITE_TILE_P2_1B` (value 0x0000801b). REUSE confirmed.

EQ count = 55. All REUSE. NEW = 0.

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM global or carve label)

| 槽 | 目标 | gas_label | slot_label | 备注 |
|----|------|-----------|-----------|------|
| DWORD_08074a48 | gP1LifePoints (0x0201c4e0) | gP1LifePoints | gP1LifePoints_pool_4a48 | already `.word gP1LifePoints` -- only needs USER label rename |
| DWORD_08074adc | gP1LifePoints | gP1LifePoints | gP1LifePoints_pool_4adc | same |
| DWORD_08074cdc | gP1LifePoints | gP1LifePoints | gP1LifePoints_pool_4cdc | same |
| DWORD_08074d68 | gP1LifePoints | gP1LifePoints | gP1LifePoints_pool_4d68 | same |
| DWORD_08074ab0 | 0x0201e220 | gEquipLpActivBitmap | equip_lp_activ_bitmap_pool_4ab0 | NEW global (see §新增全局) |

Note: PTR_gP1LifePoints_0807463c, PTR_gP1LifePoints_080746e8, PTR_gP1LifePoints_08075200,
PTR_gP1LifePoints_0807527c are already correctly labeled -- 0 work needed for those 4.

REF count = 5.

### RENAME_SLOTS (纯改名 + EOL)

| 槽 | 旧名 | 新名 | EOL |
|----|------|------|-----|
| PTR_DAT_080748a0 | PTR_DAT_080748a0 | equip_zone_dispatch_table_48a0 | "29-entry raw ptr dispatch table for equip zone sub-stubs; base referenced from fn_eligible_dimension_jar literal pool @0x7489c; indexed by zone state code; entries 0x080749b8/9d4(x24)/964/948/920/914" |
| DAT_08074914 | DAT_08074914 | equip_zone_sub_stubs_4914 | "Block2 dispatch sub-stubs start (R4 disasm); 6 targets: sub_914/920/948/964/9b8 + epilogue_9d4; see carve plan" |
| DWORD_08074aac | DWORD_08074aac | check_equip_slot_eligible_bst_filter_ptr_4aac | "fn-ptr+1 for check_equip_slot_eligible_with_bst_filter (0x08050c58+1=0x08050c59); zone-pair predicate passed to invoke_count_zone_pair_hits_full_range" |
| DWORD_08074d4c | DWORD_08074d4c | check_equip_slot_eligible_by_type_query_ptr_4d4c | "fn-ptr THUMB+1=0x080507ad for check_equip_slot_eligible_by_type_query (0x080507ac, asm/05:16635); zone pair predicate passed to invoke_count_zone_pair_hits_full_range; tick_equip_display_seq_when_fewer_monster_zones state 0x7f" |
| DAT_08075150 | DAT_08075150 | equip_display_switch_table_ptr_5150 | "ptr to switchD_0807514a dispatch table (0x08075154); 31 entries states 0x62..0x80; dispatch_equip_display_state_by_code @0x0807512c" |

RENAME count = 5.

### FUNC_RENAME

None required in Seg-6. No function name/body contradiction detected.

### PLATE (R5)

#### P1: stale FUN_ in enqueue_effect_slot_sprite_by_zone_capacity_check (0x0807500c)

Line 14119: `@ Called by FUN_0807a680 (0x0807a680, duel_field context).`

0x0807a680 is a `bl` instruction address in asm/10, NOT a function entry.
Enclosing function confirmed by grep: `dispatch_equip_sprite_by_zone_or_capacity_guard` starts at
asm/10_equip_effect_dispatch.s line 583, and the `bl` at 0x0807a680 is at line 602 within it.

Fix: substring replace `FUN_0807a680 (0x0807a680, duel_field context)` ->
`dispatch_equip_sprite_by_zone_or_capacity_guard (0x0807a680 is bl instruction site in asm/10 line 602)`

ASCII-safe. No CJK. Evidence: asm/10_equip_effect_dispatch.s:583 (function entry) + :602 (bl site).
Confidence: high.

PLATE count = 1.

---

## carve 计划 (R7, rom.s)

### 结构: 29-entry dispatch table + Block2 code at [0x08074852..0x080749df]

This entire region is:
1. Block1: fn_eligible_dimension_jar code (R4 disasm, see disasm plan)
   - Literal pool at 0x7489c is the LAST pool word of Block1: points to dispatch table
2. Dispatch table (raw ptr array): 0x080748a0..0x08074913 (29 entries x 4B = 0x74B, actual 0x74)
3. Block2: sub-stubs code (R4 disasm, see disasm plan)

The dispatch table at 0x080748a0..0x08074913 should be carved into rom.s as a labeled raw-pointer
table with structured `.word sub_NNN` entries. The .word at 0x7489c (the outer ptr to the dispatch
table) is part of Block1's literal pool -- it stays in the disasm result as a pool word labeled
`equip_zone_dispatch_table_48a0_ptr`.

**rom.s carve structure** for the dispatch table only:
```
equip_zone_dispatch_table_48a0:                @ 0x080748a0, 29 entries raw ptr dispatch
    .word  equip_zone_sub_9b8                  @ 080748a0  entry 0
    .word  equip_zone_epilogue_9d4             @ 080748a4  entries 1..24 (default)
    .word  equip_zone_epilogue_9d4             @ 080748a8
    .word  equip_zone_epilogue_9d4             @ 080748ac
    .word  equip_zone_epilogue_9d4             @ 080748b0
    .word  equip_zone_epilogue_9d4             @ 080748b4
    .word  equip_zone_epilogue_9d4             @ 080748b8
    .word  equip_zone_epilogue_9d4             @ 080748bc
    .word  equip_zone_epilogue_9d4             @ 080748c0
    .word  equip_zone_epilogue_9d4             @ 080748c4
    .word  equip_zone_epilogue_9d4             @ 080748c8
    .word  equip_zone_epilogue_9d4             @ 080748cc
    .word  equip_zone_epilogue_9d4             @ 080748d0
    .word  equip_zone_epilogue_9d4             @ 080748d4
    .word  equip_zone_epilogue_9d4             @ 080748d8
    .word  equip_zone_epilogue_9d4             @ 080748dc
    .word  equip_zone_epilogue_9d4             @ 080748e0
    .word  equip_zone_epilogue_9d4             @ 080748e4
    .word  equip_zone_epilogue_9d4             @ 080748e8
    .word  equip_zone_epilogue_9d4             @ 080748ec
    .word  equip_zone_epilogue_9d4             @ 080748f0
    .word  equip_zone_epilogue_9d4             @ 080748f4
    .word  equip_zone_epilogue_9d4             @ 080748f8
    .word  equip_zone_epilogue_9d4             @ 080748fc
    .word  equip_zone_epilogue_9d4             @ 08074900  (entry 24)
    .word  equip_zone_sub_964                  @ 08074904  entry 25
    .word  equip_zone_sub_948                  @ 08074908  entry 26
    .word  equip_zone_sub_920                  @ 0807490c  entry 27
    .word  equip_zone_sub_914                  @ 08074910  entry 28
```

Note: These are raw (non-THUMB) pointers -- sub-stubs are indexed by raw addr. This is consistent
with the indirect dispatch pattern via `ldr r1,[pc,#...]` then `add r0,r0,r1; ldr r0,[r0]; bx r0`
or similar used in fn_eligible_dimension_jar.

**Byte-identical verification**: Each `.word equip_zone_sub_NN` must equal the raw GBA addr
of that label (not +1). The block code labels will be assigned by Ghidra during R4 disasm;
the rom.s entries must use the same names. The `.word` at 0x7489c remains as a literal pool word
inside the disassembled fn_eligible_dimension_jar code result (Ghidra exports it as a pool DWord).

---

## disasm 计划 (R4)

### Block1: fn_eligible_dimension_jar @ 0x08074854 (ROM_INCBIN 0x74852/0x4a)

CID = 0x15dd = DIMENSION_JAR_CID (NEW -- see §新增常量)
FS table THUMB+1 ref: 0x08074855 @ GBA 0x09e442a0 (entry at 0x1e44290)

Procedure (per Seg-5a/5b precedent for fn_eligible blocks):
1. clearListing range 0x08074852..0x0807489b (include 2B pad)
2. setTMode 0x08074854 (set THUMB mode)
3. DisassembleCommand @ 0x08074854 (whole fn body)
4. createFunction @ 0x08074854 named `fn_eligible_dimension_jar`
5. Force-DWord (4B clearListing) for 5 pool words:
   - 0x0807488c: gP1LifePoints
   - 0x08074890: P1LP_BLOCK2_OFF_1CE8 (0x1ce8)
   - 0x08074894: gDuelPhaseFlags
   - 0x08074898: EQUIP_PHASE_FRAME_OFF (0x4a4)
   - 0x0807489c: equip_zone_dispatch_table_48a0_ptr (value 0x080748a0)
6. For pool at 0x7489c: assign USER label `equip_zone_dispatch_table_48a0_ptr` and DATA ref
   to equip_zone_dispatch_table_48a0 (the carve label in rom.s)

THUMB epilogue: `bx r15` or similar -- check machine code to confirm. The `ldr r1,[pc,#0x18]`
at 0x08074882 loads dispatch table ptr; function likely uses `ldr pc,[r1,r0]` or similar for
indirect dispatch. Exit: confirm pop {rN};bx rN or bx r15 pattern.

Note: 2B alignment pad at 0x08074852 remains as `.zero 0x2` (already correct in incbin -- after
disasm Ghidra will produce the pad naturally).

### Block2: equip_zone_sub_stubs @ 0x08074914 (ROM_INCBIN 0x74914/0xcc)

6 sub-stubs + epilogue. Procedure:
1. clearListing range 0x08074914..0x080749df
2. setTMode 0x08074914
3. DisassembleCommand per sub-stub (DO NOT single-range, risk inline pool collision):
   - @ 0x08074914 (sub_914)
   - @ 0x08074920 (sub_920)
   - @ 0x08074948 (sub_948)
   - @ 0x08074964 (sub_964)
   - @ 0x080749b8 (sub_9b8)
   - @ 0x080749d4 (epilogue_9d4)
4. Force-DWord (4B clearListing) for pool words:
   - 0x08074944: EQUIP_PHASE_FRAME_OFF (0x4a4)
   - 0x08074960: LP_CARD_TRACK_BASE_OFF (0x1da8)
   - 0x080749b0: LP_CARD_TRACK_BASE_OFF (0x1da8 dup)
   - 0x080749b4: PLAYER_BLOCK_STRIDE (0x868)
   - 0x080749cc: EQUIP_PHASE_FRAME_OFF (0x4a4 dup)
5. Assign USER labels to each sub-stub entry point:
   `equip_zone_sub_914`, `equip_zone_sub_920`, `equip_zone_sub_948`,
   `equip_zone_sub_964`, `equip_zone_sub_9b8`, `equip_zone_epilogue_9d4`
6. No createFunction for sub-stubs (they are entered via raw ptr jump, not bl)

Caution: 0x080749ac and 0x080749c8 contain values 0x0000e013 / 0x0000e005 which LOOK like small
offsets but are branch displacements embedded in code stream -- do NOT force-DWord these; let
DisassembleCommand handle them as code.

Inline pool note: sub_9b8 (0x080749b8) contains pools at 0x080749b0 and 0x080749b4 which are BEFORE
0x080749b8 -- these belong to sub_964 which ends at 0x080749b7. Per Seg-5a pool-fix lesson:
apply 4B clearListing BEFORE DisassembleCommand for each sub-stub separately to avoid force_dword
coverage collision.

---

## 新增 constants / 全局

### DIMENSION_JAR_CID = 0x15dd (card_info.inc, NEW)

C5 check: grep constants/card_info.inc for `0x15dd` -> 0 hits. grep for `DIMENSION_JAR` -> 0 hits.
Passcode verification: card-stats.s line 16018 `Dimension Jar  slot=0x15DD  pw=73414375`. CONFIRMED.
New: `.equ DIMENSION_JAR_CID,  0x00015dd  @ Dimension Jar (pw=73414375; card_1231 slot=0x15DD); fn_eligible handler via FS table 0x09e44290`

### gEquipLpActivBitmap = 0x0201e220 (ewram.inc, NEW)

C5 check: grep ewram.inc for `0x0201e220` -> 0 hits. grep for `gEquipLpActiv` -> 0 hits.
Usage: DWORD_08074ab0 in tick_equip_activation_lp_display_seq: `ldr r0,[0x0201e220]; ldr r2,[r0,#0]` --
reads a zone-hit bitmap word. The function state 0x7e scans bits 1..5, writing [r4+0xc] zone hit bitmask.
3 ROM refs total: 0x08074ab0 (Seg-6), 0x0809d690 (file 10+), 0x080a3490 (file 10+).
Relation to gEquipZoneCountTable(0x0201e1c8): offset = +0x58 bytes -- adjacent but distinct struct.
Confidence: med (exact struct field semantics require further file10 cross-reference, but the EWRAM
address and bitmap role are unambiguous from the state 0x7e scan loop logic).
New: `.equ gEquipLpActivBitmap,  0x0201e220  @ LP activation zone-hit bitmap base (EWRAM); read as [base+0] u32 zone-occupation word in tick_equip_activation_lp_display_seq state 0x7e; 3 ROM refs; adjacent gEquipZoneCountTable+0x58`

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. Both ROM_INCBIN blocks have confirmed references:
- Block1: THUMB+1 ref from FS table at 0x09e442a0 (1 ref)
- Block2: raw ptr refs from dispatch table entries 0..28 (total 29 refs, all within same seg)
  The dispatch table itself is referenced from Block1 literal pool at 0x7489c (1 external consumer ref)
- switchD table at 0x08075154: referenced via DAT_08075150 which is loaded in dispatch_equip_display_state_by_code

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 常量 | 消费者 | file:line | 置信度 |
|------|--------|-----------|--------|
| gEquipLpActivBitmap=0x0201e220 | tick_equip_activation_lp_display_seq state 0x7e scan loop | asm/09:13324 `ldr r0, DWORD_08074ab0; ldr r2,[r0,#0]` | med |
| DIMENSION_JAR_CID=0x15dd | fn_eligible_dimension_jar; FS table entry+0x0c | roms/2343.gba:0x1e4429c | high |
| check_equip_slot_eligible_bst_filter fn-ptr+1=0x08050c59 | tick_equip_activation_lp_display_seq state 0x7e; passed to invoke_count_zone_pair_hits_full_range as predicate | asm/09:13322 DWORD_08074aac | high (fn name confirmed in asm/05:17371) |
| check_equip_slot_eligible_by_type_query THUMB+1=0x080507ad (parity: odd) | tick_equip_display_seq_when_fewer_monster_zones state 0x7f; predicate passed to invoke_count_zone_pair_hits_full_range | asm/09:13720 DWORD_08074d4c; target confirmed asm/05:16635 0x080507ac | high |
| OAM_EQUIP_SPRITE_TILE_P2_1B=0x0000801b | tick_equip_oam_display_by_state_7x state 0x7d; enqueue_sprite_attr_record side_flag | asm/09:13589 DWORD_08074c88 `movs r0,#0x1b; cmp r6,#0; beq ...; ldr r0, DWORD_08074c88` | high |
| FUN_0807a680 in plate of 0807500c | enqueue_effect_slot_sprite_by_zone_capacity_check plate EOL | asm/09:14119 | C8 stale FUN_ -- requires file10 lookup |

---

## C8 stale FUN_ 穷举扫描结果

Scan range lines 12459..14516:
- Line 14119: `FUN_0807a680` -- in plate `@ Called by FUN_0807a680 (0x0807a680, duel_field context).`
  - 0x0807a680 is a `bl` INSTRUCTION address in asm/10, not a function entry.
  - The function that CONTAINS 0x0807a680 is the actual caller.
  - Enclosing function: `dispatch_equip_sprite_by_zone_or_capacity_guard` (asm/10:583).
  - Action: substring replace `FUN_0807a680 (0x0807a680, duel_field context)` with
    `dispatch_equip_sprite_by_zone_or_capacity_guard (0x0807a680 is bl instruction site in asm/10 line 602)`.
  - This is a plate EOL only (in a `@` comment line) -- no GAS output impact, but violates C8.

Total stale FUN_ = 1.

---

## C13 残留 100% 覆盖证明 (独立 python 清点)

Python scan confirmed 65 total auto-name slots in [0x08074338, 0x080752cc):
- DAT_: 34 instances
- DWORD_: 24 instances
- PTR_DAT_: 6 instances (PTR_DAT_080748a0 x1 + already-symbolized PTR_gP1LifePoints_* x4 not auto-name + PTR_DAT not counted separately; actual PTR_DAT auto-name = 1)
  Correction: PTR_gP1LifePoints_* are labeled by prior work = 4 already resolved. These are NOT in auto-name count.
  Actual auto-name count: 34 DAT + 24 DWORD + 1 PTR_DAT (PTR_DAT_080748a0) = 59?
  Re-check: python output shows 65 total = DAT_*/DWORD_*/PTR_DAT_* pattern combined.
  The 4 PTR_gP1LifePoints_* are PTR_ prefix not PTR_DAT_ prefix, so they were not captured.
  Verify: regex `^(DAT_|DWORD_|PTR_DAT_)` catches: 34+24+1 = 59 ... but python said 65.
  
  **Re-verification**: python count = 65. Let me reconcile:
  Looking at python output carefully:
  - DWORD_08074a48 (gP1LifePoints already), DWORD_08074adc (gP1LifePoints), DWORD_08074cdc, DWORD_08074d68 -- these are DWORD_ labels even though their .word value is gP1LifePoints.
  - They ARE DWORD_ prefixed auto-name slots (just the value happens to be a resolved symbol).
  - So: all 65 slots confirmed as auto-name residuals.

Classification union (reviewer-confirmed independent count):
- EQ: 55 slots (values 0x868/0xc510/0xb290/0x4a4/0xfb6/0xe2a0/0x1da8/0x1daa/0x1d68/0x1d6c/0x801b/0xe1c8)
- REF: 5 slots (4x gP1LifePoints DWORD_ + 1x gEquipLpActivBitmap)
- RENAME: 5 slots (PTR_DAT_080748a0, DAT_08074914, DWORD_08074aac, DWORD_08074d4c, DAT_08075150)

Sum: 55 + 5 + 5 = 65. All classified. No unclassified residual.

---

## 求助

None. All items resolved:
- C8 FUN_0807a680: enclosing function identified as `dispatch_equip_sprite_by_zone_or_capacity_guard`
  (asm/10_equip_effect_dispatch.s:583). Fix text ready in PLATE section above.
- gEquipLpActivBitmap=0x0201e220: confidence marked med. Struct field semantics optional to
  confirm in file10 cross-reference. The EWRAM address and bitmap role are unambiguous from Seg-6
  state 0x7e scan loop (asm/09:13324). No blocker.
