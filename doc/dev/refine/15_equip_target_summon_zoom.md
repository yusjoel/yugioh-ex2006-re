# 函数和数据细化计划 · `asm/15_equip_target_summon_zoom.s`

> 范围 `[0x080b5348,0x080c1448)`，共 49408 字节。主序已完成 16/25 个模块，历史正引用补漏 1 项。模块 15 的 Seg-1 至 Seg-10 已全部完成。

## 一、规则

沿用 `doc/dev/methodology/refine-loop.md` 的三条地址序规则和 R1–R9。先读实际消费者和现有常量。Ghidra 新 PLATE 和 EOL 用 ASCII，PLATE 上限 500 字符。

## 二、验收流程

每段备份源码和数据库，冻结提案后独立复核。复核通过后，用只读事务试跑脚本和回滚，再持久化并独立读取后态。全量重导汇编，完成 49 项资产导出和构建，逐字节核验 ROM 后更新进度。

## 三、当前进度

10 段已全部完成。全模块 252 个 Function、20373 条指令和 1446 个池字，自动数据名 0、原始块 0。下一文件为 `asm/16_duelfield_zone.s`，范围 `[0x080c1448,0x080cbf0c)`；其活动文档尚未初始化，后续须先按函数结束边界划分约 10 段，再从 Seg-1 开始。

## 四、工作记录

### 4.00 建档（2026-11-04）

保存后的只读测绘覆盖 117 个既有 Function、15092 条指令、1264 个字面量池字及全部 49408 字节，15 个数据库文件的哈希一致。边界保留 Function 的完整 body、3299 条模块内短分支和 PC 相对读取边及五个原始块。Seg-1 保留 B5D98 调度器和其共用栈帧的策略片段，下一段从 B6C08 开始。

五个原始块共 12142 字节，位置和长度记录于 `root-f15-map-source-inventory.json`，由各段核对引用。Seg-2 的 B76A4 为 4 字节回调入口，前一模块交接的 79 条奇地址表指针将随 Seg-2 处理。前态用 `root-f15-independent-map-prestate.json` 的全局 Equate 和 `root-f14-seg10-independent-post.json` 的逐表项状态交叉核验。

全量重导时保留模块 14 的三处表级操作数投影。B4BDC、B4C68 使用 `normal_summon_response_primary_table`，B4C38 使用 `normal_summon_response_secondary_table`。证据见 `f14-seg10-table-base-source-projection-v1.json`。这三处与 Ghidra 导出的首行 CID 主符号同地址，重导后在汇编层核对原字节再投影。

### 4.01 Seg-1 完成（2026-11-04）

范围 `[0x080b5348,0x080b6c08)` 共 6336 字节。保留 28 个 Function 的 body 和 2710 条指令，其中 59 个指令起点未归入 Function。141 个池槽完成，含 102 个常量绑定、24 条新增 DATA 引用、10 条既有 DATA 引用和 5 个 Thumb 回调指针。151 条既有 PC 读取、五个奇指针值和共用栈帧的机器跳转均保留。

新增 15 个常量，写入 28 条 ASCII PLATE 和 141 条 EOL。B5BAC 更名为 `score_slot_by_summon_restriction_without_chain`，同步名称来源和 B6578 的回调表达式，保留 Function ID 和签名。B5D98 的三个体内池槽记录 EOL，其中两个增加 DATA 引用。

全量重导后，在 B655C、B6578、B69DC、B6B6C、B6BB8 核对原始字，再将 Ghidra 的局部 `_1` Equate 导出表达式投影为汇编的 `Function+1`。复用 `f15-seg1-thumb-gas-projection-v1.json` 的五项地址与字节核对，连同模块 14 的三个表级操作数投影一起保留。

只读试跑和强制回滚通过。保存后的独立核验覆盖模块全部 49408 字节、117 个 Function、1264 个池槽，以及 Seg-2 待接续的 79 条表绑定。资产导出 49/49，重建 ROM 的 33554432 字节与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。

