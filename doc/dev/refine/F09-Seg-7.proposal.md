# Refine Proposal: F09-Seg-7  [0x080752cc..0x0807629c)

file 09 Seg-7

---

## 段测绘

- 段范围: `[0x080752cc, 0x0807629c)` (asm lines 14656..16265)
- 函数入口: 19 个

| addr | name | asm line |
|------|------|----------|
| 0x080752cc | enqueue_effect_card_sprite_dual_with_negated | 14656 |
| 0x08075328 | init_effect_slot_display_if_opponent_lp_active | 14720 |
| 0x080754b8 | enqueue_effect_slot_sprites_all_players | 14804 |
| 0x08075530 | check_equip_slot_placement_via_neo_daedalus | 14877 |
| 0x080755dc | check_equip_slot_placement_via_target_bitmap | 14972 |
| 0x08075668 | enqueue_equip_zone_sprite_with_slot_setup | 15058 |
| 0x080757f0 | invoke_equip_oam_for_zone_type_e_slot | 15262 |
| 0x08075874 | invoke_equip_oam_for_hand_set_code_slot | 15336 |
| 0x080758f0 | tick_equip_zone_display_seq_by_type_code | 15405 |
| 0x08075a7c | enqueue_graveyard_spell_for_hand_set_code | 15623 |
| 0x08075ac0 | tick_graveyard_spell_display_by_state | 15671 |
| 0x08075b44 | enqueue_effect_slot_sprite_mode2_and_type11 | 15747 |
| 0x08075ba4 | dispatch_effect_activation_with_lp_counter | 15807 |
| 0x08075c40 | set_field_bit_by_slot_match_equip_dir | 15898 |
| 0x08075cb0 | invoke_equip_zone_lp_shape_with_lp_counter | 15966 |
| 0x08075f70 | enqueue_effect_node_sprite_type11_from_slot | 16030 |
| 0x0807615c | enqueue_effect_slot_sprite_with_score_sum | 16070 |
| 0x080761e8 | dispatch_zone13_equip_display_by_type_code | 16150 |
| 0x08076214 | tick_effect_display_by_state_and_type_code | 16190 |

- 残留自动名槽: 46 (19 DWORD_ + 27 DAT_)
- ROM_INCBIN 块: 6 (B1..B6)
- switchD: 0 (Seg-7 无 switchD)

---

## 数据块分类 (Rule 2/3) -- 每块 ref-scan 证据

### ref-scan 方法

```python
import struct
rom = open("roms/2343.gba","rb").read()
GBA_BASE = 0x08000000
for off, sz in [(0x75378,0x28),(0x75414,0xa4),(0x75d0c,0x2c),(0x75d5c,0x214),(0x75f8e,0x2e),(0x75fe0,0x17c)]:
    gba = GBA_BASE + off
    print(hex(gba), "raw=", rom.count(struct.pack("<I",gba)), "thumb=", rom.count(struct.pack("<I",gba|1)))
```

