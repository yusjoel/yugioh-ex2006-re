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
| 5a | 0x72d20..0x73a5c | 13 | 61 | 6 inc (0x7313e/2a, 0x731e4/c4, 0x7356c/48, 0x73628/138, 0x73864/28, 0x73900/15c) | ✅ | (see §四) |
| 5b | 0x73a5c..0x74338 | 8 | 27 | 4 inc (0x73b1c/30, 0x73bc8/1bc, 0x73fde/2e, 0x74080/178) | ✅ | (see §四) |
| 6 | 0x74338..0x752cc | 20 | 65 | 2 inc (0x74852/4a, 0x74914/cc) + 1 sw (0x7514a) | ✅ | (see §四) |
| 7 | 0x752cc..0x7629c | 19 | 46 | 6 inc (0x75378/28, 0x75414/a4, 0x75d0c/2c, 0x75d5c/214, 0x75f8e/2e, 0x75fe0/17c) | ✅ | (see §四) |
| 8 | 0x7629c..0x7738c | 19 | 70 | 4 inc (0x765b0/2c, 0x765f0/19c, 0x767aa/32, 0x767f8/110) + 2 sw (0x7638c, 0x77144) | ✅ | 1e38556 |
| 9a | 0x7738c..0x77c50 | 9+3new | 31 | 5 inc (0x7757c/2c, 0x775d0/a8, 0x779e4/30, 0x77a3c/120, 0x77b88/c8) | ✅ | (see §四) |
| 9b | 0x77c50..0x7850c | 10+2new | 36 | 4 inc (0x77ecc/5c, 0x77f44/c0, 0x782c0/2c, 0x78368/14c) | ✅ | 5f27863 |
| 10a | 0x7850c..0x79500 | 13+3new | 63 | 5 inc (0x78a90/44, 0x78b24/d4, 0x78fde/f6, 0x79148/1ec, 0x793ac/154) | ✅ | be48d12 |
| 10b | 0x79500..0x79e60 | 4+3new | 24 | 5 inc (0x7965c/50, 0x796c4/10c, 0x79a1c/48, 0x79adc/13c, 0x79c9c/1c4) | ✅ | (see §四) |

**FILE 09 COMPLETE -- all 10 segments done; asm/09 ROM_INCBIN=0; SHA1 9689337d byte-identical**

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
**58 ROM_INCBIN + 4 switchD** -- 逐块 ref-scan 按 §一 分类 (handler-table THUMB+1->disasm / dispatch-table raw-ref->carve / switchD->R4 disasm / 0 引用->§5.1)。
**重段提示**: Seg-5 (10 ROM_INCBIN, 83 槽) 和 Seg-10 (10 ROM_INCBIN, 88 槽) 最重, 可能需拆 Seg-Na/Nb;
Seg-4 (8 ROM_INCBIN, 66 槽) 和 Seg-9 (9 ROM_INCBIN, 67 槽) 次重; Seg-8 (4 inc + 2 sw, 70 槽) 含双 switchD。

---

## 四、逐段完成记录

### 4.12 Seg-1 Remediation Cluster-1 完成记录

> Remediation landing: 2026-06-20. Eliminates partial-disasm ROM_INCBIN/.byte
> residue left by commit 08b3db1 in sub-stub cluster [0x0806f008..0x0806f1c4).
> Cluster-2 [0x6f85e..0x6fef2] and Cluster-3 [0x6fdec..0x6ff4f] deferred to
> F09-Seg1R2 and F09-Seg1R3 proposals.

- 范围: `[0x0806f008, 0x0806f1c4)` Cluster-1 sub-stub group
- DISASM=7 items (5 ROM_INCBIN + 2 .byte blocks):
  - B2d: equip_disp_sub_f188 body + shared epilogue @ 0x0806f18a (ROM_INCBIN 0x6f18a/0x3a; 27 instrs; creates LAB_0806f1b6/LAB_0806f1b8 for other stubs)
  - B2c: equip_disp_sub_f0cc body + b+pad @ 0x0806f0ce (ROM_INCBIN 0x6f0ce/0xb2 + b+pad 0x6f180..0x6f183; 83 instrs)
  - B2b: equip_disp_sub_f0ac body + b+pad @ 0x0806f0ae (ROM_INCBIN 0x6f0ae/0x12 + b+pad 0x6f0c0..0x6f0c3; 10 instrs)
  - B2a: equip_disp_sub_f078 body + b+pad @ 0x0806f07a (ROM_INCBIN 0x6f07a/0x22 + b+pad 0x6f09c..0x6f09f; 17 instrs)
  - B1: eligible_creature_swap_f008 body @ 0x0806f00a (ROM_INCBIN 0x6f00a/0x32; code 0x6f00a..0x6f031 20 instrs; computed jump stops DisassembleCommand; pad 0x6f032..0x6f033 .zero 2; createDWord @ 0x6f034+0x6f038)
  - B2e: eligible_sub_stubs_f054 body @ 0x0806f056 (.byte 0x10; 7 instrs)
  - B2f: equip_disp_sub_f066 body @ 0x0806f068 (.byte 0x10; 7 instrs)
- EQ=0 (no new equates; EQ_SLOTS from B1 pool handled via REF)
- REF=2 (gduel_phase_f034@0x0806f034->gDuelPhaseFlags=0x0201b290 REUSE ewram.inc; equip_disp_tbl_f038@0x0806f038->equip_disp_table_f03c=0x0806f03c REUSE existing label)
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- 新常量: none (all pool refs use existing gDuelPhaseFlags + equip_disp_table_f03c label)
- Ghidra script: `tools/ghidra-labeling/DisassembleF09Seg1RCluster1.py`
- ROM_INCBIN before: 35; after: 30 (reduced by 5 Cluster-1 blocks)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

> Remediation status after this landing:
> - Cluster-1 [0x6f008..0x6f1c4]: DONE (this record)
> - Cluster-2 [0x6f85e..0x6fef4]: 9 ROM_INCBIN + 11 .byte bodies PENDING (F09-Seg1R2)
> - Cluster-3 [0x6ff0a..0x6ff50]: .byte blocks PENDING (F09-Seg1R3, simple)

---

### 4.13 Seg-1 Remediation Cluster-2 完成记录

> Remediation landing: 2026-06-20. Eliminates all 9 ROM_INCBIN + 11 .byte companion blocks
> in [0x0806f85e..0x0806ff0a) -- two fn_eligible stubs (Destiny Board / Cathedral of Nobles)
> and their dispatch sub-stub clusters. Review noted 1 missed block (equip_lp_sub_fa4c .byte
> 0x6fa4e/0x10) which was added as Step A2b before landing.

