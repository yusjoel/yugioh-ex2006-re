# Refine Review: F15-Seg-8

## 状态: PASS

第二轮正式独立复核 **PASS**，首轮5组修订全部闭合。此结论只通过分析质量门槛，不授权实施、headless、持久保存或构建。

- 范围：`[0x080bda7c,0x080bede4)`，4968B。
- 唯一新版freeze：`f15-seg8-freeze-manifest.json`，SHA256 `0cbd79c1c7d4a1c7df81a534a88ffe7e4ba3a6934815f1553a9a79b40a3e6250`。
- formal proposal：`6a7e6f894bc69d2df9e3b192cb2703d4efffd4af4981e6dc2d1a996ed992a05e`。
- formal slots：`d2854d221b7d116d5af70f4633cecfd70fc5f7564456c6e929408acfec2784a0`。
- formal plates：`f83b17a69a01147475d53e63874765b72297a762ad82a676e10969d36541c185`。
- 完整真实before：`root-f15-seg8-composite-independent-prestate-v1.json`，SHA256 `ada618a0f83d38df53008d70bc5a47902cef79a8f23167f658b5b774cc0ed85c`。412个实际Function、10069个unique地址状态，保留原04BECC Function缺席状态。
- 首轮44文件归档收据：`8287e1834e40002fc37c7bb70e158b6e7ab8ee2671758d076785b22d0be241fb`。首轮review `22c40d2b1164d16f22148d9abcc519caaca92a3c4bc8a347481150aa57c6b9e9`和独立audit `282a1f4242bc0984559cdebc0f5549cb98e2fc74812b9feed0c9ac07e43e7b53`保持在归档中。

证据目录均为`output/refine-run-20261028-105948/`。最终本轮独立审计为`f15-seg8-reviewer-independent-v2.json`。

## 核验（C1–C13）

| # | 检查 | 结果 | 独立结论 |
|---|---|---|---|
| C1 | Rule1 地址序 | ✅ | 路线图7/10后的下一段与本区间一致；不跳段、不回头。 |
| C2 | Rule2 数据块归宿 | ✅ | 1984条typed instruction共4150B、193个word共772B、23段padding共46B，合计4968B；raw/R4/carve均0。布局及前态未变。 |
| C3 | Rule3/全ROM引用 | ✅ | 首轮本人逐字节滑动扫描7入口even/odd和95种池值，102组全一致；本轮ROM及refscan输入字节不变，继承该独立证明。没有§5.1块。 |
| C4 | R1 ROM值 | ✅ | 本轮重新核193个小端池字；41条Equate值/operand均精确，02000005保持scalar且无DATA目标。 |
| C5 | R1复用 | ✅ | 34个新GNU名称均不存在于真实旧ELF；完整global计划独立推导相等。相同数值但不同域的卡片掩码不替代DISPCNT掩码。 |
| C6 | R2槽名 | ✅ | 165个源标签符合正则且唯一；BEA90唯一变更名称改为BASE/PAL5，193图无冲突。 |
| C7 | R3完整接通 | ✅ | 全10069 state及412 Function的after由真实before+批准193图/动作独立产生，零差异；旧232 rich、8 state及prototype反例全部关闭。79条新增DATA均真实新增，73旧DATA完整保留。 |
| C8 | R5现名/持久闭包 | ✅ | BEA94现名/prototype/所有派生观察一致，C35AC仅PLATE旧名子串投影；现存BDFAC name-key registry comment-only闭合；scope明确14生产文件和冻结只读边界。 |
| C9 | ASCII/长度 | ✅ | 8个PLATE合同为5 PRESERVE+3实际写入；全部计划新写PLATE/EOL纯ASCII，PLATE最大453字符。registry3个patch的after均ASCII。 |
| C10 | R7/native导出 | ✅ | 无carve/Thumb新表。40继承+20新增pin保持；首轮84次实际native AST调用证据与当前未变的20 pin/exporter一致。段外新增.word投影为0。 |
| C11 | 函数误名 | ✅ | play_zone_type_13_card_reveal_effect与实际zone13行为吻合；1个stable-ID改名，Fn body/ABI/参数等不变。 |
| C12 | R6实际消费者 | ✅ | BASE512/PAL5有最终OAM attr2消费者证据；BEA94五次单entry尝试、phase0 bit6、LUT/sine因子、32-call等待及cleanup bit0均准确，见闭合表。 |
| C13 | 自动槽/残留 | ✅ | 193池字全覆盖，165自动源标签无遗漏；没有raw或静默保留块。04BECC历史84B正引用补漏保持单独待闭合。 |

