# 函数/数据细化计划 — `asm/00_system_str_vija.s`

> 阶段目标: 把 `asm/00_system_str_vija.s` (ROM `0x080000C0 ~ 0x0801CB00`) **逐函数/逐数据区
> 细化完成**。本文沉淀本次会话确立的「细化要求」(checklist) + 落地工作流 + 剩余工作清单。
> 总目标 (全 ROM 命名 4641/4641) 已完成; 本阶段是在已命名基础上做**内部细化** (符号化 /
> 注释订正 / 误标数据反汇编 / 数据区结构化)。

---

## 一、细化要求 (checklist) — 本次会话沉淀

每个函数 / 数据区按下列要求逐项过一遍。括注为本次会话的实例来源。

### R1 常量符号化
立即数若是已知常量, 在 Ghidra 设 **equate** (同名), 经 `ExportRangeToGas.apply_equates`
导出为符号; GAS 端靠 `constants/*.inc` 的 `.set`/`.equ` 解析回同值 (byte-identical)。
- 例: `mov r0,#0x12` → `#PSR_IRQ_MODE` (`constants/arm_psr.inc`); `0x1f`→`PSR_SYS_MODE`。
- ⚠ `ins.toString()` 不应用 equate, 必须由 `apply_equates` 文本替换 (见 build-pipeline.md §二)。
- 设 equate 用 `SetBootEquates.py` 式脚本 (`EquateTable.createEquate` + `addReference(addr,opIndex)`)。

### R2 标签可读化 (消灭自动名)
`DAT_xxx` / `LAB_xxx` / `DWORD_xxx` / `UNK_xxx` / `SUB_xxx` → 语义名 (`^[a-z][a-z0-9_]+$`)。
- 栈/指针/状态: `sp_irq_init` / `sp_sys_init`; 字面量池槽 `ptr_<目标>` (如 `ptr_intr_vector`)。
- RAM/IO 地址加 USER_DEFINED label + 写进 `constants/iwram.inc`/`gba_io.inc` 的 `.equ`
  (如 `gIntrTable=0x03000000`, `INTR_VECTOR=0x03007ffc`) → `.word` 自动符号化。
- 当前 00 文件残留 **~1519 个自动名 label** 待处理 (主要在 291 个函数体内)。

### R3 符号必须被代码「按名引用」
仅在 `data/*.s` 定义 label **不够** —— 代码字面量池仍是裸地址。必须在 Ghidra 给目标地址加
USER_DEFINED label + 给字面量池 `.word` 加 **DATA ref**, `resolve_word_symbol` 才会把
`.word 0x0800aa10` 导出成 `.word lang_select_gfx_0`。
- 教训: `lang_select_gfx_0` 初版只在 .s 定义, grep 搜不到引用 → 补 label+ref 后才接通。
- 验证: `grep <name>` 应同时命中 **定义**(data/) 和 **引用**(asm/ 字面量池)。

### R4 误标为数据的代码要反汇编
Ghidra 把代码错标成 `DWORD_`/`.incbin`/`.byte` 的, 反汇编为指令 + 必要时 createFunction。
- 例: `0x080000fc` IntrMain 体 (`ROM_INCBIN`→ARM 指令); `0x080001fc` IntrMain_RetAddr
  (`.word 0xe8bd4000`→`ldmia sp!,{lr}`)。
- **判定靠读「使用该数据的代码」** (见 R6)。流程: clearListing → setTMode(ARM=0/THUMB=1)
  → DisassembleCommand → (createFunction)。

### R5 注释订正 (错误 / 过时)
plate / EOL 注释必须准确且用**现名**:
- 过时 `FUN_xxxxxxxx` 引用 → 改现函数名 (例: write_tile_row_to_vram plate 旧引 `FUN_080ee010`)。
- 错误描述 → 改正 (例: init_cpu plate 误把 IntrMain 称 dispatch_thumb_isr_from_arm)。
- 关键行加 EOL 注释 (例: IntrMain 中断优先级扫描 / gamepak halt)。
- 零容忍词 (似乎/可能/大概) 禁用; 给 file:line 证据 + 置信度。

### R6 先读「消费者」再命名 (理解优先)
命名数据/参数前, **先读使用它的代码**搞清格式语义, 不靠猜。
- 例: 读 `write_tile_row_to_vram` 才知 map entry `B` 含 hflip/vflip/palette 位 (`B&0x3ff`=tile);
  之前没读 → 渲染漏掉带翻转位整行 ("最后少一行" bug)。
- 例: 读 copy 调用的 (dst,src,count) 才确定 0xDD90=palette(0x20)、0xDDB0=4 tile(0x80)。

