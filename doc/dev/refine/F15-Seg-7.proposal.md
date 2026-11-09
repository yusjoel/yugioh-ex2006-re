# Refine Proposal: F15-Seg-7 [0x080bc71c..0x080bda7c)

## 段测绘

- 范围: `[0x080bc71c,0x080bda7c)`, 4960 字节.
- 当前布局: 1880 个 InstructionDB, 共 3950 字节（95 条 4B BL，其余 2B）; 235 个 4B word, 共 940 字节; 35 段零填充, 共 70 字节. 三类合计 4960 字节, 无空洞和重叠.
- ROM_INCBIN / `.byte` 块: 0. 本段无 raw block, 不产生 R4, carve 或 5.1 动作.
- Function: 11 个; 全部保持入口, Function ID, body AddressSet/SHA256, ABI, 参数, 返回, flags 和 typed code.

| 入口 | 当前名 | 最终名 | body 字节 | 动作 |
|---|---|---|---:|---|
| `0x080bc71c` | `tick_duel_field_ai_state_machine` | `tick_duel_field_ai_state_machine` | 94 | PLATE_REWRITE |
| `0x080bc794` | `init_field_slot_aob_ctx_a` | `init_banner_state` | 62 | FUNC_RENAME + PLATE_REWRITE |
| `0x080bc7e0` | `blend_palette_entry_toward_target` | `blend_palette_block_toward_white` | 154 | FUNC_RENAME + PLATE_REWRITE |
| `0x080bc880` | `play_demo_shuen` | `play_demo_shuen` | 106 | PLATE_REWRITE |
| `0x080bc918` | `play_ui_effect_3b` | `play_vija_scene_with_sprite_intro` | 532 | FUNC_RENAME + PLATE_REWRITE |
| `0x080bcbd4` | `play_ui_effect_3a` | `play_exodia_demo_scene_with_field_restore` | 106 | FUNC_RENAME + PLATE_REWRITE |
| `0x080bcc6c` | `dispatch_banner_anim_tick_by_state` | `dispatch_banner_anim_tick_by_state` | 906 | PLATE_REWRITE |
| `0x080bd0a8` | `dispatch_banner_scene_tick_by_state` | `dispatch_banner_scene_tick_by_state` | 682 | PLATE_REWRITE |
| `0x080bd3f4` | `tick_banner_display_state_machine` | `tick_banner_display_state_machine` | 484 | PLATE_REWRITE |
| `0x080bd660` | `tick_duel_puzzle_banner_state_machine` | `tick_duel_puzzle_banner_state_machine` | 402 | PLATE_REWRITE |
| `0x080bd870` | `play_ui_effect_30` | `play_three_sprite_banner_blend` | 422 | FUNC_RENAME + PLATE_REWRITE |

- 235 个 word 的完整合同见 `F15-Seg-7.slots.tsv`: `EQ_ADD=45`, `REF_ADD=62`, `REF_PRESERVE=63`, `PRESERVE=65`.
- 170 个 DEFAULT 自动源标签全部物化为 USER_DEFINED 语义标签并写 ASCII EOL. 63 条既有 DATA identity（21 DEFAULT/42 USER_DEFINED）完整保留 source/type/operand/primary，不重复添加或升级；65 个 switch word 的 Data, ANALYSIS namespace/Symbol, refs, Equate 和 EOL 精确保留.
- 权威前态 `root-f15-seg7-composite-independent-prestate-v3.json`: 412 个 Function 请求中 411 个存在（04BECC 保持 NULL）, 9795 个地址状态, 模块 1446 words/49408 bytes, 48B 外部保护窗口和 2438 个全局 Equate. source171 与正确 pre-Seg7 DB15 当前/备份保持精确.

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| none | raw=0 / thumb=0 | none | 段内全部 4960B 已由 typed instructions, 4B words 和零填充覆盖; source map 与 DB typed-unit 基线均无 raw block. |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 45 个标量源槽增加 operand-0 Equate. 16 个唯一名称中 8 个复用 GAS 和 Ghidra 现有对象, 8 个新增对象; 逐地址绑定见 slots TSV 和 `f15-seg7-global-equates-plan.json`.
- 新增名称: `DUEL_FIELD_UI_EFFECT_FLAGS_OFF`, `VIJA_INTRO_WIN0H_BOUNDS`, `BANNER_OAM_TILE_ATTR_3208`, `BANNER_OAM_TILE_ATTR_3210`, `BGR555_WHITE`, `DISPCNT_WIN0_CLEAR_MASK`, `VIJA_INTRO_OAM_PACKED_POS`, `VIJA_INTRO_AOB_PACKED_INIT`.
- 全局 Equate 从 2438 增至 2446; bindings 从 12465 增至 12510. `EQUIP_CHAIN_CANCEL_OFF` 复用既有对象；before/after 全 name/value/reference multiset 完整冻结.

