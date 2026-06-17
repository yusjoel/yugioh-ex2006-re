# Refine Review: F08-Seg-7  [0x0806a118..0x0806ab0c)

Reviewer: independent agent (not proposal author).
Date: 2026-06-18

---

## Phase 1: 自主复核结果

### 1.1 C13 DAT_/DWORD_ 精确清点

`awk -F: '$1>=13881 && $1<=15411'` 从段边界行提取所有以 `^DAT_0806a` / `^DWORD_0806a` 开头的标签定义:

```
13991 DWORD_0806a1ec   14011 DWORD_0806a210   14134 DWORD_0806a2e0
14136 DWORD_0806a2e4   14138 DWORD_0806a2e8   14282 DAT_0806a3e4
14284 DAT_0806a3e8     14349 DAT_0806a440     14378 DAT_0806a47c
14380 DAT_0806a480     14382 DAT_0806a484     14471 DAT_0806a518
14473 DAT_0806a51c     14503 DWORD_0806a540   14618 DAT_0806a614
14620 DAT_0806a618     14622 DAT_0806a61c     14624 DAT_0806a620
14626 DAT_0806a624     14628 DAT_0806a628     14683 DAT_0806a690
14749 DAT_0806a6f4     14751 DAT_0806a6f8     14753 DAT_0806a6fc
14810 DAT_0806a75c     14881 DWORD_0806a7c0   14995 DWORD_0806a87c
14997 DWORD_0806a880   15086 DWORD_0806a8fc   15106 DWORD_0806a924
15108 DWORD_0806a928   15128 DWORD_0806a94c   15130 DWORD_0806a950
15173 DWORD_0806a988   15251 DAT_0806aa08     15253 DAT_0806aa0c
15255 DAT_0806aa10     15306 DAT_0806aa5c     15308 DAT_0806aa60
15392 DAT_0806ab08
```

合计: **40 个**。无 PTR_/UNK_ 自动名槽。  
PTR_gP1LifePoints_0806a6f0 (行 14747) 已描述性命名, 不计入 DAT_/DWORD_ 集合 — proposal 说明正确。  
Proposal EQ 表 40 行: **完全覆盖**。无漏槽、无越界。

### 1.2 C2 — .byte/.incbin/switchD 块扫描 (重跑)

`grep -n "ROM_INCBIN|\.incbin|switchD|\.byte"` 在行 13881..15411 命中:

```
14505:    .byte  0x00, 0x20, 0x70, 0x47
```

**Proposal 声称 0 .byte 块 — 与实际不符。**  
该 4 字节块位于 0x0806a544 (ROM addr), 解码为 THUMB `movs r0,#0; bx lr`。

### 1.3 C3 — .byte 块 0-引用核验

Python ref-scan (raw + THUMB|1):

```
0x0806a544 raw refs: 0
0x0806a545 raw refs: 0
0x0806a546 raw refs: 0
0x0806a547 raw refs: 0
```

**确认 0 引用** — 须登记 §5.1 (规则 3)。

### 1.4 C4 — ROM 字节核对 (全 40 槽 python 实读)

逐一 `struct.unpack_from('<I', rom, addr-0x08000000)` 对比 proposal:

所有 40 槽 **全部 OK**。抽查关键槽:
- 0x0806a2e4: 0x00001cb8 OK (ZONE14 offset)
- 0x0806a61c: 0x00008028 OK (OAM_ZONE_SPRITE_PAIR_P2_FIRST)
- 0x0806a7c0: 0x0000ffff OK (LP_ROW_TYPE8_ALL_SLOTS_MASK)
- 0x0806ab08: 0xffff0000 OK (EQUIP_CHAIN_SENTINEL)

### 1.5 C5 — 3 个 NEW 常量按 VALUE grep

