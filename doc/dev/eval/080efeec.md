# Naming Evaluation: 080efeec

> **版本**: v1 (2026-05-31 06:50)
> **状态**: PASSED
> **proposal**: doc/dev/eval/080efeec.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `recv_sio_deck_sync_packets`: verb=recv, object=sio_deck_sync, qualifier=packets; 合法 | — |
| R2 | plate WHY | 5/5 | 含 caller (0x080eda30)+触发+SIO 接收逻辑+副作用; 约 200 字 | — |
| R3 | 参数语义 | 5/5 | r0 标注为 "入口被 DAT 覆盖, 实质无 APCS 输入" (内部加载); r1=dest_ptr; 正确区分 | — |
| R4 | 返回值 | 5/5 | Sub-case E; LAB_080f00b8 movs r0,#0 (busy/error) / LAB_080f00ba ldrh r0,[r0,#0] (last slot halfword); 两路枚举 | — |
| R5 | 副作用 | 5/5 | [dest_ptr+slot_offset], [0x030007d2], 两个 counter bytes 全部列出 | — |
| R6 | 魔数符号化 | 5/5 | SYNC_STATE_BASE=0x030007d6, RECV_PHASE_MASK=0x30, CARD_BLOCK_OFF_A=0x436 等命名; 无裸 hex | — |
| R7 | caller 锚定 | 5/5 | indeg=1, caller 0x080eda30 含 addr+tags+role | — |
| R8 | 置信度 | 5/5 | med; L1(asm lines 412766-413012)+L6(named callee); 独立置信度/升级路径节含可操作步骤 | — |
| R9 | 硬规则 | 5/5 | 零容忍词 0; 无 hiragana/katakana; `華` (U+83EF) 仅出现在节标题非 plate 内容, 且为 CJK unified; plate 内容无 kana | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-31 06:50 | 45/45 | PASSED | 初评通过 |
