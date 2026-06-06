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
| **batch-2: GL blend/brightness 簇 (12 fn)** | 0x14600..0x14a10 | ✅ R1/R2/R3/R5 完成 (见 §四.batch-2): gGlBlendState 符号化 + 4 equate + 1 函数改名 + 7 plate 订正; byte-identical。**附带修复 1 个 pre-existing 断言串 carve 回归 (assert_..._670 标签)** |
| 代码函数 (其余 ~264 个) | 0x14398..0x1CB00 | ⬜ 函数已命名; 体内常量/指针/注释待细化 (LAB_ 内部分支按裁定跳过) |

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

### 4.0a batch-2 完成记录: GL blend/brightness 簇 (0x14600..0x14a10, 12 fn) ✅

cpu_copy_auto / gl_clear_vram_palram_scroll / reset_gl_blend_transition_state /
update_brightness_fade_flag / gl_set_brightness / init_blend_transition_params(_ex) /
gl_set_blend2_level / gl_fade_in / gl_fade_out / check_blend_transition_done /
tick_blend_transition_step。全部操作 gGlBlendState (0x02023480)。byte-identical SHA1 9689337d。

**关键发现**: 本簇核心结构 `0x02023480` 在 batch-1 多个 plate 被**误称 `gDemoState`** (实际
gDemoState=0x02029EC0)。它是 GL 屏幕亮度/alpha-blend 淡入淡出控制块 (源 GL/GL_Common.c),
与紧邻的 GL 调色板管理区 0x02023490 (gl_state_init 用) 不同。本批订正。

| 项 | 做法 | 数量 |
|---|---|---|
| R2/R3 状态结构 | `gGlBlendState=0x02023480` → `constants/ewram.inc` .equ + Ghidra USER label + 8 槽 DATA ref + 槽改名 `<func>_ptr_gl_blend_state` | 8 槽 |
| R1 位掩码 | data-equate `GL_CLEAR_BITS_9_2`(0xfffffc03, 清 blend1 step bits[9:2]) / `GL_CLEAR_BITS_17_10`(0xfffc03ff, 清 blend2 step bits[17:10]) | 11 槽/2 常量 |
| R1 fill 控制字 | data-equate `GL_CLEAR_VRAM_FILL_CTRL`(0x01006000) / `GL_CLEAR_PALRAM_FILL_CTRL`(0x01000100) | 2 槽 |
| R2 改名 | assert-line 槽 0x148bc(行 281) → `init_blend_transition_params_ex_assert_line_blend1` | 1 槽 |
| 函数改名 | 0x0801469c `clear_demo_sprite_enable_bits` → `reset_gl_blend_transition_state` (batch-1 误名: 实复位 gGlBlendState +0x8 控制字, 与 demo sprite 无关; 唯一调用者 tick_demo_scene_state_machine) | 1 fn |
| R5 注释 | 1 plate 全改 (0x1469c 函数改名) + 6 plate targeted (gDemoState→gGlBlendState ×4 + gl_set_blend2_level 的 bits[11:2]→bits[17:10] 修正 + 常量名对齐) | 7 plate |

新增: `constants/gl_blend.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineGlBlendBatch2.py`。

**⚠ 附带修复: pre-existing 断言串 carve byte-identical 回归 (与 batch-2 无关)**

batch-2 重导出后 build 出现 **2 字节** mismatch @ `0x0801a4f8`。二分确认 **HEAD 自身亦非 byte-identical**
(同 2 字节, 同 hash 668AAD0C) —— 即上一 commit (7e770e1 断言串 carve) 引入的潜伏回归, 非 batch-2 所致。
- 根因: `0x09e3c670` 的 Ghidra 符号被遗留为**裸 base 名** `assert_anmid_ig2d_getanmsequencescoun`
  (无 `_670` 后缀), 而 `assert_labels.csv` / rom.s carve block 均意图 `_670`。该截断名与 base 串
  (0x09e3b434) 的 carve label **同名碰撞** → `.word @0x1a4f8` 经 resolve_word_symbol 导出裸名 →
  GAS 解析到 0x09e3b434 (错), 应为 0x09e3c670。
- 修复: `tools/ghidra-labeling/FixAssert670Label.py` 把该符号补回 `_670` 后缀 (1 符号改名)。
- 教训: assert-carve 的同前缀串靠**地址尾号后缀**去碰撞, AddAssertStringLabels.py 须确保 Ghidra
  目标符号名 = carve label 名 (带后缀); `_verify_carve.py` 只验 carve 块字节, **不覆盖 .word 符号
  解析**, 故未拦截 → 该类回归唯一防线是 build byte-identical, **断言串改动后必须 build 复验**。

