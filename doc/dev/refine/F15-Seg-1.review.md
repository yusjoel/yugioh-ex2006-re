# F15-Seg-1 独立复核

## 第二轮 · PASS

本轮冻结清单 SHA-256 为 `0e5fb781a0666774107aaeaf042f8e3abcbbab746befe86cbc15b25c0bb5677e`。独立核验 24 项文件和首轮归档，141 槽表字节一致。28 条 PLATE 中只有计划的 12 条发生文本和字符数变化，其他字段一致。引用扫描、常量证据、Equate 前态、更名基线和查询约定也与首轮一致。独立报告 `f15-seg1-review-round2-independent.json` SHA-256 为 `a665c447ab907287a0cf3b69e78cc8d81f61451e59ce3ff8db6ddbb138770952`。

| 首轮项 | 结果 | 复核依据 |
|---|---|---|
| 1 | PASS | 快照重数为 59 个无 Function 所属的 InstructionDB 起点和 122 个指令字节。提案精确区分 5580 个已有归属字节并保留现有类型和所有权 |
| 2 | PASS | B5348、B54C0、B55AC、B5AD4 明示共享 PRNG。B5576 的 XOR 和 B5590 的原位图回退一致。B55C8 从 r10 读入口玩家以计算偏移，B5878 才读取已保存的 r2 以决定是否执行最终评分门槛 |
| 3 | PASS | B58E8 两条抽样路径按 B59EE/B59F8 分组，B59FE/B5A12 仅在已有组内候选时抽样。B5D28 明示 B5D4A 的 type-B 门槛 |
| 4 | PASS | B5D98 的 r1 在 r5 用作 effect-chain entry，零位图经 B5DB6 共享 epilogue 返回 1。非零时 B5DC0–B5DCE 将 `entry[+2].bit0 XOR entry[+3].bit6` 写到由 B5E20 取得的 `gEquipLpScoreBase`。B675C 的初值门槛及 B67B0 的全局索引与 r9 位图分工准确 |
| 5 | PASS | B697C/B697E 取 bits[20:18]，B6A70/B6AC2 的类别掩码为 `0x38000`。B6AC2 保留 `0xfc0` 的两个 entry type 及 B6B32/B6B44 的全局侧别与位图门槛，三处失败转 comparator/scored fallback |

68 处相关指令编码已直接读取原 ROM 并与汇编交叉核验。C1–C13 通过，B5BAC 更名、五个段内 Thumb 引用、三处 Seg-2 holder、B5D98 三个 EOL 与两个 DATA 增量、B76A4 的 79 个绑定及 F14 源码投影约束继续有效。落地构建与整 ROM 逐字节校验由下一阶段执行。

## 首轮复核记录

范围 `[0x080b5348, 0x080b6c08)`。冻结清单 SHA-256 为 `f92bd4546b6fc97e4172916de40fe1f840e6db4bceb9ac2a69b6f34a10953190`。独立核验 22 项冻结文件。忽略目录证据 `f15-seg1-review-independent.json` 的 SHA-256 为 `132dd7732c15b864a5dbd0636c9ac0b71bd725c9e47c589abe7fc40b0203ed8d`。

## C1–C13

| 项 | 结果 | 证据 |
|---|---|---|
| C1 | PASS | `doc/dev/refine-progress.md:12`，F14 完成后的 F15 首段 |
| C2 | FAIL | 6336 字节都有分类，提案对其中 122 个指令字节的 Function 所属断言错误，见第 1 项 |
| C3 | PASS | 无 §5.1 块。逐字节滑窗扫描 28 个入口的 raw 与 Thumb 值，偶址零命中，奇址 8 命中分属 7 入口，含三处 Seg-2 holder |
| C4 | PASS | 独立读取 141 槽及全部 107 个 Equate 绑定的原 ROM LE 值。B5CD4 的 `0x9ce00000 = 0x139c << 19` |
| C5 | PASS | 复用及新增值按消费者域区分。15 个源码定义和 20 个 Ghidra 新名称含不同类型的增量 |
| C6 | PASS | 141 个 USER 源标签唯一且符合格式 |
| C7 | PASS | 24 个 RAM DATA 增量、5 个偶址 Function DATA 增量、10 个既有 DATA 完整保留。冻结 151 个既有 READ |
| C8 | PASS | 28 条新 PLATE 使用现名或明确投影名称 |
| C9 | PASS | 141 个 EOL 与 28 个 PLATE 均为 ASCII，所有 PLATE 不超过 500 字符 |
| C10 | PASS | 五处段内原始 Thumb 字与目标偶址加 1 相符。Seg-2 的 B701C、B7234、B727C 保留 |
| C11 | PASS | B5BAC 在 restriction 非零且 `[slot+8]==0` 时给 1。新名吻合，唯一 Thumb 源 B6578 |
| C12 | FAIL | 选择器、父调度与若干 case PLATE 对参数、分支或状态的描述与指令矛盾，见第 2–5 项 |
| C13 | PASS | 141 个当前自动字标签一一覆盖。无原始数据块，无 R4 或 carve |

