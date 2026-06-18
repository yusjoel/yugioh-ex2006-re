# Refine Proposal: F09-Seg-9a  [0x0807738c..0x08077c50)

## 段测绘
- 函数入口 x9 (push-prologue):
  - 0x0807738c  invoke_setup_equip_oam_if_neo_daedalus_zone_f
  - 0x08077414  dispatch_equip_lp_bar_display_by_state
  - 0x080774f4  route_equip_partner_setup_by_lp_state
  - 0x08077538  submit_equip_bitmap_and_lp_indicator_by_slot
  - 0x08077678  render_equip_pair_zone_sprites_by_card_match
  - 0x080777b0  refresh_equip_bitmap_if_zone_flag_clear
  - 0x080777d8  dispatch_equip_slot_eligible_count_by_lp_state
  - 0x08077920  check_equip_activation_by_special_card_id
  - 0x080779bc  check_equip_target_by_chain_then_bitmap
- ROM_INCBIN 块 x5:
  - B1: 0x0807757c / 0x2c  (fn_eligible stub)
  - B2: 0x080775d0 / 0xa8  (9 sub-stubs)
  - B3: 0x080779e4 / 0x30  (fn_eligible stub)
  - B4: 0x08077a3c / 0x120 (9 sub-stubs)
  - B5: 0x08077b88 / 0xc8  (sub-stubs; ends exactly at boundary 0x08077c50)
- 残留自动名槽 x31:
  - DAT_0807740c=0x00000868, DAT_08077410=0x0201cab0
  - DAT_0807744c=0x00001ce8, DAT_08077450=0x0201b290, DAT_08077454=0x000004a4
  - DAT_080774ac=0x00000868
  - DWORD_08077524=0x0201b290
  - DWORD_08077578=0x00000bb8
  - PTR_DAT_080775ac=dispatch_table_ptr (value=0x08077648)
  - DAT_080775d0=0x08077648 (B2 start)
  - DWORD_080777a0=0x0201e1c8, DWORD_080777a4=0x00000868
  - DWORD_080777a8=0x0201c4ec, DWORD_080777ac=0x0201c600
  - DWORD_080777f8=0x0201b290
  - DWORD_08077848=0x000004a4
  - DWORD_0807788c=0x0201c4e0, DWORD_08077890=0x00000868, DWORD_08077894=0x000004a4
  - DWORD_080778e0=0x0201c4e0, DWORD_080778e4=0x00000868, DWORD_080778e8=0x000004a4
  - DWORD_0807791c=0x000004a4
  - DWORD_0807794c=0x00001703, DWORD_08077960=0x00001749, DWORD_08077964=0x00001866
  - DWORD_080779b4=0x00000868, DWORD_080779b8=0x0201c510
  - PTR_DAT_08077a18=dispatch_table_ptr (value=0x08077b00)
  - DAT_08077a3c=B4 start
  - DAT_08077b88=B5 start

## 数据块分类 (Rule 2/3) -- 每块 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| B1: 0x7757c/0x2c | raw=0 thumb=1 @0x09e41ca8 | R4 disasm (fn_eligible) | THUMB+1 in FS handler table 0x09e41c9c; entry[+8]=CID=0x16df (Spatial Collapse); first bytes 0x1c04b530=push{r4,r5,lr}+adds r4,r0,#0 (valid THUMB prologue) |
| B2: 0x775d0/0xa8 | raw=1 @0x080775cc (table[8]); sub-entries: 0x775ec raw=1,0x77648 raw=1,0x77670 raw=4 | R4 disasm (sub-stubs) | Raw pointers in PTR_DAT_080775ac 9-entry dispatch table (raw not THUMB+1); sub-stubs dispatched via MOV PC,r0/ldr+bx pattern from B1; first byte 0x1850 = inner code |
| B3: 0x779e4/0x30 | raw=0 thumb=1 @0x09e41d68 | R4 disasm (fn_eligible) | THUMB+1 in FS handler table 0x09e41d5c; entry[+8]=CID=0x1712 (Dimension Fusion); first bytes 0x1c05b570=push{r4,r5,r6,lr}+adds r5,r0,#0 (valid THUMB prologue) |
| B4: 0x77a3c/0x120 | raw=1 @0x08077a38 (table[8]); sub-entries: 0x77a70/0x77ab4/0x77ac2/0x77b00 raw=1 each,0x77b2c raw=4; B4+0xf8=0x77b34 thumb=1 @0x09e41de0 | R4 disasm (sub-stubs + fn_eligible embedded) | Raw dispatch table PTR_DAT_08077a18 (9 entries); B4+0xf8 is an embedded fn_eligible stub (CID=0x1717 Jade Insect Whistle via FS table 0x09e41dd4; THUMB+1 ref); distinct sub-stub entries at +0x00,+0x34,+0x78,+0x86,+0xc4,+0xf0 |
| B5: 0x77b88/0xc8 | raw=1 @0x08077b84 (table last entry from after B4); sub-entries: 0x77bb6/0x77c18/0x77c2c/0x77c3a raw=1 each,0x77c48 raw=6; B5+0x18=0x77ba0 thumb=1 @0x09f836e3 (REJECT: 0x09f8xxxx compressed region, not FS table) | R4 disasm (sub-stubs) | Raw dispatch table preceding B5 (entries at 0x08077b5c..0x08077b87 pointing into B5); 0x09f836e3 is compressed asset region (non-FS context, non-4B-aligned context garbage) -- 0 valid THUMB+1 refs; raw dispatch drives classification |

