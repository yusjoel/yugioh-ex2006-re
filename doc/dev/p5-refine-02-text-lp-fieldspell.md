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
| 1 | 0x2c238..0x2e108 | 23 | 318 | ✅ | 4199405 |
| 2 | 0x2e108..0x2f3a8 | 23 | 94 | ✅ | cd981d8 |
| 3 | 0x2f3a8..0x2fd00 | 23 | 58 | ✅ | a78e8b1 |
| 4 | 0x2fd00..0x309b8 | 23 | 136 | ✅ | f8cdb43 |
| 5 | 0x309b8..0x313dc | 23 | 60 | ✅ | 1ad7df7 |
| 6 | 0x313dc..0x3217c | 23 | 64 | ✅ | 8051a2e |
| 7 | 0x3217c..0x32e80 | 23 | 67 | ✅ | f12c5fe |
| 8 | 0x32e80..0x33654 | 23 | 44 | ✅ | 9892a81 |
| 9 | 0x33654..0x3407c | 23 | 63 | ✅ | 77760ad |
| 10a | 0x3407c..0x35280 | 10 | 148 | ✅ | dc67250 |
| 10b | 0x35280..0x35f54 | 7 | 98 | ✅ | (pending) |

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

**commit**: 4199405

---

### 4.02 Seg-2 完成记录 (0x0802e108..0x0802f3a8, 23 fn)

**函数列表**:
| addr       | name                                          |
|------------|-----------------------------------------------|
| 0x0802e108 | tick_campaign_card_select_display_state       |
| 0x0802e918 | tick_aob_display_with_sprite_enable_blend     |
| 0x0802e938 | tick_aob_display_with_fadein                  |
| 0x0802e95c | find_active_equip_chain_head                  |
| 0x0802e988 | replace_slot_chain_ref_by_id                  |
| 0x0802ea3c | replace_chain_refs_by_slot_id_for_player      |
| 0x0802eac8 | link_equip_node_to_chain                      |
| 0x0802eb3c | append_equip_chain_node_at_tail               |
| 0x0802eb94 | replace_chain_refs_for_slot                   |
| 0x0802ebbc | replace_chain_refs_by_id_filtered             |
| 0x0802ebfc | replace_equip_chain_slot_refs_by_match        |
| 0x0802ec3c | replace_chain_node_ref_by_zone_match          |
| 0x0802ec80 | clear_chain_refs_for_low_zone_nodes           |
| 0x0802ecbc | clear_equip_refs_for_leaving_slot             |
| 0x0802edac | clear_equip_chain_refs_for_slot_zone          |
| 0x0802edf0 | repair_slot_equip_chain_node_refs             |
| 0x0802eeac | rebuild_equip_chain_refs                      |
| 0x0802ef84 | purge_equip_chain_refs_for_zone_slot          |
| 0x0802f0d8 | clear_zone_slot_card_ref_bits                 |
| 0x0802f14c | update_equip_chain_zone_slot_refs             |
| 0x0802f1f8 | count_slot_chain_copies_of_card               |
| 0x0802f27c | count_zone_chain_eligible_cards               |
| 0x0802f394 | count_equip_chain_default_flags               |

**符号化统计**:
- EQ_SLOTS: 36 (PLAYER_BLOCK_STRIDE x13 复用 ewram.inc, CAMPAIGN_CARD_ANIM_STEP_MASK x4 复用, gDuelSceneBase x8 复用, FIELD_SLOT_PHASE_MASK x3 新建, NODE_POOL_NEG_OFFSET x4 新建, EQUIP_CHAIN_LINK_OFFSET x1 新建, EQUIP_NODE_BASE_OFFSET x2 新建, gPrng x1 复用)
- REF_SLOTS: 32 (gDuelFieldSlots x10, gEquipNodePool x15, gDuelFieldSlotState x2, gEquipChainSlotRefs x1, deck_type_table x2, scene_scroll_table x1, dispatch_table_seg2_blk1 x1)
- RENAME_SLOTS: 22 (dispatch tbl ptrs x2, sprite attrs x2, equip chain offsets x6, sentinel/masks x5, type thresholds x4, card_id masks x2, sub_dispatch x1)
- PLATE_REWRITES: 6 stale FUN_ replacements
- §5.1: 0 (两 ROM_INCBIN 均有引用, 走 R4 disasm)
- disasm: Block1 181 instr + Block2 145 instr = 326 total (2 blocks, MOV PC dispatch)
- literal pool: 8 DWord fixes (7 Block1 + 1 Block2 missing pool)

**新建 constants**:
- `duel_field.inc`: FIELD_SLOT_PHASE_MASK, EQUIP_NODE_BASE_OFFSET, NODE_POOL_NEG_OFFSET, EQUIP_CHAIN_LINK_OFFSET
- `ewram.inc`: gDuelFieldSlots, gEquipNodePool, gEquipChainSlotRefs, gDuelFieldSlotState

**carve 2 sub-splits** (Host C tail 子分裂):
- aob_phase_table body: `.incbin 0x1e59db4, 0x10` (unchanged content, new span)
- deck_type_table @ 0x09e59dc4: `.incbin 0x1e59dc4, 0x10` (8 u16 deck_type->sprite_tile_offset)
- scene_scroll_table @ 0x09e59dd4: `.incbin 0x1e59dd4, 0xe28` (0x20-entry scroll pos table)
- sum: 0x10+0x10+0xe28=0xe48 == 原 tail 大小 ✅

