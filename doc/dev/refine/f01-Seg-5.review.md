# Refine Review: f01-Seg-5

Segment: `asm/01_vija_scene_text.s` ROM [0x0801e714, 0x0801f25c), 10 fn, card_info tick + puzzle/duel dispatch.
Proposal: `doc/dev/refine/f01-Seg-5.proposal.md`
Reviewer: independent (no proposal conclusions accepted without re-verification)

---

## 自主复核

### Phase 1: ROM 字节核对 (C4)

独立 python 读 ROM `roms/2343.gba` 逐槽核 4 字节小端值。

共核对 28 个 EQ slot 地址（含多处 reuse slot）：

| 地址 | 常量 | 期望 | ROM 值 | 结果 |
|------|------|------|--------|------|
| 0x0801e748 | gDuelFieldState | 0x02023130 | 0x02023130 | OK |
| 0x0801e74c | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | 0x00000222 | 0x00000222 | OK |
| 0x0801e7c8 | card_deck_fs_path_table (REF) | 0x09e58b08 | 0x09e58b08 | OK |
| 0x0801e84c | gCardFsDataBlock | 0x0201e2b4 | 0x0201e2b4 | OK |
| 0x0801e970 | gCardIdCache | 0x0201ff60 | 0x0201ff60 | OK |
| 0x0801e980 | gCardListDisplayBuf | 0x02001138 | 0x02001138 | OK |
| 0x0801e9ec | gDuelFieldState reuse | 0x02023130 | 0x02023130 | OK |
| 0x0801e9f0 | DUEL_FIELD_FADEIN_FLAG_OFF | 0x0000021e | 0x0000021e | OK |
| 0x0801e9f4 | DUEL_FIELD_STATE_226_OFF | 0x00000226 | 0x00000226 | OK |
| 0x0801ea40 | gFontState | 0x0201f440 | 0x0201f440 | OK |
| 0x0801ea44 | gDuelCtx | 0x02020160 | 0x02020160 | OK |
| 0x0801ea48 | DUEL_CTX_ZONE_STATE_OFF | 0x00002f51 | 0x00002f51 | OK |
| 0x0801eb20 | P1LP_BLOCK2_OFF | 0x00001d08 | 0x00001d08 | OK |
| 0x0801eb24 | gDuelSceneBase | 0x02023360 | 0x02023360 | OK |
| 0x0801eb34 | gCardCtxSlotData | 0x0201ff30 | 0x0201ff30 | OK |
| 0x0801eb44 | P1LP_TIMER_OFF | 0x00001cec | 0x00001cec | OK |
| 0x0801eb74 | gDuelFieldState reuse | 0x02023130 | 0x02023130 | OK |
| 0x0801eb7c | gDuelCardCtxBase | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x0801ebbc | GPRNG_PRNG_STATE_OFF213 | 0x00000213 | 0x00000213 | OK |
| 0x0801ec08 | GPRNG_PRNG_STATE_OFF217 | 0x00000217 | 0x00000217 | OK |
| 0x0801eed4 | gZoneActivTable | 0x020230f0 | 0x020230f0 | OK |
| 0x0801eedc | PLAYER_BLOCK_STRIDE | 0x00000868 | 0x00000868 | OK |
| 0x0801eee0 | gP1ZoneHandCount | 0x0201c4ec | 0x0201c4ec | OK |
| 0x0801f0b8 | gUIEffectState (RENAME) | 0x02023110 | 0x02023110 | OK |
| 0x0801f158 | GPRNG_BANNER_FLAG_OFF | 0x0000023f | 0x0000023f | OK |
| 0x0801f1a4 | gBannerState (RENAME) | 0x0201fec0 | 0x0201fec0 | OK |
| 0x0801f258 | GAME_STR_RAW_ID_MASK | 0xfffe0000 | 0xfffe0000 | OK |
| 0x0801f0fc | gFontState reuse | 0x0201f440 | 0x0201f440 | OK |

**全 28 slot ROM 字节核对 OK，无 MISMATCH。**

额外验证 22 个 reuse slots（省略逐行列出）：全部 OK。

### Phase 1: ref-scan 独立重跑 (C3)

段内无 ROM_INCBIN / .byte 块（asm lines 3762-5154 确认）。§5.1 为空，C3 vacuously 满足。

carve 块 ref-scan（自行重跑）：
| 块地址 | raw refs | thumb+1 refs | 判定 |
|--------|----------|-------------|------|
| 0x09e58b08 (card_deck_fs_path_table) | 1 | 0 | REF=1 carve OK (被 lookup_card_entry_by_index 引用) |

### Phase 1: carve 算术核 (C10)

