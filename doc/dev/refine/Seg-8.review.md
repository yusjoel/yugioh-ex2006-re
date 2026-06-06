# Refine Review: Seg-8

## 段信息

- 文件: `asm/00_system_str_vija.s`
- ROM 范围: `0x08019a58..0x0801a794` (28 fn, banlist password 渲染簇)
- proposal: `doc/dev/refine/Seg-8.proposal.md`
- 复核日期: 2026-06-07

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致, 未跳号 | **FAIL** | Seg-8=[0x19a58,0x1a794); proposal 混入大量 >=0x1a794 Seg-9 项 (见移除清单) |
| C2 Rule2 | 每个 incbin 块有归宿 | PASS | Seg-8 内无 incbin 块 (blocks A/B 均 >=0x1a794, Seg-9); 本段 C2 vacuous |
| C3 Rule3 | §5.1 块 0 引用 | PASS | Seg-8 无 §5.1 块; vacuous |
| C4 R1 值 | EQ value == ROM 4B LE | PASS | 独立重跑: 全部 50 个 Seg-8 EQ 槽字节核对一致 (见下方核对表) |
| C5 R1 复用 | 新建前确无现有重值 | **FAIL** | 0x01000200 已存 NAME_INPUT_BG0_SCREEN_CLEAR_CTRL (name_input.inc:21); proposal 新建两个槽标签而非复用 |
| C6 R2 名 | 槽名合规, 无碰撞 | PASS | 全部 50 个 Seg-8 槽名符合 `^[a-z][a-z0-9_]+$`; 无重复 |
| C7 R3 接通 | carve 有 USER-label + DATA-ref | PASS | 7 个 Seg-8 carve 目标引用代码地址均 <0x1a794; banlist_pass_ext_char_group 唯一代码引用 0x0801abb0 (Seg-9) → 不在 Seg-8 carve |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | **FAIL** | 11 行 plate 共 14 处 FUN_<hex> 引用指向已命名的 Seg-8 函数 (见修改清单 #3) |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | 扫描 13763..15629 行全部 @ 注释行: 无 U+0080 以上字符 |
| C10 carve | 指针表 .word 正确 | PASS | banlist_pass_obj_resource_desc 4 个 .word 核对: 0x09e3c5b4/c5d0/c5ec/c608 均与 ROM 实读一致 (ROM 数据指针, 无需 +1) |
| C11 误名 | 函数体与函数名一致 | PASS | 抽查 encode_pass_table_entry_to_line_buf/load_banlist_password_table_from_rom/setup_banlist_sprite_oam_row_batch: 体名一致 |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | 消费者证据表含 8 个关键 carve 槽, 均有 asm 行号 + high 置信度 |
| C13 残留 | 段内所有 DAT_/DWORD_ 全覆盖 | PASS | 独立 grep: Seg-8 内 DAT_/DWORD_ 槽共 62 个 (<0x1a794); 全部被 EQ/RENAME/REF 覆盖 |

---

## 状态: NEEDS_FIX (4 项)

---

## 修改清单

### #1 — C1 — 从 Seg-8 proposal 移除全部 Seg-9 项 (36 项)

Seg-8 严格范围 = [0x08019a58, 0x0801a794)。以下 proposal 各章节项全部 >= 0x1a794,
须从 Seg-8 删除并留给 Seg-9:

**EQ_SLOTS 移除 (4 项)**:
| 槽地址 | 槽标签 |
|--------|--------|
| DAT_0801a800 | advance_banlist_password_cursor_slot_ewram_base |
| DAT_0801a804 | advance_banlist_password_cursor_slot_gsettings_offset |
| DAT_0801a890 | retreat_banlist_password_cursor_slot_ewram_base |
| DAT_0801a894 | retreat_banlist_password_cursor_slot_gsettings_offset |

**RENAME_SLOTS 移除 (18 项)**:
| 槽地址 | 槽标签 |
|--------|--------|
| DAT_0801a838 | advance_banlist_password_cursor_slot_dir_field_off |
| DAT_0801a898 | retreat_banlist_password_cursor_slot_dir_field_off |
| DWORD_0801a90c | load_banlist_char_by_cursor_slot_pass_buf_off_661 |
| DWORD_0801a910 | load_banlist_char_by_cursor_slot_ewram_base |
| DWORD_0801a914 | load_banlist_char_by_cursor_slot_gsettings_offset |
| DWORD_0801a94c | get_banlist_scroll_pixel_offset_scrollbar_off |
| DWORD_0801a980 | get_banlist_password_entry_ptr_cursor_hw_off |
| DWORD_0801a9f0 | render_banlist_text_col_cleared_font_scale_off |
| DWORD_0801aa18 | render_banlist_pw_chars_to_buf_scroll_hw_off |
| DWORD_0801aa1c | render_banlist_pw_chars_to_buf_step_byte_off |
| DWORD_0801aa74 | advance_banlist_pw_char_and_render_sp_adj_neg |
| DWORD_0801aa7c | advance_banlist_pw_char_and_render_pw_cur_off |
| DWORD_0801aa80 | advance_banlist_pw_char_and_render_pw_max_off |
| DWORD_0801aaf8 | advance_banlist_pw_char_and_render_scroll_hw_off |
| DWORD_0801aafc | advance_banlist_pw_char_and_render_step_byte_off |
| DWORD_0801aba8 | retreat_banlist_pw_char_and_render_scroll_hw_off |
| DWORD_0801abac | retreat_banlist_pw_char_and_render_pw_cur_off |
| DWORD_0801abd8 | retreat_banlist_pw_char_and_render_pw_cur_off_b |

**REF_SLOTS (gBanlistPasswordBuffer 全局) 移除 (7 项)**:
| 槽地址 | 槽标签 |
|--------|--------|
| DWORD_0801a904 | load_banlist_char_by_cursor_slot_ptr_banlist_pw_buf |
| DWORD_0801a948 | get_banlist_scroll_pixel_offset_ptr_banlist_pw_buf |
| DWORD_0801a97c | get_banlist_password_entry_ptr_ptr_banlist_pw_buf |
| DWORD_0801a9ec | render_banlist_text_col_cleared_ptr_banlist_pw_buf |
| DWORD_0801aa14 | render_banlist_pw_chars_to_buf_ptr_banlist_pw_buf |
| DWORD_0801aa78 | advance_banlist_pw_char_and_render_ptr_banlist_pw_buf |
| DWORD_0801aba4 | retreat_banlist_pw_char_and_render_ptr_banlist_pw_buf |

**REF_SLOTS (carve 槽) 移除 (3 项)**:
| 槽地址 | 槽标签 | 目标 |
|--------|--------|------|
| DWORD_0801a908 | load_banlist_char_by_cursor_slot_ptr_char_candidate_str | 0x09e3bcb1 |
| DWORD_0801a918 | load_banlist_char_by_cursor_slot_ptr_alt_char | 0x09e3c040 |
| DWORD_0801abb0 | retreat_banlist_pw_char_and_render_ptr_ext_char_group | 0x09e3be3c |

**ROM_INCBIN 块移除 (2 项)**:
- Block A: `ROM_INCBIN 0x1a89c, 0x20` (addr=0x0801a89c >= 0x1a794, Seg-9 §5.1 候选)
- Block B: `ROM_INCBIN 0x1ad18, 0xec` (addr=0x0801ad18 >= 0x1a794, Seg-9 disasm 候选)

**disasm 计划移除 (1 项)**:
- 整个 disasm 章节 (0x0801ad18..0x0801ae04) 移到 Seg-9

**carve label 移除 (1 项)**:
- `banlist_pass_ext_char_group` (@0x09e3be3c): 唯一代码引用是 DWORD_0801abb0 (=0x0801abb0, Seg-9); Seg-8 内无代码触发此 carve。从 Seg-8 host1 carve 计划中删除。

---

### #2 — C1+C7 — host1 carve 覆盖等式修正 (gap1 不二次拆分)

**背景**: 移除 `banlist_pass_ext_char_group` 后, host1 gap1 (0x09e3bd67..0x09e3bfdd, 0x276B) 不再分割。
Seg-8 内触发的 Seg-8 carve labels:
- `banlist_char_candidate_str` @0x09e3bcb1: 代码引用 0x08019d98 (Seg-8 `init_banlist_pass_input_bg0_page`) — **保留**
- `banlist_pass_char_str` @0x09e3bfdd: 代码引用 0x08019b2c (Seg-8 `encode_pass_table_entry_to_line_buf`) — **保留**
- `banlist_pass_alt_char` @0x09e3c040: 代码引用 0x08019b30 (Seg-8) — **保留**
- `rom_password_table` @0x09e3c044: 代码引用 0x08019c88 (Seg-8) — **保留**

注: `banlist_char_candidate_str` 的 ref-scan 结果: 0x09e3bcb1 是奇地址, raw 与 thumb|1 值相同 (均=0x09e3bcb1), 实际两个存储点为 0x08019d98 (Seg-8) 和 0x0801a908 (Seg-9)。Seg-8 carve 由 0x08019d98 触发有效; DWORD_0801a908 留 Seg-9 REF。

**正确 host1 (0x1E3B4A8, 0x10DC) 拆分**:
```gas
name_input_default_name:
    .incbin "roms/2343.gba", 0x1E3B4A8, 0x809     @ pre (0x09e3b4a8..0x09e3bcb1)
banlist_char_candidate_str:                         @ 0x09e3bcb1
    .incbin "roms/2343.gba", 0x1E3BCB1, 0xB6       @ 182B (90 SJIS 对 + null 对)
    .incbin "roms/2343.gba", 0x1E3BD67, 0x276      @ gap1 单跨度 (不分割, ext_char_group defer Seg-9)
banlist_pass_char_str:                              @ 0x09e3bfdd
    .incbin "roms/2343.gba", 0x1E3BFDD, 0x63       @ 99B
banlist_pass_alt_char:                              @ 0x09e3c040
    .incbin "roms/2343.gba", 0x1E3C040, 0x4        @ 4B (SJIS full-width space + null)
rom_password_table:                                 @ 0x09e3c044
    .incbin "roms/2343.gba", 0x1E3C044, 0x53E      @ 671 x 2B halfwords
    .incbin "roms/2343.gba", 0x1E3C582, 0x2        @ trailing pad
```
覆盖等式: 0x809 + 0xB6 + 0x276 + 0x63 + 0x4 + 0x53E + 0x2 = **0x10DC** OK。

注意: proposal 给出的 "with ext split" 等式 (0x809+0xD5+0x1A1+...) 是错的 Seg-8 版本, 必须换成上方版本。

---

### #3 — C8 — 11 行 plate 中 FUN_<hex> 引用须改为当前函数名

以下行使用了现已命名的 Seg-8 函数的旧 FUN_ 格式。Fixer 须在 Ghidra 中用脚本将各行中的 `FUN_<addr>` 替换为当前名:

| 行号 | 须替换 | 当前名 |
|------|--------|--------|
| 14015 | FUN_08019d14 | init_banlist_pass_input_bg0_page |
| 14069 | FUN_08019e2c | init_banlist_pass_input_bg2_page |
| 14069 | FUN_0801a1ac | tick_banlist_bg_scroll_step |
| 14086 | FUN_08019d14 | init_banlist_pass_input_bg0_page |
| 14225 | FUN_08019f24 | init_banlist_pass_chars_grid_row |
| 14225 | FUN_08019f78 | refresh_banlist_pass_chars_font_rows |
| 14753 | FUN_08019fe4 | tick_banlist_scroll_input_handler |
| 15169 | FUN_08019e2c | init_banlist_pass_input_bg2_page |
| 15169 | FUN_0801a1ac | tick_banlist_bg_scroll_step |
| 15185 | FUN_0801a540 | call_tick_banlist_card_slot_anim |
| 15295 | FUN_0801a690 | call_setup_banlist_sprite_oam_row |
| 15481 | FUN_08019b4c | render_banlist_pass_char_obj_rows_pair |
| 15514 | FUN_08019b4c | render_banlist_pass_char_obj_rows_pair |
| 15544 | FUN_08019e2c | init_banlist_pass_input_bg2_page |

注: 行号为当前 asm 文件行号 (复核时从文件读取)。FUN_0x0801aec8/af70/b284/b368 是 Seg-9+ 函数, 尚未命名, 暂保留 FUN_ 格式 (不在此次 Seg-8 修改范围)。

---

### #4 — C5 — host2 bg2_fs_path size 错误 + NAME_INPUT_BG0_SCREEN_CLEAR_CTRL 复用

**4a: host2 bg2_fs_path size 错误 (byte-identical 关键)**

Proposal 写: `banlist_pass_bg2_fs_path: .incbin 0x1E3C650, 0x1E`
实际: ROM 字节读 0x1E3C650..0x1E3C670 = 32 字节 (0x20), 内容 = `"pass_input/moziire_b_01.LZ5bg\0\0\0"` (29 字符 + 3 NUL)。
`0x1E3C650 + 0x1E = 0x1E3C66E`, 但 host2_end = `0x1E3C670` — 差 2 字节, **覆盖不足**。

正确写法:
```gas
banlist_pass_bg2_fs_path:
    .incbin "roms/2343.gba", 0x1E3C650, 0x20       @ "pass_input/moziire_b_01.LZ5bg\0\0\0" (32B)
```

正确覆盖等式: `0x2 + 4*0x1C + 0x10 + 0x1C + 0x20 = 0x2 + 0x70 + 0x10 + 0x1C + 0x20 = 0xBE` OK。

**4b: C5 — DWORD_08019d9c / DWORD_08019ec8 复用现有常量**

`0x01000200` 已在 `constants/name_input.inc:21` 定义为 `NAME_INPUT_BG0_SCREEN_CLEAR_CTRL`。
Proposal 为 DWORD_08019d9c 和 DWORD_08019ec8 各建了独立槽标签, 违反 C5。
应改为:
- DWORD_08019d9c → EQ 槽, `.equ`-引用 `NAME_INPUT_BG0_SCREEN_CLEAR_CTRL`
- DWORD_08019ec8 → EQ 槽, `.equ`-引用 `NAME_INPUT_BG0_SCREEN_CLEAR_CTRL`

槽标签名仍可保留以便 Ghidra DATA-ref, 但 value 必须引用现有常量而非重复定义。

---

## 附: 关键核对数据

### C4 EQ 槽 ROM byte 核对 (独立重跑)

全部 50 个 Seg-8 EQ 槽逐一 `struct.unpack_from('<I', d, addr-0x08000000)[0]` 验证, 无一 mismatch:

| 代表性槽 | 期望值 | ROM 实读 | 结果 |
|----------|--------|----------|------|
| 0x08019c20 (gTextEncodingOverride) | 0x0202348c | 0x0202348c | OK |
| 0x08019c30 (GSETTINGS_OFFSET) | 0x00006c2c | 0x00006c2c | OK |
| 0x08019c38 (pass_buf_off_675) | 0x00000675 | 0x00000675 | OK |
| 0x08019c80 (max_entries) | 0x0000029f | 0x0000029f | OK |
| 0x08019d9c (cpuset_screen) | 0x01000200 | 0x01000200 | OK (C5 issue: 已有同值常量) |
| 0x08019da0 (cpuset_char) | 0x01000898 | 0x01000898 | OK |
| 0x0801a168 (scroll_dir_off) | 0x00000666 | 0x00000666 | OK |
| 0x0801a1a0 (assert_line_2cd) | 0x000002cd | 0x000002cd | OK |
| 0x0801a31c (char_vram_addr) | 0x06002280 | 0x06002280 | OK |
| 0x0801a468 (clr_mask) | 0xffffc07f | 0xffffc07f | OK |
| 0x0801a5ec (OAM_ATTR2_CHARNAME_MASK) | 0x000003ff | 0x000003ff | OK |
| 0x0801a5f4 (wide_sprite_mode) | 0x40004000 | 0x40004000 | OK |
| 0x0801a710 (OBJ_TILE_VRAM_BASE) | 0x06010000 | 0x06010000 | OK |
| 0x0801a714 (word_count_mask) | 0x001fffff | 0x001fffff | OK |
| 0x0801a790 (scrollbar_off) | 0x0000064c | 0x0000064c | OK |

### C7 Carve 代码引用 Seg-8 确认

| carve label | target | 代码引用 @ | 是否 Seg-8 |
|------------|--------|----------|---------|
| banlist_char_candidate_str | 0x09e3bcb1 | 0x08019d98 | Seg-8 ✓ |
| banlist_pass_char_str | 0x09e3bfdd | 0x08019b2c | Seg-8 ✓ |
| banlist_pass_alt_char | 0x09e3c040 | 0x08019b30 | Seg-8 ✓ |
| rom_password_table | 0x09e3c044 | 0x08019c88 | Seg-8 ✓ |
| banlist_pass_obj_resource_desc | 0x09e3c624 | 0x0801a458 | Seg-8 ✓ |
| banlist_pass_bg1_fs_path | 0x09e3c634 | 0x0801a464 | Seg-8 ✓ |
| banlist_pass_bg2_fs_path | 0x09e3c650 | 0x0801a46c | Seg-8 ✓ |
| **banlist_pass_ext_char_group** | 0x09e3be3c | **0x0801abb0** | **Seg-9 → defer** |

banlist_pass_ext_char_group 另有 4 个 ROM 数据引用 (0x09e5895c/64/8c/90, 属 banlist_pass_char_group_ptr_table 内, Seg-7 carve), 但那是数据表内嵌指针, 不算代码触发。Seg-9 处理时再 carve。

### C10 host2 resource_desc .word 核对

| 下标 | ROM 实读 | 期望 | 结果 |
|------|----------|------|------|
| [0] 0x09e3c624 | 0x09e3c5b4 | banlist_pass_obj_ncer_path | OK |
| [1] 0x09e3c628 | 0x09e3c5d0 | banlist_pass_obj_nanr_path | OK |
| [2] 0x09e3c62c | 0x09e3c5ec | banlist_pass_obj_ncgr_path | OK |
| [3] 0x09e3c630 | 0x09e3c608 | banlist_pass_obj_nclr_path | OK |

### C13 Seg-8 DAT_/DWORD_ 槽完整核对

独立 grep asm 文件取 DAT_/DWORD_ 地址 < 0x0801a794: 共 **62 个**槽。
构建 Seg-8 已覆盖集合 (EQ 42 + REF 10 + RENAME 10) = 62。无遗漏。

### §5.1 / ROM_INCBIN 验证

Seg-8 (0x19a58..0x1a794) 内无任何 ROM_INCBIN 块。
块 A (0x1a89c) 和块 B (0x1ad18) 均 >= 0x1a794, 均属 Seg-9。
- 块 A ref-scan: raw=1 (0x08af5768, 压缩 FS 资产内偶合), thumb=0 → Seg-9 §5.1 候选
- 块 B ref-scan: 5 handler 地址各 raw=1 (跳转表内), thumb=0 → Seg-9 disasm 候选

---

## Fixer 注意事项

1. **修改 proposal 而非直接落地**: 此次 Fixer 应执行模式 A (修改 proposal), 待下一轮 reviewer 通过后再落地。

2. **host1 gap1 必须保持单一 span**: 移除 banlist_pass_ext_char_group 后, gap1 = `.incbin 0x1E3BD67, 0x276` 整体不分割。banlist_pass_ext_char_group 的 carve 整体移到 Seg-9 proposal。

3. **host2 bg2_fs_path 大小**: 必须改为 0x20 (32B), 非 0x1E。这是 byte-identical 红线: 若用 0x1E 则少 carve 2 字节, 导致汇编输出 ROM 偏移错误。

4. **C5 常量复用**: DWORD_08019d9c 和 DWORD_08019ec8 的 EQ 槽须引用 `NAME_INPUT_BG0_SCREEN_CLEAR_CTRL` (name_input.inc), 不新建同值标签。

5. **C8 plate 更新**: 须用 Ghidra ExportRangeToGas 后的 split_all_s 重导才能验证板文字更新; 或直接在 asm 文件手改对应 11 行的 FUN_<hex> 为当前名后 build 验证。FUN_0x0801aec8/af70/b284/b368 (Seg-9+未命名) 保留不动。

6. **Seg-9 proposal 首要任务**: 新增 banlist_pass_ext_char_group carve; 将 Block A (§5.1 登记) + Block B (disasm 5 stubs) 纳入; 移入 4 EQ + 18 RENAME + 10 REF 槽。
