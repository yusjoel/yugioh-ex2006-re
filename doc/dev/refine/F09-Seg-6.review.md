# Refine Review: F09-Seg-6

Segment: `[0x08074338, 0x080752cc)`, file `asm/09_equip_lp_display.s`
Proposal: `doc/dev/refine/F09-Seg-6.proposal.md`
Reviewer: independent (no proposal conclusions trusted until re-verified)

---

## Phase 1: Independent Verification Findings

### ref-scan (re-run independently)

**Block1: ROM_INCBIN 0x74852/0x4a — fn_eligible_dimension_jar @ 0x08074854**
- raw=0, THUMB+1=1 (at ROM 0x1e442a0 = GBA 0x09e442a0). Confirmed DISASM.
- FS table structure at 0x1e44290: +0x0c=0x000015dd (CID), +0x10=0x08074855 (fn+1). Verified.
- CID 0x15dd: card-stats.s L16018 `Dimension Jar slot=0x15DD pw=73414375`. CONFIRMED.

**Block2: ROM_INCBIN 0x74914/0xcc — 6 sub-stubs**
- 0x08074914: raw=1 (from dispatch table entry[28] at 0x08074910), THUMB+1=0. DISASM correct.
- 0x08074920: raw=1 (entry[27] at 0x0807490c), THUMB+1=0.
- 0x08074948: raw=1 (entry[26] at 0x08074908), THUMB+1=0.
- 0x08074964: raw=1 (entry[25] at 0x08074904), THUMB+1=0.
- 0x080749b8: raw=1 (entry[0] at 0x080748a0), THUMB+1=0.
- 0x080749d4: raw=24 (entries[1..24] at 0x080748a4..0x080748fc), THUMB+1=0.
All raw references, no THUMB+1. DISASM verdict correct.

**Dispatch table at 0x080748a0 (PTR_DAT_080748a0):**
- All 29 entries confirmed even (raw) from ROM: entries[0..24]=0x080749d4 except entry[0]=0x080749b8, entry[25]=0x08074964, entry[26]=0x08074948, entry[27]=0x08074920, entry[28]=0x08074914. No THUMB+1 needed.
- Pool word at 0x7489c = 0x080748a0 confirmed. This word is OUTSIDE the ROM_INCBIN (incbin ends at 0x7489b, word is at 0x7489c already in asm as plain `.word`).
- Dispatch table raw-ref count: raw=1 (from pool word at 0x7489c). CARVE correct.

**switchD_0807514a:**
- Jump table at 0x08075154, 31 entries (states 0x62..0x80), range check `index <= 0x1e`. All `.word` entries fully decoded in asm, case labels present. No ROM_INCBIN stub; entirely within `dispatch_equip_display_state_by_code`. NO disasm work needed. Proposal assessment correct.

### ROM byte verification (sampled 17 slots)

| Slot | Addr | ROM value | Expected | Match |
|------|------|-----------|----------|-------|
| DAT_08074428 | 0x08074428 | 0x0201b290 | gDuelPhaseFlags | OK |
| DAT_0807442c | 0x0807442c | 0x00000868 | PLAYER_BLOCK_STRIDE | OK |
| DAT_08074430 | 0x08074430 | 0x0201c510 | gDuelFieldSlots | OK |
| DAT_08074434 | 0x08074434 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | OK |
| DAT_08074484 | 0x08074484 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | OK |
| DAT_080744f0 | 0x080744f0 | 0x00000fb6 | EQUIP_ZONE_SPRITE_ATTR | OK |
| DAT_080744f4 | 0x080744f4 | 0x0201e2a0 | gDuelCardCtxBase | OK |
| DWORD_08074a4c | 0x08074a4c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | OK |
| DWORD_08074a50 | 0x08074a50 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | OK |
| DWORD_08074aac | 0x08074aac | 0x08050c59 | fn-ptr THUMB+1 | OK |
| DWORD_08074ab0 | 0x08074ab0 | 0x0201e220 | gEquipLpActivBitmap NEW | OK |
| DWORD_08074ae0 | 0x08074ae0 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | OK |
| DWORD_08074ae4 | 0x08074ae4 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | OK |
| DWORD_08074c88 | 0x08074c88 | 0x0000801b | OAM_EQUIP_SPRITE_TILE_P2_1B | OK |
| DWORD_08074d4c | 0x08074d4c | 0x080507ad | (see C7/C6 issue below) | ISSUE |
| DWORD_080750bc | 0x080750bc | 0x0201e1c8 | gEquipZoneCountTable | OK |
| DWORD_08074a48 | 0x08074a48 | 0x0201c4e0 | gP1LifePoints | OK |

### C5 new-constant verification

