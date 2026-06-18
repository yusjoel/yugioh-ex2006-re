# Refine Proposal: F09-Seg-5a  [0x08072d20..0x08073a5c)

## Splitting rationale
Seg-5 (10 ROM_INCBIN blocks, 88 slots) is split at function boundary 0x08073a5c
(test_equip_target_slot_by_zone_descriptor_match) giving:
- Seg-5a: [0x08072d20, 0x08073a5c) -- 12 fns + blocks B1-B6 (6 blocks)
- Seg-5b: [0x08073a5c, 0x08074338) --  8 fns + blocks B7-B10 (4 blocks)

## 段测绘

### 函数入口 x12
- 0x08072d20  enqueue_zone_sprite_attr_type11_from_slot  (push {lr})
- 0x08072d34  tick_equip_lp_display_state_by_slot        (push {r4,r5,r6,r7,lr})
- 0x08072eb4  setup_equip_oam_by_placeable_card_id_and_zone (push {r4,r5,r6,lr})
- 0x08072fd4  tick_equip_lp_display_bitmap_state_by_slot  (push {r4,r5,lr})
- 0x080730e0  tick_equip_lp_display_type18_state_by_slot  (push {lr})
- 0x080732a8  enqueue_equip_zone_sprite_by_slot_lp_state  (push {r4,lr})
- 0x080732fc  enqueue_slot_sprite_if_chain_flags_and_node_active (push {r4,r5,r6,r7,lr})
- 0x0807338c  tick_equip_deck_pair_hand_sprite_state       (push {r4,r5,lr})
- 0x08073428  apply_lp_delta_for_slot_by_series_code       (push {r4,r5,lr})
- 0x08073454  tick_neo_daedalus_equip_display_seq          (push {r4,r5,r6,r7,lr})
- 0x08073760  enqueue_slot_sprite_mode3_with_effect_node   (push {r4,r5,r6,lr})
- 0x080737ac  dispatch_equip_slot_activation_or_sprite_by_type (push {r4,r5,r6,lr})

(Note: 0x0807381c enqueue_hand_spell_sprite_by_set_code_match ends at 0x08073863; B5 block
       is 0x08073864..0x0807388b; next named fn is at 0x08073a5c in Seg-5b.)

Additional named fn in gap region (after B4 dispatch table):
- 0x08073760  enqueue_slot_sprite_mode3_with_effect_node
- 0x080737ac  dispatch_equip_slot_activation_or_sprite_by_type
- 0x0807381c  enqueue_hand_spell_sprite_by_set_code_match

Total: 13 named fns (including enqueue_hand_spell at 0x0807381c which ends before B5)

### ROM_INCBIN blocks x6
| Block | Start      | Size  | End        | Classification |
|-------|-----------|-------|-----------|----------------|
| B1    | 0x0807313e | 0x2a  | 0x08073168 | R4 disasm: fn_eligible Trap Dustshoot (CID 0x1546) + literal pool; dispatch table at 0x08073168-0x080731e3 -> B2 |
| B2    | 0x080731e4 | 0xc4  | 0x080732a8 | R4 disasm: dispatch sub-stubs (card_id -> effect handler; 3 stubs + default) |
| B3    | 0x0807356c | 0x48  | 0x080735b4 | R4 disasm: fn_eligible Machine Duplication (CID 0x157a) / League (CID 0x1978) shared stub + literal pool; dispatch table at 0x080735b4-0x08073627 -> B4 |
| B4    | 0x08073628 | 0x138 | 0x08073760 | R4 disasm: dispatch sub-stubs (zone_type -> effect handler; ~6 stubs + default) |
| B5    | 0x08073864 | 0x28  | 0x0807388c | R4 disasm: fn_eligible A Cat of Ill Omen (CID 0x1590) + An Owl of Luck (CID 0x1593) shared stub + literal pool; dispatch table at 0x0807388c-0x080738ff -> B6 |
| B6    | 0x08073900 | 0x15c | 0x08073a5c | R4 disasm: A Cat of Ill Omen + An Owl of Luck dispatch sub-stubs; reached via raw refs from dispatch table 0x0807388c-0x080738ff (B5) |

### 残留自动名槽 x61
(See EQ_SLOTS/REF_SLOTS/RENAME_SLOTS tables below -- 61 total)

