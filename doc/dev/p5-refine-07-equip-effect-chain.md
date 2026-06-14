# 函数/数据细化计划 — `asm/07_equip_effect_chain.s`

> 阶段目标: 把 `asm/07_equip_effect_chain.s` (ROM `0x0805C2F0 ~ 0x080643E0`, 装备效果链 +
> 卡效果按 card_id 派发 `dispatch_effect_by_card_id_*` + 大量 `check_equip_slot_eligible_*` /
> `check_*_score` 谓词 + Neo Daedalus/zone 效果) **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **8** 个文件 (file 00..06 已全 10 段完成, 见对应 `p5-refine-0N-*.md`)。
> 方法论 + R1-R9 细化清单 + 三条硬规则见 `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..06 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间
ROM_INCBIN 必 carve/disasm 或 §5.1 / 全 ROM 0 引用→§5.1)。**R1-R9 详版**见
`doc/dev/p5-refine-00-system-str-vija.md` §一。复用资产清单见 `doc/dev/p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..06 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII** (CJK 会 Jython 双重 UTF-8 mojibake); **段内常残留命名期 CJK mojibake plate,
  executor 必 grep 段内非 ASCII, 逐个整段 ASCII 重写** (substring 替换对 CJK 静默 no-op; file 05 Seg-10 / file 06 Seg-5/7/9 反复)。
- **⚠ ROM_INCBIN 分类核心 (file 06 已确认 5 次, file 07 有 35 块, 主线工作)**: `0x09e4xxxx` 区有
  **card effect handler dispatch table** (格式 `CID_word + fn_ptr1(+1) [+ fn_ptr2(+1)...] + zero_pad`,
  FS 运行时加载), 用 **THUMB|1** 指针引用代码段谓词函数。每个函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - THUMB+1 命中**别一律当压缩偶合**; 核命中点周边 ROM: 前 4/8B 是合法 CID (`data/card-stats.s` 有 slot) +
    命中 = `<块>+1` 对齐 fn_ptr → **真引用 → R4 disasm 不 §5.1** (disasm 后块字节不变, byte-identical 不受影响;
    plate 注明 "reached via card effect handler dispatch table 0x09e4xxxx, <Card> CID 0xXXXX")。
  - 块内可能含**多 sub-fn**, 经 dispatch table raw 指针或 `mov pc,r0` 到达 (file 06 Seg-6/8 范式), 逐 sub-fn 边界核 + createFunction。
  - 仅 raw=0 且 THUMB+1=0 (或命中确非 table 结构) → 真孤儿 → §5.1。
  详见 memory `feedback-card-effect-handler-table-thumb-ref`。
- **R4 disasm 范式** (file 00 Seg-5c): clearListing 整 range → setTMode → 逐 stub DisassembleCommand;
  literal pool 须 clearListing+createDWord 强制 split 才能 export label; 重跑前先 clearListing 整 range 再 setTMode (否则 ContextChangeException)。
- **C5 双向核 (file 06 Seg-9 抓 9 同名+SPIRIT_RYU 误标)**: 标 **new** 的 CID 逐一 grep card_info.inc **0 命中**;
  标 **reuse** 的逐一 grep **确存在** (反向核); 记 grep 证据。**C5 偏移放宽** (不同 base 的 `*_OFF` 各建独立);
  **卡 ID / 掩码 / 位域 / 阈值等非偏移标量严格去重** (值碰撞必复用, 除非 state_code 碰 CID 才 RENAME-only)。
