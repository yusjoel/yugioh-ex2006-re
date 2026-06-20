# Refine Review: F09-Seg-10b

Reviewer: refine-reviewer (独立复核, 不信 proposal 结论)
Date: 2026-06-21
Proposal: `doc/dev/refine/F09-Seg10b.proposal.md`
Range: [0x79500, 0x79e60)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | Seg-10b = [0x79500..0x79e60), 紧接 Seg-10a (be48d12 ✅ 状态). roadmap 第 14 行标 ⬜, 正确为下一未完成段. 无跳号/回头. |
| C2 Rule2 | ROM_INCBIN x5 全有归宿 | ✅ | B6(R4 disasm) B7(R4 disasm) B8(R4 disasm) B9(R4 disasm) B10(R4 disasm). 无静默保留. §5.1=0. |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 本段无 §5.1 块, 跳过. |
| C4 R1 值 | EQ slot 值 == ROM 4 字节小端 | ✅ | 全 15 个 DWORD_ 槽独立 python 核对, 全部 OK. 详见下方. |
| C5 R1 复用 | 新建常量前确无现有可复用 | ❌ | **PLAYER_STRIDE 误名**: 5 个槽标注 const_name=PLAYER_STRIDE, 但 constants/ewram.inc 中不存在 PLAYER_STRIDE. 实际常量为 PLAYER_BLOCK_STRIDE (ewram.inc:250). 此为 build 必失错误. 其余: INFERNO_TEMPEST_CID=0x17ca grep 0 命中确为 NEW ✅; ORDER_TO_CHARGE/ORDER_TO_SMASH/FAMILIAR_KNIGHT 均 grep 存在 ✅; gEquipZoneCountTable/gDuelFieldSlots/gDuelPhaseFlags/EQUIP_PHASE_FRAME_OFF/CARD_DISPLAY_OP31_LP_BAR_SUB 均 grep 存在 ✅. |
| C6 R2 名 | 槽名合规无碰撞 | ✅ | EQ_PLAYER_STRIDE x5 系同值多用共享 label(可接受, 与 Seg-10a 惯例一致). 其余 slot_label 格式合规, 无碰撞. |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | ✅ | 3 个 scalar .word ptr 槽各有 ptr_to_PTR_DAT_* USER-label 计划. 3 个 PTR_DAT_ + 3 个 DAT_ post-disasm rename 计划. |
| C8 R5 现名 | 无残留 stale FUN_ | ✅ | grep Seg-10b 行(24579..25177): FUN_ = 0 hits. |
| C9 ASCII | plate/EOL 纯 ASCII | ✅ | Seg-10b 行无非 ASCII 字符. 4 个命名函数的 plate 注释内容均为英文. |
| C10 carve | 指针表 .word fn+1 核对 | ✅ | B6/B8/B9 fn_eligible 入口地址经 ROM 读取 THUMB+1 值核对全部匹配 (B6→0x0807965d, B8→0x08079a1d, B9→0x08079bdd). B7/B9-stubs/B10 raw .word 均未含 +1. |
| C11 误名 | 无函数名与函数体矛盾 | ✅ | 4 个命名函数体内容与名称一致. 无 FUNC_RENAME 需求, proposal 正确说明. |
| C12 R6 | 关键槽语义有 file:line + 置信度 | ✅ | 5 个消费者证据项均有 asm/09 行号或 ref-scan 地址引用 + high 置信度标注. 无零容忍词. |
| C13 残留 | 全部残留自动名槽被覆盖 | ✅ | 独立清点 [0x79500..0x79e60): DWORD_ x15 + PTR_DAT_ x3 + DAT_ x3 = 21 自动名槽. 加 3 个 scalar .word ptr 槽共 24 项. proposal 计 24/24 = 100%, 与独立清点一致. |

---

## 独立复核细节

### C4 EQ 槽 ROM 字节核对 (python 自跑)

全 15 槽核对结果:

