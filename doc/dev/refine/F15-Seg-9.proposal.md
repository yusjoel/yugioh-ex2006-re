# Refine Proposal: F15-Seg-9 [0x080bede4..0x080c00f0)

## 段测绘

- 范围: `[0x080bede4, 0x080c00f0)`, 4876B。
- 当前布局: 1849 个 InstructionDB（1777 条助记符、72 条 `.hword`），3854B 指令；240 个 4B word，共 960B；31 段 2B 零填充，共 62B。三者连续覆盖 4876B，无重叠、无空洞。
- 函数入口（10 个）:

| 入口 | 当前名 | body | 本轮动作 |
|---|---|---:|---|
| 0x080bede4 | tick_pack_banner_aob_phase | 342B | 名称保留，重写 PLATE |
| 0x080befc0 | play_ui_effect_17 | 400B | 改名并重写 PLATE |
| 0x080bf228 | play_ui_effect_11 | 148B | 改名并重写 PLATE |
| 0x080bf2d0 | draw_number_digits_to_oam | 180B | 名称保留，重写 PLATE |
| 0x080bf394 | play_ui_effect_0e | 474B | 改名并重写 PLATE |
| 0x080bf5a0 | play_ui_effect_38 | 476B | 改名并重写 PLATE |
| 0x080bf7f8 | play_ui_effect_37 | 1204B | 改名并重写 PLATE |
| 0x080bfe0c | play_ui_effect_05 | 230B | 改名并重写 PLATE |
| 0x080bff34 | repack_nibbles_with_palette_offset | 50B | 名称保留，重写 PLATE |
| 0x080bff6c | render_card_image_to_vram | 350B | 名称保留，重写 PLATE |

- 240 个 word 全覆盖：181 个自动名槽 + 59 个既有 switch word。
- 自动名槽动作：EQ_ADD=45，REF_ADD=104，REF_PRESERVE=32。59 个 switch word 为 PRESERVE。
- 现有 Data 类型：167 个 `/undefined4`，73 个 `/pointer`。本轮全部保持原类型。
- ROM_INCBIN / `.byte` 块：0。

完整逐槽前态、refs_from、refs_to、Equate、EOL、目标前态、最终标签及 after-rich 合同见 `F15-Seg-9.slots.tsv` 和 `f15-seg9-slot-plan.json`。

## 数据块分类 (Rule 2/3)

| 块 | ref-scan | 判定 | 理由 |
|---|---|---|---|
| none | raw=0 block / THUMB=0 block | 无 R4 / R7 / §5.1 | 本段无原始块；240 个 word 均为已定义 4B DataDB，代码、word、填充已全字节闭合。 |

6 个拟改名入口的全 ROM 滑窗扫描均为 even=0、THUMB|1=0。不存在函数指针表、奇地址回调或 `_1` alias 投影。扫描结果冻结在 `f15-seg9-full-rom-refscan.json`。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

45 个 EQ_ADD 绑定如下；地址逐项见 TSV。

| 常量 | 值 | 绑定数 | 处理 |
|---|---:|---:|---|
| LP_DELTA_PREFIX_TILE_MODE0 | 0x00000202 | 1 | 新建，LP delta 非零前缀 mode0 tile |
| DUEL_FIELD_UI_EFFECT_FLAGS_OFF | 0x00000215 | 7 | 复用 ewram.inc |
| PLAYER_BLOCK_STRIDE | 0x00000868 | 10 | 复用 ewram.inc |
| NIBBLE_PAIR_MASK_0F0F | 0x00000f0f | 1 | 新建，nibble 重打包域 |
| P1LP_TIMER_OFF | 0x00001cec | 1 | 复用 ewram.inc |
| VIJA_INTRO_WIN0H_BOUNDS | 0x000028f0 | 2 | 复用 duel_field.inc |
| GSETTINGS_OFFSET | 0x00006c2c | 7 | 复用 name_input.inc |
| TEXT_RENDER_COLOR_MODE_1 | 0x00008001 | 2 | 复用 duel_field.inc |
| DISPCNT_WIN0_CLEAR_MASK | 0x0000dfff | 2 | 复用 gba_io.inc |
| OPP_CARD_NAME_STR_OFF_ES | 0x0003a90c | 3 | 复用 card_info.inc |
| OPP_CARD_NAME_STR_OFF_ES_NULL | 0x0003a90e | 3 | 复用 card_info.inc |
| AOB_POS_X124_Y56 | 0x0038007c | 1 | 新建 |
| AOB_POS_X124_Y88 | 0x0058007c | 1 | 新建 |
| AOB_MODE_TILE_BASE_512_PAL2 | 0x02000002 | 1 | 新建 |
| AOB_MODE_TILE_BASE_512_PAL3 | 0x02000003 | 1 | 新建 |
| AOB_MODE_TILE_BASE_512_PAL5 | 0x02000005 | 1 | 复用 duel_field.inc |
| AOB_INIT_MODE | 0x02000007 | 1 | 复用 gba_mem.inc |

