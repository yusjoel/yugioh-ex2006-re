# Refine Review: F11-Seg-4g

Reviewer 独立复核 (不信 proposal 结论, 自主重跑 ROM 读值 + ref-scan + dispatch table scan)。

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | §五 roadmap: Seg-4g `[0x0808cabc, 0x0808d7f4)`, 紧接 Seg-4f 末端 0x0808cabc; 未跳号/回头 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | ✅ | 段内唯一 ROM_INCBIN 0x8cabc/0xd38; 全量 disasm 覆盖 20 fn; C2 通过 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无 §5.1 块; 所有 fn 均有 dispatch table thumb-ref 确认 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | 独立 python ROM read 验证: gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868, CARD_FIELD_STAT_CLEAR_UPPER4_MASK=0x0fffffff, WINGED_KURIBOH_CID=0x18aa, gEquipEffectZoneBase=0x0201e4f0, SLOT_CARD_SET_CODE_MASK=0x1fff — 全 OK |
| C5 R1 复用 | 新建 constants 前无可复用现有同值 | ❌ | **见 #1 (CRITICAL)**: fn10/fn11/fn12 CID 标注错误导致 3 个 CID 常量归属混乱; fn10 实际 CID=0x198d (Magical Mallet) 已存在 MAGICAL_MALLET_CID (card_info.inc:842), 应 REUSE 但 proposal 标为 "none"; fn11 应为 INFERNO_RECKLESS_SUMMON_CID (REUSE card_info.inc:1613) 不是 MAGICAL_MALLET_CID; fn12 应为 WHITE_HORNS_DRAGON_CID (REUSE card_info.inc:553) 不是 INFERNO_RECKLESS_SUMMON_CID |
| C6 R2 名 | 槽名合规, 无碰撞 | ❌ | **见 #2 (CRITICAL)**: fn10 名为 `write_equip_zone_entry_substate_b_trampoline` 错误 (应为 `scan_zone_magical_mallet_substate_b`); fn11 名为 `scan_zone_magical_mallet_substate_d_e_b` 错误 (应为 `scan_zone_inferno_reckless_summon_substate_d_e_b`); fn12 名为 `scan_zone_inferno_reckless_summon_substate_e` 错误 (应为 `scan_zone_white_horns_dragon_substate_e`) |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | N/A | 无 carve; N/A |
| C8 R5 现名 | plate 无残留 `FUN_/DAT_/DWORD_` | ✅ | 20 个 plate 文本抽查: 无 FUN_/DAT_/DWORD_ 残留; BL 目标均引用语义名或十六进制地址 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 抽查 fn03/fn20 plate: `[^\x00-\x7F]` 匹配 0 命中; 所有 20 plates 纯 ASCII 确认 |
| C10 carve | 指针表条目 `+1` 正确 | N/A | 无 carve; N/A |
| C11 误名 | 函数体全局 vs 函数名矛盾已标 FUNC_RENAME | ❌ | **见 #2**: fn10/fn11/fn12 的函数名与 dispatch table 中 CID 直接矛盾; fn10 是 CID=0x198d (Magical Mallet) 的唯一 dispatch handler, 不是 "trampoline"; fn11/fn12 CID 各偏移一位 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | write_equip_zone_entry_by_substate plate 引用有效; dispatch table 地址 0x09e5a128 独立验证; gEquipEffectZoneBase=0x0201e4f0 pool 值 ROM 核对; CARD_FIELD_STAT_CLEAR_UPPER4_MASK 消费者 fn09 body 描述清晰; 置信度均 high |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ✅ | asm/11_effect_slot_puzzletext.s line 16402 有唯一 ROM_INCBIN 0x8cabc/0xd38; disasm plan 覆盖全段; C13 通过 |

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C5 — fn10/fn11/fn12 CID 赋值整体偏移一位; CID 常量归属全部错误

**独立验证方法**: python ROM read + dispatch table scan, 逐条核对 table_base=0x09e5a128, entry_size=8B。

**Dispatch table 实际读值**:

| Entry | addr | CID | fn_ptr | fn addr |
|-------|------|-----|--------|---------|
| 288 | 0x9e5aa28 | 0x198d (Magical Mallet) | 0x0808d055 | **0x0808d054 = fn10** |
| 289 | 0x9e5aa30 | 0x198e (Inferno Reckless Summon) | 0x0808d061 | **0x0808d060 = fn11** |
| 290 | 0x9e5aa38 | 0x1996 (White Horns Dragon) | 0x0808d1bd | **0x0808d1bc = fn12** |

**Proposal 错误声称**:
- fn10 (0x0808d054): CID = "none (trampoline)" → **WRONG**, CID = 0x198d (Magical Mallet)
- fn11 (0x0808d060): CID = 0x198d (Magical Mallet) → **WRONG**, CID = 0x198e (Inferno Reckless Summon)
- fn12 (0x0808d1bc): CID = 0x198e (Inferno Reckless Summon) → **WRONG**, CID = 0x1996 (White Horns Dragon)

