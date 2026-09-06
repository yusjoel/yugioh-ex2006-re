# Refine Review: F13-Seg-7

## 0. 审查结论

- 范围：`[0x080a38fc,0x080a46a0)`，长度 `0x0da4 = 3492` bytes。
- 输入 proposal SHA256：`5ba03f83cecb5ad871fd4c9b851b4d5d6aa79fa2299264bd1592b1a4f6b2b6e5`。
- 输入 TSV SHA256：`b6b90532ddb4f40e0fd65e19f124b8aa33f189c135c11fee3c4d2f767302faff`，含表头共97行、数据96行。
- 本审查未采用 executor 的 refscan/direct-edge/self-check 作为结论；以下计数由当前 `asm/13_equip_placement.s`、`roms/2343.gba`、constants、消费者和 Function inventory 重新构造。
- **Verdict：NEEDS_FIX（4项）**。数据布局、ROM值、两张外部材料表和直接边闭合均正确；三个奇地址回调槽的落地类型、两处漏改函数语义、段外旧名 PLATE 涟漪以及失败恢复合同尚不能放行 Mode B。

## 1. 独立复核摘要

### 1.1 段布局、槽与 Function body

- 从当前 asm 在本段重新提取自动定义，得到96槽，`DAT=92, PTR=4`；地址严格递增、无重复，与 TSV 地址/旧名/kind 集合逐项相等。TSV 当前动作计数确为 `EQ=70, REF=22, RENAME=4`，但其中3个 REF 分类错误，见修改清单 #1。
- 对96个槽逐一读取 ROM 小端 u32，与 TSV `original_value` 比较，差异为0。每个槽地址及 `slot|1` 的全 ROM packed scan 均为0；这是 literal-pool 槽本身没有地址引用，不影响 PC-relative LDR 归因。
- 独立解码得到100条 PC-relative literal read、96个唯一目标；目标集合与96槽完全相等，无段外 literal target 或未覆盖槽。
- 当前 asm 的机器行重新按 ROM 字节校验，差异为0。布局为1352条普通指令、91条 `.hword` 指令，共1443个代码单元/3050 bytes；96个 pool word/384 bytes；29个2-byte padding/58 bytes。三者无交叠且合计3492 bytes。
- `temp/ghidra-functions.csv` 中本段有22个既有 Function，入口集合与 proposal 相等；`0x080a3b50`、`0x080a422c` 为两个 non-push 入口。独立检查 `f13-seg7-functions.tsv` 的65个 body ranges：排序、无交叠、入口均落在自身 body、每项 byte count 正确；所有 ranges 的并集恰覆盖本段3050个代码 bytes，无缺口或额外数据。Function create/delete=0正确。

### 1.2 两张外部材料表与 Rule 2/3

- 本段 asm 内 `ROM_INCBIN=0`、`.byte=0`，没有本地裸块；29个 `.zero 0x2` 均是已归因的指令对齐 padding。
- 对 `0x09e47898` 重新做全 ROM scan：raw恰1次，来源 `0x080a3e90`；`addr|1` 为0次。ROM三词为 `0x1119,0x111a,0x111b`。`asm/13_equip_placement.s:14229-14231` 以 `ldmia/stmia` 一次复制三词；`data/card-stats.s:4292,4305,4318` 分别确认 Sanga of the Thunder、Kazejin、Suijin。因此它是 Gate Guardian 三材料 CID 表，不是代码。
- 对 `0x09e478a4` 重新做全 ROM scan：raw恰1次，来源 `0x080a3f8c`；`addr|1` 为0次。ROM三词为 `0x1288,0x129b,0x12b8`。`asm/13_equip_placement.s:14367-14369` 同样一次复制三词；`data/card-stats.s:7789,8036,8335` 确认 Alpha/Beta/Gamma。因此它是 Valkyrion 三材料 CID 表。
- 两表位于 `asm/rom.s:1514` 的 `ROM_INCBIN 0x1e47894,0x2478`。proposal 的 prefix `0x4`、两表 `0x18`、suffix `0x245c` 合计原 `0x2478`，后继偏移为 `0x1e478b0`，切割算术与ROM字节均正确。
- 本段及两依赖块均不符合全ROM 0引用条件；proposal 的 `R4=0, §5.1=0, carve=2 ranges/24 bytes` 结论正确。

### 1.3 直接控制流

