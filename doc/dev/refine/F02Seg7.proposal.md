# Refine Proposal: F02Seg7  [0x0803217c..0x08032e80)

## 段测绘

- 函数入口: 23 个 (0x0803217c..0x08032e5c)
  | addr       | name                                        |
  |------------|---------------------------------------------|
  | 0x0803217c | clear_zone_slot_chain_refs                  |
  | 0x08032194 | erase_slot_from_zone_array_by_type          |
  | 0x08032280 | dispatch_card_placement_by_zone_type        |
  | 0x08032358 | classify_card_effect_category               |
  | 0x080324b4 | find_equip_slot_by_card_id                  |
  | 0x08032500 | find_field_slot_idx_by_card_id              |
  | 0x08032548 | test_slot_has_active_card                   |
  | 0x0803259c | check_slot_equip_eligible_by_type_and_id    |
  | 0x080325dc | check_card_equip_eligibility_in_field       |
  | 0x08032654 | count_available_effect_zones                |
  | 0x0803279c | count_field_copies_of_card                  |
  | 0x08032904 | count_zones_by_card_and_mode                |
  | 0x08032960 | count_equip_eligible_slots_for_player       |
  | 0x08032a6c | count_equip_eligible_slots_both_players     |
  | 0x08032a8c | find_best_slot_for_card_by_player           |
  | 0x08032b98 | find_best_slot_atk_across_players           |
  | 0x08032bc8 | count_paired_slots_with_field5              |
  | 0x08032c94 | count_paired_slots_with_field5_default      |
  | 0x08032ca4 | count_paired_slots_both_sides               |
  | 0x08032ccc | count_equipped_paired_slots_for_player      |
  | 0x08032d1c | count_equip_set_activatable_slots_for_player|
  | 0x08032dac | count_equip_zone_slots_matching_card        |
  | 0x08032e20 | count_equip_slots_meeting_atk_threshold     |

- 残留自动名槽: 67 (全为 DAT_/DWORD_, 0 PTR_DAT_/PTR_FUN_)
  - 0x000010a4 (EFFECT_ZONE_PARTITION_OFF) x5
  - 0x000010d0 (EFFECT_ZONE_BITMASK_OFF) x1
  - 0x00000868 (PLAYER_BLOCK_STRIDE) x20
  - 0x0201c510 (gDuelFieldSlots) x18
  - 0x0201c5d8 (gDuelFieldSlots_p2_base) x2
  - 0x0201bc54 (gDuelEffectChainSlots) x1
  - 0x0201bb90 (gEquipChainSlotRefs) x1
  - 0x080321c0 (switchD_0803217c data ptr) x1
  - 0x080322a0 (switchD_0803229a data ptr) x1
  - card_id whitelist slots x17 (classify_card_effect_category x13 + check_card_equip_eligibility_in_field x4)

- ROM_INCBIN / .byte 块: 0 (本段无 incbin 块)

## 数据块分类 (Rule 2/3)

本段无 ROM_INCBIN 或 .byte 块, 跳过 ref-scan 分类步骤。所有 DAT_/DWORD_ 均属函数内 literal pool 槽, 由 EQ/RENAME 覆盖。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

#### 复用现有 inc

