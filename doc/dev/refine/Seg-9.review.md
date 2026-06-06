# Refine Review: Seg-9

Seg range: `[0x0801a794, 0x0801b850)`, 28 fn, banlist/shuen scene.
Proposal: `doc/dev/refine/Seg-9.proposal.md`.
Reviewer: independent re-scan (python ROM byte reads + grep asm).

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | last fn init_demo_shuen_display_state @0x0801b7e8 < 0x0801b850; next fn load_demo_shuen_sprite_gfx @0x0801b850 confirmed in asm L17853. 所有 carve 目标在 CART 空间 (0x09eXXXXXX), 不在代码段。 |
| C2 Rule2 | 每个 ROM_INCBIN 都有归宿 | PASS | Block A (0x1a89c, 0x20) -> §5.1; Block B (0x1ad18, 0xec) -> disasm R4 (5 stubs). 两块均有处理方案。 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | Block A: 独立重跑 ref-scan: entry 0x0801a89c raw=0/thumb=0. 0x0801a8a0 raw=1 仅在 ROM offset 0x00af5768 (vaddr 0x08af5768, FS compressed asset 区), 确为压缩数据偶合值非代码引用. Block B 5 stubs 各有 raw=1 来自 jump table (正确归 disasm). |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 全部 5 个 NAME_INPUT_MODE_CLEAR=0xfffffc3f: PASS. NAME_INPUT_PAGE_STATE_CLEAR=0xffc03fff: PASS. 全部 63 RENAME_SLOTS 值逐一读 ROM 验证: 0 误差. |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | PASS | proposal 无新建 .equ. 8 个复用常量全部在现有 inc 文件中验证: NAME_INPUT_MODE_CLEAR/NAME_INPUT_PAGE_STATE_CLEAR(name_input.inc), EWRAM_BASE(gba_mem.inc), GSETTINGS_OFFSET(name_input.inc), gBanlistPasswordBuffer/gTextEncodingOverride/gDemoState(ewram.inc), gPrng(iwram.inc). |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$ 无碰撞 | PASS | 抽查 10+ 槽名全符合格式. 多同类槽有 _a/_b/_c/_d/_e 后缀区分. |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 3 个 carve label 全有对应 REF_SLOTS 条目: banlist_pass_ext_char_group(DWORD_0801abb0), banlist_handler_table(DWORD_0801b678+DAT_0801b704), banlist_scroll_view_anim_params(DWORD_0801b3c4). |
| C8 R5 现名 | plate 引用全用现名 | **FAIL** | proposal 的 4 个 CJK plate 改写为 ASCII 且无 FUN_ — PASS. 但现有 3 个**英文 plate** 含 FUN_ 未在 proposal 中列为待更新: (1) load_banlist_char_by_cursor_slot L15787: FUN_0801aa54; (2) dispatch_banlist_cursor_action L16343: FUN_0801af70; (3) tick_banlist_oam_palette_fade L16883: FUN_0801b1a0. 另有 2 个外部调用者 FUN_ 也可更新: dispatch_banlist_pass_input_frame L17599: FUN_081089d8; scale_char_width_by_encoding L17732: FUN_0801a230. Proposal 第 404 行称"none found in Seg-9 range"与实际不符. |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 4 个 CJK plate 改写文本经独立检查: 0 non-ASCII. 现有 5 个英文 plate 无 CJK. |
| C10 carve | 指针表 THUMB ptrs + ROM raw 值核 | PASS | banlist_handler_table 3 entries (0x08019661/0x0801a329/0x0801b5d9) 全为奇地址 (THUMB+1), 对应 fn 0x08019660/0x0801a328/0x0801b5d8, 由 invoke_r1 (BX r1) 调用 — 正确. jump table (0x0801ad00) 6 entries 全为偶地址 (raw, 经 mov pc,r0 dispatch, 不切 ISA) — 正确. |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 抽查 3 fn: tick_banlist_scrollbar_and_slot_anim(调用 scrollbar+slot anim), init_demo_shuen_display_state(清 gDemoState+设 BGxCNT), dispatch_banlist_scene_handler_frame(handler table dispatch). 均与名一致. |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | banlist_handler_table: high conf, L17542; banlist_scroll_view_anim_params: med conf, L17186-17188 memcpy, 升级路径有说明; NAME_INPUT_MODE_CLEAR reuse: high conf, L16700+. 无零置信度槽. |
| C13 残留 | 段内所有残留自动名槽都被覆盖 | PASS | 独立 grep 实际残留 121 个 (proposal 称 132, 差异来自已被之前 batch 细化的部分); 逐一与 proposal EQ+REF+RENAME 对照: 0 遗漏. |

---

## carve 覆盖等式 (独立重算)

| carve | 等式 | 结论 |
|-------|------|------|
| Carve 1 (banlist_pass_ext_char_group @0x09e3be3c) | 0xD5 + 0x1A1 = 0x276 == host size | PASS |
| Carve 2 (ptr_table ext + handler_table, host 0x1E588EC) | 0xA8 + 0x10 + 0x368 = 0x420 == host size | PASS |
| Carve 3 (banlist_scroll_view_anim_params @0x09e3c6ab) | 6 + 3 = 9 == host incbin size | PASS |