## 数据块分类 (Rule 2/3)

| 块  | ref-scan (raw / THUMB+1)                    | 判定   | 理由                                                         |
|-----|---------------------------------------------|--------|--------------------------------------------------------------|
| B1  | raw=0 / entry 0x08073140 THUMB+1=1          | R4 disasm | FS handler table ref at 0x09e411b0; value 0x08073141; CID at ref-0x4 = 0x1546 (Trap Dustshoot, card-stats line 14705). Literal pool at 0x08073160-0x08073167 contains gDuelPhaseFlags + ptr to B2 dispatch table |
| B2  | entry 0x080731e4 raw=1 / 0x08073206 thumb+1=1 | R4 disasm | Entry 0x080731e4 raw=1 at 0x080731e0 (dispatch table self-ptr); 0x08073206 thumb+1 at 0x09ec7d0b (misaligned=3, compressed false positive). Raw sub-stub refs from preceding dispatch table 0x08073168..0x080731e3 confirm code. THUMB opcodes at block start: 0x4a0a (ldr r2,[pc,...]) valid |
| B3  | raw=0 / entry 0x0807356c THUMB+1=2          | R4 disasm | FS handler table refs at 0x09e41288 (CID 0x157a Machine Duplication) and 0x09e42dd0 (CID 0x1978 League). Both point to same fn+1=0x0807356d (shared fn_eligible for 2 cards). Literal pool at 0x080735b0 contains ptr to B4 dispatch table |
| B4  | entry 0x08073628 raw=1 / 0x08073660 thumb+1=1 | R4 disasm | Entry 0x08073628 raw=1 at 0x08073624 (dispatch table self-ptr); 0x08073660 thumb+1 at 0x0866dd88 (0x0866xxxx compressed data region, surrounding bytes 0x3a8a57e0/0x860f080a irregular -> false positive). Raw sub-stub refs from dispatch table 0x080735b4..0x08073627 confirm code |
| B5  | raw=0 / entry 0x08073864 THUMB+1=2          | R4 disasm | FS handler table refs: 0x09e44108 stores 0x08073865 (CID at 0x09e44104=0x1590 A Cat of Ill Omen, card_1172 pw=24140059); 0x09e44138 stores 0x08073865 (CID at 0x09e44134=0x1593 An Owl of Luck, card_1175 pw=23927567). Shared stub serves both cards. Literal pool at 0x08073884-0x0807388b: gDuelPhaseFlags + ptr 0x0807388c to B6 dispatch table |
| B6  | entry 0x08073900 raw=1 (at 0x080738fc dispatch table self-ptr) / THUMB+1=0 | R4 disasm | Raw sub-stub refs from B5 dispatch table (0x0807388c-0x080738ff) confirm code. Sub-stubs: 0x08073a46(x1), 0x08073a54(x22 default), 0x08073a34(x1), 0x080739b0(x1), 0x08073968(x1), 0x08073946(x1), 0x08073932(x1), 0x08073900(x1 self-ref). THUMB opcodes at 0x08073900: 0x78aa/0x07d0 (ldrb/beq) confirmed. DAT_08073900 is the auto-named label for this block. |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