### R7 数据区结构化
裸 `ROM_INCBIN` 的数据区, 按类型抽成可读结构, 入库的是**生成脚本**(data/、graphics/ 是
gitignore 生成产物):
- **索引/指针表** → 生成脚本写 `data/*.s` + 导出器 `SKIP_REGIONS` + `.include` + 接入
  `export_all.py` (例: `game-strings-remap-table.s` / `build_remap_table.py`)。
- **图形** → 仿 `graphics/bin/duel-field/` 组织: `palettes/`、`tiles/`、`tilemaps/` 分组**纯数据**
  bin (header 放 .s 的 `.hword`) + `images/` 每 tilemap 一张 PNG; 渲染按 map 还原真实排布
  (`A=(Y<<8)|X` 位置, `B` tile+hflip/vflip), **无调色板用 16 级灰度** (index0 透明)。
- **全 0 填充** → `.zero N` (导出器已自动)。

### R8 目视核对 (图形)
图形提取后**渲染 PNG 目视确认**可识别 (例: lang-select 渲出国旗/边框); 拦截 bpp/行序/翻转
错误。无法静态确认调色板/消费者时**诚实标注** + 走 mGBA 动态路径 (asset-location.md §二),
不臆造。

### R9 红线: byte-identical + 备份
- 每步 build 验证 **byte-identical** (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
- Ghidra 写入前**必备份** `.rep` → `.rep.bak-<ts>-pre-<task>`。
- 失败 → 回滚 .rep, 二分定位。

---

## 二、落地工作流 (pipeline)

**代码侧 (Ghidra → asm)**:
```
1. 备份 .rep
2. Ghidra 脚本 (rename/label/equate/disasm/comment)  tools/ghidra-labeling/*.py
3. 重导出: ghidra-export-range.bat 080000c0 084c7637 asm/all.s 0
4. python tools/asm-regen/inject_modes.py
5. python tools/asm-regen/split_all_s.py
6. build + byte-identical 校验 (SHA1 9689337d)
7. (改了函数名/数) ExportFunctionInventory.py + sync_ghidra_names_to_proposals.py
8. commit (用户明确指令后)
```

**数据侧 (生成脚本 → data/graphics)**:
```
1. 写生成脚本 (tools/rom-export/*.py 或 tools/game-strings/*.py)
2. 导出器 ExportRangeToGas.SKIP_REGIONS 加区段 → .include
3. 接入 tools/rom-export/export_all.py STEPS
4. 重导出 + build + byte-identical
```
要点: `SKIP_REGIONS` 的 skip_start 必须是导出器游标的落点 (上一段/字段结束处), 否则不触发
(remap 表踩过此坑: 游标落 0x242 而非 0x250)。

---

## 三、当前进度 (00_system_str_vija.s)

| 区段 | 地址 | 状态 |
|---|---|---|
| crt0 / IntrMain / IntrMain_RetAddr | 0x0C0..0x224 | ✅ 反汇编+符号化+注释 **(R1 立即数符号化已彻底)**: PSR equate / sp_*_init / IntrMain / ptr_* + REG_BASE + 14 个 INTR_FLAG_* + INTR_NESTED_ENABLE_MASK(0x26c0) + PSR_MODE_FIQ_IRQ_MASK(0xdf) + PSR_IRQ_MODE_IRQ_OFF(0x92); dispatch plate Side-effects 归属已订正 (实发生在 IntrMain_RetAddr)。剩 LAB_080001bc/c0 自动名 (用户裁定不处理) |
| game-strings remap 表 | 0x250..0xF36 | ✅ `data/game-strings-remap-table.s` |
| game-strings 指针表 | 0xF40..0xAA10 | ✅ `data/game-strings-pointer-table.s` (前序会话) |
| lang-select 图形 | 0xAA10..0xDE30 | ✅ 国旗/边框/palette/extra tiles, 符号化, 目视确认 |
| boot-ui 图形 | 0xDE30..0x13510 | 🟡 灰度导出 + 结构化; **用户裁定放最后** (导出图未确认/未找到加载方) |
| **batch-1: demo scene 簇 (15 fn)** | 0x13510..0x14398 | ✅ R1 常量 + R3 指针 + R5 注释完成 (见 §四.batch-1); byte-identical |
| 代码函数 (其余 276 个) | 0x14398..0x1CB00 | ⬜ 函数已命名; 体内常量/指针/注释待细化 (LAB_ 内部分支按裁定跳过) |

---

## 四、剩余工作

### 4.0 batch-1 完成记录: demo scene 簇 (0x13510..0x14398, 15 fn) ✅

reset_display_and_gl_state / setup_demo_sprite_entry(_alt) / dispatch_demo_sprite_setup_by_mode /
load_demo_bg_gfx_set0/1 / load_demo_obj_resource_by_slot(_slot0) / write_bg3_scroll_regs /
tick_demo_bg3_hscroll/vscroll / setup_demo_cell_anim_slot / apply_demo_window_fade_in/out_step /
tick_demo_scene_state_machine。全部操作 gDemoState (0x02029ec0)。byte-identical SHA1 9689337d。

**新增工具能力**: `ExportRangeToGas.resolve_word_equate` —— 字面量池里的**纯数值/范围外地址常量**
(位掩码 / IO 初值 / FS 区指针) 经 Ghidra **data-equate** 导出为符号名 (对未设 equate 的数据 no-op,
不影响全 ROM byte-identical)。配合 selecte-3 **槽标签按 `<func>_<const>` 改名**, 加载点与定义点都可读。

| 项 | 做法 | 数量 |
|---|---|---|
| R1 位掩码 | data-equate → `DEMO_CLEAR_BITS_<hi>_<lo>`/`DEMO_KEEP_BITS_8_0` (共享, 按位区间) | 35 槽/7 常量 |
| R1 IO/资源初值 | data-equate → `DEMO_BG1/2/3CNT_INIT`/`DEMO_CPUSET_FILL_CTRL`/`DEMO_EXTRA_RESOURCE_DESC` | 6 槽 |
| R3 FS 资源指针 | data-equate (范围外地址常量) → `PATH_DEMO_EXODIA*`/`DEMO_OBJ_RESOURCE_PTR_TABLE`/`DEMO_SPRITE_RESOURCE_DESC`/`DEMO_CELL_ANIM_ASSERT_FILE`/`_EXPR` | 10 槽 |
| R3 已符号化指针 | 槽标签改名 `<func>_ptr_gdemostate`/`<func>_ptr_<ioreg>` (值已由现有 ref 符号化) | 15 槽 |
| R5 注释 | FUN_08013bd4→tick_demo_scene_state_machine (4); caller 归属订正 reset_display+hub (直接调用者仅 play_ui_effect_3a, 0x08014398 为 indirect_table); DAT_0801393c→DEMO_EXTRA_RESOURCE_DESC; 断言文件 IG2D_Main.c→Exodia/EXO_main.c (ROM 字节核实) | 7 plate |

新增: `constants/demo_state.inc`; 脚本 `tools/ghidra-labeling/RefineDemoSceneBatch1{,B,Comments}.py`。

**R7 数据结构化 (遇未导出数据即补导出脚本, 用户标准流程)**: batch-1 的 R3 资源指针目标
(0x09e396b8..0x09e398dc, 548B) 原是 `rom.s` line733 raw `.incbin 0x1E317B4+0x27558` 大 blob
里的未分化字节。已切出结构化为 `data/demo-exodia-resources.s` (描述符 `.byte` / obj 路径池
`.asciz` / 指针表 `.word <label>` / 断言串 / BG 路径), 生成脚本 `tools/rom-export/export_demo_exodia_resources.py`
接入 `export_all.py`; blob 切成 [前 0x7F04] + [include] + [后 0x1F430]; byte-identical。
- ⚠ 该块前后仍是 NNS/GL SDK 调试串混合池 (其它子系统的断言/变量名), 未被引用故留 blob, 将来引用到再切。
- ✅ 代码侧 R3 已从 data-equate 常量切换为**直接引用 GAS label** (单一命名源): 10 个指针在 Ghidra
  给目标地址打 USER_DEFINED label (= 导出脚本 label 名) + 代码槽加 DATA ref + 删 equate, 经
  resolve_word_symbol 导出 `.word demo_sprite_resource_desc` / `.word demo_path_exodia*` 等; demo_state.inc
  里的 DEMO_*_RESOURCE_DESC / PATH_DEMO_* 常量已删 (脚本 RefineDemoSceneBatch1LabelSwitch.py)。
  注: 纯数值常量 (掩码/BG初值/EXTRA_RESOURCE) 非地址, 无 GAS label, 仍用 data-equate。

**defer (5 槽, R8 诚实标注, 低价值/需更深分析)**: `0x080000ae` (ROM 头 game-code 区 JP 探测) /
`0x02000000`+`0x6c2c` (EWRAM base+offset = 0x02006c2c 全局字节, 语义未定) / `0x14b` (断言行号 331,
自明) / `0x08013c04` (hub 10-case 跳转表基址; 表项指向 LAB_ case handler, 按 LAB_ 跳过策略留)。

**LAB_ 内部分支 (111)**: 按 boot 区裁定**跳过**。

### 4.1 boot-ui 上色 (1 项, 需 mGBA, 用户裁定放最后)
跑游戏到语言选择之后画面 → dump VRAM/PALRAM → 与 0xDE30..0x13510 字节匹配 → 定位加载
函数 + 调色板 → 替换灰度为真彩 + 语义命名段 (改 `export_boot_ui_gfx.py` 模块名/调色板)。

### 4.2 291 个代码函数内部细化 (主体工作量)
范围 `0x13510..0x1CB00`。按地址序分批 (建议 ~10-15 fn/批), 每批走「代码侧 pipeline」。
子系统聚类 (按函数名):
- 显示/GL/VRAM/BG: reset_display_and_gl_state, write_bg3_scroll_regs, copy_to_bg3_screen_map,
  init_gl_palette_slot_flags, get_obj_tile_vram_base ... (0x13510..0x150xx)
- 滚动条/anim_ctrl: compute_scrollbar_thumb_position, update_scrollbar_thumb_display,
  get_anim_ctrl_seq_id, dispatch_isd_cell_anim_oam_setup ... (0x154xx..0x158xx)
- G2D/资源加载: load_g2d_obj_resource_set, get_bgdt_entry_char_base, get_objd_inline_data_ptr,
  resolve_prhlist_entry_name_ptr ... (0x15d30..0x170xx) — NNS g2d 系, 可对照 refs/NITRO SDK
- 字符串/文本渲染: pad_str_to_char_multiple, render_jp_string_row, append_col_padded_text_to_buf,
  scale_char_width_by_encoding ... (0x178xx..0x19xxx)
- banlist 密码输入场景: banlist_password_enter_char, init_banlist_pass_input_scene,
  render_banlist_password_chars_row, advance/retreat_banlist_password_cursor ... (0x143xx, 0x186xx..0x1abxx)
- vija/shuen 场景 tick: tick_banlist_card_slot_anim_primary, write_shuen_bg3_scroll_regs,
  tick_scene_step_by_step_table_a, tick_vija_bg3_scroll_forward ... (0x1b1xx..0x1cb00)

每个函数细化清单: R1 常量 + R2 标签 + R3 引用接通 + R4 误标数据 + R5 注释 + R9 byte-identical。

参考: 系统/SDK 风格函数 (g2d/中断/newlib) 除 refs/pokeruby 外, 也查 **refs/NITRO SDK v2.0RC3**
(NitroSDK 早期亦覆盖 GBA, 见 memory reference-nitrosdk-gba)。

---

## 五、批次建议

0. ✅ **boot/IRQ 区 (0x0C0..0x224) R1 收尾** (本会话): IntrMain/RetAddr 立即数符号化 +
   dispatch plate 归属订正, byte-identical 通过 (SHA1 9689337d)。
1. ~~先清 boot-ui mGBA 上色~~ → **用户裁定: 暂跳过, 放最后处理** (当前导出图未确认、未找到加载方; 0xAA10..0x13510 暂留 🟡)。
2. 按地址序从 `reset_display_and_gl_state` (0x13510) 起, ~10-15 fn/批, 逐批走 pipeline +
   byte-identical + commit。优先同子系统连续批 (复用上下文)。
   - ⚠ batch-2 首函数 `reset_display_and_gl_state` 的 plate 仍引 `FUN_08014398` (= tick_prng_step_sequence);
     但权威 2-col callgraph 显示其**直接调用者仅 play_ui_effect_3a**, 0x08014398 是 `indirect_table`
     (函数指针表成员, 非 direct bl) → 该 caller 归属需 R6/R7 复核, 留 batch-2 处理 (同样 line 1035
     `tick_demo_scene_*` plate 的 FUN_08014398 旧名)。
3. 每批后视情况更新本文「进度」表。

---

## 六、相关文档
- `doc/dev/methodology/build-pipeline.md` (§二 导出器/equate, §七 拆分)
- `doc/dev/methodology/symbolization.md` (字面量池符号化)
- `doc/dev/methodology/asset-location.md` (§二 mGBA 动态路径 — boot-ui 上色用)
- `doc/dev/data-structure/{lang-select-tiles,boot-ui-gfx,game-strings}.md`
- 本次会话产出脚本: `tools/ghidra-labeling/{AnnotateBootIrq,SetBootEquates,AnnotateIntrRetAddr,AnnotateLangSelectGfx,DumpRefsToRange}.py`,
  `tools/rom-export/{export_ui_tile_blocks,export_boot_ui_gfx}.py`, `tools/game-strings/build_remap_table.py`
- boot/IRQ R1 收尾 (本会话): `tools/ghidra-labeling/RefineBootIrqEquates.py` (18 equate 引用 + dispatch plate 修正);
  新增常量 `constants/gba_intr.inc` (REG_BASE + INTR_FLAG_* + 复合掩码), `constants/arm_psr.inc` 追加
  PSR_MODE_FIQ_IRQ_MASK/PSR_IRQ_MODE_IRQ_OFF; `asm/rom.s` 接入 gba_intr.inc include。