- 由本段机器码在已确认的代码单元上重解 Thumb `B/Bcc/BL`，得到305条：`B=60, Bcc=163, BL=82`。其中226条目标在段内，79条到段外34个唯一地址。
- 34个段外目标均在当前 `temp/ghidra-functions.csv` 中是既有 Function；没有目标落入活动 §5.1 的 `[0x080a1dd8,0x080a1de8)` 或 `[0x080a1f54,0x080a1f68)`。唯一高端边界边为 `0x080a4698 -> 0x080a46a0`，只证明 Seg-8 入口，不授权分析其函数体。

### 1.4 constants、命名与文本

- 49个 `REUSE+EQ` 槽的 target constant 均在现有 `constants/*.inc` 中存在且值与ROM一致。11个拟新增 constant、3个 Thumb alias、2个表标签当前均无同名定义/标签碰撞。
- 七个新增 CID 的身份由 `data/card-stats.s:20165,26574,11130,16304,25326,25937,4305` 独立核对。`0x7fff` 虽与 `DISPLAY_CTX_SLOT_DATA_MASK` 同值，但现名限定 display-context slot-data 读取；本段值用于构造 equip-activation card-id 字段，proposal 的领域化新名不冒用现有名称。
- 96个最终 slot label 均匹配 `^[a-z][a-z0-9_]+$`、互不碰撞。TSV 96条 EOL 纯 ASCII，最大87 bytes。proposal 当前8条 PLATE 也全为 ASCII，长度分别为375、256、351、320、310、350、356、250 bytes，均小于500；proposal/TSV 未出现零容忍词。

## 2. C1-C13 核验

| # | 检查 | 结果 | 独立证据与裁定 |
|---|---|---|---|
| C1 | Rule 1 地址序 | PASS | 活动路线图与总进度均指定 Seg-7=`[080a38fc,080a46a0)`，前六段已完成，未跳号；唯一高边界边不扩展 Seg-8 语义。 |
| C2 | Rule 2 裸块归宿 | PASS | 本段0个 `ROM_INCBIN/.byte`；两张真实引用的段外依赖表均计划当场 carve。 |
| C3 | Rule 3 仅收0引用 | PASS | 本段 `§5.1=0`；两表各有一个真实raw入边，未误入 §5.1。 |
| C4 | R1 值 | PASS | 96/96槽 u32 与ROM一致；两表6词与ROM一致。 |
| C5 | R1 复用/NEW | PASS | 49个 REUSE EQ 定义和值全匹配；11个新常量无同名碰撞，CID身份与四个字段值均有消费者证据。 |
| C6 | R2 名称 | PASS | 96个 slot label 合法且唯一；16个拟新增定义无同名碰撞。 |
| C7 | R3 接通 | **FAIL** | TSV:36-38 把 `080a3cb0/3cbc/3cfc` 三个 odd Thumb callback word 标为 REF，但只计划 GAS `fn+1` alias。当前 exporter `ExportRangeToGas.py:506-563` 的 ROM symbol 路径要求目标是 primary USER_DEFINED LABEL，并明确排除 Function；偶地址只有 Function，奇地址又不应创建落在指令中部的 LABEL。因此计划的 DATA-ref 无法安全导出指定 alias。其余19个真正 REF 的目标/引用前后态也尚未逐项冻结。 |
| C8 | R5 现名/PLATE | **FAIL** | proposal 的8条文本自身干净，但改名后 `asm/02_text_lp_fieldspell.s:16369`、`asm/12_equip_activation_scan.s:1906-1917`、`asm/23_sound_cardlist_libc.s:15357` 仍含三个旧函数名；source scope 只列 module12/13，漏 module02/23。另两处被保留函数的现 PLATE 本身就是错误 equip 语义，见 C11。 |
| C9 | ASCII | PASS | 当前计划8 PLATE与96 EOL均逐字节为ASCII，PLATE均小于500 bytes。新增/修订文本仍须保持此门禁。 |
| C10 | carve/Thumb `+1` | PASS | 两个 carve 是CID表，不含函数指针；三项 GAS alias 的 `even_function+1` 值本身正确，问题是槽动作应走 EQ 而非 DATA-ref。 |
| C11 | Function 误名 | **FAIL** | `080a3dac`/`080a3eb4` 被错误保留。前者只消费 Gate Guardian 三材料表且 caller 的 `0x111c` 分支直达它；后者只消费 Valkyrion三材料表且 caller 由 `0x13e9-0x5f=0x138a` 分支直达它。当前 `check_equip_set_activatable_for_player`、`eval_equip_card_placeable_for_player` 及各自 PLATE 与主体不符。 |
| C12 | R6 消费者证据 | **FAIL** | 其余6项 rename 有 caller/callee/global/CID闭合，但上述两项直接消费者证据没有进入 rename/plate 计划；R9落地前态也没有可审计的Ghidra对象证据。 |
| C13 | 残留覆盖 | PASS | 当前 asm 的96个 DAT/PTR 自动槽与TSV集合完全相等，无漏槽；动作总数也为96。分类修正后仍是同一96槽集合。 |

