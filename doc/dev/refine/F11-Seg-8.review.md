# Refine Review: F11-Seg-8

> Reviewer: independent (Reviewer agent)
> Proposal: doc/dev/refine/F11-Seg-8.proposal.md
> Module: asm/11_effect_slot_puzzletext.s [0x08090a78, 0x08091888)
> Date: 2026-06-26

---

## 独立复核步骤

### Phase 1: 自主复核结果

**C13 slot-count 独立 python 枚举 (lines 24989..26884):**

```
python scan of DAT_/DWORD_/PTR_/UNK_ label definitions:
Total: 73 unique labels confirmed
```

完整 73 个标签已列出 (见下方覆盖核查)。

**对比 proposal 覆盖集合:**

Proposal 声称覆盖 73 个地址 (36 EQ_REUSE + 16 EQ_NEW + 16 REF_REUSE + 5 REF_NEW = 73)。
独立核对后发现实际仅覆盖 72 个唯一地址: proposal EQ_NEW 表只列了 15 个槽位, 漏了 1 个。

**缺失槽位:**

```
DAT_08090e84:
    .word  0x000014cc  @ 08090e84 cc140000
```

ROM 读取 `0x08090e84` = `0x000014cc` = `HUNTER_7_WEAPONS_CID` (确认)。
该槽在 `DAT_08090e80` (KINETIC_SOLDIER_CID=0x13aa) 之后紧邻, proposal 列出了 HUNTER_7_WEAPONS_CID
的两个槽 (0x08090cdc, 0x08091060) 但漏了这第三个出现。

**ref-scan 独立核对 (3 个新 REF globals):**

```
gEquipLpScoreBase  (0x0201afe0): raw=68, THUMB+1=0  -- matches proposal
gEquipCandidateSlotA (0x0201bc38): raw=2,  THUMB+1=0  -- matches proposal
gEquipCandidateSlotB (0x0201bc3c): raw=2,  THUMB+1=0  -- matches proposal
```

**ROM 字节核对 (15 个槽抽查):**

```
0x08090cb0: PLAYER_BLOCK_STRIDE    = 0x00000868 -> OK
0x08090cbc: MIRROR_WALL_CID        = 0x00001381 -> OK
0x08090cd0: KINETIC_SOLDIER_CID    = 0x000013aa -> OK
0x08090cdc: HUNTER_7_WEAPONS_CID   = 0x000014cc -> OK
0x08090cf4: STEAMROID_CID          = 0x000018f2 -> OK
0x08091358: SKYSCRAPER_CID         = 0x000018ff -> OK
0x08091388: EQUIP_ATK_SCORE_HI_2499 = 0x000009c3 -> OK
0x080914f8: EQUIP_ATK_SCORE_HI_2500 = 0x000009c4 -> OK
0x080917d0: AMAZONESS_SWORDS_WOMAN_CID = 0x000014a4 -> OK
0x08091850: DIMENSION_WALL_CID     = 0x00001930 -> OK
0x08090b34: gEquipLpScoreBase      = 0x0201afe0 -> OK
0x080917cc: gEquipCandidateSlotA   = 0x0201bc38 -> OK
0x080917e0: gEquipCandidateSlotB   = 0x0201bc3c -> OK
0x08091348: LP_EQUIP_DELTA_NEG_500 = 0xfffffe0c -> OK
0x08090e50: BALLISTA_OF_RAMPART_SMASHING_CID = 0x00001846 -> OK
Missing: DAT_08090e84              = 0x000014cc (HUNTER_7_WEAPONS_CID) -> confirmed
```

**C5 独立 value-grep (8 个新 constants):**

所有 8 个 NEW constants 的值在 `constants/*.inc` 中均为 0 命中 (按值精确匹配, 排除十六进制前缀截断误命中):