## Carve 3 assert-block 安全性结论

`0x09e3c6ab` (ROM off `0x1E3C6AB`) 位于 assert carve block 内 (`0x1E398DC..0x1E58D0C`).
经独立读 ROM 确认:
- off `0x1E3C6AA` = `0x00` (NUL), 是 `assert_anmid_ig2d_getanmsequencescoun_670` asciz 串的结束符.
- off `0x1E3C6AB..0x1E3C6B3` = `06 06 07 07 07 07 00 00 00` (6B 参数表 + 3B NUL 填充), 正是当前 `.incbin 0x1E3C6AB, 0x9`.
- off `0x1E3C6B4` 开始: `"dstBuffID >= 0 && ds..."` (assert_dstbuffid 串起点).
- **结论**: carve3 数据在两条 assert 串的间隙 incbin 内, 不与任何 `.asciz` 重叠. SAFE.

## disasm Block B 字节不变确认

Block B (ROM_INCBIN 0x1ad18, 0xec = 236B) 经 Ghidra `DisassembleCommand` 反汇编为 THUMB 代码后, **ROM 字节不改变** — disasm 只修改 listing 表示, 不修改字节. byte-identical 必然保持. 5 stubs 范围: 8+44+72+76+36 = 236B = 0xec, 覆盖完整. entry[1]=0x0801ae04 已在 Block B incbin 范围外 (反汇编好的代码), 跳过正确.

## §5.1 Block A 结论

Block A (0x1a89c, 0x20): ref-scan 独立重跑结果:
- entry 0x0801a89c: raw=0, thumb=0 -> 0 code 引用.
- 0x0801a8a0: raw=1, 引用位置 ROM off 0x00af5768 (vaddr 0x08af5768), 属于 FS compressed asset 区 (>0x08800000), 确为压缩数据偶合值, 非代码引用.
- 其余 6 个 4B sub-addr: 均 raw=0/thumb=0.
- **结论**: §5.1 dead leaf 认定正确. PASS.

---

## 状态: NEEDS_FIX

---

## 修改清单 (5 条, 均为 C8)

### #1 — C8 — load_banlist_char_by_cursor_slot plate 残留 FUN_ (L15787)

当前 plate: `"... Called by FUN_0801aa54 when user selects a character."`
FUN_0801aa54 = `advance_banlist_password_char_and_render` (Seg-9 命名函数).
**修改**: 将 plate 中 `FUN_0801aa54` 替换为 `advance_banlist_password_char_and_render`.

### #2 — C8 — dispatch_banlist_cursor_action plate 残留 FUN_ (L16343)

当前 plate: `"... Called by FUN_0801af70 each frame to detect and trigger cursor action."`
FUN_0801af70 = `tick_banlist_password_frame` (Seg-9 命名函数).
**修改**: 将 plate 中 `FUN_0801af70` 替换为 `tick_banlist_password_frame`.

### #3 — C8 — tick_banlist_oam_palette_fade plate 残留 FUN_ (L16883)

当前 plate: `"... Called each frame by FUN_0801b1a0 during banlist scene frame update."`
FUN_0801b1a0 = `tick_banlist_card_slot_anim_primary` (Seg-9 命名函数).
**修改**: 将 plate 中 `FUN_0801b1a0` 替换为 `tick_banlist_card_slot_anim_primary`.

### #4 — C8 — dispatch_banlist_pass_input_frame plate 残留 FUN_ (L17599)

当前 plate: `"... Called by FUN_081089d8 (scene_pass_input;pass_input;prng) each frame."`
FUN_081089d8 = `transition_banlist_pass_to_card_list` (asm/23_sound_cardlist_libc.s, 已命名).
**修改**: 将 `FUN_081089d8` 替换为 `transition_banlist_pass_to_card_list`. 括号内说明标签保留或删除均可.

### #5 — C8 — scale_char_width_by_encoding plate 残留 FUN_ (L17732)

当前 plate: `"@ Caller FUN_0801a230 (font_jp;game_str;settings) uses return value..."`
FUN_0801a230 = `render_banlist_title_text_to_bg` (asm/00_system_str_vija.s L14879, 已命名).
**修改**: 将 `FUN_0801a230` 替换为 `render_banlist_title_text_to_bg`. 括号内标签删除.

---

## 附: 非阻塞证据 typo (无需 NEEDS_FIX)

- proposal `game_str_pointer_table` Evidence 行写 `0x08080f40` (多一个 8), 实际 vaddr 为 `0x08000f40`. 该 label 赋值本身正确 (ROM slot 0x0801b42c = 0x08000f40 = game_str_pointer_table 实际地址). typo 在文档说明文字, 不影响 Ghidra 脚本执行. fixer 修正 proposal evidence 行即可, 不影响落地.