| 块 | GBA addr | sz | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|----|----------|----|--------------------------|------|------|
| B1 | 0x08075378 | 0x28 | raw=0 thumb=1 | R4 disasm (fn_eligible) | FS handler table at 0x09e41678 holds THUMB+1=0x08075379; entry CID at fn_ptr-4=0x09e41674=0x00001629 (Emblem of Dragon Destroyer); contains literal pool word 0x080753a0 (dispatch table for B2) |
| B2 | 0x08075414 | 0xa4 | raw=1 thumb=0 | R4 disasm (sub-stubs) | Only ref at ROM off 0x75410 = last word of dispatch table 0x753a0..0x75413 (29-entry, raw ptr); all 29 table entries fall within [0x75414,0x754b8); 6 unique sub-stub entry points |
| B3 | 0x08075d0c | 0x2c | raw=0 thumb=1 | R4 disasm (fn_eligible) | FS handler table at 0x09e41948 holds THUMB+1=0x08075d0d; entry CID at fn_ptr-4=0x09e41944=0x00001678 (Magical Dimension); contains literal pool word 0x08075d38 (dispatch table for B4) |
| B4 | 0x08075d5c | 0x214 | raw=1 thumb=0 | R4 disasm (sub-stubs) | Only ref at ROM off 0x75d58 = last word of dispatch table 0x75d38..0x75d5b (9-entry, raw ptr); all 9 table entries fall within [0x75d5c,0x75f70); 9 unique sub-stub entry points; internal THUMB+1 values at +0x88/+0xe8/+0x100/+0x190/+0x1cc are literal pool constants (callee ptrs), not external table refs |
| B5 | 0x08075f8e | 0x2e | raw=0 thumb=0 (block start); addr+2=0x08075f90 thumb=1 | R4 disasm (fn_eligible with 2B pad) | 2-byte alignment pad (0x0000) at +0x00; actual fn code starts at +0x02 (0x08075f90=push{r4,r5,r6,r7,lr}); FS handler table at 0x09e41978 holds THUMB+1=0x08075f91; entry CID at fn_ptr-4=0x09e41974=0x0000167a (Friendship -- REUSE FRIENDSHIP_CID); literal pool at +0x2a = 0x08075fbc (dispatch table base for B6) |
| B6 | 0x08075fe0 | 0x17c | raw=1 thumb=0 | R4 disasm (sub-stubs) | Only ref at ROM off 0x75fdc = last word of dispatch table 0x75fbc..0x75fdb (9-entry, raw ptr); all 9 table entries fall within [0x75fe0,0x7615c); 6 unique sub-stub entry points |

**§5.1 登记: 0 块** (所有 6 块均有引用).

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 全部 REUSE -- 按 VALUE grep 确认)

EQ 总计: 42 槽，全部 REUSE.

| 槽地址 | 值 | const_name | inc 文件 | 槽标签 |
|--------|----|------------|---------|--------|
| DWORD_0807536c | 0x0201c4e0 | gP1LifePoints | ewram.inc | DWORD_0807536c |
| DWORD_08075370 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_08075370 |
| DWORD_08075374 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | DWORD_08075374 |
| DWORD_08075524 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_08075524 |
| DWORD_08075528 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | DWORD_08075528 |
| DWORD_0807552c | 0x0201c510 | gDuelFieldSlots | ewram.inc | DWORD_0807552c |
| DWORD_080755d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_080755d4 |
| DWORD_080755d8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | DWORD_080755d8 |
| DWORD_08075660 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_08075660 |
| DWORD_08075664 | 0x0201c510 | gDuelFieldSlots | ewram.inc | DWORD_08075664 |
| DWORD_08075bc4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | DWORD_08075bc4 |
| DWORD_08075be8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | duel_field.inc | DWORD_08075be8 |
| DWORD_08075c20 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | duel_field.inc | DWORD_08075c20 |
| DWORD_08075c28 | 0x00001fff | SLOT_CARD_SET_CODE_MASK | duel_field.inc | DWORD_08075c28 |
| DWORD_08075ca8 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_08075ca8 |
| DWORD_08075cac | 0x0201c510 | gDuelFieldSlots | ewram.inc | DWORD_08075cac |
| DWORD_080761e0 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DWORD_080761e0 |
| DWORD_080761e4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | DWORD_080761e4 |
| DAT_080757e0 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_080757e0 |
| DAT_080757e4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | DAT_080757e4 |
| DAT_080757e8 | 0x000001ff | SCROLLBAR_KEEP_BITS_8_0 | gl_scrollbar.inc | DAT_080757e8 |
| DAT_080757ec | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | gl_scrollbar.inc | DAT_080757ec |
| DAT_08075870 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_08075870 |
| DAT_080758e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_080758e8 |
| DAT_080758ec | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | DAT_080758ec |
| DAT_08075924 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | DAT_08075924 |
| DAT_08075974 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_08075974 |
| DAT_08075978 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | DAT_08075978 |
| DAT_080759b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_080759b8 |
| DAT_080759bc | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | DAT_080759bc |
| DAT_080759dc | 0x000001b7 | lookup_equip_score_b_0x1b7 | duel_field.inc | DAT_080759dc |
| DAT_08075a08 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | duel_field.inc | DAT_08075a08 |
| DAT_08075a6c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | duel_field.inc | DAT_08075a6c |
| DAT_08075a70 | 0x00008056 | OAM_EFFECT_SLOT_TILE_P1 | oam_attr.inc | DAT_08075a70 |
| DAT_08075a74 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_08075a74 |
| DAT_08075a78 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc | DAT_08075a78 |
| DAT_08075ab8 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_08075ab8 |
| DAT_08075abc | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | DAT_08075abc |
| DAT_08075b10 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | DAT_08075b10 |
| DAT_08075b14 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | DAT_08075b14 |
| DAT_08075b18 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | DAT_08075b18 |
| DAT_08076250 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | DAT_08076250 |