最终门禁 SHA256 `6cc7e75fb0577d02565abdaccfd452238adcb8252884adc3b2c8d354c0cccb1d`，流水线收据 SHA256 `bd5711c32874fc32b96d2f7e35ca1d3f68b08f16fa397644e6343acbfc54e3c8`。

### 4.02 Seg-2 完成（2026-11-04）

范围 `[0x080b6c08,0x080b79f8)` 共 3568 字节。B76A4 的四个字节恢复为 `movs r0,#1` 和 `bx lr`，函数名为 `return_true_response_callback`。本段最终有 19 个 Function、1498 条指令、87 个字面量池字和 60 字节对齐填充。

完成 65 个标量绑定、10 条新增 DATA 引用、9 条既有 DATA 引用和 3 个 Thumb 池槽。写入 22 条 ASCII PLATE 和 87 条 EOL，新增 3 个 GAS 常量并复用 5 个已有定义。4 个现有函数改名。模块 14 的两个调用操作数和一条 PLATE 随 B771C 更名投影，地址和字节保留。

全 ROM 的 201 条 B76A4 回调指针来自七张表，其中两张旧表 79 条，五张新结构化表 122 条。新表共 504 条记录，创建 998 个 dword 并保留 10 个既有类型。保留相邻三行表的 24 字节和后续 2892 字节。旧表同步 89 个表达式，其中 79 条关闭 B76A4 待处理别名，10 条同步已有函数的新名。新旧表均保留原始 Thumb 低位和原始字节。

新表中的 267 条后续绑定按地址序交接。Seg-3 为 64 条、38 个目标，Seg-4 为 202 条、94 个目标，Seg-5 为 1 条、1 个目标。六处后续表基址字保留到各自所属段。全局 Equate 由 2252 个增至 2417 个，新增 168 个，退役 3 个，按计划增加或迁移 661 条绑定。

独立数据库、源码、ELF、命名同步均通过。资产导出 49/49，重建 ROM 的 33554432 字节与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 `9f80ab6414d8ad815bb130c9849e0d8d4bc5d41bee4a26d367d81aee1d46b26a`，流水线收据 SHA256 `98d8d12beeeeb84a06b86b7a5b2b8f7a30428aa5a66b6b1867b19be32fd2a814`。

### 4.03 Seg-3 完成（2026-11-05）

范围 `[0x080b79f8,0x080b8a24)` 共 4140 字节。两个原始块的 3512 字节划分为 1545 条 Thumb 指令、50 个字面量池字和 58 字节对齐填充，恢复 38 个函数。为 `0x080b88c0` 的两条既有指令另建一个恒真回调函数。本段最终有 45 个函数、1825 条指令、58 个池字和 68 字节对齐填充。

完成 29 个标量绑定、24 条新增 DATA 引用、2 条既有 DATA 引用和 3 个 Thumb 池槽。写入 45 条 ASCII PLATE 和 58 条 EOL，3 个既有函数更名。新增 `UMI_PACKED_CID_FIELD`。在既有结构化表中迁移 64 条待处理回调，并同步 3 条更名。未来 203 条表引用按地址序保留。全局 Equate 从 2417 个增至 2421 个，新增 45 个，退役 41 个。

数据库、源码、ELF 和命名同步均已独立验收。资产导出通过 49/49，重建 ROM 的 33554432 字节与原件逐字节一致，SHA1 为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 为 `9f7ac259126a63925d870235a6b26e3a86aef5aee17c8691d74a2e72e4fc299d`，流水线收据 SHA256 为 `3f909b3ee443cfe1f5073eb62cebc5f6e0e682301ab9762b544d219dca95eee4`。

### 4.04 Seg-4 完成（2026-11-05）

范围 `[0x080b8a24,0x080babd4)` 共 8624 字节。原始块 8578 字节恢复为 94 个 Function、3714 条 Thumb 指令、130 个池字和 138 字节零填充。既有 B8A24 函数的 46 字节及其元数据保留。本段最终有 95 个 Function、3735 条指令、130 个池字。

