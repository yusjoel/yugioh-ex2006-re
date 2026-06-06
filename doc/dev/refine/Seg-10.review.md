# Refine Review: Seg-10

段范围: `[0x0801b850, 0x0801cb00)` — 文件 `asm/00_system_str_vija.s` 最后一段，vija/shuen 场景 tick，32 fn。

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | refine-progress.md 列 Seg-10 = 0x1b850..0x1cb00; proposal 32 fn 全部 < 0x0801cb00; 最后槽 DAT_0801cafc=0x0801cafc < 0x0801cb00 |
| C2 Rule2 | 段内无 ROM_INCBIN/.byte | ✅ | awk 扫描第 17984 行至文件末 (20387 行) 确认 0 匹配 |
| C3 Rule3 | §5.1 无块 → 跳过 | ✅ | 无 §5.1 登记 |
| C4 R1 值 | 新建 7 个 EQ 槽 ROM 字节核 | ✅ | 全部 OK，见下表 |
| C5 R1 复用 | **SCENE_STEP_IDX_CLEAR_MASK 与现有同值** | **❌** | 0xffc03fff 已存在为 `NAME_INPUT_PAGE_STATE_CLEAR` (name_input.inc 第 28 行)；功能相同 (均清 gPrng+0x204 bits[21:14])；应复用现有常量，不新建 |
| C6 R2 名 | 70 个新 slot_label 格式和碰撞 | ✅ | 全部匹配 `^[a-z][a-z0-9_]+$`；文件内无重名 |
| C7 R3 接通 | REF_SLOTS 有 USER-label + DATA-ref | ✅ | gVijaState 新全局; trig_table 已 carve in rom.s |
| C8 R5 现名 | 板注释 FUN_ 残留 → 全部计划替换 | ✅ | 23 处 FUN_ 均在 PLATE-1 CJK 重写 / PLATE-2 / PLATE-3 / 14 个 in-place 修复覆盖范围内 |
| C9 ASCII | 提案新 plate/EOL 文本纯 ASCII | ✅ | PLATE-1/3 新文本经 grep 验证无非 ASCII；现有 19 行 CJK 全在 demo_shuen_state_machine 体内，PLATE-1 重写覆盖 |
| C10 carve | 无 carve → 跳过 | ✅ | 段内无 ROM_INCBIN |
| C11 误名 | 32 fn 名称核查 | ✅ | 抽查: demo_shuen_state_machine(体含 shuen 7-state logic), write_shuen_bg3_scroll_regs(体写 BG3HOFS/VOFS), tick_vija_obj_anim_slot(体循环 vija OBJ 槽) — 名与体一致，FUNC_RENAME=0 成立 |
| C12 R6 | gVijaState 关键槽证据 | ✅ | raw=61 (自跑 ref-scan); THUMB|1=0; 4 file:line 证据; confidence=high |
| C13 残留 | **9 个自动名槽未列入 proposal** | **❌** | 79 总计 auto-named - 70 proposal 处理 = 9 遗漏 (见下) |

## 自主复核结果

### C4 EQ 字节核 (7 新建 + 关键复用)

| 槽地址 | 提案值 | ROM 字节 | 结论 |
|--------|--------|---------|------|
| 0x0801c2a0 | 0xffc03fff | `ff 3f c0 ff` ✓ | OK |
| 0x0801c2fc | 0x05000030 | `30 00 00 05` ✓ | OK |
| 0x0801c300 | 0x00001741 | `41 17 00 00` ✓ | OK |
| 0x0801c304 | 0x00001d81 | `81 1d 00 00` ✓ | OK |
| 0x0801c308 | 0x00001e82 | `82 1e 00 00` ✓ | OK |
| 0x0801c30c | 0x00001f8b | `8b 1f 00 00` ✓ | OK |
| 0x0801c480 | 0xfffe3fff | `ff 3f fe ff` ✓ | OK |

复用 EQ 抽查: DEMO_CLEAR_BITS_13_7(0x0801b918)=0xffffc07f ✓; DEMO_KEEP_BITS_8_0(0x0801ba6c)=0x000001ff ✓; ROM_REGION_CODE_ADDR(0x0801c538)=0x080000ae ✓; GSETTINGS_OFFSET(0x0801c540)=0x00006c2c ✓。

### C12 gVijaState ref-scan

```
0x02029eb0 raw ROM count = 61  (自跑 python struct.pack)
0x02029eb1 THUMB|1 count = 0
```

Seg-10 内 gVijaState 出现 10 次 (全部 `< 0x0801cb00`，与 REF_SLOTS 10 条完全吻合)。gDemoState(0x02029ec0) raw=19 THUMB|1=0 — 独立全局; Seg-10 内有 6 处 gDemoState 引用 (shuen 函数)。

