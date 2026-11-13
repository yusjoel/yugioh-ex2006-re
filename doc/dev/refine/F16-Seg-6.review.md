# Refine Review: F16-Seg-6 — R3

## 状态: PASS

**分析与静态语义通过。** R1 的 3 项修改、R2 的 1 项修改及新增 9 个 context PLATE 已全部闭合，C1–C13 均通过。本结论不包含实际 Program 写入、owned rollback、真实 POST、持久保存、保存后核验、汇编导出或构建；实际落地与整 ROM byte-identical 验收仍待 Root 执行。

范围 `[0x080c699c,0x080c7af8)`，4444 字节。仅更新本 review 和独立证据，未修改正式方案、源码或进度。

## 权威输入与历史

独立重算统一 FINAL 的 43 项 size/SHA256，全部相等。RUN 为 `output/refine-run-20261028-105948/`。

| 输入 | 字节 | SHA256 |
|---|---:|---|
| `f16-seg6-final-manifest-v3.json` | 17913 | `e8668649b96a1ab9de71fa49368a804c2c1acc0a739546acfef53847f23758b1` |
| `doc/dev/refine/F16-Seg-6.proposal.md` | 55858 | `b2e7e21ad74dd4cdb32a17f8659eb5b55ffc6927eddf33d20745d25361a360d3` |
| `doc/dev/refine/F16-Seg-6.slots.tsv` | 512385 | `ca041835e82bddea984e4d8f106be65c62a70aefd0afcf9fde9bc562cb66771f` |
| `doc/dev/refine/F16-Seg-6.plates.tsv` | 1183550 | `d7aff52dc9d687c325372b1bf1a42cea7ab8bca4103de7d92caf9a06b361c600` |
| `f16-seg6-analysis-source-v3.json` | 65084 | `84ca5339f10f31c8757b94f7a88bc8351d7593099e963e6bf472756f115b8426` |
| `f16-seg6-inputs-v3.json` | 13064 | `bfdfeb4b1c624a4643a7aa034eb420addb14d7e424ba6b2e8e5d37f000ef5886` |

R2 review 的归档正文为 `RUN/f16-seg6-semantic-review-live-v2-archive.md`，8623 字节，SHA256 `5c8b35511441408696cc8c6898d1c901f34260af5923bbfefad236b9b5003685`。更新前独立核对其归档收据、归档正文和 live review 旧哈希，随后 CAS 更新。R1/R2 原文与旧 RUN 证据均保留。

## 修改闭合与最小差异证明

- R1 输入掩码已订正为 `0x200`，对应零位路径进入普通方向处理；其余 56 条指令 EOL 保持。
- R1 `080c7638` 已命名 `dispatch_card_display_oam_by_mode`；唯一 caller `080c8318`、`080c82e4` 及全部必要 renderer context 联动闭合。
- R1 `080d0640` 已订正为更新 counter bit0、保留 bit1。
- R2 `080d0150` 的两处 displacement 已按 reviewer 完整 ASCII 建议改为 Q8 affine scale，正文与 R2 建议逐字符相等。

缩放语义的独立证据：`asm/17_duelfield_pack_frame.s:8887 @080d0228` 及 `:8916 @080d0262` 将 r9 放入 r3 高半字；`asm/21_font_title_scene.s:6510 @080f6d04` 提取该半字，`:6730 @080f6e92` 将其作为 r1 传入 `write_obj_affine_rot_scale`。`080f60e6/60e8/60ea` 将 r1 乘入正弦表值，随后算术右移 8 位形成矩阵系数。X/Y 另行构造。相关指令重新逐字对照原 ROM，confidence high。

v2/v3 的 19 个 JSON 模型执行完整递归差异比较：12 个 JSON 内容完全相等；6 个模型各仅有一处 `080d0150` PLATE 文本替换；剩余 metadata 模型只补充 `protected_external_unit_rows=48`。没有其他字节、身份、动作、引用、owner、ABI/body 或 scope 变化。

完整 native 模型的 `protected_external_units` 保持原来的 `range/units` 两键结构，范围 `[0x09e5ab58,0x09e5ab88)`，units 共 48 行，完整对象 before==after。统计修正与真实列表长度一致。

22 个输出均有覆盖：除上述 19 个 JSON，slots TSV 与 v2 字节级相等；plates TSV 精确等于 v2 的单次旧 PLATE→新 PLATE 替换；proposal 对应更正该 PLATE并补充缩放证据及保护单元统计解释。34 个 PLATE 的正式代码块、TSV、primitives 和模型正文一致，34 个完整 before 等于冻结 native Core，body/ABI 字段保持。

全部 176 槽、98 槽名、103 USER、156 EOL、10 rename、新 GNU 11、槽动作和原证据不变。当前 ROM 仍为 33554432 字节，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。全部拆分 ASM 和 constants 文件再次与冻结源码基线比对哈希相等，因此复用 R1 的逐槽 ROM、6402 常量求值、连续覆盖和独立全 ROM ref-scan 证据。

