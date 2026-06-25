# Refine Review: F11-Seg-4b

Segment: `[0x08088904, 0x0808962c)` -- 0xD28 = 3368 bytes  
Proposal: `doc/dev/refine/F11-Seg-4b.proposal.md`  
Source: `asm/11_effect_slot_puzzletext.s` line 7658 (`ROM_INCBIN 0x88904, 0x4ef0`)  
Review date: 2026-06-25

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | roadmap §五 明确 Seg-4b = `[0x08088904, 0x0808962c)` -- 完全匹配 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 段内无 sub-block; 全 25 fn 均已 disasm 计划; 0 静默保留 |
| C3 | §5.1 块确 0 引用 | PASS | 自己重跑 ref-scan: 0x08088EF6 弱条目唯一引用来自压缩数据区 0x08CF7042 (>0x082d4000) -- 巧合字节值, 非真实调用; 25 个 fn-start 均只从 dispatch table 被引用 |
| C4 | EQ value == ROM 4 字节小端 | FAIL | fn26 header 写 `size=0x0cc (204 B)`, 实际 `0x0808962c-0x08089558=0xD4=212 B`; 其余 40 个 pool slot 值全部与 ROM 4 字节小端一致 (python 全量核对) |
| C5 | 新建 constants 前确无现有可复用 | PASS | 自行逐一 value-grep 16 个声称 NEW 的 CID: 全部 0 命中 (真 NEW); 19 个 REUSE CID 按值 grep 全部 PRESENT |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 25 个函数名全合规, 无重复 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS (minor) | REF=40 计划完整: 所有 EWRAM 地址池 DWord 均有 createDWordWithRef + ptr_* 标签; 但 2 处 section header 行数字文本有误: gP1HandSlotArray 标 "3 slots" 实列 4 行; gP1FieldArrayCBase 标 "2 slots" 实列 3 行 (脚注计数正确) |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | proposal 全文无 `FUN_[0-9a-f]{8}` |
| C9 | ASCII 检查 | PASS | plate/EOL 文本全 ASCII; 唯一非 ASCII 为 proposal markdown 标题行 `## §5.1 Entries` 中 U+00A7 (section sign), 不进入 Ghidra |
| C10 | 指针表条目 +1 (THUMB) | PASS | dispatch table 全量扫描 305 条: 25 个 fn 的 fn_ptr+1 引用完全匹配; fn21 CID pool words (0x080892cc/0x080892dc) 与 ROM 一致; 0x080892d4 确认为 CODE (`4801 4680`) 非 pool |
| C11 | 函数体全局 vs 函数名矛盾 | PASS | python 反汇编核验 7 个 fn 的 MOVS R1, #substate: fn01(0xe), fn04(0xb+0xd), fn07(0xd), fn08(0xe), fn20(0xd), fn21(0xc), fn26(0xd) 全与名称后缀吻合; 无误名信号 |
| C12 R6 | 关键槽语义有 file:line 置信度证据 | PASS | write_equip_zone_entry_by_substate asm/11 L7758 确认; dispatch_equip_zone_write_by_substate_range asm/11 L7669 确认; 全部 BL target 有现名; consumer section 完整 |
| C13 | 段内残留 DAT_ 全覆盖 | PASS | 25 fn spans 连续无间隙: sum=0xD28=segment size; post-disasm gate (grep ROM_INCBIN\|\.byte ==0) 在 disasm plan 中已指定 |

---

## 自查关键数据