- 范围: `[0x0806f85e, 0x0806ff0a)` Cluster-2 two-cluster group
- Cluster-2A: Destiny Board (CID=0x1468) eligible_destiny_board_f85c + dispatch stubs
  - B1: eligible_destiny_board_f85c body @ 0x0806f85e (ROM_INCBIN 0x6f85e/0x136; 114 instrs via 2-script fix; multi-pass CID triplet handling)
  - B2: eligible_sub_stubs_fa08 body + b+pad @ 0x0806fa0a (ROM_INCBIN 0x6fa0a/0x36 + b+pad 0x6fa40)
  - B2a: equip_lp_sub_fa4c body @ 0x0806fa4e (.byte 0x10; added per review #1)
  - B3: equip_lp_sub_fa5e body @ 0x0806fa62 (ROM_INCBIN 0x6fa62/0x12)
  - B4: equip_lp_sub_fa74 body @ 0x0806fa78 (ROM_INCBIN 0x6fa78/0x8c; 4 createDWord)
  - B5: equip_lp_sub_fb14 body @ 0x0806fb16 (ROM_INCBIN 0x6fb16/0x32; 1 createDWord)
  - B2c: equip_lp_sub_fb4c body @ 0x0806fb4e (.byte 0xa)
  - B2d: equip_lp_sub_fb58 body @ 0x0806fb5a (.byte 0xa)
  - B2e: equip_lp_sub_fb64 body @ 0x0806fb66 (.byte 0xa)
  - B2f: equip_lp_sub_fb70 body @ 0x0806fb72 (.byte 0x4)
  - B2g: equip_lp_sub_fb76 body + shared epilogue @ 0x0806fb78 (.byte 0x10; disasm FIRST)
- Cluster-2B: Cathedral of Nobles (CID=0x146f) eligible_cathedral_of_nobles_fdec + dispatch stubs
  - B6: eligible_cathedral_of_nobles_fdec body @ 0x0806fdee (ROM_INCBIN 0x6fdee/0x26; 2 createDWord)
  - B7: eligible_sub_stubs_fe88 body + b+pad @ 0x0806fe8a (ROM_INCBIN 0x6fe8a/0x4a + b+pad 0x6fed4; 1 createDWord)
  - B8: equip_chain_act_sub_fedc body @ 0x0806fede (ROM_INCBIN 0x6fede/0x12)
  - B9: equip_chain_act_sub_fef0 body @ 0x0806fef2 (ROM_INCBIN 0x6fef2/0x18)
  - B7c: equip_chain_act_sub_ff0a body @ 0x0806ff0c (.byte 0xe)
  - B7d: equip_chain_act_sub_ff1a body @ 0x0806ff1c (.byte 0x10)
  - B7e: equip_chain_act_sub_ff2c body @ 0x0806ff2e (.byte 0xe)
  - B7f: equip_chain_act_sub_ff3c body @ 0x0806ff3e (.byte 0x8)
  - B7g: equip_chain_act_sub_ff46 body + shared epilogue @ 0x0806ff48 (.byte 0x4 + .word 0x4708; disasm FIRST)
- DISASM=20 items (9 ROM_INCBIN + 11 .byte companion blocks); b+pad words decoded byte-identical
- EQ=15 (11 REUSE + 4 NEW): PLAYER_BLOCK_STRIDE/gDuelFieldSlots/SPIRIT_MESSAGE_I_CID/
  SPIRIT_MESSAGE_L_CID/gDuelPhaseFlags (x4 slots)/GRAVEROBBER_CID/EQUIP_PHASE_FRAME_OFF (REUSE);
  OAM_EQUIP_LP_SPRITE_P1_5E=0x805e (NEW, 3 slots) / SPIRIT_MESSAGE_N_CID=0x1498 (NEW) /
  SPIRIT_MESSAGE_A_CID=0x1499 (NEW) / CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d (NEW)
- REF=2 (equip_lp_tbl_f990->equip_lp_disp_table_f994; equip_chain_tbl_fe10->equip_chain_act_disp_table_fe14)
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- 新常量:
  - constants/card_info.inc: +2 (SPIRIT_MESSAGE_N_CID=0x1498, SPIRIT_MESSAGE_A_CID=0x1499)
    inserted after SPIRIT_MESSAGE_I_CID line
  - constants/card_info.inc: +1 (CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d) in new Cluster-2 section
  - constants/oam_attr.inc: +1 (OAM_EQUIP_LP_SPRITE_P1_5E=0x805e) in new Cluster-2 section
- Ghidra scripts:
  - `tools/ghidra-labeling/DisassembleF09Seg1R2Cluster2.py` (main script; 20 disasm + 15 EQ + 2 REF)
  - `tools/ghidra-labeling/DisassembleF09Seg1R2B1Fix.py` (fix: B1 unrestricted disasm; 114 instrs)
- ROM_INCBIN before: 30 (after Cluster-1); after: 21 (reduced by 9 Cluster-2 ROM_INCBIN blocks)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- CSV sync: no (sub-stub labels; no Ghidra function rename)

> Remediation status after this landing:
> - Cluster-1 [0x6f008..0x6f1c4]: DONE (commit e9636e1)
> - Cluster-2 [0x6f85e..0x6ff0a]: DONE (this record)
> - Cluster-3 [0x6ff0a..0x6ff50]: .byte blocks ff0a/ff1a/ff2c/ff3c/ff46 DONE (included above as B7c-B7g)
>   Note: Cluster-3 was co-disassembled with Cluster-2B in the same session. Seg-1 is now
>   fully remediated -- zero ROM_INCBIN and zero .byte-code residue in [0x6e76c..0x6ff50).
>
> Next remediation targets: Seg-4 remnants at 0x720e2/0x7270e/0x7276a/0x72794

---

### 4.14 Seg-4 Remediation 完成记录

> Remediation landing: 2026-06-20. Eliminates all 4 ROM_INCBIN + 4 .byte CODE + 4 .byte DATA
> blocks left by commits a9aa009 + 527e3a9 in Seg-4 range [0x080719fc..0x08072d20).
> All blocks are intra-function LAB_ continuation paths (bne/beq/bls branch targets) or
> dispatch table DATA slots. No new functions; no FS THUMB+1 stubs; no §5.1 orphans.

- 范围: `[0x080719fc, 0x08072d20)` Seg-4 remediation (full range)
- DISASM=8 items:
  - B1: ROM_INCBIN 0x720e2/0x12 -- bne-taken in field_spell_dispatch_sub_stubs_2004 (BL set_lp_display_row_type5 @ 0x080a1c2c; 8 instrs)
  - B2: ROM_INCBIN 0x7270e/0x1e -- bne-taken in fn_eligible_vampire_lord_lady_26f4 (15 instrs; bls-dispatch path to equip_zone dispatch table)
  - B3: ROM_INCBIN 0x7276a/0x1e -- bne-taken in equip_zone_sub_stubs_274c (14 instrs + pad; b@0x72784->0x727ae inside B4)
  - B4: ROM_INCBIN 0x72794/0x20 -- bne-target from B3 + 0x7f return path (14 instrs + pad; BL invoke_card_display_op_0x31_sub3_with_packed_params)
  - C1: .byte 0x71f74/0xc -- bls-taken indirect dispatch in fn_eligible_fengsheng_mirror_1f58 (5 instrs; mov r15,r0 computed jump)
  - C2: .byte 0x7241c/0xc -- bls-taken indirect dispatch in fn_eligible_fiend_comedian_2404 (5 instrs; mov r15,r0 computed jump)
  - C3: .byte 0x7256a/0xa -- bls-taken indirect dispatch in fn_eligible_last_turn_2540 (5 instrs; mov r15,r0 computed jump)
  - C4: .byte 0x72838/0x10 -- beq-taken in equip_zone_sub_2804 (7 instrs; BL trigger_card_display_op31_if_not_active @ 0x08093390)
- DATA createDWord=4:
  - 0x72430 -> .word last_turn_sub_2534 (dispatch table entry[0] in fn_eligible_fiend_comedian_2404)
  - 0x7257c -> .word vampire_sub_26bc (dispatch table entry[0] in fn_eligible_last_turn_2540)
  - 0x72734 -> .word equip_zone_sub_2856 (dispatch table entry[0] for equip zone phase dispatch)
  - 0x72830 -> .word LP_CARD_TRACK_BASE_OFF (literal pool in equip_zone_sub_2804)
- EQ=2 (all REUSE):
  - pool_b8_2830 @ 0x08072830: LP_CARD_TRACK_BASE_OFF=0x1da8 (ewram.inc:247)
  - pool_b8_27b4 @ 0x080727b4: lookup_equip_score_b_0x1b9=0x1b9 (duel_field.inc:332)
- REF=0; RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- 新常量: NONE (all REUSE)
- Ghidra scripts:
  - `tools/ghidra-labeling/DisassembleF09Seg4RBlocks.py` (main: 4 createDWord + 2 EQ + 8 disasm)
  - `tools/ghidra-labeling/FixF09Seg4RLPPoolLabel.py` (fix: rename LP_CARD_TRACK_BASE_OFF label -> pool_b8_2830 to avoid GAS self-ref)
- ROM_INCBIN before: 21 (after Seg-1 remediation); after: 17 (reduced by 4 ROM_INCBIN blocks)
- Seg-4 range [0x719fc, 0x72d20): 0 ROM_INCBIN, 0 .byte-code residue after landing
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)
- CSV sync: no (no new Ghidra functions; all CODE blocks are intra-function LAB_ continuations)