三条硬规则及R1–R9细化要求全部通过。R4/R7均无新增动作；typed units、Function body和数据类型保持原样。没有用实施、构建或自评分替代消费者核验。

## 首轮5组逐项闭合

### 1. Packed scalar字段与全层名称 — PASS

`BEA90=0x02000005`统一为`AOB_MODE_TILE_BASE_512_PAL5`，源标签为`aob_mode_tile_base_512_pal5_lit_ea90`。本轮独立比较完整global/GAS计划，变化仅该名称；value、绑定地址/operand及数量均不变。decisions、formal、slot EOL、GNU定义、global对象及所有绑定、semantic均一致，该新常量的有效after定义均采用BASE/PAL5；不更改段外既有callee注释。

实际证据继承首轮本人指令核验：`asm/21_font_title_scene.s:8992–9001`把high16/low4存ctx+0x10/+0x12；`9713–9714,9781–9783`把ctx+0x10加到pattern tile index并写OAM attr2；`9348–9353`把ctx+0x12移到attr2 bits12..15。因此是tile base512和OBJ palette bank5。交叉算式为`(06014000-06010000)/32=512`及`(050002a0-05000200)/32=5`。旧callee注释中的tile_count措辞没有被当成消费者证据。

193个formal slot row中192个逐字段不变，只有BEA90的6个已批准cell变化：constant、label、GAS表达式、EOL、消费者证据、Equate binding。typed slot JSON也仅BEA90一行变化，所有before不变。

### 2. BEA94精确状态机注释 — PASS

PLATE逐字采用首轮reviewer给出的389字符ASCII候选，formal/Function/semantic/registry copies一致。BE9BC、C35AC和五条PRESERVE文本与首轮冻结稿一致。

详细语义现已完整保留：

- Phase0在BEB00..BEB18翻转field+0x215 bit6、按gBannerState+4 side与stride0x868取数据；两张small-card图用互补/当前bit6和tile0x200/0x208。count零走update_field_slot_tile_display；count非零才检查zone13 attribute1，非零用slotbase+4 mini-frame，零用0984FBCC fallback。region==4a且settings低3位==0取bank0，否则bank1；有源时复制0x120 halfwords，最后启动sprite3。证据：`asm/15_equip_target_summon_zoom.s:20613–20777`。
- Phase1比较旧counter：BED00读取、BED02/BED04增存、BED0A/BED0C对旧值<=3分支；从0产生0..4共五次调用。10B表09E491F0实际u16为`[0,1,8,15,16]`，形成`256+5*sin[(4*v)&127]`因子并缩放signed sine/cos偏移。每次只有BECFC一个OAM writer调用，容量守卫通过才追加一条；四个affine halfword写入不代表四个sprite。证据：`20793–20876`及`asm/21_font_title_scene.s:7389–7396,7596–7606`。
- Phase2总是绘zone13，field bit6非零才绘large card。Phase3比较增后的halfword counter>31，从0等待32次，最后一次仍返回1。仅phase>3清理：AND0xFE清banner bit0，AND0xFB清field bit2，返回0；phase0..3返回1。证据：`20902–20969`。

这些条款与本轮未变化的真实指令、ROM LUT及首轮独立counter演算逐项相符。没有只把four改为five而保留错误字段消费。

### 3. 单图完整state/Function观察 — PASS

本轮机械复核独立从完整真实before推导，未调用generator的project helper，也未补修其after：14788 checks全部通过，state after和Function after差异均为0。

- 单一193-primary图=165源Label+27目标Label+1 stable-ID Function。全10069 state的symbols、refs_from/to、EOL、Equate objects/bindings和owner变化一致；5个source/target重合只有一个after。
- 全412实际Function的before逐字段等于canonical，after只含批准派生/PLATE变化。13个Function共243个rich位置受图影响；加上plate-only C35AC，共14个Function观察记录变化。
- 7个段内Function旧232条body refs、8个basic-block state refs_from反例全部关闭。BEA94 final prototype为`undefined play_zone_type_13_card_reveal_effect()`，ABI/type/参数/signature-source等不变。
- 段外01C50C/01CB00/BC918/BFF6C的5条ROM_REGION_BYTE READ、BEDE4的4条PARAM，现已完整纳入。已正确的dispatcher CALL与BEA94 incoming继续保持。没有虚构from_function字段。
- 所有rich引用严格10字段。CORE6、静态ID、ANALYSIS qualified namespace精确；DYNAMIC token只存在于已批准USER新主符号。0/1/N集合均为数组；Equate对象2字段、binding3字段保持真实getter schema。
- 独立负例再次拒绝真实旧stale记录、CORE6-only、扁平switch名称、静态ID漂移、ANALYSIS升级、未知dynamic token；不接受实施时从live metadata修补冻结after。

