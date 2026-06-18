# 函数/数据细化计划 — `asm/08_equip_oam_neodaed.s`

> 阶段目标: 把 `asm/08_equip_oam_neodaed.s` (ROM `0x080643E0 ~ 0x0806E76C`, 装备 OAM sprite 提交 +
> Neo Daedalus 效果 + effect-zone LP/sprite 派发 + field-spell placement display) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **9** 个文件 (file 00..07 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..07 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用→§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..07 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **⚠ ROM_INCBIN 分类核心 (file 06/07 已确认 N 次)**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - **`0x09e4xxxx`/`0x09e3xxxx` = card effect handler dispatch table** (entry 0x18B = `[CID, fn_activate(+1), pad, fn_eligible(+1), pad, pad]`,
    FS 运行时加载); **fn_eligible 块的 CID 在 fn_ptr 地址 -0xc 位置** (别取错下一 entry, file 07 Seg-5 教训); THUMB+1 命中核 fn_ptr-0xc 处 CID
    (python 实读, card-stats.s 坐实) → 真引用 → R4 disasm。
  - **file 08 特征 (OAM/sprite)**: 部分大 ROM_INCBIN 块 (0x374/0x298/0x27c/0x25c/0x19c/0x3d0 等) 可能是 **OAM sprite 属性数据表** (被代码 ldr/表索引引用 → carve 进 rom.s 结构化)
    而非 handler 代码。ref-scan 命中点是 ldr 字面量池/表基址 → carve (label + 结构化 + round-trip); 命中是 THUMB|1 fn-ptr → disasm。逐块据实判。
  - 块内可能多 sub-fn (经 dispatch raw 指针/mov pc,r0/switchD 到达); 仅 raw=0 且 THUMB+1=0 → §5.1。
  详见 memory `feedback-card-effect-handler-table-thumb-ref` + `refine-carve-rom-tables-immediately`。
- **switchD 跳转表 (file 08 含 5: 0x65a44/0x66f02/0x686a2/0x69edc/0x6ac1e)**: jump table 目标裸 THUMB 地址 → R4 disasm 逐 stub
  (file 00 Seg-5c 范式); case stub 可级联 bl ROM_INCBIN helper (file 06 Seg-6/8)。
- **R4 disasm 范式**: clearListing 整 range → setTMode → 逐 stub DisassembleCommand; literal pool createDWord 强制 split。
- **机器码核 (file 07 Seg-8/9 教训, 必做)**: disasm fn 比较+分支指令独立解码 (0x3801=subs#1, 0xd0xx=beq/0xd1xx=bne/0xd8xx=bhi/0xd9xx=bls, 0x4048=EOR≠AND, 0x4002=ands r2,r0,
  ldrh imm5×2 偏移); 函数名运算符/偏移/卡名与机器码一致; **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核 (file 07 反复抓误标)**: 标 **new** CID 逐一 grep 0 命中; 标 **reuse** 逐一 grep 确存在; 记证据。
  **C5 偏移放宽** (不同 base `*_OFF` 各建独立); **卡 ID/掩码/位域/阈值非偏移严格去重** (值碰撞必复用, 语义截然不同的两实体 [sprite param vs card_id] 各建独立, 读消费者裁定)。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集 (穷举对账); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实 (card record# != slot_id); passcode 逐一 python 核对; 未分配→中性 `cid_<hex>`, 勿臆造 (红线 3)。
- **误名警觉 (file 06/07 高频)**: 函数名/plate 称的卡名/全局与函数体矛盾即误名 (已抓 Otohime/Crimson Ninja/Banisher of Light/Uria/DUEL_STATE_PTR);
  gEquipChainSlotRefs=0x0201bb90 常被误称; 误名走 FUNC_RENAME/CONST_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 每个 FUN_ 地址查现名替换; 落地后 grep == 0。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04 (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05 Seg-8 6 槽 / asm/06/07 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责; file 07 Seg-9 executor 越界自评无效)。

**file 02..07 已建可复用资产** (新建前必 grep): 见 `p5-refine-05-equip-eligibility-a.md` §一 (ewram/duel_field/card_info ~510+ CID/oam_attr/gl_scrollbar/bitops/全局)。

---

## 二、落地工作流 (pipeline)

同 file 00..07 doc §二:
```
备份 .rep → Ghidra 脚本 (RefineF08Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改/建函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor → reviewer (C1-C13) → fixer (模式A/模式B)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (08_equip_oam_neodaed.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN/switch | 状态 | commit |
|-----|------|-----|--------|-------------------|------|--------|
| 1 | 0x643e0..0x6544c | 20 | 87 | 2 (0x6456c/2c, 0x645ee/1e) | ✅ | f0d7a85 |
| 2 | 0x6544c..0x66448 | 20 | 79 | 3 (0x65d78/3c, 0x65e3c/29c, 0x662a4/68) + switchD_08065a44 | ✅ | 4b6b4a4 |
| 3 | 0x66448..0x67160 | 20 | 56 | 1 (0x668c0/1cc) + switchD_08066f02 | ✅ | d6a40a5 |
| 4 | 0x67160..0x67fa4 | 20 | 74 | 0 | ✅ | 5b5eeae |
| 5 | 0x67fa4..0x690dc | 20 | 65 | 0 + switchD_080686a2 | ✅ | 82b4d8a |
| 6 | 0x690dc..0x6a118 | 20 | 90 | 1 (0x696d8/1c) + switchD_08069edc | ✅ | (see §4.06) |
| 7 | 0x6a118..0x6ab0c | 20 | 47 | 0 | ✅ | (see §4.07) |
| 8a | 0x6ab0c..0x6b56c | 6 | 22 | 4 ROM_INCBIN (3 disasm + §5.1 1) + switchD_0806ac1e | ✅ | 638c7d4 |
| 8b | 0x6b56c..0x6c0cc | 4+30(disasm) | 63 | 5 DISASM | ✅ | (see §4.09) |
| 8c | 0x6c0cc..0x6cbe8 | 9+9(disasm) | 39 | 2 DISASM | ✅ | 4c7b3d0 |
| 9 | 0x6cbe8..0x6d960 | 20 | 52 | 0 | ✅ | (see §4.11) |
| 10 | 0x6d960..0x6e76c | 11 | 46 | 4 (0x6dbcc/44, 0x6dc3c/3d0, 0x6e3fa/4e, 0x6e460/1cc) | ✅ | (see §4.12) |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
**22 ROM_INCBIN + 5 switchD** — 逐块 ref-scan 按 §一 分类 (handler-table THUMB+1→disasm / OAM 数据表 ldr-ref→carve / switchD→R4 disasm / 0 引用→§5.1)。
**重段提示**: Seg-8 (85 槽 + **11 ROM_INCBIN 含大表 0x374/0x298/0x27c/0x25c/0x19c/0x110**, OAM sprite 数据表/dispatch 簇) 最重, 已拆 Seg-8a (✅)/8b (✅)/8c (✅) **Seg-8 全完成**;
Seg-6 (90 槽) / Seg-1 (87 槽) / Seg-10 (4 块含 0x3d0=976B) 次重。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录 (0x643e0..0x6544c)

- **EQ**: 87 槽 (PLAYER_BLOCK_STRIDE x12, gDuelFieldSlots x5, gP1LifePoints x1, gDuelFieldSlots_p2_base x1, gEquipChainSlotRefs x1, 29 CID reuse, 4 duel_field.inc reuse, 27 new CID, 8 LP delta new)
- **RENAME**: 13 (PTR_gP1LifePoints_* → write_equip_lp_*_lp_base 描述性标签)
- **PLATE**: 17 (3 stale FUN_ → 当前名; 14 函数 entry plate 新设; file header mojibake 修正 via split_manifest.tsv)
- **DISASM**: 2 ROM_INCBIN → THUMB:
  - Block1 `check_opponent_chain_zone_count_gt1_for_cid_19df` @ 0x0806456c (0x2c B, CID=0x19df Success Probability 0%)
  - Block2 `check_alt_hand_sum_nonzero_for_cid_19ef` @ 0x080645f0 (0x1e B, CID=0x19ef Elemental Hero Erikshieler; 2B pad @ 0x080645ee)
- **新建 inc**: `constants/equip_lp_delta.inc` (8 LP penalty equates: NEG_300/500/600/800/1200/1500/2000/3000)
- **card_info.inc**: +27 CID (DES_KOALA/WOODLAND_SPRITE/cid_10fe/cid_12e8/GRIGGLE/REFLECT_BOUNDER 等)
- **rom.s**: 加入 equip_lp_delta.inc .include
- **CSV sync**: +2 行 (2 新 disasm 函数)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra 脚本**: `RefineF08Seg1Slots.py` + `DisassembleF08Seg1Blocks.py`

### 4.02 Seg-2 完成记录 (0x6544c..0x66448)

- **EQ**: 65 槽 (LP delta x5 [NEG_500/NEG_2000 reuse + NEG_1000 新建+reuse + NEG_800 reuse]; PLAYER_BLOCK_STRIDE x10 reuse; gEquipChainSlotRefs x1 / gDuelPhaseFlags x7 / gDuelFieldSlots x4 / gDuelCardCtxBase x2 / gEquipZoneCountTable x1 reuse; EQUIP_ACTIVE_CTX_OFF x1 reuse / EQUIP_PHASE_FRAME_OFF x3 新建; LP_BANISHER_CTX_OFF x1 reuse; 21 CID reuse + 17 CID 新建; OAM_ATTR_P1_SPRITE x1 新建)
- **REF**: 13 槽 (gP1LifePoints fn-ptr x9 + THUMB callback fn-ptr x2 + switchD table ptr x1 + dispatch jump table ptr x1)
- **RENAME**: 10 (PTR_gP1LifePoints_* 改名为描述性 slot label; 含 dispatch_equip_chain_state_jump_table: label)
- **PLATE**: 11 (FUN_08064880 x8 → dispatch_equip_lp_delta_by_card_id; FUN_080655da x1 → restore_equip_effect_frame; FUN_080712a0 x1 → dispatch_equip_chain_state_if_tile_count_valid; gEquipEffectCtx x1 → gEquipChainSlotRefs)
- **DISASM**: 3 ROM_INCBIN → THUMB (18 新函数):
  - Block1 `check_equip_eligible_state_dispatch_for_time_wizard` @ 0x08065d78 (0x3c B, CID=0x0fb6 Time Wizard fn_eligible handler; dispatches via 34-entry raw-addr jump table at 0x08065db4 to Block2 sub-fns)
  - Block2 12 sub-fn stubs @ 0x08065e3c..0x080660d7 (0x29c B): `equip_state_stub_{80/7f/7e/78/77/6d/64/63/61/60/5f/default}_time_wizard`; reached via raw-addr bx dispatch from table at 0x08065db4
  - Block3 5 case stubs @ 0x080662a4..0x0806630b (0x68 B): `equip_chain_state_stub_{80/7e/7d/78/64}`; reached via jump table at 0x08066230 in dispatch_equip_chain_state_by_slot_ownership
- **新建 constants**: equip_lp_delta.inc +1 (LP_EQUIP_DELTA_NEG_1000); ewram.inc +1 (EQUIP_PHASE_FRAME_OFF=0x4a4); oam_attr.inc +1 (OAM_ATTR_P1_SPRITE=0x8027); card_info.inc +17 CID (TIME_WIZARD/DRAGON_CAPTURE_JAR/DARK_RABBIT/SKELENGEL/FLUTE_SUMMONING_DRAGON/AIRKNIGHT_PARSHATH/CARD_OF_SAFE_RETURN/DES_LACOODA/CALL_OF_THE_MUMMY/HIDDEN_SOLDIER/PRECIOUS_CARDS_FROM_BEYOND/MOLTEN_ZOMBIE/DON_TURTLE/AVATAR_OF_THE_POT/ATOMIC_FIREFLY/MAGNET_CIRCLE_LV2/CHAINSAW_INSECT)
- **carve**: 0 (no ROM data tables; all 3 blocks are THUMB code)
- **§5.1**: 0 (all blocks have confirmed ROM references)
- **CSV sync**: +18 rows (18 new disasm functions)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg2Slots.py` + `DisassembleF08Seg2Blocks.py`

### 4.03 Seg-3 完成记录 (0x66448..0x67160)

- **EQ**: 51 槽 (DE_SPELL_CID/CYBER_STEIN_CID/ICID_RESERVED_A/B/C 新建 x5; OAM_ATTR_P2_SPRITE 新建 x1; PLAYER_BLOCK_STRIDE x14 / gDuelFieldSlots x7 / gDuelPhaseFlags x9 / gDuelCardCtxBase x3 / gP1HandSlotArray x2 / gEquipZoneCountTable x1 / EQUIP_PHASE_FRAME_OFF x3 / P1LP_BLOCK2_OFF_1CE8 x1 / gDuelEquipCtx x1 / LP_CARD_TRACK_NEXT_OFF x1 / gP1SlotSetCodeArray x1 reuse; ARMED_NINJA_CID/RAVIEL_LORD_CID/TADPOLE_CID/POLYMERIZATION_CID/BATTLE_SCARRED_CID/SHADOW_SPELL_CID/NINJITSU_ART_OF_DECOY_CID/SANGA_OF_THUNDER_CID reuse)
- **REF**: 4 槽 (gP1LifePoints raw-addr x2: dispatch_reserved_icid_lp_base + render_equip_zone_lp_base; dispatch_equip_zone_by_effect_type_jump_table ptr x1; switchD_08066f02__switchdataD_08066f0c ptr x1)
- **RENAME**: 2 (via EQ plan descriptive slot labels; no explicit FUNC_RENAME)
- **PLATE**: 2 (apply_lp_delta_for_slot_player stale FUN_ x2: FUN_08073428->apply_lp_delta_for_slot_by_series_code + FUN_08074770->dispatch_dragon_summon_or_lp_delta_by_slot_type)
- **DISASM**: 1 ROM_INCBIN 0x080668c0/0x1cc -> R4 THUMB disasm (8 raw refs; 0 THUMB+1; dispatch via MOV PC,r0 from jump table at 0x08066890):
  - `dispatch_equip_effect_type_stub_80` @ 0x080668c0 (state=0x80, entry[11])
  - `dispatch_equip_effect_type_stub_7f` @ 0x0806691c (state=0x7f, entry[10])
  - `dispatch_equip_effect_type_stub_7e` @ 0x08066934 (state=0x7e, entry[9])
  - `dispatch_equip_effect_type_stub_7d` @ 0x08066a58 (state=0x7d, entry[8])
  - `dispatch_equip_effect_type_stub_78` @ 0x08066a62 (state=0x78, entry[3])
  - `dispatch_equip_effect_type_stub_77` @ 0x08066a6e (state=0x77, entry[2])
  - `dispatch_equip_effect_type_stub_76` @ 0x08066a7a (state=0x76, entry[1])
  - `dispatch_equip_effect_type_stub_75` @ 0x08066a86 (state=0x75, entry[0])
  - States 0x79..0x7c (entries[4..7]) -> fall-through to LAB_08066a8c (outside block)
- **switchD_08066f02**: already fully disassembled inline; no additional disasm action
- **新建 constants**: card_info.inc +5 (DE_SPELL_CID=0x12eb/CYBER_STEIN_CID=0x114a/ICID_RESERVED_A=0x162c/ICID_RESERVED_B=0x184c/ICID_RESERVED_C=0x1051); oam_attr.inc +1 (OAM_ATTR_P2_SPRITE=0x8059)
- **carve**: 0 (block is THUMB code, not data table)
- **§5.1**: 0 (block has 8 confirmed raw refs)
- **CSV sync**: +8 rows (8 new disasm stub functions)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg3Slots.py` + `DisassembleF08Seg3Blocks.py`

### 4.04 Seg-4 完成记录 (0x67160..0x67fa4)

- **EQ**: 73 槽 (gDuelPhaseFlags x13 / gDuelFieldSlots x8 / PLAYER_BLOCK_STRIDE x14 / EQUIP_PHASE_FRAME_OFF x6 / EQUIP_ACTIVE_CTX_OFF x1 / gP1LifePoints x2 / gDuelCardCtxBase x1 / gP1SlotSetCodeArray x1 / LP_BANISHER_CTX_OFF x1 / P1LP_BLOCK2_OFF_1CE8 x2 / FIELD_STATE_OFF x1 / CHAIN_LINK_COUNTER_OFF x1 / DUEL_ACTIVE_PLAYER_OFF x1 / LP_COST_3000 x2 / LP_COST_5000 x1 / SWORDS_OF_REVEALING_LIGHT_CID x1 / CRUSH_CARD_CID x3 / DECK_DEVASTATION_VIRUS_CID x3 / MAGICAL_LABYRINTH_CID x1 / WALL_SHADOW_CID x1 / NEEDLE_WORM_CID x1 / SOUL_ABSORBING_BONE_TOWER_CID x1 NEW / MALICE_ASCENDANT_CID x1 NEW / CARD_FIELD3_THRESHOLD_1499 x3 NEW / CARD_FIELD3_THRESHOLD_1500 x3 NEW)
- **REF**: 1 (fn-ptr DAT_08067270 -> check_activation_ctx_zone11_match_cb+1 THUMB+1)
- **CREATE_FUNC**: 1 (check_activation_ctx_zone11_match_cb @ 0x080671bc + plate)
- **FUNC_RENAME**: 0
- **PLATE**: 1 (new fn check_activation_ctx_zone11_match_cb plate)
- **carve**: 0 (no ROM_INCBIN/ROM data blocks in Seg-4)
- **disasm**: 0
- **新建 constants**: card_info.inc +4 (SOUL_ABSORBING_BONE_TOWER_CID=0x1744 / MALICE_ASCENDANT_CID=0x19d0 / CARD_FIELD3_THRESHOLD_1499=0x5db / CARD_FIELD3_THRESHOLD_1500=0x5dc)
- **域裁定 (C5)**: CARD_FIELD3_THRESHOLD_1499 (0x5db) / CARD_FIELD3_THRESHOLD_1500 (0x5dc) 同值多域新建: field3=ATK AI 选标阈值 (Crush Card/DDV), 语义截然不同于 FIELD5_SCORE_THRESHOLD_1499 (field5 score gate) / CARD_STAT_LP_THRESHOLD_1500 (LP 渲染) / LP_COST_1500 (LP 费用). per-slot 仅作用本段 6 槽.
- **附带修正 (Seg-2 regression)**: re-export 后发现 Seg-2 disassembled block literal pools (0x08066906..0x0806699e) 以 `.byte` 序列导出但缺少 DAT_ label 定义, 导致 build 失败. 已修正: 将相关 `.byte` 块和 ROM_INCBIN (0x6695e, 0x12) 替换为带标签的 `.word` 条目 (DAT_08066908/8960/8964/8968/896c/8988/898c/899c/869d4/869e8 + 0x08066a48/4c/50/54). 并修正 Seg-2 的 2 个 check_equip_activation_at_slot11 fn-ptr +1 缺失 (0x08065c50/c60).
- **§5.1**: 0
- **CSV sync**: +1 row (check_activation_ctx_zone11_match_cb 新建函数)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra script**: `RefineF08Seg4Slots.py`

### 4.05 Seg-5 完成记录 (0x67fa4..0x690dc)

- **EQ**: 62 槽 (PLAYER_BLOCK_STRIDE x18 / gDuelFieldSlots x14 / gDuelPhaseFlags x6 / gP1FieldArrayCBase x2 / EQUIP_PHASE_FRAME_OFF x2 / gP1HandSlotArray x1 / LP_CARD_TRACK_NEXT_OFF x1 / LP_CARD_TRACK_BASE_OFF x1 / P1LP_BLOCK2_OFF_1CE8 x1 / OAM_EFFECT_SLOT_TILE_P1 x1 reuse / 8 CID reuse [SWORDS_OF_REVEALING_LIGHT/IMPERIAL_ORDER/CRUSH_CARD/BIRDFACE x2/BLAST_SPHERE x2/IMPERIAL_ORDER x1] / BLAST_SPHERE_CID x1 NEW / BIRDFACE_CID x1 NEW / gEquipLpZoneEntryBase x1 NEW / EQUIP_SLOT_SCORE_CAP x1 NEW / OAM_EQUIP_SPRITE_TILE_P2_1B x1 NEW / OAM_EQUIP_SPRITE_TILE_P2_1C x1 NEW / EQUIP_OAM_ENTRY_ATTR_14F8 x1 NEW)
- **REF**: 4 槽 (PTR_gP1LifePoints_0806867c -> gP1LifePoints; DAT_080686a8 -> switchD_080686a2__switchdataD_080686ac; DWORD_0806905c -> gP1LifePoints; DWORD_080690d0 -> gP1LifePoints)
- **RENAME**: 65 auto-name slots renamed (DWORD_/DAT_ -> descriptive labels; all via Ghidra equate/label)
- **PLATE**: 1 (dispatch_equip_slot_sprite_by_zone_type @ 0x0806882c: CJK mojibake plate -> ASCII 575-char rewrite)
- **DISASM**: 1 (check_equip_eligible_always_false @ 0x08068828, 4B THUMB stub: movs r0,#0; bx lr; IMPERIAL_ORDER fn_eligible handler)
- **FUNC_RENAME**: 0
- **carve**: 0 (no ROM data tables in Seg-5 range)
- **新建 constants**:
  - `constants/card_info.inc` +3 (BLAST_SPHERE_CID=0x1286 / BIRDFACE_CID=0x139d / IMPERIAL_ORDER_CID=0x1360)
  - `constants/ewram.inc` +2 (gEquipLpZoneEntryBase=0x0201e500 / EQUIP_OAM_ENTRY_ATTR_14F8=0x000014f8)
  - `constants/oam_attr.inc` +3 (OAM_EQUIP_SPRITE_TILE_P2_1B=0x0000801b / OAM_EQUIP_SPRITE_TILE_P2_1C=0x0000801c / EQUIP_SLOT_SCORE_CAP=0x0000ffff)
- **域裁定 (C5)**: EQUIP_SLOT_SCORE_CAP=0xffff 独立新建; 域截然不同于 SLOT_CARD_EMPTY=0xffff (card slot domain) 和 OAM_ATTR0_HIDDEN=0xffff (OAM domain); Seg-4 域裁定先例支持
- **§5.1**: 0 (Seg-5 无全 ROM 0 引用孤儿块)
- **附带修正**: switchD_080686a2 table ptr (DAT_080686a8) 已 via REF slot 正确符号化; no ROM_INCBIN blocks in Seg-5
- **CSV sync**: +1 row (check_equip_eligible_always_false @ 0x08068828 新建函数)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra script**: `RefineF08Seg5Slots.py`

### 4.06 Seg-6 完成记录 (0x690dc..0x6a118)

- **EQ**: 82 槽 (within boundary) + 7 EQ-only beyond boundary (Seg-7 literal pool)
  - CID x15 (LORD_OF_D/GRACEFUL_CHARITY/SPIRAL_SPEAR_STRIKE/PARASITE_PARACIDE/SCAPEGOAT/STRAY_LAMBS/WIDESPREAD_RUIN/HAMMER_SHOT/CHTHONIAN_BLAST x2/cid_12fb/cid_12f7/cid_131c/JAR_ROBBER) — 11 reuse + 4 new
  - gDuelPhaseFlags x12+1 / EQUIP_PHASE_FRAME_OFF x8+3 / PLAYER_BLOCK_STRIDE x10+2 / P1LP_BLOCK2_OFF_1CE8 x6 / EQUIP_ACTIVE_CTX_OFF x1 / LP_CARD_TRACK_BASE_OFF x1 / ELIGIB_SPRITE_CTRL_OFF x2 / ELIGIB_ANIM_STATE_OFF x1 / LP_BANISHER_CTX_OFF x1 / ELIGIB_STATE_CTRL_OFF x1 / ELIGIB_ACT_TYPE_OFF x1 / LP_ACTIVATION_LINK_FLAG_OFF x1 NEW / gEquipChainEntryBase x1 / gP1FieldArrayCBase x1 / gP1SlotSetCodeArray x1 / gP1ChainZoneArray x1 / gEquipLpZoneEntryBase x1 / gEquipChainSlotRefs x1 / gDuelFieldSlots x1 / gP1HandSlotArray x1 / gDuelCardCtxBase x2+1 / gEquipZoneRankState x1 / OAM_SPRITE_CODE_P1_ACTIVATION x1 NEW / ZONE_ENTRY_FLAGS_CLR_MASK x1 NEW / gP1LifePoints x11
- **REF**: 3 (invoke_effect_node_with_active_flag_3arg fn-ptr @ 0x08069ae8; check_zone_activation_ctx_match_cb fn-ptr @ 0x08069d7c; switchD_08069edc table ptr @ 0x08069eec)
- **RENAME_ONLY**: 8 (PTR_gP1LifePoints_* x6 + 2 token-table addr raw .word with ASCII EOL; Ruling A: no equate for 0x09e3fXXX ROM FS addrs)
- **PLATE**: 1 (tick_dragon_summon_display_if_slots_paired: CJK mojibake + wrong card name "Stamping Destruction" -> "Lord of D." fix)
- **DISASM**: 1 ROM_INCBIN -> THUMB (check_equip_eligible_set_slot8_flag_for_cid_12da @ 0x080696d8, 0x1c B; fn_eligible handler CID=0x12da; dispatch table ref at 0x09e3fba8)
- **CREATE_FUNC**: 1 (check_zone_activation_ctx_match_cb @ 0x08069cdc, already disasm'd inline; fn-ptr callback to init_zone_activation_display_fields)
- **新建 constants**:
  - `constants/card_info.inc` +4 (WIDESPREAD_RUIN_CID=0x1254 / BOTTOMLESS_SHIFTING_SAND_CID=0x1540 / HAMMER_SHOT_CID=0x17f2 / cid_12da=0x12da)
  - `constants/ewram.inc` +1 (LP_ACTIVATION_LINK_FLAG_OFF=0x10d0; base=gP1LifePoints)
  - `constants/oam_attr.inc` +2 (OAM_SPRITE_CODE_P1_ACTIVATION=0x8019 / ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff)
- **Ruling A**: SCAPEGOAT/STRAY_LAMBS OAM token table ROM addrs (0x09e3f11c/12c) -> RENAME-only with ASCII EOL (no equate; sibling modules all use raw .word for 0x09e3fXXX)
- **Ruling B**: ZONE_ENTRY_FLAGS_CLR_MASK -> oam_attr.inc (no new equip_sprite.inc)
- **C5 fix**: DAT_08069778 = 0x1da8 -> LP_CARD_TRACK_BASE_OFF (was LP_BANISHER_CTX_OFF which = 0x1d70, wrong value)
- **C6 fix**: DAT_08069f54 + DWORD_0806a050 label prefix -> gduelcardctxbase_* (was gduelphaseflagss_*)
- **附带修正**: RepairF08Seg3DataLabels.py (14 DWORD data labels in 0x08066900..0x08066b00 lost after Seg-6 CREATE_FUNC); FixF08Seg6ThumbPlusPtrLabels.py (created _1 labels at odd THUMB+1 addrs for GAS export); fn-ptr +1 fix (check_equip_activation_at_slot11 @ 0x08065c50/c60 -> +1 form)
- **§5.1**: 0 (switchD_08069edc 10-entry inline; all blocks have ROM refs)
- **CSV sync**: +2 rows (check_equip_eligible_set_slot8_flag_for_cid_12da + check_zone_activation_ctx_match_cb)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg6Slots.py` + `RepairF08Seg3DataLabels.py` + `FixF08Seg6ThumbPlusPtrLabels.py`

### 4.07 Seg-7 完成记录 (0x6a118..0x6ab0c)

- **EQ**: 40 槽 (37 reuse + 3 new)
  - gP1LifePoints x4 / gDuelFieldSlots x7 / gDuelPhaseFlags x5 / PLAYER_BLOCK_STRIDE x9 / OAM_EQUIP_SPRITE_TILE_P2_1C x1 / OAM_EQUIP_SLOT_SPRITE_P2 x1 / P1LP_BLOCK2_OFF_1CE8 x1 / gDuelEquipCtx x1 / LP_CARD_TRACK_BASE_OFF x1 / gP1SlotSetCodeArray x1 / POLYMERIZATION_CID x1 / MONSTER_REBORN_CID x1 / MIND_HAXORZ_CID x2 / LIGHT_OF_INTERVENTION_CID x1 / EQUIP_CHAIN_SENTINEL x1 (reuse);
  - 3 NEW: EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8 (duel_field.inc) + OAM_ZONE_SPRITE_PAIR_P2_FIRST=0x8028 (oam_attr.inc) + LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff (duel_field.inc)
- **REF**: 0 / **RENAME**: 0 / **PLATE**: 0 / **DISASM**: 0 / **FUNC_RENAME**: 0 / **carve**: 0
- **域例外 (C5)**:
  - EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8 (base=gDuelFieldSlots, gDuelFieldSlots+0x1cb8=gEquipZoneCountTable=0x0201e1c8) vs DUEL_ACTIVE_PLAYER_OFF=0x1cb8 (base=gP1LifePoints, 结果=0x0201e198) — 不同 base 不同地址, 独立新建
  - LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff (LP display all-slots selector) vs EQUIP_SLOT_SCORE_CAP/SLOT_CARD_EMPTY/OAM_ATTR0_HIDDEN (均=0xffff, 不同域)
- **§5.1**: 0x0806a544 (4B orphan `movs r0,#0; bx lr`, 0 raw+THUMB+1 refs) — 登记留待, .byte 原样不变
- **Mode A 修正**: #1 补 §5.1 登记 0x0806a544; #2 ZONE14_CHAIN_SLOT_FLAG_OFF -> EQUIP_ZONE_COUNT_TABLE_OFF (reviewer 确认 gDuelFieldSlots+0x1cb8=gEquipZoneCountTable)
- **附带修正**: re-export 后 asm/08 两处 fn-ptr 引用需 +1:
  - `check_equip_activation_at_slot11` 两处 (.word fn -> .word fn+1, 0x08065c50/0x08065c60)
  - `check_activation_ctx_zone11_match_cb_1` -> `check_activation_ctx_zone11_match_cb+1` (0x08067270)
  - `check_zone_activation_ctx_match_cb_1` -> `check_zone_activation_ctx_match_cb+1` (0x08069d7c)
- **新建 constants**: duel_field.inc +2 / oam_attr.inc +1 (3 total)
- **CSV sync**: 无 (0 disasm / 0 FUNC_RENAME)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra script**: `RefineF08Seg7Slots.py`

### 4.08a Seg-8a 完成记录 (0x6ab0c..0x6b56c)

**Seg-8 拆分方案**: 8a = 0x6ab0c..0x6b56c (6 fn + 4 ROM_INCBIN); 8b = 0x6b56c..0x6cbe8 (14 fn + 7 ROM_INCBIN 待分类)

**11 块分类表 (§五 路线图 Seg-8 全 11 ROM_INCBIN)**:

| 块地址/大小 | 所在 Seg | 判断结果 |
|---|---|---|
| §5.1 0x6adb6/0x3e | 8a | dead code (raw=0, THUMB+1=0) → §5.1 |
| Block1 0x6ae18/0x25c | 8a | THUMB disasm (8 stubs, dispatch_equip_effect_slot_display_by_state_and_card 跳转表目标) |
| Block2 0x6b098/0x19c | 8a | THUMB disasm (7 stubs, 同上跳转表继续) |
| Block3 0x6b2a8/0x74 | 8a | THUMB disasm (6 stubs, dispatch_germ_momonga_trigger_display_by_state 跳转表目标) |
| 0x6b5f2..0x6cbe8 x7 | 8b | 待 Seg-8b ref-scan 分类 |

- **EQ**: 22 槽 (21 reuse + 1 NEW: GIANT_GERM_CID=0x1339)
  - EQUIP_PHASE_FRAME_OFF x3 / gP1LifePoints x1 / P1LP_BLOCK2_OFF_1CE8 x1 / gDuelEquipCtx x1 / PLAYER_BLOCK_STRIDE x2 / gP1SlotSetCodeArray x1 / gEquipZoneCountTable x1 / gDuelCardCtxBase x1 (= gduelcardctxbase_0806b41c slot) / NIMBLE_MOMONGA_CID x3 / SPEAR_CRETIN_CID x1 / CID 0x14dd x1 / CID 0x136a x2 / CID 0x15b6 x2 / CID 0x194f x1 / CID 0x152f x1 / CID 0x1612 x1; gP1LifePoints global pointer ref x1
  - NEW constant: `constants/card_info.inc` +1 (GIANT_GERM_CID=0x1339 Giant Germ pw=95178994)
- **REF**: 1 (DAT_0806ac24 → switchD_0806ac1e data ptr)
- **RENAME**: 5 (PTR_ labels renamed to descriptive slot labels)
- **FUNC_RENAME**: 2
  - 0x0806b31c: dispatch_neo_daedalus_effect_display_by_state → **dispatch_germ_momonga_trigger_display_by_state** (误名订正: Giant Germ/Nimble Momonga fn_activate handler, not Neo Daedalus)
  - 0x0806b53c: dispatch_neo_daedalus_placement_check_if_chain_subtype → **dispatch_spear_cretin_activate_if_chain_subtype** (误名订正: Spear Cretin fn_activate handler)
- **PLATE**: 6 (substring rewrites on 2 renamed functions; all pure ASCII)
- **DISASM**: 3 ROM_INCBIN → THUMB (21 新函数):
  - Block1 0x0806ae18/0x25c (8 stubs): `equip_effect_state_stub_{default_ae18/ae48/ae90/af52/af84/afac/afec/b01c}`; switchD_0806ac1e 跳转表目标 (raw-addr, not THUMB+1)
  - Block2 0x0806b098/0x19c (7 stubs): `equip_effect_state_stub_{default_b098/b0d6/b124/b13c/b1de/b1ea/b1f4}`; 同上跳转表继续
  - Block3 0x0806b2a8/0x74 (6 stubs): `equip_germ_momonga_state_stub_{b2a8/b2ce/b2e2/b2f8/b30a/default_b314}`; dispatch_germ_momonga_trigger_display_by_state 跳转表目标
- **§5.1**: +1 → 0x0806adb6 (0x3e B, dead code, raw=0/THUMB+1=0)
- **附带修正**:
  - fn-ptr +1 周期性修复: 2 处 `.word check_equip_activation_at_slot11` → `+1` (asm/08 lines ~3691/3700)
  - `.equ check_activation_ctx_zone11_match_cb_1, check_activation_ctx_zone11_match_cb+1` + `.equ check_zone_activation_ctx_match_cb_1, check_zone_activation_ctx_match_cb+1` (GAS symbol 修复)
  - FixF08Seg8aLiteralPools.py: 21 DWORD literal pool 强制 split (DAT_ 标签补建)
  - FixF08Seg8aPlateIds.py: plate rewrite 顺序冲突后补修正 2 处 CARD_ID_0x1339/133a → GIANT_GERM_CID/NIMBLE_MOMONGA_CID
  - 跨模块 plate 修正: `asm/05_equip_eligibility_a.s` line 4 旧名 dispatch_neo_daedalus_effect_display_by_state → dispatch_germ_momonga_trigger_display_by_state
- **新建 constants**: `constants/card_info.inc` +1 (GIANT_GERM_CID=0x1339)
- **CSV sync**: +21 rows (21 new disasm stubs) + 2 FUNC_RENAME 行已手改 (rows 2009/2010)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg8aSlots.py` + `DisassembleF08Seg8aBlocks.py` + `FixF08Seg8aLiteralPools.py` + `FixF08Seg8aPlateIds.py`

### 4.09 Seg-8b 完成记录 (0x6b56c..0x6c0cc)

- **EQ**: 17 槽 (15 reuse + 2 NEW: CEASEFIRE_CID=0x135c / SPELL_ABSORBING_LIFE_CID=0x1635)
  - NUMINOUS_HEALER_CID x1 / gDuelPhaseFlags x3 / PLAYER_BLOCK_STRIDE x3 / gDuelFieldSlots x2 / gDuelCardCtxBase x1 / gP1LifePoints x3 / LP_CARD_TRACK_NEXT_OFF x1 / gEquipZoneCountTable x1 reuse
  - CEASEFIRE_CID=0x135c (Ceasefire pw=36468556; card-stats.s card_0764) NEW card_info.inc
  - SPELL_ABSORBING_LIFE_CID=0x1635 (The Spell Absorbing Life pw=99517131; card-stats.s card_1301) NEW card_info.inc
- **REF**: 2 槽
  - DWORD_0806bb28 -> check_equip_slot_eligible_by_equip_type+1 (THUMB+1 fn ptr; asm/05 L18412)
  - PTR_DAT_0806b7d4 -> cid_135b_dispatch_jump_table (10-entry raw-addr table label)
- **RENAME**: 0 (disasm 阶段替换 ROM_INCBIN start label)
- **FUNC_RENAME**: 0
- **PLATE**: 2 (dispatch_neo_daedalus_placement_check_by_state @ 0x0806c0cc: stale FUN_0806b53c -> dispatch_spear_cretin_activate_if_chain_subtype; dispatch_numinous_healer_lp_zone_sprites: inline CID ref symbolize x2)
- **DISASM**: 5 ROM_INCBIN -> THUMB (30 新函数):
  - Block1 0x0806b784/0x4c (1 fn): `check_equip_eligible_cid_135b` (fn_eligible CID=0x135b; THUMB+1 @0x1e40448)
  - Block2 0x0806b7fc/0x27c (10 stubs): `cid_135b_state_stub_{b7fc/b8a8/b8d4/b944/b950/b990/b9f0/ba00/ba28/ba64}`; dispatched from 10-entry table @0x6b7d4
  - Block3 0x0806bb74/0x44 (1 fn): `check_equip_eligible_magical_hats` (fn_eligible CID=0x1362 Magical Hats pw=81210420; THUMB+1 @0x1e40490)
  - Block4 0x0806bc2c/0x374 (11 stubs): `magical_hats_state_stub_{bc2c/bc86/bc96/bcaa/bd4c/bda8/bdce/bdf2/bf3a/bf4c/default_bf56}`; dispatched from 29-entry table @0x6bbb8; nested literal pool @0x6bf9c -> 7-entry sub-table @0x6bfa0
  - Block5 0x0806bfbc/0x110 (7 sub-stubs): `magical_hats_zone_state_stub_{bfbc/c050/c066/c080/c08e/c0a0/c0ae}`; dispatched from nested 7-entry table @0x6bfa0
- **carve**: 0 (all 5 blocks are THUMB code)
- **ss5.1**: 0 (all blocks have confirmed refs)
- **附带修正**:
  - FixF08Seg8bLiteralPools.py: 32 literal pool DWORD labels forced (DAT_ labels in .byte sequences)
  - asm/08 L3-6: .equ aliases added (check_equip_activation_at_slot11_1 / check_equip_slot_eligible_by_equip_type_1 / check_activation_ctx_zone11_match_cb_1 / check_zone_activation_ctx_match_cb_1) -- fn-ptr +1 periodic fix
  - .word slots 0x08065c50/0x08065c60 -> check_equip_activation_at_slot11_1 (THUMB+1 restore)
  - .word slot 0x0806bb28 -> check_equip_slot_eligible_by_equip_type_1 (THUMB+1 restore)
- **新建 constants**: card_info.inc +3 (MAGICAL_HATS_CID=0x1362 / CEASEFIRE_CID=0x135c / SPELL_ABSORBING_LIFE_CID=0x1635)
- **CSV sync**: +30 rows (30 new disasm functions: 2 fn_eligible handlers + 28 state stubs)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg8bSlots.py` + `DisassembleF08Seg8bBlocks.py` + `FixF08Seg8bLiteralPools.py`

### 4.10 Seg-8c 完成记录 (0x6c0cc..0x6cbe8)

- **EQ**: 39 槽 (34 reuse + 3 NEW + 2 PTR_ RENAME)
  - gDuelPhaseFlags x3 / EQUIP_PHASE_FRAME_OFF x1 / PLAYER_BLOCK_STRIDE x6 / gP1HandSlotArray x2 / SPEAR_CRETIN_CID x1 / gDuelFieldSlots x3 / gEquipChainSlotRefs x1 / gP1LifePoints x6 / gDuelCardCtxBase x1 / LP_CARD_TRACK_BASE_OFF x1 / RE_FUSION_CID x1 / SYMBOL_OF_HERITAGE_CID x2 / SOUL_RESURRECTION_CID x1 / CALL_OF_THE_HAUNTED_CID x1 / AUTONOMOUS_ACTION_UNIT_CID x1 / gEquipZoneRankState x2 / MAHARAGHI_CID x1 / P1LP_BLOCK2_OFF_1CE8 x2 (reuse)
  - 3 NEW: OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052 (oam_attr.inc) / MORPHING_JAR_2_CID=0x1369 (card_info.inc) / SOLOMONS_LAWBOOK_CID=0x137e (card_info.inc) / P2LP_BLOCK2_OFF_1CF4=0x1cf4 (ewram.inc) [4 constants total]
  - 2 PTR_ RENAME: PTR_gP1LifePoints_0806cb98 -> gp1lifepoints_0806cb98 / PTR_gP1LifePoints_0806cbe0 -> gp1lifepoints_0806cbe0
- **REF**: 0
- **RENAME**: 2 (PTR_ slot renames via RENAME_SLOTS in script)
- **FUNC_RENAME**: 1
  - 0x0806c0cc: dispatch_neo_daedalus_placement_check_by_state -> **tick_spear_cretin_placement_state_machine** (误名订正: fn CID=0x133b Spear Cretin placement state machine; "neo_daedalus" was callee identity not fn identity)
- **PLATE**: 2
  - tick_spear_cretin_placement_state_machine @ 0x0806c0cc: full ASCII rewrite (986 chars); Spear Cretin CID=0x133b placement state machine description
  - enqueue_spirit_monster_zone_sprite_otohime @ 0x0806cb54: stale FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
- **DISASM**: 2 ROM_INCBIN -> THUMB (9 新函数):
  - Block1 0x0806c3d8/0x44 (1 fn): `check_equip_eligible_morphing_jar_2` (fn_eligible CID=0x1369 Morphing Jar #2 pw=79106360; THUMB+1 @card-effect dispatch table)
  - Block2 0x0806c440/0x298 (8 stubs): `morphing_jar2_state_stub_{c440/c4e8/c52c/c5f8/c63c/c65a/c69c/c6c0}`; dispatched from 9-entry raw-addr jump table at 0x0806c41c..0x0806c43c (entry[8] shared with c440); entry[1,2] share c6c0
- **carve**: 0 (9-entry jump table 0x0806c41c..0x0806c43c already structured as .word entries in asm; no new rom.s carve)
- **§5.1**: 0 (both blocks have confirmed ROM references)
- **域例外 (C5)**:
  - P2LP_BLOCK2_OFF_1CF4=0x1cf4 (base=gP1LifePoints, abs=gP1LifePoints+0x1cf4=0x0201e1d4) vs FIELD_STATE_OFF=0x1cf4 (base=gDuelFieldSlots, abs=gDuelFieldSlots+0x1cf4=0x0201e204) — 不同 base 不同地址, 独立新建; reviewer C5 域例外已确认
- **附带修正**:
  - FixF08Seg8cLiteralPools.py: 17 literal pool DWORD labels forced (Block1 0x806c414 + Block2 0x806c4d8/4dc/4e0/4e4 + 0x806c520/524/528 + 0x806c5e8/5ec/5f0 + 0x806c638 + 0x806c68c/690/694/698 + 0x806c6d4)
  - FixF08Seg8cRipplePlate.py: cross-module plate fix dispatch_spear_cretin_activate_if_chain_subtype @ 0x0806b53c (3 occurrences of old name replaced)
  - fn-ptr +1 periodic fix (3 asm/08 slots): check_equip_activation_at_slot11 x2 @ 0x8065c50/c60 + check_equip_slot_eligible_by_equip_type @ 0x806bb28
  - rom.s: .equ check_activation_ctx_zone11_match_cb_1 + check_zone_activation_ctx_match_cb_1 aliases (permanent; re-export strips asm/08 so must live in rom.s)
- **新建 constants**:
  - `constants/card_info.inc` +2 (MORPHING_JAR_2_CID=0x1369 / SOLOMONS_LAWBOOK_CID=0x137e)
  - `constants/oam_attr.inc` +1 (OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052)
  - `constants/ewram.inc` +1 (P2LP_BLOCK2_OFF_1CF4=0x1cf4)
- **CSV sync**: +9 rows (9 new disasm functions: check_equip_eligible_morphing_jar_2 + 8 morphing_jar2_state_stubs) + 1 FUNC_RENAME 行已手改 (0x0806c0cc)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg8cSlots.py` + `DisassembleF08Seg8cBlocks.py` + `FixF08Seg8cLiteralPools.py` + `FixF08Seg8cRipplePlate.py`

### 4.11 Seg-9 完成记录 (0x6cbe8..0x6d960)

- **EQ**: 51 槽 (47 reuse + 4 NEW)
  - gDuelPhaseFlags x5 / LP_CARD_TRACK_BASE_OFF x1 / LP_CARD_TRACK_NEXT_OFF x3 / PLAYER_BLOCK_STRIDE x14 / gDuelFieldSlots x9 / LP_ACTIVATION_LINK_FLAG_OFF x1 / gEquipChainSlotRefs x1 / gEquipZoneCountTable x1 / VALKYRION_THE_MAGNA_WARRIOR_CID x1 / PUPPET_MASTER_CID x1 / EQUIP_PHASE_FRAME_OFF x2 / gDuelCardCtxBase x1 / gP1HandSlotArray x2 / EQUIP_ZONE_COUNT_TABLE_OFF x1 / P1LP_BLOCK2_OFF_1CE8 x3 (reuse)
  - 4 NEW: MAGIC_CYLINDER_CID=0x1404 (card_info.inc) / DRAINING_SHIELD_CID=0x176a (card_info.inc) / RING_OF_DESTRUCTION_CID=0x138d (card_info.inc) / SPRITE_RECORD_P2_SIDE=0x8020 (oam_attr.inc)
- **REF**: 0
- **RENAME**: 12 (PTR_gP1LifePoints_* x11 -> gp1lifepoints_0806xxxx; DWORD_0806d678 -> gp1lifepoints_0806d678)
- **FUNC_RENAME**: 0 (dispatch_neo_space_placement_by_card_id_and_state 保持现名; file 08 neo_space 已确立非正式域标签 for check_field_spell_neo_daedalus_group_placeable 门控)
- **PLATE**: 3
  - tick_equip_lp_display_state_by_zone_match @ 0x0806d3d8: CJK mojibake (636-char, 106 non-ASCII) -> 741-char ASCII rewrite (full state machine description)
  - enqueue_zone_equip_sprite_if_slot_matches @ 0x0806d514: FUN_08071404 -> enqueue_equip_sprite_guarded_by_zone_type13
  - enqueue_spirit_zone_sprite_with_lp_check @ 0x0806d680: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
- **carve**: 0 (no ROM_INCBIN)
- **disasm**: 0
- **§5.1**: 0 (no unref blocks in Seg-9)
- **新建 constants**:
  - `constants/card_info.inc` +3 (RING_OF_DESTRUCTION_CID=0x138d / MAGIC_CYLINDER_CID=0x1404 / DRAINING_SHIELD_CID=0x176a)
  - `constants/oam_attr.inc` +1 (SPRITE_RECORD_P2_SIDE=0x8020)
- **附带修正**: fn-ptr +1 periodic fix -- added `check_equip_activation_at_slot11_1` + `check_equip_slot_eligible_by_equip_type_1` .equ aliases to rom.s (L71-72); updated asm/08 L3691/L3700/L17485 to use _1 names (GAS emits function address without +1; rom.s aliases ensure THUMB+1 encoding is preserved across re-exports)
- **CSV sync**: 不需要 (0 disasm / 0 FUNC_RENAME)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra script**: `RefineF08Seg9Slots.py`

### 4.12 Seg-10 完成记录 (0x6d960..0x6e76c)

- **EQ**: 42 槽 (35 reuse + 7 NEW)
  - gDuelPhaseFlags x6 / EQUIP_PHASE_FRAME_OFF x4 / PLAYER_BLOCK_STRIDE x5 / gDuelFieldSlots x4 / gEquipChainSlotRefs x3 / DISPLAY_SEQ_ACTIVE_PLAYER_OFF x2 / EQUIP_ACTIVE_CTX_OFF x1 / gP1FieldArrayCBase x1 / gDuelCardCtxBase x1 / P2LP_BLOCK2_OFF_1CF4 x1 / gP1LifePoints x0 (reuse); THE_BLOCKMAN_CID/PHANTASMAL_MARTYRS_CID/EQUIP_ELIG_EXCL_D/LP_ACTIVATION_LINK_FLAG_OFF/OAM_SPRITE_CODE_P1_ACTIVATION (reuse)
  - 7 NEW: GAP_CID_13ED=0x13ed (card_info.inc) / MULTIPLICATION_OF_ANTS_CID=0x13fc (card_info.inc) / NEO_SPACE_SPAWN_CAT_1422=0x1422 (card_info.inc) / NEO_SPACE_SPAWN_CAT_1813=0x1813 (card_info.inc) / NEO_SPACE_SPAWN_CAT_19BA=0x19ba (card_info.inc) / LP_DISPLAY_SEQ_PROGRESS_OFF=0x1d7a (duel_field.inc) / EQUIP_BITMAP_QUERY_KEY=0x04000400 (duel_field.inc; originally misnamed DISPCNT_SHADOW, corrected by reviewer advisory #2)
- **REF**: 0
- **RENAME**: 2 (DWORD_0806e144 / DWORD_0806e6d0 -> gp1lifepoints_0806e144/e6d0)
- **FUNC_RENAME**: 0
- **PLATE**: 0 (no stale FUN_; no CJK mojibake in Seg-10)
- **DISASM**: 4 blocks (19 new functions):
  - Block1 `check_equip_eligible_state_dispatch_cid_13ed` @ 0x0806dbcc (0x44 B; GAP_CID_13ED=0x13ed fn_eligible handler; THUMB+1 ref @0x09e406d0; literal pool dc04/dc08/dc0c; 11-entry raw-addr table at 0x0806dc10)
  - Block2 11 stubs @ 0x0806dc3c..0x0806e00b (0x3d0 B): `cid_13ed_state_stub_{80/7f/7e/7d/7c/7b/7a/79/78/77/76}`; dispatched via raw MOV PC,r0 from 11-entry table; states 0x76..0x80 (index=state-0x76)
  - Block3 `check_equip_eligible_state_dispatch_de_fusion` @ 0x0806e3fc (0x4c B; DE_FUSION_CID=0x13fe fn_eligible handler; 2B pad at 0x0806e3fa; THUMB+1 ref @0x09e407f0; 6-entry raw-addr table at 0x0806e448)
  - Block4 6 stubs @ 0x0806e460..0x0806e62b (0x1cc B): `de_fusion_state_stub_{80/7f/7e/7d/7c/7b}` (CORRECTED: state determined by table index not stub addr; entry[0]=0x6e618=state_0x7b, entry[5]=0x6e460=state_0x80); states 0x7b..0x80 (index=state-0x7b)
- **State mapping correction (Mode A #1)**: reviewer C6 hard -- Block4 De-Fusion 6 stub state labels were inverted (proposal had subs r1,#0x7b index confused with descending-addr ordering). Corrected: de_fusion_state_stub_7b @ 0x0806e618 (highest addr, entry[0]), de_fusion_state_stub_80 @ 0x0806e460 (lowest addr, entry[5]).
- **Name correction (Mode A #2)**: DISPCNT_SHADOW -> EQUIP_BITMAP_QUERY_KEY; 0x04000400 exceeds I/O range, not a HW register; moved from gba_io.inc to duel_field.inc (equip domain).
- **新建 constants**:
  - `constants/card_info.inc` +5 (GAP_CID_13ED=0x13ed / MULTIPLICATION_OF_ANTS_CID=0x13fc / NEO_SPACE_SPAWN_CAT_1422=0x1422 / NEO_SPACE_SPAWN_CAT_1813=0x1813 / NEO_SPACE_SPAWN_CAT_19BA=0x19ba)
  - `constants/duel_field.inc` +2 (LP_DISPLAY_SEQ_PROGRESS_OFF=0x1d7a / EQUIP_BITMAP_QUERY_KEY=0x04000400)
- **carve**: 0 (all 4 blocks are THUMB code, no ROM data tables)
- **§5.1**: 0 (all 4 blocks have confirmed ROM references)
- **fn-ptr +1 periodic fix**: asm/08 L3691/3700 check_equip_activation_at_slot11 -> _1; L17485 check_equip_slot_eligible_by_equip_type -> _1 (re-export resets these each time)
- **CSV sync**: +19 rows (19 new disasm functions: 2 fn_eligible handlers + 11 cid_13ed stubs + 6 de_fusion stubs)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Ghidra scripts**: `RefineF08Seg10Slots.py` + `DisassembleF08Seg10Blocks.py`

**file 08 全 10 段完成 ✅** (Seg-1..10; 含 Seg-8a/8b/8c 拆分; 总计: disasm=4+18+30+9+2+1+8+21+30+9+19=151 new fn; EQ~742; RENAME~85; PLATE~50; FUNC_RENAME 8; §5.1 +3 孤儿块)

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 08 范围 `[0x080643e0, 0x0806e76c)` (191 named fn, ~674 槽, 22 ROM_INCBIN, 5 switchD)
> 按**函数数**均分 10 段 (~20 fn/段, 边界=函数结束处)。

| Seg | 地址范围 | ~fn | ~slots | 块数 | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x643e0..0x6544c | 20 | 87 | 2 inc | check_equip_slot_eligible_neo_daedalus + Neo Daedalus 资格簇 |
| Seg-2 | 0x6544c..0x66448 | 20 | 72 | 3 inc + 1 sw | write_equip_lp_delta_goblin_thief + LP delta + switchD_08065a44 |
| Seg-3 | 0x66448..0x67160 | 20 | 56 | 1 inc + 1 sw | dispatch_equip_zone_sprite_by_slot_state + switchD_08066f02 |
| Seg-4 | 0x67160..0x67fa4 | 20 | 74 | 0 | dispatch_effect_zone_lp_sprites_by_slot_flags 簇 |
| Seg-5 ✅ | 0x67fa4..0x690dc | 20 | 65 | 0 + 1 sw | scan_effect_slots_for_equip_sprite_field6 + switchD_080686a2 |
| Seg-6 ✅ | 0x690dc..0x6a118 | 20 | 90 | 1 inc + 1 sw | tick_dragon_summon_display + switchD_08069edc |
| Seg-7 ✅ | 0x6a118..0x6ab0c | 20 | 47 | 0 | dispatch_equip_zone_sprite_by_lp_state_with_placement 簇 |
| Seg-8a ✅ | 0x6ab0c..0x6b56c | 6 | 22 | 4 ROM_INCBIN (3 disasm + §5.1 1) + switchD_0806ac1e | Germ/Momonga/Spear Cretin dispatch stubs (21 new fn); 误名订正 x2 |
| Seg-8b ✅ | 0x6b56c..0x6c0cc | 4+30(disasm) | 63 | 5 DISASM | cid_135b/Magical Hats/Ceasefire/SpellAbsorbing dispatch stubs (30 new fn); 嵌套跳表 0x6bc2c->0x6bfa0->0x6bfbc |
| Seg-8c ✅ | 0x6c0cc..0x6cbe8 | 9+9(disasm) | 39 | 2 DISASM | Morphing Jar #2 stubs (9 new fn); tick_spear_cretin 误名订正; P2LP domain exception |
| Seg-9 ✅ | 0x6cbe8..0x6d960 | 20 | 52 | 0 | tick_equip_target_query_display_seq 簇 |
| Seg-10 ✅ | 0x6d960..0x6e76c | 11+19(disasm) | 46 | 4 inc | dispatch_field_spell_placement_display + De-Fusion/CID_13ED stubs (文件末) |

执行约定同 file 00..07: 每段走 §二 pipeline; 地址序不回头; 每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |
| 0x0806a544 | 4B | Seg-7 | movs r0,#0; bx lr (orphan 4B stub, 0 raw+0 THUMB+1 refs) | pending |
| 0x0806adb6 | 0x3e B | Seg-8a | dead code (0 raw + 0 THUMB+1 refs; 2B pad + 3 THUMB stubs unreferenced) | pending |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-07-equip-effect-chain.md` (file 07: handler-table disasm 大批量 / CID@fn_ptr-0xc / 机器码核 / 误名订正 / CONST_RENAME)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
