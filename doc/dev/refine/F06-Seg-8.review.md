# Refine Review: F06-Seg-8

reviewer: independent (no proposal text trusted without re-verification)
date: 2026-06-14 (iter-2)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | PASS | Seg-8 路线图范围 [0x08058cec, 0x08059de0) 正确。Block3 (0x08059cc8) / Block4 (0x08059d14) 均在 Seg-8 内 (都 < 0x08059de0)。executor 正确按实际地址处理, 而非跟随 §三 表格中将 0x59cc8/0x59d14 错列于 Seg-9 的笔误。 |
| C2 Rule2 | PASS | 段内 4 个 ROM_INCBIN 块全部有归宿 (全部 disasm R4)。无静默保留。 |
| C3 Rule3 | PASS | 无 §5.1 块。4 块全有引用 (Block1: THUMB+1 @ 0x09e46fac; Block2: raw x8 from 0x08059568 table + THUMB+1 @ 0x086f4074 内部子函数; Block3: THUMB+1 @ 0x09e451dc; Block4: raw x8 from 0x08059cf4 table)。自主 ref-scan 复核全部一致。 |
| C4 R1 值 | PASS | 独立抽查 23 个 EQ slot ROM 字节, 全部 struct.unpack_from 匹配提案值。两 iter-2 新增槽: 0x08059334=0x0201b290 (gDuelPhaseFlags) OK; 0x080593a0=0x0201e2a0 (gDuelCardCtxBase) OK。 |
| C5 R1 复用 | PASS | ABYSS_SOLDIER_CID=0x1727: grep constants/card_info.inc 无同值 (新建正确)。OP31_EFFECT_NODE_COUNT_CODE=0x13d: grep constants/duel_field.inc 无同值 (新建正确)。lookup_equip_score_mooyan_p1=0x199 已存在 duel_field.inc 中 (正确复用)。 |
| C6 R2 名 | PASS | 所有新建 label 符合 ^[a-z][a-z0-9_]+$ 形式: switchD rename (10 个), equip_type80_dispatch_table_ptr, equip_lp_spell_zone_dispatch_table_ptr, dat_check_atk_buff_predicate_{a,b}, dat_set_equip_mode_fn_ptr_{a,b,c}, dat_equip_target_table_ptr_{a,b}。无碰撞。PTR_gP1LifePoints_ 前缀沿用现有项目约定。 |
| C7 R3 接通 | PASS | 全部 REF_SLOTS 有 USER-label + DATA-ref 计划。fn-ptr 槽 (080593a4/bc, 080597b0, 08059998, 08059acc) 均为 THUMB+1 奇地址, 对应已命名函数, 将用 .word <fn>+1 接通。 |
| C8 R5 现名 | PASS | 穷举扫 [L13320, L15463) FUN_[0-9a-f]{8}: 仅 2 处。L14198 有 FUN_0805934c -> PLATE-3 substring 替换为 tick_equip_banisher_atk_activation_display_seq。L14404 有 FUN_08058550 + CJK mojibake -> PLATE-2 全段 ASCII 重写, 替换为 tick_equip_activation_neo_daedalus_gate。两者函数地址均独立确认。 |
| C9 ASCII | PASS | PLATE-1 文本 493 chars 纯 ASCII。PLATE-2 文本 543 chars 纯 ASCII。PLATE-3 substring replace 输入/输出均 ASCII。Seg-8 内现有 non-ASCII 行仅 2 条 (L13934, L14404), 均在 PLATE-1/PLATE-2 覆盖范围内。 |
| C10 carve | PASS | Block1/Block3 均用 mov pc, r0 (THUMB 0x4687) 分派, 跳转表条目为裸 THUMB 地址 (lsb=0, 无 +1), 行为正确 (THUMB 模式内 MOV PC, Rn 不切换模式)。fn-ptr REF 槽均奇地址 (THUMB+1) 正确。 |
| C11 误名 | PASS | 22 个函数名均语义合理, 无函数体行为与函数名矛盾情形。FUNC_RENAME=0 正确。 |
| C12 R6 | PASS | 关键槽全部有 asm/06_equip_eligibility_b.s:行号 证据 + high 置信度。无零容忍词。 |
| C13 残留 | PASS (iter-2) | 决定性穷举: 自主枚举 asm 段内全部 auto-name 数据槽 118 个 (DWORD_/DAT_/PTR_DAT_/PTR_gP1LifePoints_/PTR_switchdataD_/switchD_table), 与 EQ(93)+REF(21)+RENAME_PHYS(16) 三表并集 (唯一 118) 完全匹配。missing=0, extra=0, overlap自洽。两 iter-2 新增槽 (DAT_08059334/DAT_080593a0) 已正确收入 EQ 表并独立核实 ROM 值。 |

---

## 状态: PASS

---

## 附: iter-1 NEEDS_FIX 修复确认

- **#1 C13**: DAT_08059334 (=0x0201b290, gDuelPhaseFlags) + DAT_080593a0 (=0x0201e2a0, gDuelCardCtxBase) 已追加至 proposal EQ_SLOTS 表, EQ 总计 93→95。
- **C13 穷举净核**: 118 auto-name data slots vs EQ+REF+RENAME_PHYS 并集 118, missing=0, extra=0。三表并集与段内全集完全吻合。

---

## 附: 自主 ref-scan 数据 (C3 原始记录)

| 块 | raw 引用 | THUMB+1 引用 | 引用来源 |
|----|----------|-------------|---------|
| Block1 @ 0x0805953c | 0 | 1 (@ 0x09e46fac) | handler table |
| Block2 @ 0x08059588 | 1 (@ 0x08059568[0]) | 0 | dispatch table 入口 |
| Block2 @ 0x080595d4 | 2 (@ table[2]+[5]) | 0 | dispatch table |
| Block2 @ 0x08059615 | 0 | 1 (@ 0x086f4074) | 外部 THUMB 调用 |
| Block3 @ 0x08059cc8 | 0 | 1 (@ 0x09e451dc) | handler table |
| Block4 @ 0x08059d14 | 3 (@ table[0..2]) | 0 | dispatch table |
| Block4 @ 0x08059dd4 | 2 (@ table[3..4]) | 0 | dispatch table |

所有块均有引用, 无 §5.1 误判。