```
0x08079588 gEquipZoneCountTable = 0x0201e1c8: OK
0x0807958c PLAYER_BLOCK_STRIDE  = 0x00000868: OK
0x08079590 gDuelFieldSlots      = 0x0201c510: OK
0x080795b8 gDuelPhaseFlags      = 0x0201b290: OK
0x08079640 PLAYER_BLOCK_STRIDE  = 0x00000868: OK
0x08079644 gDuelFieldSlots      = 0x0201c510: OK
0x0807985c PLAYER_BLOCK_STRIDE  = 0x00000868: OK
0x08079860 gDuelFieldSlots      = 0x0201c510: OK
0x08079898 gDuelPhaseFlags      = 0x0201b290: OK
0x0807989c EQUIP_PHASE_FRAME_OFF= 0x000004a4: OK
0x08079938 PLAYER_BLOCK_STRIDE  = 0x00000868: OK
0x0807993c gDuelFieldSlots      = 0x0201c510: OK
0x08079940 EQUIP_PHASE_FRAME_OFF= 0x000004a4: OK
0x08079970 gDuelPhaseFlags      = 0x0201b290: OK
0x080799c0 CARD_DISPLAY_OP31... = 0x0000011d: OK
```

值全部正确. 正确常量名为 `PLAYER_BLOCK_STRIDE` (非 `PLAYER_STRIDE`).

### C3 ref-scan 独立重跑

B6 [0x7965c..0x796ac):
- raw=0, THUMB+1=2 at 0x9e42098 / 0x9e42200. 两者均在 0x09e4xxxx. R4 disasm 判定正确.
- CID 读取: fn_ptr_addr - 4 (非文档记载的 -0xc, 但数值正确):
  - 0x9e42094 = 0x0000179f = ORDER_TO_CHARGE_CID (card_info.inc:968 REUSE ✅)
  - 0x9e421fc = 0x000017b8 = ORDER_TO_SMASH_CID (card_info.inc:969 REUSE ✅)
- B6 fn_eligible 实际入口: 0x9e42098 储存 0x0807965d -> addr 0x0807965c ✅ 与 proposal 一致.

B7 [0x796c4..0x797d0):
- 5 entry points: raw=1 各对应 PTR_DAT_080796b0 表内项. 全部在 [0x79500..0x79e60).
- 零覆盖检验: B7 总 0x10c 字节, 5 stubs 地址排序无 gap, 合计 0x10c ✅.

B8 [0x79a1c..0x79a64):
- raw=0, THUMB+1=1 at 0x9e45ef0. 在 0x09e4xxxx. R4 disasm 判定正确.
- CID: 0x9e45eec = 0x000017c3 = FAMILIAR_KNIGHT_CID (card_info.inc:529 REUSE ✅)
- fn_eligible 实际入口: 0x9e45ef0 储存 0x08079a1d -> addr 0x08079a1c ✅.

B9 [0x79adc..0x79c18):
- 6 sub-stub raw refs 全来自 PTR_DAT_08079a68 (29 entry 表). 独立验证 29 个表项的唯一目标集合 = {0x79adc, 0x79af8, 0x79b62, 0x79b80, 0x79bb4, 0x79bd0} = proposal 一致 ✅.
- fn_eligible: THUMB+1=1 at 0x9e42230. CID: 0x9e4222c = 0x000017ca = INFERNO_TEMPEST_CID ✅.
  - card-stats.s 坐实: slot=0x17CA pw=14391920 ✅. grep card_info.inc 0x17ca = 0 hits → NEW ✅.
- fn_eligible 实际入口: 0x9e42230 储存 0x08079bdd -> addr 0x08079bdc ✅ (非 sub-stub, 正确 fn_eligible 起点).
- B9 零覆盖检验: 7 entry points(含 fn_eligible)排序无 gap, 合计 0x13c ✅.

