# 函数/数据细化计划 -- `asm/14_equip_ai_scoring.s`

> 范围 `[0x080a78dc,0x080b5348)`，精确长度55916B / 0xda6c；按文件序为第15个模块。
> Seg-1 至 Seg-10 全部通过验收。模块 14 已完成，累计完成 15/25 个模块，下一模块为 `15_equip_target_summon_zoom.s`。
> 所有落地保持ROM SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`；未经用户明确指令不stage/commit。

## 一、规则

沿用 `doc/dev/methodology/refine-loop.md` 的R1-R9和三条硬规则，以及当前 `.codex/agents/refine-{executor,reviewer,fixer}.toml`。先复用常量、读取真实消费者，Ghidra新PLATE/EOL只用ASCII且PLATE不超过500字符。source symbol与source ref分开冻结；动态DEFAULT目标物化时区分真实引用与派生目标metadata。

## 二、流水线

备份源文件/DB -> 地址序测绘与proposal -> 独立C1-C13 -> 必要Mode A修订与重审 -> PASS后脚本/fresh/dry -> root实施门禁 -> apply/保存后readonly -> 全量native导出/模式/split -> export_all49/49/build/整ROM逐字节验证 -> root独立DB/source/ELF/范围/同步验收 -> 进度记录。

## 三、当前进度

Seg-1 至 Seg-10 全部完成。全模块 204 个已命名 Function、1505 个字面量池字和 23456 条 InstructionDB，自动数据名为 0。原始数据仅保留 §5.1 登记的 140 字节。

## 四、工作记录

### 4.00 建档入口 (2026-10-28)

`split_manifest.tsv`指定本模块边界；前一模块13完成10段及收尾，ROM33554432B逐字节一致。当前记录不预判本模块数据语义或raw分类。


- 主线程完整只读查询覆盖138个Function全属性/body/引用、1044个word/82个目标、2849个Symbol、138个PLATE及55916个byte-unit，15个DB物理文件hash守恒。证据 `output/refine-run-20261028-105948/root-f14-independent-map-prestate.json`。
- 独立ASM/ELF/ROM全覆盖基线：15353 InstructionDB（14401助记符+952.hword）、1044个word及13个精确原始块；自动定义984。raw内容只做机械定位，不在建档阶段推断语义。
- `dispatch_equip_entry_slot_by_mode@080ab200`实际body向低地址延伸到`080aac1c`，整簇留在Seg-3；`080ae050 -> 080aec7a`的非CALL共享出口留在Seg-6，不按相邻CSV入口切断。
- `[080b18e0,080b40b8)`10200B原始块不可切开，因此Seg-9为11132B；其余段在合法Function边界上按字节偏差均衡。边界计划与全部约束保存在`root-f14-boundary-plan.json`。

### 4.01 Seg-1 完成 (2026-10-28) (2026-10-28)

范围`[080a78dc,080a8c30)`，13个Function、131个旧word、3块raw共1164B。静态测绘将旧word`080a7928`并入第一块R4，合计1168B分割为1006B代码（482条指令）、144B字面量池（36个word）及18B零填充（9项）。最终数据词预期为`131-1+36=166`。

主线程按ROM编码独立核对直接分支/BL/PC literal、表项及完整字节分割，`root-f14-seg1-r4-static-gate.json`通过。三个host的原body与新增代码取并集后，最终预期为386B/9个连续范围、336B/7个连续范围、436B/6个连续范围，合同为`root-f14-seg1-body-contract.json`。167行槽位合同含130个保留旧word、36个新增池和1个转指令的旧word；131旧地址前态symbols/primary/refs双向/equates/EOL已与主线程Java基线逐项一致。

外部callee/奇偶callback及R4细粒度状态补查询覆盖13个Function、124个address state、4948个byte-unit，15个DB物理文件hash守恒。首版提案已冻结并交独立C1-C13复核，manifest共16项输入且hash全匹配；13条PLATE写入、1条保留、10个函数改名、6个新常量和必要外部caller闭包均在合同内。复核通过后再实施脚本/fresh/dry门禁。

首轮独立C1-C13结论为NEEDS_FIX(3)：`8234`已有DATA/DEFAULT引用改列REF_PRESERVE（64 ADD+13 PRESERVE）；B3区分全12表源与5个块内source及7个外部tail source；全表25源指向17个目标（16新R4+1既有tail）。其他语义、R4、body及常量检查通过。20份首版/复核文件已封存于`f14-seg1-review-round1/`，修订后重新复核。

Mode A三项完成：仅`8234`的action/id_contract两个字段及proposal五行订正；17项冻结输入hash均匹配，14份PLATE合同字节不变，88份正式源码与15个DB物理文件均不变。主线程`root-f14-seg1-mode-a-narrow-gate.json`通过，当前交第二轮独立复核。

第二轮独立C1-C13全部PASS，review SHA256 `d2e3825448c959bac78b8b97fbdcc8a831c710475cb91d994b7892e5de72f528`。三项清单关闭；当前准备Mode B脚本、fresh前态、dry与当前源码备份，通过root实施门禁后再apply。

落地与最终验收：3块R4加旧word `7928`合计1168B恢复为482条指令/1006B代码、36个池/144B及9处填充/18B。最终本段2022条InstructionDB/4214B +166个word/664B +70B填充=4948B；3个Function分别扩展为386B/9范围、336B/7范围、436B/6范围，ID/接口/旧body片段守恒，未新增Function。

动作实际为61 EQ_ADD+2保留、64 REF_ADD+13保留、25 table source保持CORE6并接通17个USER目标、1 RENAME、1旧word转code、10函数改名、13 PLATE写入、166段内EOL和3个外部alias EOL投影。`7acc`准确旧673字符ASCII PLATE保留；外部`4058`只更新PLATE及调用名；file13的`3cb0/3cbc/3cfc`全局Equate名和EOL只做三个alias名称替换，值/绑定/来源完全守恒。新增6常量、4 aliases及3既有alias改名，registry 11 ADD/3 UPDATE，正式CSV仅10 name cells、真实inventory仅10 name cells+3 body lengths；carve=0、§5.1=0。

实施过程留痕：Phase1守卫修正后，首轮持久apply在R4完整指令集合门禁失败并事务回滚；root完整保留轮转后的DB并从当前模块前态备份恢复15个物理文件，哈希全部原样。只读事务诊断发现18个range-lo种子仅覆盖395/482，追加case后479/482，最后共享块seed `874a`达到482。正式V4只增加`835e/874a/8750`三个受限种子，分别补18/3/66条；新进程fresh与原前态完整JSON逐字节相同，再经root新实施门禁后apply、保存后check及全部后续流水线通过。

完整native导出和模式/split、export_all 49/49、build及整ROM逐字节验证均通过，exporter本身未改。native实际为1961条助记符+61条`.hword`指令；新5条是`7988/7992/8752/875c/8798`的非置flags MOV(sp到通用寄存器)，保持既有exporter原字节回退格式，仍全部为InstructionDB，区别于提案对助记符格式数的预测。

root独立后态覆盖152个Function、1079个word、417个address state和55916个byte-unit；验证17个switch targets、93条新指令引用（54 flow+39 PC read）、461条fallthrough、全部Symbol ID/双向CORE6/接口/注释、3个外部EQ以及误Data指针目标`08607cec`的唯一DEFAULT动态标签消失。source-scope仅允许asm13/14必要修改，其他23模块原样；ELF表达式与完整模块字节连续覆盖一致。最终门禁`root-f14-seg1-final-gates.json` PASS，landing receipt SHA256 `daed653bd523b649740e37cd285c2aa997bcd428e424ec4663611f00f68ce84a`。

ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`；未stage/commit。接续Seg-2 `[080a8c30,080aa120)`。