完成 85 个标量绑定、43 条 DATA 引用和 2 个 Thumb 池槽。写入 94 条 ASCII PLATE 和 130 条 EOL。新增 FIELD3 的 1700 门槛、Chaos Command Magician CID 和对侧 LP 的 2900 门槛三个 GAS 定义，已有 BOOK_OF_LIFE_CID 定义复用。全局 Equate 从 2421 个变为 2425 个，新增 98 个并退役 94 个，完整绑定数从 12238 变为 12325。

既有结构化表的 202 条待处理回调迁移至 94 个最终函数，原始 Thumb 低位和字节保持。Seg-5 的一条待处理引用继续按地址序交接。规范函数清单为 5413 个，新增 94 个命名函数。

数据库、源码、ELF 和命名同步独立验收通过。资产导出 49/49，重建 ROM 的 33554432 字节与原件逐字节一致，SHA1 为 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 为 `8eaf8795c71333bcbbd52abaf9338a3e630f15b8a1f63c329921489dda8e90db`，流水线收据 SHA256 为 `078c9a69e7302a135ba216b07eb4e94bea40ac51b69d232df2ccf145b4cd31df`。

本段 B9E0A 调用模块 05 的 `SUB_0804becc`。该 84 字节原始块已有 typed 调用者 04D374，旧 F05-Seg-4b 的零引用登记须重新分类。本段保存其字节、类型、DEFAULT Label 身份和 Function 缺席状态，新增当前调用的原生引用。此项进入全局正引用补漏清单，主序 25 模块完成后按地址闭合。

### 4.05 Seg-5 完成（2026-11-05）

范围 `[0x080babd4,0x080bb3dc)` 共 2056 字节。最后 48 字节原始块恢复为 1 个 Function、20 条 Thumb 指令和两个池字。本段最终为 12 个 Function、869 条指令、50 个池字和 32 字节原样零填充；模块全部原始代码块已处理。

完成 28 个标量绑定、15 条新增 DATA 引用和 7 条既有引用保留，写入 50 条 ASCII EOL、14 条 PLATE，订正两个 Function 名称及其必要段外派生引用。新增 Rapid-Fire Magician CID 和装备激活 ready 字段偏移两个 GAS 定义，Skull Descovery Knight CID 复用既有拼法及既有 Ghidra 对象。全局 Equate 2425→2429，绑定 12325→12359。

外部三行响应表 `[0x09e488d8,0x09e488f0)` 的 24 字节完成结构化，6 个词精确保留原值，三个 Thumb callback 使用 Function+1。最后一条 pending callback 绑定迁移至新函数，pending alias 全部闭合。17 个既有 GAS 投影及历史 84 字节正引用补漏的状态保留。

保存后数据库、源码、命名清单、ELF 和回调表全部通过独立验收。规范函数清单为 5414 个，其中命名 5324 个、自动名 90 个。资产导出 49/49，重建 ROM 33554432 字节与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 `90b7bd993cc3d977f4247fb6c146c0808b8585d3ec78c92af2405e1d99855146`，落地收据 SHA256 `bf081dbdb98d861db61afcd3aa11e98c9741415614e729cbe5865a2010f4d729`。未 stage/commit。

### 4.06 Seg-6 完成（2026-11-06）

范围 `[0x080bb3dc,0x080bc71c)` 共 4928 字节，12 个既有 Function、1982 条指令、160 个池字和 78 字节原样零填充。无 Function 改名、新建、R4 或 §5.1。155 个自动源名替换为语义名，5 个 switch word 保留 ANALYSIS namespace、ID、类型及既有引用。

完成 97 个标量 Equate 绑定、42 条段内新增 DATA 和 21 条既有引用保留；外表另增加两条偶入口 DATA，合计 44 条新引用。写入 155 条源 EOL、10 条外表 EOL、2 条已批准 RAM EOL 和 9 条 PLATE，另 3 条 PLATE 原样保留。新增两个 CID GAS 定义及两个 RAM 地址别名；全局 Equate 2429→2438，绑定 12359→12465。全部 167 个新主标签和旧引用的派生元数据通过完整闭包核验。

