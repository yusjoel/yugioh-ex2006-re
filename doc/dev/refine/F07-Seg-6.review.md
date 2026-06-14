# Refine Review: F07-Seg-6

段范围: ROM `0x08060898..0x080613b4`, `asm/07_equip_effect_chain.s` lines 11572..13429

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 路线图一致 (Seg-6 = 0x60898..0x613b4) | OK | 与 §五 roadmap 行完全吻合 |
| C2 | 全部 ROM_INCBIN 块有归宿 | OK | 3 块全部 R4 disasm, §5.1=0 |
| C3 | §5.1 块确 0 引用 | OK | 无 §5.1 登记; 所有 3 块均有 THUMB+1 dispatch table 引用 |
| C4 | EQ value == ROM 4 字节小端 | OK | 全 47 槽 python `struct.unpack_from` 核验, 0 mismatches |
| C5 | 复用/新建 constants 双向核 | OK with annotation | 见下节 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | OK | 全 47 labels 通过正则, 无重名 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | 无新全局; 所有 0x0201xxxx 槽均复用已命名全局 |
| C8 | plate 全用现名, 无残留 `FUN_` | OK | grep Seg-6 范围 (lines 11572-13429) FUN_[0-9a-fA-F]{8} = 0 hits |
| C9 | 所有 plate/EOL 纯 ASCII | OK | plate 节 6120 chars 纯 ASCII; RENAME_SLOTS EOL 列全 ASCII; proposal 非 ASCII 仅在 doc 节标题 (中文), 不进 Ghidra |
| C10 | 指针表条目 `+1` (THUMB) | OK | Block1 0x08060a89=0x08060a88+1, Block2 0x08061071=0x08061070+1, Block3 0x0806121d=0x0806121c+1; ROM 实读确认 |
| C11 | 函数体与函数名无矛盾 (FUNC_RENAME) | OK | 34 命名函数无语义错误; plate 内 DUEL_STATE_PTR 是 plate 注解错误非函数名错误, 已在 proposal 内正确指出 |
| C12 | 关键槽有 file:line + 置信度, 无零容忍词 | OK | DWORD_08060fd8=gEquipChainSlotRefs (ewram.inc:315 high); ZONE_DETAIL_FIELD_MASK_F88 (duel_field.inc:378 high); 无零容忍词 |
| C13 | 段内所有残留自动名槽 100% 覆盖 | OK | asm 实计: DAT_=8, DWORD_=39, PTR_=3; 共 50 槽; PTR_ 3 个均已命名 (PTR_gP1LifePoints_*) 按 scope convention 跳过; 余 47 全部在 EQ/RENAME 表; missing=0, extra=0 |

---

## 独立 ref-scan 结果 (C3)

重跑 python `rom.count(struct.pack('<I', fn_addr))` 和 `rom.count(struct.pack('<I', fn_addr+1))`, 2B-step 全 ROM 穷举:

| 块 | raw hits | THUMB+1 hits | 判定 |
|----|----------|--------------|------|
| 0x60a86/0x90 fn@0x08060a88 | 0 | 1 @ 0x09e417d0 | R4 disasm |
| 0x6106e/0x2e fn@0x08061070 | 0 | 1 @ 0x09e44668 | R4 disasm |
| 0x6121c/0x28 fn@0x0806121c | 1 @ 0x08430c4c | 1 @ 0x09e41bc0 | R4 disasm |

Block3 raw hit @ 0x08430c4c 调查: ROM offset 0x430c4c = 4.2MB, 在 FS/data 区 (起点字节 0x03 为 LZ77 header), 上下文值均非有效 ARM/THUMB code (无规则位模式, 系压缩数据). 该 raw hit 不是代码调用引用. THUMB+1 hit @ 0x09e41bc0 才是真正 dispatch table 引用 (CID=0x16d1, fn_elig=0x0806121d 确认). Block3 仍判定 R4 disasm.

dispatch table entry 实读确认:
- Block1 @ 0x09e417c0: [+0]=0, [+4]=0x0000165b, [+8]=0x080659e9, [+0xc]=0, [+0x10]=0x08060a89, [+0x14]=0
- Block2 @ 0x09e44658: [+0]=0, [+4]=0x000016c6, [+8]=0x0806c765, [+0xc]=0, [+0x10]=0x08061071, [+0x14]=0
- Block3 @ 0x09e41bb0: [+0]=0, [+4]=0x000016d1, [+8]=0x08064661, [+0xc]=0x08050751, [+0x10]=0x0806121d, [+0x14]=0

---

## C4 slot 全量核验

全 47 槽 `struct.unpack_from('<I', rom, addr-0x08000000)` 核验: 全 OK, 0 mismatches.

Block1 literal pool (0x08060af8..0x08060b0c): 6 槽全 OK.
Block3 literal pool (0x0806123c, 0x08061240): 2 槽全 OK.

Block3 PC-relative 偏移验证:
- `ldr r2,[pc,#0x1c]` @ 0x0806121e: PC=0x08061222, target=(0x08061222+0x1c)&~3=0x0806123c, value=0x0201c4e0 (gP1LifePoints) OK
- `ldr r1,[pc,#0x18]` @ 0x08061226: PC=0x0806122a, target=(0x0806122a+0x18)&~3=0x08061240, value=0x00000868 (PLAYER_BLOCK_STRIDE) OK

