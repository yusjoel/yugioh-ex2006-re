# Refine Review: F11-Seg-4f

Reviewer 独立复核 (不信 proposal 结论, 自主重跑 ROM 读值 + ref-scan)。

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | §五 roadmap: Seg-4f `[0x0808bb7c, 0x0808cabc)`, 紧接 Seg-4e `[0x0808ad8c, 0x0808bb7c)` ✅, 未跳号/回头 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | ✅ | 段内无 ROM_INCBIN/\.byte; 纯 THUMB code + literal pools; C2 通过 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无 §5.1 块; N/A |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ❌ | **见 #1**: 独立 python 读值确认关键 pool 值全 OK (gP1LifePoints 0x0201c4e0 / PLAYER_BLOCK_STRIDE 0x868 / VAMPIRE_GENESIS_GDUELPF_NEG_OFF 0xfffffef4 / GILFORD_HAND_SLOT_MASK 0xffff803f / 全部 globals OK); 但 fn21+fn22 各有第 2 个 literal pool 被 proposal **遗漏** (地址有效、LDR PC-relative 可达), 导致 pool 总数少 4 个 DWord — 见 #2 |
| C5 R1 复用 | 新建 constants 前无可复用现有同值 | ❌ | **见 #1 (CRITICAL)**: `GILFORD_HAND_SLOT_MASK=0xffff803f` 重复定义已存在的 `slot_field_mask_ffff803f=0xffff803f` (card_info.inc:1765, Seg-4d 建立). 必须 REUSE `slot_field_mask_ffff803f`. 另: `VAMPIRE_GENESIS_GDUELPF_NEG_OFF=0xfffffef4` 独立 grep 0xfffffef4 in constants/ 返回 0 命中, 确认 NEW |
| C6 R2 名 | 槽名合规, 无碰撞 | ❌ | **见 #3**: 全部 25 名满足 `^[a-z][a-z0-9_]+$`, 无重复; 但 `scan_zone_warrior_lady_wasteland_substate_bd` 的 `_bd` 后缀误导 — 独立 BL-scan 证明 fn26 只有 1 次 `write_equip_zone_entry_by_substate` 调用 (0x0808ca26, r1=0xd), r1=0xb 是传给 `find_effect_node_in_zone` (0x0802fd60) 的 zone-type 参数, 非 write_equip 的 substate; 正确后缀应为 `_d` |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | N/A | 无 carve; 所有 EWRAM REF 跟随 Seg-4a..4e createDWordWithRef 范式; N/A |
| C8 R5 现名 | plate 无残留 `FUN_/DAT_/DWORD_` | ✅ | 遍历 25 个 plate 文本, 无 FUN_/DAT_/DWORD_ 残留 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 25 个 plate 文本逐字符核: 全 ASCII (0x00-0x7F). 无 CJK/全角/假名 |
| C10 carve | 指针表条目 `+1` 正确 | N/A | 无 carve; N/A |
| C11 误名 | 函数体全局 vs 函数名矛盾已标 FUNC_RENAME | ✅ | 无误名信号; 25 fn 均为 scan_zone_<card>_substate_<x> 范式, 与函数体内 CID 及 write_equip substate 一致 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | ✅ | 消费者证据节给出 35 个 BL 目标/全局的 file:line 引用及 high/med 置信度; VAMPIRE_GENESIS_GDUELPF_NEG_OFF 标 med (结构性证据, 语义未完全确认), 合规; GILFORD_HAND_SLOT_MASK 同 med |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ✅ | 段内无 `ROM_INCBIN`/`.byte`; 无 `DAT_/DWORD_/PTR_` 残留(全新 fn); 验收通过 |

---

## 状态: NEEDS_FIX (3 items)

---

## 修改清单

### #1 — C5 — GILFORD_HAND_SLOT_MASK=0xffff803f 重复现有 slot_field_mask_ffff803f; 必须 REUSE

**证据**:
- `grep 0xffff803f constants/card_info.inc` 命中 → `card_info.inc:1765: .equ slot_field_mask_ffff803f, 0xffff803f`  (Seg-4d 建立, 注释 "scan_zone_guardian_equip_group_substate_e fn24")
- 同值还出现在 `constants/gl_scrollbar.inc:12: .equ SCROLLBAR_CLEAR_BITS_14_6, 0xffff803f`

**必改**:
- 删除 Raw-value equate 表中的 `GILFORD_HAND_SLOT_MASK=0xffff803f` 新建行
- 将 fn25 pool 0x0808c924 (`0xffff803f`) 的处置从 NEW 改为 REUSE `slot_field_mask_ffff803f` (card_info.inc:1765)
- Ghidra 脚本中该 pool slot 用 `.word slot_field_mask_ffff803f` 而非新建 `.equ GILFORD_HAND_SLOT_MASK`
- fn25 plate (len=428) 中的 `bit-mask 0xffff803f` 引用改为 `slot_field_mask_ffff803f (0xffff803f)` — 保持 ASCII 且长度不超 500

---

### #2 — C4 / REF — fn21 + fn22 各有第 2 个 literal pool 被完全遗漏; REF 总数应为 53 而非 51

**独立 ROM 扫描结果**:
- `python scan EWRAM refs in [0x0808bb7c, 0x0808cabc)` 返回 **53 个 EWRAM 地址** (0x02xxxxxx):
  `gP1LifePoints (0x0201c4e0) x22`, `gP1SlotSetCodeArray x4`, `gP1HandSlotArray x9`, `gP1HandCountBase x2`, `gP1FieldArrayCBase x7`, `gDuelPhaseFlags x4`, `gP1ChainZoneArray x3`, `gDuelFieldSlots x1`, `gP1SlotCountBase x1`