外部状态回调表 `[0x09e5ab5c,0x09e5ab84)` 结构化为 9 个 Function+1 和 1 个零终止词；host 精确拆为 2+40+120 字节。前 7 条 odd DEFAULT 引用、9 个 odd 目标、两个边界及既有类型保持；只新建 2 个四字节 Data。保留 18 个既有 GAS 投影，并落实 BC198 已冻结的 ANALYSIS 目标表达式；后续重导须携带全部 19 个投影。BC784 只作源码表达式投影。命名 registry 仅同步 7 个既有 PLATE，4 个缺席项保持缺席，CSV 和函数清单名称不变。

实施演练先结束 Ghidra 脚本自动外层事务，再开自有最外层，完整改动后态验证 0 FAIL；强制回滚后在同一 Program 上完整前态复查 0 FAIL。唯一正式保存、新进程复查、主线程独立 Java 保存后快照与全部源码/ELF 门禁通过。规范函数清单仍为 5414 个，命名 5324 个、自动 90 个、thunk 1 个。

资产导出 49/49，重建 ROM 33554432 字节与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 `fe46355a4803d2301e30bf84f6d5881e0a58a9e80f30cead3d02f6f6b1e513f7`，流水线收据 SHA256 `a97a149060472db197546260ccdea5a12a16301b6a3ffa1eaf5b28db17b1bdb1`。历史 84 字节正引用补漏及两条 CALL 状态保持。未 stage/commit。

### 4.07 Seg-7 完成（2026-11-06）

范围 `[0x080bc71c,0x080bda7c)` 共 4960 字节，11 个既有 Function、1880 条指令（3950 字节）、235 个池字（940 字节）和 35 处原样填充（70 字节）。无 R4、carve、新建 Function 或 §5.1 登记。170 个自动源标签与 EOL 完成细化，65 个 switch word 保留原类型、ANALYSIS namespace、静态 ID 及机器引用。

235 槽为 45 个 Equate 绑定、62 条真实新增 DATA、63 条既有 DATA 保留及 65 条纯保留。既有 21 条 DEFAULT 和 42 条 USER_DEFINED 引用的 CORE6 与 source 不变，派生元数据按批准的 204 节点图更新；8 个 ANALYSIS switch 的完整 qualified name、重合地址 incoming 后态均通过核验。全局 Equate 2438→2446，绑定 12465→12510。

完成 5 个稳定 ID 的 Function 改名：`init_banner_state`、`blend_palette_block_toward_white`、`play_vija_scene_with_sprite_intro`、`play_exodia_demo_scene_with_field_restore` 和 `play_three_sprite_banner_blend`。31 条完整 ASCII PLATE 与全部调用者闭包落地，ABI、body、类型、参数和旧引用保持；命名 registry 仅改 29 个现存 tuple，3 个缺席项保持缺席，C728 只同步 registry 注释。CSV 仅改 5 个 name cell，规范 inventory 仍为 5414/5324/90/1。

GAS 端追加 34 个定义，3 个既有地址定义复用；现有常量仅修正 1 处旧函数名注释。19 个继承投影、8 个 switch 投影及 13 个受原生导出地址白名单限制的 PALRAM/VRAM 投影合计 40 项，后续重导必须全部携带。原生 exporter、`asm/rom.s`、其余 19 个模块和历史命名材料保持。

实施脚本先通过实际 AST 与独立审查，再在真实 Program 中执行全部动作并核完整后态 0 FAIL；结束自有最外层事务后，同一 Program 完整前态复查 0 FAIL。唯一正式保存、新进程保存后检查、主线程独立 Java 全量查询均通过，覆盖 411 个实际 Function、10068 个完整地址状态、49408 字节模块及 48 字节外部窗口。全部源码范围、WORD/ELF 与布局门禁通过。

资产导出 49/49，33554432 字节重建 ROM 与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。最终门禁 SHA256 `9ac6e05cad40db5e6984103e9b4d59be6d6b09b9d3e3b9ecd97541777058e5dc`，落地收据 SHA256 `d4df47bf5fdea19252a3e41b6a1b39bafb25e95d297924070885b5eb90a99813`。历史 84 字节正引用补漏及两条 CALL 状态保持。未 stage/commit。

### 4.08 Seg-8 完成（2026-11-06）

