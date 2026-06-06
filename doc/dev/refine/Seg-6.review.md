# Refine Review: Seg-6

> 范围: `asm/00_system_str_vija.s` 行 9197..11199, ROM 0x0801794c..0x08018774, 28 fn
> proposal: `doc/dev/refine/Seg-6.proposal.md`
> 复核时间: 2026-06-07

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致, 未跳号/回头 | PASS | refine-progress.md 确认 Seg-5d 已完, Seg-6 (0x1794c..0x18774) 为下一步, 28 fn 计数一致 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 段内唯一 ROM_INCBIN 0x186ce/0x22 (line 11114) 已判 §5.1 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立重跑 ref-scan: 0x080186ce..0x080186ee 全 9 个 4B 子地址 raw=0, thumb=0; THUMB 入口 0x080186d0 raw=0, thumb=0 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | NEEDS_FIX | carve H palette 4 处错误: entries[4..7] proposal 0x03e0/0x7fe0/0x03ff/0x7fff, ROM 实际 0x83e0/0xffe0/0x83ff/0xffff (bit15 set); 其余 13 个 EQ 槽值独立核对全 OK |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | PASS | OAM_ATTR2_CHARNAME_MASK/CLEAR/GFX_ATTR_CLEAR_BITS_13_7/OBJ_TILE_VRAM_BASE 均正确复用现有 inc; OAM_ATTR1_X_MASK=0x1ff 与 gl_scrollbar.inc SCROLLBAR_KEEP_BITS_8_0=0x1ff 同值异义, 创建新名无冲突 |
| C6 R2 名 | 槽名格式正确, 无碰撞 | PASS | 所有 RENAME_SLOT/EQ/REF/carve 名均 `^[a-z][a-z0-9_]+$`; 常量名 `^[A-Z][A-Z0-9_]+$`; sync_scrollbar_to_bg_vofs 同值两槽用后缀 `_b` 区分 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 14 个 REF_SLOTS 全有 USER-label 目标 + DATA ref 计划 (name_char_tile_slot_table/group_ptr_table/range_table/banlist_jp_str_src/line_break_seq x2/name_o_resource_desc/name_b_0x_path x3/name_o_palette_data/cursor_anim_data_a/b) |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 DAT_ | PASS | Proposal 识别 6 处需更新的 plate, 均具体指明新名; CJK plate 标注需 ASCII 重写 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 独立检验所有 RENAME_SLOT EOL 文本: 全 ASCII; CJK plate 仅在 doc 层描述, fixer 输出需 ASCII |
| C10 carve | 指针表条目 +1 (THUMB) 检查 | PASS | carve B (name_char_group_ptr_table): 10 个样本 .word 均无 +1 (数据指针); carve F (resource desc): 4 .word 均无 +1 (数据指针) |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 抽查 zero_obj_vram_tiles/build_sprite_oam_row/read_banlist_char_at_scroll_pos: 函数名与体内操作一致; proposal 独立核查 28 fn 全 0 误名 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | 12 个消费者记录均有 asm line 号 + high 置信度; 无零容忍词 |
| C13 残留 | 段内所有残留 DAT_ 都被覆盖 | PASS | 实际 Seg-6 (asm 行 9197..11199) 共 83 个 DAT_ label; proposal 覆盖全部 83 个; 额外 3 个 (DAT_080187d4/d8/dc) 属 Seg-7 地址 (0x080187d4 > 0x08018774), 见 NEEDS_FIX #5 说明 |

---

## 状态: NEEDS_FIX (5 items)

---

## 修改清单

### #1 — C4 — carve H palette values 错误

**文件**: `doc/dev/refine/Seg-6.proposal.md`, carve H 节

**问题**: ROM file offset 0x1CCD290 处实测 16 hword 调色板, entries[4..7] 含 bit15 标志位, 与 proposal 不符。

**错误行**:
```
    .hword 0x0000, 0x7c00, 0x001f, 0x7c1f, 0x03e0, 0x7fe0, 0x03ff, 0x7fff
    .hword 0x2108, 0x6000, 0x0018, 0x6018, 0x0300, 0x6300, 0x0318, 0x5294
```

