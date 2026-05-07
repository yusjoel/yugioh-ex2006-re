# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> **每完成 1 个 batch (默认 15 函数), fixer 一次性更新本文档** (PROGRESS 字段 + N 行函数列表)

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=20 全自动模式。

python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json

启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,
单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。

**强制单 call 模式 (token 经济优先, 不在意 wall-clock)**:
  - executor: 1 个 sub-agent 一次性产出 batch 全部 20 份 proposal (禁止拆分 4×5 并行)
  - reviewer: 1 个 sub-agent 一次性评 20 份 (禁止拆分)
  - fixer iter (NEEDS_FIX): 1 个 sub-agent 处理本批所有 NEEDS_FIX
  - 拆分并行会导致 skill/feedback/asm 上下文重复加载, 实测 ~3× token 浪费, 收益仅 wall-clock

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. 该函数标 ⚠ FAIL 于函数列表对应行
  3. pick_batch.py 自动把"含失败 callee"的函数标 SKIP, 不进入下一 batch
  4. 继续下一批

仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。
```

---

## 当前状态

| 字段 | 值 |
|------|----|
| **根函数** | `campaign_scene_handler` (FUN_08025c94, 由 enter_campaign_page 写入 gMenuState+0x234, 间接调度) |
| **当前步骤** | Step 1 — executor (batch=21 模式, campaign-20) |
| **下一步** | `python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json` → 启动 4-agent loop (campaign-21) |
| **上次更新** | 2026-05-08 (campaign-20 batch, 360/1526) |
| **上次 callgraph 刷新** | 2026-05-05 (含 +50 新反汇 fns, +131 callgraph 边, +26 manual dispatch 边) |
| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |

## 进度

**360 / 1526 已分析** (campaign_scene_handler 闭包: 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过, 待命名 1526)

> 已命名函数池 (跨根复用): 259 个 (来自上一根 `enter_deck_edit_page` 任务). pick_batch.py 自动跳过已命名函数, 仅处理新根闭包内剩余 `FUN_*` 节点. 闭包内 A_named=150 即来自此池.

### 闭包 class 分布

| class | 数量 | 含义 | 处理 |
|-------|-----:|------|------|
| A_named | 150 | 已命名 (来自跨根池) | 跳过 |
| B_invoker | 8 | 0x0810e5c8..0x0810e5f0 invoker thunks | 跳过 |
| B_runtime | 14 | 0x0810e5c8 起 runtime/libgcc | 跳过 |
| C_util_high | 70 | indeg ≥ 20 的高频工具 | 命名 |
| D_shared_mid | 239 | indeg 5-19 的共享函数 | 命名 |
| E_specific_low | 1216 | indeg 1-4 的 feature-specific | 命名 |
| F_orphan | 1 | indeg=0 的 root (campaign_scene_handler 自身) | 命名 |

非 trivial SCC: 4 个 (size 3/2/6/2), 在 batch 中标记并行命名.

---

## 函数列表 (按 topo_idx 升序, 跳过 A/B 类)

> 列说明: # 序号 / topo 拓扑序 / depth BFS 深度 / indeg 全 ROM 入度 / class C 高 indeg / D 中 / E 低 / F orphan
> rev = 本函数完成命名所需的 reviewer 轮数 (期望 ≤ 3)

| # | topo | L | indeg | class | 位置 | 分析前 | 分析后 | rev | eval |
|---|------|---|-------|-------|------|--------|--------|-----|------|
| 1 | 1 | — | — | C | 0x08015194 | FUN_08015194 | fill_gl_palram_buf_0xf0 | 2 | [eval](eval/08015194.md) |
| 2 | 2 | — | — | C | 0x08015160 | FUN_08015160 | init_gl_palette_slot_flags | 2 | [eval](eval/08015160.md) |
| 3 | 8 | — | — | D | 0x080146cc | FUN_080146cc | update_brightness_fade_flag | 1 | [eval](eval/080146cc.md) |
| 4 | 10 | — | — | D | 0x08013510 | FUN_08013510 | reset_display_and_gl_state | 1 | [eval](eval/08013510.md) |
| 5 | 11 | — | — | C | 0x08015fc8 | FUN_08015fc8 | zero_struct_36bytes | 2 | [eval](eval/08015fc8.md) |
| 6 | 13 | — | — | E | 0x08014bcc | FUN_08014bcc | get_bg2_screen_vram_addr | 1 | [eval](eval/08014bcc.md) |
| 7 | 14 | — | — | E | 0x08014d94 | FUN_08014d94 | copy_to_bg2_screen_map | 1 | [eval](eval/08014d94.md) |
| 8 | 15 | — | — | E | 0x08014bec | FUN_08014bec | get_bg3_screen_vram_addr | 1 | [eval](eval/08014bec.md) |
| 9 | 16 | — | — | E | 0x08014dd4 | FUN_08014dd4 | copy_to_bg3_screen_map | 1 | [eval](eval/08014dd4.md) |
| 10 | 17 | — | — | E | 0x08014b8c | FUN_08014b8c | get_bg0_screen_vram_addr | 1 | [eval](eval/08014b8c.md) |
| 11 | 18 | — | — | E | 0x08014d14 | FUN_08014d14 | copy_to_bg0_screen_map | 1 | [eval](eval/08014d14.md) |
| 12 | 19 | — | — | E | 0x08014bac | FUN_08014bac | get_bg1_screen_vram_addr | 1 | [eval](eval/08014bac.md) |
| 13 | 20 | — | — | E | 0x08014d54 | FUN_08014d54 | copy_to_bg1_screen_map | 1 | [eval](eval/08014d54.md) |
| 14 | 21 | — | — | D | 0x080162dc | FUN_080162dc | dispatch_bg_screen_map_write | 1 | [eval](eval/080162dc.md) |
| 15 | 25 | — | — | D | 0x08016344 | FUN_08016344 | write_tile_region_to_bg_screen | 1 | [eval](eval/08016344.md) |
| 16 | 28 | — | — | D | 0x08014af0 | FUN_08014af0 | calc_bg_screenmap_block_offset | 1 | [eval](eval/08014af0.md) |
| 17 | 29 | — | — | E | 0x08014a50 | FUN_08014a50 | get_bg2_char_vram_addr | 1 | [eval](eval/08014a50.md) |
| 18 | 30 | — | — | E | 0x08014c94 | FUN_08014c94 | copy_to_bg2_char_tiles | 3 | [eval](eval/08014c94.md) |
| 19 | 31 | — | — | E | 0x08014a70 | FUN_08014a70 | get_bg3_char_vram_addr | 1 | [eval](eval/08014a70.md) |
| 20 | 32 | — | — | E | 0x08014cd4 | FUN_08014cd4 | copy_to_bg3_char_tiles | 3 | [eval](eval/08014cd4.md) |
| 21 | 33 | — | — | E | 0x08014a10 | FUN_08014a10 | get_bg0_char_vram_addr | 1 | [eval](eval/08014a10.md) |
| 22 | 34 | — | — | E | 0x08014c14 | FUN_08014c14 | copy_to_bg0_char_tiles | 3 | [eval](eval/08014c14.md) |
| 23 | 35 | — | — | E | 0x08014a30 | FUN_08014a30 | get_bg1_char_vram_addr | 1 | [eval](eval/08014a30.md) |
| 24 | 36 | — | — | E | 0x08014c54 | FUN_08014c54 | copy_to_bg1_char_tiles | 3 | [eval](eval/08014c54.md) |
| 25 | 37 | — | — | D | 0x080165bc | FUN_080165bc | apply_bgdt_entry_to_bg | 1 | [eval](eval/080165bc.md) |
| 26 | 38 | — | — | D | 0x0801626c | FUN_0801626c | write_palt_block_to_vram | 1 | [eval](eval/0801626c.md) |
| 27 | 39 | — | — | E | 0x08014c0c | FUN_08014c0c | get_obj_tile_vram_base | 1 | [eval](eval/08014c0c.md) |
| 28 | 40 | — | — | E | 0x08014e14 | FUN_08014e14 | copy_to_obj_tile_vram | 3 | [eval](eval/08014e14.md) |
| 29 | 41 | — | — | D | 0x0801695c | FUN_0801695c | apply_objd_entry_to_sprite | 1 | [eval](eval/0801695c.md) |
| 30 | 42 | — | — | D | 0x08016a7c | FUN_08016a7c | apply_gfx_resource_list | 1 | [eval](eval/08016a7c.md) |
| 31 | 43 | — | — | E | 0x08013578 | FUN_08013578 | setup_demo_sprite_entry | 2 | [eval](eval/08013578.md) |
| 32 | 44 | — | — | E | 0x08013680 | FUN_08013680 | setup_demo_sprite_entry_alt | 2 | [eval](eval/08013680.md) |
| 33 | 45 | — | — | E | 0x08013740 | FUN_08013740 | dispatch_demo_sprite_setup_by_mode | 1 | [eval](eval/08013740.md) |
| 34 | 55 | — | — | E | 0x0801379c | FUN_0801379c | load_demo_bg_gfx_set0 | 1 | [eval](eval/0801379c.md) |
| 35 | 56 | — | — | E | 0x08013864 | FUN_08013864 | load_demo_bg_gfx_set1 | 1 | [eval](eval/08013864.md) |
| 36 | 59 | — | — | D | 0x080e88cc | FUN_080e88cc | advance_anim_ctrl_frame | 1 | [eval](eval/080e88cc.md) |
| 37 | 59 | — | — | D | 0x080e8d70 | FUN_080e8d70 | step_anim_ctrl_by_frames | 1 | [eval](eval/080e8d70.md) |
| 38 | 59 | — | — | D | 0x080e90fc | FUN_080e90fc | set_anim_ctrl_position_fwd | 1 | [eval](eval/080e90fc.md) |
| 39 | 60 | — | — | D | 0x080e91a8 | FUN_080e91a8 | bind_anim_ctrl_callback | 1 | [eval](eval/080e91a8.md) |
| 40 | 61 | — | — | D | 0x080eb8e4 | FUN_080eb8e4 | set_nob_cell_frame_idx | 1 | [eval](eval/080eb8e4.md) |
| 41 | 62 | — | — | D | 0x080e8bc8 | FUN_080e8bc8 | get_anim_ctrl_current_frame_ptr | 1 | [eval](eval/080e8bc8.md) |
| 42 | 63 | — | — | D | 0x080eb8a8 | FUN_080eb8a8 | set_nob_cell_position | 1 | [eval](eval/080eb8a8.md) |
| 43 | 64 | — | — | D | 0x080eb978 | FUN_080eb978 | init_srt_ctrl_state | 1 | [eval](eval/080eb978.md) |
| 44 | 65 | — | — | D | 0x080eb94c | FUN_080eb94c | bind_srt_ctrl_data | 1 | [eval](eval/080eb94c.md) |
| 45 | 66 | — | — | D | 0x080eb7f0 | FUN_080eb7f0 | get_nob_cell_data_ptr | 1 | [eval](eval/080eb7f0.md) |
| 46 | 67 | — | — | D | 0x080eb918 | FUN_080eb918 | set_srt_ctrl_translate | 1 | [eval](eval/080eb918.md) |
| 47 | 68 | — | — | D | 0x080e9350 | FUN_080e9350 | apply_cell_anim_frame | 1 | [eval](eval/080e9350.md) |
| 48 | 69 | — | — | D | 0x080e94a4 | FUN_080e94a4 | init_cell_anim_with_seq | 1 | [eval](eval/080e94a4.md) |
| 49 | 70 | — | — | D | 0x080e90cc | FUN_080e90cc | zero_anim_ctrl_fields | 1 | [eval](eval/080e90cc.md) |
| 50 | 71 | — | — | D | 0x080e905c | FUN_080e905c | init_anim_ctrl | 1 | [eval](eval/080e905c.md) |
| 51 | 72 | — | — | D | 0x080e9400 | FUN_080e9400 | bind_cell_anim_to_bank | 1 | [eval](eval/080e9400.md) |
| 52 | 73 | — | — | D | 0x08015ac4 | FUN_08015ac4 | alloc_cell_anim_slot | 1 | [eval](eval/08015ac4.md) |
| 53 | 74 | — | — | D | 0x080eae5c | FUN_080eae5c | check_vram_location_slot | 1 | [eval](eval/080eae5c.md) |
| 54 | 75 | — | — | D | 0x080e9acc | FUN_080e9acc | set_img_proxy_vram_location | 1 | [eval](eval/080e9acc.md) |
| 55 | 76 | — | — | D | 0x080e99f0 | FUN_080e99f0 | check_vram_size_for_type | 1 | [eval](eval/080e99f0.md) |
| 56 | 77 | — | — | D | 0x080e9a18 | FUN_080e9a18 | check_img_mapping_type | 1 | [eval](eval/080e9a18.md) |
| 57 | 78 | — | — | D | 0x080e9de8 | FUN_080e9de8 | load_img_proxy_to_vram | 2 | [eval](eval/080e9de8.md) |
| 58 | 79 | — | — | D | 0x0801563c | FUN_0801563c | alloc_nce_buff_slot | 1 | [eval](eval/0801563c.md) |
| 59 | 80 | — | — | E | 0x08015b04 | FUN_08015b04 | invoke_fs_load | 1 | [eval](eval/08015b04.md) |
| 60 | 81 | — | — | D | 0x080eaf28 | FUN_080eaf28 | relocate_bin_block_ptrs | 1 | [eval](eval/080eaf28.md) |
| 61 | 82 | — | — | D | 0x080eaec4 | FUN_080eaec4 | find_bin_block_by_type | 1 | [eval](eval/080eaec4.md) |
| 62 | 83 | — | — | D | 0x080eaf58 | FUN_080eaf58 | link_nanr_anim_bank | 1 | [eval](eval/080eaf58.md) |
| 63 | 84 | — | — | D | 0x080eafb4 | FUN_080eafb4 | check_anim_block_has_data | 1 | [eval](eval/080eafb4.md) |
| 64 | 85 | — | — | D | 0x080eafd4 | FUN_080eafd4 | load_nanr_anim_bank | 1 | [eval](eval/080eafd4.md) |
| 65 | 86 | — | — | D | 0x080eb0f4 | FUN_080eb0f4 | relocate_nanr_block_ptrs | 3 | [eval](eval/080eb0f4.md) |
| 66 | 87 | — | — | D | 0x080eb54c | FUN_080eb54c | load_nclr_pltt_data | 1 | [eval](eval/080eb54c.md) |
| 67 | 88 | — | — | D | 0x080eb6b4 | FUN_080eb6b4 | relocate_ncl_pltt_data_ptr | 1 | [eval](eval/080eb6b4.md) |
| 68 | 89 | — | — | D | 0x080eb6dc | FUN_080eb6dc | get_nob_cell_data_offset | 1 | [eval](eval/080eb6dc.md) |
| 69 | 90 | — | — | D | 0x080eb718 | FUN_080eb718 | relocate_nob_exdata_block_ptrs | 1 | [eval](eval/080eb718.md) |
| 70 | 91 | — | — | D | 0x080eb744 | FUN_080eb744 | load_ncer_cell_bank | 1 | [eval](eval/080eb744.md) |
| 71 | 92 | — | — | D | 0x080eb838 | FUN_080eb838 | relocate_nob_cell_bank_ptrs | 1 | [eval](eval/080eb838.md) |
| 72 | 93 | — | — | D | 0x08015674 | FUN_08015674 | alloc_char_data_slot | 1 | [eval](eval/08015674.md) |
| 73 | 94 | — | — | E | 0x08015b10 | FUN_08015b10 | load_nce_cell_bank_from_file | 1 | [eval](eval/08015b10.md) |
| 74 | 95 | — | — | E | 0x08015b70 | FUN_08015b70 | load_nanr_anim_bank_from_file | 1 | [eval](eval/08015b70.md) |
| 75 | 96 | — | — | E | 0x08015c30 | FUN_08015c30 | load_nclr_pltt_data_from_file | 1 | [eval](eval/08015c30.md) |
| 76 | 97 | — | — | D | 0x080eb2e8 | FUN_080eb2e8 | fixup_char_block_data_ptr | 2 | [eval](eval/080eb2e8.md) |
| 77 | 98 | — | — | D | 0x080eb23c | FUN_080eb23c | parse_ncgr_char_data | 1 | [eval](eval/080eb23c.md) |
| 78 | 99 | — | — | E | 0x08015bd0 | FUN_08015bd0 | load_ncgr_char_data_from_file | 1 | [eval](eval/08015bd0.md) |
| 79 | 100 | — | — | D | 0x080e9c74 | FUN_080e9c74 | set_img_proxy_vram_slot | 1 | [eval](eval/080e9c74.md) |
| 80 | 101 | — | — | E | 0x08015c90 | FUN_08015c90 | copy_pltt_data_to_vram_proxy | 1 | [eval](eval/08015c90.md) |
| 81 | 102 | — | — | D | 0x080e9a94 | FUN_080e9a94 | init_img_proxy_fields | 1 | [eval](eval/080e9a94.md) |
| 82 | 103 | — | — | D | 0x080eb1f4 | FUN_080eb1f4 | get_anim_sequence_ptr_by_index | 1 | [eval](eval/080eb1f4.md) |
| 83 | 104 | — | — | D | 0x080e9c38 | FUN_080e9c38 | init_renderer_img_proxy_fields | 1 | [eval](eval/080e9c38.md) |
| 84 | 105 | — | — | D | 0x08015d30 | FUN_08015d30 | load_g2d_obj_resource_set | 1 | [eval](eval/08015d30.md) |
| 85 | 106 | — | — | E | 0x08013940 | FUN_08013940 | load_demo_obj_resource_by_slot | 1 | [eval](eval/08013940.md) |
| 86 | 107 | — | — | E | 0x0801398c | FUN_0801398c | load_demo_obj_resource_slot0 | 1 | [eval](eval/0801398c.md) |
| 87 | 108 | — | — | E | 0x0801399c | FUN_0801399c | write_bg3_scroll_regs | 1 | [eval](eval/0801399c.md) |
| 88 | 109 | — | — | E | 0x080139b8 | FUN_080139b8 | tick_demo_bg3_hscroll | 1 | [eval](eval/080139b8.md) |
| 89 | 110 | — | — | E | 0x08013a10 | FUN_08013a10 | tick_demo_bg3_vscroll | 1 | [eval](eval/08013a10.md) |
| 90 | 111 | — | — | D | 0x080e8b6c | FUN_080e8b6c | set_cell_anim_sequence_by_index | 2 | [eval](eval/080e8b6c.md) |
| 91 | 113 | — | — | D | 0x080e8f88 | FUN_080e8f88 | set_cell_anim_sequence_by_idx_guarded | 1 | [eval](eval/080e8f88.md) |
| 92 | 114 | — | — | D | 0x080e95ec | FUN_080e95ec | step_cell_anim_sequence_guarded | 1 | [eval](eval/080e95ec.md) |
| 93 | 115 | — | — | D | 0x080156e0 | FUN_080156e0 | dispatch_cell_anim_sequence_step | 1 | [eval](eval/080156e0.md) |
| 94 | 116 | — | — | D | 0x080e957c | FUN_080e957c | advance_cell_anim_frame_guarded | 1 | [eval](eval/080e957c.md) |
| 95 | 117 | — | — | D | 0x0801571c | FUN_0801571c | dispatch_cell_anim_frame_advance | 1 | [eval](eval/0801571c.md) |
| 96 | 118 | — | — | E | 0x08015924 | FUN_08015924 | resolve_bg_affine_param_offset | 1 | [eval](eval/08015924.md) |
| 97 | 119 | — | — | E | 0x08016108 | FUN_08016108 | resolve_isd_affine_matrix_ptr | 1 | [eval](eval/08016108.md) |
| 98 | 120 | — | — | E | 0x080151b4 | FUN_080151b4 | assign_palette_slot_entry | 1 | [eval](eval/080151b4.md) |
| 99 | 121 | — | — | D | 0x080151d8 | FUN_080151d8 | alloc_palette_entry_slot | 1 | [eval](eval/080151d8.md) |
| 100 | 122 | — | — | D | 0x080e969c | FUN_080e969c | build_oam_attrs_from_cell_with_affine | 2 | [eval](eval/080e969c.md) |
| 101 | 123 | — | — | D | 0x08015954 | FUN_08015954 | setup_isd_cell_anim_oam_entry | 2 | [eval](eval/08015954.md) |
| 102 | 124 | — | — | D | 0x08015a8c | FUN_08015a8c | dispatch_isd_cell_anim_oam_setup | 1 | [eval](eval/08015a8c.md) |
| 103 | 125 | — | — | D | 0x08015718 | FUN_08015718 | read_obj_id_field | 1 | [eval](eval/08015718.md) |
| 104 | 126 | — | — | E | 0x08013a68 | FUN_08013a68 | setup_demo_cell_anim_slot | 1 | [eval](eval/08013a68.md) |
| 105 | 127 | — | — | C | 0x080147d8 | FUN_080147d8 | gl_set_blend2_level | 2 | [eval](eval/080147d8.md) |
| 106 | 129 | — | — | E | 0x08013af4 | FUN_08013af4 | apply_demo_window_fade_in_step | 2 | [eval](eval/08013af4.md) |
| 107 | 130 | — | — | D | 0x08014914 | FUN_08014914 | tick_blend_transition_step | 1 | [eval](eval/08014914.md) |
| 108 | 131 | — | — | E | 0x08013b84 | FUN_08013b84 | apply_demo_window_fade_out_step | 1 | [eval](eval/08013b84.md) |
| 109 | 132 | — | — | E | 0x0801469c | FUN_0801469c | clear_demo_sprite_enable_bits | 1 | [eval](eval/0801469c.md) |
| 110 | 133 | — | — | D | 0x0801522c | FUN_0801522c | copy_sprite_attr_table_to_oam | 2 | [eval](eval/0801522c.md) |
| 111 | 134 | — | — | E | 0x08014838 | FUN_08014838 | init_blend_transition_params_ex | 1 | [eval](eval/08014838.md) |
| 112 | 135 | — | — | D | 0x08014754 | FUN_08014754 | init_blend_transition_params | 2 | [eval](eval/08014754.md) |
| 113 | 139 | — | — | D | 0x080148f4 | FUN_080148f4 | check_blend_transition_done | 1 | [eval](eval/080148f4.md) |
| 114 | 140 | — | — | E | 0x08013bd4 | FUN_08013bd4 | tick_demo_scene_state_machine | 1 | [eval](eval/08013bd4.md) |
| 115 | 141 | — | — | E | 0x080156c8 | FUN_080156c8 | get_title_ex_obj_field8 | 1 | [eval](eval/080156c8.md) |
| 116 | 142 | — | — | E | 0x080156cc | FUN_080156cc | set_title_ex_obj_field8 | 1 | [eval](eval/080156cc.md) |
| 117 | 144 | — | — | E | 0x08015728 | FUN_08015728 | compute_bg_affine_matrix_scaled | 2 | [eval](eval/08015728.md) |
| 118 | 145 | — | — | E | 0x08015868 | FUN_08015868 | apply_bg_affine_by_angle_scale | 1 | [eval](eval/08015868.md) |
| 119 | 146 | — | — | E | 0x0801b7e8 | FUN_0801b7e8 | init_demo_shuen_display_state | 2 | [eval](eval/0801b7e8.md) |
| 120 | 147 | — | — | E | 0x0801b850 | FUN_0801b850 | load_demo_shuen_sprite_gfx | 3 | [eval](eval/0801b850.md) |
| 121 | 148 | 7 | 1 | E | 0x0801b91c | FUN_0801b91c | load_shuen_sprite_gfx_guarded | 1 | [eval](eval/0801b91c.md) |
| 122 | 149 | 7 | 1 | E | 0x0801b93c | FUN_0801b93c | load_shuen_bg1_gfx_set | 1 | [eval](eval/0801b93c.md) |
| 123 | 150 | 7 | 1 | E | 0x0801ba04 | FUN_0801ba04 | load_shuen_obj_resource_by_slot | 1 | [eval](eval/0801ba04.md) |
| 124 | 151 | 6 | 2 | E | 0x0801ba4c | FUN_0801ba4c | load_shuen_obj_resource_slot0 | 1 | [eval](eval/0801ba4c.md) |
| 125 | 152 | 8 | 2 | E | 0x0801ba5c | FUN_0801ba5c | write_shuen_bg3_scroll_regs | 1 | [eval](eval/0801ba5c.md) |
| 126 | 153 | 7 | 1 | E | 0x0801ba78 | FUN_0801ba78 | tick_demo_shuen_bg3_hscroll | 1 | [eval](eval/0801ba78.md) |
| 127 | 154 | 8 | 1 | E | 0x0801bb28 | FUN_0801bb28 | advance_shuen_cell_anim_frame | 1 | [eval](eval/0801bb28.md) |
| 128 | 156 | 7 | 1 | E | 0x0801bbd4 | FUN_0801bbd4 | tick_shuen_anim_slots_batch | 1 | [eval](eval/0801bbd4.md) |
| 129 | 158 | 6 | 3 | E | 0x0801c2ac | FUN_0801c2ac | reset_gl_display_state | 1 | [eval](eval/0801c2ac.md) |
| 130 | 159 | 8 | 1 | E | 0x0801c310 | FUN_0801c310 | load_vija_bg_gfx_embedded | 1 | [eval](eval/0801c310.md) |
| 131 | 160 | 8 | 1 | E | 0x0801c3f4 | FUN_0801c3f4 | load_vija_bg_gfx_from_fs | 2 | [eval](eval/0801c3f4.md) |
| 132 | 161 | 7 | 2 | E | 0x0801c484 | FUN_0801c484 | load_vija_bg_gfx_by_mode | 2 | [eval](eval/0801c484.md) |
| 133 | 162 | 7 | 1 | E | 0x0801c4c0 | FUN_0801c4c0 | load_vija_obj_resource_by_region | 1 | [eval](eval/0801c4c0.md) |
| 134 | 163 | 6 | 3 | E | 0x0801c50c | FUN_0801c50c | load_vija_obj_resource_gated | 1 | [eval](eval/0801c50c.md) |
| 135 | 164 | 9 | 2 | E | 0x0801c5d8 | FUN_0801c5d8 | drive_vija_obj_cell_anim | 1 | [eval](eval/0801c5d8.md) |
| 136 | 165 | 8 | 1 | E | 0x0801c668 | FUN_0801c668 | apply_bg2_affine_fixed_angle | 1 | [eval](eval/0801c668.md) |
| 137 | 166 | 7 | 1 | E | 0x0801c694 | FUN_0801c694 | tick_bg2_affine_anim_frame | 1 | [eval](eval/0801c694.md) |
| 138 | 167 | 7 | 1 | E | 0x0801c6b0 | FUN_0801c6b0 | tick_bg_scroll_anim_frame | 1 | [eval](eval/0801c6b0.md) |
| 139 | 168 | 9 | 1 | E | 0x0801c728 | FUN_0801c728 | advance_scene_phase_counter | 1 | [eval](eval/0801c728.md) |
| 140 | 169 | 9 | 1 | E | 0x0801c74c | FUN_0801c74c | update_dual_cell_anim_oam_pos | 2 | [eval](eval/0801c74c.md) |
| 141 | 170 | 8 | 1 | E | 0x0801c794 | FUN_0801c794 | tick_vija_obj_anim_slot | 1 | [eval](eval/0801c794.md) |
| 142 | 171 | 7 | 1 | E | 0x0801cadc | FUN_0801cadc | tick_all_vija_obj_anim_slots | 1 | [eval](eval/0801cadc.md) |
| 143 | 173 | 6 | 3 | E | 0x0801cb00 | FUN_0801cb00 | run_vija_scene_state_machine | 1 | [eval](eval/0801cb00.md) |
| 144 | 246 | 7 | 2 | E | 0x0801e6f4 | FUN_0801e6f4 | open_card_info_page_from_list | 1 | [eval](eval/0801e6f4.md) |
| 145 | 249 | 2 | 3 | E | 0x0801e850 | FUN_0801e850 | fill_card_fs_display_entries | 1 | [eval](eval/0801e850.md) |
| 146 | 250 | 2 | 1 | E | 0x0801e974 | FUN_0801e974 | fill_card_fs_display_entries_for_card_list | 1 | [eval](eval/0801e974.md) |
| 147 | 251 | 4 | 2 | E | 0x0810d0a4 | FUN_0810d0a4 | write_sound_engine_request | 1 | [eval](eval/0810d0a4.md) |
| 148 | 252 | 3 | 6 | D | 0x080f9b40 | FUN_080f9b40 | request_sound_engine_code10 | 1 | [eval](eval/080f9b40.md) |
| 149 | 253 | 6 | 4 | E | 0x080f2c8c | FUN_080f2c8c | render_decimal_digits_jp | 1 | [eval](eval/080f2c8c.md) |
| 150 | 254 | 5 | 7 | D | 0x08037b90 | FUN_08037b90 | get_player_deck_flag_bit1 | 1 | [eval](eval/08037b90.md) |
| 151 | 256 | 5 | 43 | C | 0x0802fd60 | FUN_0802fd60 | find_effect_node_in_zone | 1 | [eval](eval/0802fd60.md) |
| 152 | 257 | 4 | 22 | C | 0x0803b618 | FUN_0803b618 | get_zone_card_attribute_by_type | 1 | [eval](eval/0803b618.md) |
| 153 | 258 | 8 | 4 | E | 0x0802fb2c | FUN_0802fb2c | find_node_by_value_and_zone_type | 1 | [eval](eval/0802fb2c.md) |
| 154 | 259 | 7 | 17 | D | 0x0802fdc0 | FUN_0802fdc0 | check_node_in_slot_chain | 1 | [eval](eval/0802fdc0.md) |
| 155 | 260 | 7 | 7 | D | 0x080eeea8 | FUN_080eeea8 | get_card_extended_stat_field8 | 1 | [eval](eval/080eeea8.md) |
| 156 | 261 | 8 | 7 | D | 0x0804ad70 | FUN_0804ad70 | check_card_field8_is_normal | 1 | [eval](eval/0804ad70.md) |
| 157 | 262 | 7 | 5 | D | 0x08030aa4 | FUN_08030aa4 | check_slot_card_is_equip_type | 1 | [eval](eval/08030aa4.md) |
| 158 | 263 | 5 | 4 | E | 0x08032358 | FUN_08032358 | classify_card_effect_category | 1 | [eval](eval/08032358.md) |
| 159 | 264 | 7 | 13 | D | 0x0803412c | FUN_0803412c | check_card_matches_active_effect_slot | 1 | [eval](eval/0803412c.md) |
| 160 | 265 | 7 | 3 | E | 0x0802f434 | FUN_0802f434 | count_slot_equip_list_matches | 1 | [eval](eval/0802f434.md) |
| 161 | 266 | 1 | 21 | C | 0x080eee50 | FUN_080eee50 | get_card_extended_stat_field5 | 1 | [eval](eval/080eee50.md) |
| 162 | 267 | 1 | 135 | C | 0x0804ad48 | FUN_0804ad48 | check_card_field5_is_nonzero | 1 | [eval](eval/0804ad48.md) |
| 163 | 268 | 1 | 34 | C | 0x080eee7c | FUN_080eee7c | get_card_extended_stat_field9 | 1 | [eval](eval/080eee7c.md) |
| 164 | 269 | 1 | 59 | C | 0x08032654 | FUN_08032654 | count_available_effect_zones | 1 | [eval](eval/08032654.md) |
| 165 | 270 | 1 | 117 | C | 0x0803279c | FUN_0803279c | count_field_copies_of_card | 1 | [eval](eval/0803279c.md) |
| 166 | 271 | 1 | 12 | D | 0x080364b0 | FUN_080364b0 | check_slot_card_effect_eligibility | 1 | [eval](eval/080364b0.md) |
| 167 | 272 | 1 | 17 | D | 0x08036658 | FUN_08036658 | query_slot_effect_eligibility_nonzero | 1 | [eval](eval/08036658.md) |
| 168 | 273 | 1 | 7 | D | 0x080314d4 | FUN_080314d4 | resolve_slot_card_id_for_pair | 1 | [eval](eval/080314d4.md) |
| 169 | 275 | 1 | 14 | D | 0x08031564 | FUN_08031564 | check_slot_card_pair_allowed | 1 | [eval](eval/08031564.md) |
| 170 | 276 | 1 | 12 | D | 0x08034180 | FUN_08034180 | find_paired_zone_entry_for_card | 1 | [eval](eval/08034180.md) |
| 171 | 277 | 1 | 57 | C | 0x08032548 | FUN_08032548 | test_slot_has_active_card | 1 | [eval](eval/08032548.md) |
| 172 | 278 | 1 | 12 | D | 0x08036674 | FUN_08036674 | check_slot_card_fieldspell_eligibility | 1 | [eval](eval/08036674.md) |
| 173 | 279 | 1 | 104 | C | 0x080eedf8 | FUN_080eedf8 | get_card_extended_stat_field6 | 1 | [eval](eval/080eedf8.md) |
| 174 | 280 | 1 | 2 | E | 0x0803ac04 | FUN_0803ac04 | query_slot_card_state_code | 1 | [eval](eval/0803ac04.md) |
| 175 | 281 | 1 | 44 | C | 0x0803abf0 | FUN_0803abf0 | get_slot_card_state_code | 1 | [eval](eval/0803abf0.md) |
| 176 | 282 | 1 | 21 | C | 0x080eee24 | FUN_080eee24 | get_card_extended_stat_field7 | 1 | [eval](eval/080eee24.md) |
| 177 | 283 | 1 | 3 | E | 0x0803aed0 | FUN_0803aed0 | resolve_slot_chain_best_target | 1 | [eval](eval/0803aed0.md) |
| 178 | 284 | 1 | 8 | D | 0x0803b1b0 | FUN_0803b1b0 | compute_slot_zone_eligibility_mask | 1 | [eval](eval/0803b1b0.md) |
| 179 | 285 | 1 | 1 | E | 0x0803a540 | FUN_0803a540 | check_slot_equip_chain_rule | 1 | [eval](eval/0803a540.md) |
| 180 | 286 | 1 | 3 | E | 0x0804af60 | FUN_0804af60 | check_card_is_gravekeeper | 1 | [eval](eval/0804af60.md) |
| 181 | 287 | 7 | 2 | E | 0x08037c9c | FUN_08037c9c | compute_zone_effect_atk_delta | 1 | [eval](eval/08037c9c.md) |
| 182 | 288 | 6 | 1 | E | 0x0803a658 | FUN_0803a658 | classify_equip_target_eligibility | 1 | [eval](eval/0803a658.md) |
| 183 | 289 | 7 | 5 | D | 0x0802faf4 | FUN_0802faf4 | find_node_by_value | 1 | [eval](eval/0802faf4.md) |
| 184 | 290 | 8 | 2 | E | 0x0802fcc0 | FUN_0802fcc0 | check_value_in_effect_context_chain | 1 | [eval](eval/0802fcc0.md) |
| 185 | 291 | 6 | 33 | C | 0x0802fe60 | FUN_0802fe60 | get_node_entity_id_in_slot | 1 | [eval](eval/0802fe60.md) |
| 186 | 292 | 8 | 1 | E | 0x0804c1b8 | FUN_0804c1b8 | get_card_effect_zone_check_sides | 1 | [eval](eval/0804c1b8.md) |
| 187 | 293 | 5 | 52 | C | 0x08030de8 | FUN_08030de8 | find_zone_descriptor_by_slot_id | 1 | [eval](eval/08030de8.md) |
| 188 | 294 | 8 | 9 | D | 0x0804c16c | FUN_0804c16c | check_card_is_zone_pair_restricted | 1 | [eval](eval/0804c16c.md) |
| 189 | 295 | 6 | 107 | C | 0x0802fc90 | FUN_0802fc90 | check_value_in_slot_chain | 1 | [eval](eval/0802fc90.md) |
| 190 | 296 | 8 | 2 | E | 0x0802f27c | FUN_0802f27c | count_zone_chain_eligible_cards | 1 | [eval](eval/0802f27c.md) |
| 191 | 297 | 7 | 16 | D | 0x0802f394 | FUN_0802f394 | count_equip_chain_default_flags | 1 | [eval](eval/0802f394.md) |
| 192 | 298 | 8 | 18 | D | 0x0804b4f4 | FUN_0804b4f4 | get_card_field_summon_restriction | 1 | [eval](eval/0804b4f4.md) |
| 193 | 299 | 6 | 14 | D | 0x08034298 | FUN_08034298 | check_card_targeted_by_spell_zone_effect | 1 | [eval](eval/08034298.md) |
| 194 | 300 | 7 | 2 | E | 0x0805a9a8 | FUN_0805a9a8 | check_card_placement_rules | 1 | [eval](eval/0805a9a8.md) |
| 195 | 302 | 6 | 43 | C | 0x0803b2b4 | FUN_0803b2b4 | get_zone_slot_ptr | 1 | [eval](eval/0803b2b4.md) |
| 196 | 303 | 6 | 1 | E | 0x08036c2c | FUN_08036c2c | build_effect_zone_entry | 1 | [eval](eval/08036c2c.md) |
| 197 | 304 | 7 | 93 | C | 0x08080d6c | FUN_08080d6c | read_effect_slot_side_and_type | 1 | [eval](eval/08080d6c.md) |
| 198 | 305 | 6 | 1 | E | 0x08036b88 | FUN_08036b88 | find_effect_entry_by_player_zone | 1 | [eval](eval/08036b88.md) |
| 199 | 306 | 5 | 1 | E | 0x0803a7f0 | FUN_0803a7f0 | build_equip_target_eligibility_table | 1 | [eval](eval/0803a7f0.md) |
| 200 | 307 | 4 | 4 | E | 0x080c8d30 | FUN_080c8d30 | refresh_zone_effect_buff_cache | 1 | [eval](eval/080c8d30.md) |
| 201 | 308 | 4 | 4 | E | 0x0803b4b0 | FUN_0803b4b0 | get_zone_slot_card_ref_by_type | 1 | [eval](eval/0803b4b0.md) |
| 202 | 309 | 4 | 13 | D | 0x0803b5c0 | FUN_0803b5c0 | get_zone_slot_field6_by_type | 1 | [eval](eval/0803b5c0.md) |
| 203 | 311 | 4 | 22 | C | 0x080cc8c8 | FUN_080cc8c8 | ensure_card_id_cache_entry | 1 | [eval](eval/080cc8c8.md) |
| 204 | 312 | 7 | 18 | D | 0x0802f5b0 | FUN_0802f5b0 | find_equip_chain_node_by_slot_pair | 1 | [eval](eval/0802f5b0.md) |
| 205 | 313 | 6 | 27 | C | 0x0802f680 | FUN_0802f680 | find_equip_chain_pair_across_field | 1 | [eval](eval/0802f680.md) |
| 206 | 314 | 6 | 6 | D | 0x08032e80 | FUN_08032e80 | count_monster_slots_by_state | 1 | [eval](eval/08032e80.md) |
| 207 | 315 | 6 | 8 | D | 0x08033e70 | FUN_08033e70 | count_hand_cards_by_field6 | 1 | [eval](eval/08033e70.md) |
| 208 | 316 | 6 | 1 | E | 0x08038c02 | FUN_08038c02 | compute_lp_cost_by_hand_field6 | 1 | [eval](eval/08038c02.md) |
| 209 | 317 | 7 | 4 | E | 0x080373ac | FUN_080373ac | count_zone_slots_with_card_field5 | 1 | [eval](eval/080373ac.md) |
| 210 | 318 | 6 | 1 | E | 0x08038e00 | FUN_08038e00 | compute_lp_cost_by_zone_field5_both_players | 1 | [eval](eval/08038e00.md) |
| 211 | 319 | 6 | 17 | D | 0x080370dc | FUN_080370dc | count_extra_deck_cards_by_id | 1 | [eval](eval/080370dc.md) |
| 212 | 320 | 6 | 1 | E | 0x08038d08 | FUN_08038d08 | compute_lp_cost_by_extra_deck_card_id | 1 | [eval](eval/08038d08.md) |
| 213 | 321 | 6 | 7 | D | 0x0803730c | FUN_0803730c | count_hand_cards_with_field5 | 1 | [eval](eval/0803730c.md) |
| 214 | 322 | 6 | 5 | D | 0x080eef0c | FUN_080eef0c | lookup_rom_card_attribute_table_a | 1 | [eval](eval/080eef0c.md) |
| 215 | 323 | 7 | 5 | D | 0x08032bc8 | FUN_08032bc8 | count_paired_slots_with_field5 | 1 | [eval](eval/08032bc8.md) |
| 216 | 324 | 6 | 27 | C | 0x08032c94 | FUN_08032c94 | count_paired_slots_with_field5_default | 1 | [eval](eval/08032c94.md) |
| 217 | 326 | 6 | 7 | D | 0x08033214 | FUN_08033214 | count_monster_slots_by_fnptr | 1 | [eval](eval/08033214.md) |
| 218 | 327 | 7 | 46 | C | 0x08033188 | FUN_08033188 | count_occupied_monster_zones | 1 | [eval](eval/08033188.md) |
| 219 | 328 | 6 | 4 | E | 0x080331bc | FUN_080331bc | count_occupied_monster_zones_with_effect_bonus | 1 | [eval](eval/080331bc.md) |
| 220 | 329 | 6 | 1 | E | 0x08038a1a | FUN_08038a1a | compute_lp_cost_by_occupied_monster_zones | 1 | [eval](eval/08038a1a.md) |
| 221 | 330 | 7 | 8 | D | 0x0804be38 | FUN_0804be38 | get_card_effect_category | 1 | [eval](eval/0804be38.md) |
| 222 | 331 | 6 | 16 | D | 0x0803149c | FUN_0803149c | get_slot_effect_card_value | 1 | [eval](eval/0803149c.md) |
| 223 | 332 | 7 | 6 | D | 0x08032904 | FUN_08032904 | count_zones_by_card_and_mode | 1 | [eval](eval/08032904.md) |
| 224 | 333 | 7 | 10 | D | 0x0802f3a8 | FUN_0802f3a8 | query_zone_chain_count_with_eligibility | 1 | [eval](eval/0802f3a8.md) |
| 225 | 334 | 7 | 1 | E | 0x0803a428 | FUN_0803a428 | adjust_slot_score_by_chain_and_zone | 1 | [eval](eval/0803a428.md) |
| 226 | 335 | 7 | 3 | E | 0x0804b30c | FUN_0804b30c | check_card_id_is_special_summon_type | 1 | [eval](eval/0804b30c.md) |
| 227 | 336 | 6 | 8 | D | 0x08032ef0 | FUN_08032ef0 | count_monster_slots_by_state_all | 1 | [eval](eval/08032ef0.md) |
| 228 | 337 | 7 | 1 | E | 0x0803309c | FUN_0803309c | count_active_slots_with_field6_value | 1 | [eval](eval/0803309c.md) |
| 229 | 338 | 7 | 2 | E | 0x0803407c | FUN_0803407c | eval_slot_target_eligibility_full | 1 | [eval](eval/0803407c.md) |
| 230 | 339 | 6 | 1 | E | 0x08038e1e | FUN_08038e1e | apply_slot_score_bonus_by_state | 1 | [eval](eval/08038e1e.md) |
| 231 | 340 | 6 | 1 | E | 0x08034020 | FUN_08034020 | count_hand_cards_by_field6_alt | 1 | [eval](eval/08034020.md) |
| 232 | 341 | 6 | 1 | E | 0x0803a520 | FUN_0803a520 | cleanup_slot_score_entry_epilogue | 1 | [eval](eval/0803a520.md) |
| 233 | 342 | 6 | 9 | D | 0x08032ca4 | FUN_08032ca4 | count_paired_slots_both_sides | 1 | [eval](eval/08032ca4.md) |
| 234 | 343 | 7 | 5 | D | 0x08030048 | FUN_08030048 | find_equip_chain_node_by_pred | 1 | [eval](eval/08030048.md) |
| 235 | 344 | 7 | 19 | D | 0x0803b230 | FUN_0803b230 | check_slot_zone_bit_eligible | 1 | [eval](eval/0803b230.md) |
| 236 | 345 | 6 | 29 | C | 0x0803a9a8 | FUN_0803a9a8 | eval_equip_chain_score_for_slot | 1 | [eval](eval/0803a9a8.md) |
| 237 | 346 | 6 | 38 | C | 0x08030a30 | FUN_08030a30 | check_slot_card_is_equip_whitelist | 1 | [eval](eval/08030a30.md) |
| 238 | 347 | 6 | 1 | E | 0x08038dd4 | FUN_08038dd4 | compute_lp_cost_by_zone_field5_x100 | 1 | [eval](eval/08038dd4.md) |
| 239 | 348 | 6 | 16 | D | 0x080eeed4 | FUN_080eeed4 | get_card_extended_stat_field3 | 1 | [eval](eval/080eeed4.md) |
| 240 | 349 | 6 | 3 | E | 0x0802f4e0 | FUN_0802f4e0 | count_active_extended_chain_nodes | 1 | [eval](eval/0802f4e0.md) |
| 241 | 350 | 6 | 1 | E | 0x08038dea | FUN_08038dea | compute_lp_cost_by_zone_field5_x200 | 1 | [eval](eval/08038dea.md) |
| 242 | 351 | 5 | 3 | E | 0x08037ec0 | FUN_08037ec0 | eval_slot_score_entry_full | 1 | [eval](eval/08037ec0.md) |
| 243 | 352 | 7 | 5 | D | 0x080ca660 | FUN_080ca660 | decode_card_image_tiles_to_vram | 1 | [eval](eval/080ca660.md) |
| 244 | 353 | 7 | 3 | E | 0x0804bf20 | FUN_0804bf20 | check_card_id_is_equip_set_b | 1 | [eval](eval/0804bf20.md) |
| 245 | 354 | 7 | 3 | E | 0x0804bd78 | FUN_0804bd78 | check_card_id_is_equip_set_a | 1 | [eval](eval/0804bd78.md) |
| 246 | 355 | 7 | 3 | E | 0x080cae84 | FUN_080cae84 | write_card_digit_tiles_to_vram | 1 | [eval](eval/080cae84.md) |
| 247 | 356 | 7 | 2 | E | 0x080cace8 | FUN_080cace8 | zero_card_display_vram_regions | 1 | [eval](eval/080cace8.md) |
| 248 | 357 | 7 | 2 | E | 0x080caf68 | FUN_080caf68 | render_card_name_to_sprite_vram | 1 | [eval](eval/080caf68.md) |
| 249 | 358 | 6 | 4 | E | 0x08030b70 | FUN_08030b70 | check_card_stat_field7_equals | 1 | [eval](eval/08030b70.md) |
| 250 | 359 | 6 | 3 | E | 0x0802fbbc | FUN_0802fbbc | count_chain_nodes_by_card_id | 1 | [eval](eval/0802fbbc.md) |
| 251 | 360 | 6 | 3 | E | 0x0802fc34 | FUN_0802fc34 | count_slot_chain_nodes_by_card_id | 1 | [eval](eval/0802fc34.md) |
| 252 | 361 | 6 | 2 | E | 0x080377b0 | FUN_080377b0 | eval_equip_bonus_for_slot | 1 | [eval](eval/080377b0.md) |
| 253 | 362 | 7 | 3 | E | 0x080c933c | FUN_080c933c | map_card_id_to_digit_tile_offset | 1 | [eval](eval/080c933c.md) |
| 254 | 363 | 6 | 2 | E | 0x080cb1cc | FUN_080cb1cc | render_large_card_display_by_mode | 1 | [eval](eval/080cb1cc.md) |
| 255 | 364 | 7 | 4 | D | 0x080f2c4c | FUN_080f2c4c | render_decimal_digits_jp_signed | 1 | [eval](eval/080f2c4c.md) |
| 256 | 365 | 7 | 2 | E | 0x080c7894 | FUN_080c7894 | init_bg_vram_for_card_display | 1 | [eval](eval/080c7894.md) |
| 257 | 366 | 7 | 3 | E | 0x080c9a10 | FUN_080c9a10 | write_oam_card_icon_strip | 1 | [eval](eval/080c9a10.md) |
| 258 | 367 | 7 | 2 | E | 0x080c9374 | FUN_080c9374 | write_nibble_palette_rows_to_vram | 1 | [eval](eval/080c9374.md) |
| 259 | 368 | 7 | 3 | E | 0x080c992c | FUN_080c992c | render_card_type_icon_to_vram | 1 | [eval](eval/080c992c.md) |
| 260 | 369 | 7 | 2 | E | 0x080c9ac8 | FUN_080c9ac8 | tick_card_icon_anim_step | 1 | [eval](eval/080c9ac8.md) |
| 261 | 370 | 7 | 2 | E | 0x080c9c94 | FUN_080c9c94 | advance_card_display_effect_step | 1 | [eval](eval/080c9c94.md) |
| 262 | 371 | 7 | 3 | D | 0x080f0720 | FUN_080f0720 | test_char_kinsoku_tail | 1 | [eval](eval/080f0720.md) |
| 263 | 372 | 7 | 4 | D | 0x080c76c0 | FUN_080c76c0 | render_jp_string_to_tile_line | 1 | [eval](eval/080c76c0.md) |
| 264 | 373 | 7 | 2 | E | 0x080f370c | FUN_080f370c | write_glyph_nibble_rows_to_vram | 1 | [eval](eval/080f370c.md) |
| 265 | 374 | 7 | 2 | E | 0x080f37d4 | FUN_080f37d4 | write_line_buf_to_bg_tile_vram | 1 | [eval](eval/080f37d4.md) |
| 266 | 375 | 7 | 2 | E | 0x080ce218 | FUN_080ce218 | render_card_label_text_to_bg | 1 | [eval](eval/080ce218.md) |
| 267 | 376 | 7 | 2 | E | 0x080cd9a0 | FUN_080cd9a0 | init_card_palette_and_tile_vram | 1 | [eval](eval/080cd9a0.md) |
| 268 | 377 | 7 | 2 | E | 0x080cf330 | FUN_080cf330 | init_card_stat_tile_and_scroll | 1 | [eval](eval/080cf330.md) |
| 269 | 378 | 7 | 8 | D | 0x080eec54 | FUN_080eec54 | resolve_game_str_ptr | 1 | [eval](eval/080eec54.md) |
| 270 | 379 | 7 | 2 | E | 0x080cf25c | FUN_080cf25c | render_card_numeric_stat_to_bg | 1 | [eval](eval/080cf25c.md) |
| 271 | 380 | 7 | 2 | E | 0x080cf3b0 | FUN_080cf3b0 | render_card_stat_label_with_value | 1 | [eval](eval/080cf3b0.md) |
| 272 | 381 | 7 | 3 | D | 0x080f5054 | FUN_080f5054 | copy_cstr_to_buf | 1 | [eval](eval/080f5054.md) |
| 273 | 382 | 7 | 2 | E | 0x080d03b0 | FUN_080d03b0 | init_choice_label_vram_case1 | 1 | [eval](eval/080d03b0.md) |
| 274 | 383 | 7 | 2 | E | 0x080cceb8 | FUN_080cceb8 | init_choice_label_vram_case8 | 1 | [eval](eval/080cceb8.md) |
| 275 | 384 | 7 | 2 | E | 0x080cd33c | FUN_080cd33c | render_card_name_label_to_bg | 1 | [eval](eval/080cd33c.md) |
| 276 | 385 | 7 | 2 | E | 0x080c78bc | FUN_080c78bc | init_card_icon_tile_and_palette | 1 | [eval](eval/080c78bc.md) |
| 277 | 386 | 7 | 3 | E | 0x080c3b50 | FUN_080c3b50 | render_field_zone_mini_card_tiles | 1 | [eval](eval/080c3b50.md) |
| 278 | 387 | 7 | 3 | E | 0x080c9eb8 | FUN_080c9eb8 | write_decimal_digits_to_oam | 1 | [eval](eval/080c9eb8.md) |
| 279 | 388 | 6 | 2 | E | 0x08095b50 | FUN_08095b50 | check_player_side_condition | 1 | [eval](eval/08095b50.md) |
| 280 | 389 | 7 | 2 | E | 0x080c3790 | FUN_080c3790 | get_field_slot_tile_vram_addr | 1 | [eval](eval/080c3790.md) |
| 281 | 398 | 6 | 1 | E | 0x080c3840 | FUN_080c3840 | blit_field_slot_tile_with_palette_hi | 1 | [eval](eval/080c3840.md) |
| 282 | 399 | 6 | 40 | C | 0x080333ac | FUN_080333ac | check_slot_placement_blocked_by_field_effect | 1 | [eval](eval/080333ac.md) |
| 283 | 400 | 5 | 9 | D | 0x080c3880 | FUN_080c3880 | update_field_slot_tile_display | 2 | [eval](eval/080c3880.md) |
| 284 | 401 | 6 | 3 | E | 0x0803b960 | FUN_0803b960 | check_zone_has_no_field_spell_node | 1 | [eval](eval/0803b960.md) |
| 285 | 403 | 7 | 15 | D | 0x080904f4 | FUN_080904f4 | find_card_effect_node_entry | 1 | [eval](eval/080904f4.md) |
| 286 | 404 | 8 | 14 | D | 0x08090848 | FUN_08090848 | dispatch_card_effect_activation | 1 | [eval](eval/08090848.md) |
| 287 | 405 | 7 | 7 | D | 0x08031390 | FUN_08031390 | resolve_slot_id_to_zone_ptr | 1 | [eval](eval/08031390.md) |
| 288 | 406 | 8 | 3 | E | 0x0804bc90 | FUN_0804bc90 | get_card_equip_zone_rank | 1 | [eval](eval/0804bc90.md) |
| 289 | 407 | 8 | 3 | E | 0x08055930 | FUN_08055930 | get_card_lp_cost_by_id | 1 | [eval](eval/08055930.md) |
| 290 | 408 | 8 | 2 | E | 0x08033bb0 | FUN_08033bb0 | check_slot_available_for_card | 1 | [eval](eval/08033bb0.md) |
| 291 | 409 | 7 | 11 | D | 0x0803310c | FUN_0803310c | count_occupied_all_field_zones | 1 | [eval](eval/0803310c.md) |
| 292 | 410 | 7 | 28 | C | 0x08033bf4 | FUN_08033bf4 | find_first_available_monster_slot_for_player | 2 | [eval](eval/08033bf4.md) |
| 293 | 411 | 7 | 4 | E | 0x0805aea4 | FUN_0805aea4 | apply_card_equip_activation | 1 | [eval](eval/0805aea4.md) |
| 294 | 412 | 8 | 1 | E | 0x0805a238 | FUN_0805a238 | check_spell_zone_slot_face_down | 1 | [eval](eval/0805a238.md) |
| 295 | 413 | 8 | 1 | E | 0x0803026c | FUN_0803026c | get_card_equip_target_zone_cost | 1 | [eval](eval/0803026c.md) |
| 296 | 414 | 7 | 2 | E | 0x0805a86c | FUN_0805a86c | check_equip_card_can_target_partner | 1 | [eval](eval/0805a86c.md) |
| 297 | 415 | 6 | 3 | E | 0x08033c9c | FUN_08033c9c | check_field_spell_placement_allowed | 1 | [eval](eval/08033c9c.md) |
| 298 | 416 | 6 | 3 | E | 0x0804c014 | FUN_0804c014 | check_card_is_equip_set_c | 1 | [eval](eval/0804c014.md) |
| 299 | 417 | 7 | 6 | D | 0x0805a570 | FUN_0805a570 | check_card_zone_activation_blocked | 1 | [eval](eval/0805a570.md) |
| 300 | 418 | 6 | 1 | E | 0x0805b164 | FUN_0805b164 | invoke_equip_zone_activation_check | 2 | [eval](eval/0805b164.md) |
| 301 | 419 | 7 | 15 | D | 0x0804a9dc | FUN_0804a9dc | map_field8_to_card_type_category | 1 | [eval](eval/0804a9dc.md) |
| 302 | 420 | 7 | 3 | E | 0x0804b81c | FUN_0804b81c | get_card_special_group_code | 1 | [eval](eval/0804b81c.md) |
| 303 | 421 | 6 | 20 | C | 0x0804ba58 | FUN_0804ba58 | check_card_has_equip_placement_type | 1 | [eval](eval/0804ba58.md) |
| 304 | 422 | 7 | 1 | E | 0x0804c18c | FUN_0804c18c | check_card_is_field_spell_type_b | 1 | [eval](eval/0804c18c.md) |
| 305 | 423 | 6 | 2 | E | 0x080309fc | FUN_080309fc | check_field_spell_b_placeable | 1 | [eval](eval/080309fc.md) |
| 306 | 424 | 6 | 4 | E | 0x0803b910 | FUN_0803b910 | check_lp_exceeds_spell_copy_threshold | 1 | [eval](eval/0803b910.md) |
| 307 | 425 | 8 | 3 | E | 0x0802fb6c | FUN_0802fb6c | find_node_by_value_zone_entity | 1 | [eval](eval/0802fb6c.md) |
| 308 | 426 | 7 | 10 | D | 0x0802fdf4 | FUN_0802fdf4 | check_slot_has_node_by_card_id | 1 | [eval](eval/0802fdf4.md) |
| 309 | 427 | 7 | 6 | D | 0x0803b9f4 | FUN_0803b9f4 | check_field_spell_card_placeable_strict | 1 | [eval](eval/0803b9f4.md) |
| 310 | 428 | 7 | 4 | E | 0x0803b980 | FUN_0803b980 | check_field_spell_group_placeable | 1 | [eval](eval/0803b980.md) |
| 311 | 429 | 7 | 2 | E | 0x0804ba90 | FUN_0804ba90 | check_card_not_equip_placement_type | 1 | [eval](eval/0804ba90.md) |
| 312 | 430 | 8 | 53 | C | 0x08033730 | FUN_08033730 | check_slot_card_can_be_equipped | 1 | [eval](eval/08033730.md) |
| 313 | 431 | 8 | 6 | D | 0x08033688 | FUN_08033688 | check_slot_equip_eligibility | 2 | [eval](eval/08033688.md) |
| 314 | 432 | 8 | 6 | D | 0x080337f0 | FUN_080337f0 | check_equip_cards_share_field7 | 2 | [eval](eval/080337f0.md) |
| 315 | 433 | 8 | 7 | D | 0x0803352c | FUN_0803352c | check_monster_slot_accepts_card | 1 | [eval](eval/0803352c.md) |
| 316 | 434 | 7 | 73 | C | 0x080335b8 | FUN_080335b8 | count_available_monster_slots | 1 | [eval](eval/080335b8.md) |
| 317 | 435 | 8 | 5 | D | 0x08033654 | FUN_08033654 | find_first_placeable_monster_slot | 1 | [eval](eval/08033654.md) |
| 318 | 436 | 7 | 17 | D | 0x08033634 | FUN_08033634 | get_first_placeable_monster_slot | 1 | [eval](eval/08033634.md) |
| 319 | 437 | 7 | 1 | E | 0x080a4490 | FUN_080a4490 | eval_equip_targets_for_card | 2 | [eval](eval/080a4490.md) |
| 320 | 438 | 7 | 5 | D | 0x0804c6cc | FUN_0804c6cc | get_paired_card_id_by_variant | 1 | [eval](eval/0804c6cc.md) |
| 321 | 439 | 7 | 4 | E | 0x080338b8 | FUN_080338b8 | count_equip_placements_with_chain_check | 2 | [eval](eval/080338b8.md) |
| 322 | 440 | 7 | 2 | E | 0x080a4648 | FUN_080a4648 | check_player_can_place_card | 1 | [eval](eval/080a4648.md) |
| 323 | 441 | 7 | 7 | D | 0x0804b164 | FUN_0804b164 | check_card_id_is_normal_summon_type | 1 | [eval](eval/0804b164.md) |
| 324 | 442 | 7 | 1 | E | 0x080a4574 | FUN_080a4574 | check_equip_slot_has_field_spell_target | 2 | [eval](eval/080a4574.md) |
| 325 | 443 | 8 | 2 | E | 0x08032e20 | FUN_08032e20 | count_equip_slots_meeting_atk_threshold | 2 | [eval](eval/08032e20.md) |
| 326 | 444 | 8 | 6 | D | 0x08033610 | FUN_08033610 | count_monster_slots_accepting_card | 1 | [eval](eval/08033610.md) |
| 327 | 445 | 7 | 1 | E | 0x080a45f4 | FUN_080a45f4 | check_equip_card_activation_valid | 1 | [eval](eval/080a45f4.md) |
| 328 | 446 | 6 | 6 | D | 0x080a46a0 | FUN_080a46a0 | eval_card_placement_flags_for_ai | 1 | [eval](eval/080a46a0.md) |
| 329 | 447 | 5 | 7 | D | 0x080a4694 | FUN_080a4694 | eval_card_placement_flags_default | 1 | [eval](eval/080a4694.md) |
| 330 | 448 | 7 | 11 | D | 0x080313dc | FUN_080313dc | get_equip_card_set_code_for_slot | 1 | [eval](eval/080313dc.md) |
| 331 | 449 | 8 | 1 | E | 0x080a533c | FUN_080a533c | check_equip_slot_pair_can_activate | 1 | [eval](eval/080a533c.md) |
| 332 | 450 | 7 | 1 | E | 0x080a3a80 | FUN_080a3a80 | scan_activatable_equip_slots_init | 2 | [eval](eval/080a3a80.md) |
| 333 | 451 | 7 | 2 | E | 0x08031184 | FUN_08031184 | find_slot_idx_by_set_code | 1 | [eval](eval/08031184.md) |
| 334 | 452 | 8 | 5 | D | 0x080324b4 | FUN_080324b4 | find_equip_slot_by_card_id | 1 | [eval](eval/080324b4.md) |
| 335 | 453 | 7 | 9 | D | 0x08033088 | FUN_08033088 | check_toon_world_equip_present | 1 | [eval](eval/08033088.md) |
| 336 | 454 | 8 | 1 | E | 0x080a57b8 | FUN_080a57b8 | check_equip_slot_pair_can_activate_alt | 1 | [eval](eval/080a57b8.md) |
| 337 | 455 | 7 | 2 | E | 0x080a3d0c | FUN_080a3d0c | scan_activatable_equip_slots_alt | 2 | [eval](eval/080a3d0c.md) |
| 338 | 456 | 7 | 1 | E | 0x080a3c2c | FUN_080a3c2c | check_banisher_of_light_activatable | 2 | [eval](eval/080a3c2c.md) |
| 339 | 457 | 7 | 1 | E | 0x080a3dac | FUN_080a3dac | check_equip_set_activatable_for_player | 2 | [eval](eval/080a3dac.md) |
| 340 | 458 | 8 | 29 | C | 0x0803bc24 | FUN_0803bc24 | check_spell_zone_slot_placeable | 1 | [eval](eval/0803bc24.md) |
| 341 | 459 | 8 | 2 | E | 0x080a422c | FUN_080a422c | classify_spell_card_activation_type | 1 | [eval](eval/080a422c.md) |
| 342 | 460 | 7 | 1 | E | 0x0808da68 | FUN_0808da68 | find_effect_record_index_by_id | 1 | [eval](eval/0808da68.md) |
| 343 | 461 | 6 | 101 | C | 0x0808dab0 | FUN_0808dab0 | dispatch_effect_handler_by_card_id | 1 | [eval](eval/0808dab0.md) |
| 344 | 462 | 8 | 2 | E | 0x0803bb04 | FUN_0803bb04 | check_field_spell_neo_daedalus_placeable | 1 | [eval](eval/0803bb04.md) |
| 345 | 463 | 7 | 85 | C | 0x0803bb7c | FUN_0803bb7c | check_field_spell_neo_daedalus_group_placeable | 1 | [eval](eval/0803bb7c.md) |
| 346 | 464 | 7 | 1 | E | 0x080a42b0 | FUN_080a42b0 | eval_spell_card_activation_placeable | 1 | [eval](eval/080a42b0.md) |
| 347 | 465 | 8 | 14 | D | 0x08037a2c | FUN_08037a2c | count_valid_monster_pair_slots | 1 | [eval](eval/08037a2c.md) |
| 348 | 466 | 7 | 1 | E | 0x080a3eb4 | FUN_080a3eb4 | eval_equip_card_placeable_for_player | 1 | [eval](eval/080a3eb4.md) |
| 349 | 467 | 8 | 1 | E | 0x08032fa4 | FUN_08032fa4 | count_unpaired_slots_for_card | 1 | [eval](eval/08032fa4.md) |
| 350 | 468 | 7 | 1 | E | 0x080a4134 | FUN_080a4134 | check_ritual_fusion_pairable_slots_exist | 1 | [eval](eval/080a4134.md) |
| 351 | 469 | 7 | 1 | E | 0x080a40bc | FUN_080a40bc | check_equip_target_monster_placeable | 1 | [eval](eval/080a40bc.md) |
| 352 | 470 | 7 | 16 | D | 0x080339d8 | FUN_080339d8 | count_equippable_slots_for_card | 1 | [eval](eval/080339d8.md) |
| 353 | 471 | 7 | 1 | E | 0x080a3fc8 | FUN_080a3fc8 | eval_equip_card_multi_target_placeable | 1 | [eval](eval/080a3fc8.md) |
| 354 | 472 | 8 | 4 | E | 0x0803b1a4 | FUN_0803b1a4 | resolve_best_target_slot_for_equip | 1 | [eval](eval/0803b1a4.md) |
| 355 | 473 | 7 | 1 | E | 0x080a43c8 | FUN_080a43c8 | eval_spell_equip_target_availability | 1 | [eval](eval/080a43c8.md) |
| 356 | 474 | 7 | 6 | D | 0x08032ccc | FUN_08032ccc | count_equipped_paired_slots_for_player | 1 | [eval](eval/08032ccc.md) |
| 357 | 475 | 8 | 1 | E | 0x080a80a8 | FUN_080a80a8 | check_slot_equip_target_eligible | 1 | [eval](eval/080a80a8.md) |
| 358 | 476 | 7 | 1 | E | 0x080a4058 | FUN_080a4058 | init_spell_activation_context | 1 | [eval](eval/080a4058.md) |
| 359 | 477 | 9 | 1 | E | 0x0804b350 | FUN_0804b350 | check_card_id_in_fusion_target_range | 1 | [eval](eval/0804b350.md) |
| 360 | 478 | 7 | 4 | E | 0x0802f1f8 | FUN_0802f1f8 | count_slot_chain_copies_of_card | 1 | [eval](eval/0802f1f8.md) |

---

## 历史里程碑

- 2026-05-08: **batch=20 #20 PASSED** — duel core spell/equip activation eval cluster (dispatch_effect_handler_by_card_id indeg=101 + check_field_spell_neo_daedalus_group_placeable indeg=85 + classify_spell_card_activation_type BST + find_effect_record_index_by_id binary search + eval_spell_card_activation_placeable + count_valid_monster_pair_slots r8 non-APCS + eval_equip_card_placeable_for_player r10 non-APCS + count_unpaired_slots_for_card + check_ritual_fusion_pairable_slots_exist + check_equip_target_monster_placeable + count_equippable_slots_for_card r10 non-APCS + eval_equip_card_multi_target_placeable r8 non-APCS + resolve_best_target_slot_for_equip wrapper + eval_spell_equip_target_availability + count_equipped_paired_slots_for_player r8/r10 non-APCS + check_slot_equip_target_eligible r12 non-APCS + init_spell_activation_context gSpellContext init + check_card_id_in_fusion_target_range BST + count_slot_chain_copies_of_card); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (360/1526 = 23.59%)
- 2026-05-08: **batch=20 #19 PASSED** — duel field equip activation/scan cluster (eval_card_placement_flags_for_ai/default sibling + scan_activatable_equip_slots init/alt + Toon World/Banisher of Light named card activation check + check_spell_zone_slot_placeable indeg=29) + monster slot/equip slot BST classifiers; 1 fix iter (3 NEEDS_FIX: 2 R1 bare hex card_id -> card name + 1 R3 internal working register mislabeled caller-set); first-shot 17/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (340/1526 = 22.28%)
- 2026-05-08: **batch=20 #18 PASSED** — duel field equip/placement validator chain (slot equip eligibility indeg=53 + count_monster_slots indeg=73 + field_spell_b_placeable + field_spell_group_placeable + monster_slot_accepts_card + first_placeable_monster_slot 兄弟 + equip_lock effect ID 标签); 1+1 fix iter (5 R7 caller addr 自引用/缺 +1 R6 + 2 R2 plate 字数 + 2 R6 0xb FIELD_SPELL_ZONE); first-shot 15/20; 跨过 20% 里程碑 (320/1526 = 20.97%); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b.
- 2026-05-08: **batch=20 #17 PASSED** — duel field placement/equip activation chain (slot placement blocker indeg=40 + monster slot finder indeg=28 + equip card target + activation dispatch + field spell allowed + equip set _c sibling + apply_card_equip_activation + check_card_zone_activation_blocked + invoke_equip_zone_activation_check) + field slot display update + zone descriptor resolver + find_card_effect_node_entry + dispatch_card_effect_activation; 1 fix iter (3 NEEDS_FIX: R7 caller addr placeholder + R3 player_id mislabeled card_id + R3 r3 internal sp clobber + R7 self-reference); first-shot 17/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (300/1526 = 19.66%)
- 2026-05-08: **batch=20 #16 PASSED** — card display VRAM rendering pipeline (jp_string/glyph_nibble/line_buf/card_label/stat/name/choice_label 簇) + game_str pointer resolver indeg=8 + write_decimal_digits_to_oam + 多 init_*_vram 兄弟簇; 1+1+1 fix iter (3 R3 callsite + 2 R7 caller addr r9/r10 上层调用链 + r8/r10 callee-save 删除 + r9 范围 [0..0x01FF]); first-shot 17/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (280/1526 = 18.35%)
- 2026-05-08: **batch=20 #15 PASSED (单 call 模式)** — LP cost 补全 (compute_lp_cost_by_zone_field5_x200 + eval_slot_score_entry_full) + card display pipeline 簇 (decode_card_image_tiles_to_vram + write_card_digit_tiles_to_vram + zero_card_display_vram_regions + render_card_name_to_sprite_vram + map_card_id_to_digit_tile_offset + render_large_card_display_by_mode + render_decimal_digits_jp_signed + init_bg_vram_for_card_display + write_oam_card_icon_strip + write_nibble_palette_rows_to_vram + render_card_type_icon_to_vram + tick_card_icon_anim_step) + equip set classifiers (check_card_id_is_equip_set_a/b) + duel util (check_card_stat_field7_equals + count_chain_nodes_by_card_id + count_slot_chain_nodes_by_card_id + eval_equip_bonus_for_slot); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (260/1526 = 17.04%)
- 2026-05-08: **batch=20 #14 PASSED (单 call 模式)** — duel core 评估/计数/装备链/LP cost 簇 (get_card_effect_category + get_slot_effect_card_value + count_zones_by_card_and_mode + query_zone_chain_count_with_eligibility + adjust_slot_score_by_chain_and_zone + check_card_id_is_special_summon_type + count_monster_slots_by_state_all + count_active_slots_with_field6_value + eval_slot_target_eligibility_full + apply_slot_score_bonus_by_state + count_hand_cards_by_field6_alt (冲突重命名) + cleanup_slot_score_entry_epilogue + count_paired_slots_both_sides + find_equip_chain_node_by_pred + check_slot_zone_bit_eligible + eval_equip_chain_score_for_slot indeg=29 + check_slot_card_is_equip_whitelist indeg=38 + compute_lp_cost_by_zone_field5_x100 + get_card_extended_stat_field3 (sibling cluster 第 5 元) + count_active_extended_chain_nodes); 1 name collision fix (0x08034020 count_hand_cards_by_field6 → count_hand_cards_by_field6_alt, offsets 0x1c/0x5d0 vs 0x14/0x418); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (240/1526 = 15.73%)
- 2026-05-08: **batch=20 #13 PASSED** — duel field count/cost util cluster (find_equip_chain_node/pair + count_monster_slots_by_state/fnptr + count_occupied_monster_zones indeg=46 + count_occupied_monster_zones_with_effect_bonus + count_paired_slots_with_field5 indeg=27 + count_hand_cards_by_field6/with_field5 + count_extra_deck_cards_by_id + count_zone_slots_with_card_field5 + 4x compute_lp_cost_by_* dispatch branches + get_zone_slot_card_ref/field6_by_type + ensure_card_id_cache_entry indeg=22 + lookup_rom_card_attribute_table_a); 1 fix iter (non-APCS r8 inputs clarified); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (220/1526 = 14.42%)
- 2026-05-07: **batch=20 #12 PASSED** — duel core util cluster (effect/equip node pool 链 + zone slot ptr resolver indeg=43 + card BST classifiers indeg=18+9+1 + zone descriptor finder indeg=52 + card_id whitelist + slot pair check) + Gravekeeper 后续 placement rules; 1+1 fix iter (R3 r12 internal-set 标识 + R6 ROM ATK base + r0 歧义清除); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (200/1526 = 13.10%)
- 2026-05-07: **batch=20 #11 PASSED** — 0x080eexx card extended stat getter 4-sibling 簇 (field5/6/7/9) + 0x0804ad48 indeg=135 dispatch wrapper + duel core util cluster (slot card pair check / active-card test / effect zone counter / equip chain rule / Gravekeeper card-id whitelist); 1 fix iter (R6 状态码符号化 + effect_code 计算修正); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (180/1526 = 11.80%)
- 2026-05-07: **batch=20 #10 PASSED** — vija UI effect scene 收尾 (anim slot tick + state machine) + card list info page bridge + sound engine request 簇 + duel core util cluster (effect node 查询/zone attribute getter/slot chain check/card field8 谓词); 1 fix iter (6 NEEDS_FIX: 4 R3 范围 + 1 R6 + 1 R2/R4 switch 反向修正); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (160/1526 = 10.49%)
- 2026-05-07: **campaign-9 batch PASSED** — demo_shuen 完整运行时簇 (state machine sub-funcs/scroll tick/cell anim batch) + vija UI effect scene 平行簇 (BG/OBJ load by region+mode/OBJ cell anim driver/affine tick) + reset_gl_display_state 跨 scene 重置 hub; 1 fix iter (3 R3: entry-clobber + 参数互换 + index 范围); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (140/1526 = 9.17%)
- 2026-05-06: **campaign-8 batch PASSED** — scene_demo 状态机 tick + window fade in/out + BG affine math + demo_shuen 资源加载 + ISD title_ex obj stub 簇; 6 R3+R5+R6 修复 (IO base 误读 0x04000026/WIN0H 误读 BLDCNT/r1-r2 颠倒/EWRAM-VRAM 混淆/r0-r2 矛盾/r8 输入误判 callee-saved); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (120/1526 = 7.86%)
- 2026-05-06: **campaign-7 batch PASSED** — ISD/cell anim OAM 入口 hub 簇 (3 个 D_shared_mid 跨 3 scene 共享: dispatch_cell_anim_sequence_step/dispatch_cell_anim_frame_advance/dispatch_isd_cell_anim_oam_setup) + gl_set_blend2_level (indeg=13) + palette slot allocator; 3 R3 修复 (高寄存器 callee-save vs 真输入 + 内部 DAT 加载误判为参数); byte-identical 保持. (105/1526 = 6.88%)
- 2026-05-06: **campaign-6 batch PASSED** — IG2D_Main FS loader hub (load_g2d_obj_resource_set @ 0x08015d30) + Exodia demo OBJ asset load (asset table @ 0x09e397d4) + scene_demo BG3 scroll tick + g2d_NCG_load.c parser; 2 fix iter (R4 void, R7 caller role); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (90/1526 = 5.90%)
- 2026-05-06: **campaign-5 batch PASSED** — NitroSDK G2D library wrapper 第 3 簇 (g2d_NAN_load.c / g2d_NCL_load.c / g2d_NOB_load.c / GL/IG2D_Main.c); 1 R5 register-typo 3-round 修复; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (75/1526 = 4.91%)
- 2026-05-06: **campaign-4 batch PASSED** — NitroSDK G2D library wrapper 第 2 簇 (CellAnimation/Image/SRTControl/g2d_Load); 1 R3 r1 misclassified-as-unused fix iter; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (60/1526 = 3.93%)
- 2026-05-05: **campaign-3 batch PASSED** — Exodia demo loader (`demo/exodia/exodia*.LZ5bg` assets) + NitroSDK G2D library wrappers (g2d_Animation / g2d_NOB_load / g2d_SRTControl); 2 R3 AAPCS-callee-saved-vs-non-APCS-input fix iter; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (45/1526 = 2.95%)
- 2026-05-05: **campaign-2 batch PASSED** — gfx-resource list dispatcher + BG char/OBJ tile copy cluster (5 R3 unit-fix iter); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (30/1526 = 1.97%)
- 2026-05-05: **campaign-1 batch PASSED** — campaign_scene_handler 闭包前 25 topo idx 中 15 函数 (gl/bg/palette init+util utility cluster, 2 R1/R4 fix iter); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b 保持. (15/1526 = 0.98%)
- 2026-05-05: **Step 0 完成 (campaign_scene_handler root)**: (1) 切换 root: 0x080e7994 enter_campaign_page (静态闭包仅 3 fn) → 0x08025c94 真实状态机入口. (2) Force-disassemble 3 块 .incbin (0x25d58 0x1f20 / 0x27e50 0x6c / 0x27f00 0x518) 中的 42 个 state handlers + 8 个 promoted sub-routines, 共 +50 functions. (3) 新增 `tools/ghidra-labeling/DisassembleCampaignRegion.py` (基于 DisassembleNameInputRegion.py 模板). (4) 新增 `tools/ad-hoc/{manual_dispatch_edges.csv, merge_manual_edges.py}` 处理 `mov pc,r0` 派发模式 (resolve_fnptr_tables.py 仅识别 invoker-thunk 派发). (5) byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b 全程保持. 闭包 28 → 1698 functions (A_named=150 已命名 + 1526 待命名).
- 2026-05-05: **🎉 完成 root=`enter_deck_edit_page` (0x08108ac0) 任务: 259/259 函数命名 100%, byte-identical 全程一致 (SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b), 16 batches × ~15 funcs, 全部 45/45 通过. 累计沉淀 27 feedback 文件锁入 agent (待 root 切换后保留所有规则).** Last commit: `c999fa5`.
- 2026-05-04: 切换根函数到 `enter_campaign_page` (0x080e7994). PROGRESS.md 重置 (BLOCKED 段保留). 已命名函数池 259 个跨根复用.

## BLOCKED 追踪

| SB 编号 | 日期 | 阻塞原因 | 解除前置条件 |
|---------|------|----------|-------------|
| SB-080fa4dc-1 | 2026-05-02 | r3 assert_type 枚举语义需 debug build 验证 (函数命名本身已 PASSED) | 找到 debug build 或匹配工程的 assert 宏定义 |
| SB-080f5e98-1 | 2026-05-02 | 条目 +5 / +1 的 bit mask 操作语义需 mGBA 在 scene_card_list 初始化时 dump gPrng+0x1bc 所指内存结构 (before/after) 确认 | mGBA 断点 FUN_080f5ef4 入口，dump [gPrng+0x1bc] before/after 各条目的 +5/+1 字节变化 |

> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`

## 失败追踪 (auto-skip)

> fixer 在 byte-identical ❌ / MAX_ITER / agent 求助 / 完全无法命名 时追加。
> pick_batch.py 自动:
>   - 排除 ADDR 在本表的函数 (本身失败)
>   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)
>   - 函数列表对应行标 ⚠ FAIL / ⏭ SKIP

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |
