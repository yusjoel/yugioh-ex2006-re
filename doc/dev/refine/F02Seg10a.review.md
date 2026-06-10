# Refine Review: F02Seg10a

**Segment**: [0x0803407c, 0x08035280)
**File**: asm/02_text_lp_fieldspell.s  (refine file 03)
**Proposal**: doc/dev/refine/F02Seg10a.proposal.md
**Reviewer date**: 2026-06-11

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 路线图 Seg-10=[0x3407c..0x35f54]; 本 proposal 拆分 10a=[0x3407c..0x35280) / 10b=[0x35280..0x35f54); 符合 §五 "必要时拆 Seg-Na/Nb" 约定。asm 文件确认 10a 起于 line 17842 (eval_slot_target_eligibility_full), 止于 line 20236 (DAT_0803527c), 10b 起于 line 20239 (exit_slot_activation_with_state_write at 0x08035280)。无跳号/回头。 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块均有归宿 | ✅ | Proposal 声明段内无 ROM_INCBIN/.byte 块。asm line 17841-20237 范围内独立确认：0 个 `.incbin`/`.byte` 块。Rule 2 N/A。 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | §5.1 = 0 条（无数据块）。N/A。 |
| C4 R1 值 | EQ value == ROM 小端 4 字节 | ✅ | 自主重读 ROM：Group A 24 槽全 OK；新常量 17 槽全 OK（含 duel_field.inc 5 槽 + card_info.inc 12 槽）；Group B 2 槽全 OK。REF 11 槽全 OK（gP1LifePoints=0x0201c4e0 x10 + fn-ptr=0x0804aea1 x1）。RENAME sample 80 槽全 OK。总计 134 槽独立核对，0 FAIL。 |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | ✅ | 扫全 19 个 constants/*.inc：11 个新名 (ACTIVATION_STATE_A/B_OFF / ACTIVE_EFFECT_CATEGORY_OFF / UMI_CARD_ID / A_LEGENDARY_OCEAN_CARD_ID / SPELL_ZONE_TARGET_CARD_ID / TOTAL_DEFENSE_SHOGUN_CARD_ID / EHERO_RAMPART_BLASTER_CARD_ID / TWINHEADED_BEAST_CARD_ID / TYRANT_DRAGON_CARD_ID / ARMED_SAMURAI_BEN_KEI_CARD_ID) 均无同值已有常量。EQUIP_CHAIN_PAIR_CARD_MAX=0x164f 和 EQUIP_LOCK_B_CID=0x12d1 正确复用 card_info.inc 已有常量。 |
| C6 R2 名 | 槽名格式合规，无碰撞 | ✅ | 148 个 slot_label 全部通过 `^[a-z][a-z0-9_]+$` 正则；0 重复；多同值有 _b/_c/... 后缀。 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | 10 个 PTR_gP1LifePoints_* 槽：已是 Ghidra PTR 类型（gP1LifePoints USER-label + DATA-ref 已存在），proposal 计划纯 slot_label rename。fn-ptr 槽 0x080346c0：ROM 值=0x0804aea1 (THUMB+1 奇地址已确认)，proposal 给 REF label `check_field_spell_slot_placeable_fnptr` + `.word 0x0804aea0+1`。接通计划完整。 |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | ✅ | PLATE=0 (proposal 不写任何 plate)。段内 asm line 17841-20237 仅有 2 处 FUN_ 出现：(1) line 17937 中 `hub FUN_0804074c`——跨模块 caller hub 的标注，非 stale 主语；(2) line 19025 中 `(FUN_080352b0)`——Seg-10b 尚未命名的同文件相邻函数，非 stale 主语。C8 通过。 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | PLATE=0，无 Ghidra plate/EOL 写入。Proposal 文档本身含 16 处 non-ASCII（均为 UTF-8 em-dash `—`，在 markdown 注释文本中，不写入 Ghidra）。符合规则。 |
| C10 carve | 指针表 THUMB fn-ptr +1 | ✅ | 0x080346c0 ROM 值 = 0x0804aea1 (奇，THUMB ptr)。目标函数地址 = 0x0804aea0。proposal 写 `.word 0x0804aea0+1`，正确。 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | ✅ | 10 个函数名逐一核对：eval_/check_/find_ 前缀符合 gate/query 语义；eval_slot_activation_guard_full 是 guard wrapper 而非直接 eval；check_slot_full_activation_eligibility 是 200+ 指令大复合门。无矛盾。FUNC_RENAME=0 合理。 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | Consumer Evidence 表提供：0x1d48 @ 0x0803439e (STR store)、0x1d78 @ 0x08035290 (Seg-10b 引用，合理)、0x10d8 @ 0x08034166 (LDR 6809 独立确认)、fn-ptr @ 0x080346ae (BL f7fe fdb1 独立确认)、0x1368 @ 0x08034206 (CMP)。独立确认指令编码匹配。置信度 high，无零容忍词。 |
| C13 残留 | 段内所有残留自动名槽全覆盖 | ✅ | asm 文件 line 17841-20237：grep 统计 DAT_/PTR_gP1LifePoints_* 共 148 槽（10 PTR + 138 DAT）。Proposal EQ=57 + REF=11 + RENAME=80 = 148。完全覆盖，0 遗漏。 |

---

## 独立 ref-scan 结果

自主 python 重跑（`d.count(struct.pack("<I", val))`）：

| 常量 | 值 | ROM raw refs | proposal 声称 | 一致 |
|------|----|-------------|---------------|------|
| ACTIVATION_STATE_A_OFF | 0x1d48 | 27 | 27 | ✅ |
| ACTIVATION_STATE_B_OFF | 0x1d78 | 41 | 41 | ✅ |
| ACTIVE_EFFECT_CATEGORY_OFF | 0x10d8 | 16 | 16 | ✅ |
| UMI_CARD_ID | 0x10f4 | 31 | 31 | ✅ |
| A_LEGENDARY_OCEAN_CARD_ID | 0x150b | 18 | 18 | ✅ |
| SPELL_ZONE_TARGET_CARD_ID | 0x1368 | 11 | 11 | ✅ |
| TOTAL_DEFENSE_SHOGUN_CARD_ID | 0x12b4 | 5 | 5 | ✅ |
| EHERO_RAMPART_BLASTER_CARD_ID | 0x1956 | 8 | 8 | ✅ |
| TWINHEADED_BEAST_CARD_ID | 0x1723 | 4 | 4 | ✅ |
| TYRANT_DRAGON_CARD_ID | 0x14d5 | 8 | 8 | ✅ |
| ARMED_SAMURAI_BEN_KEI_CARD_ID | 0x186c | 8 | 1 (segment) | ✅ |

注：ARMED_SAMURAI_BEN_KEI ref-scan=8 全 ROM，proposal 写 "1 raw ref; 1 slot"（仅 Seg-10a 内），与全 ROM 8 refs 不矛盾（其余 7 refs 在其他段）。

---

## 卡牌 ID 独立验证 (data/card-stats.s)

通过 passcode→slot_id 映射独立核对 11 个 CID：

| 卡名 | 声称 CID | card-stats slot_id | 一致 |
|------|---------|-------------------|------|
| Umi | 0x10f4 | 0x10f4 (card_2431 pw=22702055) | ✅ |
| A Legendary Ocean | 0x150b | 0x150b (card_3478 pw=295517) | ✅ |
| Total Defense Shogun | 0x12b4 | 0x12b4 (card_2879 pw=75372290) | ✅ |
| EHERO Rampart Blaster | 0x1956 | 0x1956 (card_4577 pw=47737087) | ✅ |
| Twinheaded Beast | 0x1723 | 0x1723 (card_4014 pw=82035781) | ✅ |
| Tyrant Dragon | 0x14d5 | 0x14d5 (card_3424 pw=94568601) | ✅ |
| Armed Samurai Ben Kei | 0x186c | 0x186c (card_4343 pw=84430950) | ✅ |
| Mataza the Zapper | 0x170a | 0x170a (card_3989 pw=22609617) | ✅ |
| Andro Sphinx | 0x17c7 | 0x17c7 (card_4178 pw=15013468) | ✅ |
| Teva | 0x172d | 0x172d (card_4024 pw=16469012) | ✅ |
| Messenger of Peace | 0x134a | 0x134a (card_3029 pw=44656491) | ✅ |

SPELL_ZONE_TARGET_CARD_ID=0x1368：card-stats 中无任何 slot_id=0x1368 的条目（card_1368 = Vilepawn Archfiend 但其 slot_id=0x168C）。Proposal 将其定性为 "effect node type ID, not card stat ID" 正确，用 SPELL_ZONE_TARGET_CARD_ID 命名含义明确（用于 find_paired_zone_entry_for_card 的 cross-player spell-zone 效果节点类型比较）。

0x180d / 0x1813 / 0x195a：copy record 槽，slot_id=0（特殊 token），proposal 用 `_cid_<hex>` RENAME 形式（低语义置信）是正确的降级处理。

---

## 状态: PASS

全部 C1-C13 通过，无修改项。

---

## 修改清单

无。

---

## Reviewer Verdict: F02Seg10a = PASS