**正确值** (独立 python 读 ROM 0x1CCD290 前 32B 核实):
```
    .hword 0x0000, 0x7c00, 0x001f, 0x7c1f, 0x83e0, 0xffe0, 0x83ff, 0xffff
    .hword 0x2108, 0x6000, 0x0018, 0x6018, 0x0300, 0x6300, 0x0318, 0x5294
```

差异: entries[4]=0x83e0, [5]=0xffe0, [6]=0x83ff, [7]=0xffff (各比 proposal 多 bit15=0x8000). 若 fixer 按 proposal 的错误值写 .hword, build 将产生 byte-mismatch (不是 byte-identical). 必须使用实测值.

---

### #2 — C4 — carve I 余 incbin 起止错误

**文件**: `doc/dev/refine/Seg-6.proposal.md`, carve I 节

**问题**: 全块 18B (0x12) = 2B NUL pad + "TableLast(%d)\n" (14 chars) + 1B NUL + 1B trailing. 共 17B 已结构化, 剩余 1B 在 file offset 0x1E3B347.

**错误行**:
```
.incbin "roms/2343.gba", 0x1E3B346, 0x8   @ remaining to end of original incbin (0x1E3B348)
```

**正确值**:
```
.incbin "roms/2343.gba", 0x1E3B347, 0x1   @ 1B trailing to end of host (0x1E3B348)
```

说明: proposal 从 0x1E3B346 (比正确起点早 1B) 开始, 大小写成 0x8 (实际只有 1B). 0x1E3B346 + 0x8 = 0x1E3B34E 超出 host 结束地址 0x1E3B348, 属越界错误, 必将 build fail.

实测全块字节: `00005461626c654c617374282564290a0000` (18B = 0x12, 末尾 1B=0x00 为 trailing).

---

### #3 — C4 — carve G 余 incbin 大小错误

**文件**: `doc/dev/refine/Seg-6.proposal.md`, carve G 节

**问题**: 主机 incbin 0x1E3B46F, 0x1115. carve 内容 = cursor_anim_data_a (12B) + gap incbin (1B) + cursor_anim_data_b (28B) = 41B = 0x29. 余 = 0x1115 - 0x29 = 0x10EC, 从 0x1E3B498 起.

**错误行**:
```
.incbin "roms/2343.gba", 0x1E3B498, 0x1087  @ remainder
```

**正确值**:
```
.incbin "roms/2343.gba", 0x1E3B498, 0x10EC  @ remainder to host end 0x1E3C584
```

说明: 0x1E3B498 + 0x1087 = 0x1E3C51F, 比 host end 0x1E3C584 少 0x65 字节 (101B), 将造成 build 覆盖缺口. 核验: 0x1E3B46F+0x1115=0x1E3C584, 紧邻 pass_main_c_filename 标签 (ROM bytes="Pass" 确认). 正确余 = 0x1115 - 41 = 0x10EC.

---

### #4 — C4 — carve B GAS snippet 仅 10 entries, 应为 50

**文件**: `doc/dev/refine/Seg-6.proposal.md`, carve B 节

**问题**: GAS snippet 只列出 10 个 .word entries (char group 0..9), 而 driver RESOLVED 节和实测均为 50 entries. carve B 节的余 incbin 也随之错误.

**错误 snippet** (仅 10 entries + 错误余):
```
    .word 0x09e3b248  @ char group 0
    ... (entries 0..9 only) ...
    .word 0x09e3b1dc  @ char group 9
.incbin "roms/2343.gba", 0x1E58818, 0x4F4   @ remaining
```

**正确值**: 50 entries (0x09e3b248 降至 0x09e3b0b0, 含重复目标 [36][38][48][49]=0x09e3b0b0), 余 incbin:

