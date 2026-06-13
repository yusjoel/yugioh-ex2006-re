# Refine Review: 05-Seg-4a  [0x0804b4f4..0x0804be38)

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | ✅ | 段起点 0x0804b4f4 == Seg-3 终点; 活动 doc §五 Seg-4 范围 [0x4b4f4,0x4c6e8) 内; Seg-4a 以 0x0804be38 (get_card_effect_category 入口) 为函数边界切分, Seg-4b=[0x4be38,0x4c6e8) 留待; 无跳号/回头 |
| C2 Rule2 | ✅ | 段内零 ROM_INCBIN/.byte 块: grep 确认 asm/05 中落在 [0x4b4f4,0x4be38) 的 ROM_INCBIN 为 0; 仅有 .zero 0x2 THUMB 对齐填充 (在 Seg-3 范围内, 不属本段); 101 .word 全为函数内嵌 literal pool, 均已处理 |
| C3 Rule3 | ✅ | 无独立数据块需做 §5.1 ref-scan; 101 slot 值域 [0xfe5..0x19ef] 全部 < 0x2000, 无 ROM 地址形式 (>= 0x08000000); 零 fn-ptr 槽 — 自主确认 |
| C4 R1 值 | ✅ | python struct.unpack_from('<I', rom, addr-0x08000000) 核对全部 101 槽: 0 mismatches; 内联 immediate 计算式核对: 0xfe<<4=0xfe0 (KURIBOH), 0x90<<5=0x1200 (PENGUIN_SOLDIER), 0xad<<5=0x15a0 (DARK_SNAKE_SYNDROME) 均正确; cmp r5,#0x16 ROM=162d, cmp r5,#0x17 ROM=172d 均正确 |
| C5 R1 复用 | ✅ | 63+3 新建 B-class CID 扫全 constants/*.inc (4883 equates): 0 同值碰撞; CARD_FIELD6_EQUIP_CONTINUOUS=0x16 / CARD_FIELD6_EQUIP_RITUAL=0x17 全 .inc 扫: 0 碰撞; A-class 32 槽对应 31 个现有 CID 常量 + upd_cid_13e9 均在 card_info.inc 中已有且值正确; EKIBYO_DRAKMORD_CID(0x149d) 与 EKIBYO_DRAKMORD_CID_SHIFTED(0xa4e80000) 值域不同、名称不同, 无碰撞 |
| C6 R2 名 | ✅ | 6 个 RENAME 标签 `^[a-z][a-z0-9_]+$` 全合规; 无重复; 63 .equ 常量名无重复 |
| C7 R3 接通 | N/A | 段内无 carve/全局槽需接通 (101 槽全为函数内嵌 literal pool EQ/RENAME, 无 REF 需建 USER-label) |
| C8 R5 现名 | ✅ | grep FUN_ 在 asm/05 行 5080..6474 (Seg-4a 范围): 0 hits; PLATE=0 (无 plate 新建/修改); 无残留 stale FUN_ |
| C9 ASCII | ✅ | 6 个 RENAME EOL 文本全 ASCII 核对通过; 63 个 .equ comment 全 ASCII; 内联 EQ 及 field6 注释全 ASCII; proposal doc/ 中文解释走 Markdown 行 (C9 仅约束 Ghidra 落地文本) |
| C10 carve | N/A | 无指针表条目 (无 fn-ptr, 无 carve 计划) |
| C11 误名 | ✅ | 抽查 10 个函数名: 消费者证据 (asm/03 L207 bl get_card_field_summon_restriction + cmp/bne 验证; asm/04 L11468 bl check_card_id_is_equip_set_a + cmp/beq 验证) 与函数名语义一致; 0 FUNC_RENAME 申报合理 |
| C12 R6 | ✅ | 消费者表含 file:line + 置信度 high; asm/03 L207/L14129, asm/04 L11468, asm/05 L9522, asm/06 多处等关键调用点均可在 asm 中核实; 无零容忍词 |
| C13 残留 | ✅ | python re 精确统计 [0x0804b4f4,0x0804be38) 内 DAT_/DWORD_/PTR_DAT_ 唯一地址: 101; A(32)+B(63)+C(6)=101; 覆盖差集为空; 无遗漏 |

## 附注: A-class 表中 DUMMY_GOLEM 双列问题

proposal A-class 表格中包含 0x0804b7fc/DUMMY_GOLEM_CID 行并标注 "-- NEW (B class)", 同时 B-class 表也正确列出该地址。editorial 标注不影响实际计数: A-class 32 槽 = 31 现有 CID + upd_cid_13e9, 0x0804b7fc 计入 B-class 63 槽, 总计 101 无重复。C5 独立验证 DUMMY_GOLEM_CID(0x18b5) 在 card_info.inc 中不存在, 新建正确。

## 状态: PASS

## 修改清单

无 (所有 C1-C13 通过, 无 NEEDS_FIX 项)。
