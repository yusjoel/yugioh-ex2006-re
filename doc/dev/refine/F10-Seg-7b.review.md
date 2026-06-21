# Refine Review: F10-Seg-7b

段范围: [0x08081900, 0x08082290), asm 行 16793..17819
Proposal: `doc/dev/refine/F10-Seg-7b.proposal.md`
Reviewer 独立复核日期: 2026-06-21

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 7b=[0x81900,0x82290) 紧接 7a=[0x80ba0,0x81900), 地址序连续无跳号 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ✅ | BLK1(0x82046/0xfa)->R4 disasm; BLK2(0x82158/0x138)->R4 disasm; switchD 已 decoded; §5.1=0 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | 无 §5.1 登记; BLK1 raw=0/THUMB+1=1; BLK2 各 sub raw=1(JT)/THUMB+1 仅压缩数据偶合 -- 自主复核见下 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | 独立 python 核对 47 EQ 槽, 全部 MATCH |
| C5 R1 复用 | 新建 constants 前无现有可复用 | ✅ | 3 NEW CID (0x17f5/0x198e/0x164a) 全 constants/ 0 命中; 11 REUSE CID 现名一一比对 MATCH |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$` | ❌ | `switchD_08081e2c_table_ptr` 含大写 'D' -- 见修改清单 #1 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | BLK1: createFunction route_penguin_soldier_equip_display; BLK2: createFunction 6 sub-stubs; FS table THUMB+1 ref 已有 |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | ✅ | 段内 FUN_ grep: 仅 L16902 1 处 (FUN_08081900), proposal 已列为 C8 fix -> tick_equip_activation_display_3state |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | proposal PLATE 节 ASCII rewrite 列无非 ASCII 字符; asm 现有 13 mojibake 行为待修内容, 非新写入 |
| C10 carve | fn-ptr+1 / .word+1 正确 | ✅ | FS 表 0x09e43428 = 0x08082049 (BLK1 fn+1); BLK2 JT 全 raw 地址(无+1); sub3=4B `movs r0,#0x75; b` 确认 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | ✅ | 12 named fn plates 与函数体一致; FUNC_RENAME=0 合理 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | 消费者证拠节逐槽给出 file:line + confidence:high; 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ❌ | DAT_08081ca8 在 56 个自动名 label 中, 但 EQ 表仅列 41 条 (proposal 称 42), 且未出现在 EQ/RENAME/PTR_skip/disasm 任何分类 -- 见修改清单 #2 |

---

## 自主复核详情

### Ref-scan 独立复核

**BLK1 (0x82046/0xfa -- fn at 0x08082048):**
- python 2-step raw scan: `rom.count(struct.pack('<I', 0x08082048))` = **0 hits** (4-byte aligned scan)
- python 2-step THUMB+1 scan (0x08082049): **1 hit at 0x09e43428** (FS card effect handler table)
- FS entry 0x09e43414 验证: [+0x00]=0x1200 (PENGUIN_SOLDIER_CID), [+0x04]=0x080676e1 (fn_activate), [+0x08]=0x080509fd (fn_eligible), [+0x14]=0x08082049 (fn_routing=BLK1+1)
- 判定: R4 disasm (THUMB fn via FS table) -- CORRECT

**BLK2 sub-stubs (0x82158..0x82290, 6 subs):**
- Jump table at 0x08082140 (6 raw entries): JT[0]=0x08082158, JT[1]=0x08082190, JT[2]=0x080821bc, JT[3]=0x08082214, JT[4]=0x08082218, JT[5]=0x08082240
- 逐 sub raw 引用: sub0..5 各 raw=1 (均来自 JT, 且只有 JT 1 处)
- sub3 (0x08082214) THUMB+1 hit at 0x8d8a9cc: file offset 0xd8a9cc = 压缩卡图数据, 非 FS table entry -- 偶合, 排除
- 判定: R4 disasm (raw-ptr JT dispatch) -- CORRECT; §5.1 为零 -- CORRECT