**落地踩坑记录**:
1. PLAYER_BLOCK_STRIDE=0x868 在 ewram.inc line 245 已有 (proposal 拟新建 FIELD_PLAYER_STRIDE=0x868 在 duel_field.inc — 重复建立); 修正: 直接复用 ewram.inc 已有常量, 不新建。
2. Ghidra 导出 Block1 literal pool 为 .byte 而非 .word (7 个池项未自动建 DWord); 追加 RefineF02Seg2LiteralPool.py 脚本修复 (8 个 createDWord: 7 Block1 + 1 Block2)。
3. PLATE_REWRITES 全 6 处 WARN "not found in plate" — 相关 plate 已无 FUN_ stale 串 (可能原始 plate 不含 / 已被先前操作清除); 不影响落地。

**脚本**:
- `tools/ghidra-labeling/RefineF02Seg2Slots.py` (EQ36/REF32/RENAME22/PLATE6)
- `tools/ghidra-labeling/DisassembleF02Seg2Blocks.py` (Block1 181i + Block2 145i)
- `tools/ghidra-labeling/RefineF02Seg2LiteralPool.py` (8 DWord pool fix)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: cd981d8

---

### 4.03 Seg-3 完成记录 (0x0802f3a8..0x0802fd00, 23 fn)

**函数列表**:
| addr       | name                                              |
|------------|---------------------------------------------------|
| 0x0802f3a8 | query_zone_chain_count_with_eligibility           |
| 0x0802f3e0 | query_slot_effect_eligibility_with_equip_fallback |
| 0x0802f434 | count_slot_equip_list_matches                     |
| 0x0802f4e0 | count_active_extended_chain_nodes                 |
| 0x0802f550 | find_zone_chain_node_by_card_id_pair              |
| 0x0802f5b0 | find_equip_chain_node_by_slot_pair                |
| 0x0802f61c | count_equip_slots_with_active_chain               |
| 0x0802f680 | find_equip_chain_pair_across_field                |
| 0x0802f6e4 | find_node_packed_by_card_id_in_dual_lists         |
| 0x0802f768 | find_card_slot_by_zone_card_id                    |
| 0x0802f81c | find_equip_slot_by_zone_card_id_with_flag         |
| 0x0802f8d8 | find_equip_chain_node_by_type_d                   |
| 0x0802f930 | find_equip_target_for_card_slot                   |
| 0x0802f9fc | build_equip_chain_slot_entry                      |
| 0x0802faf4 | find_node_by_value                                |
| 0x0802fb2c | find_node_by_value_and_zone_type                  |
| 0x0802fb6c | find_node_by_value_zone_entity                    |
| 0x0802fbbc | count_chain_nodes_by_card_id                      |
| 0x0802fbf4 | count_chain_nodes_by_card_id_and_type             |
| 0x0802fc34 | count_slot_chain_nodes_by_card_id                 |
| 0x0802fc60 | count_slot_chain_nodes_by_card_id_and_type        |
| 0x0802fc90 | check_value_in_slot_chain                         |
| 0x0802fcc0 | check_value_in_effect_context_chain               |

**符号化统计**:
- EQ_SLOTS: 33 (全复用: PLAYER_BLOCK_STRIDE x14 ewram.inc, EQUIP_NODE_BASE_OFFSET x7 duel_field.inc, OAM_ATTR0_HIDDEN x7 oam_attr.inc, NODE_POOL_NEG_OFFSET x4 duel_field.inc, SCROLLBAR_CLEAR_BITS_14_6 x1 gl_scrollbar.inc)
- REF_SLOTS: 24 (gDuelFieldSlots x14, gEquipNodePool x7, gDuelEffectChainSlots x2, gEquipChainSlotRefs x1)
- RENAME_SLOTS: 1 (count_equip_list_zone_type_bias EOL zone_type range bias)
- PLATE_REWRITES: 6 (FUN_0802f3e0, FUN_0802f680, FUN_0802fdc0, FUN_0802fe98, FUN_0802ff34, FUN_0802ff84)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants/全局** (1 项):
- `ewram.inc`: gDuelEffectChainSlots=0x0201bc54 (17 raw refs; effect context chain slot array, 2 entries stride 20B)

**落地踩坑记录**: 无 (first-shot PASS, dry run 0 FAIL, 实跑 0 SKIP)

**脚本**: `tools/ghidra-labeling/RefineF02Seg3Slots.py` (EQ33/REF24/RENAME1/PLATE6)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: a78e8b1

---

### 4.04 Seg-4 完成记录 (0x0802fd00..0x080309b8, 23 fn)

**函数列表**:
| addr       | name                                          |
|------------|-----------------------------------------------|
| 0x0802fd00 | find_chain_node_by_dual_halfword              |
| 0x0802fd60 | find_effect_node_in_zone                      |
| 0x0802fdc0 | check_node_in_slot_chain                      |
| 0x0802fdf4 | check_slot_has_node_by_card_id                |
| 0x0802fe2c | check_value_in_slot_chain_zone_entity         |
| 0x0802fe60 | get_node_entity_id_in_slot                    |
| 0x0802fe98 | get_zone_node_entity_hword_by_card_and_type   |
| 0x0802fed4 | get_zone_node_entity_hword_or_miss            |
| 0x0802ff10 | check_zone_card_id_in_node_pool               |
| 0x0802ff34 | check_node_in_zone_idx_chain                  |
| 0x0802ff58 | get_entity_id_in_zone_idx_chain               |
| 0x0802ff84 | get_entity_id_in_zone_idx_chain_by_type       |
| 0x0802ffb0 | count_chain_by_card_id_in_zone_idx            |
| 0x0802ffd0 | count_chain_by_card_id_and_type_in_zone_idx   |
| 0x0802fff0 | scan_equip_node_pool_for_card_score           |
| 0x08030048 | find_equip_chain_node_by_pred                 |
| 0x0803009c | find_zone_node_by_card_id_match               |
| 0x080300d4 | check_zone_card_special_state_by_field5       |
| 0x08030208 | count_set_bits_in_word                        |
| 0x0803026c | get_card_equip_target_zone_cost               |
| 0x08030500 | map_card_id_to_anim_type                      |
| 0x0803088c | check_effect_slot_summon_path_eligible        |
| 0x08030988 | check_effect_slot_is_equip_activatable        |

