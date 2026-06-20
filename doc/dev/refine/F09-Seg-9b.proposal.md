# Refine Proposal: F09-Seg-9b  [0x08077c50..0x0807850c)

## 段测绘
- 函数入口 x10 (push-prologue):
  - 0x08077c50  dispatch_equip_lp_row_with_neo_daedalus_gate
  - 0x08077d58  enqueue_position_sprites_for_both_players
  - 0x08077d80  submit_lp_indicator_by_slot_type_and_score
  - 0x08077e00  enqueue_equip_zone_sprite_by_state_and_equip_count
  - 0x08078004  dispatch_equip_zone_sprite_by_lp_state_with_ticker
  - 0x080780f0  enqueue_equip_type11_sprite_and_lp_bar_if_signature_match
  - 0x08078158  refresh_equip_slot_bitmap_from_zone_struct
  - 0x080781dc  invoke_equip_zone_bitmap_pair_if_spell_card_type
  - 0x0807822c  enumerate_equip_slots_for_sprite_bitmap_pair
  - 0x080784b4  scan_both_players_slots_for_equip_activation
- ROM_INCBIN 块 x4:
  - B6: 0x08077ecc / 0x5c  (fn_eligible stub)
  - B7: 0x08077f44 / 0xc0  (6 sub-stubs)
  - B8: 0x080782c0 / 0x2c  (fn_eligible stub)
  - B9: 0x08078368 / 0x14c (8 sub-stubs + default)
- 残留自动名槽 x36:
  - DWORD_08077cb4=0x0201b290, DWORD_08077cb8=0x0201c4e0, DWORD_08077cbc=0x00000868
  - DWORD_08077d2c=0x0201c4e0, DWORD_08077d30=0x00001da8, DWORD_08077d34=0x00000868
  - DWORD_08077dc8=0x0201bb90, DWORD_08077dfc=0x0201c4e0
  - DWORD_08077e90=0x00000868, DWORD_08077e94=0x0201c510, DWORD_08077e98=0x0201b290, DWORD_08077ec8=0x00001d78
  - PTR_DAT_08077f2c=dispatch_table_ptr (value=0x08077f44)
  - DAT_08077f44=B7 start
  - DWORD_08078020=0x0201b290, DWORD_08078050=0x0201e2a0, DWORD_08078054=0x0201c4e0
  - DWORD_0807808c=0x000004a4, DWORD_08078090=0x0201c4e0
  - DWORD_080780d0=0x000004a4, DWORD_080780d4=0x0201c4e0, DWORD_080780d8=0x00001da8
  - DWORD_08078144=0x00000868, DWORD_08078148=0x0201c5d8, DWORD_0807814c=0xbaf00000
  - DWORD_080781b8=0x0201bb90, DWORD_080781bc=0x00000868, DWORD_080781c0=0x0201c510
  - DWORD_08078218=0x00000868, DWORD_0807821c=0x0201c5d8, DWORD_08078220=0xbaf00000
  - DWORD_080782b4=0x00000868, DWORD_080782b8=0x0201c510, DWORD_080782bc=0x00000fa7
  - DAT_08078368=B9 start
  - DWORD_08078508=0x0201e1c8