- Proposal 列出 51 (gP1LifePoints x20 = 少 2)
- 缺失的 2 个 gP1LifePoints pool 地址: `0x0808c5e4` (fn21 body 内) 和 `0x0808c6d4` (fn22 body 内)
- 用 LDR PC-relative 解码验证两者均有 LDR 指令引用:
  - fn21: `LDR r2,[PC,#60] at 0x0808c5a4 → 0x0808c5e4 = 0x0201c4e0` (gP1LifePoints)
  - fn21: `LDR r1,[PC,#60] at 0x0808c5aa → 0x0808c5e8 = 0x00000868` (PLAYER_BLOCK_STRIDE)
  - fn22: `LDR r2,[PC,#60] at 0x0808c694 → 0x0808c6d4 = 0x0201c4e0` (gP1LifePoints)
  - fn22: `LDR r1,[PC,#60] at 0x0808c69a → 0x0808c6d8 = 0x00000868` (PLAYER_BLOCK_STRIDE)
- 即: proposal 的 pool DWord 总数也应为 **93** (而非 89)

**必改**:
- fn21 的 "Pool" 节补充: 在已有 3 个 pool 之外追加 `0x0808c5e4=gP1LifePoints`, `0x0808c5e8=PLAYER_BLOCK_STRIDE`
- fn22 的 "Pool" 节补充: 追加 `0x0808c6d4=gP1LifePoints`, `0x0808c6d8=PLAYER_BLOCK_STRIDE`
- "Literal Pool DWord List" 的 **fn21** 行: 在 `0x0808c56c, 0x0808c570, 0x0808c574` 后追加 `0x0808c5e4, 0x0808c5e8`
- "Literal Pool DWord List" 的 **fn22** 行: 在 `0x0808c65c, 0x0808c660, 0x0808c664` 后追加 `0x0808c6d4, 0x0808c6d8`
- REF_SLOTS 的 gP1LifePoints 表: 在 `0x0808c784 fn23` 之前插入 `0x0808c5e4 fn21 pool2` (顺序), 在 `0x0808c784` 之前插入 `0x0808c6d4 fn22 pool2`
- REF count gP1LifePoints 从 **20 → 22**; 总 REF 从 **51 → 53**
- Pool DWord 总数注释从 **89 → 93**
- Ghidra 脚本中这 4 个 slot 须添加 `createDWord` + `createDWordWithRef`

---

### #3 — C6 — fn26 名称后缀 `_substate_bd` 错误; 仅 substate_d 通过 write_equip 写出

**独立 BL-scan fn26 (0x0808c97c..0x0808ca64) 结果**:
fn26 全程只有 **1 次** `BL write_equip_zone_entry_by_substate (0x0808d88c)` 调用 (位于 0x0808ca26, 此前 `MOVS r1,#0xd` @ 0x0808ca22 → substate = `0xd`).
`MOVS r1,#0xb` @ 0x0808ca14 后紧接 `BL find_effect_node_in_zone (0x0802fd60)` — `0xb` 是 find_effect_node 的 zone-type 参数, 而非 write_equip 的 substate.

**必改**:
- 将 `scan_zone_warrior_lady_wasteland_substate_bd` 改为 `scan_zone_warrior_lady_wasteland_substate_d`
- fn26 描述节中 "Substates: 0xb (MOVS r1,#0xb at 0x0808ca14 then find_effect_node call at 0x0808ca18, actual write at 0x0808ca22 after BL), 0xd (MOVS r1,#0xd at 0x0808ca22 before BL write_equip)" 应改为:
  "Substate: 0xd (MOVS r1,#0xd at 0x0808ca22 before BL write_equip_zone_entry_by_substate); 0xb is zone_type arg to find_effect_node_in_zone (0x0808ca14→0x0808ca18), not a write_equip substate"
- fn26 plate 末尾的 "write substate_b+d" 改为 "write substate_d; 0xb passed to find_effect_node_in_zone as zone type"
- CSV row name 字段同步更新

---

## 附注 (非阻断, fixer 修正时顺带处理)

**A. fn21/fn22 substate_e 地址引用错误 (内部 prose)**
- fn21 plate/body: "MOVS r1,#0xe at 0x0808c5ce" — 0x0808c5ce 是 BL 高半字 (0xf001), 实际 MOVS r1,#0xe 在 `0x0808c5bc` (条件路径) 和 `0x0808c5ca` (备用路径)
- fn22 plate/body: "MOVS r1,#0xe at 0x0808c6be" — 0x0808c6be 是 BL 高半字 (0xf001), 实际在 `0x0808c6ac` 和 `0x0808c6ba`
- substate **值** (0xe) 本身正确; 这是内部地址引用偏差. 建议 fixer 修正描述地址.

**B. fn07+fn08 plate 内函数地址对调**
- Plate: "fn07(0x0808be88)+fn08 combined" — 但 0x0808be88 是 fn08 (degenerate alt-entry), fn07 实际起点为 0x0808be6c
- 应改为: "combined fn: fn07 start=0x0808be6c; fn08(0x0808be88)=degenerate excluded"

**C. fn17+fn18 plate 内函数地址错误 (同上模式)**
- Plate: "fn17(0x0808c3da) combined" — 0x0808c3da 是 fn18 (degenerate); fn17 起点 0x0808c3d0
- 应改为: "combined fn: fn17 start=0x0808c3d0; fn18(0x0808c3da)=degenerate excluded"

---

## Reviewer Verdict: F11-Seg-4f = NEEDS_FIX(3 items)