B10 [0x79c9c..0x79e60):
- 9 entry points: PTR_DAT_08079c1c 32 entry 表的唯一目标集合 = {0x79c9c, 0x79cd4, 0x79d24, 0x79d74, 0x79da4, 0x79dc0, 0x79dd8, 0x79df0, 0x79e4e} = proposal 一致 ✅.
- THUMB 疑似引用: 0x9835xxxx 和 0x874axxxx 确非 0x09e4xxxx, 属压缩数据误中; 0x79e02/0x79e1c 均在 stub[7] 内部(0x79df0..0x79e4e), 将被 disasm 覆盖 ✅.
- B10 零覆盖检验: 9 stubs 排序无 gap, 合计 0x1c4 ✅.

### C13 独立清点

[0x79500..0x79e60) 范围内自动名定义:
- `DWORD_*`: 0x79588, 0x7958c, 0x79590, 0x795b8, 0x79640, 0x79644, 0x7985c, 0x79860, 0x79898, 0x7989c, 0x79938, 0x7993c, 0x79940, 0x79970, 0x799c0 = **15 个** (与 proposal 一致)
- `PTR_DAT_*`: 0x796b0, 0x79a68, 0x79c1c = **3 个** (与 proposal 一致)
- `DAT_*`: 0x796c4, 0x79adc, 0x79c9c = **3 个** (与 proposal 一致)
- `UNK_*`: 0 个
- scalar .word ptr 槽: 0x796ac, 0x79a64, 0x79c18 = **3 个** (与 proposal 一致)
- 合计: 24/24 = 100% ✅

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单

### #1 — C5 — PLAYER_STRIDE 应改为 PLAYER_BLOCK_STRIDE (5 处)

**问题**: EQ_SLOTS 表中 5 个 slot 的 `const_name` 列填写了 `PLAYER_STRIDE`, 但该常量不存在. 正确常量为 `PLAYER_BLOCK_STRIDE` (ewram.inc:250, value=0x868). 如 fixer 照搬 proposal 生成脚本, 将导致 GAS assemble 失败 (undefined symbol `PLAYER_STRIDE`).

**修改**: 将 EQ_SLOTS 表中以下 5 行的 `const_name` 列由 `PLAYER_STRIDE` 改为 `PLAYER_BLOCK_STRIDE`:

| slot | 当前错误 | 正确 |
|------|---------|------|
| DWORD_0807958C | PLAYER_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08079640 | PLAYER_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_0807985C | PLAYER_STRIDE | PLAYER_BLOCK_STRIDE |
| DWORD_08079938 | PLAYER_STRIDE | PLAYER_BLOCK_STRIDE |
| (slot_label EQ_PLAYER_STRIDE 可沿用) | — | — |

同时将 `C5 dedup evidence` 节中对应说明更新为 `PLAYER_BLOCK_STRIDE=0x868`.

Fixer 生成 Ghidra 脚本时须使用 `PLAYER_BLOCK_STRIDE` (而非 `PLAYER_STRIDE`), 与 Seg-10a 已落地的 12 个同值 pool 槽惯例一致 (asm/09 中 135 处 `PLAYER_BLOCK_STRIDE` 引用).

---

## 附: 无需修改项

- CID 偏移描述: proposal 说 `CID@(fn_ptr-4)`, 与 ROM 实测一致 (正确). 项目方法论文档写 -0xc 系旧文档误差, 但 proposal 本身用了正确的 -4. 无需 proposal 修改.
- B10 THUMB false-positive 0x9835xxxx/0x874axxxx: 非 0x09e4xxxx, 判定为压缩数据误中正确. 两地址 (0x79e02/0x79e1c) 均在 stub[7] [0x79df0..0x79e4e) 内, disasm 后将被覆盖.
- B9 fn_eligible 地址 0x79bdc: 经 ROM THUMB+1 值直接确认, 非 sub-stub. 正确.
- INFERNO_TEMPEST_CID=0x17ca: NEW 确认, 值正确, passcode 正确, card-stats.s 坐实.
- 无 stale FUN_ (C8 ✅), 无非 ASCII (C9 ✅), 无 plate (C9 N/A).