**fn10 ref-scan**: thumb ref 0x0808d055 全 ROM 仅 1 个命中 @0x9e5aa2c (= dispatch table entry 288), fn11 body 完全不调用 fn10 (BL scan 确认 0 次命中)。因此 fn10 是 Magical Mallet 的独立 dispatch handler, 不是任何 trampoline。

**fn12 pool 核查**: fn12 (0x0808d1bc, size=0x68) 只有 2 个 pool DWord:
- 0x0808d21c = 0x0201c4e0 (gP1LifePoints) ✅
- 0x0808d220 = 0x00000868 (PLAYER_BLOCK_STRIDE) ✅

fn12 body 中无 gP1HandSlotArray pool slot (proposal body prose 写错, 实际 LDR 只引用上述 2 个 pool 地址)。

**CID 常量归属修正**:

| fn | addr | 实际 CID | 实际卡名 | CID 常量 | 状态 |
|----|------|----------|---------|---------|------|
| fn10 | 0x0808d054 | 0x198d | Magical Mallet | MAGICAL_MALLET_CID | REUSE (card_info.inc:842) |
| fn11 | 0x0808d060 | 0x198e | Inferno Reckless Summon | INFERNO_RECKLESS_SUMMON_CID | REUSE (card_info.inc:1613) |
| fn12 | 0x0808d1bc | 0x1996 | White Horns Dragon | WHITE_HORNS_DRAGON_CID | REUSE (card_info.inc:553) |

**fn11 的 NECROVALLEY_CID pool** (@0x0808d1b0=0x0000159d): fn11 的函数体确实包含 NECROVALLEY 检查, 且属于 CID=0x198e (Inferno Reckless Summon) 的 handler — 无论游戏逻辑是否直觉, dispatch table 赋值是权威。NECROVALLEY_CID REUSE 本身无误, 但所属 function 的 CID/名称须改为 Inferno Reckless Summon。

**必改**:
1. fn10 description: 删除 "CID: (none -- trampoline, NOT in dispatch table)"; 改为 "CID: 0x198d (Magical Mallet), dispatch entry [CID 0x198d]"
2. fn10 body: 移除 "trampoline stub" 描述; 改为 equip zone scan stub for Magical Mallet (12B handler, writes substate_b only)
3. fn10 "CID status" 改为: "MAGICAL_MALLET_CID(0x198d) REUSE (card_info.inc:842)"
4. fn11 "CID: 0x198d (Magical Mallet)" 改为: "CID: 0x198e (Inferno Reckless Summon)"
5. fn11 "CID status" 改为: "INFERNO_RECKLESS_SUMMON_CID(0x198e) REUSE (card_info.inc:1613)"
6. fn12 "CID: 0x198e (Inferno Reckless Summon)" 改为: "CID: 0x1996 (White Horns Dragon)"
7. fn12 "CID status" 改为: "WHITE_HORNS_DRAGON_CID(0x1996) REUSE (card_info.inc:553)"
8. fn12 body prose 中的 "gP1HandSlotArray" 引用删除 (pool 只有 2 个 DWord, 无 gP1HandSlotArray)
9. EQ_SLOTS 表中 fn11 对应的 REUSE 行: 从 MAGICAL_MALLET_CID 改为 INFERNO_RECKLESS_SUMMON_CID
10. EQ_SLOTS 表中 fn12 对应的 REUSE 行: 从 INFERNO_RECKLESS_SUMMON_CID 改为 WHITE_HORNS_DRAGON_CID

---

### #2 — C6 / C11 — fn10/fn11/fn12 函数名均错误; 须按实际 CID 更正

