# Refine Review: F07-Seg-2

Seg range: ROM `0x0805cfec..0x0805e358`, module `asm/07_equip_effect_chain.s` (lines 2128-5062).
Reviewer ran independent ref-scan, ROM byte checks, and asm label enumeration.

---

## 核验 (C1-C13) — iter-2 (re-review after mode-A fix)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | ✅ | 路线图 Seg-2 = 0x5cfec..0x5e358, 2 ROM_INCBIN. 提案一致. fn 数路线图约 34, 提案表格 34, 提案 header 误写 35 (cosmetic). |
| C2 Rule2 | 两个 ROM_INCBIN 块均有归宿 | ✅ | Block1(0x5dd3e/0x1a) → R4 DISASM 1 sub-fn; Block2(0x5ddda/0xd2) → R4 DISASM 4 sub-fn. 无静默保留. |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ N/A | 无 §5.1 块, C3 vacuously satisfied. 两块均有 THUMB 命中 (重跑 ref-scan 确认). |
| C4 R1 值 | 65+27=92 个 EQ/REF slot 值 == ROM 4B 小端 | ✅ | 独立 python 读取全部 92 个地址 (EQ 65 + REF 27), 全部 MATCH. 包含 DWORD_ 槽全核. |
| C5 R1 复用 | 20 REUSE CID 反向核 + 19 NEW CID 正向核 | ✅ | REUSE 全部在 card_info.inc 确存在; NEW 全部 grep 0 命中. cid_134e REUSE 确认 line 1116. |
| C6 R2 名 | slot_label/fn_name 格式 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | 34 现有 fn 名、5 个 disasm 新 fn 名、所有 slot_label 均通过格式检查. |
| C7 R3 接通 | REF slots 有 USER-label + DATA-ref 计划 | ✅ | gP1LifePoints/gDuelFieldSlots/gEquipChainSlotRefs/gDuelPhaseFlags 均在 ewram.inc 定义. fn_ptr slot (0x0805df94) gas_label = check_equip_slot_eligible_by_equip_type+1, 该 label 在 asm/05_equip_eligibility_a.s line 18412 有定义. |
| C8 R5 现名 | 段内无残留 stale FUN_ | ✅ | grep `FUN_[0-9a-f]{8}` 在 lines 2128-5062 = 0 命中. |
| C9 ASCII | 全部 plate/EOL 纯 ASCII | ✅ | 三块 plate 文本均纯 ASCII; asm 段内 non-ASCII byte = 0. |
| C10 carve | 无 carve 块, N/A | ✅ N/A | 两块均为 R4 DISASM, 无 carve. |
| C11 误名 | 34 fn 名与函数体一致 | ✅ | 抽查 invoke_effect_node_handler_with_zone_flag_guard 函数体: 实际调用 read_effect_slot_side_and_type + set_equip_activation_state_by_mode_alt. 函数名本身描述 "zone_flag_guard" 行为语义正确 (写/清 gDuelPhaseFlags+0x4c0). 无 FUNC_RENAME 需求. |
| C12 R6 | plate 文本语义准确 + 置信度有证据 | ✅ | **iter-2 修复**: Plate #2 (invoke_effect_node_handler_with_zone_flag_guard) 被调用者已更正为 read_effect_slot_side_and_type + set_equip_activation_state_by_mode_alt. 独立核对 asm/07 lines 3841/3853 (bl 指令): 两个 bl 目标完全吻合提案文本. 旧错误名 check_zone_slot_equip_prerequisites/invoke_effect_node_handler 已清除. |
| C13 残留 | 92 个 DAT_/DWORD_/PTR_ 全覆盖 | ✅ | 实际: DAT_=56, DWORD_=27, PTR_=9 = 92 (提案 header 写法有 cosmetic 误差). 独立提取 92 个 label 地址集与 EQ(65)+REF(27) 地址集完全一致, missing=0, extra=0. |

---

## 独立核验结果 (iter-1 + iter-2 合计)

### ref-scan (重跑)

**Block 1 (0x5dd3e/0x1a): 1 sub-fn at 0x0805dd40**

```
addr=0x0805dd40: raw=0, thumb=1
  THUMB hit ROM offset 0x1e40318 (0x09e40318)
  dispatch table record 0x09e4030c: [CID=0x0000134e][fn0=0x0806b559][00000000][fn[1]=0x0805dd41][00000000][00000000]
  CID 0x134e = cid_134e, REUSE card_info.inc line 1116. VERIFIED.
```

**Block 2 (0x5ddda/0xd2): 4 sub-fns**

```
0x0805dddc: raw=0, thumb=2
  record 0x09e4036c: CID=0x00001352 (Numinous Healer), fn[1] @ 0x09e40378 = 0x0805dddd
  record 0x09e4042c: CID=0x0000135a (Attack and Receive), fn[1] @ 0x09e40438 = 0x0805dddd
0x0805de10: raw=0, thumb=2
  record 0x09e40384: CID=0x00001353 (Appropriate), fn[1] @ 0x09e40390 = 0x0805de11
  record 0x09e436fc: CID=0x00001353 (Appropriate, 2nd entry), fn[1] @ 0x09e43708 = 0x0805de11
0x0805de50: raw=0, thumb=1
  record 0x09e4039c: CID=0x00001354 (Forced Requisition), fn[1] @ 0x09e403a8 = 0x0805de51
0x0805de7c: raw=0, thumb=1
  record 0x09e403b4: CID=0x00001355 (Minor Goblin Official), fn[1] @ 0x09e403c0 = 0x0805de7d
```

