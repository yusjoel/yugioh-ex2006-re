# 函数/数据细化计划 -- `asm/10_equip_effect_dispatch.s`

> 阶段目标: 把 `asm/10_equip_effect_dispatch.s` (ROM `0x08079e60 ~ 0x080850d8`, neo daedalus
> zone OAM + 装备判据/效果按类型派发) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **11** 个文件 (file 00..09 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..09 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用->§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..09 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **ROM_INCBIN 分类核心 (file 06..09 已确认多次)**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - **`0x09e4xxxx`/`0x09e3xxxx` = card effect handler dispatch table** (entry 0x18B = `[CID, fn_activate(+1), pad, fn_eligible(+1), pad, pad]`,
    FS 运行时加载); **fn_eligible 块的 CID 在 fn_ptr 地址 -0xc 位置** (别取错下一 entry); THUMB+1 命中 -> R4 disasm。
  - **file 10 特征**: 39 ROM_INCBIN 块 + 6 switchD。大量块属于 **跳转表** (raw-ref -> carve 进 rom.s) 或 **fn_eligible THUMB stubs** (THUMB+1 ref -> R4 disasm)。ref-scan 必做, 逐块据实判定。
  - 块内可能含多 sub-fn (经 dispatch raw 指针 / MOV PC,r0 / switchD 到达); raw=0 且 THUMB+1=0 -> §5.1。
- **switchD 跳转表 (file 10 含 6: 0x7d126/0xed22/0xee92/0xfe22/0x806cc/0x81e2c)**: 目标裸 THUMB 地址 -> R4 disasm 逐 stub (file 00 Seg-5c 范式); case stub 可级联 bl ROM_INCBIN helper。注意: switchD 地址属某段, 其目标块可能落在本段内也可能属下一段 -- 逐段 ref-scan 确认。
- **R4 disasm 范式**: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand; literal pool createDWord 强制 split。
- **机器码核 (必做)**: disasm fn 比较+分支指令独立解码; 函数名运算符/偏移/卡名与机器码一致; **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核**: 标 new CID 逐一 grep 0 命中; 标 reuse 逐一 grep 确存在; 记证据。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集 (穷举对账); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实; 未分配->中性 `cid_<hex>`, 勿臆造。
- **误名警觉**: 函数名/plate 称的卡名/全局与函数体矛盾即误名信号; 走 FUNC_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 每个 FUN_ 地址查现名替换; 落地后 grep == 0。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04 (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05 Seg-8 6 槽 / asm/06/07/08/09 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责)。
- **disasm 必须完全消除每个 sub-stub** (file 09 教训: 逐 stub per-4B DisassembleCommand; 重跑前先 clearListing 整 range 再 setTMode; 否则 ContextChangeException)。

**file 02..09 已建可复用资产** (新建前必 grep): 见 `p5-refine-05-equip-eligibility-a.md` §一 + file 06/07/08/09 新增 (card_info.inc ~600+ CID / ewram.inc / duel_field.inc / oam_attr.inc / gfx_resource.inc / g2d_tags.inc / gl_scrollbar.inc / gl_blend.inc 等)。

---

## 二、落地工作流 (pipeline)

同 file 00..09 doc §二:
```
备份 .rep -> Ghidra 脚本 (RefineF10Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
-> ghidra-export-range.bat 080000c0 084c7637 -> inject_modes.py -> split_all_s.py
-> build + byte-identical SHA1 9689337d -> (改/建函数名才) ExportFunctionInventory + sync CSV -> commit
```
3-agent: executor -> reviewer (C1-C13) -> fixer (模式A改proposal / 模式B落地)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (10_equip_effect_dispatch.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN / switchD | 状态 | commit |
|-----|------|-----|--------|----------------------|------|--------|
| 1  | 0x79e60..0x7ae84 | 19 | 61  | 8 inc (0x79fac/30, 0xa00c/e8, 0xa138/28, 0xa178/14c, 0xa3b8/38, 0xa464/11c, 0xa688/44, 0xa71c/f8) | ✅ | aa53bf0 |
| 2  | 0x7ae84..0x7be2c | 18 | 47  | 8 inc (0xaf66/3a, 0xafb8/110, 0xb4d4/2c, 0xb574/144, 0xb7dc/28, 0xb878/e0, 0xb9f4/28, 0xba30/100) | ✅ | (see below) |
| 3  | 0x7be2c..0x7cd68 | 19 | 68  | 2 inc (0xc87a/3e, 0xc92c/158) | ✅ | (see 4.03) |
| 4  | 0x7cd68..0x7db20 | 19 | 53  | 2 inc (0xd7e8/2c, 0xd830/fc) + 1 sw (0xd126) | ✅ | (see 4.04) |
| 5  | 0x7db20..0x7f730 | 19 | 64  | 8 inc (0xdd68/30, 0xddac/16c, 0xdf90/2bc, 0xe398/2c, 0xe438/16c, 0xe5d4/63c, 0xf280/3c, 0xf330/128) + 2 sw (0xed22, 0xee92) | ✅ Seg-5a+5b | 9404095 / (see 4.06) |
| 6  | 0x7f730..0x80ba0 | 18 | 123 | 0 inc + 2 sw (0xfe22, 0x806cc) | ✅ | (see 4.06b) |
| 7a | 0x80ba0..0x81900 | 9+24sub | 101 | 0 inc + 0 sw | ✅ | (see 4.07a) |
| 7b | 0x81900..0x82290 | 10 | 51  | 2 inc (0x82046/fa, 0x82158/138) + 1 sw (0x81e2c) | ✅ | (see 4.07b) |
| 8a | 0x82290..0x82b18 | 7+5fn | 49  | 2 inc (0x827d4/d8, 0x828c4/f8) | ✅ | (see 4.08a) |
| 8b | 0x82b18..0x83450 | 12 | 67  | 0 inc | ✅ | (see 4.08b) |
| 9  | 0x83450..0x84318 | 18 | 89  | 2 inc (0x8420e/26, 0x8424c/cc) | ✅ | (see 4.09) |
| 10 | 0x84318..0x850d8 | 19 | 55  | 5 inc (0x8474e/2a, 0x84790/164, 0x84918/180, 0x84af2/2a, 0x84b34/10c) | ⬜ | |

**总计**: 187 fn (全部已命名) / 825 DWORD_/DAT_ 槽 / 39 ROM_INCBIN + 6 switchD。
**重段提示**: Seg-7 (152 槽) 和 Seg-6 (123 槽) 最重, 含大型 switchD 派发族; Seg-8 (113 槽) 次重。
Seg-5 含最多 ROM_INCBIN (8 inc + 2 switchD) 且有 0xe5d4/0x63c 超大块 (1596 B), 须仔细 ref-scan 分类。

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录

- **范围**: [0x08079e60, 0x0807ae84), 19 fn, 61 slots, 8 ROM_INCBIN
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 47 (43 REUSE + 4 NEW: NEO_DAEDALUS_OAM_SPRITE_BASE/CARD_DISPLAY_OP_ID_137/EQUIP_PAIRED_SLOT_PRED/MAGICIANS_CIRCLE_CID + zone_query_hand_tag_12a1)
- **RENAME_SLOTS**: 9 (gP1LifePoints already-symbolic slots)
- **REF_SLOTS**: 5 (ROM_INCBIN entry bases + dispatch table label)
- **R4 disasm**: 8 blocks (BLK1/3/5/7 = fn_eligible THUMB stubs; BLK2/4/6/8 = dispatch sub-stubs)
  - BLK1 fn_eligible Abyssal Designator (CID=0x17f4); BLK3 Big Wave Small Wave (0x17f9)
  - BLK5 shared CID 0x1803 (unassigned) + equip_cid_15de (0x15de)
  - BLK7 Magician's Circle (MAGICIANS_CIRCLE_CID=0x1818)
  - Pool fix pass: 21 additional createDWord calls (sub-stub inline literal pools)
- **NEW constants**: NEO_DAEDALUS_OAM_SPRITE_BASE=0x180d (equip_lp_delta.inc); CARD_DISPLAY_OP_ID_137=0x137, EQUIP_PAIRED_SLOT_PRED=0x181e, zone_query_hand_tag_12a1=0x12a1 (duel_field.inc); MAGICIANS_CIRCLE_CID=0x1818 (card_info.inc)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ in [0x79e60, 0x7ae84)
- **Ghidra scripts**: RefineF10Seg1Slots.py, DisassembleF10Seg1Blocks.py, RefineF10Seg1PoolFix.py
- **commit**: aa53bf0
- **follow-up (2026-06-21)**: 4 fn_eligible stubs (BLK1/3/5/7) named as Ghidra functions (NameF10Seg1FnEligible.py); CSV +4; byte-identical 9689337d confirmed

### 4.02 Seg-2 完成记录

- **范围**: [0x0807ae84, 0x0807be2c), 18 fn, 51 slots (47 DAT_/DWORD_ + 4 PTR_gP1LifePoints_), 8 ROM_INCBIN
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 31 (all REUSE; SERIAL_SPELL_CID/gEquipChainSlotRefs x3/PLAYER_BLOCK_STRIDE x9/gP1FieldArrayCBase/gDuelFieldSlots x2/gDuelPhaseFlags x5/FIELD_STATE_OFF/PROTECTOR_OF_THE_SANCTUARY_CID/gDuelCardCtxBase x3/EQUIP_ACT_SCORE_MODE_103/LP_CARD_TRACK_NEXT_OFF/gP1ChainZoneArray/gEquipZoneCountTable/LP_CARD_TRACK_BASE_OFF/EQUIP_PHASE_FRAME_OFF x2/LP_BANISHER_CTX_OFF)
- **REF_SLOTS**: 6 (check_equip_slot_eligible_by_type_query+1 x2 / check_equip_slot_eligible_by_side_and_setcode+1 x2 / check_equip_activation_at_slot11+1 x2)
- **RENAME_SLOTS**: 14 (gP1LifePoints dup x6 + ROM_INCBIN base labels x4 + PTR_gP1LifePoints_ x4)
- **FUNC_RENAME**: 1 (tick_equip_zone_target_select_display_seq__0807bc48 -> tick_equip_zone_target_select_display_seq; drop auto-deconflict suffix)
- **PLATE**: 1 (fn_eligible_hero_kid_hyena shared stub ASCII plate; CID=0x19a7+0x1867)
- **R4 disasm**: 8 blocks
  - BLK1 fn_eligible_lighten_the_load @ 0x0807af68 (CID=0x1847); 2B pad at 0x7af66
  - BLK2 6 Lighten the Load dispatch sub-stubs @ 0x0807afb8..0x0807b0c7
  - BLK3 fn_eligible_hero_kid_hyena @ 0x0807b4d4 (CID=0x19a7+0x1867 shared); 0x4687 MOV PC,r0 code at 0x7b4f4 correctly NOT createDWord'd
  - BLK4 7 Hero Kid/Hyena dispatch sub-stubs @ 0x0807b574..0x0807b6b7 (29-entry table)
  - BLK5 fn_eligible_rescue_cat @ 0x0807b7dc (CID=0x1876)
  - BLK6 7 Rescue Cat dispatch sub-stubs @ 0x0807b878..0x0807b957 (29-entry table)
  - BLK7 fn_eligible_gatling_dragon @ 0x0807b9f4 (CID=0x1878)
  - BLK8 5 Gatling Dragon dispatch sub-stubs @ 0x0807ba30..0x0807bb2f (5-entry table)
- **PoolFix**: 33 createDWord calls (inline pools in BLK2/4/6/8 + ROM_INCBIN residuals at 0x7ba70/0x14 + 0x7bb0c/0x18)
- **createFunction**: 4 fn_eligible stubs named
- **NEW constants**: none (all REUSE)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 non-ASCII in [0x7ae84, 0x7be2c)
- **ROM_INCBIN before/after**: 31 -> 23 (8 eliminated)
- **Ghidra scripts**: RefineF10Seg2Slots.py, DisassembleF10Seg2Blocks.py, RefineF10Seg2PoolFix.py
- **commit**: 1472a5a
- **CSV**: +4 fn_eligible rows + 1 FUNC_RENAME update

### 4.03 Seg-3 完成记录

- **范围**: [0x0807be2c, 0x0807cd68), 19 fn, 68 slots, 2 ROM_INCBIN
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 52 (50 REUSE + 1 NEW: LP_CARD_TRACK_ALT_OFF=0x00001dac ewram.inc after LP_CARD_TRACK_NEXT_OFF + 3 GAS expr: gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF=0x0201b734 x3)
- **RENAME_SLOTS**: 13 (gP1LifePoints already-symbolic x12 + BLK2 base des_frog_dispatch_stubs@0x0807c92c)
- **REF_SLOTS**: 3 (check_equip_activation_at_slot11+1 x2 + invoke_effect_node_with_active_flag_3arg+1 x1)
- **FUNC_RENAME**: 1 (tick_equip_activation_display_state drop __0807c388 suffix; note: fn@0x080670a0 already has same base name -> GAS exporter auto-appends __0807c388 in export for deconfliction; no byte-identical impact)
- **PLATE**: 1 (skip: old substring not found in Ghidra plate, already applied in prior session)
- **R4 disasm**:
  - BLK1 0x7c87a/0x3e: fn_eligible_des_frog@0x0807c87c (CID=DES_FROG_CID=0x1918; 2B pad at 0x7c87a; 2 pool DWords at 0x7c8b0+0x7c8b4; NOT createDWord at 0x7c8ac=0x4687 MOV PC,r0 code)
  - BLK2 0x7c92c/0x158: 9 Des Frog dispatch sub-stubs A..I (des_frog_stub_{a_zone_check/b_display_init/c_incr_counter/d_oam_setup/e_ret77/f_ret76/g_ret64/h_enqueue_lp/i_default_exit}; 11 pool DWords; NOT createDWord at 0x7c95c=0xe00a/0x7ca08=0xe038 THUMB branches)
- **createFunction**: fn_eligible_des_frog @ 0x0807c87c (CID=0x1918=DES_FROG_CID)
- **NEW constants**: LP_CARD_TRACK_ALT_OFF=0x00001dac (ewram.inc after LP_CARD_TRACK_NEXT_OFF)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN in [0x7be2c, 0x7cd68); 0 non-ASCII new writes
- **ROM_INCBIN before/after**: 23 -> 21 (2 eliminated: BLK1+BLK2)
- **Ghidra scripts**: RefineF10Seg3Slots.py, DisassembleF10Seg3Blocks.py, RefineF10Seg3CleanLabel.py (label cleanup utility)
- **commit**: 77736c0
- **CSV**: +1 fn_eligible_des_frog row

### 4.04 Seg-4 完成记录

- **范围**: [0x0807cd68, 0x0807db20), 19 fn, 53 slots, 2 ROM_INCBIN + 1 inline .byte + switchD_0807d126
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 43 (42 REUSE + 1 NEW: TRIGGER_OP_PARAM_139=0x139 duel_field.inc after TRIGGER_OP_PARAM_107)
- **RENAME_SLOTS**: 4 (gP1LifePoints already-symbolic x3 + BLK2 base sillva_dispatch_stubs@0x0807d830)
- **REF_SLOTS**: 6 (check_equip_activation_at_slot11+1 x2 / switchD_0807d126__switchdataD_0807d130 raw-ptr / invoke_effect_node_with_active_flag_3arg+1 / check_equip_slot_eligible_by_card_id_bst+1 / check_card_id_is_normal_summon_type+1)
- **FUNC_RENAME**: 0
- **PLATE**: 5 (ASCII; build_equip_eligible_bitmap_for_slots / apply_equip_activation_with_neo_daedalus_lp_output / tick_equip_target_validity_prng_lp_display / tick_equip_activation_display_state_machine / tick_zone_pipeline_with_neo_daedalus_oam_setup)
- **switchD**: switchD_0807d126 already decoded, no R4 action needed
- **R4 disasm**:
  - BLK1 0x7d7e8/0x2c: fn_eligible_sillva_warlord_of_dark_world@0x0807d7e8 (CID=SILLVA_WARLORD_OF_DARK_WORLD_CID=0x1968; 2 pool DWords at 0x7d80c+0x7d810; NOT createDWord at 0x7d808=0x4687 MOV PC,r0 code)
  - BLK2 0x7d830/0xfc: 5 Sillva dispatch sub-stubs A..E (sillva_state_{80_activate/7f_trigger/7c_7e_hand_enqueue/7b_7d_lp_display/7a_counter}; 9 pool DWords)
  - inline .byte 0x7db14/0xc: fn_eligible_dark_deal@0x0807db14 (CID=DARK_DEAL_CID=0x1975; no pool, bx lr leaf)
- **createFunction**: fn_eligible_sillva_warlord_of_dark_world @ 0x0807d7e8, fn_eligible_dark_deal @ 0x0807db14
- **NEW constants**: TRIGGER_OP_PARAM_139=0x00000139 (duel_field.inc)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 .byte code in [0x7cd68, 0x7db20); 0 non-ASCII new writes
- **ROM_INCBIN before/after**: 21 -> 19 (2 eliminated: BLK1+BLK2; inline .byte also eliminated)
- **Ghidra scripts**: RefineF10Seg4Slots.py, DisassembleF10Seg4Blocks.py
- **CSV**: +2 fn_eligible rows (fn_eligible_sillva_warlord_of_dark_world, fn_eligible_dark_deal)

### 4.05 Seg-5a 完成记录

- **范围**: [0x0807db20, 0x0807ec10), ~19 fn, 64 slots (Seg-5 前半), 6 ROM_INCBIN blocks (BLK1..6)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 8 (6 REUSE + 2 NEW)
  - NEW: TRIGGER_OP_PARAM_10D3=0x10d3 (duel_field.inc after TRIGGER_OP_PARAM_139) + invoke_effect_node_active_fn_ptr=0x08090625 (duel_field.inc; THUMB+1 ptr to invoke_effect_node_with_active_flag_3arg)
  - REUSE: ELIGIB_SPRITE_CTRL_OFF / FREED_THE_MATCHLESS_GENERAL_CID / LP_ACTIVATION_LINK_FLAG_OFF / EQUIP_PHASE_FRAME_OFF x2 / PLAYER_BLOCK_STRIDE
- **REF_SLOTS**: 7 (gEquipZoneCountTable@0x7db58 / gDuelPhaseFlags@0x7db88+0x7dcd0+0x7e2ec / gDuelCardCtxBase@0x7dca0 / gEquipChainSlotRefs@0x7dd64 / gDuelFieldSlots@0x7e390)
- **RENAME_SLOTS**: 1 (DWORD_0807dd5c -> PTR_gP1LifePoints_0807dd5c)
- **FUNC_RENAME**: 0
- **PLATE**: 0
- **NEW constants**:
  - duel_field.inc +2: TRIGGER_OP_PARAM_10D3=0x000010d3 / invoke_effect_node_active_fn_ptr=0x08090625
  - card_info.inc +4: BES_COVERED_CORE_CID=0x000019bf / DD_GUIDE_CID=0x000019c0 / DISCIPLE_FORBIDDEN_SPELL_CID=0x000019c2 / DIVINE_DRAGON_EXCELION_CID=0x000019d3
- **R4 disasm**: 6 blocks (BLK1..6), 31 sub-stubs + 7 createFunction
  - BLK1 0x7dd68/0x30: fn_eligible_magical_mallet@0x0807dd68 (no pool; 0x4687 MOV PC,r0 code correctly NOT DWord'd)
  - BLK2 0x7ddac/0x16c: 5 Magical Mallet dispatch sub-stubs + extra sub-stub@0x7dee0 (reached via bl from case4; PoolFixF10Seg5a2 Issue 1)
  - BLK3 0x7df90/0x2bc: 12 equip_zone dispatch sub-stubs (equip_zone_stub0..11)
  - BLK4 0x7e398/0x2c: fn_eligible_ancient_gear_drill@0x0807e398 (ag_drill_eligible; pool at 0x7e3bc/0x7e3c0; 0x4687 NOT DWord'd)
  - BLK5 0x7e438/0x16c: 7 AG Drill dispatch sub-stubs; JT 24-entry DWords@0x7e3c4..0x7e420 (PoolFixF10Seg5a2 Issue 2)
  - BLK6 0x7e5d4/0x63c: 5 fn_eligible stubs (fn_eligible_bes_covered_core@0x7e5d4 / fn_eligible_dd_guide@0x7e6e0 / fn_eligible_disciple_forbidden_spell@0x7e7e4 / fn_eligible_malice_ascendant@0x7e960 / fn_eligible_divine_dragon_excelion@0x7e9f8); 17 pool DWords
- **Pool-fix passes**:
  - DisassembleF10Seg5aBlocks.py: initial pool DWords (BLK1..6 inline pools)
  - PoolFixF10Seg5a.py: 33 additional createDWord (BLK2/3/5/6 inline pools not caught in initial pass)
  - PoolFixF10Seg5a2.py: Issue 1 = re-disasm 0x7dee0 + 3 pool DWords; Issue 2 = 24 AG Drill JT DWords@0x7e3c4..0x7e420
- **createFunction**: 7 (fn_eligible_magical_mallet + fn_eligible_ancient_gear_drill + fn_eligible_bes_covered_core + fn_eligible_dd_guide + fn_eligible_disciple_forbidden_spell + fn_eligible_malice_ascendant + fn_eligible_divine_dragon_excelion)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 DAT_ in [0x7db20, 0x7ec10); 0 non-ASCII new writes
- **ROM_INCBIN before/after**: 19 -> 13 (6 eliminated: BLK1+BLK2+BLK3+BLK4+BLK5+BLK6)
- **Ghidra scripts**: RefineF10Seg5aSlots.py, DisassembleF10Seg5aBlocks.py, PoolFixF10Seg5a.py, PoolFixF10Seg5a2.py
- **CSV**: +7 fn_eligible rows (fn_eligible_magical_mallet / fn_eligible_ancient_gear_drill / fn_eligible_bes_covered_core / fn_eligible_dd_guide / fn_eligible_disciple_forbidden_spell / fn_eligible_malice_ascendant / fn_eligible_divine_dragon_excelion)
- **commit**: 9404095

### 4.06 Seg-5b 完成记录

- **范围**: [0x0807ec10, 0x0807f730), 14 fn + 2 disasm fns (BLK7/BLK8), 40 slots, 2 ROM_INCBIN + 2 switchD (already decoded)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 26 (22 REUSE + 4 NEW: FGD_CID=0x157e / FLUTE_SUMMONING_KURIBOH_CID=0x19ec / ZONE_ENTRY_OFFSET_5CC=0x5cc / EQUIP_DISPLAY_ROM_TABLE_BASE=0x09e59e14)
- **REF_SLOTS**: 12 (gDuelPhaseFlags x7 / gDuelFieldSlots x4 / gP1HandSlotArray x1)
- **RENAME_SLOTS**: 0
- **FUNC_RENAME**: 0
- **PLATE**: 9 (C8 stale FUN_ substitutions: 5 in-file + cross-file line-11578 /0807f8f0 raw-addr fix + 3 CJK->ASCII rewrites @ 0x0807ec10/0x0807ed04/0x0807f0a4)
- **R4 disasm**: 2 blocks
  - BLK7 0x7f280/0x3c: fn_eligible_flute_summoning_kuriboh@0x0807f280 (CID=0x19ec; push+MOV PC,r0 stub; pool at 0x7f2b4=gDuelPhaseFlags, 0x7f2b8=JT-base 0x7f2bc; 0x4687 NOT DWord'd)
  - BLK8 0x7f330/0x128: dispatch_flute_summoning_kuriboh_by_state_code@0x0807f330 (7 case stubs per-stub DisassembleCommand; 4 pool DWords at 0x7f3c4/0x7f3c8/0x7f400/0x7f428; epilogue pop {r4,r5,r6}+pop{r1}+bx r1)
- **createFunction**: 2 (fn_eligible_flute_summoning_kuriboh / dispatch_flute_summoning_kuriboh_by_state_code)
- **switchD disposition**: switchD_0807ed22 + switchD_0807ee92 both already decoded in asm; no R4 action
- **NEW constants**:
  - card_info.inc +2: FGD_CID=0x0000157e / FLUTE_SUMMONING_KURIBOH_CID=0x000019ec
  - ewram.inc +2: ZONE_ENTRY_OFFSET_5CC=0x000005cc / EQUIP_DISPLAY_ROM_TABLE_BASE=0x09e59e14
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 non-ASCII in [0x7ec10, 0x7f730) after 3 CJK plate rewrites
- **ROM_INCBIN before/after asm/10**: 13 -> 11 (2 eliminated: BLK7+BLK8)
- **Ghidra scripts**: RefineF10Seg5bSlots.py, RefineF10Seg5bPlateFix.py, RefineF10Seg5bCJKFix.py, DisassembleF10Seg5bBlocks.py
- **Pipeline note**: BLK8 needed per-stub DisassembleCommand (7 case stubs) not single-range; initial single disasm stopped at first unconditional branch leaving residual ROM_INCBIN; corrected by re-running with 7 individual stubs after re-export
- **CSV**: +2 new function rows (fn_eligible_flute_summoning_kuriboh / dispatch_flute_summoning_kuriboh_by_state_code)
- **commit**: (see below)

### 4.06b Seg-6 完成记录

- **范围**: [0x0807f730, 0x08080ba0), 18 fn, 123 slots (110 DAT_ + 13 DWORD_), 0 ROM_INCBIN + 2 switchD (already decoded)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 66 (63 in EQ_SLOTS + 3 DWORD_EQ_EXTRA; 15 REUSE + 9 NEW)
  - REUSE: EQUIP_ACTIVE_CTX_OFF x2 / PLAYER_BLOCK_STRIDE x13 / POLYMERIZATION_CID x2 / FUSION_GATE_CID x2 / FGD_CID x2 / EHERO_AVIAN/BURSTINATRIX/CLAYMAN/BUBBLEMAN_CID x1 each / UFOROID_FIGHTER_CID x3 / EHERO_ERIKSHIELER_CID x1 / ELIGIB_SPRITE_CTRL_OFF / ELIGIB_ANIM_STATE_OFF / LP_BANISHER_CTX_OFF / ACTIVATION_STATE_B_OFF x1 each
  - NEW: EQUIP_ZONE_ATTR_COMPOSITE_OFF=0x59c x4 / EQUIP_CRITERIA_TARGETED_FLAG_OFF=0x5a4 x11 / EQUIP_CRITERIA_DISPLAY_ARR_OFF=0x5ac x9 / DRAGONS_MIRROR_CID=0x1921 x1 / NON_FUSION_AREA_CID=0x197a x2 / OAM_EQUIP_ZONE_SPRITE_P2_4A=0x804a x1 / OAM_EQUIP_ZONE_SPRITE_P2_4B=0x804b x3 / OAM_EQUIP_ZONE_SPRITE_P2_4C=0x804c x1 / EQUIP_CRITERIA_ARR_NEG_OFF=0xfffffa54 x1
- **REF_SLOTS**: 57 (gDuelPhaseFlags x31 / gDuelPhaseFlags_criteria_count x2 / gDuelPhaseFlags_set_f_flag x3 / gDuelPhaseFlags_criteria_arr_base x1 / gP1LifePoints x1 / gP1HandCountBase x1 / gDuelFieldSlots x4 / gDuelFieldSlotState x1 / gP1FieldArrayCBase x3 / gP1ChainZoneArray x2 / gP1HandSlotArray x3 / gDuelCardCtxBase x2 / fn-ptr slot x1 EOL-only / switchD ptr x2)
- **RENAME_SLOTS**: 13 (DWORD_ literal pools at 0x08080a78..0x08080a94 x8 + 0x08080b44..0x08080b54 x5)
- **FUNC_RENAME**: 0
- **PLATE**: 11 mojibake->ASCII rewrites (initially applied to 3 wrong addresses; RefineF10Seg6CJKFix.py corrected 0x0807f7bc/0x0807fb9c/0x0807fde8) + 7 FUN_ plate substring fixes (5 already clean = [FAIL] harmless)
- **THUMB fn-ptr fix**: RefineF10Seg6ThumbFix.py removed bad label at mid-code 0x0807fad9; added EOL comment at 0x0807ff88 dispatch_criteria_caseD7d_fn_ptr slot
- **R4 disasm**: 0 (both switchD already decoded)
- **carve**: 0 (0 ROM_INCBIN in range)
- **§5.1**: 0
- **NEW constants** (12 total):
  - card_info.inc +2: DRAGONS_MIRROR_CID=0x00001921 / NON_FUSION_AREA_CID=0x0000197a
  - duel_field.inc +4: EQUIP_ZONE_ATTR_COMPOSITE_OFF=0x0000059c / EQUIP_CRITERIA_TARGETED_FLAG_OFF=0x000005a4 / EQUIP_CRITERIA_DISPLAY_ARR_OFF=0x000005ac / EQUIP_CRITERIA_ARR_NEG_OFF=0xfffffa54
  - oam_attr.inc +3: OAM_EQUIP_ZONE_SPRITE_P2_4A=0x0000804a / OAM_EQUIP_ZONE_SPRITE_P2_4B=0x0000804b / OAM_EQUIP_ZONE_SPRITE_P2_4C=0x0000804c
  - ewram.inc +3: gDuelPhaseFlags_criteria_count=0x0201b830 / gDuelPhaseFlags_set_f_flag=0x0201b838 / gDuelPhaseFlags_criteria_arr_base=0x0201b850
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ / 0 non-ASCII in [0x7f730, 0x80ba0); 1 stale FUN_08080c9c in push_to_effect_slot_array plate (Seg-7 caller, fixed when Seg-7 processed)
- **Ghidra scripts**: RefineF10Seg6Slots.py, RefineF10Seg6CJKFix.py, RefineF10Seg6ThumbFix.py
- **CSV sync**: no (FUNC_RENAME=0)

### 4.07a Seg-7a 完成记录

- **范围**: [0x08080ba0, 0x08081900), 9 main fn + 24 named sub-stubs (dispatch_equip_card_display_op_by_card_id BST hub + sub-stubs), 101 literal-pool slots, 0 ROM_INCBIN, 0 switchD
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 101 (71 REUSE + 30 NEW CID + 4 neutral cid_NNN + 3 NEW non-CID)
  - REUSE x71: PLAYER_BLOCK_STRIDE x3 / gDuelFieldSlots x3 / SLOT_FACE_STATUS_ARRAY_OFF x2 / DEMO_CLEAR_BITS_15_14 x2 / DUAL_LABEL_RENDER_STATE_CLEAR x2 + 43 card CID (REAPER_ON_NIGHTMARE/JOWLS_OF_DARK_DEMISE/SPELLBINDING_CIRCLE/HANE_HANE/RELINQUISHED/CYBER_RAIDER/COPYCAT/BRAIN_CONTROL/SNATCH_STEAL/MAGICAL_HATS/DRIVING_SNOW/RING_OF_DESTRUCTION/AQUA_SPIRIT/WINGED_MINION/BLAST_WITH_CHAIN/DRAGON_MANIPULATOR/OTOHIME/SECRET_OF_THE_BANDIT/ENEMY_CONTROLLER/GRAVEKEEPERS_ASSAILANT/INFERNO_FIRE_BLAST/CHECKMATE/FREEZING_BEAST/YZ_TANK_DRAGON/DIFFUSION_WAVE_MOTION/DARK_SCORPION_GORG_THE_STRONG/TSUKUYOMI/FALLING_DOWN/ENERGY_DRAIN/ORCA_MEGA_FORTRESS/ARCANE_ARCHER_OF_THE_FOREST/ORDER_TO_CHARGE/ARMED_DRAGON_LV5/ELEMENTAL_HERO_THUNDER_GIANT/HARPIES_HUNTING_GROUND/OVERPOWERING_EYE/WHITE_NINJA/CHARMER_RANGE_MAX/ELEMENTAL_HERO_TEMPEST/A_RIVAL_APPEARS/OJAMUSCLE/HERO_HEART/URIA_LORD/GAP_CID_13EA/SUMMONED_SKULL/REVIVAL_JAM/GRADIUS/RED_EYES_B_DRAGON)
  - NEW CID x30: SPIRIT_REAPER/RAIGEKI_BREAK/TRAP_MASTER/MAN_EATER_BUG/THE_RELIABLE_GUARDIAN/REINFORCEMENTS/DUST_TORNADO/KRYUEL/MASK_OF_DISPEL/THOUSAND_KNIVES/COLLECTED_POWER/VISER_DES/RYU_KISHIN_CLOWN/DOUBLE_SNARE/COLLAPSE/BOOK_OF_MOON/MONSTER_RELIEF/A_MAN_WITH_WDJAT/SOUL_TAKER/GUARDIAN_CEAL/GALE_LIZARD/COMPULSORY_EVACUATION_DEVICE/SHIELD_CRASH/GRANMARG_THE_ROCK_MONARCH/CATNIPPED_KITTY/ASSAULT_ON_GHQ/PATROID/VW_TIGER_CATAPULT/KARMA_CUT/GENERATION_SHIFT _CID (all in card_info.inc, pw=34460239 for GENERATION_SHIFT)
  - Neutral CID x4: cid_128a/cid_1326/cid_127 (x2)/cid_125 (not in card-stats.s; EOL "equip BST unassigned slot")
  - NEW non-CID x3 (duel_field.inc): EFFECT_SLOT_TYPE_CLEAR_MASK=0xffffc01f / STACK_ALLOC_NEG_512=0xfffffe00 / EQUIP_DISP_OP_ID_0x119=0x119
  - NEW internal-ID x1 (card_info.inc): HANE_HANE_INTERNAL_ID_0x1f5=0x1f5 (icid for card_name_lookup; not a CID)
- **REF_SLOTS**: 0
- **RENAME_SLOTS**: 0
- **FUNC_RENAME**: 0
- **PLATE**: 30 C8 stale FUN_ substitutions (assemble_effect_slot_attr_with_zone_lookup: FUN_08080c9c->enqueue_equip_slot_sprite_with_code_rotation; pack_effect_slot_attr_with_type_flags: FUN_08080d28->pack_equip_slot_sprite_with_code_attr; 24 sub-stubs: FUN_08080ea0->dispatch_equip_card_display_op_by_card_id; dispatch_card_display_op_by_id_match: FUN_080817c8->trigger_card_display_op_0x6f + FUN_080818dc->trigger_card_display_op_0x112; trigger_card_display_op_0x89: FUN_080818dc->trigger_card_display_op_0x112; cross-file asm/15 exec_equip_target_by_best_field7_score: FUN_08080c9c->enqueue_equip_slot_sprite_with_code_rotation)
- **Note C8**: FUN_08081de4 in find_effect_slot_by_side_and_type plate is Seg-7b function (not yet named); deferred to Seg-7b
- **carve**: 0 (no ROM_INCBIN in range)
- **disasm**: 0
- **§5.1**: 0
- **NEW constants**:
  - card_info.inc +35: 30 NEW CID + cid_128a/cid_1326/cid_127/cid_125 (neutral) + HANE_HANE_INTERNAL_ID_0x1f5
  - duel_field.inc +3: EFFECT_SLOT_TYPE_CLEAR_MASK/STACK_ALLOC_NEG_512/EQUIP_DISP_OP_ID_0x119
- **残留**: 0 DAT_/DWORD_ actual labels in [0x80ba0, 0x81900); 3 historical references in plate comment prose (harmless)
- **Ghidra scripts**: RefineF10Seg7aSlots.py
- **CSV sync**: no (FUNC_RENAME=0, disasm=0)

### 4.07b Seg-7b 完成记录

- **范围**: [0x08081900, 0x08082290), 12 named fn, 55 slots (EQ42 RENAME6 PTR_skip7), 2 ROM_INCBIN + 1 switchD (already decoded)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 42 (39 REUSE + 3 NEW CID)
  - REUSE x39: gDuelPhaseFlags x15 / gDuelCardCtxBase x3 / PLAYER_BLOCK_STRIDE x1 / gDuelFieldSlots x1 / DUAL_LABEL_RENDER_STATE_CLEAR x1 / ELIGIB_SPRITE_CTRL_OFF x3 / ELIGIB_ANIM_STATE_OFF x1 / TRIGGER_OP_PARAM_10D3 x2 / lookup_equip_score_mooyan_p0 x1 / gEquipChainSlotRefs x1 / PANDEMONIUM_CID / INSECT_IMITATION_CID / THE_KICK_MAN_CID / NINJITSU_ART_OF_TRANSFORMATION_CID / SPIRITUAL_EARTH_ART_CID / TRIAL_OF_THE_PRINCESSES_CID / GENERATION_SHIFT_CID / NOBLEMAN_EATER_BUG_CID / GREENKAPPA_CID / XING_ZHEN_HU_CID
  - NEW x3 (card_info.inc): LEVEL_UP_CID=0x17f5 / INFERNO_RECKLESS_SUMMON_CID=0x198e / GUARDIAN_ELMA_CID=0x164a
- **RENAME_SLOTS**: 6 (5 THUMB fn-ptr + 1 switchD table ptr tick_equip_5state_switch_table_ptr)
- **REF_SLOTS**: 0
- **FUNC_RENAME**: 0
- **PLATE**: 13 mojibake->ASCII (dispatch_equip_activation_display_by_confirm_state / tick_equip_slot_display_by_card_id_3state / dispatch_equip_display_by_type_flag_and_node_activity / enqueue_equip_slot_sprite_from_base_offset / check_effect_node_handler_for_slot / tick_equip_activation_display_5state / tick_equip_activation_display_with_card_routing) + 1 C8 FUN_08081900->tick_equip_activation_display_3state
- **R4 disasm**: 2 blocks (BLK1 + BLK2)
  - BLK1 0x82046/0xfa: route_penguin_soldier_equip_display@0x08082048 (THUMB fn, CID=0x1200=PENGUIN_SOLDIER_CID, FS table THUMB+1 ref at 0x09e43428; 2B pad at 0x82046; 6 pool DWords at 0x8210c/0x82110/0x82114/0x82118/0x82138/0x8213c; 0x82134=0x4687=THUMB code NOT DWord'd)
  - BLK2 0x82158/0x138: 6 sub-stubs (route_penguin_soldier_equip_sub0..sub5) via raw-ptr JT at 0x82140; JT already decoded as .word in asm; pool words: 0x82188/0x8218c/0x821a4/0x821f4..0x82200/0x82210/0x82238..0x8223c/0x82268..0x82270/0x8228c (pool fix pass)
- **Pool-fix pass**: PoolFixF10Seg7b.py -- 13 createDWord for BLK2 sub-stub inline literal pools
- **createFunction**: 7 (route_penguin_soldier_equip_display + sub0..sub5)
- **switchD**: switchD_08081e2c already decoded (all 5 case labels present); no R4 action
- **NEW constants**: card_info.inc +3 (LEVEL_UP_CID/INFERNO_RECKLESS_SUMMON_CID/GUARDIAN_ELMA_CID)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ (excl. PTR_skip) / 0 non-ASCII in [0x81900, 0x82290)
- **ROM_INCBIN before/after asm/10**: 11 -> 9 (2 eliminated: BLK1+BLK2)
- **Ghidra scripts**: RefineF10Seg7bSlots.py, DisassembleF10Seg7bBlocks.py, PoolFixF10Seg7b.py
- **CSV sync**: yes -- route_penguin_soldier_equip_display + sub0..sub5 (7 new functions); ExportFunctionInventory + sync needed

---

### 4.08a Seg-8a 完成记录

- **范围**: [0x08082290, 0x08082b18), 7 named fn + 4 disasm'd sub-stubs + 1 JT (已 decoded), 49 slots (EQ38 RENAME10 R4×1)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 38 (33 REUSE + 5 NEW across 8 slot occurrences)
  - REUSE x33: gDuelPhaseFlags x9 / gEquipChainSlotRefs x1 / PLAYER_BLOCK_STRIDE x2 / gDuelFieldSlots x3 / gDuelCardCtxBase x2 / DUAL_LABEL_RENDER_STATE_CLEAR x1 / EQUIP_ACT_SCORE_MODE_103 x2 / ELIGIB_SPRITE_CTRL_OFF x2 / ELIGIB_ANIM_STATE_OFF x1 / TRIGGER_OP_PARAM_10D3 x1 / lookup_equip_score_mooyan_p1 x1 / DRAW_DECIMAL_WIN_LABEL_ARG x1 / EQUIP_ACTIVATION_AUX_OFF x1 / DARK_BLADE_THE_DRAGON_KNIGHT_CID x1 / WHITE_HORNS_DRAGON_CID x1
  - NEW x5 (8 slot occurrences): EQUIP_DISPLAY_OP_PARAM_1A1=0x1a1 x1 / set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 x2 / check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr=0x0805000d x1 / GRAVEDIGGER_GHOUL_CID=0x12ed x1 / DISAPPEAR_CID=0x1515 x1
- **REF_SLOTS**: 0
- **RENAME_SLOTS**: 10 (gP1LifePoints literal pool x10 -- 5 fn literal pools each have 2 DWORD_ slots)
- **FUNC_RENAME**: 0
- **PLATE**: 6 mojibake->ASCII rewrites (dispatch_equip_activation_display_if_slot_card_id_ok / tick_equip_display_4state_with_effect_slot_array / tick_equip_display_3state_with_effect_node_probe / enqueue_equip_slot_sprite_with_attr_strip / check_effect_slot_zone_field_by_type / tick_equip_display_by_card_id_group_a_4state with ARM-verified BST: 0x12ed->type2, 0x12f9->type5, 0x1480->type3 Kycoo, 0x1515->type1, 0x183c->type3, 0x1996->type5)
- **R4 disasm**: 2 blocks (BLK1 + BLK2)
  - BLK1 0x827d4/0xd8: fn_eligible_two_pronged_attack@0x080827d4 (THUMB fn, CID=0x12e7=TWO_PRONGED_ATTACK_CID, FS table THUMB+1 ref at 0x09e3fc60; 4 pool DWords at 0x08082880/84/a4/a8; 0x080828a0=0x4687=THUMB code NOT DWord'd)
  - BLK2 0x828c4/0xf8: 4 sub-stubs (equip_sub_stub_a/b/c/shared_exit) via JT @0x828ac (already decoded as .word in asm; entries [0]=0x828c4,[1,3,5]=0x82954,[2]=0x828f4,[4]=0x82924); 11 pool DWords at 0x828ec/f0/91c/920/94c/950/988/98c/990/994/9ac
- **createFunction**: 5 (fn_eligible_two_pronged_attack + equip_sub_stub_a/b/c/shared_exit)
- **carve**: 0
- **§5.1**: 0
- **NEW constants**:
  - card_info.inc +3: TWO_PRONGED_ATTACK_CID=0x000012e7 / GRAVEDIGGER_GHOUL_CID=0x000012ed / DISAPPEAR_CID=0x00001515
  - duel_field.inc +3: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 / check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr=0x0805000d / EQUIP_DISPLAY_OP_PARAM_1A1=0x000001a1
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ / 0 non-ASCII in [0x82290, 0x82b18)
- **ROM_INCBIN before/after asm/10**: 9 -> 7 (2 eliminated: BLK1+BLK2)
- **Ghidra scripts**: RefineF10Seg8aSlots.py, DisassembleF10Seg8aBlocks.py
- **CSV sync**: yes -- fn_eligible_two_pronged_attack + equip_sub_stub_a/b/c/shared_exit (5 new functions)

---

### 4.08b Seg-8b 完成记录

- **范围**: [0x08082b18, 0x08083450), 12 named fn, 0 ROM_INCBIN, 0 disasm, 67 slots (EQ56 RENAME8 PTR_skip3)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 56 (33 REUSE + 23 via 13 NEW constants)
  - REUSE x33: gDuelPhaseFlags x9 / gDuelCardCtxBase x1 / gDuelFieldSlots x1 / gP1HandSlotArray x1 / PLAYER_BLOCK_STRIDE x3 / ELIGIB_SPRITE_CTRL_OFF x2 / ELIGIB_ANIM_STATE_OFF x1 / LP_CARD_TRACK_BASE_OFF x3 / P1LP_BLOCK2_OFF_1CE8 x1 / DUAL_LABEL_RENDER_STATE_CLEAR x5 / EQUIP_ACTIVE_CTX_OFF x2 / LP_ROW_TYPE8_ALL_SLOTS_MASK x1 / EQUIP_ACTIVATION_AUX_OFF x3 / set_equip_activation_state_by_mode_alt_fn_ptr x1 / DNA_SURGERY_CID x1 / RAY_OF_HOPE_CID x1 / DARK_FACTORY_MASS_PROD_CID x1 / BEHEMOTH_KING_CID x1 / POT_OF_AVARICE_CID x1 / equip_cid_15de_08048a68 x1 / SPELL_ZONE_TARGET_CARD_ID x1 / CARD_DISPLAY_OP31_LP_BAR_SUB x2
  - NEW x13 (23 slot occurrences): SHIFT_CID=0x140a / FIENDS_HAND_MIRROR_CID=0x1719 / BACKUP_SOLDIER_CID=0x1359 / MIRACLE_DIG_CID=0x149e / KELDO_CID=0x14e7 / HIDDEN_BOOK_OF_SPELL_CID=0x1630 / PRIMAL_SEED_CID=0x16d6 / GRAVEYARD_IN_FOURTH_DIMENSION_CID=0x17f7 / FORCES_OF_DARKNESS_CID=0x1974 / cid_1568=0x1568 / cid_16d3=0x16d3 / cid_1803=0x1803 / EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140
- **REF_SLOTS**: 0
- **RENAME_SLOTS**: 8 (4 gP1LifePoints literal pool already-symbolic + 4 fn-ptr DWORD_ with THUMB+1 EOL)
- **FUNC_RENAME**: 0
- **PLATE**: 6 mojibake->ASCII rewrites with ARM-verified content:
  - tick_equip_display_with_fn_ptr_routing_3state (0x08082b88): STATE_OFFSET=0x4b0 / EQUIP_ACTIVE_CTX_OFF=0x484 / BST 3 CIDs
  - build_equip_chain_pair_slot_entry (0x08082c8c): pair slot entry builder
  - tick_equip_display_by_card_id_group_b_3state (0x08082f44): STATE_OFFSET=0x4b0 (ARM-corrected from 0x4b4) / SLOT_PALETTE_OFFSET=0x4b4 / 11 BST CIDs
  - tick_equip_lp_display_by_node_state_4state (0x08083170): STATE_OFFSET=0x4b0 / XOR_OPERAND_OFF=0x4b4 (ARM-corrected)
  - dispatch_equip_display_if_confirm_state_one (0x080833a8): confirm_state=1 conditional
  - enqueue_equip_slot_sprites_for_pair_loop (0x080833bc): PAIR_TABLE_BASE=0x09e3f140 / r2 not r7 (B3 note)
- **carve**: 0
- **§5.1**: 0
- **NEW constants**:
  - card_info.inc +12: SHIFT_CID / FIENDS_HAND_MIRROR_CID / BACKUP_SOLDIER_CID / MIRACLE_DIG_CID / KELDO_CID / HIDDEN_BOOK_OF_SPELL_CID / PRIMAL_SEED_CID / GRAVEYARD_IN_FOURTH_DIMENSION_CID / FORCES_OF_DARKNESS_CID / cid_1568 / cid_16d3 / cid_1803
  - duel_field.inc +1: EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ (code) / 0 non-ASCII in [0x82b18, 0x83450)
- **ROM_INCBIN before/after asm/10**: 7 (unchanged, 0 ROM_INCBIN in this seg)
- **Ghidra scripts**: RefineF10Seg8bSlots.py
- **CSV sync**: no (FUNC_RENAME=0, no new functions)

---

### 4.09 Seg-9 完成记录

- **范围**: [0x08083450, 0x08084318), 18 named fn + 6 new disasm'd fn, 92 slots (EQ81 REF7 RENAME4)
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 81 (all REUSE except 4 NEW constants)
  - REUSE x77: gDuelPhaseFlags x26 / gDuelCardCtxBase x7 / gEquipChainSlotRefs x2 / ELIGIB_SPRITE_CTRL_OFF x7 / ELIGIB_ANIM_STATE_OFF x2 / LP_CARD_TRACK_BASE_OFF x1 / LP_CARD_TRACK_NEXT_OFF x1 / DUAL_LABEL_RENDER_STATE_CLEAR x7 / TRIGGER_OP_PARAM_107 x1 / PLAYER_BLOCK_STRIDE x2 / gDuelFieldSlots x1 / RED_MOON_BABY_CID x1 / DNA_TRANSPLANT_CID x1 / OTOHIME_CID x1 / TSUKUYOMI_CID x1 / EQUIP_SLOT_SCORE_CAP x1 / gP1LifePoints x16 (incl. DWORD_08083d24 added per C13 fix)
  - NEW x4: GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000 / INVOKE_OP31_SUB1_PARAM_109=0x109 / ANCIENT_LAMP_CID=0x1476 / DREAMSPRITE_CID=0x148a
  - REUSE DUAL_LABEL_RENDER_STATE_CLEAR for all 7 EQUIP_NODE_ATTR_CLEAR_MASK slots (C5 fix)
- **REF_SLOTS**: 7 (3x set_equip_act_mode fn-ptr 0x08081de5 / 3x set_equip_act_alt fn-ptr 0x080905e9 / 1x check_zone_player fn-ptr 0x08083969 / 1x check_equip_pair fn-ptr 0x08083b55)
- **RENAME_SLOTS**: 4 (3x PTR_gP1LifePoints_ + DAT_0808424c->book_of_life_eligible_dispatch_state0)
- **FUNC_RENAME**: 0
- **PLATE**: 8 CJK mojibake->ASCII rewrites (tick_equip_lamp_dream_zone_activation_3state / check_effect_slot_zone_player_by_type / tick_equip_placement_bitmap_display_4state / tick_equip_activation_sprite_array_4state / tick_equip_lp_row_display_by_state / tick_equip_lamp_dream_activation_3state / dispatch_equip_display_if_confirm_state_two / dispatch_equip_display_by_type_code_or_card_id)
- **R4 disasm**: 2 blocks
  - BLK1 0x8420e/0x26: fn_eligible_book_of_life@0x08084210 (2B zero-pad at 0x420e; CID=0x1536 BOOK_OF_LIFE_CID; THUMB+1 ref at 0x09e410b8; dispatch table entry [+0x00]=CID,[+0x14]=fn_eligible+1; 2 pool DWords: 0x422c=gDuelPhaseFlags / 0x4230=0x08084234 JT base; 0x422a=0x4687 THUMB opcode NOT DWord'd; pool-fix: DAT_0808430c=gDuelPhaseFlags + LAB_08084310 code label at movs r0,#1 epilogue)
  - BLK2 0x8424c/0xcc: 5 unique sub-stubs (states 0,1,3,4 separate; state 2+5 shared at 0x080842cc); clearListing entire range + per-stub DisassembleCommand
- **createFunction**: 6 (fn_eligible_book_of_life + book_of_life_eligible_state0/1/3/4/2_5)
- **carve**: 0
- **§5.1**: 0
- **NEW constants**:
  - card_info.inc +4: ANCIENT_LAMP_CID=0x1476 / DREAMSPRITE_CID=0x148a / BOOK_OF_LIFE_CID=0x1536 / GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000
  - duel_field.inc +1: INVOKE_OP31_SUB1_PARAM_109=0x109
  - ewram.inc +1: LP_ACTIVATION_PENDING_OFF=0x1d40
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ (code) / 0 non-ASCII in [0x83450, 0x84318)
- **ROM_INCBIN before/after asm/10**: 7 -> 5 (2 eliminated: BLK1+BLK2)
- **Ghidra scripts**: RefineF10Seg9Slots.py, DisassembleF10Seg9Blocks.py, PoolFixF10Seg9.py
- **CSV sync**: yes -- fn_eligible_book_of_life + book_of_life_eligible_state0/1/3/4/2_5 (6 new functions)
- **commit**: (pending)

---

## 五、段路线图 (Seg-1..10 细节)

按照三条硬规则 (地址序 / 函数间必处理 / 0引用->§5.1) 逐段执行。

### Seg-1 [0x08079e60, 0x0807ae84) -- 19 fn, ~61 slots
- 8 ROM_INCBIN 块 (均在函数间或函数体内): 须 ref-scan 逐块分类
  - 0x08079fac/0x30, 0x0807a00c/0xe8, 0x0807a138/0x28, 0x0807a178/0x14c
  - 0x0807a3b8/0x38, 0x0807a464/0x11c, 0x0807a688/0x44, 0x0807a71c/0xf8
- **注意**: 0xa178/0x14c (332B) 和 0xa464/0x11c (284B) 较大; 0xa00c/0xe8 (232B) 次之
- 旧覆盖: 无 (新文件)

### Seg-2 [0x0807ae84, 0x0807be2c) -- 18 fn, ~47 slots
- 8 ROM_INCBIN 块 (密集):
  - 0x0807af66/0x3a, 0x0807afb8/0x110, 0x0807b4d4/0x2c, 0x0807b574/0x144
  - 0x0807b7dc/0x28, 0x0807b878/0xe0, 0x0807b9f4/0x28, 0x0807ba30/0x100
- **注意**: 0xafb8/0x110 (272B) + 0xb574/0x144 (324B) + 0xba30/0x100 (256B) 大块; 同 Seg-1 须 ref-scan
- 旧覆盖: 无

### Seg-3 [0x0807be2c, 0x0807cd68) -- 19 fn, ~68 slots
- 2 ROM_INCBIN 块:
  - 0x0807c87a/0x3e (62B), 0x0807c92c/0x158 (344B)
- **注意**: 0xc92c/0x158 是本段最大块 (344B)
- 旧覆盖: 无

### Seg-4 [0x0807cd68, 0x0807db20) -- 19 fn, ~53 slots
- 2 ROM_INCBIN + 1 switchD:
  - 0x0807d7e8/0x2c (44B), 0x0807d830/0xfc (252B)
  - switchD_0807d126 (属函数 tick_equip_activation_display_state_machine@0x0807d104; 其代码 + switchD 均在本段)
- **注意**: switchD_0807d126 的目标块可能在本段内亦可能越界至 Seg-5; 需在 disasm 前先 ref-scan 逐目标确认
- 旧覆盖: 无

### Seg-5 [0x0807db20, 0x0807f730) -- 19 fn, ~64 slots
- **最多 ROM_INCBIN** (8 inc + 2 switchD):
  - 0x0807dd68/0x30, 0x0807ddac/0x16c (364B), 0x0807df90/0x2bc (**700B! 最大**), 0x0807e398/0x2c
  - 0x0807e438/0x16c (364B), 0x0807e5d4/0x63c (**1596B! 超大**), 0x0807f280/0x3c, 0x0807f330/0x128 (296B)
  - switchD_0807ed22, switchD_0807ee92
- **注意**: 0xe5d4/0x63c (1596B) 是全文件最大 ROM_INCBIN; 须精细 ref-scan (raw + THUMB+1 每 2B step 穷举); 压缩资产偶合要剔除
- 旧覆盖: 无

### Seg-6 [0x0807f730, 0x08080ba0) -- 18 fn, ~123 slots
- 0 ROM_INCBIN + 2 switchD:
  - switchD_0807fe22, switchD_080806cc
- **注意**: 123 DAT_/DWORD_ 槽密集; switchD 目标块须 ref-scan 确认是否在本段内
- 旧覆盖: 无

### Seg-7 [0x08080ba0, 0x08082290) -- ✅ 完成 (7a commit see 4.07a; 7b commit see 4.07b)
- 2 ROM_INCBIN + 1 switchD 全部消灭 (7b: ROM_INCBIN 0x82046/fa + 0x82158/138; switchD 已 decoded)
- **7b highlights**: route_penguin_soldier_equip_display (FS table CID=0x1200) + 6 sub-stubs; 13 mojibake->ASCII; 42 EQ + 6 RENAME

### Seg-8a [0x08082290, 0x08082b18) -- ✅ 完成 (commit see 4.08a)
- 2 ROM_INCBIN 全部消灭 (BLK1 fn_eligible_two_pronged_attack + BLK2 4 sub-stubs); 6 mojibake->ASCII; EQ38/RENAME10/PLATE6

### Seg-8b [0x08082b18, 0x08083450) -- ✅ 完成 (commit see 4.08b)
- 0 ROM_INCBIN (全段无 incbin)
- EQ56/RENAME8/PLATE6 (6 mojibake->ASCII incl. 2 ARM-corrected STATE_OFFSET=0x4b0 plates)

### Seg-9 [0x08083450, 0x08084318) -- ✅ 完成 (commit see 4.09)
- 2 ROM_INCBIN 全部消灭 (BLK1 fn_eligible_book_of_life + BLK2 5 unique sub-stubs)
- EQ81/REF7/RENAME4/PLATE8 (8 mojibake->ASCII); NEW: ANCIENT_LAMP_CID/DREAMSPRITE_CID/BOOK_OF_LIFE_CID/GEARFRIED_IRON_KNIGHT_CID_SHIFTED/INVOKE_OP31_SUB1_PARAM_109/LP_ACTIVATION_PENDING_OFF
- Pool fix: DAT_0808430c=gDuelPhaseFlags + LAB_08084310 code label (PoolFixF10Seg9.py)

### Seg-10 [0x08084318, 0x080850d8) -- 19 fn, ~55 slots
- 5 ROM_INCBIN (fn-eligible 特征):
  - 0x0808474e/0x2a (42B), 0x08084790/0x164 (356B), 0x08084918/0x180 (384B)
  - 0x08084af2/0x2a (42B), 0x08084b34/0x10c (268B)
- **注意**: 5 块集中在末尾 [0x8474e..0x84c40); 模式类似 file 09 Seg-10 fn_eligible stubs; THUMB+1 ref-scan 判定
- 旧覆盖: 无

---

## §5.1 零引用孤儿块登记

(待各段 ref-scan 确认后在此登记 0-引用块)

| 块地址 | 大小 | ref-scan raw | ref-scan THUMB+1 | 判定 | 备注 |
|--------|------|-------------|-----------------|------|------|
| (空)   |      |             |                 |      |      |

---

## 六、相关文档

| 文档 | 说明 |
|------|------|
| `doc/dev/methodology/refine-loop.md` | 完整方法论 R1-R9 + 三条硬规则 |
| `doc/dev/p5-refine-00-system-str-vija.md` | R1-R9 详版 + §一 全文 |
| `doc/dev/p5-refine-05-equip-eligibility-a.md` | 复用资产完整清单 |
| `doc/dev/p5-refine-09-equip-lp-display.md` | file 09 全记录 (fn_eligible stub 分类范式) |
| `doc/dev/refine-progress.md` | 25 文件总进度 |
| `doc/dev/refine/` | 各段 proposal.md + review.md |
| `asm/10_equip_effect_dispatch.s` | 目标文件 (19983 行) |
