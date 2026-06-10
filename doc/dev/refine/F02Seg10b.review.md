# Refine Review: F02Seg10b

Segment: `[0x08035280, 0x08035f54)` — 7 functions, 98 residual slots, file 02 final segment.

## Round 1 verdict: NEEDS_FIX (C6 — REF slot label `exit_slot_act_gDuelCardCtxBase` contained uppercase)
## Round 2 (re-review after fixer mode-A): applied fix verified below.

---

## 核验 (C1-C13) — Round 2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | Seg-10b = 0x35280..0x35f54, 接 Seg-10a; 0x35f54 == file 02 上界; 段号无跳号/回头 |
| C2 Rule2 | ROM_INCBIN/.byte 块均有归宿 | ✅ | 段内零 ROM_INCBIN/.byte 块, proposal 正确 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ N/A | 无 §5.1 块需 ref-scan |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | 抽查 7 个关键槽 (0x080352a4/0x080352ac/0x080356d0/0x08035e4c/0x08035944/0x08035ca8/0x08035f40) 全部与 ROM 小端字节吻合; 98 槽 Round 1 已全核无新回归 |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | ✅ | 新增阈值 0x0000076b/0x0000063f 在 constants/*.inc 无同值已有常量 (grep 零命中); Round 1 53 equate 去重结论无变更 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | **修正已应用**: REF 槽 label 由 `exit_slot_act_gDuelCardCtxBase` → `exit_slot_act_dctxbase` (全小写); proposal 两处出现 (L244/L256) 均已更新; 表格全量扫描无任何大写残留 (python 正则 `[A-Z]` 零命中); 无标签碰撞 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | ✅ | REF 槽 0x080352a4 → gDuelCardCtxBase (ewram.inc 已有) + DATA-ref 计划; PTR_gP1LifePoints_080352a8 已有 DATA-ref, 仅 RENAME |
| C8 R5 现名 | plate 引用全用现名, 无残留 `FUN_` | ✅ | 两个拟 ASCII plate 均无 FUN_; 所有引用函数名存在于 asm 中 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | 全文件 python `ord(c)>127` 零命中; 全部 ASCII |
| C10 carve | fn-ptr 表条目 `+1` | ✅ N/A | 段内无 fn-ptr 表 |
| C11 误名 | 函数体全局与名矛盾时已标 FUNC_RENAME | ✅ | 7 fn 名无矛盾; EHERO_WILDEDGE_CID=0x1958 与现有常量值不同, 无碰撞 |
| C12 R6 | 关键槽语义有 file:line 证据 + 置信度 | ✅ | 6 个关键槽均有 asm line 引用 + high/low 置信度; 0x1221 明确标 low conf + 理由 |
| C13 残留 | 段内所有残留自动名槽全部覆盖 | ✅ | 98 slots = REF(1) + RENAME(3) + EQ_REUSE(28) + EQ_NEW(66) = 98; 无遗漏 |

---

## 状态: PASS

所有 C1-C13 均 ✅。唯一 Round 1 缺陷 (C6 label 含大写) 已由 fixer 正确修复。

---

## 附注 (不阻塞, 供参考)

1. **EQ_REUSE 计数修正已验证**: proposal 章节头 "EQ_REUSE: 28 slots" 与表格实有 28 行一致 (Round 1 报告的不一致已修正)。

2. **plate 字符数**: refine 阶段不适用 analysis-loop 500-char 评分门槛, 不阻塞。

3. **HAMON_LORD_CID_SHIFTED 数学**: `0x19a4 << 19 = 0xcd200000` 已 ROM 字节核对确认 (slot 0x08035944 = 0xcd200000 ✅)。

4. **0x1221 unknown CID**: 低置信 label `eval_fsact_unknown_cid_1221` 合规; card-stats.s 确认无 slot=0x1221 条目。