iter-2 提案中 7 个 fn[1] ROM 地址 (0x09e40318/0x09e40378/0x09e40438/0x09e40390/0x09e43708/0x09e403a8/0x09e403c0) 已全部独立核对 ROM 正确.

**Sub-fn boundary 核对 (Block 2 bx lr 位置)**:

```
0x0805de0c (off+0x32): sub-fn 1 end
0x0805de4e (off+0x74): sub-fn 2 end (literal pool: gP1LifePoints @ 0x5de44, FIELD_STATE_OFF @ 0x5de48)
0x0805de78 (off+0x9e): sub-fn 3 end
0x0805de9c (off+0xc2): sub-fn 4 end (literal pool: gP1LifePoints/PLAYER_BLOCK_STRIDE/0x0bb8=3000)
```

Sub-fn 起点 +0x02/+0x36/+0x76/+0xa2 已核对正确.

### iter-2 四项修复核验

**Fix #1 (C12): Plate #2 被调用者名称**
- 提案现文: "... side/type already matched (read_effect_slot_side_and_type) -> return 0. Sets [gDuelPhaseFlags+0x4c0]=player_id_bit, calls set_equip_activation_state_by_mode_alt(...)"
- asm/07 line 3841: `bl read_effect_slot_side_and_type` ✅
- asm/07 line 3853: `bl set_equip_activation_state_by_mode_alt` ✅
- 旧错误名已清除: grep `check_zone_slot_equip_prerequisites|invoke_effect_node_handler` 在 plate 段 = 0 命中 ✅

**Fix #2 (dispatch table 地址)**
- 7 个 fn[1] 地址全部 ROM 独立核验 ✅ (见上方 ref-scan 详情)
- CID 值全部正确 ✅

**Fix #3 (Block1 disasm step 2 createWord)**
- 提案 step 2: `createWord 0x0805dd3e` (2B .hword, 覆盖 [0x5dd3e,0x5dd3f]) ✅
- Block1 pad 字节: 0x5dd3e=00, 0x5dd3f=00 (两字节零, createWord 正确) ✅
- sub-fn 起点 0x5dd40 不被 createWord 覆盖 ✅

**Fix #4 (MINOR_GOBLIN_OFFICIAL_CID passcode)**
- 提案: `pw=01918087` ✅
- card-stats.s line 9869: `@ Minor Goblin Official  slot=0x1355  pw=01918087` ✅

### 遗留 cosmetic 项 (不阻塞落地)

| 字段 | 提案写 | 实际 | 影响 |
|------|--------|------|------|
| Executor Report EQ= | 62 | 65 | cosmetic only |
| Executor Report fn= | 35 | 34 | cosmetic only |
| Executor Report DAT_= | 58 | 56 | cosmetic only |
| Executor Report DAT_= | 25 | 27 | cosmetic only |

提案正文表格已正确列出 65 EQ + 27 REF = 92 槽, header 数字不影响落地.

---

## 状态: PASS

---

## 核验通过项汇总

- 全部 92 个 EQ/REF slot ROM 值独立核对: 65 EQ + 27 REF = 100% MATCH
- EQ+REF 地址集与 asm 段内 92 个 label 定义地址集: missing=0, extra=0, 完全覆盖
- Block1 sub-fn 0x0805dd40: bx lr @ 0x0805dd56, size=0x18 ✅
- Block2 sub-fn 边界 (+0x02/+0x36/+0x76/+0xa2 from 0x5ddda): bx lr 位置 0x5de0c/0x5de4e/0x5de78/0x5de9c 全部独立验证 ✅
- cid_134e REUSE card_info.inc line 1116 ✅; cid_1350/1351 line 1118/1119 ✅
- 19 NEW CID 从 card-stats.s slot= 字段核对: all high-conf; cid_12f7/cid_135b 无记录 -> neutral low-conf ✅
- P2_ZONE1_LP_OFF=0x87c: 0x868+0x14=0x87c 数学验证 ✅; asm/07 line 3228 load 确认 ✅; med-conf 标记适当 ✅
- fn_ptr REF 0x0805df94 = 0x08051319 ROM 值 = check_equip_slot_eligible_by_equip_type+1 ✅; THUMB bit set ✅
- 段内 FUN_[0-9a-f]{8}: 0 命中 ✅
- 段内 non-ASCII: 0 ✅; 三块 plate 文本 ASCII ✅
- C1 段范围 [0x5cfec,0x5e358) 路线图一致 ✅; Seg-3 start 0x5e358 line 5063 ✅
- iter-2 四项修复全部独立核验通过 ✅