**符号化统计**:
- EQ_SLOTS: 46 (PLAYER_BLOCK_STRIDE x14 ewram.inc, gDuelFieldSlots x12 ewram.inc, EQUIP_NODE_BASE_OFFSET x3 duel_field.inc, gEquipNodePool x2 ewram.inc, ZONE_CHAIN_CARD_ID_OFF x6 ewram.inc NEW, OAM_ATTR0_HIDDEN x1 oam_attr.inc, POPCOUNT_MASK_* x8 bitops.inc NEW)
- REF_SLOTS: 0 (PTR_gP1LifePoints_* already resolved by prior ops)
- RENAME_SLOTS: 90 (8 PTR_gP1LifePoints_* + 1 sw-table + 8 field5 cid + 32 equip_zone_cost cid + 33 map_anim_type cid + 8 summon_path cid)
- PLATE_FULL: 3 (CJK -> ASCII rewrites: get_zone_node_entity_hword_by_card_and_type / get_zone_node_entity_hword_or_miss / scan_equip_node_pool_for_card_score)
- PLATE_SUBS: 14 stale FUN_ entries (all WARN "not found" -- stale FUN_ strings already absent from plates, no-op as in Seg-3)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants** (2 项):
- `ewram.inc`: ZONE_CHAIN_CARD_ID_OFF=0x000010e2 (gP1LifePoints+0x10e2 zone-chain card_id table; 21 raw refs; 6 Seg-4 slots)
- `constants/bitops.inc` (新文件): 8 POPCOUNT_MASK_* (ODD/EVEN/HI2/LO2/HI4/LO4/HI8/LO8, standard Hamming weight parallel-reduction masks; count_set_bits_in_word @ 0x08030208 utility fn); include added to rom.s

**落地踩坑记录**: 无 (first-shot PASS, dry run 0 FAIL, 实跑 0 SKIP; 14 PLATE_SUBS 均 WARN not found 同 Seg-3 一致, 无影响)

**脚本**: `tools/ghidra-labeling/RefineF02Seg4Slots.py` (EQ46/REF0/RENAME90/PLATE_FULL3/PLATE_SUBS14)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: f8cdb43

---

### 4.05 Seg-5 完成记录 (0x080309b8..0x080313dc, 23 fn)

**函数列表**:
| addr       | name                                          |
|------------|-----------------------------------------------|
| 0x080309b8 | check_effect_slot_zone_equip_valid            |
| 0x080309fc | check_field_spell_b_placeable                 |
| 0x08030a30 | check_slot_card_is_equip_whitelist            |
| 0x08030aa4 | check_slot_card_is_equip_type                 |
| 0x08030b0c | check_slot_card_is_monster_type               |
| 0x08030b70 | check_card_stat_field7_equals                 |
| 0x08030b88 | write_word_from_deref_src                     |
| 0x08030b90 | swap_deref_words                              |
| 0x08030b9c | check_deref_words_equal                       |
| 0x08030bac | increment_player_chain_counter                |
| 0x08030be4 | place_card_into_monster_zone_slot             |
| 0x08030cc0 | place_card_into_spelltrap_zone_slot           |
| 0x08030de8 | find_zone_descriptor_by_slot_id               |
| 0x080310d0 | find_slot_idx_in_dual_list_by_id              |
| 0x08031118 | find_field_slot_by_set_code_global            |
| 0x08031184 | find_slot_idx_by_set_code                     |
| 0x080311e0 | find_slot_idx_by_zone_id_in_chain_list        |
| 0x0803123c | find_hand_slot_idx_by_set_code                |
| 0x08031294 | find_hand_slot_idx_by_set_code_alt            |
| 0x080312ec | find_slot_idx_by_card_id_in_player_zones      |
| 0x08031348 | find_lp_entry_by_flag_and_type                |
| 0x08031390 | resolve_slot_id_to_zone_ptr                   |
| 0x080313b8 | check_equip_placement_eligible_from_slot_record |

**符号化统计**:
- EQ_SLOTS: 39 (24 EQ_REUSE + 15 EQ_NEW)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x15 + gDuelFieldSlots x7 + gP1ZoneHandCount x1 + gDuelEffectChainSlots x1
  - EQ_NEW: FIELD_SLOT_COUNT_OFF x2 + SLOT_FACE_STATUS_ARRAY_OFF x2 + FIELD_SPELL_CARD_REF_OFF x1 +
    DUEL_ACTIVE_PLAYER_OFF x1 + gP1SlotCountBase x1 + gP1SlotSetCodeArray x1 + gP1HandCountBase x1 +
    gP1HandSlotArray x1 + gP1ChainZoneCountBase x1 + gP1ChainZoneArray x1 + gP1AltHandCountBase x1 +
    gP1AltHandSlotArray x1 + FIELD_SPELL_B_EFFECT_ID x1
- REF_SLOTS: 0 (8 PTR_gP1LifePoints_* 已有 DATA refs)
- RENAME_SLOTS: 21 (8 PTR_ label renames + 7 card_id BST + 5 neg_off + 1 zone mask)
- PLATE_FULL: 10 (全段重写, C8 落地验证无残留 FUN_; 落地后 grep 验证 == 0)
- carve: 0 / disasm: 0 / §5.1: 0 (本段无 ROM_INCBIN)