范围 `[0x080bda7c,0x080bede4)` 共 4968 字节。193 槽由 41 个 Equate 绑定、79 条新增 DATA、45 条既有 DATA 保留和 28 条纯保留组成；165 个源标签与 EOL、27 个目标标签、1 个稳定 ID Function 改名及 8 条 Function PLATE 合同均已落地，其中实际写入 3 条 PLATE、保留 5 条。全局 Equate 2446→2455，绑定增加 41 条至 12551。无 R4、carve、新建 Function、数据类型变化或 §5.1 登记。

完整 412 个实际 Function、10069 个地址状态、193 个 primary 节点和 13 个 Function 的 243 条 rich reference 均按冻结后态核验；原有静态 ID、CORE6、类型、source、operand 和 primary 保持。命名 registry 的 8 个 Function 中 7 个 name-key tuple 一直存在，`BE9BC` 为唯一缺席项；`BDFAC` 仅对齐现存 tuple 的 comment，不是新增 tuple，也不是 Ghidra PLATE 写入。最终 registry 实际更新 3 项，CSV 只改 1 个 name cell，规范 inventory 仍为 5414/5324/90/1。

实施授权 v1/v2 先收紧单次保存协议和完整成功收据校验。v4 的真实只读运行在 owner DTO 后态适配与 Java heap 校验阶段终止，未执行持久保存，也未形成 rollback PASS；故障后的 DB15、source181 及副本物理哈希均与前态一致。v5 完成真实全动作后态 0 FAIL、同一 Program 强制回滚后完整前态 0 FAIL，并通过最终独立审计；随后仅执行一次持久保存（apply SHA256 `a170d43e88e0144477b1aebd9cdd6c234162fcfcb6ddd6244b034b58b28db242`），新进程保存后检查 SHA256 `835705c3aafae1c2b44ff4a64c50377147087d21b8671fb2c787631cd175277c` 及独立 Java saved-DB 验收均通过。

源码同步覆盖精确 14 个批准路径，新增 34 个 GNU 定义、携带 60 个 GAS 投影，并完成 3 个 registry 更新和 1 个 CSV name cell 更新。原生导出后 `BE108` 的字面量 `.word 0x06014000` 按冻结槽合同改为既有 `AOB_CARD_TILE_VRAM`；该 Root source-only 修正只涉及 `asm/all.s` 与模块 15 重拆分，未修改 Ghidra 或冻结的 60 项 GAS 计划，修正证据 SHA256 `71939d88a31e58fba75d26afc8933c3bf7cd9e429fa2eacb034a043e7366650d`。SourceScope 核验批准路径 14、越界变化 0，193 个表达式、34 个定义、3 个 registry 更新和 1 个 CSV name cell 全部精确。

WORD/ELF 的 193/165/9/27/1/60/4968 项核验全部通过。段内最终为 1984 条指令（1872 mnemonic + 112 hword）、193 个池字、23 处 padding，共 46 字节、自动名 0、raw 0；全模块为 20373 条指令、1446 个池字、307 个自动名、raw 0。资产导出 49/49，33554432 字节重建 ROM 与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`、SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`，ELF SHA256 `d7da270bdc6060caf9fe972a7b924d9916837ad55a9184a7f2d17d95e48bca17`。Root 最终门禁 SHA256 `ba097698fcaa858d9d72639455a4857f85d6b853429551ea01e2644c1e8af8c1`。历史 84 字节正引用补漏清单保持，未 stage/commit。

### 4.09 Seg-9 完成（2026-11-06）

范围 `[0x080bede4,0x080c00f0)` 共 4876 字节，10 个既有 Function、1849 条指令（1777 mnemonic + 72 hword）、240 个池字和 31 处原样填充（62 字节）。无 R4、carve、新建 Function 或 §5.1 登记。181 个源标签与 EOL、11 个目标标签、6 个稳定 ID Function 改名及 13 条 ASCII PLATE 完成落地，段内自动名和 raw 均为 0。

