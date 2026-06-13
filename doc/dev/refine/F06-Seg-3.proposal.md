# Refine Proposal: F06-Seg-3  [0x08054ba0..0x08055440)

## 段测绘

- 函数入口: 22 fn (0x54ba0..0x553d4 共 21 fn 在段内; 0x55440 = Seg-4 起点)
  1. check_equip_slot_eligible_by_equip_type_and_occupied @ 0x08054ba0
  2. check_equip_slot_eligible_by_prereqs_and_effect_ctx @ 0x08054bec
  3. check_equip_slot_eligible_by_opposite_whitelist_space_and_type @ 0x08054c50
  4. check_equip_slot_eligible_by_equippable_and_type_code @ 0x08054cb0
  5. check_equip_slot_eligible_by_whitelist_field7_and_zone_bit @ 0x08054d08
  6. check_equip_slot_eligible_by_display_criteria_loop @ 0x08054d5c
  7. check_equip_slot_eligible_by_opposite_field8_or_field6_and_type @ 0x08054df4
  8. check_equip_slot_eligible_by_setcode_prereqs_all_slots @ 0x08054e5c
  9. check_equip_slot_eligible_by_same_side_field8_zero_field6_and_type @ 0x08054ea8
  10. check_equip_slot_eligible_by_spell_type_and_prereqs @ 0x08054f08
  11. check_equip_slot_eligible_by_opposite_field8_zero_and_prereqs @ 0x08054f64
  12. check_equip_slot_eligible_by_opposite_prereqs_and_type @ 0x08054fbc
  13. check_equip_slot_type_eligibility_no_range @ 0x0805501c
  14. check_equip_slot_eligible_by_prereqs_and_type_code_mismatch @ 0x08055078
  15. check_equip_slot_eligible_by_prereqs_and_type @ 0x080550e4
  16. check_equip_slot_cross_player_type_eligible @ 0x08055138
  17. ROM_INCBIN 0x55188/0x34 <- between fn 16 and fn 17
  18. check_equip_slot_eligible_by_setcode_g_and_field5 @ 0x080551bc
  19. check_slot_effect_value_beats_card_category @ 0x08055248
  20. check_equip_slot_eligible_by_effect_value_and_category @ 0x080552a0
  21. check_equip_slot_player_match_and_empty_field6 @ 0x08055318
  22. check_equip_slot_eligible_by_type_mismatch_prereqs_and_eligible @ 0x08055360
  23. check_equip_slot_whitelist_with_zone_bitmap @ 0x080553d4

- 残留自动名槽: 43 个 (Python 精确清点; 无越界)
  - 21x DWORD_/DAT_ = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - 21x DWORD_/DAT_ = 0x0201c510 (gDuelFieldSlots)
  -  1x DWORD_08054c44 = 0x0201bb90 (gEquipChainSlotRefs)

- ROM_INCBIN / .byte 块: ROM_INCBIN 0x55188/0x34 (52 bytes)

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08055188 sz=0x34 | raw=0; thumb+1 (0x08055189) =2 命中 | R4 disasm | 两个 THUMB+1 命中均在 0x09e4xxxx card effect handler dispatch table (CID+fn_ptr 格式), 非压缩偶合 (见下节) |

### ref-scan 详情

**目标**: 0x08055189 (= 0x08055188 | 1)

**命中 1**: ROM offset 0x1e4365c = ROM addr 0x09e4365c
```
0x09e43654: 0x0000130f  <- CID word (slot 0x130f, unassigned in card-stats.s)
0x09e43658: 0x0806a549  <- fn_ptr1+1 (THUMB -> fn @ 0x0806a548)
0x09e4365c: 0x08055189  <- fn_ptr2+1 = 0x08055188 | 1  <<<
0x09e43660: 0x00000000  <- zero pad
```

**命中 2**: ROM offset 0x1e43b84 = ROM addr 0x09e43b84
```
0x09e43b7c: 0x000014b4  <- CID word (Byser Shock, slot 0x14b4 @ card-stats.s L13015)
0x09e43b80: 0x0806abd5  <- fn_ptr1+1 (THUMB -> fn @ 0x0806abd4)
0x09e43b84: 0x08055189  <- fn_ptr2+1 = 0x08055188 | 1  <<<
0x09e43b88: 0x00000000  <- zero pad
```

**结构判定**: 两者均符合 `[CID_word][fn_ptr1+1][fn_ptr2+1][zeros...]` 的 dispatch table 格式
(对比 Seg-2 中 0x09e421d4 已知 Desert Sunlight dispatch table 结构验证一致)。
CID 0x130f 未在 card-stats.s 中分配 (0x130d/0x130e 空缺, 下一个是 0x1310=Wall of Illusion)。
CID 0x14b4 = Byser Shock (passcode=17597059, card-stats.s L13015)。

