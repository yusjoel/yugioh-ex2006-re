# Refine Review: F09-Seg1R2 (Remediation Cluster-2)

> Reviewer: independent, self-run ref-scan + ROM byte verification
> Scope: doc/dev/refine/F09-Seg1R2.proposal.md
> ROM: roms/2343.gba (33,554,432 bytes)
> Expected SHA1: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | OK | Seg-1R2 是 Seg-1 事后修补 addendum，继承自 F09-Seg1R Cluster-1 (commit e9636e1)，地址序无回头 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | FAIL | 见 #1 -- equip_lp_sub_fa4c .byte body 0x806fa4e/0x10 在 scope 内但未列入 disasm 计划 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | §5.1=0；9 个 ROM_INCBIN 块均有引用（B1/B6 THUMB+1 x2，B2-B5/B7-B9 raw dispatch table）。自主重跑 ref-scan 全部确认（见独立验证节）。mid-body raw=2/THUMB+1=1 均为 compressed data false positive（见 C3 详证） |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 全部 19 个 pool DWORD 自主读取确认（python struct.unpack LE）：结果全部 == 提案值 |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | OK | 4 个 NEW 常量逐值精确匹配（提取 .equ 数值比对，排除 substring false alarm）：均 0 命中。14 个 REUSE 均已在 named .inc 中存在（逐一确认） |
| C6 R2 名 | 槽名合法无碰撞 | OK | 全部 18 个 slot label 均符合 `^[a-z][a-z0-9_]+$`；无命名碰撞 |
| C7 R3 接通 | REF_SLOTS 有 USER-label + DATA-ref | OK | REF=2：equip_lp_tbl_f990->equip_lp_disp_table_f994 + equip_chain_tbl_fe10->equip_chain_act_disp_table_fe14，均有现有 asm label 目标 |
| C8 R5 现名 | plate 无残留 FUN_ | OK | PLATE=0；提案无 plate/EOL 定义。两个 cluster 区域的 asm 无 FUN_ plate 残留 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | PLATE=0，无 Ghidra plate/EOL 定义。提案文档含 § (U+00A7, UTF-8 0xc2a7) 但在 Phase 4 Self-Check 散文中，非 plate/EOL 定义，不违规（同 F09-Seg1R.review.md 前例） |
| C10 carve | 指针表条目 THUMB+1 | OK N/A | carve=0；B1/B6 fn_eligible 由 FS 表 THUMB+1 引用，已在 C3 独立验证 |
| C11 误名 | 函数体全局 vs 函数名无矛盾 | OK | 两个 fn_eligible 命名与 FS 表 CID 对应（eligible_destiny_board_f85c/CID=0x1468, eligible_cathedral_of_nobles_fdec/CID=0x146f）；FUNC_RENAME=0 合理 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | OK | 所有 9 个块的 consumer evidence 均有 BL target + dispatch table ROM 地址（conf:high）；两个 med-conf 新常量 (OAM_EQUIP_LP_SPRITE_P1_5E/CARD_DISPLAY_OP31_LP_BAR_SUB) 命名描述性但中性，未过度声明语义 |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | FAIL | 见 #1 -- equip_lp_sub_fa4c .byte body 0x806fa4e/0x10 未覆盖，导致 post-remediation .byte-code residue != 0 |

---

## 独立验证结果

### ref-scan (自主重跑, raw + THUMB+1)

**ENTRY ref-scan 结果 (全部 block entries):**

