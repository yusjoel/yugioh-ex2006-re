# Refine Proposal: F06-Seg-1  [0x080537c0..0x080541cc)

## 段测绘

- 函数入口: x22
  - 0x080537c0  dispatch_equip_eligibility_by_slot_equip_flag
  - 0x080537dc  check_equip_slot_eligible_by_side_setcode_and_activation
  - 0x08053850  check_equip_slot_eligible_by_setcode_and_valid_flag
  - 0x080538a8  check_equip_slot_eligible_by_whitelist_or_type_dispatch
  - 0x080538e8  check_equip_slot_eligible_by_type_and_chain
  - 0x08053af8  check_equip_slot_eligible_by_zone_chain_scan
  - 0x08053b84  check_equip_slot_eligible_by_opposite_side_and_effect_ctx
  - 0x08053c00  check_equip_slot_eligible_by_field6_and_full_prereqs
  - 0x08053c70  check_equip_slot_eligible_by_side_mismatch_and_field8_7
  - 0x08053cc4  check_equip_slot_eligible_for_gravekeeper_series
  - 0x08053d40  check_equip_slot_eligible_by_equippable_and_monster_space
  - 0x08053d88  check_equip_slot_eligible_by_opposite_side_zone_chain
  - 0x08053e14  check_equip_slot_eligible_by_type_and_space
  - 0x08053e6c  check_equip_slot_eligible_by_setcode_dedup_only
  - 0x08053ebc  check_equip_slot_eligible_by_same_side_and_field8_9
  - 0x08053f10  check_equip_slot_eligible_by_side_match_and_type
  - 0x08053f5c  check_equip_slot_eligible_with_score_bound_and_chain_scan
  - 0x0805402c  check_equip_slot_eligible_by_opposite_side_field6_and_type
  - 0x08054088  check_equip_slot_eligible_by_field6_10_and_equippable
  - 0x080540ec  check_equip_slot_eligible_by_type_mismatch_and_eligible
  - 0x08054118  dispatch_equip_slot_eligible_by_type_prereqs_or_setcode
  - 0x08054154  check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible

- 残留自动名槽: x47 (全为 DAT_/DWORD_ 文字量池)
  - 0x08053840  DAT_08053840  = 0x00000868  x19 instances of this value
  - 0x08053844  DAT_08053844  = 0x0201c510  x19 instances of this value
  - 0x080539b4  DAT_080539b4  = 0xffff803f  x2 instances
  - 0x08053bf4  DAT_08053bf4  = 0x0201bb90  x1
  - 0x08053d30  DWORD_08053d30 = 0x0000158c  x1
  - 0x08053e08  DAT_08053e08  = 0x0804f551  x1 (fn-ptr)
  - 0x08053ff8  DAT_08053ff8  = 0x0201b290  x1
  - 0x08053ffc  DAT_08053ffc  = 0x000004cc  x1
  - 0x08054000  DAT_08054000  = 0x000004f4  x1
  - 0x08054138  DWORD_08054138 = 0x00001706  x1 (equip_flag discriminator)
  - (plus duplicates of 0x868 and 0x0201c510 totaling 47 slots)

- ROM_INCBIN / .byte 块: 0 (ref-scan 确认无)

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

Seg-1 无 ROM_INCBIN/.byte 块，此节 N/A。

Python ref-scan 确认 0 blocks:
  ROM_INCBIN in [0x080537c0, 0x080541cc): count=0  [confirmed]

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

所有 47 槽均为文字量池常量。按唯一值分组：

