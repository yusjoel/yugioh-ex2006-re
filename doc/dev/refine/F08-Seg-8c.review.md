# Refine Review: F08-Seg-8c  [0x0806c0cc..0x0806cbe8)

## 核验 (C1-C13)

| #   | 检查                         | 结果 | 备注                                                                                                     |
|-----|------------------------------|------|----------------------------------------------------------------------------------------------------------|
| C1  | 段范围与路线图一致            | PASS | Seg-8b 终止 0x6c0cc == Seg-8c 起始; Seg-8c 终止 0x6cbe8 == Seg-9 起始; 无跳号/回头                    |
| C2  | 所有 ROM_INCBIN 块有归宿      | PASS | 2 块均 DISASM: 0x6c3d8/0x44 (THUMB+1 ref) + 0x6c440/0x298 (raw ref); grep 段内 = 2, 处理数 = 2         |
| C3  | §5.1 块 0 引用独立复核       | PASS | 无 §5.1 块; 两块均有确认引用, 不适用                                                                    |
| C4  | EQ value == ROM 4 字节小端   | PASS | 抽查 16 槽全部匹配 (包含 gP1LifePoints/SPEAR_CRETIN_CID/P2LP_BLOCK2_OFF_1CF4 等关键槽)                   |
| C5  | 新建常量前无可复用现有        | PASS | P2LP_BLOCK2_OFF_1CF4=0x1cf4 裁定见下; OAM_EQUIP_ZONE_CHAIN_SPRITE_P2/SOLOMONS_LAWBOOK_CID/MORPHING_JAR_2_CID grep 0 命中 |
| C6  | 槽名 ^[a-z][a-z0-9_]+$, 无碰撞 | PASS | 49 个新标签全部合规, 无重复                                                                             |
| C7  | carve/全局槽有 USER-label+DATA-ref | PASS | 无 REF_SLOTS; PTR_ 槽已符号化 (仅 RENAME); 无新 carve 数据表                                        |
| C8  | plate 全用现名, 无残留 FUN_   | PASS | 段内唯一 FUN_: L19255 FUN_08071d64, 已在 PLATE 计划中标注替换为 dispatch_spirit_monster_zone_sprite_by_card_id |
| C9  | 所有 plate/EOL 纯 ASCII      | PASS | grep 段内 L18200-19347 无 >0x7F 字节; proposal PLATE 文本两处均纯 ASCII                                |
| C10 | 指针表条目格式正确            | PASS | 跳表 0x6c41c 为 raw 地址表 (BX 分发用), 不加 +1; fn-ptr 表 THUMB+1 单独; 两者均有 python 验证          |
| C11 | 误名已标 FUNC_RENAME          | PASS | dispatch_neo_daedalus_placement_check_by_state -> tick_spear_cretin_placement_state_machine 正确; 详见下 |
| C12 | 关键槽有 file:line + 置信度   | PASS | 所有槽均有 asm/08 行号引用 + high 置信度; 无零容忍词                                                    |
| C13 | 段内残留自动名全覆盖          | PASS | python grep: 40 个自动名标签 (39 EQ 槽 + 1 ROM_INCBIN 标签 DAT_0806c440); 全部在 EQ/disasm 表中覆盖    |

---

## 状态: PASS

---

## P2LP_BLOCK2_OFF_1CF4 碰撞独立裁定

**问题**: DAT_0806cba0=0x00001cf4 与 `duel_field.inc:206 FIELD_STATE_OFF=0x1cf4` 值相同。

**独立 python 复核**:

`enqueue_spirit_monster_zone_sprite_otohime` @ 0x0806cb54 的机器码分析:

```
0x806cb7a: 4b07  ldr r3, [pc,#28]  -> [0x806cb98] = 0x0201c4e0 = gP1LifePoints
0x806cb7c: 4d07  ldr r5, [pc,#28]  -> [0x806cb9c] = 0x00001ce8 = P1LP_BLOCK2_OFF_1CE8
0x806cb7e: 1958  adds r0, r3, r5   -> r0 = gP1LifePoints + 0x1ce8
0x806cb80: 6800  ldr r0, [r0]      -> r0 = [gP1LifePoints+0x1ce8]  (P1 LP block2)
0x806cb82: 4281  cmp r1, r0
0x806cb86: 4906  ldr r1, [pc,#24]  -> [0x806cba0] = 0x00001cf4
0x806cb88: 1858  adds r0, r3, r1   -> r0 = gP1LifePoints + 0x1cf4  (<-- 争议槽)
0x806cb8a: 6801  ldr r1, [r0]      -> r1 = [gP1LifePoints+0x1cf4]
```

**裁定**:

- DAT_0806cba0 使用 **base = gP1LifePoints = 0x0201c4e0**, 绝对地址 = 0x0201c4e0 + 0x1cf4 = **0x0201e1d4**
- FIELD_STATE_OFF 的 base = **gDuelFieldSlots = 0x0201c510**, 绝对地址 = 0x0201c510 + 0x1cf4 = **0x0201e204**
- 两者绝对地址不同, 属于不同 struct 域 → C5 relaxed-dedup 规则 (不同 base 可独立新建) **成立**
- ewram.inc L370 的 `gP1FieldState=0x0201e1d4` 是该绝对地址的直接引用名, 但它是 `.equ` 绝对地址, 不是 offset 值; 此处需要的是相对 gP1LifePoints 的 **offset equate** — ewram.inc 中不存在 `.equ ...0x00001cf4` → 确为新建
- P2LP_BLOCK2_OFF_1CF4 命名跟随 P1LP_BLOCK2_OFF_1CE8 模式, 与 asm/08 L19259 EOL `opponent_lp_offset=0x1cf4` 一致
- **结论**: 不触发 NEEDS_FIX, proposal 处理正确

---

## 2 块分类独立复核

### Block 0x6c3d8 (0x44 B)

```
python: d.count(struct.pack('<I', 0x0806c3d8)) = 0  (raw=0)
        d.count(struct.pack('<I', 0x0806c3d9)) = 1  (THUMB+1=1, hit at 0x1e43760)
```

dispatch table entry @ 0x1e43754..0x1e43768:
```
[0x1e43754] = 0x0805635d  fn_activate+1
[0x1e43758] = 0x00000000  pad
[0x1e4375c] = 0x00001369  CID (= fn_eligible_ptr - 4)
[0x1e43760] = 0x0806c3d9  fn_eligible+1  <-- THUMB+1 命中
[0x1e43764] = 0x00000000  pad
```

CID=0x1369 → card-stats.s card_0774 Morphing Jar #2 (pw=79106360) ✓

Block 首半字 0xb5f0 = `push {r4,r5,r6,r7,lr}` (THUMB 函数序言) → **DISASM 正确**

注: 本表 entry 为 5 字段 [fn_activate+1, pad, CID, fn_eligible+1, pad], CID 位于 fn_eligible_ptr-4 (非 -0xc); proposal 正确标注了这一差异。

### Block 0x6c440 (0x298 B)

```
python: d.count(struct.pack('<I', 0x0806c440)) = 1  (raw=1, hit at 0x6c43c)
        d.count(struct.pack('<I', 0x0806c441)) = 0  (THUMB+1=0)
```

0x6c43c 是 9 条目跳表末项 (`entry[8] = 0x0806c440`), 已在 asm 中结构化为 `.word`。

跳表 9 条目 python 复核 (0x806c41c..0x806c43c):
```
entry[0]=0x0806c69c, entry[1]=0x0806c6c0, entry[2]=0x0806c6c0, entry[3]=0x0806c65a,
entry[4]=0x0806c63c, entry[5]=0x0806c5f8, entry[6]=0x0806c52c, entry[7]=0x0806c4e8,
entry[8]=0x0806c440
```
8 unique stub 首指令均为合法 THUMB (0x2000/0x490d/0x4b2e/0x4d0f/0x4813/0x480c/0x2700/0x2000) → **DISASM 正确**

---

## C11 FUNC_RENAME 核

**dispatch_neo_daedalus_placement_check_by_state → tick_spear_cretin_placement_state_machine**

证据:
1. DWORD_0806c1b4 @ 0x806c1b4 = 0x0000133b = SPEAR_CRETIN_CID (python 验证; card_info.inc L796)
2. card-stats.s card_0737: Spear Cretin slot=0x133B pw=58551308
3. 函数体 L18313 直接比较 card_id 对 0x133b
4. `check_field_spell_neo_daedalus_group_placeable` 是函数内 bl 调用的 **callee** (L18243/18246), 非本函数身份
5. indeg=1: 全 ROM 中唯一 `bl dispatch_neo_daedalus_placement_check_by_state` 在 L16662 (dispatch_spear_cretin_activate_if_chain_subtype @ 0x806b54c)
6. 跨模块 grep: `dispatch_neo_daedalus_placement_check_by_state` 仅出现在 asm/08 (L16645/16650/16651/16662/18199), 无跨文件 plate; 落地后均在 re-export 中自动更新

**结论**: FUNC_RENAME 正确, 高置信度

---

## C5 其他新建常量核

| 常量                           | 值       | grep 核    | passcode 核                    |
|-------------------------------|----------|------------|-------------------------------|
| MORPHING_JAR_2_CID=0x1369     | 0x1369   | 0 命中     | card-stats.s card_0774 pw=79106360 ✓ |
| SOLOMONS_LAWBOOK_CID=0x137e   | 0x137e   | 0 命中     | card-stats.s card_0794 pw=23471572 ✓ |
| OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052 | 0x8052 | 0 命中 | oam_attr.inc 无同值条目 ✓ |

---

## C13 完整性核

`grep ^(DWORD_|DAT_|PTR_)` 在 Seg-8c (L18199-19345) 共找到 **40 个**自动名标签:
- 39 个为 literal pool EQ 槽, 全部在 proposal EQ_SLOTS 表中 (逐一对应)
- 1 个为 `DAT_0806c440` (ROM_INCBIN 0x6c440 块起始标签), 在 disasm 计划中处理

无遗漏槽, 无越界槽 (最大地址 DAT_0806cbe4 = 0x806cbe4 < 0x806cbe8 ✓)。

---

## 修改清单

无。

---

## Reviewer Verdict: F08-Seg-8c = PASS
