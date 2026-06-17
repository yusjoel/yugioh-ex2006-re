# Refine Proposal: F08-Seg-8a  [0x0806ab0c..0x0806b56c)

## Seg-8 拆分计划 (供 8b/8c 复用)

本段 (Seg-8) 因含 20 fn + 11 ROM_INCBIN + 1 switchD，按函数边界拆为 3 子段：

| 子段 | 地址范围 | fn 数 | ROM_INCBIN 块 | 说明 |
|------|----------|-------|---------------|------|
| Seg-8a | 0x6ab0c..0x6b56c | 6 | 4 (0x6adb6/0x3e, 0x6ae18/0x25c, 0x6b098/0x19c, 0x6b2a8/0x74) | LP row dispatch + switchD + Germ/Momonga/Spear Cretin handlers |
| Seg-8b | 0x6b56c..0x6c0cc | 6 | 5 (0x6b784/0x4c, 0x6b7fc/0x27c, 0x6bb74/0x44, 0x6bc2c/0x374, 0x6bfbc/0x110) | Numinous Healer + LP display + equip zone slot state machine |
| Seg-8c | 0x6c0cc..0x6cbe8 | 9 | 2 (0x6c3d8/0x44, 0x6c440/0x298) | Neo Daedalus placement + equip zone sprite chain cluster |

### 11 块 ref-scan 预分类汇总

