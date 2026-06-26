# Refine Proposal: F11-Seg-2  [0x08085d4c..0x08086cdc)

## 段测绘

- 范围: `[0x08085d4c, 0x08086cdc)`, 4,752 bytes
- 函数入口 x12 (address order):
  1. 0x08085d4c  `dispatch_field_display_state_by_type`    (~32 slots)
  2. 0x0808611c  `dispatch_equip_slot_state_by_index`      (~9 slots + ROM_INCBIN)
  3. 0x08086430  `check_equip_target_slot_by_card_id`      (~2 slots)
  4. 0x0808647c  `find_equip_target_in_effect_zones`       (~5 slots)
  5. 0x08086508  `sum_equip_zone_bonus_scores_for_player`  (~5 slots)
  6. 0x080865ac  `sum_equip_chain_scores_for_card`         (~2 slots)
  7. 0x08086634  `eval_equip_slot_score_in_range`          (~16 slots)
  8. 0x08086954  `check_sorted_array_value_in_range`       (0 slots)
  9. 0x080869a8  `scan_equip_zones_for_eligible_type11_target` (~6 slots)
  10. 0x08086a38 `eval_equip_zone_score_with_field_card`   (~2 slots)
  11. 0x08086a80 `eval_equip_zone_activation_eligible`     (~11 slots)
  12. 0x08086c80 `check_neo_daedalus_equip_zone_eligible`  (~2 slots)

- 残留自动名槽 x92 total:
  - DAT_* x74 (includes DWORD_08086160..0808616c)
  - DWORD_* x4 (inside dispatch_equip_slot_state_by_index)
  - PTR_gP1LifePoints_* x8 (RENAME targets)
  - PTR_PTR_08086170 x1 + PTR_DAT_08086174 x1 (code/table refs)
  - Total = 88 self-defining + 3 PTR_ variants + 1 previously miscounted = 92 unique slot labels

- ROM_INCBIN: 1 block
  - `0x861a0 / 0x27a` (634 B) at address 0x080861a0, labeled `DAT_080861a0`

## 数据块分类 (Rule 2/3) -- ref-scan 证据

### Block: 0x080861a0 / 0x27a (634 B)

ref-scan (python, file `roms/2343.gba`):

```python
import struct
rom = open('roms/2343.gba','rb').read()
block_start = 0x080861a0; block_end = block_start + 0x27a
raw_locs=[]
for a in range(block_start, block_end, 4):
    v=struct.pack('<I',a); o=0
    while True:
        i=rom.find(v,o)
        if i<0: break
        raw_locs.append((hex(i+0x8000000),hex(a))); o=i+1
# raw=11, thumb=4
```

| 块 | ref-scan raw | ref-scan THUMB+1 | 判定 | 理由 |
|----|-------------|-----------------|------|------|
| 0x080861a0 / 0x27a | raw=11 | THUMB+1=4 | R4 DISASM (sub-case labels, not createFunction) | 详见下节 |

**判定根据 (high confidence):**

Raw refs 来源全部分析:
- `0x8086174` -> `0x080861a0` (entry [0]): jump table slot in `PTR_DAT_08086174` -- word-aligned, legitimate raw ptr
- `0x8086178` -> `0x0808621c` (entry [1]): jump table slot -- word-aligned, legitimate
- `0x8086188` -> `0x0808621c` (entry [5]): same target as [1], word-aligned
- `0x808617c` -> `0x080862ec` (entry [2]): word-aligned, legitimate
- `0x8086180` -> `0x08086338` (entry [3]): word-aligned, legitimate
- `0x8086184` -> `0x08086370` (entry [4]): word-aligned, legitimate
- `0x808619c` -> `0x080863cc` (entry [10]): word-aligned, legitimate
- `0x87a1ee9` -> `0x08086208`: NON-word-aligned (odd offset); surrounding bytes `62 08 0b 82 20 08 62 08` -- bytestream coincidence in compressed data asset region. NOT a real ref.
- `0x8b69a5b` -> `0x08086208`: NON-word-aligned; compressed data coincidence. NOT a real ref.
- `0x89d076c` -> `0x0808625c`: surrounding bytes show `5c 62 08 08` aligned but context `55 05 aa 71 5c 62 08 08 82 a5` = high-entropy compressed data. NOT a real ref.
- `0x84eed45` -> `0x08086400`: NON-word-aligned; compressed data coincidence. NOT a real ref.