### 4.02 Seg-2 首轮复核与修订 (2026-10-28)

范围`[080a8c30,080aa120)`5360B，3现存Fn/54旧word/3raw3934B。首版拟恢复1699条指令/3484B、102池/408B、21处2B pad，新增Function9134并扩展/改名9734；拟6B u16 CID表carve。18项冻结输入及全1967候选扫描通过独立复核；五项清单为raw3的6 unique计数、raw1逐块扫描与跨块CFG口径、aa10c entry2与aa10e interior5的符号/引用分离、9134的0/1返回语义、正式temp inventory路径。首版和review已封存，当前Mode A修订后重审，尚未落地本段DB/源码。

Mode A五项已完成，root窄修门禁通过：plates仅`9134`返回文本/471字符计数与`aa10c`entry final_incoming两行变化，其他5行及156槽/R4 map字节原样；aa10e采用新派生DEFAULT code Label精确目标策略，entry2/interior5/body7分开；正式inventory明确temp四路径。20项input hash全部有效，93份源码与15物理DB在门禁时全部原样，当前交第二轮独立复核。

### 4.03 Seg-2 完成 (2026-10-28)

范围 `[080a8c30,080aa120)`，5360B。156槽为EQ_ADD31、EQ_MATERIALIZE73、REF_ADD36、REF_PRESERVE1、TABLE15；15个switch源接通11个唯一case目标。三个raw块3934B全部R4：新增1699条InstructionDB/3484 code bytes、102个pool word/408B和21个zero halfword/42B，使用12个初始seed与32个实际missing-start seed。248条direct flow（43 CALL）、126条PC READ、1616条默认API fallthrough逐地址一致；不设置FlowOverride，`97e4`保留literal pool。

