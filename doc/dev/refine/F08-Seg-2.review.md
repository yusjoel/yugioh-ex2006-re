# Refine Review: F08-Seg-2

> Seg-2 range: ROM `0x0806544c..0x08066448` (~20 fn, 79 slots, 3 ROM_INCBIN + 1 switchD)
> Proposal: `doc/dev/refine/F08-Seg-2.proposal.md`
> Module: `asm/08_equip_oam_neodaed.s`
> Reviewer: independent (python ref-scan + ROM byte read)
> iter-3 re-review (末轮): 2026-06-14

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | 段范围 0x6544c..0x66448 与 §五 路线图 Seg-2 一致; 无跳号/回头 |
| C2 Rule2 | ✅ | 3 ROM_INCBIN 全部分类处理 (R4 disasm); switchD inline (无独立 incbin); §5.1 登记节声明 0 孤儿块 (所有块有引用) |
| C3 Rule3 | ✅ | §5.1 登记为空; 所有块均有引用 (见 ref-scan 详情); 3 块全部判 R4 disasm (有引用) |
| C4 R1 值 | ✅ | 全部 79 槽 ROM 4 字节小端实读验证通过: python struct.unpack_from, 0 mismatches; 含全部 38 CID 槽 + LP delta + stride + global ptr + offset + OAM attr slots |
| C5 R1 复用 | ✅ | **iter-3 决定性按值双向核通过**: 17 New CID 值 grep `0x0*<hex>\b` — 16 值 CLEAN (0 hits); 0x1662 1 hit = CARD_STAT_LP_THRESHOLD_5730 (benign LP-threshold collision, distinct semantic domain, 正确新建 PRECIOUS_CARDS_FROM_BEYOND_CID). 21 Reuse CID 名称+值双向确认全部 PASS (含 iter-2 修正的 CORPSE_OF_YATA_GARASU_CID L816 + EHERO_BUBBLEMAN_CID L686). 无新 C5 失败. |
| C6 R2 名 | ✅ | 槽名模式 `^[a-z][a-z0-9_]+$`; 无重复碰撞 (多个 EQUIP_PHASE_FRAME_OFF 槽各有不同 per-func 后缀); EQUIP_PHASE_FRAME_OFF / OAM_ATTR_P1_SPRITE / LP_EQUIP_DELTA_NEG_1000 命名清晰无歧义 |
| C7 R3 接通 | ✅ | REF_SLOTS 均有 USER-label + DATA-ref 计划; 特别: DAT_08065c50/5c60 (fn+1 指针) + DAT_08065a4c (switchD table) + DWORD_0806622c (dispatch table ptr) 均有明确对应 label |
| C8 R5 现名 | ✅ | Seg-2 asm 范围内 FUN_ 计数: 独立 grep = 10 次 (FUN_08064880 x8 + FUN_080655da x1 + FUN_080712a0 x1); proposal 全部覆盖 (8+1+1=10 substring 替换计划); L4544 两处 FUN_ 位于 0x08066598+ 属 Seg-3 范围, 不计入 Seg-2 |
| C9 ASCII | ✅ | asm Seg-2 行范围 `grep [^\x00-\x7F]` = 0 hits; 全部 ASCII; proposal doc/ 节头为 CJK (允许, doc/ 非 Ghidra plate) |
| C10 carve | N/A | 无 carve 块 (3 块均判 R4 disasm); 不适用 |
| C11 误名 | ✅ | 20 个函数名逐一检查: write_equip_lp_delta_* / restore/submit/set/dispatch/check/tick/drive/enqueue 系列与函数体操作一致; 无矛盾信号 |
| C12 R6 | ✅ | 关键槽 (0xfffffc18/-1000, gDuelPhaseFlags+0x4a4, EQUIP_ACTIVE_CTX_OFF, fn+1 callback, Time Wizard handler table) 均有 file:line 证据和 high 置信度; 无零容忍词 |
| C13 残留 | ✅ | 79 槽全部被 EQ groups A-G + REF_SLOTS 覆盖; 70 DAT_/DWORD_ + 9 PTR_; 无遗漏 |