240 槽为 45 个 Equate 绑定、104 条新增 DATA、32 条既有 DATA 保留和 59 条 switch 保留。104 条新增引用精确进入 49 个目标；五个 source/target 重合地址只有一个批准后态。91 条旧 DATA 的 CORE6 与 source 保持，其中 DEFAULT 73 条、USER_DEFINED 18 条。完整 415 个实际 Function、10079 个地址状态及 198 个 primary 节点通过独立核验，192 个新 Label ID 只按批准地址与完整描述解析，6 个 Function 静态 ID 保持。全局 Equate 2455→2461，绑定 12551→12596。

六个函数更名为 `play_zone_card_display_transition`、`play_zone_info_palette_cycle_effect`、`play_life_point_change_effect`、`play_windowed_aob_slide_effect`、`play_correct_miss_result_effect` 和 `play_lp_timer_aob_effect`。13 条 PLATE 同时订正缓存计数、LP 进度字段、结果 OAM 的阶段与条件、半字进位公式及三个段外消费者，ABI、body、参数和已有类型保持。

真实 8G 只读演练完成全动作后态 0 FAIL，并在同一 Program 强制回滚后核完整前态 0 FAIL；物理 DB15 与 source186 均保持。最终独审通过后只执行一次持久保存，apply SHA256 `3fee137cd7774c7e403bc84ad5a10f3a7865429ebfb5f7a09caec8f60c87741f`。新进程保存后检查 SHA256 `60097685d9374319328e886248903a75b3ab741a12f489135b1fcd0195a44160`，独立 Java saved-DB 门禁 SHA256 `75ebe5e332f886c9ad4f4b000abb3edcff1a68630869015bbcbe6e20d71efe23`，均通过。

源码恰好变更 15 个批准路径，新增 15 个 GNU 定义，12 个现存 registry tuple 更新，BEDE4 缺席项保持；CSV 和规范清单只改 6 个 name cell，清单仍为 5414/5324/90/1。81 个 GAS 投影包含 61 个继承项与 20 个新增项，继承 BE108 的既有 `AOB_CARD_TILE_VRAM` 表达式。WORD/ELF、整份源码反投影和布局核验全部通过，无段外新增 word 投影或未批准源码变化。