**值 0x00000868 (x19) -- 复用 ewram.inc PLAYER_BLOCK_STRIDE**
ROM 字节核验: all OK (python struct.unpack_from verified)

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08053840 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_setcode_and_activation_stride |
| DAT_08053898 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_and_valid_flag_stride |
| DAT_080539ac | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_and_chain_stride_b |
| DAT_08053a28 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_and_chain_stride_c |
| DAT_08053ad8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_and_chain_stride_d |
| DAT_08053b24 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_zone_chain_scan_stride_b |
| DAT_08053b7c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_zone_chain_scan_stride_c |
| DAT_08053bec | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_and_effect_ctx_stride |
| DAT_08053c60 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field6_and_full_prereqs_stride |
| DAT_08053cb4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_mismatch_and_field8_7_stride |
| DWORD_08053d28 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_for_gravekeeper_series_stride_b |
| DAT_08053e00 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_zone_chain_stride |
| DWORD_08053eac | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_setcode_dedup_only_stride |
| DAT_08053f00 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_same_side_and_field8_9_stride |
| DAT_08053f4c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_match_and_type_stride |
| DAT_08053ff0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_score_bound_and_chain_scan_stride |
| DWORD_08054078 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_opposite_side_field6_and_type_stride |
| DWORD_080540dc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_field6_10_and_equippable_stride |
| DWORD_080541bc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible_stride |

**值 0x0201c510 (x19) -- 复用 ewram.inc gDuelFieldSlots**
ROM 字节核验: all OK

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08053844 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_setcode_and_activation_slots |
| DAT_0805389c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_setcode_and_valid_flag_slots |
| DAT_080539b0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_and_chain_slots_b |
| DAT_08053a2c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_and_chain_slots_c |
| DAT_08053adc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_and_chain_slots_d |
| DAT_08053b28 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_zone_chain_scan_slots_b |
| DAT_08053b80 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_zone_chain_scan_slots_c |
| DAT_08053bf0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_side_and_effect_ctx_slots |
| DAT_08053c64 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_field6_and_full_prereqs_slots |
| DAT_08053cb8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_mismatch_and_field8_7_slots |
| DWORD_08053d2c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_for_gravekeeper_series_slots |
| DAT_08053e04 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_side_zone_chain_slots |
| DWORD_08053eb0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_setcode_dedup_only_slots |
| DAT_08053f04 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_same_side_and_field8_9_slots |
| DAT_08053f50 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_match_and_type_slots |
| DAT_08053ff4 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_score_bound_and_chain_scan_slots |
| DWORD_0805407c | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_opposite_side_field6_and_type_slots |
| DWORD_080540e0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_field6_10_and_equippable_slots |
| DWORD_080541c0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible_slots |

**值 0xffff803f (x2) -- 复用 gl_scrollbar.inc SCROLLBAR_CLEAR_BITS_14_6**
ROM 字节核验: 0x080539b4 OK, 0x08053ae0 OK
用途: `ands r0, mask; orrs r0, r1; strh r0,[r2,#4]` -- clears bits[14:6] of slot[+4] halfword then ORs in new set_code_a value. 高置信度 (file:asm/06_equip_eligibility_b.s:line 275~278,asm line 440~442 确认用法). C5 严格去重: 同值 SCROLLBAR_CLEAR_BITS_14_6 已在 gl_scrollbar.inc 存在, 掩码非偏移标量不重建, 直接复用.
EOL: `clear bits[14:6] mask (shared literal SCROLLBAR_CLEAR_BITS_14_6); here extracts setcode-A field`

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_080539b4 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | check_equip_slot_eligible_by_type_and_chain_setcode_clear_b |
| DAT_08053ae0 | 0xffff803f | SCROLLBAR_CLEAR_BITS_14_6 | check_equip_slot_eligible_by_type_and_chain_setcode_clear_d |

**值 0x0201bb90 (x1) -- 复用 ewram.inc gEquipChainSlotRefs**
ROM 字节核验: 0x08053bf4 = 0x0201bb90 OK
消费者: check_equip_slot_eligible_by_opposite_side_and_effect_ctx (asm/06:line 584-589) 读 [+0x0](activation_player) 和 [+0x1c](context_slot_ref). 与 asm/02:check_value_in_effect_context_chain plate 一致 (confidence high, file:asm/02_text_lp_fieldspell.s:line 8098).

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08053bf4 | 0x0201bb90 | gEquipChainSlotRefs | check_equip_slot_eligible_by_opposite_side_and_effect_ctx_chain_refs |