| slot | value | const_name | inc_file | slot_label |
|------|-------|------------|----------|------------|
| DAT_08032274 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | erase_slot_zone_player_stride |
| DAT_08032278 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | erase_slot_zone_field_slots |
| DAT_0803222x (skip) | ... | (all same as below) | | |
| DAT_08032230 | 0x0201bc54 | gDuelEffectChainSlots | ewram.inc | erase_slot_effect_chain_slots |
| DAT_080324e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | find_equip_slot_player_stride |
| DAT_080324e8 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | find_equip_slot_field_slots |
| DWORD_0803252c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | find_field_slot_player_stride |
| DWORD_08032530 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | find_field_slot_field_slots |
| DAT_08032594 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | test_slot_active_player_stride |
| DAT_08032598 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | test_slot_active_field_slots |
| DAT_080325d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_slot_equip_elig_player_stride |
| DAT_080325d8 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | check_slot_equip_elig_field_slots |
| DAT_080326e0 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_avail_effect_zones_field_slots |
| DAT_080326e8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_avail_effect_zones_player_stride |
| DAT_08032740 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_avail_effect_zones_field_slots_b |
| DAT_08032744 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_avail_effect_zones_player_stride_b |
| DAT_08032794 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_avail_effect_zones_player_stride_c |
| DAT_08032830 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_field_copies_field_slots |
| DAT_08032838 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_field_copies_player_stride |
| DAT_080328a0 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_field_copies_field_slots_b |
| DAT_080328a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_field_copies_player_stride_b |
| DAT_08032900 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_field_copies_player_stride_c |
| DAT_08032a58 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_equip_elig_field_slots |
| DAT_08032a60 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_elig_player_stride |
| DAT_08032a68 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | count_equip_elig_chain_slot_refs |
| DAT_08032b18 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | find_best_slot_field_slots |
| DAT_08032b20 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | find_best_slot_player_stride |
| DAT_08032b90 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | find_best_slot_field_slots_b |
| DAT_08032b94 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | find_best_slot_player_stride_b |
| DAT_08032c34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_paired_slots_player_stride |
| DAT_08032c38 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_paired_slots_field_slots |
| DAT_08032c8c | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_paired_slots_field_slots_b |
| DAT_08032c90 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_paired_slots_player_stride_b |
| DAT_08032d14 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_paired_player_stride |
| DAT_08032d18 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_equip_paired_field_slots |
| DAT_08032da4 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_equip_set_field_slots |
| DAT_08032da8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_set_player_stride |
| DAT_08032e18 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_equip_zone_field_slots |
| DAT_08032e1c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_zone_player_stride |
| DAT_08032e78 | 0x0201c510 | gDuelFieldSlots    | ewram.inc | count_equip_atk_field_slots |
| DAT_08032e7c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_atk_player_stride |

合计复用 EQ: 40 (PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x18 + gDuelEffectChainSlots x1 + gEquipChainSlotRefs x1)

#### 新建 constants

**1. `duel_field.inc` — EFFECT_ZONE_PARTITION_OFF = 0x000010a4**

- 语义: gDuelFieldSlots 内 effect zone (怪兽区) slot 数组基址偏移; gDuelFieldSlots+0x10a4 = 0x0201d5b4 = 效果区 slot[0] 起始
- ROM ref-scan: raw=18, thumb (0x000010a5)=6; 18 raw refs 散布全文件 (asm L14240/14417/14709/14811/14239等)
- 消费者证据: count_available_effect_zones (L14164), count_equip_eligible_slots_for_player (L14578), find_best_slot_for_card_by_player (L14734), count_field_copies_of_card (L14336) 均注释 "gDuelFieldSlots + player*0x868 + 0x10a4" (高置信度)
- 证据文件: asm/02_text_lp_fieldspell.s L14164/L14578/L14734 plate 注释

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| DAT_0803227c | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | erase_slot_zone_effect_zone_off |
| DAT_080326e4 | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | count_avail_effect_zone_off |
| DAT_08032834 | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | count_field_copies_effect_zone_off |
| DAT_08032a5c | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | count_equip_elig_effect_zone_off |
| DAT_08032b1c | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | find_best_slot_effect_zone_off |

**2. `ewram.inc` — gDuelFieldSlots_p2_base = 0x0201c5d8**

- 语义: gDuelFieldSlots + 0xc8 = P1/P2 side[field9==2] 单槽地址 (slot[10], stride 0x14 x 10 entries = 0xc8); count_available_effect_zones 注释 "slot at 0x0201c5d8" (高置信度)
- ROM ref-scan: raw=24 (asm/02_text_lp_fieldspell.s L14333/14524)
- 证据: asm/02_text_lp_fieldspell.s L14164 plate "gDuelFieldSlots+0xc8=slot[10]"
- 注意 gDuelFieldSlots=0x0201c510, +0xc8=0x0201c5d8; 此地址为 field9==2 路径的固定单槽基址

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| DAT_08032798 | 0x0201c5d8 | gDuelFieldSlots_p2_base | count_avail_effect_zones_p2_slot |
| DAT_080328fc | 0x0201c5d8 | gDuelFieldSlots_p2_base | count_field_copies_p2_slot |

