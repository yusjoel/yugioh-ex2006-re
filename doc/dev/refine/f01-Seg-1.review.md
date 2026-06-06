# Refine Review: f01-Seg-1 [0x0801cb00..0x0801d448)

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | §五 Seg-1=0x1cb00..0x1d448, 8 fn, 全 <0x1d448; Seg-2 起点 0x1d448 确认 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | OK | Block A ROM_INCBIN 0x1d024/0x1c + Block B .byte 0x1d0bc 16B -> §5.1 登记 |
| C3 Rule3 | §5.1 块确 0 引用 | **PASS** | 独立重跑 ref-scan 见下 §一 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | OK | 15 个 EQ 槽全部 ROM 验证通过 (详见 §二) |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | **FAIL** | `STEP_ADVANCE_MASK=0xffc03fff` 已有 `NAME_INPUT_PAGE_STATE_CLEAR` (name_input.inc:28), 应复用 (详见 §三) |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | OK | 全部 27 个槽 label + 4 carve label 符合规范, 无重复 |
| C7 R3 接通 | carve 全局槽有 USER-label + DATA-ref 计划 | OK | vija_bg_fs_path_pair / vija_obj_slot_seq 均有 label + 对应 REF_SLOTS 接通 |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_ | **FAIL** | 2 处现存 plate 含 FUN_ 未在提案 PLATE 节标注修复 (详见 §四) |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | OK | decode_card_image_6bpp ASCII 替换文本已确认纯 ASCII; 其余 7 函数 plate 均纯 ASCII |
| C10 carve | 指针表条目 `+1` (THUMB fn-ptr) | N/A | 段内无 THUMB fn-ptr carve 指针表; 0x1d044 jump table 是 raw-addr ARM dispatch, 不适用 +1 规则 |
| C11 误名 | 函数名与体一致, 无 FUNC_RENAME 遗漏 | OK | 抽查 run_vija_scene_state_machine / tick_scene_step_by_step_table_b/c, 均与体匹配 |
| C12 R6 | 关键槽有 file:line + 置信度证据, 无零容忍词 | OK | 消费者证据表 8 条均给 file:line + confidence, 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽被覆盖无遗漏 | OK | 段内 26 个自动名 (25 DAT_/DWORD_ + DAT_d0bc) 全部覆盖: EQ=15, REF=3, RENAME=5, gPrng已命名=2, §5.1=1 |

**状态: NEEDS_FIX (2 items)**

---

## §一: C3 独立 ref-scan 结果

```
Block A 入口 0x0801d024: raw=0, THUMB+1(0x0801d025)=0
Block B handlers:
  0x0801d0bc raw=3 -> 全部在 jump table 0x1d044..0x1d0bb 内 (内部自引, 非外部 ref)
  0x0801d0c0 raw=2 -> 全部在 jump table 内
  0x0801d0c4 raw=25 -> 全部在 jump table 内
```

验证方法: `d.count(struct.pack('<I', addr))` 对每个值; 并对所有命中偏移检查是否在 0x1d044..0x1d0bb 范围内。

结论: Block A 入口 0 外部引用 (raw+thumb 全 0) 确认; Block B 的 3 个 handler 地址仅被 jump table 内部条目引用, 无外部引用。前函数 0x1d022 为 `bx r1` (ROM bytes `08 47`), 非 fall-through 可达。§5.1 判定 CORRECT。

---

## §二: C4 ROM 字节核对

全部 15 个 EQ 槽 + 5 个 RENAME 槽通过 ROM 字节核对:

```
EQ:
  0x0801cb1c -> 0x02029eb0 (gVijaState)             OK
  0x0801cbf8 -> 0x080000ae (ROM_REGION_CODE_ADDR)    OK
  0x0801cbfc -> 0x02000000 (EWRAM_BASE)              OK
  0x0801cc00 -> 0x00006c2c (GSETTINGS_OFFSET)        OK
  0x0801cc04 -> 0xffffe0ff (DEMO_CLEAR_BITS_12_8)    OK
  0x0801cd9c -> 0xffffe0ff                           OK
  0x0801ce3c -> 0xffffe0ff                           OK
  0x0801cf08 -> 0xffffe0ff                           OK
  0x0801cfc0 -> 0xffc03fff                           OK
  0x0801d018 -> 0xffc03fff                           OK
  0x0801d158 -> 0x06004000 (BG_CHAR_VRAM_CB2)        OK
  0x0801d424 -> 0x080000ae                           OK
  0x0801d428 -> 0x02000000                           OK
  0x0801d42c -> 0x00006c2c                           OK
  0x0801d438 -> 0x06004000                           OK
RENAME:
  0x0801cfb8 -> 0x09e589b4 (step_table_b)            OK
  0x0801d010 -> 0x09e589b4 (step_table_c)            OK
  0x0801d43c -> 0x0000031f                           OK
  0x0801d440 -> 0x00003f3f                           OK
  0x0801d444 -> 0x00000c7f                           OK
```

---

## §三: C5 STEP_ADVANCE_MASK 重复常量

`name_input.inc:28`:
```
.equ NAME_INPUT_PAGE_STATE_CLEAR, 0xffc03fff
@ bits[21:14] clear mask for page_state field @ gPrng+0x204
```

提案新建 `STEP_ADVANCE_MASK=0xffc03fff` 的注释:
```
@ clear bits[21:14] of gPrng+0x204 step-index bitfield
```

两者: 值完全相同 (0xffc03fff), 语义完全相同 (clear bits[21:14] of gPrng+0x204)。提案的
"existing scan: grep of all constants/*.inc for 0xffc03fff -> no match" **错误** (name_input.inc:28
有此值)。应复用 `NAME_INPUT_PAGE_STATE_CLEAR`, 与 Seg-10 同模式 (内存 `refine-batch-scope-conventions`)。

