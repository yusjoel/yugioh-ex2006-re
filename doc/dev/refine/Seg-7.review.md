# Refine Review: Seg-7

## 段信息

- 文件: `asm/00_system_str_vija.s`
- ROM 范围: `0x08018774..0x08019a58` (28 fn)
- proposal: `doc/dev/refine/Seg-7.proposal.md`
- 复核日期: 2026-06-07

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | Seg-7 = 0x18774..0x19a58, 紧跟 Seg-6b (✅), 先于 Seg-8; refine-progress.md 标注一致 |
| C2 Rule2 | 每个 incbin 块有归宿 | PASS | 唯一 incbin 0x19640/0x20 判为 §5.1 登记 |
| C3 Rule3 | §5.1 块 0 引用 | PASS | 独立重跑: entry 0x08019641 count=0; raw 0x08019640 count=0; 内部 0x08019650 count=1 at file offset 0x671310 (图形 blob 偶合, 非代码指针) |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 10 个 EQ 槽全部对 ROM 字节核实 (见下方 byte 核对表) |
| C5 R1 复用 | 新建 constants 前无现有重值 | PASS | 9 个新常量与 name_input.inc 现有 10 项无值冲突; NAME_INPUT_BG0_SCREEN_CLEAR_CTRL=0x01000200 正确复用现有定义 (name_input.inc line 21) |
| C6 R2 名 | 槽名模式合规, 无碰撞 | PASS | 所有 50+ 槽名满足 `^[a-z][a-z0-9_]+$`; 多实例后缀 (_a/_b/_c/_d/_e/_f) 无重复 |
| C7 R3 接通 | carve 有 USER-label + DATA-ref | PASS | carve J: PTR_name_input_state_table_080195d4 在 asm 中已有 DATA ref; carve K: DAT_080192a4/DAT_08019550 计划新建 label ref, 方案正确 |
| C8 R5 现名 | plate 引用全用现名 | PASS | proposal 标注 3 个 CJK plate 须改写为 ASCII, 未发现 FUN_/DAT_/DWORD_ 残留引用 |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | PASS | proposal 明确识别 3 处 CJK plate 并要求 fixer 清除; proposal 文档本身的中文解释不进 Ghidra |
| C10 carve THUMB+1 | carve J 指针表条目 +1 正确 | PASS | 4 个 THUMB fn 指针逐一核对 (见下方); fn_addr 处均为合法 push 开头; stored = fn_addr\|1 精确 |
| C11 误名 | 函数体与函数名一致 | PASS | 抽查 page_state_dispatcher / extract_char_entry_by_lang / init_banlist_pass_input_scene 均与体一致; FUNC_RENAME=0 合理 |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | 消费者证据表含 6 个关键槽, 均有 file:line + high/med 置信度 |
| **C13** | **所有残留自动名槽全覆盖** | **FAIL** | **7 个 DAT_/DWORD_ 槽列于段内残留表但未出现在 RENAME/EQ/REF 任何一栏** (见下方修改清单 #1-#7) |

---

## 状态: NEEDS_FIX (7 items)

---

## 修改清单

### #1 — C13 — DAT_080188cc 未覆盖

- 所属函数: `dispatch_name_input_key_by_state` (0x08018884)
- ROM 字节核: `d[0x188cc:0x188d0] = 0x00000315` (确认值 0x315)
- 列于 proposal 残留表 (段测绘第 3 条), 但 RENAME_SLOTS 表无对应条目
- 修改: 在 RENAME_SLOTS 表追加:

```
| DAT_080188cc | 0x315 | dispatch_name_input_key_by_state_key_type_offset | gState+0x315 bits[5:2] key-type field (0=null 1=confirm 2=del 3=mode_write 4=set_bit6) |
```

---

### #2 — C13 — DAT_08018d2c 未覆盖

- 所属函数: `tick_name_input_frame` 字面量池末端 (代码使用于 0x08018cbc)
- ROM 字节核: `d[0x18d2c:0x18d30] = 0x0000031e` (值 0x31e)
- 列于 proposal 残留表, RENAME_SLOTS 表无对应条目
- 修改: 在 RENAME_SLOTS 表追加:

```
| DAT_08018d2c | 0x31e | tick_name_input_frame_char_count_offset_f | gState+0x31e: char count (5th ref in frame fn, end of literal pool) |
```

---

### #3 — C13 — DAT_08018d30 未覆盖

- 所属函数: `tick_name_input_frame` 字面量池末端 (代码使用于 0x08018cc0)
- ROM 字节核: `d[0x18d30:0x18d34] = 0x0000031f` (值 0x31f)
- 修改: 在 RENAME_SLOTS 表追加:

```
| DAT_08018d30 | 0x31f | tick_name_input_frame_char_limit_offset_f | gState+0x31f: char limit (5th ref in frame fn, end of literal pool) |
```

---

### #4 — C13 — DAT_08018d38 未覆盖

- 所属函数: `tick_name_input_frame` 字面量池末端 (代码使用于 0x08018d0a)
- ROM 字节核: `d[0x18d38:0x18d3c] = 0x00000316` (值 0x316)
- 注: DAT_08018d34 = 0xfffffc3f 是 NAME_INPUT_MODE_CLEAR EQ 的第 6 个实例, 已被 EQ 条目 (x6) 覆盖, 不需额外条目
- 修改: 在 RENAME_SLOTS 表追加:

```
| DAT_08018d38 | 0x316 | tick_name_input_frame_mode_flag_offset_c | gState+0x316: input mode flag byte (3rd ref in frame fn) |
```

---

### #5 — C13 — DAT_08019220 未覆盖

- 所属函数: `tick_name_input_render_by_state` case 2 (代码使用于 0x080191fa 前加载)
- ROM 字节核: `d[0x19220:0x19224] = 0x06000020` (值 0x06000020)
- 0x06000020 = GBA_VRAM_BASE + 0x20 = BG text VRAM 基址 + 0x20 偏移; gba_mem.inc 中无此值 (仅有 GBA_VRAM_BASE=0x06000000)
- 修改: 在 RENAME_SLOTS 表追加 (或新建 EQ):

```
| DAT_08019220 | 0x06000020 | tick_name_input_render_by_state_bg_vram_text_base_a | GBA_VRAM_BASE+0x20: BG0 text VRAM base used in font/text render case2 |
```

若 0x06000020 在段内共 3 处 (08019220/08019370/08019858) 且全属同一语义, 可改为新 EQ 常量 `BG_VRAM_TEXT_BASE = 0x06000020` 追加到 gba_mem.inc 并覆盖 3 个槽。

---

### #6 — C13 — DAT_08019370 未覆盖

- 所属函数: `tick_name_input_render_by_state` case 5
- ROM 字节核: `d[0x19370:0x19374] = 0x06000020`
- 修改: 在 RENAME_SLOTS 表追加:

```
| DAT_08019370 | 0x06000020 | tick_name_input_render_by_state_bg_vram_text_base_b | GBA_VRAM_BASE+0x20: BG0 text VRAM base, case5 ref |
```

---

### #7 — C13 — DWORD_08019858 未覆盖

- 所属函数: `init_font_jp_ctx_bg_vram_text` (0x08019820)
- ROM 字节核: `d[0x19858:0x1985c] = 0x06000020`
- 列于 proposal 残留表 (`init_font_jp_ctx_bg_vram_text: DWORD_08019858 (0x06000020), DWORD_0801985c (0x02006ed0=gFontJpCtx)`)
- DWORD_0801985c 被 REF_SLOTS 覆盖 (gFontJpCtx), 但 DWORD_08019858 未覆盖
- 修改: 在 RENAME_SLOTS 表追加 (或与 #5/#6 统一为 EQ):

```
| DWORD_08019858 | 0x06000020 | init_font_jp_ctx_bg_vram_text_bg_vram_text_base | GBA_VRAM_BASE+0x20: BG text VRAM base for font jp ctx init |
```

---

## 附: 关键核对数据

### EQ 槽 ROM byte 核对 (C4)

| 槽地址 | 期望值 | ROM 实读 | 结果 |
|--------|--------|----------|------|
| 0x08018a24 | 0xfffffc3f | 0xfffffc3f | OK |
| 0x08018bb0 | 0xfffc3fff | 0xfffc3fff | OK |
| 0x080195e4 | 0xffc03fff | 0xffc03fff | OK |
| 0x080196e8 | 0x0500019e | 0x0500019e | OK |
| 0x080196ec | 0x00001d0d | 0x00001d0d | OK |
| 0x080196f0 | 0x00001f0f | 0x00001f0f | OK |
| 0x08019070 | 0x01000020 | 0x01000020 | OK |
| 0x08019074 | 0x01000200 | 0x01000200 | OK |
| 0x08019224 | 0x01000840 | 0x01000840 | OK |
| 0x08019378 | 0x01000040 | 0x01000040 | OK |

### carve J ROM byte 核对 (C10)

| 下标 | vaddr | ROM 实读 | 期望值 | 含义 |
|------|-------|----------|--------|------|
| [0] | 0x09e588b8 | 0x08017575 | name_input_page_init+1 | THUMB fn ptr |
| [1] | 0x09e588bc | 0x080180ad | name_input_page_load_assets+1 | THUMB fn ptr |
| [2] | 0x09e588c0 | 0x08019495 | name_input_page_tick+1 | THUMB fn ptr |
| [3] | 0x09e588c4 | 0x080194ed | name_input_page_exit+1 | THUMB fn ptr |
| [4] | 0x09e588c8 | 0x00000000 | NULL sentinel | |
| [5..12] | 0x09e588cc..e8 | 0x09e3bfd4..80 | banlist pass char group ptrs | ROM data ptrs |

fn 函数入口确认 (首半字均为合法 push 指令):
- 0x08017574: 0xb510 (push {r4,lr})
- 0x080180ac: 0xb5f0 (push {r4,r5,r6,r7,lr})
- 0x08019494: 0xb510 (push {r4,lr})
- 0x080194ec: 0xb500 (push {lr})

覆盖等式: 0x34 + 0x420 = 0x454 = host incbin size. PASS.

### carve K ROM byte 核对

| 地址 | ROM 实读 | 含义 |
|------|----------|------|
| 0x1E3B4A4 (name_input_render_param_4b) | 38 84 88 84 | 4B render param block |
| 0x1E3B4A8 (name_input_default_name) | 82 c4 82 b7 82 c6 00 00 | SJIS "てすと" + NUL |

参照 refs 核: 0x09e3b4a4 raw=1 (DAT_080192a4); 0x09e3b4a8 raw=1 (DAT_08019550). PASS.
覆盖等式: 0xC + 0x4 + 0x10DC = 0x10EC = host incbin size. PASS.

### §5.1 ref-scan (C3)

```
d.count(pack('<I', 0x08019641)) = 0   # THUMB entry
d.count(pack('<I', 0x08019640)) = 0   # raw addr
# interior 0x08019650: count=1, file offset 0x671310 = vaddr 0x08671310 (graphics blob, non-code)
```

### gPrng base 核实 (C7)

- PTR_gPrng_080195d8 ROM 实读: 0x03000040 (gPrng base)
- gPrng+0x21a = 0x0300025a (name_input_page_exit_committed_name_buf, DAT_08019508 实读一致)
- gPrng+0x23a = 0x0300027a (mode flag slot)
- gState+0x66e = 0x020298be (banlist total count)

---

## Fixer 注意事项

1. 修改清单 #5/#6/#7 中 3 个 0x06000020 槽, 可选方案: 新建 `BG_VRAM_TEXT_BASE = 0x06000020` 追加到 gba_mem.inc (6 个 ROM ref 全 ROM), 并作为 EQ 槽处理; 或各自独立 RENAME. 任一方案均 byte-identical.

2. Plate 改写: 3 个 CJK plate 须在 Ghidra 重写为纯 ASCII. proposal 未提供具体 ASCII 文本, fixer 可在保留现有 ASCII 段落基础上直接删除所有 CJK 字符 (U+0080 以上). 重写后需 build 验 SHA1.

3. 所有改动须在 Ghidra 脚本中实现, 重导出 + build + SHA1 = 9689337d 红线.