```
KINETIC_SOLDIER_CID      (0x13aa): NOT FOUND (OK new)
HUNTER_7_WEAPONS_CID     (0x14cc): NOT FOUND (OK new)
AMAZONESS_SWORDS_WOMAN_CID (0x14a4): NOT FOUND (OK new)
STEAMROID_CID            (0x18f2): NOT FOUND (OK new)
SKYSCRAPER_CID           (0x18ff): NOT FOUND (OK new)
DIMENSION_WALL_CID       (0x1930): NOT FOUND (OK new)
EQUIP_ATK_SCORE_HI_2499  (0x9c3):  NOT FOUND (OK new)
EQUIP_ATK_SCORE_HI_2500  (0x9c4):  NOT FOUND (OK new)
gEquipLpScoreBase        (0x0201afe0): NOT FOUND (OK new)
gEquipCandidateSlotA     (0x0201bc38): NOT FOUND (OK new)
gEquipCandidateSlotB     (0x0201bc3c): NOT FOUND (OK new)
```

**card-stats.s 确认 (6 个新 CID):**

```
KINETIC_SOLDIER_CID      0x13aa: slot=0x13aa FOUND
HUNTER_7_WEAPONS_CID     0x14cc: slot=0x14cc FOUND
AMAZONESS_SWORDS_WOMAN_CID 0x14a4: slot=0x14a4 FOUND
STEAMROID_CID            0x18f2: slot=0x18f2 FOUND
SKYSCRAPER_CID           0x18ff: slot=0x18ff FOUND
DIMENSION_WALL_CID       0x1930: slot=0x1930 FOUND
```

**DIMENSION_WALL 板注修正验证:**

`write_equip_target_score_entry` 在 L26830 执行 `ldr r2, DAT_08091850` 然后 `bl check_value_in_slot_chain`。
`DAT_08091850 = 0x00001930` 经 ROM 字节核实 = Dimension Wall CID (card-stats.s:25144)。
现有板注 (L26649) 写 "Viser Des check" 是错误的, proposal 修正为 DIMENSION_WALL_CID 是正确的。

**REF vs EQ 一致性核查:**

Seg-5/6/7 的 "REF=0" 是因为那些段里 RAM 全局地址已在早期段细化时建立了 USER label (`.word gDuelPhaseFlags` 等),
直接 EQ data-equate 即可导出命名符号。Seg-8 中有 21 个槽的地址值在 GAS 端仍为原始 `.word 0x0201xxxx`,
需要通过 createLabel + addMemoryReference (REF 路径) 建立 Ghidra USER label + DATA ref 才能导出 `.word <global_name>`。
REF 处理与 Seg-7 中 `.word gDuelFieldSlots`/`.word gEquipNodePool` 的已完成结果一致, 路径正确。

**`.byte` / `ROM_INCBIN` 扫描:**

Seg-8 范围 (lines 24989..26884) 内:
- `.byte` 行 (非注释): 0
- `ROM_INCBIN` / `.incbin` 行: 0
- 3 个函数 THUMB+1 ref-scan: raw=0, THUMB+1=0 (均非函数指针目标, 均为 bl 直接调用目标)
- 无隐藏 constant-return stub

**FUN_ 现名核实:**

```
FUN_080afcb4 -> eval_equip_spell_placement_with_score (asm/14:13860) -- OK
FUN_080b04a8 -> eval_fieldspell_equip_placement_full  (asm/14:14937) -- OK
FUN_08091888 -> eval_field_equip_activation_candidates (asm/11:26885) -- OK
FUN_08099314 -> still unnamed (Seg-9 range, not yet refined) -- allowed in plate
```

**Plate ASCII 核对:**