**ZONE14_CHAIN_SLOT_FLAG_OFF = 0x1cb8**
- `grep -rn "0x00001cb8" constants/` 命中: `duel_field.inc:155: DUEL_ACTIVE_PLAYER_OFF = 0x00001cb8`
- 值碰撞已知。Proposal 援引 C5 域例外: 两者 base 不同 (gP1LifePoints vs gDuelFieldSlots)。  
  独立核验消费者 `scan_equip_chain_slots_for_zone14_targets` (L14098-14099):
  ```
  ldr r1, DWORD_0806a2e4    @ r1 = 0x1cb8
  adds r1,r1,r6             @ r6 = gDuelFieldSlots(0x0201c510)
                            @ r1 = 0x0201c510 + 0x1cb8 = 0x0201e1c8
  ```
  base 确为 **gDuelFieldSlots**; 结果地址 = **gEquipZoneCountTable (0x0201e1c8)**,  
  与 `DUEL_ACTIVE_PLAYER_OFF` (base=gP1LifePoints, 结果 0x0201e198) 不同地址。  
  **域例外成立**, 新建独立常量正确。  
  NAME 质量备注见 #2 修改建议 (不阻塞 PASS, 但推荐改名)。

**OAM_ZONE_SPRITE_PAIR_P2_FIRST = 0x8028**
- `grep -rn "0x00008028" constants/` **0 命中** — 新建正确。
- 消费者: `dispatch_zone_sprite_with_effect_node_and_state` L14574, `enqueue_sprite_attr_record(attr=0x8028)`. 已存在同函数 OAM_EQUIP_SLOT_SPRITE_P2=0x8029 (第二 sprite), 0x8028 是第一 sprite。命名合理, conf: high。

**LP_ROW_TYPE8_ALL_SLOTS_MASK = 0xffff**
- `grep -rn "0x0000ffff" constants/` 命中 3 处:
  - oam_attr.inc: EQUIP_SLOT_SCORE_CAP=0xffff (equip score domain)
  - card_info.inc: SLOT_CARD_EMPTY=0xffff (card sentinel domain)
  - oam_attr.inc: OAM_ATTR0_HIDDEN=0xffff (OAM attr domain)
- LP row type8 slot_mask = 独立函数参数, 域截然不同 (LP display row all-slots selector)。  
  消费者 L14873-14875: `ldr r1, DWORD_0806a7c0 (0xffff); bl set_lp_display_row_type8`。  
  **域例外成立**, 新建正确。

### 1.6 C5 — 37 个 reuse 抽查 (按 VALUE grep)

抽查全部值类别:

| 值 | 期望常量 | grep 命中 | 结论 |
|----|---------|---------|------|
| 0x0201c4e0 | gP1LifePoints | ewram.inc:79 | OK |
| 0x0201c510 | gDuelFieldSlots | ewram.inc:312 | OK |
| 0x0201b290 | gDuelPhaseFlags | ewram.inc:351 | OK |
| 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:250 | OK |
| 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:275 | OK |
| 0x0201bbbc | gDuelEquipCtx | ewram.inc:455 | OK |
| 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc:247 | OK |
| 0x0000801c | OAM_EQUIP_SPRITE_TILE_P2_1C | oam_attr.inc:154 | OK |
| 0x00008029 | OAM_EQUIP_SLOT_SPRITE_P2 | oam_attr.inc:55 | OK |
| 0xffff0000 | EQUIP_CHAIN_SENTINEL | duel_field.inc:270 | OK |
| 0x0201c740 | gP1SlotSetCodeArray | ewram.inc:330 | OK |
| 0x000012ea | MONSTER_REBORN_CID | card_info.inc:788 | OK |
| 0x000012e5 | POLYMERIZATION_CID | card_info.inc:436 | OK |
| 0x0000184d | MIND_HAXORZ_CID | card_info.inc:1227 | OK |
| 0x0000135d | LIGHT_OF_INTERVENTION_CID | card_info.inc:401 | OK |

全部命中, 值精确匹配。

### 1.7 C8 — stale FUN_ 扫描

`grep -n "FUN_[0-9a-f]{8}"` 行 13881..15411: **0 命中**。

### 1.8 C9 — ASCII 验证

`python grep [^\x00-\x7F]` 行 13881..15411: **0 命中**。

### 1.9 C11 — 函数名抽查

- `dispatch_equip_zone_sprite_by_lp_state_with_placement_check` (L13880): 读 gDuelPhaseFlags[+0x4a0], switch 0x7e/0x7d/0x7f/0x80, 调 check_card_id_placement_allowed — 名称吻合。
- `enqueue_lp_row_type8_if_equippable_slots_nonzero` (L14850): 检 guard_bit, 调 count_equippable_slots_for_card, 非零时 bl set_lp_display_row_type8 — 名称吻合。
- `set_player_state_flag_if_unguarded` (L14820): 检 bit2 guard_bit, 若未设则 bl set_player_state_bit_with_sprite_update — 名称吻合。
- `enqueue_equip_chain_sprite_for_dual_slot` (L15312): 调 check_effect_slot_matches_zone_entry x2, EQUIP_CHAIN_SENTINEL 门控 — 名称吻合。