## 3. R1-R9 核验

| 项 | 结果 | 备注 |
|---|---|---|
| R1 常量 equate | **FAIL** | 70个当前EQ值正确；三个 odd callback word 也必须用 equate 路径，不能作为普通ROM REF。修后应为 `EQ=73`。 |
| R2 自动名语义化 | PASS | 全96槽均有合法唯一最终名；两表标签准确。 |
| R3 USER label + DATA-ref | **FAIL** | 两表和RAM地址可走REF；三个odd回调不可走REF。真正REF target/slot及四个RENAME现存ref还缺精确可执行合同。 |
| R4 误标代码 | PASS | 本段代码闭合为3050B，两外块均为数据；无R4。 |
| R5 注释/误名 | **FAIL** | 漏两项函数误名和三个段外旧名PLATE涟漪。 |
| R6 消费者取证 | **FAIL** | 两张表的消费者已经反证 proposal 对 `080a3dac/3eb4` 的 preserve 决定。 |
| R7 carve | PASS | 两张3-word表结构、真实引用、label与 `rom.s` 切割均正确。 |
| R8 图形 | PASS | 本段无图形资产/调色板决策。 |
| R9 备份、回滚、byte-identical | **FAIL** | proposal:231-246 只给粗粒度8文件备份和“失败恢复”一句话；没有完整source baseline、物理 `.rep` 15/15清单、fresh只读DB不变、单事务、输入冻结、receipt/marker与present/absent恢复合同，无法在全量导出/拆分/构建失败时证明无越界残留。 |

## 4. 修改清单

### #1 — C7 / R1 / R3 — 把三个奇地址 callback 槽改为 EQ，并补齐真正 REF 合同

1. 在 proposal 和 TSV 将 `0x080a3cb0=0x080a839d`、`0x080a3cbc=0x080a840d`、`0x080a3cfc=0x080a8479` 的动作从 `REF` 改为 `EQ`；target_symbol 继续使用现有三个 `*_1` alias，slot label 可保持，EOL改为明确的 `Thumb callback pointer ...+1` equate 文本，不再声称 operand-0 DATA reference。
2. 保留三个 GAS 定义 `alias = even_function+1`；Ghidra仅在三个pool word的operand 0安装同名 equate。禁止在 `080a839d/080a840d/080a8479` 创建 Label/Data/Function，禁止给三个槽创建 DATA ref。
3. 同步全部计数和验收：`EQ=73, REF=19, RENAME=4`，96槽、`REUSE=70/NEW=26`、3 aliases和总新增定义16均不变。
4. 对剩余19个 REF（5类既有RAM目标共17槽、2个新ROM表目标各1槽）新增逐target pre/post表，冻结 address/name/type/source/namespace/primary/alias count/Symbol identity与Data type/length；新增逐slot pre/post `from/to/operand/type/source/primary`、Data type/length/bytes和非目标refs合同。对四个RENAME槽同样冻结现存ref tuple并要求对象集合完全不变。导出验收必须逐槽得到预期 `.word symbol`，不能只以最终字节或文本计数代替对象检查。

### #2 — C11 / C12 / R5 / R6 — 补入两个由材料表闭合的 Function rename

1. 将 `0x080a3dac check_equip_set_activatable_for_player` 改为 `check_gate_guardian_summon_allowed`。证据链：`asm/13_equip_placement.s:14229-14334` 只装载/遍历 `09e47898` 的 Sanga/Kazejin/Suijin，`asm/13_equip_placement.s:16259-16262,16809-16812` 仅在 `0x111c` Gate Guardian dispatcher分支调用；输入为 `r0=u32 player_side`，返回u32 bool，read-only。
2. 将 `0x080a3eb4 eval_equip_card_placeable_for_player` 改为 `check_valkyrion_summon_allowed`。证据链：`asm/13_equip_placement.s:14367-14465` 遍历 `09e478a4` 的 Alpha/Beta/Gamma，`asm/13_equip_placement.s:16303-16311,16813-16816` 由 `0x13e9-0x5f=0x138a` Valkyrion分支调用；输入为 `r0=u32 player_side`，返回u32 bool，read-only。旧 PLATE 所称非APCS `r10=equip_card_id` 错误：循环中 `r10` 是从三材料表取出的当前CID。
3. 为两项写完整ASCII PLATE（每条不超过500 bytes），加入逐Function旧名/新名/APCS/body-ranges/caller/callee/global/CSV合同。同步为 Function rename=8、段内语义PLATE增加2条；CSV精确更新8个地址，22个Function body及create/delete=0不变。

