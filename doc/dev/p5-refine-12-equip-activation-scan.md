# 函数/数据细化计划 -- `asm/12_equip_activation_scan.s`

> 阶段目标: 把 `asm/12_equip_activation_scan.s` (ROM `0x080941c4 ~ 0x0809d718`, 效果 slot 显示上下文 +
> 装备发动链阻断 + 手牌/怪兽区扫描发动) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **13** 个文件 (file 00..11 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

> **模块收尾结果**: 2026-09-01，用户明确授权的 `F12-Historical-Closure` 已完成第二轮PASS、事务写回、保存后只读核验和主线程四项独立验收。模块12自动数据标签、旧自动名注释、`.byte` 残留均为0；仅保留§5.1所列四块无有效引用数据，共134字节。ROM全字节一致，本轮进入提交收束。历史预检与本次闭合记录见 `doc/dev/refine/F12-legacy-seg2-residue.md` 和§4.11；模块13当前进度见对应活动文档。

---

## 一、细化要求 (checklist)

沿用 file 00..11 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用->§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一 + file 06..11 新增。

**跨文件踩坑沿用** (file 00..11 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **ROM_INCBIN 分类核心**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - 有引用 + THUMB opcode 形态 (push 前导 / 局部分支落点 / fall-through 续接) -> R4 disasm。
  - 有引用 + 数据 (指针表/掩码/字符串) -> R7 carve 进 rom.s。
  - raw=0 且 THUMB+1=0 且非 fall-through/局部分支落点 -> §5.1 登记。
- **R4 disasm 范式**: clearListing 整 range -> setTMode THUMB -> **逐 stub/逐 fn per-block** DisassembleCommand;
  literal pool createDWord 强制 split; **每 sub-fn / 每 case-block 单独 DisassembleCommand** (单次整 range 在首 `b`/`bx` 停);
  段后 ROM_INCBIN/.byte-code grep == 0 独立验收 (memory `feedback_refine_partial_disasm_residue_gate`)。
- **机器码核 (必做)**: disasm fn 比较+分支指令独立解码; 函数名运算符/偏移/卡名与机器码一致;
  **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核 (按 VALUE grep 不按 NAME)**: 标 new CID 逐一按值 grep 0 命中; 标 reuse 逐一按值 grep 确存在
  (memory `feedback_c5_dedup_grep_by_value_not_name`)。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集。
  **+ disasm 落地后独立 grep**: disasm 创建的 pool label (createDWord) 在 proposal 写完后才出现, 逃过 per-seg C13
  -> 段落地后须独立 `grep "^DAT_\|^DWORD_" asm/12` 清残 (memory `project_file11_giant_incbin_hidden_handlers` 教训)。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实; 未分配->中性 `cid_<hex>`, 勿臆造。
- **误名警觉**: 函数名/plate 称的卡名/全局与函数体矛盾即误名信号; 走 FUNC_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 落地后 grep == 0
  (memory `feedback_refine_plate_subst_silent_noop`: WARN not-found 当 FAIL)。
- **executor 不自撰 review.md** (reviewer 独立职责; memory `feedback_refine_fixer_overstep_self_review`)。

**⚠ file 12 特征**:
- **6 个 ROM_INCBIN 小块 (合计 344 B), 全部 = 误标 THUMB 代码** (ref-scan + 字节形态确认), 集中在 Seg-1/2/4:
  - `0x9437c/0x1c` (Seg-1): THUMB helper, 结尾 `7047`=bx lr + pool word `0201e4f0`(gEffectDisplayCtx)。raw=0/thumb+1=0 -> 疑 fall-through 续接, 据消费者确认。
  - `0x943e8/0x12` (Seg-1): switch case 派发块 `0226 06e0 0426 04e0...`(movs r6,#N; b)。raw=1 -> R4 disasm。
  - `0x94c3e/0x22` (Seg-1): THUMB helper, 结尾 `7047` + pool `0201c4e0` (gP1LifePoints; 预览表 `0201e4d4` 为笔误，ROM 字节 reviewer 已纠正)。raw=0 -> §5.1 登记。
  - `0x95274/0xc0` (Seg-2): **10 case blocks** (asm 行内注释明确; `dispatch_equip_confirm_phase_by_step` 的 switch 体)。raw=2 -> R4 disasm。
  - `0x95b28/0x14` (Seg-2): THUMB helper, 结尾 `7047` + pool `0201c4e0`。raw=0 -> 据消费者确认。
  - `0x96eec/0x34` (Seg-4): THUMB helper, 结尾 `7047` + pools `0201c4e0/1d4c/1d54`。初始分类曾按raw=1列为R4 disasm；已由§5.1复核订正为raw=1/effective=0（未压缩6bpp卡图像素巧合），原ROM_INCBIN保留，未反汇编。
  - 与 file 11 不同: **无隐藏 fn-ptr-table dispatch 巨块**, 144 fn 全部已命名 (无 disasm+命名作业, 仅小块 disasm)。
- **本文件主体 = slot 符号化** (~1183 DAT_/DWORD_/PTR_ 槽) + plate 订正; **无大数据表 carve** (初判)。
- Seg-8 = 巨型主函数 `eval_equip_slot_pair_eligibility` (0x0809a1a4) + 2既有共享收尾，实测131槽；Seg-9 实测7 fn/157槽（134 DAT + 23 PTR）；
  Seg-10 = 55 个小型 scan 回调 (`scan_*_zone_*_for_equip_activation_by_*`, 低槽密度, 必要时拆 10a/10b)。
- 域: 效果 slot 显示上下文 (gEffectDisplayCtx=0x0201e4f0) + 装备发动确认相位机 + LP bar 动画 +
  装备目标资格判定 + 怪兽/魔陷/装备区逐 slot 扫描发动。

**file 02..11 已建可复用资产** (新建前必 grep): card_info.inc ~700+ CID / ewram.inc / iwram.inc /
duel_field.inc / oam_attr.inc / gfx_resource.inc / g2d_tags.inc / equip_lp_delta.inc 等。

---

## 二、落地工作流 (pipeline)

同 file 00..11 doc §二:
```
备份 .rep -> Ghidra 脚本 (RefineF12Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
-> ghidra-export-range.bat 080000c0 084c7637 -> inject_modes.py -> split_all_s.py
-> build + byte-identical SHA1 9689337d -> (改/建函数名才) ExportFunctionInventory + sync CSV -> commit
```
3-agent: executor -> reviewer (C1-C13) -> fixer (模式A改proposal / 模式B落地)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (12_equip_activation_scan.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------|------|--------|
| 1  | 0x80941c4..0x8094f20 | 19 | 113 | 3 inc (0x9437c/0x1c, 0x943e8/0x12, 0x94c3e/0x22) | ✅ | 537cb5f |
| 2  | 0x8094f20..0x8095ba8 | 15 | 109 | 2 inc (0x95274/0xc0, 0x95b28/0x14) | ✅ | aa46235 |
| 3  | 0x8095ba8..0x8096a4c | 18 | 116 | 0 inc | ✅ | ee05202 |
| 4  | 0x8096a4c..0x8097828 | 24 | 109 | 1 inc (0x96eec/0x34) | ✅ | aa2ff4e |
| 5  | 0x8097828..0x80984d0 | 5  | 118 | 0 inc | ✅ | f594243 |
| 6  | 0x80984d0..0x8099314 | 3+1 共享收尾 | 126 | 0 inc | ✅ 2026-08-31 | 本轮提交收束 |
| 7  | 0x8099314..0x809a1a4 | 3  | 135 | 0 inc | ✅ 2026-08-31 | 本轮提交收束 |
| 8  | 0x809a1a4..0x809b178 | 1+2 共享收尾 | 131 | 0 inc (eval_equip_slot_pair_eligibility 巨型主函数) | ✅ 2026-08-31 | 本轮提交收束 |
| 9  | 0x809b178..0x809c3d8 | 7  | 157 | 0 inc | ✅ 已完成 | 第三轮PASS；104EQ/32REF/21RENAME/7PLATE/26EOL；本轮提交收束 |
| 10 | 0x809c3d8..0x809d718 | 55 | 136 | 0 inc (55 小型 scan 回调，整段处理) | ✅ 2026-09-01；本段验收通过 | 本轮提交收束 |
| 历史补漏 | 模块12内按涉及地址递增 | 19原函数 | 8（7自动槽+1既有依赖槽） | 四§5.1块134 B保留；1个8 B裸块解码 | ✅ 2026-09-01；全模块验收通过 | 本轮提交收束 |

**初始测绘总计**: 144 命名 fn / ~1183 DAT_/DWORD_/PTR_ 槽 / 6 ROM_INCBIN (合计 344 B)。初计存在PTR槽漏计，完成段以逐段实测为准；裸块最终分类以各段评审及§5.1为准。
**重段提示**: Seg-8 (131槽，1主函数+2共享收尾) / Seg-9 (实测157槽) / Seg-10 (55 fn) 较重。保留 Seg-1/2/4 的旧完成记录与commit；后续模块预检发现的 Seg-2 七槽、`0x080952fc` 8字节块及20行旧注释，已在用户授权的 `F12-Historical-Closure` 中闭合。当前模块清零结论以§4.11的全模块验收为准，四个§5.1保留块不计为未处理残留。

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录 [0x080941c4, 0x08094f20)

- **EQ**: 111 槽 (87 DAT_ + 24 DWORD_ — 含 2 DWORD_ gP1LifePoints 从 REF 归正为 EQ)
- **REF**: 1 槽 (0x080943cc -> zone_type_jump_table @ 0x080943d0)
- **RENAME**: 13 槽 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- **PLATE**: 2 (get_effect_slot_entry_ptr L174 + get_activation_zone_card_type_field L212 CJK->ASCII)
- **Block2 disasm**: 0x080943e8/0x12, 5 case blocks 逐块 DisassembleCommand (clearListing+setTMode+5×DC), no createFunction
- **Block1/Block3**: §5.1 登记，ROM_INCBIN 原样保留，无 Ghidra 操作
- **新增常量**:
  - ewram.inc: CARD_PLAY_PHASE_CTR_OFF(0x1d1c) / DUEL_TURN_STATE_OFF(0x1d14) / ZONE_SLOT_ATTR_BIT12_CLEAR_MASK(0xffffefff) / EQUIP_PHASE_FN_TABLE_ROM(0x9e5aac0) / DUEL_TURN_FN_TABLE_ROM(0x9e5aadc)
  - duel_field.inc: SPRITE_ATTR_DUEL_PHASE_P2(0x800b) / SPRITE_ATTR_DUEL_PHASE_P2_B(0x8023) / SPRITE_ATTR_SPELL_8006 / SPRITE_ATTR_TRAP_8007 / SPRITE_ATTR_MONSTER_8008(域异 CARD_DESC_RENDER_PARAM) / SPRITE_ATTR_ALT_8005 / UNINIT_GUARD_FFFF(0xffff, 5-hit 域异)
  - constants/prng.inc (新建): LCG_MUL_343FD(0x343fd) / LCG_INC_269EC3(0x269ec3)
  - rom.s: `.include "constants/prng.inc"` 追加
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Gates**:
  - Gate1: DAT_/DWORD_ 残留 Seg-1 范围 [0x080941c4, 0x08094f20) = 0 ✅
  - Gate2: Block2 ROM_INCBIN/.byte [0x080943e8, 0x080943fa) = 0 ✅
  - Gate3: Seg-1 非 ASCII (除 L2 文件头) = 0 ✅
- **CSV sync**: 不需要 (无新建/改名函数)
- **§5.1**: Block1(0x9437c/0x1c) + Block3(0x94c3e/0x22) 两行登记
- **commit**: 537cb5f

---

### 4.02 Seg-2 完成记录 [0x08094f20, 0x08095ba8)

- **EQ**: 103 槽 (99 DAT_ + 4 DWORD_ 非gP1LP，含 Block1 disasm 后新增 1 池槽 ELIGIB_CARD_ID_OFF@0x952ec)
- **REF**: 2 槽 (0x08095248->equip_confirm_case_jump_table@0x0809524c + **Fix#2** 0x08095550->switchD_0809554c__switchdataD_08095554@0x08095554)
- **RENAME**: 21 槽 (12 gp1lp_ptr_* 含 **Fix#1** 0x0809552c + 3 DWORD_gP1LP + 7 DWORD_off)
- **PLATE**: 6 (6 stale FUN_ 全部替换，0 FAIL)
- **Block1 disasm**: 0x08095274/0xc0, clearListing+setTMode+9 unique case DisassembleCommand + 2 sub-stubs (0x952d4/0x952f0); 6 pool createDWord; no createFunction; Post-check ROM_INCBIN/.byte == 0 ✅
- **Block2**: §5.1 登记，ROM_INCBIN 原样保留，无 Ghidra 操作
- **新增常量**:
  - ewram.inc: LP_EQUIP_STATE_B_OFF(0x1d50) / LP_DISPLAY_STATE_OFF(0x1d0c) / LP_PLAYER_SIDE_CACHE_OFF(0x1d64) / LP_EQUIP_DISPLAY_FLAG_OFF(0x1d84) / LP_ACTIVATION_TYPE_ARRAY_BASE_OFF(0x10e1) / SPRITE_ROW_BUSY_BYTE_OFF(0x301) / SPRITE_ROW_ENTRY_30D_OFF(0x30d) / SPRITE_ROW_ENTRY_30E_OFF(0x30e) / SPRITE_ROW_ENTRY_30F_OFF(0x30f) / SPRITE_ATTR_BYTE_2FE_OFF(0x2fe) / SPRITE_ATTR_BYTE_2FF_OFF(0x2ff) / gSpriteAttrBufData(0x0201b872)
  - duel_field.inc: SPRITE_HIGH_HALF_MASK(0xffff0000, domain-distinct EQUIP_CHAIN_SENTINEL) / SPRITE_LOW_HALF_MASK(0xffff, domain-distinct x6) / SPRITE_ROW_BITS18_15_CLEAR_MASK(0xfff87fff) / SPRITE_ROW_DISPATCH_TABLE(0x080953dc)
  - card_info.inc: NEGATE_ATTACK_CID(0x12c4)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Gates**:
  - Gate1: DAT_/DWORD_/PTR_ 残留 Seg-2 范围 [0x08094f20, 0x08095ba8) = 0 ✅
  - Gate2: Block1 ROM_INCBIN/.byte [0x08095274, 0x08095334) = 0 ✅
  - Gate3: Seg-2 非 ASCII = 0 ✅
  - Gate4: Stale FUN_ 在 Seg-2 范围 = 0 ✅
- **NEEDS_FIX 修复确认**: Fix#1 (PTR_gP1LifePoints_0809552c 补入 RENAME → gp1lp_ptr_9552c) ✅; Fix#2 (DAT_08095550 REF -> switchD dispatch table) ✅; Fix#3 (Block1 标题描述更正) ✅
- **CSV sync**: 不需要 (无新建/改名函数)
- **§5.1**: Block2(0x95b28/0x14) 一行登记
- **commit**: aa46235

---

### 4.03 Seg-3 完成记录 [0x08095ba8, 0x08096a4c)

- **EQ**: 116 槽 (全部 DAT_ 槽; 8 新常量首现)
- **REF**: 0
- **RENAME**: 28 槽 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- **PLATE**: 8 操作 (4 CJK 全重写 + 4 substring FUN_ 替换)
  - 4 full rewrites: setup_equip_slot_activation_entry / _alt / eval_zone_activation_flags_by_type / dispatch_zone_effect_by_slot
  - 4 substring: FUN_0804ce78 x3 (L3561/3690/3814) + FUN_08097bec/FUN_08098020 x1 (L5499)
- **新增常量**:
  - duel_field.inc: ZONE_EVAL_PHASE_CODE_OFF(0x1bd4) / ZONE_PHASE_STATUS_OFF(0x1c58) / ACTIVATION_ENTRY_CLR_BITS_11_6(0xfffff03f) / ACTIVATION_ENTRY_CLR_BITS_14_6(0xffff803f) / ACTIVATION_ENTRY_PTR_OFF(0x1d7c)
  - ewram.inc: LP_ANIM_RESULT_OFF(0x1d74) / LP_ANIM_TRIGGER_SENTINEL(0x0fee, domain-distinct COCOON_OF_EVOLUTION_CID) / EFFECT_ID_GENERIC_WILDCARD(0x0000fffe)
- **NEEDS_FIX 修复确认**: Fix#1 (L3561 FUN_0804ce78 补入 PLATE substring -> dispatch_card_eligibility_state_machine) ✅; Fix#2 (两板精简: 0x0809650c=494 chars/0x0809678c=448 chars, both <=500, pure ASCII) ✅
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Gates**:
  - Gate1: DAT_/DWORD_/PTR_ 残留 Seg-3 范围 [0x08095ba8, 0x08096a4c) = 0 ✅
  - Gate2: Seg-3 非 ASCII = 0 ✅
  - Gate3: Stale FUN_[0-9a-f]{8} in Seg-3 = 0 ✅
  - Gate4: 精简板 char count <= 500 (494/448) ✅
- **CSV sync**: 不需要 (无新建/改名函数)
- **§5.1**: 本段无 ROM_INCBIN, 无新增登记
- **commit**: ee05202

---

### 4.04 Seg-4 完成记录 [0x08096a4c, 0x08097828)

- **EQ**: 107 槽 (95 DAT_ + 14 DWORD_ → 104 in main script + 3 remediation = 107 unique slots)
- **REF**: 2 槽 (0x08096b78 -> switchD_08096b6a__switchdataD_08096b7c + 0x08096bf4 -> switchD_08096bf2__switchdataD_08096bf8)
- **RENAME**: 15 槽 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- **FUNC_RENAME**: 4 (SUB_080970d0->get_equip_handler_table_entry_count / SUB_080970d4->get_equip_handler_card_type / SUB_080970e4->check_equip_handler_uses_fixed_activation / SUB_08097104->get_equip_handler_table_entry_param; createFunction fallback used for all 4 stub fns)
- **PLATE**: 15 操作 (4 full ASCII rewrites: dispatch_zone_activation_by_state/check_equip_effect_zone_preconditions/check_equip_zone_has_frozen_soul_or_great_long_nose/enqueue_frozen_soul_zone_sprite_or_default; 11 FUN_ substring replacements; all <=500 chars)
- **ROM_INCBIN**: 0x96eec/0x34 §5.1 登记; orphan THUMB leaf; effective raw=0/thumb+1=0; ROM_INCBIN preserved
- **Remediation**: 3 slots missed by main script (DWORD_08097110 equate + DAT_080972d0 P2LP_BLOCK2 + DAT_08097664 EARTHBOUND_INVITATION); added RefineF12Seg4Remediate.py
- **新增常量**:
  - duel_field.inc: EQUIP_CHAIN_CANCEL_OFF(0x1d30) / EQUIP_ACTIVATION_HANDLER_TABLE(0x09e47560) / APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB(0x08097025)
  - card_info.inc: FROZEN_SOUL_CID(0x16a1) / GREAT_LONG_NOSE_CID(0x1502) / DD_BORDERLINE_CID(0x16d4) / EARTHBOUND_INVITATION_CID(0x177a)
  - oam_attr.inc: OAM_EQUIP_ZONE_SPRITE_P2_18(0x8018) / OAM_EQUIP_ZONE_SPRITE_P2_0F(0x800f)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Gates**:
  - Gate1: DAT_/DWORD_/PTR_ 残留 Seg-4 范围 [0x08096a4c, 0x08097828) = 0 ✅
  - Gate2: SUB_080970d0/d4/e4/8097104 残留 = 0 ✅
  - Gate3: Seg-4 非 ASCII = 0 ✅
  - Gate4: ROM_INCBIN 0x96eec/0x34 原样保留 ✅
- **CSV sync**: 需要 (4 SUB_ 新函数加入 naming-proposals.csv; get_equip_handler_table_entry_count/card_type/uses_fixed/entry_param)
- **§5.1**: 0x96eec(0x34) 一行登记
- **commit**: aa2ff4e

---

### 4.05 Seg-5 完成记录 [0x08097828, 0x080984d0)

- **EQ**: 115 槽 (含 Fix#1 补入 DAT_080979bc → eqchain_act_79bc = EQUIP_CHAIN_ACTIVE_OFF)
- **REF**: 6 槽 (2 switchD 表基址 slot_label 全小写 Fix#2 + 4 THUMB fn-ptr)
- **RENAME**: 31 槽 (PTR_gP1LifePoints_* -> gp1lp_ptr_*)
- **FUNC_RENAME**: 0
- **PLATE**: 5 操作 (3 full rewrites + 2 trims; 全 ASCII <=500 chars; FUN_0809be70 -> advance_equip_display_phase_via_table 替换)
- **carve**: 0 / **disasm**: 0 / **§5.1**: 0 (Seg-5 无 ROM_INCBIN)
- **新增常量**:
  - oam_attr.inc: OAM_EQUIP_SPRITE_P2_15(0x8015)
  - card_info.inc: JIRAI_GUMO_CID(0x1115) / PATRICIAN_OF_DARKNESS_CID(0x139c)
- **NEEDS_FIX 修复确认**: Fix#1 (DAT_080979bc 补入 Group A → eqchain_act_79bc) ✅; Fix#2 (switchdataD_97860/c68 → switchdata_ptr_97860/c68 全小写) ✅
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- **Gates**:
  - Gate1: DAT_/DWORD_/PTR_ 残留 Seg-5 范围 [0x08097828, 0x080984d0) = 0 ✅
  - Gate2: Seg-5 非 ASCII (L7435..9119) = 0 ✅
  - Gate3: switchdata_ptr_97860/c68 (全小写) 各 2 命中, stale uppercase D = 0 ✅
  - Gate4: eqchain_act_79bc = 2 命中, stale DAT_080979bc = 0 ✅
- **CSV sync**: 不需要 (0 新建/改名函数)
- **commit**: f594243

---

### 4.06 Seg-6 完成记录 [0x080984d0, 0x08099314)

- **完成日期**: 2026-08-31；第二轮独立 review 为 PASS；提案 SHA256 `93f23b649fb8608e14278e60094b7c4dda05a8ed85812cbc61441b64644ee9a5`。
- **脚本**: `tools/ghidra-labeling/RefineF12Seg6Slots.py`；支持 dry/apply/check，写入前全量 preflight，写入事务内执行逐项 postcheck。
- **实写计数**: EQ=80、REF=39（RAM 38 + switch 1）、RENAME=7，共126槽；PLATE=4、辅助 DATA/USER_DEFINED 引用=1、EOL=8（7个 RENAME + 1个回调）。FUNC_RENAME=0。
- **回调**: `0x080987bc` 用 `CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB=0x0804b165`；辅助引用指向 `0x0804b164`，保留 `check_card_id_is_normal_summon_type` 的 FUNCTION 主符号，未在奇地址创建标签或函数。正式导出 `.word CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB`，ROM 字节为 `65 b1 04 08`。
- **新增定义**: card_info.inc 16个常量、duel_field.inc 5个常量、ewram.inc 1个常量 + `gEquipSlotActivationSnapshot` RAM 全局；总计22常量+1全局。沿用既有 include，无 rom.s 修改。
- **PLATE**: 三个主入口和共享返回尾均整段 ASCII 重写，长度379/464/459/334字符。订正 player_side 输入、状态字段基址、显示阶段和共享栈帧说明。
- **备份与执行留痕**: 初始预备份 `ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260831-195651-pre-F12Seg6` 已保留；通用 wrapper 的 dry 会 Save，未执行语义写入但数据库存储文件发生变化，因此另建后续备份。最终实写前备份为 `ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260831-203114-pre-F12Seg6-apply2`，15个文件逐一哈希核对相同，见运行目录 `seg6-apply2-backup.json`。
- **引用 API 修正**: 首次实写后检查捕获 `0x0809859c` 的既有同目标 DEFAULT 引用未被 addMemoryReference 提升来源；事务回滚后只读确认126个旧主标签、80个空 equate 槽全部恢复。脚本改为精确重建 operand0 的 DATA/USER_DEFINED 引用，保留严格 postcheck。第二次 dry/apply 和保存后的只读 check 均零 FAIL；分别见 `seg6-dry2.log`、`seg6-apply2.log`、`seg6-persisted-check.log`。
- **完整 pipeline**: 全量 `080000c0..084c7637` 重导 -> 剥离独立 .arm/.thumb -> inject_modes -> split_all_s -> build（NOPAUSE=1）。基线49步资源导出已由主线程完成；本轮构建仅出现基线已有的 r13 警告。
- **byte-identical**: ROM 逐字节一致；SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。
- **Gates**: 126槽标签/实际 .word 表达式/值全部一致；段内 DAT_/DWORD_/PTR_/UNK_/FUN_ 残留=0；ROM_INCBIN/.byte=0；段文本和新增注释均 ASCII，PLATE均≤500字符；五项 switch 目标保留偶地址；机器码地址/字节注记全部不变。结果见 `output/refine-run-20260831-194634/seg6-landing-gates.json`，主线程另以 proposal、ELF 和正式 asm 独立核验通过，见 `root-seg6-verification.json`。
- **变更范围**: 25个模块仅 `asm/12_equip_activation_scan.s` 有文本变化，全部在本段内；段外自然 xref 导出变化=0。沿用既有 CRLF，未扩大换行变更。
- **carve/disasm/§5.1**: 均为0；本段没有裸数据块，既有§5.1登记不变。**CSV sync**: 无新建或改名函数，无需同步。
- **提交状态**: 已完成、未 stage、未 commit。**下一段**: Seg-7 `[0x08099314,0x0809a1a4)`，按地址序继续。

---

### 4.07 Seg-7 完成记录 [0x08099314, 0x0809a1a4)

- **完成日期**: 2026-08-31；独立 review 为 PASS，C6/C7 标签实施补核后保持 PASS；提案 SHA256 `5463ac0f317237ce2af3e3c998a0bceb2f31af53e2179253a8e540d18e0df51d` 未变。
- **脚本**: `tools/ghidra-labeling/RefineF12Seg7Slots.py`；执行表直接提取自 PASS 提案，并与 executor 元数据逐项对照。沿用只读 dry、写入事务内 postcheck、保存后只读 check。
- **实写计数**: EQ=96、REF=27（RAM 26 + switch 1）、RENAME=12，共135槽；PLATE=3、EOL=12；FUNC_RENAME=0。
- **新增定义**: card_info.inc 14个常量、oam_attr.inc 5个常量、duel_field.inc 3个常量、ewram.inc 新全局 `gDuelEquipCtxSlotIndex=0x0201bbc0`；总计22常量+1 RAM 全局。沿用既有 include，无 rom.s 修改。
- **REF 与 switch**: 精确重建同目标 operand0 的 DATA/USER_DEFINED 引用，保留其他 operand 与非目标引用，并检查 from/to/operand/type/source/primary。表 `0x08099370` 复用既有 Symbol 对象，通过 namespace/name 的规范化得到既有 GAS 名 `switchD_0809935c__switchdataD_08099370`，再确认 USER_DEFINED 主符号；没有新建同址 switch 标签或操作内部 case 标签。对象复用依据脚本受限 API 路径，正式 asm 验证 case 标签和11项表值均不变；第7/8/9项继续共用 `0x08099a98`，全部保持 MOV pc 所需偶地址。
- **PLATE**: 三个函数入口整段 ASCII 重写，长度459/469/477字符；明确0x38字节上下文与0x14字节 activation record 的区分，订正输入、返回值、相位和 LP 基址说明。未改相邻段 plate。
- **备份**: `ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260831-204112-pre-F12Seg7`，15文件逐一哈希一致；只读 dry 后再次核验备份与源相同。Seg-6 已验证的 asm/constants/output 前态保存在运行目录 `pre-seg7/`。
- **运行验收**: `seg7-dry.log`、`seg7-apply.log`、`seg7-persisted-check.log` 均含精确成功状态与零 FAIL；实写保存成功。无失败事务或数据库回滚。
- **完整 pipeline**: 全量 `080000c0..084c7637` 重导 -> 剥离独立 .arm/.thumb -> inject_modes -> split_all_s -> build（NOPAUSE=1）；使用已完成49步资源重导的基线，仅出现已有 r13 汇编警告。
- **byte-identical**: ROM 逐字节一致；SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。
- **Gates**: 全135槽标签/实际 .word 表达式/值一致，23定义与 PASS 提案一致；段内 DAT_/DWORD_/PTR_/UNK_/FUN_ 残留=0、ROM_INCBIN/.byte=0；段文本及新增注释为 ASCII，PLATE均≤500字符。25模块的机器码地址/字节注记全部不变；仅 asm/12 有文本变化，全部位于本段内，段外自然 xref 导出变化=0。结果见 `output/refine-run-20260831-194634/seg7-landing-gates.json`；主线程另以 proposal、正式 asm、ELF 与 ROM 独立验收通过，见 `root-seg7-verification.json`。
- **carve/disasm/§5.1**: 均为0；既有§5.1登记不变。**CSV sync**: 无新建或改名函数，无需同步。
- **提交状态**: 已完成、未 stage、未 commit，保留 Seg-6 和主线程基线修复。**下一段**: Seg-8 `[0x0809a1a4,0x0809b178)`，按地址序继续。

---

### 4.08 Seg-8 完成记录 [0x0809a1a4, 0x0809b178)

- **完成日期**: 2026-08-31；首轮独立 review PASS；最终提案 SHA256 `2606ce4d5862f3f2e02171a2e22acb7ca869a56e568158a859013f5690307229` 未变。
- **脚本与计数**: `tools/ghidra-labeling/RefineF12Seg8Slots.py`，执行表直接提取自最终 PASS 提案并与元数据逐项对照。实写 EQ=95、REF=33（全部 RAM）、RENAME=3，共131槽；PLATE=3、EOL=3、FUNC_RENAME=0。只读 dry、事务内 postcheck、保存后的只读 check 全部零 FAIL，见运行目录 `seg8-dry.log`、`seg8-apply.log`、`seg8-persisted-check.log`。
- **新增定义**: card_info.inc 9个常量、duel_field.inc 1个常量 `EQUIP_ACTIVATION_PACKED_TYPE22`、ewram.inc 新全局 `gDuelEffectChainSlotsSecond=0x0201bc68`；总计10常量+1 RAM 全局，均与提案一致，沿用现有 include。
- **边界与复用**: 中性 ID 使用 `equip_pair_cid_13b0`，正式两槽 `0x0809a408/0x0809a5fc` 按该名导出，未动旧 `cid_13b0` ROM 池标签。`0x0809aaf8/0x0809aec4` 复用 `NODE_POOL_NEG_OFFSET`，保留值 `0xffffeb50` / -0x14b0，与 node_pool_base 分槽；`0x1cfc` 复用 `EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF`。
- **REF 与 PLATE**: 精确重建同目标 operand0 的 DATA/USER_DEFINED 引用，保留其他引用，严格检查目标 LABEL 主符号及 from/to/operand/type/source/primary。主入口和两个既有共享尾的 plate 全部 ASCII，长度481/393/354字符；共享尾仅改 plate，未改函数边界、寄存器或栈行为。段内无 switch 或 callback 槽。
- **备份**: `ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260831-212326-pre-F12Seg8` 的15个文件与源逐一哈希一致，dry后再次确认一致；运行目录 `pre-f12-seg-8/` 的49份 asm/constants/ROM/ELF 快照也已核验。无失败事务或回滚。
- **完整 pipeline**: 全量 `080000c0..084c7637` 重导 -> 剥离独立 .arm/.thumb -> inject_modes -> split_all_s -> build（NOPAUSE=1），沿用此前完整49步资源导出的基线；只出现既有 r13 汇编警告。
- **byte-identical**: ROM 逐字节一致；SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。
- **Gates**: 全131槽标签/实际 .word 表达式/值一致；11定义一致；段内 DAT_/DWORD_/PTR_/UNK_/FUN_ 残留=0、ROM_INCBIN/.byte=0；段文本与新增注释均 ASCII，PLATE均≤500字符。25模块机器码地址/字节注记不变；相对本段前快照仅 asm/12 有文本变化，全部在 Seg-8 内，段外自然 xref 导出变化=0。详见 `output/refine-run-20260831-194634/seg8-landing-gates.json`；主线程独立 proposal/asm/ELF/ROM 验收也通过，见 `root-seg8-verification.json`。
- **carve/disasm/§5.1**: 均为0；无 rom.s 修改，既有§5.1登记不变。**CSV sync**: 无新建或改名函数，无需同步。
- **提交状态**: 已验证、未 stage、未 commit，保留 Seg-6/7 和主线程基线修复。**下一段**: Seg-9 `[0x0809b178,0x0809c3d8)`，按地址序继续。

---

### 4.09 Seg-9 完成记录 [0x0809b178, 0x0809c3d8)

- **完成日期与提案**: 2026-08-31；第三轮正式 review PASS，最终提案 SHA256 `9c3892c87c14f6de87fa0a001d90d373f24a3a070e176d2107f31a23cf80265b`。前两项修订分别纠正 CID 证据行号、区分引用 DEFAULT 与目标 LABEL USER_DEFINED；完整历史及首次只读 dry 的22项失败记录保留。首次 dry 未进入实写。
- **脚本与计数**: `tools/ghidra-labeling/RefineF12Seg9Slots.py` 从最终提案提取执行表。实写 EQ=104、REF=32、RENAME=21，共157槽；PLATE=7、EOL=26（21条 RENAME +5条附加说明），FUNC_RENAME=0。主线程独立脚本表核验通过，见 `root-seg9-script-table-check-final.json`。
- **新增定义**: 现有 card_info.inc 追加9常量、duel_field.inc 追加2常量、oam_attr.inc 追加1常量；ewram.inc 追加 RAM 全局 `gEquipChainActivePhase=0x0201e20c` 和 ROM 表基址绝对 equate `equip_display_step_fn_table=0x09e5aaec`，合计14定义。54项复用不变，无新 include 或 rom.s 修改。
- **RENAME 与 REF**: 21条 RENAME 严格保留到 `gP1LifePoints` 的唯一 operand0 DATA/DEFAULT 主引用，目标仍为 LABEL/USER_DEFINED；apply仅改池名及EOL，所有引用的 from/to/operand/type/source/primary 前后完整相等。32条 REF 精确重建同目标 operand0 DATA/USER_DEFINED 主引用，保留其他 operand 和非目标引用，实际按提案名字导出。
- **两张 switch**: `0x0809b814` 的 Symbol ID7217 与 `0x0809c038` 的 ID7144 在 pre/post/persisted 中保持不变；复用原对象规范 namespace/name 为既有 GAS 全名，再设 USER_DEFINED 主 LABEL。没有新增同址 switch 标签或改内部 case；17项值、两个 MOV pc 编码及 Thumb 偶地址目标不变。
- **段外函数表**: 仅将 `0x09e5aaec` 表 base 建为 USER_DEFINED 数据 LABEL，并设置本段 `0x0809bea4` 的引用。14个奇函数指针及NULL原值不变；整个60字节范围的14个 Data 定义（地址/长度/类型/范围）、14个 outgoing 引用和1个其他 incoming 引用，在 dry/apply/persisted 五次观测中完全相等。`0x09e5ab24` 继续 `definedData=None`，没有新增Data、disasm或carve。
- **PLATE 与边界**: 七条 ASCII plate 长448/466/402/395/436/371/464字符；21条 RENAME EOL与5条附加EOL均为最终提案原文。七函数名称、body和内部返回块边界不变。旧 `0x0809bebc` plate 由7行改1行，`0x0809bf60/0x0809bfd4` 各由2行改1行，因此模块文本少8行，所有机器码地址和字节注记不变。
- **备份与执行**: `ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260831-215843-pre-F12Seg9` 的15文件及运行目录 `pre-f12-seg-9/` 的49份 asm/constants/ROM/ELF 快照，在最终只读 dry 后、实写前逐项复验一致。活动文档前态另备。`seg9-dry2.log`、`seg9-apply.log`、`seg9-persisted-check.log` 均为预期计数与零 FAIL，实际保存成功，无失败实写事务或回滚。
- **完整 pipeline 与 ROM**: 全量 `080000c0..084c7637` 重导 -> 剥离独立 .arm/.thumb -> inject_modes -> split_all_s -> build（NOPAUSE=1）；沿用此前已完成49步资源导出和五目录闭环的基线，仅出现既有 r13 汇编警告。ROM逐字节相同，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。
- **最终 gates**: 全157槽标签、实际 .word 表达式与原值一致；14定义完全对应提案；段内 DAT_/DWORD_/PTR_/UNK_/FUN_ 残留=0、ROM_INCBIN/.byte=0；段文本及新增注释 ASCII。相对本段快照，25模块只有 asm/12 文本改变，全部在本段；段前后文本相等，段外自然 xref 导出变化=0，既有CRLF保持。结果见 `output/refine-run-20260831-194634/seg9-landing-gates.json`、`seg9-persisted-check.json`；主线程独立 proposal/asm/ELF/ROM 验收通过，见 `root-seg9-verification.json`。
- **carve/disasm/§5.1/CSV**: 新增均为0；既有§5.1不变，无函数改名或CSV同步。**提交状态**: 已验证、未 stage、未 commit，保留 Seg-6..8 和主线程 exporter 基线修复。**下一段**: Seg-10 `[0x0809c3d8,0x0809d718)`；本轮未展开分析。

---

### 4.10 Seg-10 完成记录 [0x0809c3d8, 0x0809d718)

- **完成日期与输入**: 2026-09-01；第二轮正式 review PASS。最终提案 SHA256 `101400c177f1b1f44cbad8a74d97d0b462341f64d61f050fa3f8fb63598372cb`。首轮两项清单已修：正式CSV name同步合同、必要段外完整PLATE；本段55条原提案plate和136槽映射未因修订改变。
- **脚本与实际计数**: `tools/ghidra-labeling/RefineF12Seg10Slots.py` 直接采用最终提案；EQ=99、REF=18、RENAME=19，共136槽；FUNC_RENAME=3；PLATE=56（55段内+1必要段外），EOL=21（19条RENAME+2附加说明）。`seg10-dry.log`、`seg10-apply.log`、`seg10-persisted-check.log` 均为零FAIL，实际计数准确、保存成功，无失败实写事务或回滚。
- **三函数改名**: `0x0809c7ac` → `scan_monster_zone_slots_for_equip_activation_by_cid_table`；`0x0809c978` → `scan_zone_f_for_equip_activation_dd_scout_plane`；`0x0809d5f4` → `scan_equip_activation_candidates_with_name_display`。原FUNCTION ID6772/15795/6803及body 210/160/256字节、入口引用和EOL保持；既有四个奇函数指针物理表项不改，未切割rom.s。
- **必要段外PLATE**: `apply_equip_activation_via_packed_attr@0x0805b1f0` 在真实旧906字符全文匹配后，设置审定423字符ASCII全文，准确说明packed位域、entity low9及record+0x14的payload。FUNCTION ID455、166字节body、10条入口引用、所有body引用/EOL均保持；asm06只反映该完整plate改动，不再做旧名substring替换。
- **引用与数据表**: 19条RENAME到gP1LifePoints的operand0 DATA/DEFAULT主引用完整保留，USER_DEFINED属于目标LABEL；18条REF精确重建同目标operand0 DATA/USER_DEFINED主引用，保留其他引用。switch `0x0809c828` 复用Symbol ID6745规范为既有GAS全名，内部case对象、9个偶地址值及MOV pc编码不变。两外表 `[09e47680,09e476b0)` 的12个原word不变，五次dry/apply/persisted观测中的2个已有Data定义、0个outgoing和3个其他incoming引用完全相等；不扩定义、不carve。
- **新增定义**: 现有card_info.inc追加16常量、duel_field.inc追加4常量、rom_data.inc追加2个ROM表base绝对equate，共22定义，52项复用保持；不新增include，不改rom.s/includes。所有新增定义注释、56条PLATE和21条EOL均ASCII，PLATE最大463字符。
- **备份与完整pipeline**: `.rep.bak-20260831-232552-pre-F12Seg10` 的15文件和 `pre-f12-seg-10/` 的57份源码/产物在只读dry后、实写前再次逐项验证相同；活动文档另备。全量 `080000c0..084c7637` 导出 -> 剥离独立 .arm/.thumb -> inject_modes -> split_all_s -> build（NOPAUSE=1），沿用已完成49步资源导出及五目录闭环的基线，仅出现既有r13警告。
- **byte-identical与范围**: ROM逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。全136槽标签/实际 .word 表达式/原值一致；本段DAT_/DWORD_/PTR_/UNK_/FUN_及裸块残留=0、非ASCII=0。25模块机器码地址/字节注记不变；asm12只改Seg-10，asm06只改上述一条plate，其他23模块不变，无其他自然xref文本变化；既有CRLF保持。详见 `seg10-landing-gates.json`、`seg10-persisted-check.json`；主线程独立核验见 `root-seg10-verification.json` 与 `root-seg10-scope-verification.json`。
- **inventory、CSV与registry**: 保存后真实运行 `ExportFunctionInventory.py` 刷新temp四文件（5209函数、5119具名、90 auto）；对新inventory先执行sync `--dry-run`，仅报告本轮3个正式名差异。随后按CSV `address` 仅修改3个 `name` 单元格，proposed_name/score仍空，tags及其余所有字段/行不变；再次dry-run报告0差异，未运行sync实写。registry仅更新既有3个FUN地址key的name和审定plate，其余1515tuple保持，未执行历史全脚本。记录见 `seg10-name-sync.json` 及两次 `seg10-sync-*-dry.log`；主线程独立验收通过，见 `root-seg10-rename-verification.json`，四FUNCTION真实后态复核通过，见 `root-seg10-function-state-verification.json`。
- **提交与下一任务**: 已验证、未stage、未commit；carve/disasm/新增§5.1均0，保留此前段及主线程exporter修复。本段完成不代表模块12全清：7个历史自动槽、`0x080952fc` 的8字节块及20行旧名注释仍待用户明确授权后补漏。本轮未处理这些历史项，未预析模块13。此处为Seg-10结束时的历史状态；后续授权补漏及模块12闭合结果见§4.11。

### 4.11 F12-Historical-Closure 历史补漏与模块收尾

- **授权与评审**: 用户2026-09-01回复“可以”后按涉及地址递增执行。`doc/dev/refine/F12-Historical-Closure.proposal.md` 第二轮PASS；最终proposal SHA256 `74f49b4e0cddffe0a66dd2c0a073fe28c555a6d60d89c979bb9796aa58a5ae11`，review SHA256 `3f90388db91a3f52d6596b19f78d9ae9b6130a176f228cab0d3b038cd2397248`。第一轮仅修95554双LABEL复用合同；19PLATE、8EOL、槽映射和反汇编计划未改。
- **实际落地**: `tools/ghidra-labeling/RefineF12HistoricalClosure.py`（SHA256 `a1bea9cebf813154eeb45f4e501e126be41472d956999996cb467afa4f04909a`）完成EQ=0、REF=2、RENAME=6，共8槽；19个完整PLATE、8个EOL全部ASCII，PLATE最长485字符；DISASM=1范围/8 B/3指令。NEW=0、REUSE=6、FUNC_RENAME=0、carve=0、新增§5.1=0。
- **池与目标对象**: 六DWORD保留原ELIGIB equate、空outgoing refs及/dword4，只设USER池名/EOL。9565c保留/undefined4，仅新建operand0 DATA/USER_DEFINED/primary到既有gSpriteAttrBuf；RAM id21747及/undefined2长2不变，不读取RAM数值。95550的USER槽id31015与原DATA/USER引用完整保留；95554只调用既有global USER LABEL id31014的setPrimary，scoped ANALYSIS id4244仅转为非primary，两个对象的ID/name/namespace/source均不变。实际导出`.word switchD_0809554c__switchdataD_08095554`；没有引用重建、同址别名新增或对象合并。
- **8字节解码与函数守卫**: `[0x080952fc,0x08095304)`由8个undefined单字节单元转为`movs r0,#0`、`bl init_equip_card_sprite_row_entry`、`b LAB_0809533c`，长度2/4/2，原字节`00 20 00 f0 53 fc 1b e0`保持。逐条限制DisassembleCommand范围，关闭flow跟随及代码分析，不clearListing、不创建函数、不扩body。保留952fc原动态LABEL和两条条件跳转；callee95ba8仅增952fe CALL，epilogue9533c仅增95302 JUMP，其余ID/指令/body/旧plate/EOL/refs不变。19个原函数的ID/name/body/incoming/EOL均保持，全局函数总数仍5209。两switch共42个偶地址word及95554的30个不同case目标保持。
- **备份与流水线**: `.rep.bak-20260901-005625-pre-F12HistoricalClosure` 15文件、`pre-f12-historical-closure/` 58份源码/产物于dry前后复核一致，活动文档与历史登记另留前态。直接`-noanalysis -readOnly` dry零FAIL，主线程AST逐字核对通过后事务实写；pre/post零FAIL并Save成功。全量导出`080000c0..084c7637`，去除4条独立arm/thumb，inject_modes→split_all_s→NOPAUSE build；沿用本轮已完成49步资源导出/18200文件闭环，仅有既有r13弃用警告。保存后只读check零FAIL，15DB文件check前后hash不变。无失败事务或回滚。
- **ROM与全模块结果**: 原ROM与构建ROM均33554432 B，逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b` ✅。8槽实际标签/.word/原值/EOL、19完整PLATE、全部原机器码字节注记及3条新解码注记通过。模块自动数据标签、旧FUN/SUB/DAT/DWORD/PTR/UNK注释、`.byte`残留均0；原中文文件头保持，所有新注释ASCII。四§5.1块9437c/1c、94c3e/22、95b28/14、96eec/34总134 B原样保留；96eec的raw=1是未压缩6bpp卡图像素巧合，有效引用=0。
- **范围与独立验收**: 25模块仅asm12在批准的19PLATE/8槽/8字节解码处改变，其他24模块、22个constants、rom.s/includes、CSV/registry及4个inventory文件字节不变，无额外自然xref差异；原CRLF保持，`git -c core.whitespace=trailing-space,space-before-tab,cr-at-eol diff --check`通过。自身证据为`closure-landing-gates.json`、`closure-persisted-check.json`；主线程四项独立PASS为`root-closure-verification.json`、`root-closure-scope-verification.json`、`root-closure-state-verification.json`、`root-closure-slots-verification.json`，其四份只读后态查询也保持15DB hash不变。运行证据均位于`output/refine-run-20260831-194634/`。
- **状态与续接**: 本批已验证并进入本轮提交收束；保留此前Seg-6..10及主线程exporter修复。模块12收尾闭合，模块13已按驱动器继续推进。最终asm12 SHA256 `fd1f3a7138ef1f1076c52930479e5101e764a59fed6f47a4e26a69b3a406bfb0`。

---

## 五、Seg 路线图 (地址序, 不回头不跳号)

按 push-prologue 抽 144 函数入口, 按 slot 密度均分 10 段 (target ~118 槽/段, 边界=函数起点):

| Seg | 起始地址 | 结束地址 | fn 数 | slot 数 | 内含 ROM_INCBIN | 分类初判 |
|-----|----------|----------|-------|---------|-----------------|----------|
| 1  | 0x080941c4 | 0x08094f20 | 19 | 113 | 0x9437c/0x1c, 0x943e8/0x12, 0x94c3e/0x22 | 3 块均 THUMB code -> R4 disasm |
| 2  | 0x08094f20 | 0x08095ba8 | 13 | 109 | 0x95274/0xc0, 0x95b28/0x14 | 0x95274=10 case blocks; 0x95b28=helper -> R4 disasm |
| 3  | 0x08095ba8 | 0x08096a4c | 14 | 116 | — | 纯 slot 符号化 + plate |
| 4  | 0x08096a4c | 0x08097828 | 24 | 109 | 0x96eec/0x34 | ✅ §5.1复核完成；raw=1/effective=0，THUMB helper+pools原样保留，未disasm |
| 5  | 0x08097828 | 0x080984d0 | 5  | 118 | — | 纯 slot (装备发动相位机) |
| 6  | 0x080984d0 | 0x08099314 | 3+1 共享收尾 | 126 | — | ✅ 已完成；80EQ/39REF/7RENAME/4PLATE；含8个原PTR槽 |
| 7  | 0x08099314 | 0x0809a1a4 | 3  | 135 | — | ✅ 已完成；96EQ/27REF/12RENAME/3PLATE；含13个原PTR槽 |
| 8  | 0x0809a1a4 | 0x0809b178 | 1+2 共享收尾 | 131 | — | ✅ 已完成；95EQ/33REF/3RENAME/3PLATE；含3个原PTR槽及两个既有共享尾 |
| 9  | 0x0809b178 | 0x0809c3d8 | 7  | 157 | — | ✅ 已完成；104EQ/32REF/21RENAME/7PLATE/26EOL；两switch与段外表base符号化 |
| 10 | 0x0809c3d8 | 0x0809d718 | 55 | 136 | — | ✅ 已完成；99EQ/18REF/19RENAME/3FUNC_RENAME，55段内+1段外完整PLATE；本段4928字节验收通过 |

**续接**: 模块12及已授权历史补漏均已通过完整验收，模块13已由驱动器继续推进；当前状态见`doc/dev/p5-refine-13-equip-placement.md`。本批与后续已验收内容统一进入本轮提交收束。

**初始 ROM_INCBIN 测绘表 (6 块, 均在 Seg-1/2/4)**: 保留初始分类历史；本次收尾后实际仅余§5.1四块134字节，其他有引用内容已处理。
| ROM off | size | vaddr | Seg | ref-scan (raw / THUMB+1) | 字节首签名 | 初判 |
|---------|------|-------|-----|--------------------------|------------|------|
| 0x9437c | 0x1c | 0x0809437c | 1 | 0 / 0 | `0549 4000 8222 ... 7047 + .word 0201e4f0` | THUMB helper (fall-through?) |
| 0x943e8 | 0x12 | 0x080943e8 | 1 | 1 / 0 | `0226 06e0 0426 04e0 ...` | switch case 派发块 |
| 0x94c3e | 0x22 | 0x08094c3e | 1 | 0 / 0 | `... 7047 + .word 0201c4e0` | THUMB helper (gP1LifePoints; reviewer confirmed ROM bytes) |
| 0x95274 | 0xc0 | 0x08095274 | 2 | 2 / 0 | (asm 注释: 10 case blocks) | dispatch_equip_confirm switch 体 |
| 0x95b28 | 0x14 | 0x08095b28 | 2 | 0 / 0 | `0248 0349 ... 7047 + .word 0201c4e0` | THUMB helper |
| 0x96eec | 0x34 | 0x08096eec | 4 | 1 / 0 | `... 7047 + .word 0201c4e0/1d4c/1d54` | THUMB helper+pools |

> ref-scan raw/THUMB+1 = 0 的块由 executor 复核是否为前一函数 fall-through 续接或局部分支落点 (非真孤儿)。
> 段执行时按方法论「数据块分类决策树」复跑 ref-scan 确认分类。

---

## 5.1 未引用数据登记表

_(全 ROM 无有效引用的块在此登记；四块总计134字节。2026-09-01历史补漏复核未新增登记，全部原地址和字节保持。0x96eec虽有1次像素字节巧合raw命中，有效引用仍为0；以后出现真实引用时再处理。)_

| ROM off | size | vaddr | Seg | 初判内容 | 登记理由 |
|---------|------|-------|-----|----------|----------|
| 0x9437c | 0x1c | 0x0809437c | 1 | read_slot_tile_index_by_slot_idx (orphan THUMB code; r0=slot_idx -> bits[4:0] of gEquipEffectZoneBase+0x410+slot*2; bx lr; pool gEquipEffectZoneBase=0x0201e4f0) | ref-scan raw=0/thumb+1=0; not fall-through (preceding fn get_activation_zone_card_type_field ends bx r1 at 0x0809437a); ROM_INCBIN preserved |
| 0x94c3e | 0x22 | 0x08094c3e | 1 | reset_duel_turn_to_state2 (orphan THUMB code; writes 2 to [gP1LifePoints+0x1d14] and 0 to [gP1LifePoints+0x1d1c]; bx lr; first 2B=.zero align pad; entry @0x08094c40; pool gP1LifePoints=0x0201c4e0/DUEL_TURN_STATE_OFF=0x1d14/CARD_PLAY_PHASE_CTR_OFF=0x1d1c) | ref-scan raw=0/thumb+1=0; not fall-through (preceding fn poll_sprite_seq_until_done ends bx r0 at 0x08094c3c); ROM_INCBIN preserved |
| 0x95b28 | 0x14 | 0x08095b28 | 2 | set_lp_display_state_active (orphan THUMB code; ldr r0,[pc,#8]=gP1LifePoints; ldr r1,[pc,#12]=LP_DISPLAY_STATE_OFF(0x1d0c); adds r0,r0,r1; movs r1,#1; str r1,[r0,#0]; bx lr; pool: gP1LifePoints=0x0201c4e0/0x1d0c) | ref-scan raw=0/thumb+1=0; not fall-through (preceding step_prng_anim_frame ends pop/pop/bx r1 at 0x08095b1c); ROM_INCBIN preserved |
| 0x96eec | 0x34 | 0x08096eec | 4 | clear_activation_state_c_if_nonzero (orphan THUMB leaf; ldr gP1LifePoints; if [gP1LifePoints+ACTIVATION_STATE_C_OFF(0x1d4c)]==0 bx lr; else clear 0x1d4c=0, set ELIGIB_STATE_CTRL_OFF(0x1d54)=1, ELIGIB_ACT_TYPE_OFF(0x1d5c)=0xd; bx lr; pools: gP1LifePoints/0x1d4c/0x1d54/0x1d5c) | raw=1/thumb+1=0; the non-4-aligned hit at 0x08b16c2f is coincidental uncompressed 6bpp card-image pixel data (data/card-image-tiles.s), effective references=0; not fall-through (zero_duel_lp_display_counters ends bx lr at 0x08096edc; gap=0x08096edd..0x08096eeb .zero align pad); ROM_INCBIN preserved |
