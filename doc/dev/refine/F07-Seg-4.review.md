# Refine Review: F07-Seg-4

段范围: ROM `0x0805f1cc..0x0805fc94`, asm `asm/07_equip_effect_chain.s` (L7518..9410)

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | 活动 doc §三 Seg-4=0x5f1cc..0x5fc94，与 proposal 完全吻合 |
| C2 Rule2 | 全部 ROM_INCBIN 块有归宿 | PASS | 5 块全部分类为 disasm (R4)，每块均在 0x09e3xxxx/0x09e4xxxx handler table 找到 THUMB+1 引用 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | §5.1=0，无需登记；5 块全有引用 |
| C4 R1 值 | EQ value == ROM 4字节小端 | PASS | **iter-2 复核**: ROM[0x5f492]=0x4770(bx lr 指令，非数据); ROM[0x5f494]=0x0201c4e0(gP1LifePoints) ✓; ROM[0x5f498]=0x00001cf4(FIELD_STATE_OFF) ✓。Block1 literal pool 地址已由 0x5f492/0x5f496 改正为 0x5f494/0x5f498，与 ROM 字节完全吻合。clearListing(0x5f47e, 0x5f49c) 覆盖两槽正确。其余 EQ 槽抽查 9 个全部一致 |
| C5 R1 复用 | 新建 constants 无现有同值 | PASS | 5 新建 (gDuelEquipCtx/FUSHI_NO_TORI/TSUKUYOMI/SWARM_OF_SCARABS/LIFE_ABSORBING_MACHINE)：全部 grep 0 命中。SWARM_OF_SCARABS=0x152a 与 duel_field.inc 碰撞：不同域，card_info.inc 新建 CID 正确 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`，无碰撞 | PASS | 全部 47 槽 label + 5 个 disasm 函数名均合规 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | PASS | PTR_ 槽已有 `.word gP1LifePoints` DATA-ref；gP1LifePoints 全局 label 在 ewram.inc 已建 |
| C8 R5 现名 | 无残留 stale `FUN_` | PASS | grep 段范围 3 处 FUN_ 全在 proposal PLATE 计划中覆盖 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | grep 段内非 ASCII：0 命中 |
| C10 carve | 指针表条目 +1 核对 | PASS | DWORD_0805f28c=0x0804b049 = check_card_is_amazoness_type(0x0804b048)+1；ROM 实读一致 |
| C11 误名 | 函数体全局 vs 名无矛盾 | PASS | 34 个原有函数名无明显误名；FUNC_RENAME=0 经抽查合理 |
| C12 R6 | 关键槽语义有证据，无零容忍词 | PASS | **iter-2 复核**: Block2 plate 已改为 `slot[+0x14].bit10 set (lsls r0,r0,#21 -> blt)`，bit 位置正确 (31-21=10)。机器码 0x5f8de=0x0540 自主解码: imm5=21, bit_tested=31-21=10 ✓。函数名 check_zone640_opponent_turn_bit10_for_cid_151c 一致。板注文本 ASCII 纯净，无零容忍词 |
| C13 残留 | 段内所有残留自动名槽全覆盖 | PASS | 实测 36 DWORD + 9 DAT + 2 PTR = 47 总；EQ=42+RENAME=1+REF=4(2 PTR 计入 REF) = 47，missing=0 |

## 状态: PASS

## iter-2 修改项验证

### #1 (C4) Block1 literal pool 地址 — 已解决

iter-1 问题: proposal 写 0x5f492/0x5f496 (前者为 bx lr 指令 0x4770 地址)。

iter-2 复核结果:
- ROM[0x5f492] halfword = 0x4770 (bx lr，非数据槽) — 确认 0x5f492 不是 literal pool
- ROM[0x5f494] = 0x0201c4e0 (gP1LifePoints) — 正确
- ROM[0x5f498] = 0x00001cf4 (FIELD_STATE_OFF) — 正确
- proposal 现写: "Literal pool: 2 slots at 0x5f494 (gP1LifePoints) and 0x5f498 (0x1cf4=FIELD_STATE_OFF)"
- clearListing(0x0805f47e, 0x0805f49c): 0x5f494 in [0x5f47e, 0x5f49c) = True; 0x5f498+4=0x5f49c 边界对齐
- **RESOLVED**

### #2 (C4/C12) Block2 bit21 -> bit10 — 已解决

iter-1 问题: plate 与函数名使用 bit21，实际应为 bit10 (lsls #21 -> 31-21=10)。

iter-2 复核结果:
- ROM[0x5f8de] = 0x0540: THUMB LSL 编码 bits[10:6]=10101=21, 即 lsls r0,r0,#21
- 31 - 21 = 10，bit 位置正确
- 后续 0x5f8e0=0x2800 (cmp r0,#0), 0x5f8e2=0xdb05 (blt): blt taken 当 N=1 即 bit10=1
- 函数名已改: check_zone640_opponent_turn_bit10_for_cid_151c — 正确
- plate 已改: "slot[+0x14].bit10 set (lsls r0,r0,#21 -> blt)" — 正确
- **RESOLVED**

## 备注 (不影响状态)

- Sub-function analysis 描述 "bit10 set -> return 1; else return 0" 方向反 (实际 bit10=1→blt taken→return 0; bit10=0→return 1)，但该文本为 proposal 内部分析注释，非 Ghidra plate/EOL 绑定文本，不触发 C12 失败。
- Block3 分支方向 (bgt/beq/b 三目标 0x5f964/0x5f966) 前轮已核，未变动。
- Block4 beq+0 / Block5 bls+0 前轮已核，未变动。
- 47 槽覆盖计数: EQ=42 + RENAME=1 + REF=4(含 2 PTR) = 47，统计自洽。
