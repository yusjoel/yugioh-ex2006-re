# Refine Review: F14-Seg-7（第二轮）

## 审查输入

- 范围：`[0x080af120, 0x080b04a8)`，共 5000 B。
- 当前冻结清单：`output/refine-run-20261028-105948/f14-seg7-freeze-manifest.json`，SHA256 `c70488ece61aaff34168919e82b5f007422ba27841a1ce248fbd8b86226470f0`。
- Proposal：`doc/dev/refine/F14-Seg-7.proposal.md`，SHA256 `af76f80ef1efe54a5104e337e22d5ef3801f816444cedd14e2e74e80c5bb16cf`。
- Slots：`doc/dev/refine/F14-Seg-7.slots.tsv`，SHA256 `ac9f3d0a065408905c8c3989a65163874207a112cd1ec5ccb4287cf4a9b2e553`。
- Plates：`doc/dev/refine/F14-Seg-7.plates.tsv`，SHA256 `bbc930a2d949407da085e3c02f5938f10fd0adfe4bd05b6cd596a083d434daeb`。
- 第二轮独立审计：`output/refine-run-20261028-105948/f14-seg7-review-round2-audit.json`。

当前 manifest 的 15 个 `review_basis` 与 11 个 `immutable_inputs` 已逐项复算路径、字节数与 SHA256，26/26 一致。首轮 32 文件归档由 `root-f14-seg7-round1-archive.json` 固定，归档清单 SHA256 为 `3980e84ab6ded292f8daadb8fd390d17e86ea28d6e72758615da4012fc085ce3`；首轮 review/audit 哈希分别为 `693c5c2d19cddad8c176fd2289a84435b4bd82c75664713347b67d65bd2295ab` 与 `cabcfeccfb32d4c90d9b62ae2c1ea362d9a8175e610377216c9144f3db5ac383`。

P0 通过：输入齐全、非空，proposal 禁止标记与禁止措辞命中数为 0。

## Mode A 差异复核

- 149 行 slots 与首轮逐字节相同。
- 25 行 plates 中仅 `080af4e8`、`080af8cc`、`080af940`、`080afc24`、`080bb9b8` 发生变化；每行仅 `new_plate` 与 `new_plate_chars` 两字段变化，共 10 个 cell。其他 20 行逐字节相同，五行全部 before-state 字段也保持一致。
- Proposal 的语义差异仅为上述五项 ABI/callee/phase CFG 订正；slot、函数投影、carve、machine/selfcheck 动作没有扩张。
- 当前 118 个受保护 source 与基线一致；15 个物理 DB 文件的 current/backup 共 30 次哈希检查均一致。

## 首轮五项关闭验证

1. `080af4e8`：`asm/14_equip_ai_scoring.s:16970-17010` 显示 r1 入函数即被覆盖，r2 是循环内局部 CID，范围来自固定 `0x0fb7/0x0fbb`。新 267-char PLATE 与首轮要求逐字一致。
2. `080af8cc`：`asm/14_equip_ai_scoring.s:17546-17575` 没有读取 r2；前三个调用接收 `low16(r1)`，第四个接收完整 r1，任一返回非零即返回 1。新 367-char PLATE 与真实 OR 控制流一致。
3. `080af940`：`asm/14_equip_ai_scoring.s:17608-17627` 将原始 player 经 r3 传回 r0 后调用 `count_available_effect_zones`，没有 opponent 转换。新 250-char PLATE 已订正。
4. `080afc24`：`asm/14_equip_ai_scoring.s:18054-18064` 的直接 BL 目标为现名 `check_slot_full_activation_eligibility`；新 360-char PLATE 已使用该现名。
5. `080bb9b8`：`asm/15_equip_target_summon_zoom.s:7968-7978,7993-8008,8232-8253` 证明仅处理 phase 0/1；phase 只在 phase-0 扫描耗尽后递增，phase 0/1 接受路径都直接返回 0，其他 phase 与 phase-1 失败返回 1。新 432-char PLATE 与完整 CFG 一致。

五条文本均为纯 ASCII，字符数字段与实长一致，且 plate plan 与 registry plan 使用同一终稿。

## 核验（C1-C13）