## 数据块分类 (Rule 2/3) -- 每块 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| B6: 0x77ecc/0x5c | raw=0 thumb=1 @0x09e448d0 | R4 disasm (fn_eligible) | THUMB+1 in FS handler table 0x09e448c4; entry[+8]=CID=0x1738 (Dangerous Machine TYPE-6); first bytes 0x1c04b510=push{r4,lr}+adds r4,r0,#0 (valid THUMB prologue); B6+0x34=0x77f00 raw=6/thumb=2 are in 0x09c2xxxx (compressed pack asset region, not FS context) -- coincident raw/THUMB values in compressed data, not real code refs |
| B7: 0x77f44/0xc0 | raw=1 @0x08077f40 (table[5] of PTR_DAT_08077f2c); sub-entries: 0x77f56/6c/7a/86/9c raw=1 each | R4 disasm (sub-stubs) | Raw dispatch table PTR_DAT_08077f2c 6 entries, all pointing into B7; raw pointers (not THUMB+1); first bytes 0x07e078a4=code inside fn body (not new fn prologue at B7+0x00 itself -- B7 start is mid-function reachable via indirect table) |
| B8: 0x782c0/0x2c | raw=0 thumb=1 @0x09e41f18 | R4 disasm (fn_eligible) | THUMB+1 in FS handler table 0x09e41f0c; entry[+8]=CID=0x175c (Monster Gate); first bytes 0x4647b5f0=push{r4,r5,r6,r7,lr}+mov r7,r8 (valid THUMB prologue with high-reg save) |
| B9: 0x78368/0x14c | raw=1 @0x08078364 (table[30] of B8-dispatch-table, 31-entry table at 0x080782ec); sub-entries: 0x783a0/a8 raw=1 each, 0x78476 raw=1 @0x08078354 (entry[26]; ROM 0x08078354->0x08078476 confirmed), 0x7847c/8c/9e raw=1 each, 0x784a8 raw=24; B9+0xb4=0x0807841c thumb=1 @0x09f73fd6 (REJECT: 0x09f7xxxx compressed region; 0x0807841c is mid-BL, raw=0, NOT a dispatch entry) | R4 disasm (sub-stubs) | Raw dispatch table (31-entry at 0x080782ec..0x08078367); 8 unique targets including sub_8476; B9+0xb4 0x09f73fd6 is in compressed asset region (non-4B-aligned context garbage) -- not a real FS ref; raw dispatch drives classification |

**B6 compressed-region coincidence note**: 0x08077f00 has raw=6 refs in 0x09c2xxxx and thumb=2 refs in 0x09c26d9f/09c26f75 -- all in compressed pack data (0x09c2xxxx). These are data-byte coincidences inside pack assets, not real code pointers. The only true ref for B6 is the THUMB+1 @0x09e448d0 (FS handler table). B6 has a real FS ref.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All values verified by python read of ROM at slot address.

