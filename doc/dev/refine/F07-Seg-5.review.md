# Refine Review: F07-Seg-5

段范围: ROM `0x0805fc94..0x08060898` (~34 fn), `asm/07_equip_effect_chain.s`
Proposal: `doc/dev/refine/F07-Seg-5.proposal.md`
活动 doc: `doc/dev/p5-refine-07-equip-effect-chain.md`

---

## iter-2 复核 (2026-06-14)

### Fix #1 (C6/R4 — CID 订正) 独立验证

- `read32(0x09e4159c)` = `0x000015f3` (ROM 字节实测)
- `read32(0x09e415a8)` = `0x080605f1` (fn_ptr = THUMB+1 of 0x080605f0)
- `read32(0x09e415b4)` = `0x000015f4` (Secret Barrel 属下一条 entry，不属本 fn)
- card-stats.s L16252: `card_1249: @ Pineapple Blast  slot=0x15F3  pw=90669991` 确认
- Proposal 现名 `check_equip_slot_eligible_by_monster_zone_type_for_cid_15f3`、Plate 文本均已更正为 Pineapple Blast CID 0x15F3 pw=90669991
- constants/card_info.inc 新建项为 `PINEAPPLE_BLAST_CID = 0x000015f3`，无 SECRET_BARREL_CID 残留
- 结论: **RESOLVED**

### Fix #2 (C2 — Block3/Block4 ref-scan 计数) 独立验证

**Block3 三个子 fn：**

| 子 fn | raw | THUMB+1 | 位置 |
|---|---|---|---|
| F1 0x08060588 | 0 | 1 | 0x09e41560 (CID 0x15f0) |
| F2 0x080605b8 | 0 | 1 | 0x09e41590 (CID 0x15f2) |
| F3 0x080605f0 | 0 | 1 | 0x09e415a8 (CID 0x15f3) |

Proposal Block3 行现写 `raw=0 thumb+1=3 confirmed 0x09e4xxxx entries` — **与实测一致，RESOLVED。**

**Block4 (0x08060800 .byte fn)：**

独立 ref-scan 实测：
- `raw = 3`，位于 0x0817d63e / 0x09b94d43 / 0x09d0e30b，三处均非 4-byte 对齐 → 全部偶发字节序列，与 fn 指针无关
- `THUMB+1 = 22`，详细：
  - 2 处 handler-table 条目，4B 对齐于 `0x09e41638` 和 `0x09e46bd0` — 真实 dispatch table refs
  - 1 处代码 literal pool，4B 对齐于 `0x0813d450` — 直接 bl 调用者内嵌 ldr 字面量
  - 19 处非 4B 对齐 → 全部偶发字节序列

Proposal Block4 行现写 `raw=1(incidental) thumb+1=4(2 table@0x09e41638/0x09e46bd0 + 2 other)` — **数值仍不准确** (raw 应为 3，THUMB+1 应为 22)。

判定 `disasm (R4)` 正确（两个 handler-table 条目充分确认），但 ref-scan 证据栏数字与实测有较大出入。C2 要求"每个块都有归宿 + ref-scan 证据"——分类结论正确，但计数误差达 5-18 倍，属文档精度问题。

**Fix #2: 部分解决。Block3 RESOLVED，Block4 仍有计数偏差。**

### Fix #3 (R2 — Plate 字符数 ≤500) 独立验证

- Block3-F3 (Pineapple Blast) Plate: 399 chars，纯 ASCII — **PASS**
- Block4 (.byte fn) Plate: 466 chars，纯 ASCII — **PASS**

Fix #3: **RESOLVED**

---

