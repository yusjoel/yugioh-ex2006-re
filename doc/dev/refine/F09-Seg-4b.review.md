# Refine Review: F09-Seg-4b

Range: [0x08072404, 0x08072d20)  
Proposal: doc/dev/refine/F09-Seg-4b.proposal.md  
Reviewer: independent (no executor evidence trusted without self-verification)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | Seg-4 = [0x719fc..0x72d20); Seg-4a 已落地 commit a9aa009 [0x719fc..0x72404); Seg-4b = [0x72404..0x72d20) 连续无跳号 |
| C2 | 每个 ROM_INCBIN 块均有归宿 | ✅ | B5/B6/B7/B8 全部 DISASM；B5 无 DAT_ label (正确，proposal 已说明块前无 auto-name label) |
| C3 | §5.1 块确 0 引用 | ✅ | §5.1=0；所有 4 块均有确认引用 (B5 THUMB+1x1, B6 raw×5+THUMB+1x1, B7 raw×6+THUMB+1x3, B8 raw×6) |
| C4 | 每个 EQ value == ROM 4 字节小端 | ✅ | 独立 python 核对 23 个槽全部一致 |
| C5 | 新建 constants 前确无现有可复用 | ❌ | **VAMPIRE_LADY_CID=0x00001746 已存在于 card_info.inc:602 (REUSE)，proposal 误标 NEW；FIEND_COMEDIAN_CID=0x151d 和 LAST_TURN_CID=0x151e 确为 NEW (0 命中)；LP_DELTA_6000=0x1770 确为 NEW (仅 MARSHMALLON_CID=0x1770 存在于 card_info.inc，不同域，新建合规)** |
| C6 | 槽名格式 `^[a-z][a-z0-9_]+$`，无碰撞 | ✅ | 三个 RENAME label 全符合格式；asm 内 grep=0 确无重名 |
| C7 | carve/全局槽有 USER-label + DATA-ref | ✅ | REF_SLOTS=None；所有 DWORD 均为 literal-pool 常量，无全局指针槽需 USER-label |
| C8 | plate 引用全用现名，无残留 FUN_ | ✅ | grep FUN_[0-9a-fA-F]{8} 在 asm L8116..L8919 = 0 命中 |
| C9 | plate/EOL 文本纯 ASCII | ✅ (条件) | 段内仅 L8872 含 216 字节 CJK (tick_dragon_summon_display_if_monster_zones_occupied)；PLATE-1 计划替换为纯 ASCII，替换后 C9 满足；proposed plate 文本独立核验纯 ASCII (0 非 ASCII 字节) |
| C10 | 指针表条目 fn+1 (THUMB) 核对 | ✅ | B5: [0x09e41078]=0x08072405=0x08072404|1 (python 验证); B6: [0x09e41090]=0x08072541=0x08072540|1; B7: [0x09e43e08/0x09e44930/0x09e45b60] 全=0x080726f5=0x080726f4|1，独立重跑确认 |
| C11 | 函数体全局 vs 函数名矛盾 | ✅ | 11 个命名函数无 FUNC_RENAME；tick_dragon_summon_display_if_monster_zones_occupied 函数体与名吻合 |
| C12 | 关键槽语义有 file:line + 置信度，无零容忍词 | ✅ | Section 8 consumer evidence 含 asm/09 行号 + conf:high；无零容忍词 |
| C13 | 段内所有残留自动名槽 100% 覆盖 | ✅ | python 独立清点：3 DAT_ + 23 DWORD_ = 26 (label definitions)，与 proposal 一致；无 PTR_DAT_/UNK_；全部映射到 EQ/RENAME 三表 |

---

## 独立 ref-scan 复核结果

自主重跑 python ref-scan (raw + THUMB|1，2B-step 穷举)：

**B5 [0x08072404/0x2c]:**
- 0x08072404: raw=0, THUMB+1=1 (align=0) — FS table at ROM[0x1e41078] GBA=0x09e41078, 确为 0x09e4xxxx 区，CID[0x09e41074]=0x0000151d (Fiend Comedian, card-stats.s L14211 pw=81172176) ✅
- 0x08072408: raw=1 (ROM[0x806df] align=3，非 4 字节对齐，压缩数据，废弃) ✅