### 4. Source scope与冻结边界 — PASS

production_write_paths精确14项：all.s、3个split module、6个constant文件、registry、formal CSV和2个现有name inventory。all.s明确为generated aggregate；auto/summary明确byte-preserve。formal3及分析plan/generator为Mode B只读输入，冻结manifest同时约束所有列明材料；不能把只读列表之外的已冻结证据解释成生产写权限。

60条pin完整包含40条继承和20条新增。target计划本轮逐字节未变，段外5个既有DATA源均为模块16的STR/LDRH/LDRB指令，没有额外.word源；existing5条ref的type/source/CORE6保持。exporter、其他模块和历史eval/proposal/closure快照受保护。

### 5. BDFAC真实name-key registry持久注释 — PASS

本轮重新AST解析真实RENAMES，8个Function为7个existing、BE9BC唯一missing，无重复tuple。全部index/key/new/comment before逐字段匹配，after只3个patch：

| Function | Registry动作 | Ghidra PLATE动作 |
|---|---|---|
| BDFAC | 现存banner_anim_state_machine name-key tuple的comment-only同步为当前440字ASCII，key/name/index不变 | PRESERVE，不新增写入 |
| BEA94 | 既存tuple新名及389字PLATE | 既有RENAME_REWRITE |
| C35AC | 既存tuple旧名子串投影 | 既有SUBSTRING_RENAME |
| BE9BC | 保持真实缺席 | 既有REWRITE，未创建registry tuple |

另外4个existing PRESERVE tuple原样不动。依据真实do_rename按old name查Symbol、非FUN_首键覆盖PLATE的逻辑，BDFAC旧注释回灌路径已被精确关闭。

## 保持的动作与验证边界

193槽=`41 EQ_ADD +79 REF_ADD +45 REF_PRESERVE +28 PRESERVE`；73条旧DATA为47 DEFAULT/26 USER_DEFINED，不重加、不升级。54目标、27新USER标签/物化，9个新Equate对象，完整global2446→2455、bindings12510→12551；34新GNU定义。8条PLATE合同仅3次实际写入、1个Function rename；无Function create、R4、carve或§5.1新增。

首轮完整语义和独立ROM/native证明经hash及窄差异确认未改变。历史04BECC 84B仍有04D374/B9E0A两个CALL、没有Function/Instruction，本段不重新分类落地，也不宣称整个项目补漏已完成。

## 本轮独立证据

| 文件 | SHA256 | 实际工作 |
|---|---|---|
| f15-seg8-reviewer-mechanical-v2.json | 630cec88ffab2ba906d3e7003cc22043ef8834039aed8f319dd04b34f403a1d5 | 14788checks；ROM/全global/193图/10069state/412Fn独立推导0差异 |
| f15-seg8-reviewer-modea-closure-v2.json | 4341b05de7874252e4afaec609e274d3bb83f5c0b21306af1c2c45b98d06a0a5 | 73419checks；192slotrows、before/数组/10字段、语义/registry/scope精确窄闭合与负例 |
| f15-seg8-reviewer-generator-reproduction-v2.json | 87c0c556a1f9c0d92fd297b42affaa6372f73b5f69945716fa502f701f448f4a | unchanged实际完整generator两遍compile/exec；所有写操作在内存拦截，22输出逐字节等于freeze，两遍manifest均0cbd79…6250 |

复现执行在本review覆写前、原首轮review仍满足Mode A前置SHA时完成。虚拟读回的sha/stat绑定各次实际生成字节，没有写入任何冻结文件；没有把generator自己的PASS当独立评分。首轮独立baseline、refscan、native、semantic、registry及Function closure证据继续由原归档完整保留。

## 修改清单

无剩余分析修订项。后续实施链须另行审查和授权；本PASS不是保存许可。

本轮只写本review与非Root ignored证据。所有冻结输入、source176 current/copies及正确savedSeg7 DB15 current/backup保持精确；未headless、未动源码/DB/进度、未build/stage/commit。FINAL FROZEN + STOP。

## Reviewer Verdict: F15-Seg-8 = PASS
