# Refine Review: F13-Historical-Closure（Round 2）

## 输入与证据连续性

- 模块：`asm/13_equip_placement.s`，`[0x0809d718,0x080a78dc)`，41412 bytes。
- 当前 proposal SHA256：`c941f0068bc8242f6a69bc28ddcbeadefbccf2430b7b7c2f5435bdd5a66cbb1a`。
- 当前 source-audit SHA256：`d51c1e60ec81c26dfe75084eded5b26ede2a52e1022b35d3f8c62af6cbb0ceda`。
- plates TSV SHA256：`a98e77c26062726316b55cfdd1864058dea8792468109b753efe1a3cde5cc821`，与首轮逐字节相同。
- 当前 manifest SHA256：`87ffbd4aad972395502e3f2c8d8854efcb02657976b0e6764a394fa1a6ed6c87`；所列 11 项逐项重算，0 个 mismatch。
- 首轮不可变归档：`output/refine-run-20261028-105948/f13-closure-review-round1/`，15 文件完整；归档 review SHA256 `7611f4270b857b316893fd084f783d8aa8a3ed68e21105cbc376974c2ae71b70`，归档 reviewer audit SHA256 `db22edac4846d44c810170fd83cc157028a92039a0abf44ca4b5827967fdbeb0`。
- 第二轮独立证据：`output/refine-run-20261028-105948/reviewer-f13-closure-round2-audit.json`。

除 proposal、source-audit 与 manifest 外，plates、layout、refscan、只读 DB 前态、DB gate、模块覆盖基线、源码基线、DB backup、Function input 共 9 份证据均与首轮归档 hash 相同。因此首轮对 ROM/ref-scan、214 Functions、1530 words、16365 InstructionDB、2270 DataDB、41412-byte 完整覆盖以及 PLATE caller/body/card/text 语义的独立结论连续有效。本轮额外独立核对 Mode A 差分与 THUMB BL 编码，未运行 headless。

## 首轮修改项关闭核验

1. 当前 proposal 仅改变 source-audit hash 与 `0x080a1dd8` 分类行；分类行动作仍为 §5.1 保留，raw bytes、raw/THUMB 原始计数及 PLATE 合同未变。
2. `f13-closure-source-audit.json` 相对首轮仅改变 `raw_block_static_classification[0]` 的 `shape`、`outgoing_call`、`outgoing_args`。
3. 对 `0x080a1de0` 的编码半字 `f7ff fe0e` 独立按 THUMB BL 公式解码：PC base `0x080a1de4`，signed offset `-996`，目标精确为 `0x080a1a00`；当前 ASM `asm/13_equip_placement.s:9064-9065` 的该入口名为 `set_lp_display_row_fields`。
4. 16B wrapper 字节 `00b50d2100220023fff70efe01bc0047` 解码为 `push`、3 条 `movs`、1 条 4B `bl`、`pop`、`bx`，即 7 条指令、8 个编码半字，宽度为 `2,2,2,2,4,2,2`。当前 proposal/source-audit 均已采用此口径，并写明 `r0` 透传、`r1=13`、`r2=0`、`r3=0`。

首轮 #1 已关闭，未引入新的语义或动作差异。

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule 1 地址顺序 | ✅ | 活动路线仍为 file 13 Historical Closure，范围 `[0x0809d718,0x080a78dc)`；未进入 file 14。 |
| C2 | Rule 2 裸块归宿 | ✅ | 仅余 16B `.byte` 与 20B `ROM_INCBIN`，两块均显式归入 §5.1；Mode A 未改变分类。 |
| C3 | Rule 3 §5.1 零引用 | ✅ | 首轮独立 full-ROM 18 候选 raw/THUMB 全 0，ASM direct-flow/literal/data/numeric 全 0，无 owner/incoming/fallthrough；refscan hash 不变。第二块两条内部 literal 边仍不构成外部入口。 |
| C4 | R1 值 | ✅ | EQ=0；1530 个现有 word 的地址和值检查证据 hash 不变，均 PRESERVE。 |
| C5 | R1 常量复用 | ✅ | 新建常量 0；既有三张卡 CID 常量复用合同未变。 |
| C6 | R2 槽名 | ✅ | slot action=0，自动数据/函数符号前缀命中仍为 0，无新增槽名或碰撞。 |
| C7 | R3 接通 | ✅ | REF=0、carve=0；两块 §5.1 不创建 USER label 或 DATA reference，现有 word 元数据保持。 |
| C8 | R5 现名 | ✅ | 新 PLATE 无自动名残留；旧 `DAT_0x12d` 由 full rewrite 删除。 |
| C9 | ASCII | ✅ | PLATE TSV 字节不变；新 PLATE 490 chars、纯 ASCII，现有 EOL/PLATE ASCII 基线不变。 |
| C10 | carve 指针 | ✅ | carve=0，无 THUMB 指针表动作，raw directives 与字节保持。 |
| C11 | 函数误名 | ✅ | `tick_equip_score_display_phase` 的 caller/body 独立语义证据未变，名称与三阶段显示行为一致。 |
| C12 | R6 证据真实性 | ✅ | 首轮错误已订正：真实 BL 目标 `set_lp_display_row_fields@0x080a1a00`，7 instructions / 8 encoded halfwords，参数 `r0` passthrough、`r1=13`、`r2=0`、`r3=0`。PLATE file:line 证据与置信度保持。 |
| C13 | 全模块残留闭合 | ✅ | 214 Functions、1530 words、16365 InstructionDB、2270 DataDB 完整覆盖 41412 bytes；自动名前缀 0，唯一旧地址式 PLATE token 纳入本次 rewrite。 |

## 状态：PASS

修改清单：无。

## Reviewer Verdict: F13-Historical-Closure = PASS
