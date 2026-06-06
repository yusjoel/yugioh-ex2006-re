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
| **batch-2: GL blend/brightness 簇 (12 fn)** | 0x14600..0x14a10 | ✅ R1/R2/R3/R5 完成 (见 §四.4.0a): gGlBlendState 符号化 + 4 equate + 1 函数改名 + 7 plate 订正; byte-identical。**附带修复 1 个 pre-existing 断言串 carve 回归 (assert_..._670 标签)** |
| **batch-3: BG VRAM 地址簇 (24 fn)** | 0x14a10..0x14e14 | ✅ R1/R2/R5 完成 (见 §四.4.0c): OBJ_TILE_VRAM_BASE equate(新 gba_mem.inc) + 8 auto-name 槽改名 + 2 plate 订正; byte-identical。簇本身 plate 已高质量 (sibling getter/copy), 细化以 R2 为主 |
| **batch-4: GL palette/OAM manager 簇 (7 fn)** | 0x1510c..0x1522c | ✅ R1/R2/R3/R5 完成 (见 §四.4.0d): gGlState=0x02023490 符号化(7 槽) + 3 cpu_set equate(新 gl_state.inc) + 7 plate 订正(含 2 处 0x02024330→0x02023d30 错址 + 0x22B B / 0x200→0x400 字节单位); byte-identical |
| **batch-5: GL_Scrollbar 簇 (11 fn)** | 0x15384..0x155f4 | ✅ R1/R2/R5 完成 (见 §四.4.0e): 5 字段位掩码 equate(新 gl_scrollbar.inc) + 7 槽改名 + 4 plate 过时 FUN_ caller 改现名; byte-identical。GL_Scrollbar* 传参(非全局) |
| **batch-6: NNS IG2D 资源加载管理器 (allocators + globals)** | 0x1563c..0x15b00 (散) | ✅ R3/R5/rename 完成 (见 §四.4.0f): 6 个 IG2D 全局符号化(gIg2dUsed{CellAnm,NceBuff,NanBuff}/NceBuffBase/CharPoolBase/CellAnmBank) + 函数改名 gl_clear_frame_callbacks→reset_ig2d_load_counters(误名) + 10 plate(含 5 外部 caller); byte-identical |
| **batch-7: BG affine matrix 簇 (4 fn)** | 0x15728..0x15924 | ✅ R3/R7/R2/R5 完成 (见 §四.4.0g): trig_table(512B)+assert_expr_zero **carve 进 rom.s** + GAS label 引用 + 3 槽改名 + 3 plate FUN_ 改现名; byte-identical |
| **batch-8: NNS G2D GFX entry accessor 簇 (10 fn)** | 0x16140..0x16268 | ✅ R1/R2/R5 完成 (见 §四.4.0h): 3 FourCC tag equate(BGDT/OBJD/PALT, 新 g2d_tags.inc) + 9 槽改名 + 10 plate 去过时槽引用; byte-identical |
| **batch-9: ISD affine matrix 指针簇 (3 fn)** | 0x16098..0x1613c | ✅ R3/R7/R2/R5 完成 (见 §四.4.0i): 3 个 ROM 数据 **carve 进 rom.s**(isd_affine_matrix_ptr_type4/type9 NULL 槽 + assert_expr_zero_65c) + 9 槽 GAS label 引用/改名 + 3 plate; byte-identical |
| **batch-10: ISD cell-anim OAM 簇 (2 fn)** | 0x15954..0x15ac4 | ✅ R3/R1/R2/R5 完成 (见 §四.4.0j): gOamAttrBuildBuf=0x030007f8(iwram.inc, OAM 属性构建暂存缓冲 128×8B=0x400B) + 2 attr2 char-name 字段掩码 equate(新 oam_attr.inc) + 2 槽改名(scale-shift 阈值/assert 行号) + 3 plate 散文符号化(含消费者 build_oam_attrs_from_cell_with_affine); byte-identical |
| **batch-11: NNS IG2D 资源加载族 (7 fn)** | 0x15b04..0x15e72 | ✅ R1/R3/R2/R5 完成 (见 §四.4.0k): OBJ_PALRAM_BASE=0x05000200(gba_mem.inc) + 16 个 assert-line DAT 槽改名(`<func>_assert_line_<hexlineno>` 避碰撞) + copy_pltt plate 散文符号化; byte-identical。load_nce/nanr/ncgr/nclr_*_from_file sibling + copy_pltt_data_to_vram_proxy + load_g2d_obj_resource_set hub; plate 已高质量, 细化以 R2 灭自动名为主 |
| **batch-12: NNS G2D 写族 前 2 fn** | 0x1626c..0x16342 | ✅ R1/R3/R2/R5 完成 (见 §四.4.0l): write_palt_block_to_vram(OBJ_PALRAM_BASE 复用 batch-11 + plate 0x05000000/0x05000200→GBA/OBJ_PALRAM_BASE) + dispatch_bg_screen_map_write(0xfff00000 raw-addr 判别掩码槽改名); byte-identical。write_tile_region_to_bg_screen(0x16344, med-conf struct 字段待 runtime) defer |
| 代码函数 (其余 ~194 个) | 0x14398..0x143f0, 0x14470..0x14600, 0x152b0..0x15384, 0x15674..0x15728, 0x15954..0x16098, 0x16140..0x16140, 0x1626c..0x1CB00 | ⬜ 函数已命名; 体内常量/指针/注释待细化 (LAB_ 内部分支按裁定跳过) |

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

### 4.0c batch-3 完成记录: BG VRAM 地址簇 (0x14a10..0x14e14, 24 fn) ✅

get_bgN_char_vram_addr ×4 / bgN_cnt_get_screen_size ×4 / calc_bg_screenmap_block_offset /
write_bg_scroll_pair / get_bgN_screen_vram_addr ×4 / get_obj_tile_vram_base /
copy_to_bgN_char_tiles ×4 / copy_to_bgN_screen_map ×4 / copy_to_obj_tile_vram。
读 BGnCNT 提取 char_base/screen_base/screen_size 字段算 VRAM 地址, 或 bios_cpu(_fast)_set
拷贝 tile/screen-map。byte-identical SHA1 9689337d。

