# Refine Review: F16-Seg-8

第二轮独立C1–C13语义审查：PASS。范围 [080c8bf0,080c9c94)，4260B。权威FINAL为f16-seg8-semantic-firststage-final-v2.json，4495B，SHA256 717f59e111ae0d9affeff74db7b011415aa9cb8730a37d88a5603f3774cc4a55；12项record与完整before e57f1ebbd099ce66aa5af2a8071b4d47056e4232022c58167a79bb214f535efa已独立逐条验哈希。

首轮完整C1–C13结论及R7/R8证据保留；本轮独立重核唯一修复F16S8-R1、严格最小差异、producer回放及全部复用证据字节。原NEEDS_FIX文档已由Root逐字归档，更新前校验canonical旧SHA256 5f502f357f62337f7b0af38697bf8e158849bb82481daa3149d1c0d33c3057c5与archive映射及字节相等。未改proposal/源文件，未操作Program/Ghidra，未构建或执行Git。

本结论只通过分析质量与静态语义计划。完整POST模型、生产脚本、实际fullrollback、保存及整ROM验收仍由后续ModeB验证；不授予持久写入许可。

## 核验（C1–C13）

| # | 检查 | 结果 | 独立证据与结论 |
|---|---|---|---|
| C1 | Rule1 地址序 | ✅ | 活动路线图Seg7已完成，Seg8为本范围；16Fn/110word/95auto与实际源码一致，下一边界9c94。 |
| C2 | Rule2 块归宿 | ✅ | 独立段内扫描ROM_INCBIN/.byte均0。外部R7仅bb8..abc8的16B，原68B分为16+52；后两张独立表与pack边界全部保持。 |
| C3 | Rule3 全ROM引用 | ✅ | 复用本人R7子集的独立全ROM扫描并重新校验其12条证据：38个偶半字及其Thumb值覆盖保护区76地址候选，精确确认各独立基址引用；不设§5.1。 |
| C4 | R1 值 | ✅ | 110个池字逐槽重读ROM小端，33EQ原值相等；4个R7字/Thumb+1/NULL与完整before再次核对。 |
| C5 | R1 复用 | ✅ | 独立计算全部既有equ/set表达式；17种数值常量复用，8个新numeric/9个新address/1个carve label合理。0x1a1现名为另一操作参数，0x9fff与既有0xffff9fff四字节不同，均有明确理由。 |
| C6 | R2 名与碰撞 | ✅ | 95新槽名和12新函数名符合形式，117个primary地址/名字唯一且未碰撞源码；10个目标名遵循既有全局约定。 |
| C7 | R3 接通 | ✅ | 48新增DATA、14既有DATA保持，95槽+10目标USER；R7三个存储odd DATA指向已固定public DEFAULT身份，NULL空引用保持。正式TSV与primitives逐字段一致。 |
| C8 | R5 现名 | ✅ | 18条新PLATE不含旧FUN/DAT/DWORD或12个旧函数名；源码中旧名PLATE引用均在本次18条重写集合。12rename的全部BL/必要显示名投影明确列入计划。 |
| C9 | ASCII | ✅ | 18条PLATE、179条EOL全ASCII且PLATE≤500；本文引用的修正文本同样ASCII。 |
| C10 | carve | ✅ | 四项为三Function+1与0，原16B可精确重组。首/dword保持，其余三项全部字节data_at/containing为空，建三/dword；52B尾段、前驱null及abfc pack区域保持。 |
| C11 | 误名 | ✅ | 12rename与实际用途一致：equip资格cache、field背景窗口转换、list序号、trap等级、字体4bpp、description滚动。4个保留函数名与实际功能兼容，无ABI/body/override动作。 |
| C12 | R6 消费者/注释 | ✅ | 全16段内与2个context函数、全部池槽消费者及80个EOL的首轮独立证据保持。8E6C PLATE、8F1E EOL与producer说明已同步为保存的get_duel_field_card_count结果等于0，唯一F16S8-R1闭合。 |
| C13 | 自动名覆盖 | ✅ | 95个段内自动名逐一对应95槽USER；110word全部处理，15个even CASE值/类型/ref核心保持；无模块raw或额外自动槽遗漏。 |

## 关键语义核验

