# Refine Review: F10-Seg-3

> Range: [0x0807be2c, 0x0807cd68) -- 19 fn, 68 pool labels, 2 ROM_INCBIN
> Reviewer: independent (no executor output trusted without re-verification)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | Seg-3 [0x7be2c..0x7cd68) 与 §五 路线图完全一致; Seg-2 (commit 1472a5a) 已落地; 无跳号/回头 |
| C2 Rule2 | PASS | 独立 grep 确认 Seg-3 内 2 个 ROM_INCBIN (L5780/L5811); 均分配 R4 disasm; zero residue |
| C3 Rule3 | PASS | 独立重跑 ref-scan: BLK1 THUMB+1=1 (at ROM 0x01e45290); BLK2 stub A..I raw=1/1/1/1/1/1/1/1/21; 全部有引用, 无 0-ref 块 |
| C4 EQ values | PASS | 随机抽查 35 处 EQ 槽 (含全部 3 个 GAS expr 槽 / 12 个 gP1LifePoints RENAME 槽 / LP_CARD_TRACK_ALT_OFF) ROM 字节核对全部吻合 |
| C5 REUSE dedup | PASS | LP_CARD_TRACK_ALT_OFF=0x1dac grep constants/*.inc 0 命中, 确为 NEW; 11 个 REUSE 值逐一按 VALUE grep 命中现有名 (P1LP_BLOCK2_OFF_1CE8/PLAYER_BLOCK_STRIDE 用紧凑格式 0x1ce8/0x868 存在于 ewram.inc L275/L250) |
| C6 Label names | PASS | 全部 32 个新槽标签 + 11 个 disasm 标签符合 ^[a-z][a-z0-9_]+$; 无碰撞 |
| C7 REF_SLOTS | PASS | 3 个 REF 槽均有 USER-label + DATA-ref 计划; check_equip_activation_at_slot11_1 alias 在 rom.s L73 确认存在; fn addrs 0x08065990/0x08090624 首 hword=0xb570 (push lr 确为函数头) |
| C8 stale FUN_ | PASS | 独立 grep: Seg-3 L4358..L6238 范围内 FUN_[0-9a-f]{8} 命中 0 处 |
| C9 ASCII plate/EOL | PASS | proposal.md 文件中 CJK 仅出现在 Consumer Evidence 引用现有 @ 注释文本 (引用 asm L6048 处 plate 内容), 非 Ghidra 命令文本; PLATE=1 行动仅重命名函数 label (drop __0807c388), 不新写 CJK; Seg-3 asm 内 25 处非 ASCII 行是历史 mojibake @ 注释, 非本 Seg-3 proposal 引入 |
| C10 carve ptr+1 | N/A | 无 carve 计划; 派发表 0x7c8b8 为 RAW 指针入 THUMB 代码 (29 entry 全部 raw, 经 ROM 读取确认); BLK1 fn_eligible 在 FS 表以 THUMB+1=0x0807c87d 引用 (正确); BLK2 pool word 逐个 ROM 核对全部吻合 |
| C11 FUNC_RENAME | PASS | tick_equip_activation_display_state__0807c388 -> tick_equip_activation_display_state; indeg=0 独立验证 (asm/*.s 全扫无 bl 调用); 唯一引用为函数标签本身 L5116; __0807c388 不出现在 plate 文本中; 函数体 (4 态装备激活显示 FSM 0x80/0x7f/0x7d/0x7c) 与新名语义一致 |
| C12 R6 semantics | PASS | 6 个关键槽均有 file:line + high 置信度证据; 无零容忍词; LP_CARD_TRACK_ALT_OFF 语义 (gP1LifePoints+0x1dac, 4 raw ROM refs 独立计数确认) 描述充分 |
| C13 full count | PASS | 独立 python 扫描 [0x0807be2c, 0x0807cd68): 68 个自动名标签 (DAT_/DWORD_ 无 PTR_DAT_/UNK_); 与 proposal 52+3+13=68 完全一致; 无遗漏, 无越界 |

---

## 附加核验备注

### BLK1 (fn_eligible_des_frog) 结构核实

- +0x00: `00 00` = 2B pad (ROM 0x7c87a); 对应 proposal `des_frog_fn_eligible_pad` 标签
- +0x02: `f0 b5` = 0xb5f0 = `push {r4,r5,r6,r7,lr}` (THUMB); fn 起始 0x0807c87c
- +0x32: `87 46` = 0x4687 = `MOV PC,r0` (THUMB 指令, 非数据字); 已标 pool-vs-code trap NOT createDWord -- 正确
- +0x36: `90 b2 01 02` = 0x0201b290 = gDuelPhaseFlags (createDWord 0x0807c8b0) -- 正确
- +0x3a: `b8 c8 07 08` = 0x0807c8b8 = dispatch_table_base (createDWord 0x0807c8b4) -- 正确
- BLK1 共 62 bytes = 0x3e; 全覆盖无残留

### BLK2 (sub-stubs A..I) 结构核实

- 9 个 sub-stub 连续覆盖 0x0807c92c..0x0807ca84 = 344 bytes = 0x158; 全覆盖验证通过
- 派发表 (0x7c8b8..0x7c928, 29 entry): entry 00 = 0x0807ca74 (H), entry 01-17 = 0x0807ca7a (I, default=21 次), entry 18=G, 19=F, 20=E, 21-24=I, 25=D, 26=C, 27=B, 28=A -- 与 proposal 对应
- 11 个 createDWord pool 地址逐一 ROM 核对全部吻合
- pool-vs-code 排除 (0x0807c95c=0xe00a / 0x0807ca08=0xe038, 均为 THUMB 跳转指令) -- 正确

### CID 位置说明

- FS 表结构经独立验证: 6-word entry, CID 在 entry_base (+0), fn_eligible+1 在 entry_base+4。
- 对 Des Frog: fn_eligible+1 = 0x0807c87d 在 0x09e45290; CID = 0x1918 在 0x09e4528c (= fn_eligible_slot - 4)。
- MEMORY.md doc 描述的 "-0xc" 规则适用于不同表结构, 本段表中 CID 在 fn_eligible_slot - 4。
- 这不影响 proposal 正确性: CID=0x1918=DES_FROG_CID 已被正确识别 (card_info.inc L1247 独立确认)。

### GAS 表达式 (gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF)

- 0x0201b290 + 0x000004a4 = 0x0201b734 (python 验证)
- ROM 实际值: DWORD_0807bef0/bf30/bf4c 均为 0x0201b734 (独立 ROM 读取)
- 无需新建常量, GAS 表达式在汇编时求值 -- 字节等效

### LP_CARD_TRACK_ALT_OFF 新常量

- 值 0x00001dac; ewram.inc 中 0 命中 (确为新建); 4 raw ROM refs 独立计数: 0x0807cc9c / 0x080a2164 / 0x080a21a0 / 0x080a21e4
- 置于 LP_CARD_TRACK_NEXT_OFF (L248) 之后, 语义 (LP card-track 数组 +4 偏移) 充分

---

## 状态: PASS

所有 C1-C13 检查均通过。proposal 数据精确, 无遗漏, 无误分类。fixer 可直接进入模式 B 落地。

---

## 修改清单

无 (PASS, 无需修改)。

---

## Reviewer Verdict: F10-Seg-3 = PASS
