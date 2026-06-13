# Refine Review: F05-Seg-8

段范围: `0x08050e40..0x08051cc4`, asm/05 lines 17671..19858, 24 fn, 83 slots, 1 ROM_INCBIN

---

## 核验 (C1-C13) — iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | 0x08050e40..0x08051cc4 与 §五 Seg-8 行一致; Seg-7 已完成于 0x08050e40; Seg-9 从 0x08051cc4 接续 |
| C2 | 所有 ROM_INCBIN 有归宿 | PASS | 1 块: 0x08051bfc/0x40 -> §5.1; carve=0, disasm=0 |
| C3 | §5.1 块确 0 引用 | PASS | 独立 2B-step 穷举扫描 [0x08051bfc, 0x08051c3c): raw=0 真实代码引用, THUMB+1=0 真实代码引用; 仅 3 个 0x09xxxxxx 压缩资源偶合 (0x9e404ac/0x9e410c4/0x9c245a9/0x9d8930a) — 排除 |
| C4 | EQ 值 == ROM 4 字节小端 | PASS | 抽查 30+ 槽: PLAYER_BLOCK_STRIDE=0x868 / gDuelFieldSlots=0x0201c510 / gEquipChainSlotRefs=0x0201bb90 / gDuelPhaseFlags 4 槽 / P1LP 2 槽 / 20 CID 槽 / 6 fn-ptr 槽; 全部 OK |
| C5 | 新建常量前无同值碰撞 | PASS (iter-2) | `FIELD5_SCORE_THRESHOLD_999=0x3e7` 已从 duel_field.inc 新建清单移除; 槽 DAT_08051868 改为复用 `CARD_STAT_LP_THRESHOLD_999` (card_info.inc:83); duel_field.inc 新建由 4→3 (仅 SLOT_CARD_TYPE_MASK/ELIGIBLE_A/ELIGIBLE_B); Executor Report 明确标注「reuse CARD_STAT_LP_THRESHOLD_999 for 0x3e7 slot (C5 dedup)」|
| C6 | 槽名合规无碰撞 | PASS | 全部抽查槽 label 符合 `^[a-z][a-z0-9_]+$`; 多槽函数均有 `_a/_b/_stride/_gdfs/_dts/_dpf/…` 后缀区分; 未见重名 |
| C7 | carve/全局槽有 DATA-ref 计划 | PASS | REF 槽 DWORD_08051304 计划 `.word gP1LifePoints`; 6 fn-ptr 槽计划 `.word <fn>+1` |
| C8 | plate 无残留 FUN_ | PASS | 独立 grep lines 17671..19858: 仅 line 19638 有 `FUN_08053704` + `FUN_08054118`; 两处均在 proposal PLATE 清单内。ASCII 板 → substring replace 可行。`gDuelTurnStruct->gEquipChainSlotRefs` prose 修正亦已列出 |
| C9 | plate/EOL 纯 ASCII | PASS | Seg-8 所有 asm plate 行验证无 0x80+ 字节; 18674/18747/18758 行 gDuelTurnStruct 均纯 ASCII; proposal RENAME_SLOTS EOL 文本纯 ASCII |
| C10 | fn-ptr 条目 +1 (THUMB) | PASS | 6 个 fn-ptr 槽均验证为奇地址 (THUMB): 0x080502b1/0x08050a55/0x08052aa9/0x08050995/0x08051b21(×2); 各目标函数首半字均为 push (0xb5xx 系) |
| C11 | 函数名与函数体一致 | PASS | 24 fn 均为 `check_equip_slot_eligible_by_*` / `build_equip_chain_for_*` 形式; 无函数体与名称矛盾。`gDuelTurnStruct` 是 plate 散文误名 (非函数级误名), 已按 gEquipChainSlotRefs 订正 |
| C12 | 关键槽有 file:line 证据 + 置信度 | PASS | 主要常量均有 ewram.inc / card_info.inc 行号引用; med-conf 项 (SLOT_CARD_TYPE_MASK 等) 已标置信度并附 ROM 字节证据; 无零容忍词 |
| C13 | 段内 DAT_ 100% 覆盖 | PASS | 独立 Python set() 枚举所有 83 个槽地址 (stride×25 + gdfs×24 + equip_chain×2 + dpf_group×4 + P1LP_BLOCK2×1 + CID_reuse×7 + CID_new×9 + card_stat_lp×1 + threshold×1 + slot_empty×1 + fn_ptr×6 + REF×1 + RENAME×1 = 83); 与 proposal 声明的 83 一致; C13 PASS |

---

## 附加说明 (非阻断)

1. **EQ=75 报告值与实际 word 槽数不一致**: Executor Report 计 EQ=75 (含 type_mask×3 inline 常量, 未计 9 个新建 CID word 槽)。实际 EQ word 槽约 81, REF=1, RENAME=1 = 83。此为 presentation 问题, 不影响 C13 覆盖。落地时 fixer 按 proposal 各表实际执行即可, 不受 EQ=75 数字约束。

2. **0x08051424/0x08051080 双列**: 出现于「reuse CID」表和「新建 CID」表两处, 属编辑冗余。Python 去重后 83 个唯一地址, 无覆盖缺失。Fixer 按新建处理, 避免重复 equate。

3. **FIELD5_SCORE_THRESHOLD_1999 = 0x7cf**: C5 自检 FIELD5_SCORE_THRESHOLD_1299=0x513 (不同值), 新建无碰撞。

4. **fn-ptr _e/_f 同目标**: 0x080510a4 / 0x080510cc 均 -> 0x08051b21 (check_equip_slot_eligible_by_setcode_and_prereqs+1), 两条独立 dispatch 表条目属正常。

---

## 状态: PASS

---

## Reviewer Verdict: F05-Seg-8 = PASS