## 核验矩阵 (C1-C13) — iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | Seg-5 = 0x5fc94..0x60898，顺接 Seg-4 (0x5f1cc..0x5fc94)，无跳号回头 |
| C2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ❌ | Block4 ref-scan 证据计数错误: proposal 写 raw=1/thumb+1=4, 实测 raw=3/thumb+1=22; 分类 disasm(R4) 正确但证据栏数字不准 |
| C3 | §5.1 块确 0 引用 | ✅ | 无块入 §5.1；所有块均有 THUMB+1 handler-table 引用 |
| C4 | EQ value == ROM 4 字节小端 | ✅ | 53 个槽逐一验证，0 mismatch |
| C5 | 新建 constants 前确无现有可复用 | ✅ | 15 REUSE 均存在，8 NEW 均 0 命中 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`，无碰撞 | ✅ | F3 已改为 cid_15f3；7 个 disasm fn 名均合规，无碰撞 |
| C7 | carve/全局槽有 USER-label + DATA-ref | ✅ | 本段无 REF_SLOTS/carve，不适用 |
| C8 | plate 引用全用现名，无残留旧 `FUN_` | ✅ | 4 处 stale FUN_ 均给出正确现名；Block3-F3 plate 已更正为 PINEAPPLE_BLAST |
| C9 | 所有 plate/EOL 文本纯 ASCII | ✅ | 6 个 disasm plate 均为纯 ASCII；asm 中 17 行 mojibake CJK，提案 P2 节正确识别需重写 |
| C10 | 指针表条目 `+1` 核 | ✅ | 无 carve 指针表，不适用 |
| C11 | 函数体全局 vs 函数名矛盾 | ✅ | 34 named fn 语义一致，无误名信号 |
| C12 | 关键槽语义有 file:line + 置信度，无零容忍词 | ✅ | R6 消费者节各槽均含 asm/07 行号 + confidence:high，无零容忍词 |
| C13 | 段内残留自动名槽 100% 覆盖 | ✅ | Python 清点 53 个 DAT_/DWORD_/PTR_ 标签，与提案完全对应，无遗漏 |

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单

### #1 — C2 — Block4 ref-scan 证据计数仍不准确

**问题：** Proposal 数据块分类表 Block4 行写 `raw=1(incidental) thumb+1=4(2 table@0x09e41638/0x09e46bd0 + 2 other)`，但 reviewer 独立 ref-scan 实测：

- `raw=3`：分别在 0x0817d63e / 0x09b94d43 / 0x09d0e30b，三处均非 4-byte 对齐，全部偶发字节序列
- `THUMB+1=22`：2 个 handler-table 条目 (0x09e41638, 0x09e46bd0 — 4B 对齐) + 1 个代码 literal pool (0x0813d450 — 4B 对齐) + 19 个非 4B 对齐偶发序列

**判定 `disasm (R4)` 不受影响** (两个 handler-table 条目充分确认)。需修正证据文字精度。

**需修改（提案 §数据块分类 Block4 行 ref-scan 列）：**

将：
```
raw=1(incidental) thumb+1=4(2 table@0x09e41638/0x09e46bd0 + 2 other)
```
改为：
```
raw=3(all incidental, non-4B-aligned) thumb+1=22(2 handler-table@0x09e41638/0x09e46bd0 + 1 code-literal@0x0813d450 + 19 incidental non-4B-aligned)
```

---

## 附：iter-1 通过项确认

**C1**: Seg-5 地址序正确，无跳号。

**C3 重跑 ref-scan：**
- Block1 0x0806008c: raw=0, THUMB+1=1 @ 0x09e412c0 (CID 0x159a Reasoning) ✓
- Block2 0x08060386: raw=0, THUMB+1=1 @ 0x09e44290 (CID 0x15dc Helping Robo) ✓
- Block3 F1: raw=0, THUMB+1=1 @ 0x09e41560 (CID 0x15f0 Thunder of Ruler) ✓
- Block3 F2: raw=0, THUMB+1=1 @ 0x09e41590 (CID 0x15f2 Meteorain) ✓
- Block3 F3: raw=0, THUMB+1=1 @ 0x09e415a8 (CID 0x15f3 Pineapple Blast) ✓
- Block4 0x08060800: 2 handler-table refs @ 0x09e41638/0x09e46bd0 确认 (CID 0x1624 Pitch-Black Power Stone) ✓

**C4**: 53 槽全部 python 独立核验，0 mismatch。

**C5**: 8 个 NEW 常量 0 命中（含 PINEAPPLE_BLAST_CID=0x15f3）；REUSE 15 项全在 inc 中存在。

**C8**: 4 处 stale FUN_ 均给出正确现名；无残留 0x15f4 或 SECRET_BARREL。

**C13**: asm Seg-5 范围 53 个自动名标签，提案全覆盖，无遗漏。

---

## Reviewer Verdict: F07-Seg-5 = NEEDS_FIX(1 item)