**B5 boundary note**: B5 ends exactly at 0x08077c50 = Seg-9a boundary. Block is entirely within Seg-9a.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All values verified by python read of ROM at slot address.

| slot | value | const_name | slot_label | reuse/new | evidence |
|---|---|---|---|---|---|
| DAT_0807740c | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_740c | REUSE | ewram.inc; 2146 raw refs |
| DAT_08077410 | 0x0201cab0 | gP1AltHandSlotArray | gP1AltHandSlotArray_pool_7410 | REUSE | ewram.inc; 15 ROM refs |
| DAT_0807744c | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_pool_744c | REUSE | ewram.inc; 184 ROM refs |
| DAT_08077450 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_7450 | REUSE | ewram.inc; 676 raw refs |
| DAT_08077454 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_7454 | REUSE | ewram.inc; 241 ROM refs |
| DAT_080774ac | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_74ac | REUSE | ewram.inc |
| DWORD_08077524 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_7524 | REUSE | ewram.inc |
| DWORD_08077578 | 0xbb8 | CARD_STAT_LP_THRESHOLD | lp_threshold_pool_7578 | REUSE | card_info.inc: CARD_STAT_LP_THRESHOLD=0x00000bb8; "3000 LP threshold for card stat display branch" |
| DWORD_080777a0 | 0x0201e1c8 | gEquipZoneCountTable | gEquipZoneCountTable_pool_77a0 | REUSE | ewram.inc; 55 ROM refs |
| DWORD_080777a4 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_77a4 | REUSE | ewram.inc |
| DWORD_080777a8 | 0x0201c4ec | gP1ZoneHandCount | gP1ZoneHandCount_pool_77a8 | REUSE | ewram.inc; 23 ROM refs |
| DWORD_080777ac | 0x0201c600 | gP1FieldArrayCBase | gP1FieldArrayCBase_pool_77ac | REUSE | ewram.inc; 115 raw refs |
| DWORD_080777f8 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_pool_77f8 | REUSE | ewram.inc |
| DWORD_08077848 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_7848 | REUSE | ewram.inc |
| DWORD_0807788c | 0x0201c4e0 | gP1LifePoints | gP1LifePoints_pool_788c | REUSE | ewram.inc |
| DWORD_08077890 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_7890 | REUSE | ewram.inc |
| DWORD_08077894 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_7894 | REUSE | ewram.inc |
| DWORD_080778e0 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints_pool_78e0 | REUSE | ewram.inc |
| DWORD_080778e4 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_78e4 | REUSE | ewram.inc |
| DWORD_080778e8 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_78e8 | REUSE | ewram.inc |
| DWORD_0807791c | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_791c | REUSE | ewram.inc |
| DWORD_0807794c | 0x1703 | PRICKLE_FAIRY_CID | prickle_fairy_cid_pool_794c | REUSE | card_info.inc: PRICKLE_FAIRY_CID=0x00001703; asm/09 check_equip_activation_by_special_card_id: ldr r0,DWORD_0807794c; cmp r1,r0; beq LAB_08077980 (zone11 path) |
| DWORD_08077960 | 0x1749 | LEGENDARY_JUJITSU_MASTER_CID | legendary_jujitsu_master_cid_pool_7960 | NEW | card-stats.s line 19827: card_1524 Legendary Jujitsu Master slot=0x1749 pw=25773409; C5 grep 0x1749 in constants/: 0 hits |
| DWORD_08077964 | 0x1866 | KANGAROO_CHAMP_CID | kangaroo_champ_cid_pool_7964 | NEW | card-stats.s line 22986: card_1767 Kangaroo Champ slot=0x1866 pw=95789089; C5 grep 0x1866 in constants/: 0 hits |
| DWORD_080779b4 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_79b4 | REUSE | ewram.inc |
| DWORD_080779b8 | 0x0201c510 | gDuelFieldSlots | gDuelFieldSlots_pool_79b8 | REUSE | ewram.inc |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label | evidence |
|---|---|---|---|---|
| PTR_DAT_080775ac | 0x08077648 (entry[0]) | spatial_collapse_dispatch_table_75ac | PTR_DAT_080775ac | 9-entry raw-ptr dispatch table; entry[8]=0x080775d0=B2 start; referenced by .word 0x080775ac @0x080775a8 (1 raw ref); raw dispatch from MOV PC / ldr+bx inside B1 fn_eligible |
| PTR_DAT_08077a18 | 0x08077b00 (entry[0]) | jade_insect_dispatch_table_7a18 | PTR_DAT_08077a18 | 9-entry raw-ptr dispatch table; entry[8]=0x08077a3c=B4 start; referenced by .word 0x08077a18 @0x08077a14 (1 raw ref); same dispatch pattern |
| DAT_080775d0 | (B2 stub start) | spatial_collapse_dispatch_sub_stubs_75d0 | DAT_080775d0 | B2 sub-stubs block; entry[8] of PTR_DAT_080775ac = 0x080775d0 |
| DAT_08077a3c | (B4 stub start) | jade_insect_dispatch_sub_stubs_7a3c | DAT_08077a3c | B4 sub-stubs block; entry[8] of PTR_DAT_08077a18 = 0x08077a3c; also B4+0xf8=fn_eligible_jade_insect_whistle_7b34 (THUMB+1 in FS table) |
| DAT_08077b88 | (B5 stub start) | dimension_fusion_dispatch_sub_stubs_7b88 | DAT_08077b88 | B5 sub-stubs block; last entry of B4-trailing dispatch table at 0x08077b84 = 0x08077b88 (1 raw ref) |