注: gVijaState(0x02029eb0) 和 gDemoState(0x02029ec0) 相距 0x10 字节，reset_gl_display_state 的 bios_cpu_set 从 0x02029eb0 清 0xc0 字节，逻辑正确 (两 demo 场景不并发，同一 EWRAM 块分时复用)。

### BG3HOFS 地址订正核

ROM 0x0801ba70 = `1c 00 00 04` = 0x0400001c = BG3HOFS (gba_io.inc line 25)。
现有 PLATE-2 写 `BG3HOFS (0x04000018)` — 实际为 BG2HOFS，错误确认。
现有 PLATE-3 写 `BG3HOFS (0x04000016)` 和 `BG3VOFS (0x04000018)` — 分别对应 BG1VOFS 和 BG2HOFS，均错误。
提案修正后值 BG3HOFS=0x0400001c / BG3VOFS=0x0400001e 正确。

### 边界核 (C1)

proposal 所有 56 个槽地址最大值 = 0x0801cafc < 0x0801cb00。无越界。

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C5 — SCENE_STEP_IDX_CLEAR_MASK 应复用 NAME_INPUT_PAGE_STATE_CLEAR

**问题**: proposal 在 `constants/demo_state.inc` 新建 `.equ SCENE_STEP_IDX_CLEAR_MASK, 0xffc03fff`，但该值已存在于 `constants/name_input.inc` 第 28 行:
```
.equ NAME_INPUT_PAGE_STATE_CLEAR, 0xffc03fff  @ bits[21:14] clear mask for page_state field @ gPrng+0x204
```
语义完全一致 (均清 gPrng+0x204 bits[21:14] 的 step index 字段)。

**修改**: 不新建 `SCENE_STEP_IDX_CLEAR_MASK`；改为复用 `NAME_INPUT_PAGE_STATE_CLEAR`。

具体改动:
- **demo_state.inc**: 删除新建行 `.equ SCENE_STEP_IDX_CLEAR_MASK, 0xffc03fff`
- **slot 0x0801c2a0 处**: slot_label = `tick_scene_step_by_step_table_a_step_idx_clear_mask`，const_name 改为 `NAME_INPUT_PAGE_STATE_CLEAR`
- includes.inc 中 `name_input.inc` 已被包含 (确认无需重复 include)

**影响**: EQ 新建从 7 个减为 6 个。

---

### #2 — C13 — 9 个自动名槽未列入 proposal RENAME 节

**问题**: 段内实际 auto-named label 定义共 79 个 (64 DAT_ + 8 DWORD_ + 7 PTR_)，proposal 处理 70 个 (33 EQ + 12 REF + 18 RENAME + 7 PTR_fix = 70)。以下 9 个 label 已有语义 `.word` 值但 label 名仍为自动名，未列入 RENAME 节:

| label | 地址 | 当前值 | 应改为 |
|-------|------|--------|--------|
| DAT_0801b910 | 0x0801b910 | .word gDemoState | load_demo_shuen_sprite_gfx_demo_state |
| DAT_0801ba44 | 0x0801ba44 | .word gDemoState | load_shuen_obj_resource_by_slot_demo_state |
| DAT_0801bac8 | 0x0801bac8 | .word gDemoState | tick_demo_shuen_bg3_hscroll_demo_state |
| DAT_0801bb20 | 0x0801bb20 | .word gDemoState | tick_shuen_bg3_vscroll_phase_demo_state |
| DAT_0801bb94 | 0x0801bb94 | .word gDemoState | advance_shuen_cell_anim_frame_demo_state |
| DAT_0801bd30 | 0x0801bd30 | .word gDemoState | demo_shuen_state_machine_demo_state |
| DWORD_0801c29c | 0x0801c29c | .word gPrng | tick_scene_step_by_step_table_a_prng |
| DWORD_0801c558 | 0x0801c558 | .word BG3HOFS | apply_bg3_scroll_masked_bg3hofs |
| DWORD_0801c55c | 0x0801c55c | .word BG3VOFS | apply_bg3_scroll_masked_bg3vofs |

**注**: 这些槽的 `.word` 值已是语义符号 (不是裸 hex)，fixer 只需改 label 名，不改 `.word` 行。

**修改**: 将以上 9 条加入 proposal 的 RENAME_SLOTS 节 (纯 label 改名类)。

---

## 附注

- gVijaState=0x02029eb0 独立性: ewram.inc 已有 gDemoState=0x02029ec0，两者相距 0x10B，均为 demo 场景 EWRAM 区，提案正确区分。
- trig_table=0x09e399d0 复用 rom.s 现有 carve label，ref-scan raw=7 全为代码字面池引用，无误。
- VIJA_CPUSET_FILL_CTRL=0x05000030: bit26=fill, bit24=32bit, count=0x30 words = 0xc0 bytes，逻辑核实正确。
- PLATE-3 FUN_0801c560/0801c59c 已列入 14 个 FUN_ in-place 修复 (apply_bg3_scroll_masked 板注释)，核实无漏。