---

## §四: C8 plate 中残留 FUN_ 未修复

提案 PLATE 节仅修复 `decode_card_image_6bpp` 的 CJK 行 (asm line 963), 但段内另有 2 处
现有 plate 引用了 FUN_ 旧名:

1. **asm line 708** (write_tile_attr_byte_to_vram plate):
   ```
   @ Called by FUN_0801d174 in inner loop ...
   ```
   FUN_0801d174 = `write_tile_attr_strip_4wide` (asm line 812, addr 0x0801d174, 属 Seg-1 内命名函数)。
   应改为: `@ Called by write_tile_attr_strip_4wide in inner loop ...`

2. **asm line 787** (copy_palette_bank_by_slot plate):
   ```
   @ Called by FUN_0801d208 (tile map update function).
   ```
   FUN_0801d208 = `apply_palette_and_tile_attr_strips` (asm line 898, addr 0x0801d208, 属 Seg-1 内命名函数)。
   应改为: `@ Called by apply_palette_and_tile_attr_strips ...`

提案 PLATE 节未列出这两处修复 -> C8 FAIL。

---

## §五: carve 覆盖等式验证

host incbin: `.incbin "roms/2343.gba", 0x1E3D9CF, 0xC33D`

```
span 1: .incbin 0x1E3D9CF, 5           ->  5B  (pre-pad, bytes 00 01 02 01 00)
span 2: .asciz "demo/vija/BG1_all.LZ5bg"    -> 24B  (23 chars + NUL, ends 0x1E3D9EC)
span 3: .asciz "demo/vija/BG1_all_US.LZ5bg" -> 27B  (26 chars + NUL, ends 0x1E3DA07)
span 4: .byte 0x0                       ->  1B  (align pad, 0x1E3DA07->0x1E3DA08)
span 5: vija_bg_fs_path_pair 2x.word   ->  8B  (ptrs 0x09E3D9D4/0x09E3D9EC, ROM verified)
span 6: vija_obj_slot_seq .byte x5+pad ->  8B  (01 03 00 02 04 00 00 00, ROM verified)
span 7: .incbin 0x1E3DA18, 0xC2F4      -> 0xC2F4B
----
total: 5+24+27+1+8+8+0xC2F4 = 0xC33D  MATCH
```

span7 end: 0x1E3DA18 + 0xC2F4 = 0x1E49D0C = 0x1E3D9CF + 0xC33D  VERIFIED.

GBA addr 解析: JP ptr = 0x09E3D9D4 (ROM 0x1E3D9D4) = EWRAM_BASE_GBA + str1_off 正确;
US ptr = 0x09E3D9EC 正确。

注: 提案在 span 3 写 "27B + 1B NUL pad = 28B" 是将 .asciz NUL 和对齐 pad 合并计数,
实际 .asciz 自带 NUL (27B), 再加 .byte 0x0 (1B) = 28B, 结果等价, byte-identical 正确。

---

## §六: 提案内部不一致 (非 C1-C13 违规, 供 fixer 参考)

提案 `## disasm 计划 (R4)` 节仍保留了对 0x1d024 块的 disasm 计划 (含 dispatch_tile_attr_op_by_index
命名草案), 但 `## Executor Report` 末行写 "disasm=2 blocks, §5.1=0", 与 driver 订正后的
`## §5.1 登記` 节 (disasm=0, §5.1=1 cluster) 矛盾。

Fixer 应以 `## §5.1 登記` 节 + driver 订正为准 (§5.1, 不 disasm, 保 ROM_INCBIN/.byte 原样),
`## disasm 计划` 节内容为过期草案, 不执行。

---

## 修改清单 (NEEDS_FIX)

### #1 — C5 — 复用 NAME_INPUT_PAGE_STATE_CLEAR 替代新建 STEP_ADVANCE_MASK

- 位置: EQ_SLOTS 表第 9/10 行 (DWORD_0801cfc0 / DWORD_0801d018) + 新增 constants 节
- 具体改动:
  - EQ_SLOTS 表 `const_name` 列: `STEP_ADVANCE_MASK` -> `NAME_INPUT_PAGE_STATE_CLEAR`
  - EQ_SLOTS 表 `source` 列: "新建 (vija.inc 或 demo_state.inc)" -> "复用 name_input.inc:28"
  - 删除 `## 新增 constants / 全局` 下的 `### STEP_ADVANCE_MASK` 小节
  - slot_label 保持不变 (tick_scene_step_by_step_table_b_step_advance_mask 等可保留语义命名)
- 根据: name_input.inc:28 `.equ NAME_INPUT_PAGE_STATE_CLEAR, 0xffc03fff` 同值同语义;
  提案 "existing scan" 结论有误

### #2 — C8 — PLATE 节增加 2 处 FUN_ 现名替换

- 位置: 提案 `### PLATE (R5)` 节末尾补充
- 具体改动: 在 PLATE 节追加:
  ```
  - write_tile_attr_byte_to_vram (asm line 708): "FUN_0801d174" -> "write_tile_attr_strip_4wide"
    Full: @ Called by write_tile_attr_strip_4wide in inner loop for each of 4 sub-elements ...
  - copy_palette_bank_by_slot (asm line 787): "FUN_0801d208" -> "apply_palette_and_tile_attr_strips"
    Full: @ Called by apply_palette_and_tile_attr_strips (tile map update function). ...
  ```
- 根据: FUN_0801d174 = write_tile_attr_strip_4wide (asm:812, push @ 0801d174);
  FUN_0801d208 = apply_palette_and_tile_attr_strips (asm:898, push @ 0801d208);
  均属 Seg-1 内命名函数, R5 要求 plate 用现名

---

## 状态: NEEDS_FIX (2 items)