| Block | Entry | raw 命中 | THUMB+1 命中 | 判断 |
|-------|-------|---------|------------|------|
| B1  | 0x0806f85c | 0 | 2 @ 0x1e40a90, 0x1e43a30 | CODE (fn_eligible THUMB+1) |
| B2  | 0x0806fa08 | 1 @ 0x6fa04 | 0 | CODE (dispatch_table[28]) |
| B3  | 0x0806fa5e | 1 @ 0x6f9fc | 0 | CODE (dispatch_table[26]) |
| B4  | 0x0806fa74 | 1 @ 0x6f9f8 | 0 | CODE (dispatch_table[25]) |
| B5  | 0x0806fb14 | 1 @ 0x6f9f4 | 0 | CODE (dispatch_table[24]) |
| B2c | 0x0806fb4c | 1 @ 0x6f9e4 | 0 | CODE (dispatch_table[20]) |
| B2d | 0x0806fb58 | 1 @ 0x6f9e0 | 0 | CODE (dispatch_table[19]) |
| B2e | 0x0806fb64 | 1 @ 0x6f9dc | 0 | CODE (dispatch_table[18]) |
| B2f | 0x0806fb70 | 1 @ 0x6f994 | 0 | CODE (dispatch_table[0]) |
| B2g | 0x0806fb76 | 20 @ 0x6f998..0x6f9f0 x17 | 0 | CODE (shared epilogue) |
| B6  | 0x0806fdec | 0 | 2 @ 0x3d3eb6, 0x1e46610 | CODE (fn_eligible THUMB+1) |
| B7  | 0x0806fe88 | 1 @ 0x6fe84 | 0 | CODE (dispatch_table[28]) |
| B8  | 0x0806fedc | 1 @ 0x6fe80 | 0 | CODE (dispatch_table[27]) |
| B9  | 0x0806fef0 | 2 @ 0x6fe7c, 0x47ec0d | 3 @ 0x22ffb3, 0x3381e0, 0x4a46b5 | CODE (dispatch_table[26]) |
| B7c | 0x0806ff0a | 1 @ 0x6fe3c | 0 | CODE (dispatch_table[10]) |
| B7d | 0x0806ff1a | 1 @ 0x6fe38 | 0 | CODE (dispatch_table[9]) |
| B7e | 0x0806ff2c | 1 @ 0x6fe34 | 0 | CODE (dispatch_table[8]) |
| B7f | 0x0806ff3c | 1 @ 0x6fe14 | 0 | CODE (dispatch_table[0]) |
| B7g | 0x0806ff46 | 22 @ 0x6fe18..0x6fe7b x21 | 0 | CODE (shared epilogue) |

**MID-BODY 0-ref 确认 (自主重跑):**

全部 9 个 ROM_INCBIN block-start 地址 raw=0, THUMB+1=0。B6-mid (0x806fdee) raw=2、B9-mid (0x806fef2) raw=1 THUMB+1=1 详见 C3 分析。

### C3 可疑引用独立分析

**B6 mid-body 0x806fdee raw=2 原因:**
- 命中 0x38c775: mod4=1 (非 4B 对齐) -> 绝对非指针。
- 命中 0x4b4f44: mod4=0 (4B 对齐)，但 GBA 地址 = 0x08000000 + 0x4b4f44 = 0x0b4b4f44，超出 ROM 合法区间 [0x08000000, 0x09FFFFFF]，不是有效 GBA ROM 指针。上下文字节 0xe6 0xe0 0xe3 0xee 0xfd 0x06 0x08 0xfa 0xfe 0xf8 = 压缩/加密数据特征 (值主要在 0xe0..0xff 范围)。判定: 压缩数据巧合匹配，conf:high。

**B9 mid-body 0x806fef2 raw=1 THUMB+1=1 原因:**
- raw 命中 0x15903f: mod4=3 (非对齐)。
- THUMB+1 命中 0x17ca27: mod4=3 (非对齐)。
- 两个均非 4B 对齐 -> 绝对非指针。
- B9 真正引用: dispatch_table[26] @ 0x806fe7c = 0x0806fef0 (entry, raw=1, authentic)。

**B6 THUMB+1 命中 0x3d3eb6:**
- mod4=2 (非 4B 对齐) -> 绝对非指针。

结论: 全部可疑 mid-body 引用均为 false positive，C3 OK。

### FS handler table 验证 (B1, B6)

**B1 (eligible_destiny_board_f85c):**
- ROM 0x1e40a90: [+0x00]=NULL, [+0x04]=NULL, [-0x04]=0x1468 (CID Destiny Board), [0]=0x0806f85d (fn_eligible+1 OK)
- ROM 0x1e43a30: [-0x04]=0x1468, [0]=0x0806f85d OK (second variant entry)
- card_info.inc:578 DESTINY_BOARD_CID=0x1468 confirmed

