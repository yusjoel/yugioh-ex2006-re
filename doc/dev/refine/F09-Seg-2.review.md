# Refine Review: F09-Seg-2

Range: `[0x0806ff50, 0x0807104c)` — asm/09_equip_lp_display.s lines 2769..5264

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | 路线图: Seg-2 = 0x6ff50..0x7104c；proposal 头: [0x0806ff50..0x0807104c)；Seg-1 commit 08b3db1 已完成。完全一致。 |
| C2 Rule2 | 所有 ROM_INCBIN 块都有归宿 | OK | 1 块: 0x70476/0x90 → DISASM (R4)，THUMB+1 命中确认。 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | §5.1 = 0 块；唯一 ROM_INCBIN 块有 THUMB+1 确引，不进 §5.1。re-scan 独立复核见下。 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | **FAIL** | DAT_08070754: ROM = 0x00008019，proposal 称 OAM_EQUIP_SPRITE_P2_1A (0x0000801a) ≠ 0x8019。实际应映射到 OAM_SPRITE_CODE_P1_ACTIVATION (0x00008019)。37 个被核对槽中有 1 个错误。 |
| C5 R1 复用 | 新常量 0 hit；REUSE 确存在 | **FAIL** | DAT_08070754 (0x8019) 对应 OAM_SPRITE_CODE_P1_ACTIVATION (已存在 oam_attr.inc)，而非 OAM_EQUIP_SPRITE_P2_1A (0x801a)。10 个 NEW CID 均已逐一 grep 确认 0 命中，其余 REUSE 正确。 |
| C6 R2 名 | 槽名格式合规，无碰撞 | OK | 10 个新 CID 常量名均大写合法；FUNC_RENAME `check_zone_tile_count_and_set_summon_restriction_flag` 符合 ^[a-z][a-z0-9_]+$。 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | REF_SLOTS: PTR_gP1LifePoints_0807061c, PTR_gP1LifePoints_08070668, DAT_08070758 (gEquipChainSlotRefs) 均有 GAS label。carve=0。 |
| C8 R5 现名 | 无残留 `FUN_` | OK | grep "FUN_" asm/09_equip_lp_display.s 在 Seg-2 行范围 2769..5264 内 0 命中。 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | proposal 全文 non-ASCII 字符 = 0。 |
| C10 carve | 指针表条目 `.word fn+1` == ROM raw | OK | 3 RENAME 槽均验证: DWORD_0806ffb0/0806ffec = 0x08051f05 (check_equip_slot_eligible_by_side_and_type_query+1)；DAT_08070a64 = 0x08090625 (invoke_effect_node_with_active_flag_3arg+1)。目标函数 push 指令字节已核。 |
| C11 误名 | 函数名/全局与函数体无矛盾 | OK | FUNC_RENAME 0x08070900: 体内读 gDuelFieldSlots (stride=0x868)、两侧 tile_count、slot[4] bits[14:9]、calls get_card_field_summon_restriction、条件置 slot[4] bits1+2。名称语义吻合。注: proposal 称"4 THUMB+1 refs"，实际 re-scan 仅 1 命中 (0x09e40b50, Royal Command CID=0x148e fn_eligible)；ref 数量有误但不影响 FUNC_RENAME 正确性。 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | OK | 10 个新 CID 槽均给出 consumer fn + asm/09 行号 + conf:high。 |
| C13 残留 | 段内所有自动名槽 100% 覆盖 | **FAIL** | 独立清点 ASM 行 2769..5264: 77 个自动名槽（73 DAT_/DWORD_ + 2 PTR_gP1LifePoints_ + 2 DWORD_08071xxx）。proposal 的 C13 分类表漏列 DWORD_080703b8 (L3413, = 0x0201b290 = gDuelPhaseFlags) + DWORD_08070edc 被双重计入 (既在 gDuelFieldSlots x10 中又在 gP1HandSlotArray x1 中)。两错相消令算术达 77，但 DWORD_080703b8 没有显式出现在任何分类子列表中，实质未覆盖。 |

---

## 独立 ref-scan 复核 (C3)

ROM_INCBIN block GBA 0x08070476..0x08070505 (file 0x70476 size 0x90):