新增 `process_equip_mode1_phase_3_to_7@9134`，1326B/10个canonical ranges；`9734`改名为 `dispatch_equip_mode1_phase_by_combined_index`，body52→2210B/27 ranges。6条新ASCII PLATE写入、1条准确PLATE保留，最长471字符。`aa10c`既有Function ID16954及18B body保持，entry incoming=2；`aa10e`为精确DEFAULT code Label，interior incoming=5，body external incoming共7。所有既有Function接口、flags及静态Symbol IDs保持。

`[09e478c8,09e478ce)` carve为3项ushort CID表（Horn of Heaven/Solemn Judgment/Triage），raw `0013fd123219`，前后bookends与incbin终点保持。新增常量13项（card_info5、duel_field2、oam_attr6）。registry新增6 tuple、8c30 tuple原样；正式CSV仅1个既有name cell和1个新增row；四份temp inventory为5214/5124 named/90 auto，9134与9734的size分别1326/2210B。

落地初版的observer前态整行守卫遗漏23个静态callee的39条批准新增入口CALL：事务原子回滚，failed.rep保留，15个物理DB文件从pre-Seg2备份逐hash恢复。V2只修正incoming预期及证据路径，实际执行AST和其他guard保持原样；第二次apply、保存后独立新进程check和root全部门禁通过。43 CALL的其余4条为1条到新9134及3条到本body内部aa0d2，分开核验。

全量native exporter保持SHA256 `4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87`。本段最终2250条InstructionDB=2144 mnemonic+106 `.hword`，156 word/624B，74B padding；段内自动数据名和raw均0。root独立后态覆盖174 Function rows、1181 words、757 address states和全模块55916 byte units；source98仅11项批准变化、其余24模块守恒，source/name/ELF/split/whitespace全部通过。

证据目录 `output/refine-run-20261028-105948/`：最终root门禁 `root-f14-seg2-final-gates.json`；正式脚本 `RefineF14Seg2.py` SHA256 `a6c5ba6fcd81254eccfeacd3e99e68bdd21668d1b7f8b530c3206166ab1a54f9`；最终receipt `f14-seg2-modeb-landing-receipt.json` SHA256 `518ac9b054a429890618d59caaceb02b8486be07193e6187a5a6292fb0edef55`。export_all49/49、build exit0；ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，继续Seg-3 `[080aa120,080aba78)`。

### 4.04 Seg-3 完成 (2026-10-28)

范围 `[080aa120,080aba78)`，6488B。206槽分为EQ_ADD57、EQ_MATERIALIZE65、REF_ADD30、REF_PRESERVE1、REF_MATERIALIZE25、TABLE_ENTRY_MATERIALIZE23和TABLE_ENTRY_EQUATE_EVEN_FUNCTION5。五个raw块3334B全部R4：恢复1411条InstructionDB/2938B代码、90个pool word/360B和18处padding/36B；248条direct flow含58 CALL，95条PC READ，1338条默认API fallthrough逐地址一致。27条跨owner边保持既有共享尾块归属及ABI。

三个dispatcher改名为 `dispatch_equip_mode2_phase_by_combined_index@aa120`、`dispatch_equip_mode3_phase_by_combined_index@aa77c` 和 `dispatch_equip_mode4_phase_by_combined_index@aaf64`，body分别68→1392B、46→1196B、104→568B。AB200的23段body保持共享代码，只释放literal word AB278前两字节的错误函数归属，2426→2424B；该word四字节、Data类型及既有READ引用保持。AAF54的16B body及Function Symbol ID16957保持。5条ASCII PLATE准确写入，最长500字符；AB200说明修正为半字+0x12的bits[8:6]选择模式。

28个表项接通16个唯一目标，其中15个DEFAULT Label物化、1个既有USER Function保持。AA7C0/C4/C8/CC/D0保留原有DEFAULT DATA引用和pointer Data类型，新增同名全局Equate `exit_equip_phase_oob_epilogue=0x080aaf54` 的5个operand-0绑定，供既有native exporter导出偶地址函数名。EquateTable与SymbolTable分开，不添加Symbol alias、不加THUMB低位、不修改exporter。

新增15个常量/全局：card_info11、oam_attr1、ewram1、duel_field2。LP显示计数器统一使用 `gLpBarDisplayCounter`，定义为 `gDuelPhaseFlags + LP_BAR_DISPLAY_CTR_OFF`，槽AB494直接使用该USER目标名。既有AB6D0到gP1LifePoints的USER DATA引用及ID15545保持。registry为2 ADD/3 UPDATE；正式CSV仅3个name cells，真实temp inventory仅3个name cells和4个body lengths；全局5214 Function、5124 named、90 auto，未新建Function，carve=0、§5.1=0。