| # | 检查 | 结果 | 独立证据与结论 |
|---|---|---|---|
| C1 | Rule1 地址序与路线图 | PASS | 活动路线图、proposal 与 TSV 均为 Seg-7 `[080af120,080b04a8)`，未跳段或回退。 |
| C2 | Rule2 所有 raw 块有归宿 | PASS | 当前模块独立测绘仍为 2115 InstructionDB（1985 mnemonic + 130 `.hword`）、4328 B code、149 words/596 B、76 B padding、raw 0 B，总计 5000 B。段内无遗漏 `ROM_INCBIN/.byte`；段外获批 carve 完整覆盖 25×u16。 |
| C3 | Rule3 §5.1 块为全 ROM 0 引用 | PASS | 本段无 §5.1。第二轮重新逐字节扫描 raw 与 THUMB\|1：AF3B0/AF72C/AF940/AFC24 均 0 holds；AF980/AF984 各只有批准的 odd callback 源；AF9C0 的唯一 `082979d1` 命中仍是无对象的未对齐资产偶合；表基址 AB28 仅有 AF804 真引用。 |
| C4 | R1 EQ 值等于 ROM 小端字 | PASS | 149 个槽重新读 ROM，`original_value`/`old_bytes` 错误数为 0；106 个 EQ 的 operand/value 合同沿用字节完全不变的首轮输入。 |
| C5 | R1 常量复用 | PASS | 9 CID、4 score、RAM 标签与 2 callback aliases 的复用审计保持成立。`0xfffffc18` 的既有同值名属于 LP 域，不能替代 score 域定义；九张卡的 ID/stats/passcode/data.md 四层证据未变。补充全局 Equate 前态证据 SHA256 `a0ce3dd3e798a6842382ca8b9cfd04e2264b81507ac46e225f1db1f699759b05` 与动作范围一致。 |
| C6 | R2 槽名与唯一性 | PASS | 149/149 final labels 满足 `^[a-z][a-z0-9_]+$`，无重复或现有全局 label 冲突。 |
| C7 | R3 数据接通 | PASS | 9 个 `REF_PRESERVE` 原 DATA ref/core6 精确保持；34 个 `REF_ADD` 均为一条 USER_DEFINED DATA/op0/primary。B00C 的 13 条旧引用与新增 AFCB0、AB28/AB2A 的旧 READ 与新增 AF804 DATA ref 均分层冻结。odd callback 只加 Equate，不建立奇地址 Symbol/Data/ref。 |
| C8 | R5 PLATE 使用现名且陈述准确 | PASS | 五个首轮问题已关闭；25 条 PLATE 全部使用现名，无 `FUN_/DAT_/DWORD_/PTR_DAT_/UNK_` 残留。其余 20 行未变化。 |
| C9 | ASCII | PASS | 25 条 PLATE 与 149 条 EOL 全为 ASCII；char count 全部准确，新 PLATE 最大 435 chars。 |
| C10 | carve 指针与 THUMB `+1` | PASS | carve `[09e5ab28,09e5ab5a)` 为 25×u16 CID 表而非函数指针表，SHA256 `c339eb5246b0053978f633d8969b2307fefbb0153f6087e8469ec5c5f3417d33`；循环实际覆盖 index 0..24，AB5A padding 与 AB5C 后继 pointer 受保护。两个 callback 原值为偶地址 Function `+1`，且不创建 odd 对象。 |
| C11 | 函数误名 | PASS | AF3B0/AF72C/AF940/AFC24 四个 rename 及 AF980 create 仍与 body、caller、极性和返回语义一致；Mode A 未改变这些合同。 |
| C12 | R6 证据、ABI 与控制流 | PASS | 五个首轮 ABI/callee/CFG 问题均由真实指令重新核对并关闭；proposal 对应重点陈述已同步，禁止措辞命中 0。其余关键槽、card identity、carve 和 callback 证据沿首轮不可变归档连续成立。 |
| C13 | 残留自动名覆盖 | PASS | 149 个 word 槽一对一覆盖（106 EQ_ADD + 34 REF_ADD + 9 REF_PRESERVE），地址唯一；无 raw。21 个既有 body 共 4324 B，加 AF980 新 body 4 B，精确覆盖 4328 B code。 |

## 状态: PASS

首轮五项修改清单全部关闭，第二轮未发现新增问题。当前 proposal 可进入 Mode B Phase 1；本结论不授权提前持久化，也不改变后续脚本静态审查、dry-run、强制回滚验证和 byte-identical 红线。

## Reviewer Verdict: F14-Seg-7 = PASS
