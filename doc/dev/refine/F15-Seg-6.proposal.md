# Refine Proposal: F15-Seg-6 [0x080bb3dc..0x080bc71c)

## 段测绘

- 范围: `[0x080bb3dc,0x080bc71c)`, 4928 字节.
- 当前布局: 1982 个 InstructionDB, 共 4210 字节; 160 个 4B word, 共 640 字节; 39 段零填充, 共 78 字节. 三类合计 4928 字节, 无空洞和重叠.
- 段内 ROM_INCBIN / `.byte` 块: 0. 消费者闭包另发现一个必须随本段处理的段外正引用回调表 `[0x09e5ab5c,0x09e5ab84)`, 见下表和 carve 计划.
- 当前 Function: 12 个, 全部保留入口, Function ID, body AddressSet, body SHA256, 签名和所有标志.

| 入口 | 当前名 | body 字节 | 处理 |
|---|---|---:|---|
| `0x080bb3dc` | `check_normal_summon_eligible_for_any_effect_zone` | 52 | PLATE_REWRITE |
| `0x080bb414` | `dispatch_equip_activation_full_sequence` | 1242 | PLATE_REWRITE |
| `0x080bb9b8` | `eval_field_spell_equip_activation_candidate` | 500 | PLATE_REWRITE |
| `0x080bbbf8` | `check_field_spell_icid_summon_restriction` | 420 | PLATE_REWRITE |
| `0x080bbde8` | `execute_field_spell_equip_placement` | 308 | PLATE_REWRITE |
| `0x080bbf38` | `check_field_spell_equip_placement_eligible` | 462 | PLATE_REWRITE |
| `0x080bc168` | `dispatch_equip_activation_by_field_state` | 446 | PLATE_REWRITE |
| `0x080bc388` | `try_execute_toon_world_equip_placement` | 126 | PRESERVE PLATE |
| `0x080bc418` | `eval_equip_slot_target_eligibility_full` | 272 | PLATE_REWRITE |
| `0x080bc54c` | `run_equip_activation_state_machine_p1` | 114 | PRESERVE PLATE |
| `0x080bc5d4` | `run_equip_activation_state_machine_p2` | 98 | PRESERVE PLATE |
| `0x080bc648` | `dispatch_equip_activation_phase_by_state` | 170 | PLATE_REWRITE |

- 160 个 word 的完整前态和后态合同见 `doc/dev/refine/F15-Seg-6.slots.tsv`. 其中 155 个是 DEFAULT 自动源标签, 其余 5 个是 Ghidra switch table word.
- 动作由 TSV 派生: `EQ_ADD=97`, `REF_ADD=42`, `REF_PRESERVE=21`. 155 个自动源标签全部改为 USER_DEFINED 语义标签并写 ASCII EOL. 五个 switch word 不增加同址别名或 EOL.
- 只读 DB 闭包: `root-f15-seg6-supplement-prestate.json`, 94 个真实 Function, 160 个源 word, 436 个地址状态, 17 个 target, 全段 4928 个字节状态. 15 个数据库文件查询前后哈希一致.
- 完整上下文前态: `root-f15-seg6-composite-independent-prestate-v4.json`, 396 个请求 Function 中 395 个存在, 9769 个地址状态, 模块 1446 个 word, 49408 个逐字节 unit, 48B 外表保护窗口和 2429 个全局 Equate. v4 在 v3 上新增 `0x080bb2d5` 完整 odd 前态；其余状态逐字段一致，并继续覆盖外表末两项及 `0x09e5ab84` 右 bookend.

## 数据块分类 (Rule 2/3)