- Host incbin (rom.s line 1611..1612): `card_type_alt_display_table:  @ 0x09e58ac4` + `.incbin "roms/2343.gba", 0x1E58AC4, 0x248`
- card_deck_fs_path_table ROM addr: 0x09e58b08
- file offset: 0x09e58b08 - 0x08000000 = 0x01e58b08
- 偏移 within incbin: 0x01e58b08 - 0x01e58ac4 = 0x44 (verified)
- 分割: 0x44 + 0x204 = 0x248 (verified == original size, byte-identical)
- ROM 内容核: d[0x1E58B08:+4] = `f8e3e309` -> first_ptr = 0x09e3e3f8 -> string "deck/LV1_kuriboh.ydc" (OK)

### Phase 1: C13 残留 DAT_ 扫描

asm lines 3762-5154 实测 **66 个** DAT_/PTR_ 自动名 label（含 `PTR_card_stats_table_0801e96c` 和已符号化的 `PTR_gPrng_*`, `PTR_gP1LifePoints_*`）。

Proposal header 写"65 DAT_/PTR_ slots" —— **实际 66 个**，差 1。

逐项对照 proposal EQ_SLOTS + RENAME_SLOTS 表，发现 **2 个 DAT_ 标签未被覆盖**：

1. **`DAT_0801e744`** (值: 0x0201afb0 = gCardInfoPageState，原始 hex，非符号)：
   - 在 tick_card_info_page_by_state 的字面量池中，被 `ldr r1, DAT_0801e744` 使用
   - gCardInfoPageState 已在 ewram.inc 定义，该槽需 RENAME
   - Proposal 的 EQ_SLOTS 和 RENAME_SLOTS 表中均无此地址

2. **`DAT_0801eb3c`** (值: `gBannerState` 符号，但 slot label 仍为 DAT_)：
   - asm line 4336: `.word  gBannerState  @ 0801eb3c c0fe0102` — 值已符号化
   - 但 slot label `DAT_0801eb3c:` 仍是自动名，需 RENAME
   - Proposal 的 EQ_SLOTS 和 RENAME_SLOTS 表中均无此地址

这两处 DAT_ label 在落地后将保留为自动名，违反 C13。

### Phase 1: C5 重值去重 + C6 名称核实

检查 constants/*.inc 所有文件：
- 所有 10 个新全局地址 (gDuelFieldState / gFontState / gDuelCtx 等) 均不在任何现有 .inc 中定义（以 `.equ` 形式），无重复定义。
- 偏移常量 (DUEL_FIELD_*/GPRNG_*/P1LP_*/PLAYER_BLOCK_STRIDE/GAME_STR_RAW_ID_MASK) 均不在现有 .inc 中。

**命名冲突发现 (C5/C6 concern)**：

`gDuelFieldState` 在 asm/07_equip_effect_chain.s 中已**非正式使用**于地址 0x0201bb90 和 0x0201b290（在 plate 注释中，非 .equ 定义）：

```
asm/07_equip_effect_chain.s:18082: gDuelFieldState (0x0201bb90) ...
asm/07_equip_effect_chain.s:18776: gDuelFieldState=0x0201bb90 ...
asm/07_equip_effect_chain.s:19068: gDuelFieldState=0x0201bb90 ...
asm/07_equip_effect_chain.s:19118: gDuelFieldState = 0x0201b290 ...
```

若 ewram.inc 新增 `.equ gDuelFieldState=0x02023130`，则 asm/07 中已用同名引用不同地址的 plate 注释将造成混淆（该结构名已被别处预占）。

此外，eval 文档对 0x02023130 的命名存在多版本：`gDuelFieldCtx` (11次)、`gGameState` (6次)、`gPageState` (4次)、`gCardState` (4次)。最高频使用为 **`gDuelFieldCtx`**（doc/dev/eval/080c6a20.md:22、080c4ca0.proposal.md 等）。

已有 ewram.inc line 102 注释`@ 注: gPageState @ +0x20 (0x02023130) 是相邻另一结构`。

**结论**: 建议将 `gDuelFieldState=0x02023130` 重命名为 `gDuelFieldCtx=0x02023130`，与 eval 文档最高频用法一致，避免与 07 文件 duel-chain 语义的 gDuelFieldState (0x0201bb90) 混淆。

### Phase 1: C9 ASCII 核实

asm line 4845 (play_ui_effect plate) 包含 **92 个非 ASCII 字符**（CJK 汉字 + 特殊符号）：
- 包含 UI特效派发器、按 ID 分派、子状态机、识别等 CJK 字符

Proposal 的替换文本（约 490 字符）已为纯 ASCII，替换正确。

其他 9 个函数 plate 均无 CJK（已逐行核查 asm lines 3762-5154 中 @ 注释）。

### Phase 1: FUNC_RENAME 抽查 (C11)

