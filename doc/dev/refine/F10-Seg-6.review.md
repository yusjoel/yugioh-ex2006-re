# Refine Review: F10-Seg-6  [0x0807f730, 0x08080ba0)

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | §五 Seg-6=[0x7f730,0x80ba0),18fn,123slots,0inc+2sw(0xfe22,0x806cc); 前段 Seg-5 状态=✅; 顺序正确 |
| C2 Rule2 | ROM_INCBIN/.byte 块全有归宿 | OK | 段内 ROM_INCBIN=0 (python 扫描确认); Rule2 trivially satisfied |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 无 §5.1 块; C3 N/A |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | OK | python 核对全部 13 DWORD_ pool (两个 literal pool 13/13 OK) + 抽查 22/110 DAT_ 槽; 全数匹配 |
| C5 R1 复用 | 9 NEW 值在 constants/*.inc 无现有可复用 | OK | 详见下文 §C5 细节 |
| C6 R2 名 | 12 新槽名/标签格式无碰撞 | OK | 12 RENAME 槽新标签均 ^[a-z][a-z0-9_]+$; 12 equate/abs-label 均 ^[A-Z][A-Z0-9_]+$ 或 g[a-z]*_*; asm/10 内 0 碰撞 |
| C7 R3 接通 | 3 NEW abs ewram 标签有 DATA-ref 计划 | OK | gDuelPhaseFlags_criteria_count/set_f_flag/criteria_arr_base 均为 `label = 0xADDR` GAS 绝对符号; DAT_ 槽将 .word <label> 引用; 接通路径完整 |
| C8 R5 现名 | plate/EOL 无残留 FUN_ | FAIL | proposal 报告 5 in-file FUN_; 独立扫描发现 **6** 个: L11931/L12062×2/L12847/L12904 (已在提案中) + **L14644 FUN_08081ce8 缺失** (push_to_effect_slot_array 的 plate, 函数 0x08080b74 在段内); 另 L14675 FUN_08080c9c 属 assemble_effect_slot_attr_with_zone_lookup(0x08080ba0, Seg-7 首函数) 的 pre-plate, 不属本段责任 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 11 条 mojibake 行已识别 (L12017/12018/12274/12277-12279/12587/12904/13566/13570/14361); 提议 ASCII 替换文本 grep [^\x00-\x7F] = 0 命中; 新增 constants 定义纯 ASCII |
| C10 carve | 无 carve | N/A | 段内无 ROM_INCBIN; N/A |
| C11 误名 | 函数名与函数体无矛盾 | OK | 18 fn 名均与代码一致; 两个 switchD 派发函数名与 switch 结构匹配; FUNC_RENAME=0 正确 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | OK | 10 项 Consumer Evidence 均有 asm/10 行号 + high 置信度; 无零容忍词 |
| C13 残留 | 段内所有自动名槽均被覆盖 | OK | 独立 python: DAT_=110, DWORD_=13, PTR_gP1LifePoints_=6(不计入); 110+13=123; EQ(66)+REF(57)=123; 全覆盖; 61 DAT_EQ + 5 DWORD_EQ = 66 ✓; 49 DAT_REF + 8 DWORD_REF = 57 ✓ |

---

## §C5 细节 (9 NEW 值)

| 值 | 名称 | constants/*.inc 命中 | 判定 |
|----|------|---------------------|------|
| 0x0000059c | EQUIP_ZONE_ATTR_COMPOSITE_OFF | 0 | NEW OK |
| 0x000005a4 | EQUIP_CRITERIA_TARGETED_FLAG_OFF | 0 | NEW OK |
| 0x000005ac | EQUIP_CRITERIA_DISPLAY_ARR_OFF | 0 | NEW OK |
| 0x00001921 | DRAGONS_MIRROR_CID | 0 | NEW OK; card-stats.s card_1918 slot=0x1921 pw=71490127 确认 |
| 0x0000197a | NON_FUSION_AREA_CID | 0 | NEW OK; card-stats.s card_1991 slot=0x197A pw=27581098 确认 |
| 0x0000804a | OAM_EQUIP_ZONE_SPRITE_P2_4A | 0 (.equ) | NEW OK; 命中行均为地址注释 (0x0804a5b8 等) 非等式定义 |
| 0x0000804b | OAM_EQUIP_ZONE_SPRITE_P2_4B | 0 (.equ) | NEW OK; 命中行为 ewram.inc 注释文本 "804B" (字节数) 及 name_input.inc 注释, 非等式定义 |
| 0x0000804c | OAM_EQUIP_ZONE_SPRITE_P2_4C | 0 | NEW OK |
| 0xfffffa54 | EQUIP_CRITERIA_ARR_NEG_OFF | 0 | NEW OK; 验证: (-0x5ac) & 0xffffffff = 0xfffffa54 ✓ |
| 0x0201b830 | gDuelPhaseFlags_criteria_count | 0 | NEW OK; gDuelPhaseFlags(0x0201b290)+0x5a0=0x0201b830 ✓; raw_refs=2 |
| 0x0201b838 | gDuelPhaseFlags_set_f_flag | 0 | NEW OK; +0x5a8=0x0201b838 ✓; raw_refs=3 |
| 0x0201b850 | gDuelPhaseFlags_criteria_arr_base | 0 | NEW OK; +0x5c0=0x0201b850 ✓; raw_refs=1 |

注: 0x804a/804b 的 C5 grep 结果初看为 "HIT", 详查均属注释中的 ROM 地址或字节数, 无 `.equ` 定义 — 判定 NEW。

---

## §switchD 独立复核

### switchD_0807fe22 (dispatch_equip_criteria_display_by_type_code)

- DAT_0807fe28 ROM 值: 0x0807fe2c ✓ (table ptr)
- 表 start: 0x0807fe2c; 30 项 (case 0x63..0x80); 8 unique targets
- 所有 targets 在段内 [0x7f730, 0x80ba0): YES
- 无 THUMB+1 裸目标 (全部偶数地址): YES
- `.hword 0x4687` 位于 asm/10 L12937 (`@ 0807fe22 8746`) → 正确表示为代码 (MOV PC,r0), 非数据
- caseD_80 target: 0x0807fea4 → caseD_80 代码体, bl activate_field_spell_neo_daedalus_group_if_placeable @ 0x0807fea8; 逻辑一致

### switchD_080806cc (tick_equip_slot_sprite_display_6state)

- DAT_080806d4 ROM 值: 0x080806d8 ✓ (table ptr)
- 表 start: 0x080806d8; 6 项 (caseD_0..5); 6 unique targets
- 所有 targets 在段内: YES
- 无 THUMB+1 裸目标: YES
- `.hword 0x4687` 位于 asm/10 L14051 (`@ 080806cc 8746`) → 正确为代码

两个 switchD 均已完整 decode; 无 bare-THUMB 目标; 无越界; R4 disasm N/A ✓

---

## §C13 独立清点

```
python 独立扫描 (asm/10 L11932..L14679):
  DAT_ labels: 110
  DWORD_ labels: 13
  PTR_gP1LifePoints_ labels: 6 (proposal 正确标注为 "already symbolized, not counted")
  PTR_DAT_ / UNK_: 0
  Total auto-name (DAT_+DWORD_): 123 = EQ(66)+REF(57) ✓

DWORD_ partition:
  EQ: 5 (a7c=0x197a, a80=0x59c, a84=0x868, a8c=0x5a4, b44=0x868)
  REF: 8 (a78=gDuelPhaseFlags, a88=gP1ChainZoneArray, a90=gP1LifePoints, a94=gDuelPhaseFlags_set_f_flag,
           b48=gDuelFieldSlotState, b4c=gDuelPhaseFlags_set_f_flag, b50=gDuelPhaseFlags, b54=gDuelPhaseFlags_criteria_count)
  Total DWORD_ = 5+8 = 13 ✓

DAT_ partition:
  EQ: 61 (24 unique values 全部命中 eq_values set)
  REF: 49 (15 unique addrs 全部命中 ref_values set)
  Unclassified: 0 ✓
```

---

## §C8 stale FUN_ 详细清单

proposal 报告 5 处, 独立扫描结果 6 处 (段内):

| Line | Stale ref | 所在函数 plate | 当前名 | 状态 |
|------|-----------|--------------|--------|------|
| L11931 | FUN_0807f7bc | get_equip_display_criteria_code_by_card_and_slot pre-plate | fill_equip_criteria_display_code_array | 提案已收录 |
| L12062 | FUN_0807f974 | fill_equip_criteria_display_code_array plate? | check_equip_slot_eligible_with_criteria_and_target | 提案已收录 |
| L12062 | FUN_08080348 | 同上 | check_equip_slot_eligible_with_criteria_and_prerequisites | 提案已收录 |
| L12847 | FUN_0807fde8 | activate_field_spell_neo_daedalus_group_if_placeable plate | dispatch_equip_criteria_display_by_type_code | 提案已收录 |
| L12904 | FUN_08080944 | 同函数 plate | build_equip_criteria_for_target_slots | 提案已收录 |
| **L14644** | **FUN_08081ce8** | **push_to_effect_slot_array plate (fn 0x08080b74 in-seg)** | **tick_equip_effect_slot_display_state** | **提案缺失** |

注: L14675 (FUN_08080c9c) 在 assemble_effect_slot_attr_with_zone_lookup (0x08080ba0, Seg-7 首函数) 的 pre-plate 中, 不属本段修复责任。

---

## §RENAME 备注

DWORD_08080a90 (L14525): proposal RENAME 表中声明 "label already PTR_gP1LifePoints_08080a90", 但当前文件确认该标签仍为 `DWORD_08080a90` (值已符号化为 `gP1LifePoints`). 实际需要的 fixer 动作: rename DWORD_08080a90 → PTR_gP1LifePoints_08080a90。该 action 已包含在 RENAME=13 计数中 (逻辑正确), 但 proposal 中的措辞造成误解。Fixer 须执行 rename, 不能跳过。

---

## 状态: NEEDS_FIX(1 item)

---

## 修改清单

### #1 — C8 — L14644: 补充 FUN_08081ce8 stale FUN_ 修复

**问题**: proposal C8 表遗漏 push_to_effect_slot_array (0x08080b74, in-seg) 的 plate 中 `FUN_08081ce8`。

**当前 asm/10 L14644 内容** (pre-function plate for push_to_effect_slot_array):
```
@ Called by FUN_08081ce8 and related effect node write routines; each call writes one equip effect node slot entry.
```

**要求修复**: 将 `FUN_08081ce8` 替换为其当前名 `tick_equip_effect_slot_display_state` (confirmed: asm/10 L17355).

**修复后应为**:
```
@ Called by tick_equip_effect_slot_display_state and related effect node write routines; each call writes one equip effect node slot entry.
```

**修复方式**: 在 Ghidra 脚本中对 push_to_effect_slot_array (0x08080b74) 追加 `setPlateComment` 更新, 或 fixer 直接在 proposal C8 table 中补充此条目并在落地脚本中执行。

---

**其余所有 C1-C7/C9-C13 均 PASS。无其他阻断项。**

Proposal 主体 (EQ66+REF57=123/C4/C5/C7/C9/C10/C12/C13) 经独立复核全部正确。RENAME=13 的实际操作正确 (含 DWORD_08080a90→PTR_gP1LifePoints_ rename), 仅 proposal 描述措辞略有歧义, 不影响 fixer 落地。

## Reviewer Verdict: F10-Seg-6 = NEEDS_FIX(1 item)