**新建 constants** (3 文件, 13 项):
- `duel_field.inc`: FIELD_SLOT_COUNT_OFF=0x1cb4, SLOT_FACE_STATUS_ARRAY_OFF=0x10b1,
  FIELD_SPELL_CARD_REF_OFF=0x1390, DUEL_ACTIVE_PLAYER_OFF=0x1cb8
- `ewram.inc`: gP1SlotCountBase=0x0201c4f0, gP1SlotSetCodeArray=0x0201c740,
  gP1HandCountBase=0x0201c4f4, gP1HandSlotArray=0x0201c8f8,
  gP1ChainZoneCountBase=0x0201c4f8, gP1ChainZoneArray=0x0201c880,
  gP1AltHandCountBase=0x0201c4fc, gP1AltHandSlotArray=0x0201cab0
- `card_info.inc`: FIELD_SPELL_B_EFFECT_ID=0x1407

**C8 plate 验证**:
- 10 个 plate 全用 setPlateComment 整段重写 (非 substring replace), 写入后读回 re 扫描确认无 FUN_ 残留
- 导出后 grep asm/02_text_lp_fieldspell.s Seg-5 范围 (L10082..L11545) @ 行含 FUN_ = **0** (落地验收通过)

**落地踩坑记录**: 无 (first-shot PASS, dry run 0 FAIL, 实跑 0 SKIP/FAIL)

**脚本**: `tools/ghidra-labeling/RefineF02Seg5Slots.py` (EQ39/REF0/RENAME21/PLATE_FULL10)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: 1ad7df7

---

### 4.06 Seg-6 完成记录 (0x080313dc..0x0803217c, 23 fn)

**函数列表**:
| addr       | name                                    |
|------------|-----------------------------------------|
| 0x080313dc | get_equip_card_set_code_for_slot        |
| 0x08031474 | find_equip_chain_node_min_count_by_pred |
| 0x0803149c | get_slot_effect_card_value              |
| 0x080314d4 | resolve_slot_card_id_for_pair           |
| 0x08031564 | check_slot_card_pair_allowed            |
| 0x08031578 | insert_slot_ref_into_hand_array         |
| 0x080315f8 | append_slot_ref_to_hand_array           |
| 0x08031630 | append_slot_ref_to_equip_array          |
| 0x08031668 | shuffle_player_hand_list                |
| 0x080316b8 | find_card_pair_in_player_deck_list      |
| 0x08031710 | find_chain_zone_slot_by_pair_card       |
| 0x08031768 | remove_slot_from_equip_array_by_index   |
| 0x080317e0 | erase_slot_from_hand_array_by_ptr       |
| 0x0803189c | remove_zone_slot_entry_by_card_id       |
| 0x08031954 | retire_equip_slot_with_relink           |
| 0x08031978 | erase_slot_from_equip_array_b_by_ptr    |
| 0x08031a34 | count_monster_slots_with_field5_nonzero |
| 0x08031a84 | count_zone_card_pair_allowed_for_card   |
| 0x08031ae4 | count_chain_zone_card_pair_allowed_for_card |
| 0x08031b44 | sort_hand_cards_by_lp_score             |
| 0x08031b90 | init_player_hand_display_slots          |
| 0x08031d44 | build_hand_zone_display_slots_shuffled  |
| 0x08031ebc | serialize_field_zone_setcodes_to_buf    |

**符号化统计**:
- EQ_SLOTS: 38 (32 EQ_REUSE + 6 EQ_NEW)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x3 + gP1SlotSetCodeArray x4 + gP1ChainZoneArray x2 + GPRNG_STEP_CTR_MASK x2 + OAM_ATTR0_HIDDEN x1
  - EQ_NEW: EQUIP_SLOT_ACTIVE_TAG x1 (duel_field.inc) + SLOT_CARD_SET_CODE_MASK x2 (card_info.inc) + OAM_ATTR2_TILE_CLEAR x3 (oam_attr.inc)
- REF_SLOTS: 0 (16 PTR_gP1LifePoints_* 已有 DATA refs)
- RENAME_SLOTS: 26 (16 PTR_/DWORD_ label renames + 10 DAT_/DWORD_ domain labels)
- PLATE_FULL: 11 (全段重写, C8 Ghidra readback 验证 11/11 无 FUN_ 残留)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants** (3 项):
- `duel_field.inc`: EQUIP_SLOT_ACTIVE_TAG=0xa5600000 (packed slot state tag; slot[0]<<19==this -> active equip; 5 raw refs)
- `card_info.inc`: SLOT_CARD_SET_CODE_MASK=0x00001fff (13-bit set_code/card_id mask for zone slot arrays; 101 raw refs)
- `oam_attr.inc`: OAM_ATTR2_TILE_CLEAR=0xffffe000 (AND mask clearing OAM attr2 bits[12:0]; 31 raw refs)

**C8 plate 验证**:
- 11 个 plate 全用 setPlateComment 整段重写 (非 substring replace), 写入后读回 re 扫描确认无 FUN_ 残留
- 导出后 grep asm/02_text_lp_fieldspell.s Seg-6 范围 (L11545..L13505) @ 行含 FUN_ = **0** (落地验收通过)

**落地踩坑记录**: 无 (iteration-2 PASS, dry run 0 FAIL, 实跑 EQ=38/RENAME=26/PLATE 11 PLF OK, 0 SKIP)

**脚本**: `tools/ghidra-labeling/RefineF02Seg6Slots.py` (EQ38/REF0/RENAME26/PLATE_FULL11)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: 8051a2e