### #3 — C8 / R5 — 闭合段外旧名与 source projection 涟漪

1. 全仓固定字符串扫描八个旧Function名，并把所有正式asm中的自由文本旧名纳入批准PLATE。当前至少有：`0x08033610 count_monster_slots_accepting_card` 的 PLATE（module02）含 `check_banisher_of_light_activatable`；`0x08094f58 write_spell_activation_type_display_bit` 的 PLATE（module12）含 `classify_spell_card_activation_type`；`0x0810e5e4 invoke_r7` 的 PLATE（module23）含 `check_banisher_of_light_activatable`。
2. 三处必须完整重写为ASCII并引用修后现名；其中 `08094f58` 的描述也必须改为实际调用的 special-summon material-rule classifier，不能只机械替换名字后继续声称 spell activation type。不得借本段扩大分析 Seg-8。
3. source projection 至少应列 `asm/02_text_lp_fieldspell.s`、`asm/12_equip_activation_scan.s`、`asm/13_equip_placement.s`、`asm/23_sound_cardlist_libc.s`、`asm/rom.s`、两份constants、CSV/registry/inventory/progress；重算 PLATE 总数。按当前闭合最小集合，总PLATE应为原8 + 两个新rename主体 + 三个段外ripple = **13**。落地后全仓扫描八个旧名在正式asm必须0命中，不能只查8/10个段内PLATE。

### #4 — R9 / C7 — 写成可执行、fail-closed 的 Mode B 与恢复合同

1. real apply 前建立新的物理 `.rep` 备份，冻结当前/backup完整relative-path、size、SHA256并要求15/15 exact；另起 fresh `-noanalysis -readOnly` prestate/dry，记录真实命令、脚本hash、exit=0/成功marker、DB查询前后15文件完整manifest exact equal。dry必须核全部96槽、19 REF、4 RENAME、22 Function bodies、2 carve targets、8 rename、13 PLATE、305 edges及ROM值，`FAIL=0`。
2. 冻结 proposal/TSV/review/plan/script及全部只读证据hash。对可能被全量 exporter/mode injection/split/inventory/sync/build触碰的正式路径建立物理 source baseline：至少全部25个 `asm/NN_*.s`、所有现存 `asm/*.s`（含 `rom.s/includes.inc`）、全部 `constants/*.inc`、Function registry、CSV、四份inventory、活动/总进度文档及计划script/plan；逐路径记录存在性、size、SHA256和物理副本。不得以Git作为恢复基线。
3. Ghidra real actions与postcheck放在一个transaction内；失败时 transaction rollback。apply进程只有在exit=0、transaction-commit marker、receipt状态/hash/counts全正确且DB确有预期变化时才算成功；启动前拒绝/删除旧receipt。保存后另起 fresh `-noanalysis -readOnly` persisted check，查询前后DB 15/15不变。
4. persisted check后才允许全量导出、mode injection、split、常量/alias/carve/CSV/inventory同步、`export_all.py`、`NOPAUSE=1 build.bat`、ROM size `33554432`、`fc /b`和SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。每一阶段都要做source-scope allowlist和最终无旧名/无自动槽/无意外Function或body变化检查。
5. transaction、save、persisted check、export、source edit、inventory、build、ROM或scope任一步失败，均立即忽略并删除provisional receipt，从物理backup恢复DB，再按baseline对原存在文件逐字节恢复、删除prestate absent而本轮新建的正式文件，最后fresh只读验证回到原prestate；不得写完成态progress/CSV。review通过后须按依赖顺序重冻review hash，再生成plan/script/source baseline/final dry，避免追加review造成hash循环。

## 5. 保持项

修订不得改变以下已独立通过的事实：范围3492B；96槽=`DAT92/PTR4`；100条literal reads覆盖96槽；布局1443代码单元/3050B、96 words/384B、29 padding/58B；22既有Function与65 body ranges；Function create/delete=0；两table carve共24B；R4=0；§5.1=0；305 direct edges=`60/163/82`；11 constants、3 aliases、2 labels及总新增定义16；所有Ghidra EOL/PLATE纯ASCII且PLATE不超过500 bytes。

## Reviewer Verdict: F13-Seg-7 = NEEDS_FIX(4 items)

---

## 6. 第二轮独立复审

### 6.1 冻结输入与证据

