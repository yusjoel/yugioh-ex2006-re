# Refine Review: F10-Seg-8a

**Segment**: Seg-8a [0x08082290..0x08082b18)
**File**: `asm/10_equip_effect_dispatch.s`
**Proposal**: `doc/dev/refine/F10-Seg-8a.proposal.md`
**Reviewer**: independent (no executor trust)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与 §五 路线图一致, 未跳号/回头 | PASS | Roadmap Seg-8 [0x82290..0x83450); proposal 在函数边界 0x82b18 拆为 8a/8b, 符合方法论允许的重段拆分; 无跳号回头 |
| C2 | 每个 ROM_INCBIN 块都有归宿 | PASS | BLK1 0x827d4/0xd8 -> R4 disasm; BLK2 0x828c4/0xf8 -> R4 disasm; 无静默保留 |
| C3 | §5.1 块确 0 引用 | PASS | 无 §5.1 块; BLK1 有 1 个 THUMB+1 ref (FS table 0x09e3fc60 -> 0x080827d5); BLK2 有 1 个 raw ref (JT@0x080828ac -> 0x080828c4); 均已独立重跑 python ref-scan 核实 |
| C4 | 每个 EQ value == ROM 4 字节小端 | PASS | 独立 python 核对全部 38 个 hex-value EQ 槽, 均与 ROM 字节一致; fn-ptr 槽 0x080905e9/0x0805000d/0x1a1/0x103 逐一核对通过 |
| C5 | 新建 constants 前确无现有可复用 | PASS | 所有标 REUSE 的值均 grep 命中现有 constant (包括 DUAL_LABEL_RENDER_STATE_CLEAR=0xFFFC7FFF 大写, PLAYER_BLOCK_STRIDE=0x868 等价); 所有标 NEW 的值均 grep 0 命中 (duel_field.inc/card_info.inc 逐一核实) |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 5 个新常量名: set_equip_activation_state_by_mode_alt_fn_ptr / check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr / EQUIP_DISPLAY_OP_PARAM_1A1 / GRAVEDIGGER_GHOUL_CID / DISAPPEAR_CID - 注意前两个以 fn_ptr 结尾 (全小写), EQUIP_DISPLAY_OP_PARAM_1A1 全大写; 均符合规则且 grep 无碰撞 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | N/A | Seg-8a 无新 carve / 无新 USER-label 全局槽; fn-ptr 均作 EQ 常量处理 |
| C8 | 无残留 stale FUN_ | PASS | grep `FUN_[0-9a-fA-F]{8}` 在 L18116-19056 范围内 0 命中 |
| C9 | plate/EOL 文本纯 ASCII | **NEEDS_FIX** | 现存 10 条 mojibake 注释行需 ASCII 重写; 6 条提议 ASCII plate 本身纯 ASCII (C9 字面合规); **但 plate #6 (tick_equip_display_by_card_id_group_a_4state) ASCII 文本含 5 处 BST 映射错误** (类型号对调/CID 误标), 违反 "faithful" 要求 - 详见修改清单 #1 |
| C10 | 指针表条目 +1 (THUMB), fn-ptr 值 == ROM raw | PASS | 0x080905e9 = fn@0x080905e8 (PUSH 0xb570 已核实) +1; 0x0805000d = fn@0x0805000c (PUSH 0xb570 已核实) +1; FS table THUMB+1: ROM[0x09e3fc60]=0x080827d5 = fn@0x080827d4 + 1 (PUSH 0xb5f0 已核实) |
| C11 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | PASS | 7 个函数名与 ASM 功能一致, 无误名信号 |
| C12 | 关键槽语义有 file:line + 置信度证据 | PASS | 4 个 CID 槽和 3 个新 EQ 常量均有 asm/10 L-number 引用 + 置信度标注; fn-ptr 有 naming-proposals.csv 或 asm 内 EOL 佐证 |
| C13 | 段内全部残留自动名槽 100% 覆盖 | PASS | ASM L18116-19056 内独立清点 DAT_/DWORD_/PTR_ = 49 个; proposal 分区: 10 RENAME + 1 DAT_(R4) + 38 EQ = 49; 集合恰好覆盖 |

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单 (逐条可执行)