---

## C5 双向核

**新建 CID (0 hits in card_info.inc 确认)**:
SAGES_STONE_CID(0x167e), QUEENS_KNIGHT_CID(0x157f), OJAMA_YELLOW_CID(0x16b3),
CHAOS_EMPEROR_DRAGON_CID(0x16e4), CONTRACT_WITH_EXODIA_CID(0x165b),
FENRIR_CID(0x16c6), CHAOS_END_CID(0x16d1),
RIGHT_LEG/LEFT_LEG/RIGHT_ARM/LEFT_ARM/EXODIA_THE_FORBIDDEN_ONE_CID(0x0fb7-0x0fbb)
均 0 命中 (name + hex value 双核). 全部新建合理.

**复用 CID (存在核)**:
FRIENDSHIP_CID(0x167a, L1067), UNITY_CID(0x167b, L1068), MUSTERING_DARK_SCORPIONS_CID(0x169e, L704),
DARK_MAGICIAN_GIRL_CID(0x129e, L319), DON_ZALOOG_CID(0x1532, L594),
BANISHER_OF_THE_LIGHT_CID(0x1332, L452), TERRORKING_ARCHFIEND_CID(0x1691, L961),
CLIFF_THE_TRAP_REMOVER_CID(0x161e, L1076), DARK_SCORPION_CHICK_CID(0x1656, L702),
DARK_SCORPION_GORG_THE_STRONG_CID(0x1685, L1026), DARK_SCORPION_MEANAE_CID(0x1686, L703),
CRIMSON_NINJA_CID(0x16b8, L744), BLACK_LUSTER_SOLDIER_ENVOY_CID(0x16cb, L748),
OJAMA_GREEN_CID(0x1681, L666), OJAMA_BLACK_CID(0x16b4, L668), EXODIA_NECROSS_CID(0x1645, L245)
全部确认存在.

card-stats.s CID 槽 ID 坐实: 0x165b=Contract with Exodia(card_1331), 0x16c6=Fenrir(card_1416),
0x16d1=Chaos End(card_1427), 0x0fb7=Right Leg(card_0017), 0x0fb8=Left Leg(card_0018),
0x0fb9=Right Arm(card_0019), 0x0fba=Left Arm(card_0020), 0x0fbb=Exodia the Forbidden One(card_0021),
0x167e=Sage's Stone(card_1355), 0x157f=Queen's Knight(card_1158), 0x16b3=Ojama Yellow(card_1399),
0x16e4=Chaos Emperor Dragon(card_1445). 全部确认.

---

## 备注: 提案中的次要错误 (不阻塞落地)

### (1) Block2 fn entry 首指令描述错误
Proposal 语义节: "THUMB code starts with `push {lr}` (1c02)"
ROM 实读: 0x0806106e-0x0806106f = 0x0000 (2B padding), 0x08061070-0x08061071 = 0x1c02 = `adds r2,r0,#0` (即 movs r2,r0).
0xB500 才是 `push {lr}`. Block2 fn 是无 push 的 leaf fn, BX LR 退出.
**影响**: 仅 disasm 计划的注释描述不准确. 实际 DisassembleCommand(0x08061070) 操作不受影响. 落地可直接进行, fixer 执行后自行修正描述.

### (2) Exodia 件 passcode 注释有两处错位
Proposal 写 RIGHT_LEG_FORBIDDEN_ONE_CID pw=70903634, LEFT_LEG_FORBIDDEN_ONE_CID pw=08124921;
card-stats.s 显示 RIGHT_LEG slot=0x0FB7 pw=08124921, LEFT_LEG slot=0x0FB8 pw=44519536.
RIGHT_ARM pw=70903634 正确. 这是 card_info.inc 中 `.equ` 注释 passcode 值错误.
**影响**: CID 槽值 0x0fb7/0x0fb8/0x0fb9 全部正确; 仅 passcode 注释文字串位. fixer 应修正:
- `RIGHT_LEG_FORBIDDEN_ONE_CID` 注释 pw=08124921 (非 70903634)
- `LEFT_LEG_FORBIDDEN_ONE_CID` 注释 pw=44519536 (非 08124921)

### (3) EQ/RENAME 双计数报告
Executor report 写 EQ=47 + RENAME=47 (同一批 47 槽同时被计为两类). 实质: 47 槽均为 EQ 操作 (setLabel + equate annotation). 无落地影响, 仅计数描述冗余.

---

## 状态: PASS

所有 13 项核验均通过. 3 处次要标注:
- Block2 push/entry 注释描述错误 (不影响落地)
- 两处 Exodia 件 passcode 注释错位 (fixer 修正 card_info.inc 注释)
- EQ/RENAME 双计报告 (无影响)

以上均属 fixer 落地时可原地修正的 minor items, 不构成 NEEDS_FIX 阻塞.

---

## Reviewer Verdict: F07-Seg-6 = PASS