| 槽                          | 值           | const_name                 | 来源/C5 dedup                                 |
|-----------------------------|--------------|----------------------------|-----------------------------------------------|
| DWORD_08072d58              | 0x0201b290   | gDuelPhaseFlags            | REUSE ewram.inc                               |
| DWORD_08072d90              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_08072db8              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF      | REUSE ewram.inc                               |
| DWORD_08072dc0              | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc                               |
| DWORD_08072df4              | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc (dup slot same fn)            |
| DWORD_08072e5c              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF      | REUSE ewram.inc                               |
| DWORD_08072e60              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_08072e64              | 0x0201c600   | gP1FieldArrayCBase         | REUSE ewram.inc                               |
| DWORD_08072e68              | 0x00001c88   | EQUIP_CHAIN_BASE_OFF       | NEW: gP1FieldArrayCBase(0x0201c600)+0x1c88=0x0201e288=gEquipChainEntryBase (ewram.inc line 390); offset not yet in constants. grep 0x1c88 ewram.inc -> 0 hits. NEW to equip_lp_delta.inc or ewram.inc |
| DWORD_08072eb0              | 0x0201bb90   | gEquipChainSlotRefs        | REUSE ewram.inc                               |
| DWORD_08072ee4              | 0x000013ff   | JAM_BREEDING_MACHINE_CID   | REUSE card_info.inc                           |
| DWORD_08072f1c              | 0x00001595   | COBRA_JAR_CID              | REUSE card_info.inc                           |
| DWORD_08072f20              | 0x000013ff   | JAM_BREEDING_MACHINE_CID   | REUSE card_info.inc (dup slot)                |
| DWORD_08072f2c              | 0x00001543   | STATUE_OF_THE_WICKED_CID   | NEW: card-stats line 14666 "Statue of the Wicked"; grep 0x1543 card_info.inc -> 0 hits |
| DWORD_08072f44              | 0x000015d5   | DES_DENDLE_CID             | REUSE card_info.inc                           |
| DWORD_08072f58              | 0x000019a5   | RAVIEL_LORD_CID            | REUSE card_info.inc                           |
| DWORD_08072f60              | 0x000013fb   | TOKEN_13FB_CID             | NEW: card-stats line 27068, slot=0x13FB copy=0 (unnamed token). grep 0x13fb card_info.inc -> 0 hits |
| DWORD_08072f68              | 0x000014fa   | TOKEN_14FA_CID             | NEW: card-stats line 27120, slot=0x14FA copy=0 (unnamed token). grep 0x14fa card_info.inc -> 0 hits |
| DWORD_08072f70              | 0x0000154e   | TOKEN_154E_CID             | NEW: card-stats line 27133, slot=0x154E copy=0 (unnamed token). grep 0x154e card_info.inc -> 0 hits |
| DWORD_08072f78              | 0x000015bd   | TOKEN_15BD_CID             | NEW: card-stats line 27146, slot=0x15BD copy=0 (unnamed token). grep 0x15bd card_info.inc -> 0 hits |
| DWORD_08072f84              | 0x000015be   | TOKEN_15BE_CID             | NEW: card-stats line 27159, slot=0x15BE copy=0 (unnamed token). grep 0x15be card_info.inc -> 0 hits |
| DWORD_08072f8c              | 0x00001603   | TOKEN_1603_CID             | NEW: card-stats line 27172, slot=0x1603 copy=0 (unnamed token). grep 0x1603 card_info.inc -> 0 hits |
| DWORD_08072f94              | 0x00001639   | TOKEN_1639_CID             | NEW: card-stats line 27185, slot=0x1639 copy=0 (unnamed token). grep 0x1639 card_info.inc -> 0 hits |
| DWORD_08072fcc              | 0x0000195a   | TOKEN_195A_CID             | NEW: card-stats line 27250, slot=0x195A copy=0 (unnamed token). grep 0x195a card_info.inc -> 0 hits |
| DWORD_08072fd0              | 0xffffdfff   | SPRITE_ATTR_CLR_BIT13      | NEW: ~0x2000, clears bit13 (player_id bit in sprite attr, PLAYER_BIT_SHIFT=0xd in fn comment). grep 0xffffdfff oam_attr.inc -> 0 hits. New in oam_attr.inc |
| DAT_08072ff4                | 0x0201b290   | gDuelPhaseFlags            | REUSE ewram.inc                               |
| DAT_08073040                | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DAT_08073074                | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc                               |
| DAT_08073090                | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc (dup slot)                    |
| DAT_080730dc                | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc                               |
| DAT_08073108                | 0x0201b290   | gDuelPhaseFlags            | REUSE ewram.inc                               |
| DAT_08073120                | 0x00001da8   | LP_CARD_TRACK_BASE_OFF     | REUSE ewram.inc                               |
| DWORD_080732f8              | 0x00001ce8   | P1LP_BLOCK2_OFF_1CE8       | REUSE ewram.inc                               |
| DWORD_08073380              | 0x000010d0   | LP_ACTIVATION_LINK_FLAG_OFF| REUSE ewram.inc                               |
| DWORD_08073384              | 0x0201bb90   | gEquipChainSlotRefs        | REUSE ewram.inc                               |
| DWORD_08073388              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_080733ac              | 0x0201b290   | gDuelPhaseFlags            | REUSE ewram.inc                               |
| DWORD_080733fc              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_08073400              | 0x0201c740   | gP1SlotSetCodeArray        | REUSE ewram.inc                               |
| DWORD_08073474              | 0x0201b290   | gDuelPhaseFlags            | REUSE ewram.inc                               |
| DWORD_080734d8              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF      | REUSE ewram.inc                               |
| DWORD_080734dc              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_080734e0              | 0x0201c510   | gDuelFieldSlots            | REUSE ewram.inc                               |
| DWORD_08073528              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF      | REUSE ewram.inc                               |
| DWORD_0807355c              | 0x000004a4   | EQUIP_PHASE_FRAME_OFF      | REUSE ewram.inc                               |
| DWORD_08073560              | 0x00000868   | PLAYER_BLOCK_STRIDE        | REUSE ewram.inc                               |
| DWORD_08073564              | 0x0201c600   | gP1FieldArrayCBase         | REUSE ewram.inc                               |
| DWORD_08073568              | 0x00001c88   | EQUIP_CHAIN_BASE_OFF       | REUSE same new const above (dup slot)         |