**B6 (eligible_cathedral_of_nobles_fdec):**
- ROM 0x1e46610: [-0x04]=0x146f (CID Cathedral of Nobles), [0]=0x0806fded (fn_eligible+1 OK)
- card-stats.s L12300: slot=0x146F Cathedral of Nobles confirmed

### dispatch table 验证

**equip_lp_disp_table_f994 @ 0x806f994 (29 entries):**
- [0]=0x806fb70 (B2f) OK, [1..17,21..23]=0x806fb76 (B2g) OK, [18]=0x806fb64 (B2e) OK, [19]=0x806fb58 (B2d) OK, [20]=0x806fb4c (B2c) OK, [24]=0x806fb14 (B5) OK, [25]=0x806fa74 (B4) OK, [26]=0x806fa5e (B3) OK, [27]=0x806fa4c (equip_lp_sub_fa4c -- see C2 issue), [28]=0x806fa08 (B2) OK

**equip_chain_act_disp_table_fe14 @ 0x806fe14 (29 entries):**
- [0]=0x806ff3c (B7f) OK, [1..7,11..25]=0x806ff46 (B7g) OK, [8]=0x806ff2c (B7e) OK, [9]=0x806ff1a (B7d) OK, [10]=0x806ff0a (B7c) OK, [26]=0x806fef0 (B9) OK, [27]=0x806fedc (B8) OK, [28]=0x806fe88 (B7) OK

### pool DWORD 字节核对 (全部 19 个)

全部 19 个 pool 地址 4 字节 LE 读取与提案值完全一致 (见 ROM 核对表)。代表性验证:

| 地址 | ROM 值 | 提案值 | 名称 |
|------|--------|--------|------|
| 0x806f92c | 0x00000868 | 0x00000868 | PLAYER_BLOCK_STRIDE |
| 0x806f930 | 0x0201c510 | 0x0201c510 | gDuelFieldSlots |
| 0x806f934 | 0x0000805e | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E |
| 0x806f954 | 0x00001497 | 0x00001497 | SPIRIT_MESSAGE_I_CID |
| 0x806f95c | 0x00001498 | 0x00001498 | SPIRIT_MESSAGE_N_CID |
| 0x806f964 | 0x00001499 | 0x00001499 | SPIRIT_MESSAGE_A_CID |
| 0x806f988 | 0x0000149a | 0x0000149a | SPIRIT_MESSAGE_L_CID |
| 0x806f98c | 0x0201b290 | 0x0201b290 | gDuelPhaseFlags |
| 0x806f990 | 0x0806f994 | 0x0806f994 | equip_lp_disp_table_f994 |
| 0x806fa40 | 0x0000e09a | 0x0000e09a | b+pad A |
| 0x806fb04 | 0x0000805e | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E B4 |
| 0x806fb08 | 0x00001379 | 0x00001379 | GRAVEROBBER_CID |
| 0x806fb0c | 0x0201b290 | 0x0201b290 | gDuelPhaseFlags B4 |
| 0x806fb10 | 0x000004a4 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF |
| 0x806fb48 | 0x0000805e | 0x0000805e | OAM_EQUIP_LP_SPRITE_P1_5E B5 |
| 0x806fe0c | 0x0201b290 | 0x0201b290 | gDuelPhaseFlags B6 |
| 0x806fe10 | 0x0806fe14 | 0x0806fe14 | equip_chain_act_disp_table_fe14 |
| 0x806fed4 | 0x0000e038 | 0x0000e038 | b+pad B7 |
| 0x806fed8 | 0x0000011d | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB |

### C5 精确值匹配 (以 .equ 数值提取, 非 substring grep)

| 常量 | 值 | 精确命中数 | 判定 |
|------|-----|-----------|------|
| SPIRIT_MESSAGE_N_CID | 0x1498 | 0 | NEW confirmed |
| SPIRIT_MESSAGE_A_CID | 0x1499 | 0 | NEW confirmed |
| OAM_EQUIP_LP_SPRITE_P1_5E | 0x805e | 0 | NEW confirmed |
| CARD_DISPLAY_OP31_LP_BAR_SUB | 0x011d | 0 | NEW confirmed |