```
    .word 0x09e3b248  @ [0]
    .word 0x09e3b23c  @ [1]
    ... (entries 0..49) ...
    .word 0x09e3b0b0  @ [49]
.incbin "roms/2343.gba", 0x1E588B8, 0x454   @ remaining
```

计算: carve A (4B) + carve B (200B) = 204B = 0xCC; host 0x520 - 0xCC = 0x454; start = 0x1E587EC + 0xCC = 0x1E588B8. 独立核验: entry[50] at 0x09e588b8 = 0x08017575 (CODE, 出界正确).

完整 50 entries (独立读 ROM 0x09e587f0 core):
```
[0..9]:  0x09e3b248 23c 230 224 218 20c 200 1f4 1e8 1dc
[10..19]: 1d0 1c4 1b8 1ac 1a0 194 188 178 16c 160
[20..29]: 158 150 148 140 138 128 118 108 0f8 0e8
[30..39]: 0e0 0d8 0d0 0c8 0c0 0b4 0b0 0a4 0b0 098
[40..49]: 090 088 080 078 070 068 060 058 0b0 0b0
```
(prefixed with 0x09e3b; entries [36][38][48][49] = 0x09e3b0b0 重复)

---

### #5 — C4 — carve F 末尾余 incbin 不应存在

**文件**: `doc/dev/refine/Seg-6.proposal.md`, carve F 节

**问题**: host incbin 0x1E3B35E, 0xD6 (214B) 被 7 个结构体 完整覆盖:
2B pad + 4x28B (ncer/nanr/ncgr/nclr paths) + 16B (resource_desc) + 3x28B (name_b_01/02/04 paths) = 2+112+16+84 = 214 = 0xD6. 余 = 0B, 无需 incbin.

**错误行**:
```
.incbin "roms/2343.gba", 0x1E3B434, 0x3B  @ remainder to end (ends 0x1E3B46F)
```

**说明**: 0x1E3B35E + 0xD6 = 0x1E3B434 = host 结束地址, 余 0B. proposal 写的 0x3B bytes 是 host 之外的区域, 覆盖了 rom.s line 944 已有的 `assert_anmid_ig2d_getanmsequencescoun` .asciz 标签 (独立核验: 该 .asciz = "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])" = 58+1=59=0x3B bytes). 若 fixer 写入此余 incbin 会重复/覆盖现有 assert 标签, 破坏 rom.s 一致性. 删除此行即可.

布局核验 (各路径):
- name_o_ncer_path @0x09e3b360: "name_input/name_o_01.LZncer" (27+NUL=28B, 4B-aligned)
- name_o_nanr_path @0x09e3b37c: 28B (offset +0x1E 正确)
- name_o_ncgr_path @0x09e3b398: 28B (offset +0x3A 正确)
- name_o_nclr_path @0x09e3b3b4: 28B (offset +0x56 正确)
- name_o_resource_desc @0x09e3b3d0: 4 words=16B (offset +0x72 正确)
- name_b_01_path @0x09e3b3e0: "name_input/name_b_01.LZ5bg" (26+NUL=27, aligned=28B)
- name_b_02_path @0x09e3b3fc: 28B
- name_b_04_path @0x09e3b418: 28B (ends @+0xD4=0x09e3b432 ... wait, 0x09e3b418+28=0x09e3b434=host end OK)

---

### #6 — C13/scope note — 3 Seg-7 DAT_ 槽混入 Seg-6 proposal

**文件**: `doc/dev/refine/Seg-6.proposal.md`, 残留自动名槽表

**问题**: DAT_080187d4 / DAT_080187d8 / DAT_080187dc 位于地址 0x080187d4..0x080187dc, 均 > Seg-6 上边界 0x08018774, 属 refresh_selected_char_obj_tile (Seg-7 首函数) 的 literal pool.

**不阻塞** (83 个实际 Seg-6 DAT_ 全部覆盖, 0 遗漏), 但 fixer 需注意:
- 这 3 槽若在 Seg-6b 中处理则提前消化 Seg-7 工作, 可接受;
- 若不处理需在 Seg-7 proposal 中再次列出;
- 它们的值已独立核验正确 (0x02029250=gState, 0x09e587ec=name_char_tile_slot_table, 0x000002c2).