| slot | value | const_name | slot_label | reuse/new | evidence |
|---|---|---|---|---|---|
| DWORD_08077cb4 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_pool_7cb4 | REUSE | ewram.inc; 676 raw refs |
| DWORD_08077cb8 | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_7cb8 | REUSE | ewram.inc |
| DWORD_08077cbc | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_7cbc | REUSE | ewram.inc |
| DWORD_08077d2c | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_7d2c | REUSE | ewram.inc |
| DWORD_08077d30 | 0x1da8 | LP_CARD_TRACK_BASE_OFF | lp_card_track_base_pool_7d30 | REUSE | ewram.inc: LP_CARD_TRACK_BASE_OFF=0x00001da8; 109 raw ROM refs |
| DWORD_08077d34 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_7d34 | REUSE | ewram.inc |
| DWORD_08077dc8 | 0x0201bb90 | gEquipChainSlotRefs | gequip_chain_refs_pool_7dc8 | REUSE | ewram.inc: gEquipChainSlotRefs=0x0201bb90; 260 raw refs |
| DWORD_08077dfc | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_7dfc | REUSE | ewram.inc |
| DWORD_08077e90 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_7e90 | REUSE | ewram.inc |
| DWORD_08077e94 | 0x0201c510 | gDuelFieldSlots | gduel_field_slots_pool_7e94 | REUSE | ewram.inc |
| DWORD_08077e98 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_pool_7e98 | REUSE | ewram.inc |
| DWORD_08077ec8 | 0x1d78 | ACTIVATION_STATE_B_OFF | activation_state_b_pool_7ec8 | REUSE | duel_field.inc: ACTIVATION_STATE_B_OFF=0x00001d78; consumer asm/09 L20424 `ldr r4, DWORD_08077ec8`; `add r4,r8`; `ldrh r4,[r4,#0x0]`; reads gP1LifePoints[player*0x868+0x1d78] sprite data; conf: high |
| DWORD_08078020 | 0x0201b290 | gDuelPhaseFlags | gduel_phase_pool_8020 | REUSE | ewram.inc |
| DWORD_08078050 | 0x0201e2a0 | gDuelCardCtxBase | gduel_card_ctx_pool_8050 | REUSE | ewram.inc: gDuelCardCtxBase=0x0201e2a0; 442 raw refs |
| DWORD_08078054 | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_8054 | REUSE | ewram.inc |
| DWORD_0807808c | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_808c | REUSE | ewram.inc |
| DWORD_08078090 | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_8090 | REUSE | ewram.inc |
| DWORD_080780d0 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | equip_phase_frame_pool_80d0 | REUSE | ewram.inc |
| DWORD_080780d4 | 0x0201c4e0 | gP1LifePoints | gp1lp_pool_80d4 | REUSE | ewram.inc |
| DWORD_080780d8 | 0x1da8 | LP_CARD_TRACK_BASE_OFF | lp_card_track_base_pool_80d8 | REUSE | ewram.inc |
| DWORD_08078144 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_8144 | REUSE | ewram.inc |
| DWORD_08078148 | 0x0201c5d8 | gDuelFieldSlots_p2_base | gduel_slots_p2_base_pool_8148 | REUSE | ewram.inc: gDuelFieldSlots_p2_base=0x0201c5d8; 24 raw refs |
| DWORD_0807814c | 0xbaf00000 | SANCTUARY_CID_SHIFTED | sanctuary_cid_shifted_pool_814c | REUSE | card_info.inc: SANCTUARY_CID_SHIFTED=0xbaf00000 (SANCTUARY_IN_THE_SKY_CID(0x175e)<<19); consumer asm/09 L20640 `ldr r1, DWORD_0807814c`; `cmp r0,r1` where r0=slot_word<<0x13; conf: high |
| DWORD_080781b8 | 0x0201bb90 | gEquipChainSlotRefs | gequip_chain_refs_pool_81b8 | REUSE | ewram.inc |
| DWORD_080781bc | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_81bc | REUSE | ewram.inc |
| DWORD_080781c0 | 0x0201c510 | gDuelFieldSlots | gduel_field_slots_pool_81c0 | REUSE | ewram.inc |
| DWORD_08078218 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_8218 | REUSE | ewram.inc |
| DWORD_0807821c | 0x0201c5d8 | gDuelFieldSlots_p2_base | gduel_slots_p2_base_pool_821c | REUSE | ewram.inc |
| DWORD_08078220 | 0xbaf00000 | SANCTUARY_CID_SHIFTED | sanctuary_cid_shifted_pool_8220 | REUSE | card_info.inc |
| DWORD_080782b4 | 0x868 | PLAYER_BLOCK_STRIDE | player_block_stride_pool_82b4 | REUSE | ewram.inc |
| DWORD_080782b8 | 0x0201c510 | gDuelFieldSlots | gduel_field_slots_pool_82b8 | REUSE | ewram.inc |
| DWORD_080782bc | 0xfa7 | BLUE_EYES_WHITE_DRAGON_CID | blue_eyes_cid_pool_82bc | REUSE | card_info.inc: BLUE_EYES_WHITE_DRAGON_CID=0x00000fa7; consumer asm/09 L20829 `ldr r1, DWORD_080782bc`; `bl check_card_pair_allowed`; used as card_type upper bound / pair key; conf: high |
| DWORD_08078508 | 0x0201e1c8 | gEquipZoneCountTable | gequip_zone_cnt_pool_8508 | REUSE | ewram.inc: gEquipZoneCountTable=0x0201e1c8; 55 ROM refs |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label | evidence |
|---|---|---|---|---|
| PTR_DAT_08077f2c | 0x08077f44 (entry[0]) | dangerous_machine_dispatch_table_7f2c | PTR_DAT_08077f2c | 6-entry raw-ptr dispatch table (0x08077f44..0x08077f9c); referenced by .word 0x08077f2c @0x08077f28 (1 raw ref); raw dispatch from B6 fn_eligible via ldr+bx pattern |
| DAT_08077f44 | (B7 stub start) | dangerous_machine_dispatch_sub_stubs_7f44 | DAT_08077f44 | B7 sub-stubs block; entry[0] of PTR_DAT_08077f2c = 0x08077f44 (raw=1 @0x08077f3c) |
| DAT_08078368 | (B9 stub start) | monster_gate_dispatch_sub_stubs_8368 | DAT_08078368 | B9 sub-stubs block; entry[30] of 31-entry dispatch table at 0x080782ec = 0x08078368 (raw=1) |