**结论**: ROM_INCBIN 0x55188/0x34 = THUMB 代码, 被两个 CID 的 handler dispatch table 引用为 fn_ptr2
-> **R4 disasm** (不 §5.1)

---

## 数据块内容分析 (为 R4 disasm 服务)

ROM_INCBIN 0x55188/0x34 THUMB 解码:

```
0x08055188: 2301  movs r3, #1
0x0805518a: 400b  ands r3, r1            ; r3 = player_id & 1
0x0805518c: 0090  lsls r0, r2, #2        ; r0 = slot_idx << 2
0x0805518e: 1880  adds r0, r0, r2        ; r0 = slot_idx*5
0x08055190: 8000  lsls r0, r0, #2        ; r0 = slot_idx*20
0x08055192: 4907  ldr r1, [pc, #28]      ; r1 = PLAYER_BLOCK_STRIDE (pool @ 0x080551b0)
0x08055194: 4359  muls r1, r3            ; r1 = (player_id&1) * 0x868
0x08055196: 1840  adds r0, r0, r1        ; r0 = slot_idx*20 + player_block
0x08055198: 4906  ldr r1, [pc, #24]      ; r1 = gDuelFieldSlots (pool @ 0x080551b4)
0x0805519a: 1841  adds r1, r0, r1        ; r1 = zone entry ptr
0x0805519c: 6808  ldr r0, [r1, #0]       ; r0 = zone word
0x0805519e: 04c0  lsls r0, r0, #19       ; test bits[12:0] nonzero (alt is_present check)
0x080551a0: 2800  cmp r0, #0
0x080551a2: d009  beq LAB_080551b8       ; branch if bits[12:0]==0 (no card) -> fail
0x080551a4: 8908  ldrh r0, [r1, #8]      ; r0 = zone[+8] equip valid flag
0x080551a6: 2800  cmp r0, #0
0x080551a8: d106  bne LAB_080551b8       ; branch if zone[+8]!=0 (equip busy) -> fail
0x080551aa: 2001  movs r0, #1            ; return 1 (pass: occupied AND equip flag clear)
0x080551ac: e005  b LAB_080551ba
0x080551ae: 0000  .zero 2
0x080551b0: 0868 0000  .word 0x00000868  ; PLAYER_BLOCK_STRIDE (pool)
0x080551b4: c510 0201  .word 0x0201c510  ; gDuelFieldSlots (pool)
LAB_080551b8:
0x080551b8: 2000  movs r0, #0            ; return 0 (fail)
LAB_080551ba:
0x080551ba: 4770  bx lr                  ; leaf fn, returns via lr (NOT pop{r1};bx r1)
```

**Branch targets verified**:
- beq (0xd009) @ 0x080551a2: PC=0x080551a6, target=0x080551a6+9*2=0x080551b8 (fail)
- bne (0xd106) @ 0x080551a8: PC=0x080551ac, target=0x080551ac+6*2=0x080551b8 (fail)
- b   (0xe005) @ 0x080551ac: PC=0x080551b0, target=0x080551b0+5*2=0x080551ba (bx lr)
- lsls #19 = 0x04c0 verified: bits[12:11]=00 (LSL), imm5=19, Rs=Rd=r0 (python decode)

**修正后语义**:
- 输入: r0=ignored, r1=player_id [0..1], r2=slot_idx (unchecked)
- 检查: (1) gDuelFieldSlots[player_id&1][slot_idx] word bits[12:0] != 0 (slot 有卡)
          AND (2) zone[+8] (equip valid flag) == 0 (equip 链头空位)
- 返回: r0=1 (pass) or 0 (fail)
- 调用约定: bx lr (leaf, NOT pop {r1}; bx r1)

**函数名**: `check_zone_slot_occupied_with_clear_equip_flag`
置信度: high (file:asm/06_equip_eligibility_b.s L3970 ROM_INCBIN; dispatch table context + THUMB decode verified)

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 全部复用 ewram.inc 现有常量)