- 修订 proposal SHA256：`72a2db1629f8859c7447d8a372343e80c173f1178f1401f15451505b4f11fa06`，395行。
- 修订 TSV SHA256：`2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f`，含表头97行、数据96行。
- 第一轮 review SHA256：`c712c4c0bed4d32f74ff076e2ed15ba10baa83473010d8c296e734d0632fc89c`。
- `f13-seg7-ghidra-prestate.json` SHA256：`1f3e9e9caeac326228363210903928d94a2ea3359ff3c80ee2f624fb88374140`；gate SHA256：`0b270860b55175a9e6469c4291b4cccce69aee6d4fc5c7bbb0e9c2375519cf87`；查询脚本实算 SHA256 `57dc9f25d912f974e70e94a9394267ee981b00a3bf8f539fc33ab666ea3779bf`，与gate一致。
- gate记录的真实headless参数包含 `-noanalysis -readOnly`，exit=0且成功marker存在。独立重算当前 `.rep` 的15个文件，relative path、size、SHA256仍与gate before/after的15项完全相等；DB没有被本轮查询改变。
- `f13-seg7-modea1-selfcheck.json` 的摘要计数和输入hash均能复算，但该文件仅作为交叉索引，不替代以下独立判断。

### 6.2 第一轮四项修改复核

| 第一轮修改项 | 结果 | 第二轮独立证据 |
|---|---|---|
| #1 odd callback EQ与REF对象合同 | **PASS** | TSV三槽 `080a3cb0/3cbc/3cfc` 均已改为EQ，值分别为 `080a839d/840d/8479`，EOL明确 `even Function + 1` 且禁止DATA ref。对应偶地址 `080a839c/840c/8478` 仍是现有Global USER_DEFINED Function，三个 alias 无当前定义碰撞。总数已为 `EQ73/REF19/RENAME4`。独立解析prestate：19个REF源均为唯一Global primary DEFAULT label、`/undefined4`/4B、refs/equates为空；四个RENAME均为`/pointer`/4B并精确保留唯一 `operand0 DATA/DEFAULT/primary -> 0201c4e0(id15545)`。八个target的ID/name/source/type/namespace/primary/alias/Data与proposal逐项一致。 |
| #2 `3dac/3eb4`新增rename | **PASS** | 两项已加入Function表、精确body/APCS、CSV/registry与PLATE合同；总计8 rename。ROM与消费者仍证明 `3dac` 只扫描Sanga/Kazejin/Suijin且由Gate Guardian `111c`分支调用，`3eb4`只扫描Alpha/Beta/Gamma且由Valkyrion `138a`分支调用；`r10`是循环内材料CID而非入口参数。22个段内Function及65 body ranges不变。 |
| #3 三处段外ripple与13 PLATE | **FAIL：仍有一层直接涟漪** | proposal列出的13条PLATE全是ASCII且长度均小于500，module02 `08033610`、module12 `08094f58`、module23 `0810e5e4`三处已纳入。但 `08094f58` 的新文本仍写“no caller-passed parameters”；实际 `asm/04_card_zone_sprite.s:3053-3057` 从当前field-slot word抽取低13位CID到r0后直接调用它。该文本随后又明确“not a spell activation type”，却保留自相矛盾的Function名 `write_spell_activation_type_display_bit`。其唯一直接caller `0804154c` 的现PLATE在 `asm/04_card_zone_sprite.s:2989` 仍含 `FUN_08094f58 (write_spell_activation_type_display_bit)`；module04、该PLATE及该Function rename均未进入scope。C8/C11/R5仍未闭合。 |
| #4 R9 landing/恢复合同 | **PASS** | proposal:345-382 已写明新物理`.rep`、15/15 manifest、完整formal source present/absent物理baseline、冻结输入依赖顺序、fresh只读dry、单transaction+rollback、commit marker/provisional receipt、fresh persisted check、full export/mode/split/inventory/CSV/registry/export_all/build/fc/SHA1、任一步失败的DB与source物理恢复；禁止stage/commit。合同足以在Mode B物化时做fail-closed实现审查。 |

### 6.3 回归核验