```
=== 独立 ref-scan (THUMB+1) 结果 ===
弱条目 0x08088EF6: 唯一引用 0x08CF7042 (压缩数据区), 值=0x08088EF7; 该地址 ROM bytes=0x2816 (cmp r0,#22) -- 非 push prologue
退化强条目 0x0808939C: 唯一 non-table ref = 0x08B573A4 (压缩数据区, >0x082d4000), 值=0x0808939D
退化强条目 0x08089560: 唯一 non-table ref = 0x08735E94 (压缩数据区), 值=0x08089561
以上 3 个条目的非 table 引用全来自压缩数据区 -- 巧合字节, 非运行时调用路径

25 个 fn-start 首字节:
  0x08088904=0xB5F0, 0x0808896c=0xB5F0, 0x080889c4=0xB5F0, 0x08088a34=0xB5??, 0x08088ad4=0xB5?? ...
  全部为 0xB4xx/0xB5xx (push prologue) -- 25/25 OK

dispatch table 全量扫描 (305 entries, 0x09e5a128):
  25 fns 的 CID 集合与 proposal 完全匹配 (fn08 × 13 CIDs, fn22 × 4 CIDs 等全部一致)

pool DWord ROM 核对 (40 slots python 全量):
  40 OK, 0 FAIL
  fn01 0x08088964=0x0201C4E0 (gP1LifePoints) ✓
  fn12 0x08088f68=0x0201B290 (gDuelPhaseFlags) ✓ [两条 ldr 均解析同一 slot]
  fn18 0x080891f4=0x00000868 (PLAYER_BLOCK_STRIDE) ✓
  fn21 0x080892cc=0x00001507 (SUPER_ROBOLADY) ✓; 0x080892dc=0x00001508 ✓
  fn26 0x08089628=0x0201C4F0 (gP1SlotCountBase) ✓

fn26 大小核算:
  0x0808962c - 0x08089558 = 0xD4 = 212 bytes (实际)
  proposal header 写 "size=0x0cc (204 B)" -- 少 8 字节 (对应 0x08089624/0x08089628 两个 pool words)
  但 pool list 中已正确列出 0x08089628 (gP1SlotCountBase), 覆盖完整

substate 核验 (BL 0x0808d88c 前的 MOVS R1):
  fn01→0xe, fn04→0xb+0xd, fn07→0xd, fn08→0xe, fn20→0xd, fn21→0xc, fn26→0xd -- 全匹配

C5 value-grep (16 NEW CIDs 全部 0 hits):
  0x1480 KYCOO_THE_GHOST_DESTROYER, 0x1474 FOOLISH_BURIAL, 0x18E0 INFERNAL_FLAME_EMPEROR,
  0x1484 SPIRIT_OF_FLAMES, 0x1487 GARUDA_THE_WIND_SPIRIT, 0x15BC LEKUNGA,
  0x16C0 FREED_THE_BRAVE_WANDERER, 0x16C7 GIGANTES, 0x148B SUPPLY, 0x1490 SKULL_LAIR,
  0x14D0 REINFORCEMENT_OF_THE_ARMY, 0x14EF DES_FERAL_IMP, 0x14F7 SILENT_FIEND,
  0x1507 SUPER_ROBOLADY, 0x1508 SUPER_ROBOYAROU, 0x152F PYRAMID_TURTLE
  -- 全部在 card-stats.s 中有对应 slot=0x<CID> 行 ✓

gP1HandSlotArray 4 slots 全核: 0x08088DB4/0x08088F78/0x080891C4/0x08089280 = 0x0201C8F8 全 OK
gP1FieldArrayCBase 3 slots 全核: 0x08088C8C/0x08088FDC/0x08089110 = 0x0201C600 全 OK
ewram.inc 8 个全局值全部吻合 (gP1LifePoints/gP1SlotSetCodeArray 等)
```

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单 (fixer 逐条执行)

### #1 -- C4 -- fn26 size 文本错误

**问题**: fn26 header 第一行写 `size=0x0cc (204 B)`, 实际 fn26 span = `0x08089558..0x0808962c` = `0xD4 = 212 bytes`. 差异来自 proposal 未将最后两个 pool words (0x08089624 和 0x08089628) 计入 size -- 但这两个词已正确列入 pool list, 故覆盖完整, 仅描述文字错误.

**修正**: `### fn26: 0x08089558  size=0x0cc (204 B)` --> `### fn26: 0x08089558  size=0x0d4 (212 B)`

---

### #2 -- C7 editorial -- REF section header 计数文字有误

**问题**: 两处 section header 行描述的 slot 数量与实际表格行数不符 (不影响落地正确性, 但 reviewer 需要可信赖的文档):

- `### gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 3 slots` -- 实际列出 4 行 (fn08/fn12/fn18/fn19); footer 已正确写 `REF count gP1HandSlotArray: **4**`
- `### gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 2 slots` -- 实际列出 3 行 (fn06/fn13/fn16); footer 已正确写 `REF count gP1FieldArrayCBase: **3**`

**修正**:
- `-- 3 slots` --> `-- 4 slots` (gP1HandSlotArray section header)
- `-- 2 slots` --> `-- 3 slots` (gP1FieldArrayCBase section header)

---

## 不阻塞项 (信息性)

**I1**: 弱条目 0x08088EF6 的唯一引用来自压缩数据区 (0x08CF7042), 值 0x08088EF7. 这是压缩内容中的巧合字节序列; 对应地址在 fn11 mid-loop body (0x2816=cmp r0,#22), 排除是真实 fn_ptr. 已在提案中正确分类为 EXCLUDE.

**I2**: 退化强条目 0x0808939C 和 0x08089560 的 non-table 引用均来自压缩数据区 (分别 0x08B573A4 和 0x08735E94), 均 >0x082d4000. 0x0808939C 的 ROM bytes = 0x4690 0x46A1 (mov r8,r2; mov r9,r4) -- 不是 push prologue; 0x08089560 = 0xB4E0 (push {r5,r6,r7}) -- 是 fn26 双 push 序列的第二 push. 两者在 dispatch table 均无对应条目, 正确排除.

**I3**: fn13 无 gP1LifePoints pool (只有 PLAYER_BLOCK_STRIDE + gP1FieldArrayCBase), 与 LDR 扫描一致; 对应 REF table 中 fn13 未出现在 gP1LifePoints section -- 正确.

**I4**: fn21 的 0x080892d4 确认为 CODE bytes (0x46804801 = `ldr r0,[pc,#4]; mov r8,r0`), 不是 pool word -- 与提案 note 一致.

**I5**: 25 个函数名中不含 CJK, 不含零容忍词, 所有 plate 文本 <=500 chars (最长 fn08 = 489 chars).

---

## 状态: NEEDS_FIX(2 items)

#1 和 #2 均为 proposal 文字修正 (Mode A), 不需要 Ghidra 落地; 修正后可直接进入 fixer 落地阶段.