**3. `duel_field.inc` — EFFECT_ZONE_BITMASK_OFF = 0x000010d0**

- 语义: gDuelFieldSlots+0x10d0 = gP1LifePoints+0x10d0 = 0x0201d5b0 = 效果区域 occupation bitmask word (4B); count_equip_eligible_slots_for_player 中 `r10+0x10d0` 读该位域; count_monster_slots_by_state_all (Seg-8 L15646) 注释 "gP1LifePoints[+0x10d0] bonus flag"
- ROM ref-scan: raw=45 (asm L14713/15711/15790 等多处)
- 消费者证据: asm/02_text_lp_fieldspell.s L14645-14650: `ldr r0,DAT_08032a64(=0x10d0); add r0,r10; ldr r0,[r0]; ands r0,#1; cmp r0,#0; beq LAB_08032a48` — 读 bitmask bit0 判断是否跳过 (高置信度)
- 注: gDuelFieldSlots(0x0201c510)+0x10a0 = gP1LifePoints(0x0201c4e0)+0x10d0 = 0x0201d5b0; EFFECT_ZONE_BITMASK_OFF 相对 gDuelFieldSlots 是 0x10d0-0x30+0x30=0x10d0; 在代码中 r10=gDuelFieldSlots-0x30, 故 r10+0x10d0=gDuelFieldSlots+0x10a0

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| DAT_08032a64 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | count_equip_elig_bitmask_off |

合计新建 EQ: 8 (EFFECT_ZONE_PARTITION_OFF x5 + gDuelFieldSlots_p2_base x2 + EFFECT_ZONE_BITMASK_OFF x1)

**总 EQ: 48**

---

### RENAME_SLOTS (纯改名 + EOL)

#### switchD 表指针 (内部 ROM 地址)

| slot | addr | gas_label | EOL |
|------|------|-----------|-----|
| DAT_080321bc | 0x080321bc | erase_slot_zone_switch_data | switchD dispatch table for erase_slot_from_zone_array_by_type |
| DAT_0803229c | 0x0803229c | dispatch_card_placement_switch_data | switchD dispatch table for dispatch_card_placement_by_zone_type |

#### card_id whitelist 槽 — classify_card_effect_category (函数 0x08032358)

命名约定: `classify_card_effect_category_cid_<hex4>` (沿用 Seg-4 `<func>_cid_<hex4>` 约定)

| slot | value | slot_label | EOL |
|------|-------|------------|-----|
| DAT_0803238c | 0x00001348 | classify_card_effect_category_cid_1348 | card_id 0x1348 effect category whitelist entry |
| DAT_08032390 | 0x000010f5 | classify_card_effect_category_cid_10f5 | card_id 0x10f5 effect category whitelist entry |
| DAT_080323a4 | 0x000010f3 | classify_card_effect_category_cid_10f3 | card_id 0x10f3 effect category whitelist entry |
| DAT_080323c0 | 0x00001345 | classify_card_effect_category_cid_1345 | card_id 0x1345 effect category whitelist entry |
| DAT_080323d4 | 0x00001346 | classify_card_effect_category_cid_1346 | card_id 0x1346 effect category whitelist entry |
| DAT_080323fc | 0x0000169f | classify_card_effect_category_cid_169f | card_id 0x169f effect category whitelist entry |
| DAT_08032400 | 0x000014d1 | classify_card_effect_category_cid_14d1 | card_id 0x14d1 effect category whitelist entry |
| DAT_08032404 | 0x00001349 | classify_card_effect_category_cid_1349 | card_id 0x1349 effect category whitelist entry |
| DAT_08032408 | 0x0000149c | classify_card_effect_category_cid_149c | card_id 0x149c effect category whitelist entry |
| DAT_0803241c | 0x0000150b | classify_card_effect_category_cid_150b | card_id 0x150b effect category whitelist entry |
| DAT_08032438 | 0x0000187f | classify_card_effect_category_cid_187f | card_id 0x187f effect category whitelist entry |
| DAT_0803243c | 0x0000175e | classify_card_effect_category_cid_175e | card_id 0x175e effect category whitelist entry |
| DAT_08032450 | 0x000018ff | classify_card_effect_category_cid_18ff | card_id 0x18ff effect category whitelist entry |