**ROM byte 核对:** 独立 python 读取 47 个 EQ 槽地址各 4 字节, 全部与 proposal 值匹配 (PASS)

**switchD_08081e2c:** asm 有 caseD_0/1/2/3/default 全 5 标签 (L17526-17644); JT at 0x08081e38: [0]=0x08081e4c, [1]=0x08081e68, [2]=0x08081ec8, [3]=0x08081e98, [4]=0x08081ec8 (case 4=case 2 confirmed) -- already decoded, no R4 action needed

### C13 独立清点

python re 扫 asm/10_equip_effect_dispatch.s (行 1..19983), 范围 [0x8081900,0x8082290):

- `^(DAT_|DWORD_|PTR_|UNK_)[0-9a-fA-F]{8}:` pattern: **51 hits**
- `^PTR_gP1LifePoints_[0-9a-fA-F]{8}:` pattern: **5 hits**
- **总计 56 个自动名 label** (含 DAT_08082158 = BLK2 ROM_INCBIN 基址)

Proposal 残留列表为 55 项 (不含 DAT_08082158). Proposal C13 声称 EQ=42+RENAME=6+PTR_skip=7=55.

**实际比对:**
- EQ 表实际条目数 = **41** (逐行计数)
- 缺失: `DAT_08081ca8` -- ROM值=0x0201b290=gDuelPhaseFlags, 在残留55列表内, 但不在 EQ/RENAME/PTR_skip/disasm 任何分类中
- 总覆盖: 41 EQ + 6 RENAME + 7 PTR_skip + 1 disasm (DAT_08082158) = **55** (未覆盖 DAT_08081ca8 = 1 slot 遗漏)

### CID 核对 (7a 制造疏漏教训: 逐 value 核对)

| slot | value | card_info.inc 现有 name | 比对 |
|------|-------|------------------------|------|
| DAT_08081a00 | 0x17f5 | -- (0 hits) | NEW LEVEL_UP_CID; card-stats.s L21673: "Level Up! slot=0x17F5 pw=25290459" CONFIRMED |
| DAT_08081a04 | 0x169f | PANDEMONIUM_CID | NAME_MATCH |
| DAT_08081a08 | 0x140b | INSECT_IMITATION_CID | NAME_MATCH |
| DAT_08081a10 | 0x164a | -- (0 hits) | NEW GUARDIAN_ELMA_CID; card-stats.s L17110: "Guardian Elma slot=0x164A pw=74367458" CONFIRMED |
| DAT_08081a28 | 0x1745 | THE_KICK_MAN_CID | NAME_MATCH |
| DAT_08081a3c | 0x1768 | NINJITSU_ART_OF_TRANSFORMATION_CID | NAME_MATCH |
| DAT_08081a5c | 0x198e | -- (0 hits) | NEW INFERNO_RECKLESS_SUMMON_CID; card-stats.s L26106: "Inferno Reckless Summon slot=0x198E pw=12247206" CONFIRMED |
| DAT_08081a70 | 0x1927 | SPIRITUAL_EARTH_ART_CID (L976) | NAME_MATCH (L1073 也含 0x1927 但在注释内, 非定义行) |
| DAT_08081a88 | 0x19d8 | TRIAL_OF_THE_PRINCESSES_CID | NAME_MATCH |
| DAT_08081a9c | 0x19dd | GENERATION_SHIFT_CID | NAME_MATCH (7a 新建, 已存在) |
| DAT_08081f7c | 0x17ea | NOBLEMAN_EATER_BUG_CID (L756) | NAME_MATCH |
| DAT_08081f80 | 0x11f0 | GREENKAPPA_CID (L1135) | NAME_MATCH |
| DAT_08081f8c | 0x184a | XING_ZHEN_HU_CID (L538) | NAME_MATCH |
| BLK1 FS entry | 0x1200 | PENGUIN_SOLDIER_CID (L776) | REUSE confirmed (用于 fn name/plate, 非 EQ 槽) |