---

## 状态: PASS

---

## 按值双向核结果 (C5 决定性证据, iter-3)

### 17 New CID 值 — card_info.inc value-grep (`grep -iE '0x0*<hex>\b'`)

| value | proposed_name | value-grep 结果 |
|---|---|---|
| 0x0fb6 | TIME_WIZARD_CID | CLEAN (0 hits) |
| 0x10ef | DRAGON_CAPTURE_JAR_CID | CLEAN (0 hits) |
| 0x1126 | DARK_RABBIT_CID | CLEAN (0 hits) |
| 0x11c2 | SKELENGEL_CID | CLEAN (0 hits) |
| 0x12ca | FLUTE_SUMMONING_DRAGON_CID | CLEAN (0 hits) |
| 0x139f | AIRKNIGHT_PARSHATH_CID | CLEAN (0 hits) |
| 0x1403 | CARD_OF_SAFE_RETURN_CID | CLEAN (0 hits) |
| 0x1533 | DES_LACOODA_CID | CLEAN (0 hits) |
| 0x153b | CALL_OF_THE_MUMMY_CID | CLEAN (0 hits) |
| 0x1572 | HIDDEN_SOLDIER_CID | CLEAN (0 hits) |
| 0x1662 | PRECIOUS_CARDS_FROM_BEYOND_CID | 1 hit: L85 CARD_STAT_LP_THRESHOLD_5730 (benign — LP 阈值非 CID; 独立新建正确) |
| 0x16f7 | MOLTEN_ZOMBIE_CID | CLEAN (0 hits) |
| 0x16fd | DON_TURTLE_CID | CLEAN (0 hits) |
| 0x1748 | AVATAR_OF_THE_POT_CID | CLEAN (0 hits) |
| 0x174e | ATOMIC_FIREFLY_CID | CLEAN (0 hits) |
| 0x19ac | MAGNET_CIRCLE_LV2_CID | CLEAN (0 hits) |
| 0x19c7 | CHAINSAW_INSECT_CID | CLEAN (0 hits) |

结论: 16 值完全 CLEAN; 0x1662 碰撞已知且良性 (不同语义域). 17 New CID 均合法新建.

### 21 Reuse CID — 名称+值双向核 (所有 PASS)

| const_name | value | card_info.inc 行 |
|---|---|---|
| DARK_MAGICIAN_CID | 0x0fc9 | L310 |
| MASKED_SORCERER_CID | 0x1082 | L587 |
| APPROPRIATE_CID | 0x1353 | L621 |
| TOON_MASKED_SORCERER_CID | 0x1563 | L595 |
| HELPING_ROBO_FOR_COMBAT_CID | 0x15dc | L1185 |
| GRANADORA_CID | 0x163f | L516 |
| ROYAL_MAGICAL_LIBRARY_CID | 0x161a | L808 |
| CONTRACT_WITH_EXODIA_CID | 0x165b | L1195 |
| ULTRA_EVOLUTION_PILL_CID | 0x1715 | L962 |
| GOBLIN_THIEF_CID | 0x1761 | L1275 |
| SOLAR_RAY_CID | 0x1767 | L1276 |
| MARSHMALLON_CID | 0x1770 | L192 |
| DARK_MIMIC_LV1_CID | 0x17d5 | L481 |
| CORPSE_OF_YATA_GARASU_CID | 0x1776 | L816 |
| GREED_CID | 0x1802 | L625 |
| SERIAL_SPELL_CID | 0x183e | L991 |
| MECHA_DOG_MARRON_CID | 0x1869 | L538 |
| KING_DRAGUN_CID | 0x1879 | L242 |
| EHERO_BUBBLEMAN_CID | 0x18f9 | L686 |
| CYBER_ARCHFIEND_CID | 0x1911 | L629 |
| BROWW_HUNTSMAN_OF_DARK_WORLD_CID | 0x1966 | L469 |

