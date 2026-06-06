# Refine Review: Seg-5d

ROM 0x080171ec..0x0801794c, file asm/00_system_str_vija.s ~L8181..L9197
Review date: 2026-06-07

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | refine-progress.md Seg-5d: 0x171ec..0x1794c 与 proposal 完全吻合 |
| C2 Rule2 | ROM_INCBIN 块全有归宿 | PASS | 1 个 ROM_INCBIN 0x17424/0x40 -> §5.1 登记 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立重跑 ref-scan: 16 对齐子地址全为 raw=0/thumb=0 |
| C4 R1 值 | EQ value == ROM 4B LE | PASS | 17 个 slot 逐一 python 核对, 全部匹配 |
| C5 R1 复用 | 新建 constants 无可复用冲突 | **FAIL** | OAM_ATTR2_PALETTE_CLEAR_MASK=0xffffc07f 与 GFX_ATTR_CLEAR_BITS_13_7=0xffffc07f (gfx_resource.inc) 同值; 应复用, 不应新建 |
| C6 R2 名 | 槽名格式合规, 无碰撞 | PASS | 所有 label 满足 ^[a-z][a-z0-9_]+$, 含后缀 _b/_c 区分同值多引用 |
| C7 R3 接通 | carve label 有 USER-label + DATA-ref | PASS | char_frame_decode_lut / sprite_gfx_type_meta / sprite_palette_type_table 均有 REF_SLOT 计划 |
| C8 R5 现名 | plate 无残留 FUN_ | PASS | 4 处 FUN_ 替换均有对应现名: validate_complement_checksum/compute_floor_log2/unpack_bits_to_byte_buf/pack_bytes_to_vram_bits |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | 独立检查所有 EOL 文本, 无 CJK 字符 |
| C10 carve | DATA 表无误加 +1 | PASS | 两个 carve 均为 DATA 表 (非 fn 指针); raw ref 均 1 次, THUMB ref 均 0; 无 +1 |
| C11 误名 | 无遗漏 FUNC_RENAME | PASS | 4 函数名目视检查与函数体一致; 无矛盾信号 |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | gState/gFontJpCtx/carve tables 均有 file:line 证据 + high 置信度 |
| C13 残留 | 段内全部自动名槽覆盖 | PASS | 12 DWORD_ + 22 DAT_ = 34 槽全在 proposal 计划内; 无遗漏 |

---

## 独立 ref-scan 复核结果

### §5.1: ROM_INCBIN 0x17424/0x40

扫描 16 个 4B 对齐子地址 (0x08017424..0x08017460, 步长 4):

```
全部 raw=0, thumb=0 -> §5.1 CONFIRMED
```

executor 结论属实, 无需 carve 或 disasm。

### carve 引用验证

| 表 | ROM addr | raw refs | thumb refs |
|---|---|---|---|
| char_frame_decode_lut | 0x09e3a660 | 1 | 0 |
| sprite_gfx_type_meta | 0x09e3afc8 | 1 | 0 |
| sprite_palette_type_table | 0x09e3afd8 | 1 | 0 |

均为 DATA 引用 (raw=1, thumb=0), 无需 +1。

---

## carve 覆盖核对 (字节级)

### Carve 1: char_frame_decode_lut @ 0x09e3a660/0x110

原 incbin: `.incbin "roms/2343.gba", 0x1E3A65E, 0x112`

拆分: 0x2 (align pad) + 0x110 (LUT body) = 0x112 == 原大小. PASS

file_off 核对: 0x1E3A65E + 0x2 = 0x1E3A660, ROM addr = 0x09e3a660. 与 DWORD_08017410=0x09e3a660 吻合. PASS

LUT .word 值: ROM @0x1E3A660 开头已独立读取, 与 proposal 拆分计划一致 (原 incbin 内容保持不变). PASS

### Carve 2: sprite_gfx_type_meta+sprite_palette_type_table @ 0x09e3afc8/20B

原 incbin: `.incbin "roms/2343.gba", 0x1E3A78D, 0xB2B`

拆分: 0x83B (prefix) + 0x10 (4 words) + 0x4 (4 bytes) + 0x2DC (suffix) = 0xB2B == 原大小. PASS