**B6 [0x08072444/0x138]:**
- 0x08072444/0x0807248a/0x080724ac/0x080724b4/0x08072534: raw=1 各 1 (分别来自 0x72440/0x7243c/0x72438/0x72434/0x72430 dispatch table，ROM 独立核对一致) ✅
- 0x08072540: raw=0, THUMB+1=1 — FS table [0x09e41090]=0x08072541，CID[0x09e4108c]=0x0000151e (Last Turn, card-stats.s L14224 pw=28566710) ✅
- 0x08072510: raw=1 (ROM[0x9ab0b1] align=1，废弃) ✅

**B7 [0x08072594/0x1a0]:**
- 0x08072594/0x080725e8/0x08072624/0x0807264c/0x08072678/0x080726bc: raw=1 各 1 (dispatch table 0x7257c..0x72593，ROM 独立核对一致) ✅
- 0x080726f4: raw=0, THUMB+1=3 — 三个 FS 条目：[0x09e43e04]=0x1522 Vampire Lord, [0x09e4492c]=0x1746 Vampire Lady, [0x09e45b5c]=0x1522 Vampire Lord ✅
- 0x08072606: THUMB+1=1 (ROM[0x1837c01] align=1，废弃) ✅
- 0x08072628: raw=9 (全部在 0x081c5xxx 压缩数据区；align=0 的 1 处 ROM[0x1c5818] 上下文为乱码数据，非指针，废弃) ✅
- 0x08072700: raw=1 (ROM[0x1e7fc23] align=3，废弃) ✅

**B8 [0x0807274c/0x124]:**
- 0x0807274c/0x080727b8/0x080727e4/0x08072804/0x08072848/0x08072856: raw=1 各 1 (dispatch table 0x72734..0x7274b，ROM 独立核对一致) ✅
- THUMB+1=0，无 fn_eligible ✅

---

## 发现问题

### C5 错误：VAMPIRE_LADY_CID 误标 NEW

card_info.inc:602 已存在：
```
.equ VAMPIRE_LADY_CID, 0x00001746  @ Vampire Lady (pw=26495087; card_1521); setup_equip_slot_sprite_attr_by_card dispatch
```

Proposal Section 6 将 VAMPIRE_LADY_CID=0x00001746 标为 NEW 并计划 `card_info.inc +3`，实际应为 `card_info.inc +2` (FIEND_COMEDIAN_CID + LAST_TURN_CID 新建，VAMPIRE_LADY_CID REUSE)。

Executor report 第 430 行 "New constants: card_info.inc +3" 需订正为 `card_info.inc +2`。

EQ slot 映射本身不受影响：proposal Section 3 的 EQ_SLOTS 表未出现 VAMPIRE_LADY_CID 的等值槽（fn_eligible 入口点是 disasm label，不是 literal-pool EQ 槽），故 23 EQ slots 均正确。

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单

### #1 — C5 — VAMPIRE_LADY_CID 改为 REUSE，card_info.inc +3 改为 +2

**位置**: `doc/dev/refine/F09-Seg-4b.proposal.md` Section 6 "card_info.inc additions" 表格。

**当前内容**:
```
| VAMPIRE_LADY_CID | 0x00001746 | Vampire Lady | card-stats.s (pw=26495087); FS table fn_eligible B7; conf:high |
```
并在 C5 dedup 注中标注 "0x00001746: grep constants/ -> 0 hits. NEW confirmed."

**正确内容**:
- VAMPIRE_LADY_CID=0x00001746 已存在于 card_info.inc:602，改为 REUSE，从 NEW 新建列表移除。
- Section 6 card_info.inc additions 改为 +2 (FIEND_COMEDIAN_CID + LAST_TURN_CID)。
- Executor report 结尾 "New constants: card_info.inc +3" 改为 "card_info.inc +2"。
- C5 dedup 注文字更新：将 "0x00001746: grep constants/ -> 0 hits. NEW confirmed." 改为 "0x00001746: grep constants/ -> card_info.inc:602 VAMPIRE_LADY_CID=0x00001746. REUSE confirmed."
- disasm 计划 Section 4 B7 部分已正确写 "VAMPIRE_LORD_CID already exists: card_info.inc:L556" 并提到 fn_eligible 同时处理 VAMPIRE_LADY_CID——fixer 落地时直接 REUSE，无需重建。

**影响范围**: proposal 文本订正；fixer 落地时 B7 fn_eligible 注释/EOL 中直接引用现有名 VAMPIRE_LADY_CID 即可，不新增该行。

---

其他所有 C1-C4/C6-C13 检查均 PASS。EQ 值全部 ROM 字节核验通过，ref-scan 独立重跑结果与 proposal 一致，CJK plate 存在且替换文本为纯 ASCII，无 stale FUN_，C13=26/26 覆盖完整。