> Remediation status after this landing:
> - Seg-1 [0x6e76c..0x6ff50]: DONE (4.12 + 4.13)
> - Seg-4 [0x719fc..0x72d20]: DONE (this record)
> - Next remediation targets: Seg-5 remnants at 0x73218/0x12 + 0x73636/0x56

---

### 4.15 Seg-5 Remediation 完成记录

> Remediation landing: 2026-06-20. Eliminates 2 ROM_INCBIN + 7 .byte CODE + 3 .byte DATA
> blocks left by commits fa30373 + 4ba8057 in Seg-5 range [0x08072d20..0x08074338).
> All blocks are intra-function LAB_ continuation paths (bne/beq/bls/bcs branch targets) or
> dispatch table DATA slots. No new functions; no FS THUMB+1 stubs; no §5.1 orphans.

- 范围: `[0x08072d20, 0x08074338)` Seg-5 remediation (Seg-5a + Seg-5b full range)
- DISASM=9 items:
  - A1: .byte 0x73156/0x0a -- bls-taken indirect dispatch in fn_eligible_trap_dustshoot_3140 (5 instrs; mov r15,r0 computed jump)
  - B1: ROM_INCBIN 0x73218/0x12 -- bne-taken in trap_dustshoot_dispatch_sub_stubs_31e4 (BL set_lp_display_row_type5 @ 0x080a1c2c; 9 instrs; b trap_dustshoot_default_32a0)
  - A2: .byte 0x7326c/0x04 -- entry stub trap_dustshoot_sub_326c (2 HW entry; fall-through to decoded body at 0x73270)
  - A3: .byte 0x7359e/0x0a -- bls-taken indirect dispatch in fn_eligible_machine_dup_and_league_356c (5 instrs; mov r15,r0 computed jump)
  - B2: ROM_INCBIN 0x73636/0x56 -- bne-taken (2-path) in machine_dup_dispatch_sub_stubs_3628 (43 HW total; NOT-taken b@0x7365a->machine_dup_default_3756; taken b@0x7368a->LAB_08073758; BL dispatch_effect_handler_by_card_id @ 0x0808dab0 + BL count_available_monster_slots @ 0x080335b8 x2 + BL trigger_card_display_op31_if_not_active @ 0x08093390)
  - A4: .byte 0x73732/0x08 -- bcs-taken in machine_dup_sub_3704 (4 HW; BL decrement_lp_bar_display_counter @ 0x0804a870; movs r0,#0x64; b machine_dup_default_3756)
  - A5: .byte 0x7387a/0x0a -- bls-taken indirect dispatch in fn_eligible_cat_ill_omen_and_owl_of_luck (5 instrs; mov r15,r0 computed jump)
  - A6: .byte 0x73922/0x10 -- bne-taken in cat_ill_omen_dispatch_sub_stubs_3900 (8 HW; BL trigger_card_display_op31_if_not_active @ 0x08093390; movs r0,#0x7f; b cat_ill_omen_default_3a54)
  - A7: .byte 0x73d30/0x0e -- beq-taken (2 beq sources at 0x73cb8+0x73cc2) in reasoning_dispatch_sub_stubs_3bc8 (7 HW; BL enqueue_equip_zone_sprite_attr_full @ 0x080495fc; movs r0,#0x7d; b LAB_08073d74)
- DATA createDWord=3:
  - 0x73168 -> .word trap_dustshoot_sub_3290 (dispatch table[0] for trap_dustshoot_dispatch_table_3168)
  - 0x735b4 -> .word machine_dup_sub_374c (dispatch table[0] for machine_dup_dispatch_table_35b4)
  - 0x7388c -> .word cat_ill_omen_sub_3a46 (dispatch table[0] for cat_ill_omen_dispatch_table_388c)
- EQ=1 (REUSE): pool_b4_368c @ 0x7368c -> CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d (card_info.inc:1496)
  Note: pool label stays pool_b4_368c (not renamed to equate name; Seg-4R lesson)
- REF=0; RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- 新常量: NONE (all REUSE)
- Ghidra script: `tools/ghidra-labeling/DisassembleF09Seg5RBlocks.py`
- ROM_INCBIN before: 17 (after Seg-4 remediation); after: 15 (reduced by 2 ROM_INCBIN blocks)
- Seg-5 range [0x72d20, 0x74338): 0 ROM_INCBIN, 0 .byte-code residue after landing
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- CSV sync: no (no new Ghidra functions; all CODE blocks are intra-function LAB_ continuations)

> Remediation status after this landing:
> - Seg-1 [0x6e76c..0x6ff50]: DONE (4.12 + 4.13)
> - Seg-4 [0x719fc..0x72d20]: DONE (4.14)
> - Seg-5 [0x72d20..0x74338]: DONE (this record)
> - Last done-segment remnant: Seg-8 0x768dc (not yet remediated; Seg-9b + Seg-10 fully unstarted)
> - Next remediation targets: Seg-9b/10 when those segments have been landed

---

### 4.16 Seg-8 Remediation 完成记录 (LAST done-segment remnant)

> Remediation landing: 2026-06-21. Eliminates 1 ROM_INCBIN + 1 .byte CODE + 2 .byte DATA
> blocks left by commit 1e38556 in Seg-8 range [0x0807629c..0x0807738c).
> All 4 blocks are intra-function code paths (conditional branch targets) or
> literal pool DATA slots. No new functions; no FS THUMB+1 stubs; no §5.1 orphans.
> This completes ALL done-segment remediation: done range [0x6e76c..0x7738c) now has
> zero ROM_INCBIN and zero .byte-code residue.

- 范围: `[0x0807629c, 0x0807738c)` Seg-8 remediation (2 CODE blocks + 2 DATA blocks)
- DISASM=2 items:
  - Block A: ROM_INCBIN 0x768dc/0x1e -- beq-taken path of spell_vanishing_sub_6818 inner loop
    (beq LAB_080768dc @ 0x08076866, hw=0xd039; 15 THUMB instrs: lsrs/subs x2/ands/mov/muls/adds x3/movs/BL pair/movs/b;
    BL target: dispatch_equip_zone_sprite_banisher_by_field_count @ 0x080445a4 asm/04:9609;
    fall-through: b LAB_080768fc already decoded; no internal literal pool)
  - Block B: .byte 0x10,0x20 at LAB_08076750 -- beq-taken path of fn_eligible_mustering_dark_scorpions
    (beq LAB_08076750 @ 0x0807672e, hw=0xd00f; 1 instr: movs r0,#0x10;
    fall-through to LAB_08076752: ldrh r2,[r4,#0x8] already decoded)
- DATA createDWord=2:
  - Block C @ 0x08076720: Ghidra split artifact (2B DAT_ + 2B fake movs r0,r0) -> true .word 0x00001531
    = DARK_SCORPION_BURGLARS_CID (REUSE card_info.inc:1476)
    (consumer: ldr r0,DAT_08076720 @ 0x08076704; cmp r2,r0 @ 0x08076706)
  - Block D @ 0x0807677c: 4-byte .byte -> .word 0x00000868
    = PLAYER_BLOCK_STRIDE (REUSE ewram.inc:250)
    (consumer: ldr r2,DAT_0807677c @ 0x0807675e; muls r1,r2 @ 0x08076760)
- EQ=2 (all REUSE: DARK_SCORPION_BURGLARS_CID from card_info.inc:1476 / PLAYER_BLOCK_STRIDE from ewram.inc:250)
  Pool labels: DWORD_08076720 / DWORD_0807677c (differ from equate names, no GAS collision)
- REF=0; RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- 新常量: NONE (all REUSE)
- Ghidra script: `tools/ghidra-labeling/RefineF09Seg8RBlocks.py`
- ROM_INCBIN before: 15 (after Seg-5 remediation); after: 14 (reduced by 1 ROM_INCBIN block)
- Seg-8 range [0x7629c, 0x7738c): 0 ROM_INCBIN, 0 .byte-code residue after landing
- GLOBAL done-range [0x6e76c, 0x7738c) (Seg-1..8 + Seg-9a): 0 ROM_INCBIN, 0 .byte-code residue
  (Seg-9b [0x77c50+] and Seg-10 [0x7850c+] are forward work not yet done; 14 ROM_INCBIN remain there)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- CSV sync: no (no new Ghidra functions; both CODE blocks are intra-function LAB_ continuations)

> REMEDIATION COMPLETE: All four remediation campaigns (Seg-1/4/5/8) finished.
> Done-segment range [0x6e76c, 0x7738c) (Seg-1 through Seg-9a, 12 segments total) now has
> zero partial-disasm residue. Forward work continues at Seg-9b [0x08077c50..0x0807850c).

---

### 4.11 Seg-9a 完成记录

- 范围: `[0x0807738c, 0x08077c50)` -- 9 named fn + 3 new fn_eligible (fn_eligible_spatial_collapse / fn_eligible_dimension_fusion / fn_eligible_jade_insect_whistle)
- EQ=26 (all REUSE: PLAYER_BLOCK_STRIDE x6 / gP1AltHandSlotArray x1 / P1LP_BLOCK2_OFF_1CE8 x1 / gDuelPhaseFlags x4 / EQUIP_PHASE_FRAME_OFF x7 / CARD_STAT_LP_THRESHOLD x1 / gEquipZoneCountTable x1 / gP1ZoneHandCount x1 / gP1FieldArrayCBase x1 / gP1LifePoints x2 / PRICKLE_FAIRY_CID x1 / LEGENDARY_JUJITSU_MASTER_CID x1 NEW / KANGAROO_CHAMP_CID x1 NEW / gDuelFieldSlots x1; NEW CIDs added to card_info.inc before script)
- REF=5 (PTR_DAT_080775ac->spatial_collapse_dispatch_table_75ac@0x08077648; DAT_080775d0->spatial_collapse_dispatch_sub_stubs_75d0; PTR_DAT_08077a18->jade_insect_dispatch_table_7a18@0x08077b00; DAT_08077a3c->jade_insect_dispatch_sub_stubs_7a3c; DAT_08077b88->dimension_fusion_dispatch_sub_stubs_7b88)
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0
- DISASM=5 blocks:
  - B1: fn_eligible_spatial_collapse @ 0x0807757c (ROM_INCBIN 0x7757c/0x2c; FS THUMB+1 @0x09e41ca8; CID=0x16df SPATIAL_COLLAPSE_CARD_ID; literal pool x2: 0x775a0/a4; createFunction; 18 instrs)
  - B2: 6 sub-stubs spatial_collapse @ 0x080775d0 (ROM_INCBIN 0x775d0/0xa8; 9-entry dispatch table @0x080775ac; labels: sub_75d0/75ec/7602/762a/7648/default_7670; 62 instrs)
  - B3: fn_eligible_dimension_fusion @ 0x080779e4 (ROM_INCBIN 0x779e4/0x30; FS THUMB+1 @0x09e41d68; CID=0x1712 DIMENSION_FUSION_CID; literal pool x2: 0x77a0c/a10; createFunction; 19 instrs)
  - B4: 6 sub-stubs jade_insect + fn_eligible_jade_insect_whistle @ 0x08077a3c (ROM_INCBIN 0x77a3c/0x120; 9-entry dispatch table @0x08077a18; labels: sub_7a3c/7a70/7ab4/7ac2/7b00/7b2c; embedded fn_eligible @0x08077b34 FS THUMB+1 @0x09e41de0 CID=0x1717 JADE_INSECT_WHISTLE_CID; 111 instrs)
  - B5: 6 sub-stubs dimension_fusion @ 0x08077b88 (ROM_INCBIN 0x77b88/0xc8; 11-entry dispatch table @0x08077b5c; labels: sub_7b88/7bb6/7c18/7c2c/7c3a/default_7c48; 83 instrs)
- §5.1=0 (all 5 blocks have confirmed refs)
- 新常量: constants/card_info.inc (+3: JADE_INSECT_WHISTLE_CID=0x1717 / LEGENDARY_JUJITSU_MASTER_CID=0x1749 / KANGAROO_CHAMP_CID=0x1866)
- 踩坑1: REF_SLOTS gas_label==slot_label collision: PTR_DAT_080775ac and PTR_DAT_08077a18 had slot_label=gas_label; Ghidra export resolved .word to slot's own address; fix = RefineF09Seg9aRefFix.py (remove duplicate from slot, add unique *_ptr_* label to slot, setPrimary at target)
- 踩坑2: PoolFixF09Seg9a.py needed for 12 non-EWRAM constant pool DWords (0x4a4/0x1ce8/0x1da8/0x8056/0x1daa) emitted as .byte by Ghidra
- CSV: +3 rows (fn_eligible_spatial_collapse @0x0807757c / fn_eligible_dimension_fusion @0x080779e4 / fn_eligible_jade_insect_whistle @0x08077b34; all refine-created)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.17 Seg-9b 完成记录

- 范围: `[0x08077c50, 0x0807850c)` -- 10 named fn + 2 new fn_eligible (fn_eligible_dangerous_machine_type6 / fn_eligible_monster_gate)
- EQ=33 (all REUSE: gDuelPhaseFlags x3 / gP1LifePoints x8 / PLAYER_BLOCK_STRIDE x9 / LP_CARD_TRACK_BASE_OFF x3 / gEquipChainSlotRefs x2 / gDuelFieldSlots x3 / ACTIVATION_STATE_B_OFF x1 / gDuelCardCtxBase x1 / EQUIP_PHASE_FRAME_OFF x4 / gDuelFieldSlots_p2_base x2 / SANCTUARY_CID_SHIFTED x2 / BLUE_EYES_WHITE_DRAGON_CID x1 / gEquipZoneCountTable x1)
- REF=3 (PTR_DAT_08077f2c->dangerous_machine_dispatch_table_7f44@0x08077f44 [slot label = dangerous_machine_dispatch_table_ptr_7f2c]; DAT_08077f44->dangerous_machine_dispatch_sub_stubs_7f44 [self-ref]; DAT_08078368->monster_gate_dispatch_sub_stubs_8368 [self-ref])
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0
- DISASM=4 blocks:
  - B6: fn_eligible_dangerous_machine_type6 @ 0x08077ecc (ROM_INCBIN 0x77ecc/0x5c; FS THUMB+1 @0x09e448d0; CID=0x1738 DANGEROUS_MACHINE_TYPE6_CID; literal pool: 0x77ee8/0x77f20/0x77f24; createFunction; extended body @LAB_08077eec disasm via FixF09Seg9bResidues.py)
  - B7: 6 sub-stubs dangerous_machine @ 0x08077f44 (ROM_INCBIN 0x77f44/0xc0; 6-entry dispatch table @0x08077f2c; labels: sub_7f44/7f56/7f6c/7f7a/7f86/7f9c; shared branch targets LAB_08077fae+LAB_08077fd0 disasm via FixF09Seg9bResidues.py; pool: 0x77f98/0x77fcc/0x77ff0/0x77ff4/0x77ff8)
  - B8: fn_eligible_monster_gate @ 0x080782c0 (ROM_INCBIN 0x782c0/0x2c; FS THUMB+1 @0x09e41f18; CID=0x175c MONSTER_GATE_CID; literal pool: 0x782e4/0x782e8; createFunction)
  - B9: 8 sub-stubs monster_gate @ 0x08078368 (ROM_INCBIN 0x78368/0x14c; 31-entry dispatch table @0x080782ec; labels: sub_8368/83a0/83a8/8476/847c/848c/849e/default_84a8; 0x0807841c excluded [mid-BL]; pool: 0x78394/0x78398/0x78450/0x78454)
- §5.1=0 (all 4 blocks have confirmed refs)
- 新常量: constants/card_info.inc (+2: DANGEROUS_MACHINE_TYPE6_CID=0x1738 / MONSTER_GATE_CID=0x175c)
- Ghidra scripts:
  - `tools/ghidra-labeling/RefineF09Seg9bSlots.py` (33 EQ + 3 REF)
  - `tools/ghidra-labeling/DisassembleF09Seg9bBlocks.py` (B6/B7/B8/B9 disasm)
  - `tools/ghidra-labeling/FixF09Seg9bPools.py` (4 missing pool DWords: 0x77f98/0x78394/0x78398/0x78454)
  - `tools/ghidra-labeling/FixF09Seg9bResidues.py` (3 residue blocks: LAB_08077eec/08077fae/08077fd0)
  - `tools/ghidra-labeling/FixF09Seg9bPools2.py` (2 wrong DWords at 0x77f18/1c -> correct at 0x77f20/24)
- 踩坑: Multi-round pool fix (5 scripts total): (1) pool addresses in proposal were off (0x77f18/1c=CODE, actual pools at 0x77f20/24); (2) force_dword didn't cover 0x77f98 (fn_ptr pool in B7) and 3 B9 pools; (3) residue ROM_INCBIN at LAB_08077eec/fae/fd0 (conditional branch targets not reached by per-entry DisassembleCommand)
- ROM_INCBIN before: 14; after: 10 (reduced by 4 B6/B7/B8/B9 blocks)
- Seg-9b range [0x77c50, 0x7850c): 0 ROM_INCBIN, 0 non-ASCII in exported asm
- Seg-9 COMPLETE (9a [0x7738c..0x77c50] + 9b [0x77c50..0x7850c] both done)
- CSV: +2 rows (fn_eligible_dangerous_machine_type6 @0x08077ecc / fn_eligible_monster_gate @0x080782c0; refine-created)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: 5f27863

---

### 4.18 Seg-10a 完成记录

- 范围: `[0x0807850c, 0x08079500)` -- 13 named fn + 3 new fn_eligible (fn_eligible_emissary_of_the_afterlife / fn_eligible_first_sarcophagus / fn_eligible_human_wave_tactics)
- EQ=60 (58 REUSE + 2 NEW: CARD_TYPE_FIELD8_MASK=0xb4f80000 / RECYCLE_CID=0x16d5)
- REF=3 (DWORD_080785bc/d4->invoke_effect_node_with_active_flag_if_player_mismatch+1 self-ref x2; DWORD_08078a20->check_equip_slot_eligible_by_side_match_and_type+1 cross-module fn-ptr)
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0
- DISASM=5 blocks:
  - B1: fn_eligible_emissary_of_the_afterlife @ 0x08078a90 (ROM_INCBIN 0x78a90/0x44; FS THUMB+1 @0x09e45e78; CID=0x1796 REUSE; createFunction)
  - B2: 8 sub-stubs equip_state_dispatch @ 0x08078b24 (ROM_INCBIN 0x78b24/0xd4; 19-entry dispatch table @PTR_DAT_08078ad8; stubs: sub_b24/b38/b58/b70/b7c/b9c/bd8/default_bec)
  - B3: fn_eligible_first_sarcophagus @ 0x08078fe0 + first_sarcophagus_sub_9040 (ROM_INCBIN 0x78fde/0xf6; 2-byte pad; FS THUMB+1 @0x09e44b10; CID=0x17af REUSE; cross-module raw ref @0x084d6254->0x79040; createFunction)
  - B4: 9 sub-stubs + fn_eligible_human_wave_tactics @ 0x080792f8 (ROM_INCBIN 0x79148/0x1ec; 29-entry dispatch table @0x080790d4; FS THUMB+1 @0x09e44b28; CID=0x17b2 REUSE; 2-byte pad @0x792f6; 10 entries; createFunction)
  - B5: 7 sub-stubs equip_zone_seq @ 0x080793ac (ROM_INCBIN 0x793ac/0x154; 30-entry dispatch table @0x08079334; stubs: sub_93ac/93ec/940a/9434/94da/94ec/default_94f6)
- 踩坑: DisassembleF09Seg10aPoolFix.py needed for 12 constant-value pool DWords (PLAYER_BLOCK_STRIDE=0x868 / EQUIP_PHASE_FRAME_OFF=0x4a4 / CID-related values not in EWRAM/ROM address range); caused DAT_0807XXXX build errors on first attempt. Pattern: constant-valued pools need force_dword even when value < 0x02000000.
- §5.1=0 (all 5 blocks confirmed refs)
- 新常量: constants/card_info.inc (+2: RECYCLE_CID=0x16d5 after INFERNO_CID / CARD_TYPE_FIELD8_MASK=0xb4f80000 in new Seg-10a section)
- Ghidra scripts: RefineF09Seg10aSlots.py (60 EQ + 3 REF) + DisassembleF09Seg10aBlocks.py (5 blocks) + DisassembleF09Seg10aPoolFix.py (12 pool DWords fix)
- ROM_INCBIN before: 10 (after Seg-9b); after: 5
- Seg-10a range [0x7850c, 0x79500): 0 ROM_INCBIN, 0 non-ASCII in exported asm
- CSV: +3 rows (fn_eligible_emissary_of_the_afterlife @0x08078a90 / fn_eligible_first_sarcophagus @0x08078fe0 / fn_eligible_human_wave_tactics @0x080792f8)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: be48d12

---

### 4.19 Seg-10b 完成记录 (FILE 09 FINAL SEGMENT)

- 范围: `[0x08079500, 0x08079e60)` -- 4 named fn + 3 new fn_eligible (fn_eligible_order_to_charge_or_smash / fn_eligible_familiar_knight / fn_eligible_inferno_tempest)
- EQ=15 (all REUSE: gEquipZoneCountTable x1 / PLAYER_BLOCK_STRIDE x4 / gDuelFieldSlots x4 / gDuelPhaseFlags x3 / EQUIP_PHASE_FRAME_OFF x2 / CARD_DISPLAY_OP31_LP_BAR_SUB x1)
- REF=3 (0x080796ac->PTR_DAT_080796b0 B7 5-entry dispatch table; 0x08079a64->PTR_DAT_08079a68 B9 29-entry dispatch table; 0x08079c18->PTR_DAT_08079c1c B10 32-entry dispatch table)
- RENAME=0; FUNC_RENAME=0; PLATE=0; carve=0
- DISASM=5 blocks:
  - B6: fn_eligible_order_to_charge_or_smash @ 0x0807965c (ROM_INCBIN 0x7965c/0x50; FS THUMB+1 @0x09e42098 CID=0x179f ORDER_TO_CHARGE_CID + @0x09e42200 CID=0x17b8 ORDER_TO_SMASH_CID; shared fn_eligible; createFunction; pool x4: 0x79670/0x7967c/0x796a4/0x796a8)
  - B7: 5 sub-stubs equip_act dispatch @ 0x080796c4 (ROM_INCBIN 0x796c4/0x10c; PTR_DAT_080796b0 5-entry table; stubs: equip_act_sub_96c4/970e/9734/9760/default_97c4; pool x10)
  - B8: fn_eligible_familiar_knight @ 0x08079a1c (ROM_INCBIN 0x79a1c/0x48; FS THUMB+1 @0x09e45ef0; CID=0x17c3 FAMILIAR_KNIGHT_CID REUSE; createFunction; pool x4: 0x79a54/a58/a5c/a60)
  - B9: 6 sub-stubs + fn_eligible_inferno_tempest @ 0x08079bdc (ROM_INCBIN 0x79adc/0x13c; PTR_DAT_08079a68 29-entry table + FS THUMB+1 @0x09e42230; CID=0x17ca INFERNO_TEMPEST_CID NEW; stubs: sub_9adc/9af8/9b62/9b80/9bb4/default_9bd0 + fn_eligible@0x79bdc; createFunction; pool x11)
  - B10: 9 sub-stubs neo_daedalus_lp @ 0x08079c9c (ROM_INCBIN 0x79c9c/0x1c4; PTR_DAT_08079c1c 32-entry table; stubs: sub_9c9c/9cd4/9d24/9d74/9da4/9dc0/9dd8/9df0/default_9e4e; pool x19)
- 踩坑: FixF09Seg10bB10Pool.py needed for B10 sub_9df0 [0x79e0c..0x79e4d] (LAB_08079e2c + LAB_08079e4a undefined); sub_9df0 has code paths AFTER literal pool at 0x79e04/0x79e08 that weren't reached by DisassembleCommand; solution: separate clearListing+setTMode+disasm at 0x79e0c + 0x79e2c.
- 踩坑: FixF09Seg10bB6Start.py for 0x7965c..0x7965f (B6_LO was 0x79660 instead of 0x7965c in first script; fixed by disasm from 0x7965c; Ghidra function at 0x79660 due to OverlappingFunctionException; 4 bytes exported as orphan code before fn label; byte-identical verified OK).
- §5.1=0 (all 5 blocks have confirmed refs)
- 新常量: constants/card_info.inc +1 (INFERNO_TEMPEST_CID=0x17ca after FAMILIAR_KNIGHT_CID)
- Ghidra scripts: RefineF09Seg10bSlots.py (15 EQ + 3 REF) + DisassembleF09Seg10bBlocks.py (B6-B10) + FixF09Seg10bB6Start.py + FixF09Seg10bB10Pool.py
- ROM_INCBIN before: 5 (after Seg-10a); after: 0 (file 09 fully zero ROM_INCBIN)
- Seg-10 COMPLETE (10a [0x7850c..0x79500] + 10b [0x79500..0x79e60] both done)
- **FILE 09 COMPLETE**: asm/09_equip_lp_display.s [0x6e76c..0x79e60] -- all 10 segments done; ROM_INCBIN=0; byte-identical SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- CSV: +3 rows (fn_eligible_order_to_charge_or_smash @0x08079660 / fn_eligible_familiar_knight @0x08079a1c / fn_eligible_inferno_tempest @0x08079bdc)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.10 Seg-8 完成记录

- 范围: `[0x0807629c, 0x0807738c)` -- 19 fn (enqueue_hand_spell_sprite_with_lp_counter / invoke_equip_oam_for_zone_e_bits46 / tick_equip_zone_bitmap_display_seq / enqueue_equip_slot_sprite_if_not_in_chain / tick_equip_zone_hand_sprite_by_card_pair / check_effect_slot_card_type_flag_by_id / fn_eligible_mustering_dark_scorpions [new] / mustering_dark_scorpions_dispatch_sub_stubs_65f0 + 5 sub-stubs / fn_eligible_spell_vanishing [new] / spell_vanishing_dispatch_sub_stubs_67f8 + 7 sub-stubs / enqueue_effect_node_sprite_type11_mode5 / enqueue_hand_spell_sprite_with_slot_count / enqueue_equip_zone_sprite_zone_type15 / tick_zone_sprite_pipeline_by_lp_table_delta / enqueue_equip_zone_sprite_with_neo_daedalus_and_chain / check_equip_slot_match_for_card_render / dispatch_spell_zone_sprite_by_display_state / update_equip_target_bitmap_for_zone15 / enqueue_zone_equip_sprite_black_luster_soldier)
- EQ=68 (63 REUSE + 5 NEW: DARK_SCORPION_BURGLARS_CID=0x1531 @0x08076570; DD_SCOUT_PLANE_CID=0x16be @0x08076ba4; ENERGY_DRAIN_CID=0x16e3 @0x08076f1c; GIFT_OF_THE_MARTYR_CID=0x18ca @0x08076f50; HAND_SPELL_SLOT_CC8_OFF=0xcc8 @0x080769d4)
- REF=0
- RENAME=8 (bitmap_dispatch_switch_table_ptr_6398; check_equip_slot_eligible_by_type_query_ptr_63c8/63dc/6418; check_equip_slot_eligible_by_side_match_ptr_63f4; mustering_dark_scorpions_dispatch_sub_stubs_65f0; spell_vanishing_dispatch_sub_stubs_67f8; equip_effect_opcode_switch_table_ptr_714c)
- FUNC_RENAME=0; PLATE=0; carve=0
- DISASM=4 blocks:
  - B1: fn_eligible_mustering_dark_scorpions @ 0x080765b0 (ROM_INCBIN 0x765b0/0x2c; FS THUMB+1 @0x09e4xxxx; CID=Dark Scorpion Burglars; literal pool 2 DWords 0x765d4/d8; createFunction)
  - B2: 5 sub-stubs mustering_dark_scorpions_dispatch_sub_stubs_65f0 @ 0x080765f0 (ROM_INCBIN 0x765f0/0x19c; 5-entry dispatch table @0x765dc..0x765ef)
  - B3: fn_eligible_spell_vanishing @ 0x080767ac (ROM_INCBIN 0x767aa/0x32; 2B pad @0x767aa; FS THUMB+1 @0x09e4xxxx; CID=Spell Vanishing; literal pool 2 DWords 0x767d4/d8; createFunction)
  - B4: 7 sub-stubs spell_vanishing_dispatch_sub_stubs_67f8 @ 0x080767f8 (ROM_INCBIN 0x767f8/0x110; 7-entry dispatch table @0x767dc..0x767f7)
- switchD_0807638c + switchD_08077144: already fully decoded in prior pass; no additional work
- §5.1=0 (all 4 blocks have confirmed refs)
- 新常量: constants/card_info.inc (+5: DARK_SCORPION_BURGLARS_CID=0x1531, DD_SCOUT_PLANE_CID=0x16be, ENERGY_DRAIN_CID=0x16e3, GIFT_OF_THE_MARTYR_CID=0x18ca, DEAL_OF_PHANTOM_CID=0x1492 doc-only); constants/ewram.inc (+1: HAND_SPELL_SLOT_CC8_OFF=0xcc8)
- CSV: +2 rows (fn_eligible_mustering_dark_scorpions @0x080765b0, fn_eligible_spell_vanishing @0x080767ac; both refine-created functions)
- reviewer correction applied: DWORD_080769d4 (0xcc8) EOL = "bits[12:0] via ldrh+lsls#19+lsrs#19" (not "bits[23:22]")
- 踩坑: B2/B4 8-pass pool fix campaign (PoolFixF09Seg8.py -> b -> c -> d -> e -> f -> g -> h); root cause = DisassembleCommand stops at unconditional branch + clearListing code range wipes adjacent pool DWords + Ghidra merges adjacent DWords back to .byte; fix = split each disasm range at pool boundaries + per-stub DisassembleCommand starting at each unreachable stub entry; literal pool cluster at 0x666c required all 4 DWords forced individually (0x666c/670/674/678); sub_66d8 case targets at 0x76744/48/50 required 3 separate passes (G disassembled 0x76744..0x76747, H disassembled 0x76748..0x76751) due to 'b' stopping flow
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: 1e38556

---

### 4.09 Seg-7 完成记录

- 范围: `[0x080752cc, 0x0807629c)` -- 19 fn (enqueue_effect_card_sprite_dual_with_negated / init_effect_slot_display_if_opponent_lp_active / enqueue_effect_slot_sprites_all_players / check_equip_slot_placement_via_neo_daedalus / check_equip_slot_placement_via_target_bitmap / enqueue_equip_zone_sprite_with_slot_setup / invoke_equip_oam_for_zone_type_e_slot / invoke_equip_oam_for_hand_set_code_slot / tick_equip_zone_display_seq_by_type_code / enqueue_graveyard_spell_for_hand_set_code / tick_graveyard_spell_display_by_state / enqueue_effect_slot_sprite_mode2_and_type11 / dispatch_effect_activation_with_lp_counter / set_field_bit_by_slot_match_equip_dir / invoke_equip_zone_lp_shape_with_lp_counter / enqueue_effect_node_sprite_type11_from_slot / enqueue_effect_slot_sprite_with_score_sum / dispatch_zone13_equip_display_by_type_code / tick_effect_display_by_state_and_type_code)
- EQ=42 (all REUSE: gP1LifePoints x1 / PLAYER_BLOCK_STRIDE x14 / gDuelCardCtxBase x3 / gEquipZoneCountTable x1 / gDuelFieldSlots x6 / gDuelPhaseFlags x4 / EQUIP_PHASE_FRAME_OFF x4 / SLOT_CARD_SET_CODE_MASK x1 / SCROLLBAR_KEEP_BITS_8_0 x1 / SCROLLBAR_CLEAR_BITS_14_6 x1 / gP1HandSlotArray x3 / lookup_equip_score_b_0x1b7 x1 / OAM_EFFECT_SLOT_TILE_P1 x1 / gP1SlotSetCodeArray x1)
- REF=0
- RENAME=4 (DAT_08075414->emblem_dispatch_sub_stubs_5414; DWORD_08075c24->dispatch_eff_act_card_id_ptr_5c24 (Ruling A FS ROM ptr + ASCII EOL); DAT_08075d5c->magical_dim_dispatch_sub_stubs_5d5c; DAT_08075fe0->friendship_dispatch_sub_stubs_5fe0)
- FUNC_RENAME=0
- PLATE=2 updates (enqueue_effect_slot_sprites_all_players @0x080754b8: gEffectSlots->gEquipZoneCountTable + gSlotData->gDuelFieldSlots; reviewer non-blocking cleanup landed OK)
- carve=0
- disasm=6 blocks:
  - B1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378 (ROM_INCBIN 0x75378/0x28; FS THUMB+1 @0x09e41678; CID=0x1629; literal pool 1 DWord 0x0807539c; createFunction)
  - B2: 6 emblem sub-stubs @ 0x08075414 (ROM_INCBIN 0x75414/0xa4; 29-entry dispatch table @0x753a0..0x75413; labels: sub_5414/5446/545a/5492/54a4/default_54ae)
  - B3: fn_eligible_magical_dimension @ 0x08075d0c (ROM_INCBIN 0x75d0c/0x2c; FS THUMB+1 @0x09e41948; CID=0x1678; literal pool 2 DWords 0x75d30/34; createFunction)
  - B4: 9 magical_dim sub-stubs @ 0x08075d5c (ROM_INCBIN 0x75d5c/0x214; 9-entry dispatch table @0x75d38..0x75d5b; labels: sub_5d5c/5dc4/5de8/5e20/5e60/5e8c/5ec0/5f02/5f2c; 3 rounds pool fix: PoolFixF09Seg7.py + b.py + c.py for 29+7 DWords)
  - B5: fn_eligible_friendship @ 0x08075f90 (ROM_INCBIN 0x75f8e/0x2e; 2B pad @0x75f8e; FS THUMB+1 @0x09e41978; CID=0x167a FRIENDSHIP_CID REUSE; literal pool 2 DWords 0x75fb4/b8; createFunction)
  - B6: 6 friendship sub-stubs @ 0x08075fe0 (ROM_INCBIN 0x75fe0/0x17c; 9-entry dispatch table @0x75fbc..0x75fdb; labels: sub_5fe0/5ff4/6030/609e/6100/default_6146; pool fix for 3 DWord clusters in B6)
- §5.1=0 (all 6 blocks have confirmed refs)
- 新常量: constants/card_info.inc (+2: EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629, MAGICAL_DIMENSION_CID=0x1678); FRIENDSHIP_CID=0x167a REUSE
- CSV: +3 rows (fn_eligible_emblem_of_dragon_destroyer @0x08075378 / fn_eligible_magical_dimension @0x08075d0c / fn_eligible_friendship @0x08075f90; all refine-created functions)
- 踩坑: B4/B6 多轮 pool fix (PoolFixF09Seg7.py -> b -> c): B4 大段 0x214B 含 THUMB+1 callee ptrs + 多个 data pool clusters; redisasm clearListing 会覆写 force_dword (需先 disasm 再单独 force_dword 不含 re-clearListing); B4+0x52 末尾 ROM_INCBIN 0x75f52/0x16 残留 4 个 pool DWords (PoolFixF09Seg7c.py)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.08 Seg-6 完成记录

- 范围: `[0x08074338, 0x080752cc)` -- 20 fn (apply_equip_activation_for_zone_slot_sprite / dispatch_equip_zone_bitmap_or_neo_daedalus_sprite / enqueue_equip_zone_sprite_full_from_slot / dispatch_equip_zone_sprite_mode2_or_activation / dispatch_dragon_summon_or_lp_delta_by_slot_type / dispatch_equip_chain_activation_if_zone_pair_aligned / enqueue_slot_sprite_type4_from_entry_attr / tick_equip_activation_lp_display_seq / dispatch_equip_zone_sprite_with_type11_at_step80 / tick_equip_oam_display_by_state_7x / dispatch_banisher_sprite_loop_for_opponent_zones / tick_equip_display_seq_when_fewer_monster_zones / tick_equip_oam_display_by_type_code / enqueue_effect_slot_sprites_all_sides / enqueue_effect_slot_sprite_with_type11 / enqueue_effect_slot_sprite_by_zone_capacity_check / enqueue_effect_card_sprites_all_players / dispatch_equip_node_display_by_type_code / enqueue_effect_card_sprite_single_slot / dispatch_equip_display_state_by_code)
- EQ=55 (all REUSE: gDuelPhaseFlags x9 / PLAYER_BLOCK_STRIDE x12 / gDuelFieldSlots x8 / EQUIP_PHASE_FRAME_OFF x11 / EQUIP_ZONE_SPRITE_ATTR x6 / gDuelCardCtxBase x2 / LP_CARD_TRACK_BASE_OFF x2 / LP_CARD_TRACK_NEXT_OFF x1 / ELIGIB_SPRITE_CTRL_OFF x1 / ELIGIB_ANIM_STATE_OFF x1 / OAM_EQUIP_SPRITE_TILE_P2_1B x1 / gEquipZoneCountTable x1)
- REF=5 (4x gP1LifePoints=0x0201c4e0: DWORD_08074a48/adc/cdc/d68; 1x gEquipLpActivBitmap=0x0201e220 NEW)
- RENAME=5 (PTR_DAT_080748a0->equip_zone_dispatch_table_48a0; DAT_08074914->equip_zone_sub_stubs_4914; DWORD_08074aac->check_equip_slot_eligible_bst_filter_ptr_4aac; DWORD_08074d4c->check_equip_slot_eligible_by_type_query_ptr_4d4c; DAT_08075150->equip_display_switch_table_ptr_5150)
- FUNC_RENAME=0
- PLATE=1 (C8 stale FUN_0807a680->dispatch_equip_sprite_by_zone_or_capacity_guard in enqueue_effect_slot_sprite_by_zone_capacity_check @0x0807500c) + CJK fix (dispatch_dragon_summon_or_lp_delta_by_slot_type @0x08074770 plate rewritten ASCII)
- carve=1 (equip_zone_dispatch_table_48a0 @0x080748a0: 29-entry raw-ptr table via Ghidra label renaming + sub-stub symbolic .word entries via disasm)
- disasm=2 blocks:
  - B1: fn_eligible_dimension_jar @ 0x08074854 (ROM_INCBIN 0x74852/0x4a; FS THUMB+1 @GBA:0x09e442a0; CID=0x15dd Dimension Jar; literal pool 4 DWords 0x488c/90/94/98; createFunction)
  - B2: 6 equip_zone sub-stubs @ 0x08074914 (ROM_INCBIN 0x74914/0xcc; raw ptr dispatch from equip_zone_dispatch_table_48a0; labels: sub_914/sub_920/sub_948/sub_964/sub_9b8/epilogue_9d4; force-DWord pool x5)
- switchD_0807514a: already fully decoded (31-entry .word table + case labels in asm); no additional work
- §5.1=0 (both ROM_INCBIN blocks confirmed referenced)
- 新常量: constants/card_info.inc (+1: DIMENSION_JAR_CID=0x15dd); constants/ewram.inc (+1: gEquipLpActivBitmap=0x0201e220)
- CSV: +1 row (fn_eligible_dimension_jar @ 0x08074854; refine-created function)
- 踩坑: CJK mojibake plate in dispatch_dragon_summon_or_lp_delta_by_slot_type @0x08074770 (CJK plate from naming phase) -> FixF09Seg6CjkPlate.py ASCII rewrite
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.06 Seg-5a 完成记录

- 范围: `[0x08072d20, 0x08073a5c)` -- 13 fn (enqueue_zone_sprite_attr_type11_from_slot / tick_equip_lp_display_state_by_slot / setup_equip_oam_by_placeable_card_id_and_zone / tick_equip_lp_display_bitmap_state_by_slot / tick_equip_lp_display_type18_state_by_slot / enqueue_equip_zone_sprite_by_slot_lp_state / enqueue_slot_sprite_if_chain_flags_and_node_active / tick_equip_deck_pair_hand_sprite_state / apply_lp_delta_for_slot_by_series_code / tick_neo_daedalus_equip_display_seq / enqueue_slot_sprite_mode3_with_effect_node / dispatch_equip_slot_activation_or_sprite_by_type / enqueue_hand_spell_sprite_by_set_code_match)
- EQ=48 (38 REUSE + 10 NEW: EQUIP_CHAIN_BASE_OFF / STATUE_OF_THE_WICKED_CID / SPRITE_ATTR_CLR_BIT13 / TOKEN_13FB_CID / TOKEN_14FA_CID / TOKEN_154E_CID / TOKEN_15BD_CID / TOKEN_15BE_CID / TOKEN_1603_CID / TOKEN_1639_CID [TRAP_DUSTSHOOT_CID + TOKEN_195A_CID = 12 NEW .equ created total; EQUIP_CHAIN_BASE_OFF 2nd slot = REUSE])
- REF=10 (all gP1LifePoints=0x0201c4e0: DWORD_08072d8c/dbc/df0 + PTR_gP1LifePoints_x5 + DWORD_080732f4/337c)
- RENAME=3 (DAT_080731e4->trap_dustshoot_dispatch_sub_stubs_31e4; DAT_08073628->machine_dup_dispatch_sub_stubs_3628; DAT_08073900->cat_ill_omen_dispatch_sub_stubs_3900)
- FUNC_RENAME=0; PLATE=0; carve=0; §5.1=0
- DISASM=6 blocks:
  - B1: fn_eligible_trap_dustshoot_3140 @ 0x08073140 (ROM_INCBIN 0x7313e/0x2a; FS table THUMB+1 @GBA:0x09e411b0; CID=0x1546 Trap Dustshoot; literal pool 2 DWords)
  - B2: 6 sub-stubs trap_dustshoot_sub_31e4..default_32a0 @ 0x080731e4..0x080732a7 (ROM_INCBIN 0x731e4/0xc4; 31-entry dispatch table @0x73168..0x731e3; inline pool words at 0x73210/73214/73264/73268)
  - B3: fn_eligible_machine_dup_and_league_356c @ 0x0807356c (ROM_INCBIN 0x7356c/0x48; FS table THUMB+1 x2 @GBA:0x09e41288/0x09e42dd0; CID=0x157a Machine Duplication + CID=0x1978 League; literal pool 3 DWords)
  - B4: 7 sub-stubs machine_dup_sub_3628..default_3756 @ 0x08073628..0x0807375f (ROM_INCBIN 0x73628/0x138; 29-entry dispatch table @0x735b4..0x73627; inline pools at 0x736a0/a4 within sub_3690)
  - B5: fn_eligible_cat_ill_omen_and_owl_of_luck @ 0x08073864 (ROM_INCBIN 0x73864/0x28; FS table THUMB+1 x2 @GBA:0x09e44108/0x09e44138; CID=0x1590 A Cat of Ill Omen + CID=0x1593 An Owl of Luck; literal pool 2 DWords)
  - B6: 8 sub-stubs cat_ill_omen_sub_3900..default_3a54 @ 0x08073900..0x08073a5b (ROM_INCBIN 0x73900/0x15c; 29-entry dispatch table @0x7388c..0x738ff; multiple inline pools at 0x73990/94/98/39ac/39d4/3a30)
- 新常量: constants/card_info.inc (+10: STATUE_OF_THE_WICKED_CID/TRAP_DUSTSHOOT_CID/TOKEN_13FB..195A_CID x8 + TOKEN_195A_CID); constants/ewram.inc (+1: EQUIP_CHAIN_BASE_OFF=0x1c88); constants/oam_attr.inc (+1: SPRITE_ATTR_CLR_BIT13=0xffffdfff)
- 踩坑: force_dword 用 8B clearListing 覆写相邻 inline pool 后的代码 (B4 sub_3690 + B6 sub_3968/39b0 均受影响) -> 改 4B clearListing (force_dword_4b) + 逐段 DisassembleCommand 修复; B4 sub_3690 代码分 5 个分散片段 (pool 中断流) 须 5 次 DisassembleCommand; 修复脚本: PoolFix.py -> PoolFix2.py -> PoolFix3.py -> PoolFix4.py -> PoolFix5.py (5 轮). 教训: 含多处 inline pool 的 sub-stub 须逐块 clearListing(4B)+disasm, 不可一次性 force_dword 整段.
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

### 4.07 Seg-5b 完成记录

- 范围: `[0x08073a5c, 0x08074338)` -- 8 fn (test_equip_target_slot_by_zone_descriptor_match / enqueue_lp_counter_sprite_by_mode_and_player / tick_equip_zone_sprite_and_lp_counter_state / enqueue_zone_sprite_type5_from_slot / tick_equip_zone_eligibility_display_state_seq / tick_equip_lp_counter_display_state_seq / enqueue_spirit_zone_sprite_type11)
- EQ=21 (19 REUSE + 2 NEW: RELOAD_CID=0x16d9 Reload pw=22589918 / DISTURBANCE_STRATEGY_CID=0x15aa Disturbance Strategy pw=77561728)
- REF=4 (all gP1LifePoints=0x0201c4e0: DWORD_08073ae0/b14/3f94/742b0)
- RENAME=2 (DAT_08073bc8->reasoning_dispatch_sub_stubs_3bc8; DAT_08074080->reversal_quiz_dispatch_sub_stubs_4080)
- FUNC_RENAME=0; PLATE=1 (enqueue_spirit_zone_sprite_type11 @ 0x08074318: FUN_08071d64->dispatch_spirit_monster_zone_sprite_by_card_id; was already correct in Ghidra, stale only in pre-export asm)
- carve=0; §5.1=0
- DISASM=4 blocks:
  - B7: fn_eligible_reasoning @ 0x08073b1c (ROM_INCBIN 0x73b1c/0x30; FS THUMB+1 @GBA:0x09e412b8; CID=0x159a Reasoning; literal pool 2 DWords at 0x08073b44/48)
  - B8: 9 sub-stubs reasoning_sub_3bc8..reasoning_default_3d74 @ 0x08073bc8..0x08073d83 (ROM_INCBIN 0x73bc8/0x1bc; 31-entry dispatch table @0x73b4c..0x73bc7 = 0x7c bytes; inline pools at 0x73bf0/f4 + 0x73c44/48/4c + 0x73d14/18/1c/20)
  - B9: fn_eligible_reversal_quiz @ 0x08073fe0 (ROM_INCBIN 0x73fde/0x2e; 2B pad at 0x73fde; FS THUMB+1 @GBA:0x09e41378; CID=0x15a5 Reversal Quiz; literal pool 2 DWords at 0x08074004/08)
  - B10: 6 sub-stubs reversal_quiz_sub_4080..reversal_quiz_default_41ee @ 0x08074080..0x080741f7 (ROM_INCBIN 0x74080/0x178; 29-entry dispatch table @0x7400c..0x7407f = 0x74 bytes; inline pools at 0x740b8/bc/c0 + 0x740e4 + 0x7410c/10 + 0x74170/74/78 + 0x741dc/e0)
- 新常量: constants/card_info.inc (+2: RELOAD_CID=0x16d9, DISTURBANCE_STRATEGY_CID=0x15aa)
- 踩坑: DisassembleF09Seg5bBlocks.py 初版 force_dword 地址偏 2 字节 (用了 pad+pool 合并地址如 0x73d12 而非实际对齐池 0x73d14) -> 导致 GAS "value too big (0xFFFFFFFC)" 错误; 修复: PoolFixF09Seg5b.py 重跑 clearListing + 重新 disasm + 正确 force_dword 各 pool 的 4B 对齐地址. 教训: inline pool 前 2B pad 不纳入 force_dword 范围, pool 从第一个 4B 对齐位置起.
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- commit: (see git log)

---

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
| Seg-9 | 0x7738c..0x7850c | 19+5new | 67 | 9 inc(0x7757c/2c, 0x775d0/a8, 0x779e4/30, 0x77a3c/120, 0x77b88/c8, 0x77ecc/5c, 0x77f44/c0, 0x782c0/2c, 0x78368/14c) | ✅ invoke_setup_equip_oam + dispatch_equip_lp_bar_display + dispatch_equip_banisher 簇; 9 inc **重段**; 5 new fn_eligible (Seg-9a x3 + Seg-9b x2) |
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
