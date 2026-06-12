# Refine Review: F03-Seg-8

Seg range: `[0x0803c774, 0x0803d91c)`, file `asm/03_equip_chain_hand.s`, 13 functions.
Review iteration: 2 (fix-iter-1 applied; fast confirmation pass).

## 核验结果 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围 vs §五路线图 | PASS | 范围 0x3c774..0x3d91c 与 roadmap 一致; 13 fn 全在范围内; Seg-9 边界 0x3d91c 确认. 不回头不跳号. |
| C2 Rule2 | ROM_INCBIN/.byte 块 | PASS | Seg-8 范围内无 inter-function incbin 或孤立 .byte. 无需处理. |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | Seg-8 无 §5.1 登记; 13 个函数入口全经 switchD_0803be70 switch table 分派 (裸偶地址, raw=0/thumb=0 符合预期). |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | PASS | 独立 python 核对 26 个关键槽, 全部与 ROM 一致 (含 0x0803c7c4=0xffbfffff / 0x0803c86c=0x00000fa7 / 0x0803cd0c=0x0201bcc2 / 0x0803d8f4=0x00000818 / 0x0803d918=0xffdfffff 等). |
| C5 R1 复用 | 新建常量前确无现有同值 | PASS | 独立 grep 全 19 个 constants/*.inc 对全部 18 个新值 (11 duel_field + 3 ewram + 4 card_info): 无重复. |
| C6 R2 名 | 槽名格式合规, 无碰撞 | PASS | RENAME label `normal_summon_switch_table_ptr` 合规; 全部 REF slot labels 和新 const 名符合 `^[a-z][a-z0-9_]+$`. |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 无 carve 块; 3 个新 ewram 全局各有对应 REF slot; 全部 REF slot 有 gas_label + slot_label. |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | PASS | Seg-8 内 11 个函数 plate 含 FUN_ 引用, PLATE=11 计数正确. 两处 full rewrite 各提供纯 ASCII 替换文本. |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 独立扫描 asm 行 14327-16741: non-ASCII = 0. 两处提议替换文本无 CJK. |
| C10 carve | 指针表条目 +1 核对 | PASS | 唯一 RENAME 槽 0x0803d224=0x0803d228 为 data table ptr (偶数, 不需 +1). ROM 核对一致. |
| C11 误名 | 函数名无矛盾 FUNC_RENAME | PASS | 13 函数体与名称交叉核对; clear_equip_chain_active_state plate 旧地址 0x0201b290 属注释错误 (已列入 PLATE 修正), 非函数名矛盾. FUNC_RENAME=0 正确. |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | 消费者证据表对 11 个关键槽各给出函数名/asm 行号/指令序列/置信度; BEWD=0x0FA7 / A Deal with Dark Ruler=0x165A 经 card-stats.s 坐实; gap CID (0x0FA6/0x11ED) 标 low-conf. 无零容忍词. |
| C13 残留 | 所有 DAT_/PTR_ 均被覆盖 | PASS | Seg-8 范围 DAT_ 121 + PTR_gP1LifePoints_ 15 = 136 个唯一槽; EQ=82 + REF=53 + RENAME=1 = 136. 覆盖率 100%. |

---

## Fix-iter-1 确认 (本次核验重点)

4 项修改均已正确落入 proposal:

| # | 内容 | 验证位置 | 状态 |
|---|------|----------|------|
| #1 | Executor Report + 槽表页脚改为 EQ=82/REF=53/total=136 | proposal 第 569 行 + 第 170 行 + Fix log 第 595-596 行 | CONFIRMED |
| #2 | PLAYER_BLOCK_STRIDE x15, DISPLAY_SEQ_STEP_LOCK_OFF x11, reuse=43, total EQ=82 | proposal 第 214/217/226/282 行 | CONFIRMED |
| #3 | duel_field.inc section title "11 new offsets/masks" + C5 note "all 11" | proposal 第 455 行 + 第 472 行 | CONFIRMED |
| #4 | `.equ DISP_SEQ_STEP_LOCK_A_OFF, 0x0000080a` (8 位十六进制) | proposal 第 464 行 | CONFIRMED |

交叉校验: 82+53+1=136; DAT_121+PTR_15=136. 均一致.

---

## 状态: PASS

---

## Reviewer Verdict: F03-Seg-8 = PASS