- 8bf0/8c58：five-slot mask在cursor state=3时按player/slot/arg2=1建立；ZoneDisplayState+c等于-1只清其bit0。渲染选中槽时bit1/bit0分别控制特殊路径与显式pair坐标，AOB基址与tick条件已核。
- 8d30/8d68及3a7f0：packed cursor的player bit7、zone bits6:0、subindex bits14:8；输出2×11个u16，stride0x16。特殊code7/6保持，其他按两个方向分类；消费者用(2*code+0x110)|0x2400选择OBJ指标。low13非零判断与20B槽stride成立。
- 8f48..91e0：field-card分类与R8图像共同支撑背景命名。index*0x1680与palette index*32、WIN0/WIN1 bits13/14、phase1和3的counter0..8九帧、callback非零才推进outer phase、NULL返回0均已核。abdc的尾零仅保留ROM事实，不当作phase终止条件。
- 9218/933c：逆序绘制record index+1的list ordinal；每个序号全部decimal digits使用同一x。四个CID返回level10/4/4/4，其余0。CB2E6保存baseline至sp+48，CB8B8/CB8BA与sp+34当前level比较；card_stats首20B记录使table+22*i+0xa对应后续record的level字段。
- 9374：r1截低16、r2截低8；ctx width bits9:2乘rows，64B源byte-pixel tile转换为32B目标4bpp，16组半字写入起始为0。代码没有显式四位pixel mask，该限制在新PLATE中已说明。
- 992c/9a10/9ac8及EEB54：来源为localized description表；设置16tile宽/84rows并只初填最多13rows，显示14row环形OBJ，每行四个32×8。scroll状态低7总行、bits13:7文本行、bits15:14 phase、signed byte2 offset、byte3 ring，±8触发重填；0x800额外mosaic和正常绘制均核。
- 02039eb0仅按共享scene work area命名；其他scene的OBJ list/link使用已读，不把该地址单凭本处clear认作font pixel source。
- R8已目视查看PNG，并独立重解码6样本/69120像素，tile与RGB555 palette逐像素最大仅1级量化差；Forest/Wasteland/Mountain与分类消费者相符。
- registry独立AST确认14个既有tuple逐字一致、4个entry确实缺席；既有16998行Tiny/1940边中指向变化节点的typed edge与未变化DEFAULT派生节点均为0，三R7 odd public IDs有实际before事实。

## 状态：PASS

## 已闭合 F16S8-R1

8E82调用get_duel_field_card_count，8E86半字0x4682为mov r10,r0；8F08调用OAM helper后，8F0C半字0x4650为mov r0,r10。因此8F0E/8F10比较保存卡数值，只有零值路径才在8F1E将gDuelFieldState+0x215 OR0x20。已重核这13个原始指令位置、源行与ROM字节；原有两项相反结果的领域反例保持有效。证据为asm/16_duelfield_zone.s:16279、:16280、:16344–16354，置信度high。

新的377字符ASCII PLATE、EOL与本人首轮建议逐字相等：

> Render a horizontal slot-count gauge. Read count bits11:4 from gFontState+0xa0e and save the value from get_duel_field_card_count. Center count eight-pixel entries at x140-4*count,y68. Indices before count-value use palette0, the rest palette3. Append four frame pieces at x100,116,132,148. Set gDuelFieldState+0x215 bit5 when the saved value is0. Emit OAM directly. No inputs.

> Set gDuelFieldState+0x215 bit5 when the saved get_duel_field_card_count result is0.

authoring严格只变schema和上述两个文本；primitives严格只变schema、author proof的path/size/hash及两个after文本，共6叶。其余所有字段、类型、列表顺序/长度、before与registry_before保持。plates.tsv只变080c8e6c的plate_after，slots.tsv全字节保持；proposal只变这两个文本并增加同一guard消费者解释。future registry仍为既有缺席项APPEND_MISSING，文本直接使用修正后的plate_after。

producer原有全部函数AST相等，只有三个版本路径替换与这一条消费者解释插入。独立纯内存输出捕获保留全部生成表达式与断言：v1五输出与归档逐字相等；v2两次独立运行的五输出彼此相等且与冻结的primitives/proposal/slots/plates/selfcheck全字节相等。没有执行生产Program动作。

全部counts保持：110word/95auto、33EQ/48REF_ADD/14REF_PRESERVE/15CASE、105新USER、12rename、117primary、18PLATE、179EOL；R7仍只切16B、保持后52B，无R4/body/ABI/override变更。其余17条PLATE与79条指令EOL保持，未重复无变化的R7扫描、R8像素或通用矩阵。

## 独立证据

- f16-seg8-semantic-rereview-evidence-v2.json：本轮归档及输入校验、精确字段差异、原始guard、高寄存器MOV、registry文本来源与独立producer回放。
- f16-seg8-semantic-review-structural-v1.json：首轮ROM、常量、95自动名/110word、消费者、TSV、registry、闭包与public odd IDs；证据记录已重新验哈希。
- f16-seg8-semantic-review-consumers-v1.json：完整领域核验、分支反例及6个R8样本/69120像素结果；原字节未变。
- f16-seg8-r7-review-v1.json：本人独立全ROM扫描、native类型/引用及16/52切割边界，复用冻结事实。
- root-f16-seg8-semantic-v1-archive-final.json：原NEEDS_FIX与v1正式文件归档映射。统一结论及精确size/SHA见f16-seg8-semantic-review-final-v2.json。

## Reviewer Verdict: F16-Seg-8 = PASS