### 4.0b NNS/GL SDK 断言串符号化 (全 ROM, 156 串)

`suppress_assert_report(file, line, expr)` 全 ROM 728 调用点; file/expr 字符串集中在
0x09e398dc..0x09e5073c (line733 raw blob 的 after-demo 段内, 与图形/二进制/指针表混合)。
**最终形态 (用户定): 把 156 个被引用的断言串本体 carve 进 rom.s 成带 label 的 `.asciz`, 其余
(未引用串/二进制/指针表) 仍 `.incbin` 原样保留; 代码 .word 经 resolve_word_symbol 指向 carve label。**

落地 (byte-identical):
- 扫描器 `tools/rom-export/export_assert_strings.py` (一次性, 非 export_all): 扫 asm 调用点
  (closest r0/r2 + is_asciz 校验 + demo 块排除) → `assert_labels.csv` (slot,string,label) +
  `assert_carve_block.txt` (137 `.incbin` + 156 `<label>: .asciz "<content>"`, 替换 rom.s
  after-demo incbin) + `assert_slots.csv` (459 槽 `<func>_<assertlabel>` 改名 + EOL=断言原文)。
- `AddAssertStringLabels.py`: 串地址建 USER_DEFINED label + 443 槽加 DATA ref (驱动 resolve_word_symbol)。
- `SetAssertSlotLabels.py`: 459 槽 `DAT_xxx → <func>_<assertlabel>` (setName 重命名) + EOL_COMMENT=断言原文。
- `RenameAssertPreexisting.py` + `FixAssertPlateRef.py`: 把 2 个旧名 (gl_bright_assert/nns_g2d_assert_anmID)
  统一为 my-scheme (与 carve 一致), 并订正 1 处 plate 散文旧名。
- `_verify_carve.py`: 核对 carve 块覆盖字节 == 原 incbin (0x1F430) 且重建序列 == ROM。
- `assert_carve_block.txt` 内容粘入 `asm/rom.s` (替换 `0x1E398DC,0x1F430` 那行)。

工具改动:
- `ExportRangeToGas.py`: (a) `resolve_word_equate` (字面量池数值常量 data-equate, demo 掩码用);
  (b) `emit_defined_data` 取 EOL_COMMENT 追加到 `.word ... @ addr bytes` 之后 (断言原文渲染)。

效果: 898 处 `.word assert_*`/`*_filename` + EOL 原文; 串本体在 rom.s carve 块 (含 content), **不在
rom_data.inc** (carved `name:` 被 scan_existing_asm_labels 跳过, 0 残留); demo 块 2 串
(EXO_main.c/anmID) 由 demo-exodia-resources.s 处理, 排除。
- ⚠ 弯路 (3 版): data-equate(constants/assert_strings.inc) → rom_data.inc 自动 label → asm/assert_str_const.s
  的 .equ → **最终 carve `.asciz` 进 rom.s** (用户定: 槽用函数名前缀避重 + .word 加 EOL 原文 + 串本体写 rom.s)。

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
2. ✅ **batch-2 (0x14600..0x14a10, GL blend/brightness 簇 12 fn)** 完成 (见 §四.4.0a):
   gGlBlendState 符号化 + equate + 函数改名 + plate 订正; byte-identical。附带修复 1 个 pre-existing
   断言串 carve 回归。
   - 注: §五.0/batch-1 提到的 `reset_display_and_gl_state` plate 旧名 `FUN_08014398` 已在 batch-1
     订正 (现引 play_ui_effect_3a + indirect_table 说明), 全文件 plate 散文无 FUN_08014398 残留。
3. 下一批 (batch-3) 候选: 按地址序 `0x14398` 起的剩余簇 ——
   tick_prng_step_sequence / banlist_password_enter_char / 文本测量簇 (copy_str_unbounded,
   measure_text_pixel_width...) / BG VRAM 地址簇 (get_bgN_char_vram_addr, copy_to_bgN_*, 0x14a10..0x14e14) /
   GL 调色板管理簇 (gl_state_init, init_gl_palette_slot_flags @ 0x02023490, 0x1510c..)。
   建议优先 **BG VRAM 地址簇** (0x14a10..0x14e14, ~24 个小 getter/copy, 高度同构, R1 IO 寄存器密集)。
4. 每批后视情况更新本文「进度」表。

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
