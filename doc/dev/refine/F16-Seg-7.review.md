# Refine Review: F16-Seg-7

v2独立复审，最终静态语义结论PASS。范围 [0x080c7af8,0x080c8bf0)，4344B。当前权威为f16-seg7-semantic-firststage-final-v2.json（5323B，SHA256 55e203e02522de13d64ae808eba6cf62e161155a35520bfe2d2ba038b4c2339d），15项record逐条重新验哈希。完整before仍为43ad18a014d573ab7202f16d32bd54baa5ded952b36297cc6875be87bfc6c1d2。

首轮C1–C13审查、R4/R7独立扫描和ROM证据全部保留；本轮独立核实最小字段差异并闭合唯一F16S7-R1。原NEEDS_FIX review（7791B，SHA256 248846458f217846b8e1e80f2d80ba1af64f2ed83542f9bb37b1b40f90a29f6b）已按f16-seg7-mode-a-cas-archive-v2.json映射逐字节归档，旧RUN不覆盖。

本结论只通过分析质量与计划完整性。reviewer无Program/Ghidra/native执行、无源码实施、构建或Git操作。生产POST模型/脚本、实际撤销、保存后核验及整ROM构建尚由Root后续落地阶段执行；本报告不授予持久apply或宣称其已通过。

## 核验（C1–C13）

| # | 检查 | 结果 | 独立证据与结论 |
|---|---|---|---|
| C1 | Rule1 地址序 | ✅ | 活动文档§五第7段为本范围；Seg1–6已完成，下一边界8bf0。12个既有Function、223池字、152源码自动名与路线图一致。 |
| C2 | Rule2 块归宿 | ✅ | 独立源码扫描仅1个58B ROM_INCBIN [7b68,7ba2)，全归R4。外部表精确20B R7，原88B切为20B+68B，尾从bb8留Seg8。 |
| C3 | Rule3 全ROM引用 | ✅ | 复用本人冻结R4/R7扫描，并重验其全部证据。29个半字候选的raw/Thumb值覆盖裸块58个地址值：13次raw命中全为真实14项表中的13项，Thumb命中0；无§5.1。 |
| C4 | R1 值 | ✅ | 独立重读223个池字小端ROM；73条EQ逐槽相等。5个外部表word与ROM相等，类型before与正式Core相等。 |
| C5 | R1 复用 | ✅ | 独立解析constants下6426条equ/set，全部表达式已解析。14个数值常量及两个既有地址alias复用；新11个数值、17个地址与1个carve定义，共29项。0x141旧alias为另一操作参数，frame tile的新alias有消费者区分。 |
| C6 | R2 名与碰撞 | ✅ | 151池槽、11代码标签和4个新函数名均满足命名形式；186个primary节点地址/名字各自唯一，未碰撞既有源码label。全局名称沿用项目既有大小写约定。 |
| C7 | R3 接通 | ✅ | 68条段内DATA新增、8条既有DATA完整保持；20目标USER、151槽USER、11代码USER。外表4条DATA采用实际保存odd地址，4个DEFAULT动态public ID已由Root实际getter固定，非POST接纳未知ID；零项空引用保持。 |
| C8 | R5 现名 | ✅ | 15条新PLATE无旧FUN/DAT/DWORD引用或四个旧函数名。全源码旧名PLATE依赖位于82e4与841c，均在本次重写集合。D70DC派生名及70AE READ holder/full owner D7064明确列入。 |
| C9 | ASCII | ✅ | 15条PLATE、238条EOL全ASCII；PLATE最长453字符，均≤500。正式TSV全部对应primitives逐字段相等。 |
| C10 | carve/分支数值 | ✅ | 外表4个非零表达式为实际Function+1，终止0无ref；14项R4内部向量和其余60项CASE为偶值且保持原ROM。MOV PC与BX的Thumb规则分别核验。 |
| C11 | 函数误名 | ✅ | 四处改名分别对应BG框初始化、打开、七状态转换、关闭；a01为独立显示模式，a18/a1a为各状态位域。函数名与实际体操作一致。 |
| C12 | R6 语义证据 | ✅ | 首轮223槽/229消费者与全部PLATE/EOL证据保持；F7DA4修复后使用实际u16(section+u32(section+8))比较，renderer将该flag映射到attr0 bit13，ROM反例已重读。 |
| C13 | 自动名覆盖 | ✅ | 独立扫描152个自动标签：151池槽逐一有USER计划，唯一裸块首DAT通过R4标签覆盖；223word无遗漏，74CASE中两处已有自动表头改名，其余72项保持。 |

## 语义核验记录

