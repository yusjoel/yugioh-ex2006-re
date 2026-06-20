# Refine Review: F10-Seg-1

> Seg-1 [0x08079e60, 0x0807ae84) -- 19 fn, 61 auto-name slots, 8 ROM_INCBIN blocks.
> Proposal: `doc/dev/refine/F10-Seg-1.proposal.md`
> Reviewer ran independent python ref-scan, ROM byte verification, and C5 grep.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | Seg-1 范围与 §五 路线图一致 | OK | 路线图 [0x79e60, 0x7ae84) 与 proposal 一致; fn 数19(proposal 正确纠正了 commit_serial_spell_effect_node 属 Seg-2) |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | OK | 8 块全部 R4 disasm: BLK1/3/5/7 = fn_eligible stubs(THUMB+1 命中), BLK2/4/6/8 = dispatch sub-stubs(raw 命中). §5.1=0. |
| C3 Rule3 | §5.1 块确 0 引用 | OK | §5.1=0 正确; 所有 8 块均有引用; 独立 ref-scan 确认 |
| C4 R1 值 | EQ slot 每个值 == ROM 4 字节小端 | FAIL | 47 个 EQ slot 字节全部正确 (47/47 OK). 但 **BLK5 disasm 计划中 literal pool 地址错误** (见 #FIX2); **BLK1 disasm 计划缺 createDWord 一个地址** (见 #FIX3) |
| C5 R1 复用 | 新建 constants 前无现有可复用 | FAIL | **BLK7 literal pool 0x7a6c0 = 0x1ce8: 提案说"no existing equate"但 `P1LP_BLOCK2_OFF_1CE8 = 0x1ce8` 已在 ewram.inc 第 275 行** (见 #FIX1) |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | OK | RENAME 槽名 (lp_state_base_a32c, player_life_ptr_a99x 等 9 个) 和 REF 槽名 (equip_sprite_*_stubs 等 5 个) 全部合规; constant 名 UPPER_SNAKE_CASE 合规 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | 5 个 REF_SLOTS: dispatch 表 (.word 条目已在 ASM) 均已引用对应入口地址; PTR_DAT_0807a6d0 保留并改名; 接通正确 |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_ | OK | Seg-1 行范围 (L10-L1575) 内 FUN_[0-9a-f]{8} = 0 hits |
| C9 ASCII | plate/EOL 纯 ASCII | OK | Seg-1 行范围内非 ASCII 字符 = 0 hits; PLATE=0 |
| C10 carve | fn_eligible 块用 THUMB+1, dispatch 用 raw | OK | 独立验证: BLK1/3/5/7 的 FS 表条目 [+0xc] 均为 stub_addr|1; BLK2/4/6/8 的 dispatch 表条目为 raw 地址 |
| C11 误名 | 函数名与函数体无矛盾 | OK | 抽查 4 个函数: enqueue_neo_daedalus_zone_oam_on_available_slot / dispatch_equip_sprite_by_zone_type_or_draw_counter / apply_partner_flags_on_equip_pair_slot_count_hit / tick_hand_effect_node_match_display_seq -- 均与 body callees/逻辑一致; FUNC_RENAME=0 正确 |
| C12 R6 | 关键槽有 file:line + 置信度证据 | OK | NEO_DAEDALUS_OAM_SPRITE_BASE(high)/CARD_DISPLAY_OP_ID_137(high)/EQUIP_PAIRED_SLOT_PRED(med)/0x12a1(high) 均有 asm/10 行号证据; 无零容忍词 |
| C13 残留 | 段内全部残留自动名槽被覆盖 | OK | 独立 python 清点: 61 个 (DWORD_/DAT_/PTR_DAT_ labels); 47 EQ + 9 RENAME + 5 REF = 61; 无遗漏, 无双计 |

---

## 独立 ref-scan 结果 (C2/C3)

运行 python `rom.count(struct.pack('<I', addr))` (raw) 和 `rom.count(struct.pack('<I', addr|1))` (THUMB+1):

| 块 | raw 命中 (地址) | THUMB+1 命中 (地址) | 判定 |
|---|---|---|---|
| BLK1 0x79fac/0x30 | 0 | 1 (0x9e42290) | R4 disasm, fn_eligible |
| BLK2 0x7a00c/0xe8 | 1 (0x807a008) + 6 inner | 0 | R4 disasm, dispatch sub-stubs |
| BLK3 0x7a138/0x28 | 0 | 1 (0x9e422f0) | R4 disasm, fn_eligible |
| BLK4 0x7a178/0x14c | 1 (0x807a174) + 5 inner | 0 | R4 disasm, dispatch sub-stubs |
| BLK5 0x7a3b8/0x38 | 0 | 2 (0x9e42398, 0x9e442b8) | R4 disasm, fn_eligible (shared) |
| BLK6 0x7a464/0x11c | 1 (0x807a460) + 5 inner | 0 | R4 disasm, dispatch sub-stubs |
| BLK7 0x7a688/0x44 | 0 | 1 (0x9e42410) | R4 disasm, fn_eligible |
| BLK8 0x7a71c/0xf8 | 1 (0x807a718) + 7 inner | 0 | R4 disasm, dispatch sub-stubs |

FS handler table CID 独立读取 (entry [+0x8] = CID, [+0xc] = fn_eligible+1):
- BLK1: 0x9e4228c = 0x17f4 (Abyssal Designator) -- OK
- BLK3: 0x9e422ec = 0x17f9 (Big Wave Small Wave) -- OK
- BLK5a: 0x9e42394 = 0x1803 (unassigned) -- OK
- BLK5b: 0x9e442b4 = 0x15de (unassigned, equip_cid_15de_08048a68) -- OK
- BLK7: 0x9e4240c = 0x1818 (Magician's Circle) -- OK

Dispatch table unique entry sets (独立读取) match proposal exactly:
- BLK2: 7 unique (0x7a00c/0x7a03a/0x7a0a8/0x7a0bc/0x7a0cc/0x7a0da/0x7a0ea)
- BLK4: 6 unique (0x7a178/0x7a1ae/0x7a21a/0x7a240/0x7a25e/0x7a278)
- BLK6: 6 unique (0x7a464/0x7a4ac/0x7a534/0x7a544/0x7a560/0x7a570)
- BLK8: 8 unique (0x7a71c/0x7a730/0x7a764/0x7a77c/0x7a786/0x7a7a8/0x7a7ec/0x7a804)

Zero-residue 覆盖: 各偶数块的入口集合连续覆盖对应 ROM_INCBIN 字节范围 (每段 stub 结束即下一入口开始), 全部 match. 每个入口前 4 条 THUMB half-word 均为合理 THUMB 指令 (ldrb/ldr/movs/push 等开头).

---

## 三项裁定 (Adjudicated Items)

### 裁定 1 -- CID 0x1803 (BLK5 第一个 FS 条目)

card-stats.s 独立验证: 0x1802 = Greed (card_1679), 0x1804 = Cemetary Bomb (card_1680), 中间无 0x1803 条目. 确认为未分配槽.

**裁定**: 0x1803 确为未分配; 使用中性 EOL 注释 "CID 0x1803 (unassigned)" 或标 `equip_cid_1803_unassigned`, 不需独立 .equ. Proposal 处理方案正确, 无需变更.

### 裁定 2 -- DWORD_0807a998 = 0x12a1 vs PARASITE_PARACIDE_CID

ASM L820-L822 (0x0807a968-0x0807a96c):
```
    movs r1,#0xb                   @ zone_id = hand zone (type 0xb)
    ldr r2, DWORD_0807a998         @ r2 = 0x12a1 = node-type tag
    bl find_effect_node_in_zone
```
r2 = 0x12a1 是传给 `find_effect_node_in_zone` 的第三个参数 (node-type attribute code), 与 PARASITE_PARACIDE_CID 数值相同但语义完全不同 (节点类型标记 vs. 卡牌 ID 查找). 这是跨语义值碰撞.

**裁定**: 不得复用 `PARASITE_PARACIDE_CID`. 正确选项: 新建 `ZONE_QUERY_HAND_TAG_12A1` 或保留原值加 EOL 注释 "zone query node-type tag for find_effect_node_in_zone (hand zone=0xb)". Proposal 推荐 EOL-only 方案可接受 (单一调用点, 不必独立 equate). 两种选项均合规.

### 裁定 3 -- BLK7 literal pool 0x7a6c0 = 0x1ce8

独立验证 ewram.inc 第 275 行: `.equ P1LP_BLOCK2_OFF_1CE8, 0x1ce8`. 该常量已存在.

LDR 指令确认: BLK7 +0x08 (0x0807a690): `LDR r0,[PC,#44]` -> 0x7a6c0 = 0x00001ce8.

**裁定**: `P1LP_BLOCK2_OFF_1CE8` (ewram.inc) 必须 REUSE. Proposal 在 BLK7 disasm 计划中说 "no existing equate -- use raw literal 0x1ce8" 是 **错误的**. 这是 C5 违反, 需要修正 (见 #FIX1).

注: 0x1ce8 不在 61 个 DWORD_/DAT_/PTR_DAT_ slot 标签内 (它在 ROM_INCBIN 块内), 但 disasm 计划的 createEquate/EOL 注释必须引用正确的常量名.

---

## 状态: NEEDS_FIX (3 items)

---

## 修改清单

### #FIX1 -- C5 -- BLK7 disasm 计划: 0x1ce8 必须 REUSE P1LP_BLOCK2_OFF_1CE8

**位置**: Proposal §disasm 计划 BLK7 节 + BLK7 literal pool note 节.

**错误**: 两处均写 "no existing equate -- use raw literal 0x1ce8" 或类似表述.

**修正**:
- BLK7 literal pool note: `0x7a6c0: 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8, ewram.inc REUSE)` -- 不是 raw literal.
- BLK7 disasm 计划 createDWord 后: 注释改为 `createEquate(0x7a6c0, P1LP_BLOCK2_OFF_1CE8)` 或 EOL comment 写 `P1LP_BLOCK2_OFF_1CE8`.
- C5 双向核表: 增加行 `0x1ce8 -> P1LP_BLOCK2_OFF_1CE8 (ewram.inc REUSE, value grep match)`.

Fixer 执行时: BLK7 disasm 后在 0x7a6c0 处创建 Ghidra createEquate 或 setEolComment 引用 `P1LP_BLOCK2_OFF_1CE8`.

---

### #FIX2 -- C4 -- BLK5 disasm 计划 literal pool 地址错误 (HIGH 优先级)

**位置**: Proposal §disasm 计划 BLK5 节.

**错误**:
> Literal pool within BLK5 at +0x2c..+0x33 (last 8B):
>   +0x2c: gDuelPhaseFlags (0x0201b290) -> createDWord at 0x7a3e4
>   +0x30: (dispatch table ptr 0x0807a3f0) -> createDWord at 0x7a3e8

独立验证:
- `0x7a3e4` (+0x2c) = 0x4687 (THUMB 指令 `MOV PC,r0`) -- 这是代码, 不是 literal pool!
- `0x7a3e6` (+0x2e) = 0x0000 (.zero 2 对齐填充)
- `0x7a3e8` (+0x30) = 0x0201b290 (gDuelPhaseFlags -- 正确 pool word 1)
- `0x7a3ec` (+0x34) = 0x0807a3f0 (dispatch table ptr -- 正确 pool word 2)

LDR 指令交叉验证:
- BLK5 +0x12 (0x7a3ca): `LDR r0,[PC,#28]` -> target = 0x7a3e8 = 0x0201b290 (gDuelPhaseFlags) -- 正确
- BLK5 +0x26 (0x7a3de): `LDR r1,[PC,#12]` -> target = 0x7a3ec = 0x0807a3f0 (dispatch table ptr) -- 正确

**修正**:
```
Literal pool within BLK5 at +0x30..+0x37 (last 8B, after .zero 2 at +0x2e):
  +0x30: gDuelPhaseFlags (0x0201b290) -> createDWord at 0x7a3e8
  +0x34: dispatch table ptr (0x0807a3f0) -> createDWord at 0x7a3ec
```

**重要**: Fixer 执行时 **绝对不得调用** `createDWord(0x7a3e4)`. 在 THUMB 代码地址强制创建 4B 数据会覆盖 `MOV PC,r0` 指令 (0x4687), 导致 BLK5 disasm 破坏. 正确地址: `createDWord(0x7a3e8)` 和 `createDWord(0x7a3ec)`.

---

### #FIX3 -- C4 -- BLK1 disasm 计划缺 gDuelPhaseFlags pool word (LOW 优先级)

**位置**: Proposal §disasm 计划 BLK1 节.

**错误**: 仅列 `createDWord at 0x79fd8 (.word 0x08079fdc -- dispatch table ptr)`, 未列 gDuelPhaseFlags 池字.

独立验证:
- `0x79fd4` (+0x28) = 0x0201b290 (gDuelPhaseFlags)
- `0x79fd8` (+0x2c) = 0x08079fdc (dispatch table ptr)

LDR 指令确认:
- BLK1 +0x0c (0x79fb8): `LDR r0,[PC,#24]` -> 0x79fd4 = 0x0201b290 (gDuelPhaseFlags)

**修正**: BLK1 disasm 计划增加:
```
createDWord at 0x79fd4  (.word gDuelPhaseFlags = 0x0201b290)
createDWord at 0x79fd8  (.word dispatch table ptr = 0x08079fdc)
```

严重性: LOW. Ghidra 的 DisassembleCommand 通常会从 `LDR r0,[PC,#24]` 指令自动识别 0x79fd4 为 literal pool word, 所以漏掉 createDWord 可能不影响最终 disasm. 但 proposal 应完整记录以确保 fixer 明确.

---

## 通过/可接受项 (记录)

- 47 个 EQ slot 全部 ROM 字节核对 OK (python 独立验证 47/47).
- C13 全部 61 槽独立清点 = 47+9+5, 无遗漏无双计.
- BLK2/4/6/8 dispatch 入口覆盖: 各块 stub 入口集合恰好连续覆盖 ROM_INCBIN 全部字节 (zero-residue 验证通过).
- BLK3 (0x7a138) 和 BLK7 (0x7a688) literal pool 地址正确.
- C5 新建值 0x180d/0x137/0x181e/0x1818/0x1803 均为 0 hits (exact value grep).
- C8: 0 stale FUN_ in Seg-1 range. C9: 0 non-ASCII.
- 所有 RENAME slot 新名和 REF slot 新名符合 `^[a-z][a-z0-9_]+$`.
- 裁定 1 (CID 0x1803 unassigned) 和裁定 2 (0x12a1 EOL-only) proposal 处理方案均正确.