| 块 | ref-scan | 判定 | 理由 |
|---|---|---|---|
| none | raw=0, thumb=0 | none | 本段源码和 typed-unit 基线均无 ROM_INCBIN 或 `.byte`; 4928 字节已由 InstructionDB, word 和零填充精确覆盖. |
| `0x09e5ab5c..0x09e5ab84`, 40B, 段外 `asm/rom.s:2067` | 表基址 raw=1 (`0x080bc784`); 9 个 THUMB+1 词全部是真回调, 偶入口 raw=0 | carve | `tick_duel_field_ai_state_machine` 在 `0x080bc740` 取表基址, `0x080bc748` 读取 `state_id*4` 回调, `0x080bc74a` 检查零. 9 个非零回调后 `0x09e5ab80` 的零词是 state 9 终止项. |

- 本段 `carve=1` 个 40B 外表, `disasm=0`, `5.1=0`.
- 12 个现有 Function 和外表 state 0 的既有 Function 已执行全 ROM 非对齐 raw 和 THUMB-or-1 扫描, 结果保存于 `f15-seg6-function-pointer-holds.json`. 9 个回调词是全部真实 THUMB holder; 各偶入口 raw holder 均为 0. 本段不改 Function 名称, 不在奇地址创建 Symbol, Data 或 ref.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 97 个标量源槽全部增加 operand 0 Equate, 完整地址逐项见 slots TSV.
- 共 59 个唯一常量名. 95 个绑定复用现有 GAS 定义和现有 Ghidra 全局 Equate; 2 个绑定新增 GAS 和 Ghidra Equate.
- 高频复用组: `PLAYER_BLOCK_STRIDE` 17 处, `P1LP_BLOCK2_OFF_1CE8` 6 处, `LP_PLAYER_SIDE_CACHE_OFF` 6 处, `ACTIVATION_ENTRY_CLR_BITS_14_6` 4 处, `EFFECT_ID_GENERIC_WILDCARD` 3 处.
- 卡 CID 复用 `constants/card_info.inc` 的现有定义. 每个值按实际消费者域选择名称, 未按同值跨域复用.
- `0x00001cf4` 的消费者基址是 `gP1LifePoints`, 因此使用 `P2LP_BLOCK2_OFF_1CF4`, 不使用以 `gDuelFieldSlots` 为基址的 `FIELD_STATE_OFF`.

新增项:

| 值 | 名称 | 文件 | 证据 |
|---|---|---|---|
| `0x0000049c` | `FIELD_COPY_GUARD_CID_049C` | `constants/card_info.inc` | `asm/15_equip_target_summon_zoom.s:14304-14307` 把该值传给 `count_field_copies_of_card`; 名称只冻结 card-id 参数域, 不绑定卡名. Confidence high. |
| `0x0000138f` | `SEBEKS_BLESSING_CID` | `constants/card_info.inc` | `data/card-stats.s:10467,37959` 和 `data/cards-ids-array.s:1017` 共同确认 Sebek's Blessing, slot `0x138f`. `asm/15_equip_target_summon_zoom.s:14349-14358` 消费. Confidence high. |

### REF_SLOTS

42 个原来无 DATA ref 的地址槽增加 USER DATA ref. 目标和数量如下:

| 目标 | 源槽数 | 合同 |
|---|---:|---|
| `effect_zone_response_table` `0x09e48918` | 2 | 保留 USER target ID 和表类型, 仅追加 ref. |
| `field_spell_activation_response_table` `0x09e48f90` | 1 | 保留 USER target ID 和表类型, 仅追加 ref. |
| `gEquipLpScoreBase` `0x0201afe0` | 20 | 保留 USER target ID, refs 和 Data. |
| `gP1ZoneHandCount` `0x0201c4ec` | 3 | 保留 USER target ID, refs 和 Data. |
| `gDuelFieldSlots` `0x0201c510` | 6 | 保留 USER target ID, refs 和 Data. |
| `gP1FieldArrayCBase` `0x0201c600` | 4 | 保留 USER target ID, refs 和 Data. |
| `gP1SlotSetCodeArray` `0x0201c740` | 1 | 保留 USER target ID, refs 和 Data. |
| `gP1HandSlotArray` `0x0201c8f8` | 1 | 保留 USER target ID, refs 和 Data. |
| `gEquipActivationStateA` `0x0201e228` | 1 | 将动态 DEFAULT RAM 标签物化为 USER_DEFINED; 保留 13 条旧来向 CORE6, 仅派生 target-primary 字段换名和换合法新 ID. |
| `gEquipActivationReadyFlag` `0x0201e238` | 2 | 将动态 DEFAULT RAM 标签物化为 USER_DEFINED; 保留 18 条旧来向 CORE6, 仅派生 target-primary 字段换名和换合法新 ID. |
| `switchdataD_080bc19c` `0x080bc19c` | 1 | 目标 ANALYSIS symbol ID 7270 和 namespace ID 7262 保持, 新增源 `0x080bc198` 的 USER DATA ref. GAS 表达式使用现有 `switchD_080bc18a__switchdataD_080bc19c`. |

