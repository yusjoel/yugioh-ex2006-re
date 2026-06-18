# Refine Review: F08-Seg-8b  [0x0806b56c..0x0806c0cc)

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | Seg-8b 范围 0x6b56c..0x6c0cc 位于路线图 Seg-8b 条目 (0x6b56c..0x6cbe8) 内。Seg-8a proposal 已建立 8a/8b/8c 三段拆分约定，Seg-8b 是该拆分的第 2 子段，无跳号/回头。 |
| C2 Rule2 | ✅ | 段内 ROM_INCBIN 恰好 5 块 (asm lines 16986/17000/17141/17172/17181)，全部在 proposal 中有归宿 (均判 DISASM R4)，无静默保留。 |
| C3 Rule3 | ✅ | 0x6b784: 全 ROM raw=1 唯一命中在 0x66067f (0x66067f % 4 = 3，非对齐字节偏移 3，位于压缩图形数据 0x66xxxx 区，独立确认为偶合)；THUMB+1=1 @0x1e40448 真引用 → DISASM，非 ss5.1。0x6bb74: raw=0，THUMB+1=1 @0x1e40490 → DISASM，非 ss5.1。余 3 块均有真 raw 引用。无零引用块被误归 ss5.1，也无有引用块进 ss5.1。 |
| C4 R1 值 | ✅ | 独立 python 逐字节核对全部 17 EQ slot + 1 REF slot (DWORD_0806bb28=0x08051319)，ROM 实值与 proposal 表格完全吻合。详见下文字节核对表。 |
| C5 R1 复用 | ✅ | 3 个 NEW (CEASEFIRE_CID=0x135c / MAGICAL_HATS_CID=0x1362 / SPELL_ABSORBING_LIFE_CID=0x1635) 各 grep constants/ 0 命中，confirmed NEW。15 个 reuse 均 grep 确存在。详见下文 C5 核对。 |
| C6 R2 名 | ✅ | 所有 slot 标签形如 `<semantic>_<hex_addr>`，符合 `^[a-z][a-z0-9_]+$`；未发现重复 label。 |
| C7 R3 接通 | ✅ | PTR_DAT_0806b7d4 有 USER-label cid_135b_dispatch_jump_table + DATA-ref 计划。DWORD_0806bb28 有 fn ptr 引用 (check_equip_slot_eligible_by_equip_type+1) 并计划 DATA-ref。carve=0 (jump tables 均已在 asm 中结构化为 .word 条目，位于 ROM_INCBIN 之外)。 |
| C8 R5 现名 | ✅ | 段内唯一 stale FUN_：asm line 17183 的 `FUN_0806b53c` (dispatch_neo_daedalus_placement_check_by_state 的 plate)。proposal PLATE 节正确识别并计划改为 `dispatch_spear_cretin_activate_if_chain_subtype`。其他 FUN_ 全扫结果：asm lines 16692..17189 内仅此一处。 |
| C9 ASCII | ✅ | python 扫描 asm lines 16692..17189 全部字符，无超出 ASCII 范围字节。proposal plate/EOL 文本节亦全 ASCII。 |
| C10 carve | ✅ | THUMB+1 fn ptr 经 python 验证：0x1e40448 处 value=0x0806b785 (=block 0x6b784+1)，0x1e4048c 处 value=0x1362 (CID)，0x1e40490 处 value=0x0806bb75 (=block 0x6bb74+1)。7-entry 嵌套表末项 [6] @0x6bfb8=0x0806bfbc (=block 0x6bfbc 起始)，literal pool @0x6bf9c=0x0806bfa0 (指向该 7-entry table 起始) 均 python 实读验证一致。 |
| C11 误名 | ✅ | fn_eligible 在本模块 0x09e40xxx 分发表的结构：entry[+0]=CID，entry[+4]=fn_eligible+1，entry[+0xc]=fn_activate+1 (或其他 fn ptr)。entry+4 位置存放的是 fn_eligible 函数指针 — 经 Seg-8a 0x6c3d8/Morphing Jar2 + 0x133b/Spear Cretin 等跨段一致性验证，以及 0x6c3d8 与 0x6b784 首 8 字节完全相同 (f0b5 5746 4e46 4546)，确认该命名规律。`check_equip_eligible_cid_135b` 和 `check_equip_eligible_magical_hats` 命名正确，无误名。4 个已命名函数体行为与名称一致，无 FUNC_RENAME 需求。 |
| C12 R6 | ✅ | 关键新 slot 均有 asm file:line + high conf：CEASEFIRE_CID @ asm/08 L17103-17104 (DWORD 0x135c)；SPELL_ABSORBING_LIFE_CID @ L17105-17106 (DWORD 0x1635)；两者均被 L17002 plate 以明文 "0x135c Ceasefire / 0x1635 The Spell Absorbing Life" 提及；MAGICAL_HATS_CID 由 0x1e4048c python 读出；card-stats.s 逐一坐实。proposal 无零容忍词。 |
| C13 残留 | ✅ | python 扫描 asm lines 16692..17189：22 个自动名 label (18 DWORD_ + 1 PTR_DAT_ + 3 DAT_)。对账：17 EQ DWORD + 1 REF DWORD + 1 REF PTR_DAT_ + 3 ROM_INCBIN DAT = 22，完全吻合，无漏槽。 |