### RENAME_SLOTS (纯改名 + EOL)

None required. The PTR_DAT_ and DAT_ slots above are fully handled via REF_SLOTS.

### FUNC_RENAME

No function name conflicts detected in Seg-9b. All 10 named functions have semantic consistency between plate/comments and body. No misname signals found.

### PLATE (R5)

No CJK mojibake found in Seg-9b line range (20068..20968). Zero non-ASCII chars confirmed by python scan.

No stale FUN_ references found in Seg-9b line range.

## disasm 计划 (R4)

### B6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc
- ROM_INCBIN 0x77ecc/0x5c
- FS THUMB+1 ref @0x09e448d0; entry @0x09e448c4; CID=0x1738 (DANGEROUS_MACHINE_TYPE6_CID, NEW)
- Prologue bytes: 0x1c04b510 = push{r4,lr} + adds r4,r0,#0 (confirmed THUMB)
- Literal pool at +0x1c (0x0201b290=gDuelPhaseFlags) and +0x54..+0x58 (0x0201c4e0=gP1LifePoints, 0x00001da8=LP_CARD_TRACK_BASE_OFF)
- Total: 3 DWord pools
- Action: clearListing 0x77ecc..0x77f27; setTMode; DisassembleCommand(0x77ecc); createFunction(0x77ecc, "fn_eligible_dangerous_machine_type6")
- Pool: force_dword(0x08077ee8) [gDuelPhaseFlags], force_dword(0x08077f18) [gP1LifePoints], force_dword(0x08077f1c) [LP_CARD_TRACK_BASE_OFF]

### B7: dangerous_machine sub-stubs @ 0x08077f44..0x08078003
- ROM_INCBIN 0x77f44/0xc0
- Raw dispatch table PTR_DAT_08077f2c (6 entries): 0x77f44, 0x77f56, 0x77f6c, 0x77f7a, 0x77f86, 0x77f9c
- Literal pool words:
  - B7+0x50 = 0x08077f94: ROM value = 0x0000e033 (CODE -- a `b` branch instruction inside sub_7f86 body; NOT a pool word; do NOT force_dword(0x08077f94))
  - B7+0x88 = 0x08077fcc: ROM value = 0x080507ad (fn_ptr to code outside Seg-9; this is the correct pool word bearing 0x080507ad; force_dword(0x08077fcc) is the correct action)
  - B7+0xac..+0xb4 = 0x08077ff0..0x08077ff8: (0x0201c4e0=gP1LifePoints, 0x00001d68, 0x00001d6c)
- GUARD: Ghidra script must NOT call force_dword(0x08077f94) -- that address is CODE (branch 0xe033 inside sub_7f86); only force_dword(0x08077fcc) for the 0x080507ad fn_ptr pool word
- Action: clearListing 0x77f44..0x78003; setTMode; DisassembleCommand per entry (6 calls)
- Labels: sub_7f44, sub_7f56, sub_7f6c, sub_7f7a, sub_7f86, sub_7f9c (or last may be default_7f9c)
- Pool pass: force_dword for pool words at +0x88(0x77fcc)/+0xac(0x77ff0)/+0xb0(0x77ff4)/+0xb4(0x77ff8); NOT +0x50(0x77f94)

### B8: fn_eligible_monster_gate @ 0x080782c0
- ROM_INCBIN 0x782c0/0x2c
- FS THUMB+1 ref @0x09e41f18; entry @0x09e41f0c; CID=0x175c (MONSTER_GATE_CID, NEW)
- Prologue bytes: 0x4647b5f0 = push{r4,r5,r6,r7,lr} + mov r7,r8 (THUMB with high-reg save; b5f0=push, 4647=mov r7,r8)
- Literal pool at +0x24..+0x28 (0x0201b290=gDuelPhaseFlags, 0x080782ec=dispatch_table_ptr)
- Action: clearListing 0x782c0..0x782eb; setTMode; DisassembleCommand(0x782c0); createFunction(0x782c0, "fn_eligible_monster_gate")
- Pool: force_dword(0x080782e4) [gDuelPhaseFlags], force_dword(0x080782e8) [dispatch_table_label]
- Note: 0x080782ec is the dispatch table start (31-entry table at 0x080782ec..0x08078367 already structured as .word entries)

