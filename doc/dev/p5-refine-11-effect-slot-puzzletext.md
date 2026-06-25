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
| 1  | 0x80850d8..0x8085d4c | 10 | ~100 | 2 inc (0x850f0/0x28, 0x85130/0x14c) | ✅ | (see §四 4.01) |
| 2  | 0x8085d4c..0x8086cdc | 12 | ~91  | 1 inc (0x861a0/0x27a) | ⬜ | |
| 3  | 0x8086cdc..0x8087d58 | 19 | ~151 | 0 inc (heavy; 可拆 3a/3b) | ⬜ | |
| 4  | 0x8087d58..0x808d7f4 | ~197 | 0 (1 巨块) | **1 inc 0x87d58/0x5a9c = 未反汇编 THUMB 代码** (拆 4a..4g) | ⬜ | |
| 5  | 0x808d7f4..0x808e8fc | 18 | ~105 | 0 inc | ⬜ | |
| 6  | 0x808e8fc..0x808f7c0 | 19 | ~97  | 0 inc | ⬜ | |
| 7  | 0x808f7c0..0x8090a78 | 32 | ~117 | 0 inc | ⬜ | |
| 8  | 0x8090a78..0x8091888 | 3  | ~74  | 0 inc (build_equip_candidate_score_table 数据密集) | ⬜ | |
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
- **commit**: (see §三)

---

## 五、Seg 路线图 (地址序, 边界 = 函数结束处)

按 push-prologue 检测函数入口, 地址序均分; 巨块 0x87d58 独占 Seg-4 (拆子段)。

### region A (0x80850d8..0x8087d58, 41 命名 fn, 342 槽, 3 小 incbin)

- **Seg-1** `[0x80850d8, 0x8085d4c)` -- 10 fn (enqueue_effect_slot_attr_from_bb .. build_field_action_text_by_zone_type)
  - incbin: 0x850f0/0x28, 0x85130/0x14c (疑 fn-ptr / dispatch 表; ref-scan 待执行)
  - 重函数: scan_equip_target_slots_for_card (48 槽)
- **Seg-2** `[0x8085d4c, 0x8086cdc)` -- 12 fn (dispatch_field_display_state_by_type .. check_neo_daedalus_equip_zone_eligible)
  - incbin: 0x861a0/0x27a (疑 dispatch_equip_slot_state_by_index 跳转表)
  - 重函数: dispatch_field_display_state_by_type (32 槽)
- **Seg-3** `[0x8086cdc, 0x8087d58)` -- 19 fn (dispatch_equip_zone_activation_state .. scan_zone_opponent_field5_substate_e)
  - 0 incbin; 重函数: dispatch_equip_zone_activation_state (37 槽) + write_equip_zone_entries_by_lv_card_id (49 槽)
  - **heavy (~151 槽), 执行时可拆 3a/3b**

### region B (0x8087d58..0x808d7f4, ~197 未命名 THUMB fn, 巨块)

- **Seg-4** `[0x8087d58, 0x808d7f4)` -- ROM_INCBIN 0x87d58/0x5a9c (23,196 B) = 未反汇编 THUMB 代码区
  - **拆 Seg-4a..4g** (~28-30 fn/子段, 地址序): 逐 fn R4 disasm + createFunction + 命名 + CSV row
  - 入口: ~197 distinct THUMB+1 fn-ptr 目标 (引用来自全 ROM card effect handler dispatch table)
  - 含 61 even-addr 引用 (jump-table 裸指针 / data ref, 据实判定)

### region C (0x808d7f4..0x80941c4, 101 命名 fn, 710 槽, 0 incbin)

- **Seg-5** `[0x808d7f4, 0x808e8fc)` -- 18 fn (dispatch_equip_zone_write_by_substate_range .. scan_all_zone_slots_for_lp_change_indicator)
  - 重函数: scan_all_slots_for_max_equip_match (24 槽)
- **Seg-6** `[0x808e8fc, 0x808f7c0)` -- 19 fn (enqueue_paired_slot_sprite_attrs_for_player .. enqueue_sprite_by_field_copy_count)
- **Seg-7** `[0x808f7c0, 0x8090a78)` -- 32 fn (scan_field_slots_for_equip_chain_node_bitmap_update .. scan_equip_chain_nodes_for_bitmap_update)
  - 多小 invoke_*/check_* effect-node 包装函数 (零槽); 重函数 dispatch_equip_field_scan_sequence (16 槽)
- **Seg-8** `[0x8090a78, 0x8091888)` -- 3 fn (build_equip_candidate_score_table + invoke_ + write_equip_target_score_entry)
  - build_equip_candidate_score_table (63 槽, 0xc48 B 数据密集)
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
