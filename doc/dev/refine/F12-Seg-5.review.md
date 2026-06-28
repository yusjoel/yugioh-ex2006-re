# Refine Review: F12-Seg-5

Segment [0x08097828, 0x080984d0), file `asm/12_equip_activation_scan.s`.
5 named functions (装备发动相位机), 0 ROM_INCBIN blocks.
Reviewer ran all checks independently.

---

## 独立复核结果

### 独立 ROM_INCBIN / .byte 扫描

Python scan of ASM lines 7435..9119 (0-indexed 7434..9118):
- ROM_INCBIN count: 0
- `.byte` code blocks: 0
- `.zero` alignment pads: present (legitimate)

Proposal 声明 "0 ROM_INCBIN / 0 .byte": 独立确认正确。

### 独立 C13 槽清点 (独立 python scan)

```
DAT_  slots:               118
DWORD_ slots:                0
PTR_gP1LifePoints_ slots:   31
PTR_switchdataD_ slots:       2
Other PTR_:                   0
Total auto-name:            151
```

Proposal 声称 118 DAT_ + 31 PTR_gP1LP + 2 PTR_switchD = 151。与独立清点完全一致。

**C13 覆盖分析:**

独立从 ROM 按值归组后，0x1d2c (EQUIP_CHAIN_ACTIVE_OFF) 实际命中 **43 个** DAT_ 槽，而 proposal Group A 列表只有 42 个：

缺失槽：`DAT_080979bc` (值 0x1d2c，ROM bytes @ 0x080979bc = `0x00001d2c` 独立核验)。

该槽位于 ASM L7635，属于 `switchD_08097850__caseD_2` 的 fail-path 代码：
```
DAT_080979bc:
    .word  0x00001d2c    @ 080979bc 2c1d0000
```
应归入 Group A (EQUIP_CHAIN_ACTIVE_OFF)，槽名 `eqchain_act_79bc`。

结论：EQ+REF+RENAME 并集 = 117 DAT_ + 4 REF_DAT_ + 31 PTR_LP = 152，但实际总量 151；C13 有 1 个 DAT_ 槽未覆盖 → **C13 FAIL**。

### 独立 C4 ROM 字节核对

独立 python 读 ROM 核对 64 槽，含全部 NEW 首现槽、REF 槽、全部 EQ 组代表槽：

所有 64 项 PASS (0 failures)：
- Group A (0x1d2c): 5 抽查槽全 OK
- Group B (0x1d28): 3 抽查槽全 OK
- Group C (0x1d30): 2 抽查槽全 OK
- Group D (0x0201bb90): 5 抽查槽全 OK
- Group E (0x0201afe0): 2 OK
- Group F (0x0201e2a0): 6 OK
- Group G (0x1d54): 3 OK
- Group H (0x1d5c): 4 OK
- Group I (0x1d58): 2 OK
- Group J (0x1d6c @ DAT_08098148): OK
- Group K (0x1d68 @ DAT_08098458): OK
- Group L (0x1da8): 2 OK
- Group M (0x1daa): OK
- Group N (0x868): 2 OK
- Group O NEW (0x8015): OK
- Group P NEW (0x139c): 3 OK; NEW (0x1115): OK
- REF THUMB fn ptr: DAT_080980ec=0x08097bed OK, DAT_08098104=0x08097bed OK,
  DAT_080983fc=0x0809822d OK, DAT_08098414=0x0809822d OK
- PTR_switchdataD_: 0x08097860=0x08097864 OK, 0x08097c68=0x08097c6c OK

### 独立 C5 按 VALUE grep