16 个既有 `/pointer` 源槽保持原 DEFAULT DATA ref 的 type, source, operand 和 primary 位, 只将源槽 DEFAULT 标签改为 USER_DEFINED 并写 EOL. 静态 target ID 全部保持.

### 段外回调表 source-word 合同

- `0x09e5ab5c..0x09e5ab7c` 共 9 个 THUMB 回调词增加 operand 0 Function+1 Equate; 7 个唯一 Equate 对象, 9 个绑定.
- `0x09e5ab5c..0x09e5ab74` 的 7 条旧 DEFAULT DATA ref 原样保持, 包括 odd target label ID, source, operand 和 primary. 不把它们改指偶入口, 不升级 ref source.
- `0x09e5ab78` 保留原 `/undefined4`, DEFAULT `DAT_09e5ab78` 的合法动态 ID 可随 USER source label 物化变化; 新增到偶 Function `0x080bc5d4` 的 USER DATA ref.
- `0x09e5ab7c` 原为 implicit Data/no Symbol/no ref; 创建 `/dword`, USER source label 和到偶 Function `0x080bb9b8` 的 USER DATA ref. 不创建 pointer Data, 避免 Ghidra 自动生成未批准的 odd ref.
- `0x09e5ab80` 原为 implicit zero word; 创建 `/undefined4` 和 `duel_field_ai_state_callback_table_end`, 不加 Equate/ref.
- 所有 9 个 odd target 地址的现有 TMode, DEFAULT alias, incoming ref, Function containment 和缺失/存在的 Symbol 状态逐项保持. 奇地址不创建 Symbol, Data 或 ref.
- `0x080bc784` 属 Seg-7, Ghidra `/undefined4`, DEFAULT source label, PC READ, refs_from 空集, Equate 空集和 EOL 全部不变, 不新增 Ghidra DATA ref. USER table-base label 会使 exporter 将 native 表达式从 numeric `0x09e5ab5c` 投影为 `duel_field_ai_state_callback_table`; 只批准这一处 source-only GAS 投影并登记为第 18 个 sticky pin.

### RENAME_SLOTS

- 单独纯改名槽为 0.
- 155 个自动源标签的改名已并入各自 EQ_ADD, REF_ADD 或 REF_PRESERVE 动作.
- 新标签全部满足 `^[a-z][a-z0-9_]+$`.

### switch table 保留合同

| 源地址 | 原值 | Data | 原源符号 | DATA target |
|---|---|---|---|---|
| `0x080bc19c` | `0x080bc1b0` | `/undefined *` | `switchdataD_080bc19c`, ID 7270, namespace `switchD_080bc18a` | `caseD_0`, ID 7264 |
| `0x080bc1a0` | `0x080bc298` | `/undefined *` | none | `caseD_1`, ID 7265 |
| `0x080bc1a4` | `0x080bc2bc` | `/undefined *` | none | `caseD_2`, ID 7266 |
| `0x080bc1a8` | `0x080bc2d4` | `/undefined *` | none | `caseD_3`, ID 7267 |
| `0x080bc1ac` | `0x080bc2f8` | `/undefined *` | none | `caseD_4`, ID 7268 |