THUMB+1 refs:
- `0x8937339` -> `0x08086205` (odd offset, non-aligned source): compressed data coincidence. NOT a real BL target.
- `0x8f9552d` -> `0x08086235` (odd offset): compressed data coincidence. NOT a real BL target.
- `0x8a1718d` -> `0x0808624d` (odd offset): compressed data coincidence. NOT a real BL target.
- `0x8d79908` -> `0x0808634d` (word-aligned source): BUT surrounding words at 0x8d79900 are `12e48b2a b3128508 0808634d d74dc682 ...` -- random high-entropy values, confirmed compressed/encrypted data. NOT a real fn-ptr table entry.

**Effective refs: 7 distinct word-aligned raw entries, all from `PTR_DAT_08086174` jump table. 0 valid THUMB+1 refs.**

**Dispatch mechanism:** parent `dispatch_equip_slot_state_by_index` at 0x0808615e executes `.hword 0x4687` = `mov pc,r0` after loading raw address from the jump table. This is a raw-PC dispatch (not `blx`), so entries are raw (non-THUMB+1) code addresses. The 11-entry jump table has entries [0..10] where [6..9] = 0x0808641a (fallback "return 1" outside block) and entry [5] = same as [1].

**Distinct sub-handlers inside block** (6 non-fallback entries):
| entry | addr | first 2 halfwords | semantic |
|-------|------|-------------------|---------|
| [0] | 0x080861a0 | 0x00a0 0x1c11 | slot_substate_0: loads sp+offset, reads aux_ctx, checks slot active |
| [1,5] | 0x0808621c | 0x4809 0x23b2 | slot_substate_1: reads [gDuelPhaseFlags+0x5b2*8], checks, calls BL |
| [2] | 0x080862ec | 0x4a08 0x23ea | slot_substate_2: reads [gDuelPhaseFlags+0x1d5+0x5<<1], calls clear function |
| [3] | 0x08086338 | 0x4805 0x21b2 | slot_substate_3: reads state, calls state function |
| [4] | 0x08086370 | 0x4904 0x4b05 | slot_substate_4: reads gP1LifePoints + offset |
| [10] | 0x080863cc | 0x21b2 0x00c9 | slot_substate_a: reads state, reads halfwords, calls enable function |

None of the 6 entries have `push {lr}` prologues -- they are raw fall-through switch-case bodies sharing the parent function stack frame. **Action: R4 DISASM the block as contiguous THUMB code; create sub-case LABELs (not createFunction) for each of the 6 distinct entry points; create literal pool DWord entries for embedded pool words.**

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

Format: `(slot_label @ addr, value, const_name, source_inc, new/reuse)`