每个 Equate 绑定固定到 source word 的 operand 0；Equate 对象没有 SourceType。完整全局图从 2455 个对象 / 12551 个绑定投影到 2461 个对象 / 12596 个绑定，新增 6 个对象和 45 个绑定。

### REF_SLOTS

- REF_ADD=104：为原本无 DATA ref 的自动名槽建立 USER/ANALYSIS 目标 DATA ref，source type 固定为 USER_DEFINED，operand=0，primary=true。
- REF_PRESERVE=32：保持现有 DATA ref 的 CORE6、source type、primary 位和静态目标 ID；仅重命名 source slot 并增加 ASCII EOL。
- 唯一目标值 59 个。既有 USER/ANALYSIS 目标保持静态 ID；11 个 DEFAULT 目标按批准名称物化 USER label，其中 9 个新增 GNU 定义，2 个复用已有 GNU 定义。
- 新物化目标:

| 值 | 最终名 | GNU 位置 |
|---:|---|---|
| 0x020230f8 | gDuelFieldAuxAobCtx | constants/ewram.inc |
| 0x060148c0 | CARD_IMAGE_TILE_VRAM_BASE | constants/gba_mem.inc |
| 0x08510460 | shared_ui_palette_256 | constants/rom_data.inc |
| 0x09851ffc | lp_digit_tile_rows | constants/rom_data.inc |
| 0x09899e08 | ui_effect_38_tile_rows | constants/rom_data.inc |
| 0x0989da08 | ui_effect_38_palette | constants/rom_data.inc |
| 0x0989da88 | ui_effect_38_ptnsect | constants/rom_data.inc |
| 0x0989eda8 | lp_timer_aob_tile_rows | constants/rom_data.inc |
| 0x0989f5a8 | lp_timer_aob_ptnsect | constants/rom_data.inc |
| 0x05000300 | AOB_CARD_PAL_DST | 复用 constants/gba_mem.inc |
| 0x06014200 | AOB_DISPLAY_TILE_VRAM_A | 复用 constants/gba_mem.inc |

目标物化引起的 target-primary 派生字段按单一 after 图更新；旧 reference 对象的 CORE6 不重建、不升级 source type。104 个 REF_ADD 的完整 10 字段 DATA 引用按目标分组加入 49 个 target after，五个 source/target 重合地址仍只有一个 after；91 条既有 DATA（73 DEFAULT、18 USER_DEFINED）逐边保持。

### RENAME_SLOTS

181 个自动名槽均改为 `^[a-z][a-z0-9_]+$` 的地址唯一名并写 ASCII EOL。59 个 switch word 保持原有 label/no-label、`/pointer`、ANALYSIS namespace、qualified name、namespace ID、静态 Symbol ID 与 DATA ref，不为统一外观新增 alias。

### FUNC_RENAME