**板子点 (card names in PLATE text):** L16903 提到 Samsara(0x19da) 为 BST 覆盖的卡, 但 0x19da 不是 literal pool word (python scan 0 hits in range) -- 正确, BST 中间节点可用 inline 立即数.

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单

### #1 — C6 — switchD_08081e2c_table_ptr 名含大写 D, 违反 ^[a-z][a-z0-9_]+$

**现名 (proposal):** `switchD_08081e2c_table_ptr`

**问题:** `switchD` 中的 `D` 为大写, 违反槽名命名规则. 参考 Seg-6 已落地命名:
- `dispatch_criteria_display_switch_table_ptr` (for switchD_0807fe22)
- `tick_equip_6state_switch_table_ptr` (for switchD_080806cc)

**正确名:** `tick_equip_5state_switch_table_ptr`

理由: DAT_08081e34 位于 tick_equip_activation_display_5state 函数体内 (L17510 = 0x08081e10), 与 Seg-6 的 `tick_equip_6state_switch_table_ptr` 命名模式完全一致.

**操作:** proposal RENAME_SLOTS 第 6 项改为:
```
DAT_08081e34 -> tick_equip_5state_switch_table_ptr; EOL: "ptr to switchdataD_08081e38 (5-entry jump table)"
```

---

### #2 — C13 — DAT_08081ca8 未被任何分类覆盖

**slot:** `DAT_08081ca8` (asm L17302)  
**ROM value:** 读取 0x08081ca8 处 4 字节 = `0x0201b290` = gDuelPhaseFlags

**问题:** 该槽出现在 proposal 的 55 个残留自动名列表中, 但未出现在 EQ/RENAME/PTR_skip/disasm 任何分类表. proposal 称 EQ=42, 实际 EQ 表仅 41 条, 差 1 条即此槽.

**正确处理:** 加入 EQ_SLOTS REUSE 表:
```
| DAT_08081ca8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc |
```

**操作:** proposal EQ_SLOTS REUSE 表新增一行, EQ 计数从 41 更正为 42, C13 breakdown 维持 42+6+7=55 (total 56 with disasm DAT_08082158).

---

## 附: 通过项确认

- C1: 地址序 7a→7b 连续, 无跳号
- C2: BLK1/BLK2 均 R4 disasm 计划; switchD 已 decoded; §5.1=0 合理
- C3: 独立 ref-scan 复核 BLK1(raw=0,THUMB+1=1) 和 BLK2(6 subs raw=1 from JT only) -- 判定与 proposal 一致
- C4: 47 EQ 槽 ROM 字节全部 MATCH
- C5: 3 NEW CID 全 constants/ 0 命中; 11 REUSE CID 现名 MATCH; lookup_equip_score_mooyan_p0(0x197) REUSE 合规
- C7: createFunction 计划覆盖 BLK1 fn + 6 BLK2 sub-stubs; FS THUMB+1 ref 在 FS table 中存在
- C8: 1 FUN_ hit at L16902 (FUN_08081900 -> tick_equip_activation_display_3state) 正确识别
- C9: PLATE 节 ASCII rewrite 列纯 ASCII
- C10: BLK1 FS table THUMB+1 ptr (0x08082049) 正确; BLK2 JT raw ptrs 正确; sub3 = `movs r0,#0x75; b` 4-byte stub 确认
- C11: FUNC_RENAME=0 合理; 12 named fn plates 与函数体语义一致
- C12: 消费者证拠节逐槽有 file:line + confidence:high; 无零容忍词
- PTR_gP1LifePoints_*: 5 slots 均 = 0x0201c4e0 = gP1LifePoints (CORRECT)
- DWORD_08081d2c/d98: 均 = 0x0201c4e0 = gP1LifePoints, PTR_skip 正确
- disasm BLK2 coverage: 6 sub-stubs 合计 0x138 bytes = BLK2 total, 无间隙
- sub5 exit: 0xbc02 (pop {r1}) + 0x4708 (bx r1) = Sub-case E confirmed

---

## Reviewer Verdict: F10-Seg-7b = NEEDS_FIX(2 items)