### #1 — C9/R5 — Plate #6 (tick_equip_display_by_card_id_group_a_4state) BST 映射错误

**位置**: proposal §PLATE 第 6 条 (L18846) ASCII 重写文本

**问题**: ASCII plate 重写复制了原 mojibake plate 中的五处错误, 未与 ARM 机器码核对:

| 错误 | Proposal 写的 | ARM 代码真相 |
|------|--------------|-------------|
| a | `0x12ed(Gravedigger Ghoul)->type 1` | `0x12ed -> beq LAB_08082a08 -> movs r1,#2` = **type 2** |
| b | `0x1515(Disappear)->type 2` | `0x1515 -> beq LAB_08082a14 -> movs r1,#1` = **type 1** |
| c | `0x14a4(Amazoness Swords Woman, computed 0xa4<<5=0x1480)->type 5` | `movs r0,#0xa4; lsls r0,r0,#0x5 => r0=0x1480` (不等于 0x14a4); CID 0x1480 = Kycoo the Ghost Destroyer (card_0839, pw=88240808); `r2==0x1480 -> beq LAB_08082a08 -> movs r1,#2` = **type 2** |
| d | 缺失节点 | `adds r0,#0xc` after 0x12ed miss => `r0=0x12f9` (Soul Release, card_0680 pw=05758500); `r2==0x12f9 -> beq LAB_08082a10 -> movs r1,#5` = **type 5** |

**ARM 代码证据** (ASM L18864-18912, 已独立阅读):
```
L18864: movs r0,#0xa4        ; r0=0xa4
L18865: lsls r0,r0,#0x5      ; r0=0xa4<<5=0x1480 (Kycoo the Ghost Destroyer)
L18866: cmp r2,r0             ; r2 vs 0x1480
L18867: beq LAB_08082a08      ; 0x1480 -> type 2
L18870: ldr r0, DWORD_080829dc  ; r0=0x12ed
L18871: cmp r2,r0
L18872: beq LAB_08082a08      ; 0x12ed -> type 2
L18873: adds r0,#0xc          ; r0=0x12f9 (Soul Release)
L18874: b LAB_080829fe        ; -> cmp r2,0x12f9; beq LAB_08082a10 -> type 5
L18884: ldr r0, DWORD_080829f8  ; r0=0x1515
L18886: beq LAB_08082a14      ; 0x1515 -> type 1 (movs r1,#1)
L18881: beq LAB_08082a0c      ; 0x183c -> type 3 (movs r1,#3) [CORRECT]
L18897: beq LAB_08082a10      ; 0x1996 -> type 5 (movs r1,#5) [CORRECT]
LAB_08082a08: movs r1,#0x2    ; type 2
LAB_08082a0c: movs r1,#0x3    ; type 3
LAB_08082a10: movs r1,#0x5    ; type 5
LAB_08082a14: movs r1,#0x1    ; type 1
```

**修正后 plate 中的 BST 描述** (仅替换 card_id BST 那句话):
```
card_id BST dispatch: 0x12ed(Gravedigger Ghoul)->type 2,
0x12f9(Soul Release, computed DWORD_080829dc+0xc=0x12ed+0xc)->type 5,
0x1480(Kycoo the Ghost Destroyer, computed 0xa4<<5)->type 2,
0x1515(Disappear)->type 1, 0x183c(Dark Blade the Dragon Knight)->type 3,
0x1996(White Horns Dragon)->type 5.
```

注: 0x12f9 是通过 `adds r0,#0xc` 计算得出, 无对应 DWORD_ 字面池槽, 无需新建 EQ 常量.