EQ total Seg-5a: EQ_REUSE=38, EQ_NEW=10; 48 EQ total.
  NEW (10 unique new constants, first-occurrence slot): STATUE_OF_THE_WICKED_CID, TOKEN_13FB_CID, TOKEN_14FA_CID, TOKEN_154E_CID, TOKEN_15BD_CID, TOKEN_15BE_CID, TOKEN_1603_CID, TOKEN_1639_CID, TOKEN_195A_CID, SPRITE_ATTR_CLR_BIT13.
  EQUIP_CHAIN_BASE_OFF created at DWORD_08072e68; second slot DWORD_08073568 = REUSE (+1 -> REUSE=38).
  REUSE=38: 37 pre-existing constant slots + DWORD_08073568 (EQUIP_CHAIN_BASE_OFF re-use).

### REF_SLOTS (USER-label + DATA-ref)

| 槽                              | target           | gas_label        | slot_label                          |
|---------------------------------|------------------|------------------|-------------------------------------|
| DWORD_08072d8c                  | gP1LifePoints    | gP1LifePoints    | DWORD_08072d8c -> .word gP1LifePoints |
| DWORD_08072dbc                  | gP1LifePoints    | gP1LifePoints    | DWORD_08072dbc -> .word gP1LifePoints |
| DWORD_08072df0                  | gP1LifePoints    | gP1LifePoints    | DWORD_08072df0 -> .word gP1LifePoints |
| PTR_gP1LifePoints_0807303c      | gP1LifePoints    | gP1LifePoints    | already named PTR_, rename label only |
| PTR_gP1LifePoints_08073070      | gP1LifePoints    | gP1LifePoints    | already named PTR_, rename label only |
| PTR_gP1LifePoints_0807308c      | gP1LifePoints    | gP1LifePoints    | already named PTR_, rename label only |
| PTR_gP1LifePoints_080730d8      | gP1LifePoints    | gP1LifePoints    | already named PTR_, rename label only |
| PTR_gP1LifePoints_0807311c      | gP1LifePoints    | gP1LifePoints    | already named PTR_, rename label only |
| DWORD_080732f4                  | gP1LifePoints    | gP1LifePoints    | DWORD_080732f4 -> .word gP1LifePoints |
| DWORD_0807337c                  | gP1LifePoints    | gP1LifePoints    | DWORD_0807337c -> .word gP1LifePoints |

REF total Seg-5a: 10 (all gP1LifePoints -- 5 already PTR_ labeled, 5 DWORD_ to convert)

### RENAME_SLOTS (auto-name -> semantic label)

| 槽             | addr       | new_label                                    | EOL_ascii                                   |
|----------------|-----------|----------------------------------------------|---------------------------------------------|
| DAT_080731e4   | 0x080731e4 | trap_dustshoot_dispatch_sub_stubs_31e4       | Trap Dustshoot CID=0x1546 dispatch sub-stubs |
| DAT_08073628   | 0x08073628 | machine_dup_dispatch_sub_stubs_3628          | Machine Dup/League CID=0x157a/0x1978 sub-stubs |
| DAT_08073900   | 0x08073900 | cat_ill_omen_dispatch_sub_stubs_3900         | A Cat of Ill Omen/An Owl of Luck CID=0x1590/0x1593 sub-stubs |

RENAME total Seg-5a: 3

### FUNC_RENAME (if any)

