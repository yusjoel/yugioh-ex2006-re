# Refine Proposal: F11-Seg-1  [0x080850d8..0x08085d4c)

## 段测绘

- 函数入口: x10
  - 0x080850d8  enqueue_effect_slot_attr_from_bb
  - 0x0808527c  enqueue_zone_slot_sprite_pair_if_unset
  - 0x080852cc  enqueue_effect_slot_attr_from_node_ptr
  - 0x080852e4  dispatch_equip_display_with_pair_card_id
  - 0x08085320  submit_lp_bar_sprite_row_by_type
  - 0x08085430  build_sprite_row_from_zone_state
  - 0x080854b8  scan_equip_target_slots_for_card   (~48 literal pool slots; heaviest fn)
  - 0x08085838  scan_all_zones_for_equip_target
  - 0x08085928  check_equip_target_card_id_eligible
  - 0x08085a50  build_field_action_text_by_zone_type

- 残留自动名槽: x101 total (DAT_/DWORD_/PTR_ labels; see EQ/REF/RENAME tables).
  Note: DAT_08085130 is the ROM_INCBIN start marker, classified as disasm (R4) -- it gets
  replaced by real labels after disassembly; the remaining 100 are literal pool slots.

- ROM_INCBIN / .byte 块: x2
  - 0x080850f0  size 0x28  (block1 -- fn_activate dispatcher for CID 0x196a)
  - 0x08085130  size 0x14c (block2 -- 16 THUMB sub-function bodies)

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

```python
import struct
rom = open("roms/2343.gba","rb").read()
for bstart, bsize in [(0x080850f0, 0x28), (0x08085130, 0x14c)]:
    for a in range(bstart, bstart+bsize, 2):
        for v in (a, a|1):
            c = rom.count(struct.pack("<I",v))
            if c: print(hex(v), c)
```