- DIMENSION_JAR_CID=0x15dd: grep constants/ for `0x15dd` => 0 hits, `DIMENSION_JAR` => 0 hits. NEW confirmed.
- gEquipLpActivBitmap=0x0201e220: grep constants/ for `0x0201e220` => 0 hits, `gEquipLpActiv` => 0 hits. NEW confirmed.
- All REUSE constants verified by grep: EQUIP_PHASE_FRAME_OFF=0x4a4 (ewram.inc:435), PLAYER_BLOCK_STRIDE=0x868 (ewram.inc:250), EQUIP_ZONE_SPRITE_ATTR=0xfb6 (duel_field.inc:314), LP_CARD_TRACK_BASE_OFF=0x1da8 (ewram.inc:247), LP_CARD_TRACK_NEXT_OFF=0x1daa (ewram.inc:248), ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc:420), ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc:421), OAM_EQUIP_SPRITE_TILE_P2_1B=0x801b (oam_attr.inc:154), gEquipZoneCountTable=0x0201e1c8 (ewram.inc:396), gDuelPhaseFlags=0x0201b290 (ewram.inc:352), gDuelFieldSlots=0x0201c510 (ewram.inc:313), gDuelCardCtxBase=0x0201e2a0 (ewram.inc:218). All confirmed present.

### C13 independent count

Python scan found exactly **65** auto-name labels (`DAT_`/`DWORD_`/`PTR_DAT_`) with addresses in [0x08074338, 0x080752cc). Classification:
- EQ: 55 slots
- REF: 5 slots (4x gP1LifePoints DWORD_ + 1x gEquipLpActivBitmap)
- RENAME: 5 slots (PTR_DAT_080748a0, DAT_08074914, DWORD_08074aac, DWORD_08074d4c, DAT_08075150)
- Total: 65. All classified. **No unclassified residual.**

Note: The proposal's header says EQ=51, which is incorrect (true pure-EQ count is 55). This is an internal counting error in the proposal text. The slot tables do cover all 65 slots; no slot is actually missing. This is a documentation inconsistency, not a coverage gap.

### C8 stale FUN_ scan

Line 14119: `FUN_0807a680` — confirmed as the sole stale FUN_ in Seg-6 (lines 12459..14516). Independent grep found 1 match only.

Proposal fix: replace with `dispatch_equip_sprite_by_zone_or_capacity_guard (0x0807a680 is bl instruction site in asm/10 line 602)`. Verified: asm/10_equip_effect_dispatch.s:583 is function start, L602 contains `bl enqueue_effect_slot_sprite_by_zone_capacity_check @ 0807a680`. Fix text is correct.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | 路线图: Seg-6 0x74338..0x752cc, 2 inc(0x74852/4a, 0x74914/cc) + 1 sw(0x7514a). 完全吻合. |
| C2 Rule2 | 全部 ROM_INCBIN/.byte 块有归宿 | OK | Block1 -> DISASM; Block2 -> DISASM; switchD 已解码无 ROM_INCBIN. PTR_DAT_080748a0 (dispatch table) -> CARVE. |
| C3 Rule3 | §5.1 块确 0 引用 | OK | §5.1=0; 两块均有引用 (Block1 THUMB+1, Block2 raw). |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 随机抽查 15+ 槽全对. |
| C5 R1 复用 | new 常量 0 命中; reuse 常量存在 | OK | DIMENSION_JAR_CID/gEquipLpActivBitmap 各 0 命中. 所有 REUSE 常量经 grep 确认存在. |
| C6 R2 名 | 槽名格式 + 语义正确 | **FAIL** | DWORD_08074d4c 新名 `build_equip_zone_bitmap_predicate_ptr_4d4c` 错误: (1) 值 0x080507ad 是奇数 = THUMB+1, 非 "raw fn-ptr non-THUMB"; (2) 目标函数是 `check_equip_slot_eligible_by_type_query` (0x080507ac in asm/05:16635), 非 `build_equip_zone_bitmap_for_player` (0x080906cc in asm/11:11918). 名称含错误函数名. |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | dispatch table RENAME 有 USER-label `equip_zone_dispatch_table_48a0`; gEquipLpActivBitmap REF 有 DATA-ref 计划; Block1 pool word at 0x7489c 已有 `.word 0x080748a0` in asm, proposal adds label `equip_zone_dispatch_table_48a0_ptr`. |
| C8 R5 现名 | plate 无残留 FUN_ | OK | Seg-6 内仅 1 处 FUN_0807a680, proposal 已给正确修复文本. |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 所有 RENAME EOL strings 均 pure ASCII (经 regex 验证). proposal doc 本体 CJK 在文档说明中, 合法. |
| C10 carve | carve 表条目 .word raw even addr | OK | dispatch table 29 条目均 even (raw). 验证全部 29 条目. 不需 +1. |
| C11 误名 | 函数体全局 vs 函数名矛盾 | NOTE | 无 FUNC_RENAME 需求. 但 DWORD_08074d4c 的 EOL (plate) 也将含 `build_equip_zone_bitmap_for_player` 错误归因, 须一并修正. |
| C12 R6 | 关键槽有 file:line + 置信度证据 | OK | gEquipLpActivBitmap med; DIMENSION_JAR_CID high; fn-ptrs high with asm references. 无零容忍词. |
| C13 残留 | 所有 DAT_/DWORD_/PTR_DAT_ 无遗漏 | OK | 独立 python 计数 65 = 55 EQ + 5 REF + 5 RENAME. 全覆盖. |

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C6 — DWORD_08074d4c fn-ptr 归因错误 (RENAME 槽)