独立C1-C13及最终实现静态核查均PASS。写入前关闭两类observer错误：AB278的槽位批准改动与Data布局守恒分开检查；90个pool和18处padding均不属于最终code-only Function body。首次持久apply在三个TABLE_BASES的空前态Symbol ID检查处异常，事务回滚，失败DB现场完整封存并从正确pre-Seg3备份恢复15个物理文件，哈希逐项一致。窄修只允许这三个获批的新USER Label使用新ID，其余静态USER目标继续保持ID/type/source；随后以相同函数AST完成只读完整事务并强制回滚，再经新root实施门禁落地。全部修正限于检查条件，实际apply AST保持一致，历史快照及复核输入保留。最终脚本SHA256 `d8a576dbcc7b1cd058760e1d71d3f99be3f7826b568247e5f4898c040839f072`，root实施门禁覆盖103份源码、15份DB文件、224份Function观察记录、320处地址状态及6488个byte-unit。

最终本段2696条InstructionDB=2604条mnemonic+92条`.hword`，206 word/824B，68B padding。root独立后态覆盖190个Function、1271个word、1174处地址状态与全模块55916个byte-unit；source/name/ELF/模式/split及其余24模块范围守恒全部通过。全量native exporter保持SHA256 `4544a6a95f922f5a1779553555180ed2184955bc4fc1e92f96ad9b500ddaeb87`。

证据目录 `output/refine-run-20261028-105948/`：最终门禁 `root-f14-seg3-final-gates.json`，landing receipt SHA256 `abf666a7a58399c96cafba510e5662b9882ccb91347c44f2fb1aeed16d8cc9cf`。export_all49/49、build exit0，ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，按地址序接续Seg-4 `[080aba78,080acc30)`。

### 4.05 Seg-4 完成 (2026-10-28)

范围 `[080aba78,080acc30)`，4536B，19个段内Function及2个必要外部caller。131个旧自动槽全部完成：104 EQ_ADD（72个唯一Equate名，57复用、15新定义）、20条USER DATA新增、7条既有DATA保持。136条PC READ和6个RAM目标的USER Symbol ID/type/source保持，后态27条RAM DATA ref；131个源标签均为单一global USER Label，Data类型121 undefined4、6 pointer、4 dword逐项保持。

`ABA78`改名为 `return_zero_from_equip_entry_dispatch`，ID16959与2B body保持：只设置r0=0并经共享epilogue返回上层，未写phase字段；上层将0作为继续检查的状态。`ACBF0`改名为 `check_player_lp_exceeds_chain_energy_cost`，ID5587与50B body保持：实际比较Chain Energy场上份数乘500后的LP成本。四条真实BL的名称投影保持原指令字节。`ABA7A`的共享出口说明订正为从r3/r4/r5分别恢复r8/r9/r10。

21条ASCII PLATE全部更新（17 rewrite、2 rename、2 external projection），最长458字符。外部BC168按完整state0..4/default及三个出口r0定义核对，返回只为0/1；states2/3的非零子调用结果会将state清零并返回0，无store completion与stored-next-state路径分开。BC388明确入口state非0返回1且不推进，以及initial-zero成功/失败路径的实际推进边界。所有Function body/ranges/hash/interface/flags/return/params保持。

新增15个常量（card_info7、duel_field8）。`TRICKY_TOKEN_CID=0x180d`由cid2093/Token13的结构化数据交叉确认；四个半字读写消费者使用 `EQUIP_STATE_CLEAR_BITS_8_6_MASK=0xfffffe3f`，清除 `[8:6]` 并分别设置mode1/2/3/4。registry为8 ADD、12 PLATE-only UPDATE、1 rename+PLATE UPDATE；正式CSV5079行及实际temp inventory5214/5124 named/90 auto只改两个name cells，body lengths、行顺序与auto/summary原样。无新Function、R4、body扩展、carve、alias或§5.1项，既有7个外部Equate aliases原样。

最终C1-C13与独立脚本静态审计均PASS。正式脚本SHA256 `81cfb2c4aa44f545c2acb2b8d9b598a992cb98a25155ca26ec17a792db29fb40`；Phase1 source108/DB15备份、192 Function、131 words、6 RAM targets、140 consumers、4536 byte-units及72 planned/7 protected global Equates完整冻结。正式同AST的apply/post在只读事务中完整通过并强制回滚，再经root实施门禁进行持久apply、保存后新进程check；consumer派生metadata逐项匹配live exact primary ID/name/type/source。

最终本段1873条InstructionDB=1734 mnemonic+139 `.hword`，3922B code+131 word/524B+90B padding=4536B，自动数据名/raw均0。root独立后态覆盖192个Function、1271个word、1177个address state与整个55916B模块，原typed unit/bytes/owner/flow保持；source108仅9项批准变化，除module14/15外其余23模块逐字节原样，source/name/ELF/模式/split及范围门禁全部通过。