**不受影响的内容** (无需修改):
- CID EQ 槽名: GRAVEDIGGER_GHOUL_CID (0x12ed), DISAPPEAR_CID (0x1515) - **正确**
- CID REUSE: DARK_BLADE_THE_DRAGON_KNIGHT_CID (0x183c), WHITE_HORNS_DRAGON_CID (0x1996) - **正确**
- BLK1 fn_eligible_two_pronged_attack CID=0x12e7 验证 - **正确**
- 所有 EQ slot 值 vs ROM 字节 - **全部正确**
- Consumer evidence file:line 引用 - **正确**
- C13 覆盖计数 49 - **正确**

---

## 独立核验记录 (Phase 1)

### BLK1 ref-scan (独立重跑)
- `raw 0x080827d4`: 0 hits
- `THUMB 0x080827d5`: 1 hit @ 0x09e3fc60 (FS handler table entry +0x14 for CID 0x12e7 Two-Pronged Attack)
- 巧合命中: raw 0x08082802 -> 0x9d5f662 (压缩资产), raw 0x08082808 -> 0x9d5f66a (压缩资产)
- 判定: R4 disasm (1 valid THUMB+1 ref)

### BLK2 ref-scan (独立重跑)
- `raw 0x080828c4`: 1 hit @ 0x080828ac (JT entry 已在 ASM 解码为 `.word 0x080828c4`)
- `THUMB 0x080828c5`: 0 hits
- JT sub-stubs raw refs: 0x828f4@0x828b4, 0x82924@0x828bc, 0x82954@0x828b0/b8/c0 - 全部来自 JT 内部
- 判定: R4 disasm (1 valid raw ref from JT)

### FS table CID 验证
- ROM[0x09e3fc4c] = 0x12e7 (CID = Two-Pronged Attack, card_0671 pw=83887306)
- ROM[0x09e3fc60] = 0x080827d5 (fn_eligible+1 = BLK1 THUMB+1)
- entry format [+0x0]=CID, [+0x14]=fn_eligible+1: offset 0x60-0x4c=0x14 确认

### 全部 EQ ROM 字节核对
- 38 个 hex-value 槽全部独立 python 核对通过

### card-stats.s CID 验证
- 0x12ed: card_0675 Gravedigger Ghoul pw=82542267 - 确认
- 0x1515: card_1087 Disappear pw=24623598 - 确认
- 0x183c: DARK_BLADE_THE_DRAGON_KNIGHT_CID 已在 card_info.inc:606 - REUSE 确认
- 0x1996: WHITE_HORNS_DRAGON_CID 已在 card_info.inc:553 - REUSE 确认

### fn-ptr 目标验证
- ROM[0x080905e8] hword=0xb570 (PUSH, fn start 确认)
- ROM[0x0805000c] hword=0xb570 (PUSH, fn start 确认); asm/05 check_equip_slot_eligible_by_card_id_and_prereqs 确认
- 0x080905e9 raw ref count: 20 (与 proposal 一致)
- 0x0805000d raw ref count: 114 (与 proposal 一致)

### 分段边界确认
- ROM[0x08082b18] hword=0xb500 (PUSH{lr}) - 函数边界确认
- ROM[0x080829bc] hword=0xb570 - tick_equip_display_by_card_id_group_a_4state 入口确认

### 其他 BLK2 验证
- 4 sub-stubs 入口: 0x828c4 (0x78aa), 0x828f4 (0x78a9), 0x82924 (0x78a9), 0x82954 (0xf014)
- BLK2 结束于 0x829bc (hword=0xb570 = 下一函数入口)
- 所有 BLK2 字节 [0x828c4..0x829bc) 有 4 个 sub-stub 覆盖 (0x30+0x30+0x30+0x68=0xf8 bytes = BLK2 size)

---

## Reviewer Verdict: F10-Seg-8a = NEEDS_FIX(1 items)