### B9: monster_gate sub-stubs @ 0x08078368..0x080784b3
- ROM_INCBIN 0x78368/0x14c
- Raw dispatch table (31-entry at 0x080782ec..0x08078367); 8 unique entry points:
  - entry[30]=0x08078368 (raw=1 @0x08078364)
  - entry[28]=0x080783a0 (raw=1 @0x0807835c)
  - entry[27]=0x080783a8 (raw=1 @0x08078358)
  - entry[26]=0x08078476 (raw=1 @0x08078354) -- ROM confirmed: 0x08078354->0x08078476; decodes BL 0x0804a870; b 0x080784a8 (6 bytes 0x78476..0x7847b)
  - entry[2] =0x0807847c (raw=1 @0x080782f4)
  - entry[1] =0x0807848c (raw=1 @0x080782f0)
  - entry[0] =0x0807849e (raw=1 @0x080782ec)
  - entries[3..25,29]=0x080784a8 (raw=24, default)
- NOTE: 0x0807841c (B9+0xb4) is NOT a dispatch target: 0x0807841a=0xf7bb (BL-hi), 0x0807841c=0xf8cd (BL-lo) -- mid-BL; THUMB+1 @0x09f73fd6 is in 0x09f7xxxx compressed region (REJECT); raw=0; DisassembleCommand(0x0807841c) would corrupt sub_83a8 body; EXCLUDED
- Action: clearListing 0x78368..0x784b3; setTMode; DisassembleCommand per entry (8 calls = 7 unique non-default + 1 default)
  - DisassembleCommand(0x08078368)  # sub_8368
  - DisassembleCommand(0x080783a0)  # sub_83a0
  - DisassembleCommand(0x080783a8)  # sub_83a8
  - DisassembleCommand(0x08078476)  # sub_8476 (BL 0x0804a870; b 0x080784a8)
  - DisassembleCommand(0x0807847c)  # sub_847c
  - DisassembleCommand(0x0807848c)  # sub_848c
  - DisassembleCommand(0x0807849e)  # sub_849e
  - DisassembleCommand(0x080784a8)  # default_84a8
- Labels: sub_8368, sub_83a0, sub_83a8, sub_8476, sub_847c, sub_848c, sub_849e, default_84a8
- Pool pass: force_dword for DWord pools at 0x7838e+0x2c (0x0201c4e0) and 0x783ec (0x00000868) and others in body
- Zero-residue proof: 8 DisassembleCommand targets cover all unique dispatch entries; 0x78476..0x7847b (6 bytes sub_8476) now explicitly disassembled; no ROM_INCBIN gap between sub_83a8 (ends at 0x78476) and sub_8476 (starts at 0x78476); post-landing ROM_INCBIN in B9 = 0

## carve 計画 (R7)

None required. The 31-entry dispatch table at 0x080782ec..0x08078367 is already structured as .word entries in asm (lines 20877..20907). Only needs label renaming for DAT_08078368 via REF_SLOTS above.

## 新增 constants / 全局

constants/card_info.inc -- 2 NEW:
- DANGEROUS_MACHINE_TYPE6_CID = 0x00001738  @ Dangerous Machine TYPE-6 (pw=76895648; card-stats.s L19607 card_1507 slot=0x1738); fn_eligible_dangerous_machine_type6 dispatch gate; C5 grep 0x1738 in constants/: 0 hits (rom_data.inc has card_07E3=0x09821738 -- ROM address not CID, distinct domain)
- MONSTER_GATE_CID = 0x0000175c  @ Monster Gate (pw=43040603; card-stats.s L20076 card_1543 slot=0x175C); fn_eligible_monster_gate FS dispatch stub; C5 grep 0x175c in constants/: 0 hits

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 4 ROM_INCBIN blocks have confirmed refs:
- B6: THUMB+1 in FS handler table @0x09e448d0 (conf: high); compressed-region raw/THUMB hits at 0x09c2xxxx are data coincidences, not code refs
- B7: raw ptrs in dispatch table PTR_DAT_08077f2c (conf: high)
- B8: THUMB+1 in FS handler table @0x09e41f18 (conf: high)
- B9: raw ptr in 31-entry dispatch table entry[30]=0x08078368 (conf: high)