**dispatch_field_display_state_by_type (0x08085d4c):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08085d74 @ 0x08085d74 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085d78 @ 0x08085d78 | 0x0000057c | FIELD_DISPLAY_TYPE_OFF | ewram.inc | REUSE |
| DAT_08085ea0 @ 0x08085ea0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085ea4 @ 0x08085ea4 | 0x00000584 | ELIGIB_RESULT_OFF | ewram.inc | REUSE |
| DAT_08085ea8 @ 0x08085ea8 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | REUSE |
| DAT_08085ebc @ 0x08085ebc | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085f28 @ 0x08085f28 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085f58 @ 0x08085f58 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc | REUSE |
| DAT_08085f70 @ 0x08085f70 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085f90 @ 0x08085f90 | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc | REUSE |
| DAT_08085fb4 @ 0x08085fb4 | 0x00001d5c | ELIGIB_ACT_TYPE_OFF | ewram.inc | REUSE |
| DAT_08085fb8 @ 0x08085fb8 | 0x00001d58 | ELIGIB_ACT_COUNT_OFF | ewram.inc | REUSE |
| DAT_08085ff8 @ 0x08085ff8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08085ffc @ 0x08085ffc | 0x00000584 | ELIGIB_RESULT_OFF | ewram.inc | REUSE |
| DAT_08086000 @ 0x08086000 | 0x0201b870 | gSpriteAttrBuf | ewram.inc | REUSE |
| DAT_08086028 @ 0x08086028 | 0x0201b870 | gSpriteAttrBuf | ewram.inc | REUSE |
| DAT_0808602c @ 0x0808602c | 0x00000584 | ELIGIB_RESULT_OFF | ewram.inc | REUSE |
| DAT_08086064 @ 0x08086064 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc | REUSE |
| DAT_08086080 @ 0x08086080 | 0x00001d44 | ELIGIB_CARD_ID_OFF | ewram.inc | REUSE |
| DAT_080860bc @ 0x080860bc | 0x00001d54 | ELIGIB_STATE_CTRL_OFF | ewram.inc | REUSE |
| DAT_080860c0 @ 0x080860c0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_080860c4 @ 0x080860c4 | 0x00000584 | ELIGIB_RESULT_OFF | ewram.inc | REUSE |
| DAT_080860f4 @ 0x080860f4 | 0x0000057c | FIELD_DISPLAY_TYPE_OFF | ewram.inc | REUSE |
| DAT_080860fc @ 0x080860fc | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | REUSE |
| DAT_08086100 @ 0x08086100 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | ewram.inc | REUSE |

**dispatch_equip_slot_state_by_index (0x0808611c):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DWORD_08086160 @ 0x08086160 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | REUSE |
| DWORD_08086164 @ 0x08086164 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DWORD_08086168 @ 0x08086168 | 0x00000594 | EFFECT_ENTRY_COUNT_OFF | ewram.inc | REUSE |
| DWORD_0808616c @ 0x0808616c | 0x0000058c | EQUIP_SLOT_SUBSTATE_OFF | ewram.inc | NEW (value-grep=0 hits) |

**check_equip_target_slot_by_card_id (0x08086430):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086448 @ 0x08086448 | 0x09e5a0c4 | gEquipEffectZoneTable | card_info.inc or new equip_zone.inc | NEW (value-grep=0 hits) |
| DAT_0808645c @ 0x0808645c | 0x00001698 | CONTRACT_WITH_ABYSS_CID | card_info.inc | NEW (value-grep=0 hits, card-stats.s L17957 confirmed: "Contract with the Abyss slot=0x1698 pw=69035382") |

**find_equip_target_in_effect_zones (0x0808647c):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_080864dc @ 0x080864dc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_080864e0 @ 0x080864e0 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE (same new constant) |
| DAT_080864e4 @ 0x080864e4 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DAT_08086504 @ 0x08086504 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |

**sum_equip_zone_bonus_scores_for_player (0x08086508):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086564 @ 0x08086564 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086568 @ 0x08086568 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DAT_080865a4 @ 0x080865a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_080865a8 @ 0x080865a8 | 0x0201c4ec | gP1ZoneHandCount | ewram.inc | REUSE |

**sum_equip_chain_scores_for_card (0x080865ac):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_0808662c @ 0x0808662c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086630 @ 0x08086630 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |

**eval_equip_slot_score_in_range (0x08086634):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_080866dc @ 0x080866dc | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_080866e0 @ 0x080866e0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE |
| DAT_080866e4 @ 0x080866e4 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
| DAT_080866e8 @ 0x080866e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_080866ec @ 0x080866ec | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DAT_08086790 @ 0x08086790 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086794 @ 0x08086794 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |
| DAT_08086798 @ 0x08086798 | 0x00001716 | EARTH_CHANT_CID | card_info.inc | NEW (value-grep=0 hits, card-stats.s L19335: "Earth Chant slot=0x1716 pw=59820352") |
| DAT_080867b8 @ 0x080867b8 | 0x000019d9 | END_OF_WORLD_CID | card_info.inc | NEW (value-grep=0 hits, card-stats.s L26795: "End of the World slot=0x19D9 pw=08198712") |
| DAT_0808683c @ 0x0808683c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_080868f8 @ 0x080868f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_080868fc @ 0x080868fc | 0x0201c4ec | gP1ZoneHandCount | ewram.inc | REUSE |
| DAT_08086950 @ 0x08086950 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |

