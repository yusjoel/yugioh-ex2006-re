# Refine Review: F06-Seg-1

Segment: ROM `[0x080537c0, 0x080541cc)`, asm `asm/06_equip_eligibility_b.s`, 22 fn, 47 slots.
Reviewed against proposal `doc/dev/refine/F06-Seg-1.proposal.md` and active doc `doc/dev/p5-refine-06-equip-eligibility-b.md`.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | roadmap Seg-1: 0x537c0..0x541cc, 22fn, 47slots, 无 ROM_INCBIN — 与 proposal 完全吻合 |
| C2 Rule2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 独立确认: 段内 [0x537c0,0x541cc) 纯 THUMB 代码, 无 ROM_INCBIN/.byte 块. Seg-1 线性函数链无跳转表. |
| C3 Rule3 | §5.1 块确 0 引用 | PASS/NA | 段内无 §5.1 块, 不适用. |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | python `struct.unpack_from('<I', rom, addr-0x08000000)` 全 47 槽核验通过. 含 fn-ptr 0x08053e08=0x0804f551 OK. |
| C5 R1 复用 | 新建常量无同值碰撞 | PASS (iter-2) | `SLOT_SETCODE_A_CLEAR_MASK` 已删 (proposal 0 命中). DAT_080539b4 / DAT_08053ae0 const_name 改为 `SCROLLBAR_CLEAR_BITS_14_6` (gl_scrollbar.inc:line 12 = 0xffff803f, 自核). card_info.inc 仅新建 GRAVEKEEPERS_CANNONHOLDER_CID=0x158c (grep 确认无同值碰撞). |
| C6 R2 名 | 槽名格式合规, 无碰撞 | PASS | 全 47 个 slot_label 均符合 `^[a-z][a-z0-9_]+$`. 无重复 label. |
| C7 R3 接通 | REF 槽有 USER-label + DATA-ref 计划 | PASS | `DAT_08053e08` → `check_equip_slot_eligible_triple_predicate` USER-label, `.word check_equip_slot_eligible_triple_predicate+1`. fn 位于 asm/05:line 13830. ROM ref-scan: 0x0804f551 raw=11 refs (含本槽), 0x0804f550 even=0 refs. C10 THUMB+1 OK. |
| C8 R5 现名 | plate/EOL 全用现名, 无残留 `FUN_` | PASS with note | 段内 lines 1-1481 全穷举 `FUN_[0-9a-f]{8}`: 仅 line 1024 (`FUN_08054e5c`) + line 1482 (`FUN_08054e5c`). 现名 = `check_equip_slot_eligible_by_setcode_prereqs_all_slots` (asm/06:line 3419, addr 0x08054e5c). P2 (line 1024) 属 Seg-1 函数 0x08053ebc; P3 (line 1482) 属 Seg-2 首函数 0x080541cc — 超出 Seg-1 边界, 参见注记. |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 新 plate (P1, 4行) 纯 ASCII 实测. EOL text 纯 ASCII. 现有 asm line 1380 含 CJK mojibake, proposal 正确标记整段 ASCII 重写. |
| C10 carve | 指针表条目 `.word <fn>+1` == ROM raw 值 | PASS | 0x0804f550 THUMB fn, ROM[0x08053e08]=0x0804f551 = fn+1. |
| C11 误名 | 函数名与函数体无矛盾 | PASS | 22 个函数均为 `check_equip_slot_eligible_*` 谓词形式, 返回 bool 0/1; 无全局写与函数名矛盾信号. 无需 FUNC_RENAME. |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | 所有关键槽均有 asm/06:line 证据 + high/med 置信度. DWORD_08054138=0x1706 为 equip_flag 鉴别码 (非 TORPEDO_FISH_CID), med-conf 合理. EQUIP_CTX_PLAYER_OFF=0x0 / EQUIP_CTX_SLOT_REF_OFF=0x1c 有 file:line 证据. 无零容忍词. |
| C13 残留 | 段内所有残留自动名槽全覆盖 | PASS | 47 槽: 19 stride + 19 slots + 2 mask_clear + 1 chain_refs + 1 excl_cid + 1 fn_ptr + 3 phase/chain_arr + 1 RENAME flag = 47. 全部在 [0x537c0, 0x541cc) 内 (无边界泄漏). |

---

## 状态: PASS (iter-2, 2026-06-14)

---

## 修改清单

### #1 — C5 — RESOLVED (iter-2)

`SLOT_SETCODE_A_CLEAR_MASK` 已从 proposal 完全删除 (grep 0 命中). DAT_080539b4 / DAT_08053ae0 均改为复用 `SCROLLBAR_CLEAR_BITS_14_6`. card_info.inc 新建仅剩 `GRAVEKEEPERS_CANNONHOLDER_CID=0x158c` (无碰撞). 统计自洽: EQ 47 槽全覆盖不变.

---

## 附注

### C8 P3 跨段注记 (不阻塞)

P3 (line 1482) 对应函数 `check_equip_slot_eligible_by_side_setcode_prereqs_and_type` 地址 `0x080541cc`, 恰好等于 Seg-1 结束地址 (排他边界), 属 Seg-2 首函数。在 Seg-1 proposal 中提前修订该函数 plate 内的 `FUN_08054e5c` 属跨段提前处理。**不阻塞**: 修订不影响 Seg-1 byte-identical, 且有利于减少 Seg-2 工作量。fixer 可选择在 Seg-1 落地时一并处理 P3, 或推迟至 Seg-2。

### EQUIP_CTX_PLAYER_OFF=0x0 说明 (不阻塞)

新建偏移常量 `EQUIP_CTX_PLAYER_OFF=0x0` 仅用作结构体字段偏移文档化, 不替换任何 DAT_ 字面量池 slot (代码中以即时偏移 `#0x0` 出现)。已确认 constants/*.inc 无同值 `*_OFF=0x0` 常量。在 ewram.inc 中新建此常量合规 (偏移放宽规则允许不同 base 的偏移 0 各建)。

---

## Reviewer Verdict: F06-Seg-1 = PASS