### REF_SLOTS

- 62 个地址槽新增 USER DATA ref；63 个地址槽只改源 USER label/EOL并保持既有 DATA identity。48 个唯一目标的完整 before/after Symbol, Data, refs, comments 和 ID 合同见 `f15-seg7-target-plan.json`.
- `gEquipLpScoreBase`, `gP1LifePoints`, `gBannerState`, `gPrng`, WIN0/BLD registers, callback table 和 sin table 的静态 USER ID 原样保持.
- 8 个 switch table target 保持 ANALYSIS Symbol ID/namespace/Data; 每个新增一条源 USER DATA ref，slot/target 两份完整 after 完全相同。rich target name 使用原 qualified name `switchD_*::switchdataD_*`；native 源使用 8 个扁平 source-only GAS 投影.
- `gVijaIntroAobCtxA/B`, OBJ palette slots 3/4, Vija/banner VRAM, 20 个 ROM palette/tile/motion资源和 3 个现有 DEFAULT RAM/VRAM target 均按批准名称物化 USER label. 旧来向 CORE6 原样保持, 只更新派生 target-primary metadata.

### RENAME_SLOTS

- 纯 RENAME 槽为 0. 170 个自动源标签改名已并入 EQ_ADD/REF_ADD/REF_PRESERVE.
- 最终标签全部匹配 `^[a-z][a-z0-9_]+$`, 地址唯一且名称唯一.

### FUNC_RENAME

| 入口 | 旧名 | 新名 | 证据 |
|---|---|---|---|
| `0x080bc794` | `init_field_slot_aob_ctx_a` | `init_banner_state` | 清零并初始化 `gBannerState`，设置banner/field状态位；没有field-slot AOB写入或调用. |
| `0x080bc7e0` | `blend_palette_entry_toward_target` | `blend_palette_block_toward_white` | 16 色 BGR555 循环; 每分量按 r2 clamp16 向 31 递增; destination=`OBJ_PALRAM_BASE+(u16(r1)<<5)`. |
| `0x080bc918` | `play_ui_effect_3b` | `play_vija_scene_with_sprite_intro` | phases0..5 初始化 Vija sprite intro, phases6..11 执行 Vija scene/field restore/fade lifecycle. |
| `0x080bcbd4` | `play_ui_effect_3a` | `play_exodia_demo_scene_with_field_restore` | reset display -> Exodia demo tick -> duel-field restore -> fadeout 的完整共享出口闭合. |
| `0x080bd870` | `play_ui_effect_30` | `play_three_sprite_banner_blend` | 装载effect30 palette/tile，固定3个OAM的alpha ramp/hold/teardown；没有sin调用. |

- 五入口 whole-ROM 非对齐 even/Thumb+1 均为 0, 无 Function-pointer 或 `_1` alias 投影.
- 既有调用和新增 C794 两条incoming（01EF3E/01EF66）按 `f15-seg7-name-reference-baseline.json` 精确闭合。CSV为5个现有name cell；canonical inventory只改5个name，Function总数/named/auto/thunk保持 `5414/5324/90/1`.

### PLATE

