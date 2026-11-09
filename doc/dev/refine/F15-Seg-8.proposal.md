# Refine Proposal: F15-Seg-8 [0x080bda7c..0x080bede4)

## 段测绘

- 范围: `[0x080bda7c,0x080bede4)`, 4968 字节.
- 当前布局: 1984 个 InstructionDB, 共 4150 字节; 193 个 4B word, 共 772 字节; 23 段零填充, 共 46 字节. 三类合计 4968 字节, 无空洞和重叠.
- ROM_INCBIN / `.byte` 块: 0. 本段不产生 R4, carve 或 5.1 动作.
- 193 个 word 完整动作: `EQ_ADD=41`, `REF_ADD=79`, `REF_PRESERVE=45`, `PRESERVE=28`; 165 个 DEFAULT 自动源标签全部覆盖.
- 权威 before: `root-f15-seg8-composite-independent-prestate-v1.json` (413 requests/412 actual Functions, 9796 slots, module 1446 words/49408 bytes, 324 target states, 2446 global Equates). slots+words+targets.exact 无损并集为10069个唯一地址状态, 全部纳入 `f15-seg8-fullstate-observation-plan.json` 的 before/after/rollback 观察合同. source176 和正确 post-Seg7 DB15 备份保持不变.

| 入口 | 当前名 | 最终名 | body 字节 | 动作 |
|---|---|---|---:|---|
| `0x080bda7c` | `tick_pack_banner_state_machine_a` | `tick_pack_banner_state_machine_a` | 234 | PRESERVE |
| `0x080bdbb4` | `tick_pack_banner_state_machine_b` | `tick_pack_banner_state_machine_b` | 246 | PRESERVE |
| `0x080bdcfc` | `play_ui_effect_04` | `play_ui_effect_04` | 532 | PRESERVE |
| `0x080bdfac` | `banner_anim_state_machine` | `banner_anim_state_machine` | 1416 | PRESERVE |
| `0x080be600` | `tick_banner_pack_state_machine` | `tick_banner_pack_state_machine` | 836 | PRESERVE |
| `0x080be9bc` | `load_pack_aob_gfx_by_mode` | `load_pack_aob_gfx_by_mode` | 142 | REWRITE |
| `0x080bea94` | `play_ui_effect_15` | `play_zone_type_13_card_reveal_effect` | 744 | RENAME_REWRITE |

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| none | raw=0 / thumb=0 | none | 全段由 typed instructions, 4B words 和零填充连续覆盖; 无 raw block. |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 41 个源槽增加 operand-0 Equate; 9 个新对象, 其余复用现有对象. 新对象: `WINOUT_OUTSIDE_ALL_OBJWIN_NO_EFFECTS`, `DISPCNT_WINDOWS_CLEAR_MASK`, `DISPCNT_WIN1_OBJWIN_CLEAR_MASK`, `LARGE_CARD_DISPLAY_ZONE13_MODE_BASE`, `OAM_ATTR2_TILE_C0_PAL4`, `OAM_ATTR2_TILE_48_PAL4_PRI2`, `OAM_ATTR2_TILE_C0_PAL4_PRI2`, `AOB_MODE_TILE_BASE_512_PAL5`, `SLOT_SET_CODE_TO_COUNT_NEG_OFF`.
- `0x02000005` 是传给 `init_aob_ctx_from_ptnsect` 的 packed scalar: high16=`OBJ tile base=512`, low4=`OBJ palette bank=5`; 不创建指向 `DAT_02000005` 的 DATA ref.
- 全局 Equate before/after name/value/reference multiset 见 `f15-seg8-global-equates-plan.json`.

### REF_SLOTS

- 79 个地址槽新增 USER_DEFINED DATA ref; 45 个槽保持既有 DATA ref 的 type/source/operand/primary, 只投影最终目标主符号的派生字段.
- 54 个唯一目标的完整 before/after state 见 `f15-seg8-target-plan.json`. 静态 USER/ANALYSIS IDs 保持; DEFAULT materialize 的动态 ID 在落地时分配.
- 5 个 switch 目标保持 ANALYSIS namespace、qualified name、Data 和 ID; native 源用独立扁平 GAS 投影, 不改 namespace.
- 新地址定义: `OBJ_PALRAM_SLOT_5`, `BANNER_SECONDARY_TILE_VRAM`, `card_mini_frame_fallback_tile_data`, `pack_aob_mode7_tile_rows`, `pack_aob_mode7_palette`, `pack_aob_mode7_ptnsect`, `pack_aob_mode5_tile_rows`, `pack_aob_mode5_palette`, `pack_aob_mode5_ptnsect`, `pack_aob_mode0_8_tile_rows`, `pack_aob_mode0_palette`, `pack_aob_mode8_palette`, `pack_aob_mode0_8_ptnsect`, `banner_pack_palette`, `banner_pack_tile_rows`, `ui_effect_04_palette`, `ui_effect_04_tile_rows`, `pack_banner_b_palette`, `pack_banner_b_tile_rows`, `pack_banner_a_palette`, `pack_banner_a_tile_rows`, `banner_anim_palette`, `banner_anim_tile_rows`, `banner_anim_alt_tile_rows`, `zone_type_13_reveal_angle_step_table`.

### RENAME_SLOTS

- 纯 `RENAME_SLOTS=0`; 165 个自动源标签改名随 EQ/REF 动作完成. 最终源标签全部符合 `^[a-z][a-z0-9_]+$` 且唯一.