- 重新逐行读取TSV并从ROM取值：96行、地址有序唯一，`DAT92/PTR4`、`REUSE70/NEW26`、`EQ73/REF19/RENAME4`；96/96 u32值相等，96个slot地址的raw与THUMB|1全ROM scan仍全为0。所有slot label合法唯一，96个EOL均为ASCII。
- 两个依赖表的全ROM扫描仍分别只有 `080a3e90 -> 09e47898`、`080a3f8c -> 09e478a4` 两个raw命中，THUMB|1均0；六词仍为 `1119/111a/111b` 与 `1288/129b/12b8`，carve切割 `4+24+245c=2478` 正确。
- 当前 `asm/13_equip_placement.s` SHA256仍为 `bedc6c7c34abfb18f1ddbcc979e1ad49d5f33d1bfcc740ba1a76316d2090042f`，故第一轮自主重解的1443代码单元/3050B、96 words/384B、29 padding/58B、305 edges=`60/163/82`及22 Function/65 body并集结论未漂移。
- 13条现有计划PLATE长度为 `375,256,351,395,414,320,310,350,356,250,371,382,351`，全部ASCII且小于500；proposal/TSV没有零容忍词。11 constants、3 aliases、2 labels仍无同名碰撞；新候选名 `write_special_summon_material_rule_display_bit` 也无碰撞。
- 因第三项未闭合，最终矩阵保持 `C8/C11` 与 `R5` 失败；C1-C7、C9-C10、C12-C13及R1-R4、R6-R9通过。本轮没有证据构成BLOCKED。

### 6.4 第二轮修改清单

#### #1 — C8 / C11 / R5 — 闭合 `08094f58 -> 0804154c` 的直接语义涟漪

1. 将 `0x08094f58 write_spell_activation_type_display_bit` 改名为 `write_special_summon_material_rule_display_bit`。其代码直接把入口r0传给 `get_special_summon_material_rule_by_card_id`，所以签名必须为 `r0=u16 card_id; returns void`，不能写“no caller-passed parameters”。冻结同一Function ID、Global USER_DEFINED source和精确body `[0x08094f58,0x08094f6e)`；禁止resize/create/delete/split。
2. 将 `0x08094f58` 的完整ASCII PLATE改为等价的精确文本：`Tests whether card_id r0 has a dedicated special-summon material rule. Calls get_special_summon_material_rule_by_card_id; if the result is nonzero, calls write_card_display_index_with_bit_offset with display index 0x1a and bit value 1. Returns without writing when the rule is 0. Input: r0=u16 card_id. Returns: void. Confidence: high.`
3. 新增 `0x0804154c tick_spell_equip_zone_display_seq` 的完整ASCII ripple PLATE，去掉 `FUN_08094f58` 和旧名并引用新名。可执行文本：`Handles duel display sequence case 0x44 for a spell or equip field slot. Reads the player, slot and packed flags from the display state, writes applicable display-index bits, and calls write_special_summon_material_rule_display_bit with the current field-slot card ID. Marks the field slot active, dispatches display operation 0x24, and clears the step-lock field. Confidence: high.`
4. 同步proposal、consumer/ripple evidence、CSV/registry和所有验收计数：Function rename=`9`，PLATE=`14`，旧名固定扫描集合=`9`；source projection新增 `asm/04_card_zone_sprite.s`，成为modules `02/04/12/13/23`。段内22 Function/65 bodies、96槽与 `73/19/4`、13项新增定义目标、两carve、305 edges、R4=0、§5.1=0均不得改变。
5. 增补 `08094f58` Function及 `0804154c` PLATE的fresh只读prestate合同；第三轮复审通过后按 `review -> plan -> script -> complete source baseline -> final fresh dry` 顺序重新冻结hash。本review在最终PASS后冻结，之后不得以追加说明再次制造hash循环。

## 第二轮状态：NEEDS_FIX

## Reviewer Verdict: F13-Seg-7 = NEEDS_FIX(1 item)

---

## 7. 第三轮最终独立复审

### 7.1 冻结输入与 fresh 前态

- 最终 proposal SHA256：`129f42778a7ed9da2ec4e082da91d71577532e56016d4f2cb394e797a8d63a99`；TSV SHA256：`2bd2619525cf56f5a996a2c8eb4dd91161958b1e825906d91e680e690221a99f`；本轮追加前 review SHA256：`61b478f23eea5439a83843a0e7ae6cb11f6698a7119e84f0823abf47fc4839f3`。
- Round2 self-check SHA256：`e5ec57751e8531fbdd4dd92cfd6d7ad5d6039fdcde0d9c3f8a7dabb499834d6e`。该文件只作交叉索引；本节结论来自ROM、当前asm、TSV、registry/CSV及fresh Ghidra证据的独立核对。
- fresh查询脚本、结果、gate SHA256依次为 `13d5032c70438ca67cd5ad8e8bdbc2089cb70cdee6606c0f2ea7f196f760d51f`、`54d59f1f9cdad65c034da875f92f367944adba41ab332a93b4a5e031ddf0a623`、`57efed71e2db94267a220d69f0c07478371c117c2157742a363db9a03a2ccbab`。gate记录真实命令含字面量 `-noanalysis -readOnly`，exit=0，日志含成功marker `targets=8 REF=19 RENAME=4 EXT_FN=2`。独立重算当前 `.rep` 得15文件；relative path、size、SHA256与gate before/after逐项相等，差异0、额外文件0。
- 保持项证据仍被冻结为 refscan `e98fe19aa98963f587f62ef05107aad86e1a2aa3292d4a7b54cb8472c276d52a`、Functions/body ledger `57e4d3cf6a5720d6ddf7d20074fdddd58a688489f6c125e3397de7c2940301c3`、direct-edge ledger `afc0106593069583a9ad418b6e4c5501bc6f277a3eac92d90208c1200632767e`、layout `c2487fa74d1ee2f348e0e8e07c0f8f816c131004c93a6b1a79ad98cec1a50798`。当前 `asm/13_equip_placement.s` SHA256仍为 `bedc6c7c34abfb18f1ddbcc979e1ad49d5f33d1bfcc740ba1a76316d2090042f`，因此上一轮已独立重解的Function/body/layout/305条直接边没有输入漂移。

