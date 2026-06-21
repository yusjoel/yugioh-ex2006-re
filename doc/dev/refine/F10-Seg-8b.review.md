# Refine Review: F10-Seg-8b

**Segment**: [0x08082b18, 0x08083450)
**Proposal**: `doc/dev/refine/F10-Seg-8b.proposal.md`
**Reviewer**: independent (no proposal conclusions trusted without re-verification)

---

## 核验结果 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | Seg-8b 在 Seg-8a (commit 3909787) 之后, 地址序连续 [0x82b18, 0x83450), 路线图 §五 一致 |
| C2 Rule2 | ✅ | 段内 0 ROM_INCBIN (python grep 确认), 无需处理 |
| C3 Rule3 | ✅ | 无 §5.1 块 (同上) |
| C4 R1 值 | ✅ | python 独立读 ROM 4 字节小端: 全 61 个可核对槽全部与 proposal 值一致 (见下表) |
| C5 R1 复用 | ✅ | REUSE 槽逐值 grep constants/*.inc 均有命中; NEW 槽逐值 grep card_info.inc 均 0 命中 |
| C6 R2 名 | ✅ | 所有新 CID 名符合 `^[A-Z][A-Z0-9_]+_CID$` 约定; 无碰撞; neutral cid_<hex> 格式正确 |
| C7 R3 接通 | ✅ | 无 §5.1 REF 块, 不适用 |
| C8 R5 现名 | ✅ | asm/10 L19057..20682 grep `FUN_[0-9a-f]{8}` = 0 命中; 跨 asm/*.s grep Seg-8b 函数旧名 = 0 命中 |
| C9 ASCII | ❌ | 见 NEEDS_FIX #1: 6 条 CJK mojibake 行存在且 proposal 板 3 的 ASCII 重写包含语义错误 |
| C10 carve | ✅ | 无指针表 carve (无 ROM_INCBIN) |
| C11 误名 | ✅ | 12 个函数名与函数体操作一致, 无明显误名信号 |
| C12 R6 | ❌ | 见 NEEDS_FIX #2: plate 3 和 plate 4 的 STATE_OFFSET 声明与 ARM 机器码矛盾 |
| C13 残留 | ✅ | python 独立计: 67 个唯一标签定义在 [0x82b18, 0x83450) = 3 PTR_(skip) + 4 gP1LP(RENAME) + 4 fn-ptr(RENAME) + 56 EQ = 全覆盖 |

---

## 独立复核证据

### C4 ROM 字节核对 (python `struct.unpack_from('<I', data, addr-0x08000000)`)

批次 1 (25 槽):

| addr | 预期 | 实测 | 结果 |
|------|------|------|------|
| 0x08082ba8 | 0x0000140a | 0x0000140a | OK |
| 0x08082bb4 | 0x00001719 | 0x00001719 | OK |
| 0x08082bbc | 0x08082b19 | 0x08082b19 | OK |
| 0x08082bc4 | 0x08082b2d | 0x08082b2d | OK |
| 0x08082be4 | 0x08082b5d | 0x08082b5d | OK |
| 0x08082be8 | 0x0201b290 | 0x0201b290 | OK |
| 0x08082c30 | 0x00000484 | 0x00000484 | OK |
| 0x08082c5c | 0x0201c4e0 | 0x0201c4e0 | OK (gP1LifePoints=0x0201c4e0, RENAME) |
| 0x08082c60 | 0x00001d68 | 0x00001d68 | OK |
| 0x08082c78 | 0x00000484 | 0x00000484 | OK |
| 0x08082cf8 | 0x0000ffff | 0x0000ffff | OK |
| 0x08082d2c | 0x0201b290 | 0x0201b290 | OK |
| 0x08082d60 | 0x080905e9 | 0x080905e9 | OK |
| 0x08082dbc | 0x08082c8d | 0x08082c8d | OK |
| 0x08082dc0 | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x08082e20 | 0x00000868 | 0x00000868 | OK |
| 0x08082e24 | 0x0201c510 | 0x0201c510 | OK |
| 0x08082e60 | 0x00001d68 | 0x00001d68 | OK |
| 0x08082e64 | 0x00001d6c | 0x00001d6c | OK |
| 0x08082e68 | 0x0201b290 | 0x0201b290 | OK |
| 0x08082e80 | 0x0201b290 | 0x0201b290 | OK |
| 0x08082eb4 | 0x0201b290 | 0x0201b290 | OK |
| 0x08082ee0 | 0xfffc7fff | 0xfffc7fff | OK |
| 0x08082f08 | 0x00001da8 | 0x00001da8 | OK |
| 0x08082f30 | 0x00001357 | 0x00001357 | OK |

批次 2 (36 槽, 含 CID):

| addr | 预期 | 实测 | 结果 |
|------|------|------|------|
| 0x08082f38 | 0x00001da8 | 0x00001da8 | OK |
| 0x08082f7c | 0x000016d6 | 0x000016d6 | OK |
| 0x08082f80 | 0x000014e7 | 0x000014e7 | OK |
| 0x08082f84 | 0x00001359 | 0x00001359 | OK |
| 0x08082f90 | 0x0000149e | 0x0000149e | OK |
| 0x08082fa8 | 0x00001630 | 0x00001630 | OK |
| 0x08082fb4 | 0x000016a8 | 0x000016a8 | OK |
| 0x08082fd0 | 0x000017f7 | 0x000017f7 | OK |
| 0x08082fd8 | 0x000017f1 | 0x000017f1 | OK |
| 0x08082ff0 | 0x0000196f | 0x0000196f | OK |
| 0x08082ff4 | 0x00001864 | 0x00001864 | OK |
| 0x08083000 | 0x00001974 | 0x00001974 | OK |
| 0x08083010 | 0x0000011d | 0x0000011d | OK |
| 0x08083054 | 0x0000011d | 0x0000011d | OK |
| 0x08083088 | 0x0201b290 | 0x0201b290 | OK |
| 0x080830d0 | 0xfffc7fff | 0xfffc7fff | OK |
| 0x080830f8 | 0x000004b4 | 0x000004b4 | OK |
| 0x0808314c | 0x000004b4 | 0x000004b4 | OK |
| 0x0808319c | 0x0201c4e0 | 0x0201c4e0 | OK (gP1LifePoints=0x0201c4e0) |
| 0x080831a0 | 0x00001ce8 | 0x00001ce8 | OK |
| 0x080831a4 | 0x0201b290 | 0x0201b290 | OK |
| 0x080831a8 | 0x000004b4 | 0x000004b4 | OK |
| 0x080831cc | 0xfffc7fff | 0xfffc7fff | OK |
| 0x0808321c | 0x0201b290 | 0x0201b290 | OK |
| 0x0808325c | 0x00001da8 | 0x00001da8 | OK |
| 0x08083260 | 0x00000868 | 0x00000868 | OK |
| 0x0808329c | 0x0201b290 | 0x0201b290 | OK |
| 0x080832cc | 0xfffc7fff | 0xfffc7fff | OK |
| 0x080832ec | 0x000015de | 0x000015de | OK |
| 0x080832f0 | 0x00001368 | 0x00001368 | OK |
| 0x080832f4 | 0x00001568 | 0x00001568 | OK |
| 0x08083308 | 0x000016d3 | 0x000016d3 | OK |
| 0x08083314 | 0x00001803 | 0x00001803 | OK |
| 0x08083358 | 0x0201b290 | 0x0201b290 | OK |
| 0x080833f0 | 0x00000868 | 0x00000868 | OK |
| 0x080833f4 | 0x0201c8f8 | 0x0201c8f8 | OK |
| 0x080833f8 | 0x09e3f140 | 0x09e3f140 | OK |

### C5 CID 核查 (逐值 grep card_info.inc)

**NEW CID — card_info.inc 0 命中, card-stats.s 坐实:**

| value | proposal name | card-stats.s entry | passcode |
|-------|--------------|-------------------|---------|
| 0x0000140a | SHIFT_CID | card_0885: Shift slot=0x140A | 59560625 |
| 0x00001719 | FIENDS_HAND_MIRROR_CID | card_1489: Fiend's Hand Mirror slot=0x1719 | 58607704 |
| 0x00001359 | BACKUP_SOLDIER_CID | card_0762: Backup Soldier slot=0x1359 | 36280194 |
| 0x0000149e | MIRACLE_DIG_CID | card_0988: Miracle Dig slot=0x149E | 06343408 |
| 0x000014e7 | KELDO_CID | card_1047: Keldo slot=0x14E7 | 80441106 |
| 0x00001630 | HIDDEN_BOOK_OF_SPELL_CID | card_1297: Hidden Book of Spell slot=0x1630 | 21840375 |
| 0x000016d6 | PRIMAL_SEED_CID | card_1431: Primal Seed slot=0x16D6 | 23701465 |
| 0x000017f7 | GRAVEYARD_IN_FOURTH_DIMENSION_CID | card_1668: The Graveyard in the Fourth Dimension slot=0x17F7 | 88089103 |
| 0x00001974 | FORCES_OF_DARKNESS_CID | card_1985: The Forces of Darkness slot=0x1974 | 29826127 |

全部 NEW CID: card_info.inc grep = 0 命中确认. card-stats.s 卡名/slot 与 proposal 一致.

**中性 CID — card-stats.s 无 slot 分配:**

| value | proposed | card-stats.s grep | 结论 |
|-------|---------|-------------------|------|
| 0x00001568 | cid_1568 | 无 slot=0x1568 | 确认未分配 |
| 0x000016d3 | cid_16d3 | 无 slot=0x16D3 | 确认未分配 |
| 0x00001803 | cid_1803 | 无 slot=0x1803 | 确认未分配 |

**REUSE CID — card_info.inc 有命中:**

| value | name | card_info.inc line |
|-------|------|--------------------|
| 0x00001357 | DNA_SURGERY_CID | :391 |
| 0x000016a8 | RAY_OF_HOPE_CID | :818 |
| 0x000017f1 | DARK_FACTORY_MASS_PROD_CID | :829 |
| 0x00001864 | BEHEMOTH_KING_CID | :358 |
| 0x0000196f | POT_OF_AVARICE_CID | :839 |
| 0x000015de | equip_cid_15de_08048a68 | :600 |
| 0x00001368 | SPELL_ZONE_TARGET_CARD_ID | :147 |

### C4 gP1LifePoints RENAME 核对

Proposal 的 4 个 "already-symbolic" 槽均存储 0x0201c4e0 (= gP1LifePoints, ewram.inc:79). ROM 实测确认:
- 0x08082c5c = 0x0201c4e0 OK
- 0x08082e5c = 0x0201c4e0 OK
- 0x0808319c = 0x0201c4e0 OK
- 0x08083388 = 0x0201c4e0 OK

### C8 FUN_ 扫描

- asm/10 L19057..20682 范围内 `FUN_[0-9a-f]{8}` = 0 命中 (proposal 正确)
- 跨 asm/*.s grep Seg-8b 12 个函数地址的 `FUN_` 旧名 = 0 命中

### C13 独立计数

python 扫 [0x82b18, 0x83450): 67 个唯一 DAT_/DWORD_/PTR_ 标签定义:
- PTR_gP1LifePoints_ x3: 0x82f04 / 0x82f34 / 0x83150 — SKIP
- DWORD_gP1LP 已符号化 x4: 0x82c5c / 0x82e5c / 0x8319c / 0x83388 — RENAME
- fn-ptr DWORD_ x4: 0x82bbc / 0x82bc4 / 0x82be4 / 0x82dbc — RENAME
- EQ/REF x56 — EQ (REUSE + NEW)
- **并集 = 67 = 全集, 覆盖 100%**

### EQUIP_PAIR_ENTRY_TABLE_BASE 核查

0x09e3f140 原始引用计数 (python `data.count(struct.pack('<I', 0x09e3f140))`): **1 次**, 位于 0x080833f8.

0x09e3f140 落在 FS 虚拟地址空间 (0x09eXXXXX), 不是 ROM flat 地址. 消费者 enqueue_equip_slot_sprites_for_pair_loop 在循环内 ldr r2, DAT_080833f8 加载此值作为配对数据表基址, 循环 r6=0..2 读 [r2+r6*4]. 语义正确 (FS 配对条目表基址), C5 grep constants/*.inc = 0 命中, 确认为 NEW.

---

## 问题清单 (NEEDS_FIX)

### #1 — C9/C12 — plate 3 (tick_equip_display_by_card_id_group_b_3state) 的 STATE_OFFSET 声明错误

**问题**: Proposal 提供的 ASCII 重写 (plate 3) 声明 "STATE_OFFSET=0x4b4 (this function uses 0x4b4 not 0x4b0)". 但 ARM 机器码显示:

```
0x0808306c: ldr r5, DAT_08083088      @ r5 = 0x0201b290 (gDuelPhaseFlags)
0x0808306e: movs r0,#0x96
0x08083070: lsls r0,r0,#0x3           @ r0 = 0x96<<3 = 0x4b0 (state offset)
0x08083072: adds r0,r0,r5             @ r0 = gDuelPhaseFlags+0x4b0
0x08083076: ldr r0,[r0,#0x0]          @ load state from [gDuelPhaseFlags+0x4b0]
0x08083078: cmp r0,#0x1; beq ...     @ state branch uses 0x4b0 NOT 0x4b4
```

0x4b4 是 state 1 清零的 SLOT_PALETTE_OFFSET (DAT_080830f8/0808314c), 不是状态机步进计数器. 当前既存 mojibake plate 本身的 "STATE_OFFSET = 0x4b0" 和 "SLOT_PALETTE_OFFSET = 0x4b4" 注释是正确的, 但额外的 "此函数使用 0x4b4 非 0x4b0" 断言是错误的.

**修正**: ASCII 重写中将 "STATE_OFFSET=0x4b4 (this function uses 0x4b4 not 0x4b0)" 改为 "STATE_OFFSET=0x4b0 (same as fn1). SLOT_PALETTE_OFFSET=0x4b4 (zeroed in state 1, counted in state 2)."

正确的 plate 3 ASCII 重写:
```
Equip display 3-state machine routed by card_id group B. card_id BST dispatches 11 card slots: 0x1359(Backup Soldier), 0x149e(Miracle Dig), 0x14e7(Keldo), 0x1630(Hidden Book of Spell), 0x16a8(Ray of Hope), 0x16d6(Primal Seed), 0x17f1(Dark Factory of Mass Production), 0x17f7(Graveyard in the Fourth Dimension), 0x1864(Behemoth the King of All Animals), 0x196f(Pot of Avarice), 0x1974(The Forces of Darkness). STATE_OFFSET=0x4b0 (same offset as fn1). SLOT_PALETTE_OFFSET=0x4b4 (zeroed in state 1, palette count in state 2).
```

### #2 — C12 — plate 4 (tick_equip_lp_display_by_node_state_4state) 的 STATE_OFFSET 声明错误

**问题**: Proposal plate 4 声明 "STATE_OFFSET=0x4b4 (this function uses 0x4b4 not 0x4b0)". ARM 机器码显示:

```
DWORD_080831a4 = 0x0201b290 (gDuelPhaseFlags)
DWORD_080831a8 = 0x000004b4

ldr r1, DWORD_080831a4    @ r1 = gDuelPhaseFlags
ldr r2, DWORD_080831a8    @ r2 = 0x4b4
adds r3,r1,r2             @ r3 = gDuelPhaseFlags+0x4b4
ldr r0,[r3,#0x0]          @ r0 = [gDuelPhaseFlags+0x4b4] (XOR operand, NOT state)
subs r2,#0x4              @ r2 = 0x4b4 - 4 = 0x4b0 (state offset!)
adds r6,r1,r2             @ r6 = gDuelPhaseFlags+0x4b0
ldr r2,[r6,#0x0]          @ r2 = [gDuelPhaseFlags+0x4b0] (actual state for branching)
cmp r2,#0x1; beq ...
```

XOR 计算使用 [gDuelPhaseFlags+0x4b4], 但状态机分支依据 [gDuelPhaseFlags+0x4b0] (`subs r2,#0x4` 从 0x4b4 减 4 得 0x4b0). STATE_OFFSET 是 0x4b0, 不是 0x4b4. 0x4b4 是 XOR 操作数来源.

**修正**: ASCII 重写中将 "STATE_OFFSET=0x4b4 (this function uses 0x4b4 not 0x4b0)" 改为:
```
STATE_OFFSET=0x4b0 (subs r2,#0x4 from 0x4b4 -> state at gDuelPhaseFlags+0x4b0). XOR_OPERAND_OFF=0x4b4 ([gDuelPhaseFlags+0x4b4] XORd with [gP1LifePoints+0x1ce8] to compute r4).
```

**注**: 既存 mojibake plate L20275 "STATE_OFFSET = 0x4b4 (此函数使用 0x4b4 非 0x4b0)" 是历史误标, 需要同步订正不能直接复制.

---

## 次要备注 (不阻断 PASS 但 fixer 落地时注意)

### B1 — 行号参考与实际定义行不符

Proposal survey 表中列出的 `L19167`/`L19174` 等行号对应的是 `ldr rN, DWORD_...` 引用行, 而不是 `DWORD_xxx:` 标签定义行 (实际在 L19458/L19465 等). Ghidra 脚本按地址操作, 不按行号, 无功能影响. 但 proposal 开头说 "L19057" 为 Seg-8b 起点而实际 invoke_effect_node_handler_if_slot_in_range 函数定义在 L19348 (L19057 仍在 Seg-8a 代码内). 文档错误, 不影响落地.

### B2 — "14 non-ASCII comment lines" 计数错误

Proposal 称 "14 non-ASCII comment lines". 实测 (python grep `[^\x00-\x7F]` L19057..20682): **6 条** (L19431/19580/19949/19954/20271/20275). 6 条全部有对应 ASCII 重写 (plate 1/2/3/4 覆盖全 6 条). 计数错误不影响完整性.

### B3 — enqueue_equip_slot_sprites_for_pair_loop plate 寄存器描述小偏差

Plate 6 ASCII 重写称 "loads ROM pair data base address 0x09e3f140 into r7". 实测: `ldr r7, DAT_080833f4 = gP1HandSlotArray (0x0201c8f8)`, `ldr r2, DAT_080833f8 = 0x09e3f140`. 即 0x09e3f140 加载到 r2 (循环内), 不是 r7. 既存 mojibake plate 有同样错误. 属于 plate 描述小偏差, 不影响 EQ 值正确性.

### B4 — TWO_PRONGED_ATTACK_CID 注记已存在

Proposal New Constants 末尾注记 "TWO_PRONGED_ATTACK_CID should also be added". 该常量已在 Seg-8a 落地时加入 card_info.inc:1609. 不需要再新增.

---

## 状态: NEEDS_FIX (2 items)

NEEDS_FIX #1 和 #2 均属 Plate ASCII 重写的 STATE_OFFSET 语义错误. 两处修正均可执行 (给出了正确 ASCII 文本). 其余 C4/C5/C8/C13 全部通过, CID 无虚构问题.

---

## Reviewer Verdict: F10-Seg-8b = NEEDS_FIX(2 items)
