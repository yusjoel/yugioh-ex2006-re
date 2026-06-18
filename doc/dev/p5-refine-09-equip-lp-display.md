# 函数/数据细化计划 — `asm/09_equip_lp_display.s`

> 阶段目标: 把 `asm/09_equip_lp_display.s` (ROM `0x0806e76c ~ 0x08079e60`, slot sprite type11 +
> 装备 LP 计数显示状态机 + equip zone bitmap 派发 + Neo Daedalus OAM) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **10** 个文件 (file 00..08 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..08 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用->§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..08 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **ROM_INCBIN 分类核心 (file 06/07/08 已确认 N 次)**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - **`0x09e4xxxx`/`0x09e3xxxx` = card effect handler dispatch table** (entry 0x18B = `[CID, fn_activate(+1), pad, fn_eligible(+1), pad, pad]`,
    FS 运行时加载); **fn_eligible 块的 CID 在 fn_ptr 地址 -0xc 位置** (别取错下一 entry, file 07 Seg-5 教训); THUMB+1 命中核 fn_ptr-0xc 处 CID
    (python 实读, card-stats.s 坐实) -> 真引用 -> R4 disasm。
  - **file 09 特征 (equip LP display / OAM)**: 大量 ROM_INCBIN 块 (0x28..0x1ec 不等) 多为
    **raw-addr 跳转表** (函数间 dispatch table, .word fn_addr 形式, 被 ldr+MOV PC,r0 或 ldr+bx 引用 ->
    carve 进 rom.s 结构化) 或 **fn_eligible THUMB stubs** (被 0x09e4xxxx 表 THUMB+1 引用 -> R4 disasm)。
    ref-scan 命中是 raw fn_addr (code-addr, non-THUMB) -> carve; 命中是 THUMB|1 fn-ptr -> disasm。逐块据实判。
  - 块内可能多 sub-fn (经 dispatch raw 指针/MOV PC,r0/switchD 到达); 仅 raw=0 且 THUMB+1=0 -> §5.1。
  详见 memory `feedback-card-effect-handler-table-thumb-ref` + `refine-carve-rom-tables-immediately`。
- **switchD 跳转表 (file 09 含 4: 0x6e8b6/0x7514a/0x7638c/0x77144)**: jump table 目标裸 THUMB 地址 -> R4 disasm 逐 stub
  (file 00 Seg-5c 范式); case stub 可级联 bl ROM_INCBIN helper。
- **R4 disasm 范式**: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand; literal pool createDWord 强制 split。
- **机器码核 (file 07 Seg-8/9 教训, 必做)**: disasm fn 比较+分支指令独立解码; 函数名运算符/偏移/卡名与机器码一致;
  **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核 (file 07/08 反复抓误标)**: 标 **new** CID 逐一 grep 0 命中; 标 **reuse** 逐一 grep 确存在; 记证据。
  **C5 偏移放宽** (不同 base `*_OFF` 各建独立); **卡 ID/掩码/位域/阈值非偏移严格去重** (值碰撞必复用, 语义截然不同各建独立, 读消费者裁定)。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集 (穷举对账); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实 (card record# != slot_id); passcode 逐一 python 核对; 未分配->中性 `cid_<hex>`, 勿臆造 (红线 3)。
- **误名警觉 (file 06/07/08 高频)**: 函数名/plate 称的卡名/全局与函数体矛盾即误名;
  gEquipChainSlotRefs=0x0201bb90 常被误称; 误名走 FUNC_RENAME/CONST_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 每个 FUN_ 地址查现名替换; 落地后 grep == 0。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04 (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05 Seg-8 6 槽 / asm/06/07/08 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责)。
- **0x09e3fXXX 区 raw `.word`+EOL 兄弟惯例**: 0x09e3fXXX FS ROM 地址槽 -> RENAME_ONLY + ASCII EOL (不建 equate; 沿用 file 08 Seg-6 Ruling A)。

**file 02..08 已建可复用资产** (新建前必 grep): 见 `p5-refine-05-equip-eligibility-a.md` §一 (ewram/duel_field/card_info ~600+ CID/oam_attr/gl_scrollbar/bitops/全局) + file 06/07/08 新增 (equip_lp_delta/g2d_tags/gfx_resource/name_input/oam_attr 扩展等)。

---

## 二、落地工作流 (pipeline)

同 file 00..08 doc §二:
```
备份 .rep -> Ghidra 脚本 (RefineF09Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
-> ghidra-export-range.bat 080000c0 084c7637 -> inject_modes.py -> split_all_s.py
-> build + byte-identical SHA1 9689337d -> (改/建函数名才) ExportFunctionInventory + sync CSV -> commit
```
3-agent: executor -> reviewer (C1-C13) -> fixer (模式A/模式B)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (09_equip_lp_display.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN/switch | 状态 | commit |
|-----|------|-----|--------|-------------------|------|--------|
| 1 | 0x6e76c..0x6ff50 | 20 | 74 | 6 inc + 1 sw (0x6e8b6) | ✅ | 08b3db1 |
| 2 | 0x6ff50..0x7104c | 20 | 75 | 1 inc (0x70476/90) | ✅ | 79000e6 |
| 3 | 0x7104c..0x719fc | 20 | 39 | 2 inc (0x716fa/42, 0x71754/9c) | ✅ | c1c490d |
| 4a | 0x719fc..0x72404 | 9 | 40 | 4 inc (0x71a92/2a, 0x71ad4/108, 0x71f56/32, 0x72004/100) | ✅ | (see §四) |
| 4b | 0x72404..0x72d20 | 11 | 26 | 4 inc (0x72404/2c, 0x72444/138, 0x72594/1a0, 0x7274c/124) | ✅ | (see §四) |
| 5 | 0x72d20..0x74338 | 20 | 83 | 10 inc (0x7313e/2a, 0x731e4/c4, 0x7356c/48, 0x73628/138, 0x73864/28, 0x73900/15c, 0x73b1c/30, 0x73bc8/1bc, 0x73fde/2e, 0x74080/178) | ⬜ | |
| 6 | 0x74338..0x752cc | 20 | 65 | 2 inc (0x74852/4a, 0x74914/cc) + 1 sw (0x7514a) | ⬜ | |
| 7 | 0x752cc..0x7629c | 19 | 46 | 6 inc (0x75378/28, 0x75414/a4, 0x75d0c/2c, 0x75d5c/214, 0x75f8e/2e, 0x75fe0/17c) | ⬜ | |
| 8 | 0x7629c..0x7738c | 19 | 70 | 4 inc (0x765b0/2c, 0x765f0/19c, 0x767aa/32, 0x767f8/110) + 2 sw (0x7638c, 0x77144) | ⬜ | |
| 9 | 0x7738c..0x7850c | 19 | 67 | 9 inc (0x7757c/2c, 0x775d0/a8, 0x779e4/30, 0x77a3c/120, 0x77b88/c8, 0x77ecc/5c, 0x77f44/c0, 0x782c0/2c, 0x78368/14c) | ⬜ | |
| 10 | 0x7850c..0x79e60 | 19 | 88 | 10 inc (0x78a90/44, 0x78b24/d4, 0x78fde/f6, 0x79148/1ec, 0x793ac/154, 0x7965c/50, 0x796c4/10c, 0x79a1c/48, 0x79adc/13c, 0x79c9c/1c4) | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
**58 ROM_INCBIN + 4 switchD** -- 逐块 ref-scan 按 §一 分类 (handler-table THUMB+1->disasm / dispatch-table raw-ref->carve / switchD->R4 disasm / 0 引用->§5.1)。
**重段提示**: Seg-5 (10 ROM_INCBIN, 83 槽) 和 Seg-10 (10 ROM_INCBIN, 88 槽) 最重, 可能需拆 Seg-Na/Nb;
Seg-4 (8 ROM_INCBIN, 66 槽) 和 Seg-9 (9 ROM_INCBIN, 67 槽) 次重; Seg-8 (4 inc + 2 sw, 70 槽) 含双 switchD。

---

## 四、逐段完成记录

### 4.05 Seg-4b 完成记录

- 范围: `[0x08072404, 0x08072d20)` -- 11 fn (fn_eligible_fiend_comedian_2404 + 5×last_turn_sub_stubs + fn_eligible_last_turn_2540 + 6×vampire_sub_stubs + fn_eligible_vampire_lord_lady_26f4 + 6×equip_zone_sub_stubs + dispatch_lp_delta_display_by_card_pair_diff + tick_dragon_summon_display_if_monster_zones_occupied + 2×fn_ptr_dispatch_table_anchors)
- EQ=23 (22 REUSE + 1 NEW: LP_DELTA_6000=0x1770)
- REF=0
- RENAME=3 (DAT_08072444->last_turn_dispatch_sub_stubs_2444; DAT_08072594->vampire_dispatch_sub_stubs_2594; DAT_0807274c->equip_zone_sub_stubs_274c)
- FUNC_RENAME=0
- PLATE=1 (CJK mojibake deferred from Seg-4a @0x08072ce4 tick_dragon_summon_display_if_monster_zones_occupied; ASCII rewrite: "Equip chain dragon-summon display gate driver...")
- DISASM=4 blocks:
  - B5: fn_eligible_fiend_comedian_2404 @ 0x08072404 (ROM_INCBIN 0x72404/0x2c; FS table THUMB+1 @GBA:0x09e41078; CID=0x151d Fiend Comedian)
  - B6: 5 sub-stubs last_turn_sub_2444..2534 + fn_eligible_last_turn_2540 @ 0x08072444..0x08072573 (ROM_INCBIN 0x72444/0x138; 5-entry dispatch table @0x72430..0x72443)
  - B7: 6 sub-stubs vampire_sub_2594..26bc + fn_eligible_vampire_lord_lady_26f4 @ 0x08072594..0x08072733 (ROM_INCBIN 0x72594/0x1a0; 6-entry dispatch table @0x7257c..0x72593)
  - B8: 6 sub-stubs equip_zone_sub_274c..2856 @ 0x0807274c..0x0807286f (ROM_INCBIN 0x7274c/0x124; 6-entry dispatch table @0x72734..0x7274b)
- carve=0; §5.1=0
- 新常量: constants/card_info.inc (+2: FIEND_COMEDIAN_CID=0x151d, LAST_TURN_CID=0x151e); constants/duel_field.inc (+1: LP_DELTA_6000=0x1770)
- 踩坑:
  - pool 地址 0x0007xxxx->0x0807xxxx (GBA 地址空间未映射到 0x0007xxxx)
  - force_dword 8-byte clearListing 覆写相邻 stub 首 4 字节 -> 改 4-byte clearListing
  - CodeUnitInsertionException Java 异常须显式 import + except 子句
  - B6/B7 多处隐藏代码区 (分支目标在 pool DWord 之后) 须逐一 DisassembleCommand
  - LAB_080726e6/e8 均在 0x726e6..0x726f3 区域; DisassembleCommand 从 0x726d2 仅到达 0x726e8 不到 0x726e6 -> 补 DisassembleCommand @ 0x726e6
  - pool 小值 (0x1d6c/0x1d70/0x1daa/0x1ce8/0x10d0) 不满 0x02000000 被初始扫描漏掉 -> 手补
  - 多轮 fix 脚本: RefineF09Seg4bSlots.py -> PoolFix -> DisasmFix -> LabelFix2/3 -> ResetAndFix -> Fix4
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.04 Seg-4a 完成记录

- 范围: `[0x080719fc, 0x08072404)` -- 9 fn (setup_equip_oam_entry_for_neo_daedalus_zone14 + dispatch_field_spell_display_by_activation_state + dispatch_spirit_monster_zone_sprite_by_card_id + tick_equip_activation_zone13_oam_state + enqueue_slot_card_sprite_if_effect_node_active + dispatch_equip_zone_sprite_by_zone_bit4_state + refresh_equip_zone_bitmap_with_full_mask + tick_equip_lp_row_sprite_extended_state + dispatch_banisher_equip_zone_sprite_by_target_slot)
- EQ=38 (36 REUSE + 2 NEW: YAMATA_DRAGON_CID=0x1501 / DARK_DUST_SPIRIT_CID=0x1526)
- REF=0
- RENAME=2 (DAT_08071ad4 -> neo_daedalus_z14_sub_stubs_1ad4; DAT_08072004 -> field_spell_dispatch_sub_stubs_2004)
- FUNC_RENAME=0
- PLATE=1 (PLATE-1: dispatch_spirit_monster_zone_sprite_by_card_id @0x08071d64 -- callee-swap fix: 0x14ff Yata-Garasu and 0x1501 Yamata Dragon had swapped callee names)
- PLATE-2 (CJK mojibake @0x08072ce4 tick_dragon_summon_display_if_monster_zones_occupied) deferred to Seg-4b
- DISASM=4 blocks:
  - B1: fn_eligible_fiber_jar_1a94 @ 0x08071a94 (ROM_INCBIN 0x71a92/0x2a; FS table THUMB+1 ref @GBA:0x09e43c88; CID=0x14fb Fiber Jar)
  - B2: 7 sub-stubs field_spell_sub_1ad4..1bbc @ 0x08071ad4..0x08071bdb (ROM_INCBIN 0x71ad4/0x108; 6-entry raw dispatch table @ 0x71abc..0x71ad0)
  - B3: fn_eligible_fengsheng_mirror_1f58 @ 0x08071f58 (ROM_INCBIN 0x71f56/0x32; FS table THUMB+1 ref @GBA:0x09e40f58; CID=0x1509 Fengsheng Mirror)
  - B4: 11 sub-stubs field_spell_sub_2004..20f4 @ 0x08072004..0x08072103 (ROM_INCBIN 0x72004/0x100; 32-entry raw dispatch table @ 0x71f88..0x72000)
- carve=0; §5.1=0
- 新常量: constants/card_info.inc (+5: YATA_GARASU_CID=0x14ff / YAMATA_DRAGON_CID=0x1501 / HINO_KAGU_TSUCHI_CID=0x1504 / FENGSHENG_MIRROR_CID=0x1509 / DARK_DUST_SPIRIT_CID=0x1526)
- 踩坑: 3 轮 pool fix (5+3 个 DWord/Word 强制): B2 sub_1b64 pool @0x08071b90..0x08071b9b (3 DWords); B4 sub_2088 pool @0x080720a4..0x080720ab (2 DWords); B2 sub_1ba0 dead bytes @0x08071b9c (1 DWord) + 2-byte align pad @0x08071bb6 (1 Word) + DAT_08071bb8=0x0201e1c8 (1 DWord)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: a9aa009

---

### 4.03 Seg-3 完成记录

- 范围: `[0x0807104c, 0x080719fc)` -- 20 fn, dispatch_equip_chain_effect_slot + enqueue_field_slot_overlay + enqueue_eligible_slot + tick_equip_lp + Neo Daedalus OAM cluster
- EQ=35 (33 REUSE + 2 NEW: EQUIP_ZONE_WORD_MASK=0x00f0ffff / FREED_THE_MATCHLESS_GENERAL_CID=0x000014c4)
- REF=0
- RENAME=4 (DWORD_0807129c -> check_effect_slot_equip_zone_pattern_ptr; DWORD_08071538 -> invoke_effect_node_with_active_flag_3arg_ptr_1538 (`_1538` suffix per C6 fix); PTR_DAT_08071740 -> equip_lp_disp_sub_table; DAT_08071754 -> equip_lp_sub_stubs_754)
- FUNC_RENAME=0; PLATE=2 (PLATE-1: L6141 CJK mojibake -> ASCII rewrite for dispatch_equip_lp_bar_or_bitmap_by_zone_type; PLATE-2: L6209 stale FUN_08090714->count_effect_node_zone_activations + FUN_08096a4c->set_equip_activation_state_by_mode__08096a4c)
- DISASM=2 blocks:
  - Block1: eligible_dragged_down_into_grave_16fc @ 0x080716fc (fn_eligible stub; CID=0x14e8 Dragged Down into the Grave; FS table THUMB+1 ref @GBA:0x09e40e98); literal pool 4 DWords
  - Block2: 5 sub-stubs equip_lp_sub_{754,77c,78a,7a4,7c4} @ 0x08071754..0x080717ef (raw dispatch; MOV PC,r0 indirect via PTR_DAT_08071740; shared epilogue @0x080717e8); per-stub DisassembleCommand; Block2PoolFix for 4 literal pool DWords (dat_08071774/778/7a0/7b8_pool)
- carve=0; §5.1=0
- 新常量: constants/duel_field.inc (+1: EQUIP_ZONE_WORD_MASK); constants/card_info.inc (+2: FREED_THE_MATCHLESS_GENERAL_CID, DRAGGED_DOWN_INTO_GRAVE_CID)
- 踩坑: Block2 literal pool words exported as .byte sequences causing "invalid offset" GAS errors; fixed by RefineF09Seg3Block2PoolFix.py (createDWord + label for 4 pool words)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: c1c490d

---

### 4.02 Seg-2 完成记录

- 范围: `[0x0806ff50, 0x0807104c)` -- 22 fn, tick_equip_partner_lp_indicator + invoke_equip_oam_setup + dispatch_equip_lp_or_hand_sprite cluster
- EQ=71 (61 REUSE + 10 NEW: GUARDIAN_BAOU_CID/LEGENDARY_FIEND_CID/INSECT_PRINCESS_CID/AQUA_SPIRIT_CID/THUNDER_CRASH_CID/ENCHANTED_ARROW_CID/TOKEN_THANKSGIVING_CID/TOKEN_FEASTEVIL_CID/GRYPHONS_FEATHER_DUSTER_CID/CYCLONE_BOOMERANG_CID)
  - DAT_08070754 = OAM_SPRITE_CODE_P1_ACTIVATION (0x8019, REUSE; C4/C5 fix from NEEDS_FIX #1)
  - DWORD_080703b8 = gDuelPhaseFlags (added; C13 fix from NEEDS_FIX #2)
  - DWORD_08070edc = gP1HandSlotArray (corrected from double-count; C13 fix from NEEDS_FIX #3)
- REF=3 (PTR_gP1LifePoints x2 + gEquipChainSlotRefs x1)
- RENAME=3 (fn-ptr THUMB+1 slots: check_equip_slot_eligible_by_side_and_type_query x2 + invoke_effect_node_with_active_flag_3arg x1)
- FUNC_RENAME=1 (0x08070900 -> check_zone_tile_count_and_set_summon_restriction_flag; label created, no Ghidra fn object -- fn body was embedded in build_equip_chain_entries_from_zone_slots range; CSV row added manually)
- PLATE=0
- DISASM=1 block: fn_eligible_bazoo_the_soul_eater @ 0x08070478 (ROM_INCBIN 0x70476/0x90 eliminated) + literal pool words player_stride_pool_0514/gduel_slots_pool_0518; also re-disasmed check_zone_tile_count fn body 0x08070900..0x08070971 and test_equip_zone body 0x0807097c..0x080709ff (clearListing overspill fix)
- carve=0; §5.1=0
- 新常量: constants/card_info.inc (+11: 10 CIDs + BAZOO_THE_SOUL_EATER_CID)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see §三 table)

---

### 4.01 Seg-1 完成记录

- 范围: `[0x0806e76c, 0x0806ff50)` — 20 fn, enqueue_slot_sprite_type11 + dispatch_equip_zone_token/lp + state machine 簇
- EQ=40 (33 reuse + 7 NEW: BIG_MARCH_OF_ANIMALS_CID/CREATURE_SWAP_CID/ICID_RESERVED_D/ICID_RESERVED_E/LP_D_TRIBE_BLOCK_OFF/LP_P2_LOOP_CEIL_OFF/OAM_EQUIP_SPRITE_P2_1A)
- REF=34 (gP1LifePoints×12, gDuelPhaseFlags×9, gDuelFieldSlots×10, gP1HandSlotArray×1, gEquipChainSlotRefs×2)
- RENAME=3 (DAT_0806f054/fa08/fe88 → eligible_sub_stubs_f054/fa08/fe88)
- FUNC_RENAME=0; PLATE=2 (FUN_0806e898→dispatch_equip_chain_state_sprite_by_slot; (gP1LifePoints)→(gDuelPhaseFlags))
- DISASM=6 blocks (Block1: eligible_creature_swap_f008; Block2: 6 dispatch sub-stubs; Block3: eligible_destiny_board_f85c; Block4: 10 dispatch sub-stubs; Block5: eligible_cathedral_of_nobles_fdec; Block6: 8 dispatch sub-stubs) + 3 dispatch tables labeled
- carve=0; §5.1=0 (all 6 blocks have confirmed refs)
- 新常量: constants/card_info.inc (+4), constants/ewram.inc (+2), constants/oam_attr.inc (+1)
- Literal pool fix: FixF08Seg10AndF09Seg1LiteralPools.py (43 DWORDs) + FixF08Seg10CidStateLiteralPools2.py (8 DWORDs) + FixF08ThumbPlusOneLabels.py (2 THUMB+1 labels restored)
- byte-identical: ✅ SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: 08b3db1

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 09 范围 `[0x0806e76c, 0x08079e60)` (196 named fn, ~673 auto-name 槽, 58 ROM_INCBIN, 4 switchD)
> 按**函数数**均分 10 段 (~19-20 fn/段, 边界=函数结束处)。

| Seg | 地址范围 | ~fn | ~slots | 块/switchD | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x6e76c..0x6ff50 | 20 | 74 | 6 inc + 1 sw(0x6e8b6) | enqueue_slot_sprite_type11 + dispatch_equip_zone_token/lp + state machine 簇; switchD_0806e8b6 |
| Seg-2 | 0x6ff50..0x7104c | 20 | 75 | 1 inc(0x70476/90) | tick_equip_partner_lp_indicator + invoke_equip_oam_setup + dispatch_equip_lp_or_hand_sprite 簇 |
| Seg-3 | 0x7104c..0x719fc | 20 | 39 | 2 inc(0x716fa/42, 0x71754/9c) | dispatch_equip_chain_effect_slot + enqueue_field_slot_overlay + enqueue_eligible_slot 簇; Neo Daedalus OAM |
| Seg-4 | 0x719fc..0x72d20 | 20 | 66 | 8 inc(0x71a92/2a, 0x71ad4/108, 0x71f56/32, 0x72004/100, 0x72404/2c, 0x72444/138, 0x72594/1a0, 0x7274c/124) | setup_equip_oam_for_neo_daedalus + dispatch_field_spell_display + dispatch_spirit_monster_zone 簇; **重段** 8 块 |
| Seg-5 | 0x72d20..0x74338 | 20 | 83 | 10 inc(0x7313e/2a, 0x731e4/c4, 0x7356c/48, 0x73628/138, 0x73864/28, 0x73900/15c, 0x73b1c/30, 0x73bc8/1bc, 0x73fde/2e, 0x74080/178) | tick_equip_lp_display_state_by_slot + setup_equip_oam_by_placeable_card + tick_equip_lp_display_bitmap 簇; **最重段** 10 块, 建议拆 Seg-5a/5b |
| Seg-6 | 0x74338..0x752cc | 20 | 65 | 2 inc(0x74852/4a, 0x74914/cc) + 1 sw(0x7514a) | apply_equip_activation_for_zone + dispatch_equip_zone_bitmap_or_neo_daedalus + dispatch_equip_display_state 簇; switchD_0807514a |
| Seg-7 | 0x752cc..0x7629c | 19 | 46 | 6 inc(0x75378/28, 0x75414/a4, 0x75d0c/2c, 0x75d5c/214, 0x75f8e/2e, 0x75fe0/17c) | enqueue_effect_card_sprite + tick_graveyard_spell_display + dispatch_effect_activation 簇; 含大 inc 0x75d5c/0x214 |
| Seg-8 | 0x7629c..0x7738c | 19 | 70 | 4 inc(0x765b0/2c, 0x765f0/19c, 0x767aa/32, 0x767f8/110) + 2 sw(0x7638c, 0x77144) | tick_equip_zone_bitmap_display + enqueue_equip_zone_sprite_zone_type15 + dispatch_equip_effect_node 簇; **双 switchD** |
| Seg-9 | 0x7738c..0x7850c | 19 | 67 | 9 inc(0x7757c/2c, 0x775d0/a8, 0x779e4/30, 0x77a3c/120, 0x77b88/c8, 0x77ecc/5c, 0x77f44/c0, 0x782c0/2c, 0x78368/14c) | invoke_setup_equip_oam + dispatch_equip_lp_bar_display + dispatch_equip_banisher 簇; 9 inc **重段** |
| Seg-10 | 0x7850c..0x79e60 | 19 | 88 | 10 inc(0x78a90/44, 0x78b24/d4, 0x78fde/f6, 0x79148/1ec, 0x793ac/154, 0x7965c/50, 0x796c4/10c, 0x79a1c/48, 0x79adc/13c, 0x79c9c/1c4) | dispatch_equip_slot_activation_seq + dispatch_equip_slot_sprite_by_zone_flag + tick_neo_daedalus_equip_lp 簇; **最重段** 10 块含 0x1ec/0x1c4/0x154 大表, 建议拆 Seg-10a/10b |

执行约定同 file 00..08: 每段走 §二 pipeline; 地址序不回头; 每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-05-equip-eligibility-a.md` (file 05: 复用资产总表)
- `doc/dev/p5-refine-07-equip-effect-chain.md` (file 07: handler-table disasm 大批量 / CID@fn_ptr-0xc / 机器码核 / 误名订正)
- `doc/dev/p5-refine-08-equip-oam-neodaed.md` (file 08: OAM sprite 数据表 carve / switchD 5 处 / 误名订正 8 次)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