**C5 dedup evidence (BY VALUE):**
- PLAYER_BLOCK_STRIDE=0x868: `grep -c "0x00000868" constants/duel_field.inc` >= 1 (exists: `PLAYER_BLOCK_STRIDE, 0x868`) -- REUSE confirmed.
- gDuelFieldSlots=0x0201c510: exists in ewram.inc -- REUSE confirmed.
- gP1LifePoints=0x0201c4e0: exists in ewram.inc -- REUSE confirmed.
- gDuelCardCtxBase=0x0201e2a0: exists in ewram.inc -- REUSE confirmed.
- gEquipZoneCountTable=0x0201e1c8: exists in ewram.inc -- REUSE confirmed.
- gDuelPhaseFlags=0x0201b290: exists in ewram.inc -- REUSE confirmed.
- EQUIP_PHASE_FRAME_OFF=0x4a4: exists in duel_field.inc -- REUSE confirmed.
- SLOT_CARD_SET_CODE_MASK=0x1fff: exists in duel_field.inc -- REUSE confirmed.
- SCROLLBAR_KEEP_BITS_8_0=0x1ff: exists in gl_scrollbar.inc -- REUSE confirmed.
- SCROLLBAR_CLEAR_BITS_14_6=0xffff803f: exists in gl_scrollbar.inc -- REUSE confirmed.
- gP1HandSlotArray=0x0201c8f8: exists in ewram.inc -- REUSE confirmed.
- lookup_equip_score_b_0x1b7=0x1b7: exists in duel_field.inc -- REUSE confirmed.
- OAM_EFFECT_SLOT_TILE_P1=0x8056: exists in oam_attr.inc -- REUSE confirmed.
- gP1SlotSetCodeArray=0x0201c740: exists in ewram.inc -- REUSE confirmed.

### REF_SLOTS (USER-label + DATA-ref RAM/ROM globals)

REF 总计: 0 (本段所有全局访问均为 pc-relative literal pool .word，均以 EQ 方式处理; PTR_gP1LifePoints_XXXX 槽已由命名阶段处理，不计入残留).

### RENAME_SLOTS (改名 + EOL)

RENAME 总计: 4 槽.

| 槽地址 | 原名 | 新标签 | EOL_ASCII (如有) |
|--------|------|--------|-----------------|
| 0x08075414 | DAT_08075414 | emblem_dispatch_sub_stubs_5414 | (disasm 处理后 B2 首 sub-stub 标签) |
| 0x08075c24 | DWORD_08075c24 | dispatch_eff_act_card_id_ptr_5c24 | FS ROM ptr: [0x09e3f134]=0x1670 (unassigned CID); read mask 0x1fff in dispatch_effect_activation_with_lp_counter state 0x7f |
| 0x08075d5c | DAT_08075d5c | magical_dim_dispatch_sub_stubs_5d5c | (disasm 处理后 B4 首 sub-stub 标签) |
| 0x08075fe0 | DAT_08075fe0 | friendship_dispatch_sub_stubs_5fe0 | (disasm 处理后 B6 首 sub-stub 标签) |

**Note on DWORD_08075c24 (Ruling A):** 0x09e3f134 是 FS ROM 地址 (0x09e3fXXX 模式); Ruling A 规定使用 RENAME_ONLY + ASCII EOL, 不建立 .equ. ROM off 0x1e3f134 值 = 0x1670 (unassigned card CID slot, card-stats.s line 27198: `card_2091: @ slot=0x1670 copy=0`). 消费者: dispatch_effect_activation_with_lp_counter @0x08075bec state 0x7f path (asm L15849-15873): `ldr r0, DWORD_08075c24; ldr r0,[r0]; ands r0, SLOT_CARD_SET_CODE_MASK; str r0,[sp+4]` (loads card_id from FS ROM, masks to 13 bits). Conf: high.

