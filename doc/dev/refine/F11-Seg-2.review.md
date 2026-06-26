# Refine Review: F11-Seg-2

## 段信息

- 范围: `[0x08085d4c, 0x08086cdc)`, 4,752 bytes
- 模块: `asm/11_effect_slot_puzzletext.s`, lines 1757..3510
- ROM_INCBIN: 1 块 (0x861a0/0x27a)
- 函数: 12 个

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | §五 Seg-2 = `[0x8085d4c, 0x8086cdc)` 完全匹配 |
| C2 | 每个 ROM_INCBIN 块都有归宿 | ✅ | 唯一块 0x861a0/0x27a -> R4 DISASM 计划 |
| C3 | §5.1 块确 0 引用 | ✅ (N/A) | 本段无 §5.1 条目; 该块有 7 个真实 word-aligned raw 引用 |
| C4 | EQ value == ROM 4 字节小端 | ✅ | 独立 python 验证全 13 个抽样槽 (见下) |
| C5 | 新建 constants 无现有可复用 | ❌ | **0x1d68 已存在 `ELIGIB_SPRITE_CTRL_OFF`** (见 #1) |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | 全部函数名/标签/sub-case label 合规; constants 按 UPPER_CASE 惯例 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | 4 个 REF_SLOTS 均有 gas_label + slot_label 计划; 值已 ROM 验证 |
| C8 | plate 引用全用现名, 无残留 FUN_ | ❌ | **`FUN_080a0a8c` 在 dispatch_equip_slot_state_by_index plate 未修** (见 #2) |
| C9 | 所有 plate/EOL 文本纯 ASCII | ✅ | `python -c "...非 ASCII 字节"` 返回空 -- 全 ASCII |
| C10 | 指针表条目 raw (非 THUMB+1); `.word <fn>` == ROM raw 值 | ✅ | 跳转表 11 entries 全为 raw 偶地址; `mov pc,r0` 机制确认; ROM 解码完全匹配提案 |
| C11 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | ✅ | 无误名信号; 12 个函数名与函数体操作一致 |
| C12 | 关键槽语义有 file:line + 置信度证据 | ✅ | 8 个关键槽均有 asm/11 行号 + card-stats.s 行号证据; high confidence |
| C13 | 段内所有残留自动名槽 100% 覆盖 | ❌ | **2 个槽遗漏: `DAT_08086c34`, `DAT_08086c6c`** (见 #3) |

## 独立复核记录

### ref-scan 重跑 (C3)

```
python -c "import struct; rom = open('roms/2343.gba','rb').read(); ..."
```

**Raw refs: 11 total**
- word-aligned (真实跳转表): src=0x08086174->0x080861a0 [0], 0x08086178->0x0808621c [1], 0x08086188->0x0808621c [5], 0x0808617c->0x080862ec [2], 0x08086180->0x08086338 [3], 0x08086184->0x08086370 [4], 0x0808619c->0x080863cc [10] -- 7 real refs, 全来自 PTR_DAT_08086174
- 非 word-aligned (compressed data): 0x087a1ee9, 0x08b69a5b, 0x084eed45 -- 3 个 NOT real
- word-aligned but high-entropy (0x089d076c->0x0808625c): 上下文 `71965965 4825cbdf 9b7eb195 71aa0555 0808625c 825aa582 20820820` -- NOT real (compressed data pattern)

**THUMB+1 refs: 4 total**
- 非 word-aligned source: 0x08937339, 0x08f9552d, 0x08a1718d -- NOT real
- word-aligned source: 0x08d79908->0x0808634d; 上下文 `12e48b2a b3128508 0808634d d74dc682 b317d359 ebaed744` -- high-entropy compressed data, NOT real

**结论: 0 valid THUMB+1 refs, 7 valid raw refs (全部来自跳转表).**  
**块判定正确: R4 DISASM (sub-case labels, NOT createFunction).**

### 跳转表 ROM 解码验证 (C10)

11 entries 0x08086174..0x08086198:
```
[0]=0x080861a0 [1]=0x0808621c [2]=0x080862ec [3]=0x08086338
[4]=0x08086370 [5]=0x0808621c [6..9]=0x0808641a(fallback) [10]=0x080863cc
```
block_end = 0x080861a0 + 0x27a = 0x0808641a = fallback target 精确对齐. 6 distinct in-block case bodies. 提案描述完全正确.

### ROM 字节核对 (C4)

全部 13 个抽样槽与 ROM 字节一致:
- 0x0808616c EQUIP_SLOT_SUBSTATE_OFF=0x0000058c OK
- 0x08086448 gEquipEffectZoneTable=0x09e5a0c4 OK
- 0x0808645c CONTRACT_WITH_ABYSS_CID=0x00001698 OK
- 0x08086798 EARTH_CHANT_CID=0x00001716 OK
- 0x080867b8 END_OF_WORLD_CID=0x000019d9 OK
- 0x08085d74 gDuelPhaseFlags=0x0201b290 OK
- 0x08085d78 FIELD_DISPLAY_TYPE_OFF=0x0000057c OK
- 0x08085ea4 ELIGIB_RESULT_OFF=0x00000584 OK
- 0x08086064 ELIGIB_ANIM_STATE_OFF=0x00001d6c OK
- 0x08086080 ELIGIB_CARD_ID_OFF=0x00001d44 OK
- 0x08086c34 (missed slot) =0x00000868 OK
- 0x08086c6c (missed slot) =0x09e5a0c4 OK
- 0x080863f8 (求助 offset) =0x00001d68 OK -- 已存在 ELIGIB_SPRITE_CTRL_OFF

### C5 dedup 验证

5 个 NEW constants 对 value grep constants/*.inc:
- 0x0000058c (EQUIP_SLOT_SUBSTATE_OFF): 0 hits OK -> NEW
- 0x09e5a0c4 (gEquipEffectZoneTable): 0 hits OK -> NEW
- 0x00001698 (CONTRACT_WITH_ABYSS_CID): 0 hits OK -> NEW; card-stats.s L17957 confirmed
- 0x00001716 (EARTH_CHANT_CID): 0 hits OK -> NEW; card-stats.s L19335 confirmed
- 0x000019d9 (END_OF_WORLD_CID): 0 hits OK -> NEW; card-stats.s L26795 confirmed

**BUT** 0x00001d68 (求助 slot 0x080863f8):
```
grep "0x1d68" constants/ewram.inc
-> .equ ELIGIB_SPRITE_CTRL_OFF, 0x00001d68  @ [gP1LifePoints+0x1d68] sprite display control; ...
```
已存在. 提案未 grep 到是因为只搜了 new constants 而未对 0x1d68 执行 C5 检查.

### C13 精确计数

`grep -E "^DAT_|^DWORD_|^PTR_" asm/11 lines 1757..3510` 返回 **92** 个定义.  
提案称 "91 unique slot labels" -- 少 1 (计数误差).  
提案 EQ(77) + REF(4) + RENAME(8) + DISASM(1 ROM_INCBIN label) = 90, 缺 2 个槽.

实际未覆盖: `DAT_08086c34` (addr=0x08086c34, value=0x00000868) 和 `DAT_08086c6c` (addr=0x08086c6c, value=0x09e5a0c4), 均属 `eval_equip_zone_activation_eligible` 尾部 literal pool (L3401/L3416 in asm/11).

### 求助项独立解析

提案将 0x080863f8 处 value=0x1d68 标为 BLOCKED. 独立复核:

1. `constants/ewram.inc` L422: `.equ ELIGIB_SPRITE_CTRL_OFF, 0x00001d68` 已存在.
2. `asm/12_equip_activation_scan.s` L3440 (`init_equip_card_sprite_row_entry` plate): "Reads player_bit from [gP1LifePoints+**0x1d68**]" -- 语义已知.
3. `asm/12` L3654: "gP1LifePoints state words at offsets **0x1d68**, 0x1d6c, 0x1d70; uses first as main param"
4. 多个 asm/12 函数用 SLOT_PARAM_OFFSET=0x1d68 (L3659).

**结论: NOT BLOCKED. 正确行动 = EQ REUSE ELIGIB_SPRITE_CTRL_OFF (ewram.inc L422), conf=high.**  
提案错误: 将已知常量标 BLOCKED 且未作为 C5 项检查.

### 跨文件 plate (C8 补充)

提案的 11 个 plate 更新中, 段内 6 个覆盖了所有段内 FUN_ (FUN_08086a80 x2, FUN_08086634 x2, FUN_08086c80 x3, FUN_080869a8 x1, 共 6 处); 跨文件 5 个 (asm/11 L18359, asm/12 L3440/3569/3693/3867) 覆盖了 FUN_08085d4c.

**但遗漏**: asm/11 L2213 (`dispatch_equip_slot_state_by_index` plate) 含 `FUN_080a0a8c`, 对应 `asm/13_equip_placement.s` 的 `route_equip_slot_tick_by_flag`. 这是段内函数的 plate, C8 要求修复.

## 状态: NEEDS_FIX (3 items)

## 修改清单 (逐条可执行)

### #1 -- C5 -- 0x080863f8 处 value=0x1d68 改 REUSE ELIGIB_SPRITE_CTRL_OFF

**位置**: 提案 disasm 计划节, 最后一条 literal pool 条目 (`0x080863f8: 0x00001d68`); 以及 "求助" 节.

**错误**: 提案将此值标为 BLOCKED/未知, 未执行 C5 value-grep.

**修正**: 
- 将 0x080863f8 处 literal pool 条目改为:
  `0x080863f8: 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF -- REUSE ewram.inc L422; [gP1LifePoints+0x1d68] sprite display control)`
- 删除 "求助" 节中 `ELIGIB_ANIM_BASE_OFF=0x1d68` 的 NEW 常量候选
- 删除 "可能追加常量" 中 `ELIGIB_ANIM_BASE_OFF=0x1d68` 条目 (med conf/BLOCKED 均无效)
- 在 disasm 执行脚本中, 对 0x080863f8 处 DWord 加 equate ELIGIB_SPRITE_CTRL_OFF (与同块其他 ewram.inc 常量一致)

### #2 -- C8 -- FUN_080a0a8c 在 dispatch_equip_slot_state_by_index plate 未修

**位置**: asm/11 lines 2213 (`dispatch_equip_slot_state_by_index` plate comment 第一行).

**原文**: `Called by FUN_080a0a8c (equip slot flag router) when bit4 check passes and bit2 sub-branch hits.`

**修正**: 将 `FUN_080a0a8c` -> `route_equip_slot_tick_by_flag`  
(确认: `asm/13_equip_placement.s` L6781: `route_equip_slot_tick_by_flag:` push {r4,r5,lr} @ 080a0a8c)

在提案 PLATE 节追加第 7 条:
```
| 0x0808611c (dispatch_equip_slot_state_by_index) plate line 2213 | FUN_080a0a8c | route_equip_slot_tick_by_flag |
```

### #3 -- C13 -- DAT_08086c34 和 DAT_08086c6c 遗漏

**位置**: `eval_equip_zone_activation_eligible` (0x08086a80) 尾部 literal pool.

**遗漏槽**:
- `DAT_08086c34` @ 0x08086c34: ROM 值 = 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc) -> REUSE
- `DAT_08086c6c` @ 0x08086c6c: ROM 值 = 0x09e5a0c4 = gEquipEffectZoneTable (新建, 同本段其他用途) -> REUSE (same new constant)

**修正**: 在提案 `eval_equip_zone_activation_eligible` EQ 表末尾追加两行:
```
| DAT_08086c34 @ 0x08086c34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | REUSE |
| DAT_08086c6c @ 0x08086c6c | 0x09e5a0c4 | gEquipEffectZoneTable | new | REUSE |
```
同时将 "残留自动名槽 x91 total" 改为 "x92 total".  
EQ 总数从 77 改为 79 (加上 #1 中 0x1d68 从 BLOCKED 改 REUSE 计入 EQ: 实际 EQ 总数 = 79 + disasm-block EQ 若干).