- 11 个段内 Function +20 个必要外部消费者（新增 `dispatch_card_display_op@01EC9C`）, 共31条完整 PLATE 重写; 全部 ASCII, 每条 <=500 字符. C728仅现存registry注释投影，不写Ghidra PLATE.
- 外部作用域仅覆盖模块00/01/15/16/17/21 的真实调用者/被调者注释. Function body, ABI, signature, IDs 和非批准语义均不变.
- `tick_duel_field_ai_state_machine`: null callback 返回1; handler非零后清+8/+c并推进, gate字段非零返回1, 否则0. 该极性由 C71C 全部终端闭合.
- `blend_palette_block_toward_white`: 明确16色整块和向白色31的三分量 clamp, 不沿用旧单entry/任意target描述.
- 三个 scene rename 的 phase 范围, 资源, 状态推进, restore/teardown 和1/0返回均由实际 switch 分支与共享出口冻结.
- cleanup mask统一按指令事实：AND0xfe清banner bit0，AND0xfb清field+0x215 bit2，AND0xc0清frame-counter低6位并保留bits6/7；C918 phase5推进到6后立即清flags并返回0.
- CC6C只推进inner+0x11；cases0..8均返回1，inner>8直接0且无cleanup/outer写。D0A8/D3F4/D660各自的8/16/3-step计数、65/89/65次门槛、方向分流位置和phase8 inner委派逐项写入PLATE.
- 13BD4按bits16:9取state；13BD4/1CB00的返回1都要求最后blend check为0且对应flag bit0置位。1EF94 case2先做font/zone早退，0x31/0x32直接返回flag位；01EC9C所有handled路径统一常量1，invalid/default统一0，不转发callee返回.
- BDA7C/BDBB4 phase2精确32次（0..8递增ramp，9..16递减ramp，17..31只画两OAM）；其phase0初始化、1/3/4推进与清counter动作分开记录，cleanup仅越界分支.
- C1F10/C21A0每个适用phase均写明三对共6条OAM；phase6执行teardown并推进到7且本call仍返回1，>6仅返回0. BE600按phase写明12/6/12条OAM与8/64/8次计数；BDFAC phase3为8次OAM过渡并调用 `sync_state_and_init_sprite(8)`.
- DCFC phase>5以halfword banner+8、两个dword等值/零门槛控制byte[0x0201ff30] bit3，再清banner/field flags；宽度、绝对地址和AND/OR极性均保留.

## carve 计划 (R7)

none.

## disasm 计划 (R4)

none. 保持1880个 InstructionDB 地址, 3950B typed code, 235 words和70B padding的精确布局.

## 新增 constants / 全局

- `constants/ewram.inc`: `DUEL_FIELD_UI_EFFECT_FLAGS_OFF`, `gVijaIntroAobCtxA`, `gVijaIntroAobCtxB`; 0x1d30复用 `EQUIP_CHAIN_CANCEL_OFF`.
- `constants/gba_mem.inc`: `OBJ_PALRAM_SLOT_3`, `OBJ_PALRAM_SLOT_4`, `VIJA_INTRO_TILE_VRAM`, `BANNER_TILE_VRAM`.
- `constants/gba_io.inc`: `DISPCNT_WIN0_CLEAR_MASK`.
- `constants/oam_attr.inc`: `BANNER_OAM_TILE_ATTR_3208`, `BANNER_OAM_TILE_ATTR_3210`, `VIJA_INTRO_OAM_PACKED_POS`.
- `constants/duel_field.inc`: `VIJA_INTRO_WIN0H_BOUNDS`, `VIJA_INTRO_AOB_PACKED_INIT`, `BGR555_WHITE`.
- `constants/rom_data.inc`: 本段新命名的20个 ROM palette/tile/motion labels.
- `gDuelFieldState`, `OBJ_PALRAM_BASE`, `AOB_CARD_TILE_VRAM` 已有 GAS 定义; 本段只物化 Ghidra USER target, 不重复 GAS 定义.

## 5.1 登记 (Rule 3)

none.

## 消费者证据 (R6)