3 个 NEW 常量逐一按值 grep constants/*.inc:

| const_name | value | grep 结果 | 裁定 |
|---|---|---|---|
| OAM_EQUIP_SPRITE_P2_15 | 0x00008015 | 0 命中 | NEW OK |
| JIRAI_GUMO_CID | 0x00001115 | 0 命中 | NEW OK |
| PATRICIAN_OF_DARKNESS_CID | 0x0000139c | 0 命中 | NEW OK |

card-stats.s 核实：
- card_0325 "Jirai Gumo" slot=0x1115 pw=94773007 → JIRAI_GUMO_CID 坐实
- card_0813 "Patrician of Darkness" slot=0x139C pw=19153634 → PATRICIAN_OF_DARKNESS_CID 坐实

### 独立 C8 stale FUN_ 扫描

独立扫描 ASM L7435..9119:

| 行号 | FUN_ | 所在函数 | 真实名 | proposal 处理 |
|---|---|---|---|---|
| L7967 | FUN_0809be70 | dispatch_equip_slot_display_state_by_phase 板 | advance_equip_display_phase_via_table (asm/12 L16737) | PLATE 表 full rewrite 覆盖 |
| L8783 | FUN_0809be70 | tick_activation_display_state_machine 板 | advance_equip_display_phase_via_table | PLATE 表 full rewrite 覆盖 |
| L9118 | FUN_0809be70 | activate_effect_zone_display_for_slot 板 | advance_equip_display_phase_via_table | 属于 Seg-6 首函数 (0x080984d0)，超出 Seg-5 范围 |

Seg-5 范围内 2 处 FUN_0809be70 均被 PLATE 表覆盖。L9118 不在 Seg-5 作用域。**C8: PASS**。

### 独立 C9 ASCII 核对

独立扫描 ASM L7435..9119 非 ASCII 行: **0 行**。当前 asm 内容已全 ASCII。

新 PLATE 文本核对 (proposal 提供的 5 条):
- dispatch_equip_activation_state_by_substate: 469 chars, ASCII OK
- check_equip_target_slot_eligibility: 401 chars, ASCII OK
- dispatch_equip_slot_display_state_by_phase: 412 chars, ASCII OK
- check_slot_equippable_excluding_self: 402 chars, ASCII OK
- tick_activation_display_state_machine: 455 chars, ASCII OK

全部 <=500 字符且纯 ASCII。

### 独立 C6 槽名格式检查

扫描 proposal 中全部 151 个槽名 (`^[a-z][a-z0-9_]+$`):

**发现 2 个不合规名称：**
- `switchdataD_97860`: 含大写 'D' — 违反 `^[a-z][a-z0-9_]+$`
- `switchdataD_97c68`: 含大写 'D' — 违反命名规则

其余 149 个标签格式全部合规，无重复碰撞。

### 独立 REF 槽核验 (C7/C10)

**REF-1 (PTR_switchdataD_):**
- PTR_switchdataD_08097864_08097860 @ 0x08097860: 值 0x08097864 = switch data table 起始，目标在 asm 已有 label `switchD_08097850__switchdataD_08097864`。计划 createLabel + DATA-ref。合理。
- PTR_switchdataD_08097c6c_08097c68 @ 0x08097c68: 值 0x08097c6c = switch data table 起始，目标在 asm 已有 label `switchD_08097c58__switchdataD_08097c6c`。合理。

**REF-2 (THUMB fn ptr):**
- DAT_080980ec = 0x08097bed = check_equip_target_slot_eligibility (0x08097bec) | 1，ROM 独立核验 OK。
  0x08097bec 处 THUMB prologue bytes = 0xb530 (push {r4,r5,lr}) 确认。
- DAT_08098104 = 0x08097bed，同上。
- DAT_080983fc = 0x0809822d = check_slot_equippable_excluding_self (0x0809822c) | 1，ROM 独立核验 OK。
  0x0809822c 处 THUMB prologue bytes = 0xb570 (push {r4,r5,r6,lr}) 确认。
- DAT_08098414 = 0x0809822d，同上。

4 个 THUMB ptr 槽全部正确，均为已命名函数的 THUMB 指针 (addr|1)。C7/C10: PASS。

### C11 函数名核验 (误名检查)

5 个函数体 vs 函数名独立抽查：

- `dispatch_equip_activation_state_by_substate`: 体内读 [gP1LifePoints+0x1d2c] → 5-way dispatch。名符实。
- `check_equip_target_slot_eligibility`: 体内读 gEquipChainSlotRefs[0] (active_player)，检查 combined_slot<=4，调用 eval_slot_activation_eligibility_full。名符实。
- `dispatch_equip_slot_display_state_by_phase`: 体内读 [gP1LifePoints+0x1d2c] → 12-case switch。名符实。
- `check_slot_equippable_excluding_self`: 体内检查 slot<=4，调用 check_slot_card_can_be_equipped，guard 同 player 同 slot。名符实。
- `tick_activation_display_state_machine`: 体内读 [gP1LifePoints+0x1d2c]，多级 cmp 树 (0/0x64/0x65/0x66/0xc8/0xc9)。名符实。

注: 板注释中 "gDuelBattleState"/"gDuelTurnStruct" 是旧名，板改写已订正为 gEquipChainSlotRefs。函数名本身无误。FUNC_RENAME: 0。C11: PASS。

### C12 R6 证据核验

Consumer Evidence 节共 13 条，逐一有 asm/12 file:line + conf:high；无零容忍词。
C12: PASS。

### C3 §5.1 块引用核验

Seg-5 无 §5.1 登记条目 (0 ROM_INCBIN 块)。C3: N/A。

### OPEN QUESTION 裁定

**OQ-1: gEquipChainSlotRefs vs "gDuelBattleState"**
裁定: HIGH-CONF。ewram.inc 中 gEquipChainSlotRefs = 0x0201bb90 是权威名称。旧板中的 gDuelBattleState/gDuelTurnStruct 均为 stale 旧名。Plate 改写已全部替换为 gEquipChainSlotRefs。Fixer 落地验收须确认新板无 gDuelBattleState 残留。

**OQ-2: inline 偏移字段不需建常量**
裁定: HIGH-CONF。[+0x4]/[+0x8]/[+0xc]/[+0x18]/[+0x1c]/[+0x20] 均以 STR/LDR 指令 immediate offset 形式出现，未 pool 为 DAT_ 槽，不在 C13 作用域内，fixer 不需为其建常量。

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致，未跳号/回头 | PASS | §五 Seg-5: [0x08097828, 0x080984d0); proposal 精确匹配；Seg-4 已完成 (commit aa2ff4e)，Seg-6 未开始 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 独立确认 Seg-5 含 0 ROM_INCBIN/code-.byte；无分类决策需求 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | Seg-5 无 §5.1 登记条目 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立核对 64 槽含全部 NEW 首现槽，全部 0 失败 |
| C5 R1 复用 | 新建前确无现有可复用 | PASS | 3 个 NEW 常量 (0x8015/0x1115/0x139c) 逐一按值 grep constants/ 返回 0 命中；card-stats.s 核实 CID 值 |
| C6 R2 名 | 槽名格式 `^[a-z][a-z0-9_]+$`，无碰撞 | **FAIL** | REF-1 槽名 `switchdataD_97860` / `switchdataD_97c68` 含大写 'D'，违反命名规则；其余 149 个合规 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 6 个 REF 槽均有 createLabel + DATA-ref 计划 (2 switchdataD_ ptr + 4 THUMB fn-ptr)；目标在 asm 已有 label |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | PASS | Seg-5 范围 L7967/L8783 两处 FUN_0809be70 均被 PLATE full rewrite 覆盖；L9118 属 Seg-6 范围外 |
| C9 ASCII | plate/EOL 文本纯 ASCII，且 <=500 字符 | PASS | 当前 asm Seg-5 范围 0 非 ASCII 行；5 条新板文本 469/401/412/402/455 字符，纯 ASCII |
| C10 carve | 指针表条目 +1 (THUMB) 核对 | PASS | 4 个 THUMB fn-ptr 槽独立 ROM 核验；目标函数 THUMB prologue 字节确认 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 5 函数名均与体内操作一致；FUNC_RENAME 0 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据，无零容忍词 | PASS | 13 条消费者证据均有 asm/12 file:line + conf:high；全文无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖，无遗漏 | **FAIL** | `DAT_080979bc` (0x1d2c = EQUIP_CHAIN_ACTIVE_OFF) 缺失于 EQ 表；ROM 值独立核验 = 0x1d2c；proposal Group A 列 42 槽，实际有 43 槽 |

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单 (NEEDS_FIX，逐条可执行)

### Fix #1 — C13 — DAT_080979bc 缺失于 EQ 表

**位置**: proposal §EQ_SLOTS > Group A

**问题**: 独立 ROM 扫描发现 `DAT_080979bc` 值 = 0x1d2c (EQUIP_CHAIN_ACTIVE_OFF)，未出现在 Group A 列表中。Group A 实际有 43 个槽而非 42 个。

**ROM 核验**: ROM @ 0x080979bc = `0x00001d2c` (独立读取确认)。

**位置上下文**: ASM L7635:
```
DAT_080979bc:
    .word  0x00001d2c    @ 080979bc 2c1d0000
```
出现在 `switchD_08097850__caseD_2` fail-path，与相邻 Group B/C 槽 (DAT_080979b8=0x1d28, DAT_080979c0=0x1d30) 并排。

**修改**: 在 EQ_SLOTS Group A 表中新增一行：

```
| DAT_080979bc | eqchain_act_79bc |
```

Group A 计数从 42 改为 43，EQ 总计从 114 改为 115，C13 计数从 114+4+31=151 改为 115+4+31=152 — 注意总计 151 不变，只是 EQ 表 DAT_ 数从 114 增为 115。

**Ghidra 操作**: equate DAT_080979bc = EQUIP_CHAIN_ACTIVE_OFF + createLabel("eqchain_act_79bc", 0x080979bc)。

---

### Fix #2 — C6 — REF-1 槽名含大写 D

**位置**: proposal §REF_SLOTS > REF-1 (PTR_switchdataD_ slots)

**问题**: 建议槽名 `switchdataD_97860` 和 `switchdataD_97c68` 含大写字母 'D'，违反命名规则 `^[a-z][a-z0-9_]+$`。

**修改**: 将两个槽名中的大写 'D' 改为小写 'd'：

| slot addr | 原 slot_label | 修正 slot_label |
|---|---|---|
| 0x08097860 | `switchdataD_97860` | `switchdata_d97860` 或 `switchdata_ptr_97860` |
| 0x08097c68 | `switchdataD_97c68` | `switchdata_d97c68` 或 `switchdata_ptr_97c68` |

推荐: `switchdata_ptr_97860` / `switchdata_ptr_97c68` (避免 'd' 开头分隔符歧义)，符合 `^[a-z][a-z0-9_]+$`。

---

## Reviewer Verdict: F12-Seg-5 = NEEDS_FIX(2 items)
