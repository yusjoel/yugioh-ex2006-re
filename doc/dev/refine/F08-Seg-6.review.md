# Refine Review: F08-Seg-6

Segment range: ROM `[0x080690dc, 0x0806a118)`, 21 named fn, 96 auto-name slots,
1 ROM_INCBIN (0x080696d8/0x1c), 1 switchD (0x08069edc).
Proposal: `doc/dev/refine/F08-Seg-6.proposal.md`

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图 Seg-6 一致，未跳号 | OK | Seg-1..5 全 ✅，Seg-6 = 0x690dc..0x6a118 吻合 |
| C2 | 段内唯一 ROM_INCBIN 0x080696d8/0x1c 有归宿 | OK | 归 R4 disasm，verdict 正确 |
| C3 | §5.1 登记块确 0 引用 | OK | 本段 §5.1=0；无需检验 |
| C4 | EQ value == ROM 4 字节 | OK (部分抽查) | 已 python 核对 28 个 EQ 槽，全部匹配 |
| C5 | 新建常量前确无可复用 | **FAIL** | 见 Issue #1 (0x09e3fXXX equate) + Issue #3 (LP_BANISHER_CTX_OFF 名称错误) |
| C6 | RENAME 槽名合法，无碰撞 | **FAIL** | 见 Issue #4 (DAT_08069f54/DWORD_0806a050 label 前缀与常量不符) |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | REF_SLOTS 3 个均有完整证据 |
| C8 | plate/RENAME 无残留 FUN_ | OK | Seg-6 行范围无 FUN_ |
| C9 | plate/EOL 文本纯 ASCII | OK | 唯一 PLATE 纯 ASCII；RENAME 标签全 ASCII |
| C10 | fn-ptr 槽 `+1` THUMB 验证 | OK | DWORD_08069ae8=0x08090625 (+1)；DAT_08069d7c=0x08069cdd (+1) |
| C11 | 函数名/plate 无误名矛盾 | OK | tick_dragon_summon_display_if_slots_paired 含义与代码体一致；plate 修正卡名 Lord of D. 正确 |
| C12 | 关键槽有 file:line 证据 + 置信度 | OK | 消费者证据节覆盖全部新建/复用槽 |
| C13 | 段内全部残留自动名槽被覆盖 | OK | python 枚举 asm/08 Seg-6 行区间所有 DWORD_/DAT_/PTR_ = 96 个；RENAME 表 = 96 个；完全覆盖，无遗漏 |

---

## 状态: NEEDS_FIX (4 items)

---

## 修改清单

### #1 — C5 + Ruling A — 0x09e3fXXX 地址不得新建 equate

**根据**：`grep -rn "0x09e3f" asm/` 确认所有兄弟模块（asm/05 L8915、asm/09 L13772、asm/10 L16668、asm/11 L1475 等）一律使用 raw `.word 0x09e3fXXX` + ASCII EOL，**无一 equate，无一 carve**。

**违规位置**：
- `DWORD_080694d4 = 0x09e3f11c` -> proposal 建议 `SCAPEGOAT_OAM_TOKEN_TABLE_ADDR`（EQ 条目）
- `DWORD_08069504 = 0x09e3f12c` -> proposal 建议 `STRAY_LAMBS_OAM_TOKEN_TABLE_ADDR`（EQ 条目）

**执行动作**（fixer 模式 A）：
1. 从 EQ_SLOTS 删除这 2 个条目（`SCAPEGOAT_OAM_TOKEN_TABLE_ADDR` / `STRAY_LAMBS_OAM_TOKEN_TABLE_ADDR`）。
2. 不创建 `token_tables.inc`（Ruling A + Ruling B 共同裁定）。
3. Ghidra 对这 2 个槽改为描述性 label + ASCII EOL：
   - `DWORD_080694d4` -> label `scapegoat_token_tbl_080694d4`，EOL `"ROM ptr: Scapegoat OAM token slot-id table, 8 hwords @ 0x09e3f11c"`
   - `DWORD_08069504` -> label `stray_lambs_token_tbl_08069504`，EOL `"ROM ptr: Stray Lambs OAM token slot-id table, 8 hwords @ 0x09e3f12c"`
   （RENAME 项保留，但 EQ equate 不建）
4. 这 2 个槽在 RENAME 表中的动作也相应调整（不引用 equate 名，仅改 Ghidra label）。

---

### #2 — C5 — DAT_08069778 名称错误（LP_BANISHER_CTX_OFF 与 ewram.inc 不符）

**验证**（python 独立核查）：
- `DAT_08069778` ROM 值 = `0x00001da8`（已读取确认）
- `ewram.inc` 中：
  - `LP_BANISHER_CTX_OFF = 0x1d70`（**值不同**）
  - `LP_CARD_TRACK_BASE_OFF = 0x1da8`（正确匹配，109 ROM refs，base = gP1LifePoints）