抽查 3 个函数：
- **tick_card_info_page_by_state** (0x1e714): body 读 gCardInfoPageState+4 halfword 按 [0,1,2,3] 分派；RENAME=0 OK。
- **tick_duel_field_main_frame** (0x1e984): body 检查 [0x02023130+0x88*4] bitmask，多路分派 duel field；RENAME=0 OK。
- **dispatch_card_display_op** (0x1ec9c): body 61-entry jump table，r0=op_code；RENAME=0 OK。

### Phase 1: C12 R6 消费者证据

关键全局核实：

| 全局 | ref-scan raw | eval 文档证据 | 置信度判定 |
|------|-------------|--------------|-----------|
| gDuelFieldState=0x02023130 | 170 | eval/080c6a20.md（gDuelFieldCtx）; eval/080c4ca0.proposal.md | high（但见命名冲突）|
| gFontState=0x0201f440 | 91 | eval/080c7638.proposal.md line 11 FONT_STATE_BASE | high |
| gDuelCtx=0x02020160 | 95 | eval/080d0c7c.md R6 | high |
| gDuelCardCtxBase=0x0201e2a0 | 442 | eval/080566f4.proposal.md line 11 ACTIVATION_STATE_BASE | high |
| gCardFsDataBlock=0x0201e2b4 | 4 | asm/01 line 3933 comment | high |
| gCardIdCache=0x0201ff60 | 5 | eval/080cc8c8.proposal.md line 9 | high |
| gCardListDisplayBuf=0x02001138 | 12 | asm/01 line 4091 plate | high |
| gDuelSceneBase=0x02023360 | 192 | eval/08028874.proposal.md line 11 SCENE_BASE | high |
| gCardCtxSlotData=0x0201ff30 | 29 | eval/080c6240.proposal.md line 11 | high |
| gP1ZoneHandCount=0x0201c4ec | 23 | gP1LifePoints+0xc=0x0201c4ec (verified) | high |
| gZoneActivTable=0x020230f0 | **1** | asm line 4749-4756 context 索引 player0/1 | **med** |
| PLAYER_BLOCK_STRIDE=0x868 | 2146 raw | eval/0805e578.proposal.md 0x868=33*64（实际 33*8*4？）| **med** |

gP1ZoneHandCount = gP1LifePoints + 0xc = 0x0201c4e0 + 0xc = 0x0201c4ec (verified arithmetic OK)。

PLAYER_BLOCK_STRIDE=0x868: proposal 说 0x868=33*64=2112 但 33*64=2112≠0x868=2152。实际 0x868=2152=33*8*8+8? 语义备注有误，但值本身正确（ROM 核实 OK）。med 置信度可接受。

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ PASS | Seg-4 end=0x1e714 = Seg-5 start；最大 slot DAT_0801f258 = 0x1f258 < 0x1f25c；copy_game_text_if_raw 起于 0x1f238 < 0x1f25c；append_game_text_if_raw 起于 0x1f25c（不含，正确）|
| C2 Rule2 | ✅ PASS | 段内 0 个 ROM_INCBIN/.byte 块；carve 在 rom.s 中进行（已有 card_type_alt_display_table host）|
| C3 Rule3 | N/A | 无 §5.1 块，vacuously OK |
| C4 R1 值 | ✅ PASS | 全 28 主验槽 + 22 reuse 槽 ROM 字节核对 100% OK |
| C5 R1 复用 | ❌ NEEDS_FIX | `gDuelFieldState=0x02023130` 与 asm/07 plates 中非正式使用同名于 0x0201bb90 冲突；eval 最高频名为 `gDuelFieldCtx` |
| C6 R2 名 | ✅ PASS | 所有新 slot label 符合 `^[a-z][a-z0-9_]+$`；多同类加 _a/_b 等后缀；无碰撞 |
| C7 R3 接通 | ✅ PASS | card_deck_fs_path_table REF_SLOT 有 USER-label + DATA-ref plan；两 jump table REF_SLOT 均指向已存在的 switchD_ label |
| C8 R5 现名 | ✅ PASS | 抽查 proposal plates：无残留 FUN_/DAT_ 旧名（Proposal 中两处 FUN_ 提及均为说明性 plate 中已知函数名，非槽引用）|
| C9 ASCII | ✅ PASS | play_ui_effect plate 含 92 个非 ASCII 字符，proposal 替换为纯 ASCII；其余 9 fn plates ASCII-only |
| C10 carve | ✅ PASS | 0x44+0x204=0x248；file offset 0x1E58B08 验证为 deck/LV1_kuriboh.ydc 指针数组（第 1 项 confirmed）|
| C11 误名 | ✅ PASS | 3 fn 抽查名与体一致；FUNC_RENAME=0 合理 |
| C12 R6 | ✅ PASS | 10 全局均有 file:line 证据；gZoneActivTable/PLAYER_BLOCK_STRIDE 标 med-conf；PLAYER_BLOCK_STRIDE 语义注释算术有误（33*64≠0x868）但值正确，可附带修正 |
| C13 残留 | ❌ NEEDS_FIX | asm 实测 66 个自动名 label，proposal 覆盖 64（遗漏 DAT_0801e744 + DAT_0801eb3c），2 处残留自动名 |

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C13 — DAT_0801e744 未覆盖 (遗漏 RENAME)

