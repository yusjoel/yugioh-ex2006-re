# Refine Review: F09-Seg-8 REMEDIATION

Reviewer: refine-reviewer (independent)
Date: 2026-06-21
Proposal: `doc/dev/refine/F09-Seg8R.proposal.md`
Module: `asm/09_equip_lp_display.s`
Range: [0x0807629c, 0x0807738c) -- Seg-8 partial-disasm remnants from commit 1e38556

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | p5-refine-09 §三 表: Seg-8 [0x7629c,0x7738c) commit 1e38556, 最后一个有残留的已完成段; remediation 是下一步 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块都有归宿 | PASS | 独立 grep: Seg-8 范围内恰好 4 个 (1 ROM_INCBIN + 3 .byte); proposal 覆盖全部 4 个 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | proposal §5.1=0; 所有 4 块均有消费引用 (2 beq + 2 ldr pc-rel); ref-scan 结果与分类一致 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立 python 读: 0x08076720 = {31,15,00,00} = 0x00001531 (DARK_SCORPION_BURGLARS_CID); 0x0807677c = {68,08,00,00} = 0x00000868 (PLAYER_BLOCK_STRIDE) -- 均与 proposal 一致 |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | PASS | grep 按值: 0x1531 仅 card_info.inc:1476; 0x868 仅 ewram.inc:250 (含多处用途引用). 2 EQ 均为 REUSE, 无新建 |
| C6 R2 名 | 槽名合法, 无碰撞 | PASS | createDWord 后 Ghidra 自动命名 DWORD_08076720 / DWORD_0807677c; 代码块用 LAB_ (Ghidra 自动); 无自定义命名冲突 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | Block C/D 均为 pc-rel ldr 字面量池 (intra-fn); 无外部 .word 指针 (ref-scan raw=0/thumb=0); createDWord+equate 足够, 不需要 REF_SLOT 接通 |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | PASS | grep 扫 Seg-8 asm 行 [17601..20014]: 0 FUN_ 残留; proposal 无 plate 操作 (PLATE=0) |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | proposal 文件全 ASCII 确认 (python 扫描); 两条 EOL comment 字符串均纯 ASCII |
| C10 carve | 指针表条目 +1 (THUMB) / .word fn+1 == ROM raw 值 | PASS | Block A/B 是条件分支目标, 不是 fn-ptr 表条目; Block C/D 是字面量池 DATA 整数 (非函数指针); C10 不适用于这 4 块 |
| C11 误名 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | PASS | FUNC_RENAME=0; 19 个函数命名在 1e38556 中完成; grep FUN_ = 0 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | consumer evidence 表完整; beq hw 逐一 python 验证; ldr pc-rel EA 公式验证; BL target 反算到 asm/04:9609; 置信度均 high |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | PASS | 独立 grep [lines 17601..20014]: ROM_INCBIN=1, .byte=3, 总计 4; proposal 处理 4; post-state = 0 残留 |

---

## 独立验证结果

### Block A ref-scan (自主重跑)

```
python: data.count(struct.pack("<I", 0x080768dc)) = 0  (raw)
python: data.count(struct.pack("<I", 0x080768dd)) = 0  (THUMB+1)
```

0 引用均为外部指针. 块由 `beq LAB_080768dc @ 0x08076866` 到达.

- `beq hw=0xd039`: ROM bytes @ 0x08076866 = `39d0` CONFIRMED.
- target = 0x08076866 + 4 + 0x39*2 = 0x080768dc CONFIRMED.
- 15 halfwords @ 0x080768dc 完整解码: 全部合法 THUMB16 指令 (lsrs/subs/ands/mov/muls/adds x3/movs/BL-pair/movs/b).
- 无 `ldr r,[pc,#imm]` (0x48xx 模式) 在 Block A 范围内 -- 无内部字面量池, 不需要 createDWord.
- BL 反算: hw1=0xf7cd (off_hi=0x7cd, signed=-51), hw2=0xfe57 (off_lo=0x657); target = 0x080768f2 + 4 + (-51<<12) + (0x657<<1) = 0x080445a4 CONFIRMED.
- `dispatch_equip_zone_sprite_banisher_by_field_count` @ 0x080445a4: asm/04:9609 `push {r4,r5,r6,lr} @ 080445a4 70b5` CONFIRMED (ROM bytes `70b5`).
- 末指令 `b LAB_080768fc`: hw=0xe000, target = 0x080768f8 + 4 + 0 = 0x080768fc CONFIRMED; LAB_080768fc 已解码 (asm:18487, ROM bytes `18bc` = pop{r3,r4}).