### FUNC_RENAME (误名订正, 如有)

FUNC_RENAME: 0 (本段函数名经逐一核验与函数体一致; 无误名信号).

### PLATE (R5; full 重写 或 substring 替换; 全 ASCII)

PLATE: 0 (Seg-7 无 CJK mojibake, 无 stale FUN_ refs -- grep 结果为 0).

---

## disasm 计划 (R4)

### B1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378

- ROM_INCBIN 0x75378, 0x28 (40 bytes)
- FS table THUMB+1 ref at ROM off 0x1e41678 (GBA 0x09e41678); CID at fn_ptr-4=0x09e41674=0x00001629 (Emblem of Dragon Destroyer; card-stats.s line 16811: `card_1292: @ Emblem of Dragon Destroyer slot=0x1629 pw=06390406`). Conf: high.
- Block contains literal pool word at +0x24 = 0x080753a0 (dispatch table base for B2).
- Procedure: clearListing 0x08075378 range 0x28 -> setTMode(0x08075378) -> DisassembleCommand(0x08075378) -> createFunction(0x08075378, "fn_eligible_emblem_of_dragon_destroyer") -> createDWord for literal pool words at end of block.
- New constant: EMBLEM_OF_DRAGON_DESTROYER_CID = 0x1629 (NEW in card_info.inc; pw=06390406).

### B2: emblem_dispatch_sub_stubs @ 0x08075414

- ROM_INCBIN 0x75414, 0xa4 (164 bytes)
- Dispatch table 0x753a0..0x75413 (29 entries, raw ptr); table is in Ghidra as 29 .word entries in existing asm -- already symbolized by auto-naming stage.
- Unique sub-stub entry points: 0x75414, 0x75446, 0x7545a, 0x75492, 0x754a4, 0x754ae (6 unique, of which 0x754ae is the default/epilogue).
- Labels: emblem_sub_5414, emblem_sub_5446, emblem_sub_545a, emblem_sub_5492, emblem_sub_54a4, emblem_default_54ae.
- Procedure: clearListing 0x08075414 range 0xa4 -> setTMode -> per-sub-stub DisassembleCommand (6 calls) -> createFunction for each -> force_dword_4b for any inline literal pool words.
- DAT_08075414 rename to emblem_dispatch_sub_stubs_5414 (used as RENAME_SLOT).

### B3: fn_eligible_magical_dimension @ 0x08075d0c

- ROM_INCBIN 0x75d0c, 0x2c (44 bytes)
- FS table THUMB+1 ref at ROM off 0x1e41948 (GBA 0x09e41948); CID at fn_ptr-4=0x09e41944=0x00001678 (Magical Dimension; card-stats.s line 17552: `card_1349: @ Magical Dimension slot=0x1678 pw=28553439`). Conf: high.
- Block contains literal pool words at +0x24=0x0201b290 (gDuelPhaseFlags) and +0x28=0x08075d38 (dispatch table base for B4).
- Procedure: clearListing 0x08075d0c range 0x2c -> setTMode -> DisassembleCommand(0x08075d0c) -> createFunction -> createDWord for pool words (2 DWords at 0x08075d30, 0x08075d34).
- New constant: MAGICAL_DIMENSION_CID = 0x1678 (NEW in card_info.inc; pw=28553439).

### B4: magical_dim_dispatch_sub_stubs @ 0x08075d5c