| 入口 | 当前名 | 最终名 | 实际 indeg | 证据 |
|---|---|---|---:|---|
| 0x080befc0 | play_ui_effect_17 | play_zone_card_display_transition | 1 | play_ui_effect@0801f21a；三阶段 zone/card-display 流程 |
| 0x080bf228 | play_ui_effect_11 | play_zone_info_palette_cycle_effect | 1 | play_ui_effect@0801f0de；phase0 首次更新 + phase1 63 次 palette cycle，坐标固定 |
| 0x080bf394 | play_ui_effect_0e | play_life_point_change_effect | 1 | play_ui_effect@0801f10e；LP 数字 tile/OAM 与十进制步长更新 |
| 0x080bf5a0 | play_ui_effect_38 | play_windowed_aob_slide_effect | 1 | play_ui_effect@0801f202；WIN0/BLDY、AOB、正弦位移 |
| 0x080bf7f8 | play_ui_effect_37 | play_correct_miss_result_effect | 1 | play_ui_effect@0801f1fc；0326/0327 多语言字符串与结果 bitmask |
| 0x080bfe0c | play_ui_effect_05 | play_lp_timer_aob_effect | 1 | play_ui_effect@0801f132；P1LP_TIMER_OFF 守卫与 AOB 流程 |

6 个入口的 Function ID、body ranges、body SHA、ABI、signature、parameter/return、incoming reference CORE6 全部守恒。实际 BL operand、source Function 记录、registry、正式 CSV 和 canonical temp inventories 同步投影；全 ROM even/odd holder 均为 0，因此不创建函数指针 alias。

### PLATE

- 13 个 Function 合同：段内 10 个 + 必要外部注释闭包 3 个。
- 13 个 PLATE 均写入；`tick_pack_banner_aob_phase` 的错误 971 字符旧 PLATE 改为 0/1/default 的真实状态机摘要。
- 13 个写入 PLATE 全部 ASCII 且每条不超过 500 字符。
- 第二轮窄修：BEDE4 明确 N/C 缓存条件；BF394 明确 banner+0x18 是 progress 字段偏移；BF7F8 明确 ptnsect/string 与 phase2 latch；BFF34 明确 lower carry 可设置 bits11:8。
- 外部必要闭包:
  - 0x080ca5f8 `write_lp_digit_tiles_to_vram`: 旧注释中的 `play_ui_effect_0e` 改为新名并压缩为准确 ASCII PLATE。
  - 0x080f0cc0 `setup_line_buf_with_font_and_align`: 旧注释中的 `play_ui_effect_37` 改为新名并保留实际字段语义。
  - 0x080f8000 `render_aob_frame_to_oam`: 旧注释中的 `play_ui_effect_37/38` 改为两个新名并保留实际渲染语义。

完整 PLATE 全文、旧全文 SHA、Function 全属性、incoming/body reference before/after 见 `F15-Seg-9.plates.tsv`。

## carve 计划 (R7)

无。

## disasm 计划 (R4)

无。现有 1849 个 InstructionDB 地址和字节全部保持。

## 新增 constants / 全局

- 新增 scalar Equate 6 个：`LP_DELTA_PREFIX_TILE_MODE0`、`NIBBLE_PAIR_MASK_0F0F`、`AOB_POS_X124_Y56`、`AOB_POS_X124_Y88`、`AOB_MODE_TILE_BASE_512_PAL2`、`AOB_MODE_TILE_BASE_512_PAL3`。
- 新增地址定义 9 个：上表 `gDuelFieldAuxAobCtx` 至 `lp_timer_aob_ptnsect`。
- 这 15 个名称在冻结前 GNU constants/source labels 中命中 0；复用名称的值与当前 GNU/Ghidra 对象逐项相等。
- 新 USER Symbol 的 ID 由 Ghidra 动态分配；既有 USER/ANALYSIS Symbol 和 Function 的静态 ID 必须保持。

## §5.1 登记 (Rule 3)

无。本段无 raw 块。

## 消费者证据 (R6)