---

### 4.07 Seg-7 完成记录 (0x0803217c..0x08032e80, 23 fn)

**函数列表**:
| addr       | name                                         |
|------------|----------------------------------------------|
| 0x0803217c | clear_zone_slot_chain_refs                   |
| 0x08032194 | erase_slot_from_zone_array_by_type           |
| 0x08032280 | dispatch_card_placement_by_zone_type         |
| 0x08032358 | classify_card_effect_category                |
| 0x080324b4 | find_equip_slot_by_card_id                   |
| 0x08032500 | find_field_slot_idx_by_card_id               |
| 0x08032548 | test_slot_has_active_card                    |
| 0x0803259c | check_slot_equip_eligible_by_type_and_id     |
| 0x080325dc | check_card_equip_eligibility_in_field        |
| 0x08032654 | count_available_effect_zones                 |
| 0x0803279c | count_field_copies_of_card                   |
| 0x08032904 | count_zones_by_card_and_mode                 |
| 0x08032960 | count_equip_eligible_slots_for_player        |
| 0x08032a6c | count_equip_eligible_slots_both_players      |
| 0x08032a8c | find_best_slot_for_card_by_player            |
| 0x08032b98 | find_best_slot_atk_across_players            |
| 0x08032bc8 | count_paired_slots_with_field5               |
| 0x08032c94 | count_paired_slots_with_field5_default       |
| 0x08032ca4 | count_paired_slots_both_sides                |
| 0x08032ccc | count_equipped_paired_slots_for_player       |
| 0x08032d1c | count_equip_set_activatable_slots_for_player |
| 0x08032dac | count_equip_zone_slots_matching_card         |
| 0x08032e20 | count_equip_slots_meeting_atk_threshold      |

**符号化统计**:
- EQ_SLOTS: 48 (40 EQ_REUSE + 8 EQ_NEW)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x18 + gDuelEffectChainSlots x1 + gEquipChainSlotRefs x1
  - EQ_NEW: EFFECT_ZONE_PARTITION_OFF x5 (duel_field.inc) + gDuelFieldSlots_p2_base x2 (ewram.inc) + EFFECT_ZONE_BITMASK_OFF x1 (duel_field.inc)
- REF_SLOTS: 0
- RENAME_SLOTS: 19 (2 switchD ptr + 13 classify_cid + 4 equip_elig_cid)
- PLATE_FULL: 5 (全段重写, C8 Ghidra readback 验证 5/5 无 FUN_ 残留)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants** (3 项):
- `duel_field.inc`: EFFECT_ZONE_PARTITION_OFF=0x000010a4 (gDuelFieldSlots+0x10a4=effect zone slot array base; 18 raw refs)
- `duel_field.inc`: EFFECT_ZONE_BITMASK_OFF=0x000010d0 (gDuelFieldSlots+0x10a0=effect zone occupation bitmask; 45 raw refs)
- `ewram.inc`: gDuelFieldSlots_p2_base=0x0201c5d8 (gDuelFieldSlots+0xc8=slot[10] for field9==2 path; 24 raw refs)

**C8 plate 验证**:
- 5 个 plate 全用 setPlateComment 整段重写 (非 substring replace), 写入后读回 re 扫描确认无 FUN_ 残留
- 导出后 grep asm/02_text_lp_fieldspell.s Seg-7 范围 (L13475..L15283) @ 行含 FUN_ = **0** (落地验收通过)

**落地踩坑记录**: 无 (first-shot PASS, dry run 0 FAIL, 实跑 EQ=48/RENAME=19/PLATE 5 PLF OK, 0 SKIP)

**脚本**: `tools/ghidra-labeling/RefineF02Seg7Slots.py` (EQ48/REF0/RENAME19/PLATE_FULL5)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: f12c5fe

---

### 4.08 Seg-8 完成记录 (0x08032e80..0x08033654, 23 fn)

**函数列表**:
| addr       | name                                              |
|------------|---------------------------------------------------|
| 0x08032e80 | count_monster_slots_by_state                      |
| 0x08032ef0 | count_monster_slots_by_state_all                  |
| 0x08032f00 | count_eligible_zone_slots_for_player              |
| 0x08032f6c | count_eligible_zone_slots_all_flags               |
| 0x08032f7c | count_slot_card_pair_allowed_for_card             |
| 0x08032fa4 | count_unpaired_slots_for_card                     |
| 0x08032fd8 | count_field_cards_pair_allowed_for_card           |
| 0x08033088 | check_toon_world_equip_present                    |
| 0x0803309c | count_active_slots_with_field6_value              |
| 0x0803310c | count_occupied_all_field_zones                    |
| 0x08033188 | count_occupied_monster_zones                      |
| 0x080331bc | count_occupied_monster_zones_with_effect_bonus    |
| 0x08033214 | count_monster_slots_by_fnptr                      |
| 0x08033258 | count_field_slots_with_field8_is_9                |
| 0x08033294 | count_slots_with_chain_field_match                |
| 0x080332f0 | count_slots_matching_card_pair                    |
| 0x08033334 | count_monster_slots_by_chain_head_id              |
| 0x08033370 | count_active_cards_in_zone_by_player              |
| 0x080333ac | check_slot_placement_blocked_by_field_effect      |
| 0x0803352c | check_monster_slot_accepts_card                   |
| 0x080335b8 | count_available_monster_slots                     |
| 0x08033610 | count_monster_slots_accepting_card                |
| 0x08033634 | get_first_placeable_monster_slot                  |