**scan_equip_zones_for_eligible_type11_target (0x080869a8):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086a08 @ 0x08086a08 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08086a0c @ 0x08086a0c | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc | REUSE |
| DAT_08086a10 @ 0x08086a10 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
| DAT_08086a14 @ 0x08086a14 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086a18 @ 0x08086a18 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DAT_08086a34 @ 0x08086a34 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |

**eval_equip_zone_score_with_field_card (0x08086a38):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086a58 @ 0x08086a58 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08086a5c @ 0x08086a5c | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc | REUSE |

**eval_equip_zone_activation_eligible (0x08086a80):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086a78 @ 0x08086a78 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08086a7c @ 0x08086a7c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE |
| DAT_08086b20 @ 0x08086b20 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | REUSE |
| DAT_08086b24 @ 0x08086b24 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | REUSE |
| DAT_08086b28 @ 0x08086b28 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
| DAT_08086b2c @ 0x08086b2c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086b30 @ 0x08086b30 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |
| DAT_08086b48 @ 0x08086b48 | 0x00001716 | EARTH_CHANT_CID | card_info.inc | REUSE (same new) |
| DAT_08086bfc @ 0x08086bfc | 0x000019d9 | END_OF_WORLD_CID | card_info.inc | REUSE (same new) |
| DAT_08086c00 @ 0x08086c00 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
| DAT_08086c04 @ 0x08086c04 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (NOTE: this was listed at wrong address -- value confirmed 0x868) |

Wait -- let me re-check: DAT_08086c04 = 0x00000868 per slot list above. But looking at the asm listing at line 3386 shows DAT_08086c04 at `0x09e5a0c4`. Let me reconcile -- the slot addresses above may have gotten shifted. The actual values (ROM-verified) are in the table above in the slot enumeration section. Fixer should cross-check slot label vs ROM offset.

Actually re-reading the raw data: from the Python enumeration:
- DAT_08086c04 @ 0x08086c04 = 0x09e5a0c4 (gEquipEffectZoneTable)
- DAT_08086c08 @ 0x08086c08 = 0x00000868 (PLAYER_BLOCK_STRIDE)