#### card_id 槽 — check_card_equip_eligibility_in_field (函数 0x080325dc)

命名约定: `check_card_equip_eligibility_in_field_cid_<hex4>`

| slot | value | slot_label | EOL |
|------|-------|------------|-----|
| DAT_0803263c | 0x0000166c | check_card_equip_eligibility_in_field_cid_166c | same-name field limit guard (max 1 copy) |
| DAT_08032640 | 0x000012bf | check_card_equip_eligibility_in_field_cid_12bf | chain eligibility guard: check_value_in_slot_chain zone=0xb |
| DAT_08032644 | 0x0000148e | check_card_equip_eligibility_in_field_cid_148e | summon restriction type==1 copy check A |
| DAT_08032648 | 0x000014da | check_card_equip_eligibility_in_field_cid_14da | summon restriction type==1 copy check B |

**总 RENAME: 19** (2 switchD ptr + 13 classify_cid + 4 equip_elig_cid)

---

### PLATE (R5; 全 ASCII 重写)

5 个函数 plate 含 stale FUN_ 引用需整段重写 (setPlateComment):

**1. dispatch_card_placement_by_zone_type (0x08032280)**
- 替换: FUN_08037630 -> place_equip_card_if_type_matches
- 替换: FUN_08031630 -> append_slot_ref_to_equip_array
- 替换: FUN_08031578 -> insert_slot_ref_into_hand_array
- 替换: FUN_080315f8 -> append_slot_ref_to_hand_array
- 替换: FUN_08036cb8 -> place_card_into_graveyard_slot
- 替换: FUN_08036d08 -> place_card_into_graveyard_slot_with_seq
- 新 plate (ASCII):
  Routes a card placement to the appropriate zone handler by zone_type (r1). 6-case switch + default dual-branch: case 0xb=equip-type-check insert (place_equip_card_if_type_matches), case 0xc=direct equip insert (append_slot_ref_to_equip_array), case 0xd=hand insert or append (insert_slot_ref_into_hand_array / append_slot_ref_to_hand_array), case 0xe=graveyard check insert (place_card_into_graveyard_slot), case 0xf=graveyard insert with seq (place_card_into_graveyard_slot_with_seq), case 0x10=general branch; default<=4=monster zone (place_card_into_monster_zone_slot), default>4=spell/trap zone (place_card_into_spelltrap_zone_slot). After switch, optionally calls clear_equip_refs_for_leaving_slot and clear_equip_chain_refs_for_slot_zone. r0=u8 player_id, r1=u8 zone_type, r2=u8 flags, r3=ptr slot_ref. Returns void. indeg=10.

**2. classify_card_effect_category (0x08032358)**
- 替换: FUN_0803412c -> check_card_matches_active_effect_slot
- 替换: FUN_0804074c -> tick_card_effect_category_display_seq
- 新 plate (ASCII):
  Maps card_id (r0) to an effect category code [1..0x17] (23 categories) via multi-level cmp/beq tree. Hardcoded whitelist: 0x1348/0x10f5/0x10f3/0x10f1/0x10f2/0x1345/0x1346/0x169f/0x14d1/0x1349/0x149c/0x150b/0x175e/0x187f/0x18ff and others. card_id not in whitelist -> returns 0. r0=u16 card_id. Returns u8 effect_category [1..0x17] or 0. Callers: check_card_matches_active_effect_slot, tick_card_effect_category_display_seq, dispatch_equip_pair_sprites_by_state, 0x080c8f48.