证据目录 `output/refine-run-20261028-105948/`：最终门禁 `root-f14-seg4-final-gates.json`，landing receipt SHA256 `3b6d0ec91746907f5ea3ac35b9df8f448506aa8ddc9bea351e0f2565235c5165`。export_all49/49、build exit0；ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，接续Seg-5 `[080acc30,080ade8c)`。

### 4.06 Seg-5 完成 (2026-10-29)

范围 `[080acc30,080ade8c)`，4700B，19个段内Function及外部caller `080b1458`。150个旧自动槽全部完成：132 EQ_ADD（109个唯一Equate名）、10条USER DATA新增、8条既有DATA保持；152条PC READ及原有DATA CORE6逐项保持。150个源标签均为单一global USER Label，138个undefined4、6个pointer、6个dword的数据类型及字节保持。7个RAM目标中6个静态USER Symbol的ID/type/source保持，`0201e500`的DEFAULT动态标签物化为唯一USER `gEquipLpZoneEntryBase`，旧46条incoming引用CORE6保持并新增来自`ADE70`的一条DATA引用；所有引用的派生metadata与live exact primary一致。

两项误名订正：`AD270`从 `check_card_id_in_field_spell_bst` 改为 `check_card_id_in_field_spell_placement_bypass_set`，ID7257/body158B保持，其实际作用由`B1458`调用点的放置绕行分支核实；`AD844`从 `find_monster_slot_by_card_id_in_player_zone_alt` 改为 `find_chain_zone_slot_by_card_id_for_player`，ID16761/body72B保持，实际以player块内`+0x18`为count、`gP1ChainZoneArray`为4B步长数组。两者全ROM非对齐raw/THUMB|1扫描均无存储指针，外部`B1460`的BL仅投影新名、指令字节保持。

20条ASCII PLATE覆盖19个段内函数和外部caller，所有Function body/ranges/hash/interface/flags/return/params保持。独立复核按实际高寄存器MOV和stack参数核定ABI，区分模式标志与排除列表指针；AD4C8/AD608成功返回为(slot<<8)|player，即高字节槽号、低字节玩家；`AD794`的0/1/2分类返回按真实出口描述。原查询误列的两个内部地址保留NULL证据，另查真实call-host owners `0563CC`与`06A118`完成查询闭包。新增10个card_info常量与1个field_spell_bonus常量，7张卡由IDs/stats/passcode/结构化文本交叉确认，3个CID gap由0xffff映射确认。当前ADC68使用准确的ZONE_EFFECT_ATK_PENALTY_400=0xfffffe70(-400)，既有误名500定义和5条旧绑定原样。registry为6 ADD、13 PLATE-only UPDATE、1 rename+PLATE UPDATE；正式CSV5079行和实际temp inventory5214/5124 named/90 auto只改两个name cells，无行增删、重排或body length变化。无R4、新Function、body扩展、carve、Function alias或§5.1项，exporter与既有7个外部Equate aliases保持。

最终独立C1-C13及脚本静态审计PASS。正式脚本SHA256 `834f4996b29437556d0bb7902e82aa3763075f896d45cac296d4605134a790af`；当前源码113项和正确preSeg5数据库15文件备份验证通过。实际apply/post先在只读事务中完整通过并强制回滚，再经root实施门禁授权持久apply、保存及新进程check。最终root后态覆盖202个Function、1271个word、1300个address state（含5个旧500常量槽）和整个55916B模块，typed bytes/units/owner/flow保持。本段1906条InstructionDB=1834 mnemonic+72 `.hword`，3976B code+150 word/600B+124B padding=4700B；24个其他模块逐字节原样，source/name/ELF及范围验收全部通过。

证据目录 `output/refine-run-20261028-105948/`：最终门禁 `root-f14-seg5-final-gates.json`，landing receipt SHA256 `ad377da80234cbc50d10e13a2542e1773decfeb4674177336322acdc3d0fd80d`。export_all49/49、build exit0；ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，接续Seg-6 `[080ade8c,080af120)`。

### 4.07 Seg-6 完成 (2026-10-29)

范围 `[080ade8c,080af120)`，4756B，14个段内Function及直接callee `ADE48`、caller `B67E8` 两个必要外部注释闭包。143个旧自动槽全部完成：110 EQ_ADD（102复用源槽、8新增绑定/7唯一新定义），27条USER DATA新增、6条既有DEFAULT DATA保持。147条PC READ与5个静态USER RAM目标ID/type/source保持，后态33条RAM DATA引用；143个源标签均为单一global USER Label，130个undefined4、7个dword、6个pointer的数据类型和字节保持。

本段1894条InstructionDB=1785 mnemonic+109 `.hword`；4100B code+143 word/572B+84B padding=4756B。14个Function body合计4120B、互不重叠且覆盖全部code，其中AE050旧body还包含AE230/AE234/AE268/AE26C/AE270五个4B literal DataDB。五处仍为scalar word，保留原AE050 owner和PC READ，仅绑定Equate，未改变body及引用CORE6。AEC7A共享出口的16 BL与28 B保留真实引用类型和父frame约定。