源码许可仍为段外 BL 24 处：asm01=3、asm15=2、asm16=6、asm17=13，即跨文件 18 加同模块 6。原有同模块 5 处与新增 `080c8318` 均保留；registry 34、两份 CSV 各 10 个 name cell、113 primary、163 native 表达式、13 新 fallback、139 继承 pins、152 有效 pins 保持。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule1 地址顺序 | ✅ | 与活动文档 §五 Seg-6 一致，紧接已完成 Seg-5；13 个既有 Function 完整，边界不变。 |
| C2 | Rule2 裸块归宿 | ✅ | raw=0；3688 指令字节、704 池字字节、52 原样零对齐字节覆盖全部 4444 字节；稳定 ASM 和原独立测绘保持。 |
| C3 | Rule3 零引用登记 | ✅ | §5.1=0，R4/R7=0。ROM 与候选集合保持，沿用 reviewer 自行重跑的 266 地址 raw/THUMB+1 全 ROM ref-scan，不依赖 executor 的零引用判断。 |
| C4 | R1 EQ 值 | ✅ | 35 EQ 及全部 176 池字值与原 ROM 的独立核对保持；slots.tsv 原字节不变，1933 holder 与完整 BEFORE ROM 证据保持。 |
| C5 | R1 常量复用 | ✅ | 新 GNU 11、新 Equate 9 及复用计划不变；全部常量源码哈希保持，原 6402 定义独立求值和同值域核对继续有效。 |
| C6 | R2 命名和碰撞 | ✅ | 98 槽名和 10 函数新名规范、无冲突；新增 dispatcher 名的全项目 static global 无碰撞证明保持。 |
| C7 | R3 按名引用 | ✅ | 48 REF_ADD、15 REF_PRESERVE、35 EQ_ADD、78 CASE_CORE、5 目标 USER 及完整引用计划不变。 |
| C8 | R5 使用现名 | ✅ | 34 PLATE 和 156 EOL 无旧自动名或 10 个旧函数名；旧 dispatcher 的 11 个原 PLATE 引用完整覆盖。 |
| C9 | ASCII 与长度 | ✅ | 34 PLATE、98 槽 EOL、58 指令 EOL 全 ASCII；最大 PLATE 411 字符；所有正式文本一致。 |
| C10 | carve 与 THUMB 指针 | ✅ | carve=0；六表共 78 个偶数 case 向量及 mov pc,r0 消费者保持，原 ROM 逐字证明有效。 |
| C11 | 函数误名订正 | ✅ | 10 个改名包含显示模式 dispatcher；全部必要 caller/renderer context 与 24 处段外 BL 许可闭合。 |
| C12 | R6 消费者语义 | ✅ | 原 3 修复、9 新 context 和 R2 仿射 scale 修复全部闭合；file:line/ROM 证据支持位域、除法参数、真实 OAM 与矩阵语义，confidence high。 |
| C13 | 自动名覆盖 | ✅ | 全部 98 自动数据定义逐地址对应 98 SOURCE_LABEL；全部 176 word 有动作，原独立覆盖证明及稳定 ASM 保持。 |

## 修改清单

无。静态语义门禁通过，后续实际落地由 Root 执行。

## 独立证据

| RUN 文件 | 字节 | SHA256 |
|---|---:|---|
| `f16-seg6-semantic-review-independent-r3-v3.json` | 28548 | `2a03f2e6314a2f84a49c40d33c8521acb5d01ed2db59506d9162200567d7aa90` |
| `f16-seg6-semantic-review-independent-r2-v2.json` | 31443 | `d82065e894f5b24cdaf8a5a96ce09c11b4e6621392f311f6106ceced1d2f3dab` |
| `f16-seg6-semantic-review-r5-supplement-v1.json` | 313681 | `da246993e72f73027a8d05db0564223f1b840cb67d141509fd642ff415d612fe` |
| `f16-seg6-semantic-review-independent-values-v1.json` | 322586 | `de825f38b4f8acbf6bda3e8d9100e2bdf3ab5180165c8364f6b77d2184ea0570` |
| `f16-seg6-semantic-review-independent-refscan-v2.json` | 576217 | `477dbca7d7c921b31b366ee6408ff9c5ca93aef351df03e0b88f75f037ba91bd` |

模型定点反例和双回放按冻结收据关联，本 reviewer 未重跑未修改的旧反例矩阵。Program/Ghidra/JVM/CLI、build、Git、Computer Use 操作均为 0，实际 runtime/POST/save/build 不在本 PASS 内。

## Reviewer Verdict: F16-Seg-6 = PASS

## Root实际落地验收（2026-11-13）

真实回滚、唯一保存、新进程与独立后验全部通过；源码范围精确、49/49资产导出和构建通过，整ROM33554432字节逐字节相等，SHA1为`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。Java扩展采集器字段不匹配曾被拒绝，已用冻结标准采集器重采闭合，未放宽比较器。详见活动文档§4.06。

| 验收记录 | SHA256 |
|---|---|
| `f16-seg6-phase1-static-review-v1.json` | `c3ca5db4b707c9aad25d75f4c633ceff99a7045e7d7232925b8858a0800df997` |
| `f16-seg6-apply-v1.json` | `183bfb586ba60f9117db8895c7a3dc0d304a4c074b38d6cd7d928c29438a4558` |
| `f16-seg6-persisted-check-v1.json` | `c6a3e8b098f57b576dcce3d622ef24365018ca3f1c2e015eec67c1d267efca91` |
| `root-f16-seg6-saved-native-gate-v1.json` | `df2a2f88157e21376034647ea62d70e64b3638d5d1d147e1ca8e689c421c7859` |
| `f16-seg6-source-landing-final-v1.json` | `b77fbd2e90571c6bf42b5e3a5842bb8751750428918a0afd0e199dac63382fb7` |
| `f16-seg6-saved-java3-schema-investigation-v1.json` | `65c766797075f2736b38408fbc2e7e23a699ac44ff618af26908490ef214b3d4` |