**符号化统计**:
- EQ_SLOTS: 38 (33 EQ_REUSE + 5 EQ_NEW)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x14 + gDuelFieldSlots x12 + EFFECT_ZONE_BITMASK_OFF x2 + gEquipChainSlotRefs x3 + NODE_POOL_NEG_OFFSET x1 + gP1AltHandCountBase x1
  - EQ_NEW: gDuelFieldSpellZoneBase x1 (ewram.inc) + TOON_WORLD_CARD_ID x1 + GROUND_COLLAPSE_FIELD_CARD_ID x1 + OJAMA_KING_CARD_ID x1 + SPATIAL_COLLAPSE_CARD_ID x1 (card_info.inc)
- REF_SLOTS: 0
- RENAME_SLOTS: 6 (4 PTR_gP1LifePoints + 2 independent DAT)
- PLATE_FULL: 3 (全段重写, C8 Ghidra readback 验证 3/3 无 FUN_ 残留)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants** (5 项):
- `card_info.inc`: TOON_WORLD_CARD_ID=0x12be (Toon World field-magic card id; equip-zone scan; 9 raw refs)
- `card_info.inc`: GROUND_COLLAPSE_FIELD_CARD_ID=0x1432 (data.md line 900, passcode 90502999; 18 raw refs)
- `card_info.inc`: OJAMA_KING_CARD_ID=0x17ee (data.md line 1639, passcode 90140980; 13 raw refs)
- `card_info.inc`: SPATIAL_COLLAPSE_CARD_ID=0x16df (Spatial Collapse field spell; monster zone clamp; 16 raw refs)
- `ewram.inc`: gDuelFieldSpellZoneBase=0x0201c5ec (gDuelFieldSlots+11*0x14=P0 field-spell zone slot entry base; 6 raw refs)

**C8 plate 验证**:
- 3 个 plate 全用 setPlateComment 整段重写 (非 substring replace), 写入后读回 re 扫描确认无 FUN_ 残留
- 导出后 grep asm/02_text_lp_fieldspell.s Seg-8 范围 (L15282..L16430) @ 行含 FUN_ = **0 stale subjects** (落地验收通过; 3 个 FUN_ 命中均为 P4/P5 外部未命名 caller 上下文说明, 非 stale 主语)
- Non-ASCII scan: 0 行

**落地踩坑记录**: 无 (iteration-2 PASS, dry run 0 FAIL, 实跑 EQ=38/RENAME=6/PLATE 3 PLF OK, 0 SKIP/FAIL)

**脚本**: `tools/ghidra-labeling/RefineF02Seg8Slots.py` (EQ38/REF0/RENAME6/PLATE_FULL3)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: 9892a81

---

### 4.09 Seg-9 完成记录 (0x08033654..0x0803407c, 23 fn)

**函数列表**:
| addr       | name                                    |
|------------|-----------------------------------------|
| 0x08033654 | find_first_placeable_monster_slot       |
| 0x08033688 | check_slot_equip_eligibility            |
| 0x08033730 | check_slot_card_can_be_equipped         |
| 0x080337f0 | check_equip_cards_share_field7          |
| 0x080338b8 | count_equip_placements_with_chain_check |
| 0x080339d8 | count_equippable_slots_for_card         |
| 0x08033a6c | count_slots_equippable_by_state_code    |
| 0x08033b08 | count_equip_slots_active_only           |
| 0x08033b18 | count_equip_slots_matching_whitelist    |
| 0x08033bb0 | check_slot_available_for_card           |
| 0x08033bf4 | find_first_available_monster_slot_for_player |
| 0x08033c44 | count_available_field_zones_for_player  |
| 0x08033c9c | check_field_spell_placement_allowed     |
| 0x08033cf8 | check_player_has_equip_type_in_slots    |
| 0x08033d44 | check_any_slot_fieldspell_zone_eligible |
| 0x08033d98 | count_hand_slots_with_field6_val_0x17   |
| 0x08033de4 | count_hand_slots_with_field6_val_0x16   |
| 0x08033e30 | count_spell_zone_slots_with_empty_chain |
| 0x08033e70 | count_hand_cards_by_field6              |
| 0x08033ecc | count_graveyard_cards_by_field7_value   |
| 0x08033f28 | count_graveyard_equip_cards_by_field9   |
| 0x08033fa4 | count_graveyard_fieldspell_cards_by_field9 |
| 0x08034020 | count_hand_cards_by_field6_alt          |

**符号化统计**:
- EQ_SLOTS: 57 (39 EQ_REUSE + 18 EQ_NEW via new card_info.inc constants)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x13 + SPATIAL_COLLAPSE_CARD_ID x3 + gDuelFieldSlots_p2_base x1 + gP1HandSlotArray x2
  - EQ_NEW: EQUIP_LOCKDOWN_CID x4 + EQUIP_ZONE_BLOCKER_CID x1 + EQUIP_LOCK_A_CID x1 + EQUIP_LOCK_B_CID x1 + EQUIP_ELIG_EXCL_A/B/C/D x4 + EQUIP_PAIR_EXCL_A/B/C x3 + EQUIP_PAIR_RANGE_MAX x1 + EQUIP_CHAIN_PAIR_CARD_MAX x1 + MONSTER_SLOT_ORDER_TABLE x1 + AVAIL_SLOT_ORDER_TABLE x1
- REF_SLOTS: 0
- RENAME_SLOTS: 6 (PTR_gP1LifePoints x6)
- PLATE_FULL: 3 (CJK->ASCII 全段重写, Ghidra readback 3/3 无 FUN_ 残留)
- carve: 2 (monster_slot_order_table @0x09e3ef4c/20B + available_slot_order_table @0x09e3ef60/20B)
- disasm: 0 / §5.1: 0