五项保持原 Data 类型, ANALYSIS namespace, Symbol ID, target ID 和 DEFAULT DATA ref CORE6. 不创建 USER case alias, 不改变 switch Function body.

### FUNC_RENAME

- 0. 12 个名称与实际输入, 控制流, 共享返回和写入对象一致.
- 无 Function rename；CSV/inventory 名称与计数不变。registry 实际8个旧tuple中7个仅更新PLATE、C388完整保留；C418/C54C/C5D4/C648四个tuple实际缺席并保持缺席。

### PLATE

- 12 个 Function 均在 `F15-Seg-6.plates.tsv` 冻结完整前态和完整最终文本.
- 重写 9 个, 保留 3 个. 12 个最终文本均为 ASCII 且不超过 500 字符.
- `run_equip_activation_state_machine_p1` 和 `_p2` 保留 Seg-5 已验收的 mode 0/1, FieldState 和 cache 条件全文, 不回退旧描述.
- `dispatch_equip_activation_full_sequence` 的旧 1338 字符非 ASCII 文本替换为 403 字符 ASCII, 按真实顺序冻结207行扫描、wildcard、Skill Drain、slot0..4提交和1/0返回.
- `check_field_spell_icid_summon_restriction` 的旧 699 字符非 ASCII 文本替换为 397 字符 ASCII, 明确 low-13-bit CID, direct true, Morphing Jar, whitelist 和 node-count 分支极性.
- `dispatch_equip_activation_phase_by_state` 明确 phase0到3的终止值；phase2严格区分advance=0保持2/返回0、advance!=0且cancel返回1、advance!=0且无cancel推进3/返回0.

## carve 计划 (R7)

`asm/rom.s:2067` 当前单条 host:

```asm
.incbin "roms/2343.gba", 0x1E5AB5A, 0xA2
```

按原边界精确拆为:

```asm
.incbin "roms/2343.gba", 0x1E5AB5A, 0x2
duel_field_ai_state_callback_table:
    .word dispatch_equip_activation_ai_by_phase+1
    .word dispatch_equip_activation_by_field_state+1
    .word run_equip_activation_state_machine_p1+1
    .word dispatch_equip_activation_phase_by_state+1
    .word try_execute_toon_world_equip_placement+1
    .word run_equip_activation_state_machine_p1+1
    .word dispatch_equip_activation_phase_by_state+1
    .word run_equip_activation_state_machine_p2+1
    .word eval_field_spell_equip_activation_candidate+1
duel_field_ai_state_callback_table_end:
    .word 0
.incbin "roms/2343.gba", 0x1E5AB84, 0x78
```

- 结构化范围 `[0x09e5ab5c,0x09e5ab84)` 为 40B, SHA256 `f862148805f56f8bd9ae84e53780d2ccddaffca2c2dff49f436fd5bfcf7370dd`.
- 前缀 `[0x09e5ab5a,0x09e5ab5c)` 两个零字节和后缀 `[0x09e5ab84,0x09e5abfc)` 120B 原样保留. 左侧 `0x09e5ab58` 的 `SANGAN_CID` halfword 保持; 右侧 `0x09e5ab84` 的 `/dword`, DEFAULT `DWORD_09e5ab84` ID 4611686018593434500, 两条 ANALYSIS 来向和字节 `85610c08` 全部保持.
- 详细 before/after Data, Symbol, refs, Equate, EOL, odd target 和消费 Function 合同见 `f15-seg6-external-ai-state-table-plan.json`.

## disasm 计划 (R4)

none. 保持 1982 个 InstructionDB 地址, 4210 字节指令, 160 个 word 和 39 段零填充的精确布局.

## 新增 constants / 全局

新增 GAS:

```asm
.equ FIELD_COPY_GUARD_CID_049C, 0x0000049c
.equ SEBEKS_BLESSING_CID,       0x0000138f
.equ gEquipActivationStateA,    gP1LifePoints + ACTIVATION_STATE_A_OFF
.equ gEquipActivationReadyFlag, gP1FieldArrayCBase + EQUIP_ACTIVATION_READY_FLAG_OFF
```