| 槽 | addr | value | const_name | slot_label |
|---|---|---|---|---|
| DWORD_08054bdc | 0x08054bdc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_equip_type_and_occupied_stride |
| DWORD_08054be0 | 0x08054be0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_equip_type_and_occupied_slots |
| DWORD_08054c3c | 0x08054c3c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_and_effect_ctx_stride |
| DWORD_08054c40 | 0x08054c40 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_prereqs_and_effect_ctx_slots |
| DWORD_08054ca0 | 0x08054ca0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_whitelist_space_and_type_stride |
| DWORD_08054ca4 | 0x08054ca4 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_whitelist_space_and_type_slots |
| DWORD_08054cf8 | 0x08054cf8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_equippable_and_type_code_stride |
| DWORD_08054cfc | 0x08054cfc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_equippable_and_type_code_slots |
| DWORD_08054d4c | 0x08054d4c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_whitelist_field7_and_zone_bit_stride |
| DWORD_08054d50 | 0x08054d50 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_whitelist_field7_and_zone_bit_slots |
| DWORD_08054dd8 | 0x08054dd8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_display_criteria_loop_stride |
| DWORD_08054ddc | 0x08054ddc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_display_criteria_loop_slots |
| DWORD_08054e4c | 0x08054e4c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_field8_or_field6_and_type_stride |
| DWORD_08054e50 | 0x08054e50 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_field8_or_field6_and_type_slots |
| DWORD_08054ef8 | 0x08054ef8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_same_side_field8_zero_field6_and_type_stride |
| DWORD_08054efc | 0x08054efc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_same_side_field8_zero_field6_and_type_slots |
| DWORD_08054f54 | 0x08054f54 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_spell_type_and_prereqs_stride |
| DWORD_08054f58 | 0x08054f58 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_spell_type_and_prereqs_slots |
| DAT_08054fac | 0x08054fac | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_field8_zero_and_prereqs_stride |
| DAT_08054fb0 | 0x08054fb0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_field8_zero_and_prereqs_slots |
| DAT_0805500c | 0x0805500c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_prereqs_and_type_stride |
| DAT_08055010 | 0x08055010 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_prereqs_and_type_slots |
| DAT_08055068 | 0x08055068 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_type_eligibility_no_range_stride |
| DAT_0805506c | 0x0805506c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_type_eligibility_no_range_slots |
| DAT_080550d4 | 0x080550d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_and_type_code_mismatch_stride |
| DAT_080550d8 | 0x080550d8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_prereqs_and_type_code_mismatch_slots |
| DAT_08055128 | 0x08055128 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_and_type_stride |
| DAT_0805512c | 0x0805512c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_prereqs_and_type_slots |
| DAT_08055178 | 0x08055178 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_cross_player_type_eligible_stride |
| DAT_0805517c | 0x0805517c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_cross_player_type_eligible_slots |
| DAT_08055204 | 0x08055204 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_g_and_field5_stride |
| DAT_08055208 | 0x08055208 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_setcode_g_and_field5_slots |
| DAT_08055278 | 0x08055278 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_slot_effect_value_beats_card_category_stride |
| DAT_0805527c | 0x0805527c | 0x0201c510 | gDuelFieldSlots | check_slot_effect_value_beats_card_category_slots |
| DAT_08055308 | 0x08055308 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_effect_value_and_category_stride |
| DAT_0805530c | 0x0805530c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_effect_value_and_category_slots |
| DAT_08055350 | 0x08055350 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_player_match_and_empty_field6_stride |
| DAT_08055354 | 0x08055354 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_player_match_and_empty_field6_slots |
| DAT_080553c4 | 0x080553c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_mismatch_prereqs_and_eligible_stride |
| DAT_080553c8 | 0x080553c8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_mismatch_prereqs_and_eligible_slots |
| DAT_08055430 | 0x08055430 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_whitelist_with_zone_bitmap_stride |
| DAT_08055434 | 0x08055434 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_whitelist_with_zone_bitmap_slots |

**复用确认**:
- PLAYER_BLOCK_STRIDE=0x868: ewram.inc L? 已存在 (grep 确认)
- gDuelFieldSlots=0x0201c510: ewram.inc 已存在 (grep 确认)
- 0 new EQ constants needed

### REF_SLOTS (USER-label + DATA-ref)

| 槽 | addr | value | target | gas_label | slot_label |
|---|---|---|---|---|---|
| DWORD_08054c44 | 0x08054c44 | 0x0201bb90 | gEquipChainSlotRefs | gEquipChainSlotRefs | check_equip_slot_eligible_by_prereqs_and_effect_ctx_ctx |

**注**: gEquipChainSlotRefs=0x0201bb90 已在 ewram.inc 定义 (grep 确认); 同 Seg-1 @ L611 pattern (.word gEquipChainSlotRefs)。

### RENAME_SLOTS (纯改名)

全部 42 个 EQ_SLOTS (非 REF) 均需同步改 slot label: 见 EQ_SLOTS 表中 slot_label 列。

### FUNC_RENAME

无 (all 22 functions already named correctly; plates are clean ASCII with no stale FUN_)

### PLATE (R5)

无需 plate 修改: Seg-3 内所有函数 plate 均已为 ASCII (grep 确认: 0 non-ASCII lines, 0 stale FUN_ refs)。
disasm'd 新函数 check_zone_slot_occupied_with_clear_equip_flag 需设 plate (见 disasm 计划)。

