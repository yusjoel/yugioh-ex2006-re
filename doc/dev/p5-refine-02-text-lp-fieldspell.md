# 函数/数据细化计划 — `asm/02_text_lp_fieldspell.s`

> 阶段目标: 把 `asm/02_text_lp_fieldspell.s` (ROM `0x0802C238 ~ 0x08035F54`, 游戏文本十进制渲染 +
> LP 条目查找 + 场地魔法发动判定 + equip chain 节点管理) **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **3** 个文件 (file 00 / file 01 已全 10 段完成, 见 `p5-refine-00-system-str-vija.md`
> 与 `p5-refine-01-vija-scene-text.md`)。方法论 + R1-R9 细化清单 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00/01 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**跨文件踩坑沿用** (file 00/01 沉淀):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式; 否则 GAS PC-relative
  "value too big") — 见 memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
  (proposal/review markdown 文档可中文, 仅写入 Ghidra .rep 的 plate/EOL 须 ASCII)
- carve byte-identical: host incbin 覆盖等式 `sum(spans)==原 size`; THUMB fn-ptr 表 `.word <fn>+1`,
  数据指针不 +1; `.asciz` 须含 NUL+对齐 pad; .hword RGB15 注意 bit15。
- **executor 严守段上界** (reviewer C1 逐槽地址裁定)。
- **C5 按值去重不分语义域** (file 01 Seg-8/9 反复): 新建常量前必扫全 18 个 constants/*.inc 确认无同值常量;
  REF/RENAME 不得绕过已存在常量值 (file 01 Seg-9 #6); 不建孤儿常量 (段内无槽持该值, file 01 Seg-9 #2)。
- **C13 残留 100% 覆盖** (file 01 Seg-7/8/9 均多轮 NEEDS_FIX): 段内 incbin 块外所有 DAT_/DWORD_/PTR_
  净数须被 EQ+REF+RENAME 去重全覆盖, 勿留"低优先级不处理"。
- **C8 stale 函数名** (file 01 Seg-9 #5): plate 中 `FUN_xxxx`/`PTR_FUN_xxxx` **完整字符串**匹配替换现名
  (禁子串匹配, 否则 PTR_PTR_ 双前缀); 函数内 LAB_ 跳转目标误标为函数名须订正。
- **R4 大块 disasm** (file 01 Seg-6/10): flow-disasm 会把 literal pool 当 THUMB 解码 →
  reference-manager 扫 PC-relative ldr 目标 createDWord 一次性全覆盖; mov pc,r0 派发表存裸 THUMB 地址 (无 +1);
  重跑前 clearListing 整 range 再 setTMode (避 ContextChangeException)。
- 复用 file 00/01 已建 carve label 与 constants/*.inc (duel_field.inc [file 01 大量新建] /
  ewram.inc / gba_mem.inc / oam_attr.inc / gfx_resource.inc / card_info.inc / name_input.inc /
  gl_blend.inc; gVijaState=0x02029eb0 / gDemoState=0x02029ec0 / gDuelSceneBase=0x02023360 /
  gDuelCardCtxBase=0x0201e2a0 / gDuelDispCtx=0x0203eeb0 / gCampaignDisplayState / gCampaignSpriteCtxBase)。

---

## 二、落地工作流 (pipeline)

同 file 00/01 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF02Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。

---

## 三、当前进度 (02_text_lp_fieldspell.s)

| Seg | 范围 | ~fn | ~slots | 状态 | commit |
|-----|------|-----|--------|------|--------|
| 1 | 0x2c238..0x2e108 | 23 | 318 | ✅ | (见 §四) |
| 2 | 0x2e108..0x2f3a8 | 23 | 94 | ⬜ | |
| 3 | 0x2f3a8..0x2fd00 | 23 | 58 | ⬜ | |
| 4 | 0x2fd00..0x309b8 | 23 | 136 | ⬜ | |
| 5 | 0x309b8..0x313dc | 23 | 60 | ⬜ | |
| 6 | 0x313dc..0x3217c | 23 | 64 | ⬜ | |
| 7 | 0x3217c..0x32e80 | 23 | 67 | ⬜ | |
| 8 | 0x32e80..0x33654 | 23 | 44 | ⬜ | |
| 9 | 0x33654..0x3407c | 23 | 63 | ⬜ | |
| 10 | 0x3407c..0x35f54 | 17 | 246 | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录 (0x0802c238..0x0802e108, 23 fn)

**函数列表**:
| addr       | name                                         |
|------------|----------------------------------------------|
| 0x0802c238 | render_game_text_decimal_to_line             |
| 0x0802c30c | render_card_name_format_to_line              |
| 0x0802c358 | render_card_name_escape_to_line              |
| 0x0802cba0 | init_jp_font_linebuf_for_render              |
| 0x0802cc08 | commit_glyph_linebuf_to_sprite_vram_with_index |
| 0x0802cc68 | init_card_name_result_screen                 |
| 0x0802cf98 | tick_scene_blend_fadeout_step                |
| 0x0802cfb4 | tick_scene_blend_fadein_step                 |
| 0x0802cfd4 | tick_scene_blend_fade_sequence               |
| 0x0802d074 | init_campaign_bg_and_obj_vram                |
| 0x0802d1a0 | init_opponent_card_bg_vram                   |
| 0x0802d25c | init_pack_selection_tile_vram_default        |
| 0x0802d2fc | init_pack_selection_tile_vram_by_deck_a      |
| 0x0802d3c4 | init_pack_selection_tile_vram_by_deck_b      |
| 0x0802d48c | init_duel_scroll_params                      |
| 0x0802d4bc | tick_opponent_aob_by_phase                   |
| 0x0802d58c | draw_card_name_label_to_sprite_vram          |
| 0x0802d638 | render_opponent_card_icon_and_name           |
| 0x0802d970 | render_dual_label_to_bg_vram                 |
| 0x0802dacc | setup_label_render_ctx                       |
| 0x0802db3c | dispatch_opponent_slot_oam_by_phase          |
| 0x0802de04 | init_opponent_card_display_vram              |
| 0x0802dfb8 | tick_opponent_aob_display                    |

**符号化统计**:
- EQ_SLOTS: 140 (含复用 EWRAM_BASE x12, GSETTINGS_OFFSET x11, gFontJpCtx x11, gDuelSceneBase x10, CARD_DESC_RENDER_PARAM x4, TEXT_RENDER_COLOR_MODE_1 x5, etc.)
- REF_SLOTS: 77 (carve label refs + game_str refs + existing label refs)
- RENAME_SLOTS: 60 (switchD pool slots + OAM constants + misc)
- PLATE_REWRITES: 4 (FUN_ -> current name; 3 plates had no stale FUN_ present)
- §5.1: 0 (本段无 ROM_INCBIN)
- disasm: 0 (本段无误标代码块)

**新建 constants** (写入现有 inc 文件):
- `gba_mem.inc`: RESULT_SCREEN_TILE_IDX_VRAM, RESULT_SCREEN_BG2CNT_INIT, RESULT_SCREEN_TILEMAP_TARGET, RESULT_SCREEN_FONT_CTX_OFF, RESULT_SCREEN_SPRITE_VRAM, AOB_CARD_TILE_VRAM, AOB_CARD_PAL_DST, AOB_INIT_MODE, AOB_DISPLAY_TILE_VRAM_A/B, OBJ_ICON_TILE_VRAM_BASE, OPP_CARD_NAME_TILE_VRAM, OBJ_PAL_ICON_BASE, OPP_CARD_LABEL_TILE_VRAM_A/B/C/D, OBJ_VRAM_BASE_1000, CAMPAIGN_BG_TILEMAP_BASE
- `duel_field.inc`: TEXT_RENDER_FLAG_LAYER2, DUAL_LABEL_RENDER_STATE_CLEAR, LABEL_CTX_RENDER_STATE_CLEAR, LABEL_CTX_DISPLAY_PARAM
- `card_info.inc`: GAME_STR_TEXT_BASE, CARD_ID_BASE_NEG_ADJ, PACK_DECK_A_KEY, OPP_CARD_NAME_STR_OFF_ES, OPP_CARD_NAME_STR_OFF_ES_NULL
- `ewram.inc`: JP_LANG5_STR_BASE, JP_LANG5_STR_OFFSET_ES, JP_LANG4_STR_PTR_DE, JP_LANG3_STR_PTR_FR, JP_LANG2_STR_PTR_IT, JP_LANG1_STR_PTR_EN, CAMPAIGN_BG1CNT_INIT, CAMPAIGN_BG2CNT_INIT, CAMPAIGN_TILEMAP_SEQ_START

**carve 26 label / 3 host**:
- Host A (old rom.s line 572, `.incbin 0x18972F0, 0x278EBC`): 17 new labels, 18 spans, sum=0x278EBC
  - aob_card_tile_src, aob_card_pal_src, aob_ptnsect_src, campaign_bg_pal_src_{a,b,c}, campaign_bg_tile_src, campaign_bg_tilemap_src, pack_deck_b_{pal,tile1,tile2,tile3,tilemap}_src, pack_deck_a_{tile1,tile2,tile3,tilemap}_src
- Host B (old rom.s line 660, `.incbin 0x1B8FB8C, 0x1CE18`): 8 new labels, 9 spans, sum=0x1CE18
  - result_screen_{pal2,tile1,tile2,tile3,tile4}_src, pack_default_{pal,tile,tilemap}_src
- Host C (old rom.s line 1633+, `.incbin 0x1E59DA8, 0xE54`): 1 new label, 2 spans, sum=0xE54
  - aob_phase_table

**复用 label (3 项, 不新建)**:
- name_o_palette_data @ rom.s line 685
- puzzle_challenge_record_array @ rom.s line 1647
- game_str_{ja,en,de,fr,it}_{0326,0327} (12 slots) @ data/game-strings-*.s

**落地踩坑记录**:
1. Ghidra REF(slot=0x0802dedc, target=0x020233ac, label='gDuelSceneBase'): 在 0x020233ac 创建了 'gDuelSceneBase' 标签; 导出时该槽变成 `.word gDuelSceneBase`; 但 gDuelSceneBase 实际地址=0x02023360 != 0x020233ac; build 出错。修复: 删除 0x020233ac 处的 USER label, 改为 RENAME_SLOT 保留原始值 `.word 0x020233ac`。
2. Proposal 中 game_str 语言标签 DE/IT 互换 (0x0802df04 = 0x09dec2de 实为 IT range, 非 DE); 导致 build 两处字节 swap。修复: RefineF02Seg1Fix.py 交换标签后 byte-identical 恢复。

**脚本**: `tools/ghidra-labeling/RefineF02Seg1Slots.py` + `RefineF02Seg1Fix.py` + `RefineF02Seg1Fix2.py`

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: (见 B6)

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 02 范围 `[0x0802c238, 0x08035f54)` (span 0x9D1C, 224 named fn [305 含 81 switchD 跳转表
> case 标签], 1152 DAT_/DWORD_/PTR_ 槽, 2 ROM_INCBIN) 按**函数数**均分 10 段 (~23 fn/段,
> 边界=函数起点)。文本渲染密集段 Seg-1 (318 槽) / Seg-10 (246 槽) 较重, 必要时拆 Seg-Na/Nb。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN | 备注 |
|---|---|---|---|---|---|
| Seg-1 | 0x2c238..0x2e108 | 23 | 318 | — | ✅ 文本十进制渲染 + 卡名格式化 + scene init |
| Seg-2 | 0x2e108..0x2f3a8 | 23 | 94 | **0x2e22c/0x19c, 0x2e554/0x144** | campaign card-select + opponent card display; 2 incbin (ref-scan 分类) |
| Seg-3 | 0x2f3a8..0x2fd00 | 23 | 58 | — | zone chain count / eligibility query |
| Seg-4 | 0x2fd00..0x309b8 | 23 | 136 | — | equip chain node find/link/replace 簇 |
| Seg-5 | 0x309b8..0x313dc | 23 | 60 | — | effect slot zone equip valid 判定 |
| Seg-6 | 0x313dc..0x3217c | 23 | 64 | — | equip card set-code / slot ref array |
| Seg-7 | 0x3217c..0x32e80 | 23 | 67 | — | zone slot chain refs clear/dispatch |
| Seg-8 | 0x32e80..0x33654 | 23 | 44 | — | monster slot count/state scan |
| Seg-9 | 0x33654..0x3407c | 23 | 63 | — | placeable monster slot find |
| Seg-10 | 0x3407c..0x35f54 | 17 | 246 | — | slot target eligibility full + fieldspell zone (重) |

执行约定同 file 00/01: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-01-vija-scene-text.md` (file 01 完整记录, equip/card 显示相关 carve label 与 constants)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
