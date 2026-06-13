# Refine Review: F06-Seg-5

Segment: `0x080565e8..0x08057458`, `asm/06_equip_eligibility_b.s` lines 7237..9445 (23 fn, 117 slots)
Proposal: `doc/dev/refine/F06-Seg-5.proposal.md`
Reviewer: independent re-scan (ref-scan / ROM byte verification / ASM grep / card-stats cross-check)
Iteration: 2 (iter-1 NEEDS_FIX(3): #1 C8 stale FUN_ line 7237 / #2 C9 5 CJK plates / #3 C13 4 DWORD_gP1LP missing; fixer mode A applied)

---

## 独立复核方法 (iter-2)

- Python 枚举 ASM label 定义: `^(DAT_|DWORD_|PTR_(?:gP1LifePoints_)?)(08[0-9a-fA-F]{6}):\s*$` grep asm/06, 筛选 [0x080565e8, 0x08057458) => **117 个** (82 DAT_ + 19 DWORD_ + 16 PTR_) 与 proposal 声明完全一致
- C13 穷举对账: 构造 proposal 三表并集 (EQ 94 + REF 23 = 117), 与 117 全集比对 => missing=0, extra=0, overlap=0
- C4 新增槽: 4 个 DWORD_ gP1LP 槽 ROM 字节独立重验 (`struct.unpack_from('<I', rom, addr-0x08000000)`)
- C8: python grep `FUN_[0-9a-fA-F]{8}` lines 7237..9445 => 3 occurrences (lines 7237×1 + 9253×2)
- C9: python grep `[^\x00-\x7F]` lines 7237..9445 => 5 non-ASCII lines (7237/7297/7378/9157/9411)
- C10: fn-ptr 3 槽 ROM 值 + THUMB target code bytes 上轮已验 (iter-1 PASS, 本轮不变)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | Seg-5 = 0x565e8..0x57458; F06-Seg-4 review 确认前段终于 0x565e8; 未跳号/回头 |
| C2 Rule2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 独立 grep 行 7237-9445: 0 incbin, 0 .byte |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无数据块; ref-scan 不适用 |
| C4 R1 值 | EQ slot ROM 4字节小端核对 | PASS | 新增 4 DWORD_gP1LP 槽全部 0x0201c4e0 OK; 其余 iter-1 已验 |
| C5 R1 复用 | 10 新 constants 无现有同值 | PASS | 7 CID + 3 scalar 全部 grep 0 命中 (iter-1) |
| C6 R2 名 | 槽名合规, 无碰撞 | PASS | 后缀 _a/_b/_c/_d 区分同函数多 gP1LP 槽; 格式合规 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | N/A | 无 carve 块 |
| C8 R5 现名 | 所有 plate stale FUN_ 已覆盖 | PASS | iter-2 补 P0(PLATE_SET line 7237: FUN_08057430→现名); P5(PLATE_SUB line 9253: FUN_0805663c/FUN_080563cc→现名); 3 FUN_ 全覆盖 |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | iter-2 补 P0-P4 (PLATE_SET x5): lines 7237/7297/7378/9157/9411; 5 CJK lines 全覆盖; 拟写文本纯 ASCII 核验 OK |
| C10 carve | 指针表条目 +1 THUMB | PASS | 3 fn-ptr ROM 值核对 OK (iter-1); fn-ptr target code bytes push{} 正确 |
| C11 误名 | 函数体操作与函数名一致 | PASS | 23 fn 无矛盾; FUNC_RENAME=0 |
| C12 R6 | 关键槽有 file:line + 置信度, 无零容忍词 | PASS | 5 消费者证据均有 asm/06 行号 + conf: high/med; 无禁用词 |
| C13 残留 | 段内全部 117 槽 100% 覆盖 | PASS | Python 枚举: EQ(94) + REF(23) = 117; missing=0, extra=0, overlap=0 |

---

## 状态: PASS

---

## 附: 独立验证摘要 (iter-2 新增)

**C13 穷举对账**:
- Python 枚举 ASM slot 定义: 117 个 (82 DAT_ + 19 DWORD_ + 16 PTR_)
- Proposal 三表并集: EQ=94 (含 RENAME_as_EQ 3 槽) + REF=23 (16 PTR_gP1LP + 4 DWORD_gP1LP + 3 fn-ptr)
- 合计 117; missing=0; extra=0; overlap=0 => PASS

**4 新增 DWORD_gP1LP 槽 ROM 字节验证 (C4)**:
- 0x0805673c: ROM=0x0201c4e0 = gP1LifePoints OK
- 0x0805678c: ROM=0x0201c4e0 = gP1LifePoints OK
- 0x0805680c: ROM=0x0201c4e0 = gP1LifePoints OK
- 0x08056858: ROM=0x0201c4e0 = gP1LifePoints OK

**C8 stale FUN_ 覆盖确认**:
- line 7237: FUN_08057430 -> tick_equip_activation_lp_cost_sprite_by_type (P0 PLATE_SET)
- line 9253: FUN_0805663c -> tick_equip_activation_with_slot_sprite_mode4 (P5 PLATE_SUB, 函数在 line 7298 确认)
- line 9253: FUN_080563cc -> tick_equip_activation_state_machine (P5 PLATE_SUB, 函数在 line 6902 确认)

**C9 CJK 覆盖确认**:
- line 7237: P0 PLATE_SET (同时消 FUN_) => ASCII 文本纯净
- line 7297: P1 PLATE_SET => ASCII 文本纯净
- line 7378: P2 PLATE_SET => ASCII 文本纯净
- line 9157: P3 PLATE_SET => ASCII 文本纯净
- line 9411: P4 PLATE_SET => ASCII 文本纯净

**gDuelPhaseFlags 实际计数复核**: ROM 扫段范围 = 11 槽 (与 proposal 一致; iter-1 review 提到"12"系拼写误差, 实际 proposal 正文已列 11 条)

---

## Reviewer Verdict: F06-Seg-5 = PASS