**问题**: 值 `0x080507ad` 是 ODD (bit0=1), 即 THUMB+1, 不是 "raw fn-ptr, non-THUMB"。目标函数地址 = `0x080507ac` = `check_equip_slot_eligible_by_type_query` (asm/05_equip_eligibility_a.s:16635)。`build_equip_zone_bitmap_for_player` 在 asm/11_effect_slot_puzzletext.s:11918 的 0x080906cc。两者完全不同。

**需改**:
1. RENAME_SLOTS 表中 DWORD_08074d4c 的 新名: 将 `build_equip_zone_bitmap_predicate_ptr_4d4c` 改为 `check_equip_slot_eligible_by_type_query_ptr_4d4c` (或语义相近、正确指向 `check_equip_slot_eligible_by_type_query` 的名字)。
2. EOL 改为: `"fn-ptr THUMB+1=0x080507ad for check_equip_slot_eligible_by_type_query (0x080507ac, asm/05:16635); zone pair predicate passed to invoke_count_zone_pair_hits_full_range; tick_equip_display_seq_when_fewer_monster_zones state 0x7f"`
3. 消费者证据表 (R6) 中对应行的 `build_equip_zone_bitmap_for_player raw=0x080507ad` 描述改为 `check_equip_slot_eligible_by_type_query THUMB+1=0x080507ad (parity: odd)`。
4. `tick_equip_display_seq_when_fewer_monster_zones` 函数 plate 中 Constants 行 `ZONE_PAIR_PREDICATE=0x080507ad` 已正确 (无函数名), 不影响 C8, 但如有 `build_equip_zone_bitmap_for_player` 文字引用须同步修正。

**注**: 此错误不影响 ROM 字节 (raw `.word` 值 0x080507ad 本身正确), 但 slot 名和 EOL 含错误函数名, 违反 C6 (R2 名语义正确性)。

### #2 — C13 header count discrepancy (EQ count 内部矛盾)

**问题**: 提案 header 及多处说 EQ=51, 但独立计数 = 55 纯 EQ + 5 REF + 5 RENAME = 65 total。实际纯 EQ 为 55, 不是 51 (4 slots 差距)。所有槽均已分类 (无遗漏), 但 EQ=51 的内部说明是错的。

**需改**: 将提案 §残留自动名槽 小结及 EQ_SLOTS 末尾的 `EQ count = 49`/`EQ=51` 统一改为 `EQ = 55`。同时删除已经混入 EQ_SLOTS 表的 DWORD_08074cdc 行 "REF -- see REF_SLOTS" 标注 (它已在 REF_SLOTS 表中; 不要在 EQ 表里列 REF 槽)。**说明**: 此项不影响 ROM 落地行为, 属提案文本准确性问题; fixer 可在改 #1 时一并订正。

---

## 其他观察 (不阻断 PASS, 供 fixer 参考)

- Pool word at 0x7489c (`equip_zone_dispatch_table_48a0_ptr`) 已在 asm 中以 `.word 0x080748a0` 存在 (line 13174), 提案计划为其加 USER-label。这不在 C13 65-slot 统计内 (无 DAT_ 前缀), 正确。
- DWORD_08074aac RENAME (`check_equip_slot_eligible_bst_filter_ptr_4aac`): 值 0x08050c59 = THUMB+1 of 0x08050c58 = `check_equip_slot_eligible_with_bst_filter` (asm/05:17370). 正确。
- switchD_0807514a 已完全在 asm 中 (`.word` jump table + case labels), 无额外 disasm 工作。提案评估正确。
- gEquipLpActivBitmap=0x0201e220: 3 ROM refs 可独立验证 (0x08074ab0, 0x0809d690, 0x080a3490); med 置信度标注合适。

---

## Reviewer Verdict: F09-Seg-6 = NEEDS_FIX(2 items)