结论: 21 Reuse CID 全部名称存在且值匹配. CORPSE_OF_YATA_GARASU_CID (iter-2 修正) 和 EHERO_BUBBLEMAN_CID (iter-2 修正) 均已正确归入 Reuse.

---

## iter-2 修正验证 (简核)

| 原 # | 内容 | iter-3 状态 |
|---|---|---|
| #4 | CORPSE_YATA_CID→CORPSE_OF_YATA_GARASU_CID Reuse (L816) | ✅ proposal New 表已删去; Reuse 节已含 "CORPSE_OF_YATA_GARASU_CID (0x1776, L816)"; 值核 L816 OK |
| #5 | ELEMENTAL_HERO_BUBBLEMAN_CID→EHERO_BUBBLEMAN_CID Reuse (L686) | ✅ proposal New 表已删去; Reuse 节已含 "EHERO_BUBBLEMAN_CID (0x18f9, L686)"; 值核 L686 OK |

---

## iter-1 三项已确认修正 (简核通过)

| 原 # | 内容 | iter-3 状态 |
|---|---|---|
| #1 | PLAYER_BLOCK_STRIDE 来源 duel_field.inc → ewram.inc | ✅ proposal Group B: "reuse ewram.inc (L250)" |
| #2 | 8 CID 从 New 移至 Reuse | ✅ 全部 8 个名称在 card_info.inc 独立 grep 确认存在 |
| #3 | BROWW_HUNTSMAN_CID→Reuse L469; SATURN_AGENT/KOZAKY_SDB 从 EQ 表移除 | ✅ 已修正 |

---

## ref-scan 独立结果 (关键证据, 与 iter-1/2 一致)

### Block1 (0x08065d78, 0x3c = 60B)
- raw refs: 1 → 0x09e46328 存 0x08065d79 (fn+1 THUMB ptr, card effect handler table)
- THUMB+1 refs: 1 (同一条目)
- 结论: R4 disasm ✅

### Block2 (0x08065e3c, 0x29c = 668B)
- raw refs (2-step): 34 条, 全部来自 0x8065db4..0x8065e3b 段内 dispatch table (34-entry .word 表)
- THUMB+1 refs (2-step): 0 条
- 结论: R4 disasm ✅

### Block3 (0x080662a4, 0x68 = 104B)
- raw refs (2-step): 5 条 (全部来自 dispatch_equip_chain_state 自身 jump table)
- THUMB+1 refs: 0
- 结论: R4 disasm ✅

### switchD_08065a44
- jump table 0x8065a50 (29 entries); 6 个唯一目标均在函数体内; 内联, 无需 disasm 动作 ✅

---

## EQ 值独立验证抽查

全部 79 槽 python struct.unpack_from 实读, 0 mismatch:
- DAT_08065464=0xfffffe0c ✅ / DAT_08065480=0xfffff830 ✅
- DAT_080654f4=0xfffffc18 ✅ / DAT_08065554=0xfffffc18 ✅
- DAT_08065ae8=0x4a4 ✅ / DAT_08065b58=0x4a4 ✅ / DAT_08065ccc=0x4a4 ✅
- DWORD_08066334=0x8027 ✅ / DAT_08065cbc=0x1d70 ✅
- PTR_gP1LifePoints_* x9: 全部 = 0x0201c4e0 ✅
- DAT_08065c50=0x08065991 ✅ / DAT_08065c60=0x08065991 ✅
- DAT_08065a4c=0x08065a50 ✅ / DWORD_0806622c=0x08066230 ✅
- DWORD_08065d6c=0xfc9 ✅ / DWORD_08066168=0x10ef ✅
- DAT_0806572c=0x1662 ✅ / DAT_080657f8=0x1776 ✅ / DAT_08065824=0x18f9 ✅
- 全部 CID 槽 (38 slots): PASS

---

## Reviewer Verdict: F08-Seg-2 = PASS
