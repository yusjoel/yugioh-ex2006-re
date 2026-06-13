# Refine Review: 05-Seg-4b  [0x0804be38..0x0804c6e8)

Reviewer: independent (C1-C13 self-verified, no trust of proposal conclusions)

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-4b: 0x4be38..0x4c6e8; Seg-4a (0x4b4f4..0x4be38) commit 3155175 已完成; 无回头/跳号 |
| C2 Rule2 | 所有 ROM_INCBIN 块有归宿 | OK | 唯一块 0x4becc/0x54 -> §5.1; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 独立重跑: raw=0 (0x0804becc), THUMB+1=0 (0x0804becd); 穷举 2B step [0x4becc,0x4bf20) 全 sub-address 均 0 引用 |
| C4 R1 值 | ROM 4 字节小端核对 | OK | 抽验 25 槽全部匹配 (0x161a/0x128e/0x1610/0x1615/0x16de/0x186a/0x1983/0x10a8/0x10b3/0x1138/0x114f/0x1228/0x1232/0x12ea/0x12ec x2/0x1529 x2/0x161a x2/0x179c x2/0xffffe9b6/0x0804c6e8 + gap CID 全 8) |
| C5 R1 复用 | 新建常量前无同值现有 | OK | 迭代2确认: 3碰撞全改复用 (EQUIP_CHAIN_PAIR_CARD_MAX/HORUS_LV4_CID/D3S_FROG_CID); Section B 无残留同值; ROM字节3槽独立复核 OK |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | OK | 全 10 个 RENAME label 格式合规 |
| C7 R3 接通 | carve/全局槽 USER-label + DATA-ref | OK | 0 inter-function ROM_INCBIN; 不需 carve |
| C8 R5 现名 | plate 引用全用现名 | OK | FUN_0803088c -> check_effect_slot_summon_path_eligible 已在 asm/02_text_lp_fieldspell.s:9900 确认 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 提议 plate 字符串纯 ASCII; .equ 注释纯 ASCII; CJK 仅在 doc 文本内 (合规) |
| C10 carve | 指针表 +1 核对 | OK | 结构常量 0xffffe9b6/0x0804c6e8 ROM 精确匹配; switchD 表项 0x4c6e8+ 为 even addr (MOV PC,r0 软件 switch, 非 THUMB fn-ptr, 不需 +1) |
| C11 误名 | 函数体/全局与函数名矛盾 | OK | 14 个函数名语义与函数体一致; 无 FUNC_RENAME 信号 |
| C12 R6 | 关键槽语义有证据+置信度 | OK | 6 函数 R6 证据; 无零容忍词; file:line/数值证据均已给出 |
| C13 残留 | 段内所有残留自动名槽被覆盖 | OK | 独立 grep: 唯一 DAT_0804xxxx 槽 99 个; EQ(25+64)+RENAME(8+2)=99; 覆盖完整 |

## 状态: PASS

## 迭代历史

- 迭代 1: NEEDS_FIX(3 items) — C5 x3 碰撞 (GUARDIAN_TRYCE_CID/HORUS_BLACK_FLAME_LV4_CID/D3S_FROG_CID 未复用现有)
- 迭代 2: 3 碰撞全改复用; Section B 57 新建 CID 无残留同值; C13 checksum 28+61+8+2=99 不变; 终核 PASS

## 其他备注 (不阻塞)

- **switchD_0804c6dc 结构核实**: 0x4c6dc 处字节 `0x4687` = THUMB `MOV PC,r0` 指令 (函数体末尾间接跳转)；后接 2 字节对齐 padding + 2 个 literal pool 槽 (DAT_0804c6e0/c6e4)。跳转表 (switchdataD_0804c6e8 起) 位于 Seg-5，不属于本段处理范围。proposal 对此判断正确，C2/C10 均 OK。
- **新建 CID 数修正后**: 60 新 -> 57 新 (减去 GUARDIAN_TRYCE/HORUS_BLACK_FLAME_LV4/D3S_FROG 三条); Section A reuse +3 条 (EQUIP_CHAIN_PAIR_CARD_MAX/HORUS_LV4_CID/D3S_FROG_CID); EQ 槽总数保持 25+64=89 -> 变为 28+61=89；slot 覆盖总数 99 不变。
- **C3 独立 ref-scan 确认**: 0x0804becc (0x54 bytes = 0x4becc..0x4bf20) 全 ROM raw 引用=0, THUMB+1 引用=0, 穷举 42 个 2B 步进 sub-addr 均 0；§5.1 判定成立。

## Reviewer Verdict: 05-Seg-4b = PASS