- sprite_gfx_type_meta: 0x1E3A78D + 0x83B = 0x1E3AFC8, ROM addr = 0x09e3afc8. 吻合. PASS
- sprite_palette_type_table: 0x1E3AFC8 + 0x10 = 0x1E3AFD8, ROM addr = 0x09e3afd8. 吻合. PASS
- suffix end: 0x1E3AFD8 + 0x4 + 0x2DC = 0x1E3B2B8 = 0x1E3A78D + 0xB2B. PASS

.word 值字节核对 (python 实测):
```
word[0] @ 0x1e3afc8 = 0x031e0000  (proposal: 0x031e0000) PASS
word[1] @ 0x1e3afcc = 0x061e0300  (proposal: 0x061e0300) PASS
word[2] @ 0x1e3afd0 = 0x081e0600  (proposal: 0x081e0600) PASS
word[3] @ 0x1e3afd4 = 0x0a1e0800  (proposal: 0x0a1e0800) PASS
```

.byte 值字节核对:
```
bytes @ 0x1e3afd8 = [1, 1, 16, 16]  (proposal: [1, 1, 16, 16]) PASS
```

---

## 状态: NEEDS_FIX

---

## 修改清单 (1 项)

### #1 — C5 — DAT_08017784 slot: 复用已有常量, 不新建 OAM_ATTR2_PALETTE_CLEAR_MASK

**问题**: proposal 计划在 `constants/oam_attr.inc` 新建:
```
.equ OAM_ATTR2_PALETTE_CLEAR_MASK, 0xffffc07f
```
但 `constants/gfx_resource.inc` 已有:
```
.equ GFX_ATTR_CLEAR_BITS_13_7, 0xffffc07f  @ clear attr bits[13:7] (tile/screen-map field)
```
两者值相同 (0xffffc07f = ~0x00003f80 = bits[13:7] mask)。C5 规则要求 "新建 constants 前确无现有可复用"。

**正确做法**: slot label `apply_sprite_gfx_by_type_oam_pal_mask` 应指向 `GFX_ATTR_CLEAR_BITS_13_7` (来自 gfx_resource.inc), 不新建 `OAM_ATTR2_PALETTE_CLEAR_MASK`。

**修改**:
1. 从 `oam_attr.inc` 新增计划中删除 `OAM_ATTR2_PALETTE_CLEAR_MASK`。
2. 将 DAT_08017784 的 EQ 行改为 `GFX_ATTR_CLEAR_BITS_13_7` (gfx_resource.inc), 或标注为 REF/复用。
3. slot_label 保持 `apply_sprite_gfx_by_type_oam_pal_mask`, const_name 改为 `GFX_ATTR_CLEAR_BITS_13_7`, inc 文件改为 `gfx_resource.inc` (已存在, 无需追加)。

**影响范围**: 仅 proposal 中 EQ_SLOTS 表的一行 + "新增 constants/oam_attr.inc 追加" 节。代码侧改名 slot_label 不变, 只是 const_name 来源不同。

---

## 备注

- decode_char_frame_to_vram 确认 0 ROM refs (raw=0, thumb=0), 是完全的孤儿函数。DWORD_0801740c=0x201 的 RENAME_SLOT 处理 (factual EOL, 无语义主张) 符合规则。
- DWORD_08017420=0x3e9c (vram_step) 标为 med-conf 是恰当的——函数是孤儿且 vram step 语义来自上下文推断。
- gState=0x02029250 (raw=37), gFontJpCtx=0x02006ed0 (raw=202), EWRAM_BASE=0x02000000 (raw=4295) 引用计数与 proposal 声明一致, 均为高引用全局, 值得命名。
- GSETTINGS_OFFSET=0x6c2c 核算: 0x02006c2c (ewram.inc gSettings) - 0x02000000 (EWRAM_BASE) = 0x6c2c. 正确。
- OAM_ATTR0_HIDDEN=0x0000ffff: oam_attr.inc 中无此值, 是新建, C5 PASS。
- 全部 34 个段内自动名槽均有覆盖计划 (C13 PASS)。
- 边界函数 load_game_str_1006_to_state 的 4 个槽 (0x08017990/994/9c/a0) 在 Seg-6 地址范围内, proposal 附带处理无违规 (共享常量 gState/EWRAM_BASE 已被同段 load_game_str_pair_1004_to_state 驱动定义)。
