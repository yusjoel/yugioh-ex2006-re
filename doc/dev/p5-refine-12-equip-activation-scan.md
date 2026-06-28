# 函数/数据细化计划 -- `asm/12_equip_activation_scan.s`

> 阶段目标: 把 `asm/12_equip_activation_scan.s` (ROM `0x080941c4 ~ 0x0809d718`, 效果 slot 显示上下文 +
> 装备发动链阻断 + 手牌/怪兽区扫描发动) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **13** 个文件 (file 00..11 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

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
  - `0x96eec/0x34` (Seg-4): THUMB helper, 结尾 `7047` + pools `0201c4e0/1d4c/1d54`。raw=1 -> R4 disasm。
  - 与 file 11 不同: **无隐藏 fn-ptr-table dispatch 巨块**, 144 fn 全部已命名 (无 disasm+命名作业, 仅小块 disasm)。
- **本文件主体 = slot 符号化** (~1183 DAT_/DWORD_/PTR_ 槽) + plate 订正; **无大数据表 carve** (初判)。
- Seg-8 = 单个巨型函数 `eval_equip_slot_pair_eligibility` (0x0809a1a4, 128 槽); Seg-9 = 7 fn/134 槽;
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
| 1  | 0x80941c4..0x8094f20 | 19 | 113 | 3 inc (0x9437c/0x1c, 0x943e8/0x12, 0x94c3e/0x22) | ✅ | (pending) |
| 2  | 0x8094f20..0x8095ba8 | 13 | 109 | 2 inc (0x95274/0xc0, 0x95b28/0x14) | ⬜ |  |
| 3  | 0x8095ba8..0x8096a4c | 14 | 116 | 0 inc | ⬜ |  |
| 4  | 0x8096a4c..0x8097828 | 24 | 109 | 1 inc (0x96eec/0x34) | ⬜ |  |
| 5  | 0x8097828..0x80984d0 | 5  | 118 | 0 inc | ⬜ |  |
| 6  | 0x80984d0..0x8099314 | 3  | 118 | 0 inc | ⬜ |  |
| 7  | 0x8099314..0x809a1a4 | 3  | 122 | 0 inc | ⬜ |  |
| 8  | 0x809a1a4..0x809b178 | 1  | 128 | 0 inc (eval_equip_slot_pair_eligibility 巨型单函数) | ⬜ |  |
| 9  | 0x809b178..0x809c3d8 | 7  | 134 | 0 inc | ⬜ |  |
| 10 | 0x809c3d8..0x809d718 | 55 | 116 | 0 inc (55 小型 scan 回调, 可拆 10a/10b) | ⬜ |  |

**总计**: 144 命名 fn / ~1183 DAT_/DWORD_/PTR_ 槽 / 6 ROM_INCBIN (合计 344 B, 全部误标 THUMB 代码)。
**重段提示**: Seg-8 (128 槽单函数) / Seg-9 (134 槽) / Seg-10 (55 fn) 较重; Seg-1/2/4 含 ROM_INCBIN 需 R4 disasm。

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

---

## 五、Seg 路线图 (地址序, 不回头不跳号)

按 push-prologue 抽 144 函数入口, 按 slot 密度均分 10 段 (target ~118 槽/段, 边界=函数起点):

| Seg | 起始地址 | 结束地址 | fn 数 | slot 数 | 内含 ROM_INCBIN | 分类初判 |
|-----|----------|----------|-------|---------|-----------------|----------|
| 1  | 0x080941c4 | 0x08094f20 | 19 | 113 | 0x9437c/0x1c, 0x943e8/0x12, 0x94c3e/0x22 | 3 块均 THUMB code -> R4 disasm |
| 2  | 0x08094f20 | 0x08095ba8 | 13 | 109 | 0x95274/0xc0, 0x95b28/0x14 | 0x95274=10 case blocks; 0x95b28=helper -> R4 disasm |
| 3  | 0x08095ba8 | 0x08096a4c | 14 | 116 | — | 纯 slot 符号化 + plate |
| 4  | 0x08096a4c | 0x08097828 | 24 | 109 | 0x96eec/0x34 | THUMB helper+pools -> R4 disasm |
| 5  | 0x08097828 | 0x080984d0 | 5  | 118 | — | 纯 slot (装备发动相位机) |
| 6  | 0x080984d0 | 0x08099314 | 3  | 118 | — | 纯 slot (display 状态机) |
| 7  | 0x08099314 | 0x0809a1a4 | 3  | 122 | — | 纯 slot (equip field phase / spell display 状态机) |
| 8  | 0x0809a1a4 | 0x0809b178 | 1  | 128 | — | 巨型单函数 eval_equip_slot_pair_eligibility |
| 9  | 0x0809b178 | 0x0809c3d8 | 7  | 134 | — | 纯 slot (display state / chain scan) |
| 10 | 0x0809c3d8 | 0x0809d718 | 55 | 116 | — | 55 小型 scan_*_zone_*_for_equip_activation 回调, 可拆 10a/10b |

**ROM_INCBIN 全表 (6 块, 均在 Seg-1/2/4)**:
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

_(全 ROM 0 引用的块在此登记, 引用到时再处理)_

| ROM off | size | vaddr | Seg | 初判内容 | 登记理由 |
|---------|------|-------|-----|----------|----------|
| 0x9437c | 0x1c | 0x0809437c | 1 | read_slot_tile_index_by_slot_idx (orphan THUMB code; r0=slot_idx -> bits[4:0] of gEquipEffectZoneBase+0x410+slot*2; bx lr; pool gEquipEffectZoneBase=0x0201e4f0) | ref-scan raw=0/thumb+1=0; not fall-through (preceding fn get_activation_zone_card_type_field ends bx r1 at 0x0809437a); ROM_INCBIN preserved |
| 0x94c3e | 0x22 | 0x08094c3e | 1 | reset_duel_turn_to_state2 (orphan THUMB code; writes 2 to [gP1LifePoints+0x1d14] and 0 to [gP1LifePoints+0x1d1c]; bx lr; first 2B=.zero align pad; entry @0x08094c40; pool gP1LifePoints=0x0201c4e0/DUEL_TURN_STATE_OFF=0x1d14/CARD_PLAY_PHASE_CTR_OFF=0x1d1c) | ref-scan raw=0/thumb+1=0; not fall-through (preceding fn poll_sprite_seq_until_done ends bx r0 at 0x08094c3c); ROM_INCBIN preserved |