- 7ba8/841c：a18 word经LSL15/LSR24提取bits16:9；三个phase对应右侧条带、双边框展开/收窄、外沿完成/擦除。phase1的8位步进由a1b bits7:1与a1c bit0拼接，写回保留相邻位；关闭使用4-step反向坐标。返回值0运行、无有效phase时1与回调表一致。
- 7ea0/82e4/8688：detail为a1a bits8:1；master为a17 bits7:1加a18 bit0；scene为a18 bits8:1。输入掩码实际均0x200（gPrng+0x146/+0x148）。25列循环含端点，行stride0x40；timeout的-13为0xf3，正确清bits3:2并置bit2，保留bit0。scene成功后精确清frame phase、frame step和master，null路径返回0。
- 879c/8870：六次tile copy参数为14×2、6×4、14×2、4×1、10×1、16×4；helper宽度乘32、目的stride0x400。8870读取玩家stride0x868计数；计数>24用attr2=0xcc4，11..24用0xcc0，映射玩家加8；坐标使用zone13，r1=0x80为OBJ属性。
- 8904/89a8/89e8/8aa8：循环分别覆盖types0..4、5..10；7个可见槽用zone11且slot在r2。activation结果测试bit11，打包到word bits17:11；field低11位保留。OAM grid的field6仅对types0..4查询，attr2等于10+2*field6，后续7个可见槽使用zone11/index。
- 3b3a8/F616C：r0/r1/r2为player/type/subindex，r3被入口覆盖为scratch；LSL19/LSR19确为low13。OAM writer的r1高byte/低byte分别形成attr0/attr1上位，r0携x/y，r2为attr2。
- R8：已查看冻结9-tile图，边框片段与三类行tile组合一致；06008000 + 0x13e*32 = 0600a7c0，0x120B恰为9个4bpp BG tiles。没有断言实际调色板颜色。
- registry独立AST检索确认14个before tuple完全一致；8870 tuple确实缺席，应追加1条。
- R7完整计划选用odd DATA目标；本人早期R7小报告建议的even DATA目的属于实现选择。当前整体审查以完整冻结计划及4个prospective public-ID事实为准；早期ROM/类型/边界结论继续有效。D70DC现有4B /undefined *与DEFAULT DATA引用、派生源ID、70AE READ显示名均保留并作名称投影。

## 状态：PASS

## 复审关闭项：F16S7-R1

F7DA4新PLATE已准确描述实际条件u16(r1+u32(r1+8)) >16。source在F7DB2/F7DB4/F7DD4按第三项偏移读取半字；pattern count另由F7E16..F7E1E按首项偏移读取。ROM section09899838的pattern count=24、实际比较值=16，bit7不置；此反例已再次直接读取ROM核验。F8036..F8042将ctx+0x12 bit7映射为0x2000，即OBJ attr0 bit13。

当前334字符ASCII PLATE：

> Initialize the0x14-byte AOB context r0 from the pattern section r1. r2 high16 supplies the tile base at ctx+0x10; its low4 supplies the palette index in ctx+0x12 bits3:0. Set ctx+0x12 bit7 when u16(r1+u32(r1+8)) exceeds16; render_aob_frame_to_oam maps it to attr0 bit13. Copy r3 bit0 into bit6, set ctx+0xe to1, then resolve pattern0.

已逐字段确认authoring context_plates、primitives plate_after、plates.tsv以及proposal文本完全一致；对应registry既有tuple保持，future replacement使用该新plate_after。其余14条PLATE、所有before字段、223word、238EOL、4rename、182USER、R4/R7及typed closure通过深差异核对保持。slot TSV逐字节相同。producer所有函数AST相同，仅版本字符串与同一消费者解释同步。

修改清单为空。未重采before或重跑不变R4/R7矩阵。

## 独立证据

- f16-seg7-semantic-rereview-evidence-v2.json：归档映射、authoring/primitives/TSV实际差异、producer函数AST、公式/attr0 bit13的源字节和ROM反例。
- f16-seg7-semantic-review-structural-v1.json的77条证据以及首轮review索引records重新核验；旧canonical路径按CAS归档映射解析。
- f16-seg7-semantic-review-consumers-v1.json保留223槽229消费者和源行证据；其首轮NEEDS_FIX状态为历史记录，唯一问题已由本复审关闭。
- f16-seg7-raw-review-v1.json与f16-seg7-r7-review-v1.json保留原独立字节、引用、控制流和carve边界事实。
- 统一FINAL：f16-seg7-semantic-review-final-v2.json。

## Reviewer Verdict: F16-Seg-7 = PASS

## Root实际落地验收（2026-11-14）

实际完整后态与同Program回滚、唯一保存、新进程及三套独立Java后验全部通过。源码仅15个批准路径变化；173pins、223段内断言及R7五值、49/49资产和构建通过，33554432字节整ROM逐字节相等，SHA1为`9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。完整记录见活动文档§4.07。概述文件数4→5和D70DC模块17→18的文案订正与preapply历史分开记录。

| 验收记录 | SHA256 |
|---|---|
| `f16-seg7-phase1-static-review-v1.json` | `adf7f830359a8f2a089bb84aa6378c5fc4ea98ea9a89f2fea32286b21eb0dfaa` |
| `f16-seg7-apply-v1.json` | `edfb3b785ff9410768b886d8517e91b7c25a9f7d9ac1fd4d8533781e4271e5f3` |
| `f16-seg7-persisted-check-v1.json` | `439464fdcd63d325bb977aad9f38ee04913ebae9b285886e423ef55c8e3982a0` |
| `root-f16-seg7-saved-native-gate-v1.json` | `bb15e65807b740c616612084ad9c9c28bddbc4bf5415db51aa31d6c433f95a17` |
| `f16-seg7-source-landing-final-v1.json` | `48b212c596eaac63371649c11583053b4d72c372ad5e6736105e9835538fe510` |