| 块 | ref-scan summary (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x080850f0 sz=0x28 | raw=0; thumb=1 (0x080850f1 at 0x09e46248) | R4 disasm | Single THUMB+1 fn-ptr in card effect dispatch table at 0x09e46248; context: [fn_act+1=0x080850f1, CID=0x196a (Scarr Scout of Dark World), fn_elig+1=0x080661fd]; first 2 bytes 0xb510=push {r4,lr} confirms THUMB prologue; function is fn_activate handler dispatching by gDuelPhaseFlags+SLOT_DISPLAY_TYPE_OFF to 6 block2 sub-handlers via MOV PC,r0 table at 0x08085118..0x0808512c |
| 0x08085130 sz=0x14c | raw=11 distinct addrs; thumb=12 distinct addrs (16 total entry pts) | R4 disasm | 16 function entry points confirmed: 4 via raw fn-ptr table at 0x08085118 (pointed to by block1 dispatcher); 12 via THUMB+1 refs from card effect dispatch tables throughout ROM. Raw refs to 0x08085148/0x08085202/0x08085208/0x0808520c are pc-relative literal pool loads in other THUMB functions -- not fn-ptrs. First 2 bytes at each entry confirm THUMB code (ldr, strh, bl, etc.). Not §5.1 (has refs). Not carve (code, not data). |

### 16 block2 sub-function entry points (R4 targets)

| addr | refs (raw+thumb) | notes |
|---|---|---|
| 0x08085130 | raw:1 (table[0]) | fn-ptr table entry 0; first inst: ldr r0,[r1,#4] |
| 0x08085140 | raw:1 thumb:1 | raw ref is in code (literal pool); 1 THUMB dispatch ref |
| 0x08085142 | raw:1 thumb:2 | 3 total refs |
| 0x08085144 | raw:0 thumb:6 | most-referenced sub-fn in block2 |
| 0x08085150 | raw:0 thumb:1 | |
| 0x080851a8 | raw:2 (table[1,4]) | fn-ptr table entries 1 and 4 |
| 0x080851cc | raw:0 thumb:1 | |
| 0x080851d4 | raw:2 (table[2,5]) | fn-ptr table entries 2 and 5 |
| 0x08085200 | raw:0 thumb:1 | |
| 0x08085204 | raw:0 thumb:1 | |
| 0x0808520e | raw:0 thumb:1 | |
| 0x08085210 | raw:2 thumb:1 | raw refs are literal pool loads in code |
| 0x08085228 | raw:0 thumb:1 | |
| 0x08085230 | raw:1 (table[3]) | fn-ptr table entry 3 |
| 0x08085248 | raw:0 thumb:1 | |
| 0x0808524a | raw:0 thumb:1 | |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate)

All values verified against ROM bytes at slot address (python struct.unpack_from('<I',rom,addr-0x08000000)).

| slot addr | value | const_name | source file | slot_label | evidence |
|---|---|---|---|---|---|
| 0x080850ec | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:317 | gequipchainslot_8050ec | consumed: enqueue_effect_slot_attr_from_bb ldr r2,DWORD_080850ec; ldr r1,[r2,#4]; ldr r2,[r2,#0x20] -- reads player_flag/col from equip chain slot ref base; high-conf |
| 0x080852c0 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:317 | gequipchainslot_8052c0 | same global, enqueue_zone_slot_sprite_pair_if_unset; high-conf |
| 0x080852c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 | player_stride_8052c4 | muls r1,r2 stride multiplication; high-conf |
| 0x080852c8 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 | gduelfieldslots_8052c8 | ldrh r0,[r0,#8] slot pair guard read; high-conf |
| 0x0808536c | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 (P1LP_BLOCK2_OFF=0x1d08 at line 243) | p1lp_block2off_853_6c | [gP1LifePoints+0x1d08] guard read in submit_lp_bar_sprite_row_by_type; identical usage as other files; high-conf |
| 0x08085370 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_8537_0 | adds r2,r7,r0; then offset 0x1ce8 used for second lookup [gP1LifePoints+0x1ce8]; high-conf |
| 0x08085374 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85374 | [gDuelCardCtxBase+4] = player_flag check; high-conf |
| 0x080853b8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 | gduelphaseflag_853b8 | ldr r1,[r0,r2] gDuelPhaseFlags+0x9a<<3=0x4d0 check; high-conf |
| 0x080853bc | 0x000004c4 | LP_BAR_DISPLAY_CTR_OFF | ewram.inc:404 | lpbar_dctr_off_853bc | [gDuelPhaseFlags+0x4c4] LP bar display counter; high-conf |
| 0x080853c0 | 0x000004d3 | LP_BAR_ROW_XCOORD_OFF | ewram.inc NEW | lpbar_xcoord_off_853c0 | strb r4,[r0] x-coord byte written to gDuelPhaseFlags+new_count+0x4d3; high-conf (see new constants) |
| 0x08085420 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc:405 | lpbar_anim_st_85420 | [gDuelPhaseFlags+0x4cc] anim state; high-conf |
| 0x08085424 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc:411 | sprite_row_data_85424 | [gDuelPhaseFlags+0x4d4] byte array data; high-conf |
| 0x08085428 | 0x0000057c | FIELD_DISPLAY_TYPE_OFF | ewram.inc NEW | field_disp_type_85428 | [gDuelPhaseFlags+0x57c] display type field; 7 ROM refs; high-conf (see new constants) |
| 0x0808542c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_8542c | same pattern; high-conf |
| 0x080854a4 | 0x00001d08 | P1LP_BLOCK2_OFF | ewram.inc:243 | p1lp_block2off_854a4 | guard read in build_sprite_row_from_zone_state; high-conf |
| 0x080854a8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 | gduelphaseflag_854a8 | base for +0x4cc lookup; high-conf |
| 0x080854ac | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc:405 | lpbar_anim_st_854ac | ldr r0,[r0,0] reads lp bar row count from [gDuelPhaseFlags+0x4cc]; high-conf |
| 0x080854b0 | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc:411 | sprite_row_data_854b0 | byte array flag base; high-conf |
| 0x080854b4 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | ewram.inc:447 | chain_node_arr_854b4 | card pointer array in zone state; high-conf |
| 0x080854dc | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | ewram.inc:411 | sprite_row_data_854dc | scan_equip_target_slots_for_card: ldrb r0,[r0,0] reads slot type byte; high-conf |
| 0x08085568 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85568 | [gDuelCardCtxBase+r1*4+8] = equip slot active flag; high-conf |
| 0x0808557c | 0x000015ad | NON_AGGRESSION_AREA_CID | card_info.inc:402 | non_aggr_area_8557c | caseD_2: cmp r4,NON_AGGRESSION_AREA_CID (equip eligibility switch); high-conf |
| 0x08085580 | 0x0000131e | SPECIAL_EQUIP_TARGET_CID_A | card_info.inc:1093 | spec_equip_cid_a_85580 | caseD_2 lower-bound CID; high-conf |
| 0x08085590 | 0x000015f0 | THUNDER_OF_RULER_CID | card_info.inc:1195 | thunder_ruler_85590 | caseD_2 upper-bound: cmp r4,THUNDER_OF_RULER_CID; high-conf |
| 0x080855a4 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc:330 | embodiment_apophis_855a4 | caseD_3 pivot; high-conf |
| 0x080855a8 | 0x00001358 | REGULATION_OF_TRIBE_CID | card_info.inc NEW | reg_tribe_855a8 | caseD_3 lower bound; card-stats.s card_0761 slot=0x1358 Regulation of Tribe; 11 ROM refs; high-conf |
| 0x080855b8 | 0x000017fc | TAUNT_CID | card_info.inc:196 | taunt_cid_855b8 | caseD_3 upper bound; high-conf |
| 0x080855c0 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | card_info.inc:330 | embodiment_apophis_855c0 | caseD_4 lower bound (same CID reused); high-conf |
| 0x080855e8 | 0x000013fa | TORRENTIAL_TRIBUTE_CID | card_info.inc NEW | torrential_trib_855e8 | caseD_6 pivot; card-stats.s card_0871 Torrential Tribute; 9 ROM refs; high-conf |
| 0x080855ec | 0x000012cd | CHAIN_DESTRUCTION_CID | card_info.inc:938 | chain_dest_855ec | caseD_6 sub-pivot; high-conf |
| 0x080855f4 | 0x000012e4 | TRAP_HOLE_CID | card_info.inc:939 | trap_hole_855f4 | caseD_6 range check; high-conf |
| 0x0808560c | 0x000015f3 | PINEAPPLE_BLAST_CID | card_info.inc:1197 | pineapple_blast_8560c | caseD_6 upper-upper pivot; high-conf |
| 0x08085638 | 0x000015f8 | ADHESION_TRAP_HOLE_CID | card_info.inc NEW | adhesion_th_85638 | caseD_6 final pivot; card-stats.s card_1252 Adhesion Trap Hole; 9 ROM refs; high-conf |
| 0x08085660 | 0x000013fa | TORRENTIAL_TRIBUTE_CID | card_info.inc NEW | torrential_trib_85660 | caseD_7 pivot (same CID reuse); high-conf |
| 0x08085664 | 0x000012cd | CHAIN_DESTRUCTION_CID | card_info.inc:938 | chain_dest_85664 | caseD_7 sub-pivot; high-conf |
| 0x0808566c | 0x000012e4 | TRAP_HOLE_CID | card_info.inc:939 | trap_hole_8566c | caseD_7 range check; high-conf |
| 0x08085680 | 0x00001572 | HIDDEN_SOLDIER_CID | card_info.inc:1320 | hidden_soldier_85680 | caseD_7 upper pivot; high-conf |
| 0x08085690 | 0x000015f8 | ADHESION_TRAP_HOLE_CID | card_info.inc NEW | adhesion_th_85690 | caseD_7 upper final; high-conf |
| 0x080856b4 | 0x0000140f | SHADOW_OF_EYES_CID | card_info.inc NEW | shadow_eyes_856b4 | caseD_8 pivot; card-stats.s card_0890 Shadow of Eyes; 8 ROM refs; high-conf |
| 0x080856b8 | 0x000012cd | CHAIN_DESTRUCTION_CID | card_info.inc:938 | chain_dest_856b8 | caseD_8 sub-pivot; high-conf |
| 0x080856bc | 0x000013fa | TORRENTIAL_TRIBUTE_CID | card_info.inc NEW | torrential_trib_856bc | caseD_8 sub-upper; high-conf |
| 0x080856cc | 0x00001518 | BOTTOMLESS_TRAP_HOLE_CID | card_info.inc:986 | bottomless_th_856cc | caseD_8 upper cluster; high-conf |
| 0x080856e4 | 0x0000192e | DD_TRAP_HOLE_CID | card_info.inc NEW | dd_trap_hole_856e4 | caseD_8 topmost pivot; card-stats.s card_1931 D.D. Trap Hole; 8 ROM refs; high-conf |
| 0x08085704 | 0x0000195d | CHTHONIAN_POLYMER_CID | card_info.inc:228 | chtho_polymer_85704 | caseD_8 neighbor; high-conf |
| 0x0808570c | 0x000012d7 | TRAGEDY_CID | card_info.inc NEW | tragedy_cid_8570c | caseD_b lower bound; card-stats.s card_0662 Tragedy; 10 ROM refs; high-conf |
| 0x08085720 | 0x0000140f | SHADOW_OF_EYES_CID | card_info.inc NEW | shadow_eyes_85720 | caseD_9 pivot (reuse); high-conf |
| 0x08085724 | 0x0000192e | DD_TRAP_HOLE_CID | card_info.inc NEW | dd_trap_hole_85724 | caseD_9 pair check; high-conf |
| 0x08085738 | 0x00001352 | NUMINOUS_HEALER_CID | card_info.inc:1160 | numinous_healer_85738 | caseD_10 pivot; high-conf |
| 0x08085740 | 0x0000134e | cid_134e | card_info.inc:1123 | cid_134e_85740 | caseD_18 lower bound (reuse existing cid_134e constant); high-conf |
| 0x08085754 | 0x00001353 | APPROPRIATE_CID | card_info.inc:623 | appropriate_85754 | caseD_19 pivot; high-conf |
| 0x08085758 | 0x0000151c | DROP_OFF_CID | card_info.inc NEW | drop_off_85758 | caseD_19 pair; card-stats.s card_1091 Drop Off; 16 ROM refs; high-conf |
| 0x08085778 | 0x0000135b | cid_135b | card_info.inc:1164 | cid_135b_85778 | caseD_1b pivot (reuse existing cid_135b); high-conf |
| 0x0808578c | 0x000015b5 | ROPE_OF_SPIRIT_CID | card_info.inc:1027 | rope_spirit_8578c | caseD_1b upper; high-conf |
| 0x08085790 | 0x0000195e | CHTHONIAN_BLAST_CID | card_info.inc:1265 | chtho_blast_85790 | caseD_1b final; high-conf |
| 0x08085798 | 0x00001354 | FORCED_REQUISITION_CID | card_info.inc:1161 | forced_req_85798 | caseD_1d lower bound; high-conf |
| 0x080857c0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_857c0 | [gDuelCardCtxBase+r5] equip slot select; high-conf |
| 0x080857c8 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_857c8 | gP1LifePoints+0x1ce8 load; high-conf |
| 0x080857fc | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_857fc | caseD_17: same global; high-conf |
| 0x08085800 | 0x000012f3 | ULTIMATE_OFFERING_CID | card_info.inc:261 | ultimate_offer_85800 | caseD_17 lower bound cmp r4; high-conf |
| 0x08085804 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 | gduelphaseflag_85804 | loop counter comparison vs [gDuelPhaseFlags+0x4cc]; high-conf |
| 0x08085808 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc:405 | lpbar_anim_st_85808 | slot count limit comparison; high-conf |
| 0x08085828 | 0x000017bc | CRUSH_D_GANDRA_CID | card_info.inc:1042 | crush_gandra_85828 | check_equip_target_card_id_eligible__0808580c: zone_card_id == CRUSH_D_GANDRA; high-conf |
| 0x0808582c | 0x000014e6 | EMERGENCY_PROVISIONS_CID | card_info.inc NEW | emerg_prov_8582c | equip_card_id == EMERGENCY_PROVISIONS; card-stats.s card_1046 slot=0x14E6; grep 0x14e6 in card_info.inc = 0 hits; high-conf |
| 0x08085830 | 0x0000183e | SERIAL_SPELL_CID | card_info.inc:997 | serial_spell_85830 | equip_card_id == SERIAL_SPELL; high-conf |
| 0x080858f4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 | player_stride_858f4 | muls r2,r1 player stride; high-conf |
| 0x080858f8 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 | gduelfieldslots_858f8 | outer scan loop base; high-conf |
| 0x08085900 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc:366 | gp1fieldarrayc_85900 | effect zone secondary scan; high-conf |
| 0x08085924 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 | player_stride_85924 | inner loop zone count stride; high-conf |
| 0x08085a18 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 | player_stride_85a18 | check_equip_target_card_id_eligible; high-conf |
| 0x08085a1c | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 | gduelfieldslots_85a1c | field slot scan base; high-conf |
| 0x08085a24 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc:366 | gp1fieldarrayc_85a24 | effect zone second pass; high-conf |
| 0x08085a4c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 | player_stride_85a4c | zone count stride; high-conf |
| 0x08085a88 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 | gduelphaseflag_85a88 | build_field_action_text_by_zone_type ctrl word read; high-conf |
| 0x08085a8c | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc:405 | lpbar_anim_st_85a8c | [gDuelPhaseFlags+0x4cc] = ctrl_word 0 check; high-conf |
| 0x08085b48 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_85b48 | caseD_17 of build_field_action_text_by_zone_type; high-conf |
| 0x08085b70 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 | p1lp_1ce8_85b70 | caseD_5; high-conf |
| 0x08085b4c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85b4c | [gDuelCardCtxBase+4] player side flag; high-conf |
| 0x08085b74 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85b74 | caseD_5 player flag check; high-conf |
| 0x08085be4 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85be4 | caseD_6 inner text id select; high-conf |
| 0x08085c0c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:317 | gequipchainslot_85c0c | caseD_12 [gEquipChainSlotRefs+0] current side; high-conf |
| 0x08085c10 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85c10 | caseD_12 player side check; high-conf |
| 0x08085c58 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85c58 | caseD_f player side check; high-conf |
| 0x08085c94 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85c94 | caseD_10 player side check; high-conf |
| 0x08085cbc | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85cbc | caseD_19 player side check; high-conf |
| 0x08085d18 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 | gduecardctx_85d18 | caseD_1d player side check; high-conf |

### REF_SLOTS (USER-label + DATA-ref)

| slot addr | value | gas_label | slot_label | evidence |
|---|---|---|---|---|
| 0x080854e0 | 0x080854e4 | switchD_080854da__switchdataD_080854e4 (already labeled in asm) | switchdata_ref_854e0 | Points to switch data table; already has ASM label at target; rename slot only |
| 0x08085a90 | 0x08085a94 | switchD_08085a86__switchdataD_08085a94 (already labeled in asm) | switchdata_ref_85a90 | Same pattern |
| 0x08085b98 | 0x08085b9c | switchD_08085b94__switchdataD_08085b9c (already labeled in asm) | switchdata_ref_85b98 | Same pattern |
| 0x08085d44 | 0x09e3f14c | (no existing label; raw ROM addr in text table area) | text_sep_ptr_85d44 | Value 0x09e3f14c = game text separator record (3 ROM refs; first byte 0x0a); used in build_field_action_text_by_zone_type as append_game_text_if_raw argument; high-conf |
| 0x08085d48 | 0x0000010d | (literal 0x10d; tail text ID) | text_tail_id_85d48 | text_id 0x10d appended after separator; same fn; med-conf (text ID semantics not reverified) |
| 0x08085c3c | 0x00000105 | (literal 0x105; text ID) | text_id_105_85c3c | caseD_e: ldr r1, DAT_08085c3c; b LAB_08085d0e -> copy_game_text_if_raw(r4, 0x105); med-conf |
| 0x08085ccc | 0x0000010b | (literal 0x10b; text ID) | text_id_10b_85ccc | caseD_1b: ldr r1, DAT_08085ccc; b LAB_08085d0e; med-conf |

### RENAME_SLOTS (slot label rename + EOL)

The PTR_gP1LifePoints_xxxxxxxx slots already hold gP1LifePoints (correct equate); only the
slot label needs rename to snake_case per naming convention.

| slot addr | current_label | new slot_label | eol |
|---|---|---|---|
| 0x08085368 | PTR_gP1LifePoints_08085368 | gp1lp_ptr_85368 | none |
| 0x080854a0 | PTR_gP1LifePoints_080854a0 | gp1lp_ptr_854a0 | none |
| 0x080857c4 | PTR_gP1LifePoints_080857c4 | gp1lp_ptr_857c4 | none |
| 0x080857f8 | PTR_gP1LifePoints_080857f8 | gp1lp_ptr_857f8 | none |
| 0x080858fc | PTR_gP1LifePoints_080858fc | gp1lp_ptr_858fc | none |
| 0x08085b44 | PTR_gP1LifePoints_08085b44 | gp1lp_ptr_85b44 | none |
| 0x08085b6c | PTR_gP1LifePoints_08085b6c | gp1lp_ptr_85b6c | none |
| 0x08085a20 | PTR_gP1LifePoints_08085a20 | gp1lp_ptr_85a20 | none |

### FUNC_RENAME

None for the 10 pre-existing named functions in Seg-1 (all names consistent with bodies).
New functions from block1+block2 disasm are named in the disasm plan below (Fix #2).

### PLATE (R5)

One plate comment in Seg-1 contains CJK (mojibake risk):

| fn addr | current plate (excerpt) | action |
|---|---|---|
| 0x080852e4 dispatch_equip_display_with_pair_card_id | "@  (CJK text describing pair card ID dispatch)" | Replace entire plate with ASCII: "Dispatches equip activation display and resolves paired card ID. Calls dispatch_equip_activation_display_by_confirm_state: if returns 0 outputs 0 (incomplete). Else: checks card_slot[+6] bits[4:2] (mask 0x1c = pair-slot flag); if 0 returns 1. Else: calls read_effect_slot_side_and_type(card_slot,0) -> (side,type); calls resolve_slot_card_id_for_pair(type,side) -> pair_card_id; writes to card_slot[+0xa] (strh). Returns 1." |

All other 9 function plates in Seg-1 are confirmed ASCII only (grep [^\x00-\x7F] clean for
those comment lines).

---

## carve 计划 (R7, 如有)

None. Block 0x080850f0 and 0x08085130 are both code (R4 disasm), not data to carve.

The fn-ptr table at 0x08085118..0x0808512c (6 .word entries pointing into block2) is already
present in the asm as explicit .word lines between the two ROM_INCBIN blocks -- no carve needed.

---

## disasm 计划 (R4)

### Block 1: 0x080850f0 / 0x28  THUMB

Single function. Confirmed prologue: 0xb510 = push {r4,lr}.
- clearListing 0x080850f0 .. 0x08085118
- setTMode THUMB for [0x080850f0, 0x08085118)
- DisassembleCommand at 0x080850f0
- createFunction at 0x080850f0; setFunctionName -> dispatch_equip_slot_display_by_type_scarr
- CSV row: 0x080850f0, dispatch_equip_slot_display_by_type_scarr
- Plate (ASCII): "fn_activate handler for CID 0x196a (Scarr, Scout of Dark World). Reads [gDuelPhaseFlags+SLOT_DISPLAY_TYPE_OFF]; if <= 5 dispatches to one of 4 sub-handlers (types 0,1/4,2/5,3) via raw-ptr table at 0x08085118 (MOV PC,r0). Returns 0 on normal advance, 1 on skip."

### Block 2: 0x08085130 / 0x14c  THUMB  (13 createFunction targets + 3 degenerate skip)

Analysis of 16 listed entry points reveals 3 are NOT valid code starts:
- 0x80851cc: second halfword of BL instruction at 0x80851ca/cc (mid-BL split; no word-aligned ref); skip createFunction.
- 0x808520e: 0x0000 padding byte after B instruction; skip createFunction.
- 0x8085210: literal pool word = 0x0201c4e0 (gP1LifePoints); skip createFunction.

13 valid createFunction targets. Procedure:
- clearListing 0x08085130 .. 0x0808527c
- setTMode THUMB for [0x08085130, 0x0808527c)
- Per entry (address-ordered): DisassembleCommand at each address; createFunction; setFunctionName.
- Post-disasm check: ROM_INCBIN/.byte-code grep in [0x08085130, 0x0808527c) == 0.

Entry order for per-stub DisassembleCommand (13 valid EPs):
  0x08085130, 0x08085140, 0x08085142, 0x08085144, 0x08085150, 0x080851a8,
  0x080851d4, 0x08085200, 0x08085204,
  0x08085228, 0x08085230, 0x08085248, 0x0808524a

---

## Block disasm function naming

### Block 1 (1 function)

| addr | standalone-or-alt-entry | proposed_name | conf | ASCII plate | CSV row |
|------|------------------------|---------------|------|-------------|---------|
| 0x080850f0 | standalone (fn_activate via CID 0x196a THUMB+1 ref at 0x9e46248) | dispatch_equip_slot_display_by_type_scarr | high | "fn_activate for Scarr (CID 0x196a). Reads [gDuelPhaseFlags+SLOT_DISPLAY_TYPE_OFF]; if <= 5 dispatches to one of 4 sub-handler entries via raw-ptr table at 0x08085118 (MOV PC,r0). Returns 0 on advance, 1 on skip/done." | 0x080850f0, dispatch_equip_slot_display_by_type_scarr |

### Block 2 (13 createFunction EPs; 3 degenerate skipped)

The 4 standalone handlers cover SLOT_DISPLAY_TYPE values 0..5 dispatched from block1.
Cascade alt-entries within the type-0 body (0x8085140/42/44/50) and type-2/5 body
(0x8085200/04/28/48/4a) receive createFunction calls; their bodies fall through to the
shared epilogue at 0x808526e (POP {r4}; POP {r1}; BX r1) which belongs to block1's
stack frame -- these are tail-dispatch sub-handlers, not independently callable routines.

Degenerate skips (no createFunction):
- 0x080851cc: second halfword of BL at 0x80851ca/cc; non-aligned coincidental ref; not code start.
- 0x0808520e: 0x0000 padding after B instruction; no ref.
- 0x08085210: literal pool (gP1LifePoints = 0x0201c4e0); not code.

| addr | standalone-or-alt-entry | proposed_name | conf | ASCII plate | CSV row |
|------|------------------------|---------------|------|-------------|---------|
| 0x08085130 | standalone (table[0] raw ref @0x8085118) | clear_equip_slot_attr_bits_and_activate | high | "Type-0 sub-handler. Clears bits 15-17 of slot+4 (sprite attr word) and bits 2-4 of slot+6 (display byte), then falls through to check player-zone match and set LP activation." | 0x08085130, clear_equip_slot_attr_bits_and_activate |
| 0x08085140 | alt-entry into type-0 body (no external word-aligned ref; Ghidra will create from clearListing+disasm range) | store_equip_slot_attr_byte_and_activate | med | "Alt-entry into type-0 body after sprite-word clear; executes STRB r0,[r4,#6] to store pre-computed display byte, then falls through to player-zone match check." | 0x08085140, store_equip_slot_attr_byte_and_activate |
| 0x08085142 | alt-entry into type-0 body (no external word-aligned ref) | load_equip_slot_player_and_activate | med | "Alt-entry; skips display byte store, loads player-flag byte at slot+2, then falls through to eval_equip_slot_player_match_and_set_lp_active logic." | 0x08085142, load_equip_slot_player_and_activate |
| 0x08085144 | alt-entry into type-0 body (no external word-aligned ref) | eval_equip_slot_player_match_and_set_lp_active | high | "Core type-0 eval: extracts bit0 of slot+2 as player side; loads slot+0x14 word; checks bits 11 and 9 vs player (same-side guard -> return 1). Calls count_effect_node_zone_activations; if 0 returns 1. Checks gDuelCardCtxBase[player+8]==1: if yes writes 1 to gEquipLpActivBitmap[player]; else calls invoke_card_display_op_0x31_sub1(0x13a). Increments SLOT_DISPLAY_TYPE, returns 0." | 0x08085144, eval_equip_slot_player_match_and_set_lp_active |
| 0x08085150 | alt-entry into type-0 body (no external word-aligned ref) | check_equip_slot_zone_bit9_and_activate | med | "Alt-entry inside type-0 eval; re-enters after bit-11 check, tests bit 9 of slot+0x14 vs player side (second same-side guard -> return 1). Falls through to activation path." | 0x08085150, check_equip_slot_zone_bit9_and_activate |
| 0x080851a8 | standalone (table[1,4] raw refs @0x808511c and @0x8085128; types 1 and 4) | check_lp_pending_and_set_equip_activation_state | high | "Types 1 and 4 sub-handler. Reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]: if zero returns 1 (no pending, skip). Else extracts player from slot+2, loads CID from slot+0, calls set_equip_activation_state_by_mode(player, CID, check_effect_node_handler_for_slot+1). Increments SLOT_DISPLAY_TYPE, returns 0." | 0x080851a8, check_lp_pending_and_set_equip_activation_state |
| 0x080851d4 | standalone (table[2,5] raw refs @0x8085120 and @0x808512c; types 2 and 5) | enqueue_equip_slot_sprite_if_display_confirmed | high | "Types 2 and 5 sub-handler. Calls check_activation_display_state_is_confirmed: if not confirmed decrements SLOT_DISPLAY_TYPE by 2, returns 0. If confirmed: loads ELIGIB_SPRITE_CTRL_OFF and ELIGIB_ANIM_STATE_OFF from gP1LifePoints region; calls enqueue_equip_slot_sprite_with_code_rotation then count_effect_node_zone_activations(r4); if activations <= 1 returns 1; checks bits 4-2 of slot+6 <= 1, then increments SLOT_DISPLAY_TYPE and returns 0." | 0x080851d4, enqueue_equip_slot_sprite_if_display_confirmed |
| 0x08085200 | alt-entry into type-2/5 body (one word-aligned THUMB+1 ref at 0x8ad7afc -- context: compressed-data region, likely coincidental) | check_activation_count_lte1_and_advance | med | "Alt-entry after enqueue sprite call; CMP r0,#1; BLE -> return 1 (if activation count <= 1 skip advance). Else loads byte at slot+6, extracts bits 4-2, tests > 1 -> return 1; else increments SLOT_DISPLAY_TYPE and returns 0." | 0x08085200, check_activation_count_lte1_and_advance |
| 0x08085204 | alt-entry into type-2/5 body (no external word-aligned ref) | check_slot_display_field_and_advance_type | med | "Alt-entry with byte already in r4; extracts bits 4-2 from r4 (3-bit display field 0-7); if > 1 returns 1; else B to increment-SLOT_DISPLAY_TYPE path (returns 0)." | 0x08085204, check_slot_display_field_and_advance_type |
| 0x08085228 | alt-entry (no external word-aligned ref; immediately B forward to store path) | store_decremented_display_type_and_return | med | "Minimal stub: immediately branches to 0x808526a (STR r0,[r1]; return 0). Entered with r0 = display_type - 2 and r1 = ptr to SLOT_DISPLAY_TYPE_OFF. Stores the decremented value and returns 0. Used as shared tail for type-2/5 not-confirmed path." | 0x08085228, store_decremented_display_type_and_return |
| 0x08085230 | standalone (table[3] raw ref @0x8085124; type 3) | activate_or_enqueue_type3_equip_slot_display | high | "Type-3 sub-handler. Reads player from slot+2; checks gDuelCardCtxBase[player*4+8]: if == 1 writes 1 to [gP1LifePoints+LP_ACTIVATION_PENDING_OFF] and increments SLOT_DISPLAY_TYPE, returns 0. Else calls invoke_card_display_op_0x31_sub1(0x13b) then increments SLOT_DISPLAY_TYPE, returns 0." | 0x08085230, activate_or_enqueue_type3_equip_slot_display |
| 0x08085248 | alt-entry into type-3 body (no external word-aligned ref) | complete_lp_pending_offset_and_set | med | "Alt-entry mid-computation of LP_ACTIVATION_PENDING_OFF: r3 already holds 0xea (from prior MOVS at 0x8085246); LSLS r3,r3,#5 -> r3=0x1d40; ADDS r0,r0,r3; STR r1,[r0]; then B to increment-SLOT_DISPLAY_TYPE path." | 0x08085248, complete_lp_pending_offset_and_set |
| 0x0808524a | alt-entry into type-3 body (no external word-aligned ref) | write_lp_activation_pending_and_advance | med | "Alt-entry with r0 = final gP1LifePoints+LP_ACTIVATION_PENDING_OFF ptr and r1=1 already computed; STR r1,[r0] writes activation pending; B to increment-SLOT_DISPLAY_TYPE path, returns 0." | 0x0808524a, write_lp_activation_pending_and_advance |

### CSV rows summary (14 total: 1 block1 + 13 block2)

```
0x080850f0, dispatch_equip_slot_display_by_type_scarr
0x08085130, clear_equip_slot_attr_bits_and_activate
0x08085140, store_equip_slot_attr_byte_and_activate
0x08085142, load_equip_slot_player_and_activate
0x08085144, eval_equip_slot_player_match_and_set_lp_active
0x08085150, check_equip_slot_zone_bit9_and_activate
0x080851a8, check_lp_pending_and_set_equip_activation_state
0x080851d4, enqueue_equip_slot_sprite_if_display_confirmed
0x08085200, check_activation_count_lte1_and_advance
0x08085204, check_slot_display_field_and_advance_type
0x08085228, store_decremented_display_type_and_return
0x08085230, activate_or_enqueue_type3_equip_slot_display
0x08085248, complete_lp_pending_offset_and_set
0x0808524a, write_lp_activation_pending_and_advance
```

---

## 新增 constants / 全局

All new constants require value-grep == 0 in existing .inc files (confirmed above).

### card_info.inc (8 new CIDs)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| REGULATION_OF_TRIBE_CID | 0x00001358 | card-stats.s:9908 card_0761 "The Regulation of Tribe"; 0x1358 in card_info.inc = 0 hits | 11 |
| TORRENTIAL_TRIBUTE_CID | 0x000013fa | card-stats.s:11338 card_0871 "Torrential Tribute"; 0x13fa in card_info.inc = 0 hits | 9 |
| SHADOW_OF_EYES_CID | 0x0000140f | card-stats.s:11585 card_0890 "Shadow of Eyes"; 0x140f in card_info.inc = 0 hits | 8 |
| EMERGENCY_PROVISIONS_CID | 0x000014e6 | card-stats.s card_1046 "Emergency Provisions"; 0x14e6 in card_info.inc = 0 hits (Fix #1: was incorrectly marked REUSE) | (counted from EQ slot evidence) |
| DROP_OFF_CID | 0x0000151c | card-stats.s:14198 card_1091 "Drop Off"; 0x151c in card_info.inc = 0 hits | 16 |
| ADHESION_TRAP_HOLE_CID | 0x000015f8 | card-stats.s:16291 card_1252 "Adhesion Trap Hole"; 0x15f8 in card_info.inc = 0 hits | 9 |
| DD_TRAP_HOLE_CID | 0x0000192e | card-stats.s:25118 card_1931 "D.D. Trap Hole"; 0x192e in card_info.inc = 0 hits | 8 |
| TRAGEDY_CID | 0x000012d7 | card-stats.s:8621 card_0662 "Tragedy"; 0x12d7 in card_info.inc = 0 hits (mentioned in cid_12da comment but not defined) | 10 |

### ewram.inc (5 new gDuelPhaseFlags-relative offsets)

| const_name | value | evidence | ROM refs |
|---|---|---|---|
| SLOT_DISPLAY_TYPE_OFF | 0x000004b0 | [gDuelPhaseFlags+0x4b0] = slot display type selector in block1 fn (0x96<<3=0x4b0); cmp r0,#5 -> 6-way dispatch; 0x4b0 in ewram.inc = 0 hits | 35 |
| LP_BAR_ROW_COUNT_OFF | 0x000004c8 | [gDuelPhaseFlags+0x4c8] = LP bar row count word; submit_lp_bar_sprite_row_by_type movs r2,#0x99;lsls r2,#3=0x4c8; incremented up to 0x20; 0x4c8 in ewram.inc = 0 hits | 5 |
| LP_BAR_ROW_ACTIVE_OFF | 0x000004d0 | [gDuelPhaseFlags+0x4d0] = LP bar row active flag; movs r2,#0x9a;lsls r2,#3=0x4d0; cmp r1,#0 (skip if nonzero); neighbors LP_BAR_ANIM_STATE_OFF(0x4cc) and SPRITE_ROW_ENTRY_DATA_OFF(0x4d4); 0x4d0 in ewram.inc = 0 hits | 8 |
| LP_BAR_ROW_XCOORD_OFF | 0x000004d3 | [gDuelPhaseFlags+count+0x4d3] = per-row x-coord byte array; strb r4,[r0] writes x_coord; adjacent to SPRITE_ROW_ENTRY_DATA_OFF(0x4d4); 0x4d3 in ewram.inc = 0 hits | 22 |
| FIELD_DISPLAY_TYPE_OFF | 0x0000057c | [gDuelPhaseFlags+0x57c] = field display type code; dispatch_field_display_state_by_type (next segment fn) reads [gDuelPhaseFlags+0xaf<<3=0x578] type and [+0x57c] ctrl; build_sprite_row_from_zone_state also reads [gDuelPhaseFlags+0x57c]; 7 ROM refs; 0x57c in ewram.inc = 0 hits | 7 |

---

## §5.1 登记 (Rule 3) -- 0 引用块

No ROM_INCBIN or .byte blocks with 0 refs in Seg-1. Both blocks have references and
are classified R4 disasm above.

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| slot | consumer evidence | confidence |
|---|---|---|
| gEquipChainSlotRefs (0x0201bb90) | asm/11 L7-16: enqueue_effect_slot_attr_from_bb reads [gEquipChainSlotRefs+4] player_flag and [+0x20] col_nibble | high |
| gDuelPhaseFlags (0x0201b290) | asm/11 L122-264: submit_lp_bar_sprite_row_by_type full scan of LP bar state fields; LP_BAR_ANIM_STATE_OFF/LP_BAR_DISPLAY_CTR_OFF confirmed against ewram.inc | high |
| FIELD_DISPLAY_TYPE_OFF (0x57c) | asm/11 L267-337: build_sprite_row_from_zone_state; DAT_08085428=0x57c; ldr r0,[r3,r2+0x57c-0x4cc] pattern | high |
| SLOT_DISPLAY_TYPE_OFF (0x4b0) | block1 ROM bytes 0x080850f0-0x080850fe: ldr r0,[gDuelPhaseFlags]; movs r1,#0x96; lsls r1,#3 -> r1=0x4b0; adds r0,r0,r1; ldr r0,[r0] | high |
| CID_1358 (Regulation of Tribe) | asm/11 L436-437: caseD_3 in scan_equip_target_slots_for_card uses 0x1358 as lower bound for Embodiment of Apophis group | high |
| DD_TRAP_HOLE_CID (0x192e) | asm/11 L614-616 and L652-654: caseD_8 and caseD_9 both compare r4 against 0x192e as zone type discriminator | high |

---

## 求助

One low-confidence item:

- 0x08085200 check_activation_count_lte1_and_advance: the one THUMB+1 ref at 0x8ad7afc is
  in a compressed-data region (non-code context confirmed by surrounding byte entropy). The
  address may have no real external callers and the function may only be reachable as a
  mid-body alt-entry of enqueue_equip_slot_sprite_if_display_confirmed (confidence: med).
  No semantic change implied -- the name is based on observable behavior at the entry point
  regardless of call convention. Not BLOCKED.