**值 0x0000158c (x1) -- 新建 GRAVEKEEPERS_CANNONHOLDER_CID (card_info.inc)**
ROM 字节核验: 0x08053d30 = 0x0000158c OK
card-stats.s 核验: card_1168 = "Gravekeeper's Cannonholder" slot=0x158C pw=99877698 (file:data/card-stats.s:line 15199, high conf). 排除: GRAVEKEEPERS_SERVANT_CID=0x131d, GRAVEKEEPERS_ASSAILANT_CID=0x158d 均不同值. 0x158c 在 card_info.inc 中不存在 (grep 确认).

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DWORD_08053d30 | 0x0000158c | GRAVEKEEPERS_CANNONHOLDER_CID | check_equip_slot_eligible_for_gravekeeper_series_excl_cid |

**值 0x0201b290 (x1) -- 复用 ewram.inc gDuelPhaseFlags**
ROM 字节核验: 0x08053ff8 OK. 676 raw ROM refs. 用于 check_equip_slot_eligible_with_score_bound_and_chain_scan 读取 chain list count (file:asm/06:line 1168-1175).

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08053ff8 | 0x0201b290 | gDuelPhaseFlags | check_equip_slot_eligible_with_score_bound_and_chain_scan_phase_flags |

**值 0x000004cc (x1) -- 复用 ewram.inc LP_BAR_ANIM_STATE_OFF**
ROM 字节核验: 0x08053ffc OK. 用于读 [gDuelPhaseFlags+0x4cc] 作为 chain list entry count (file:asm/06:line 1168-1172).

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08053ffc | 0x000004cc | LP_BAR_ANIM_STATE_OFF | check_equip_slot_eligible_with_score_bound_and_chain_scan_chain_cnt_off |

**值 0x000004f4 (x1) -- 复用 ewram.inc CHAIN_NODE_CARD_ARR_OFF**
ROM 字节核验: 0x08054000 OK. 用于 [gDuelPhaseFlags+0x4f4] card ptr array iteration (file:asm/06:line 1177-1178).

| slot | value | const_name | slot_label |
|------|-------|-----------|-----------|
| DAT_08054000 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | check_equip_slot_eligible_with_score_bound_and_chain_scan_card_arr_off |

### REF_SLOTS (USER-label + DATA-ref)

**fn-ptr 槽 0x08053e08 = 0x0804f551**
值 0x0804f551 = check_equip_slot_eligible_triple_predicate + 1 (THUMB fn-ptr, odd addr).
ROM 字节核验: 0x08053e08 = 0x0804f551 OK. 函数头 0x0804f550: ROM bytes = 70b5061c (push {r4,r5,r6,lr}) -- valid THUMB prologue.
ref-scan: raw 0x0804f551 = 11 refs in ROM; 函数定义: asm/05_equip_eligibility_a.s:line 13830.
用途: count_zone_pair_hits_with_fn_ptr 的 fn-ptr 参数 (file:asm/06:line 906 `ldr r1, DAT_08053e08`). high conf.

| slot | target | gas_label | slot_label |
|------|--------|-----------|-----------|
| DAT_08053e08 | check_equip_slot_eligible_triple_predicate+1 | check_equip_slot_eligible_triple_predicate | check_equip_slot_eligible_by_opposite_side_zone_chain_fn_ptr |

### RENAME_SLOTS (纯改名 + EOL)