- 前两项写入 `constants/card_info.inc`; 后两项写入 `constants/ewram.inc`.
- Ghidra 全局 Equate 从 2429 个增至 2438 个. 标量池新增 2 个对象和 97 条绑定; 外部回调表新增 7 个 Function+1 对象和 9 条绑定; 合计 106 条新绑定. 其余 57 个标量名称复用现有对象.
- 两个 RAM label 的旧 DEFAULT 动态 ID 可合法变化; 其 Data `/undefined4` 和所有旧 refs CORE6 不变.
- `f15-seg6-global-equates-plan.json` 冻结 2429 个 before 对象和 2438 个 after 对象的完整 name/value/reference multiset.

## 5.1 登记 (Rule 3)

none.

## 消费者证据 (R6)

| 项目 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| effect-zone 表 | `asm/15_equip_target_summon_zoom.s:13348-13379`, `13380-13437` | 207 行表, stride 8, 经 `check_normal_summon_eligible_for_slot` 或 `try_activate_equip_for_matching_slot` 消费. | high |
| field-spell 表 | `asm/15_equip_target_summon_zoom.s:14145-14337` | phase 0 扫描 70 行; 成功返回 0, exhaustion 进入 phase 1. | high |
| `gEquipActivationStateA` | `asm/15_equip_target_summon_zoom.s:15120-15132`; `root-f15-seg6-supplement-prestate.json` 的 13 条来向 | 写入 `((word>>22)&0xff)*2 | ((word>>13)&1)`, 并被 rank-state 和 sprite/display 路径读取. | high |
| `gEquipActivationReadyFlag` | `asm/15_equip_target_summon_zoom.s:13956-13960,14046-14050`; supplement 的 18 条来向 | 多条激活和显示状态路径写入 ready/count 状态; 复用 Seg-5 的 `EQUIP_ACTIVATION_READY_FLAG_OFF`. | high |
| activation entry mask | `asm/15_equip_target_summon_zoom.s:13917,14044,14142,14689` | 所有消费者对 activation entry halfword 清 bits 14..6, 复用 `ACTIVATION_ENTRY_CLR_BITS_14_6`. | high |
| `0x049c` | `asm/15_equip_target_summon_zoom.s:14304-14307` | 直接作为 `count_field_copies_of_card` 参数; 只命名参数域, 不绑定卡名. | high |
| Sebek's Blessing | `asm/15_equip_target_summon_zoom.s:14349-14358`; `data/card-stats.s:10467,37959` | `0x138f` 是 Sebek's Blessing internal CID. | high |
| phase dispatcher | `asm/15_equip_target_summon_zoom.s:15822-15928` | phase 0/1/2/3 的返回值, 状态推进, cancel 读取和 OAM 值均由终端指令闭合. | high |
| AI state callback table | `asm/15_equip_target_summon_zoom.s:15934-15997`; `asm/rom.s:2067` | `BC740/BC748` 以 state_id*4 读取 `09e5ab5c`; 9 个非零回调后 `AB80` 零项在 state 9 触发 `BC74C -> BC78C` 终止. | high |

## 完整元数据和作用域合同