五项语义名订正：ADE8C `select_empty_slot_preferring_different_card_id` 明确优先different-CID集合并在空集合时回退；ADF40 `find_empty_slot_by_card_id_and_player` 明确palette-empty及CID/side过滤；AEF1C `compute_peak_monster_zone_score_with_gates` 返回peak score；AF070 `find_lowest_scored_monster_slot` 以99999为上界、仅更小score更新。必要直接callee ADE48改为 `find_first_empty_slot_by_card_id`，ID555/body58与其两个已完成word/EOL/refs保持，28个AE050 BL仅投影新名。该callee同源bitfield说明从旧low19订正为实际bits12:0 CID：LSL/LSR #19保留低13位，LSL #18/LSR #31提取player bit13。四个段内函数与ADE48的raw/even、THUMB|1全ROM非对齐扫描均无存储指针，不增Function alias或pointer Equate。

16条ASCII PLATE完成（4段内rename、1段外rename、10段内rewrite、1段外rewrite），最大440字符，Function body/ranges/hash/interface/flags/return/params保持。查询修正保留原58个有效Function，追加真实call-host `run_equip_activation_display_phase_by_state_code@9F9CC`（ID4830/body1828）；原9FB16是2B return-zero stub，A001E/A0030的实际owner通过body和getFunctionContaining闭合。首轮两项修订及独立复审均留有不可变证据，143行slots TSV原样。

新增7个常量：card_info中5个CID由IDs/stats/passcode/结构化文本四路确认，另有 `GAIA_SOUL_PACKED_CID_FIELD=0xc1a80000`（GAIA_SOUL_CID左移19）；duel_field新增 `ZONE_SCORE_CEILING_99999=0x1869f`。8个新增源绑定中，Cyber Twin在AE74C/AE76C共用一个定义，其余6定义各一源。registry为3 ADD、8 PLATE-only UPDATE、5 rename+PLATE UPDATE；正式CSV5079行及actual temp inventory5214/5124 named/90 auto只改5个name cells，无行增删、重排或body length变化。

正式脚本SHA256 `394ec1e9a36caf2c16f13d77a48721bc2605cb91aa69afc9296b3ba808cec587`。Phase1 source118/DB15、230 Function、143 source slots、5 RAM targets、203 consumers（147 PC READ+56 rename CALL）、82 global Equates（73 planned+9 protected）及4756 byte-units冻结；实际同AST apply/post先完整通过只读事务并强制回滚，独立脚本静态审计和root实施门禁通过后才持久apply/save并新进程check。原7个Function Equate aliases、旧penalty500五绑定和400单绑定保持，无新RAM实物化、R4、新Function、body扩展、carve或§5.1项。

root独立后态覆盖230 Function、1271 word、1642 address state及整个55916B模块，typed bytes/units/owners/flow保持。source118仅9项批准变化；module14的prefix/suffix仅必要名称与ADE48注释投影，module15仅B67E8注释与B6868名称，其余23模块逐字节原样。source/name/ELF及范围验收全部通过。

证据目录 `output/refine-run-20261028-105948/`：最终门禁 `root-f14-seg6-final-gates.json`，landing receipt SHA256 `11c866936012a6ce4ce16ee7f5ad2f4944ce0941f57b06a0847fd43ba12a6793`。export_all49/49、build exit0；ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，接续Seg-7 `[080af120,080b04a8)`。

### 4.08 Seg-7 完成 (2026-11-03)

范围 `[080af120,080b04a8)`，5000B。149个旧自动word槽全部完成：106 EQ_ADD、34 REF_ADD、9 REF_PRESERVE；前态类型为130个undefined4、12个dword、7个pointer。153条PC READ与9条既有source DATA引用CORE6保持，149个source bytes/Data type/owner均保持；所有最终slot label和EOL均为ASCII。`0201b00c`物化为唯一USER `gEquipSpellZoneScoreBase`，13条旧incoming引用（含`090b28` primary=false）保持并新增`AFCB0`一条DATA引用。其余静态USER RAM目标ID/type/source保持。

四项Function误名订正：AF3B0 `check_field_spell_placement_available_by_card_id`、AF72C `count_equip_eligible_cards_across_field_zones`、AF940 `check_effect_zone_unavailable_for_player`、AFC24 `compute_peak_spell_zone_score_excluding_slot`。四个旧Function的ID/body/ranges/SHA/interface/incoming CORE6保持，全ROM非对齐raw/even与THUMB|1扫描均无存储函数指针。AF980原有`movs r0,#1; bx lr`两条typed InstructionDB建立为新USER Function `accept_slot_scan_candidate_unconditionally`，body `[080af980,080af984)` 4B、SHA256 `64d23481cb6a254816fb9c4c9b22031f78ed0a6ece5a6b0f6849a3ee7f77a2bb`；未clear/disassemble或改指令。其odd callback `AF981`只保留既有PARAM ref并投影`+1` Equate，不创建奇地址Symbol/Data/ref。