```
Plate 1 (build_equip_candidate_score_table): 417 chars, non-ASCII=0 -- OK
Plate 2 (invoke_):                           300 chars, non-ASCII=0 -- OK
Plate 3 (write_equip_target_score_entry):    446 chars, non-ASCII=0 -- OK
```

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | ✅ | roadmap §三 Seg-8=[0x8090a78,0x8091888); Seg-7 已完成确认 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | ✅ | 0 ROM_INCBIN, 0 .byte-code 行, python 独立扫描确认 |
| C3 Rule3 | §5.1 块 0 引用 | ✅ | 无 §5.1 块 (N/A); 3 函数 THUMB+1=0 独立验证 |
| C4 R1 值 | ROM 4 字节小端核对 | ✅ | 15 个槽抽查全 OK; 缺失槽 DAT_08090e84 值也已确认 |
| C5 R1 复用 | 新建 constants 无现有可复用 | ✅ | 8 个新 CID + 3 个新 RAM globals 均按值 grep = 0 命中 |
| C6 R2 名 | 槽名格式合规, 无碰撞 | ✅ | ptr_g 混合大小写有 file 00 ptr_gIntrTable 先例; 无重名 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | 21 REF 槽均有 createLabel + addMemoryReference 计划 |
| C8 R5 现名 | 板注全用现名, 无残留旧 FUN_ | ✅ | 3 个 plate 无旧名; FUN_08099314 在 Seg-9 未细化故允许 |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | ✅ | 3 个拟写 plate 均 0 non-ASCII, 均 <= 500 chars |
| C10 carve | 无指针表条目 +1 (THUMB) 需核对 | ✅ | 无 carve 计划, 无函数指针表 |
| C11 误名 | 函数名与体无矛盾 | ✅ | 3 个函数名与函数体行为吻合; plate "Viser Des" 修正为 Dimension Wall 正确 |
| C12 R6 | 关键槽有 file:line + 置信度 | ✅ | 7 个关键槽均有 asm/11 行号 + card-stats.s 行号 + conf:high |
| C13 残留 | 段内全部 DAT_ 槽均被覆盖 | **❌** | DAT_08090e84 (0x000014cc=HUNTER_7_WEAPONS_CID) 未在 proposal 中覆盖; 实覆盖 72/73 |

---

## 状态: NEEDS_FIX

---

## 修改清单 (1 项)

### #1 — C13 — DAT_08090e84 遗漏 (必须修复后才能落地)

**位置**: `asm/11_effect_slot_puzzletext.s` L25525

**当前 asm**:
```
DAT_08090e84:
    .word  0x000014cc  @ 08090e84 cc140000
```

**ROM 字节**: `0x08090e84` = `0x000014cc` = `HUNTER_7_WEAPONS_CID` (与 0x08090cdc/0x08091060 同值)

**修复方式**: 在 proposal 的 EQ_NEW 表中, 将 HUNTER_7_WEAPONS_CID 行:

```
| 0x08090cdc, 0x08091060 | 0x000014cc | HUNTER_7_WEAPONS_CID | ...
```

修改为:

```
| 0x08090cdc, 0x08090e84, 0x08091060 | 0x000014cc | HUNTER_7_WEAPONS_CID | ...
```

**C13 Coverage Statement 同步修正**:
- EQ_NEW 从 15 槽改为 16 槽
- 总计仍 36+16+16+5 = 73 (数字与 proposal 声明的 73 相符, 但原 EQ_NEW=16 的声明是错的;
  修正后 EQ_NEW 确实 = 16 个槽位)

**Ghidra 脚本影响**: 落地脚本需增加对 `DAT_08090e84` 的 equate 操作 (`HUNTER_7_WEAPONS_CID, 0x14cc`)。
其余 52 个 EQ 槽处理逻辑不变。

---

## 附注

**REF=21 一致性**: REF 路径 (createLabel + addMemoryReference) 对于 Seg-8 中尚未建立 USER label 的
RAM 全局地址槽是正确处理方式, 与 Seg-7 中已完成的 `.word gDuelFieldSlots` 等输出结果一致。
Seg-5/6/7 REF=0 是因为那些段中所有 RAM 全局在更早的段中已建立了 label, 非处理方式不同。

**Seg-7 活动 doc 状态**: `p5-refine-11-effect-slot-puzzletext.md` §三 表中 Seg-7 仍标 ⬜, 但 Seg-7
实际已完成 (refine-progress.md 记录 + asm 中 0 DAT_ 残留 + `ptr_case_body_f934`/`return_effect_node_result_0/2`
均已落地)。落地 Seg-8 前建议顺手更新活动 doc 中 Seg-7 状态为 ✅。

---

## Reviewer Verdict: F11-Seg-8 = NEEDS_FIX(1 item)