---

## 独立 ref-scan 核查 (Phase 1)

### python 重跑结果 (raw + THUMB|1)

| Block | sz | raw 真引用 | THUMB+1 | 独立裁定 |
|-------|----|---------|---------| --------|
| 0x6b784 | 0x4c | **0** (0x66067f 处 1 命中为非对齐偶合: 0x66067f%4=3，字节跨 0x66067c word，压缩图形区) | 1 @0x1e40448 | DISASM R4 |
| 0x6b7fc | 0x27c | 1 @0x6b7f8 (10-entry 跳表第 [9] 条，表 0x6b7d4..0x6b7f8 全 10 条均指向本块内) | 0 | DISASM R4 |
| 0x6bb74 | 0x44 | 0 | 1 @0x1e40490 | DISASM R4 |
| 0x6bc2c | 0x374 | 1 @0x6bc28 (29-entry 跳表第 [28] 条，全 29 条指向本块) | 0 | DISASM R4 |
| 0x6bfbc | 0x110 | 1 @0x6bfb8 (7-entry 嵌套表第 [6] 条，全 7 条指向本块) | 0 | DISASM R4 |

**注意：0x6b784 的 raw=1 不是真引用。** python 确认：needle `0x0806b784` 在 ROM 中唯一命中在偏移 `0x66067f`，该偏移 mod 4 = 3 (非 word 对齐)，位于 0x66xxxx 压缩图形数据区，字节序列 `c8 00 04 [84 b7 06 08] 82 30` — 系随机字节偶合，非代码指针。实际 real raw refs = 0。

---

## CID 偏移核验

### Block 0x6b784 (fn_eligible for CID=0x135b)

分发表项 @file-offset 0x1e40444 (ROM addr 0x09e40444):

```
+0x0 @0x1e40444: 0x0000135b  <- CID
+0x4 @0x1e40448: 0x0806b785  <- fn_eligible+1 (THUMB+1 ref = block start)
+0x8 @0x1e4044c: 0x00000000
+0xc @0x1e40450: 0x0805dc6d  <- fn_activate+1 (另一函数)
+0x10 @0x1e40454: 0x00000000
+0x14 @0x1e40458: 0x00000000
```

CID 在 fn_eligible ptr 地址 **-4** 处 (本模块 0x09e40xxx 表结构，与方法论文档描述的 -0xc 不同；-0xc 适用于其他 FS runtime 表结构)。proposal 读 fn_ptr-4 = CID = 0x135b，正确。

### Block 0x6bb74 (fn_eligible for CID=0x1362 Magical Hats)

分发表项 @file-offset 0x1e4048c:

```
+0x0 @0x1e4048c: 0x00001362  <- CID
+0x4 @0x1e40490: 0x0806bb75  <- fn_eligible+1 (THUMB+1 ref = block start)
+0x8 @0x1e40494: 0x08051e25
+0xc @0x1e40498: 0x0805dfa1  <- fn_activate+1
```

CID 同样在 fn_ptr-4 处。python 读出 0x00001362。Magical Hats passcode=81210420 查 card-stats.s card_0769 slot=0x1362 坐实。

---

## C4 EQ 字节核对

| slot | ROM addr | ROM 4B (LE) | 期望值 | 核对 |
|------|---------|-------------|-------|------|
| DWORD_0806b58c | 0x806b58c | 0x00001352 | 0x00001352 | OK |
| DWORD_0806b638 | 0x806b638 | 0x0201b290 | 0x0201b290 | OK |
| DWORD_0806b68c | 0x806b68c | 0x00000868 | 0x00000868 | OK |
| DWORD_0806b690 | 0x806b690 | 0x0201c510 | 0x0201c510 | OK |
| DWORD_0806b6bc | 0x806b6bc | 0x0201b290 | 0x0201b290 | OK |
| DWORD_0806b6ec | 0x806b6ec | 0x0201e2a0 | 0x0201e2a0 | OK |
| DWORD_0806b6f0 | 0x806b6f0 | 0x0201c4e0 | 0x0201c4e0 | OK |
| DWORD_0806b71c | 0x806b71c | 0x0201c4e0 | 0x0201c4e0 | OK |
| DWORD_0806b75c | 0x806b75c | 0x0201c4e0 | 0x0201c4e0 | OK |
| DWORD_0806b760 | 0x806b760 | 0x00001daa | 0x00001daa | OK |
| DWORD_0806b764 | 0x806b764 | 0x00000868 | 0x00000868 | OK |
| DWORD_0806bafc | 0x806bafc | 0x0201b290 | 0x0201b290 | OK |
| DWORD_0806bb00 | 0x806bb00 | 0x00000868 | 0x00000868 | OK |
| DWORD_0806bb04 | 0x806bb04 | 0x0201e1c8 | 0x0201e1c8 | OK |
| DWORD_0806bb08 | 0x806bb08 | 0x0201c510 | 0x0201c510 | OK |
| DWORD_0806bb2c | 0x806bb2c | 0x0000135c | 0x0000135c | OK |
| DWORD_0806bb30 | 0x806bb30 | 0x00001635 | 0x00001635 | OK |
| DWORD_0806bb28 (REF) | 0x806bb28 | 0x08051319 | 0x08051319 | OK |