**FUNC_RENAME = 0**: 确认正确。

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 0x6a118..0x6ab0c = Seg-7 第 7 段, 未跳号/回头 |
| C2 Rule2 | 所有 .byte 块有归宿 | ❌ | **0x0806a544 (4B) `.byte 0x00,0x20,0x70,0x47` 被 proposal 遗漏** |
| C3 Rule3 | §5.1 块确 0 引用 | ❌ (派生) | **0x0806a544 确 0 引用 (raw+THUMB+1 全 0), 须补 §5.1 登记** |
| C4 R1 值 | EQ value == ROM 4 字节小端 | ✅ | 全 40 槽 python 实读 OK |
| C5 R1 复用 | new 前无现有同值可复用 | ✅ | 3 new 均无名字冲突; 值碰撞均有域例外依据 |
| C6 R2 名 | 槽名格式合规, 无碰撞 | ✅ | 3 new 常量 `^[A-Z][A-Z0-9_]+$`, grep 0 命中 |
| C7 R3 接通 | carve/全局槽有 USER-label+DATA-ref | N/A | 无 carve/REF 槽 |
| C8 R5 现名 | 无残留 FUN_/DAT_/DWORD_ 引用 | ✅ | grep 段内 0 命中 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 0 非 ASCII |
| C10 carve | 指针表 +1 正确 | N/A | 无 carve |
| C11 误名 | 函数体与函数名一致 | ✅ | 抽查 4 fn 一致 |
| C12 R6 | 关键槽有 file:line+置信度 | ✅ | 7 consumer evidence 行齐全 |
| C13 残留 | 段内所有 DAT_/DWORD_ 被覆盖 | ✅ | 实数 40 == proposal 40 |

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单 (NEEDS_FIX)

### #1 — C2/C3 — 补 §5.1 登记: 0x0806a544 4B 孤儿 stub

**问题**: Proposal 声称 "ROM_INCBIN / .byte blocks: 0" 及 "§5.1 None", 但 asm/08 行 14505 存在:

```
    .byte  0x00, 0x20, 0x70, 0x47
```

该 4 字节位于 ROM 地址 0x0806a544 (紧跟 DWORD_0806a540 字面量池), 解码为 THUMB `movs r0,#0 (0x2000)` + `bx lr (0x4770)`。

**Ref-scan 结果** (python 独立验证):
- raw refs to 0x0806a544: 0
- THUMB+1 refs to 0x0806a545: 0

**处置**: 按规则 3 (全 ROM 0 引用 → §5.1 登记留待)。Proposal 须补 §5.1 条目:

```
| 0x0806a544 | 4B | Seg-7 | movs r0,#0; bx lr (orphan 4B stub, 0 raw+THUMB refs) | pending |
```

无需 disasm / carve (0 引用, 无消费者)。只需在 proposal §5.1 Registry 节添加该记录。

---

## 附: ZONE14_CHAIN_SLOT_FLAG_OFF 名称质量建议 (不阻塞, 可选改进)

当前名 `ZONE14_CHAIN_SLOT_FLAG_OFF` (med conf) 包含 "ZONE14" 和 "CHAIN_SLOT_FLAG" 均未经实际结构确认。  
独立核验: gDuelFieldSlots(0x0201c510)+0x1cb8 = **0x0201e1c8 = gEquipZoneCountTable** (ewram.inc:395, 55 ROM refs 命名全局)。  
此偏移是 "从 gDuelFieldSlots 到 gEquipZoneCountTable 的偏移量", 语义明确。  
建议改名为 `EQUIP_ZONE_COUNT_TABLE_OFF` (conf: high; 与 asm/05 L17480 注释 "gDuelFieldSlots offset to gEquipZoneCountTable" 一致)。  
现有 DUEL_ACTIVE_PLAYER_OFF=0x1cb8 注释为 "gP1LifePoints+0x1cb8", 两者明确区分 base。  
**决策权归 fixer/用户** — 不修改不阻塞落地, 但推荐接受改名以提高准确性。

---

## Reviewer Verdict: F08-Seg-7 = NEEDS_FIX(1 item)