资产导出 49/49，33554432 字节重建 ROM 与原件逐字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`。ELF SHA256 `721404dab10ea6d774ce433ad3c0a097f3927d3c5f85ab2c02554d41a2b3c047`，流水线收据 SHA256 `676ba9dbc8d2de929c3126271a173ae5731f350ec61bf6721c563ba02e83967f`，Root 最终门禁 SHA256 `9afef7510c67193ffd23b65e0aeae2e23672686fa1373d367ebd6adf6329ceed`。历史 84 字节正引用补漏及两条 CALL 状态保持，未 stage/commit。

### 4.10 Seg-10 完成（2026-11-06）

范围 `[0x080c00f0,0x080c1448)` 共 4952 字节。152 槽为 47 个 Equate 绑定、30 条新增 DATA、49 条既有 DATA 保留和 26 条纯保留；写入 126 个源标签与 EOL、7 个目标标签、18 条 ASCII PLATE，另保留 3 条 Function 上下文 PLATE。完成 11 个稳定 ID Function 改名、22 个 GNU 定义和 94 个有效 GAS 投影（81 个继承项与 13 个 source-only fallback）；152 条表达式断言由 139 条 native-exact 和 13 条 fallback 组成。无新建 Function、carve、R4 或 §5.1 登记。

Phase1 v1 的真实 8G 演练在后态出现 3 个 FAIL，原因仅为四条 `0201fec5` offcut rich reference 的派生显示名仍冻结为 `DAT_0201fec4+1`；该轮未保存，也没有形成回滚 PASS。v2 只为这四条完整 rich10 记录补入 `gBannerEffectArgs+1` 的精确派生名称投影，其他九个字段、owner、静态 ID 和全部动作保持。随后真实 full post 为 0 FAIL，同一 Program 强制回滚后的完整前态复查也为 0 FAIL，独立审计通过后才使用唯一授权保存一次。保存授权 SHA256 `fbc7f6caa696fc73100ed3c1d222363e5a8cae34b3c801e866de81dc4bc482ea`，apply SHA256 `60a8d089ac455eaef88a36c8ff51d0a3ab931e56cfa28310fe49a3e57f7e6ed4`，新进程检查 SHA256 `f3fe8a0a86fc97ed0b74c3058692f7fb62a519a39d2561b413bcb16b602ea209`，独立保存后快照 SHA256 `6655a7bc849a8f0a27c743f0a46cb4e847214ba46a32567e6ac9c938db138340`，saved-DB 门禁 SHA256 `9d230a416cd4d87c3849f4803f1c2c3c5f8c0e4d3eb0a9ebd716d6e679751856`。

独立保存后验覆盖 422 个实际 Function、10092 个主状态及 5 个 offcut 状态、144 个 primary 节点、2476 个全局 Equate 和 12643 条绑定。源码恰好变更 14 个批准路径，越界变化 0；18 个既有 registry tuple 更新，CSV 与 inventory 仅 11 个 name cell 改变。原生门禁 SHA256 `ccef16a42274f014a4c88294f4b2d92aa4a4859658ffbbecba4531bcdcdad53e`，源码同步 SHA256 `0992cd91ae473e2af7fcf26d222ad4dcbbc289a3e2c005f067dd34af277e4162`，流水线收据 SHA256 `ba0fcdda982089b6e12246ea1852ab141efbd75ff06b62fea256cff421618afe`。

段内最终为 2041 条指令（1879 mnemonic + 162 hword）、152 个池字和 26 处原样填充（52 字节），自动名 0、raw 0；全模块为 20373 条指令（19321 mnemonic + 1052 hword）、1446 个池字、自动名 0、raw 0。资产导出 49/49、构建及整份 33554432 字节 ROM 的 SequenceEqual 与 Root Python 全字节比较均通过；ROM SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`，SHA256 `f405c620da05a817a5d63f45a4707b914260fb5802fe519b1e31bf050ba8f524`，ELF SHA256 `cc2ed74397bc1e93d559df05f09a1252693cdaa477f8685025e09b7461fc7b09`。Root 最终门禁 SHA256 `6d20d4d9833cc7d6bf8f3eb9eaef9f371a62ecca9655fc3d43e10c9557421877`。历史 `[0x0804becc,0x0804bf20)` 84 字节正引用补漏及 04D374、B9E0A 两个 caller 保持，仍待主序 25 模块完成后闭合。未 stage/commit。

## 五、地址序路线图

| Seg | 半开范围 | 字节 | Function | 4B word | 自动槽/块头 | raw 块/字节 | 状态 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | `0x080b5348..0x080b6c08` | 6336 | 28 | 141 | 0/0 | 0/0 | ✅ root 全部验收 |
| 2 | `0x080b6c08..0x080b79f8` | 3568 | 19 | 87 | 0/0 | 0/0 | ✅ root 全部验收 |
| 3 | `0x080b79f8..0x080b8a24` | 4140 | 45 | 58 | 0/0 | 0/0 | ✅ root 全部验收 |
| 4 | `0x080b8a24..0x080babd4` | 8624 | 95 | 130 | 0/0 | 0/0 | ✅ root 全部验收 |
| 5 | `0x080babd4..0x080bb3dc` | 2056 | 12 | 50 | 0/0 | 0/0 | ✅ root 全部验收 |
| 6 | `0x080bb3dc..0x080bc71c` | 4928 | 12 | 160 | 0/0 | 0/0 | ✅ root 全部验收 |
| 7 | `0x080bc71c..0x080bda7c` | 4960 | 11 | 235 | 0/0 | 0/0 | ✅ root 全部验收 |
| 8 | `0x080bda7c..0x080bede4` | 4968 | 7 | 193 | 0/0 | 0/0 | ✅ root 全部验收 |
| 9 | `0x080bede4..0x080c00f0` | 4876 | 10 | 240 | 0/0 | 0/0 | ✅ root 全部验收 |
| 10 | `0x080c00f0..0x080c1448` | 4952 | 13 | 152 | 0/0 | 0/0 | ✅ root 全部验收 |

### 5.1 无有效引用的保留块

按各段的全 ROM 引用复核登记。
