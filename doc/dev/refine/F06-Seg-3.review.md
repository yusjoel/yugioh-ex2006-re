# Refine Review: F06-Seg-3

> Reviewer: independent (refine-reviewer agent)
> Date: 2026-06-14
> Proposal: doc/dev/refine/F06-Seg-3.proposal.md
> Segment: ROM 0x08054ba0..0x08055440 (~22 fn), asm/06_equip_eligibility_b.s

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致, 未跳号/回头 | OK | 路线图: Seg-3 = 0x54ba0..0x55440; 前段 Seg-2 commit 6c90482 已完成; proposal 范围完全一致 |
| C2 | 每个 ROM_INCBIN/.byte 块都有归宿 | OK | 唯一块 0x55188/0x34 -> R4 disasm (check_zone_slot_occupied_with_clear_equip_flag); 有 2 THUMB+1 引用, 非 §5.1 |
| C3 | §5.1 块确 0 引用 | N/A | 本段无 §5.1 登记; ROM_INCBIN 块有引用故 R4 disasm, 不进 §5.1 |
| C4 | EQ value == ROM 4 字节小端 | OK | 全 42 EQ 槽 + 1 REF 槽 + 2 disasm 内部 pool 槽 (45 total) 均 python struct.unpack_from 核对 OK |
| C5 | 新建 constants 前确无现有可复用 | OK | 0 new constants; 全部 3 unique 值 (0x868/0x0201c510/0x0201bb90) 均已在 ewram.inc 存在 |
| C6 | 槽名 ^[a-z][a-z0-9_]+$, 无碰撞 | OK | 45 个标签全合法; 无重复; 无与 asm/06 现有 313 标签碰撞 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | REF slot gEquipChainSlotRefs=0x0201bb90 -> .equ 已在 ewram.inc; .word gEquipChainSlotRefs 可正确解析 |
| C8 | plate 引用全用现名, 无残留旧 FUN_/DAT_/DWORD_ | OK | Seg-3 asm 行范围 (L3014..L4389) grep FUN_[0-9a-f]{8} = 0 stale 命中; proposal 也无 stale FUN_ |
| C9 | ASCII-only plate/EOL | OK | Ghidra plate text (225 字节) 经 python 字符扫描 = 0 非 ASCII; proposal .md 文件本身含中文 (正常 doc 用途) |
| C10 | 指针表条目 +1 (.word <fn>+1 == ROM raw 值) | N/A | 无 carve; ROM_INCBIN 是 disasm 入函数体, 不产生 .word <fn>+1 行 |
| C11 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | OK | 新函数 check_zone_slot_occupied_with_clear_equip_flag: 语义 = zone slot has card AND equip flag clear; 函数名准确; 无误名信号 |
| C12 | 关键槽语义有 file:line + 置信度证据 | OK | R6 gEquipChainSlotRefs: file asm/06_equip_eligibility_b.s L3054-3121 (confirmed 有效); disasm fn: roms/2343.gba @ 0x09e4365c + 0x09e43b84; 均 high confidence; 无零容忍词 |
| C13 | 段内所有残留自动名槽被覆盖 (无遗漏) | OK | ASM Seg-3 范围内 DWORD_/DAT_ 定义精确 43 个; proposal EQ=42 + REF=1 = 43; 完全覆盖 |

---

## 独立复核细节

### ref-scan (C2/C3 关键)

自主重跑 python word-aligned 全 ROM 扫描:

- `raw 0x08055188`: **0 命中**
- `THUMB+1 0x08055189`: **2 命中**
  - ROM offset 0x1e4365c (addr 0x09e4365c): 前置 CID=0x0000130f, fn_ptr1=0x0806a549, pad=0x00000000 -- dispatch table 结构验证 OK
  - ROM offset 0x1e43b84 (addr 0x09e43b84): 前置 CID=0x000014b4 (Byser Shock, card-stats.s L13015 确认), fn_ptr1=0x0806abd5, pad=0x00000000 -- dispatch table 结构验证 OK

结论: proposal 的 ref-scan 数据完全正确; R4 disasm 判定成立 (非 §5.1).

### THUMB 解码核验

块 0x08055188..0x080551bc (52B) 字节 dump 对照 proposal 逐条验证:

- `lsls r0,r0,#19` @ 0x0805519e: 0x04c0, imm5=19, Rm=r0, Rd=r0 -- 正确
- `beq` @ 0x080551a2: 0xd009, target = 0x080551a6 + 9*2 = 0x080551b8 (LAB_080551b8 fail) -- 正确
- `bne` @ 0x080551a8: 0xd106, target = 0x080551ac + 6*2 = 0x080551b8 (LAB_080551b8 fail) -- 正确
- `b` @ 0x080551ac: 0xe005, target = 0x080551b0 + 5*2 = 0x080551ba (LAB_080551ba = bx lr) -- 正确
- `bx lr` @ 0x080551ba: 0x4770 -- 正确
- ldr r1,[pc,#28] @ 0x08055192 (0x4907): PC_aligned=0x08055194, target=0x080551b0, value=0x00000868 -- 正确
- ldr r1,[pc,#24] @ 0x08055198 (0x4906): PC_aligned=0x0805519c, target=0x080551b4, value=0x0201c510 -- 正确

### EQ/REF 字节核对 (C4)

45 个槽地址全部 OK (见上方核验矩阵 C4).

### C13 精确计数

- Ghidra autoname 定义 (DWORD_/DAT_) in Seg-3 行范围: **43** (独立 grep 计数)
- Proposal EQ=42 + REF=1 = **43**
- 完全一致; 无越界吃 Seg-4 槽

### 小问题: 描述性文本轻微错误 (不影响落地)

Proposal doc ref-scan 详情节描述: "0x130d/0x130e 空缺" -- 实际 0x130d = Germ Infection (已分配), 只有 0x130e 和 0x130f 才是空缺. 此错误仅在 proposal .md 描述性文字中, **未出现在 Ghidra plate text** (plate 只说 "CID 0x130f (unassigned)" 这是正确的). 不影响落地正确性; 无需修改.

---

## 状态: PASS

所有 C1-C13 检查通过. 无 NEEDS_FIX 项.

### 落地前提醒 (fixer 注意)

1. Disasm 步骤 6 的两个 pool 槽 (0x080551b0 = PLAYER_BLOCK_STRIDE, 0x080551b4 = gDuelFieldSlots) 在 Ghidra disasm 后需要显式 equate; 这是在已 disasm 的函数体内部, proposal 已在 disasm 计划第 6 步列出, fixer 确保执行.
2. Seg-3 共 43 Ghidra 自动名槽; 落地后 grep DWORD_/DAT_ 段内范围应为 0 (全部替换).
3. CSV sync 新增 1 行 (0x08055188, check_zone_slot_occupied_with_clear_equip_flag).
4. CID 0x130f = 双空缺之一 (0x130e 和 0x130f 均空), 0x130d = Germ Infection (非空缺); 该事实只需知晓, 不影响 plate text 或落地.
