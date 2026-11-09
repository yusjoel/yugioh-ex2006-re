# Refine Review: F13-Seg-8（第二轮）

## 复核输入

- 段范围：`[0x080a46a0,0x080a585c)`，长度 `0x11bc = 4540` bytes。
- proposal：`doc/dev/refine/F13-Seg-8.proposal.md`，SHA256 `5835bdaaf66fe4269cbcc552db086f02e1dc63eee115f077a4686f50256fa731`。
- slots：`doc/dev/refine/F13-Seg-8.slots.tsv`，SHA256 `c62a1ff6516fbfe9e51e1c584ce734d7a3d702975f1303f821f1a0e9e6842db6`。
- plates：`doc/dev/refine/F13-Seg-8.plates.tsv`，SHA256 `a470fdbf187bb779d4fbbea8d0fd0b5a989ad276957beb0a3896ecd770083c76`。
- Mode A 独立门禁：`output/refine-run-20261011-103530/root-f13-seg8-mode-a-independent-gate.json`，SHA256 `2d37ee9454a8f37a864ef5f18352a85a8753791de27d328d2837c3cf46773bd5`。
- 首轮冻结件与 `NEEDS_FIX(6 items)` review 保存在 `output/refine-run-20261011-103530/seg8-review-round1/`；首轮 review SHA256 为 `17b5494cbdaaba1e53e5a0dac70ec5b94f50962ff146c7f7dc4a754085e2c627`。

第二轮只读前态使用实际存在的完整路径：

- `output/refine-run-20261011-103530/f13-seg8-slots-prestate.json`
- `output/refine-run-20261011-103530/f13-seg8-functions-prestate.json`
- `output/refine-run-20261011-103530/f13-seg8-external-callers-prestate.json`
- `output/refine-run-20261011-103530/f13-seg8-external-caller-6508-prestate.json`
- `output/refine-run-20261011-103530/f13-seg8-oddword-slots-prestate.json`

## 六项修订复核

| 首轮项 | 第二轮独立结果 | 证据 |
|---|---|---|
| C7：12个范围外 packed Thumb words 的 Data 类型 | ✅ 前6槽为 `/undefined4:4`，后6槽为 `/dword:4`。12槽的 dynamic DEFAULT Symbol ID、唯一 incoming DEFAULT READ、refs-from=0、equates=0、raw word 均逐槽吻合。proposal 明确保持原 `.word`，不创建 odd Symbol/ref/equate。 | `f13-seg8-oddword-slots-prestate.json`；`asm/13_equip_placement.s:19574-20435` |
| C8/C12：`0x080a3ae8` PLATE | ✅ 初始化 player/card-ID/flag/mode；2×5扫描中首次命中返回1，全失返回0。修订文本没有首轮多写的 capacity/counter 分支。 | `asm/13_equip_placement.s:13827-13882` |
| C8/C12：`0x080a3b74` PLATE | ✅ 每次命中递减 remaining count；同玩家命中经 field-effect gate 设置 flag；remaining 大于0先返回0，归零后由 flag 或 available-slot 决定1/0。 | `asm/13_equip_placement.s:13909-13996` |
| C8/C12：`0x080a6630` PLATE | ✅ bit1未置位时直接返回 dispatcher 结果；state0返回0，state1确认后返回1、等待返回-1，later states返回0。 | `asm/13_equip_placement.s:19835-19960` |
| C12/R8：两项资产偶合 | ✅ `tb1250.bin+0x0d84` 与 ROM `0x08aca144` 均为 `89 4c 0a 08`；`tb0291.bin+0x0499` 与 ROM `0x08665b19` 均为 `b5 55 0a 08`。proposal 保留各自 raw=0、thumb=1 及上下文原字节。 | `data/card-image-tiles.s:1256,297`；对应两个 `graphics/bin/card-images/tiles/*.bin` |
| C13：InstructionDB/DataDB 布局 | ✅ 独立源码计数为1738条助记符、61条 `.hword`、155条 `.word`；只读 DB 单元为1687×2B Instruction、112×4B Instruction、155×4B Data、98×1B Data。合计1799 InstructionDB、253 DataDB、4540B。 | `root-f13-seg8-baseline-v2.json`，SHA256 `45289f412678d5729c893e827bbc5ecd7733cb42fb5ad3b7c08ca57b5d033c05`；V1保持历史文件 |

Mode A 相对首轮只改三条 PLATE 全文与上述证据/合同；`slots.tsv` 未变化。14条 PLATE 均在 proposal 中全文出现，纯 ASCII，长度271..477，且不含 `FUN_/DAT_/DWORD_/PTR_DAT_`。三条改动地址严格为 `0x080a3ae8,0x080a3b74,0x080a6630`。

## 完整独立复核

