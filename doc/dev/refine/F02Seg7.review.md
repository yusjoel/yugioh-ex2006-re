# Refine Review: F02Seg7

**文件**: `asm/02_text_lp_fieldspell.s`
**段范围**: `[0x0803217c, 0x08032e80)` — 23 fn, 67 DAT_/DWORD_ slots
**Proposal**: `doc/dev/refine/F02Seg7.proposal.md`
**Reviewer**: 独立复核 (不信 proposal 自检结论)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | §五表: Seg-7 = 0x3217c..0x32e80; Seg-6 已 commit 8051a2e; 无跳号 |
| C2 Rule2 | ROM_INCBIN/.byte 块全有归宿 | ✅ | 段内 `grep .incbin` = 0; C2 N/A (无 incbin 块) |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | 段内无 ROM_INCBIN; C3 N/A |
| C4 R1 值 | EQ value == ROM 4字节小端 | ✅ | 独立 python 核对全部 7 个关键槽 + 17 card_id 槽 + 36 spot-check reuse 槽; 全匹配 |
| C5 R1 复用 | 新建常量前无现有同值 | ✅ | 扫描全 19 constants/*.inc: 0x10a4/0x10d0/0x0201c5d8 均无现有定义; PLAYER_BLOCK_STRIDE/gDuelFieldSlots/gDuelEffectChainSlots/gEquipChainSlotRefs 正确复用 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | 67 个 slot_label 全通 regex; 无重复; 同函数多同类槽用 `_b/_c` 后缀区分 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | 本段无 carve 块; C7 N/A |
| C8 R5 现名 | plate 引用全用现名 | ✅ | 5 个 plate 均计划整段 setPlateComment 重写; 所有 FUN_ 替换目标经独立核对: 0x08037630=place_equip_card_if_type_matches, 0x0803412c=check_card_matches_active_effect_slot, 0x0804074c=tick_card_effect_category_display_seq, 0x08032960=count_equip_eligible_slots_for_player, 0x08032a6c=count_equip_eligible_slots_both_players, 0x080325dc=check_card_equip_eligibility_in_field, 0x080490b4=tick_duel_field_zone_sprite_update_pipeline, 0x0808db90=dispatch_equip_pair_sprites_by_state, 0x08048020=render_slot_card_sprite_and_effects, 0x08048364=render_slot_card_sprite_with_chaos_equip_check, 0x08099aac=run_equip_slot_display_update_state_machine, 0x08099e0c=run_equip_spell_display_state_machine; 全 verified |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 5 个 plate 文本 `grep -P '[^\x00-\x7F]'` = 0; 全 ASCII |
| C10 carve | 指针表 THUMB +1 核对 | ✅ | 本段无 carve 块; C10 N/A |
| C11 误名 | 函数体全局 vs 函数名矛盾 | ✅ | 抽查 clear_zone_slot_chain_refs / count_field_copies_of_card / count_equip_eligible_slots_both_players 体: 操作语义与函数名一致; 无误名信号 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | EFFECT_ZONE_PARTITION_OFF: L14164/L14578/L14734/L14336 plate 注释 (high); EFFECT_ZONE_BITMASK_OFF: L14645-14650 ldr/ands/beq 指令序列直接证明 bit0 bitmask test (high); gDuelFieldSlots_p2_base: L14164/L14336 plate 注释 + gDuelFieldSlots+0xc8=0x14*10=0x0201c5d8 算术验证 (high) |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ✅ | `grep DAT_/DWORD_` 段内精确 = 67; EQ 48 + RENAME 19 = 67; 全覆盖; 无 PTR_DAT_/PTR_FUN_/UNK_ 遗漏 |

---

## 独立复核结论

### ROM 字节核对 (C4)

自己 python 读 ROM, 核对结果:

| 槽地址 | ROM 原始字节 | 解出值 | Proposal 值 | 一致 |
|--------|------------|--------|------------|------|
| 0x08032274 | `68080000` | 0x00000868 | PLAYER_BLOCK_STRIDE | OK |
| 0x08032278 | `10c50102` | 0x0201c510 | gDuelFieldSlots | OK |
| 0x0803227c | `a4100000` | 0x000010a4 | EFFECT_ZONE_PARTITION_OFF | OK |
| 0x08032230 | `54bc0102` | 0x0201bc54 | gDuelEffectChainSlots | OK |
| 0x08032a64 | `d0100000` | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | OK |
| 0x08032a68 | `90bb0102` | 0x0201bb90 | gEquipChainSlotRefs | OK |
| 0x08032798 | `d8c50102` | 0x0201c5d8 | gDuelFieldSlots_p2_base | OK |
| 0x080321bc | `c0210308` | 0x080321c0 | switchD_0803217c ptr | OK |
| 0x0803229c | `a0220308` | 0x080322a0 | switchD_0803229a ptr | OK |

card_id whitelist 槽 (全部抽查): 0x08032390=0x10f5, 0x080323a4=0x10f3, 0x080323c0=0x1345, 0x080323d4=0x1346, 0x0803263c=0x166c, 0x08032640=0x12bf, 0x08032644=0x148e, 0x08032648=0x14da — 全 OK。

36 个 EQ REUSE 槽 spot-check (PLAYER_BLOCK_STRIDE x18 + gDuelFieldSlots x16 + DWORD x2): 全 OK。

### ref-scan (C3)

本段无 ROM_INCBIN 或 `.byte` 块 (grep 验证 = 0 条), ref-scan 步骤 N/A。

### C5 值去重

扫描 19 个 constants/*.inc 文件:
- `0x000010a4` (EFFECT_ZONE_PARTITION_OFF): 未见任何现有定义 → 新建合规
- `0x000010d0` (EFFECT_ZONE_BITMASK_OFF): 未见任何现有定义 → 新建合规
- `0x0201c5d8` (gDuelFieldSlots_p2_base): 未见任何现有定义; 地址算术 gDuelFieldSlots(0x0201c510)+0xc8=0x14×10=0x0201c5d8 验证正确 → 新建合规

### C8 stale FUN_ 映射核对

独立核查 12 个 FUN_ → 现名映射, 全部通过:
- FUN_08037630 → place_equip_card_if_type_matches (asm/03_equip_chain_hand.s L3208, push @ 08037630)
- FUN_0803412c → check_card_matches_active_effect_slot (asm/02 L17939, push @ 0803412c)
- FUN_0804074c → tick_card_effect_category_display_seq (asm/04 L844, push @ 0804074c)
- FUN_08032960 → count_equip_eligible_slots_for_player (asm/02 L14580, push @ 08032960)
- FUN_08032a6c → count_equip_eligible_slots_both_players (asm/02 L14719, push @ 08032a6c)
- FUN_080325dc → check_card_equip_eligibility_in_field (asm/02 L14104)
- FUN_080490b4 → tick_duel_field_zone_sprite_update_pipeline (asm/05 L88, push @ 080490b4)
- FUN_0808db90 → dispatch_equip_pair_sprites_by_state (asm/11 L6113, push @ 0808db90)
- FUN_08048020 → render_slot_card_sprite_and_effects (asm/04 L17765, push @ 08048020)
- FUN_08048364 → render_slot_card_sprite_with_chaos_equip_check (asm/04 L18202, push @ 08048364)
- FUN_08099aac → run_equip_slot_display_update_state_machine (asm/12 L11834, push @ 08099aac)
- FUN_08099e0c → run_equip_spell_display_state_machine (asm/12 L12280, push @ 08099e0c)

注: proposal 摘要称 "14 处 stale FUN_ 替换" 与实际统计 (5 个 plate 共 16 个 FUN_ 出现, 其中含重复) 存在数字差异, 但采用 setPlateComment 整段重写方式即可完全消除, 不影响落地正确性。

### EFFECT_ZONE_BITMASK_OFF 语义核对

Proposal 注释: "r10=gDuelFieldSlots-0x30; r10+0x10d0=gDuelFieldSlots+0x10a0=0x0201d5b0"

验算: gDuelFieldSlots(0x0201c510)-0x30 = 0x0201c4e0 = gP1LifePoints; gP1LifePoints+0x10d0 = 0x0201d5b0 = gDuelFieldSlots+0x10a0 — 算术正确。

L14645-14650 指令序列: `ldr r0,DAT_08032a64` + `add r0,r10` + `ldr r0,[r0,#0]` + `ands r0,r1(=1)` + `beq LAB_08032a48` — 直接证明 bit0 occupation bitmask test, 置信度 high。

---

## 状态: PASS

本 proposal 全部 13 项核验通过。无需修改。可直接进入落地 (fixer 模式 B)。

---

## 修改清单

无 (PASS, 无 NEEDS_FIX 项)。