- **C13 残留 100% 覆盖**: executor 必 python 精确清点段内 DAT_/DWORD_/PTR_ 槽总数 (别漏 DWORD_, file 05 Seg-9/file 06 Seg-5/8 反复);
  EQ+REF+RENAME 三表并集 == 段内全集 (穷举对账 missing=0/extra=0); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实 passcode→slot_id→卡名 (**card record# != slot_id**, file 06 Seg-6 Otohime 教训);
  passcode 注释逐一 python 核对 (file 05/06 反复抓错); 未分配 → 中性 `cid_<hex>` 低置信, 勿臆造 (红线 3)。
- **C8 stale FUN_**: **穷举 pattern `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含每个函数 plate 上方行 + 一 plate 多 FUN_,
  含跨模块)**; 对每个 FUN_ 地址查现名 (naming-proposals.csv / asm label) 替换; 真无名 → 裸地址措辞; 落地后 grep 段范围 == 0。
- **EOL 数学自检**: 移位/算术/分支方向等式 python 实算 + 机器码核验 (file 05 Seg-7 <<19 / Seg-10 ble 方向); 算不准 → 中性 "exact semantics not decoded"。
- **fn-ptr +1 永久踩坑**: re-export 后须重补已知周期性修复槽: asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) /
  asm/04 (0x40ab4/0x42638/0x45efc/0x478f0) / asm/05 Seg-8 6 槽 / asm/06 各段 fn-ptr 槽。file 07 新 fn-ptr 同样处理。
- 复用 file 00..06 已建 constants/*.inc 与 carve label。

**file 02..06 已建可复用资产** (新建前必 grep): 见 `doc/dev/p5-refine-05-equip-eligibility-a.md` §一
(ewram.inc / duel_field.inc / card_info.inc ~430+ CID / oam_attr.inc / gl_scrollbar.inc / bitops.inc / 全局 / caller hub)。

---

## 二、落地工作流 (pipeline)

同 file 00..06 doc §二:
```
备份 .rep → Ghidra 脚本 (RefineF07Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改/建函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。
重段 (>~120 槽 或 多 ROM_INCBIN) 按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (07_equip_effect_chain.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------------|------|--------|
| 1 | 0x5c2f0..0x5cfec | 34+5 | 66 | 5 (0x5c40a/5e disasm, 0x5c4aa/2a §5.1, 0x5c608/28 disasm, 0x5cd86/2a disasm, 0x5cf1c/20 disasm) | ✅ | 7e1caa2 |
| 2 | 0x5cfec..0x5e358 | 34 | 83 | 2 (0x5dd3e/1a, 0x5ddda/d2) | ✅ | da58892 |
| 3 | 0x5e358..0x5f1cc | 34 | 40 | 4 (0x5e744/4c, 0x5ed4a/2a, 0x5ed8e/92, 0x5ee9c/ec) | ✅ | 2b80239 |
| 4 | 0x5f1cc..0x5fc94 | 34 | 45 | 5 (0x5f47e/1e, 0x5f8b4/40, 0x5f92e/3a, 0x5fa5c/28, 0x5fc10/2c) | ✅ | 667391b |
| 5 | 0x5fc94..0x60898 | 34 | 44 | 3 (0x6008c/28, 0x60386/32, 0x60588/7c) | ✅ | 3fcbbce |
| 6 | 0x60898..0x613b4 | 34 | 47 | 3 (0x60a86/90, 0x6106e/2e, 0x6121c/28) | ✅ | — |
| 7 | 0x613b4..0x61eb4 | 34 | 57 | 1 (0x61c66/2a) | ⬜ | — |
| 8 | 0x61eb4..0x62d28 | 34 | 49 | 5 (0x62378/2c, 0x623ec/60, 0x6246e/2a, 0x62a9c/2c, 0x62c52/66) | ⬜ | — |
| 9 | 0x62d28..0x63830 | 34 | 40 | 3 (0x62ebe/3e, 0x62f38/28, 0x636f8/38) | ⬜ | — |
| 10 | 0x63830..0x643e0 | 33 | 54 | 4 (0x6384e/2a, 0x63cf0/14, 0x63db4/40, 0x63fc4/24) | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
**35 个 ROM_INCBIN 块 (无 switchD 表)** — 绝大多数预判为 card effect handler dispatch table (0x09e4xxxx) 引用的谓词代码 →
逐块 ref-scan 按 §一 handler-table 法分类 (THUMB+1 命中核 CID+fn_ptr 结构 → R4 disasm; 真 0 引用 → §5.1)。
重段提示: Seg-2 (83 槽) / Seg-1+Seg-7 (57 槽) 较重, 必要时拆 Seg-Na/Nb。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录 (2026-06-14)

范围: ROM 0x0805c2f0..0x0805cfec (34 原有 fn + 5 disasm 新 fn = 39 fn)

**落地数据**:
- EQ=54 (PLAYER_BLOCK_STRIDE x15 + P1LP_BLOCK2_OFF_1CE8 x2 + FIELD_STATE_OFF x4 + gEquipChainSlotRefs x4 + gDuelFieldSlots x6 + gDuelPhaseFlags x1 + LP_BAR_ANIM_STATE_OFF x1 + SPRITE_ROW_ENTRY_DATA_OFF x1 + CHAIN_NODE_CARD_ARR_OFF x1 + 11 CID equates + 3 scalar reuse)
- REF=3 (gP1LifePoints 0x0201c4e0 x3)
- RENAME=9 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- PLATE=0 (无 stale FUN_; 无 CJK plate)
- FUNC_RENAME=0
- disasm=4 blocks (5 new fn): check_equip_slots_for_dreamer_blade_rabbit_dispatch@0x5c40c + check_equip_slots_for_sage_burial_army_dispatch@0x5c43c + check_equip_slots_for_cid_11a0_dispatch@0x5c608 + check_equip_slots_for_confiscation_duo_sentry_dispatch@0x5cd88 + check_equip_slots_for_adhesive_tape_trap_hole_dispatch@0x5cf1c
- §5.1: 1 orphan block (0x5c4aa/0x2a, 0-引用 THUMB code)
- card_info.inc +11 CID: SANGA_OF_THUNDER(0x1119)/SCAPEGOAT(0x12d2)/GRACEFUL_CHARITY(0x12cc)/GREENKAPPA(0x11f0)/REAPER_OF_CARDS(0x0ffa)/HARPIES_FEATHER_DUSTER(0x1246)/DRIVING_SNOW(0x134d)/NOBLEMAN_EXTERMINATION(0x1364)/BAIT_DOLL(0x149b)/cid_131c(0x131c)/cid_12fb(0x12fb)
- CSV sync: +5 rows (5 disasm new fn)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

### 4.02 Seg-2 完成记录 (2026-06-14)

范围: ROM 0x0805cfec..0x0805e358 (34 原有 fn + 5 disasm 新 fn = 39 fn)

**落地数据**:
- EQ=65 (PLAYER_BLOCK_STRIDE x16 + P1LP_BLOCK2_OFF_1CE8 x6 + FIELD_STATE_OFF x6 + EFFECT_ZONE_BITMASK_OFF x1 + P2_ZONE1_LP_OFF x1 + 20 CID REUSE + 15 CID NEW)
- REF=27 (gP1LifePoints x14 + gDuelFieldSlots x7 + gEquipChainSlotRefs x4 + gDuelPhaseFlags x1 + fn-ptr x1)
- RENAME=0 FUNC_RENAME=0
- PLATE=3 (check_equip_zone_effect_eligible_by_card_id BST desc + invoke_effect_node_handler zone-flag-guard + check_field_active_slot_or_zone_pair outer-loop)
- disasm=2 blocks (5 new fn): check_equip_zone_eligible_cid_134e@0x5dd40 + check_equip_zone_eligible_numinous_healer_and_recv@0x5dddc + check_equip_zone_eligible_appropriate@0x5de10 + check_equip_zone_eligible_forced_requisition@0x5de50 + check_equip_zone_eligible_minor_goblin_official@0x5de7c
- Literal pool fix: FixF07Seg1Seg2LiteralPools.py (13 slots: 8 Seg-1 + 5 Seg-2)
- Periodic fn-ptr fixes: asm/03 x4 (check_level_conv_lab_node_match+1 x2 + check_card_is_amazoness_type+1 x2) + asm/04 x3 (zone_monster_field_bonus_table+7*16 + apply_nitro_unit_equip_activation+1 + 0x0201d5b4) + asm/06 x1 (0x0201d5b4) + asm/07 x1 (check_equip_slot_eligible_by_equip_type+1)
- card_info.inc +19 new CID (DARK_HOLE/RAIGEKI/ALPHA_MAGNET_WARRIOR/BETA_MAGNET_WARRIOR/GAMMA_MAGNET_WARRIOR/cid_12f7/MAGIC_DRAIN/RIRYOKU_FIELD/TUTAN_MASK/CURSE_OF_ROYAL/TRAP_JAMMER/ARMOR_BREAK/NUMINOUS_HEALER/FORCED_REQUISITION/MINOR_GOBLIN_OFFICIAL/ATTACK_AND_RECEIVE/cid_135b/SPELL_STOPPING_STATUTE/ROYAL_SURRENDER)
- ewram.inc +1 (P2_ZONE1_LP_OFF=0x87c)
- CSV sync: +5 rows (5 disasm new fn)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

### 4.03 Seg-3 完成记录 (2026-06-14)

范围: ROM 0x0805e358..0x0805f1cc (34 原有 fn + 11 disasm 新 fn = 45 fn)

**落地数据**:
- EQ=24 (PLAYER_BLOCK_STRIDE x14 + FIELD_STATE_OFF x2 + CID x8: BANISHER_OF_THE_LIGHT/UMI_CARD_ID/REVIVAL_JAM/EQUIP_LOCKDOWN/RED_MOON_BABY/DARK_MAGICIAN_0FC9/DARK_MAGICIAN_142D + P1LP_BLOCK2_OFF_1CE8 + EFFECT_ZONE_BITMASK_OFF)
- REF=16 (gDuelFieldSlots x7 + gEquipChainSlotRefs x4 + gP1ZoneHandCount x2 + gP1LifePoints x2 + gP1LifePoints REF x1)
- RENAME=5 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- PLATE_SUB=2 (FUN_080839b4->tick_equip_placement_bitmap_display_4state in check_effect_activations_both_sides plate; FUN_08057874->tick_equip_slot_score_fill_display_seq in eval_spell_zone_equip_eligibility plate)
- FUNC_RENAME=0
- disasm=4 blocks (11 new fn):
  - Block1: check_equip_type480_cross_player_for_cid_13f9@0x5e744 + check_equip_type_bits_range6_8_for_cid_13fa@0x5e778 (bx lr exit)
  - Block2: check_slot_count_exceeds_2_for_cid_144e@0x5ed4c (bx lr exit)
  - Block3: check_zone_field6_hw_zero_for_cid_1450@0x5ed90 + check_zone_field6_hw_nonzero_for_cid_1451@0x5edc0 + check_opponent_lp_above_3000_for_cid_1460@0x5edf0 (bx lr exit)
  - Block4: check_free_monster_zone_for_cid_1468@0x5ee9c + check_neo_daedalus_no_banisher_for_cid_146f@0x5eeb8 + check_field_state24_neo_daedalus_for_cid_1472@0x5eee4 + check_chain_match_opponent_for_cid_1475@0x5ef10 + check_field_0c_nonzero_no_banisher_for_cid_147f@0x5ef4c (pop{r1}/bx r1 exit)
- Literal pool fix: FixF07Seg3LiteralPools.py (18 slots across all 4 blocks)
- fn-ptr periodic fix: asm/03 x4 (check_level_conv_lab_node_match+1 x2 + check_card_is_amazoness_type+1 x2) + asm/04 x3 (zone_monster_field_bonus_table+7*16 + apply_nitro_unit_equip_activation+1 + 0x0201d5b4) + asm/06 x1 (0x0201d5b4) + asm/07 x1 (check_equip_slot_eligible_by_equip_type+1)
- card_info.inc +2 new CID (REVIVAL_JAM_CID=0x13c7 / RED_MOON_BABY_CID=0x1415)
- CSV sync: +11 rows (11 disasm new fn)
- §5.1: 0 (all 4 blocks have confirmed THUMB+1 refs in 0x09e4xxxx handler tables)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

### 4.04 Seg-4 完成记录 (2026-06-14)

范围: ROM 0x0805f1cc..0x0805fc94 (34 原有 fn + 5 disasm 新 fn = 39 fn)

**落地数据**:
- EQ=44 (gP1LifePoints x6 DAT + PLAYER_BLOCK_STRIDE x9 DWORD+x3 DAT + gDuelFieldSlots x6 DWORD+x1 DAT + gEquipChainSlotRefs x6 DWORD + P1LP_BLOCK2_OFF_1CE8 x3 DWORD + gDuelEquipCtx x1 + BANISHER_OF_THE_LIGHT_CID x1 + SLOT_CARD_EMPTY x1 + FIELD_STATE_OFF x1 + FIELD5_SCORE_THRESHOLD_1999 x1 + FUSHI_NO_TORI_CID x1 + TSUKUYOMI_CID x1 + SWARM_OF_SCARABS_CID x1 + LIGHT_OF_INTERVENTION_CID x2 + LIFE_ABSORBING_MACHINE_CID)
- REF=2 (gP1LifePoints PTR slots x2: 0x0805f688, 0x0805f838)
- RENAME=1 (DWORD_0805f28c -> check_card_is_amazoness_type_ptr)
- PLATE_SUB=3 (FUN_0805f614->check_player_has_active_monster_return2 x1; FUN_0805f784->dispatch_slot_placement_check_by_card_id x2)
- FUNC_RENAME=0
- disasm=5 blocks (5 new fn):
  - Block1 0x5f480/0x1c: check_field_state_leq3_for_cid_14d4 (A Feint Plan CID=0x14d4)
  - Block2 0x5f8b4/0x40: check_zone640_opponent_turn_bit10_for_cid_151c (Drop Off CID=0x151c)
  - Block3 0x5f930/0x38: check_opp_turn_lp_leq1000_return2_for_cid_151e (Last Turn CID=0x151e)
  - Block4 0x5fa5c/0x28: check_player_lp_state_off10_nonzero (14 CIDs shared)
  - Block5 0x5fc10/0x2c: check_player_zone_count_above3_for_cid_1546 (Trap Dustshoot CID=0x1546)
- Literal pool fix: FixF07Seg4LiteralPools.py (11 slots across 5 blocks)
- Periodic fn-ptr/offset fixes: FixF07Seg4PeriodicFnPtrs.py + FixF07Seg4PeriodicFnPtrs2.py + FixF07Seg4SymbolPrimary.py
  - fn-ptr +1: asm/03 x2 (check_level_conv_lab_node_match+1 at 0x37884/0x3aa74) — remove DATA refs -> raw literal
  - table offset: asm/04 0x40ab4 -> zone_monster_field_bonus_dest_entry7 at 0x09e3f104 (fix primary symbol)
  - EWRAM offset: asm/04/06/07 x2 (0x80478f0/0x805b888 -> gDuelFieldSlotsEffectZoneBase at 0x0201d5b4, fix primary symbol)
- constants: ewram.inc +2 (gDuelEquipCtx=0x0201bbbc, gDuelFieldSlotsEffectZoneBase=0x0201d5b4); card_info.inc +4 CID (FUSHI_NO_TORI/TSUKUYOMI/SWARM_OF_SCARABS/LIFE_ABSORBING_MACHINE); rom.s +1 label (zone_monster_field_bonus_dest_entry7 at 0x09e3f104)
- CSV sync: +5 rows (5 disasm new fn)
- §5.1: 0
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

### 4.05 Seg-5 完成记录 (2026-06-14)

范围: ROM 0x0805fc94..0x08060898 (34 原有 fn + 6 disasm 新 fn = 40 fn)

**落地数据**:
- EQ=52 (gP1LifePoints x17 (slot label gp1lp_ptr_*) + PLAYER_BLOCK_STRIDE x14 (slot label player_stride_*) + CID REUSE x16 (SECOND_GOBLIN/BANISHER_OF_THE_LIGHT/BLUE_EYES_WHITE_DRAGON/NECROVALLEY/RING_OF_MAGNETISM/EQUIP_LOCKDOWN/PITCH_BLACK_POWER_STONE + 9 others) + CID NEW x3 (PEOPLE_RUNNING_ABOUT/OPPRESSED_PEOPLE/UNITED_RESISTANCE 0x15ca/cb/cc) + scalar NEW x2 (LP_SLOT_ACTIVE_OFF=0x10 / HAND_SLOT_TO_ZONE_COUNT_NEG_OFF=0xfffffbf4))
- REF=0; RENAME=0; FUNC_RENAME=0
- PLATE=10 (4 stale FUN_ substring subs + 6 CJK plate full ASCII rewrites)
  - FUN_ subs: check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14 / check_equip_slot_eligible_with_monster_count_gate / check_equip_slot_eligible_by_lp_status_and_slot_value / check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect
  - CJK rewrites: 0x0806019c / 0x080601dc / 0x080602a8 / 0x08060484 / 0x08060684 / 0x080607b4
- disasm=3 blocks (6 new fn):
  - Block1 0x6008c/0x28: check_equip_slot_eligible_by_lp_slot_for_cid_159a (Reasoning CID 0x159a)
  - Block2 0x60386/0x32: pad_word@0x60386 + check_equip_slot_eligible_by_type_and_player_for_cid_15dc@0x60388 (Helping Robo for Combat CID 0x15dc)
  - Block3 0x60588/0x7c: F1=check_equip_slot_eligible_by_active_player_phase_for_cid_15f0@0x60588 (Thunder of Ruler CID 0x15f0) + F2=check_equip_slot_eligible_by_active_player_phase_for_cid_15f2@0x605b8 (Meteorain CID 0x15f2) + F3=check_equip_slot_eligible_by_monster_zone_type_for_cid_15f3@0x605f0 (Pineapple Blast CID 0x15f3)
  - Block4 0x60800/0x8: check_equip_slot_eligible_active_player_with_chain_and_node_count@0x60800 (Pitch-Black Power Stone CID 0x1624, body continues in named asm@0x60808)
- Literal pool fix: FixF07Seg5LiteralPools.py (9 DWORD slots: Block1 x2 + Block3-F1 x3 + Block3-F2 x3 + Block4 named-asm-area x1)
- Periodic fn-ptr fix: FixF07Seg4PeriodicFnPtrs.py (known periodic fn-ptr slots asm/03..07)
- constants: card_info.inc +8 CID (PEOPLE_RUNNING_ABOUT/OPPRESSED_PEOPLE/UNITED_RESISTANCE + REASONING/HELPING_ROBO_FOR_COMBAT/THUNDER_OF_RULER/METEORAIN/PINEAPPLE_BLAST); ewram.inc +3 (LP_SLOT_ACTIVE_OFF=0x10 / LP_LOOP_CEIL_OFF=0xc / HAND_SLOT_TO_ZONE_COUNT_NEG_OFF=0xfffffbf4); duel_field.inc +1 (ZONE_DETAIL_FIELD_MASK_F88=0x00f88000)
- carve=0
- CSV sync: +6 rows (6 disasm new fn)
- §5.1: 0
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

### 4.06 Seg-6 完成记录 (2026-06-14)

范围: ROM 0x08060898..0x080613b4 (34 原有 fn + 3 disasm 新 fn = 37 fn)

**落地数据**:
- EQ=47 (gP1LifePoints x10 + PLAYER_BLOCK_STRIDE x9 + P1LP_BLOCK2_OFF_1CE8 x2 + FIELD_STATE_OFF x1 + ZONE_DETAIL_FIELD_MASK_F88 x1 + gDuelFieldSlots x2 + gEquipChainSlotRefs x1 + CID REUSE x17 (FRIENDSHIP/UNITY/MUSTERING_DS/DMG/DON_ZALOOG x2/BANISHER/TERRORKING/CLIFF/DS_CHICK/DS_GORG/DS_MEANAE/CRIMSON_NINJA/BLS_ENVOY x2/OJAMA_GREEN/OJAMA_BLACK) + CID NEW x4 (SAGES_STONE/QUEENS_KNIGHT/OJAMA_YELLOW/CHAOS_EMPEROR_DRAGON))
- REF=0; RENAME=0; FUNC_RENAME=0
- PLATE=6 (6 CJK plate full ASCII rewrites: 0x08060974/0x08060a5c/0x08060c30/0x08060e24/0x08060fe8/0x080612e4; 0x08060fe8 also corrects semantic error DUEL_STATE_PTR->gEquipChainSlotRefs)
- disasm=3 blocks (3 new fn):
  - Block1 0x60a86/0x90: check_exodia_set_in_extra_for_cid_165b@0x08060a88 (Contract with Exodia CID 0x165b; 5 Exodia piece CIDs + EXODIA_NECROSS in literal pool)
  - Block2 0x6106e/0x2e: check_zone_type580_direction_mismatch_for_cid_16c6@0x08061070 (Fenrir CID 0x16c6; leaf fn)
  - Block3 0x6121c/0x28: check_lp_zone_hand_above6_for_cid_16d1@0x0806121c (Chaos End CID 0x16d1; literal pool: gP1LifePoints+PLAYER_BLOCK_STRIDE)
- card_info.inc +12 CID: QUEENS_KNIGHT(0x157f)/CONTRACT_WITH_EXODIA(0x165b)/SAGES_STONE(0x167e)/OJAMA_YELLOW(0x16b3)/FENRIR(0x16c6)/CHAOS_END(0x16d1)/CHAOS_EMPEROR_DRAGON(0x16e4)/RIGHT_LEG/LEFT_LEG/RIGHT_ARM/LEFT_ARM/EXODIA_THE_FORBIDDEN_ONE (0x0fb7-0x0fbb)
- CSV sync: +3 rows (3 disasm new fn)
- carve=0; §5.1=0
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

---

## §5.1 零引用块登记 (Seg-1)

| addr | size | Seg | judgment | ref-scan evidence |
|------|------|-----|----------|-------------------|
| 0x0805c4aa | 0x2a (42B) | Seg-1 | orphan THUMB code | raw=0, THUMB+1=0 全穷举; 起始 .zero 2 + 有效 THUMB code 但无任何 ROM 指针引用 |

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 07 范围 `[0x0805c2f0, 0x080643e0)` (339 named fn, ~516 DAT_/DWORD_/PTR_ 槽, 35 ROM_INCBIN 块, 0 switchD)
> 按**函数数**均分 10 段 (~34 fn/段, 边界=函数结束处=下一函数起点)。

| Seg | 地址范围 | ~fn | ~slots | ROM_INCBIN 数 | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x5c2f0..0x5cfec | 34 | 57 | 5 | dispatch_effect_by_card_id_with_display_lookup + 效果派发簇头 |
| Seg-2 | 0x5cfec..0x5e358 | 34 | 83 | 2 | check_spell_zone_effect_activatable + spell/zone 效果谓词簇 |
| Seg-3 | 0x5e358..0x5f1cc | 34 | 40 | 4 | check_monster_slot_field5_score_in_range + score 谓词簇 |
| Seg-4 | 0x5f1cc..0x5fc94 | 34 | 45 | 5 | check_equip_slot_at_turn_player_side + turn/side 谓词簇 |
| Seg-5 | 0x5fc94..0x60898 | 34 | 44 | 3 | check_equip_slot_eligible_by_chain_score_and_owner 簇 |
| Seg-6 | 0x60898..0x613b4 | 34 | 47 | 3 | check_equip_slot_eligible_by_lp_slot_and_effect_dispatch 簇 |
| Seg-7 | 0x613b4..0x61eb4 | 34 | 57 | 1 | check_equip_slot_eligible_by_card_id_graveyard_threshold 簇 |
| Seg-8 | 0x61eb4..0x62d28 | 34 | 49 | 5 | check_equip_slot_eligible_by_zone_slot_flag_and_status 簇 |
| Seg-9 | 0x62d28..0x63830 | 34 | 40 | 3 | store_slot_effect_value_from_card + 效果值存取簇 |
| Seg-10 | 0x63830..0x643e0 | 33 | 54 | 4 | check_opponent_monster_slot_present 簇 (文件末) |

执行约定同 file 00..06: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-06-equip-eligibility-b.md` (file 06: handler-table disasm 分类 / cascading sub-fn / CJK plate 重写 / C5 双向核)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