**DWORD_08054138 = 0x00001706 -- equip_flag discriminator**
不是 CID: TORPEDO_FISH_CID = 0x1706 (card_info.inc:line 926) 同值但不同实体 (equip flag vs card ID). 按 C5 "state_code 碰 CID --> RENAME-only". 值被用作 slot[+0xa] halfword 等值比较: equip_flag == 0x1706 => type_then_prereqs 路径; equip_flag == 0x1709 (=0x1706+3) => setcode_and_prereqs 路径 (file:asm/06:line 1386-1391). 语义: equip slot type-discriminator code A; 置信 med (未能完全解析 slot[+0xa] 完整枚举, 但 dispatch 逻辑清晰).

| slot | slot_label | eol_ascii |
|------|-----------|-----------|
| DWORD_08054138 | dispatch_equip_slot_eligible_by_type_prereqs_or_setcode_flag_a | equip_flag=0x1706: type_then_prereqs path; +3=0x1709: setcode_and_prereqs path (med-conf) |

### FUNC_RENAME (误名订正)

无 -- 所有 22 个函数名语义清晰, 与函数体操作一致。无误名信号。

### PLATE (R5)

**P1: dispatch_equip_slot_eligible_by_type_prereqs_or_setcode (0x08054118)**
现有 plate (line 1380): CJK mojibake (非 ASCII 检测确认). 须整段 ASCII 重写.
消费者证据: asm/06:line 1381-1411 实现逻辑 (high conf).

新 plate (全 ASCII):
```
Equip slot eligibility 3-way dispatch by slot[+0xa] equip flag. Reads slot[+0xa] halfword: if ==DISPATCH_FLAG_A (0x1706) calls check_equip_slot_eligible_by_type_then_prereqs; if ==DISPATCH_FLAG_A+3 (0x1709) calls check_equip_slot_eligible_by_setcode_and_prereqs; else calls check_equip_slot_eligible_by_card_id_tree. Transparent return (Sub-case E).
Params: r0=ptr card_slot; r1=u32 player_id [0..1]; r2=u32 zone_slot_idx
Returns: r0=u32 bool (1=eligible, 0=rejected; Sub-case E)
Side effects: none
```

**P2 (EOL line 1024): stale FUN_08054e5c in check_equip_slot_eligible_by_same_side_and_field8_9 plate**
FUN_08054e5c 现名 = check_equip_slot_eligible_by_setcode_prereqs_all_slots (asm/06:line 3419, high conf).
替换: substring `FUN_08054e5c` -> `check_equip_slot_eligible_by_setcode_prereqs_all_slots` in that EOL comment.

**P3 (EOL line 1482): stale FUN_08054e5c in check_equip_slot_eligible_by_side_setcode_prereqs_and_type plate**
同上, 同 FUN_08054e5c -> check_equip_slot_eligible_by_setcode_prereqs_all_slots.

## carve 计划 (R7) -- rom.s incbin 切割

N/A -- Seg-1 无 ROM_INCBIN 块。

## disasm 计划 (R4)

N/A -- Seg-1 无 ROM_INCBIN 可 disasm, 无 switch 跳转表 (这三个 switchD 都在 Seg-8/10).

## 新增 constants / 全局

### card_info.inc 新增

1. `GRAVEKEEPERS_CANNONHOLDER_CID = 0x0000158c`
   - Gravekeeper's Cannonholder (pw=99877698; data/card-stats.s card_1168 slot=0x158C)
   - asm/06:line 765 用于排除该卡 (high conf)
   - card_info.inc 中相邻: GRAVEKEEPERS_ASSAILANT_CID=0x158d (line 663), GRAVEKEEPERS_SERVANT_CID=0x131d (line 658)

注: 0xffff803f 掩码复用 gl_scrollbar.inc:SCROLLBAR_CLEAR_BITS_14_6, 不在 card_info.inc 新建.

### ewram.inc 新增

