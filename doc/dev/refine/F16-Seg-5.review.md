# Refine Review: F16-Seg-5

范围 `[0x080c57c4,0x080c699c)`。独立审查冻结 FINAL v1；结论为方案 PASS，可进入 Mode B 实施准备。本结论不代表实际 POST、事务回滚、保存或 ROM 构建已经验收。

## 输入与独立执行

唯一 FINAL manifest：`output/refine-run-20261028-105948/f16-seg5-final-manifest-v1.json`，SHA256 `cbf9e2591a0af6bed6a45fbc82747e0008b4a752a22e2ac9cd78ce050d20bb4f`。正式 proposal SHA256 `4f069a7d05817e6154459cb39c9be1a1ebd31ae60ba22a6b31a9bd39f4ccd29a`；source JSON SHA256 `8239a98d4a3d85f1b9e9d9933d8659865752df984060f48185057260ca405030`。

独立核验 FINAL 34 records、formal 三份副本及相关冻结输入，共 94 个唯一文件的实际 size/SHA。调用冻结 `runner_source.replay(source_path, inputs_path, False, True)`：26 份产物共 222516544 字节，两遍 producer 全字节一致，两次完整 validator PASS，且 26 份内存产物与冻结文件全部一致。19 个受影响反例全部拒绝，两个完整 native 私有正例通过。未调用 Ghidra，未运行构建或 Git，未修改模型和生产源码。

## 核验（C1-C13）

| # | 检查 | 结果 | 独立证据与边界 |
|---|---|---|---|
| C1 | 地址序与路线图 | ✅ | 活动文档 §五及总进度均指定本段；前段结束 57c4，下段开始 699c，11 个既有函数，无跳段。 |
| C2 | 每个 raw 块有归宿 | ✅ | 两个 ROM_INCBIN：5c3c+1102、63e0+118；一处无标签 `.byte`：60f4+4。总 1224B 精确分为 794B 代码、412B 池字、18B 零对齐。 |
| C3 | 0 引用分类 | ✅ | 自行扫描全 ROM 每字节位置，覆盖 612 个偶地址 raw/THUMB 候选及 1224 个字节地址候选；结果逐项匹配冻结扫描。60f4 的绝对扫描虽为 0，原 ROM 指令 6088 的 PC-relative LDR 实际读取它，因此没有送入 §5.1。 |
| C4 | EQ 值 | ✅ | 37 EQ 全部重新读取 ROM little-endian 4B；连同其余槽，共 250 word 原值与 before/after 完全一致。 |
| C5 | 常量复用 | ✅ | 独立查 GNU 常量与现有 ELF 符号；7 个复用值域覆盖 28 bindings，9 个新值域在既有 GNU 定义中无同值候选。8008 使用同 glyph-render 参数域的 CARD_DESC_RENDER_PARAM。 |
| C6 | 槽名与碰撞 | ✅ | 所有槽名满足小写下划线形式；333 个 USER 名唯一，与全程序既有静态符号不存在异址同名碰撞。既有 RAM 全局保留项目命名形式。 |
| C7 | 按名引用接通 | ✅ | 139 个新增 operand-0 USER DATA 引用、4 个保留引用、93 个实际新增 DATA 目标的完整 graph 接通；235 个 native 表达式和 7 个精确 fallback 由实际 exporter AST 校验。 |
| C8 | 现名注释 | ✅ | 11 个 after PLATE 与所有拟设 EOL 均无残留自动名引用；9 个函数更名同步 registry、CSV 和精确外部 BL。 |
| C9 | ASCII | ✅ | 逐条校验所有拟写 PLATE/EOL 为 ASCII；PLATE 均不超过 500 字符。before 旧注释仅作保护证据。 |
| C10 | carve THUMB | ✅ | 8 项/32B 中 6 个非零项均以真实函数地址+1 编码，包含重复 close handler；索引 4/7 为 0。独立重编码与原 ROM 精确相等。 |
| C11 | 函数语义与误名 | ✅ | 完整函数体、raw CFG、共享消费者共同支持 action-menu 相关 9 个订正；6638/6800 保留函数名并更正真实寄存器说明。 |
| C12 | 消费者证据 | ✅ | 11 个函数、37 EQ、局部化标量、VRAM/调色板及 R7 均有实际 PC/源行证据。独立执行原 ROM 13 roots×6 语言共 78 条路径，结果与同 master row 的真实 GNU 字符串地址一致。 |
| C13 | 自动名覆盖 | ✅ | 自行定位段内全部 79 个 DAT/DWORD/PTR 自动定义，均有计划；139 个既有 word、103 个新池字、8 个 R7 cell 全覆盖，无漏项。 |

## R1-R9 与结构保护