- 重新枚举当前 ASM 与 TSV：155槽=`138 DAT + 17 PTR`，动作=`112 EQ + 26 REF + 17 RENAME`，155个 final label 合法且唯一；段内没有 `ROM_INCBIN` 或 `.byte` 裸块。155个自动名定义与 TSV 地址/旧名集合精确相等。
- 155个槽的 ROM 小端值全部与 TSV 相等。全 ROM raw/`THUMB|1` 重扫与附件逐项相等：只有 `0x080a4700` raw=3、`0x080a4c88` thumb=1、`0x080a55b4` thumb=1；其余152槽为0/0。
- 七个 Function 入口重扫为：`46a0=0/0`、`4af4=0/0`、`5188=0/2`、`533c=0/2`、`5498=0/0`、`5714=0/4`、`57b8=0/4`。后12个命中就是 proposal 冻结的范围外 packed words。
- 94个 REUSE EQ 名称与数值均命中现有定义；15个新增数值没有可复用的现有常量，15个新常量名与1个 odd Thumb alias 名均未占用。`0x0804aea1 = check_card_is_archfiend_type + 1`，保持 EQ-only。
- `f13-seg8-slots-prestate.json` 逐槽确认：17个 RENAME 槽各保留一条 source=`DEFAULT` 的 operand-0 DATA ref，target `gP1LifePoints` 为 USER_DEFINED；26个 REF target 均为既有 USER_DEFINED globals。reference source 与 target symbol source 已分开冻结。155个 dynamic DEFAULT source label 物化为唯一 USER label时允许合法 ID 变化，静态 target/Function ID 继续守恒。
- 四个函数重命名的 body、direct caller 和 `0/0x800` 返回语义仍与首轮结论一致。14条 Function 记录的 ID、source、body、body size 和旧 PLATE 长度全部等于三份完整前态 JSON；范围组成7个段内 Function与7个必要段外 caller，新增/删除/resize均为0。
- card-ID 证据仍由 `data/cards-ids-array.s` 的 `icid/slot -> cid` 列与 `data/card-stats.s` 的 cid/card name/password 双重闭合；proposal 没有把 card ID 数值改写成 set code。两个 `0x1cf4` consumer 的 base 均为 `gP1LifePoints`，使用 `P2LP_BLOCK2_OFF_1CF4` 正确。
- proposal 证据表14个文件全部存在，当前 SHA256 与表内值完全一致。文本中没有禁止词，EOL/PLATE 全部纯 ASCII。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1：范围与路线图 | ✅ | 活动文档 `doc/dev/p5-refine-13-equip-placement.md:5,170-173` 指定相同半开区间并从低地址推进。 |
| C2 | Rule 2：每个裸块有归宿 | ✅ | 本段 `ROM_INCBIN/.byte` 数为0；carve=0、disasm=0、§5.1=0。 |
| C3 | Rule 3：§5.1 块确为0引用 | ✅ | 本段没有 §5.1 块；155槽和7个入口已重跑 raw/Thumb ref-scan，全部非零命中均有现有槽、caller或资产偶合归属。 |
| C4 | R1：EQ 值等于 ROM | ✅ | 112个 EQ 与其余43槽均逐项读取 ROM 4字节小端核对，无差异。 |
| C5 | R1：常量复用 | ✅ | 94行复用精确匹配；16个新增定义通过 exact-name/value-domain 扫描。shifted CID 与 odd alias 算术正确。 |
| C6 | R2：槽名合法且唯一 | ✅ | 155个 final label 全部匹配 `^[a-z][a-z0-9_]+$`，唯一且无现态碰撞。 |
| C7 | R3：label/ref 接通及前态守恒 | ✅ | 26 REF、17 preserved refs、112 EQ-only 合同完整；12个范围外 packed words 已按6+6 Data 类型逐槽冻结并保持 raw/no-new-ref。 |
| C8 | R5：现名与 PLATE | ✅ | 四个函数重命名与 body/caller吻合；14条新 PLATE 使用 final name。三条首轮语义错误已按实际分支订正。 |
| C9 | ASCII | ✅ | 155 EOL 与14 PLATE 全部纯 ASCII；PLATE 最大477字符。 |
| C10 | carve/Thumb +1 | ✅ | 本段无 carve；12个 packed callback words及新增 GAS alias均满足 `raw = even_function + 1`。 |
| C11 | 函数误名 | ✅ | 四个 FUNC_RENAME 均有 body、caller、卡数据和返回值证据；其余三函数现名与全局访问一致。 |
| C12 | R6/R8：消费者与资产证据 | ✅ | 关键槽有 file:line/high 证据；两个资产偶合均给出具体文件、偏移、原字节、上下文与原始命中数。 |
| C13 | 完整残留与布局 | ✅ | 155个自动名 word 全覆盖，无遗漏；1799 InstructionDB、253 DataDB与4540B范围闭合，V2为当前布局证据。 |

## 状态: PASS

首轮六项修改均已完成，第二轮没有新增修改项。Mode B 仍须按 proposal §9 的 transaction、persisted read-only、export/split、inventory、ROM byte-identical 与 rollback 合同执行。

## Reviewer Verdict: F13-Seg-8 = PASS