**3. check_card_equip_eligibility_in_field (0x080325dc)**
- 替换: FUN_08032960 (×2) -> count_equip_eligible_slots_for_player
- 替换: FUN_08048020 -> render_slot_card_sprite_and_effects
- 替换: FUN_08048364 -> render_slot_card_sprite_with_chaos_equip_check
- 替换: FUN_08099aac -> run_equip_slot_display_update_state_machine
- 替换: FUN_08099e0c -> run_equip_spell_display_state_machine
- 新 plate (ASCII):
  Multi-layer equip eligibility check for a field slot entry ptr (r0). Checks: (1) check_card_field8_is_normal; (2) slot[+0x34] existing equip bind == 0; (3) count_field_copies_of_card(0x166c) == 0 (same-name field limit); (4) if slot[+0x8] nonzero: check_value_in_slot_chain(0x12bf, zone=0xb) == 0; (5) get_card_field_summon_restriction: if type==1 checks copies of 0x148e and 0x14da; (6) check_card_targeted_by_spell_zone_effect. Returns 1 if all pass, 0 on any failure. No write side effects. indeg=6. Callers: count_equip_eligible_slots_for_player, render_slot_card_sprite_and_effects, render_slot_card_sprite_with_chaos_equip_check, run_equip_slot_display_update_state_machine, run_equip_spell_display_state_machine.

**4. count_equip_eligible_slots_for_player (0x08032960)**
- 替换: FUN_08032a6c -> count_equip_eligible_slots_both_players
- 替换: FUN_080490b4 -> tick_duel_field_zone_sprite_update_pipeline
- 替换: FUN_080325dc -> check_card_equip_eligibility_in_field
- 新 plate (ASCII):
  Counts equip-eligible monster-zone slots for player (r0) and card_id (r1). Scans 5 slots at gDuelFieldSlots + player*0x868 + 0x10a4 + slot*0x14 (slot 0..4): card_id match, active flags (bit5/bit1 clear), bitmask check, then calls check_card_equip_eligibility_in_field. Also checks gEquipChainSlotRefs[0]/[4] for matching card_id via separate path. Returns count of eligible slots. Pure query. Callers: count_equip_eligible_slots_both_players, tick_duel_field_zone_sprite_update_pipeline.

**5. count_equip_eligible_slots_both_players (0x08032a6c)**
- 替换: FUN_0808db90 -> dispatch_equip_pair_sprites_by_state
- 替换: FUN_08032960 -> count_equip_eligible_slots_for_player
- 新 plate (ASCII):
  Calls count_equip_eligible_slots_for_player(0, slot_ref) + count_equip_eligible_slots_for_player(1, slot_ref) and returns sum. r0=ptr slot_ref. Returns u32 total eligible slot count (P1+P2). Pure wrapper. Callers: dispatch_equip_pair_sprites_by_state.

**总 PLATE: 5**

---

## carve 计划 (R7)

なし。本段无 ROM_INCBIN。

## disasm 计划 (R4)

なし。本段无误标数据块。

## 新增 constants / 全局