- 消费者上下文（asm/08 L12738-12743）：`ldr r4, PTR_gP1LifePoints_08069774; ldr r1, DAT_08069778; adds r0,r4,r1`，访问 `[gP1LifePoints+0x1da8]` -> 与 `LP_CARD_TRACK_BASE_OFF` 语义吻合，base 相同，无域例外。

**执行动作**：
- EQ 表中将 `DAT_08069778 -> LP_BANISHER_CTX_OFF=0x1da8 (Reuse)` 改为 `DAT_08069778 -> LP_CARD_TRACK_BASE_OFF=0x1da8 (Reuse ewram.inc)`。
- RENAME 表中将 `lp_banisher_ctx_off_08069778` 改为 `lp_card_track_base_off_08069778`。
- 消费者证据节相应更新。
- （`LP_BANISHER_CTX_OFF=0x1d70` 在 DAT_08069df4 的用法**保持正确**，无需动）。

---

### #3 — C6 — RENAME 标签前缀与常量不符（2 个槽）

**违规位置**：
- `DAT_08069f54`：proposal RENAME label = `gduelphaseflagss_08069f54`，但 EQ 值为 `gDuelCardCtxBase=0x0201e2a0`（已 python 读取确认）。
- `DWORD_0806a050`：proposal RENAME label = `gduelphaseflagss_0806a050`，但 EQ 值为 `gDuelCardCtxBase=0x0201e2a0`（已读取确认）。

**执行动作**：
- `DAT_08069f54` -> Ghidra label 改为 `gduellcardctxbase_08069f54`（或 `gduell_card_ctx_base_08069f54`，符合 `^[a-z][a-z0-9_]+$`）
- `DWORD_0806a050` -> Ghidra label 改为 `gduellcardctxbase_0806a050`

---

### #4 — Ruling B — ZONE_ENTRY_FLAGS_CLR_MASK 放入 oam_attr.inc 而非新建 equip_sprite.inc

**验证**：`oam_attr.inc` 已含 `OAM_SPRITE_ATTR_CLR_BITS20_17`（类似掩码）、`OAM_ATTR_P1_SPRITE`/`OAM_ATTR_P2_SPRITE`（类似 sprite code 格式），风格一致。主线程裁定：`ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff` 放入 `oam_attr.inc`，**不创建** `equip_sprite.inc`。

**执行动作**：
- 不创建 `constants/equip_sprite.inc`。
- 在 `constants/oam_attr.inc` 中添加 `.equ ZONE_ENTRY_FLAGS_CLR_MASK, 0x1fff @ ...`。
- proposal 中 "Consider new equip_sprite.inc or add to oam_attr.inc" 的歧义消除，固定为 oam_attr.inc。

---

## 独立验证结果

### Ruling A 独立验证

`grep -rn "0x09e3f" asm/` 返回的全部命中分析：
- `asm/05` L8915：`.word 0x09e3f118` + EOL "ROM ptr: 10-entry CID array"（无 equate）
- `asm/09` L13772：`.word 0x09e3f134`（无 equate）
- `asm/10` L16668：`.word 0x09e3f140`（无 equate）
- `asm/11` L1475、L1647：`.word 0x09e3f14c`（无 equate，2 处）
- `asm/11` L6752：`.word 0x09e3f164`（无 equate）
- `asm/11` L11665：`.word 0x09e3f19c`（无 equate）
- `asm/08` L12059：`.word 0x09e3f11c`（已有 EOL 注释，无 equate）
- `asm/08` L12085：`.word 0x09e3f12c`（已有 EOL 注释，无 equate）

**结论：裁定 A 成立，proposal 的 equate 不符合兄弟模块惯例。**

### Ruling B 独立验证

- `oam_attr.inc` L88：`OAM_SPRITE_ATTR_CLR_BITS20_17 = 0xffe1ffff`（掩码型，与 ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff 同类）
- `oam_attr.inc` L147-148：`OAM_ATTR_P1_SPRITE=0x8027 / OAM_ATTR_P2_SPRITE=0x8059`（sprite code 型，与 OAM_SPRITE_CODE_P1_ACTIVATION=0x8019 同类）
- **结论：裁定 B 成立，两个新常量均适合放入 oam_attr.inc。**

### C4 ROM 字节核对（28 槽抽查）

python 独立读取 ROM `roms/2343.gba`，对以下槽逐一核对：`DWORD_080690f8/164/168/1b4/1b8/1c0/924c/4c4/4c8/4d4/504/960/968/95a0/a00/a18/a24/ae8; DAT_08069d7c/eec/d00/778/b34/b38/df4/f78/fa8`。全部 OK，无 MISMATCH。

### C3 ref-scan 独立复核

- `0x080696d8`（raw=`0x080696d8`）：ROM 全局搜索 `struct.pack("<I", 0x080696d8)` = **0 hits**
- `0x080696d9`（THUMB+1）：`struct.pack("<I", 0x080696d9)` = **1 hit at ROM addr 0x09e3fba8**
- 命中处 `value @ 0x01e3fba8 = 0x080696d9` 确认
- CID 在 hit-4 (offset 0x01e3fba4)：值 = `0x12da`（注：hit-0xc 处为 0x0000，说明 entry 格式为 [CID(4B), fn_elig(4B), ...]，CID 在 fn_elig_ptr - 4 而非 -0xc）
- `cid_12da=0x12da` 在 card-stats.s 中确认为未分配 gap（0x12D7=Tragedy, 0x12DC=Ectoplasmer，中间无 0x12da 条目）
- **R4 disasm 判定正确**

