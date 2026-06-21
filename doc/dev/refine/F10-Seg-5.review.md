# Refine Review: F10-Seg-5a

Reviewer: independent (not executor). ROM `E:/Workspace/yugioh-ex2006-re/roms/2343.gba`.
All ref-scans and byte checks run independently via Python.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | Seg-5a [0x7db20..0x7ec10) 与 roadmap 一致; Seg-4 终止 0x7db20, Seg-5a 紧接; Seg-5b 延续 0x7ec10 |
| C2 Rule2 | ✅ | 6 ROM_INCBIN 全部有归宿 (BLK1/4 THUMB+1 R4 disasm; BLK2/3/5 raw-ref R4 disasm; BLK6 5×THUMB+1 R4 disasm×5); 无静默保留 |
| C3 Rule3 | ✅ | 无 §5.1 块; 所有 6 BLK 各有 ≥1 真实引用, 独立 ref-scan 确认 |
| C4 R1 值 | ✅ | 8 个 EQ 槽 ROM 字节全部匹配 (独立 python 核对见下方) |
| C5 R1 复用 | ✅ REUSE + ⚠️ NEW | 6 REUSE 均有 grep 命中; 6 NEW 在 constants/*.inc 均 0 命中; 但见 #1 (invoke_effect_node_active_fn_ptr 命名有 -ptr 歧义) |
| C6 R2 名 | ✅ | 所有 7 fn_eligible/31 disasm fn 命名符合 `^[a-z][a-z0-9_]+$`; 无碰撞 |
| C7 R3 接通 | ✅ | 7 REF 槽均有对应 ewram.inc 全局符号; DATA-ref 计划明确 |
| C8 R5 现名 | ✅ | 独立 grep `FUN_` 在 lines 8281..8877: 0 命中; PLATE=0 无残留 FUN_ |
| C9 ASCII | ✅ | PLATE=0; proposal 文本无 CJK; EOL 均 ASCII |
| C10 carve | ✅ | carve=0; 不适用 |
| C11 误名 | ✅ | 6 具名函数体逻辑与函数名一致; FUNC_RENAME=0 正确 |
| C12 R6 | ✅ | 6 关键槽均有 file:line 消费者证据 + high 置信度; 无零容忍词 |
| C13 残留 | ❌ | `DWORD_0807dd5c` 在 proposal 中被列为 "PTR_NAMED already" 跳过, 但 asm 内标签为 DWORD_ (非 PTR_gP1LifePoints_), 未纳入 RENAME_SLOTS; 见修改清单 #2 |

---

## 独立 ref-scan 结果 (Python 重跑)

```
BLK1 @0x7dd68/0x30: raw=0, thumb+1=1   (FS entry fn_eligible CID=0x198d Magical Mallet)
BLK2 @0x7ddac/0x16c: raw=1, thumb+1=0  (jump table .word @ 0x7dd98)
BLK3 @0x7df90/0x2bc: raw=1, thumb+1=0  (jump table PTR_DAT_0807df1c)
BLK4 @0x7e398/0x2c: raw=0, thumb+1=1   (FS entry fn_eligible CID=0x19ae Ancient Gear Drill)
BLK5 @0x7e438/0x16c: raw=1, thumb+1=0  (jump table .word @ 0x7e3c4)
BLK6 @0x7e5d4/0x63c: raw=0, thumb+1=1  (only 0x7e5d4 start has 1 FS ref; 5 stubs each ref'd separately)
```

### BLK6 细节

独立 2B-step 扫描: BLK6 内部共 9 个 THUMB+1 ref (各地址独立计数):

| 地址 | ref ROM offset | 类型 | 判定 |
|------|---------------|------|------|
| 0x7e5d4 | 0x1e45458 (0x9e45458) | FS table entry[+4], CID=0x19bf | REAL |
| 0x7e6dc | 0x433407 (0x8433407) | 代码段, mod4=3 **未对齐** | false positive |
| 0x7e6e0 | 0x1e45470 (0x9e45470) | FS table entry[+4], CID=0x19c0 | REAL |
| 0x7e7c4 | 0x2abd08 (0x82abd08) | 代码/data 区, 对齐但指向 stub-2 内部 (+0xe4), 无 push | false positive (code-literal coincidence) |
| 0x7e7e4 | 0x1e45488 (0x9e45488) | FS table entry[+4], CID=0x19c2 | REAL |
| 0x7e960 | 0x1e45530 (0x9e45530) | FS table entry[+4], CID=0x19d0 | REAL |
| 0x7e9f8 | 0x1e45548 (0x9e45548) | FS table entry[+4], CID=0x19d3 | REAL |
| 0x7eaea | 0x13d5e6 (0x813d5e6) | 代码段, mod4=2 **未对齐** | false positive |
| 0x7ec06 | 0x1833327 (0x9833327) | FS 区, mod4=3 **未对齐** | false positive |

**5 个 REAL THUMB+1 = 5 个 FS entry[+4] (fn_eligible 槽), 每个 CID 唯一**, 确认 BLK6 = 5 独立 fn_eligible stubs; 4 个 false positive 均为字节巧合 (未对齐或 stub 中段).

### BLK6 stub 覆盖

push `0xb5f0` 扫描 + return `0x47xx` 分析:

| stub | 起止 | 大小 | CID | 名称 |
|------|------|------|-----|------|
| 1 | 0x7e5d4..0x7e6df | 268B | 0x19bf | fn_eligible_bes_covered_core |
| 2 | 0x7e6e0..0x7e7e3 | 260B | 0x19c0 | fn_eligible_dd_guide |
| 3 | 0x7e7e4..0x7e95f | 380B | 0x19c2 | fn_eligible_disciple_forbidden_spell |
| 4 | 0x7e960..0x7e9f7 | 152B | 0x19d0 | fn_eligible_malice_ascendant |
| 5 | 0x7e9f8..0x7ec0f | 536B | 0x19d3 | fn_eligible_divine_dragon_excelion |
| **总计** | | **1596B = 0x63c** | | 全覆盖, 无残余 |

BLK6 末 2 字节 0x7ec0e-0x7ec0f: `00 00` (.zero 2), 0x7ec10 起: `70 b5` (下一函数 push). 边界精确.

**注**: 提案 ref-scan 表格写 "BLK6: raw=0, thumb+1=5" 是对 BLK6 起始地址 (0x7e5d4) 单点扫描 thumb+1=1 的**误记** (正确应为 1); "5" 是 5 个子 stub 各有 1 ref 的总和描述, 数字本身正确但不是 count 命令的输出. 此为文档表述问题, 不影响判断逻辑.

---

## EQ 槽 ROM 字节核对

| 槽地址 | 期望值 | ROM 实际 | 结果 |
|--------|--------|---------|------|
| 0x7dc9c | 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF) | 0x00001d68 | ✅ |
| 0x7dcd4 | 0x000014c4 (FREED_THE_MATCHLESS_GENERAL_CID) | 0x000014c4 | ✅ |
| 0x7dd60 | 0x000010d0 (LP_ACTIVATION_LINK_FLAG_OFF) | 0x000010d0 | ✅ |
| 0x7e2f0 | 0x000004a4 (EQUIP_PHASE_FRAME_OFF) | 0x000004a4 | ✅ |
| 0x7e38c | 0x00000868 (PLAYER_BLOCK_STRIDE) | 0x00000868 | ✅ |
| 0x7e394 | 0x000004a4 (EQUIP_PHASE_FRAME_OFF dup) | 0x000004a4 | ✅ |
| 0x7dc04 | 0x000010d3 (TRIGGER_OP_PARAM_10D3) | 0x000010d3 | ✅ |
| 0x7dc08 | 0x08090625 (invoke_effect_node_active_fn_ptr) | 0x08090625 | ✅ |

---

## CID 及 fn-ptr 核对

| 常量 | 值 | card-stats.s | 结果 |
|------|-----|-------------|------|
| BES_COVERED_CORE_CID | 0x19bf | card_2034 slot=0x19BF pw=15317640 | ✅ |
| DD_GUIDE_CID | 0x19c0 | card_2035 slot=0x19C0 pw=52702748 | ✅ |
| DISCIPLE_FORBIDDEN_SPELL_CID | 0x19c2 | card_2037 slot=0x19C2 pw=15595052 | ✅ |
| MALICE_ASCENDANT_CID | 0x19d0 | card_2051 slot=0x19D0 (REUSE, card_info.inc:1337) | ✅ |
| DIVINE_DRAGON_EXCELION_CID | 0x19d3 | card_2054 slot=0x19D3 pw=10032958 | ✅ |
| invoke_effect_node_active_fn_ptr | 0x08090625 | ROM @ 0x8090624: `70 b5 04 1c` (THUMB push, fn in asm/11) | ✅ |

---

## BLK3 跳转表条目数修正

提案说 "28 entries". ROM 直读: 0x7df1c..0x7df8c 共 **29 entries** (状态 0..0x1c = 29 个). 最后一条 entry[28] @ 0x7df8c = 0x0807df90 指向 BLK3 起始. 提案计数偏低 1, 是文档问题但不影响分类正确性 (BLK3 仍为 R4 disasm).

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单 (NEEDS_FIX 必填)

### #1 — C5/C6 — `invoke_effect_node_active_fn_ptr` 常量名歧义 (低风险, 可接受)

**位置**: proposal §新建常量, `.equ invoke_effect_node_active_fn_ptr, 0x08090625`

**问题**: 该名称以 `_fn_ptr` 结尾表示这是一个 **指针常量** (THUMB+1 值 0x08090625), 而非函数本身. 但本项目的常量命名惯例中 `_fn_ptr` 后缀一般用于 EWRAM/IWRAM 中存储的函数指针槽, 不用于 ROM literal pool 中的 THUMB+1 立即数.

参考: 其他 literal pool 中的函数 THUMB+1 地址常量 (如 Seg-3 的 `check_equip_activation_at_slot11+1`) 通常用 `<name>+1` 形式内联, 不定义 .equ.

**可选处理**: 保留当前名称并在注释中说明 "THUMB+1 literal value, not a stored ptr", 或改名为更明确的 `invoke_effect_node_active_thumb_ptr`. 若 executor 认为该项目中已有其他 `_fn_ptr` literal 先例则可维持原名.

**严重性**: 低. 字节 identical 不受影响. 可选修改, 但需在 proposal 中添加说明以避免误读.

---

### #2 — C13 — `DWORD_0807dd5c` 未纳入 RENAME_SLOTS (需修复)

**位置**: proposal §PTR_NAMED slots 列表 + §Symbolization Plan

**问题**: Proposal 将 `0x7dd5c` 列入 "PTR_NAMED slots (already use symbol gP1LifePoints -- skip)" 并注明 "DWORD_0807dd5c". 但在 asm 中该槽的 **标签** 为 `DWORD_0807dd5c` (非 `PTR_gP1LifePoints_0807dd5c`), 这意味着 Ghidra 数据名仍是自动命名的 DWORD_, 尚未执行 rename 操作. 同一段内 0x7dc00 和 0x7dc98 确实已命名为 `PTR_gP1LifePoints_`, 而 0x7dd5c 落后.

**独立验证**:
```
asm/10 line 8592: DWORD_0807dd5c:
asm/10 line 8593:     .word  gP1LifePoints  @ 0807dd5c e0c40102
```
VALUE 已含 gP1LifePoints 符号 (DATA-ref 到位), 但 LABEL 仍为 DWORD_.

**修正**: 在 proposal §Symbolization Plan 的 RENAME_SLOTS 中补充:

```
| 0x7dd5c | DWORD_0807dd5c | -> PTR_gP1LifePoints_0807dd5c | rename label, value already symbolic |
```

并在 Ghidra 脚本中添加对应 renameData 调用. 这样 C13 全部 auto-named 槽均有明确处理动作.

**严重性**: 中. 现状字节 identical 不受影响 (.word gP1LifePoints 汇编正确), 但 Ghidra 中留有残余 DWORD_ 自动名, 不符合 C13 "100% 覆盖" 要求.

---

## 附: 无误的要点确认

- **BLK1 CID**: Magical Mallet (0x198d), FS entry @ 0x1e42ea4, fn_eligible ptr 0x807dd69 -> 0x7dd68 (BLK1 start). OK.
- **BLK4 CID**: Ancient Gear Drill (0x19ae), FS entry @ 0x1e42f1c, fn_eligible ptr 0x807e399 -> 0x7e398 (BLK4 start). OK.
- **BLK2/BLK5 jump tables**: raw ptr verified in ROM; targets within respective BLK. OK.
- **BLK6 false-positive @ 0x82abd08**: 4-byte aligned but points to 0x7e7c4 = inside stub-2 (+0xe4), no push at that addr; conclusively not a fn entry; proposal call of "misaligned code-literal coincidence" correct in effect (though technically 4B aligned, the ROM context shows it as instruction bytes `e7c5 0807` = data word, not called fn).
- **REF slots**: all 7 values match ROM. All globals confirmed in ewram.inc. OK.
- **C5 NEW grep**: all 6 new values have 0 hits in constants/*.inc. OK.
- **C5 REUSE grep**: all 6 reuse constants confirmed present and correct value. OK.
- **C8**: 0 FUN_ in Seg-5a asm lines 8281..8877.
- **C9**: PLATE=0; all proposal text ASCII.
- **C11**: No misnomers; 6 named fn bodies consistent with names.

---

## Reviewer Verdict: F10-Seg-5a = NEEDS_FIX(2 items)