**新建 constants** (13 项, card_info.inc Seg-9 additions block):
- EQUIP_LOCKDOWN_CID=0x13f2, EQUIP_ZONE_BLOCKER_CID=0x13eb
- EQUIP_LOCK_A_CID=0x16a4, EQUIP_LOCK_B_CID=0x12d1
- EQUIP_ELIG_EXCL_A=0x14f9, EQUIP_ELIG_EXCL_B=0x1836, EQUIP_ELIG_EXCL_C=0x1670, EQUIP_ELIG_EXCL_D=0x19ee
- EQUIP_PAIR_EXCL_A=0x17e9, EQUIP_PAIR_EXCL_B=0x1521, EQUIP_PAIR_EXCL_C=0x1798
- EQUIP_PAIR_RANGE_MAX=0x1874, EQUIP_CHAIN_PAIR_CARD_MAX=0x164f

**carve 验证**: 0x1534+0x14+0x14+0xAD98=0xC2F4 (== host incbin size) ✅

**C8 plate 验证**:
- 3 个 plate 全用 setPlateComment 整段重写, 写入后 readback re 扫描确认 3/3 无 FUN_ 残留
- Non-ASCII scan: 0 行 ✅
- 段范围行中残余 FUN_: 4 处均在其他函数 plate 的跨模块 callee 上下文 (非 stale 主语, 属正常)

**落地踩坑记录**:
- MONSTER_SLOT_ORDER_TABLE/AVAIL_SLOT_ORDER_TABLE 是 rom.s carve label，不能作为 equate 导出到 asm (会产生 undefined reference); 修复: asm/02_text_lp_fieldspell.s 中两处 `.word MONSTER_SLOT_ORDER_TABLE/AVAIL_SLOT_ORDER_TABLE` 手改为 `.word monster_slot_order_table/available_slot_order_table` (carve label)。

**脚本**: `tools/ghidra-labeling/RefineF02Seg9Slots.py` (EQ57/REF0/RENAME6/PLATE_FULL3)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: 77760ad

---

### 4.10a Seg-10a 完成记录 (0x0803407c..0x08035280, 10 fn)

**函数列表**:
| addr       | name                                         |
|------------|----------------------------------------------|
| 0x0803407c | eval_slot_target_eligibility_full            |
| 0x0803412c | check_card_matches_active_effect_slot        |
| 0x08034180 | find_paired_zone_entry_for_card              |
| 0x08034298 | check_card_targeted_by_spell_zone_effect     |
| 0x08034358 | check_slot_field_action_eligibility          |
| 0x080345e0 | check_field_spell_slot_placeable             |
| 0x080346c4 | check_slot_monster_activation_eligible       |
| 0x0803495c | eval_slot_activation_guard_full              |
| 0x080349b0 | check_slot_card_activatable                  |
| 0x08034a58 | check_slot_full_activation_eligibility       |

**符号化统计**:
- EQ_SLOTS: 57 (40 EQ_REUSE + 17 EQ_NEW)
  - EQ_REUSE: PLAYER_BLOCK_STRIDE x19 + gDuelFieldSlots x14 + gDuelCardCtxBase x4 + gDuelFieldSlotState x1 + gEquipChainSlotRefs x1 + gDuelFieldSlots_p2_base x1 + EQUIP_CHAIN_PAIR_CARD_MAX x1 (card_info.inc) + EQUIP_LOCK_B_CID x1 (card_info.inc)
  - EQ_NEW (card_info.inc): UMI_CARD_ID=0x10f4 x2 + A_LEGENDARY_OCEAN_CARD_ID=0x150b x1 + SPELL_ZONE_TARGET_CARD_ID=0x1368 x2 + TOTAL_DEFENSE_SHOGUN_CARD_ID=0x12b4 x1 + EHERO_RAMPART_BLASTER_CARD_ID=0x1956 x1 + TWINHEADED_BEAST_CARD_ID=0x1723 x1 + TYRANT_DRAGON_CARD_ID=0x14d5 x1 + ARMED_SAMURAI_BEN_KEI_CARD_ID=0x186c x1
  - EQ_NEW (duel_field.inc): ACTIVATION_STATE_A_OFF=0x1d48 x2 + ACTIVATION_STATE_B_OFF=0x1d78 x3 + ACTIVE_EFFECT_CATEGORY_OFF=0x10d8 x1
- REF_SLOTS: 11 (10 PTR_gP1LifePoints_* rename + 1 fn-ptr slot)
- RENAME_SLOTS: 80 (verified card IDs / chain node type IDs)
- FUNC_RENAME: 0
- PLATE: 0 (no stale FUN_ in segment plates; PLATE=SKIP confirmed)
- carve: 0 / disasm: 0 / §5.1: 0

**新建 constants** (11 项):
- `duel_field.inc`: ACTIVATION_STATE_A_OFF=0x1d48 (gP1LifePoints+side*0x868+0x1d48; activation state field A; 27 raw refs)
- `duel_field.inc`: ACTIVATION_STATE_B_OFF=0x1d78 (activation state field B; 41 raw refs)
- `duel_field.inc`: ACTIVE_EFFECT_CATEGORY_OFF=0x10d8 (gP1LifePoints+0x10d8=0x0201D5B8; active effect slot category; 16 raw refs)
- `card_info.inc`: UMI_CARD_ID=0x10f4, A_LEGENDARY_OCEAN_CARD_ID=0x150b, SPELL_ZONE_TARGET_CARD_ID=0x1368
- `card_info.inc`: TOTAL_DEFENSE_SHOGUN_CARD_ID=0x12b4, EHERO_RAMPART_BLASTER_CARD_ID=0x1956
- `card_info.inc`: TWINHEADED_BEAST_CARD_ID=0x1723, TYRANT_DRAGON_CARD_ID=0x14d5, ARMED_SAMURAI_BEN_KEI_CARD_ID=0x186c