### RENAME_SLOTS (纯改名 + EOL)

None in Seg-9a -- the PTR_DAT_ and DAT_ above are all handled via REF_SLOTS rename.

### FUNC_RENAME

No function name conflicts detected in Seg-9a. All 9 named functions have semantic consistency between plate and body (verified by reading function bodies).

### PLATE (R5)

No CJK mojibake found in Seg-9a line range (19213..20068). Zero non-ASCII chars confirmed by python scan.

No stale FUN_ references found in Seg-9a line range.

## disasm 计划 (R4)

### B1: fn_eligible_spatial_collapse @ 0x0807757c
- ROM_INCBIN 0x7757c/0x2c
- FS THUMB+1 ref @0x09e41ca8; entry @0x09e41c9c; CID=0x16df (SPATIAL_COLLAPSE_CARD_ID, REUSE)
- Prologue bytes: 0x1c04b530 = push{r4,r5,lr} + adds r4,r0,#0 (confirmed THUMB)
- Literal pool at +0x24..+0x28 (2 DWords: 0x0201b290=gDuelPhaseFlags, 0x000004a4=EQUIP_PHASE_FRAME_OFF)
- Action: clearListing 0x7757c..0x757a7; setTMode; DisassembleCommand(0x7757c); createFunction(0x7757c, "fn_eligible_spatial_collapse")
- Pool: force_dword(0x08077594) [gDuelPhaseFlags], force_dword(0x08077598) [EQUIP_PHASE_FRAME_OFF]

### B2: spatial_collapse sub-stubs @ 0x080775d0..0x08077677
- ROM_INCBIN 0x775d0/0xa8
- Raw dispatch table PTR_DAT_080775ac 9 entries; entry addresses target into B2
- 9 unique entry points: 0x080775d0, 0x080775ec, 0x08077602, 0x0807762a, 0x08077648, 0x08077670 (appears 4x in table)
- Action: clearListing 0x775d0..0x77677; setTMode; DisassembleCommand per stub entry (6 calls for unique addresses)
- Labels: sub_75d0, sub_75ec, sub_7602, sub_762a, sub_7648, default_7670
- Likely contains inline literal pools -- apply force_dword pass after disasm