- 源槽 before/after rich state 见 `f15-seg6-slot-plan.json`. Data type, bytes, TMode, PC READ CORE6, refs_from, refs_to, Equate 和 EOL 均逐项冻结.
- 11 个 REF_ADD target 的完整 before/after 见 `f15-seg6-target-plan.json`. 9 个静态 target ID 保持; 2 个动态 RAM target 按批准物化.
- 两个 RAM label 影响的 19 个段外 owner Function 见 `f15-seg6-external-target-projection.json`. Function 全属性, body, PLATE, EOL 和 incoming 不变; 只更新 body reference 的派生 target-primary 字段.
- 12 个段内 Function 的完整 before/after 见 `f15-seg6-function-plan.json`. body 与全部旧 incoming CORE6 保持；只新增批准的 `09e5ab7c -> 080bb9b8` 和 `09e5ab78 -> 080bc5d4` 两条 USER DATA incoming.
- 17 个历史 native GAS 投影按 `f15-seg6-sticky-gas-projections.json` 原样保留.
- `0x080bc784` 新增且只新增 source-only `duel_field_ai_state_callback_table` 表达式投影; 合同文件把原 17 项和该第 18 项一起冻结. Ghidra 词状态不变.
- 模块 05 `[0x0804becc,0x0804bf20)` 的 84 字节正引用补漏保持 Function 缺席和原字节状态, 本段不回头处理.
- 外表 consumer `tick_duel_field_ai_state_machine@080bc71c` 的 Function 全属性, body, PLATE, EOL, incoming 和现有 CORE6 保持; 仅 `BC740/BC748` 指向新 USER source label 的 derived target-primary 字段按批准 Symbol 图更新. `BC748 -> BC5D5` 的既有 odd PARAM ref 原样保持.
- 正式潜在落地范围只包含模块15当前asm、`asm/rom.s`、`constants/card_info.inc`、`constants/ewram.inc`、`tools/ghidra-labeling/RenameKnownFunctions.py`、三份本段文档和既有规范Function inventory文件。registry仅七个既有tuple的PLATE字段更新；CSV/inventory名称与四个缺席tuple均不变.

## 自检

- ROM 160 个源 word 的 `old_bytes` 与源码注解和原 ROM 全部一致.
- 160 个地址唯一; 155 个新源标签正则通过; 155 条新 EOL 全 ASCII.
- 12 个最终 PLATE 全 ASCII 且均不超过 500 字符.
- 5 个 switch word 的类型, namespace, Symbol ID 和 ref 合同逐项一致.
- 外表 9 个 callback 词和 1 个零终止词 ROM bytes 精确; 前 7 条 odd DEFAULT refs 原样保持, 后 2 条只增加偶 Function USER refs; 所有 odd target 状态不变.
- 外表原 host 的 2B 前缀和 120B 后缀逐字节保留; 结构化 40B SHA256 已核对.
- source baseline 166 文件和 pre-Seg-6 DB15 备份未修改; readonly 查询 DB15 before/after 完全一致.
- 无 Ghidra 写入, 无正式源码改动, 无 build, stage 或 commit.

## 求助

none.

## Executor Report: F15-Seg-6

- 段内槽: EQ=97 REF_ADD=42 REF_PRESERVE=21 RENAME=0 FUNC_RENAME=0 PLATE_REWRITE=9 PLATE_PRESERVE=3.
- 段外回调表: carve=1, callback Equate bindings=9, source labels=10, preserved odd refs=7, new even Function refs=2, native table-base projection=1.
- disasm=0 range, 5.1=0.
- 新增 constants/全局: `FIELD_COPY_GUARD_CID_049C`, `SEBEKS_BLESSING_CID`, `gEquipActivationStateA`, `gEquipActivationReadyFlag`, 7 个 Function+1 Ghidra Equate 对象, `duel_field_ai_state_callback_table`.
- 求助: none.
- proposal: `doc/dev/refine/F15-Seg-6.proposal.md`.

## Mode A round-1 corrections (authoritative)

- All formal collection fields and typed after-state collections use `[]`, `[row]`, or `[row,...]`; scalar primary/EOL/PLATE fields remain scalar. Equate getters are distinct: `equates=[{name,value}]`, while `equate_references=[{name,value,operand}]`.
- BC19C retains static Symbol ID7270, ANALYSIS source, namespace7262 and qualified name `switchD_080bc18a::switchdataD_080bc19c`; its incoming set is old BC188 DATA + BC184 PARAM + new BC198 USER DATA. External table DATA incoming is added only to B9B8 Function3443 and C5D4 Function7274.
- All nine callback odd targets are preserved. State0 freezes B2D5 DEFAULT Label ID4611686018562372309/TMode1/unique AB5C incoming. No odd Symbol/Data/ref is created. The approved graph freezes 44 new DATA edges; only explicit DYNAMIC IDs resolve later.
- Registry: seven existing tuples receive PLATE-only updates, C388 remains exact, and four missing tuples C418/C54C/C5D4/C648 remain absent. CSV/inventory names and counts stay unchanged.

