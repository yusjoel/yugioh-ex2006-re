# Refine Review: F13-Seg-4

- 范围：`[0x080a0840,0x080a1658)`，3608 B。
- Proposal：`doc/dev/refine/F13-Seg-4.proposal.md`，SHA256 `2dba3097eafc80290faa35c4a8d7e02541b3a7cd7f08676c5d7f1cdcda2d4eba`。
- Plan：`output/refine-run-20260831-194634/f13-seg4-plan.json`，SHA256 `66e0dfd362db5f82670dd3cbcaa5c878e25e5c8ed9fd91ad32bbdef819c823fa`。
- 独立机械证据：`f13-seg4-review-slots.json`、`f13-seg4-review-constants-names.json`、`f13-seg4-review-block.json`、`f13-seg4-review-fresh-summary.json`。

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 Rule1 | 段范围与路线图一致，未跳号/回头 | ✅ | 活动文档 §五将 Seg-4 定为 `[0x080a0840,0x080a1658)`；Seg-1 至 Seg-3 已闭合，Seg-5 从 `0x080a1658` 开始。Proposal 未扩入 Seg-5。 |
| C2 Rule2 | 每个 `ROM_INCBIN`/`.byte` 块都有归宿 | ✅ | 段内恰有一块 `ROM_INCBIN 0xa0b20,0x818`，无 `.byte`；Proposal 将该块完整归入 §5.1，没有静默保留。函数间 `.zero 2` 均为对齐。 |
| C3 Rule3 | §5.1 块确为 0 可信引用 | ✅ | 独立扫描入口 `0x080a0b20` 的 raw/THUMB\|1 均为 0；1036 个半字候选共得 raw 391、odd 367 次字节命中，经当前真实机器行和结构化 `.word` 源地址过滤后可信来源为 0，当前 asm 直接 B/BL 入边也为 0。递归解码得到 822 指令/1754 B、71 literal words/284 B、17 处 padding/34 B，精确合计 2072 B。汇总见 `f13-seg4-review-fresh-summary.json`。 |
| C4 R1 值 | 每个 EQ value 等于 ROM 小端 word | ✅ | 34/34 EQ 槽逐地址读 ROM 均与 Plan 一致；57 个动作槽的原 word 也全部一致。 |
| C5 R1 复用 | NEW 前无可复用的同域常量 | ✅ | 8 个 NEW 名称均未定义；7 个值没有现有 `.equ` 同值命中。`0x1d8c` 唯一同值项 `NAME_INPUT_BG1CNT_INIT` 属 BG 控制值域，与本段的 `gP1LifePoints` 字段偏移不同，不可复用。另 14 个既有 constant/global 均按现值复用。 |
| C6 R2 名 | 槽名格式、唯一性、碰撞 | ✅ | 57 个新槽名均匹配 `^[a-z][a-z0-9_]+$`，地址后缀消除同类碰撞；全计划无重复地址、重复动作或既有符号碰撞。 |
| C7 R3 接通 | 全局槽有 USER label 与 DATA ref 计划 | ✅ | 16 个 REF 槽均指定目标 USER symbol 与 operand-0 `DATA/USER_DEFINED` 引用；`gEffectEntryArray` 复用并规范同一主对象，不创建同址 alias。7 个 RENAME 槽明确保留现有 `gP1LifePoints` 引用。无 carve。 |
| C8 R5 现名 | Plate 使用现名，无旧自动名 | ✅ | 7 条新 PLATE 均使用当前函数/global/constant 名；文本中没有 `FUN_`、`DAT_`、`DWORD_` 或旧被替换名称。 |
| C9 ASCII | 所有 PLATE/EOL 为 ASCII | ✅ | 57 条 EOL 与 7 条 PLATE 全部为 ASCII；PLATE 长度为 167–466 字符，最大 466，均不超过 500。 |
| C10 carve | Thumb 指针表 `+1` 保值 | ✅（N/A） | 本段无 carve、无函数指针表动作；§5.1 块保持原 `ROM_INCBIN`。 |
| C11 误名 | 函数体与函数名无矛盾 | ✅ | 7 个函数逐体抽查：前三个分别处理 sprite-state/effect/LP-delta，router 与 wrapper 名称吻合；phase A/B 分别执行 Second Coin Toss 与 Dice Re-Roll 的 equip-zone sprite 状态机。无需 `FUNC_RENAME`。 |
| C12 R6 | 关键语义有消费者证据和置信度 | ✅ | Proposal 给出 `asm/13_equip_placement.s:6652-7508` 的六组消费者证据，均标 high。`0x11f` 对应 game string 287；`0x150f/0x16a5` 经 data.md、card-stats、passcodes 三方对应卡名；`0x1d8c/0x1d98/0x1d9a` 的读取宽度和用途由 phase A/B 机器行支持；`0x805b/0x805c` 与非零 player 分支及内联 `0x5b/0x5c` 成对。8 个 NEW 的目标文件和符号化方式可落地。 |
| C13 残留 | 段内自动名槽全部覆盖 | ✅ | 独立枚举为 57 个 4 B 自动槽（14 `DAT_` + 43 `DWORD_`）；Plan 精确覆盖为 34 EQ + 16 REF + 7 RENAME，无遗漏、越界或重复。裸块单独计入 C2/C3，块头没有额外自动标签。 |

## R1-R9 结论

- R1-R3：常量值、复用、槽命名和引用接通计划完整。
- R4/R7：唯一裸块满足 Rule 3，故不执行 disasm/carve；分类证据完整。
- R5/R6：7 条 PLATE 与全部槽语义均由现名和消费者支持。
- R8：本段不新增图形资产分类；两个 OAM sprite code 由调用参数与 player 分支证明。
- R9：Proposal 已列出备份、dry-run、全量导出、构建、ROM SHA1 与保存后只读核验；这些由 fixer 落地阶段执行。

## 状态: PASS

没有需要回改 Proposal 的项目。Proposal 中 PLATE 最大长度概述写作 461，独立实测最大值为 466；两者都低于 500 字符门槛，不影响 C9 或落地内容，fixer 以 Plan 中 7 条原文为准。

## Fixer 落地清单

1. 写入前备份 Ghidra `.rep`，按 Plan 先 dry-run 全部前态 guard。
2. 落地 34 EQ、16 REF、7 RENAME；保持 57 个 Data4、59 条 literal READ 和 7 条既有 `gP1LifePoints` DATA ref 的身份与来源。
3. 新增 8 个 constants；复用 14 个既有 constant/global；只把 `0x0201b590` 的现有主对象规范为 `gEffectEntryArray`，不创建 alias 或 RAM Data。
4. 全量替换 7 条 ASCII PLATE 和 57 条 ASCII EOL；Function ID、名称、body、incoming 不变。
5. 保持 `[0x080a0b20,0x080a1338)` 原 `ROM_INCBIN`、ROM 字节及 Ghidra undefined 前态，并在活动文档 §5.1 登记该 2072 B 块及独立 0 引用证据。
6. 全量导出、inject/split、`export_all.py`、build；验证输出 ROM 逐字节一致且 SHA1 为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。
7. 保存后以 fresh read-only 检查槽、函数、PLATE/EOL、裸块与 DB 持久化状态，并更新 Seg-4 完成记录；本段无函数改名，不同步命名 CSV/registry。

## Reviewer Verdict: F13-Seg-4 = PASS
