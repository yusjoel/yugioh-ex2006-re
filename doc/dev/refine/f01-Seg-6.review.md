# Refine Review: f01-Seg-6

> Reviewer: refine-reviewer (independent)
> Date: 2026-06-07
> Proposal: doc/dev/refine/f01-Seg-6.proposal.md
> ASM: asm/01_vija_scene_text.s (lines ~5165..6437)
> ROM range: [0x0801f25c, 0x08020fa8)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致, 未跳号/回头 | OK | 活动 doc §三 row 6: Seg-6 = 0x1f25c..0x20fa8 (16fn, 4 incbin). 前段 Seg-5 = 0x1e714..0x1f25c 已完成. Seg-7 border render_lp_record_text_set_b @ 0x08020fa8 在 ASM line 6437 确认 (push {r4,r5,r6,lr} @ 08020fa8). 全 16 fn + 4 块地址 < 0x08020fa8. |
| C2 Rule2 | 4 个 ROM_INCBIN 块全有归宿 | OK | Block1 (0x1f4d0/0x690) disasm R4; Block2 (0x1fb90/0x302) disasm R4; Block3 (0x202fe/0x36) disasm R4; Block4 (0x20370/0xa44) disasm R4. §5.1=0. |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 本段无 §5.1 块. |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 30 个 EQ 槽全部自行 python 读字节核对. 全匹配 (见附). |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | OK | 0xffffc03f 在全部 constants/*.inc 中未发现. 0xffc03fff (NAME_INPUT_PAGE_STATE_CLEAR) 不同值. 提案不新建常量, 以 RENAME-only 处理 — 合理. |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$ 无碰撞 | OK | 全 82 个 label 均满足正则, 无重复 (python 验证). |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | REF_SLOTS: find_card_index_in_rom_table_count_ptr (0x098973f6) / find_card_index_in_rom_table_data_ptr (0x098972f0) 各有 createLabel 计划. 值已核对. 不 carve 理由合理 (远端 FS 数据, 边界未知). |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_/DAT_/DWORD_ | OK | 新 plate (run_duel_puzzle_scene_state_machine) 全用语义名. 其余 14 fn 现有 plate 为 ASCII, 无残留自动名 (抽查 tick_duel_puzzle_scene_step @ line 5471, render_lp_record_text_set_a @ line 6144). |
| C9 ASCII | plate/EOL 文本纯 ASCII | PARTIAL FAIL | 现有 plate (line 5581) 含大量 CJK — 提案已计划修复为纯 ASCII. 提案新 plate 文本本身经逐字符检验全 ASCII (无非 ASCII). 现存 CJK 是"待修复"的目标, 不是"提案引入"的问题. **fixer 执行时须替换.** |
| C10 carve | 指针表 THUMB+1 / .word <fn>+1 核对 | OK | 步表 PTR_DAT_0801f47c / PTR_DAT_08020338 条目均为偶数原始地址 (用 .hword 0x4687 = MOV PC,R0 跳转, 非 BX). gMenuState fn-ptr 槽 ROM[0xe1c88]=0x0801fec1 (THUMB+1) 正确. 无需 .word <fn>+1 carve. |
| C11 误名 | 函数体全局 vs 函数名矛盾 | OK | 抽查: find_card_index_in_rom_table 体线性搜索 halfword 数组 (ldrh+cmp+bne 循环) 名符; render_lp_record_text_set_a 体 card-ID 二叉树 + lp 显示, 名符; run_duel_puzzle_scene_state_machine 体读 gPrng+0x202 bits[13:6] 9-case 派发, 名符. FUNC_RENAME=0 合理. |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | OK | 消费者证据节覆盖 15 条关键槽, 均含 constants/ewram.inc 行号引用或 ROM 地址证据. 置信度 high/med 标注, 无零容忍词. |
| C13 残留 | 段内所有残留自动名槽全被覆盖 | OK | 独立 grep: Seg-6 (line 5165..6437) 内共 82 个 DAT_/DWORD_ 自动名. 提案 EQ+RENAME+REF+disasm 共覆盖 82 个 (python 交叉核验). 无遗漏. |

---

## 独立 ref-scan 结论 (C2/C3 核心)

使用修正后的 scan 函数 (`base = v & ~1; THUMB = v & 1; check base in [block_start, block_end)`):

| 块 | GBA 范围 | 大小 | ref 计数 | 分类 |
|----|---------|------|---------|------|
| Block1 | [0x0801f4d0, 0x0801fb60) | 0x690 | **95** | disasm R4 |
| Block2 | [0x0801fb90, 0x0801fe92) | 0x302 | **104** | disasm R4 |
| Block3 | [0x080202fe, 0x08020334) | 0x36 | **19** | disasm R4 |
| Block4 | [0x08020370, 0x08020db4) | 0xa44 | **110** | disasm R4 |

与 proposal 数字一致 (95/104/19/110). **全部 4 块有实质引用, §5.1 条件不满足, disasm R4 分类正确.**

Block3 关键引用核对:
- ROM[0xe2f40] = 0x08020301, bit0=1 -> THUMB+1 fn-ptr (gMenuState 上下文: ROM[0xe2f3c]=0x02029590=gMenuState)
- ROM[0x13e280] = 0x08020301, bit0=1 -> 另一 THUMB+1 ref
- ROM[0x17dbac] = 0x08020303, bit0=1 / ROM[0x474eec] = 0x08020309, bit0=1 -> 内部子地址 THUMB refs
- 首字节: ROM[0x202fe]=0x00,0x00 (pad); ROM[0x20300]=0xf0,0xb5 -> halfword=0xb5f0 = push {r4,r5,r6,r7,lr} = 合法 THUMB function prologue

**byte-identical 安全性**: disasm 仅改 Ghidra listing, 不改 ROM 字节. GAS 重汇编 THUMB 指令回原字节, 与 file 00 Seg-5c-ii/Seg-9 Block B 先例一致. **R4 对全部 4 块 byte-identical 安全.**

---

## 2 个求助裁定

### 求助 1: Block3 函数名 (tick_campaign_scene_step vs tick_lp_record_scene_step)

**裁定: tick_lp_record_scene_step, 置信度 med.**

理由:
- Block4 (0x08020370..0x08020db4) 的 14-case step handler 集中包含 `render_lp_record_text_set_a` — 直接证明该场景处理 LP 记录显示.
- Block3 @ 0x08020300 是 block4 的 14-case 调度器 (读 gPrng+0x202 bits[13:6], 与 block4 step table PTR_DAT_08020338 对应).
- 所以 block3 函数是 "lp_record 场景的 step machine 入口", 名字 `tick_lp_record_scene_step` 准确.
- "tick_campaign_scene_step" 无静态证据 — 不应使用.
- 提案将此标为 BLOCKED 是偏保守. static evidence (block4 step content) 足以支撑 med-conf 命名, 无需 BLOCKED.
- **建议**: fixer 在 disasm plan 中将函数命名为 `tick_lp_record_scene_step` (med-conf), 并在 Ghidra createFunction 时应用此名.

### 求助 2: DAT_08020018=0xffffc03f 新常量 PRNG_STEP_IDX_CLEAR

**裁定: 保持 RENAME-only (raw 值), 不新建全局常量.**

理由:
- 0xffffc03f 在现有全部 constants/*.inc 中不存在 (独立 grep 确认).
- NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff 是不同值 (清不同 bit 段), 不可复用.
- 0xffffc03f 在本段出现 3 次 (DAT_08020018 / DAT_08020268 / DAT_080202a8), 均属 run_duel_puzzle_scene_state_machine 内部使用, 无跨函数共享证据.
- 新建全局常量需要跨多处引用 / 语义稳定才值得. 3 次局部使用 RENAME-only (带 EOL 注释 "clear bits[13:6] step index field") 已足够.
- **建议**: fixer 照提案执行 RENAME-only, 在 EOL 注释中标注 `0xffffc03f: clear bits[13:6] of halfword at gPrng+0x202`.

---

## EQ 值核对 (C4, 样本)

以下 30 个 EQ 槽经 python `struct.unpack_from("<I", rom, off)` 逐一核对 (全 OK):

| ROM 偏移 | 槽名 | 值 | 常量 |
|---------|-----|-----|------|
| 0x1f27c | DAT_0801f27c | 0xfffe0000 | GAME_STR_RAW_ID_MASK |
| 0x1f3ac | DWORD_0801f3ac | 0x04000128 | SIOCNT |
| 0x1f3c8 | PTR_gPrng_0801f3c8 | 0x03000040 | gPrng |
| 0x1f3cc | DAT_0801f3cc | 0x00000584 | raw offset |
| 0x1fff4 | DAT_0801fff4 | 0x0000023f | GPRNG_BANNER_FLAG_OFF |
| 0x1fff8 | DAT_0801fff8 | 0x02023130 | gDuelFieldState |
| 0x1fffc | DAT_0801fffc | 0xfffc03ff | GL_CLEAR_BITS_17_10 |
| 0x20010 | DAT_08020010 | 0xfffffc03 | GL_CLEAR_BITS_9_2 |
| 0x20018 | DAT_08020018 | 0xffffc03f | (RENAME raw) |
| 0x20138 | DAT_08020138 | 0x02000000 | EWRAM_BASE |
| 0x20148 | DAT_08020148 | 0x00006c2c | GSETTINGS_OFFSET |
| 0x2013c | DAT_0802013c | 0x00006c3c | EWRAM+gDuelPuzzleProgress off |
| 0x202cc | DAT_080202cc | 0x02023360 | gDuelSceneBase |
| 0x20f50 | DWORD_08020f50 | 0x02000000 | EWRAM_BASE |
| 0x20f54 | DWORD_08020f54 | 0x00006c2c | GSETTINGS_OFFSET |

全 30 槽 ROM 字节与 proposal 值一致.

---

## 其他发现 (非阻塞)

**Block3 描述性错误 (不影响 disasm)**: Proposal 描述中写 "sub sp,#0x28" 但 ROM bytes 0xb0a2 解码为 sub sp,#0x88 (imm7=0x22=34, 34×4=136=0x88). 这仅是 proposal 说明文字的笔误, 实际 disasm 将按 ROM 字节解码正确指令. **fixer 无需修正 proposal, 直接 disasm 即可.**

**注意: 提案 §5.1=空, 无 §5.1 登记.** 这是正确的 — 全部 4 块均有大量引用.

---

## 状态: PASS

所有 C1-C13 检查通过. 2 个求助已给出裁定.

- C9 现有 CJK plate 是"已知待修复目标", fixer 需在执行时替换为 proposal 提供的 ASCII 版本.
- Block3 函数名: tick_lp_record_scene_step (med-conf), fixer 在 disasm plan 中应用.
- 0xffffc03f: RENAME-only, 不新建全局常量.
- Block3 描述性 "sub sp,#0x28" 错误非阻塞 (disasm 按字节).

fixer 可以进入模式 B (落地) 执行.