**特点**: 本簇 plate 已高质量 (sibling getter/copy, 现名/公式/调用者齐全), 细化以 **R2 消灭
auto-name** 为主, R1 仅 1 个 pool 常量。

| 项 | 做法 | 数量 |
|---|---|---|
| R1 区基址 | data-equate `OBJ_TILE_VRAM_BASE`(0x06010000) @0x14c10; 新增 `constants/gba_mem.inc` (VRAM/OBJ/PALRAM/OAM 区基址参考表) | 1 槽 |
| R2 scroll 槽 | `DWORD_08014b84/b88`(BG0HOFS/BG0VOFS) → `write_bg_scroll_pair_ptr_bg0hofs/vofs` | 2 槽 |
| R2 assert-line | `DAT_*`(行 487/497/503/513/518) → `<func>_assert_line` | 5 槽 |
| R2 OBJ-base 槽 | `DAT_08014c10` → `get_obj_tile_vram_base_obj_tile_vram_base` (= equate 槽) | 1 槽 |
| R5 注释 | get_obj_tile_vram_base + copy_to_obj_tile_vram 的 `DAT_08014c10`/`0x06010000` → `OBJ_TILE_VRAM_BASE` | 2 plate |

新增: `constants/gba_mem.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineBgVramBatch3.py`。
注: `PTR_BGxCNT_xxxx` 槽 (~16 个) 按 batch-2 策略**跳过** (PTR 不在 R2 列表, 已显寄存器名;
`.word BG0CNT` 等已可读)。内联 VRAM 基址 (`0xc0<<0x13`=0x06000000) 为 movs+lsls 复合值, 无 pool
槽, 不符号化 (plate 已注)。

### 4.0d batch-4 完成记录: GL palette/OAM manager 簇 (0x1510c..0x1522c, 7 fn) ✅

get_gl_oam_entry_ptr / gl_state_init / init_gl_palette_slot_flags / fill_gl_palram_buf_0xf0 /
assign_palette_slot_entry / alloc_palette_entry_slot / copy_sprite_attr_table_to_oam。
全部操作 GL 主状态结构 gGlState (0x02023490, 0x8ac B)。byte-identical SHA1 9689337d。

**与 batch-2 配对**: 补全 0x02023480 (gGlBlendState) / 0x02023490 (gGlState) 这对相邻 GL 结构的命名。

| 项 | 做法 | 数量 |
|---|---|---|
| R2/R3 状态结构 | `gGlState=0x02023490` → ewram.inc .equ + Ghidra label + 7 槽 ref + 槽改名 `<func>_ptr_gl_state` (含字段布局: +0 OAM/affine, +0x400 palette entry, +0x800 slot_record, +0x880 palette_map, +0x8a0 计数器) | 7 槽 |
| R1 cpu_set 控制字 | data-equate `GL_STATE_INIT_FILL_CTRL`(0x0500022b) / `GL_PALRAM_FILL_CTRL`(0x05000100) / `GL_PALENTRY_ZERO_CTRL`(0x05000002); 新增 `constants/gl_state.inc` | 3 槽 |
| R5 注释订正 | 7 plate: 0x02023490→gGlState; **alloc 计数器错址 0x02024330→0x02023d30(=gGlState+0x8a0)**; gl_state_init `(0x22B B)`→`(0x8ac B=0x22b 字)`; fill_gl_palram `0x100 halfword(0x200 字节)`→`0x100 字(0x400 字节)` (bit26=32-bit, 对照 demo_state.inc CpuSet 解码) | 7 plate |
| R5 附带 | setup_isd_cell_anim_oam_entry (0x15954, 簇外) plate 里 propagated 的同一 0x02024330 错址订正 | 1 plate |

新增: `constants/gl_state.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineGlStateBatch4.py` + `FixIsdCounterAddr.py`。
注: tick_palette_fade_to_oam_palram (0x152b0) / init_scrollbar_oam_entry (0x15384) 不引用 gGlState
(用传入指针/OBJ PALRAM), 留后续批。内联 OAM VRAM 基址 (0xe0<<0x13=0x07000000) 无 pool 槽不符号化。

### 4.0e batch-5 完成记录: GL_Scrollbar 簇 (0x15384..0x155f4, 11 fn) ✅

init_scrollbar_oam_entry / get_scrollbar_range_param / compute_scrollbar_thumb_position /
get_scrollbar_cur_value / set_scrollbar_cur_pos / check_scrollbar_can_advance /
advance/retreat_scrollbar_pos_one / advance/retreat_scrollbar_pos_page /
update_scrollbar_thumb_display。源 GL/GL_Scrollbar.c。byte-identical SHA1 9689337d。

**特点**: GL_Scrollbar* 由 r0 传参 (非全局, 无 ewram label)。plate 已高质量 (字段布局/行号/
现名齐全), 细化以 R1 字段掩码 + R5 过时 caller 名为主。结构字段: +0w(attr,bit0 visible) /
+4 u16 cur_pos / +6 u16 total_count / +8 track_len / +9 margin_top / +a offset / +b visible_count /
+c w(bits[14:6] range_param, bits[23:15] Y base, bits[17:9] thumb pos)。

| 项 | 做法 | 数量 |
|---|---|---|
| R1/R2 字段掩码 | data-equate `SCROLLBAR_INIT_FILL_CTRL`(0x05000004) / `SCROLLBAR_KEEP_BITS_8_0`(0x1ff) / `SCROLLBAR_CLEAR_BITS_14_6`(0xffff803f) / `_23_15`(0xff007fff) / `_17_9`(0xfffc01ff); 新增 `constants/gl_scrollbar.inc` | 7 槽/5 常量 |
| R5 注释 | 4 plate 过时 FUN_ caller 改现名 (FUN_080155f4→update_scrollbar_thumb_display; FUN_08018d3c→tick_oam_palette_fade_settings; banlist_080186f0→read_banlist_char_at_scroll_pos; FUN_08018434→tick_name_input_scrollbar_and_anims; FUN_0801a794→tick_banlist_scrollbar_and_slot_anim) + thumb mask 名对齐 equate | 4 plate |