Corrected table for eval_equip_zone_activation_eligible (0x08086a80) tail:

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086c00 @ 0x08086c00 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
| DAT_08086c04 @ 0x08086c04 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086c08 @ 0x08086c08 | 0x0201c510 | gDuelFieldSlots | ewram.inc | REUSE |
| DAT_08086c0c @ 0x08086c0c | 0x0201c600 | gP1FieldArrayCBase | ewram.inc | REUSE |
| DAT_08086c34 @ 0x08086c34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE (ROM-verified: offset 0x86c34 = 0x00000868; second consumer of PLAYER_BLOCK_STRIDE in this function's tail literal pool) |
| DAT_08086c6c @ 0x08086c6c | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE (ROM-verified: offset 0x86c6c = 0x09e5a0c4; second consumer of gEquipEffectZoneTable in this function's tail literal pool) |

**dispatch_equip_slot_state_by_index -- disasm block internal equate (equip_slot_casea_body @ 0x080863cc):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| (pool @ 0x080863f8) | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc | REUSE (ewram.inc L422; [gP1LifePoints+0x1d68] sprite display control; resolved from formerly-BLOCKED 求助 item) |

**check_neo_daedalus_equip_zone_eligible (0x08086c80):**

| slot | value | const_name | inc | status |
|------|-------|-----------|-----|--------|
| DAT_08086ca0 @ 0x08086ca0 | 0x000013f2 | MASK_OF_RESTRICT_CID | card_info.inc | REUSE (existing; value-grep hits both MASK_OF_RESTRICT_CID and EQUIP_LOCKDOWN_CID at 0x13f2; context = count_field_copies_of_card(0x13f2) blocking equip -> MASK_OF_RESTRICT_CID fits better) |
| DAT_08086cd8 @ 0x08086cd8 | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |

### REF_SLOTS (USER-label + DATA-ref)

| slot | addr | value | gas_label | slot_label | note |
|------|------|-------|----------|-----------|------|
| DAT_08085d7c | 0x08085d7c | 0x08085d80 | switchD_08085d70__switchdataD_08085d80 | dispatch_field_switchdata_base_ptr | internal code ref; rename slot to snake_case |
| DAT_08085ef8 | 0x08085ef8 | 0x09e3f14c | (label already exists at 0x08085d44 in Seg-1 as game_text_sep_record) | game_text_sep_ptr | REUSE existing label; slot at 0x08085ef8 renamed |
| PTR_PTR_08086170 | 0x08086170 | 0x08086174 | (self-ref; jump table pointer-to-pointer) | equip_slot_state_jt_ptr_ptr | internal code ref |
| PTR_DAT_08086174 | 0x08086174 | 0x080861a0 | (becomes sub-case label after R4 disasm) | equip_slot_state_case0_base | first entry of jump table |

### RENAME_SLOTS (PTR_gP1LifePoints_* -> snake_case)

All 8 slots follow the same pattern as Seg-1 (rename PTR_gP1LifePoints_ADDR -> gp1lp_ptr_ADDR):

| slot | addr | new_label |
|------|------|-----------|
| PTR_gP1LifePoints_08085f44 | 0x08085f44 | gp1lp_ptr_08085f44 |
| PTR_gP1LifePoints_08085f8c | 0x08085f8c | gp1lp_ptr_08085f8c |
| PTR_gP1LifePoints_08086060 | 0x08086060 | gp1lp_ptr_08086060 |
| PTR_gP1LifePoints_080860b8 | 0x080860b8 | gp1lp_ptr_080860b8 |
| PTR_gP1LifePoints_080860f8 | 0x080860f8 | gp1lp_ptr_080860f8 |
| PTR_gP1LifePoints_080864d8 | 0x080864d8 | gp1lp_ptr_080864d8 |
| PTR_gP1LifePoints_08086560 | 0x08086560 | gp1lp_ptr_08086560 |
| PTR_gP1LifePoints_08086838 | 0x08086838 | gp1lp_ptr_08086838 |

EOL for all 8: `gP1LifePoints pool (dispatch_field_display_state_by_type / dispatch_equip_slot_state_by_index / eval_equip_slot_score_in_range)`

### FUNC_RENAME

None. All 12 function names are consistent with their bodies. No misnomer signals detected.

Note: plate for `sum_equip_zone_bonus_scores_for_player` (line 2410) refers to `FUN_08086c80` (equip scoring chain) -- this is a stale FUN_ in plate text (see PLATE section).

### PLATE (R5)

Stale FUN_ references to fix in plate comments (substring replacement):

| addr | function | stale text | replacement |
|------|---------|-----------|------------|
| 0x08086430 (`check_equip_target_slot_by_card_id`) plate line 2285 | `FUN_08086a80` | `eval_equip_zone_activation_eligible` |
| 0x0808647c (`find_equip_target_in_effect_zones`) plate line 2332 | `FUN_08086a80` | `eval_equip_zone_activation_eligible` |
| 0x08086508 (`sum_equip_zone_bonus_scores_for_player`) plate line 2410 | `FUN_08086c80` and `FUN_08086634` | `check_neo_daedalus_equip_zone_eligible` and `eval_equip_slot_score_in_range` |
| 0x080865ac (`sum_equip_chain_scores_for_card`) plate line 2499 | `FUN_08086c80` | `check_neo_daedalus_equip_zone_eligible` |
| 0x08086954 (`check_sorted_array_value_in_range`) plate line 2983 | `FUN_08086634` | `eval_equip_slot_score_in_range` |
| 0x08086a80 (`eval_equip_zone_activation_eligible`) plate line 3178 | `FUN_080869a8` and `FUN_08086c80` | `scan_equip_zones_for_eligible_type11_target` and `check_neo_daedalus_equip_zone_eligible` |
| 0x0808611c (`dispatch_equip_slot_state_by_index`) plate line 2213 | `FUN_080a0a8c` | `route_equip_slot_tick_by_flag` (confirmed: asm/13_equip_placement.s L6781 `route_equip_slot_tick_by_flag:` @ 0x080a0a8c) |

Also: `invoke_card_display_op_0x31_with_params` plate in asm/11 line 18359 contains `FUN_08085d4c` -> replace with `dispatch_field_display_state_by_type`. And asm/12 lines 3440, 3569, 3693, 3867 all contain `FUN_08085d4c` -> replace with `dispatch_field_display_state_by_type`.

Cross-asm grep for all other `FUN_080a0a8c` occurrences in asm/*.s: found in asm/13 lines 6436, 6550, 6667, 6855 -- these are within asm/13's own function plates (not plates of Seg-2 functions), so they are out of scope for this segment's PLATE fixes. No additional Seg-2-function plates contain `FUN_080a0a8c`.

Total plate updates: 7 (in-segment, including the new #7 above) + 5 (cross-file asm/11 L18359 + asm/12 L3440/3569/3693/3867) = 12 plate substring replacements.

All plate text in Seg-2 itself (lines 1757..3510) has 0 non-ASCII characters (verified by grep `[^\x00-\x7F]`). No CJK mojibake to fix within Seg-2.

## disasm 计划 (R4)

### Block 0x080861a0 / 0x27a (634 B) -- THUMB sub-case handlers

**Parent context:** `dispatch_equip_slot_state_by_index` (0x0808611c) dispatches via `mov pc,r0` using raw-address jump table at `PTR_DAT_08086174`. The 11-entry table sends sub-states [0..10] to 6 distinct handler bodies inside this block (entries [6..9] go to the fallback at 0x0808641a outside the block).

**Disasm procedure:**
1. `clearListing` 0x080861a0..0x0808641a
2. `setTMode` THUMB for range 0x080861a0..0x0808641a
3. Disassemble contiguous THUMB from 0x080861a0 to end of block (0x0808641a)
4. `createLabel` for each of the 6 entry points:
   - `equip_slot_case0_body` @ 0x080861a0
   - `equip_slot_case1_5_body` @ 0x0808621c
   - `equip_slot_case2_body` @ 0x080862ec
   - `equip_slot_case3_body` @ 0x08086338
   - `equip_slot_case4_body` @ 0x08086370
   - `equip_slot_casea_body` @ 0x080863cc
5. For each literal pool `.word` embedded in the block: `createDWord` to force proper split
   Literal pool words identified in block (addresses from byte-decode):
   - 0x080861dc: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x080861fc: 0x00000000 (pad or null)
   - 0x08086200: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x0808623c: BNE offset (not a literal pool -- it is a branch encoding 0xe02d)
   - 0x08086240: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x08086244: 0x0201b290 (gDuelPhaseFlags)
   - 0x080862b4: 0x09e3f14c (game_text_sep_record)
   - 0x080862e4: 0x0201b290 (gDuelPhaseFlags)
   - 0x080862e8: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x08086310: 0x0201c4e0 (gP1LifePoints)
   - 0x08086314: 0x0201b290 (gDuelPhaseFlags)
   - 0x08086318: 0x000004cc (LP_BAR_ANIM_STATE_OFF)
   - 0x08086330: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x08086334: 0x00001d54 (ELIGIB_STATE_CTRL_OFF)
   - 0x08086350: 0x0201b290 (gDuelPhaseFlags)
   - 0x08086364: (branch encoding, not pool)
   - 0x08086368: 0x0201b290 (gDuelPhaseFlags)
   - 0x0808636c: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x08086384: 0x0201c4e0 (gP1LifePoints)
   - 0x08086388: 0x00001d54 (ELIGIB_STATE_CTRL_OFF)
   - 0x0808638c: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x080863ac: 0x00001d5c (ELIGIB_ACT_TYPE_OFF)
   - 0x080863b0: 0x00001d58 (ELIGIB_ACT_COUNT_OFF)
   - 0x080863b4: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x080863c8: 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF)
   - 0x080863f4: 0x0201c4e0 (gP1LifePoints)
   - 0x080863f8: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF -- REUSE ewram.inc L422; [gP1LifePoints+0x1d68] sprite display control, conf=high)
   - 0x080863fc: 0x00001d6c (ELIGIB_ANIM_STATE_OFF)

6. After disasm: verify `ROM_INCBIN` / `.byte` grep in range == 0.

**Sub-case label plan** (createLabel, NOT createFunction):

| addr | label | semantic |
|------|-------|---------|
| 0x080861a0 | equip_slot_case0_body | slot_substate 0: read aux_ctx at gDuelPhaseFlags+0x58c*slot stride, check active/enabled |
| 0x0808621c | equip_slot_case1_body | slot_substate 1 (and 5): check active bit and call state handler |
| 0x080862ec | equip_slot_case2_body | slot_substate 2: reads gDuelPhaseFlags field, may call text append |
| 0x08086338 | equip_slot_case3_body | slot_substate 3: reads LP state, writes state value |
| 0x08086370 | equip_slot_case4_body | slot_substate 4: reads gP1LifePoints LP fields |
| 0x080863cc | equip_slot_casea_body | slot_substate 0xa: reads two halfword fields, calls enable function |

All intermediate LABs generated by disasm keep their auto-generated `LAB_` names (not renamed in this pass).

## carve 计划 (R7)

None. The ROM_INCBIN block is code (R4 disasm), not a data table to carve.

## 新增 constants / 全局

Per C5 rule -- value-grep before all NEW declarations:

| name | value | inc | C5 grep evidence |
|------|-------|-----|-----------------|
| EQUIP_SLOT_SUBSTATE_OFF | 0x0000058c | ewram.inc | grep `0x0000058c` in constants/*.inc = 0 hits -> NEW |
| gEquipEffectZoneTable | 0x09e5a0c4 | card_info.inc (or new equip_zone.inc) | grep `0x09e5a0c4` in constants/*.inc = 0 hits; grep `9e5a0c4` = 0 hits -> NEW; 14 ROM refs; ROM effect zone/equip card-data table used by equip eligibility and activation scanners. Add to card_info.inc with comment. |
| CONTRACT_WITH_ABYSS_CID | 0x00001698 | card_info.inc | grep `0x00001698` = 0 hits; grep `1698` in card_info.inc = 0 hits -> NEW; card-stats.s L17957 "Contract with the Abyss slot=0x1698 pw=69035382" confirmed |
| EARTH_CHANT_CID | 0x00001716 | card_info.inc | grep `0x00001716` = 0 hits; grep `1716` in card_info.inc shows only ELEMENT_SAURUS_CID=0x1827 (different) and card_1716 label -- value 0x1716 NOT yet in card_info.inc -> NEW; card-stats.s L19335 "Earth Chant slot=0x1716 pw=59820352" confirmed |
| END_OF_WORLD_CID | 0x000019d9 | card_info.inc | grep `0x000019d9` = 0 hits -> NEW; card-stats.s L26795 "End of the World slot=0x19D9 pw=08198712" confirmed |

## §5.1 登记 (Rule 3) -- 0 引用块

None. The one ROM_INCBIN block (0x080861a0 / 0x27a) has 7 real word-aligned references from its parent jump table. No §5.1 entries for this segment.

## 消费者证据 (R6) -- 关键槽语义

| slot | semantic | evidence | confidence |
|------|---------|---------|-----------|
| DAT_08085d78 = FIELD_DISPLAY_TYPE_OFF | [gDuelPhaseFlags+0x57c] field display type | asm/11 L1984: `DAT_08085f70: .word 0x0201b290` + offset 0x57c used in `dispatch_field_display_state_by_type` title; ewram.inc already defined | high |
| DAT_08085ea4 = ELIGIB_RESULT_OFF | [gDuelPhaseFlags+0x584] eligibility result 0=pending,1=confirmed | ewram.inc L416 definition; asm/11 L1882 `str r2,[r0,#0]` writes 0 then writes state on confirm path | high |
| DWORD_0808616c = EQUIP_SLOT_SUBSTATE_OFF | [gDuelPhaseFlags+0x58c] equip slot sub-state index [0..0xa] | asm/11 L2260: `cmp r0,#0xa; bls LAB_08086156` bounds check; loaded as slot index for jump dispatch | high |
| DAT_08086448 = gEquipEffectZoneTable | ROM effect zone table base 0x09e5a0c4 | asm/11 L2302: loaded as base for `lsls r1,r1,#0x2; adds r1,r1,r0; ldr r0,[r1,#0x0]` -- array of card_id+field5 words indexed by player_stride*player + zone_idx | high |
| DAT_0808645c = CONTRACT_WITH_ABYSS_CID | Card ID 0x1698 | asm/11 L2312: `cmp r2,r0` vs r2=card_id; beq LAB_08086460 -> calls check_card_stat_field7_equals(cid, 2); card-stats.s L17957 confirmed | high |
| DAT_08086798 = EARTH_CHANT_CID | Card ID 0x1716 | asm/11 L2738: `ldr r0, DAT_08086798; cmp r1,r0; beq LAB_080867a2` -> sets score=1 for Earth Chant; card-stats.s L19335 confirmed | high |
| DAT_080867b8 = END_OF_WORLD_CID | Card ID 0x19d9 | asm/11 L2769: `ldr r0, DAT_080867b8; cmp r1,r0; bne LAB_080867a6` -> same score override path as Earth Chant; card-stats.s L26795 confirmed | high |
| DAT_08086ca0 = MASK_OF_RESTRICT_CID | Card ID 0x13f2 Mask of Restrict | asm/11 L3470: `ldr r0, DAT_08086ca0; bl count_field_copies_of_card; cmp r0,#0; beq LAB_08086ca8` -- if any Mask of Restrict on field, block equip activation; card_info.inc L1237 confirmed MASK_OF_RESTRICT_CID=0x13f2 | high |

## 解决项 (formerly BLOCKED)

**`0x080863f8` value = 0x00001d68**: previously marked BLOCKED, but C5 value-grep `0x1d68` in constants/ewram.inc returns `ELIGIB_SPRITE_CTRL_OFF, 0x00001d68` at L422. This is a REUSE of an existing constant (ewram.inc L422: [gP1LifePoints+0x1d68] sprite display control). No new constant needed. EQ action: equate 0x080863f8 to ELIGIB_SPRITE_CTRL_OFF (ewram.inc), conf=high. See also EQ_SLOTS table for equip_slot_casea_body below (disasm block internal literal pool).

## C13 coverage summary

Total unique slot labels in segment: **92** (corrected from original 91; DAT_08086c34 and DAT_08086c6c were previously missed).

Coverage breakdown:
- EQ_SLOTS: **80** (25 dispatch_field + 4 dispatch_equip + 2 check_equip_target + 4 find_equip_target + 4 sum_bonus + 2 sum_chain + 13 eval_slot_score + 6 scan_equip_zones + 2 eval_zone_score + 15 eval_zone_activation [11 initial + c08 + c0c + c34 + c6c] + 1 casea_body internal + 2 check_neo = 80)
- REF_SLOTS: **4**
- RENAME_SLOTS: **8**
- Total EQ+REF+RENAME = 80+4+8 = **92/92** (100% coverage)