None identified.

### PLATE (R5)

| fn                                            | addr       | action                                                              |
|-----------------------------------------------|-----------|---------------------------------------------------------------------|
| enqueue_spirit_zone_sprite_type11             | 0x08074318 | stale FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id (substring replace; fn is in Seg-5b but cross-ref is to Seg-3 fn which has correct name) |

Note: The stale FUN_ references found in Seg-5 are at line 11513 and 11549:
- Line 11513: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id (asm/09 Seg-3)
- Line 11549: FUN_08074708 -> dispatch_equip_zone_sprite_mode2_or_activation (asm/09 Seg-6, not yet named) -- leave as-is until Seg-6 processed; or update if name is confirmed
  FUN_0807479c -> dispatch_equip_chain_activation_if_zone_pair_aligned (asm/09 Seg-6, not yet named) -- same

Line 11513 is in Seg-5b (enqueue_spirit_zone_sprite_type11 plate). Handle in Seg-5b.
Line 11549 is in apply_equip_activation_for_zone_slot_sprite @ 0x08074338 (Seg-6, out of scope).

## disasm 计划 (R4)

### B1: fn_eligible_trap_dustshoot @ 0x08073140 (block 0x0807313e/0x2a)
- Block structure: .zero 0x2 (0x0807313e-0x0807313f) + fn_elig stub (0x08073140-0x08073167)
- FS handler ref: 0x09e411b0 stores 0x08073141 (THUMB+1); CID at ref-0x4=0x1546 (Trap Dustshoot)
- Stub contains literal pool: 0x08073160=gDuelPhaseFlags, 0x08073164=0x08073168 (ptr to B2 dispatch table)
- Action: setTMode(0x08073140); DisassembleCommand(0x08073140..0x08073168); createDWord for pools at 0x08073160/0x08073164
- Dispatch table 0x08073168..0x080731e3 (0x7c bytes, 31 .word entries): label as trap_dustshoot_dispatch_table_3168; entries reference B2 sub-stubs

### B2: dispatch sub-stubs @ 0x080731e4 (block 0x080731e4/0xc4, end 0x080732a8)
- Sub-stub entry addresses from dispatch table: 0x08073290, 0x08073280, 0x0807326c, 0x080732a0, 0x0807322a, 0x080731e4
- Default stub at 0x080732a0: movs r0,#0x0 (return 0, opcode 0x2000)
- Action: clearListing(0x080731e4..0x080732a8); setTMode; DisassembleCommand per stub entry point
- Label each non-default stub: trap_dustshoot_sub_31e4, trap_dustshoot_sub_322a, trap_dustshoot_sub_326c, trap_dustshoot_sub_3280, trap_dustshoot_sub_3290, trap_dustshoot_default_32a0

### B3: fn_eligible_machine_dup_and_league @ 0x0807356c (block 0x0807356c/0x48, end 0x080735b4)
- FS handler refs: 0x09e41288 (CID 0x157a Machine Duplication), 0x09e42dd0 (CID 0x1978 League) -- shared stub
- Stub contains literal pool: pool at 0x080735b0=0x080735b4 (ptr to B4 dispatch table)
- Other pool: 0x0201b290=gDuelPhaseFlags somewhere in the block
- Action: setTMode(0x0807356c); DisassembleCommand(0x0807356c..0x080735b4); createDWord for pools
- Dispatch table 0x080735b4..0x08073627 (0x74 bytes, 29 .word entries): label as machine_dup_dispatch_table_35b4

### B4: dispatch sub-stubs @ 0x08073628 (block 0x08073628/0x138, end 0x08073760)
- Sub-stub entry addresses from dispatch table: 0x0807374c, 0x08073756, 0x0807373a, 0x08073704, 0x080736ee, 0x08073690, 0x08073628
- Default stub at 0x08073756: movs r0,#0x0 (return 0, opcode 0x2000)
- Action: clearListing(0x08073628..0x08073760); setTMode; DisassembleCommand per stub entry point
- Label stubs: machine_dup_sub_3628, machine_dup_sub_3690, machine_dup_sub_36ee, machine_dup_sub_3704, machine_dup_sub_373a, machine_dup_sub_374c, machine_dup_default_3756