**C8 stale FUN_ 验收**: grep Seg-10a 范围 (L17843..L20238) 中主语 FUN_ = **0** (2 处括注 FUN_ 均为跨模块/跨段上下文说明, 非 stale 主语)。

**Non-ASCII scan**: 1 处 (L19025 eval_slot_activation_guard_full 的存量 CJK plate, 命名阶段遗留, 本次 PLATE=0 未写入新 plate/EOL, 超出本段责任)。

**落地踩坑记录**:
1. fn-ptr REF slot 0x080346c0: 初始脚本误将 label `count_monster_slots_by_fnptr_pred_0804aea0` 建在目标奇地址 0x0804aea1, 导出器输出 `.word count_monster_slots_by_fnptr_pred_0804aea0` (无 +1, GAS undefined reference)。修复: FixF02Seg10aFnPtrSlot.py 删除奇地址 label + 重建 DATA ref 指向偶地址 0x0804aea0 (`check_card_is_archfiend_type`)。导出后 `.word 0x0804aea1` (原始奇地址值, slot label `check_field_spell_slot_placeable_fnptr` 正确输出)。
2. Seg-9 残留: MONSTER_SLOT_ORDER_TABLE/AVAIL_SLOT_ORDER_TABLE 大写 equate 在 Seg-9 时已建立, 但 rom.s carve label 为小写, 每次重新 export 导致 GAS undefined reference。根治: rom.s 加 `.equ` 别名 `MONSTER_SLOT_ORDER_TABLE = monster_slot_order_table` / `AVAIL_SLOT_ORDER_TABLE = available_slot_order_table`。

**脚本**: `tools/ghidra-labeling/RefineF02Seg10aSlots.py` (EQ57/REF11/RENAME80) + `tools/ghidra-labeling/FixF02Seg10aFnPtrSlot.py` (fn-ptr 修正)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: dc67250

---

### 4.10b Seg-10b 完成记录 (0x08035280..0x08035f54, 7 fn) — file 02 最终段

**函数列表**:
| addr       | name                                              |
|------------|---------------------------------------------------|
| 0x08035280 | exit_slot_activation_with_state_write             |
| 0x080352b0 | eval_slot_activation_eligibility_full             |
| 0x0803594c | count_activatable_slots_for_player                |
| 0x08035988 | check_slot_field_spell_chain_eligible             |
| 0x08035b24 | check_field_spell_trap_chain_eligible             |
| 0x08035ba4 | check_player_field_spell_chain_eligible           |
| 0x08035bc8 | eval_slot_fieldspell_activation_full              |

**符号化统计**:
- EQ_SLOTS: 95 (28 EQ_REUSE + 67 EQ_NEW)
  - EQ_REUSE (28): ACTIVATION_STATE_B_OFF x1 + PLAYER_BLOCK_STRIDE x14 + gDuelFieldSlots x11 + UMI_CARD_ID x3
  - EQ_NEW card_info.inc (51): JINZO_7_CID..HAMON_LORD_CID + HAMON_LORD_CID_SHIFTED
  - EQ_NEW duel_field.inc (2): FIELD5_SCORE_ACTIVATION_THRESHOLD + FIELD5_SCORE_FIELDSPELL_THRESHOLD
- REF_SLOTS: 1 (gDuelCardCtxBase @ 0x080352a4)
- RENAME_SLOTS: 2 (exit_slot_act_gp1lp + eval_fsact_unknown_cid_1221)
- PLATE_FULL: 3 (eval_slot_activation_eligibility_full + eval_slot_fieldspell_activation_full + eval_slot_activation_guard_full Seg-10a CJK cleanup)
- carve: 0 / disasm: 0 / §5.1: 0

**新建常量**:
- card_info.inc: 51 card ID equates (JINZO_7_CID 0x114c .. FEATHER_SHOT_CID 0x195b) + HAMON_LORD_CID=0x19a4 + HAMON_LORD_CID_SHIFTED=0xcd200000
- duel_field.inc: FIELD5_SCORE_ACTIVATION_THRESHOLD=0x76b + FIELD5_SCORE_FIELDSPELL_THRESHOLD=0x63f

**C8 plate 验证**: 3 个 plate 全用 setPlateComment 整段重写; Ghidra readback 确认 3/3 无 stale FUN_ 且无 non-ASCII.
Non-ASCII scan (Seg-10 整段, lines 19024..21953): 0 行 ✅

**脚本**: `tools/ghidra-labeling/RefineF02Seg10bSlots.py` (EQ95/REF1/RENAME2/PLATE_FULL3)

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: (pending)

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
| Seg-7 | 0x3217c..0x32e80 | 23 | 67 | — | ✅ zone slot chain refs clear/dispatch + effect zone offset symbolization |
| Seg-8 | 0x32e80..0x33654 | 23 | 44 | — | ✅ monster slot count/state scan + field spell placement check |
| Seg-9 | 0x33654..0x3407c | 23 | 63 | — | ✅ equip slot eligibility/lock + monster slot find + carve 2 slot-order tables |
| Seg-10a | 0x3407c..0x35280 | 10 | 148 | — | ✅ slot activation eligibility full cluster |
| Seg-10b | 0x35280..0x35f54 | 7 | 98 | — | ✅ exit_slot_activation_with_state_write + fieldspell zone; file 02 全 10 段完成 |

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