- **raw ref** (0x08070476): **0 命中** — 已核。
- **THUMB+1 穷举** (2B step 遍历全块 entry):
  - `0x08070479` (entry 0x08070478): **1 真命中** @ file 0x1e46658 (GBA 0x09e46658)
    - 上下文验证: 该 offset 处 4 字节 = 0x08070479 ✓
    - 所在区域 GBA 0x09e4xxxx (FS handler dispatch table) ✓
    - 结构解析 (6 words from entry base): [0x08057661, 0x0, 0x00001482, 0x08070479, 0x0, 0x0805efb9]
      - word[0] = fn_activate+1 (0x08057661)
      - word[2] = CID 0x1482 = Bazoo the Soul-Eater (card-stats.s 已坐实 pw=40133511) ✓
      - word[3] = fn_eligible+1 = 0x08070479 ✓
    - **结构为** [fn_activate+1, pad, CID, fn_eligible+1, pad, fn_next] — CID 在 fn_eligible_ptr-4，非 fn_ptr-0xc
  - 其余 6 个 THUMB+1 命中 (0x080704f2/f3..0x080704ff/0x08070503 等): 经逐一上下文验证均为压缩数据误命中 (周边字节序列为典型压缩数据模式 f0f0f1f3..., ff000307...，非对齐指针表)，均为 false positive ✓
- **结论**: 块确有 1 个真实 THUMB+1 引用。DISASM 判定正确，不入 §5.1。

---

## 状态: NEEDS_FIX (3 items)

---

## 修改清单

### #1 — C4/C5 — DAT_08070754 映射到错误常量

**问题**: proposal 将 DAT_08070754 (ROM = 0x00008019) 标为 `OAM_EQUIP_SPRITE_P2_1A`，但 oam_attr.inc 中 `OAM_EQUIP_SPRITE_P2_1A = 0x0000801a`（差 1）。正确的已有常量是 `OAM_SPRITE_CODE_P1_ACTIVATION = 0x00008019`（oam_attr.inc 中已定义）。

**修改**:
- EQ_REUSE 表 DAT_08070754 行: 将 `const_name` 从 `OAM_EQUIP_SPRITE_P2_1A` 改为 `OAM_SPRITE_CODE_P1_ACTIVATION`，inc_file 保持 `oam_attr.inc`。
- C13 breakdown 对应行: 将 `OAM_EQUIP_SPRITE_P2_1A x1: DAT_08070754` 改为 `OAM_SPRITE_CODE_P1_ACTIVATION x1: DAT_08070754`。
- 无需新建 .equ（已有现成常量 OAM_SPRITE_CODE_P1_ACTIVATION = 0x00008019）。

---

### #2 — C13 — DWORD_080703b8 未覆盖

**问题**: ASM L3413 `DWORD_080703b8` (GBA 0x080703b8, ROM value = 0x0201b290 = gDuelPhaseFlags) 存在于 Seg-2 范围内，但 proposal 的 C13 分类表（EQ_REUSE / EQ_NEW / REF / RENAME 四类）均未显式列入该槽。

**修改**:
- 在 EQ_REUSE 的 `gDuelPhaseFlags` 子列表中补充 `DWORD_080703b8`，使该组变为 12 项（原来是 11，但实际 ASM 中共 12 个 gDuelPhaseFlags 槽）。
  - 验证: ROM @ 0x080703b8 file offset 0x703b8 = 0x0201b290 (4 字节小端已核)。
- 更新 C13 gDuelPhaseFlags 数: 11 → 12，同时将 C13 EQ_REUSE 小计和总计相应更新。
- 注意: 原 C13 算术因另一双计 (DWORD_08070edc) 虚增 1、此处少计 1，两误相消令总和仍显 77。修正后正确分布为: gDuelPhaseFlags=12, gDuelFieldSlots=9 (移除 DWORD_08070edc), gP1HandSlotArray=1 (DWORD_08070edc alone)，总和 = 77 仍然正确。

---

### #3 — C13 — DWORD_08070edc 双重计入

**问题**: DWORD_08070edc (ROM = 0x0201c8f8 = gP1HandSlotArray) 在 C13 中被同时列入 `gDuelFieldSlots x10`（明显错误，文字中自注"wait: DWORD_08070edc=gP1HandSlotArray"）和 `gP1HandSlotArray x1`，形成双重计入。

**修改**:
- 将 `gDuelFieldSlots` 子列表从 10 项改为 9 项，移除 DWORD_08070edc（保留其余 9 项）。
- `gP1HandSlotArray x1: DWORD_08070edc = 1`（正确，保留）。
- C13 总计维持 77（与 #2 修正后合并: gDuelPhaseFlags=12, gDuelFieldSlots=9, gP1HandSlotArray=1, 其余不变）。
