# Refine Review: F10-Seg-9

**Segment**: [0x08083450, 0x08084318)  
**Proposal**: `doc/dev/refine/F10-Seg-9.proposal.md`  
**Reviewer**: independent C1-C13 self-verification

---

## Phase 1: 自主复核数据

### BLK1 literal pool (executor BLOCKED 求助)

ROM 实测：

| 地址 | ROM 值 | 语义 |
|------|--------|------|
| 0x0808422c | 0x0201b290 | gDuelPhaseFlags (REUSE ewram.inc) |
| 0x08084230 | 0x08084234 | BLK2 JT base 裸 ROM 指针 |

BLK2 JT 条目 6 个全部 ROM 核对 OK（见下节 C10）。

### BLK1 ref-scan 独立重跑

```
THUMB+1 val 0x0808420f  => 全 ROM 0 hits（步长 1）
THUMB+1 val 0x08084211  => 1 hit at GBA 0x09e410b8 (file off 0x1e410b8)
```

dispatch table GBA 0x09e410b8 = 0x08084211，不是 0x0808420f。

**关键：** ROM_INCBIN 起始 0x0808420e 是 2B 零填充对齐 pad；fn_eligible THUMB 代码从 **0x08084210** 开始（opcode 0xb570 = push {r4,r5,r6,lr}），THUMB+1 = **0x08084211**，这才是 dispatch table 里的引用值。Proposal 把 THUMB+1 写成 0x0808420f 是笔误（从块起始而非代码起始算）。

dispatch table 入口结构（0x09e410a4 起，6 word = 0x18B）：

| 偏移 | 值 | 含义 |
|------|----|------|
| +0x00 | 0x00001536 | CID = Book of Life（确认） |
| +0x04 | 0x08072aad | fn_activate+1 |
| +0x08 | 0x00000000 | pad |
| +0x0c | 0x0805fa85 | alt fn+1 |
| +0x10 | 0x00000000 | pad |
| +0x14 | 0x08084211 | fn_eligible+1（=BLK1 fn 起始） |

CID 位于 fn_eligible_ptr 地址 −0x14（非 MEMORY.md 记录的 −0xc）。分类正确（R4 disasm），CID=0x1536 正确。