25条full ASCII PLATE完成：21个既有段内Function、AF980新Function及三个必要外部caller；最大435字符。第二轮独立C1-C13关闭AF4E8、AF8CC、AF940、AFC24、BB9B8五项ABI/callee/phase问题。v6静态审查进一步锁定AF981的name/qname/namespace/ID/type/source/primary/global完整后态，v5到v6仅扩展该post guard，apply/capture/verify_post及动作范围不变。

段外ROM表`[09e5ab28,09e5ab5a)`按真实inclusive index 0..24 carve为`equip_hand_candidate_card_id_table`，25个u16 internal CID、50B，SHA256 `c339eb5246b0053978f633d8969b2307fefbb0153f6087e8469ec5c5f3417d33`。AB28/AB2A两个既有undefined2及两条READ保持，AB2C..AB58新增23个undefined2；AF804新增表首DATA ref。AB5A两字节padding及AB5C后继pointer单元保持。`asm/rom.s` host incbin严格分为`0x0d54 + 0x32 + 0x00a2 = 0x0e28`，无R4或§5.1项。

新增14个constants/globals：9个card internal CID、4个score-domain常量及`gEquipSpellZoneScoreBase`；另新增1个ROM table label和2个THUMB callback aliases。九张卡均由cards-ids/card-stats/passcode/data.md四路结构证据闭合。registry更新10个既有tuple并新增15个tuple；正式CSV更新4个name并新增AF980一行，四份inventory同步4 rename和1 new Function，总Function数仅因AF980增加1。

本段2115条InstructionDB=1985 mnemonic+130 `.hword`，4328B code+149 word/596B+76B padding=5000B；21个旧body共4324B，加AF980 4B ownership后精确覆盖全部code。全模块最终140个Function、1271个word、18945条InstructionDB；自动数据名余170，后续两块已登记raw仍为10628B。本段没有新增指令、pool word、既有body更新或even Function Equate ref。

Phase1冻结123项source、15个物理DB文件、262个observer Function（261既有+AF980 absent前态）、1271 words、2755 address states、55916 byte-units及79 global Equates。dry与真实apply/post强制回滚均FAIL0，独立静态审查与root实施门禁PASS后才持久apply/save并由新进程check。最终root后态、source scope、name sync、ELF/范围/module布局及完整pipeline全部通过；批准source变化12项，其余受保护源逐字节保持。

正式脚本SHA256 `ed6312f107ed9a2412a2500ff4e2ce4c6bdb1f612d4917b18016d89b3f2bf648`。证据目录 `output/refine-run-20261028-105948/`：最终门禁 `root-f14-seg7-final-gates.json` SHA256 `f8089f20fb5950e8fc5edd260f1def30111bc689d2846e0033e52d151810e13a`，landing receipt SHA256 `fd0e1d1a90bd0ca6159bd1bc36765bd9911ba418de0b0657c9b2e2e83ca7d618`。export_all49/49、build exit0；ROM33554432B与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。未stage/commit，接续Seg-8 `[080b04a8,080b153c)`。

### 4.09 Seg-8 完成 (2026-11-03)

范围 `[080b04a8,080b153c)`，4244B。101 个自动池槽完成，新增 61 个 Equate 绑定、35 条 DATA 引用，保留 5 条已有 DATA 引用和 114 条 PC READ。1,819 条指令（含 160 条 `.hword`）、404 字节字面量池和 52 字节填充均保持原字节和类型。

修正 B06B4、B0C60、B135C、B1400 四个函数名，保留函数 ID、body、签名和 9 条直接调用。写入 14 条 ASCII PLATE，其中段内 13 条、段外 B153C 1 条。B1458 的原注释保持。最长新 PLATE 497 字符。新增 4 个常量和 4 个 RAM 名称，保留四个目标的 19 条旧引用及既有 Data。carve、disasm 和 §5.1 新登记均为 0。

独立数据库、源码范围、命名同步、段及全模块 ELF 均通过。资产导出 49/49，构建 ROM 与原件 33554432 字节逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。证据位于 `output/refine-run-20261028-105948/`，最终门禁 SHA256 `49a36c02fcc57ea5167b58711a701399cd07970de3c18c496f64e6a718d64d61`，落地收据 SHA256 `32e2a7771d5567e8ab5bebc175d1156b1b1a3aacef74c934a56ebe4ad37ba5d2`。接续 Seg-9 `[080b153c,080b40b8)`。

### 4.10 Seg-9 完成 (2026-11-03)