- ROM_INCBIN 0x75d5c, 0x214 (532 bytes)
- Dispatch table 0x75d38..0x75d5b (9 entries, raw ptr): 0x75f2c, 0x75f02, 0x75ec0, 0x75e8c, 0x75e60, 0x75e20, 0x75de8, 0x75dc4, 0x75d5c. All confirmed in [0x75d5c, 0x75f70).
- 9 unique sub-stub entry points, all in B4 range.
- Internal THUMB+1 values at B4+0x088=0x08053e15 (check_equip_slot_eligible_by_type_and_space), B4+0xe8=B4+0x100=0x08065991 (check_equip_activation_at_slot11), B4+0x190=B4+0x1cc=0x08050751 (check_equip_slot_eligible_type_and_card_match) are LITERAL POOL constants within sub-stub code, not external table refs to B4.
- Labels: magical_dim_sub_5d5c, magical_dim_sub_5dc4, magical_dim_sub_5de8, magical_dim_sub_5e20, magical_dim_sub_5e60, magical_dim_sub_5e8c, magical_dim_sub_5ec0, magical_dim_sub_5f02, magical_dim_sub_5f2c.
- Procedure: clearListing 0x08075d5c range 0x214 -> setTMode -> 9x DisassembleCommand per entry point -> createFunction for each -> force_dword_4b for inline literal pool DWords (at B4+0x88, +0xe8, +0x100, +0x190, +0x1cc and any others found during disasm).
- DAT_08075d5c rename to magical_dim_dispatch_sub_stubs_5d5c (RENAME_SLOT).

### B5: fn_eligible_friendship @ 0x08075f8e

- ROM_INCBIN 0x75f8e, 0x2e (46 bytes)
- 2-byte alignment pad (0x0000) at +0x00 (0x08075f8e); fn code starts at +0x02 (0x08075f90).
- FS table THUMB+1 ref at ROM off 0x1e41978 (GBA 0x09e41978); THUMB+1=0x08075f91; CID at fn_ptr-4=0x09e41974=0x0000167a (Friendship; REUSE FRIENDSHIP_CID, exists in card_info.inc line 1071). Conf: high.
- Block contains literal pool words at +0x26=0x0201b290 (gDuelPhaseFlags) and +0x2a=0x08075fbc (dispatch table base for B6).
- Procedure: Do NOT clearListing the 2-byte pad at 0x08075f8e (leave as .zero 0x2 or createWord); clearListing 0x08075f90 range 0x2c -> setTMode(0x08075f90) -> DisassembleCommand(0x08075f90) -> createFunction(0x08075f90, "fn_eligible_friendship") -> createDWord for pool words at 0x08075fb4 and 0x08075fb8.
- No new CID constant needed (FRIENDSHIP_CID=0x167a REUSE).

### B6: friendship_dispatch_sub_stubs @ 0x08075fe0

- ROM_INCBIN 0x75fe0, 0x17c (380 bytes)
- Dispatch table 0x75fbc..0x75fdb (9 entries, raw ptr): 0x8076100, 0x8076146 (x4), 0x807609e, 0x8076030, 0x8075ff4, 0x8075fe0. All confirmed in [0x75fe0, 0x7615c).
- 6 unique sub-stub entry points: 0x75fe0, 0x75ff4, 0x76030, 0x7609e, 0x76100, 0x76146 (default).
- Labels: friendship_sub_5fe0, friendship_sub_5ff4, friendship_sub_6030, friendship_sub_609e, friendship_sub_6100, friendship_default_6146.
- Procedure: clearListing 0x08075fe0 range 0x17c -> setTMode -> 6x DisassembleCommand per entry point -> createFunction for each -> force_dword_4b for inline pool words.
- DAT_08075fe0 rename to friendship_dispatch_sub_stubs_5fe0 (RENAME_SLOT).

---

## carve 计划 (R7)

**carve: 0 块.**

Seg-7 の 6 ROM_INCBIN 块全部为 fn_eligible THUMB stubs (B1/B3/B5) 或 raw-dispatch sub-stubs (B2/B4/B6), 均通过 R4 disasm 处理而非 carve. 无需 rom.s 改动.

---

## 新增 constants / 全局

2 个新 CID 常量 (constants/card_info.inc 新增):

```
.equ EMBLEM_OF_DRAGON_DESTROYER_CID, 0x00001629  @ Emblem of Dragon Destroyer (pw=06390406); slot=0x1629 in card-stats.s line 16811; fn_eligible B1 @ 0x08075378; FS ref @ 0x09e41678
.equ MAGICAL_DIMENSION_CID,          0x00001678  @ Magical Dimension (pw=28553439); slot=0x1678 in card-stats.s line 17552; fn_eligible B3 @ 0x08075d0c; FS ref @ 0x09e41948
```

FRIENDSHIP_CID=0x167a: REUSE (已存在于 card_info.inc line 1071).