### FUNC_RENAME

| 入口 | 旧名 | 新名 | 证据 |
|---|---|---|---|
| `0x080bea94` | `play_ui_effect_15` | `play_zone_type_13_card_reveal_effect` | 唯一 typed caller `asm/01_vija_scene_text.s:4948-4950` 为 UI effect 0x15; body phases0..3 固定处理 zone type13 small/large card reveal, 32-call wait 和清理. whole-ROM even/Thumb holders 均为0. |

- 必要外部闭包: `resolve_zone_oam_base_coords_by_type@080c35ac` 仅把 PLATE 中旧名子串替换为新名; Function ID/body/ABI/refs 全部保持.
- registry、CSV 和 temp4 inventory 只做现有 BEA94 name projection; Function/named/auto/thunk 计数不变.

### PLATE

- 段内7条 + 外部C35AC一条, 共8条合同. 前5个段内准确 PLATE `PRESERVE`; BE9BC完整ASCII压缩重写; BEA94 rename+完整ASCII重写; C35AC仅旧名子串投影.
- BE9BC明确 r0 仅接受0/5/7/8, r1截断为u16 animation entry, 每条有效路径选择资源三元组和 tile height, 写OBJ palette/VRAM并初始化AOB ctx; 其他mode返回0.
- BEA94明确 phase0切换field+0x215 bit6并按side/count/attribute/region/settings选择资源; phase1以LUT[0,1,8,15,16]和sin[(4*v)&127]缩放偏移, counter0..4每次仅尝试一个OAM entry; phase2条件large-card; phase3执行32次且最后一次仍返回1; 仅phase>3清banner bit0和field bit2并返回0.
- 全部写入PLATE为ASCII且<=500字符; 详细消费者证据见 `f15-seg8-semantic-plan.json`.

## carve 计划 (R7)

- none.

## disasm 计划 (R4)

- none; 1984 条现有 InstructionDB 和Function body均保持.

## 新增 constants / 全局

- 新增 GNU definitions 共34: 9个scalar Equate +25个地址标签. 每项 name/value/file 见 `f15-seg8-gas-projections.json`; 计划名前态均不存在.
- 复用/物化名称另行核对现有GNU定义与Ghidra对象, 不重复定义.
- native全重导携带 inherited40 + 本段20 = 60 条固定 source projection; exporter不改.

## 5.1 登记 (Rule 3)

- none.

## 消费者证据 (R6)

| 对象 | 证据 | 结论 | 置信度 |
|---|---|---|---|
| `load_pack_aob_gfx_by_mode` | `asm/15_equip_target_summon_zoom.s:20442-20538` | r0=0/5/7/8资源分派; r1低16位为entry; packed mode high16为OBJ tile base512, low4为OBJ palette bank5. | high |
| `play_zone_type_13_card_reveal_effect` | `asm/15_equip_target_summon_zoom.s:20562-20978`; caller `asm/01_vija_scene_text.s:4948-4950` | zone13 reveal phase0真实资源分支; phase1五次单OAM尝试; phase2条件large-card; phase3共32次; phase>3清理返回0. | high |
| `DISPCNT_WINDOWS_CLEAR_MASK` | 实指令AND `0x1fff` | 清DISPCNT bits13..15三种window enable. | high |
| `DISPCNT_WIN1_OBJWIN_CLEAR_MASK` | 实指令AND `0x3fff` | 清DISPCNT WIN1/OBJWIN bits14..15并保留WIN0. | high |
| `SLOT_SET_CODE_TO_COUNT_NEG_OFF` | slot-set-code base加有符号`-0x250` | 从 `gP1SlotSetCodeArray` 转换到 `gP1SlotCountBase`. | high |

## 求助

- none.

## Executor Report: F15-Seg-8
- 槽: EQ=41 REF_ADD=79 REF_PRESERVE=45 PRESERVE=28 FUNC_RENAME=1 PLATE=8.
- carve=0 disasm=0 range 5.1=0.
- 新增 constants/全局: 34个GNU definitions; Ghidra新增9个Equate对象和27个目标USER label/materialization合同.
- 求助: none.
- proposal: `doc/dev/refine/F15-Seg-8.proposal.md`.

## Mode A v2 derived-closure corrections

- A single 193-primary graph (165 source labels, 27 changed targets, and the BEA94 Function symbol) projects all 10069 canonical states and all 412 actual Functions. Exactly 13 Functions contain 243 changed rich-reference rows; every row preserves CORE6 and changes only target-primary id/name/type/source. Static IDs remain exact and dynamic IDs are limited to approved USER materializations.
- `f15-seg8-full-function-observation-plan.json` freezes complete Function before/after metadata, including BEA94 prototype `undefined play_zone_type_13_card_reveal_effect()`, all incoming/body refs, owners, symbols, ABI, body geometry and EOL comments. Before records remain the observed pre-Seg8 state.
- Registry closure is seven existing tuples and one missing tuple. BDFAC is an existing name-key tuple and receives comment-only ASCII synchronization; BE9BC remains missing; BEA94 updates its existing name/comment; C35AC changes only the old-name substring. Ghidra PLATE writes remain exactly three.
- Production source scope is `asm/all.s`, three split modules, six constant files, the registry, formal CSV, and two canonical name inventories. Formal analysis artifacts are immutable Mode-B inputs; auto/summary inventories are byte-preserved. Native regeneration carries all 60 approved pins and changes no exporter or namespace.