### 7.2 上一轮唯一修改项闭合

| 核验点 | 结果 | 独立证据与裁定 |
|---|---|---|
| `0804154c` caller传参 | PASS | ROM `080415b6..080415c2` 为 `4146 0868 c004 c00c 53f0 cbfc`：`mov r1,r8; ldr r0,[r1]; lsls/lsrs #19` 精确抽取低13位card ID，`080415be` 的Thumb BL独立解码目标为 `08094f58`。新PLATE写明current field-slot card ID，删除了旧 `FUN_08094f58` 与旧函数名，文本335 bytes、纯ASCII。 |
| `08094f58` body与新名 | PASS | ROM `08094f58..08094f6e` 为22 bytes，入口先 `push {lr}`，`08094f5a` BL独立解码到 `080a422c`；调用前没有改写r0。返回值为0时直返，非零时装载 `r0=0x1a,r1=1` 并在 `08094f66` BL到 `write_card_display_index_with_bit_offset`。因此 `write_special_summon_material_rule_display_bit` 与 `r0=u16 card_id; returns void` 同时符合caller和callee；名称满足R1且全仓无现有同名碰撞。新PLATE 351 bytes、纯ASCII。 |
| Function对象合同 | PASS | fresh前态中 `08094f58` 是ID5446、唯一Global primary USER_DEFINED Function、alias0、body `[08094f58,08094f6e)`/22B；`0804154c` 是ID5416、同类唯一Function、alias0、四段body共466B。两者 calling convention=`unknown`、return=`/undefined`、parameters=`[]`。proposal只授权前者同ID改名和两者完整PLATE替换，禁止body或Function集合变化。 |
| CSV、registry、exporter | PASS | `doc/dev/naming-proposals.csv` 九个地址各恰有一行，`08094f58` 当前行名是旧名；registry八个段内 `FUN_` tuple各恰一项，`FUN_08094f58` 当前为0项，符合“更新8项并新增1项”的合同。投影已冻结为 module12 定义新名、`08094f5a -> get_special_summon_material_rule_by_card_id`、module04 `080415be -> write_special_summon_material_rule_display_bit`；正式模块落地后旧九名及 `FUN_08094f58` 必须为0。 |
| 计数与范围同步 | PASS | proposal现为 `FUNC_RENAME=9, PLATE=14`，14个地址唯一；PLATE长度 `375,256,351,395,414,320,310,350,356,250,371,382,335,351`，全部ASCII且最大414B。批准源模块精确为02/04/12/13/23；module04与 `08094f58` 已进入pre/post、receipt、persisted、exporter、CSV/registry和恢复合同。 |

### 7.3 回归抽检

- 重新读取TSV并取ROM小端值：96行地址有序唯一，`DAT92/PTR4`、`EQ73/REF19/RENAME4`、`REUSE70/NEW26`；96/96值相等，96个slot地址的全ROM raw与THUMB|1扫描均为0。slot label全部合法唯一，96条EOL全部ASCII。
- 三个odd callback槽仍为EQ：`080a3cb0=080a839d`、`080a3cbc=080a840d`、`080a3cfc=080a8479`；没有奇地址Label/Data/Function/REF授权。19 REF、4 RENAME及8 target的fresh对象合同与第二轮结论一致。
- 全ROM重扫两表：`09e47898` raw唯一来源 `080a3e90`、THUMB|1为0，三词 `1119/111a/111b`；`09e478a4` raw唯一来源 `080a3f8c`、THUMB|1为0，三词 `1288/129b/12b8`。两段各12B、carve总24B，R4=0、Rule3=0保持。
- ledger仍为22个本段Function/65 body ranges、305 direct edges=`B60/Bcc163/BL82`，Function create/delete=0。11 constants、3 Thumb aliases、2 table labels及总新增定义16不变；proposal/TSV的执行文本没有非ASCII或禁词。