| 块 | sz | raw | THUMB+1 | 判定 | 引用点 / 证据 |
|----|----|-----|---------|------|---------------|
| 0x6adb6 | 0x3e | 0 | 0 | §5.1 | 全 ROM 无引用；首 2B=0x0000 pad，0x6adb8 起 0xb5f0 push (THUMB code，但不可达) |
| 0x6ae18 | 0x25c | 1 | 0 | DISASM R4 | raw ref @0x806ae14 (jump table 第 9 条，9 条均指向本块内；0x6adb6 块之后的 jump table，0x806adf4..0x806ae14) |
| 0x6b098 | 0x19c | 1 | 0 | DISASM R4 | raw ref @0x806b094 (jump table 最后 1 条，指向本块起始；表 0x806b234..0x806b2a4 共 29 条) |
| 0x6b2a8 | 0x74 | 1 | 0 | DISASM R4 | raw ref @0x806b2a4 (jump table 第 29/29 条；本块 IS 该 29 条跳表本体，0x6b2a8+0x74=0x6b31c); THUMB+1 @0x89416ca 为压缩资产偶合，非真引用 |
| 0x6b784 | 0x4c | 0 | 1 | DISASM R4 | THUMB+1 @0x9e40448 = fn_eligible handler; 表项 [-4]=CID=0x135b (cid_135b, unassigned slot; 不在 card-stats.s，slot gap 0x135a->0x135c) |
| 0x6b7fc | 0x27c | 1 | 0 | DISASM R4 | raw ref @0x806b7f8 (jump table 第 10/10 条；表 0x806b7d4..0x806b7f8 全部 10 条均指向本块内) |
| 0x6bb74 | 0x44 | 0 | 1 | DISASM R4 | THUMB+1 @0x9e40490 = fn_eligible handler; 表项 [-4]=CID=0x1362 (MAGICAL_HATS_CID, card-stats slot=0x1362 Magical Hats) |
| 0x6bc2c | 0x374 | 1 | 0 | DISASM R4 | raw ref @0x806bc28 (jump table 第 29/29 条；表 0x806bbb8..0x806bc28, 28 条全指向本块) |
| 0x6bfbc | 0x110 | 1 | 0 | DISASM R4 | raw ref @0x806bfb8 (jump table 第 7/7 条，表 0x806bfa0..0x806bfb8 全 7 条指向本块内) |
| 0x6c3d8 | 0x44 | 0 | 1 | DISASM R4 | THUMB+1 @0x9e43760 = fn_eligible handler; 表项 [-4]=CID=0x1369 (MORPHING_JAR2_CID, card-stats slot=0x1369 Morphing Jar #2) |
| 0x6c440 | 0x298 | 1 | 0 | DISASM R4 | raw ref @0x806c43c (jump table 第 9/9 条；表 0x806c41c..0x806c43c 全 9 条指向本块内) |

**统计**: 0 carve / 10 disasm / 1 §5.1

---

## 段测绘 (Seg-8a only: 0x6ab0c..0x6b56c)

### 函数入口 (6 fn)

| 地址 | 名称 | push 指令 |
|------|------|-----------|
| 0x0806ab0c | dispatch_lp_row_or_banisher_sprite_by_state_with_slot_check | push {r4,r5,r6,lr} |
| 0x0806abd4 | relay_equip_zone_bitmap_to_zone11_update | push {r4,lr} |
| 0x0806abec | dispatch_equip_effect_slot_display_by_state_and_card | push {r4,r5,r6,r7,lr} (含 switchD_0806ac1e inline) |
| 0x0806b31c | dispatch_neo_daedalus_effect_display_by_state | push {r4,r5,r6,lr} -- FUNC_RENAME 候选 |
| 0x0806b53c | dispatch_neo_daedalus_placement_check_if_chain_subtype | push {lr} -- FUNC_RENAME 候选 |
| 0x0806b558 | enqueue_zone_sprite_type11_from_node | push {lr} |

### 残留自动名槽

| 槽 | 地址 | 值 |
|----|------|----|
| DAT_0806ab60 | 0x0806ab60 | 0x0201b290 |
| DAT_0806ab68 | 0x0806ab68 | 0x00000868 |
| DAT_0806ab94 | 0x0806ab94 | 0x00000868 |
| DAT_0806abc8 | 0x0806abc8 | 0x00001da8 |
| DAT_0806ac20 | 0x0806ac20 | 0x0201b290 |
| DAT_0806ac24 | 0x0806ac24 | 0x0806ac28 |
| DAT_0806ad24 | 0x0806ad24 | 0x00000868 |
| DAT_0806ad28 | 0x0806ad28 | 0x0201c740 |
| DAT_0806ad5c | 0x0806ad5c | 0x00001da8 |
| DAT_0806ad84 | 0x0806ad84 | 0x00001daa |
| DWORD_0806b340 | 0x0806b340 | 0x0201b290 |
| DWORD_0806b360 | 0x0806b360 | 0x00001339 |
| DWORD_0806b3d4 | 0x0806b3d4 | 0x0201b290 |
| DWORD_0806b3d8 | 0x0806b3d8 | 0x000004a4 |
| DWORD_0806b41c | 0x0806b41c | 0x0201e2a0 |
| DWORD_0806b420 | 0x0806b420 | 0x0201c4e0 |
| DWORD_0806b434 | 0x0806b434 | 0x00001339 |
| DWORD_0806b498 | 0x0806b498 | 0x0201c4e0 |
| DWORD_0806b49c | 0x0806b49c | 0x000004a4 |
| DWORD_0806b4a0 | 0x0806b4a0 | 0x00001339 |
| DWORD_0806b4d8 | 0x0806b4d8 | 0x00000868 |
| DWORD_0806b510 | 0x0806b510 | 0x00000868 |
| DWORD_0806b538 | 0x0806b538 | 0x000004a4 |

已命名 PTR_ 槽 (不计入残留自动名，但需 RENAME): PTR_gP1LifePoints_0806ab64, PTR_gP1LifePoints_0806ab90, PTR_gP1LifePoints_0806abc4, PTR_gP1LifePoints_0806ad58, PTR_gP1LifePoints_0806ad80

### ROM_INCBIN / .byte 块 (Seg-8a 内)

| 块 | 大小 | 地址范围 |
|----|------|----------|
| ROM_INCBIN 0x6adb6 | 0x3e B | 0x0806adb6..0x0806adf4 |
| ROM_INCBIN 0x6ae18 | 0x25c B | 0x0806ae18..0x0806b074 |
| ROM_INCBIN 0x6b098 | 0x19c B | 0x0806b098..0x0806b234 |
| ROM_INCBIN 0x6b2a8 | 0x74 B | 0x0806b2a8..0x0806b31c |

---

## 数据块分类 (Rule 2/3)

### Seg-8a 内 4 块

| 块 | sz | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|----|----|--------------------------|----- |------|
| 0x6adb6 | 0x3e | raw=0 thumb=0 | §5.1 | 全 ROM 0 引用；0x6adb6/7 = 0x0000 alignment pad，0x6adb8 起有 THUMB code (push {r4,r5,r6,r7,lr}=0xb5f0) 但不可达；asm/08 line 15743 |
| 0x6ae18 | 0x25c | raw=1 thumb=0 | DISASM R4 | raw ref @0x806ae14 in jump table context (9 entries 0x806adf4..0x806ae14, 全部指向本块内部目标 0x806ae48..0x806b01c); asm/08 line 15754; first bytes: 0x490a 0x1c28 (ldr + adds = THUMB code) |
| 0x6b098 | 0x19c | raw=1 thumb=0 | DISASM R4 | raw ref @0x806b094 (jump table entry 29/29 in table 0x806b234..0x806b2a4); 其他 28 条指向 0x806b2a8 块内；asm/08 line 15765; first bytes: 0x1c30 0xf7c8 (adds + bl = THUMB code) |
| 0x6b2a8 | 0x74 | raw=1 thumb=1(*) | DISASM R4 | raw ref @0x806b2a4 (jump table 29th entry = 本块起始地址); 29 条 jump table 在 0x806b234..0x806b2a4 且全指向本块内 (0x806b2a8..0x806b31c); THUMB+1 @0x89416ca 为偶合（压缩资产区 0x089xxxxx 随机字节）；asm/08 line 15796; first bytes: 0x78a1 0x07c8 (ldrb + lsls = THUMB code) |

(*) THUMB+1 ref at 0x89416ca: surrounding bytes `20 d2 48 53 [a9 b2 06 08] 6a 18` 无指针表结构特征，为压缩数据中的偶合值，不计真引用。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

| 槽 | 值 | const_name | 来源 | 槽新标签 |
|----|----|------------|------|---------|
| DAT_0806ab60 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc L351 | gduelphaseflags_0806ab60 |
| DAT_0806ab68 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse ewram.inc | player_block_stride_0806ab68 |
| DAT_0806ab94 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse | player_block_stride_0806ab94 |
| DAT_0806abc8 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | reuse ewram.inc L247 | lp_card_track_base_off_0806abc8 |
| DAT_0806ac20 | 0x0201b290 | gDuelPhaseFlags | reuse | gduelphaseflags_0806ac20 |
| DAT_0806ad24 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse | player_block_stride_0806ad24 |
| DAT_0806ad28 | 0x0201c740 | gP1SlotSetCodeArray | reuse ewram.inc L330 | gp1slotsetcodearray_0806ad28 |
| DAT_0806ad5c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | reuse | lp_card_track_base_off_0806ad5c |
| DAT_0806ad84 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | reuse ewram.inc L248 | lp_card_track_next_off_0806ad84 |
| DWORD_0806b340 | 0x0201b290 | gDuelPhaseFlags | reuse | gduelphaseflags_0806b340 |
| DWORD_0806b360 | 0x00001339 | GIANT_GERM_CID | NEW card_info.inc | giant_germ_cid_0806b360 |
| DWORD_0806b3d4 | 0x0201b290 | gDuelPhaseFlags | reuse | gduelphaseflags_0806b3d4 |
| DWORD_0806b3d8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | reuse ewram.inc L434 | equip_phase_frame_off_0806b3d8 |
| DWORD_0806b41c | 0x0201e2a0 | gDuelCardCtxBase | reuse ewram.inc L218 | gduelcardctxbase_0806b41c |
| DWORD_0806b420 | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc | gp1lifepoints_0806b420 |
| DWORD_0806b434 | 0x00001339 | GIANT_GERM_CID | reuse (NEW above) | giant_germ_cid_0806b434 |
| DWORD_0806b498 | 0x0201c4e0 | gP1LifePoints | reuse | gp1lifepoints_0806b498 |
| DWORD_0806b49c | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | reuse | equip_phase_frame_off_0806b49c |
| DWORD_0806b4a0 | 0x00001339 | GIANT_GERM_CID | reuse | giant_germ_cid_0806b4a0 |
| DWORD_0806b4d8 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse | player_block_stride_0806b4d8 |
| DWORD_0806b510 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse | player_block_stride_0806b510 |
| DWORD_0806b538 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | reuse | equip_phase_frame_off_0806b538 |

总计: 22 EQ slots (21 reuse + 1 NEW: GIANT_GERM_CID)

### REF_SLOTS (USER-label + DATA-ref)

| 槽 | 目标 | gas_label | 槽新标签 | 说明 |
|----|------|-----------|---------|------|
| DAT_0806ac24 | 0x0806ac28 | switchD_0806ac1e__switchdataD_0806ac28 | switchd_0806ac1e_data_ptr_0806ac24 | switchD 跳转表数据指针；已 inline 在 dispatch_equip_effect_slot_display_by_state_and_card 内 |

总计: 1 REF slot

### RENAME_SLOTS (PTR_ 前缀标签改名，含 EOL)

| 槽 | 当前标签 | 新标签 | EOL |
|----|---------|--------|-----|
| 0x0806ab64 | PTR_gP1LifePoints_0806ab64 | lp_base_slot_player_0806ab64 | (none) |
| 0x0806ab90 | PTR_gP1LifePoints_0806ab90 | lp_base_opponent_0806ab90 | (none) |
| 0x0806abc4 | PTR_gP1LifePoints_0806abc4 | lp_base_face_down_0806abc4 | (none) |
| 0x0806ad58 | PTR_gP1LifePoints_0806ad58 | lp_base_card_lookup_0806ad58 | (none) |
| 0x0806ad80 | PTR_gP1LifePoints_0806ad80 | lp_base_hand_sprite_0806ad80 | (none) |

总计: 5 RENAME slots

### FUNC_RENAME (误名订正)

#### ripple 收尾清单 (落地时必须执行)

a. **CSV sync**: `doc/dev/naming-proposals.csv` 第 2009 行 (0x0806b31c) + 第 2010 行 (0x0806b53c) 旧名 → 新名:
   - 0x0806b31c: `dispatch_neo_daedalus_effect_display_by_state` -> `dispatch_germ_momonga_trigger_display_by_state`
   - 0x0806b53c: `dispatch_neo_daedalus_placement_check_if_chain_subtype` -> `dispatch_spear_cretin_activate_if_chain_subtype`

b. **跨模块 plate**: `asm/05_equip_eligibility_a.s` line 4 的 plate 文本含旧名 `dispatch_neo_daedalus_effect_display_by_state`，落地 re-export 后须 grep 全 asm/*.s 手改残留 plate 散文为新名（Ghidra rename 自动更新 bl 引用但不更新 plate 散文）。

#### 1. dispatch_neo_daedalus_effect_display_by_state @ 0x0806b31c

证据 (high confidence):
- 函数体仅比较 CID 0x1339 和 0x133a (asm/08 L15856, DWORD_0806b360=0x1339, 代码 `cmp r1,r0; beq; adds r0,#1; cmp r1,r0`)
- 0x1339 = Giant Germ (card-stats.s card_0735 slot=0x1339 pw=95178994; asm/08 L15856-15856)
- 0x133a = Nimble Momonga (NIMBLE_MOMONGA_CID = 0x133a; constants/card_info.inc L501)
- 均非 Neo Daedalus；函数名 'neo_daedalus' 系历史误名
- 函数是 CID 0x1339 + 0x133a 的共享 fn_activate handler，dispatch table @0x9e45800 (CID=0x1339) 和 @0x9e45818 (CID=0x133a) 均指向 0x806b31d
- indeg=2 (仅 fn_activate THUMB+1 dispatch table refs，无 bl callers)

旧名: dispatch_neo_daedalus_effect_display_by_state
新名: dispatch_germ_momonga_trigger_display_by_state
PLATE: 全文替换 (substring):
- "Neo-Daedalus group A" -> "Giant Germ (CID=0x1339)"
- "Neo-Daedalus group B" -> "Nimble Momonga (CID=0x133a)"
- "Neo-Daedalus effect series" -> "Giant Germ / Nimble Momonga trigger effect"
- "CARD_ID_0x1339=0x1339 (Neo-Daedalus group A)" -> "GIANT_GERM_CID=0x1339 (Giant Germ)"
- "CARD_ID_0x133a=0x133a (Neo-Daedalus group B)" -> "NIMBLE_MOMONGA_CID=0x133a (Nimble Momonga)"

#### 2. dispatch_neo_daedalus_placement_check_if_chain_subtype @ 0x0806b53c

证据 (high confidence):
- dispatch table @0x9e436d0 项: 表项 [-4]=CID=0x133b, fn_activate+1=0x806b53d
- dispatch table @0x9e45830 项: 表项 [-4]=CID=0x133b, fn_activate+1=0x806b53d
- 0x133b = SPEAR_CRETIN_CID (constants/card_info.inc L795; card-stats.s card_0737 slot=0x133B pw=58551308)
- 函数名 'neo_daedalus_placement_check' 与 CID=Spear Cretin 矛盾
- 函数体: reads byte[+3] & 0x30, if ==0x20 calls dispatch_neo_daedalus_placement_check_by_state (callee 暂未改名，Seg-8c 范围); else returns 0
- indeg=2 (THUMB+1 dispatch refs @0x9e436d0, 0x9e45830; no bl callers)

旧名: dispatch_neo_daedalus_placement_check_if_chain_subtype
新名: dispatch_spear_cretin_activate_if_chain_subtype
PLATE: function label substring replace only:
- "Neo Daedalus placement check by equip-slot subtype" -> "Spear Cretin activate by equip-slot chain subtype"

### PLATE (R5)

| 函数 | 类型 | 内容 |
|------|------|------|
| dispatch_germ_momonga_trigger_display_by_state (renamed) | substring replace | 见 FUNC_RENAME 上文 5 处替换 |
| dispatch_spear_cretin_activate_if_chain_subtype (renamed) | substring replace | "Neo Daedalus placement check" -> "Spear Cretin activate" |

注: Seg-8a 其余 4 函数现有 plate 均 ASCII 无 CJK，无 stale FUN_ 引用，不需要额外 plate 操作。

---

## carve 计划 (R7)

无 -- Seg-8a 4 个 ROM_INCBIN 全部判定 DISASM 或 §5.1，无 carve。

---

## disasm 计划 (R4)

Seg-8a 内 3 个 DISASM 块：

### 块 0x6ae18 (0x25c B, 0x0806ae18..0x0806b074)

结构分析:
- 9-entry jump table at 0x806adf4..0x806ae14 指向本块内 9 个 case handler stubs
- 引用点: raw ref @0x806ae14 = 0x806ae18 (jump table 第 9 条 = 本块起始)
- 块内目标: 0x806ae18, 0x806ae48, 0x806ae90, 0x806af52, 0x806af84, 0x806afac, 0x806afec, 0x806b01c (x2)

THUMB disasm 范围: 0x0806ae18..0x0806b074 (0x25c B)
方法: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand (每个跳表目标逐一执行)

### 块 0x6b098 (0x19c B, 0x0806b098..0x0806b234)

结构分析:
- 29-entry jump table at 0x806b234..0x806b2a4 指向本块内 case handler stubs
- 引用点: raw ref @0x806b094 = 0x806b098 (jump table 最后 1 条 = 本块起始)
- 块内目标: 0x806b098, 0x806b0d6, 0x806b124, 0x806b13c, 0x806b1de, 0x806b1ea, 0x806b1f4, 0x806b2ce, 0x806b2e2, 0x806b2f8, 0x806b30a, 0x806b314 (default)

THUMB disasm 范围: 0x0806b098..0x0806b234 (0x19c B)
方法: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand

### 块 0x6b2a8 (0x74 B, 0x0806b2a8..0x0806b31c)

结构分析:
- 本块 IS 29-entry jump table 的最后目标，内容为 case stubs
- 引用点: raw ref @0x806b2a4 (jump table [28] = 本块起始) -- 真引用（代码上下文）
- THUMB+1 @0x89416ca: 压缩资产偶合，已排除
- 块内目标: 0x806b2a8, 0x806b2ce, 0x806b2e2, 0x806b2f8, 0x806b30a, 0x806b314

THUMB disasm 范围: 0x0806b2a8..0x0806b31c (0x74 B)
方法: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand

---

## 新增 constants / 全局

### card_info.inc (新增 1 项)

```
.equ GIANT_GERM_CID,   0x00001339  @ Giant Germ (pw=95178994; card-stats.s slot=0x1339); fn_activate handler dispatch_germ_momonga_trigger_display_by_state; shared with Nimble Momonga (0x133a) for summon-from-deck trigger
```

C5 双向核: grep card_info.inc "0x1339" -> 0 命中 -> NEW 确认。邻近已有 NIMBLE_MOMONGA_CID=0x133a (L501), KARATE_MAN_CID=0x1337 (L500)。

### 不新增其他常量

所有其他 EQ 值均已在 ewram.inc / duel_field.inc 存在 (gDuelPhaseFlags=0x0201b290 L351 / PLAYER_BLOCK_STRIDE=0x868 / LP_CARD_TRACK_BASE_OFF=0x1da8 L247 / LP_CARD_TRACK_NEXT_OFF=0x1daa L248 / EQUIP_PHASE_FRAME_OFF=0x4a4 L434 / gP1SlotSetCodeArray=0x0201c740 L330 / gDuelCardCtxBase=0x0201e2a0 L218 / gP1LifePoints=0x0201c4e0)。

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | 大小 | Seg | 初判内容 | 状态 |
|------|------|-----|----------|------|
| 0x0806adb6 | 0x3e B | F08-Seg-8a | 2B align pad (0x0000) + THUMB code stubs (push {r4,r5,r6,r7,lr} @0x6adb8); raw=0 THUMB+1=0 全 ROM 无引用; dead code | pending |

---

## 消费者证据 (R6) -- 关键槽语义

| 槽 | 消费者 file:line | 置信度 |
|----|-----------------|--------|
| GIANT_GERM_CID=0x1339 | asm/08_equip_oam_neodaed.s L15856 (DWORD_0806b360) + dispatch table @0x9e45800 CID field (python verify) | high |
| NIMBLE_MOMONGA_CID=0x133a | card_info.inc L501; dispatch table @0x9e45818 CID field | high |
| SPEAR_CRETIN_CID=0x133b | card_info.inc L795; dispatch table @0x9e436cc, 0x9e4582c CID field (python verify) | high |
| gDuelPhaseFlags=0x0201b290 | ewram.inc L351 (676 raw refs); asm/08 L15569 (DAT_0806ac20 = 0x0201b290) | high |
| PLAYER_BLOCK_STRIDE=0x868 | asm/08 L15441 (DAT_0806ab68; DWORD_0806b3d8 etc.); ewram.inc pattern | high |
| LP_CARD_TRACK_BASE_OFF=0x1da8 | ewram.inc L247 (109 raw ROM refs; "[gP1LifePoints+0x1da8] LP card-ref tracking array base") | high |
| LP_CARD_TRACK_NEXT_OFF=0x1daa | ewram.inc L248 (44 raw ROM refs; "[gP1LifePoints+0x1daa] 5-entry hword clear loop base") | high |
| EQUIP_PHASE_FRAME_OFF=0x4a4 | ewram.inc L434 (241 ROM refs; "[gDuelPhaseFlags+0x4a4] dragon-summon/equip effect phase frame counter") | high |
| gP1SlotSetCodeArray=0x0201c740 | ewram.inc L330 (82 ROM refs; "gP1LifePoints+0x260: slot set_code data array P1 base") | high |
| gDuelCardCtxBase=0x0201e2a0 | ewram.inc L218 (442 raw refs; "duel card activation context base") | high |

---

## 求助

None -- 所有语义均有 file:line + 置信度 high 证据支撑。

FUNC_RENAME 备注: dispatch_neo_daedalus_placement_check_if_chain_subtype 改名后仍调用 dispatch_neo_daedalus_placement_check_by_state (Seg-8c 内)。该 callee 名称是否也错误 (Spear Cretin 的"placement check"含义是否准确) 需在 Seg-8c 阶段验证，Seg-8a 不阻塞。