独立字节分区为 2710 条指令、5702 指令字节、564 池字节、70 填充字节。B5D98 冻结 EOL 增量恰为 B6344、B6390、B63F8 三处，body 引用增量恰为前两处到 `gEquipChainSlotRefs` 的 DATA。B76A4 保留完整 79 个绑定。三处 F14 已冻结的源码投影、现有 Function 身份和富引用字段继续作为落地约束。

## 状态 NEEDS_FIX（5 项）

### 1. C2 · 纠正指令覆盖归属

提案完整布局及 disasm 段落都写成所有指令属于当前 Function。初始快照 `extra_units` 中恰有 59 个 InstructionDB 起点、122 个指令字节的 Function 为空，例如 B69C4。更新提案与机器合同中同义断言，精确区分 5580 个已有归属字节和 122 个无归属字节。全体保留当前指令类型、机器流和已存在的 Function body。仍无需 R4。

### 2. C12 · B5348/B54C0/B55AC/B5AD4 选择器

- **B5348** · 恢复此前已核准的共享 PRNG 副作用。B5394 调用 `sample_prng_scaled`，候选超过一个时运行洗牌。保留 B548E 的当前目标名。
- **B54C0** · B5552–B5576 用 mode 0 对 CID 做集合检查，将通过者建成掩码后与原位图 XOR，评分使用差集。B558C–B5590 失败时从原位图采样。改掉“retaining”表述并注明 B5508 与采样会推进共享 PRNG。
- **B55AC** · B55B8 保存 r0 到 r10，B55C8 的 `0x4653` 是 `mov r3,r10`，B55CA 以此左移 4 得到侧别位偏移。删除入口 r3 提供偏移的断言。入口 r2 保存在 `sp+0x54`，B5878–B587C 在最终分值门槛前检查其零/非零。B58C4–B58C8 从原位图随机采样，B55FE 的洗牌也推进共享 PRNG。
- **B5AD4** · 指明从入口 r1 指定的侧别开始，失败后翻转侧别复用顺序（B5ADE/B5B38–B5B40）。B5AF4 洗牌推进共享 PRNG。保留 handler 非零后入队返回 1 的描述。

### 3. C12 · B58E8 与 B5D28 的条件

- **B58E8** · B5932 的回调接收 `(player, 0xb, hand_index)`，非零才继续。两处替换抽样都推进共享 PRNG。B5A02 属于激活检查返回零且 type 为 3 的候选组，B5A16 属于激活检查非零或 type 不是 3 的另一组。两组的首次候选无需抽样，组内已有候选时才采样是否替换。修改将 PRNG 限定于 type 3 的句子。
- **B5D28** · B5D4A–B5D50 在枚举最终进化目标前要求当前 CID 通过 `check_card_id_is_effect_monster_type_b`。在注释写出这一必经门槛，并保留目标 CID 比较及合法槽或牌组条件。

### 4. C12 · B5D98 父帧入口和 B67B0/B675C 的筛选

- **B5D98** · B5DA6 保存入口 r1 到 r5，B696C/B697A 以 r5 解引用 effect-chain entry。位图由 B5DAA 的 helper 返回并在 B5DAE 放入 r9。B5DB0–B5DB6 位图为零时经父帧 epilogue 返回 1，无入队动作。非零路径在 B5DCE 将两字段 XOR 后的有效侧别写入 `gEquipLpScoreBase`，再按 r2 CID 分派。把这四项写进 PLATE，保留共同的 0x2c 帧及机器 BL。
- **B67B0** · B67BA 以继承 r8 的 bit0 比较全局 `[+0]`，相等从 `[+0x1c]` 取槽索引，否则从 `[+0x20]` 取。B67CE–B67DA 在继承的 r9 位图上测试 `(r8.bit0 << 4) + index`。更正从全局选择位图的表述。
- **B675C** · B675C–B6760 的 best score 和索引均为 -1，B678E 只接受严格更高的分数。即使对侧位图有候选，全部分数为 -1 或更低仍会进入随机路径。把“无候选”精确化为“无候选超过初值 -1”。

### 5. C12 · B6962/B6A70/B6AC2 的 packed 字段

- **B6962** · B697C/B697E 与 B69BA/B69BC 的 `LSL #14; LSR #29` 取原字 bits[20:18]。修复 PLATE 的 bits[18:16]。保持解码 link 侧别等于装备 entry 侧别、type 至多 4 和位图位的三项测试。
- **B6A70/B6AC2** · B6A74–B6A82 与 B6AC6–B6AD4 测 `(word & 0x38000) == 0x8000`。称为 bits[17:15] 类别门槛，实际 link 数量是上条的独立字段。B6AC2 的备用直接接受路径还要求 `(entry[+2] & 0xfc0)` 为 `0x480/0x4c0`、全局 `[+0]` 等于装备侧的对侧，并在继承位图验证 `(side << 4) + global[+0x1c]`。B6B20/B6B32/B6B44 各失败分支进入 comparator/scored fallback。用这些精确条件替换笼统的 state 检查。

Mode A 仅修订上述提案事实、相应 PLATE 与直接派生元数据后重新冻结。保留原 ROM 值、槽表、三个内置数据字约定、B5BAC 更名闭包、未来三处 holder、B76A4 绑定与 F14 源码投影。

## Reviewer Verdict: F15-Seg-1 = PASS