### B3: fn_eligible_dimension_fusion @ 0x080779e4
- ROM_INCBIN 0x779e4/0x30
- FS THUMB+1 ref @0x09e41d68; entry @0x09e41d5c; CID=0x1712 (DIMENSION_FUSION_CID, REUSE; card_info.inc already present)
- Prologue bytes: 0x1c05b570 = push{r4,r5,r6,lr} + adds r5,r0,#0 (confirmed THUMB)
- Literal pool at +0x28..+0x2c (2 DWords: 0x0201b290=gDuelPhaseFlags, 0x000004a4=EQUIP_PHASE_FRAME_OFF)
- Action: clearListing 0x779e4..0x77a13; setTMode; DisassembleCommand(0x779e4); createFunction(0x779e4, "fn_eligible_dimension_fusion")
- Pool: force_dword(0x08077a0c) [gDuelPhaseFlags], force_dword(0x08077a10) [EQUIP_PHASE_FRAME_OFF]

### B4: jade_insect_dispatch sub-stubs + embedded fn_eligible @ 0x08077a3c..0x08077b57
- ROM_INCBIN 0x77a3c/0x120
- Raw dispatch table PTR_DAT_08077a18 (9 entries); 6 unique sub-stub entries: 0x77a3c, 0x77a70, 0x77ab4, 0x77ac2, 0x77b00, 0x77b2c
- Embedded fn_eligible at B4+0xf8=0x08077b34 (FS THUMB+1 @0x09e41de0; CID=0x1717 Jade Insect Whistle, NEW)
- Action: clearListing 0x77a3c..0x77b57; setTMode; DisassembleCommand per sub-stub entry (6 calls) + DisassembleCommand(0x77b34); createFunction(0x77b34, "fn_eligible_jade_insect_whistle")
- Pool: inline pools likely at multiple points; apply force_dword pass for each 4B-aligned pool DWord
- Labels: sub_7a3c, sub_7a70, sub_7ab4, sub_7ac2, sub_7b00, sub_7b2c (or default_7b2c), fn_eligible_jade_insect_7b34
- Note: B4+0xf8 is fn_eligible embedded inside sub-stubs block (same ROM_INCBIN range); handle in same disasm pass

### B5: dimension_fusion sub-stubs @ 0x08077b88..0x08077c4f
- ROM_INCBIN 0x77b88/0xc8
- Raw dispatch table entries preceding B5 (0x08077b5c..0x08077b87 trailing B4 block); entry [last]=0x08077b88
- 6 unique entry points from entries at 0x77b5c table: 0x77b88, 0x77bb6, 0x77c18, 0x77c2c, 0x77c3a, 0x77c48
- B5+0x18=0x08077ba0 THUMB+1 ref @0x09f836e3 is in compressed region (0x09f8xxxx) -- NOT a valid FS ref; not a fn_eligible block; classify as sub-stub
- Action: clearListing 0x77b88..0x77c4f; setTMode; DisassembleCommand per entry (6 calls)
- Labels: sub_7b88, sub_7bb6, sub_7c18, sub_7c2c, sub_7c3a, default_7c48
- Pool: apply force_dword pass after disasm

## carve 计划 (R7)

None required. No raw-data structures warranting carve into rom.s. The dispatch tables preceding B2 (PTR_DAT_080775ac) and B4 (PTR_DAT_08077a18) are already structured as .word entries in the asm; they only need label renaming via REF_SLOTS above.

## 新增 constants / 全局

constants/card_info.inc -- 2 NEW:
- LEGENDARY_JUJITSU_MASTER_CID = 0x00001749  @ Legendary Jujitsu Master (pw=25773409; card-stats.s L19827 card_1524); check_equip_activation_by_special_card_id zone13 test path; C5 grep 0x1749 in constants/: 0 hits
- KANGAROO_CHAMP_CID = 0x00001866  @ Kangaroo Champ (pw=95789089; card-stats.s L22986 card_1767); check_equip_activation_by_special_card_id activation check path; C5 grep 0x1866 in constants/: 0 hits

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 5 ROM_INCBIN blocks have confirmed refs:
- B1: THUMB+1 in FS handler table (conf: high)
- B2: raw ptrs in dispatch table PTR_DAT_080775ac (conf: high)
- B3: THUMB+1 in FS handler table (conf: high)
- B4: raw ptrs in dispatch table PTR_DAT_08077a18 + embedded THUMB+1 fn_eligible ref (conf: high)
- B5: raw ptr in trailing dispatch table (0x08077b84 entry; conf: high)

## 消费者证据 (R6) -- 关键槽语义 file:line + 置信度