### 7.4 C1-C13 最终矩阵

| # | 检查 | 结果 | 第三轮裁定 |
|---|---|---|---|
| C1 | Rule1地址序 | PASS | 范围仍为 `[080a38fc,080a46a0)`，不分析Seg-8 body。 |
| C2 | Rule2裸块归宿 | PASS | 段内无裸块；两张有引用的三词表均carve。 |
| C3 | Rule3零引用 | PASS | 本段§5.1=0；两表各有唯一raw入边，未误收Rule3。 |
| C4 | R1值 | PASS | 96/96槽与两表6词均与ROM一致。 |
| C5 | R1复用/NEW | PASS | 复用与新增集合、值和定义碰撞检查未漂移。 |
| C6 | R2名称 | PASS | 96槽、16新增定义及九个函数终名合法且无碰撞。 |
| C7 | R3接通 | PASS | 19 REF/4 RENAME/8 targets有完整对象合同；三个odd callback仅走EQ。 |
| C8 | R5现名/PLATE | PASS | 14条完整ASCII PLATE覆盖九个rename、两个段内保留函数和三处外部ripple；模块02/04/12/13/23闭合全部旧名涟漪。 |
| C9 | ASCII | PASS | 14 PLATE与96 EOL全部ASCII，PLATE均小于500B。 |
| C10 | carve/Thumb+1 | PASS | 两表是CID数据；三个callback alias精确为even Function+1且不创建odd Symbol。 |
| C11 | Function误名 | PASS | 九项rename均有body/caller/callee/global/CID证据；本轮新增 `08094f58` 由caller传参与callee行为双向闭合。 |
| C12 | R6消费者证据 | PASS | 关键语义均有地址或file:line证据；`0804154c -> 08094f58 -> 080a422c` 已由ROM机器码复核。 |
| C13 | 残留与恢复 | PASS | 96自动槽全覆盖；R9计数、source scope、present/absent恢复及receipt门禁同步到9 rename/14 PLATE。 |

### 7.5 R1-R9 最终矩阵

| 项 | 结果 | 裁定 |
|---|---|---|
| R1 | PASS | 73 EQ值正确；九个函数终名均为合法verb-object-qualified形式。 |
| R2 | PASS | 96个自动槽都有唯一语义名。 |
| R3 | PASS | 19 REF可导出，4 RENAME保持原引用，target/slot对象合同完整。 |
| R4 | PASS | 代码/word/padding布局闭合，无新增反汇编。 |
| R5 | PASS | 九个误名及14条PLATE的语义和旧名涟漪全部闭合。 |
| R6 | PASS | 材料表、guard、CID及本轮card_id参数均有独立消费者证据。 |
| R7 | PASS | 两表carve边界、引用、ROM词与rom.s切割合同正确。 |
| R8 | PASS | 无图形资源决策。 |
| R9 | PASS | proposal要求新物理`.rep` 15/15、完整source present/absent物理baseline、输入hash冻结、fresh只读dry、单事务rollback、commit marker与严格receipt、fresh persisted check、全量export/mode/split/inventory/CSV/registry/export_all/build/fc/SHA1；任一失败均物理恢复DB与source后再fresh验证。receipt精确计数为 `EQ73/REF19/RENAME4/EOL96/FUNC_RENAME9/PLATE14/CARVE2/FIXED_OLD_NAME_SCAN9`，缺项、额外项或错值均拒绝。 |

### 7.6 Mode B允许范围与冻结顺序

本proposal获准进入物化与实现审查，但尚未授权real apply。Mode B只可实现：96槽的 `73 EQ + 19 REF + 4 RENAME + 96 EOL`；九个既有Function同ID改名；14条完整PLATE；两张12B表carve；11 constants、3 aliases、2 labels；CSV九行、registry八项更新加一项新增、四inventory及进度同步。Ghidra Function create/delete、body改变、R4和§5.1均为0。正式asm批准变化限定modules02/04/12/13/23以及明确列出的rom.s/constants/CSV/registry/inventory/docs；其余正式路径必须与baseline一致。

本节追加后review冻结。fixer必须按 `final review SHA -> plan -> script -> complete source baseline -> final fresh dry -> 独立实现审查` 顺序重冻输入；任何后续文档追加都会使旧hash失效。real apply仅能在实现审查通过及root最终门禁通过后执行。

## 第三轮状态：PASS

## Reviewer Verdict: F13-Seg-7 = PASS
