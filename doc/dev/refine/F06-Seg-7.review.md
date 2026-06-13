# Refine Review: F06-Seg-7

## 段信息

- 范围: ROM `0x08058550..0x08058cec`
- 模块: `asm/06_equip_eligibility_b.s`
- 函数: 22 个
- 残留槽: 58 个 (54 DAT_/DWORD_/PTR_08xxx + 4 PTR_gP1LifePoints_08058xxx)
- ROM_INCBIN: 0
- 路线图: `doc/dev/p5-refine-06-equip-eligibility-b.md` §五 Seg-7 行

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致，未跳号/回头 | ✅ | Seg-6 commit 51ebd37 结束于 0x08058550，Seg-7 接续到 0x08058cec；Seg-8 紧随 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ✅ | grep 确认段内 [0x58550,0x58cec) 无任何 ROM_INCBIN；路线图记录的 6 个 incbin 块全部在段外 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ N/A | 无 ROM_INCBIN，无需 ref-scan；C3 trivially 通过 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | 独立 python 验证全部 53 EQ 槽 + 5 REF 槽，共 58 个地址，全部 in_seg=True，ROM 值与 proposal 一致 |
| C5 R1 复用 | 新建前确无现有可复用 | ✅ | CRIMSON_NINJA_CID=0x16b8、LP_BANISHER_CTX_OFF=0x1d70、EQUIP_ACTIVE_CTX_OFF=0x484 均在全 `constants/*.inc` `.equ` 扫描中 0 命中，新建正确；12 个复用常量（含 gDuelPhaseFlags/EQUIP_ACTIVATION_STEP_OFF/gP1LifePoints 等）在对应 inc 中 `.equ` 值完全匹配 |
| C6 R2 名 | 槽名符合规范，无碰撞 | ✅ | 58 个 slot label 全部通过 `^[a-z][a-z0-9_]+$` 检验；无重复 |
| C7 R3 接通 | 5 个 REF 槽有 USER-label + DATA-ref 计划 | ✅ | 5 REF 槽均规划 `.word <fn>+1`（THUMB）；目标函数名已存在于 asm |
| C8 R5 现名 | stale FUN_/CJK 全覆盖 | ✅ | 独立 grep `FUN_[0-9a-f]{8}` 段行范围 L12066-L13293，仅发现 1 处：L12568 `FUN_0805a1dc`，已纳入 P3 ASCII 重写计划；现名 `tick_equip_activation_sprite_mode2_by_type` 在 asm/06 L15868 确认；CJK 非 ASCII 行精确 4 条（L12097/12167/12568/12821），全对应 P1-P4 计划函数 |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | ✅ | P1-P4 重写文本独立检验，437/574/582/542 字符全部 ord<=127 |
| C10 carve | 5 fn-ptr +1 核对 | ✅ | python 验证：0x080586f0→0x08058639（check_equip_slot_has_active_effect_value+1）；0x08058b80/b9c→0x08058a41（check_zone_entity_field6_in_equip_range+1）×2；0x08058c90/ca8→0x08065991（check_equip_activation_at_slot11+1）×2；全部 raw==fn+1 |
| C11 误名 | 函数体操作与函数名矛盾时标 FUNC_RENAME | ✅ N/A | 22 个函数名与函数体一致；proposal 正确报告 FUNC_RENAME=0 |
| C12 R6 | 关键槽语义有 file:line + 置信度，无零容忍词 | ✅ | CRIMSON_NINJA_CID 有 card_stats.s card_1404 坐实 + asm/07 L794；LP_BANISHER_CTX_OFF 有 asm/06 L12605/12924/13172 三处注明；EQUIP_ACTIVE_CTX_OFF 有 asm/06 L12843-12851 + asm/08/09/10 跨模块 4 处；proposal 无零容忍词 |
| C13 残留 | 段内全部残留槽覆盖 | ✅ | python 精确清点段内所有自动名标签：54 个 DAT_/DWORD_/PTR_DAT_/PTR_08xxx + 4 个 PTR_gP1LifePoints_08058xxx = 58 个；proposal EQ(53)+REF(5)=58，100% 覆盖，无遗漏，无越界 |

## 独立复核发现

**ROM_INCBIN 确认 (C2/C3):** 全文件 ROM_INCBIN 地址为 0x5953a/0x59588/0x59cc8/0x59d14/0x5a0aa/0x5a0f8，全部在 [0x58cec, +∞)，段内零块。

**PTR_gP1LifePoints_ 四槽 (C13 关键细节):** ASM 中这 4 个标签（08058958/08058980/080589c0/08058cd4）是 Ghidra 在前期命名阶段部分解析的结果——`.word gP1LifePoints` 值已正确，但 slot label 仍为自动名 PTR_gP1LifePoints_XXXX。Proposal 将其归入 EQ 组（值=gP1LifePoints=0x0201c4e0，ROM 核对 4 处全 OK），需 Ghidra setLabel 改槽名，属正确分类。

**ref count 细节 (非阻塞):** EQUIP_ACTIVE_CTX_OFF=0x484 的 proposal 称"46 ROM refs"。独立计数：4 字节对齐 word 出现 34 次，THUMB+1 1 次，原始字节串 `\x84\x04\x00\x00` 出现 46 次（含非对齐）。Proposal 使用原始字节串计数，与项目 ref-scan 方法一致。

**同值不同语义复用 (C5 偏移放宽):** LP_BAR_ANIM_STATE_OFF(0x4cc)、SPRITE_ROW_ENTRY_DATA_OFF(0x4d4)、CHAIN_NODE_CARD_ARR_OFF(0x4f4) 在 `tick_equip_effect_activation_display_seq` 中分别作为 NODE_COUNT_OFF/NODE_ZONE_OFF/NODE_SLOT_OFF 使用。同值不同语义，但均为 `[gP1LifePoints+offset]` 的偏移，属 ewram 结构体字段偏移的良性碰撞，符合 C5 偏移放宽规则，proposal 注明 EOL 实际用途，正确。

**SPRITE_PARAM 注解 (非阻塞):** asm/06 L12500 现有 ASCII 注释写"SPRITE_PARAM=0x16b8 // attr11 sprite index"，语义描述不精确（应为 card_id）。该注释为 ASCII 非 CJK，不触发 C8 强制重写规则。Proposal 通过槽名 `tick_equip_sprite_attr11_crimson_ninja_cid` 已在语义层面订正，无需额外 FUNC_RENAME。

## 状态: PASS

所有 C1-C13 项无 ❌。

## 修改清单

无 (PASS，无需修改)。

---

Reviewer: refine-reviewer-slim
Date: 2026-06-14