范围 `[080b153c,080b40b8)`，11132B。原 10200B 误标区拆为 8982B 可达 Thumb 指令、924B 字面量池、154B 零填充和 140B 无外部引用例程。新增 59 个回调 Function、4317 条指令和 231 个字面量池。17 条同帧 BL 保留机器指令和默认 fallthrough，语义控制流按共享尾部处理。原函数及其两个 pointer 类型均保留。

237 槽完成，含 153 个 Equate、82 条 DATA 新增和 2 条 DATA 保留。两张外部回调表共 291 条记录、2328B，永久源为 `asm/normal_summon_response_tables.inc`。195 条记录关联到本段新增或既有 Function，96 条后续回调值逐条保留原始 Thumb 低位。其中 17 条指向 Seg-10 的 5 个入口，79 条指向模块 15 的 B76A4，随地址序接续。

独立数据库、源码、ELF、命名与 49 项资产导出均通过。重建 ROM 与原件的 33554432 字节逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 `77599a24fe15c4bb66165f57c6591ba44a1a234472db514ed9c1b1345030fa58`，落地收据 SHA256 `3fb2a96770dbef6beb0f27a4c1c05b1655880c4252c50b89fee66cf4dd29f39a`。接续 Seg-10 `[080b40b8,080b5348)`。

### 4.11 Seg-10 完成 (2026-11-04)

范围 `[0x080b40b8,0x080b5348)` 共 4752 字节。原 428 字节块恢复为 5 个 Thumb 回调、194 条指令（414 字节）、3 个字面量池（12 字节）和 2 字节对齐填充。最终本段有 34 个 Function、2131 条指令和 66 个字面量池字。

66 个池槽中，37 个绑定 Equate、20 个新增 DATA 引用、9 个保留原 DATA 引用。写入 35 条 ASCII PLATE 和 66 条 EOL，新增 3 个常量。两个现有函数改名，保留其 Function ID、函数体和签名。模块 15 的 B5348 只更新 PLATE 和 B548E 调用名。

两张表的 291 条记录及其 Thumb 低位逐条核对。17 条表项绑定到 5 个新增回调，另 2 条表项同步 B4464 的新名。B76A4 的 79 条待处理绑定交给模块 15。三个表基址池槽使用同地址的汇编表级符号，Ghidra 保留原有主符号。

第三轮独立复核通过。首次只读试跑因验收脚本读取了错误的预期引用字段而回滚。修正后，69 条原有读取及 5 条新增读取、强制回滚和保存后复查均通过。资产导出 49/49，重建 ROM 的 33554432 字节与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

最终门禁 SHA256 `3a71eea4f99929a19701fbcf5e7533f357f99d27e78aca9bf3031b9f743a0f7c`，落地收据 SHA256 `12cc1dcbfddcd536a2c98a4aa94952d688e4ee2de51e4485622a97f3578a30e6`。按地址序进入模块 15。

## 五、地址序路线图

| Seg | 半开范围 | 字节 | Function | 4B word | 自动word槽/块头 | raw块/字节 | 状态 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | `0x080a78dc..0x080a8c30` | 4948 | 13 | 166 | 0/0 | 0/0 | ✅ root全部验收 |
| 2 | `0x080a8c30..0x080aa120` | 5360 | 4 | 156 | 0/0 | 0/0 | ✅ root全部验收 |
| 3 | `0x080aa120..0x080aba78` | 6488 | 5 | 206 | 0/0 | 0/0 | ✅ root全部验收 |
| 4 | `0x080aba78..0x080acc30` | 4536 | 19 | 131 | 0/0 | 0/0 | ✅ root全部验收 |
| 5 | `0x080acc30..0x080ade8c` | 4700 | 19 | 150 | 0/0 | 0/0 | ✅ root全部验收 |
| 6 | `0x080ade8c..0x080af120` | 4756 | 14 | 143 | 0/0 | 0/0 | ✅ root全部验收 |
| 7 | `0x080af120..0x080b04a8` | 5000 | 21 | 149 | 0/0 | 0/0 | ✅ root全部验收 |
| 8 | `0x080b04a8..0x080b153c` | 4244 | 14 | 101 | 0/0 | 0/0 | ✅ root全部验收 |
| 9 | `0x080b153c..0x080b40b8` | 11132 | 60 | 237 | 0/0 | 1/140 | ✅ root全部验收，§5.1一项 |
| 10 | `0x080b40b8..0x080b5348` | 4752 | 34 | 66 | 0/0 | 0/0 | ✅ root 全部验收 |

### 5.1 未引用数据登记表

| 地址范围 | 字节 | 来源段 | 初判与引用证据 |
|---|---:|---|---|
| `[0x080b2758,0x080b27e4)` | 140 | Seg-9 | 独立 Thumb 例程，含内部字面量池。全 ROM 逐字节 raw/Thumb 搜索与直接分支扫描均无外部引用。前一例程在 B274C 返回，随后为字面量池。保留原字节。 |