CODE 分类: 正确.

### Block B ref-scan (自主重跑)

```
python: data.count(struct.pack("<I", 0x08076750)) = 0  (raw)
python: data.count(struct.pack("<I", 0x08076751)) = 0  (THUMB+1)
```

- `beq hw=0xd00f`: ROM bytes @ 0x0807672e = `0fd0` CONFIRMED.
- target = 0x0807672e + 4 + 0x0f*2 = 0x08076750 CONFIRMED.
- 2 bytes @ 0x08076750 = `10 20` = hw 0x2010 = `movs r0,#0x10` CONFIRMED.
- Fall-through: LAB_08076752 @ 0x08076752 (asm:18274 `ldrh r2,[r4,#0x8]`) 已解码, 无空隙.

CODE 分类: 正确.

### Block C & D (createDWord)

- Block C @ 0x08076720: `ldr r0,[pc,#0x18]` @ 0x08076704 (hw=0x4806, rd=0, imm8=0x06); EA = (0x08076704+4)&~3 + 0x06*4 = 0x08076708 + 0x18 = 0x08076720 CONFIRMED; ROM[0x08076720..23] = {31,15,00,00} = 0x00001531 CONFIRMED.
- Block D @ 0x0807677c: `ldr r2,[pc,#0x1c]` @ 0x0807675e (hw=0x4a07, rd=2, imm8=0x07); EA = (0x0807675e+4)&~3 + 0x07*4 = 0x08076760 + 0x1c = 0x0807677c CONFIRMED; ROM[0x0807677c..7f] = {68,08,00,00} = 0x00000868 CONFIRMED.

DATA 分类 (createDWord): 正确. Ghidra 的半字 split artifact (Block C: 2B DAT_ + 2B fake `movs r0,r0`) 由 clearListing(0x08076720, 0x08076724) + createDWord(0x08076720) 一并消除.

### C5 by-value 去重

- 0x00001531: grep `constants/*.inc` = 1 命中: `card_info.inc:1476 DARK_SCORPION_BURGLARS_CID`. REUSE.
- 0x00000868: grep `constants/*.inc` = 1 命中 (PLAYER_BLOCK_STRIDE 的定义行): `ewram.inc:250`. REUSE.
- 两个常量在 Seg-8 之前已由 commit 1e38556 建立, proposal 正确标注 REUSE.

### C8 FUN_ sweep

python 扫描 asm lines 17601..20014: FUN_ 命中 = 0. CLEAN.

### C9 ASCII sweep

python 扫描 proposal 文件全文: 非 ASCII 字符 = 0. 两条 EOL comment 字符串均为纯 ASCII.

---

## 次要发现 (不阻塞)

**Block B asm 行号引用错误 (C12 minor)**: proposal ref-scan 表格和 Consumer Evidence 表中将 `beq LAB_08076750 @ 0x0807672e d00f` 标注为 `asm:18272`. 实际上 line 18272 是 `LAB_08076750:` (目标标签), beq 指令在 line 18251. 这是纯文档引用错误; hw decode (0xd00f) 和 target 地址 (0x08076750) 均独立验证正确. fixer 执行 Ghidra 脚本无需参考此行号.

---

## 状态: PASS

所有 C1-C13 均通过. Block A/B CODE 分类经独立字节解码确认; BL 目标反算确认; Block C/D DATA 分类经 PC-rel 公式确认; ref-scan 自主重跑均 0 引用; 两个 EQ 值 ROM 字节匹配; REUSE 按值确认; C8 FUN_=0; C9 ASCII clean; C13 完整覆盖 4/4 残留块.

fixer 可直接执行 proposal Disasm Plan (Block B -> Block A -> createDWord C -> createDWord D), 产出 DWORD_08076720 (.word DARK_SCORPION_BURGLARS_CID) 和 DWORD_0807677c (.word PLAYER_BLOCK_STRIDE), build 后验证 SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b.