| slot | value | consumer | file:line | confidence |
|---|---|---|---|---|
| DAT_0807740c=0x868 | PLAYER_BLOCK_STRIDE | invoke_setup_equip_oam_if_neo_daedalus_zone_f | asm/09 L19237 `ldr r2, player_block_stride_pool_737c` (prior pool; same constant) | high |
| DAT_08077410=0x0201cab0 | gP1AltHandSlotArray | invoke_setup_equip_oam_if_neo_daedalus_zone_f | asm/09 L19239 `ldr r0, gP1AltHandSlotArray_pool_7380` (adjacent prior pool); ewram.inc | high |
| DAT_0807744c=0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | dispatch_equip_lp_bar_display_by_state | asm/09 L19373 `ldr r0, DAT_0807744c` then `adds r1,r3,r0` (gP1LifePoints+0x1ce8 offset) | high |
| DAT_08077450=0x0201b290 | gDuelPhaseFlags | dispatch_equip_lp_bar_display_by_state | asm/09 L19375 `ldr r0, DAT_08077450` | high |
| DAT_08077454=0x4a4 | EQUIP_PHASE_FRAME_OFF | dispatch_equip_lp_bar_display_by_state | asm/09 L19376 `ldr r4, DAT_08077454` then `adds r2,r0,r4` -> state_base+0x4a4 | high |
| DWORD_08077578=0xbb8 | CARD_STAT_LP_THRESHOLD | submit_equip_bitmap_and_lp_indicator_by_slot | asm/09 L19560 `ldr r2, DWORD_08077578`; passed as r2 to submit_lp_indicator_with_slot_xor_flag; 0xbb8=3000 LP threshold | high |
| DWORD_0807794c=0x1703 | PRICKLE_FAIRY_CID | check_equip_activation_by_special_card_id | asm/09 L19979 `ldr r0, DWORD_0807794c`; `cmp r1,r0`; beq LAB_08077980 (zone11 test path); PRICKLE_FAIRY_CID already in card_info.inc | high |
| DWORD_08077960=0x1749 | LEGENDARY_JUJITSU_MASTER_CID | check_equip_activation_by_special_card_id | asm/09 L19991 `ldr r0, DWORD_08077960`; `cmp r1,r0`; beq LAB_08077974 (zone13 path); card-stats.s L19827 Legendary Jujitsu Master slot=0x1749 | high |
| DWORD_08077964=0x1866 | KANGAROO_CHAMP_CID | check_equip_activation_by_special_card_id | asm/09 L19994 `ldr r0, DWORD_08077964`; `cmp r1,r0`; beq LAB_08077980 (activation path); card-stats.s L22986 Kangaroo Champ slot=0x1866 | high |

## C13 残留 100% 覆盖证明 (Seg-9a)

Python exhaustive scan confirmed 31 unique auto-name slots in [0x0807738c, 0x08077c50).

分类并集:
- EQ_SLOTS: 27 slots (DAT_0807740c/10/4c/50/54/ac, DWORD_08077524/578/77a0/a4/a8/ac/7f8/848/88c/890/894/8e0/8e4/8e8/91c/94c/960/964/9b4/9b8 = 27)
- REF_SLOTS: 4 slots (PTR_DAT_080775ac, PTR_DAT_08077a18, DAT_080775d0, DAT_08077a3c)
- RENAME_SLOTS: 0
- disasm内嵌 (DAT_08077b88 -> REF_SLOTS category): already counted above

Wait -- DAT_08077b88 is in REF_SLOTS. Let me recount:
- REF_SLOTS actual: PTR_DAT_080775ac + DAT_080775d0 + PTR_DAT_08077a18 + DAT_08077a3c + DAT_08077b88 = 5 slots
- EQ_SLOTS: 31 - 5 = 26 slots

Recount EQ_SLOTS (all non-REF slots):
DAT_0807740c, DAT_08077410, DAT_0807744c, DAT_08077450, DAT_08077454, DAT_080774ac (6)
DWORD_08077524, DWORD_08077578 (2)
DWORD_080777a0, DWORD_080777a4, DWORD_080777a8, DWORD_080777ac (4)
DWORD_080777f8 (1)
DWORD_08077848, DWORD_0807788c, DWORD_08077890, DWORD_08077894 (4)
DWORD_080778e0, DWORD_080778e4, DWORD_080778e8, DWORD_0807791c (4)
DWORD_0807794c, DWORD_08077960, DWORD_08077964 (3)
DWORD_080779b4, DWORD_080779b8 (2)
Total EQ: 26

REF: PTR_DAT_080775ac, DAT_080775d0, PTR_DAT_08077a18, DAT_08077a3c, DAT_08077b88 = 5

Total: 26 + 5 = 31. Matches python count.

No slots unclassified. Union coverage = 31/31 = 100%.

## 求助

None. All semantics derived from direct code evidence at high confidence.