| 规则 | 结果与依据 |
|---|---|
| R1 | 37 EQ、9 新 Equates/37 bindings、15 新 GNU 定义均有值和域证据；JA 到 ES 的 8 个 delta 保留 base+offset 结构，0000ffe8 保留 u16(-24) 原值。 |
| R2 | USER graph 333 名完整、唯一。保留原有非 DEFAULT 符号的 ID/type/source/namespace，原生 null 保持 null。 |
| R3 | 139 DATA 的实际来源/目标、全部持有者图及 export 表达式闭合；62 个 computed-PC 表项保持偶数和既有 DATA 引用核心，不统一添加 THUMB bit。 |
| R4 | 直接对原 ROM 的 69 个 code span 独立 GNU 解码，395 heads/794B 全部匹配，完整指令长度均在 codeSet 内。全部 16 个真实 case roots 可达精确 395 heads；103 literal/9 zero-run 无代码边穿入。 |
| R5 | 9 rename、11 PLATE、registry 11 既有 tuple、CSV 9 name cell 及 temp 两 body 长度一致；参数、返回、storage、ABI 和 flags 不修改。 |
| R6 | packed selection 的 player bit7/zone bits6:0/index bits14:8 由真实移位与掩码确认；RAM 0201ff5a 是 ctx+2a 的 byte step，保持其原生数据与 ROM null 字段。 |
| R7 | 精确 32B 表与 88B 后缀；第一 cell 原有 /dword 保留，其余 7 cell 建 /dword；8 cell references_from 全部继续为空，不制造 PointerDataType 或函数入口引用。 |
| R8 | 从原 ROM 渲染 28×2 个 4bpp tile、实际两组 palette 及三块 frame tile 并目视检查，图形与菜单图标、左右/中间框条消费者相符；不增加超出消费者的素材身份断言。 |
| R9 | 已有物理 before/备份与完整模型绑定。真正落地仍必须经过 ownedFalse 完整 POST/恢复、唯一保存、新进程 check、独立后验及 33554432B ROM 逐字节相等；本轮只验方案。 |

R4 安全调用明确为 `DisassembleCommand(all395Heads, exact69CodeSpans, false)` 加 `enableCodeAnalysis(false)`，仅 794 code bytes 的 TMode 改为 1。103 池字为 `/undefined4`，18B 对齐仍无类型且 TMode0。240 个 automatic refs 按原始 opcode 与 detached prototype representation/factory 双重核对：103 READ（operand1）、62 CONDITIONAL_JUMP、73 UNCONDITIONAL_JUMP、2 UNCONDITIONAL_CALL（flow operand0），均 DEFAULT/primary true。没有新增 computed-switch flow、FlowOverride 或 Function create/delete/merge。

两个父 body 是旧 AddressSet 与新代码字节的规范化并集：5b78 从 330B 加 698B 到 1028B/67 ranges，6268 从 334B 加 96B 到 430B/8 ranges。所有新增字节在真实 before 中均无函数归属，与全部既有函数 body 无交集；不合入 pool/padding。对应 ROM body SHA256 分别为 `68e78aef760cb3c0dc96be818122aa639c7e2da6cd794d5cd5df7bcf1550ee33`、`a92f2c7a304ac5f04e2b9dc17da2b78cbc90fae880f915b4aa3d3f68cb68f33f`。

## R7 边界与共享消费者复核

`asm/16_duelfield_zone.s:8647..8654` 清 0x2c bytes 并置 valid bit，phase 从 0 开始；`:8820..8823` 的直接结束路径置 phase4。普通链是 0→1→2→3→4(NULL)。原 ROM 641c/6426 对 selection0 跳到 6450..6454 写 phase4，handler6470 返回1，driver65fa..6600 读回并加1到 phase5；renderer 的 5872/5884、593e/5950 分支明确共用 phase3/5 闭合几何。其后 5→6(card-info)→7(NULL)。NULL 路径 6624..662e 清 valid bit并返回1，不递增。

所以 09e5ab98 不是可截断边界。原 ROM 表为 `[6185,6241,6269,6491,0,6491,64b9,0]`，6 个非零 cell 对应 5 个唯一函数。下一独立表 09e5aba4 的首 word 为 080c7af9，代码 literal080c8754 及 86c2/86d4/86e0/86e2 独立选择、读取和调用该表；它完整留在后缀 `[01e5aba4,01e5abfc)`，不能并入本次 carve。旧 firststage 20B 推断只保留历史字节，不作为最终 payload。

## 完整模型与反例

真实 Java/Jython before 做 1418466 次严格递归比较：137 Fn、7295 去重 state（7218 slot/1755 word/578 target holders）、20264 条完整 instruction properties、2441 Tiny rows 及 83960 before IDs 一致。仅明确无序的原生引用枚举使用完整类型/字段且保留重复次数的 bag；其他字段、数组和 whole-properties header 原样保护。5 个非 null even_function 持有者保留完整 ABI，43716 module units 与 48 external units 不缩小。

POST 契约仅允许绑定 333 个不可预知的新 USER ID：严格正 int64、唯一、与全程序 35925 static+48035 dynamic IDs 全部互斥；其他 rich 字段全部由独立 before 与批准最小动作推导。19 个反例实际经完整入口拒绝，包括固定行集合缺失/重复、真实 evenFn ABI、whole header、pool dtype、R7 空引用/THUMB/suffix、body 规范化、padding context、automatic source、源码 scope/AST 和静态/动态/0/float/重复 USER ID。普通非连续 ID 与低于旧最大值的合法稀疏 ID 两个完整私有正例通过；它们不冒充实际 native POST。

source_scope 为 15 条许可路径：asm16、精确 raw carve、四个段外 BL（asm01@0801ef10、asm15@080beec6、asm17@080cccc4/080ccd26），以及明确的 constants/registry/CSV/temp 变更。全 1755 module word AST 检查段外变化为 0；132 继承 pins 原值逐条保持，最终 139 pins。原生无 DTO 的 94 个继承 pin 不捏造 DTO，38 个实际受观测的 pin 执行 before/after 原生 AST 相等检查。

## 状态: PASS

必须修复项：0。独立审计入口及实际 hash 见 `output/refine-run-20261028-105948/f16-seg5-reviewer-audit-v1.json`；raw/refscan、回放、引用类型、ROM/常量/自动名及图形证据分别独立冻结于同目录的 reviewer 文件。

## Reviewer Verdict: F16-Seg-5 = PASS
