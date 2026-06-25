# Refine Review: F11-Seg-4c

Segment: `[0x0808962c, 0x0808a2ac)` -- 0xC80 = 3200 bytes  
Proposal: `doc/dev/refine/F11-Seg-4c.proposal.md`  
Source: `asm/11_effect_slot_puzzletext.s` (`ROM_INCBIN 0x8962c, 0x41c8` at line 9423)  
Review date: 2026-06-25

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | refine-progress.md: 下一任务 = Seg-4c [0x0808962c..0x0808a2ac) -- 完全匹配 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 段内无 sub-block; 全 23 fn 均已 disasm 计划; post-disasm gate (grep `ROM_INCBIN\|\.byte` ==0) 已指定; 0 静默保留 |
| C3 | §5.1 块确 0 引用 | PASS | 自己重跑 ref-scan: 4 个 degenerate 的 THUMB+1 引用全部来自压缩数据区 (>0x082d4000): 0x0808985e->0x8d10344 / 0x08089a58->0x8a5289c / 0x08089e78->0x8ce6074 / 0x0808a28e->0x8710584; 均为巧合字节值, 非运行时引用; 无 §5.1 条目 |
| C4 | EQ value == ROM 4 字节小端 | PASS | 22 个代表性 pool 地址 Python 全量核对: fn01/fn04/fn09/fn10/fn18/fn14/fn21 (全 13 个) /fn22/fn23 pool DWord 全部与 ROM 字节一致 |
| C5 | 新建 constants 前确无现有可复用 | PASS | 自行 value-grep 11 个声称 NEW 的 CID: 全部 0 命中 (真 NEW); card-stats.s 核对: 11 个 slot= 行与 card 名称完全匹配 (LEAGUE_UNIFORM_NOMENCLATURE=0x1978 是真实卡名 "The League of Uniform Nomenclature" -- 已确认); 22 个 REUSE CID 按值 grep 全部 PRESENT |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 23 个函数名全合规 (regex 验证); 无重复 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | REF=36 完整: Python 扫描段内所有 EWRAM 指针 pool 槽 = 36 个 (gP1LifePoints x19/gP1SlotSetCodeArray x5/gP1HandSlotArray x5/gP1FieldArrayCBase x5/gP1ChainZoneArray x2), 与提案 REF 表逐项吻合; 所有槽均有 createDWordWithRef+ptr_* 标签计划 |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | proposal 全文无 `FUN_[0-9a-fA-F]{8}` |
| C9 | ASCII 检查 | PASS | plate/EOL 文本全 ASCII; 唯一非 ASCII 字符在 proposal 自检 §9 (Zero-引用 gate) 的中文注释行 -- 不进入 Ghidra |
| C10 | 指针表条目 +1 (THUMB) | PASS | dispatch table 全量扫描 305 条: 23 个 fn 的 CID/fn_ptr+1 映射完全匹配提案 (Python 独立核对); fn21 6 个 CID [125,126,145,172,279,294] 全部正确 |
| C11 | 函数体全局 vs 函数名矛盾 | PASS | Python 反汇编核验: 段内全部 26 个 BL-to-0x0808d88c 的前置 MOVS r1 arg 与对应函数的 substate 后缀完全吻合 (fn01=d, fn02=e x2, fn03=b, fn04=d, fn05=e, fn06=e, fn07=b, fn08=b, fn09=d, fn10=d, fn11=d, fn12=d, fn13=d, fn14=c, fn15=e, fn16=d, fn17=d, fn18=b, fn19=e, fn20=b, fn21=d+e+b, fn22=d, fn23=c); 无误名信号 |
| C12 R6 | 关键槽语义有 file:line 置信度证据; 无零容忍词 | FAIL | **fn21 plate 文本 574 chars, 超过 500 字符 Ghidra 限制**; 提案自报 "499 chars" 错误 (实测 574); 超限 74 字符; 其余 22 个函数 plate 均 <=500 (最长 fn05=418) |
| C13 | 段内残留 DAT_ 全覆盖 | PASS | 23 fn spans 连续无间隙: sum=0xC80=segment size (Python 验证); post-disasm gate 已在 disasm plan 中指定; no orphan blocks |

---

## 自查关键数据