| 项目 | 消费者证据 | 结论 | 置信度 |
|---|---|---|---|
| AI callback dispatch | `asm/15_equip_target_summon_zoom.s:15934-15997` | C71C按state读取外表; null与handler返回的分支极性、state推进和gate字段全部闭合. | high |
| palette blend | `asm/15_equip_target_summon_zoom.s:16040-16130`; 16个真实incoming | C7E0处理16个BGR555颜色, 每分量向31推进, destination按palette block索引. | high |
| banner scene phase0 gate | `asm/15_equip_target_summon_zoom.s:17229-17287` (`080bd0f8-080bd15e`) | 置field+0x21e bit0并拷palette；`byte[02006c2c]&7`形成0x1800 stride，按`dword[0201e1e0]`零/非零选择gate-zero/gate-nonzero tile base后拷到`06014000`. | high |
| banner display phase0 gate | `asm/15_equip_target_summon_zoom.s:17651-17709` (`080bd444-080bd4aa`) | 同样置flag/拷palette/形成0x1800 stride，按`0201e1e0`零/非零选择该dispatcher的两组tile base并写`06014000`. | high |
| duel-puzzle banner resources/motion | `asm/15_equip_target_summon_zoom.s:17925-18057` (`080bd664-080bd770`) | 每次dispatch前以sin表和banner halfword计数生成坐标；phase0按region低3位形成0x1800 stride，拷palette至`05000260`、tile至`06014000`. | high |
| three-sprite banner phase0 | `asm/15_equip_target_summon_zoom.s:18219-18256` (`080bd8a8-080bd8f4`) | 置field flag、装载palette/tile并形成regional stride；`080bd8e0-080bd8e8`写BLDCNT=0x3f40。BLDALPHA分别在phase1 `080bd934`与phase3 `080bd9e8`写入；三次独立OAM追加保持. | high |
| Vija reset | `asm/00_system_str_vija.s:19364-19409` (`0801c2ac-0801c30c`) | load `gVijaState`后CpuSet清0xc0字节，写DISPCNT/BG0-2CNT，调用GL/IG2D reset，返回1. | high |
| Vija resource gate | `asm/00_system_str_vija.s:19672-19701` (`0801c50c-0801c540`) | load/compare ROM region与settings low3 bits，经条件branch选择variant，再调用`load_vija_obj_resource_by_region`. | high |
| Vija scene runner | `asm/01_vija_scene_text.s:5-75` (`0801cb00-0801cb98`) | load `gVijaState+0x8d`、compare/branch十case，phase0加载regional资源并写scene state；后续case执行OBJ/BG/blend ticks. | high |
| duel-field restore | `asm/17_duelfield_pack_frame.s:1373-1425` (`080cc904-080cc978`) | 清/重建VRAM与display state，写DISPCNT/BG控制并拷field tile资源；是Vija/Exodia恢复阶段的真实host. | high |
| duel-field fade | `asm/17_duelfield_pack_frame.s:1515-1532` (`080cca38-080cca58`) | load field+0x215、OR bit1并store，随后调用`tick_blend_step_by_delta(2)`；是Vija/Exodia fade host. | high |
| Exodia scene | `asm/15_equip_target_summon_zoom.s:16556-16634`; `asm/00_system_str_vija.s` demo callees | reset, demo tick, field restore, fadeout顺序与最终blend/flag返回闭合. | high |
| dispatcher returns | `asm/01_vija_scene_text.s:4520-5142` (`[0801ec9c,0801ef94)`, `0801ef94-0801f238`) | card-display dispatcher只有handled常量1与invalid常量0出口；UI dispatcher保留case2早退、31/32 inline位返回及30/3a/3b/3c当前handler. | high |

## 完整元数据和作用域合同

- 源槽 before/after rich state 在 `f15-seg7-slot-plan.json`; target图在 `f15-seg7-target-plan.json`; 31个 Function 全属性在 `f15-seg7-function-plan.json`.
- 所有 reference 均保留 from/to/type/source/operand/primary CORE6；仅62个全新identity追加记录，63个既有identity保持原source。旧DEFAULT target物化时只有派生 target-primary ID/name/type/source按最终Symbol图变化；8个ANALYSIS目标始终保留namespace/ID/source.
- 19个继承 GAS projection 原样保持, 追加8个switch和13个PALRAM/VRAM source-only投影, 共40项. 后13项由native exporter的02-04/08-09地址白名单限制触发；DB动作不变，exporter不改.
- module05 `[0x0804becc,0x0804bf20)` 84B正引用backlog保持无Function/无Instruction状态, 本段不回头处理.
- 正式潜在落地只允许 `f15-seg7-source-scope-plan.json` 白名单；C728只改现存registry注释。历史eval/proposal/closure检索命中与两份legacy inventory snapshots全部只读.

## 自检

- 235 source words 的地址/字节/值与原ROM及initial baseline逐项一致; 170 auto +65 preserved精确覆盖.
- 动作计数 `45+62+63+65=235`; 170个新源标签正则/唯一性通过; 170条EOL全ASCII.
- 31条最终PLATE全ASCII且<=500; 5个新Function名全库无碰撞; 五入口whole-ROM even/Thumb+1 holder均为0.
- 全局Equate before2438/after2446及完整12510 bindings multiset冻结; 40个GAS投影覆盖19继承+8个switch+13个PALRAM/VRAM表达式.
- source171当前/副本与correct pre-Seg7 DB15备份经Root gates保持; 两次readonly DB15 before/after相同.
- 无Ghidra写入, 无正式ASM/constants/registry/CSV/progress修改, 无build/stage/commit.

## 求助

none.

## Executor Report: F15-Seg-7

- 槽: EQ=45 REF_ADD=62 REF_PRESERVE=63 PRESERVE=65 FUNC_RENAME=5 PLATE=31.
- carve=0 disasm=0 range 5.1=0.
- 新增 constants/全局: 8个Ghidra Equate对象, 2个RAM label, 4个PALRAM/VRAM label, 20个ROM资源/表label; 复用项按现有GAS/Ghidra双域合同冻结.
- 求助: none.
- proposal: `doc/dev/refine/F15-Seg-7.proposal.md`.