新增: `constants/gl_scrollbar.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineScrollbarBatch5.py`。

**defer (R4)**: 0x1550a 处 14 字节 `.byte` 块 (check_scrollbar_can_advance 与 advance_scrollbar_pos_one
之间) 反汇编为一个小函数 (adds/ldrh/orrs/lsrs#0x1f/bx lr, 取某字段最高位返回), Ghidra 误标为数据;
未在函数清单。独立 R4 案 (需 disasm+createFunction), 本批跳过, 留专项处理 (字节保持 .byte → byte-identical)。

### 4.0f batch-6 完成记录: NNS IG2D 资源加载管理器 (allocators + globals) ✅

alloc_nce_buff_slot (0x1563c) / alloc_char_data_slot (0x15674) / reset_ig2d_load_counters
(0x156ac, 原 gl_clear_frame_callbacks) / alloc_cell_anim_slot (0x15ac4) +
load_nce_cell_bank_from_file 等加载族引用。源 GL/IG2D_Main.c。byte-identical SHA1 9689337d。

**R3 6 个 IG2D 资源管理器全局** (NNS SDK assert 串直接给名, 高置信):

| 全局 | 地址 | 语义 |
|---|---|---|
| gIg2dUsedCellAnm | 0x03000bf8 | 已用 CellAnm 槽数 (max 0x40) |
| gIg2dUsedNceBuff | 0x03000bfc | 已用 NceBuff 槽数 (max 2) |
| gIg2dUsedNanBuff | 0x03000c00 | 已用 NanBuff/char 槽数 (max 2) |
| gIg2dNceBuffBase | 0x03000c08 | NceBuff 池基址 |
| gIg2dCharPoolBase | 0x03002c08 | char-data 池基址 |
| gIg2dCellAnmBank | 0x02027d40 | CellAnmBank (0x40×0x54 B) |

iwram.inc(前 5)+ewram.inc(CellAnmBank); 9 槽 ref+改名。

**函数改名**: `gl_clear_frame_callbacks` → `reset_ig2d_load_counters` (误名: 实清 bf8/bfc/c00
三个 used-count 计数器 = 释放所有 IG2D 加载槽, 与"帧回调"无关; indeg=6)。`bl` 6 处自动更新;
**5 个外部 caller plate** (reset_display_and_gl_state / init_banlist_pass_input_scene /
init_demo_shuen_display_state / reset_gl_display_state / 模块 21 GL scene init @0x80fd2f0) 的散文
名 + "清空帧回调队列"/"callbacks reset" 描述一并订正。CSV sync 完成。

新增脚本: `tools/ghidra-labeling/RefineIg2dLoadBatch6.py`。
注: load_*_from_file 加载族 (0x15b10..0x15d30) 的 assert-line DAT 槽 + 深度细化留后续批
(本批只接通其全局引用)。

### 4.0g batch-7 完成记录: BG affine matrix 簇 (0x15728..0x15924, 4 fn) ✅

compute_bg_affine_matrix_scaled / setup_oam_affine_matrix_from_scale /
apply_bg_affine_by_angle_scale / resolve_bg_affine_param_offset。源 GL/IG2D_Main.c。
BG/OAM 仿射矩阵 PA/PB/PC/PD 计算 (bios_div 求倒数 + trig 查表 + __muldi3 定点乘)。
byte-identical SHA1 9689337d。

| 项 | 做法 | 数量 |
|---|---|---|
| **R7 carve trig_table** | 表体 512B (0x1E399D0) 从 `.incbin 0x1E399CD+0x283` 切出 → rom.s `trig_table:` + 256 `.hword` (signed, 16/行, round-trip 验证) + 前 3B 对齐填充/后 0x80B 仍 incbin; 256 项 s16 cos/sin 查表, 幅值 256=Q8.8 的 1.0, 全圆 256 步 (sin(a)=trig[a], cos(a)=trig[a+0x40]) | 512 B |
| **R7 carve assert_expr_zero** | "0" 串 (0x1E3A4F8) 从 `.incbin 0x1E3A4F7+0x5` 切出 → rom.s `assert_expr_zero:` + `.asciz "0"` (前 1B/后 2B 仍 incbin); resolve_bg_affine_param_offset 的 assert(0) 表达式 | 1 串 |
| R3 GAS label 引用 | 2 槽从 data-equate/裸值切换为 carve label DATA ref (单一命名源): `.word trig_table` / `.word assert_expr_zero` | 2 槽 |
| R2 改名 | muldi3 定点舍入对 (0x800 lo/0x0 hi) | 2 槽 |
| R5 注释 | 3 plate FUN_ caller 改现名 (FUN_08015820→setup_oam_affine_matrix_from_scale; FUN_080ee654→alloc_affine_oam_entry_with_defaults; FUN_0801c668→apply_bg2_affine_fixed_angle) | 3 plate |

脚本: `tools/ghidra-labeling/RefineAffineBatch7.py` (符号化/改名/plate) + `CarveTrigTableAssertZero.py`
(equate→carve-label 切换)。**当场 carve, 不留待办** (用户标准: 细化即 carve 出数据表体)。
PTR_BG2X/BG2PA 槽按策略跳过 (已显寄存器名)。内联 FIXED_ONE(0x80<<0x11=0x01000000) 无 pool 槽不符号化。

### 4.0h batch-8 完成记录: NNS G2D GFX entry accessor 簇 (0x16140..0x16268, 10 fn) ✅

find_gfx_entry_by_tag (核心线性查找) + 9 个 tag-based accessor (get_bgdt/objd/palt_entry_* /
get_bgdt/objd_inline_data_ptr / get_bgdt/objd_second_blob_ptr / get_bgdt_entry_pixel_dimensions)。
源 GL/IG2D_Main.c。资源链表按 4 字节 FourCC tag 查找。byte-identical SHA1 9689337d。

| 项 | 做法 | 数量 |
|---|---|---|
| R1/R2 FourCC tag | data-equate `BGDT_TAG`(0x54444742='BGDT', 5 槽) / `OBJD_TAG`(0x444a424f='OBJD', 3 槽) / `PALT_TAG`(0x544c4150='PALT', 1 槽); 新增 `constants/g2d_tags.inc`; 9 槽改名 `<func>_<tag>` | 9 槽/3 常量 |
| R5 注释 | 9 accessor plate 去掉过时 `, DAT_/DWORD_xxx)` 槽引用 + find_gfx plate `tag_*`→`*_TAG` | 10 plate |

新增: `constants/g2d_tags.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineG2dTagsBatch8.py`。
注: write_palt_block_to_vram (0x1626c, 调色板写 VRAM) / dispatch_bg_screen_map_write (0x162dc) 非
纯 tag accessor (无 tag 槽, 按 caller tag 调用), 留后续批。

### 4.0i batch-9 完成记录: ISD affine matrix 指针簇 (0x16098..0x1613c, 3 fn) ✅

set_isd_affine_matrix_ptr_by_type / get_isd_affine_matrix_ptr_from_obj /
resolve_isd_affine_matrix_ptr。源 GL/ISD_Draw.c。按 affine_type {4=BG2, 9=BG3} 读写
ISD 仿射矩阵指针槽。byte-identical SHA1 9689337d。

**当场 carve 3 个 ROM 数据** (用户标准):

| carve label | 地址 | 内容 | 引用槽 |
|---|---|---|---|
| isd_affine_matrix_ptr_type4 | 0x09e587e4 | `.word 0x0` (type-4 矩阵指针, ROM 内 NULL) | 6 槽 (set/get/resolve ×2) |
| isd_affine_matrix_ptr_type9 | 0x09e587e8 | `.word 0x0` (type-9, NULL) | (同上) |
| assert_expr_zero_65c | 0x09e3a65c | `.asciz "0"` (类型 assert(0) 条件串) | 3 槽 |

从 `.incbin 0x1E50777+0x8595` (matrix 槽, off 0x806D) + `.incbin 0x1E3A65A+0x116` (assert, off 2)
切出。9 槽加 GAS label DATA ref + 改名 (`<func>_ptr_type4/9` / `_assert_expr_zero`)。

**语义注**: 矩阵指针槽在 ROM 内恒为 NULL; set_isd 的 `str r1,[槽]` 写 ROM 是 no-op (硬件只读),
故 get/resolve 恒返回 NULL —— 该 ISD 仿射路径在本 build 实际未启用 (carve 如实记录 NULL)。
assert "0" 与 batch-7 assert_expr_zero (0x09e3a4f8) 同内容不同 ROM 拷贝, 加 _65c 后缀避碰撞。

R5: set/get/resolve plate 的 DWORD_/DAT_ 槽引用改 carve label。
脚本: `tools/ghidra-labeling/RefineIsdAffineBatch9.py`。

### 4.0j batch-10 完成记录: ISD cell-anim OAM 簇 (0x15954..0x15ac4, 2 fn) ✅

setup_isd_cell_anim_oam_entry (0x15954) / dispatch_isd_cell_anim_oam_setup (0x15a8c)。
源 GL/IG2D_Main.c。核心 cell→OAM 构建: resolve affine offset/matrix → 断言 pCell → 循环
alloc_palette_entry_slot → build_oam_attrs_from_cell_with_affine 写暂存缓冲, 再逐项把 OAM
attr2 的 char-name (tile index) 与 palette nibble 做 base 重映射。byte-identical SHA1 9689337d。

| 项 | 做法 | 数量 |
|---|---|---|
| R3 暂存缓冲全局 | `gOamAttrBuildBuf=0x030007f8` → `constants/iwram.inc` .equ + Ghidra USER label + 槽 0x15a80 DATA ref + 改名 `setup_isd_cell_anim_oam_entry_ptr_oam_attr_build_buf`。**128 项 × 8 B = 0x400 B**, 终址 0x03000bf8 = gIg2dUsedCellAnm (边界吻合佐证) | 1 槽 |
| R1 OAM 字段掩码 | data-equate `OAM_ATTR2_CHARNAME_MASK`(0x3ff, 保留 attr2 bits[9:0]=char name) / `OAM_ATTR2_CHARNAME_CLEAR`(0xfffffc00, 清同字段); 新增 `constants/oam_attr.inc` | 2 槽/2 常量 |
| R2 槽改名 | 0x15a74(0x1ff: `cmp r5` 阈值, 选 scale-shift `asrs #5`/`asrs #9`) → `_scale_shift_threshold`; 0x15af8(0x127=295, alloc_cell_anim_slot assert 行号, batch-6 遗留) → `alloc_cell_anim_slot_assert_line` | 2 槽 |
| R5 注释 | 3 plate 的 `0x030007f8` 散文引用 → `gOamAttrBuildBuf`: setup (build_oam 调用 + side-effect) / setup_decimal_digit_oam_batch (0x15ea4, side-effect + OAM_BUF=) / **消费者** build_oam_attrs_from_cell_with_affine (0x080e969c, `[...at callsite]`) | 3 plate |

新增: `constants/oam_attr.inc` (接入 rom.s); 脚本 `tools/ghidra-labeling/RefineCellAnimOamBatch10.py`。
**消费者佐证 (R6)**: 读 build_oam_attrs_from_cell_with_affine (module 20) 确认 r0=pDst 即
gOamAttrBuildBuf, 每项写 attr0/attr1 对; attr2 char-name 字段 (bits[9:0]) 经 setup 循环加 tile-base
重映射 — 故 0x3ff/0xfffffc00 命名为 attr2 char-name 掩码 (非臆测, ldrh [r4+0x4]+lsls#0x16/lsrs#0x16 取低 10 位佐证)。
注: 内联 0xf palette nibble 掩码 / rsbs 取负 (-0x11/-0x4) 无 pool 槽, 不符号化 (沿用 batch-2 策略)。

### 4.0k batch-11 完成记录: NNS IG2D 资源加载族 (0x15b04..0x15e72, 7 fn) ✅

invoke_fs_load (0x15b04, thin wrapper, 已干净) / load_nce_cell_bank_from_file (0x15b10) /
load_nanr_anim_bank_from_file (0x15b70) / load_ncgr_char_data_from_file (0x15bd0) /
load_nclr_pltt_data_from_file (0x15c30) / copy_pltt_data_to_vram_proxy (0x15c90) /
load_g2d_obj_resource_set (0x15d30, hub indeg=6)。源 GL/IG2D_Main.c。NCE/NANR/NCGR/NCLR
四类 G2D 资源 FS 加载 + 解析 + VRAM 写入。byte-identical SHA1 9689337d。

**特点**: 本族 plate 已高质量 (sibling load 函数, assert 行号/调用链/参数齐全), 细化以 **R2 灭
自动名** 为主 + 1 个 R1/R3 区基址。

| 项 | 做法 | 数量 |
|---|---|---|
| R1/R3 OBJ 调色板基址 | data-equate `OBJ_PALRAM_BASE`(0x05000200) @0x15ce4 (copy_pltt DMA 目标); 加入 `constants/gba_mem.inc` (= PALRAM+0x200, OBJ/sprite 16 调色板) | 1 槽 |
| R2 assert-line 槽 | 16 个 `DAT_` line-number 槽 → `<func>_assert_line_<hexlineno>` (load_g2d hub 含 4 个 pBuf 断言行号不同 0x32d/331/355/36a, 故用 hex 行号后缀避碰撞; 另 nce 199/nanr 1c1/ncgr 23e+23f/nclr 266+267/copy_pltt 2d9+2da+2e3) | 16 槽 |
| R5 注释 | copy_pltt_data_to_vram_proxy plate 2 处 `0x05000200` → `OBJ_PALRAM_BASE` | 1 plate |

新增脚本: `tools/ghidra-labeling/RefineIg2dLoadBatch11.py`。`constants/gba_mem.inc` 追加 OBJ_PALRAM_BASE。
注: 各 load 函数另有 1 条 assert 行号是**内联**计算 (`movs r1,#N; lsls r1,#1`, 如 nce 0x198=`0xcc<<1`),
无 pool 槽不符号化。assert 串本体槽 (`_assert_<expr>_null` 等) 已由 4.0b 全 ROM 断言串 carve 处理。
其余 0x05000200 字面量槽 (write_palt_block_to_vram 0x162bc / 模块 01/15) 留各自批次符号化。

### 4.0l batch-12 完成记录: NNS G2D 写族 前 2 fn (0x1626c..0x16342) ✅

write_palt_block_to_vram (0x1626c) / dispatch_bg_screen_map_write (0x162dc)。源 GL/IG2D_Main.c。
PALT 调色板块写 PALRAM (按 type 选 BG/OBJ 调色板) + BG screen-map 写入分派 (raw-addr 直写
或 bg_index+offset 分派到 copy_to_bgN_screen_map)。byte-identical SHA1 9689337d。

| 项 | 做法 | 数量 |
|---|---|---|
| R1/R3 OBJ 调色板基址 | data-equate `OBJ_PALRAM_BASE`(0x05000200, **复用 batch-11 gba_mem.inc 常量**) @0x162bc + 槽改名 `write_palt_block_to_vram_obj_palram_base` | 1 槽 |
| R2 判别掩码 | 0x162fc(0xfff00000, 测 dst 高 20 位判 raw-addr/offset 两路径) → `dispatch_bg_screen_map_write_raw_addr_mask` | 1 槽 |
| R5 注释 | write_palt plate 2 处: `0x05000000`→`GBA_PALRAM_BASE` (BG 调色板) + `0x05000200`→`OBJ_PALRAM_BASE` (OBJ 调色板) | 1 plate |

脚本: `tools/ghidra-labeling/RefineG2dWriteBatch12.py` (无新增 constants, 复用 gba_mem.inc)。
注: BG 调色板基址 0x05000000 由 `movs r0,#0xa0; lsls r0,#0x13` (=0xa0<<0x13) 内联合成, 无 pool
槽不符号化 (plate 已注)。**defer**: write_tile_region_to_bg_screen (0x16344) 体大且 plate 自标
med-conf (r6 struct +0x14/+0x15/+0x16 字段布局待 runtime verify) + 含 0x02023d40 全局, 留专项批。

### 4.0m Seg-1a 完成记录: b1 残留 3 defer 槽 (demo scene) ✅

地址序 Seg-1 第一部分: 回填 batch-1 当年 R8 诚实 defer 的 3 处 demo-scene 槽。byte-identical 9689337d。

| 残留 | 函数 | 做法 |
|---|---|---|
| 0x13674/78/7c | setup_demo_sprite_entry (0x13578) | **区域/语言检测**: 0x080000ae→`ROM_REGION_CODE_ADDR` equate(新 `constants/rom_region.inc`) + 0x02000000/0x6c2c 槽改名(`_ewram_base`/`_gsettings_offset` + EOL); plate R5 订正 (旧误称 "JP BIOS version byte" → ROM game-code 区域字符 + gSettings(0x02006c2c) language_id bits[2:0], 既有 ewram.inc gSettings 名) |
| 0x13ab8 | setup_demo_cell_anim_slot (0x13a6c) | assert 行号槽 0x14b=331 → `_assert_line_14b` |
| 0x13c00 | tick_demo_scene_state_machine (0x13bd4) | 10-case 状态机跳转表基址槽 → `_state_jump_table_ptr` + DATA ref→表 0x13c04 + EOL (switchD 表标签保留) |

新增: `constants/rom_region.inc` (ROM_REGION_CODE_ADDR/REGION_CODE_JP/REGION_LANG_ID_MASK; 接入 rom.s)。
脚本: `tools/ghidra-labeling/RefineSeg1aDemoResiduals.py`。**§5.1 登记: 无** (3 槽均有引用, 当场符号化)。
关键发现: 0x02006c2c 早已在 ewram.inc 定义为 `gSettings` (language_id), 故复用既有名, 未新建常量。

### 4.0n Seg-1b 完成记录: 0x14398..0x14600 gap (7 fn) ✅

地址序 Seg-1 第二部分: b1→b2 之间 7 个未细化函数 (PRNG/demo-phase + banlist 密码 + 文字测量簇)。
byte-identical 9689337d。

| 函数 | 做法 |
|---|---|
| tick_prng_step_sequence (0x14398) | **误名订正 → RENAME `step_demo_scene_phase`**: 实为 demo 场景阶段分派器 (仅用 gPrng 地址当 base, 经 +0x204 读 gDemoSceneInitPhase=0x03000244 bits[21:14] 阶段索引)。**R7 carve `demo_scene_phase_table`** (0x09e587d4, 3 THUMB fn ptr `+1` + NULL: reset_display_and_gl_state/load_demo_obj_resource_slot0/tick_demo_scene_state_machine, 从 incbin 末 0x10B 切出) + 表/gPrng base/phase-clear-mask 槽改名 + plate 全重写 + CSV sync |
| banlist_password_enter_char (0x143f0) | gSettings(0x02006c2c via base+offset) 槽改名 + **gTextEncodingOverride=0x0202348c** 符号化 |
| copy_str_unbounded (0x14470) | 0x05f5e0ff 无上限哨兵槽改名 |
| append/advance/count/measure (0x14480/144e8/1455c/145bc) | gSettings base+offset 槽改名(各 2) + gTextEncodingOverride 符号化(各 1) + plate 0x0202348c→符号 |

**新全局**: `gTextEncodingOverride=0x0202348c` (ewram.inc, TCG/OCG 编码覆盖; **物理在 gGlBlendState
footprint 内但逻辑独立** —— 10+ refs 全文字函数, 0 blend; blend 结构仅用 +0/+4/+8, 已验证);
`gDemoSceneInitPhase=0x03000244` (iwram.inc, 参考; 经 gPrng+0x204 访问无直接槽)。
脚本: `tools/ghidra-labeling/RefineSeg1bTextPrng.py`。**§5.1 登记: 无** (STEP_TABLE 有引用 → 当场 carve)。
**Seg-1 完成** (Seg-1a 残留 + Seg-1b gap)。下一段 Seg-2 (0x14838..0x14fa8, 含 carve 0x14e54/76B)。

### 4.0o Seg-2 完成记录: 0x14838..0x14fa8 (b2-tail + b3 + gap, register-only) ✅

Seg-2 大部分已被旧 batch-2/batch-3 细化; 新增工作仅为**§5.1 登记** (无 Ghidra 改动 / 无 build):

| 函数/区段 | 状态 |
|---|---|
| 0x14838..0x14a10 | ✅ batch-2 GL blend/brightness 已细化 |
| 0x14a10..0x14e14 | ✅ batch-3 BG VRAM 簇 24fn 已细化 |
| copy_to_obj_tile_vram (0x14e14, b3 末) | ✅ 已细化 (槽 0x14e4c/50 已符号化为 _gl_common_c_filename / _assert_u32_psrc_0x3_0) |
| **ROM_INCBIN 0x14e54/0x4c** | **§5.1 登记** (3 个 THUMB 孤儿小函数, 0 ROM 引用; 与 batch-3 BG VRAM 同模式但操作 ptr-to-BGnCNT-copy; Ghidra 未识别) |
| measure_str_bytelen (0x14ea0) | ✅ 已干净 (plate 完整, 无 pool 槽) |
| find_substr_offset (0x14eb4) | ✅ 已干净 (3 pool 槽已经全局 assert carve 符号化) |
| fs_resolve_path_to_fid (0x14f54) | ✅ 已干净 (plate 完整, 无 pool 槽) |
| **0x14f9c .byte 14B 孤儿 thunk** | **§5.1 登记** (`fs_load_no_flag` wrapper, 0 ROM 引用; `.byte` 形式未违反 Rule 2) |
| fs_load (0x14fa8) | → **Seg-3 起点**, 留 Seg-3 处理 |

byte-identical 保持 9689337d (无任何 Ghidra/asm 改动)。Seg-2 完成, 进入 Seg-3。

### 4.0p Seg-3a 完成记录: fs_load (0x14fa8..0x1510a) ✅

Seg-3 起点。fs_load 是 FS 路径解析+解压 hub: ① 用 #/!/.LZ 3 个魔数 prefix 探测路径 →
② 据 gSettings language_id (bits[2:0]) 把 # 替换为 j/e/g/f/i/s; ROM region byte 把 ! 替换
为 'J' / 'E' → ③ fs_resolve_path_to_fid 查 FID → ④ LZ77/Huff 解压。9 个 pool 槽全符号化。
byte-identical 9689337d。

| 项 | 做法 | 数量 |
|---|---|---|
| **R7 rom.s carve** | 把 `.incbin 0x1E39979, 0x3F` (63B) 切为: 3B 对齐填充 + `fs_key_lz_suffix`(".LZ") + `fs_key_hash`("#") + `fs_key_excl`("!") + 6 个 `fs_lang_char_<j/e/g/f/i/s>` (每个 4B 对齐) + `fs_language_char_ptr_table` (6 .word ptr 表) | 1 incbin → 10 labels |
| R3 carve label ref | 4 个 fs key/table 槽 (0x1507c/15080/15090/15098) → carve label DATA ref + 改名 `fs_load_ptr_key_<hash/excl/lz_suffix>` / `_ptr_language_char_table` | 4 槽 |
| R3 新全局 | `gFsDecompBuf`=0x0200af20 (ewram.inc, FS LZ77 解压暂存缓冲) + 槽 0x1509c ref + 改名 | 1 槽/1 全局 |
| R1 区域字节 | ROM_REGION_CODE_ADDR=0x080000ae equate (Seg-1a 复用) @0x15094 + 改名 | 1 槽 |
| R2 EWRAM base+offset | 0x15088/0x1508c → `fs_load_ewram_base` / `fs_load_gsettings_offset` (gSettings 0x02006c2c pattern, 同 Seg-1a/1b) | 2 槽 |
| R2 VRAM 边界 | 0x150a0 (0x05ffffff = 0x06000000-1) → `fs_load_vram_boundary_threshold` + EOL (LZ77→gFsDecompBuf vs 直接 huff 到 dest 判别) | 1 槽 |

新增: `gFsDecompBuf` (ewram.inc); 脚本: `RefineSeg3aFsLoad.py`。
**踩坑修复**: Seg-1b `copy_str_unbounded_len_sentinel` + Seg-3a `fs_load_vram_boundary_threshold`
2 个 EOL 含 CJK → Ghidra Jython 双重 UTF-8 编码 mojibake (feedback_jython_unicode_plate_comment.md
再确认)。脚本 `FixSeg1bSeg3aEOLAscii.py` 重写为纯 ASCII; **规则**: Ghidra 设的 EOL/plate 一律避免
CJK, 必要解释走 doc/dev/。**§5.1 登记: 无** (10 个 carve label 均有引用)。

### 4.0q Seg-3b/3 完成记录: 0x1510a..0x1571c (b4/b5/b6 复用 + R5 + §5.1) ✅

| 区段/函数 | 处理 |
|---|---|
| 0x1510c..0x1522c | ✅ b4 GL palette/OAM 7fn 已细化 (零自动名残留) |
| **0x1522c..0x15384 gap** | ✅ tick_palette_fade_to_oam_palram (0x152b0) 已细化 (plate 完整, 无 pool 槽残留) |
| 0x15384..0x155f4 | ✅ b5 GL_Scrollbar 11fn 已细化 |
| **ROM_INCBIN 0x1547e/0x26** | **§5.1 登记** (3 个 GL_Scrollbar 字段孤儿小函数, 0 ROM 引用) |
| **0x1550a .byte 14B** | **§5.1 登记** (1 个谓词函数 "字段非零?", 0 引用) |
| 0x155f4..0x1563c update_scrollbar_thumb_display | ✅ b5 末细化 |
| 0x1563c..0x15724 IG2D allocators (b6) | ✅ batch-6 IG2D 资源加载管理器已细化 |
| 0x156d0..0x1571c cell-anim accessor | ✅ 已细化 (4 fn; `get_anim_ctrl_seq_id` R5 plate 旧 DWORD_08015710/14 → 现槽名, byte-identical) |
| **0x156ec .byte 6B** | **§5.1 登记** (1 个 setter `str r1,[r0,#0xc]`, 0 引用) |
| 0x1571c..0x15728 dispatch_cell_anim_frame_advance | ✅ b6 边缘已细化 (plate 完整, 无 pool 槽) |

byte-identical 9689337d 保持。脚本: `RefineSeg3bGetAnimCtrl.py` (单 plate R5)。**Seg-3 完成**。

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

### 4.2 代码函数内部细化 (主体工作量, 284 fn)
范围 `0x13510..0x1CB00`。**执行计划见 §五 地址序路线图 (Seg-1..Seg-10)**——已于 2026-06-06
按用户 3 条硬规则重排为严格地址序 (取代原"子系统聚类")。每段走「代码侧 pipeline」, 段内逐函数
+ 函数间 ROM_INCBIN 一并细化。

每个函数细化清单: R1 常量 + R2 标签 + R3 引用接通 + R4 误标数据 + R5 注释 + R7 数据 carve +
R9 byte-identical。

参考: 系统/SDK 风格函数 (g2d/中断/newlib) 除 refs/pokeruby 外, 也查 **refs/NITRO SDK v2.0RC3**
(NitroSDK 早期亦覆盖 GBA, 见 memory reference-nitrosdk-gba)。

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> **2026-06-06 重排 (用户定 3 条硬规则, 取代旧"子系统聚类"方式)**:
> 1. **严格地址序**, 不按子系统/难度。整个代码区 `0x13510..0x1CB00` (284 fn) 按地址均分 **10 段
>    (Seg-1..Seg-10)**, 每段 ~28 fn, **段边界 = 某函数结束处** (不切断函数)。按 Seg 序号执行,
>    段内从低地址往高地址逐函数细化, 不回头不跳号。
> 2. **函数间数据也要细化**: 段内出现的 `ROM_INCBIN <off>, <size>` (Ghidra 未分化的函数间数据)
>    **不允许保留**——当场 carve 进 rom.s (label + 结构化 `.byte`/`.word`/`.asciz`) 或反汇编成
>    指令/函数 (R4/R7), round-trip 验 byte-identical。
> 3. **唯一例外**: 若该数据**全 ROM 无任何引用** (grep `.word <addr>` / DATA ref 皆空), 允许暂不
>    carve, 在下方「§5.1 未引用数据登记表」标记, 留以后处理 (引用到时再切)。
>
> 旧 batch-1..12 (子系统聚类, 已完成, byte-identical) 记录见 **§四 4.0/4.0a..4.0l + §三 进度表**,
> 作为历史保留; 其覆盖映射到下表 "旧覆盖" 列。新执行单位是 **Seg-N**。

| Seg | 地址范围 | ~fn | 内含 ROM_INCBIN (必 carve/或登记) | 旧覆盖 | 剩余工作 (本轮要做) |
|---|---|---|---|---|---|
| **Seg-1** | 0x13510..0x14838 | ~30 | — | b1, b2(头) | b1 残留 3 defer 槽 (0x13674 ROM头JP探测/0x02006c2c 全局 + 0x13ab8 assert行号 + 0x13c00 hub跳转表基址) + **0x14398..0x14600 gap 7 fn** (tick_prng_step_sequence / banlist_password_enter_char / copy_str_unbounded / append_text_to_buf_charlen / advance_text_ptr_by_charlen / count_str_charlen / measure_text_pixel_width) |
| **Seg-2** | 0x14838..0x14fa8 | ~28 | **0x14e54/0x4c** | b2(尾), b3 | 0x14e14..0x14fa8 gap fn + **carve 0x14e54 (76B)** |
| **Seg-3** | 0x14fa8..0x1571c | ~28 | **0x1547e/0x26** | b4, b5, b6(部分), b7(头) | 0x14fa8..0x1510c / 0x1522c..0x15384 (tick_palette_fade) / 0x155f4..0x1563c / 0x15674..0x1571c gap fn + **carve 0x1547e (38B)** + **R4: 0x1550a 14B `.byte` 误标小函数** disasm+createFunction |
| **Seg-4** | 0x1571c..0x16218 | ~28 | **0x15d18/0x18, 0x15fe8/0x2c, 0x16074/0x24** | b7, b10, b11, b9, b8(部分) | 0x15924..0x15954 / 0x15e72..0x16098 gap fn + **carve 3 incbin** + zero_struct_36bytes cpu_set 控制字槽 (0x01000012) + **R4: 0x1604c jump-table 分派器** (含 0x16060 跳转表 + 0x16074..8c 5×6B handler, 均误标数据) disasm+createFunction |
| **Seg-5** | 0x16218..0x1794c | ~28 | **0x169d6/0x16, 0x16a20/0x5c, 0x170d4/0xfc, 0x17424/0x40** | b8(尾), b12 | **0x16344 起几乎全新** (write_tile_region_to_bg_screen 含 0x02023d40 全局 med-conf + G2D 系) + **carve 4 incbin (含 252B 大块 @0x170d4)** |
| **Seg-6** | 0x1794c..0x18774 | ~28 | **0x186ce/0x22** | — | **全新**: 字符串/文本渲染簇 (render_jp_string_row ...) + carve 0x186ce (34B) |
| **Seg-7** | 0x18774..0x19a58 | ~28 | **0x19640/0x20** | — | **全新**: name_input/banlist 场景 + carve 0x19640 (32B) |
| **Seg-8** | 0x19a58..0x1a794 | ~28 | — | — | **全新**: banlist password 渲染簇 |
| **Seg-9** | 0x1a794..0x1b850 | ~28 | **0x1a89c/0x20, 0x1ad18/0xec** | — | **全新**: banlist/shuen + **carve 2 incbin (含 236B 大块 @0x1ad18)** |
| **Seg-10** | 0x1b850..0x1cb00 | ~32 | — | — | **全新**: vija/shuen 场景 tick (tick_*_obj_anim ...) |

执行约定:
- 每个 Seg 走 §二「代码侧 pipeline」(备份 .rep → Ghidra 脚本 → 重导出 → split → build → byte-identical
  SHA1 9689337d → 函数改名才 CSV sync)。Seg 内可分多次提交, 但**地址序不回头**。
- 每个函数细化清单: R1 常量 + R2 标签 + R3 引用接通 + R4 误标数据反汇编 + R5 注释 + R7 数据 carve
  + R9 byte-identical。
- 已被旧 batch 细化干净的函数 (旧覆盖列) 跳过, 只补 gap 函数 + carve incbin + 清残留 DAT。
- 每完成一段, 更新 §三 进度表 + 下方登记表。

### 5.1 未引用数据登记表 (规则 3: 全 ROM 无引用, 暂不 carve, 留后)

> 执行 Seg 时遇 ROM_INCBIN 先 grep 引用; 有引用→当场 carve; **无引用→登记此表**, 注地址/大小/
> 所在 Seg/初判内容, 引用到时再切。(初始为空, 逐 Seg 填。)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| 0x08014e54 | 76 B | Seg-2 | **3 个 THUMB 孤儿小函数 (Ghidra 未识别为代码)**: ①0x14e54 (24B) `sub sp,#4;ldrh;mov;strh;ldr [sp]` 从 u16 ptr 取 bits[3:2]×0x4000 + VRAM_BASE (char_base addr); ②0x14e70 (20B) 同壳取 bits[15:14] 返回 screen_size 值 (0..3); ③0x14e84 (28B) 同壳取 bits[12:8]×0x800 + VRAM_BASE (screen_base addr)。**与 batch-3 BG VRAM 族同模式但操作 ptr-to-BGnCNT-copy 而非 register**。**ROM 内 0 引用** (扫描 ROM_BASE+1 / 原值均零真匹配)。**留待**: 引用到时按 R4 disasm + createFunction (Ghidra 反汇编 + 4-byte 对齐 alignment pad) |
| 0x08014f9c | 14 B | Seg-2 | **1 个 THUMB 孤儿 thunk (`.byte` 块, 非 ROM_INCBIN)**: 0x14f9e `push lr;movs r1,#0;bl fs_load;pop r0;bx r0` = `fs_load_no_flag(path)` wrapper (强制 flag=0)。**ROM 内 0 引用**。**留待**: 引用到时 R4 disasm。注: 已是 `.byte` 形式, 未违反 Rule 2 |
| 0x0801547e | 38 B (`ROM_INCBIN 0x1547e, 0x26`) | Seg-3 | **3 个 THUMB 孤儿 GL_Scrollbar 字段小函数**: ①0x15480 (8B) `bits[5:2] getter` (`ldrb [r0];lsls#0x1a;lsrs#0x1c;bx lr`); ②0x15488 (8B) `bit[0] getter` (`ldrb [r0];lsls#0x1f;lsrs#0x1f;bx lr`); ③0x15490 (18B) `bit[0] setter from r1&1` (read-modify-write [r0])。**ROM 内 0 引用** (全 ROM 扫 raw+THUMB+1 均零)。**留待**: 引用到时 R4 disasm |
| 0x0801550a | 14 B (`.byte` 块, 非 ROM_INCBIN) | Seg-3 | **1 个 THUMB 孤儿谓词函数**: 0x1550c `adds r1,r0,#0;ldrh r2,[r1+4];rsbs r0,r2,#0;orrs r0,r2;lsrs r0,#0x1f;bx lr` = "返回 [r0+4] 的 u16 字段是否非零 (0/1)" 谓词。**ROM 内 0 引用**。**留待**: R4 disasm |
| 0x080156ec | 6 B (`.byte` 块, 非 ROM_INCBIN) | Seg-3 | **1 个 THUMB 孤儿 setter**: 0x156ee `str r1,[r0,#0xc];bx lr` = `void f(void* p, u32 val) { p[+0xc]=val; }`。**ROM 内 0 引用**。**留待**: R4 disasm |

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