## 消費者証拠 (R6) -- 关键槽语义 file:line + 置信度

| slot | value | consumer | file:line | confidence |
|---|---|---|---|---|
| DWORD_08077ec8=0x1d78 | ACTIVATION_STATE_B_OFF | enqueue_equip_zone_sprite_by_state_and_equip_count | asm/09 L20424 `ldr r4, DWORD_08077ec8`; `add r4,r8`; `ldrh r4,[r4,#0x0]`; reads [r8+0x1d78] where r8=gP1LifePoints; duel_field.inc ACTIVATION_STATE_B_OFF=0x1d78 | high |
| DWORD_0807814c=0xbaf00000 | SANCTUARY_CID_SHIFTED | enqueue_equip_type11_sprite_and_lp_bar_if_signature_match | asm/09 L20640-L20641 `ldr r1, DWORD_0807814c`; `cmp r0,r1` where r0=slot_word<<0x13; card_info.inc SANCTUARY_CID_SHIFTED=0xbaf00000=(0x175e<<19) sentinel | high |
| DWORD_080782bc=0xfa7 | BLUE_EYES_WHITE_DRAGON_CID | enumerate_equip_slots_for_sprite_bitmap_pair | asm/09 L20829 `ldr r1, DWORD_080782bc`; `bl check_card_pair_allowed` r0=card_id,r1=0xfa7; card_info.inc BLUE_EYES_WHITE_DRAGON_CID=0x00000fa7; used as card type pairing upper-bound key | high |
| DWORD_08078050=0x0201e2a0 | gDuelCardCtxBase | dispatch_equip_zone_sprite_by_lp_state_with_ticker | asm/09 L20494 `ldr r0, DWORD_08078050`; reads [0x0201e2a0+player*4+8]; ewram.inc gDuelCardCtxBase | high |
| DWORD_08077dc8=0x0201bb90 | gEquipChainSlotRefs | submit_lp_indicator_by_slot_type_and_score | asm/09 L20277 `ldr r3, DWORD_08077dc8`; `ldr r0,[r3,#0x38]`; accesses equip chain slot reference struct; ewram.inc gEquipChainSlotRefs | high |

## C13 残留 100% 覆盖证明 (Seg-9b)

Python exhaustive scan confirmed 36 unique auto-name slots in [0x08077c50, 0x0807850c).

分類并集:
- EQ_SLOTS: 33 slots (all DWORD_ entries in EQ table above = 33)
- REF_SLOTS: 3 slots (PTR_DAT_08077f2c + DAT_08077f44 + DAT_08078368)
- RENAME_SLOTS: 0

Total: 33 + 3 = 36. Matches python count.

No slots unclassified. Union coverage = 36/36 = 100%.

disasm zero-residue post-landing (corrected B9 plan):
- B6: 1 DisassembleCommand(0x08077ecc) -> fn_eligible_dangerous_machine_type6; 0 ROM_INCBIN residue
- B7: 6 DisassembleCommand (sub_7f44/56/6c/7a/86/9c); pool force_dword at 0x77fcc/0x77ff0/0x77ff4/0x77ff8 (NOT 0x77f94); 0 ROM_INCBIN residue
- B8: 1 DisassembleCommand(0x080782c0) -> fn_eligible_monster_gate; 0 ROM_INCBIN residue
- B9: 8 DisassembleCommand (sub_8368/83a0/83a8/8476/847c/848c/849e/default_84a8); sub_8476 covers 0x78476..0x7847b (6 bytes) previously missing; 0x0807841c excluded (mid-BL, not a valid entry); 0 ROM_INCBIN residue
- Total post-landing: 0 ROM_INCBIN + 0 .byte-code in [0x08077c50, 0x0807850c)

## 求助

None. All semantics derived from direct code evidence at high confidence.
