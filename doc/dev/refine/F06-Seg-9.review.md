# Refine Review: F06-Seg-9

Segment: `[0x08059de0, 0x0805b480)` -- `asm/06_equip_eligibility_b.s` lines 15895-18793  
Proposal: `doc/dev/refine/F06-Seg-9.proposal.md`  
Active doc: `doc/dev/p5-refine-06-equip-eligibility-b.md`  
Reviewer date: 2026-06-14 (iter-3, final -- mode-A fix verified)

---

## C1-C13 核验矩阵 (iter-3)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | 路线图 Seg-9: 0x59de0..0x5b480; proposal 一致; Seg-8 (commit 11c409d) 已完成; Seg-10 未开始; 无跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | PASS | Block1 disasm 范围 0x0805a0ac..0x0805a0df (0x34 B); Block2 disasm 0x0805a0f8..0x0805a1db (0xe4 B); 两块均有处理 |
| C3 Rule3 | §5.1 块 确 0 引用 | PASS | §5.1=0; 独立重跑 ref-scan: Block1 fn 0x0805a0ad=2 hits; Block2 raw-ptr 各 1 hit; 无孤儿块 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立 python 核对 20 个新建 CID slot 全 OK (含 SPIRIT_RYU_CID 0x14d7 @ 0x0805a90c); 非 CID 新建常量前轮已核; 全部 OK |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | PASS | **iter-3 独立双向核**: 20 个 new CID 精确值搜索 card_info.inc 全 0 命中 (真新建); 9 reuse-same-name 全确认存在 (name+value 匹配); 2 reuse-diff-name (EQUIP_ZONE_BLOCKER_CID 0x13eb / GROUND_COLLAPSE_FIELD_CARD_ID 0x1432) 存在; 额外 reuse 条目 (SLOT_CARD_EMPTY/FIELD_SPELL_B_EFFECT_ID/DARK_RULER_VANDALGYON_CID/MAKYURA_THE_DESTRUCTOR_CID/BUBBLE_ILLUSION_CID/ANCIENT_GEAR_DRILL_CID/ANCIENT_GEAR_GOLEM_CID/SONIC_JAMMER_CID/AMPLIFIER_CID/JINZO_CID/JUDGEMENT_OF_PHARAOH_CID/PROTECTOR_OF_THE_SANCTUARY_CID/KUNAI_WITH_CHAIN_CID/BLAST_WITH_CHAIN_CID/THE_FIRST_SARCOPHAGUS_CID) 全确认存在; **SPIRIT_RYU_CID (0x14d7): card_info.inc grep=0 确认真新建; 已正确标 (new) 并列为第 20 条新建 CID; card-stats.s L13418 card_1031 Spirit Ryu pw=67957315 坐实**; 零方向误标 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 所有 slot_label 符合格式规范; 同值多槽有行号后缀区分; 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | REF=1 (DWORD_08059e2c -> .word set_equip_activation_state_by_mode_alt+1); PTR_DAT_0805a0e4 -> tick_bonding_photon_state_table 接通完整 |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_ | PASS | 独立穷举: Seg-9 范围 4 行有 FUN_ (L17374/L18216/L18441/L18532); proposal PLATE=7 覆盖全部; 7 个现名 address→label 精确匹配全 OK |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 10 个 proposal 新 plate block 均 ASCII-clean; 当前 asm 内 4 处 CJK mojibake 均在 PLATE 计划覆盖内 |
| C10 carve | 指针表条目 fn-ptr 核对 | PASS | Block2 raw-ptr 模式 (非+1): ref-scan 确认 raw=1 each sub-fn THUMB+1=0; 正确 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 无 FUNC_RENAME; 23 函数名无矛盾 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | Consumer evidence 表 7 个关键槽均有 file:line+confidence; cid_18f5/cid_1684 标 low-conf+seek-help |
| C13 残留 | 段内所有残留自动名槽全覆盖 | PASS | 独立清点: Seg-9 共 147 个自动名 label definitions (146 DAT_/DWORD_ + 1 PTR_DAT_0805a0e4); 与 proposal 数字一致; proposal 覆盖全部 147 (PTR_DAT_0805a0e4 改名为 tick_bonding_photon_state_table); 无遗漏 |

---

## 独立双向核验结果 (iter-3)

### 方向 A: new CID 全部 card_info.inc grep=0 (真新建)

精确值搜索 (0x%08x 格式) 确认 20 个 new CID 全部在 card_info.inc 中无同名无同值:

| value | name | grep 结果 |
|-------|------|---------|
| 0x000014d7 | SPIRIT_RYU_CID | 0 hits (新建) |
| 0x00001390 | ANTI_SPELL_FRAGRANCE_CID | 0 hits (新建) |
| 0x00001944 | LEVEL_MODULATION_CID | 0 hits (新建) |
| 0x000015da | SPELL_CANCELLER_CID | 0 hits (新建) |
| 0x00001910 | MECHANICAL_HOUND_CID | 0 hits (新建) |
| 0x00001722 | INVADER_OF_DARKNESS_CID | 0 hits (新建) |
| 0x00001832 | CREEPING_DOOM_MANTA_CID | 0 hits (新建) |
| 0x00001833 | PITCH_BLACK_WARWOLF_CID | 0 hits (新建) |
| 0x00001834 | MIRAGE_DRAGON_CID | 0 hits (新建) |
| 0x000019bb | ANCIENT_GEAR_CANNON_CID | 0 hits (新建) |
| 0x00001664 | FAIRY_OF_THE_SPRING_CID | 0 hits (新建) |
| 0x000016dd | CURSED_SEAL_FORBIDDEN_SPELL_CID | 0 hits (新建) |
| 0x00001243 | SHADOW_SPELL_CID | 0 hits (新建) |
| 0x00001103 | SPELLBINDING_CIRCLE_CID | 0 hits (新建) |
| 0x00001710 | STRAY_LAMBS_CID | 0 hits (新建) |
| 0x0000173f | AGENT_OF_JUDGMENT_SATURN_CID | 0 hits (新建) |
| 0x000018d3 | IMPENETRABLE_FORMATION_CID | 0 hits (新建) |
| 0x0000150d | SMOKE_GRENADE_OF_THIEF_CID | 0 hits (新建) |
| 0x000015ee | WAVE_MOTION_CANNON_CID | 0 hits (新建) |
| 0x000019d8 | TRIAL_OF_THE_PRINCESSES_CID | 0 hits (新建) |

### 方向 B: reuse CID 全部 card_info.inc grep>0 (真存在)

9 reuse-same-name: COCOON_OF_EVOLUTION_CID/CHAIN_ENERGY_CID/CATHEDRAL_OF_NOBLES_CID/MAGICAL_LABYRINTH_CID/DARK_MAGIC_CURTAIN_CID/SKILL_DRAIN_CID/XING_ZHEN_HU_CID/RARE_METALMORPH_CID/SPARK_BLASTER_CID -- 全部确认存在 (name+value 完全匹配).

2 reuse-diff-name: EQUIP_ZONE_BLOCKER_CID (0x13eb) / GROUND_COLLAPSE_FIELD_CARD_ID (0x1432) -- 均确认存在.

额外 reuse (EQ_SLOTS 表内): SLOT_CARD_EMPTY/FIELD_SPELL_B_EFFECT_ID/DARK_RULER_VANDALGYON_CID/MAKYURA_THE_DESTRUCTOR_CID/BUBBLE_ILLUSION_CID/ANCIENT_GEAR_DRILL_CID/ANCIENT_GEAR_GOLEM_CID/SONIC_JAMMER_CID/AMPLIFIER_CID/JINZO_CID/JUDGEMENT_OF_PHARAOH_CID/PROTECTOR_OF_THE_SANCTUARY_CID/KUNAI_WITH_CHAIN_CID/BLAST_WITH_CHAIN_CID/THE_FIRST_SARCOPHAGUS_CID -- 全部确认存在.

### ROM 字节核对 (iter-3 新 20 个 new CID)

python struct.unpack_from('<I', rom, addr-base) 核对 20/20 OK:
- SPIRIT_RYU_CID: ROM[0x0805a90c]=0x000014d7 OK
- 其余 19 个: 全 OK (见独立运行结果)

### card-stats.s 坐实 SPIRIT_RYU

card-stats.s L13418: `card_1031:  @ Spirit Ryu  slot=0x14D7  pw=67957315` -- 确认为 Spirit Ryu.

---

## 状态: PASS

---

## 附注 (iter-3 最终确认)

**C5 #1 (SPIRIT_RYU_CID)**: 已正确标 `card_info.inc (new)` (EQ_SLOTS 行 172) 且列为第 20 条新建 CID (proposal 行 549). 新建 CID 总数 20 = Executor Report 中 "20 new CID equates" 一致.

**C13 计数细节**: 147 = 146 DAT_/DWORD_ + 1 PTR_DAT_ (PTR_DAT_0805a0e4 @ L16318). 独立清点确认.

**C8 细节**: L18441 的 plate 已由 iter-2 fixer 改写为含现名 (asm 内仍有 FUN_0804c910 等 5 个 stale ref), PLATE 计划覆盖.

**上轮已 PASS 项 (C1/C2/C3/C6/C7/C8/C9/C10/C11/C12) 本轮简核统计自洽, 维持 PASS.**

---

## Reviewer Verdict: F06-Seg-9 = PASS