### B5: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864 (block 0x08073864/0x28, end 0x0807388c)
- FS handler refs: 0x09e44108 stores 0x08073865 (CID at 0x09e44104=0x1590 A Cat of Ill Omen); 0x09e44138 stores 0x08073865 (CID at 0x09e44134=0x1593 An Owl of Luck). Shared fn_eligible stub for both cards (same pattern as B3 Machine Dup + League).
- Neither CID appears as a literal-pool word in the fn body -- no new CID constants needed for B5.
- Literal pool: 0x08073884=gDuelPhaseFlags, 0x08073888=0x0807388c (ptr to B6 dispatch table)
- Action: setTMode(0x08073864); DisassembleCommand(0x08073864..0x0807388c); createDWord for pool words; label stub fn_eligible_cat_ill_omen_and_owl_of_luck
- Dispatch table 0x0807388c..0x080738ff (0x74 bytes, 29 .word entries): label as cat_ill_omen_dispatch_table_388c (B6 sub-stubs in block 0x73900/0x15c)

### B6: cat_ill_omen_dispatch_sub_stubs @ 0x08073900 (block 0x08073900/0x15c, end 0x08073a5c)
- Dispatch table at 0x0807388c-0x080738ff (29 entries, in B5 literal-pool-referenced region):
  entries: 0x08073a46(x1), 0x08073a54(x22 default), 0x08073a34(x1), 0x080739b0(x1), 0x08073968(x1), 0x08073946(x1), 0x08073932(x1), 0x08073900(x1 self-ref)
- Sub-stub entry points (from dispatch table): 0x08073900, 0x08073932, 0x08073946, 0x08073968, 0x080739b0, 0x08073a34, 0x08073a46
- Default stub at 0x08073a54: movs r0,#0x0 / pop {r4,r5,r6} / pop {r1} / bx r1
- Action: clearListing(0x08073900..0x08073a5c); setTMode(0x08073900); DisassembleCommand per entry point
- Labels: cat_ill_omen_sub_3900, cat_ill_omen_sub_3932, cat_ill_omen_sub_3946,
          cat_ill_omen_sub_3968, cat_ill_omen_sub_39b0, cat_ill_omen_sub_3a34,
          cat_ill_omen_sub_3a46, cat_ill_omen_default_3a54

## carve 计画 (R7)

No inter-function ROM data tables requiring rom.s carve in Seg-5a. All 6 blocks are code (R4 disasm). The dispatch tables (0x08073168, 0x080735b4, 0x0807388c) are function-internal data that can remain in asm/09 with structural labels.

## 新增 constants / 全局

File: constants/card_info.inc (append)
- STATUE_OF_THE_WICKED_CID = 0x1543   @ Statue of the Wicked (card-stats line 14666)
- TOKEN_13FB_CID = 0x13fb             @ unnamed token slot (card-stats line 27068, copy=0)
- TOKEN_14FA_CID = 0x14fa             @ unnamed token slot (card-stats line 27120, copy=0)
- TOKEN_154E_CID = 0x154e             @ unnamed token slot (card-stats line 27133, copy=0)
- TOKEN_15BD_CID = 0x15bd             @ unnamed token slot (card-stats line 27146, copy=0)
- TOKEN_15BE_CID = 0x15be             @ unnamed token slot (card-stats line 27159, copy=0)
- TOKEN_1603_CID = 0x1603             @ unnamed token slot (card-stats line 27172, copy=0)
- TOKEN_1639_CID = 0x1639             @ unnamed token slot (card-stats line 27185, copy=0)
- TOKEN_195A_CID = 0x195a             @ unnamed token slot (card-stats line 27250, copy=0)
- TRAP_DUSTSHOOT_CID = 0x1546         @ Trap Dustshoot (card-stats line 14705)

File: constants/ewram.inc (append)
- EQUIP_CHAIN_BASE_OFF = 0x1c88       @ gP1FieldArrayCBase(0x0201c600)+0x1c88=gEquipChainEntryBase(0x0201e288); setup_equip_oam_by_placeable_card_id_and_zone; grep 0x1c88 ewram.inc -> 0 hits

File: constants/oam_attr.inc (append)
- SPRITE_ATTR_CLR_BIT13 = 0xffffdfff  @ AND mask: clears bit13 (player_id encode bit shift=0xd); setup_equip_oam_by_placeable_card_id_and_zone uses to clear player bit from sprite attr; grep 0xffffdfff oam_attr.inc -> 0 hits