fn_eligible 代码已完整 ARM 解码：  
state = [gDuelPhaseFlags+0x4b0]；ldr r1,[pc,#8] 指向 0x08084230 = JT base 0x08084234；mov pc,r0 跳至 BLK2 sub-stub。

### ROM 字节核对（采样覆盖所有 EQ 类别）

| 地址 | ROM 值 | Proposal 声明 | 结论 |
|------|--------|---------------|------|
| 0x08083470 | 0x0201b290 | gDuelPhaseFlags | OK |
| 0x080834cc | 0xfffc7fff | EQUIP_NODE_ATTR_CLEAR_MASK | OK（但见 C5） |
| 0x080834d0 | 0x0201e2a0 | gDuelCardCtxBase | OK |
| 0x080835c4 | 0x00000107 | TRIGGER_OP_PARAM_107 | OK |
| 0x0808366c | 0x9e180000 | GEARFRIED_SHIFTED | OK |
| 0x080836b4 | 0x080905e9 | set_equip_act_alt fn-ptr | OK |
| 0x0808390c | 0x00001415 | RED_MOON_BABY_CID | OK |
| 0x08083e70 | 0x00001476 | ANCIENT_LAMP_CID | OK |
| 0x08083e94 | 0x0000148a | DREAMSPRITE_CID | OK |
| 0x080841b0 | 0x00001503 | OTOHIME_CID | OK |
| 0x080841b4 | 0x00001694 | TSUKUYOMI_CID | OK |
| 0x080837e0 | 0x00000109 | INVOKE_OP31_SUB1_PARAM_109 | OK |
| 0x08083d28 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | OK |
| 0x0808411c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | OK |
| 0x080834fc | 0x08081de5 | set_equip_act_mode fn-ptr | OK |
| 0x08083aec | 0x08083969 | check_zone_player fn-ptr | OK |
| 0x08083c18 | 0x08083b55 | check_equip_pair fn-ptr | OK |
| 0x0808411c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF（非 gP1LP）| OK |
| 0x080840e0 | 0x0000ffff | EQUIP_SLOT_SCORE_CAP | OK |

### C5 独立 grep

| 值 | grep 结果 |
|----|-----------|
| 0xfffc7fff / 0xFFFC7FFF | **duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR = 0xFFFC7FFF** |
| 0x00001536 | constants/ 0 hits → NEW |
| 0x00001476 | constants/ 0 hits → NEW |
| 0x0000148a | constants/ 0 hits → NEW |
| 0x00001415 | card_info.inc:1175 RED_MOON_BABY_CID → REUSE |
| 0x0000171f | card_info.inc:395 DNA_TRANSPLANT_CID → REUSE |
| 0x00001503 | card_info.inc:1084 OTOHIME_CID → REUSE |
| 0x00001694 | card_info.inc:1182 TSUKUYOMI_CID → REUSE |
| 0x9e180000 | constants/ 0 hits → NEW |
| 0x000013c3 | card_info.inc:446 GEARFRIED_IRON_KNIGHT_CID → REUSE base |
| 0x00000109 | constants/ 0 hits → NEW |
| 0x00001d40 | constants/ 0 hits → NEW |

**C5 命中：** 0xfffc7fff 已存在为 DUAL_LABEL_RENDER_STATE_CLEAR（duel_field.inc:134）。

### C13 独立清点

Python 扫描 ASM 行 20678~22630（Seg-9 边界）：

```
DAT_:    20
DWORD_:  69
PTR_gP1LifePoints_: 3
Total: 92
```

逐一列表共 92 个标签（脚本输出完整 label 列表已核验）。

Proposal 覆盖集合独立计算：91 个（proposal 合计缺少 DWORD_08083d24）。

**缺失槽：** DWORD_08083d24（ASM line 21898），ROM 值 = 0x0201c4e0 = gP1LifePoints 指针。在 EQ 表 gP1LifePoints 分组中未出现（proposal 的 15 个 gP1LifePoints DWORD_ 仅列 14 个实际地址）。

---

## 核验矩阵 (C1–C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围 [0x83450,0x84318) 与 §五 路线图 Seg-9 一致 | ✅ | |
| C2 Rule2 | 2 ROM_INCBIN 块均有归宿（BLK1=R4 disasm, BLK2=R4 disasm） | ✅ | |
| C3 Rule3 | BLK1 THUMB+1 ref 独立重跑确认 1 hit（0x08084211@0x09e410b8）；BLK2 raw .word x6 | ✅ | 无 §5.1 块 |
| C4 R1 值 | 所有采样 EQ slot 4 字节与 ROM 一致 | ✅ | 见上表 |
| C5 R1 复用 | **0xfffc7fff 已存在 duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR；proposal 误建 NEW EQUIP_NODE_ATTR_CLEAR_MASK** | ❌ | 7 个槽需改为 REUSE DUAL_LABEL_RENDER_STATE_CLEAR |
| C6 R2 名 | 槽名均符合 ^[a-z][a-z0-9_]+$ | ✅ | 注意 label typo 见 C6 备注 |
| C7 R3 接通 | REF_SLOTS 7 个 fn-ptr 均有 USER-label（内联 raw hex+EOL） | ✅ | |
| C8 R5 现名 | 独立 grep `FUN_[0-9a-f]{8}` Seg-9 行：0 hits | ✅ | |
| C9 ASCII | proposal plate/EOL 文本全 ASCII；ASM 中 9 行 CJK（待 plate 替换） | ✅ | 新写内容均 ASCII |
| C10 carve | BLK2 JT 6 条 .word 全部 ROM 核对正确；+1 不适用（raw 地址非 THUMB fn-ptr） | ✅ | |
| C11 误名 | 18 个函数名无矛盾信号；FUNC_RENAME=0 合理 | ✅ | |
| C12 R6 | 关键槽（0xfffc7fff/Gearfried/fn-ptrs/CIDs）均有 file:line + 置信度 | ✅ | |
| C13 残留 | 独立计 92 槽；proposal 仅覆盖 91 槽；**DWORD_08083d24 漏覆盖** | ❌ | 0x08083d24=0x0201c4e0=gP1LifePoints |

---

## 状态: NEEDS_FIX (3 items)

---

## 修改清单

### #1 — C5 — EQUIP_NODE_ATTR_CLEAR_MASK 须 REUSE DUAL_LABEL_RENDER_STATE_CLEAR

**问题：** `constants/duel_field.inc:134` 已有 `DUAL_LABEL_RENDER_STATE_CLEAR = 0xFFFC7FFF`，语义相同（clears bits[17:15]），Seg-7a/8b 在同一模块已 REUSE 此名。Proposal 新建 `EQUIP_NODE_ATTR_CLEAR_MASK = 0xfffc7fff` 违反 C5 按值去重规则（AND mask 是绝对常量，无 *_OFF 例外）。

**修改：** 删除 `EQUIP_NODE_ATTR_CLEAR_MASK` 新建计划。将以下 7 个槽改为 REUSE：

| 槽 | 地址 |
|----|------|
| DAT_080834cc | 0x080834cc |
| DAT_080835c0 | 0x080835c0 |
| DWORD_08083908 | 0x08083908 |
| DWORD_08083a3c | 0x08083a3c |
| DWORD_08083c14 | 0x08083c14 |
| DWORD_08083e6c | 0x08083e6c |
| DWORD_08083fc8 | 0x08083fc8 |

EQ 操作改为：`setEquateReference(addr, "DUAL_LABEL_RENDER_STATE_CLEAR", "duel_field.inc")`。

PLATE 中引用 `EQUIP_NODE_ATTR_CLEAR_MASK` 的文字也全部替换为 `DUAL_LABEL_RENDER_STATE_CLEAR`（影响 tick_equip_activation_sprite_array_4state、tick_equip_lamp_dream_activation_3state 两个 plate）。

### #2 — C13 — DWORD_08083d24 漏覆盖

**问题：** 独立扫描发现 ASM line 21898 有 `DWORD_08083d24`，ROM 值 = 0x0201c4e0 = gP1LifePoints 指针。Proposal 的 EQ gP1LifePoints 分组实际仅列 14 个 DWORD_ 地址（缺此槽），C13 总覆盖 = 91 ≠ 92。

**修改：** 在 EQ 表 gP1LifePoints 分组中补入 DWORD_08083d24：
- addr: 0x08083d24，value: 0x0201c4e0，const_name: gP1LifePoints，slot_label: `gp1_life_points_ptr_08083d24`，C5: REUSE ewram.inc
- gP1LifePoints 分组槽数由 14 → 15，proposal 总计 91 → 92，匹配实际扫描结果。

### #3 — C4（BLK1 pool 0x08084230 悬而未决） + 执行时标签精度

**问题 A：** Proposal BLOCKED 项未解决：BLK1 pool slot at 0x08084230 = 0x08084234（BLK2 JT 基址，裸 ROM 指针）。独立复核已确认此值。Fixer 需为此 pool word 做 EQ/REF 处理：由于 0x08084234 不是 named global 而是 JT 本体的起始地址，建议作为 REF 添加 EOL 注释 `"JT base: book_of_life_eligible state dispatch table start"`，或 createDWord + EOL，不建议新建全局 equate。

**问题 B（标签名精度）：** Proposal EQ 表多处标签名与 ASM 实际不符，影响 Ghidra 脚本正确性：
- Proposal 写 `DWORD_08083580`，ASM 实际是 `DAT_08083580`（line 20847）
- Proposal REF_SLOTS 写 `DWORD_08083836b4`（slot label 列，多了前缀 38），ASM 实际是 `DAT_080836b4`（line 20999）

Fixer 执行脚本时须使用 ASM 实际标签名（`DAT_08083580`、`DAT_080836b4`），否则 `setEquateReference` / `setLabel` 会 not-found 静默失败。

**问题 C（ref-scan 笔误，不影响执行）：** Proposal ref-scan 节写 "THUMB+1 val = 0x0808420f"，实际 dispatch table 存的是 **0x08084211**（fn_eligible 从 0x08084210 起，+1=0x08084211）。disasm plan 本体正确（clearListing 从 0x08084210 起），不影响 fixer 执行，但须在 proposal 中更正此笔误，避免混淆后续核对。

---

## Reviewer Verdict: F10-Seg-9 = NEEDS_FIX(3 items)
