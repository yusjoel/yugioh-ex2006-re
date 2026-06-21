# Refine Review: F10-Seg-4

> Seg-4 [0x0807cd68, 0x0807db20) -- file 10 `asm/10_equip_effect_dispatch.s`
> Reviewer: independent (refine-reviewer agent)
> Date: 2026-06-21

---

## 核验矩阵 (C1-C13)

| #   | 检查                        | 结果 | 备注 |
|-----|-----------------------------|------|------|
| C1  | 段范围与 §五 路线图一致      | ✅   | Seg-4 [0x7cd68, 0x7db20) 与 roadmap 完全匹配；Seg-3 commit 77736c0 已落地；Seg-5 从 0x7db20 开始 |
| C2  | 每个 ROM_INCBIN/.byte 块有归宿 | ✅   | 2×ROM_INCBIN + 1×inline .byte = 3 块：BLK1→R4 disasm, BLK2→R4 disasm, inline→R4 disasm；无静默保留 |
| C3  | §5.1 块确 0 引用             | ✅   | §5.1=0，无登记块。BLK1/BLK2/inline 均有 refs，不进 §5.1 |
| C4  | EQ value == ROM 4 字节小端   | ✅   | 独立验证 27 个 EQ 槽全部 OK（含 TRIGGER_OP_PARAM_139=0x139, gDuelPhaseFlags, LP_BANISHER_CTX_OFF, FEATHER_SHOT_CID 等关键槽） |
| C5  | 新建前无现有可复用           | ✅   | TRIGGER_OP_PARAM_139=0x139 在 constants/*.inc 中 0 命中（grep 0x00000139 + 完整 0x139 前缀）；所有 REUSE 槽按值确认存在 |
| C6  | 槽名 ^[a-z][a-z0-9_]+$，无碰撞 | ✅   | 62 个 slot/stub/pool 标签全部符合命名约束；多同类已加 _a/_b/_b 后缀 |
| C7  | carve/全局槽 USER-label + DATA-ref 有计划 | ✅ | 6 个 REF 槽：check_equip_activation_at_slot11_1 已存于 asm/08 L3691；switchD_0807d126__switchdataD_0807d130 已存于 asm/10 L6957；其余 3 个 _1 标签由 fixer 创建，计划明确 |
| C8  | plate 引用全用现名，无残留 FUN_ | ✅   | grep FUN_[0-9a-f]{8} 在 Seg-4 范围内：0 命中 |
| C9  | ASCII 纯净                   | ✅   | 5 个 plate 文本 + EOL 文本均为纯 ASCII（逐字符验证） |
| C10 | carve 指针表条目 fn+1，ROM 原始值一致 | ✅ | 4 个 fn-ptr REF 槽 ROM 字节验证：check_equip_activation_at_slot11+1=0x08065991, invoke_effect_node+1=0x08090625, check_equip_slot_eligible_bst+1=0x08050a55, check_card_id_is_normal_summon_type+1=0x0804b165 全部 OK；各 base fn 首 hword 均为 THUMB 指令 |
| C11 | 函数体全局 vs 函数名矛盾标 FUNC_RENAME | ✅ | FUNC_RENAME=0，19 函数名与函数体语义核查无矛盾 |
| C12 | 关键槽语义有 file:line + 置信度 | ✅ | TRIGGER_OP_PARAM_139 (asm/10 L7007-7008, high)；FEATHER_SHOT_CID (asm/10 L7599, high)；fn-ptr REF 槽 (asm/05, high)；BLK1/inline CID (FS table ROM 0x09e46220/0x09e42d88, high) |
| C13 | 段内残留自动名槽 100% 覆盖   | ✅   | 独立 ASM grep：53×DAT_/DWORD_ + 6×PTR_ = 59 总标签；proposal: EQ43+REF6+RENAME3+BLK-base1=53 非 PTR_，PTR_ 6 个跳过，59 全部覆盖，无遗漏 |

---

## switchD_0807d126 独立核验

从 ROM 直读 0x0807d130..0x0807d1a0（29×4B 跳转表）：

- 案例范围：case 0x64..0x80（29 个）
- 唯一目标 8 个：0x0807d1a4, 0x0807d1ba, 0x0807d1e0, 0x0807d1f4, 0x0807d22e, 0x0807d260, 0x0807d2d0, 0x0807d2d4
- 全部在 [0x7cd68, 0x7db20) 内：**confirmed**
- 无溢出至 Seg-5：**confirmed**
- 所有目标块在 ASM 中均已 disasm（switchD_0807d126__caseD_* 标签可见，asm/10 L6987-7132 区间）
- Proposal 结论"已解码，无需 R4 行动"正确

---

## 3 disasm 块独立核验

### BLK1: fn_eligible_sillva_warlord_of_dark_world @ 0x0807d7e8 (0x2c B)

- raw=0, THUMB+1=1 at ROM 0x09e46220 → R4 disasm 正确
- CID @ 0x09e4621c = 0x00001968 = SILLVA_WARLORD_OF_DARK_WORLD_CID：verified
- 首 hword 0xb530 = push {r4,r5,lr}：valid THUMB
- 0x4687 at +0x20 (0x0807d808)：**CODE (MOV PC,r0)**，proposal 已正确标注不 createDWord
- Pool 1 @ 0x0807d80c = 0x0201b290 (gDuelPhaseFlags)：verified
- Pool 2 @ 0x0807d810 = 0x0807d814 (Sillva JT base)：verified

### BLK2: sillva_dispatch_stubs @ 0x0807d830 (0xfc B)

- 5 unique sub-stubs；raw refs: A=1, B=1, C=2, D=2, E=1（全部来自 JT @ 0x7d814..0x7d82c）
- THUMB+1=0 for ALL 5 stubs：verified（非 fn_eligible，由 raw JT 访问）
- 0x4687 在 BLK2 中**不存在**：verified
- 覆盖度：0x50+0x18+0x3c+0x4c+0xc = 0xfc，完整覆盖，无残留
- 9 个 pool word 值全部 ROM 核对 OK
- BLK2 range 完全在 Seg-4 内（结束 @ 0x7d92c < 0x7db20）

### inline .byte: fn_eligible_dark_deal @ 0x0807db14 (0xc B)

- raw=0, THUMB+1=1 at ROM 0x09e42d88 → R4 disasm 正确
- CID @ 0x09e42d84 = 0x00001975 = DARK_DEAL_CID：verified
- 字节序列 `20200a791043087100207047`：ROM 精确匹配
- 结束于 0x0807db20 = Seg-4 边界：**confirmed，刚好到边**，无越界

---

## C5 新常量独立核验

- `TRIGGER_OP_PARAM_139 = 0x00000139`：grep `0x00000139` → 0 命中；grep `0x139` 命中的均为 CID/不同语义（0x1399, 0x1390, 0x139f, 0x139d）；该值确实是 NEW，无碰撞
- 消费者证据：asm/10 L7007 `ldr r1, DAT_0807d1d8` + L7008 `bl trigger_card_display_op31_if_not_active`；语义为第 2 参数；置信度 high
- 与 TRIGGER_OP_PARAM_107=0x107 值域不同（0x107 vs 0x139），属同族不同参数，各建 .equ 正确

---

## C13 独立计数 vs 提案

| 来源 | 数量 |
|------|------|
| 独立 grep 段内 DAT_/DWORD_ 标签 | 53 |
| 独立 grep 段内 PTR_ 标签 | 6 |
| **总计** | **59** |

提案：EQ43 + REF6 + RENAME3 + BLK-base1 = 53 非 PTR_ + 6 PTR_ = 59。完全匹配。

> 注：提案 header 文本写"50 DAT_/DWORD_"属内部计算笔误，但 C13 reconciliation 节正确核算为 52 非 BLK-base + 1 BLK-base = 53。无实质错误。

---

## 轻微文本问题（不影响落地，不构成 NEEDS_FIX）

1. **提案 header** 第 4 行"50 DAT_/DWORD_ auto-names"：实为 52（43 EQ + 6 REF + 3 RENAME），header 与 C13 节不一致。C13 节正确。fixer 落地时无需额外动作。
2. **EQ_SLOTS 表格** 标注 DAT_0807d12c 为 EQ row 但备注"see REF_SLOTS"——实质是 REF，表中有标注说明，不影响落地。

---

## 状态: PASS

所有 C1-C13 项目均通过，无 NEEDS_FIX 项。Fixer 可直接进入模式 B 落地。

---

## 落地要点提醒（供 fixer 参考）

1. BLK1 @ +0x20 (0x0807d808) = `0x4687` = THUMB `MOV PC,r0` 指令，**不** createDWord。
2. BLK2 无 0x4687，安全 createDWord 9 个 pool words。
3. 3 个 REF_SLOT 需 fixer 新建 Ghidra USER-label：`invoke_effect_node_with_active_flag_3arg_1`、`check_equip_slot_eligible_by_card_id_bst_1`、`check_card_id_is_normal_summon_type_1`。
4. TRIGGER_OP_PARAM_139 插入 duel_field.inc TRIGGER_OP_PARAM_107 行之后。
5. inline .byte 结束于 0x7db20，DisassembleCommand 范围 [0x0807db14, 0x0807db20)。
6. 落地后 build 必须 byte-identical SHA1 9689337d。