## §5.1 登记 (Rule 3) -- 0 引用块

None in Seg-5a. All 6 blocks have confirmed refs (B1/B3/B5: FS THUMB+1 refs; B2/B4/B6: raw sub-stub refs from preceding dispatch tables which are loaded at runtime).

## 消费者证据 (R6)

### EQUIP_CHAIN_BASE_OFF (0x1c88)
- asm/09_equip_lp_display.s line 9598 (DWORD_08072e68): `ldr r3, DWORD_08072e68; adds r4,r4,r3; ldrh r2,[r4,#0x0]`
  Base in r4 = gP1FieldArrayCBase (0x0201c600); offset 0x1c88 -> 0x0201e288 = gEquipChainEntryBase (ewram.inc line 390). Confidence: high.
- asm/09_equip_lp_display.s line 10530 (DWORD_08073568): same pattern in tick_neo_daedalus_equip_display_seq.

### SPRITE_ATTR_CLR_BIT13 (0xffffdfff)
- asm/09_equip_lp_display.s line 9829: `ldr r3, DWORD_08072fd0; ands r1,r3; orrs r1,r2` where r2 = player_id << 0xd
  Used to clear old player_id bit then OR in new; function comment: PLAYER_BIT_SHIFT=0xd MASK_DFFF=0xffffdfff. Confidence: high.

### Token CIDs (unnamed tokens)
- asm/09_equip_lp_display.s lines 9785-9816: `setup_equip_oam_by_placeable_card_id_and_zone` BST comparing input card_id vs placeable card_id and mapping to result token card_id via pool literals.
  Function comment lists: RESULT_CARD_ID_TOKEN_A=0x13fb ... RESULT_CARD_ID_TOKEN_H=0x195a (all verified unnamed in card-stats). Confidence: high.

### STATUE_OF_THE_WICKED_CID (0x1543)
- asm/09_equip_lp_display.s line 9754: DWORD_08072f2c = 0x00001543; compared vs [r4+0] card_id in BST.
  Function comment: INPUT_CARD_ID_STATUE_OF_THE_WICKED=0x1543; card-stats line 14666 confirms. Confidence: high.

## C8 stale FUN_ scan

grep FUN_ in seg-5a (lines 9415-~11070):
- Line 11513: "FUN_08071d64" in plate comment of enqueue_spirit_zone_sprite_type11 (0x08074318) -- this fn is in Seg-5b, handled there
- No stale FUN_ in Seg-5a range functions themselves (lines 9415-~10760)

## C13 残留 100% 覆盖证明 (Seg-5a)

Total auto-name slots in Seg-5a [0x08072d20..0x08073a5c): 61

Classification union:
- EQ_SLOTS (REUSE): 38 slots -> DWORD_08072d58/d90/db8/dc0/df4/e5c/e60/e64/eb0/ee4/f1c/f20/f44/f58/fd0 + DAT_08072ff4/3040/3074/3090/30dc/3108/3120 + DWORD_080732f8/3380/3384/3388/33ac/33fc/3400/3474/34d8/34dc/34e0/3528/355c/3560/3564/3568 = 38 (37 pre-existing + DWORD_08073568 reusing EQUIP_CHAIN_BASE_OFF)
- EQ_SLOTS (NEW): 10 unique new constants -> DWORD_08072e68 (EQUIP_CHAIN_BASE_OFF), DWORD_08072f2c/f60/f68/f70/f78/f84/f8c/f94/fcc (9 CIDs/masks) + DWORD_08072fd0 (SPRITE_ATTR_CLR_BIT13) = 11 NEW-tagged rows in table; DWORD_08073568 is REUSE of EQUIP_CHAIN_BASE_OFF (counted in REUSE=38 above)
- REF_SLOTS: 10 slots -> DWORD_08072d8c/dbc/df0 + PTR_ x5 (PTR_gP1LifePoints_0807303c/3070/308c/30d8/311c) + DWORD_080732f4/0807337c = 10
- RENAME_SLOTS: 3 slots -> DAT_080731e4, DAT_08073628, DAT_08073900

48 EQ + 10 REF + 3 RENAME = 61. Coverage complete. No unclassified slots.

## 求助

None. All semantics confirmed with file:line evidence.