---

## 各 carve 覆盖核对结论

| carve | host incbin | 覆盖等式 | 状态 |
|-------|-------------|---------|------|
| A: name_char_tile_slot_table | 0x1E587EC, 0x520 | 4B .hword x2 | OK (含入 B 计算) |
| B: name_char_group_ptr_table | (同上, +4B) | 200B (50 .word) + incbin 0x1E588B8, 0x454 = 0x51C; A+B+rem=0x520 OK | NEEDS_FIX (snippet 仅 10) |
| C: name_char_range_table | 0x1E3AFDC, 0x2DC (kana 池) | label+incbin-span 法, 无需计算总量; 含入 kana 池整体 carve | OK (BLOCKED 消解) |
| D: line_break_seq | (同上) | label @+0x2D8, incbin-span 到块尾 | OK |
| E: banlist_jp_str_src | (同上, 块首) | label @+0x0 | OK |
| F: name_o_resource_desc block | 0x1E3B35E, 0xD6 | 2+4x28+16+3x28=214=0xD6, 余=0; 无余 incbin | NEEDS_FIX (多余 0x3B 行) |
| G: cursor_anim_data_a/b | 0x1E3B46F, 0x1115 | 12+1+28+0x10EC=0x1115 OK | NEEDS_FIX (余应为 0x10EC 不是 0x1087) |
| H: name_o_palette_data | 0x1CCD290, 0x16D0 | 32B .hword + incbin 0x16B0 = 0x16D0 OK (结构正确, 但 .hword 值错) | NEEDS_FIX (4 hword 值 bit15 错) |
| I: assert_table_last_fmt | 0x1E3B336, 0x12 | 2+14+1=17B + 1B trailing = 18=0x12 OK | NEEDS_FIX (余应 0x1E3B347/0x1 不是 0x1E3B346/0x8) |

---

## kana 区 ref-scan 结论

独立重扫 incbin 0x1E3AFDC, 0x2DC (0x09e3afdc..0x09e3b2b8, 732B):
- 4B-aligned 扫描命中 50 个有引用地址 (49 raw + 1 thumb-only)
- 0x09e3b251 (非 4B 对齐) 额外有 raw=1 ref
- 合计 distinct 被引用地址 = 51 (与 proposal 一致)
- 但 distinct label 位置 = 50 (0x09e3b250 的 thumb ref 目标即为 0x09e3b251, 不需在 0x09e3b250 再加 label)

关键子地址核验:
- 0x09e3afdc: raw=1 (banlist_jp_str_src) OK
- 0x09e3b2b4: raw=2 (line_break_seq, 两个消费者) OK; bytes=81 40 00 00 (SJIS full-width space) OK
- 0x09e3b251: raw=1, 0x09e3b250 thumb=1 (name_char_range_table) OK
- name_char_group_ptr_table: 50 entries 全在 kana 区 [0x09e3afdc..0x09e3b2b8]

ptr 表 50-entry 核验: entry[50] = 0x08017575 (CODE, 确认边界). Entry[0..49] 全落 kana 区. 独立核验 PASS.

---

## §5.1 ref-scan 详细结果

ROM_INCBIN 0x186ce (0x080186ce), 0x22 = 34B, 含 9 个 4B-aligned 子地址:

| 子地址 | raw | thumb |
|--------|-----|-------|
| 0x080186ce | 0 | 0 |
| 0x080186d2 | 0 | 0 |
| 0x080186d6 | 0 | 0 |
| 0x080186da | 0 | 0 |
| 0x080186de | 0 | 0 |
| 0x080186e2 | 0 | 0 |
| 0x080186e6 | 0 | 0 |
| 0x080186ea | 0 | 0 |
| 0x080186ee | 0 | 0 |

全 0 引用确认. THUMB 入口 0x080186d1 (.word 值) = 0 refs. §5.1 登记合规.