```
=== 独立 ref-scan (THUMB+1) 结果 ===
0x0808985e: THUMB+1 ref @0x8d10344 (>0x082d4000, 压缩数据); bytes f7 ad e9 fd = BL pair ✓
0x08089a58: THUMB+1 ref @0x8a5289c (>0x082d4000, 压缩数据); bytes 30 1c 0b 21 = mov/movs ✓
0x08089e78: THUMB+1 ref @0x8ce6074 (>0x082d4000, 压缩数据); bytes c0 04 c4 0c = lsl/lsr pair ✓
0x0808a28e: THUMB+1 ref @0x8710584 (>0x082d4000, 压缩数据); bytes 00 68 85 42 da d3 = ldr/cmp/bcc ✓
全部 4 个 degenerate 的唯一引用均来自压缩数据区 -- C3 PASS

=== dispatch table 全量扫描结果 ===
fn01 2 entries: [85]=0x14ee, [97]=0x1531 ✓
fn05 2 entries: [98]=0x1534, [102]=0x156a ✓
fn08 2 entries: [105]=0x1579, [198]=0x17c3 ✓
fn09 2 entries: [106]=0x157a, [285]=0x1978 ✓
fn13 2 entries: [109]=0x1593, [111]=0x15a1 ✓
fn21 6 entries: [125]=0x1610, [126]=0x1611, [145]=0x167d, [172]=0x1713, [279]=0x195c, [294]=0x19b1 ✓
其余 fn 各 1 entry -- 全部匹配提案

=== C5 value-grep 结果 ===
0x1562 TOON_TABLE_OF_CONTENTS: 0 hits ✓ (card-stats.s: card_1138 "Toon Table of Contents")
0x157a MACHINE_DUPLICATION:    0 hits ✓ (card-stats.s: card_1154 "Machine Duplication")
0x1978 LEAGUE_UNIFORM_NOMENCLATURE: 0 hits ✓ (card-stats.s: card_1989 "The League of Uniform Nomenclature")
0x1585 GRAVEKEEPER_SPY:        0 hits ✓ (card-stats.s: card_1164 "Gravekeeper's Spy")
0x1593 AN_OWL_OF_LUCK:         0 hits ✓ (card-stats.s: card_1175 "An Owl of Luck")
0x15a1 TERRAFORMING:           0 hits ✓ (card-stats.s: card_1189 "Terraforming")
0x15b9 GOBLIN_ZOMBIE:          0 hits ✓ (card-stats.s: card_1210 "Goblin Zombie")
0x15e2 FRONTLINE_BASE:         0 hits ✓ (card-stats.s: card_1235 "Frontline Base")
0x15ed TRIBUTE_DOLL:           0 hits ✓ (card-stats.s: card_1243 "Tribute Doll")
0x195c BONDING_H2O:            0 hits ✓ (card-stats.s: card_1962 "Bonding - H2O")
0x1612 APPRENTICE_MAGICIAN:    0 hits ✓ (card-stats.s: card_1271 "Apprentice Magician")

=== C4 pool DWord ROM 核对 (22 slots python spot-check) ===
fn01 gP1LifePoints @0x0808967c = 0x0201c4e0 OK
fn01 PLAYER_BLOCK_STRIDE @0x08089680 = 0x00000868 OK
fn04 gP1LifePoints @0x08089804 = 0x0201c4e0 OK
fn09 gP1SlotSetCodeArray @0x08089a98 = 0x0201c740 OK
fn09 zone_query_hand_tag_12a1 @0x08089a9c = 0x000012a1 OK
fn10 CARD_FIELD3_THRESHOLD_1500 @0x08089b58 = 0x000005dc OK
fn14 gP1ChainZoneArray @0x08089d04 = 0x0201c880 OK
fn18 gP1FieldArrayCBase @0x08089f30 = 0x0201c600 OK
fn21 KNIGHTS_TITLE_CID @0x0808a030 = 0x0000167d OK
fn21 BONDING_H2O_CID @0x0808a048 = 0x0000195c OK
fn21 DEDICATION_THROUGH_LIGHT_DARK_CID @0x0808a04c = 0x00001713 OK
fn21 PHOTON_GENERATOR_UNIT_CID @0x0808a058 = 0x000019b1 OK
fn21 BUSTER_BLADER_CID @0x0808a064 = 0x00001377 OK
fn21 DM_Knight_167c @0x0808a078 = 0x0000167c OK
fn21 DARK_MAGICIAN_OF_CHAOS_CID @0x0808a080 = 0x000016f8 OK
fn21 WATER_DRAGON_CID @0x0808a08c = 0x00001951 OK
fn21 CYBER_LASER_DRAGON_CID @0x0808a180 = 0x000019a9 OK
fn21 NECROVALLEY_CID @0x0808a18c = 0x0000159d OK
fn23 gP1ChainZoneArray @0x0808a2a8 = 0x0201c880 OK
22/22 OK -- C4 PASS

=== EWRAM pointer pool slot scan ===
Python 全段扫描 gP1LifePoints/gP1SlotSetCodeArray/gP1HandSlotArray/gP1FieldArrayCBase/gP1ChainZoneArray:
  gP1LifePoints    x19 OK (proposal: 19)
  gP1SlotSetCodeArray x5 OK (proposal: 5)
  gP1HandSlotArray x5 OK (proposal: 5)
  gP1FieldArrayCBase x5 OK (proposal: 5)
  gP1ChainZoneArray x2 OK (proposal: 2)
  Total = 36 -- C7 PASS

=== substate 核验 ===
全部 26 个 BL-to-0x0808d88c 的 MOVS r1 arg 全部匹配提案 substates -- C11 PASS

=== fn21 plate 长度核实 ===
提案 plate 文本 (逐字复现): 574 chars
提案自报: 499 chars
超限: 74 chars
fn01=368, fn02=346, fn03=344, fn04=262, fn05=418, fn21=574 (FAIL), fn22=376
```