| 证据 | 结论 | 置信度 |
|---|---|---|
| asm/15_equip_target_summon_zoom.s:20997-21094 | type0xb 仅在 u32(N-C)<=7 且 N>7 时把缓存 C 写为 C-1；不写 real N；随后刷新 field tiles/count tag | high |
| asm/15_equip_target_summon_zoom.s:21212-21517 | 0x17 phase1 做 32 次 palette 更新且 phase0 不落入 phase1；phase2 refresh 后推进 | high |
| asm/15_equip_target_summon_zoom.s:21519-21607 | 0x11 数量差 clamp0..6；phase0 落入首次 palette 更新，phase1 再做 63 次，坐标固定 | high |
| asm/15_equip_target_summon_zoom.s:21609-21708 | r0 player、r1 magnitude、r2 mode；非零前缀 mode0=0x202/mode1=0x200，digit tile0x204+2*d | high |
| asm/15_equip_target_summon_zoom.s:21711-21993 | progress 位于 banner+0x18，按所选十进制 step 累加并 clip；mode1 写 LP+progress，mode0 写 max(LP-progress,0) | high |
| asm/15_equip_target_summon_zoom.s:21995-22297 | WIN0/BLDY、AOB 资源、正弦位移、淡入/保持/淡出 | high |
| asm/15_equip_target_summon_zoom.s:22299-23117 | phase0 ptnsect 初始化且 strings 走 line buffer；phase2 nonzero tick 锁 latch，latch0 才按ctx写两结果OAM；all-tick0才增hold | high |
| asm/15_equip_target_summon_zoom.s:23119-23268 | timer0 清两flag；两处相反anm比较；结束仅保留03000254 bit31 | high |
| asm/15_equip_target_summon_zoom.s:23270-23299 | 从 a&0x0f0f 开始 OR 两个 u8 调整量；lower carry 可设置 bits11:8，不能宣称原低nibble全部不变 | high |
| asm/15_equip_target_summon_zoom.s:23302-23497 | 10行*80组*4halfword；3200 repack/strh，4800B源、6400B目的及128B palette | high |
| asm/20_anim_jp_tileblit.s:14944-14965 | ctx15写bit0；ctx14写bits6:2并保留bit7及bits1:0 | high |

## Source / exporter 合同

- 继承 61 条已批准 GAS pin，并新增 20 条 source-only pin，总计 81 条。
- 本段新增 pin 精确覆盖 15 个 PALRAM/VRAM source fallback 和 5 个 ANALYSIS switch-table base fallback。DB 中 DATA ref 保持独立，不以 exporter 输出替代 DB 合同。
- 生产范围仅限 source-scope plan 中列出的 5 个 split module、必要 constants、registry、正式 CSV 与 canonical temp inventories。旧 `tools/ghidra-labeling/ghidra-functions.*` 快照保持字节不变。
- 历史正引用 backlog `[0x0804becc,0x0804bf20)` 保持，不在本段回溯处理。

## 冻结与实施门禁

- canonical BEFORE: `root-f15-seg9-composite-independent-prestate-v1.json`，416 请求 / 415 实际 Function，10079 个唯一 address state，1446 个 module word，324 个 target，2455 个 global Equate。
- 完整 after 图必须覆盖同一 10079 地址集合；重合地址只有一个 after 状态。
- `f15-seg9-analysis-v2-producer.py --generate` 从 canonical BEFORE、formal 动作和 198 节点批准图生成后态；`f15-seg9-analysis-v2-validator.py` 独立重派生全部 10079 states / 416 Function，并实际执行 104 个单边删除负例，任一缺边均拒绝。
- 240 个 source word 的 ROM 值、字节、Data 类型、PC READ、旧 refs/equates/EOL 和 owner 全部由 formal TSV 冻结。
- build/ROM byte-identical 是后续 fixer 的红线；executor 不执行 Ghidra、导出或构建。

## 求助

无。

## Executor Report: F15-Seg-9

- 槽: EQ=45 REF_ADD=104 REF_PRESERVE=32 PRESERVE=59 FUNC_RENAME=6 PLATE=13（写13，保留0）
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: 6 scalar Equate + 9 address definitions
- 求助: none
- proposal: `doc/dev/refine/F15-Seg-9.proposal.md`
