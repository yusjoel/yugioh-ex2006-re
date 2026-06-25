# 函数/数据细化计划 -- `asm/11_effect_slot_puzzletext.s`

> 阶段目标: 把 `asm/11_effect_slot_puzzletext.s` (ROM `0x080850d8 ~ 0x080941c4`, 效果 slot attr +
> 交换 sprite + 装备区扫描派发 + duel puzzle 文本队列) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **12** 个文件 (file 00..10 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..10 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用->§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一 + file 06..10 新增。

**跨文件踩坑沿用** (file 00..10 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **ROM_INCBIN 分类核心**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - 有引用 + THUMB opcode 形态 (push 前导) -> R4 disasm (+ createFunction + 命名 + CSV row)。
  - 有引用 + 数据 (指针表/掩码/字符串) -> R7 carve 进 rom.s。
  - raw=0 且 THUMB+1=0 -> §5.1 登记。
- **R4 disasm 范式**: clearListing 整 range -> setTMode THUMB -> **逐 stub/逐 fn per-block** DisassembleCommand;
  literal pool createDWord 强制 split; **每 sub-fn 单独 DisassembleCommand** (单次整 range 在首 `b`/`bx` 停);
  段后 ROM_INCBIN/.byte-code grep == 0 独立验收 (memory `feedback_refine_partial_disasm_residue_gate`)。
- **机器码核 (必做)**: disasm fn 比较+分支指令独立解码; 函数名运算符/偏移/卡名与机器码一致;
  **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核 (按 VALUE grep 不按 NAME)**: 标 new CID 逐一按值 grep 0 命中; 标 reuse 逐一按值 grep 确存在
  (memory `feedback_c5_dedup_grep_by_value_not_name`)。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实; 未分配->中性 `cid_<hex>`, 勿臆造。
- **误名警觉**: 函数名/plate 称的卡名/全局与函数体矛盾即误名信号; 走 FUNC_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 落地后 grep == 0
  (memory `feedback_refine_plate_subst_silent_noop`: WARN not-found 当 FAIL)。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04
  (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05..10 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责; memory `feedback_refine_fixer_overstep_self_review`)。

**⚠ file 11 特征 (本文件最大特点)**:
- **Seg-4 = 巨型 ROM_INCBIN `0x87d58 / 0x5a9c` (23,196 B)**: ref-scan 已确认 = **未反汇编的 THUMB 代码区**,
  含 **~197 个 distinct 函数入口** (全 ROM ~345 处 THUMB+1 fn-ptr 引用指入, 来自 card effect handler
  dispatch table)。首字节 `70b5 0024 0d4a` = `push {r4-r6,lr}; movs r4,#0; ...` 函数前导。
  - 这是 **隐藏的 ~200 函数反汇编+命名作业** (命名阶段 4641/4641 未含这些 fn-ptr-only 块 -- 从未被 disasm)。
  - **Seg-4 必拆多子段 (4a..4g, 每 ~28-30 fn)**: 地址序逐 fn disasm + createFunction + 命名 (card effect
    fn_activate/fn_eligible body) + CSV row; 引用它的 dispatch table 散落全 ROM, fn-ptr 引用据 THUMB+1 落地。
  - 入口最小 0x08087d58 (块首) 最大 0x0808d7de (块尾), 平均间距 118 B; 另有 61 个 even-addr 引用 (jump-table
    裸指针 / data ref, 执行时据实判定 carve vs disasm 边界)。
- 其余 ROM_INCBIN (3 小块): 0x850f0/0x28 + 0x85130/0x14c (Seg-1) + 0x861a0/0x27a (Seg-2); ref-scan 待执行
  (疑 dispatch 跳转表 / fn-ptr table, 据实 carve/disasm)。
- region C (Seg-5..10) **0 ROM_INCBIN**, 纯 slot 符号化 + plate 订正; 但含 2 个超大数据密集函数:
  `build_equip_candidate_score_table` (0x8090a78, 63 槽) 与 `eval_field_equip_activation_candidates`
  (0x8091888, **187 槽**, 0x1afc B) -- 大量内嵌 literal pool / score table DWord。

**file 02..10 已建可复用资产** (新建前必 grep): card_info.inc ~600+ CID / ewram.inc / iwram.inc /
duel_field.inc / oam_attr.inc / gfx_resource.inc / g2d_tags.inc / equip_lp_delta.inc 等。

---

## 二、落地工作流 (pipeline)

同 file 00..10 doc §二:
```
备份 .rep -> Ghidra 脚本 (RefineF11Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
-> ghidra-export-range.bat 080000c0 084c7637 -> inject_modes.py -> split_all_s.py
-> build + byte-identical SHA1 9689337d -> (改/建函数名才) ExportFunctionInventory + sync CSV -> commit
```
3-agent: executor -> reviewer (C1-C13) -> fixer (模式A改proposal / 模式B落地)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (11_effect_slot_puzzletext.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------|------|--------|
| 1  | 0x80850d8..0x8085d4c | 10 | ~100 | 2 inc (0x850f0/0x28, 0x85130/0x14c) | ✅ | 7d15bd6 |
| 2  | 0x8085d4c..0x8086cdc | 12 | ~92  | 1 inc (0x861a0/0x27a) | ✅ | 281d133 |
| 3a | 0x8086cdc..0x80872e4 | 4  | 46   | 0 inc | ✅ | 3689026 |
| 3b | 0x80872e4..0x8087d58 | 15 | 105  | 0 inc | ✅ | 793378c |
| 4a | 0x8087d58..0x8088904 | 21   | 84+44=128 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4b | 0x8088904..0x808962c | 25   | EQ=36/REF=40/PLATE=25 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4c | 0x808962c..0x808a2ac | 23 | EQ=39/REF=36/PLATE=23 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4d | 0x808a2ac..0x808ad8c | 24 | EQ=30/REF=34/PLATE=24 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4e | 0x808ad8c..0x808bb7c | 25 | EQ=30/REF=46/PLATE=25 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4f | 0x808bb7c..0x808cabc | 25 | EQ=37/REF=53/PLATE=25 | 0 inc (全 disasm) | ✅ | (see §四) |
| 4g | 0x808cabc..0x808d7f4 | 20 | EQ=30/REF=42/PLATE=20 | 0 inc (全 disasm) | ✅ | (see §四) |
| 5  | 0x808d7f4..0x808e8fc | 18 | 107(EQ)+15(RENAME)+12(PLATE) | 0 inc | ✅ | (see §四) |
| 6  | 0x808e8fc..0x808f7c0 | 19 | 97(EQ=85/RENAME=12/PLATE=17) | 0 inc | ✅ | (see §四) |
| 7  | 0x808f7c0..0x8090a78 | 32 | ~117 | 0 inc | ✅ | (see §四) |
| 8  | 0x8090a78..0x8091888 | 3  | ~74  | 0 inc (build_equip_candidate_score_table 数据密集) | ✅ | (see §四) |
| 9  | 0x8091888..0x8093598 | 20 | ~191 | 0 inc (eval_field 187 槽; 可拆 9a/9b) | ⬜ | |
| 10 | 0x8093598..0x80941c4 | 9  | ~118 | 0 inc (duel puzzle 文本: parse 68 槽 + render 14) | ⬜ | |

**总计 (region A+C 已命名)**: 142 命名 fn / ~1052 DAT_/DWORD_/PTR_ 槽 / 4 ROM_INCBIN。
**外加 Seg-4 巨块**: ~197 未命名 THUMB fn 待 disasm + 命名 (region B)。
**重段提示**: **Seg-4 (巨块, ~197 fn) 为本文件压倒性工作量, 必拆 4a..4g**; Seg-9 (191 槽 eval_field 怪兽)
和 Seg-3 (151 槽) 次重; Seg-8 (build 数据密集) 与 Seg-10 (puzzle text parse) 含大内嵌表。

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录

- **范围**: `[0x080850d8, 0x08085d4c)` — 10 pre-existing named fn + 15 new disasm fn
- **EQ**: 85 槽 (gEquipChainSlotRefs x3 / PLAYER_BLOCK_STRIDE x5 / gDuelFieldSlots x3 / P1LP_BLOCK2_OFF x2 / P1LP_BLOCK2_OFF_1CE8 x6 / gDuelCardCtxBase x11 / gDuelPhaseFlags x4 + 19 CID/offset constants)
- **REF**: 7 槽 (3 switchD + 2 raw text-ptr + 2 raw text-id)
- **RENAME**: 8 槽 (PTR_gP1LifePoints_ x8 -> gp1lp_ptr_xxx snake_case)
- **PLATE**: 1 (dispatch_equip_display_with_pair_card_id CJK -> ASCII) + nuance applied (bits 0,2,3,4 in clear_equip_slot_attr_bits_and_activate plate)
- **disasm**: 2 blocks (BLK1 0x850f0/0x28 = 1 fn, BLK2 0x85130/0x14c = 13+1+1_tail = 15 fn); 14 literal pool DWord createDWord fixes (RefineF11Seg1PoolFix)
- **新增 CID**: 8 (TRAGEDY/REGULATION_OF_TRIBE/TORRENTIAL_TRIBUTE/SHADOW_OF_EYES/EMERGENCY_PROVISIONS/DROP_OFF/ADHESION_TRAP_HOLE/DD_TRAP_HOLE) -> card_info.inc
- **新增 ewram**: 5 (SLOT_DISPLAY_TYPE_OFF/LP_BAR_ROW_COUNT_OFF/LP_BAR_ROW_ACTIVE_OFF/LP_BAR_ROW_XCOORD_OFF/FIELD_DISPLAY_TYPE_OFF) -> ewram.inc
- **carve**: 0
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV rows**: +15 (14 proposal + store_slot_display_type_and_return_zero tail)
- **commit**: `7d15bd6`

### 4.02 Seg-2 完成记录

- **范围**: `[0x08085d4c, 0x08086cdc)` — 12 pre-existing named fn; 0 new fn
- **EQ**: 80 槽 (79 pool槽 + 1 disasm-block-internal @0x080863f8 ELIGIB_SPRITE_CTRL_OFF); gDuelPhaseFlags x14 / PLAYER_BLOCK_STRIDE x13 / gEquipEffectZoneTable x9 / gDuelFieldSlots x5 / gP1FieldArrayCBase x5 + 17 other offsets/globals
- **REF**: 4 槽 (dispatch_field_switchdata_base_ptr / game_text_sep_ptr / equip_slot_state_jt_ptr_ptr / equip_slot_state_case0_base)
- **RENAME**: 8 槽 (PTR_gP1LifePoints_ x8 -> gp1lp_ptr_xxx snake_case, with EOL)
- **PLATE**: 12 (7 in-segment: dispatch_equip_slot_state_by_index/check_equip_target/find_equip_target/sum_zone_bonus/sum_chain/check_sorted_array/eval_zone_activation + 5 cross-file: asm/11 L18360 invoke_card_display_op_0x31_with_params + asm/12 L3441/3570/3694/3868)
- **disasm**: 1 block 0x861a0/0x27a -> 6 sub-case labels (equip_slot_case0/1/2/3/4/casea_body) + 26 literal pool DWords; NO createFunction; pool fix @0x08086424/28/2c (RefineF11Seg2PoolFix)
- **新增 constants**: card_info.inc +4 (CONTRACT_WITH_ABYSS_CID=0x1698 / EARTH_CHANT_CID=0x1716 / END_OF_WORLD_CID=0x19d9 / gEquipEffectZoneTable=0x09e5a0c4); ewram.inc +1 (EQUIP_SLOT_SUBSTATE_OFF=0x58c)
- **carve**: 0
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: not needed (no new/renamed functions)
- **commit**: `281d133`

### 4.04a Seg-4a 完成记录

- **范围**: `[0x08087d58, 0x08088904)` — 0xBAC = 2988 B; **21 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 44 槽 (PLAYER_BLOCK_STRIDE x20 / KINGS_KNIGHT_CID x1 / POLYMERIZATION_CID x1 / cid_10e2 x1 / CONTRACT_WITH_EXODIA_CID / ANCIENT_LAMP_CID / VAMPIRE_ORCHIS_CID / RED_EYES_B_CHICK_CID / THE_CREATOR_INCARNATE_CID / DES_DENDLE_CID / EXODIA_NECROSS_CID / RED_EYES_B_DRAGON_CID / BLUE_EYES_WHITE_DRAGON_CID + raw equates cid_1497_range_lo/hi/cid_15b7_kk_pair/cid_1121_la_jinn/cid_15d1_zombie_tiger + CARD_STAT_LP_THRESHOLD_1500 x2 + zone_query_hand_tag_12a1 x5)
- **REF**: 36 槽 (gP1LifePoints x18 ptr_lp_* / gP1SlotSetCodeArray x8 ptr_sca_* / gP1HandSlotArray x5 ptr_hsa_* / gP1FieldArrayCBase x2 ptr_fac_* / gP1SlotCountBase x2 ptr_scb_* / gEquipZoneBase_1d98 x1 ptr_ezb_*)
- **FUNC_RENAME**: 21 (all newly created functions named at createFunction + re-confirmed by RefineF11Seg4aSlots)
- **PLATE**: 21 (all ASCII, all <= 500 chars; all <= 427 chars)
- **disasm**: 21 fn (clearListing + setTMode + per-fn DisassembleCommand + createFunction; 84 pool DWords; 6 degenerate entries excluded from createFunction)
- **carve**: 0
- **新增 CID (card_info.inc)**: 26 NEW (21 proposal + 5 additional raw equates for BST exclusion values: cid_1497_range_lo=0x1497/cid_1497_range_hi=0x17ae/cid_15b7_kk_pair=0x15b7/cid_1121_la_jinn=0x1121/cid_15d1_zombie_tiger=0x15d1); 27 REUSE confirmed
- **新增 ewram**: 1 (gEquipZoneBase_1d98=0x0201e278 fn16 GAP_CID_13ED zone scan base)
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +21 rows (all NEW functions added to naming-proposals.csv)
- **commit**: (see below)

### 4.04c Seg-4c 完成记录

- **范围**: `[0x0808962c, 0x0808a2ac)` — 0xC80 = 3200 B; **23 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 39 槽 (PLAYER_BLOCK_STRIDE x23 / CARD_FIELD3_THRESHOLD_1500 x1 / zone_query_hand_tag_12a1 x4 / fn21 CID dispatch pool x11: KNIGHTS_TITLE_CID/BONDING_H2O_CID/DEDICATION_THROUGH_LIGHT_DARK_CID/PHOTON_GENERATOR_UNIT_CID/BUSTER_BLADER_CID/DARK_MAGICIAN_CID_0FC9/DARK_MAGICIAN_OF_CHAOS_CID/WATER_DRAGON_CID/CYBER_LASER_DRAGON_CID/NECROVALLEY_CID) + 1 RAW label (cid_167c_dark_magician_knight)
- **REF**: 36 槽 (gP1LifePoints x19 ptr_lp_* / gP1SlotSetCodeArray x5 ptr_sca_* / gP1HandSlotArray x5 ptr_hsa_* / gP1FieldArrayCBase x5 ptr_fac_* / gP1ChainZoneArray x2 ptr_cza_*)
- **FUNC_RENAME**: 23 (all newly created functions)
- **PLATE**: 23 (all ASCII, all <=500 chars; max=475 chars fn09; fn21 plate corrected from 574->472 chars by reviewer)
- **disasm**: 23 fn (clearListing + setTMode + 23 per-fn DisassembleCommand + createFunction; 76 pool DWords; 4 degenerate entries excluded: 0x0808985e/0x08089a58/0x08089e78/0x0808a28e; 0x0808a046=0x0000 padding excluded)
- **carve**: 0
- **新增 CID (card_info.inc)**: 11 NEW (TOON_TABLE_OF_CONTENTS_CID=0x1562 / MACHINE_DUPLICATION_CID=0x157a / GRAVEKEEPER_SPY_CID=0x1585 / AN_OWL_OF_LUCK_CID=0x1593 / TERRAFORMING_CID=0x15a1 / GOBLIN_ZOMBIE_CID=0x15b9 / FRONTLINE_BASE_CID=0x15e2 / TRIBUTE_DOLL_CID=0x15ed / APPRENTICE_MAGICIAN_CID=0x1612 / BONDING_H2O_CID=0x195c / LEAGUE_UNIFORM_NOMENCLATURE_CID=0x1978); 22 REUSE confirmed; C5 value-grep all 0 hits before adding
- **1 group-handler function**: fn21 (6-CID magic evolution group: Skilled White/Dark Magician + Knight's Title + Dedication/Light+Dark + Bonding-H2O + Photon Generator Unit; partner CID dispatch + 3 loops substate d/e/b)
- **4 degenerate entries excluded from createFunction**: 0x0808985e (BL mid-loop fn05) / 0x08089a58 (fall-through fn09) / 0x08089e78 (bitfield pair fn17) / 0x0808a28e (bcc backward fn23)
- **review corrections applied**: fn21 plate 574->472 chars; fn08 addr 0x08089990 (header typo fixed); fn03 pw 04861205 (corrected)
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +23 rows (naming-proposals.csv)
- **commit**: (pending)

### 4.06 Seg-6 完成记录

- **范围**: `[0x0808ea28, 0x0808f7c0)` -- 19 pre-existing named fn (equip field scan / sprite enqueue cluster, region C, 0 ROM_INCBIN)
- **EQ**: 85 槽 (73 named REUSE + 12 NEW eq from raw/state-mask table: SPELL_ZONE_TARGET_CID_PACKED/SOLEMN_WISHES_CID_SHIFTED x2/FIRE_PRINCESS_CID_SHIFTED/AMAZONESS_TIGER_CID_SHIFTED/FATAL_ABACUS_CID_SHIFTED x2/SLOT_CARD_EMPTY x2/EQUIP_NODE_TAG_MASK x2/CRUSH_CARD_ZONE11_TAG/DECK_DEV_VIRUS_ZONE11_TAG)
- **RENAME**: 12 槽 (7x PTR_gP1LifePoints_0808xxxx -> ptr_lp_* + 5x raw neg-offset/internal: slot_set_code_array_neg_off_eb64/equip_zone_to_slot_state_neg_off_ee6c/lp_block2_to_zone_chain_neg_off_f6d4/lp_block2_to_zone_chain_neg_off_f7b0/switchd_base_f818)
- **REF**: 0
- **PLATE**: 17 functions (C8 stale-FUN_ substitution; 13 unique FUN_ addresses: FUN_08044e30/FUN_08047218/FUN_08047f50/FUN_08048020/FUN_08048364/FUN_080486e4/FUN_08049014/FUN_080490b4/FUN_0804a2c8/FUN_0806c368/FUN_08090218/FUN_08099e0c/FUN_0809a1a4 -> current names)
- **disasm**: 0
- **carve**: 0
- **新增 constants**: card_info.inc +12 (THUNDER_NYAN_NYAN_CID=0x13a4/FIRE_PRINCESS_CID=0x144d/MYSTICAL_BEAST_SERKET_CID=0x147a/CONVULSION_OF_NATURE_CID=0x1510/KOZAKY_CID=0x1784 + SOLEMN_WISHES_CID_SHIFTED=0xa0280000/FIRE_PRINCESS_CID_SHIFTED=0xa2680000/FATAL_ABACUS_CID_SHIFTED=0xa5f80000/AMAZONESS_TIGER_CID_SHIFTED=0xb0780000 + SPELL_ZONE_TARGET_CID_PACKED=0x13680000/CRUSH_CARD_ZONE11_TAG=0x0002123b/DECK_DEV_VIRUS_ZONE11_TAG=0x0002188c); duel_field.inc +1 (EQUIP_NODE_TAG_MASK=0x000fffff); C5 value-grep all 13 NEW -> 0 hits confirmed
- **新增/改名函数**: 0 (no CSV sync needed)
- **§5.1**: 0
- **post-landing gates**: non-ASCII=0 / FUN_[0-9a-f]{8} in Seg-6=0 / DAT_0808[ef]=0 / PTR_gP1LifePoints_ residue=0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: not needed (0 new/renamed functions)
- **commit**: (see git log)

### 4.07 Seg-7 完成记录

- **范围**: `[0x0808f7c0, 0x08090a78)` -- 30 pre-existing named fn + 2 NEW stub fn
- **EQ**: 109 槽 (108 literal pool slots REUSE/NEW + 1 EFFECT_NODE_TABLE_TYPE1_COUNT slot @0x08090534)
  - NEW: BERSERK_GORILLA_CID/FALLING_DOWN_CID_SHIFTED/SOUL_ABSORBING_BONE_TOWER_CID_SHIFTED/THE_BLOCKMAN_CID_SHIFTED/THEINEN_ACTIVATION_PACKED (card_info.inc +5)
  - NEW: SPHINX_ACTIVATION_INIT_TEMPLATE/EFFECT_NODE_TABLE_TYPE0_BASE/EFFECT_NODE_TABLE_TYPE0_COUNT/EFFECT_NODE_TABLE_TYPE1_BASE/EFFECT_NODE_TABLE_TYPE1_COUNT/EFFECT_NODE_TABLE_TYPE2_BASE/EFFECT_NODE_TABLE_TYPE3_BASE/EQUIP_ZONE_COUNT_TABLE (duel_field.inc +8)
  - C5 corrections: EQUIP_ZONE_COUNT_TABLE_OFF(0x1cb8) kept as offset for file08; new EQUIP_ZONE_COUNT_TABLE(0x0201e1c8) for abs-ptr Seg-7 slots; ANDRO_SPHINX_CID(0x17c7) corrected from erroneous SPHINX_TELEIA_CID
- **REF**: 0
- **RENAME**: 10 槽 (9x PTR_gP1LifePoints_0808xxxx -> ptr_lp_xxx / 1x DAT_0808f934 -> ptr_case_body_f934)
- **FUNC_RENAME**: 1 (set_equip_activation_state_by_mode_alt -> invoke_effect_node_handler_3arg @0x080905e8; old name was wrong -- no equip state write, just effect-node 3-arg dispatch)
- **PLATE**: 36 (33 C8 stale-FUN_ substitution + 2 CJK->ASCII rewrite for count_effect_node_activations_by_zone/scan_equip_chain_nodes_for_bitmap_update + 2 new stubs return_effect_node_result_0/2 + 1 find_card_effect_node_entry)
- **disasm**: 2 callback stubs (return_effect_node_result_0 @ 0x080904ec: movs r0,#0;bx lr; return_effect_node_result_2 @ 0x080904f0: movs r0,#2;bx lr; clearListing+setTMode+2x DisassembleCommand+2x createFunction)
- **carve**: 0
- **§5.1**: 0
- **新增 constants**: card_info.inc +5 CID; duel_field.inc +8 (see EQ above)
- **post-landing gates**: non-ASCII in Seg-7=0 / FUN_[0-9a-f]{8} in Seg-7=0 / DAT_/PTR_gP1LifePoints_ in Seg-7=0 / ROM_INCBIN/.byte in stub range=0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +2 rows (return_effect_node_result_0/2) + 1 rename (invoke_effect_node_handler_3arg) = 3 rows total
- **commit**: (see below)

### 4.08 Seg-8 完成记录

- **范围**: `[0x08090a78, 0x08091888)` -- 3 pre-existing named fn (region C, 0 ROM_INCBIN)
  - `build_equip_candidate_score_table` (0x08090a78, 0xc48 B, 数据密集 63 pool 槽)
  - `invoke_build_equip_candidate_score_table` (0x080916c0)
  - `write_equip_target_score_entry` (0x080916e4)
- **EQ**: 52 槽 (36 REUSE + 16 NEW)
  - NEW: KINETIC_SOLDIER_CID=0x000013aa / HUNTER_7_WEAPONS_CID=0x000014cc / AMAZONESS_SWORDS_WOMAN_CID=0x000014a4 / STEAMROID_CID=0x000018f2 / SKYSCRAPER_CID=0x000018ff / DIMENSION_WALL_CID=0x00001930 (card_info.inc +6)
  - NEW: EQUIP_ATK_SCORE_HI_2499=0x000009c3 / EQUIP_ATK_SCORE_HI_2500=0x000009c4 (card_info.inc +2)
  - REUSE: STEAMROID_CID x2 + KINETIC_SOLDIER_CID x2 + HUNTER_7_WEAPONS_CID x3 (at 0x08090cdc/0x08090e84/0x08091060) + AMAZONESS_SWORDS_WOMAN_CID x1 + SKYSCRAPER_CID x1 + DIMENSION_WALL_CID x1 + EQUIP_ATK_SCORE_HI_2499 x4 + EQUIP_ATK_SCORE_HI_2500 x2 + gEquipLpScoreBase x5 + gEquipCandidateScoreBase x4 + gEquipCandidateInitBase x2 + SLOT_ACTIVE_CHECK_CODE x5 + gEquipCandidateSlotA x2 + gEquipCandidateSlotB x2 + gP1LifePoints x7 + gEquipEffectZoneBase x2 + PLAYER_BLOCK_STRIDE x3 + gDuelFieldSlots x1
- **REF**: 21 槽 (16 REUSE + 5 NEW)
  - NEW: gEquipLpScoreBase=0x0201afe0 / gEquipCandidateSlotA=0x0201bc38 / gEquipCandidateSlotB=0x0201bc3c (ewram.inc +3 = 5 NEW total; 2 others from existing REUSE slots)
  - 16 ptr_gP1LifePoints_ / ptr_gEquipEffectZoneBase / ptr_gEquipLpScoreBase / ptr_gEquipCandidateScoreBase / ptr_gEquipCandidateInitBase / ptr_gEquipCandidateSlotA / ptr_gEquipCandidateSlotB group
- **RENAME**: 21 (all REF slot labels: DAT_ -> ptr_global_hexaddr with EOL)
- **PLATE**: 3 ASCII rewrites
  - `build_equip_candidate_score_table`: FUN_080afcb4->eval_equip_spell_placement_with_score / FUN_080b04a8->eval_fieldspell_equip_placement_full (417 chars)
  - `invoke_build_equip_candidate_score_table`: FUN_08099314 kept (Seg-9+ unnamed, allowed per C8) (300 chars)
  - `write_equip_target_score_entry`: factual correction "Viser Des check"->"DIMENSION_WALL_CID=0x1930" / FUN_08091888->eval_field_equip_activation_candidates (446 chars)
- **disasm**: 0
- **carve**: 0
- **新增 constants**: card_info.inc +8 (6 CID + 2 score gates); ewram.inc +3 (gEquipLpScoreBase/gEquipCandidateSlotA/gEquipCandidateSlotB); C5 value-grep all 8 NEW -> 0 hits confirmed
- **post-landing gates**: non-ASCII in Seg-8=0 / FUN_[0-9a-f]{8} in Seg-8 residue=FUN_08099314 only (Seg-9+, allowed per review C8) / DAT_/PTR_ in Seg-8=0
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: not needed (0 new/renamed functions)
- **commit**: (see below)

### 4.05 Seg-5 完成记录

- **范围**: `[0x0808d7f4, 0x0808e8fc)` -- 18 pre-existing named fn (region C, 0 ROM_INCBIN)
- **EQ**: 107 槽 (14x PTR_gP1LifePoints REUSE + 23x PLAYER_BLOCK_STRIDE REUSE + 13x gDuelFieldSlots REUSE + 5x gDuelFieldSlotState REUSE + 7x gEquipEffectZoneBase REUSE + 6x gEquipZoneCountTable REUSE + 8x misc EWRAM globals + 30x CID/ROM ptr EQ)
- **RENAME**: 15 (14x PTR_gP1LifePoints_0808xxxx -> ptr_lp_* + 1x DAT_0808d8a8 -> switchd_base_d8a8 internal switchD table ptr)
- **REF**: 0 (no REF slots; PTR_ handled via equate-based RENAME, consistent with Seg-3a/3b)
- **PLATE**: 12 (C8 stale-FUN_ substitution: fn04/fn05/fn06/fn08/fn10/fn11/fn12/fn13/fn14/fn16/fn17/fn18)
- **carve**: 0
- **disasm**: 0
- **新增 constants**: card_info.inc +7 CID (MAIDEN_OF_THE_AQUA_CID=0x13a2 / FINAL_ATTACK_ORDERS_CID=0x15fb / LEVEL_LIMIT_AREA_B_CID=0x17a6 / LEVEL_LIMIT_AREA_A_CID=0x197b / KOTODAMA_CID=0x1343 / MAGICAL_THORN_CID=0x1306 / SKULL_INVITATION_CID=0x1361); duel_field.inc +4 (gEffectHandlerTable=0x09e5a128 / gEquipCandidateScoreBase=0x09e3f150 / gEquipCandidateInitBase=0x09e3f164 / SLOT_ACTIVE_CHECK_CODE=0x0000104c); C5 value-grep all 11 NEW -> 0 hits confirmed
- **raw DWORD 留 DAT_**: 5 slots (DAT_0808dc1c=0xfdc / DAT_0808e4d4=0x98300000 / DAT_0808e5b0=0xffffe358 / DAT_0808e834=0x3a200000 / DAT_0808e8f8=0x9b080000) -- no named constant, intentionally left as-is
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **post-landing gates**: non-ASCII=0 ✅ / FUN_[0-9a-f]{8}=0 ✅ / PTR_gP1LifePoints residue=0 ✅ / DAT_ residue=5 raw slots (intentional) ✅
- **CSV sync**: not needed (0 new/renamed functions)
- **commit**: (see git log)

### 4.04g Seg-4g 完成记录 (LAST giant-block sub-segment — Seg-4 COMPLETE)

- **范围**: `[0x0808cabc, 0x0808d7f4)` — 0xD38 = 3384 B; **20 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 30 槽 (PLAYER_BLOCK_STRIDE x21 / NECROVALLEY_CID REUSE x1 / PARASITE_PARACIDE_CID REUSE x3 / CARD_FIELD3_THRESHOLD_1500 REUSE x1 / WINGED_KURIBOH_CID=0x18aa NEW x1 / SLOT_CARD_SET_CODE_MASK REUSE x1 / CARD_FIELD_STAT_CLEAR_UPPER4_MASK=0x0fffffff NEW x1 / slot_field_mask_ffff803f REUSE x1)
- **REF**: 42 槽 (gP1LifePoints x17 / gP1HandSlotArray x7 / gP1SlotSetCodeArray x8 / gP1HandCountBase x3 / gP1FieldArrayCBase x4 / gDuelFieldSlots x1 / gEquipEffectZoneBase x2 / gP1SlotCountBase x1)
- **FUNC_RENAME**: 20 (all newly created functions)
- **PLATE**: 20 ASCII plates (all <= 500 chars; max 494: fn11 Inferno Reckless Summon 3-loop)
- **carve**: 0 (no data tables in range)
- **disasm**: 20 functions via DisassembleF11Seg4gBlocks.py; 72 pool DWords; degenerate excluded: 0x0808d20e (mid-body CMP r2,r1 fn12 offset+0x52) + 0x0808d21e (upper half pool word gP1LifePoints at 0x0808d21c fn12) + 0x0808d7de (align pad upper half SLOT_CARD_SET_CODE_MASK fn20); weak excluded: 0x0808d58c (mid-body CMP r1,r0 fn17 offset+0xf8); fixup script DisassembleF11Seg4gFixupPools.py (3 pool DWords for SUB_080970d4/e4 helper stubs in asm/12 disassembled as BL targets from fn20)
- **NEW constants**: card_info.inc +5 CID (WINGED_KURIBOH_CID=0x18aa / SCARR_DARK_WORLD_CID=0x196a / GATEWAY_DARK_WORLD_CID=0x1973 / ARMED_CHANGER_CID=0x197c / NEXT_TO_BE_LOST_CID=0x19dc) + CARD_FIELD_STAT_CLEAR_UPPER4_MASK=0x0fffffff; ewram.inc +1 (gEquipEffectZoneBase=0x0201e4f0); 3 REUSE confirmed (MAGICAL_MALLET_CID/INFERNO_RECKLESS_SUMMON_CID/WHITE_HORNS_DRAGON_CID fn10/fn11/fn12 -- CID shift correction applied per reviewer fix #1/2)
- **reviewer fixes applied**: #1 fn10/fn11/fn12 CID assignment shift corrected (fn10=0x198d Magical Mallet, fn11=0x198e Inferno Reckless Summon, fn12=0x1996 White Horns Dragon; all 3 REUSE); #2 fn10 name corrected to scan_zone_magical_mallet_substate_b / fn11 to scan_zone_inferno_reckless_summon_substate_d_e_b / fn12 to scan_zone_white_horns_dragon_substate_e
- **multi-CID handlers**: fn18 (NEXT_TO_BE_LOST_CID=0x19dc + GENERATION_SHIFT_CID=0x19dd, 2 dispatch table entries); fn20 (CID=0xfffe group sentinel, variable substate r8=arg2, calls scan_card_type_effect_handler_table)
- **§5.1**: 0 (all 20 fn referenced in dispatch table)
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +20 rows (naming-proposals.csv)
- **commit**: (see git log)

**Seg-4 SUMMARY (4a+4b+4c+4d+4e+4f+4g = 163 new functions, GIANT BLOCK FULLY ELIMINATED)**:
- Total new functions: 21+25+23+24+25+25+20 = **163 hidden card-effect scan callbacks disassembled+named**
- Total giant ROM_INCBIN 0x87d58/0x5a9c (23,196 B) = ZERO ROM_INCBIN remaining in [0x08087d58, 0x0808d7f4)
- All 7 sub-segments byte-identical SHA1 9689337d throughout

### 4.04f Seg-4f 完成记录

- **范围**: `[0x0808bb7c, 0x0808cabc)` — 0xF40 = 3904 B; **25 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 37 槽 (PLAYER_BLOCK_STRIDE x27 / EQUIP_ACTIVE_CTX_OFF x4 / CARD_FIELD3_THRESHOLD_1500 x1 / SKULL_SERVANT_CID REUSE x1 / KING_OF_SKULL_SERVANTS_CID REUSE x1 / PARASITE_PARACIDE_CID REUSE x1 / slot_field_mask_ffff803f REUSE x1 / VAMPIRE_GENESIS_GDUELPF_NEG_OFF=0xfffffef4 NEW x1)
- **REF**: 53 槽 (gP1LifePoints x22 / gP1SlotSetCodeArray x4 / gP1HandSlotArray x9 / gP1HandCountBase x2 / gP1FieldArrayCBase x7 / gDuelPhaseFlags x4 / gP1ChainZoneArray x3 / gDuelFieldSlots x1 / gP1SlotCountBase x1)
- **FUNC_RENAME**: 25 (all newly created functions)
- **PLATE**: 25 ASCII plates (all <= 500 chars; max 430: fn07+fn08 Vampire Genesis + fn25 Gilford the Legend)
- **carve**: 0 (no data tables in range)
- **disasm**: 25 functions via DisassembleF11Seg4fBlocks.py; 93 pool DWords; degenerate excluded: 0x0808be88 (fn07+fn08 mid-body BNE) + 0x0808c3da (fn17+fn18 mid-body LDR); weak excluded: 0x0808bf4a; fixup script RefineF11Seg4fFixup.py (stride at 0x0808c4a0 fn19 missed)
- **NEW constants**: card_info.inc +10 CID (RESCUE_CAT/FULFILLMENT_CONTRACT/BEAST_SOUL_SWAP/HERO_SIGNAL/WROUGHTWEILER/POWER_BOND/SUMMON_PRIEST/FUSION_RECOVERY/MIRACLE_FUSION/WARRIOR_LADY_WASTELAND) + 1 raw (VAMPIRE_GENESIS_GDUELPF_NEG_OFF=0xfffffef4)
- **group-handlers**: 0 (all 25 functions handle exactly one CID each; fn07+fn08 and fn17+fn18 are alt-entry fallthrough pairs)
- **reviewer fixes**: #1 NO new GILFORD_HAND_SLOT_MASK (REUSE slot_field_mask_ffff803f); #2 fn21/fn22 each TWO pools (+4 DWords, REF 51->53); #3 fn26 name _d not _bd
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +25 rows (naming-proposals.csv)
- **commit**: (see below)

### 4.04e Seg-4e 完成记录

- **范围**: `[0x0808ad8c, 0x0808bb7c)` — 0xDF0 = 3568 B; **25 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 30 槽 (PLAYER_BLOCK_STRIDE x25 / POT_OF_GREED_CID x1 REUSE / PARASITE_PARACIDE_CID x2 REUSE / CARD_FIELD3_THRESHOLD_1500 x1 REUSE / sentinel_bc100000 x1 raw sentinel)
- **REF**: 46 槽 (gP1LifePoints x21 / gP1FieldArrayCBase x7 / gP1HandSlotArray x6 / gP1SlotSetCodeArray x7 / gP1ZoneHandCount x2 / gP1SlotCountBase x1 / gDuelFieldSlots x1 / gP1ChainZoneArray x1)
- **FUNC_RENAME**: 25 (all newly created functions)
- **PLATE**: 25 (all ASCII, all <=500 chars; max=466 chars fn25 hex-sealed fusion group)
- **disasm**: 25 fn (clearListing + setTMode + 25 per-fn DisassembleCommand + createFunction; 76 pool DWords; 2 degenerate strong excluded: 0x0808b40e mid-body MOVS fn12 + 0x0808b95a mid-body LSRS fn23; 2 weak excluded: 0x0808b58a mid-prologue MOV fn16 + 0x0808b798 upper-half BL fn19)
- **carve**: 0
- **新增 CID (card_info.inc)**: 11 NEW (LIGHT_OF_JUDGMENT_CID=0x1764 / BECKONING_LIGHT_CID=0x1769 / SPIRIT_CALLER_CID=0x1795 / SOUL_REVERSAL_CID=0x17a2 / HOWLING_INSECT_CID=0x17e5 / TWO_MAN_CELL_BATTLE_CID=0x17f8 / MONSTER_REINCARNATION_CID=0x1845 / LIGHTEN_THE_LOAD_CID=0x1847 / LIGHT_HEX_SEALED_FUSION_CID=0x1870 / DARK_HEX_SEALED_FUSION_CID=0x1871 / EARTH_HEX_SEALED_FUSION_CID=0x1872) + sentinel_bc100000=0xbc100000 raw equ; 21 REUSE confirmed; C5 value-grep all 0 hits before adding
- **4 excluded entries**: 2 degenerate strong (0x0808b40e mid-body fn12 / 0x0808b95a mid-body fn23) + 2 weak (0x0808b58a mid-prologue fn16 / 0x0808b798 upper-half BL fn19)
- **group-handler functions**: fn03 (Archlord Zerato + Light of Judgment, 2 CID light-attr); fn14 (Howling Insect + Masked Dragon + UFOroid, 3 CID ATK<=1500+FLIP); fn25 (Hex-Sealed Fusion Light/Dark/Earth, 3 CID chain zone)
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +25 rows (naming-proposals.csv)
- **commit**: (see below)

### 4.04d Seg-4d 完成记录

- **范围**: `[0x0808a2ac, 0x0808ad8c)` — 0xAE0 = 2784 B; **24 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 30 槽 (PLAYER_BLOCK_STRIDE x25 / EMBLEM_OF_DRAGON_DESTROYER_CID x1 / BUSTER_BLADER_CID x1 / NECROVALLEY_CID x1 / CARD_FIELD3_THRESHOLD_1500 x1 / slot_field_mask_ffff803f x1 raw mask)
- **REF**: 34 槽 (gP1LifePoints x22 ptr_lp_* / gP1FieldArrayCBase x3 ptr_fac_* / gP1HandSlotArray x5 ptr_hsa_* / gP1SlotSetCodeArray x2 ptr_sca_* / gP1AltHandSlotArray x1 ptr_aha_* / gP1HandCountBase x1 ptr_hcb_*)
- **FUNC_RENAME**: 24 (all newly created functions)
- **PLATE**: 24 (all ASCII, all <=500 chars; max=477 chars fn14 chaos envoy group)
- **disasm**: 24 fn (clearListing + setTMode + 24 per-fn DisassembleCommand + createFunction; 64 pool DWords; 3 degenerate strong excluded: 0x0808a44c/0x0808a450 fn05 mid-loop + 0x0808a996 fn16 mid-body; 3 weak excluded: 0x0808a974/0x0808a9c2/0x0808ab2c; 0x0808ab92 alignment padding excluded)
- **carve**: 0
- **新增 CID (card_info.inc)**: 11 NEW (SENRI_EYE_CID=0x1628 / ARSENAL_ROBBER_CID=0x166b / CHAOSRIDER_GUSTAPH_CID=0x16c4 / DIMENSION_DISTORTION_CID=0x16d8 / RETURN_FROM_DD_CID=0x17be / DDM_DIFF_DIM_MASTER_CID=0x191e / MANJU_TEN_THOUSAND_HANDS_CID=0x170c / SALVAGE_CID=0x1714 / LADY_NINJA_YAE_CID=0x1754 / ARSENAL_SUMMONER_CID=0x1647 / CHOPMAN_THE_DESPERATE_OUTLAW_CID=0x16bc) + 1 raw mask (slot_field_mask_ffff803f=0xffff803f); 23 REUSE confirmed; C5 value-grep all 0 hits before adding
- **6 excluded entries**: 3 degenerate strong (0x0808a44c mid-loop LDR fn05 / 0x0808a450 mid-loop MUL fn05 / 0x0808a996 mid-body MOVS fn16) + 3 weak (0x0808a974 pool literal / 0x0808a9c2 mid-code MOV / 0x0808ab2c fn19 epilogue bytes)
- **group-handler functions**: fn17 (4-CID Dimension Removal group: Dimension Distortion + Fusion + Return from DD + D.D.M.); fn24 (3-CID Guardian equip group: Guardian Elma + Chopman + The Kick Man; local struct + memset + mask 0xffff803f)
- **review correction applied**: fn20 pool addr 0x0808ab92->0x0808ab94 (C4 alignment fix applied to proposal and script)
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +24 rows (naming-proposals.csv)
- **commit**: (see below)

### 4.04b Seg-4b 完成记录

- **范围**: `[0x08088904, 0x0808962c)` — 0xD28 = 3368 B; **25 NEW fn (equip zone scan callbacks, all dispatched from table 0x09e5a128)**
- **EQ**: 36 槽 (PLAYER_BLOCK_STRIDE x27 / SUPER_ROBOLADY_CID x1 + SUPER_ROBOYAROU_CID x2 CID pool pairs / zone_query_hand_tag_12a1 x4 / LP_BAR_ANIM_STATE_OFF x1 / SPRITE_ROW_ENTRY_DATA_OFF x1)
- **REF**: 40 槽 (gP1LifePoints x23 ptr_lp_* / gP1SlotSetCodeArray x6 ptr_sca_* / gP1HandSlotArray x4 ptr_hsa_* / gP1FieldArrayCBase x3 ptr_fac_* / gP1ChainZoneArray x1 / gP1AltHandSlotArray x1 / gP1SlotCountBase x1 / gDuelPhaseFlags x1)
- **FUNC_RENAME**: 25 (all newly created functions named at createFunction + re-confirmed by RefineF11Seg4bSlots)
- **PLATE**: 25 (all ASCII, all <= 500 chars; max = 489 chars fn08)
- **disasm**: 25 fn (clearListing + setTMode + per-fn DisassembleCommand + createFunction; 79 pool DWords; 2 degenerate entries excluded: 0x0808939c mid-body bcs target of fn23 + 0x08089560 mid-prologue second-push of fn26; 1 weak entry excluded: 0x8088ef6 mid-loop fn11)
- **carve**: 0
- **新增 CID (card_info.inc)**: 16 NEW (KYCOO_THE_GHOST_DESTROYER_CID=0x1480 / FOOLISH_BURIAL_CID=0x1474 / INFERNAL_FLAME_EMPEROR_CID=0x18e0 / SPIRIT_OF_FLAMES_CID=0x1484 / GARUDA_THE_WIND_SPIRIT_CID=0x1487 / LEKUNGA_CID=0x15bc / FREED_THE_BRAVE_WANDERER_CID=0x16c0 / GIGANTES_CID=0x16c7 / SUPPLY_CID=0x148b / SKULL_LAIR_CID=0x1490 / REINFORCEMENT_OF_THE_ARMY_CID=0x14d0 / DES_FERAL_IMP_CID=0x14ef / SILENT_FIEND_CID=0x14f7 / SUPER_ROBOLADY_CID=0x1507 / SUPER_ROBOYAROU_CID=0x1508 / PYRAMID_TURTLE_CID=0x152f); 32 REUSE confirmed (C5 value-grep all 0 hits before adding)
- **7 group-handler functions**: fn01 (Kycoo/Dark Blade), fn03 (Dark Necrofear/Megarock/Doom Dozer), fn08 (13-CID spirit/elemental/removed group), fn13 (cid_135b/Marauding Captain), fn19 (Silent Fiend/Soul Resurrection), fn21 (Super Robolady/Roboyarou pair), fn22 (Keldo/Disappear/Dimension Jar/D.D.Guide), fn23 (Last Turn), fn25 (Vampire Lord/Lady)
- **3 excluded entries**: degenerate 0x0808939c (fn23 bcs target) + 0x08089560 (fn26 2nd push) + weak 0x8088ef6 (fn11 mid-loop)
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: +25 rows (naming-proposals.csv)
- **commit**: (see below)

### 4.03b Seg-3b 完成记录

- **范围**: `[0x080872e4, 0x08087d58)` — 15 named fn (write_equip_zone_entries_by_lv_card_id .. scan_zone_opponent_field5_substate_e)
- **EQ**: 82 槽 (10 NEW CID + 72 REUSE PLAYER_BLOCK_STRIDE x15 / MYSTIC_SWORDSMAN_LV2_CID / TIME_WIZARD_CID / GREAT_DEZARD_CID / A_DEAL_WITH_DARK_RULER_CID / SAGES_STONE_CID / ULTIMATE_INSECT_LV1/3/5/7_CID / HORUS_LV6/8_CID / SILENT_SWORDSMAN_LV3/5/7_CID / SILENT_MAGICIAN_LV4/8_CID / ARMED_DRAGON_LV5/7_CID / THEINEN_THE_GREAT_SPHINX_CID / BERSERK_DRAGON_CID / DARK_MAGICIAN_CID_0FC9 / TRANSCENDENT_WINGS_CID / ATTACK_REFLECTOR_UNIT_CID / TRIAL_OF_THE_PRINCESSES_CID / HARPIE_LADY_CID / FUSHIOH_RICHIE_CID / BLUE_EYES_WHITE_DRAGON_CID / DARK_MIMIC_LV3_CID / SACRED_PHOENIX_CID / GEARFRIED_SWORDMASTER_CID / WINGED_KURIBOH_LV10_CID / WHITE_MAGICIAN_PIKERU_CID / EBON_MAGICIAN_CURRAN_CID / PRINCESS_PIKERU_CID / PRINCESS_CURRAN_CID / POLYMERIZATION_CID x2 / RED_GADGET_CID / GREEN_GADGET_CID x2 / YELLOW_GADGET_CID x2 / BIRDFACE_CID / CARD_STAT_LP_THRESHOLD_1500 / zone_query_hand_tag_12a1 / CHIMERA_FLYING_MYTHICAL_BEAST_CID / MIRACLE_RESTORING_CID / PARASITE_PARACIDE_CID / MAGICAL_LABYRINTH_CID / WALL_SHADOW_CID / DARK_MAGICIAN_CID_0FC9 x3)
- **REF**: 10 槽 (gP1FieldArrayCBase x3 / gP1SlotSetCodeArray x4 / gP1ChainZoneArray x1 / gP1HandSlotArray x2; all ewram.inc REUSE)
- **RENAME**: 13 槽 (PTR_gP1LifePoints_ x13 -> ptr_lp_xxxx)
- **PLATE**: 14 (14 full ASCII rewrites <=488 chars; 3 CORRECTED misnomer base-addr: gDuelCardPool_alt_base->gP1HandSlotArray x2 + gDuelEffectZones/gDuelCardPool_alt->gP1FieldArrayCBase/gP1SlotSetCodeArray)
- **disasm**: 0
- **carve**: 0
- **新增 CID**: 10 -> card_info.inc (ELEGANT_EGOTIST_CID=0x10e4 / GAZELLE_CID=0x1291 / BERFOMET_CID=0x1293 / BUSTER_BLADER_CID=0x1377 / DARK_SAGE_CID=0x146e card_0944 / MIRAGE_KNIGHT_CID=0x1643 / MYSTICAL_SHINE_BALL_CID=0x173d / SPIRIT_OF_PHARAOH_CID=0x1788 / RELEASE_RESTRAINT_CID=0x187e / CYBER_BARRIER_DRAGON_CID=0x19a8)
- **新增/改名函数**: 0
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: not needed
- **commit**: `793378c`

### 4.03a Seg-3a 完成记录

- **范围**: `[0x08086cdc, 0x080872e4)` — 4 named fn (dispatch_equip_zone_activation_state / populate_equip_zone_entries_substate_d / populate_equip_zone_entries_substate_e / write_equip_zone_entries_substate_d_range)
- **EQ**: 36 槽 (全 REUSE; gDuelPhaseFlags x3 / EQUIP_PHASE_FRAME_OFF x3 / gEquipEffectZoneTable x5 / PLAYER_BLOCK_STRIDE x9 / gDuelCardCtxBase x3 / gP1FieldArrayCBase x2 / LP_BANISHER_CTX_OFF x3 / ELIGIB_ANIM_STATE_OFF x1 / ELIGIB_SPRITE_CTRL_OFF x1 / SAMSARA_CID x1 / END_OF_WORLD_CID x1 / EARTH_CHANT_CID x1 / gP1SlotSetCodeArray x1 / CARD_FIELD3_THRESHOLD_1500 x1 / zone_query_hand_tag_12a1 x1)
- **REF**: 4 槽 (switchdata_86d18 / scan_equip_zone11_fnptr_86e98 / eval_equip_score_fnptr_86fa0 / eval_equip_score_fnptr_86fb0)
- **RENAME**: 6 槽 (PTR_gP1LifePoints_ x6 -> gp1lp_ptr_xxx snake_case, EOL=gP1LifePoints)
- **PLATE**: 5 (1 CJK mojibake->ASCII rewrite dispatch_equip_zone_activation_state 497 chars + 2 misnomer fixes gDuelCardPool->gP1SlotSetCodeArray/gDuelCardPool_alt_base->gP1HandSlotArray + 2 stale FUN_ fixes FUN_080871a8/FUN_08086e90+FUN_08086fa6)
- **disasm**: 0
- **carve**: 0
- **新增 constants**: 0 (全 REUSE)
- **新增/改名函数**: 0
- **§5.1**: 0
- **byte-identical**: SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅
- **CSV sync**: not needed
- **commit**: `3689026`

---

## 五、Seg 路线图 (地址序, 边界 = 函数结束处)

按 push-prologue 检测函数入口, 地址序均分; 巨块 0x87d58 独占 Seg-4 (拆子段)。

### region A (0x80850d8..0x8087d58, 41 命名 fn, 342 槽, 3 小 incbin)

- **Seg-1** `[0x80850d8, 0x8085d4c)` -- 10 fn (enqueue_effect_slot_attr_from_bb .. build_field_action_text_by_zone_type)
  - incbin: 0x850f0/0x28, 0x85130/0x14c (疑 fn-ptr / dispatch 表; ref-scan 待执行)
  - 重函数: scan_equip_target_slots_for_card (48 槽)
- **Seg-2** `[0x8085d4c, 0x8086cdc)` ✅ -- 12 fn (dispatch_field_display_state_by_type .. check_neo_daedalus_equip_zone_eligible)
  - incbin: 0x861a0/0x27a -> R4 disasm 6 sub-case labels (equip_slot_case0..4+casea_body), NO createFunction
  - 重函数: dispatch_field_display_state_by_type (32 槽)
- **Seg-3a** `[0x8086cdc, 0x80872e4)` ✅ -- 4 fn (dispatch_equip_zone_activation_state .. write_equip_zone_entries_substate_d_range)
  - 0 incbin; EQ=36 REUSE / REF=4 / RENAME=6 / PLATE=5 (1 CJK+2 misnomer+2 stale FUN_)
- **Seg-3b** `[0x80872e4, 0x8087d58)` ✅ -- 15 fn (write_equip_zone_entries_by_lv_card_id .. scan_zone_opponent_field5_substate_e)
  - 0 incbin; EQ=82(10 NEW CID+72 REUSE)/REF=10/RENAME=13/PLATE=14; Seg-3 (3a+3b) fully done

### region B (0x8087d58..0x808d7f4, ~197 未命名 THUMB fn, 巨块)

- **Seg-4** `[0x8087d58, 0x808d7f4)` -- ROM_INCBIN 0x87d58/0x5a9c (23,196 B) = 未反汇编 THUMB 代码区
  - **拆 Seg-4a..4g** (~27 fn/子段, 地址序): 逐 fn R4 disasm + createFunction + 命名 + CSV row
  - ref-scan 已定标: **197 distinct THUMB+1 fn-ptr 目标; 185 有 word-aligned dispatch-table 引用 = 强函数入口**
    (其中 163 个首半字 = `0xb5xx` push{..,lr} 前导, 确证真函数); 12 个仅非对齐 THUMB+1 = 偶合 (disasm 时据实排除,
    类比 Seg-1/2 degenerate entry: mid-BL 2nd halfword / 0x0000 pad / literal-pool word)。
  - **命名范式 (file 06..10 fn_eligible/fn_activate 沿用)**: 每 fn 经 dispatch table entry 反查 CID
    (entry 0x18B = `[CID, fn_activate+1, pad, fn_eligible+1, pad, pad]`, **fn_eligible 块 CID 在 fn_ptr-0xc**),
    查 `data/card-stats.s` 得卡名 -> `fn_activate_<card>` / `fn_eligible_<card>` (+ 核 body activate vs eligible 语义); 未分配 CID -> `cid_<hex>`。
  - 子段边界 (强入口均分 ~7 组):
    - **Seg-4a** `[0x08087d58, 0x08088904)` 21 fn ✅ (21 NEW scan_zone_* + 26 CID equates + REF=36 + 21 PLATE; byte-identical)
    - **Seg-4b** `[0x08088904, 0x0808962c)` 25 fn ✅ (25 NEW scan_zone_* + 16 CID equates + REF=40 + 25 PLATE; byte-identical)
    - **Seg-4c** `[0x0808962c, 0x0808a2ac)` 23 fn ✅ (23 NEW scan_zone_* + 11 CID equates + REF=36 + 23 PLATE; fn21 6-CID magic evolution group; byte-identical)
    - **Seg-4d** `[0x0808a2ac, 0x0808ad8c)` 24 fn ✅ (24 NEW scan_zone_* + 11 NEW CID equates + REF=34 + 24 PLATE + 1 raw mask equ; 6 excluded entries (3 degenerate strong + 3 weak); byte-identical)
    - **Seg-4e** `[0x0808ad8c, 0x0808bb7c)` 25 fn ✅ (25 NEW scan_zone_* + 11 NEW CID equates + REF=46 + 25 PLATE + 1 raw sentinel equ; 4 excluded entries (2 degenerate strong + 2 weak); byte-identical)
    - **Seg-4f** `[0x0808bb7c, 0x0808cabc)` 25 fn ✅ (25 NEW scan_zone_* + 10 NEW CID equates + 1 raw equ + REF=53 + 25 PLATE; fn07+fn08 Vampire Genesis + fn17+fn18 Summon Priest alt-entry pairs; fn21/fn22 dual-pool each; byte-identical)
    - **Seg-4g** `[0x0808cabc, 0x0808d7f4)` 20 fn ✅ (20 NEW scan_zone_* + 5 NEW CID + 2 NEW non-CID constants + REF=42 + 20 PLATE; fn10/fn11/fn12 CID corrected; fn20 group-sentinel; Seg-4 COMPLETE 163 fn total; byte-identical)

### region C (0x808d7f4..0x80941c4, 101 命名 fn, 710 槽, 0 incbin)

- **Seg-5** `[0x808d7f4, 0x808e8fc)` ✅ -- 18 fn (dispatch_equip_zone_write_by_substate_range .. scan_all_zone_slots_for_lp_change_indicator)
  - EQ=107/RENAME=15/PLATE=12/NEW CID=7/NEW duel_field=4/0 disasm/0 carve/0 §5.1; byte-identical
- **Seg-6** `[0x808e8fc, 0x808f7c0)` ✅ -- 19 fn (enqueue_paired_slot_sprite_attrs_for_player .. enqueue_sprite_by_field_copy_count)
  - EQ=85/RENAME=12/PLATE=17/NEW card_info=12/NEW duel_field=1/0 disasm/0 carve/0 §5.1; byte-identical
- **Seg-7** `[0x808f7c0, 0x8090a78)` ✅ -- 32 fn (scan_field_slots_for_equip_chain_node_bitmap_update .. scan_equip_chain_nodes_for_bitmap_update)
  - EQ=109(11 NEW+REUSE)/RENAME=10/FUNC_RENAME=1/PLATE=36/disasm=2 stubs/NEW card_info=5/NEW duel_field=8/0 carve/0 §5.1; byte-identical
- **Seg-8** `[0x8090a78, 0x8091888)` ✅ -- 3 fn (build_equip_candidate_score_table + invoke_ + write_equip_target_score_entry)
  - EQ=52(36R+16N)/REF=21(16R+5N)/RENAME=21/PLATE=3; NEW card_info=8/NEW ewram=3; byte-identical
- **Seg-9** `[0x8091888, 0x8093598)` -- 20 fn (eval_field_equip_activation_candidates + card_display_op_0x31 族)
  - **eval_field_equip_activation_candidates (187 槽, 0x1afc B 怪兽), heavy, 执行时可拆 9a/9b**
- **Seg-10** `[0x8093598, 0x80941c4)` -- 9 fn (clear_duel_puzzle_wram_regions .. render_duel_puzzle_text_to_sprite_queue)
  - duel puzzle 文本: parse_duel_puzzle_text_token (68 槽) + render_duel_puzzle_text_to_sprite_queue (14 槽)

---

## 5.1 未引用数据登记表

(全 ROM 0 引用的数据块登记于此, 引用到时再处理)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|------|------|---------|---------|------|
| (暂无) | | | | |