---

## carve 计划 (R7)

无 carve. ROM_INCBIN 0x55188/0x34 分类为 R4 disasm, 不 carve 进 rom.s.

---

## disasm 计划 (R4)

**ROM_INCBIN 0x55188/0x34** -> THUMB leaf fn `check_zone_slot_occupied_with_clear_equip_flag`

范围: 0x08055188..0x080551bc (0x34 bytes)

执行步骤 (file 00 Seg-5c R4 范式):
1. Ghidra: clearListing(0x08055188, 0x080551bb) [byte range]
2. setTMode(0x08055188, true)
3. DisassembleCommand(0x08055188)  [注意: 按地址, NOT per-stub loop; this is one fn]
4. createFunction(0x08055188, "check_zone_slot_occupied_with_clear_equip_flag")
5. setPlateComment(0x08055188, plate text below)
6. 两个 literal pool 槽 (0x080551b0 + 0x080551b4) 需 EQ 处理:
   - 0x080551b0: .word 0x00000868 -> slot_label: check_zone_slot_clear_equip_stride; EQ PLAYER_BLOCK_STRIDE
   - 0x080551b4: .word 0x0201c510 -> slot_label: check_zone_slot_clear_equip_slots; EQ gDuelFieldSlots

**Plate text (ASCII)**:
```
check_zone_slot_occupied_with_clear_equip_flag @ 0x08055188
Equip target slot eligibility predicate: slot has card AND equip-valid flag is clear.
Called as fn_ptr2 for CID 0x130f (unassigned) @ dispatch_table 0x09e43654
  and CID 0x14b4 (Byser Shock) @ dispatch_table 0x09e43b7c.
Checks in order: (1) gDuelFieldSlots[player_id&1][slot_idx] zone_word bits[12:0] != 0
(occupied, alt is_present check via lsls #19); (2) zone[+8] (equip valid flag) == 0.
Returns 1 if both pass (slot occupied + equip chain head empty).
Leaf fn using bx lr (NOT pop{r1};bx r1). Inputs: r0=ignored, r1=player_id, r2=slot_idx.
Constants: PLAYER_BLOCK_STRIDE=0x868, gDuelFieldSlots=0x0201c510.
```

**CSV 同步**: 新增行 `0x08055188, check_zone_slot_occupied_with_clear_equip_flag`

---

## 新增 constants / 全局

**无** (所有 44 个槽值均复用现有 constants/ewram.inc 常量)

---

## §5.1 登记 (Rule 3)

**无** (ROM_INCBIN 0x55188/0x34 有 2 个 THUMB+1 真引用 -> R4 disasm, 不 §5.1)

---

## 消费者证据 (R6)

- **check_equip_slot_eligible_by_prereqs_and_effect_ctx** (fn 2, 0x08054bec):
  gEquipChainSlotRefs[+4] compared to player_id (activating player); [+0x20] compared to slot_idx.
  file: asm/06_equip_eligibility_b.s L3054-3121 (plate comment). Confidence: high.
  Note: offsets +4 and +0x20 are ldr instruction immediates, NOT literal pool slots; no new EQ needed.

- **check_zone_slot_occupied_with_clear_equip_flag** (disasm'd fn):
  fn_ptr2 in dispatch table entries for CID 0x130f and CID 0x14b4 (Byser Shock).
  file: roms/2343.gba @ 0x09e4365c and 0x09e43b84. Confidence: high (decode verified).
  ldrh [+8] = equip valid flag (consistent with existing plates: "ldrh [slot,#8]!=0 (equip valid flag)").

---

## 求助

**无** (所有槽语义 high/med confidence; disasm 函数语义经 THUMB 精确解码确认)

**已解的歧义**:
- lsls r0, r0, #19 确认为: 0x04c0 = bits[12:11]=00 (LSL), imm5=19; 检查 bits[12:0] nonzero
- bne 0xd106 at 0x080551a8 目标 = LAB_080551b8 (fail path); 语义: zone[+8]!=0 -> fail (not bne to pass)
- 函数语义: occupied AND equip flag CLEAR (not occupied AND equip flag set)

---

## Executor Report: F06-Seg-3

- 槽: EQ=42 REF=1 RENAME=43 FUNC_RENAME=0 PLATE=0 (已 clean) + 1 plate for disasm'd fn
- carve=0 disasm=1 (ROM_INCBIN 0x55188/0x34 -> check_zone_slot_occupied_with_clear_equip_flag) §5.1=0
- 新增 constants/全局: none (all 3 unique values reuse ewram.inc)
- 求助: none
- proposal: doc/dev/refine/F06-Seg-3.proposal.md
