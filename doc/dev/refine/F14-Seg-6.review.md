# Refine Review: F14-Seg-6（第二轮）

## 审查基线

- 段范围：`asm/14_equip_ai_scoring.s [0x080ade8c,0x080af120)`，4756 bytes。
- proposal：`a6c4b189af17b7c8d2340da93ba9790f284de71b015d35b42950fec5e056975e`
- slots：`d370766bbade690b64ff31eec01beb6367eae2e8f7e761e7c5b4cb9253de557f`
- plates：`76e193cf960f777ebf42bcf2aee740112c935fd3e4dc360223c1d62527cfcec2`
- freeze manifest：`f0c7fd24647d3526e707737d57f95e71e9e1496efcbc513ee81a9101847da456`；独立重算 25 个 `review_basis` 的 `bytes` 与 SHA256，差异为 0。
- 第一轮不可变依据：`output/refine-run-20261028-105948/f14-seg6-review-round1/`；review SHA256 `c4a0b9d54660e2e8f0ce7f61546873d7d6aa94bfdbc3515ffd1ae0f229bd64cd`，audit SHA256 `f5681bc6aacd801e1960fc483f729f0357044768662edb8772b148ac58f7aa02`。
- 本轮独立证据：`output/refine-run-20261028-105948/f14-seg6-review-round2-audit.json`。

## 第二轮独立复核摘要

1. 独立逐项验证当前 25 个冻结输入，并重新核对 113 个 source 文件与 15 个物理 DB 文件；current/backup 共 30 个 DB 文件对的 size/SHA256 差异为 0。slots TSV 字节未变，因此第一轮对 143 个 ROM word、147 条 PC READ、DATA 引用、常量值、ABI、返回路径及卡身份的逐项独立证据连续有效。
2. 独立比较两轮 plates TSV：16 行中仅 `0x080ade48` 行的 7 个批准后态字段变化；16 条新 PLATE 正文均未变化，其余 15 行所有字段精确相同。ADE48 的 28 条 incoming 保持 from/to/operand/type/source/primary/target ID/type/source，仅派生 `target_primary_name` 改为 `find_first_empty_slot_by_card_id`。
3. 独立重读 ADE48 body 与 28 个调用点：`LSL/LSR #19` 提取 bits12:0 internal CID，修订名与消费者一致。Function ID555、58-byte body、body SHA256 `af0a281c9e3d711eb56a64229f24706fed3192d373f0f98860b83144f095ae36`、接口和两条已完成数据槽均保持。当前 35 个旧名文本位置已完整进入 asm/registry/formal CSV/canonical inventory 投影合同；全 ROM 非对齐 raw/even 与 THUMB|1 扫描均为 0，不需要 alias 或 Equate。
4. 独立从 slots 重新计数：110 EQ_ADD = 102 个 reuse source rows + 8 个 new source rows；后者对应 7 个唯一新定义，只有 `CYBER_TWIN_DRAGON_CID` 由 `0x080ae74c`、`0x080ae76c` 两槽共享。proposal、slot plan、slot selfcheck、machine plan 和 manifest 的计数一致。
5. 独立复查完整合同：5 FUNC_RENAME；16 PLATE = 4 段内 rename + 10 段内 rewrite + 1 段外 rename + 1 段外 rewrite；registry 13 existing + 3 missing；formal CSV 5 个 name cells 与 4 个 canonical inventory 投影均有明确范围。未发现新增语义矛盾。

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule1 地址序 | ✅ PASS | 活动路线图 `doc/dev/refine/14_equip_ai_scoring.md:130` 的 Seg-6 正是 `[0x080ade8c,0x080af120)`；Seg-1..5 已闭合，未跳段。 |
| C2 | Rule2 raw 块归宿 | ✅ PASS | 段内 143 `.word`、1894 InstructionDB 与 84 padding bytes 完整覆盖 4756 bytes；`ROM_INCBIN=0`、`.byte=0`，无未分类 raw 块。 |
| C3 | Rule3 §5.1 0 引用 | ✅ PASS | 本段无 raw/§5.1 候选。独立重跑 ADE48/ADE8C/ADF40/AEEB0/AEF1C/AF070 的全 ROM 非对齐 raw 与 THUMB\|1 扫描，12 个结果均为 0。 |
| C4 | R1 值 | ✅ PASS | slots 字节未变；143 个槽逐一从原 ROM 读取 4-byte little-endian 值，`original_value`/`old_bytes` 差异为 0。 |
| C5 | R1 常量复用 | ✅ PASS | 独立计数为 102 reuse rows、8 new rows、7 unique new definitions。66 个既有常量名称和值匹配；7 个新增定义无准确同值语义常量。5 个 CID 的四路身份、packed CID 与 99999 signed 比较证据保持闭合。 |
| C6 | R2 槽名 | ✅ PASS | 143 个 final labels 全唯一，均满足 `^[a-z][a-z0-9_]+$`；无同址 alias 计划。 |
| C7 | R3 接通 | ✅ PASS | 27 REF_ADD 前态均无 DATA ref，计划新增唯一 USER DATA/op0/primary；6 REF_PRESERVE 保持原 DEFAULT DATA CORE6。5 个 target 的 USER Symbol ID/type/source 冻结；110 EQ 仅加 operand-0 Equate。 |
| C8 | R5 现名/注释 | ✅ PASS | 16 条批准新 PLATE 无自动名残留。ADE48 新名已进入 PLATE、28 incoming 派生名、registry/CSV/inventory/source 合同；旧名仅保留在明确的 before/prestate 字段与待投影源文本基线。 |
| C9 | ASCII | ✅ PASS | 16 PLATE 与 143 EOL 非 ASCII 计数均为 0；最大 PLATE 440 chars。 |
| C10 | carve/Thumb 值 | ✅ PASS | 无 carve、无 ROM Function pointer slot、无 odd alias 或 `+1` 表达式动作。 |
| C11 | 误名 | ✅ PASS | 第一轮 ADE48 问题已关闭：`find_first_empty_slot_by_card_id` 精确描述 bits12:0 CID 消费者；最终 5 个 rename 的 body/ID/接口均保持。5 个 entry 的 raw/+1 holds 均为 0，名称投影范围完整。 |
| C12 | R6 证据/合同自洽 | ✅ PASS | 第一轮计数问题已关闭：proposal `:44,:126` 与两份 slot contract 均明确 `102 + 8 = 110`、8 source rows/7 definitions，并列出 Cyber Twin 两槽共享。file:line/confidence、动作分组、registry/CSV/temp 合同与 manifest 派生计数一致；禁用措辞扫描无命中。 |
| C13 | 自动名残留覆盖 | ✅ PASS | 段内 143 `.word`、143 自动定义与 slots 143 行一一覆盖；每个 `old_name` 在当前 asm 中恰有一个定义，遗漏和重复均为 0。 |

## 状态：PASS

第一轮两项修改均已闭合，当前 C1-C13 全部通过；无剩余修改项。

## Reviewer Verdict: F14-Seg-6 = PASS
