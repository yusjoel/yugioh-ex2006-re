# Refine Review: F11-Seg-4a

Segment: `[0x08087d58, 0x08088904)` — 0xBAC = 2988 bytes  
Proposal: `doc/dev/refine/F11-Seg-4a.proposal.md`  
Source: `asm/11_effect_slot_puzzletext.s` line 6089 (`ROM_INCBIN 0x87d58, 0x5a9c`)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | Seg 范围与路线图一致 | PASS | roadmap §五 明确 Seg-4a = `[0x08087d58, 0x08088904)` — 完全匹配 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | FAIL | fn07 dispatch table 实有 6 entries, 提案仅列 5 (漏 entry[29] = UFO Turtle CID=0x1335) |
| C3 | §5.1 块确 0 引用 | N/A | 本段无 §5.1 |
| C4 | EQ value == ROM 4 字节小端 | FAIL | (a) fn06 size 写 168 bytes, 实际 `0x080880c0-0x08088058=0x68=104 bytes`; (b) fn19 描述误称 degenerate 0x080887ec "at end of fn19", 实际在 fn20; (c) fn21 CONTRACT_WITH_EXODIA_CID 写 card_1310, 实际 card_1331 |
| C5 | 新建 constants 前确无现有可复用 | FAIL | 11 个声称 NEW 的 CID 在 card_info.inc 已存在 (见修改清单 #3) |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 21 个函数名全合规, 无重复 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | FAIL | REF=0 声明但 ~36 个 EWRAM 指针池 DWord (gP1LifePoints x18, gP1SlotSetCodeArray x8 等) 无 DATA-ref 计划, 将以 raw hex 导出; 0x0201e278 (fn16 pool) 不在 ewram.inc 且无新 equate 计划 |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | proposal 全文无 FUN_ |
| C9 | ASCII 检查 | PASS | 所有 plate 文本纯 ASCII; doc 标题中的 `§` (U+00A7) 仅为 markdown section 标记, 不进入 Ghidra |
| C10 | 指针表条目 +1 (THUMB) | PASS | 自查: fn21 BST 13 个 pool DWord 全与 ROM 字节一致 (python 验证); fn09 pool (0x15b6/0x15b7/0x0201c4e0/0x00000868) 全正确 |
| C11 | 函数体全局 vs 函数名矛盾 | PASS | 抽查 fn07/fn11/fn16/fn21: MOVS R1 arg 与 substate 后缀完全吻合; 所有函数调用 write_equip_zone_entry_by_substate (BL 目标 0x0808d88c 逐 fn 验证) |
| C12 R6 | 关键槽语义有 file:line 证据 | PASS | 分派表地址 0x09e5a128 引用的 dispatch_equip_zone_write_by_substate_range 在 asm/11 L6100 确认; write_equip_zone_entry_by_substate 0x0808d88c 确认; 置信度高 |
| C13 | 段内残留 DAT_ 全覆盖 | PASS | 21 fn 起止地址连续无间隙: 修正 fn06=104B 后 sum=2988=segment 大小; 后处理 gate (grep `ROM_INCBIN\|\.byte` ==0) 已在提案中指定 |

**关键自查数据**:

```
反向扫描所有 6 strong degenerate THUMB+1 引用位置:
  0x08088354 -> 0x08f38b54 (ROM offset > 0x082d4000, 压缩数据)
  0x08088394 -> 0x08a6f1e0 (压缩数据); BL pair 0xf7c2/0xfcd9 @0x08088392/0x08088394 解码 target=0x0804ad48 ✓
  0x0808855a -> 0x086ba9f4 (压缩数据); halfword=0x005b (lsls r3,r3,#1, 非 prologue) ✓
  0x0808866c -> 0x08eb8328 (压缩数据); halfword=0x1852 (adds r2,r2,r1, 非 prologue) ✓
  0x080887ec -> 0x08af13f8 (压缩数据); halfword=0x2816 (cmp r0,#0x16, 非 prologue) ✓
  0x08088080 -> 0x0878ab58 (压缩数据); halfword=0x00c0 (lsls r0,r0,#3, 非 prologue) ✓
  
21 个真实函数首字节: 全部 0xb5xx (push LR) ✓
fn01 pool @0x08087d94=0x0201c4e0, @0x08087d98=0x00000868 — ROM bytes 确认 ✓
fn21 pool 13 条全部 ROM bytes 匹配 ✓
substate 验证: fn01→0xd@0x08087d7a, fn02→0xe@0x08087dc0/0xdea, fn11→0xb@0x0808834a,
  fn16→0xb@0x080885bc, fn07→0xb(find_effect_node arg)@0x08088146/0xd(write_equip)@0x08088154 ✓

dispatch table 0x09e5a128 全量扫描:
  fn07 (0x080880c0): 6 entries [27]=0x1333,[29]=0x1335,[33]=0x133c,[34]=0x133e,[35]=0x133f,[37]=0x1342
    (提案仅列 5, 漏 [29]=UFO Turtle 0x1335)
  fn09 (0x08088214): 8 entries [30][31][43][82][115][236][277][291] — 与提案 CID 列表一致 ✓
  fn12 (0x08088360): 6 entries [41][42][46][71][225][264] — 与提案一致 ✓
  fn21 (0x0808882c): 8 entries [62][118][119][141][169][209][226][249] — 与提案一致 ✓
```

---

## 状态: NEEDS_FIX

---

## 修改清单 (8 items, fixer 逐条执行)

### #1 — C2 — fn07 漏 UFO Turtle (CID=0x1335, 整个 EQ_SLOTS 段需增补)

**问题**: dispatch table entry[29] = CID=0x1335 fn=0x080880c1 — fn07 是 6-CID 共享函数, 但提案仅列 5 个 CID, 缺 UFO Turtle (card_0732, pw=60806437, slot=0x1335).

**修正**:

1. fn07 CID 列表: 加入 `0x1335 (UFO Turtle)` (dispatch table entry[29])
2. fn07 plate 文本: 在 Giant Rat 后添加 `UFO Turtle(0x1335)`, 更新 entry indices 为 `[27,29,33,34,35,37]`
3. EQ_SLOTS 段添加:
   ```
   .equ UFO_TURTLE_CID,          0x00001335  @ UFO Turtle (pw=60806437; card_0732 slot=0x1335)
   ```
4. NEW CID Summary 表添加 0x1335 行

---

### #2 — C4 — fn06 size 数值错误 + fn19 degenerate 归属错误

**问题 A**: fn06 描述写 "168 bytes" 但实际 `0x080880c0 - 0x08088058 = 0x68 = 104 bytes`. 提案同时写了正确的范围 `0x08088058..0x080880c0`, 仅 size 数字错误.

**修正 A**: fn06 中 `168 bytes` → `104 bytes`.

**问题 B**: fn19 描述写 "Full span 0x080886f8..0x080887b0 (includes degenerate 0x080887ec at end)". 但 0x080887ec = fn20 起点 0x080887b0 + 0x3c, 完全在 fn20 范围内, 不属于 fn19.

**修正 B**: fn19 描述删除 "includes degenerate 0x080887ec at end". fn20 描述正确 (已写 "post-BL continuation of fn20").

**问题 C**: fn21 EQ_SLOTS 注释写 `card_1310 slot=0x165B`. data/card-stats.s 实际: `card_1331: @ Contract with Exodia  slot=0x165B` (line 17318).

**修正 C**: `CONTRACT_WITH_EXODIA_CID` equate 注释中 `card_1310` → `card_1331`.

---

### #3 — C5 — 11 个 CID 已存在 card_info.inc, 不得重建

提案将下列 CID 标为 NEW 并计划新增 equate, 但 card_info.inc 已有对应定义 (自查 value-grep 逐一验证):

| CID (hex) | 提案打算新增名 | 现有名 (card_info.inc 行) | 使用现名 |
|-----------|--------------|--------------------------|---------|
| 0x136a | BUBONIC_VERMIN_CID | BUBONIC_VERMIN_CID (line 726) | REUSE |
| 0x194f | HYDROGEDDON_CID | HYDROGEDDON_CID (line 943) | REUSE |
| 0x1488 | GILASAURUS_CID | GILASAURUS_CID (line 732) | REUSE |
| 0x144c | cid_144c | ICID_RESERVED_D (line 1403) | REUSE |
| 0x1452 | cid_1452 | ICID_RESERVED_E (line 1404) | REUSE |
| 0x15d0 | DECAYED_COMMANDER_CID | DECAYED_COMMANDER_CID (line 867) | REUSE |
| 0x15d4 | VAMPIRE_ORCHIS_CID | VAMPIRE_ORCHIS_CID (line 870) | REUSE |
| 0x165b | CONTRACT_WITH_EXODIA_CID | CONTRACT_WITH_EXODIA_CID (line 1204) | REUSE |
| 0x16fd | DON_TURTLE_CID | DON_TURTLE_CID (line 1323) | REUSE |
| 0x12e5 | POLYMERIZATION_2_CID (fn18 pool) | POLYMERIZATION_CID (line 436) | REUSE |
| 0x10e2 | cid_10e2 (fn18 pool, "if needed") | cid_10e2 (line 888) | REUSE (已存在) |

**修正**:

- EQ_SLOTS 段删除上述 11 个条目 (不再新增).
- 每处引用 (plate 文本/CSV 注释) 中出现 `cid_144c`/`cid_1452`/`POLYMERIZATION_2_CID` 的位置替换为现有名称.
- fn17 plate: `cid_144c(unallocated)` → `ICID_RESERVED_D(0x144c)`
- fn20 plate: `unallocated CID 0x1452` → `ICID_RESERVED_E (0x1452)`
- fn18 pool section: `POLYMERIZATION_2_CID=0x000012e5` → `POLYMERIZATION_CID (reuse, line 436)`, `cid_10e2` → `reuse cid_10e2 (line 888)`.

注: fn09 HYDROGEDDON_CID + fn07/fn09 BUBONIC_VERMIN_CID 的 EQ_SLOTS 条目也要删除; 对应 NEW CID Summary 表行也要删除或改为 REUSE.

---

### #4 — C7 — REF=0 导致 ~36 个 EWRAM 指针 pool DWord 将以 raw hex 导出

**问题**: 提案 "REF=0" 意味着 84 个 pool DWord 全部仅 createDWord, 不创建 DATA 引用. 已完成的 Seg-3b (commit 793378c) 模式是: EWRAM 地址 pool DWord 须 createDWordWithRef + RENAME (ptr_lp_XXXXX) 才能导出为 `.word gP1LifePoints` / `.word gP1SlotSetCodeArray` 等符号形式, 否则导出 raw hex `.word 0x0201c4e0`.

按 ewram.inc 已有 equate 清查:
- `gP1LifePoints = 0x0201c4e0` (ewram.inc line 79): **18 个** pool slot (@0x08087d94, 0x08087e00, 0x08087ea8, 0x08087fb4, 0x08088044, 0x080880b8, 0x08088180, 0x08088208, 0x0808827c, 0x080882f8, 0x080883c8, 0x08088460, 0x080884e8, 0x08088598, 0x08088640, 0x080886e8, 0x080887a0, 0x08088820)
- `gP1SlotSetCodeArray = 0x0201c740` (ewram.inc line 332): **8 个** pool slot (@0x08087eb0, 0x08087f44, 0x0808804c, 0x08088188, 0x08088210, 0x08088300, 0x080885a0, 0x080887a8)
- `gP1HandSlotArray = 0x0201c8f8` (ewram.inc line 334): **5 个** pool slot (@0x080883d0, 0x08088468, 0x080884f0, 0x08088648, 0x08088828)
- `gP1FieldArrayCBase = 0x0201c600` (ewram.inc line 366): **2 个** pool slot (@0x0808835c, 0x0808886c)
- `gP1SlotCountBase = 0x0201c4f0` (ewram.inc line 331): **2 个** pool slot (@0x08087f3c, 0x08088194)
- `0x0201e278 (NOT in ewram.inc)`: **1 个** pool slot (@0x080885cc, fn16 only)

**修正**:

1. 将上述 36 个 EWRAM 地址 pool slot 从 createDWord 改为 createDWordWithRef, 引用对应全局.
2. 每个 pool slot 加 RENAME: `PTR_xxx` → `ptr_lp_XXXXX` (与 Seg-3b 模式一致; ptr_lp_* 用于 gP1LifePoints; gP1SlotSetCodeArray 等其他全局用类似 `ptr_sca_XXXXX` 或直接 EOL 标注 — 按 Seg-3b 实际模式执行).
3. 对 `0x0201e278` (fn16 pool @0x080885cc): ewram.inc 新增 equate. 该地址 = gP1LifePoints + 0x1d98, ROM 全段仅 1 处引用 (fn16). 建议:
   ```
   .equ LP_FN16_ZONE_OFF_BASE, 0x0201e278  @ gP1LifePoints+0x1d98; fn16 scan_zone_cid_13ed simple loop base; 1 ROM ref
   ```
   (名称待 fixer 按 fn16 体语义确认; 若 fixer 确认语义不足可改用 `LP_ZONE_BASE_1D98` 或 raw 加 EOL)
4. 更新提案 EQ_SLOTS 段从 "REF=0" 改为 "REF=36 (createDWordWithRef for EWRAM pointer pools)".

**注意**: 不执行此项则 byte-identical 仍可通过 (raw hex 汇编值相同), 但 36 个 pool slot 导出为 raw `.word 0x0201c4e0` 而非 `.word gP1LifePoints`, 与 Seg-3b 已建立的模式不一致, 构成残留 raw-value 未符号化问题.

---

### #5 — C4 附属 — fn18 EQ_SLOTS 注释需更新 (关联 #3)

fn18 body 正文中 "POLYMERIZATION_CID=0x12e5 not in card_info.inc (0 hits value grep)" 是错误的 value grep 结论. 实际 card_info.inc line 436 明确定义 `POLYMERIZATION_CID = 0x000012e5`. 需订正提案中该叙述并替换 EQ_SLOTS 计划为 REUSE (已在 #3 覆盖).

---

## 不阻塞项 (信息性记录, 不影响 fixer 落地)

**I1**: degenerate 0x080885e0 出现在 fn17 描述("mid-loop degenerate") 和 WEAK 表中, 两者一致; 但 STRONG 六条清单未包含 0x080885e0 (它是 WEAK 候选). 描述准确, 无须修改.

**I2**: fn17 包含 ICID_RESERVED_D (0x144c), 命名为 `scan_zone_return_from_grave_group_substate_e` 是基于其他 3 个 CID 的主导语义命名, 可接受. 函数名本身不需改.

**I3**: fn20 名称 `scan_zone_cid_1452_substate_e` 保留 (cid_1452 风格适用于 unallocated/reserved CIDs 的函数命名约定); 仅 EQ_SLOTS 须改用 ICID_RESERVED_E.

**I4**: fn05 pool 中 0x1497/0x17ae (CID range比较值) 暂为 raw pool scalar, 无现有 equate; 可接受为 raw with EOL (未分配且无语义等价 equate).

**I5**: PLAYER_BLOCK_STRIDE 21 次出现 (fn04 有 2 处 pool section) — ROM bytes 全部 = 0x00000868 确认; REUSE 正确.

---

## 状态: NEEDS_FIX(5 items)

修改 #1-#5 均为 proposal 修正 (Mode A); 无需 Ghidra 落地就能更正提案后提交给 fixer.

修改完成后 reviewer 应重核 C2/C4/C5/C7 四项, 确认全 PASS 后方可落地.