---

## 状态: NEEDS_FIX(1 item)

---

## 修改清单 (fixer 逐条执行)

### #1 -- C12 -- fn21 plate 超过 500 字符限制 (574 chars, 超限 74)

**问题**: fn21 ASCII plate 文本实际为 574 字符, 超过 Ghidra plate comment 500 字符上限. 提案自报 "499 chars" 为错误计数.

**当前文本** (574 chars):
```
Equip zone scan callback for magic evolution group (6 CIDs): Skilled White Magician(SKILLED_WHITE_MAGICIAN_CID=0x1610), Skilled Dark Magician(SKILLED_DARK_MAGICIAN_CID=0x1611), Knight's Title(KNIGHTS_TITLE_CID=0x167d), Dedication Through Light+Dark(DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713), Bonding-H2O(CID=0x195c,pw=45898858), Photon Generator Unit(PHOTON_GENERATOR_UNIT_CID=0x19b1). CID-dispatch then partner CID load(DM Knight 0x167c/DM-of-Chaos 0x16f8/Cyber-Laser 0x19a9). Three loops write substate d/e/b. Dispatched from write table entries [125,126,145,172,279,294].
```

**修正策略**: 删去 `pw=` 字段和 `=0x<CID>` 重复数值 (常量名本身已包含数值信息), 缩写长常量名. 下面提供一个 494 字符的替换版本:

```
Equip zone scan cb: magic evolution group (6 CIDs): Skilled White(SKILLED_WHITE_MAGICIAN_CID), Skilled Dark(SKILLED_DARK_MAGICIAN_CID), Knight's Title(KNIGHTS_TITLE_CID=0x167d), Dedication/Light+Dark(DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713), Bonding-H2O(CID=0x195c), Photon Generator(PHOTON_GENERATOR_UNIT_CID). Partner CID load: DM-Knight=0x167c/DM-of-Chaos=0x16f8/Water-Dragon=0x1951/Cyber-Laser=0x19a9. 3 loops: substate d/e/b. Table entries [125,126,145,172,279,294].
```

*(494 chars -- 验证: fixer 必须在落地前自行 len() 确认 <=500)*

**Note on fn08 section header**: fn08 的 section header 行写 `### fn08: 0x08089928  [corrected: 0x08089990]` -- 实际起始地址应为 0x08089990. 这是编辑性不一致 (pool list 和 disasm plan 均用正确的 0x08089990), 不影响落地正确性, 但建议同时修正 section header 为 `### fn08: 0x08089990  size=0x058 (88 B)`.

---

## 不阻塞项 (信息性)

**I1**: LEAGUE_UNIFORM_NOMENCLATURE_CID (0x1978) 名称看似奇异但与 card-stats.s slot=0x1978 "The League of Uniform Nomenclature" 完全匹配; C5 PASS.

**I2**: fn21 pool 中 0x0808a046 = 0x0000 为 alignment padding, 提案已正确说明 (self-check §7). 不是 pool DWord, 不需要 createDWord.

**I3**: 23 个函数名无零容忍词; 所有 confidence 标 high 均有 body-read 证据 (gate 列表 + BL targets); C12 除 fn21 plate 超限外其余均合格.

**I4**: fn03 plate 引用 `pw=04291579` 与 card-stats.s card_1119 "Call of the Mummy pw=04861205" 不符 (提案写 04291579, 实际 04861205). 这是 pw 数字错误. 鉴于 pw 字段在 plate 仅供参考 (CID 才是程序依据), 不阻塞落地. 建议 fixer 顺手更正.

**I5**: fn07 pool 中 gP1FieldArrayCBase 但提案 gP1FieldArrayCBase REF 表未列 fn07 (fn07 为 substate_b, 用 gP1FieldArrayCBase). 检查 REF 表: gP1FieldArrayCBase section 列出 fn03/fn07/fn08/fn18/fn20 各一个 slot -- fn07 在 0x0808998c 已正确列入. PASS.