**C5 dedup 验证 (NEW 槽按值 grep):**
- EMBLEM_OF_DRAGON_DESTROYER_CID 0x1629: `grep -c "0x00001629" constants/card_info.inc` = 0 -> NEW confirmed.
- MAGICAL_DIMENSION_CID 0x1678: `grep -c "0x00001678" constants/card_info.inc` = 0 -> NEW confirmed.

---

## §5.1 登记 (Rule 3) -- 0 引用块

无. 所有 6 块均有 FS THUMB+1 或 raw dispatch ptr 引用, 均须 R4 disasm 处理. §5.1 登记表无新增.

---

## 消费者证据 (R6) -- 关键槽语义

| 槽 | 值 | 消费者 (file:line) | 语义 | conf |
|----|----|--------------------|------|------|
| DWORD_08075528 | 0x0201e1c8 | asm/09_equip_lp_display.s L14816: `ldr r1, DWORD_08075528; ldr r4,[r1,#0]` in enqueue_effect_slot_sprites_all_players | gEquipZoneCountTable (plate comment: gEffectSlots=0x0201e1c8) -- confirmed same addr | high |
| DWORD_08075c24 | 0x09e3f134 | asm/09_equip_lp_display.s L15849: `ldr r0, DWORD_08075c24; ldr r0,[r0,#0]; ldr r1, DWORD_08075c28; ands r0,r1; str r0,[sp,#4]` in dispatch_effect_activation_with_lp_counter | FS ROM ptr to card_id data (0x09e3f134 dereferences to 0x1670 = unassigned CID, masked to 13 bits) | high |
| DAT_08075a70 | 0x00008056 | asm/09_equip_lp_display.s L15569: `ldr r6, DAT_08075a70; adds r0,r6,#0` in tick_equip_zone_display_seq_by_type_code state 0x7d player==0 path | OAM_EFFECT_SLOT_TILE_P1 sprite type code (player==1 uses inline 0x56=OAM_EFFECT_SLOT_TILE_P2) | high |
| DAT_080757e8 | 0x000001ff | asm/09_equip_lp_display.s L15187-15190: `ldr r7, DAT_080757e8; ands r3,r0; lsls r3,r3,#6` in enqueue_equip_zone_sprite_with_slot_setup | 9-bit bit-mask for zone slot field -- same domain as SCROLLBAR_KEEP_BITS_8_0 | high |
| DAT_080757ec | 0xffff803f | asm/09_equip_lp_display.s L15192-15195: `ldr r0, DAT_080757ec; ands r0,r5; orrs r0,r3; strh r0,[r4,#4]` | SCROLLBAR_CLEAR_BITS_14_6 clears bits[14:6] in zone slot halfword field | high |
| DAT_08075a78 | 0x0201c740 | asm/09_equip_lp_display.s L15577: `ldr r3, DAT_08075a78; adds r0,r0,r3` in tick_equip_zone_display_seq_by_type_code state 0x7d | gP1SlotSetCodeArray base (player=0 path; *0x868 player offset added prior) | high |

---

## C13 残留 100% 覆盖证明

- 精确 python 清点 (独立脚本): 19 DWORD_ + 27 DAT_ = 46 auto-name slots in lines 14656..16265.
- EQ 计划覆盖: 42 槽 (18 DWORD_ + 24 DAT_).
- RENAME 计划覆盖: 4 槽 (DWORD_08075c24 + DAT_08075414 + DAT_08075d5c + DAT_08075fe0).
- 并集: 42 + 4 = 46 = 精确总数. 无漏项, 无重复.
- 三张表中 PTR_gP1LifePoints_XXXX 槽 (4 个: 0807586c/08075970/080759b4/08075a0c) 已由命名阶段处理 (非 DAT_/DWORD_/UNK_), 不计入 46 slot 总数.

---

## 求助

无低置信度语义. 所有槽均有 file:line 证据支撑, 置信度 high.

一个注意点: DAT_080757e8=0x1ff 和 DAT_080757ec=0xffff803f 复用 SCROLLBAR_ 前缀常量, 因为它们的位域操作语义 (9-bit field insert/clear) 与 scrollbar 完全一致. 不新建同义 equate (C5 原则: 值碰撞语义一致必复用).
