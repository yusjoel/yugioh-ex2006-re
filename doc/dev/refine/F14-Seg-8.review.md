# Refine Review: F14-Seg-8

第二轮审查使用冻结清单 SHA256 `fa023e29fa8ba9b64a65f9c04c680f9ba2d6cc0f7e3348c4a46febd5aa6f355e`。首轮评审存于 `output/refine-run-20261028-105948/f14-seg8-review-round1/doc/dev/refine/F14-Seg-8.review.md`。

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1 地址序 | ✅ | 路线图第 168 行与半开区间 `[0x080b04a8,0x080b153c)` 一致。 |
| C2 | Rule 2 数据块分类 | ✅ | 1659 条 mnemonic、160 条指令 `.hword`、101 个池槽和 52B 填充完整覆盖 4244B。 |
| C3 | Rule 3 引用扫描 | ✅ | 全 ROM 对槽和入口的重扫见 `f14-seg8-review-independent-scan.json`。第二轮对四个改名入口再次扫 raw 和 Thumb，全部 0 / 0。 |
| C4 | EQ 数值 | ✅ | 101 槽 TSV 与首轮逐字节相同，原 ROM SHA1 为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。首轮独立验证了所有槽值和 GAS 表达式。 |
| C5 | 常量复用 | ✅ | 56 行复用。5 行使用经消费者核实的 4 个新常量，含 CID 1525 对应的 KA-2 Des Scissors。 |
| C6 | 槽名 | ✅ | 101 个唯一标签符合命名格式，与编号模块已有定义无碰撞。 |
| C7 | 引用接通与保留 | ✅ | 35 个新 USER DATA、5 个既有 DATA 和 114 个入向 PC READ 的合同保持。四个 RAM 目标的 19 条旧引用在源与目标记录中逐条对应。 |
| C8 | PLATE 使用现名 | ✅ | B0BC0 引用实际 callee。B1114 和 B135C 使用 B0C60 的获批新名。 |
| C9 | ASCII | ✅ | 101 个 EOL 和 15 个 PLATE 行均为 ASCII。实际最长为 B0C60 的 497 字符，以 TSV、plate plan 和 selfcheck 为准。 |
| C10 | Thumb carve | ✅ | 无 carve 或 ROM 指针池表达式新增。 |
| C11 | 函数名与行为 | ✅ | 四项改名的 9 个 BL 均由原 ROM 半字重新解码，目标与汇编和冻结计划一致。每项保持 Function ID、代码范围、代码 SHA256 及引用 CORE6。 |
| C12 | 消费者与 ABI | ✅ | 四处修正经调用点、写入指令和返回路径复核。详情见下。 |
| C13 | 自动名覆盖 | ✅ | 96 个 DAT/DWORD 与 5 个 PTR 定义精确对应 101 个槽动作。 |

## 状态: PASS

- B0BC0 在 B0BFA 调用 `check_field_spell_last_warrior_placeable`。B0BFE 检查其返回值，成功路径从 B0C02 重新读取 field8。只有 B0C2E 的结果非零才走到 B0C38/B0C3A 写 field6 和 field8。新 PLATE 使用实际名称，也删除了对拒绝条目的清除断言。
- B0C60 通过 B0CB4 从固定优先序取首个可放置槽，在 B0CE4/B0CE6/B0CEC 写入槽字段。B0D38 的特例涵盖两个 Maju Garzett ID 和未分配的 0x1388。新名为 `prepare_first_placeable_monster_slot`，保留 ID 7167。B126A/B1380 是两个直接调用，调用者 PLATE 和引用派生目标名同步投影。registry、CSV 和 inventory 使用原地址行。
- B1114 从 B1154 读取该玩家的 `gP1ZoneHandCount`，以 4B 步长访问 `gP1FieldArrayCBase`。B1316 保存候选索引，B1330 返回该索引或初值 -1。外部 0x080bc284 将其传给操作同一数组的 `execute_field_spell_equip_placement`。
- B135C 在 B13E8 写 `result+0x18`。B13FA/B13FC 使用 r0 承载返回地址，B142A/B169C 的调用者从输出结构取值。新 PLATE 按输出结构描述该 ABI。

第二轮与首轮比较，只有 B0BC0、B0C60、B1114、B135C 四行 PLATE 合同变化。实际写入为段内 13 条与段外 B153C 1 条，B1458 为保留行。提案正文仍有首轮的最大长度 439，执行与验收使用实测最大长度 497。

B0C60 的 TSV prototype 已投影为 `undefined prepare_first_placeable_monster_slot()`，与首轮相比仅替换函数名。B06B4、B135C、B1400 的 TSV prototype 保留旧名，最终数据库投影各只替换为获批新名。审查对九条调用引用的投影逐条检查，仅改变派生的目标主符号名。