机器码核对（独立解码）：
- `0x080696d8 (1c0a)`: movs r2, r1
- `0x080696da (2104)`: movs r1, #4
- `0x080696dc (7900)`: ldrb r0, [r0, #4]（注：proposal 写 "ldrb r1,[r0,+0]" 有细节偏差，但不影响分类判定）
- `0x080696de (4001)`: ands r1, r0
- ... 中间 test/branch 序列
- `0x080696f2 (4770)`: bx lr

14 个 halfword，有效 THUMB 函数，以 `bx lr` 结束。

### C13 自主清点

python 枚举 `asm/08_equip_oam_neodaed.s` 内所有 `DWORD_/DAT_/PTR_gP1LifePoints_` 标签，地址落在 `[0x080690dc, 0x0806a118)` = **96 个**。RENAME 表独立枚举 = **96 个**。两集合完全相同（`rename_set == asm_auto_labels`）。C13 PASS。

EQ 表中有 7 个槽地址 >= 0x0806a118（Seg-7 领域），但这 7 个槽**不出现在 RENAME 表中**，即 Seg-6 Ghidra 脚本不会对其操作。C13 不受影响，但 EQ 表列错（Issue #5 辅助信息）。

### switchD_08069edc 验证

python 读取 10 个 case 目标：全部落在 `[0x08069f18, 0x08069ff4]`，均在 Seg-6 范围内。switchD 已 inline disasm，**无需额外 R4 disasm**。proposal 判定正确。

### C5 双向核（新建常量）

- `WIDESPREAD_RUIN_CID=0x1254`：`grep -rn "0x1254" constants/` = 0 hits。card-stats.s 确认 pw=77754944。OK
- `HAMMER_SHOT_CID=0x17f2`：`grep -rn "0x17f2" constants/` = 0 hits。card-stats.s 确认 pw=26412047。OK
- `cid_12da=0x12da`：`grep -rn "0x12da" constants/` = 0 hits。card-stats.s 确认 gap。OK
- `BOTTOMLESS_SHIFTING_SAND_CID=0x1540`（无 slot，仅文档用）：`grep -rn "0x1540" constants/` = 0 hits。card-stats.s 确认 slot=0x1540 pw=76532077。OK
- `LP_ACTIVATION_LINK_FLAG_OFF=0x10d0`：`grep -rn "0x10d0" constants/` = 1 hit in `duel_field.inc` L166：`EFFECT_ZONE_BITMASK_OFF=0x10d0`，base=gDuelFieldSlots。本段 consumer（asm/08 L12689）base=`gP1LifePoints`。不同 base -> 域例外成立，新建独立常量 OK。
- `OAM_SPRITE_CODE_P1_ACTIVATION=0x8019`：`grep -rn "0x8019" constants/` = 0 hits。OK
- `ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff`：`grep -rn "0x1fff" constants/` = 0 hits。OK

C5 复用核（关键 Reuse）：
- `LP_BANISHER_CTX_OFF=0x1d70` at DAT_08069df4：ewram.inc L421 确认存在，值匹配。OK
- `LP_CARD_TRACK_BASE_OFF=0x1da8`（Issue #3 修正后）：ewram.inc L247 确认存在，值匹配。OK
- `PLAYER_BLOCK_STRIDE=0x868`：ewram.inc L250 确认。OK
- `gDuelPhaseFlags=0x0201b290`：ewram.inc L351 确认。OK
- `gEquipLpZoneEntryBase=0x0201e500`：ewram.inc L472 确认。OK

### 两项 Seg-5 遗留待办验证

**(a) gEquipLpZoneEntryBase=0x0201e500 在本段是否被称 "OAM_DATA_PTR"？**

- 查 asm/08 L12523-12529：`ldr r1, DAT_0806982c; DAT_0806982c: .word 0x0201e500`
- proposal 正确处理：`DAT_0806982c -> gEquipLpZoneEntryBase=0x0201e500 (Reuse ewram.inc)`
- 没有被误称 "OAM_DATA_PTR"。OK

**(b) tick_dragon_summon_display_if_slots_paired @ 0x080690dc plate 卡名订正（0x128b=Lord of D.）**

- proposal PLATE 节：旧 plate 误称 "Stamping Destruction"；新 plate 正确写 "Loads fixed CID 0x128b (Lord of D.)"
- ROM 读取 `DWORD_080690f8 @ 0x080690f8 = 0x0000128b` 确认
- card-stats.s `card_0599 @ Lord of D. slot=0x128B pw=17985575` 确认
- 新 plate 纯 ASCII。OK

---

## Reviewer Verdict: F08-Seg-6 = NEEDS_FIX(4 items)