### Corrected semantic contracts

1. B3DC scans indices0..0xce inclusive (207 rows) and returns1 on the first accepted row, else0.
2. B414 executes in this order: scan207 rows; after a miss, each wildcard D/E/C path that actually calls its handler returns1 without testing the handler result; if none dispatches, nonzero Skill Drain count returns0; otherwise scan slots0..4. A matching type9/5/8 path caches player by STR32 at0x0201e244, writes1 by STR32 at0x0201e238, initializes target refs and returns1. Slot exhaustion returns0.
3. B9B8 phase0 scans70 rows: hit returns0; exhaustion increments phase and enters phase1. Phase1 requires capacity>1, no-field-node nonzero, unavailable nonzero, and at most one of slots5..10 with nonzero low13 CID, halfword+8 zero and word+0x10 bit20 set. Each candidate must pass field5==0, LP threshold nonzero, placement-available nonzero and field-spell-B-placeable==0. Then primary requires owner==player and (field6!=0x16 or field9==5 or 049C count nonzero); 131E/10DD force primary1 and 138F forces0 but never bypasses the four early gates. Without primary, use the last post-gate index only when index>=0, active count0 and zones>4; this can bypass primary failure including 138F. Commit refs(player,11,index,7), STR32 player to0201e244, STR32 1 to0201e238, return0. Phase1 failure and every phase other than0/1 return1.
4. BDE8 distinguishes input/effective mode; strict failure forces mode1. Candidate-1 returns-1; same-player restriction initializes then0. field7 nonzero writes twice/spends two budget units. LP+1d48 comes from selected bits22..29+bit13; rank tests effective-mode0, clears +180, returns1.
5. BF38 stores `(((word>>22)&0xff)*2)|((word>>13)&1)` and keeps strict/count/bit0x10/CID/two-cache/rank/return gates.
6. C168 state0 clears scoreBase+180; LP+1cec==0 returns1. Otherwise bit17 at LP+side*868+11c set, Chain Energy LP check0, both strict/group checks0, or count_available_effect_zones(1-player,0x1102,-1)>0 advances1/returns0. If gates pass, placement-eligible nonzero keeps state0/0; otherwise strict then resolve/cache/best/fallback selection runs, no target or execute result nonzero advances1/0, execute0 keeps0/0. State1 first signed score compare<0 clears+c/advances2/0; only otherwise compute cache, zero also advances2/0, nonzero=>1. State2 calls dispatch_equip_activation_full_sequence; state3 calls scan_all_effect_zone_entries_for_equip_activation; nonzero resets0, zero advances, both return0. State4 requires Chain Energy LP nonzero, bit17 clear, and strict or group nonzero; failure advances5/0. Then index<0 or output score nonzero=>1; execute0 keeps4/0, positive resets1/0, negative=>1. Other states=>1.
7. C418 tests slot+8. result0/+8zero requires Last Warrior; only field8==6 adds Neo-Daedalus+Toon World, then init returns1 without sprite. result0/+8nonzero requires +6nonzero and Level Limit B absent or signed score<=3. result1 requires +6zero, Final Attack Orders absent, Level Limit A absent or score>3. Last two accepts call sprite/return1; reject0.
8. C648 phase0 precondition failure or chain-blocked plus monster-score0 returns1; otherwise two-table nonzero returns0 without advance, while zero clears step/active and advances. Phase1 submits LP row3, advances and returns0. Phase2 advance0 does not read cancel, stays2 and returns0; advance nonzero plus cancel nonzero stays2/returns1; advance nonzero plus cancel0 advances3/returns0. Phase3 selects attr0x10/0x8010 by player and returns1. Other phases return0.