2. `EQUIP_CTX_PLAYER_OFF = 0x00000000`
   - [gEquipChainSlotRefs+0x0] activation player id field
   - asm/06:line 585-586 ldr/cmp r0,[r1,#0x0] vs r5(player_id) (high conf)
   - asm/02_text_lp_fieldspell.s:line 8098 plate 确认: "activation_player_offset=0"

3. `EQUIP_CTX_SLOT_REF_OFF = 0x0000001c`
   - [gEquipChainSlotRefs+0x1c] context zone slot reference field
   - asm/06:line 588-589 ldr/cmp r0,[r1,#0x1c] vs r4(zone_idx) (high conf)
   - asm/02_text_lp_fieldspell.s:line 8098 plate 确认: "context_slot_ref_offset=0x1c"

## §5.1 登记 (Rule 3) -- 0 引用块

Seg-1 无 ROM_INCBIN 块, §5.1 N/A.

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 常量/槽 | 消费函数 | file:line | 证据 | 置信度 |
|---------|---------|-----------|------|--------|
| PLAYER_BLOCK_STRIDE=0x868 | check_equip_slot_eligible_by_side_setcode_and_activation | asm/06:82-83 | ldr stride; muls player_id; gDuelFieldSlots index | high |
| gDuelFieldSlots=0x0201c510 | 同上 + 其余 18 函数 | asm/06:83-84 | adds r0,r1; ldr base; adds slot ptr | high |
| SCROLLBAR_CLEAR_BITS_14_6=0xffff803f | check_equip_slot_eligible_by_type_and_chain (type==1 path) | asm/06:275-278 | ldr mask; ands; orrs set_code_bits; strh [sp+temp+4] | high |
| gEquipChainSlotRefs=0x0201bb90 | check_equip_slot_eligible_by_opposite_side_and_effect_ctx | asm/06:584-589 | ldr ptr; ldr[+0x0] == player; ldr[+0x1c] == zone_idx | high |
| GRAVEKEEPERS_CANNONHOLDER_CID=0x158c | check_equip_slot_eligible_for_gravekeeper_series | asm/06:763-766 | load CID; cmp icid,cid; beq reject | high |
| check_equip_slot_eligible_triple_predicate (fn-ptr) | check_equip_slot_eligible_by_opposite_side_zone_chain | asm/06:862 | ldrh slot[+0xa]!=0 fast-path: bl triple_predicate | high |
| gDuelPhaseFlags=0x0201b290 | check_equip_slot_eligible_with_score_bound_and_chain_scan | asm/06:1167-1168 | ldr base; adds ptr; ldr chain_cnt | high |
| LP_BAR_ANIM_STATE_OFF=0x4cc | 同上 | asm/06:1169-1172 | ldr off=0x4cc; r0=[base+off] = chain count | high |
| CHAIN_NODE_CARD_ARR_OFF=0x4f4 | 同上 | asm/06:1177-1178 | ldr off=0x4f4; r3=[base+off] = card array base | high |
| TORPEDO_FISH_CID=0x1706 (碰撞提示) | dispatch_equip_slot_eligible_by_type_prereqs_or_setcode | asm/06:1386 | slot[+0xa] equip_flag comparison; NOT a card ID | med |
| FUN_08054e5c now check_equip_slot_eligible_by_setcode_prereqs_all_slots | check_equip_slot_eligible_by_same_side_and_field8_9 plate | asm/06:1024 | EOL comment caller ref | high |
| EQUIP_CTX_PLAYER_OFF=0x0 | check_equip_slot_eligible_by_opposite_side_and_effect_ctx | asm/06:585 | ldr r0,[r1,#0x0]; cmp r0,r5(player) | high |
| EQUIP_CTX_SLOT_REF_OFF=0x1c | 同上 | asm/06:588 | ldr r0,[r1,#0x1c]; cmp r0,r4(zone_idx) | high |

## 求助

无低置信度语义阻塞项。

DWORD_08054138 = 0x1706 为 equip_flag 鉴别码 (不是 TORPEDO_FISH_CID)，置信度 med -- 全枚举 slot[+0xa] 值域需要更多 Seg 数据积累，当前标 RENAME-only 合理，无需 BLOCK。