---

## C5 新建常量核对

| 常量 | 值 | grep constants/ | 判定 |
|------|-----|-----------------|------|
| CEASEFIRE_CID | 0x0000135c | 0 命中 | NEW 确认 |
| MAGICAL_HATS_CID | 0x00001362 | 0 命中 | NEW 确认 |
| SPELL_ABSORBING_LIFE_CID | 0x00001635 | 0 命中 | NEW 确认 |

card-stats.s 坐实：card_0764 slot=0x135C pw=36468556 Ceasefire；card_0769 slot=0x1362 pw=81210420 Magical Hats；card_1301 slot=0x1635 pw=99517131 The Spell Absorbing Life。

reuse 验证 (全部 grep 命中):

| 常量 | 值 | 来源 | grep 验证 |
|------|-----|------|---------|
| NUMINOUS_HEALER_CID | 0x00001352 | card_info.inc L1154 | OK |
| cid_135b | 0x0000135b | card_info.inc L1158 | OK |
| gDuelPhaseFlags | 0x0201b290 | ewram.inc L351 | OK |
| PLAYER_BLOCK_STRIDE | 0x00000868 | ewram.inc L250 | OK |
| gDuelFieldSlots | 0x0201c510 | ewram.inc L312 | OK |
| gDuelCardCtxBase | 0x0201e2a0 | ewram.inc L218 | OK |
| gP1LifePoints | 0x0201c4e0 | ewram.inc L79 | OK |
| LP_CARD_TRACK_NEXT_OFF | 0x00001daa | ewram.inc L248 | OK |
| gEquipZoneCountTable | 0x0201e1c8 | ewram.inc L395 | OK |

---

## 嵌套跳表结构核验

### 10-entry 表 @0x6b7d4 (cid_135b stubs -> block 0x6b7fc)

ROM 实读 10 条目，全部指向 [0x806b7fc, 0x806ba78) 内，与 proposal 表一致。第 [9] 条 @0x6b7f8 = 0x0806b7fc (block 起始) = raw ref 点，verified。

### 29-entry 表 @0x6bbb8 (Magical Hats stubs -> block 0x6bc2c)

ROM 实读 29 条目，11 个唯一目标，与 proposal index 映射完全一致：entry[0]=0x806bf4c, entry[10]=0x806bf3a, entry[20..28]=明确 stub 地址，其余 1..9/11..19/27 = default 0x806bf56。

### literal pool @0x6bf9c (嵌套 7-entry 表指针，offset 0x370 within block 0x6bc2c)

ROM 读出 0x0806bfa0，指向 7-entry sub-dispatch 表起始，verified。

### 7-entry 表 @0x6bfa0 (sub-stubs -> block 0x6bfbc)

ROM 实读：[6]=0x0806bfbc (= block 起始，raw ref 点)，全 7 条目均位于 [0x806bfbc, 0x806c0cc) 内，verified。

---

## 机器码抽查

| Block | ROM addr | 期望指令 | 实际首 hw | 核对 |
|-------|---------|---------|----------|------|
| 0x6b784 | 0x0806b784 | push {r4-r7,lr} = 0xb5f0 | 0xb5f0 | OK |
| 0x6b7fc | 0x0806b7fc | movs r0,#4 = 0x2004 | 0x2004 | OK |
| 0x6bb74 | 0x0806bb74 | push {r4-r7,lr} = 0xb5f0 | 0xb5f0 | OK |
| 0x6bc2c | 0x0806bc2c | adds r0,r6,#0 = 0x1c30 | 0x1c30 | OK |
| 0x6bfbc | 0x0806bfbc | adds r0,r4,#0 = 0x1c20 | 0x1c20 | OK |

---

## 状态: PASS

proposal 逻辑自洽，所有 5 块 ref-scan 独立复核结果与 proposal 一致，EQ 值、新建常量、reuse 常量、slot 计数、机器码首指令均经 python 字节级验证无误。stale `FUN_0806b53c` 已被识别并计划修正。

---

## 修改清单

无。所有 C1-C13 通过，fixer 可直接执行 proposal 落地流程 (Ghidra 脚本: equate 17 槽 + ref/rename 2 槽 + plate 2 处 + disasm 5 blocks + card_info.inc +3 new equates)。
