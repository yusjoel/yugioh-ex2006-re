# Refine Review: F11 Seg-5

> Reviewer: independent (overwriting self-authored fixer review)
> Proposal: doc/dev/refine/F11-Seg-5.proposal.md
> Module: asm/11_effect_slot_puzzletext.s [0x0808d7f4, 0x0808e8fc)
> Scan scope: asm lines 18163-20622 (fn01..fn18 incl. fn18 literal pool to 0x0808ea24)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | Seg-5 = [0x0808d7f4, 0x0808e8fc), 18 fn, Seg-4g ✅ — 与 §五路线图一致 |
| C2 Rule2 | ✅ | 0 ROM_INCBIN / 0 .byte-as-code; switchD 已 decode (case labels present) |
| C3 Rule3 | ✅ | 无 §5.1 块需 ref-scan; 段内无孤儿数据块 |
| C4 R1 值 | ❌ | DAT_0808e824 在 gEquipZoneCountTable 区块 (line 104) 被错标为 0x0201e1c8 — ROM 实值 0x00001354 (FORCED_REQUISITION_CID); raw 区后段正确分配但与该行矛盾 |
| C5 R1 复用 | ✅ | 11 个 NEW 常量全部按 VALUE grep 0 命中; 7 REUSE CID 按值 grep 确认存在 |
| C6 R2 名 | ✅ | 14 RENAME 标签格式 `ptr_lp_<4hex>` 符合 `^[a-z][a-z0-9_]+$`; 无碰撞 |
| C7 R3 接通 | ✅ | 无 REF 槽; PTR_ 作 EQ (equate-based RENAME) 无需 addMemoryReference — 与 Seg-3a/3b 一致 |
| C8 R5 现名 | ✅ | 12 函数 17 处 FUN_ 替换: 逐一查 asm/*.s label 定义, 地址全部匹配 (invoke_r3@0x0810e5d4, scan_card_placement_for_activation@0x0808fc78, scan_field_slots_for_archfiend_equip_bitmap_update@0x0808fbd0, dispatch_equip_field_scan_sequence@0x08090218, count_equip_eligible_slots_both_players@0x08032a6c, enqueue_effect_zone_pair_sprite_scan@0x080454c0, dispatch_equip_slot_sprite_with_field6_score@0x08067ea0, dispatch_equip_sprite_update_by_slot_icid@0x080a0334, dispatch_equip_zone_sprite_and_activation@0x080440b8, render_monster_slot_card_with_lp_bar@0x0804a334, trigger_lp_bar_animation_if_ready@0x08095ca0, init_equip_slot_entry_with_copy_flag_sprite@0x080abbd8, init_equip_slot_entry_with_placement_type_check@0x080abe54, handle_card_effect_zone_eligibility_by_field6@0x08047218, render_slot_card_sprite_from_descriptor@0x08047f50, render_slot_card_sprite_and_effects@0x08048020, render_slot_card_sprite_with_chaos_equip_check@0x08048364) |
| C9 ASCII | ✅ | grep 非 ASCII: lines 18163-20622 全部纯 ASCII, 0 命中 |
| C10 carve | ✅ | 无 carve; 无 fn-ptr+1 条目 |
| C11 误名 | ✅ | 抽查 fn03/fn09/fn15 函数体与名称: find_effect_record_index_by_id (二分搜索), scan_slots_activate_equip_by_effect_id (2x5 扫描+激活), enqueue_equip_chain_sprites_for_zones (扫描 zone 入队 OBJ sprite) — 无矛盾 |
| C12 R6 | ✅ | NEW 常量均有 file:line 证据 (card-stats.s slot 编号) 和置信度; 无零容忍词 |
| C13 残留 | ❌ | 自跑 python 统计: asm 实有 113 个 auto-named 槽; proposal 仅覆盖 109 个; 4 槽无处置 (详见修改清单) |

---

## 独立复核关键步骤

### C13 slot count 独立核查

python 扫描 asm lines 18162-20622 (`DAT_0808xxxx:` / `DWORD_0808xxxx:` / `PTR_*_0808xxxx:` 标签定义):

```
Total: 113 slots
```

proposal §十 声称 "113 total" 但内部三表并集仅 109 个, 缺 4 个 (见修改清单 #2)。

### C4 DAT_0808e824 双重归属

python 读 ROM[0x0808e824] = `0x00001354` = FORCED_REQUISITION_CID.
- proposal §二 gEquipZoneCountTable 区块 line 104: 错误列出 `DAT_0808e824 (fn13 zone_chain_base ref) — Note: 0x0201e1c8 | gEquipZoneCountTable`
- proposal §二 raw 区块: 正确列出 `DAT_0808e824 | 0x00001354 | FORCED_REQUISITION_CID`

两行为同一槽, 第一行值错误. 第一行必须删除.

### C5 NEW 常量 value-grep

按值 grep `constants/` 目录:
- 0x13a2 / 0x15fb / 0x17a6 / 0x197b / 0x1343 / 0x1306 / 0x1361: 全部 0 命中 ✅
- 0x09e5a128 / 0x09e3f150 / 0x09e3f164 / 0x0000104c: 全部 0 命中 ✅
- gEquipEffectZoneTable=0x09e5a0c4 已存在 (card_info.inc L1662); 新 gEffectHandlerTable=0x09e5a128 为不同地址, 无碰撞 ✅
- EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140 (duel_field.inc L460); 新 gEquipCandidateScoreBase=0x09e3f150 (+0x10), gEquipCandidateInitBase=0x09e3f164 (+0x24) — 不同地址 ✅

### C4 ROM 字节核对 (抽样 16 槽)

全部通过 python struct.unpack("<I") 比对:
DAT_0808da8c=0x09e5a128 ✅, DAT_0808e054=0x09e3f164 ✅, DAT_0808e060=0x09e3f150 ✅,
DWORD_0808df30=0x0000104c ✅, DAT_0808e4d4=0x98300000 ✅, DAT_0808e8f8=0x9b080000 ✅,
DAT_0808e834=0x3a200000 ✅, DAT_0808e5b0=0xffffe358 ✅, DAT_0808dc24=0x000013a2 ✅,
DAT_0808e824=0x00001354 ✅ (与 raw 区行一致; gEquipZoneCountTable 行错误),
DAT_0808de38=0x00001009 ✅, DAT_0808de3c=0x00000ff9 ✅, DAT_0808e444=0x000012ea ✅,
DAT_0808e448=0x0201e1c8 ✅, DWORD_0808df2c=0x0201e1c8 ✅, DAT_0808d8f8=0x0201e4f0 ✅.

### §四 RENAME 行数核查

asm 中 `PTR_gP1LifePoints_0808xxxx:` 标签定义 14 个; §四 表格也有 14 行 (含 ptr_lp_ea10). 正确.
§四 文字前言写 "13 PTR" 为文字笔误, 表格本身正确.

---

## 状态: NEEDS_FIX

---

## 修改清单 (逐条可执行)

### #1 — C4 — 删除 §二 gEquipZoneCountTable 区块中错误的 DAT_0808e824 行

**问题**: proposal §二 REUSE 区块第 104 行把 `DAT_0808e824` 错误归入 gEquipZoneCountTable (0x0201e1c8), 而 ROM 实值为 0x00001354 (FORCED_REQUISITION_CID).

**操作**: 删除以下行:
```
| DAT_0808e824 (fn13 zone_chain_base ref) — Note: 0x0201e1c8 | gEquipZoneCountTable | ewram.inc |
```
(raw 区中正确的 `DAT_0808e824 | 0x00001354 | FORCED_REQUISITION_CID` 行保留不动.)

---

### #2 — C13 — 补充 4 个缺失槽的处置

asm 中存在但 proposal 未处置的 4 个槽:

#### #2a — DAT_0808d8a8 @ 0x0808d8a8 = 0x0808d8ac

**含义**: fn02 (`write_equip_zone_entry_by_substate`) switch(substate-0xb) 的 switchD jump table 基址指针; `switchD_0808d8a4__switchdataD_0808d8ac` 标签已在 asm 中.
外部 ref-scan: raw=0, THUMB+1=0 (纯内部 pc-relative 字面池, 0 外部引用).
**处置**: 参照 Seg-1 precedent (`switchdata_ref_*`); 在 proposal §三 REF_SLOTS 中增加一行 (RENAME slot 到 `switchdata_ref_d8a8`), 或在 §二 raw 区增加 EQ 行注明 "switchD base for 0x0808d8a4, value = asm label switchD_0808d8a4__switchdataD_0808d8ac; internal ptr, add as raw EQ with name switchd_base_d8a8".

推荐处置: 在 §二 raw 区增加:
```
| DAT_0808d8a8 | 0x0808d8ac | switchd_base_d8a8 | internal (Ghidra: EQ or rename; switchD_0808d8a4 jump table base ptr, 0 external refs) |
```

#### #2b — DAT_0808e5b8 @ 0x0808e5b8 = 0x00000868

**含义**: fn13 (`scan_field_slots_for_lp_zone_sprite_with_equip`, 0x0808e4d8) 字面池 PLAYER_BLOCK_STRIDE.
ROM 实值: 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc, 已存在).
**处置**: 在 §二 EQ REUSE PLAYER_BLOCK_STRIDE 组增加:
```
| DAT_0808e5b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
```

#### #2c — DAT_0808e5bc @ 0x0808e5bc = 0x0201c510

**含义**: fn13 字面池 gDuelFieldSlots.
ROM 实值: 0x0201c510 = gDuelFieldSlots (ewram.inc, 已存在).
**处置**: 在 §二 EQ REUSE gDuelFieldSlots 组增加:
```
| DAT_0808e5bc | 0x0201c510 | gDuelFieldSlots | ewram.inc |
```

#### #2d — DAT_0808ea18 @ 0x0808ea18 = 0x00000868

**含义**: fn18 (`scan_all_zone_slots_for_lp_change_indicator`, 0x0808e8fc) 字面池 PLAYER_BLOCK_STRIDE.
ROM 实值: 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc, 已存在).
**处置**: 在 §二 EQ REUSE PLAYER_BLOCK_STRIDE 组增加:
```
| DAT_0808ea18 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc |
```

---

### #3 — 文字笔误 (非阻断) — §四 前言 "13 PTR" 应为 "14 PTR"

§四 preamble: "13 PTR_gP1LifePoints_ slots in range" -> 改为 "14 PTR_gP1LifePoints_ slots in range".
(表格已有 14 行, 正确; 仅前言数字笔误.)

---

### #4 — §十 执行摘要更新

修完 #1/#2 后, §十 计数更新:
- EQ total: 建议列出正确分类数 (删除 DAT_0808e824 重复行, 增加 4 个缺失槽 = 净增 3, 删除 1 错误行).
- 明确说明 switchd_base_d8a8 处置选择 (EQ raw 或 REF).

---

## Reviewer Verdict: F11 Seg-5 = NEEDS_FIX(4 items)