**问题**: `DAT_0801e744` (值 0x0201afb0 = `gCardInfoPageState`) 在 tick_card_info_page_by_state 字面量池中，使用原始 hex，不是符号。该 slot label 仍为自动名 DAT_，未在 RENAME_SLOTS 中列出。

**修正**: 在 RENAME_SLOTS 表中新增：

```
| DAT_0801e744 (=gCardInfoPageState) | tick_card_info_page_by_state_card_info_page_state | none |
```

fixer 落地时对应 Ghidra 操作：将 0x0801e744 槽标签重命名为 `tick_card_info_page_by_state_card_info_page_state`，并将值符号化为 `.word gCardInfoPageState`（gCardInfoPageState=0x0201afb0 已在 ewram.inc）。

### #2 — C13 — DAT_0801eb3c 未覆盖 (遗漏 RENAME)

**问题**: `DAT_0801eb3c` (值已为 `gBannerState` 符号，但 slot label 仍为 `DAT_0801eb3c:`) 在 tick_duel_field_main_frame 字面量池中，值侧已符号化（`.word gBannerState`），但 label 本身仍是自动名，未在 RENAME_SLOTS 中列出。

**修正**: 在 RENAME_SLOTS 表中新增：

```
| DAT_0801eb3c (=gBannerState) | tick_duel_field_main_frame_banner_state_b | none |
```

fixer 落地时对应 Ghidra 操作：将 0x0801eb3c 槽标签重命名为 `tick_duel_field_main_frame_banner_state_b`（_b 后缀与 play_ui_effect_banner_state 区分，且在 tick_duel_field_main_frame 函数中已有多个 gBannerState 相关用法）。

---

## 附加建议 (非 NEEDS_FIX，但推荐 fixer 落地前确认)

### 建议 A — C5 命名一致性: gDuelFieldState → gDuelFieldCtx

`gDuelFieldState=0x02023130` 与 asm/07_equip_effect_chain.s 中 plate 注释使用同名于不同地址 (0x0201bb90/0x0201b290) 存在逻辑混淆。eval 文档最高频名为 `gDuelFieldCtx` (11 次 vs 4 次 gPageState, 6 次 gGameState)。

建议将 proposal 中所有 `gDuelFieldState` 替换为 `gDuelFieldCtx`（ewram.inc 条目名 + 所有 EQ_SLOTS const_name + 所有 slot_label 中的 `duel_field_state` → `duel_field_ctx`）。

这是一个语义一致性建议，不影响 byte-identical 正确性，但影响跨文件命名统一。fixer 可自行判断是否纳入本轮。若纳入，需同步修改 ewram.inc 新增条目名及其他引用此常量的 slot label。

### 建议 B — PLAYER_BLOCK_STRIDE 语义注释算术修正

Proposal 注释写 `0x868=33*64=2112` 但 33*64=2112≠0x868=2152。实际 0x868 = 0x434*2 = 1076? 不对。0x868 = 2152 = 8*269。可能实际 stride = 34*8*8 = 34*64 = 2176? 也不对。建议 fixer 在 ewram.inc 注释中去掉 `33*64` 展开式，仅写 `player data block stride (0x868=2152 bytes)` 或待运行时核实。

---

## 落地前置提醒 (fixer 参考)

1. **先修改 proposal**（模式A）：补充 RENAME_SLOTS #1/#2；可选采纳建议A改 gDuelFieldState→gDuelFieldCtx。
2. **ewram.inc 新增**: 10 个全局 + 11 个偏移/常量（含 GAME_STR_RAW_ID_MASK；注意不放入 card_info.inc，应放 ewram.inc 或新 duel_field.inc）。
3. **rom.s carve**: card_type_alt_display_table incbin 拆分为 0x44 + (label) + 0x204。
4. **Ghidra 脚本**: 64 个 EQ/RENAME + 2 个新增 RENAME = 66 slot labels 全部处理。
5. **play_ui_effect plate**: 替换为 ASCII 版本（proposal §PLATE 1）。
6. byte-identical SHA1 `9689337d` 落地后必须 build 验证。

---

## 状态: NEEDS_FIX (2 items)