**fn10 (0x0808d054)**: 须从 `write_equip_zone_entry_substate_b_trampoline` 改为 `scan_zone_magical_mallet_substate_b`。
- substate 0xb confirmed: ROM @0x0808d056 = 0x210b (MOVS r1,#0xb) ✅
- Plate 须改为: `Equip zone scan for Magical Mallet (MAGICAL_MALLET_CID=0x198d). Stub: push{lr}; MOVS r1,#0xb; BL write_equip_zone_entry_by_substate (0x0808d88c); pop{r0};bx r0. write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x198d].`

**fn11 (0x0808d060)**: 须从 `scan_zone_magical_mallet_substate_d_e_b` 改为 `scan_zone_inferno_reckless_summon_substate_d_e_b`。
- Substates d/e/b confirmed (ROM reads: 0x210d @0x0808d0b4, 0x210e @0x0808d120, 0x210b @0x0808d182) ✅
- CID 引用: plate 中将 MAGICAL_MALLET_CID 替换为 INFERNO_RECKLESS_SUMMON_CID

**fn12 (0x0808d1bc)**: 须从 `scan_zone_inferno_reckless_summon_substate_e` 改为 `scan_zone_white_horns_dragon_substate_e`.
- Substate 0xe confirmed (ROM @0x0808d200 = 0x210e) ✅; BL 0x0808d204 -> 0x0808d88c ✅
- fn12 calls get_card_extended_stat_field6 (race) with result CMP 0x16 (Zombie race) — consistent with White Horns Dragon (searches for Zombie monsters)
- Plate 须引用 WHITE_HORNS_DRAGON_CID=0x1996 (REUSE)

**RENAME_SLOTS 表** (all 3 rows 须同步更新):
| addr | old_name | 旧 new_name (proposal) | 正确 new_name |
|------|----------|----------------------|--------------|
| 0x0808d054 | FUN_0808d054 | write_equip_zone_entry_substate_b_trampoline | scan_zone_magical_mallet_substate_b |
| 0x0808d060 | FUN_0808d060 | scan_zone_magical_mallet_substate_d_e_b | scan_zone_inferno_reckless_summon_substate_d_e_b |
| 0x0808d1bc | FUN_0808d1bc | scan_zone_inferno_reckless_summon_substate_e | scan_zone_white_horns_dragon_substate_e |

**CSV rows** (3 行须同步更新):
- `0x0808d054,scan_zone_magical_mallet_substate_b`
- `0x0808d060,scan_zone_inferno_reckless_summon_substate_d_e_b`
- `0x0808d1bc,scan_zone_white_horns_dragon_substate_e`

---

## 附注 (非阻断)

**A. Weak entry 0x0808d58c 定位错误 (不影响正确性)**

Proposal 声称 0x0808d58c 是 fn18 (0x0808d5b0) 体内的 BCC=0xd800。

独立核查:
- ROM @0x0808d58c = 0x4281 (CMP r1,r0), **不是** 0xd800 (BCC)
- 0x0808d58c 位于 fn17 [0x0808d494, 0x0808d494+0x11c) = [0x0808d494, 0x0808d5b0), offset=+0xf8, **在 fn17 体内而非 fn18 体内**

后果: Ghidra 在 disassemble fn17 时会自然处理 0x0808d58c 这两字节, 排除操作本身没有错误影响 (该地址不会被 Ghidra 误识为独立 function)。属于 proposal 中的证据描述错误, 不影响落地正确性。fixer 修正 proposal 时可顺带订正 weak entry 的文本描述, 但不需要为此阻断。

**B. fn12 body prose 轻微误导**

Proposal fn12 body 写 "monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray" — pool 中无 gP1HandSlotArray 槽 (LDR decode 确认仅 2 个 pool 地址)。fn12 实际是通过 gP1LifePoints 起始地址偏移遍历 slot array, 不用独立的 HandSlotArray 指针。REF_SLOTS 表本身无误 (只列了 2 个 pool), prose 描述需删除 "gP1HandSlotArray"。

---

## 独立核验数据汇总

| 核验项 | 独立结果 |
|--------|---------|
| Dispatch table 扫描 [0x0808cabc, 0x0808d7f4) | 21 entries (276..305+terminator), 与 proposal 匹配 (CID 赋值除外) |
| fn10 thumb-ref 全 ROM 扫描 (0x0808d055) | 1 次, @0x9e5aa2c (dispatch table only) |
| fn18 thumb-ref 全 ROM 扫描 (0x0808d5b1) | 2 次 (CID 0x19dc + CID 0x19dd) ✅ |
| EWRAM pool DWord count in range | 42 slots (17xLP+8xSetCode+7xHand+3xField+3xHandCnt+1xFieldSlot+1xSlotCnt+2xZoneBase) |
| PLAYER_BLOCK_STRIDE (0x868) pool count | 21 slots |
| Total REF = 42+21 | 63 ✅ (matches proposal) |
| Pool value spot-checks (20 values) | 全部 OK |
| Degenerate byte 0x0808d20e | 0x4285 = CMP r2,r1 ✅ |
| Degenerate word 0x0808d21c | 0x0201c4e0 = gP1LifePoints ✅ |
| Degenerate byte 0x0808d7de | 0x0000 = upper half of SLOT_CARD_SET_CODE_MASK ✅ |
| Weak entry 0x0808d58c | 0x4281 = CMP r1,r0 (NOT 0xd800 BCC); inside fn17 (NOT fn18) |
| C5 value-grep (5 NEW CIDs + mask + global) | 全 0 hits ✅ |
| MAGICAL_MALLET_CID (0x198d) | card_info.inc:842 EXISTS (REUSE for fn10) |
| INFERNO_RECKLESS_SUMMON_CID (0x198e) | card_info.inc:1613 EXISTS (REUSE for fn11) |
| WHITE_HORNS_DRAGON_CID (0x1996) | card_info.inc:553 EXISTS (REUSE for fn12) |
| Size sum (fn01..fn20) | 0xd38 ✅, last end = 0x0808d7f4 ✅ |
| All spans contiguous | ✅ (0 gap, 0 overlap) |
| ROM_INCBIN in Seg-4 range | exactly 1 (line 16402, to be eliminated) ✅ |
| fn11 substates | 0xd/0xe/0xb all confirmed by ROM byte reads ✅ |
| fn18 substates | 0xd/0xc confirmed ✅ |
| All plates <= 500 chars | ✅ (max=476 fn11) |

---

## Reviewer Verdict: F11-Seg-4g = NEEDS_FIX(2 items)