经全 18 个 constants/*.inc 扫描确认无同值常量, 新建 3 项:

**1. `constants/duel_field.inc` 追加 (file 02 Seg-7 additions section)**

```
.equ EFFECT_ZONE_PARTITION_OFF, 0x000010a4  @ gDuelFieldSlots+0x10a4 = effect zone slot array base offset (0x0201d5b4); 18 raw refs
.equ EFFECT_ZONE_BITMASK_OFF,   0x000010d0  @ gDuelFieldSlots+0x10a0 = effect zone occupation bitmask word offset; 45 raw refs
                                             @ (used as: r10=gDuelFieldSlots-0x30; r10+0x10d0=gDuelFieldSlots+0x10a0=0x0201d5b0)
```

**2. `constants/ewram.inc` 追加 (file 02 Seg-7 additions section)**

```
.equ gDuelFieldSlots_p2_base, 0x0201c5d8    @ gDuelFieldSlots+0xc8 = slot[10] base for field9==2 single-slot path; 24 raw refs
```

## §5.1 登记 (Rule 3) — 0 引用块

本段无 ROM_INCBIN 块, §5.1 无新增。

## 消费者证据 (R6)

| 常量/全局 | 消费者函数 | file:line | 置信度 |
|-----------|-----------|-----------|--------|
| EFFECT_ZONE_PARTITION_OFF=0x10a4 | count_available_effect_zones | asm/02_text_lp_fieldspell.s L14164 plate: "gDuelFieldSlots + player*0x868 + 0x10a4" | high |
| EFFECT_ZONE_PARTITION_OFF=0x10a4 | count_equip_eligible_slots_for_player | asm/02_text_lp_fieldspell.s L14578 plate: "zone_offset=0x10a4" | high |
| EFFECT_ZONE_PARTITION_OFF=0x10a4 | find_best_slot_for_card_by_player | asm/02_text_lp_fieldspell.s L14734 plate: "equip_zone_offset=0x10a4" | high |
| EFFECT_ZONE_PARTITION_OFF=0x10a4 | count_field_copies_of_card | asm/02_text_lp_fieldspell.s L14336 plate: "0x10a4=effect zone partition offset" | high |
| EFFECT_ZONE_BITMASK_OFF=0x10d0 | count_equip_eligible_slots_for_player | asm/02_text_lp_fieldspell.s L14645-14650: ldr r10+0x10d0; ands r0,#1; beq skip => bitmask bit0 field occupation test | high |
| EFFECT_ZONE_BITMASK_OFF=0x10d0 | count_monster_slots_by_state_all (Seg-8) | asm/02_text_lp_fieldspell.s L15646 plate: "gP1LifePoints[+0x10d0] bonus flag" | high |
| gDuelFieldSlots_p2_base=0x0201c5d8 | count_available_effect_zones | asm/02_text_lp_fieldspell.s L14164 plate: "gDuelFieldSlots+0xc8=slot[10]" | high |
| gDuelFieldSlots_p2_base=0x0201c5d8 | count_field_copies_of_card | asm/02_text_lp_fieldspell.s L14336 plate: "gDuelFieldSlots_side1=0x0201c5d8" | high |
| classify_card_effect_category card_id whitelist | classify_card_effect_category | asm/02_text_lp_fieldspell.s L13724 plate + L13754-13860 cmp/beq tree | high |
| check_card_equip_eligibility_in_field card_ids | check_card_equip_eligibility_in_field | asm/02_text_lp_fieldspell.s L14103 plate: "card_ids=0x166c/0x12bf/0x148e/0x14da" | high |

## 求助

None. 所有槽语义均有消费者证据支撑, 置信度全 high。

---

## 自检结果

1. **EQ value 核对**: ROM 字节验证
   - 0x0201c510 @0x08032278: ROM = `10c50102` LE = 0x0201c510 ✓
   - 0x00000868 @0x08032274: ROM = `68080000` LE = 0x00000868 ✓
   - 0x0201bc54 @0x08032230: ROM = `54bc0102` LE = 0x0201bc54 ✓
   - 0x000010a4 @0x0803227c: ROM = `a4100000` LE = 0x000010a4 ✓
   - 0x000010d0 @0x08032a64: ROM = `d0100000` LE = 0x000010d0 ✓
   - 0x0201bb90 @0x08032a68: ROM = `90bb0102` LE = 0x0201bb90 ✓
   - 0x0201c5d8 @0x08032798: ROM = `d8c50102` LE = 0x0201c5d8 ✓

2. **switchD 表内容核对**: 
   - 0x080321c0 @0x080321bc ✓ (switchD caseD data table ptr)
   - 0x080322a0 @0x0803229c ✓ (switchD case data table ptr)

3. **carve 无**: 不涉及 THUMB fn-ptr 检查

4. **plate/EOL 文本 ASCII 审查**: 所有 plate 文本均为纯英文 ASCII, 无 CJK 字符 ✓

5. **槽名规范**: 所有 slot_label 满足 `^[a-z][a-z0-9_]+$`; 同函数多 PLAYER_BLOCK_STRIDE 槽用 `_b/_c` 后缀区分碰撞 ✓

6. **C13 残留覆盖**: 67 DAT_/DWORD_ 槽 = EQ 48 + RENAME 19 = 67; 全覆盖 ✓

7. **C5 值去重**: 扫描全 18 个 constants/*.inc 确认 0x000010a4/0x000010d0/0x0201c5d8 均无现有定义 ✓

8. **§5.1**: 本段无 ROM_INCBIN, 无需登记

9. **新建 constants 孤儿检查**: 3 项新常量在段内均有槽持该值 ✓
