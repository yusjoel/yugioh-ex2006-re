# Naming Evaluation: 0x080abcac

> **版本**: v1 (2026-05-15 12:00)
> **状态**: PASSED
> **proposal**: doc/dev/eval/080abcac.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `init_equip_sub_entry_fields_from_slot` — 全小写下划线, 动词 init, 对象 equip_sub_entry_fields, 修饰 from_slot; 无 ARM 助记符冲突 | — |
| R2 | plate WHY | 5/5 | 中文, 含调用方 (0x08095d44/0x080abbd8/0x080bc4a8) + 触发 (装备精灵处理簇) + 副作用 (0x0201e4d0 多字段 + 精灵行缓冲区); 具体地址/常数充足; 字数估计在 200-400 字内 | — |
| R3 | 参数语义 | 5/5 | r0: u8 player_id [0..1]; r1: u8 slot_idx [0..9]; void 返回 (尾调用) — 类型+含义+范围齐全 | — |
| R4 | 返回值 | 5/5 | 明确标注 void (尾调用 init_equip_sub_entry_state_with_sprite_submit) | — |
| R5 | 副作用 | 5/5 | [0x0201e4d0+0x0/+0x2/+0x4/+0x8] 四处写入含地址+含义; via callee 副作用标注 | — |
| R6 | 魔数符号化 | 5/5 | EQUIP_STRUCT=0x0201e4d0, gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14, FIELD8_IS_6=0x6 均有符号名 | — |
| R7 | caller 锚定 | 5/5 | 三个 caller 均有地址+tags+role 描述; 第三个 0x080bc4a8 tags=unknown 但 role 已给出 field spell handler; 满足 form (b) | — |
| R8 | 置信度 | 5/5 | high; 三层证据: 命名 callee 锚定 + 数据标签 + 兄弟簇; 证据数 ≥ 3 | — |
| R9 | 硬规则 | 5/5 | grep 零容忍词全 0; 无全角符号/弯引号/中文顿号 | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-15 12:00 | 45/45 | PASSED | 初始评分 |