注: 初步 substring grep 误报了 0x1498 (命中 0x1483 行) 等，改用 .equ 值域精确匹配后全部 0 命中。

REUSE 确认: PLAYER_BLOCK_STRIDE(duel_field.inc:173), gDuelFieldSlots(ewram.inc:313), SPIRIT_MESSAGE_I_CID(card_info.inc:802), SPIRIT_MESSAGE_L_CID(card_info.inc:569), gDuelPhaseFlags(ewram.inc:352), GRAVEROBBER_CID(card_info.inc:453), EQUIP_PHASE_FRAME_OFF(ewram.inc:436), DESTINY_BOARD_CID(card_info.inc:578) -- 全部存在。

### 指令级解码验证 (独立 ROM 字节解码)

**B1 ldr+b+.word CID pattern (0x806f950..0x806f967):**
- 0x6f950: 0x4b00 = ldr r3,[pc,#0] OK
- 0x6f952: 0xe00a = b imm11=10, offset=0x14, PC=0x6f956, target=0x6f96a OK
- 0x6f954: 0x00001497 = SPIRIT_MESSAGE_I_CID OK
- 0x6f958: 0x4b00 = ldr r3,[pc,#0]
- 0x6f95a: 0xe006 = b imm11=6, offset=0xc, PC=0x6f95e, target=0x6f96a OK
- 0x6f95c: 0x00001498 = SPIRIT_MESSAGE_N_CID OK
- 0x6f960: 0x4b00 = ldr r3,[pc,#0]
- 0x6f962: 0xe002 = b imm11=2, offset=4, PC=0x6f966, target=0x6f96a OK
- 0x6f964: 0x00001499 = SPIRIT_MESSAGE_A_CID OK

**B6 body (0x806fdee) key instructions:**
- 0x6fdee: 0x1c04 = adds r4,r0,#0 OK
- 0x6fe00: 0xe0a1 = b imm11=161, offset=0x142, PC=0x6fe04, target=0x6ff46 (equip_chain_act_sub_ff46) OK
- 0x6fe0a: 0x4687 = mov r15,r0 (computed dispatch) OK

**B2g shared epilogue (0x806fb78..0x806fb86):**
- 0xb006 add sp,#0x18 / 0xbc38 pop {r3,r4,r5} / 0x4698 mov r8,r3 / 0x46a1 mov r9,r4 / 0x46aa mov r10,r5 / 0xbcf0 pop {r4,r5,r6,r7} / 0xbc02 pop {r1} / 0x4708 bx r1 -- 全部 OK

**B8 body start (0x806fede):**
- 0x07c8 = lsls r0,r1,#31 OK (提案说 lsls r0,r1,#0x1f)
- b at 0x6feee: 0xe02b, target=0x6fef2+0x56=0x6ff48 OK

**b+pad byte-identity:**
- 0x806fa40 = 0x0000e09a: b imm11=0x9a, offset=0x134, target=0x806fa44+0x134=0x806fb78 OK
- 0x806fed4 = 0x0000e038: b imm11=0x38, offset=0x70, target=0x806fed8+0x70=0x806ff48 OK

**.word 0x00004708 at 0x806ff4c:**
- LE bytes: 08 47 00 00 = bx r1 (0x4708) + .zero 2 (0x0000)
- DisassembleCommand will decode as bx r1 + 2B zero pad -> byte-identical OK

---

## 修改清单

### #1 -- C2/C13 -- equip_lp_sub_fa4c .byte body 0x806fa4e/0x10 未列入 disasm 计划

**问题:**

dispatch_table[27] @ 0x806fa00 = 0x806fa4c，指向 equip_lp_sub_fa4c。该 stub 的 entry 指令 (lsls r0,r5,#0x1f @ 0x806fa4c) 已在 asm 中解码，但其 .byte body (0x806fa4e..0x806fa5d, 16 字节) 未被任何 proposal block 覆盖。该地址在声明的 scope [0x6f85e..0x6fef4) 内。

ref-scan 确认: entry 0x806fa4c raw=1 @ 0x6fa00 (dispatch_table[27]) THUMB+1=0 -> CODE。

.byte body 机器码独立解码:
- 0x6fa4e: 0x0fc0 = lsrs r0,r0,#31
- 0x6fa50: 0x4641 = mov r1,r8
- 0x6fa52: 0x880a = ldrh r2,[r1,#0]
- 0x6fa54: 0x2106 = movs r1,#0x6
- 0x6fa56/58: 0xf024/0xfbb5 = BL 0x080941c4 (init_effect_slot_display_context)
- 0x6fa5a: 0x207e = movs r0,#0x7e
- 0x6fa5c: 0xe08c = b imm11=0x8c, offset=0x118, target=0x806fa60+0x118=0x806fb78 (B2g 共享 epilogue body 入口 OK)

**要求修复:** 在 disasm plan Step A9 (B2, eligible_sub_stubs_fa08) 之前、Step A2 (B2f) 之后，插入:

**Step A2b -- equip_lp_sub_fa4c body (新增步骤)**

- clearListing(0x0806fa4e, 0x0806fa5e)  [.byte body 16 字节; entry at 0x6fa4c 已解码, 无需 clear]
- DisassembleCommand(0x0806fa4e)
- 预期: 8 条指令 (lsrs r0,r0,#31; mov r1,r8; ldrh r2,[r1,#0]; movs r1,#0x6; BL init_effect_slot_display_context; movs r0,#0x7e; b LAB_0806fb78)
- 无 createDWord 需要 (body 内无 PC-relative LDR 池)
- 执行时机: 必须在 B2g (Step A1) 之后 (LAB_0806fb78 须已创建)

**必须在 Ghidra 脚本中加入此步骤，否则 post-remediation .byte-code 残余 != 0。**

**对 C13 post-remediation proof 的修正:**

| Block | ROM off / size | 当前计划 | 修正后 |
|-------|----------------|---------|--------|
| equip_lp_sub_fa4c .byte | 0x6fa4e / 0x10 | 未列入 | DISASM (Step A2b) |

修正后 post-remediation .byte-code residue in [0x6f85e..0x6fef4): 0 (原为 1 block)

---

## 通过检查汇总

- C3: 9 个 ROM_INCBIN block 的 entry ref-scan 自主重跑验证完毕，全部有有效引用。可疑 mid-body 引用 (B6-mid raw=2, B9-mid raw=1 THUMB+1=1) 均为 compressed data false positive（对齐错或 GBA 地址超 ROM 范围），不影响 CODE 分类。
- C4: 全部 19 个 pool DWORD 自主读取 OK。
- C5: 4 个 NEW 常量精确值匹配 0 命中；14 个 REUSE 全部存在。CID 0x1498/0x1499/0x146f 在 card-stats.s 中独立确认。
- C6: 所有 slot label 合法，无碰撞。
- C8: PLATE=0，无 FUN_ 残留。
- C9: 提案 § 符号在 doc 散文中，非 plate/EOL，不违规。
- C10: carve=0，N/A。
- C11: fn_eligible 命名与 FS 表 CID 对应，无误名信号。
- C12: 9 个 consumer evidence 有 BL target + dispatch table 证据 (conf:high)；2 个 med-conf 新常量命名中性描述性，可接受。
- disasm 执行顺序: B2g (shared epilogue) first 正确；B7g (shared epilogue) first 正确；clearListing 边界不覆盖 pool DWORDs；b+pad byte-identity OK；.word 0x00004708 byte-identity OK。
- B9 范围 (0x6fef2+0x18=0x6ff0a) 超出声明 scope end (0x6fef4)：提案已在 NOTE 中说明，由同一 Ghidra 脚本一并处理，属合理扩展。B7c-B7g (0x6ff0c..0x6ff4c) 超 scope 同理。

---

## 状态: NEEDS_FIX(1 item)

修复要求: 在 disasm plan 中加入 Step A2b (equip_lp_sub_fa4c .byte body 0x806fa4e/0x10 的 clearListing + DisassembleCommand)，更新 C13 post-remediation proof table，使 .byte-code residue 计数归零。其余各项全部通过，修复后可直接落地。

---

## Reviewer Verdict: F09-Seg1R2 = NEEDS_FIX(1 item)
