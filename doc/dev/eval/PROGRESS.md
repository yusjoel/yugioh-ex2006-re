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
| **当前步骤** | Step 1 — executor (batch=20 全自动模式, campaign-50) |
| **下一步** | `python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json` → 启动 4-agent loop (campaign-50, 下一候选: topo=1038+) |
| **上次更新** | 2026-05-14 (campaign-49 batch #49, 887/1526) |
| **上次 callgraph 刷新** | 2026-05-05 (含 +50 新反汇 fns, +131 callgraph 边, +26 manual dispatch 边) |
| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |

## 进度

**887 / 1526 已分析** (campaign_scene_handler 闭包: 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过, 待命名 1526)

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
| 361 | 479 | 8 | 2 | E | 0x080a5498 | FUN_080a5498 | check_equip_slot_pair_can_activate_full | 1 | [eval](eval/080a5498.md) |
| 362 | 480 | 8 | 1 | E | 0x080a5714 | FUN_080a5714 | check_equip_slot_can_activate_with_context | 1 | [eval](eval/080a5714.md) |
| 363 | 481 | 7 | 1 | E | 0x080a3ae8 | FUN_080a3ae8 | scan_equip_activation_for_player | 1 | [eval](eval/080a3ae8.md) |
| 364 | 482 | 7 | 21 | C | 0x080312ec | FUN_080312ec | find_slot_idx_by_card_id_in_player_zones | 1 | [eval](eval/080312ec.md) |
| 365 | 483 | 8 | 2 | E | 0x080a3b50 | FUN_080a3b50 | get_equip_activation_mode_by_card_id | 1 | [eval](eval/080a3b50.md) |
| 366 | 484 | 7 | 1 | E | 0x080a3b74 | FUN_080a3b74 | scan_equip_activation_with_mode | 1 | [eval](eval/080a3b74.md) |
| 367 | 485 | 7 | 1 | E | 0x080a3d74 | FUN_080a3d74 | check_banisher_pair_activation_allowed | 1 | [eval](eval/080a3d74.md) |
| 368 | 486 | 6 | 4 | E | 0x080a4af4 | FUN_080a4af4 | eval_equip_target_slot_flags | 1 | [eval](eval/080a4af4.md) |
| 369 | 487 | 5 | 1 | E | 0x08095fe0 | FUN_08095fe0 | eval_spell_activation_flags_by_zone | 1 | [eval](eval/08095fe0.md) |
| 370 | 488 | 7 | 6 | D | 0x0804ae2c | FUN_0804ae2c | check_card_stat_field8_is_8 | 1 | [eval](eval/0804ae2c.md) |
| 371 | 489 | 6 | 3 | E | 0x0809058c | FUN_0809058c | check_card_has_activatable_effect_node | 1 | [eval](eval/0809058c.md) |
| 372 | 490 | 6 | 3 | E | 0x0804c05c | FUN_0804c05c | check_card_id_is_equip_blocker | 1 | [eval](eval/0804c05c.md) |
| 373 | 491 | 6 | 6 | D | 0x0805a3e0 | FUN_0805a3e0 | eval_equip_activation_for_slot | 1 | [eval](eval/0805a3e0.md) |
| 374 | 492 | 6 | 5 | D | 0x0805a280 | FUN_0805a280 | setup_equip_context_for_slot_activation | 1 | [eval](eval/0805a280.md) |
| 375 | 493 | 6 | 4 | E | 0x0805a354 | FUN_0805a354 | setup_equip_context_for_zone_activation | 1 | [eval](eval/0805a354.md) |
| 376 | 494 | 6 | 1 | E | 0x0803b738 | FUN_0803b738 | read_player_field_slot_word_by_zone | 1 | [eval](eval/0803b738.md) |
| 377 | 495 | 5 | 3 | E | 0x080968f4 | FUN_080968f4 | check_zone_slot_card_activatable | 1 | [eval](eval/080968f4.md) |
| 378 | 496 | 5 | 1 | E | 0x08096864 | FUN_08096864 | eval_zone_activation_flags_for_player | 1 | [eval](eval/08096864.md) |
| 379 | 497 | 6 | 16 | D | 0x0804ae04 | FUN_0804ae04 | check_card_stat_field8_is_6 | 1 | [eval](eval/0804ae04.md) |
| 380 | 498 | 7 | 2 | E | 0x08032d1c | FUN_08032d1c | count_equip_set_activatable_slots_for_player | 1 | [eval](eval/08032d1c.md) |
| 381 | 499 | 6 | 6 | D | 0x08034358 | FUN_08034358 | check_slot_field_action_eligibility | 2 | [eval](eval/08034358.md) |
| 382 | 500 | 7 | 3 | E | 0x0803ba98 | FUN_0803ba98 | check_field_spell_last_warrior_placeable | 2 | [eval](eval/0803ba98.md) |
| 383 | 501 | 6 | 3 | E | 0x080345e0 | FUN_080345e0 | check_field_spell_slot_placeable | 2 | [eval](eval/080345e0.md) |
| 384 | 502 | 6 | 2 | E | 0x080346c4 | FUN_080346c4 | check_slot_monster_activation_eligible | 2 | [eval](eval/080346c4.md) |
| 385 | 503 | 8 | 1 | E | 0x08035280 | FUN_08035280 | exit_slot_activation_with_state_write | 2 | [eval](eval/08035280.md) |
| 386 | 504 | 7 | 3 | E | 0x08033cf8 | FUN_08033cf8 | check_player_has_equip_type_in_slots | 2 | [eval](eval/08033cf8.md) |
| 387 | 505 | 7 | 4 | E | 0x08035988 | FUN_08035988 | check_slot_field_spell_chain_eligible | 2 | [eval](eval/08035988.md) |
| 388 | 506 | 7 | 2 | E | 0x08035b24 | FUN_08035b24 | check_field_spell_trap_chain_eligible | 2 | [eval](eval/08035b24.md) |
| 389 | 507 | 8 | 1 | E | 0x08032dac | FUN_08032dac | count_equip_zone_slots_matching_card | 2 | [eval](eval/08032dac.md) |
| 390 | 508 | 7 | 7 | D | 0x08034a58 | FUN_08034a58 | check_slot_full_activation_eligibility | 2 | [eval](eval/08034a58.md) |
| 391 | 509 | 6 | 8 | D | 0x080349b0 | FUN_080349b0 | check_slot_card_activatable | 2 | [eval](eval/080349b0.md) |
| 392 | 510 | 6 | 6 | D | 0x08035ba4 | FUN_08035ba4 | check_player_field_spell_chain_eligible | 2 | [eval](eval/08035ba4.md) |
| 393 | 511 | 7 | 9 | D | 0x08030b0c | FUN_08030b0c | check_slot_card_is_monster_type | 2 | [eval](eval/08030b0c.md) |
| 394 | 512 | 7 | 6 | D | 0x0802f61c | FUN_0802f61c | count_equip_slots_with_active_chain | 2 | [eval](eval/0802f61c.md) |
| 395 | 513 | 7 | 7 | D | 0x0804aea0 | FUN_0804aea0 | check_card_is_archfiend_type | 2 | [eval](eval/0804aea0.md) |
| 396 | 514 | 7 | 1 | E | 0x0804b048 | FUN_0804b048 | check_card_is_amazoness_type | 2 | [eval](eval/0804b048.md) |
| 397 | 515 | 7 | 41 | C | 0x0803a958 | FUN_0803a958 | get_slot_field5_score | 2 | [eval](eval/0803a958.md) |
| 398 | 516 | 8 | 10 | D | 0x080366f0 | FUN_080366f0 | check_slot_fieldspell_eligible_by_side | 2 | [eval](eval/080366f0.md) |
| 399 | 517 | 7 | 3 | E | 0x0802f3e0 | FUN_0802f3e0 | query_slot_effect_eligibility_with_equip_fallback | 2 | [eval](eval/0802f3e0.md) |
| 400 | 518 | 7 | 3 | E | 0x080332f0 | FUN_080332f0 | count_slots_matching_card_pair | 2 | [eval](eval/080332f0.md) |
| 401 | 519 | 6 | 11 | D | 0x080352b0 | FUN_080352b0 | eval_slot_activation_eligibility_full | 1 | [eval](eval/080352b0.md) |
| 402 | 520 | 7 | 1 | E | 0x08033d44 | FUN_08033d44 | check_any_slot_fieldspell_zone_eligible | 1 | [eval](eval/08033d44.md) |
| 403 | 521 | 7 | 5 | D | 0x08033294 | FUN_08033294 | count_slots_with_chain_field_match | 1 | [eval](eval/08033294.md) |
| 404 | 522 | 6 | 6 | D | 0x08035bc8 | FUN_08035bc8 | eval_slot_fieldspell_activation_full | 1 | [eval](eval/08035bc8.md) |
| 405 | 523 | 5 | 9 | D | 0x0803495c | FUN_0803495c | eval_slot_activation_guard_full | 1 | [eval](eval/0803495c.md) |
| 406 | 524 | 5 | 1 | E | 0x08096264 | FUN_08096264 | setup_equip_slot_activation_entry | 1 | [eval](eval/08096264.md) |
| 407 | 525 | 5 | 2 | E | 0x08096954 | FUN_08096954 | dispatch_zone_effect_by_slot | 1 | [eval](eval/08096954.md) |
| 408 | 526 | 5 | 1 | E | 0x0809678c | FUN_0809678c | eval_zone_activation_flags_by_type | 1 | [eval](eval/0809678c.md) |
| 409 | 527 | 6 | 3 | E | 0x0805b0cc | FUN_0805b0cc | build_zone_activation_entry_blocked | 1 | [eval](eval/0805b0cc.md) |
| 410 | 528 | 6 | 1 | E | 0x0805b034 | FUN_0805b034 | build_zone_activation_entry_equip | 1 | [eval](eval/0805b034.md) |
| 411 | 529 | 5 | 1 | E | 0x0809650c | FUN_0809650c | setup_equip_slot_activation_entry_alt | 1 | [eval](eval/0809650c.md) |
| 412 | 530 | 4 | 5 | D | 0x08096b3c | FUN_08096b3c | dispatch_zone_activation_by_state | 1 | [eval](eval/08096b3c.md) |
| 413 | 531 | 5 | 2 | E | 0x080c89a8 | FUN_080c89a8 | query_player_slot_activation_bitmask | 1 | [eval](eval/080c89a8.md) |
| 414 | 532 | 4 | 5 | D | 0x080c38cc | FUN_080c38cc | render_field_slot_card_tile | 1 | [eval](eval/080c38cc.md) |
| 415 | 533 | 4 | 6 | D | 0x080c4220 | FUN_080c4220 | refresh_player_field_slot_tiles | 1 | [eval](eval/080c4220.md) |
| 416 | 534 | 4 | 4 | E | 0x080c39fc | FUN_080c39fc | render_field_zone_card_tile_by_type | 1 | [eval](eval/080c39fc.md) |
| 417 | 535 | 3 | 1 | E | 0x080c4d04 | FUN_080c4d04 | redraw_all_field_slot_tiles | 1 | [eval](eval/080c4d04.md) |
| 418 | 536 | 3 | 1 | E | 0x080c36a8 | FUN_080c36a8 | write_palette_tile_row_to_vram | 1 | [eval](eval/080c36a8.md) |
| 419 | 537 | 4 | 5 | D | 0x080ee3a8 | FUN_080ee3a8 | apply_palette_offset_to_tile_row | 1 | [eval](eval/080ee3a8.md) |
| 420 | 538 | 4 | 1 | E | 0x080ca4f4 | FUN_080ca4f4 | upload_player_icon_gfx_to_vram | 1 | [eval](eval/080ca4f4.md) |
| 421 | 539 | 4 | 3 | E | 0x080ca5f8 | FUN_080ca5f8 | write_lp_digit_tiles_to_vram | 1 | [eval](eval/080ca5f8.md) |
| 422 | 540 | 3 | 1 | E | 0x080ca8ec | FUN_080ca8ec | init_duel_field_tile_indices | 1 | [eval](eval/080ca8ec.md) |
| 423 | 542 | 5 | 3 | E | 0x080f7e0c | FUN_080f7e0c | resolve_aob_pattern_entry_ptr | 1 | [eval](eval/080f7e0c.md) |
| 424 | 543 | 4 | 14 | D | 0x080f7e48 | FUN_080f7e48 | init_aob_ctx_with_anm_entry | 1 | [eval](eval/080f7e48.md) |
| 425 | 544 | 4 | 14 | D | 0x080f7da4 | FUN_080f7da4 | init_aob_ctx_from_ptnsect | 1 | [eval](eval/080f7da4.md) |
| 426 | 545 | 3 | 1 | E | 0x080c879c | FUN_080c879c | init_duel_field_lp_aob_ctx | 1 | [eval](eval/080c879c.md) |
| 427 | 546 | 2 | 8 | D | 0x080cc904 | FUN_080cc904 | init_duel_field_vram_layout | 1 | [eval](eval/080cc904.md) |
| 428 | 547 | 2 | 8 | D | 0x080cca38 | FUN_080cca38 | tick_duel_field_fadeout_step | 1 | [eval](eval/080cca38.md) |
| 429 | 548 | 2 | 10 | D | 0x080cca5c | FUN_080cca5c | tick_duel_field_fadein_step | 1 | [eval](eval/080cca5c.md) |
| 430 | 550 | 6 | 8 | D | 0x080bc7e0 | FUN_080bc7e0 | blend_palette_entry_toward_target | 1 | [eval](eval/080bc7e0.md) |
| 431 | 551 | 5 | 1 | E | 0x080be600 | FUN_080be600 | tick_banner_pack_state_machine | 1 | [eval](eval/080be600.md) |
| 432 | 552 | 6 | 2 | E | 0x080c0760 | FUN_080c0760 | write_card_image_oam_grid | 1 | [eval](eval/080c0760.md) |
| 433 | 553 | 6 | 2 | E | 0x080f5668 | FUN_080f5668 | tick_blend_step_with_bldcnt | 1 | [eval](eval/080f5668.md) |
| 434 | 554 | 8 | 2 | E | 0x080f0db4 | FUN_080f0db4 | init_line_buf_with_jp_font_flag | 1 | [eval](eval/080f0db4.md) |
| 435 | 555 | 7 | 1 | E | 0x080c0180 | FUN_080c0180 | draw_card_atkdef_label_to_vram | 1 | [eval](eval/080c0180.md) |
| 436 | 556 | 8 | 1 | E | 0x080bff34 | FUN_080bff34 | repack_nibbles_with_palette_offset | 1 | [eval](eval/080bff34.md) |
| 437 | 557 | 7 | 1 | E | 0x080bff6c | FUN_080bff6c | render_card_image_to_vram | 1 | [eval](eval/080bff6c.md) |
| 438 | 558 | 7 | 1 | E | 0x080c00f0 | FUN_080c00f0 | draw_card_name_to_bg_tile_vram | 1 | [eval](eval/080c00f0.md) |
| 439 | 559 | 8 | 1 | E | 0x080c0204 | FUN_080c0204 | write_nibble_to_bg_tile_cell | 1 | [eval](eval/080c0204.md) |
| 440 | 560 | 7 | 2 | E | 0x080c0274 | FUN_080c0274 | write_nibble_sequence_to_bg_tiles | 1 | [eval](eval/080c0274.md) |
| 441 | 561 | 6 | 2 | E | 0x080c0310 | FUN_080c0310 | write_nibble_row_pair_to_bg_tiles | 1 | [eval](eval/080c0310.md) |
| 442 | 562 | 6 | 1 | E | 0x080c0394 | FUN_080c0394 | copy_card_frame_nibbles_to_palette_vram | 1 | [eval](eval/080c0394.md) |
| 443 | 563 | 5 | 2 | E | 0x080c05b4 | FUN_080c05b4 | render_card_display_with_type_gfx | 1 | [eval](eval/080c05b4.md) |
| 444 | 564 | 5 | 2 | E | 0x080f55fc | FUN_080f55fc | clamp_blend_counter_to_target | 1 | [eval](eval/080f55fc.md) |
| 445 | 565 | 7 | 5 | D | 0x080c2d24 | FUN_080c2d24 | blit_card_frame_tile_row_to_vram | 1 | [eval](eval/080c2d24.md) |
| 446 | 566 | 4 | 1 | E | 0x080c8bf0 | FUN_080c8bf0 | build_slot_activation_mask_for_player | 1 | [eval](eval/080c8bf0.md) |
| 447 | 567 | 7 | 1 | E | 0x080f70c4 | FUN_080f70c4 | push_oam_entry_to_aob_slot | 1 | [eval](eval/080f70c4.md) |
| 448 | 568 | 6 | 11 | D | 0x080f8000 | FUN_080f8000 | render_aob_frame_to_oam | 1 | [eval](eval/080f8000.md) |
| 449 | 569 | 6 | 11 | D | 0x080f7f08 | FUN_080f7f08 | tick_aob_frame_counter | 1 | [eval](eval/080f7f08.md) |
| 450 | 570 | 8 | 1 | E | 0x080c2ddc | FUN_080c2ddc | write_digit_oam_column_with_scroll | 1 | [eval](eval/080c2ddc.md) |
| 451 | 571 | 7 | 1 | E | 0x080c2e58 | FUN_080c2e58 | render_decimal_number_to_oam | 1 | [eval](eval/080c2e58.md) |
| 452 | 572 | 6 | 1 | E | 0x080c2eac | FUN_080c2eac | render_card_number_oam_by_player | 1 | [eval](eval/080c2eac.md) |
| 453 | 573 | 5 | 1 | E | 0x080c305c | FUN_080c305c | render_dual_card_number_oam_columns | 1 | [eval](eval/080c305c.md) |
| 454 | 574 | 4 | 11 | D | 0x08096e14 | FUN_08096e14 | init_duel_zone_target_slot_refs | 1 | [eval](eval/08096e14.md) |
| 455 | 575 | 5 | 2 | E | 0x080c6800 | FUN_080c6800 | transform_zone_oam_coords_by_player | 1 | [eval](eval/080c6800.md) |
| 456 | 576 | 5 | 11 | D | 0x080c35ac | FUN_080c35ac | resolve_zone_oam_base_coords_by_type | 1 | [eval](eval/080c35ac.md) |
| 457 | 577 | 4 | 1 | E | 0x080c8aa8 | FUN_080c8aa8 | render_duel_field_slot_oam_grid | 1 | [eval](eval/080c8aa8.md) |
| 458 | 578 | 5 | 3 | E | 0x080c57c4 | FUN_080c57c4 | compute_card_sprite_oam_coords_by_zone | 1 | [eval](eval/080c57c4.md) |
| 459 | 579 | 4 | 1 | E | 0x080c6240 | FUN_080c6240 | tick_card_sprite_oam_step_a | 1 | [eval](eval/080c6240.md) |
| 460 | 582 | 5 | 2 | E | 0x080f7528 | FUN_080f7528 | write_tile_rows_to_vram_by_mode | 1 | [eval](eval/080f7528.md) |
| 461 | 583 | 8 | 1 | E | 0x080c5b78 | FUN_080c5b78 | dispatch_duel_field_zone_oam_by_type | 1 | [eval](eval/080c5b78.md) |
| 462 | 584 | 7 | 1 | E | 0x080c6184 | FUN_080c6184 | init_duel_field_card_sprite_vram | 1 | [eval](eval/080c6184.md) |
| 463 | 585 | 7 | 1 | E | 0x080c6268 | FUN_080c6268 | tick_card_sprite_oam_step_b | 1 | [eval](eval/080c6268.md) |
| 464 | 587 | 7 | 1 | E | 0x080c6490 | FUN_080c6490 | tick_card_sprite_oam_step_c | 1 | [eval](eval/080c6490.md) |
| 465 | 588 | 6 | 1 | E | 0x080c65b0 | FUN_080c65b0 | tick_card_sprite_oam_phase_dispatch | 1 | [eval](eval/080c65b0.md) |
| 466 | 589 | 5 | 6 | D | 0x080c6638 | FUN_080c6638 | resolve_zone_data_ptr_by_oam_word | 1 | [eval](eval/080c6638.md) |
| 467 | 590 | 6 | 1 | E | 0x080c64b8 | FUN_080c64b8 | dispatch_duel_zone_pair_to_oam | 1 | [eval](eval/080c64b8.md) |
| 468 | 591 | 6 | 1 | E | 0x080c5444 | FUN_080c5444 | setup_zone_oam_entry_by_field_slot | 1 | [eval](eval/080c5444.md) |
| 469 | 592 | 6 | 2 | E | 0x08096ecc | FUN_08096ecc | zero_duel_lp_display_counters | 1 | [eval](eval/08096ecc.md) |
| 470 | 593 | 7 | 1 | E | 0x0802cf98 | FUN_0802cf98 | tick_scene_blend_fadeout_step | 1 | [eval](eval/0802cf98.md) |
| 471 | 594 | 7 | 1 | E | 0x0802cfb4 | FUN_0802cfb4 | tick_scene_blend_fadein_step | 1 | [eval](eval/0802cfb4.md) |
| 472 | 595 | 6 | 1 | E | 0x0802cfd4 | FUN_0802cfd4 | tick_scene_blend_fade_sequence | 1 | [eval](eval/0802cfd4.md) |
| 473 | 596 | 6 | 1 | E | 0x080c55dc | FUN_080c55dc | init_zone_oam_ctx_by_type | 1 | [eval](eval/080c55dc.md) |
| 474 | 597 | 7 | 1 | E | 0x0802cba0 | FUN_0802cba0 | init_jp_font_linebuf_for_render | 1 | [eval](eval/0802cba0.md) |
| 475 | 598 | 7 | 1 | E | 0x0802cc08 | FUN_0802cc08 | commit_glyph_linebuf_to_sprite_vram_with_index | 1 | [eval](eval/0802cc08.md) |
| 476 | 599 | 3 | 13 | D | 0x080f5a98 | FUN_080f5a98 | upload_pack_vram_and_palette | 1 | [eval](eval/080f5a98.md) |
| 477 | 600 | 8 | 3 | E | 0x08031348 | FUN_08031348 | find_lp_entry_by_flag_and_type | 1 | [eval](eval/08031348.md) |
| 478 | 603 | 8 | 1 | E | 0x0802c30c | FUN_0802c30c | render_card_name_format_to_line | 1 | [eval](eval/0802c30c.md) |
| 479 | 604 | 8 | 3 | E | 0x080f51ac | FUN_080f51ac | expand_card_name_escape_to_buf | 1 | [eval](eval/080f51ac.md) |
| 480 | 605 | 3 | 6 | D | 0x08094e74 | FUN_08094e74 | get_card_data_bit_by_index | 1 | [eval](eval/08094e74.md) |
| 481 | 606 | 8 | 1 | E | 0x0802c238 | FUN_0802c238 | render_game_text_decimal_to_line | 1 | [eval](eval/0802c238.md) |
| 482 | 607 | 9 | 7 | D | 0x080e3258 | FUN_080e3258 | get_duel_puzzle_count | 1 | [eval](eval/080e3258.md) |
| 483 | 608 | 8 | 1 | E | 0x080e325c | FUN_080e325c | find_puzzle_slot_by_id | 1 | [eval](eval/080e325c.md) |
| 484 | 609 | 7 | 1 | E | 0x0802c358 | FUN_0802c358 | render_card_name_escape_to_line | 1 | [eval](eval/0802c358.md) |
| 485 | 610 | 6 | 1 | E | 0x0802cc68 | FUN_0802cc68 | init_card_name_result_screen | 1 | [eval](eval/0802cc68.md) |
| 486 | 611 | 7 | 1 | E | 0x080c6e9c | FUN_080c6e9c | decode_zone_oam_word_to_cursor_fields | 1 | [eval](eval/080c6e9c.md) |
| 487 | 612 | 8 | 1 | E | 0x080c4cd4 | FUN_080c4cd4 | check_lp_threshold_for_zone_slot | 1 | [eval](eval/080c4cd4.md) |
| 488 | 613 | 7 | 1 | E | 0x080c6b04 | FUN_080c6b04 | decode_zone_oam_word_to_slot_fields | 1 | [eval](eval/080c6b04.md) |
| 489 | 614 | 6 | 2 | E | 0x080c707c | FUN_080c707c | check_zone_card_id_cache_valid | 1 | [eval](eval/080c707c.md) |
| 490 | 616 | 4 | 3 | E | 0x080cc618 | FUN_080cc618 | sort_zone_oam_entries_to_vram | 1 | [eval](eval/080cc618.md) |
| 491 | 617 | 6 | 3 | E | 0x080c699c | FUN_080c699c | set_zone_oam_coords_by_player | 1 | [eval](eval/080c699c.md) |
| 492 | 619 | 4 | 2 | E | 0x08096974 | FUN_08096974 | get_lp_display_anim_counter | 1 | [eval](eval/08096974.md) |
| 493 | 622 | 7 | 2 | E | 0x080f6144 | FUN_080f6144 | write_oam_entry_attr_pairs | 1 | [eval](eval/080f6144.md) |
| 494 | 623 | 6 | 2 | E | 0x080f72e8 | FUN_080f72e8 | write_oam_sprite_entry_by_flip_mode | 1 | [eval](eval/080f72e8.md) |
| 495 | 626 | 6 | 1 | E | 0x080bf2d0 | FUN_080bf2d0 | draw_number_digits_to_oam | 1 | [eval](eval/080bf2d0.md) |
| 496 | 629 | 6 | 4 | E | 0x080fa4d8 | FUN_080fa4d8 | return_void_noop | 1 | [eval](eval/080fa4d8.md) |
| 497 | 630 | 6 | 8 | D | 0x080fa4cc | FUN_080fa4cc | suppress_display_output | 1 | [eval](eval/080fa4cc.md) |
| 498 | 633 | 7 | 5 | D | 0x080f609c | FUN_080f609c | write_obj_affine_rot_scale | 1 | [eval](eval/080f609c.md) |
| 499 | 634 | 6 | 6 | D | 0x080f6ccc | FUN_080f6ccc | write_pack_obj_attr_by_dir_stacked | 1 | [eval](eval/080f6ccc.md) |
| 500 | 636 | 3 | 2 | E | 0x080f59a0 | FUN_080f59a0 | advance_blend_evy_step | 1 | [eval](eval/080f59a0.md) |
| 501 | 637 | 3 | 2 | E | 0x080f5928 | FUN_080f5928 | start_blend_fade_with_evy | 1 | [eval](eval/080f5928.md) |
| 502 | 638 | 8 | 2 | E | 0x080f6074 | FUN_080f6074 | write_obj_affine_scale_diagonal | 1 | [eval](eval/080f6074.md) |
| 503 | 639 | 7 | 1 | E | 0x080f6adc | FUN_080f6adc | write_pack_obj_attr_by_dir | 1 | [eval](eval/080f6adc.md) |
| 504 | 640 | 6 | 3 | E | 0x080bcc6c | FUN_080bcc6c | dispatch_banner_anim_tick_by_state | 1 | [eval](eval/080bcc6c.md) |
| 505 | 641 | 6 | 5 | D | 0x080f68ec | FUN_080f68ec | write_pack_obj_attr_by_dir_split | 1 | [eval](eval/080f68ec.md) |
| 506 | 642 | 6 | 3 | E | 0x080cc694 | FUN_080cc694 | compute_duel_zone_dir_for_player | 1 | [eval](eval/080cc694.md) |
| 507 | 643 | 5 | 1 | E | 0x080bd0a8 | FUN_080bd0a8 | dispatch_banner_scene_tick_by_state | 1 | [eval](eval/080bd0a8.md) |
| 508 | 646 | 4 | 3 | E | 0x080c678c | FUN_080c678c | update_zone_oam_card_count_tag | 1 | [eval](eval/080c678c.md) |
| 509 | 647 | 6 | 1 | E | 0x080f64dc | FUN_080f64dc | write_obj_attr_256color_affine | 1 | [eval](eval/080f64dc.md) |
| 510 | 649 | 5 | 11 | D | 0x0803b3a8 | FUN_0803b3a8 | get_zone_slot_entity_ref_by_type | 1 | [eval](eval/0803b3a8.md) |
| 511 | 652 | 6 | 1 | E | 0x080c1f10 | FUN_080c1f10 | tick_pack_banner_3d_state_machine | 1 | [eval](eval/080c1f10.md) |
| 512 | 653 | 6 | 1 | E | 0x080c21a0 | FUN_080c21a0 | tick_pack_banner_3d_state_machine_alt | 1 | [eval](eval/080c21a0.md) |
| 513 | 655 | 5 | 10 | D | 0x080f67f4 | FUN_080f67f4 | write_oam_entry_with_slot_check | 1 | [eval](eval/080f67f4.md) |
| 514 | 656 | 6 | 2 | E | 0x080c124c | FUN_080c124c | render_card_zoom_oam_sprite_grid | 1 | [eval](eval/080c124c.md) |
| 515 | 658 | 5 | 2 | E | 0x080c2990 | FUN_080c2990 | write_zone_pair_oam_with_coords | 1 | [eval](eval/080c2990.md) |
| 516 | 659 | 6 | 1 | E | 0x080bdbb4 | FUN_080bdbb4 | tick_pack_banner_state_machine_b | 1 | [eval](eval/080bdbb4.md) |
| 517 | 660 | 6 | 1 | E | 0x080bda7c | FUN_080bda7c | tick_pack_banner_state_machine_a | 1 | [eval](eval/080bda7c.md) |
| 518 | 661 | 4 | 2 | E | 0x080c6a20 | FUN_080c6a20 | write_zone_slot_oam_descriptor | 1 | [eval](eval/080c6a20.md) |
| 519 | 664 | 6 | 1 | E | 0x080c4ca0 | FUN_080c4ca0 | clear_ui_effect_state_flags | 1 | [eval](eval/080c4ca0.md) |
| 520 | 665 | 5 | 1 | E | 0x080c4350 | FUN_080c4350 | dispatch_ui_effect_by_card_type | 1 | [eval](eval/080c4350.md) |
| 521 | 668 | 5 | 1 | E | 0x080c4edc | FUN_080c4edc | run_ui_effect_card_pair_state_machine | 1 | [eval](eval/080c4edc.md) |
| 522 | 669 | 5 | 1 | E | 0x080bd660 | FUN_080bd660 | tick_duel_puzzle_banner_state_machine | 1 | [eval](eval/080bd660.md) |
| 523 | 671 | 6 | 1 | E | 0x080c8fd8 | FUN_080c8fd8 | init_window_regs_for_campaign_banner | 1 | [eval](eval/080c8fd8.md) |
| 524 | 672 | 6 | 1 | E | 0x080c9030 | FUN_080c9030 | tick_campaign_banner_slide_state_machine | 1 | [eval](eval/080c9030.md) |
| 525 | 673 | 6 | 1 | E | 0x080c91bc | FUN_080c91bc | reset_blend_control_regs | 1 | [eval](eval/080c91bc.md) |
| 526 | 678 | 5 | 1 | E | 0x080bd3f4 | FUN_080bd3f4 | tick_banner_display_state_machine | 1 | [eval](eval/080bd3f4.md) |
| 527 | 682 | 3 | 2 | E | 0x0803bc58 | FUN_0803bc58 | check_card_play_condition_eligible | 1 | [eval](eval/0803bc58.md) |
| 528 | 683 | 5 | 2 | E | 0x080c9f50 | FUN_080c9f50 | render_card_view_scene_by_lp_time | 1 | [eval](eval/080c9f50.md) |
| 529 | 684 | 5 | 2 | E | 0x080cd250 | FUN_080cd250 | init_field_bg_tile_vram_layout | 1 | [eval](eval/080cd250.md) |
| 530 | 685 | 6 | 1 | E | 0x080cea50 | FUN_080cea50 | render_card_entry_jp_labels_to_bg | 1 | [eval](eval/080cea50.md) |
| 531 | 686 | 5 | 2 | E | 0x080cf7d4 | FUN_080cf7d4 | render_card_stat_tiles_to_vram | 1 | [eval](eval/080cf7d4.md) |
| 532 | 687 | 5 | 2 | E | 0x080cff50 | FUN_080cff50 | init_field_slot_tile_attrs | 1 | [eval](eval/080cff50.md) |
| 533 | 688 | 6 | 1 | E | 0x080cffd4 | FUN_080cffd4 | render_duel_zone_card_detail_to_vram | 1 | [eval](eval/080cffd4.md) |
| 534 | 689 | 6 | 1 | E | 0x080d04dc | FUN_080d04dc | render_jp_two_line_text_to_bg_vram | 1 | [eval](eval/080d04dc.md) |
| 535 | 690 | 5 | 2 | E | 0x080ca160 | FUN_080ca160 | render_lp_zone_digit_oam_row | 1 | [eval](eval/080ca160.md) |
| 536 | 691 | 6 | 1 | E | 0x080ccfe4 | FUN_080ccfe4 | render_jp_two_line_text_to_bg_vram_alt | 1 | [eval](eval/080ccfe4.md) |
| 537 | 692 | 6 | 1 | E | 0x080cda6c | FUN_080cda6c | render_jp_label_row_with_tile_count | 1 | [eval](eval/080cda6c.md) |
| 538 | 693 | 6 | 1 | E | 0x080cd870 | FUN_080cd870 | render_jp_label_row_with_tile_pos | 1 | [eval](eval/080cd870.md) |
| 539 | 694 | 5 | 2 | E | 0x080ce7f0 | FUN_080ce7f0 | zero_fill_card_label_vram_if_ready | 1 | [eval](eval/080ce7f0.md) |
| 540 | 695 | 5 | 10 | D | 0x080c7530 | FUN_080c7530 | write_card_list_oam_row_strip | 1 | [eval](eval/080c7530.md) |
| 541 | 696 | 5 | 1 | E | 0x080c7ea0 | FUN_080c7ea0 | dispatch_card_display_state_by_mode | 1 | [eval](eval/080c7ea0.md) |
| 542 | 697 | 6 | 1 | E | 0x080cf9f4 | FUN_080cf9f4 | render_card_name_jp_to_bg_tile_vram | 1 | [eval](eval/080cf9f4.md) |
| 543 | 698 | 5 | 2 | E | 0x080ce078 | FUN_080ce078 | init_card_info_display_with_jp_label | 1 | [eval](eval/080ce078.md) |
| 544 | 699 | 6 | 1 | E | 0x080cd138 | FUN_080cd138 | render_card_list_oam_row_by_lp_counter | 1 | [eval](eval/080cd138.md) |
| 545 | 700 | 6 | 1 | E | 0x080cd5ec | FUN_080cd5ec | render_card_list_oam_row_by_nibble_rotate | 1 | [eval](eval/080cd5ec.md) |
| 546 | 701 | 6 | 1 | E | 0x080cd94c | FUN_080cd94c | render_card_list_oam_row_by_flag_check | 1 | [eval](eval/080cd94c.md) |
| 547 | 702 | 6 | 1 | E | 0x080cdd70 | FUN_080cdd70 | render_card_list_oam_row_by_lp_nibble | 1 | [eval](eval/080cdd70.md) |
| 548 | 703 | 7 | 1 | E | 0x080cdf6c | FUN_080cdf6c | find_next_occupied_slot_in_main_list | 1 | [eval](eval/080cdf6c.md) |
| 549 | 704 | 7 | 1 | E | 0x080cdff4 | FUN_080cdff4 | find_next_occupied_slot_in_secondary_list | 1 | [eval](eval/080cdff4.md) |
| 550 | 705 | 6 | 1 | E | 0x080ce428 | FUN_080ce428 | render_card_list_oam_row_by_slot_advance | 1 | [eval](eval/080ce428.md) |
| 551 | 706 | 6 | 1 | E | 0x080cf52c | FUN_080cf52c | render_card_list_oam_row_by_stat_display | 1 | [eval](eval/080cf52c.md) |
| 552 | 707 | 6 | 1 | E | 0x080d029c | FUN_080d029c | render_card_list_oam_row_by_lp_init | 1 | [eval](eval/080d029c.md) |
| 553 | 708 | 6 | 1 | E | 0x080d0640 | FUN_080d0640 | render_card_list_oam_row_by_slot_nibble | 1 | [eval](eval/080d0640.md) |
| 554 | 709 | 5 | 1 | E | 0x080cedd0 | FUN_080cedd0 | render_card_list_oam_row_by_jp_type | 1 | [eval](eval/080cedd0.md) |
| 555 | 710 | 6 | 1 | E | 0x080d05e4 | FUN_080d05e4 | render_card_list_oam_row_by_pack_slot | 1 | [eval](eval/080d05e4.md) |
| 556 | 711 | 6 | 1 | E | 0x080cdba8 | FUN_080cdba8 | render_card_list_oam_row_by_dual_slot | 1 | [eval](eval/080cdba8.md) |
| 557 | 712 | 6 | 1 | E | 0x080ced0c | FUN_080ced0c | render_card_list_oam_row_by_cursor_slot | 1 | [eval](eval/080ced0c.md) |
| 558 | 713 | 6 | 1 | E | 0x080cf490 | FUN_080cf490 | render_card_list_oam_row_by_anim_frame | 1 | [eval](eval/080cf490.md) |
| 559 | 714 | 6 | 1 | E | 0x080cfad0 | FUN_080cfad0 | render_card_list_oam_row_by_rarity_flag | 1 | [eval](eval/080cfad0.md) |
| 560 | 715 | 6 | 1 | E | 0x080d0150 | FUN_080d0150 | render_card_list_oam_row_by_pack_column | 1 | [eval](eval/080d0150.md) |
| 561 | 716 | 6 | 1 | E | 0x080ce2f4 | FUN_080ce2f4 | render_card_list_oam_row_by_type_icon | 1 | [eval](eval/080ce2f4.md) |
| 562 | 717 | 6 | 1 | E | 0x080cd454 | FUN_080cd454 | render_card_list_oam_row_by_single_slot | 1 | [eval](eval/080cd454.md) |
| 563 | 718 | 6 | 1 | E | 0x080cd0dc | FUN_080cd0dc | render_card_list_oam_row_by_cost_bar | 1 | [eval](eval/080cd0dc.md) |
| 564 | 719 | 5 | 1 | E | 0x080c7638 | FUN_080c7638 | dispatch_card_list_oam_row_by_card_type | 1 | [eval](eval/080c7638.md) |
| 565 | 720 | 6 | 1 | E | 0x080cf754 | FUN_080cf754 | find_next_occupied_slot_backward | 1 | [eval](eval/080cf754.md) |
| 566 | 721 | 6 | 1 | E | 0x080cf6d8 | FUN_080cf6d8 | find_next_occupied_slot_forward | 1 | [eval](eval/080cf6d8.md) |
| 567 | 722 | 5 | 1 | E | 0x080cfbdc | FUN_080cfbdc | render_card_list_oam_row_by_stat_state | 1 | [eval](eval/080cfbdc.md) |
| 568 | 723 | 6 | 1 | E | 0x080c82e4 | FUN_080c82e4 | tick_card_list_display_master | 1 | [eval](eval/080c82e4.md) |
| 569 | 724 | 6 | 1 | E | 0x080c7ba8 | FUN_080c7ba8 | render_card_list_face_row_by_mode | 1 | [eval](eval/080c7ba8.md) |
| 570 | 725 | 6 | 1 | E | 0x080c7af8 | FUN_080c7af8 | copy_card_frame_tiles_by_type | 1 | [eval](eval/080c7af8.md) |
| 571 | 726 | 6 | 1 | E | 0x080c841c | FUN_080c841c | render_card_list_face_row_by_mode_alt | 1 | [eval](eval/080c841c.md) |
| 572 | 727 | 5 | 1 | E | 0x080c8688 | FUN_080c8688 | tick_card_list_scene_frame | 1 | [eval](eval/080c8688.md) |
| 573 | 728 | 5 | 5 | D | 0x08094540 | FUN_08094540 | set_tile_palette_index_in_buf | 1 | [eval](eval/08094540.md) |
| 574 | 729 | 5 | 2 | E | 0x08094290 | FUN_08094290 | get_clamped_tile_row_count | 1 | [eval](eval/08094290.md) |
| 575 | 730 | 5 | 3 | E | 0x080d25e0 | FUN_080d25e0 | check_field_scroll_phase_ready | 1 | [eval](eval/080d25e0.md) |
| 576 | 731 | 6 | 14 | D | 0x080d0784 | FUN_080d0784 | check_zone_slot_attr_visible | 1 | [eval](eval/080d0784.md) |
| 577 | 732 | 6 | 4 | E | 0x080d3830 | FUN_080d3830 | render_zone_slot_card_icon_tile | 1 | [eval](eval/080d3830.md) |
| 578 | 733 | 6 | 2 | E | 0x080d08a4 | FUN_080d08a4 | render_zone_card_detail_panel | 1 | [eval](eval/080d08a4.md) |
| 579 | 734 | 6 | 1 | E | 0x080cad78 | FUN_080cad78 | render_zone_card_jp_text_panel | 1 | [eval](eval/080cad78.md) |
| 580 | 735 | 5 | 5 | D | 0x080d0818 | FUN_080d0818 | dispatch_zone_card_display_by_mode | 1 | [eval](eval/080d0818.md) |
| 581 | 736 | 4 | 1 | E | 0x080d2c60 | FUN_080d2c60 | tick_zone_card_detail_view | 1 | [eval](eval/080d2c60.md) |
| 582 | 737 | 5 | 2 | E | 0x080d1bb4 | FUN_080d1bb4 | dispatch_zone_card_anim_by_type | 1 | [eval](eval/080d1bb4.md) |
| 583 | 738 | 6 | 1 | E | 0x080d2390 | FUN_080d2390 | tick_zone_card_anim_state | 1 | [eval](eval/080d2390.md) |
| 584 | 739 | 7 | 1 | E | 0x080d3820 | FUN_080d3820 | advance_zone_card_anim | 1 | [eval](eval/080d3820.md) |
| 585 | 740 | 7 | 1 | E | 0x080d3826 | FUN_080d3826 | signal_zone_tick_done | 1 | [eval](eval/080d3826.md) |
| 586 | 741 | 5 | 1 | E | 0x080d2a08 | FUN_080d2a08 | dispatch_zone_card_anim_by_type_alt | 1 | [eval](eval/080d2a08.md) |
| 587 | 742 | 7 | 1 | E | 0x080d3828 | FUN_080d3828 | exit_zone_tick_frame | 1 | [eval](eval/080d3828.md) |
| 588 | 743 | 7 | 1 | E | 0x080d1088 | FUN_080d1088 | render_zone_card_anim_oam_frame | 1 | [eval](eval/080d1088.md) |
| 589 | 744 | 7 | 1 | E | 0x080d0c7c | FUN_080d0c7c | render_zone_card_anim_oam_frame_alt | 1 | [eval](eval/080d0c7c.md) |
| 590 | 745 | 8 | 1 | E | 0x080d07cc | FUN_080d07cc | check_zone_anim_id_in_table | 1 | [eval](eval/080d07cc.md) |
| 591 | 746 | 8 | 7 | D | 0x0804ae18 | FUN_0804ae18 | check_card_stat_field8_is_7 | 1 | [eval](eval/0804ae18.md) |
| 592 | 747 | 10 | 5 | D | 0x0804bb6c | FUN_0804bb6c | check_card_is_equip_target_eligible | 1 | [eval](eval/0804bb6c.md) |
| 593 | 748 | 10 | 10 | D | 0x0803bba4 | FUN_0803bba4 | eval_equip_placement_full_check | 1 | [eval](eval/0803bba4.md) |
| 594 | 749 | 9 | 3 | E | 0x08037568 | FUN_08037568 | check_zone_slot_equip_eligible_alt | 1 | [eval](eval/08037568.md) |
| 595 | 750 | 7 | 7 | D | 0x08031294 | FUN_08031294 | find_hand_slot_idx_by_set_code_alt | 1 | [eval](eval/08031294.md) |
| 596 | 751 | 10 | 1 | E | 0x08033a6c | FUN_08033a6c | count_slots_equippable_by_state_code | 1 | [eval](eval/08033a6c.md) |
| 597 | 752 | 9 | 21 | C | 0x08037434 | FUN_08037434 | check_zone_slot_equip_eligible | 1 | [eval](eval/08037434.md) |
| 598 | 753 | 7 | 43 | C | 0x0803123c | FUN_0803123c | find_hand_slot_idx_by_set_code | 1 | [eval](eval/0803123c.md) |
| 599 | 754 | 8 | 1 | E | 0x08094398 | FUN_08094398 | dispatch_effect_ctx_slot_by_zone_type | 1 | [eval](eval/08094398.md) |
| 600 | 755 | 7 | 1 | E | 0x080d136c | FUN_080d136c | render_zone_card_anim_oam_with_base | 1 | [eval](eval/080d136c.md) |
| 601 | 756 | 6 | 1 | E | 0x080d1b2c | FUN_080d1b2c | render_zone_card_anim_dual_pass | 1 | [eval](eval/080d1b2c.md) |
| 602 | 757 | 6 | 6 | D | 0x080942d0 | FUN_080942d0 | write_effect_ctx_slot_index | 1 | [eval](eval/080942d0.md) |
| 603 | 758 | 6 | 1 | E | 0x080d2690 | FUN_080d2690 | dispatch_zone_card_anim_by_subtype | 1 | [eval](eval/080d2690.md) |
| 604 | 759 | 6 | 1 | E | 0x080d2634 | FUN_080d2634 | update_zone_anim_queue_entry | 1 | [eval](eval/080d2634.md) |
| 605 | 760 | 9 | 2 | E | 0x080d3dc4 | FUN_080d3dc4 | compare_zone_slot_card_stat_pair_win | 1 | [eval](eval/080d3dc4.md) |
| 606 | 761 | 9 | 2 | E | 0x080d3d28 | FUN_080d3d28 | compare_zone_slot_card_stat_pair_alt | 1 | [eval](eval/080d3d28.md) |
| 607 | 762 | 9 | 2 | E | 0x080d3c8c | FUN_080d3c8c | compare_zone_slot_card_stat_pair | 1 | [eval](eval/080d3c8c.md) |
| 608 | 763 | 9 | 2 | E | 0x080d3b6c | FUN_080d3b6c | compare_zone_slot_visibility_pair | 1 | [eval](eval/080d3b6c.md) |
| 609 | 764 | 9 | 2 | E | 0x080d3bf0 | FUN_080d3bf0 | compare_zone_slot_stat_with_type_alt | 1 | [eval](eval/080d3bf0.md) |
| 610 | 765 | 9 | 2 | E | 0x080d3e50 | FUN_080d3e50 | compare_zone_slot_card_stat_with_atk | 1 | [eval](eval/080d3e50.md) |
| 611 | 766 | 9 | 2 | E | 0x080d3f4c | FUN_080d3f4c | compare_zone_slot_card_stat_with_level | 1 | [eval](eval/080d3f4c.md) |
| 612 | 767 | 8 | 2 | E | 0x080d403c | FUN_080d403c | sort_zone_slots_by_stat_insertion | 1 | [eval](eval/080d403c.md) |
| 613 | 768 | 7 | 1 | E | 0x080d4148 | FUN_080d4148 | sort_zone_slots_by_stat_quicksort | 1 | [eval](eval/080d4148.md) |
| 614 | 769 | 6 | 1 | E | 0x080d4268 | FUN_080d4268 | setup_zone_slot_sorted_view | 1 | [eval](eval/080d4268.md) |
| 615 | 770 | 5 | 1 | E | 0x080d4478 | FUN_080d4478 | tick_zone_card_list_state_machine | 1 | [eval](eval/080d4478.md) |
| 616 | 771 | 4 | 1 | E | 0x080d2ef4 | FUN_080d2ef4 | tick_zone_card_list_view | 1 | [eval](eval/080d2ef4.md) |
| 617 | 772 | 3 | 1 | E | 0x080cc340 | FUN_080cc340 | invert_zone_tick_result | 1 | [eval](eval/080cc340.md) |
| 618 | 773 | 4 | 1 | E | 0x080cc208 | FUN_080cc208 | tick_zone_detail_render_step | 1 | [eval](eval/080cc208.md) |
| 619 | 774 | 4 | 1 | E | 0x080cc228 | FUN_080cc228 | tick_zone_detail_panel_by_anim_state | 1 | [eval](eval/080cc228.md) |
| 620 | 775 | 4 | 1 | E | 0x080cc354 | FUN_080cc354 | tick_zone_field_info_panel | 1 | [eval](eval/080cc354.md) |
| 621 | 776 | 3 | 1 | E | 0x080cc528 | FUN_080cc528 | tick_zone_display_frame | 1 | [eval](eval/080cc528.md) |
| 622 | 777 | 5 | 2 | E | 0x08093598 | FUN_08093598 | play_card_ok_ui_effect | 1 | [eval](eval/08093598.md) |
| 623 | 778 | — | 2 | E | 0x0801f3d4 | FUN_0801f3d4 | return_void_noop_stub | 1 | [eval](eval/0801f3d4.md) |
| 624 | 779 | — | 135 | C | 0x0803bd2c | FUN_0803bd2c | enqueue_sprite_attr_record | 1 | [eval](eval/0803bd2c.md) |
| 625 | 780 | — | 5 | D | 0x080ed858 | FUN_080ed858 | write_sprite_row_to_vram_buffer | 1 | [eval](eval/080ed858.md) |
| 626 | 781 | — | 2 | E | 0x080953c4 | FUN_080953c4 | dispatch_sprite_row_write_by_type | 1 | [eval](eval/080953c4.md) |
| 627 | 782 | — | 14 | D | 0x08095498 | FUN_08095498 | submit_sprite_row_data | 1 | [eval](eval/08095498.md) |
| 628 | 783 | — | — | E | 0x08095380 | FUN_08095380 | pack_sprite_row_attr_words | 1 | [eval](eval/08095380.md) |
| 629 | 784 | — | — | E | 0x080c2880 | FUN_080c2880 | init_field_slot_aob_ctx_b | 1 | [eval](eval/080c2880.md) |
| 630 | 785 | — | — | E | 0x080c3d00 | FUN_080c3d00 | init_field_slot_ctx_zoom | 1 | [eval](eval/080c3d00.md) |
| 631 | 786 | — | — | E | 0x080c8904 | FUN_080c8904 | refresh_all_zone_slot_tile_display | 1 | [eval](eval/080c8904.md) |
| 632 | 787 | — | — | E | 0x080bc794 | FUN_080bc794 | init_field_slot_aob_ctx_a | 1 | [eval](eval/080bc794.md) |
| 633 | 788 | — | — | E | 0x080c291c | FUN_080c291c | write_zone_oam_entry_with_flip | 1 | [eval](eval/080c291c.md) |
| 634 | 789 | — | — | E | 0x080c4ea0 | FUN_080c4ea0 | init_field_slot_aob_ctx_c | 1 | [eval](eval/080c4ea0.md) |
| 635 | 790 | — | — | E | 0x080c412c | FUN_080c412c | render_field_slot_card_tile_by_id | 1 | [eval](eval/080c412c.md) |
| 636 | 791 | — | — | E | 0x080c2840 | FUN_080c2840 | write_field_slot_activation_mask | 1 | [eval](eval/080c2840.md) |
| 637 | 792 | — | — | E | 0x080c8f48 | FUN_080c8f48 | init_card_effect_aob_ctx | 1 | [eval](eval/080c8f48.md) |
| 638 | 793 | — | — | E | 0x080c786c | FUN_080c786c | zero_card_name_vram_buf | 1 | [eval](eval/080c786c.md) |
| 639 | 794 | — | — | E | 0x080c7950 | FUN_080c7950 | copy_game_text_to_card_name_vram | 1 | [eval](eval/080c7950.md) |
| 640 | 795 | — | — | E | 0x08094314 | FUN_08094314 | get_duel_activation_zone_id | 1 | [eval](eval/08094314.md) |
| 641 | 796 | — | — | E | 0x080cbf58 | FUN_080cbf58 | build_field_zone_display_state | 1 | [eval](eval/080cbf58.md) |
| 642 | 797 | — | — | E | 0x080c40e0 | FUN_080c40e0 | init_field_slot_aob_ctx_d | 1 | [eval](eval/080c40e0.md) |
| 643 | 798 | — | — | E | 0x080c89e8 | FUN_080c89e8 | update_zone_activation_display_state | 1 | [eval](eval/080c89e8.md) |
| 644 | 799 | — | — | E | 0x08094678 | FUN_08094678 | get_player_lp_by_field_type | 1 | [eval](eval/08094678.md) |
| 645 | 800 | — | 114 | C | 0x0801ec9c | FUN_0801ec9c | dispatch_card_display_op | 1 | [eval](eval/0801ec9c.md) |
| 646 | 801 | — | — | E | 0x0809355c | FUN_0809355c | invoke_card_display_op_0x31 | 1 | [eval](eval/0809355c.md) |
| 647 | 802 | — | — | E | 0x08094a28 | FUN_08094a28 | process_card_play_ok_sequence | 1 | [eval](eval/08094a28.md) |
| 648 | 803 | — | — | E | 0x080abb90 | FUN_080abb90 | reset_sprite_attr_record_flags | 1 | [eval](eval/080abb90.md) |
| 649 | 804 | — | 32 | D | 0x08085320 | FUN_08085320 | submit_lp_bar_sprite_row_by_type | 1 | [eval](eval/08085320.md) |
| 650 | 805 | — | — | E | 0x080909e0 | FUN_080909e0 | check_card_effect_node_active | 1 | [eval](eval/080909e0.md) |
| 651 | 806 | — | — | E | 0x0805b2a4 | FUN_0805b2a4 | dispatch_card_effect_by_stat_type | 1 | [eval](eval/0805b2a4.md) |
| 652 | 807 | — | — | E | 0x0801f3b0 | FUN_0801f3b0 | read_prng_entry_flag_clear | 1 | [eval](eval/0801f3b0.md) |
| 653 | 808 | — | — | E | 0x080a1968 | FUN_080a1968 | commit_lp_display_row_to_sprite | 1 | [eval](eval/080a1968.md) |
| 654 | 809 | — | — | E | 0x080a1a38 | FUN_080a1a38 | setup_lp_display_row_with_data | 1 | [eval](eval/080a1a38.md) |
| 655 | 810 | — | — | E | 0x08095b3c | FUN_08095b3c | get_lp_display_state_word | 1 | [eval](eval/08095b3c.md) |
| 656 | 811 | — | — | E | 0x0803bde4 | FUN_0803bde4 | write_sprite_attr_record_entry | 1 | [eval](eval/0803bde4.md) |
| 657 | 812 | — | 64 | C | 0x0804a76c | FUN_0804a76c | increment_lp_bar_display_counter | 1 | [eval](eval/0804a76c.md) |
| 658 | 813 | — | — | E | 0x080310d0 | FUN_080310d0 | find_slot_idx_in_dual_list_by_id | 1 | [eval](eval/080310d0.md) |
| 659 | 814 | — | 11 | D | 0x0803b8b0 | FUN_0803b8b0 | write_field_slot_bit_by_player | 1 | [eval](eval/0803b8b0.md) |
| 660 | 815 | — | 29 | D | 0x0804a970 | FUN_0804a970 | set_field_slot_bit_with_sprite_update | 1 | [eval](eval/0804a970.md) |
| 661 | 816 | — | — | E | 0x0804c76c | FUN_0804c76c | submit_slot_card_sprite_row_entry | 1 | [eval](eval/0804c76c.md) |
| 662 | 817 | — | 67 | C | 0x0804a870 | FUN_0804a870 | decrement_lp_bar_display_counter | 1 | [eval](eval/0804a870.md) |
| 663 | 818 | — | 10 | D | 0x08094eb4 | FUN_08094eb4 | write_card_display_index_entry | 1 | [eval](eval/08094eb4.md) |
| 664 | 819 | — | 27 | D | 0x08094f3c | FUN_08094f3c | write_card_display_index_with_bit_offset | 1 | [eval](eval/08094f3c.md) |
| 665 | 820 | — | — | E | 0x08094f70 | FUN_08094f70 | update_card_display_index_by_type_rules | 1 | [eval](eval/08094f70.md) |
| 666 | 821 | — | — | E | 0x0804a7f8 | FUN_0804a7f8 | increment_lp_bar_counter_no_player | 1 | [eval](eval/0804a7f8.md) |
| 667 | 822 | — | — | E | 0x080ed674 | FUN_080ed674 | check_prng_anim_frame_slot_occupied | 1 | [eval](eval/080ed674.md) |
| 668 | 823 | 5 | 3 | E | 0x080ed6fc | FUN_080ed6fc | dequeue_prng_anim_entry | 2 | [eval](eval/080ed6fc.md) |
| 669 | 824 | 4 | 1 | E | 0x080954e8 | FUN_080954e8 | step_prng_anim_frame | 1 | [eval](eval/080954e8.md) |
| 670 | 825 | 6 | 1 | E | 0x0804f0e4 | FUN_0804f0e4 | flush_sprite_row_queue_partial | 2 | [eval](eval/0804f0e4.md) |
| 671 | 826 | 7 | 1 | E | 0x0804daf6 | FUN_0804daf6 | reset_sprite_row_queue_tail | 1 | [eval](eval/0804daf6.md) |
| 672 | 827 | 6 | 2 | E | 0x0804d1e4 | FUN_0804d1e4 | dispatch_sprite_row_anim_by_state | 2 | [eval](eval/0804d1e4.md) |
| 673 | 828 | 8 | 3 | E | 0x0804c958 | FUN_0804c958 | init_card_sprite_row_entry | 2 | [eval](eval/0804c958.md) |
| 674 | 829 | 8 | 3 | E | 0x0804caf0 | FUN_0804caf0 | init_card_sprite_row_entry_alt | 2 | [eval](eval/0804caf0.md) |
| 675 | 830 | 6 | 74 | C | 0x08043054 | FUN_08043054 | enqueue_sprite_attr_with_mode | 1 | [eval](eval/08043054.md) |
| 676 | 831 | 7 | 81 | C | 0x0804a484 | FUN_0804a484 | enqueue_sprite_attr_type11 | 1 | [eval](eval/0804a484.md) |
| 677 | 832 | 8 | 10 | D | 0x080486b0 | FUN_080486b0 | enqueue_sprite_attr_by_sign | 1 | [eval](eval/080486b0.md) |
| 678 | 833 | 7 | 13 | D | 0x08048750 | FUN_08048750 | enqueue_sprite_attr_clamped | 1 | [eval](eval/08048750.md) |
| 679 | 834 | 8 | 5 | D | 0x0808e5c4 | FUN_0808e5c4 | render_field_card_copy_count | 1 | [eval](eval/0808e5c4.md) |
| 680 | 835 | 7 | 25 | C | 0x0804adc8 | FUN_0804adc8 | check_card_type_is_spell | 2 | [eval](eval/0804adc8.md) |
| 681 | 836 | 9 | 8 | D | 0x08045268 | FUN_08045268 | enqueue_sprite_attr_with_shape | 2 | [eval](eval/08045268.md) |
| 682 | 837 | 9 | 9 | D | 0x0808e85c | FUN_0808e85c | scan_field_slots_for_equip_sprite | 2 | [eval](eval/0808e85c.md) |
| 683 | 838 | 10 | 7 | D | 0x0802f930 | FUN_0802f930 | find_equip_target_for_card_slot | 1 | [eval](eval/0802f930.md) |
| 684 | 839 | 9 | 5 | D | 0x08033b18 | FUN_08033b18 | count_equip_slots_matching_whitelist | 2 | [eval](eval/08033b18.md) |
| 685 | 840 | 8 | 12 | D | 0x08033b08 | FUN_08033b08 | count_equip_slots_active_only | 1 | [eval](eval/08033b08.md) |
| 686 | 841 | 9 | 3 | E | 0x08030500 | FUN_08030500 | map_card_id_to_anim_type | 1 | [eval](eval/08030500.md) |
| 687 | 842 | 8 | 37 | C | 0x08036870 | FUN_08036870 | check_card_equip_eligible_for_slot | 1 | [eval](eval/08036870.md) |
| 688 | 843 | 7 | 4 | E | 0x080369a4 | FUN_080369a4 | check_equip_eligibility_via_request_buf | 1 | [eval](eval/080369a4.md) |
| 689 | 844 | 10 | 2 | E | 0x080300d4 | FUN_080300d4 | check_zone_card_special_state_by_field5 | 1 | [eval](eval/080300d4.md) |
| 690 | 845 | 7 | 44 | C | 0x0804adf0 | FUN_0804adf0 | check_card_field8_is_9 | 1 | [eval](eval/0804adf0.md) |
| 691 | 846 | 10 | 4 | E | 0x0808f3b0 | FUN_0808f3b0 | scan_field_slots_for_attached_sprite_by_id | 1 | [eval](eval/0808f3b0.md) |
| 692 | 847 | 11 | 1 | E | 0x0802f6e4 | FUN_0802f6e4 | find_node_packed_by_card_id_in_dual_lists | 1 | [eval](eval/0802f6e4.md) |
| 693 | 848 | 7 | 7 | D | 0x0805b1f0 | FUN_0805b1f0 | apply_equip_activation_via_packed_attr | 1 | [eval](eval/0805b1f0.md) |
| 694 | 849 | 6 | 61 | C | 0x0804c910 | FUN_0804c910 | apply_equip_activation_with_id_lookup | 1 | [eval](eval/0804c910.md) |
| 695 | 850 | 9 | 1 | E | 0x0808f938 | FUN_0808f938 | refresh_opponent_field_slots_for_card_attached | 1 | [eval](eval/0808f938.md) |
| 696 | 851 | 8 | 16 | D | 0x080487dc | FUN_080487dc | submit_lp_change_indicator_with_chain_check | 1 | [eval](eval/080487dc.md) |
| 697 | 852 | 11 | 2 | E | 0x0802ff10 | FUN_0802ff10 | check_zone_card_id_in_node_pool | 1 | [eval](eval/0802ff10.md) |
| 698 | 853 | 6 | 40 | C | 0x08048674 | FUN_08048674 | enqueue_sprite_attr_for_zone_card_id_lookup | 1 | [eval](eval/08048674.md) |
| 699 | 854 | 11 | 1 | E | 0x0803009c | FUN_0803009c | find_zone_node_by_card_id_match | 1 | [eval](eval/0803009c.md) |
| 700 | 855 | 10 | 4 | E | 0x0804559c | FUN_0804559c | dispatch_card_effect_sprite_render_by_card_id | 1 | [eval](eval/0804559c.md) |
| 701 | 856 | 10 | 6 | D | 0x08046bd0 | FUN_08046bd0 | dispatch_card_effect_zone_action_by_card_id | 1 | [eval](eval/08046bd0.md) |
| 702 | 856 | 9 | 2 | E | 0x08047218 | FUN_08047218 | handle_card_effect_zone_eligibility_by_field6 | 1 | [eval](eval/08047218.md) |
| 703 | 857 | 8 | 5 | D | 0x08036ac0 | FUN_08036ac0 | check_slot_card_eligible_for_special_action | 1 | [eval](eval/08036ac0.md) |
| 704 | 858 | 8 | 7 | D | 0x0802f550 | FUN_0802f550 | find_zone_chain_node_by_card_id_pair | 1 | [eval](eval/0802f550.md) |
| 705 | 859 | 8 | 2 | E | 0x0802fd00 | FUN_0802fd00 | find_chain_node_by_dual_halfword | 1 | [eval](eval/0802fd00.md) |
| 706 | 860 | 7 | 9 | D | 0x08043240 | FUN_08043240 | enqueue_sprite_attr_for_chain_node_match | 1 | [eval](eval/08043240.md) |
| 707 | 861 | 6 | 25 | C | 0x08045240 | FUN_08045240 | enqueue_sprite_attr_with_xy_split | 1 | [eval](eval/08045240.md) |
| 708 | 862 | 8 | 35 | C | 0x080431ac | FUN_080431ac | enqueue_equip_slot_sprite_attr | 1 | [eval](eval/080431ac.md) |
| 709 | 863 | 9 | 2 | E | 0x0808ea28 | FUN_0808ea28 | enqueue_paired_slot_sprite_attrs_for_player | 2 | [eval](eval/0808ea28.md) |
| 710 | 864 | 9 | 5 | D | 0x0804543c | FUN_0804543c | enqueue_equip_card_sprite_attr_for_slot | 2 | [eval](eval/0804543c.md) |
| 711 | 865 | 8 | 13 | D | 0x08045314 | FUN_08045314 | enqueue_effect_card_slot_sprite_attr | 2 | [eval](eval/08045314.md) |
| 712 | 866 | 8 | 7 | D | 0x08043128 | FUN_08043128 | enqueue_equip_chain_slot_sprite_attr | 1 | [eval](eval/08043128.md) |
| 713 | 867 | 9 | 1 | E | 0x0804317c | FUN_0804317c | enqueue_equip_chain_all_slots_for_pair | 1 | [eval](eval/0804317c.md) |
| 714 | 868 | 10 | 1 | E | 0x08032a8c | FUN_08032a8c | find_best_slot_for_card_by_player | 2 | [eval](eval/08032a8c.md) |
| 715 | 869 | 9 | 1 | E | 0x08032b98 | FUN_08032b98 | find_best_slot_atk_across_players | 1 | [eval](eval/08032b98.md) |
| 716 | 870 | 8 | 2 | E | 0x0805b5f0 | FUN_0805b5f0 | populate_effect_node_snapshot | 1 | [eval](eval/0805b5f0.md) |
| 717 | 871 | 10 | 74 | C | 0x0803670c | FUN_0803670c | query_slot_card_type_eligibility | 1 | [eval](eval/0803670c.md) |
| 718 | 872 | 10 | 1 | E | 0x0804640c | FUN_0804640c | check_slot_equip_placement_valid | 1 | [eval](eval/0804640c.md) |
| 719 | 873 | 9 | 1 | E | 0x08046538 | FUN_08046538 | build_equip_placement_valid_bitmap | 1 | [eval](eval/08046538.md) |
| 720 | 874 | 9 | 1 | E | 0x0804659c | FUN_0804659c | check_slot_equip_target_eligibility | 2 | [eval](eval/0804659c.md) |
| 721 | 875 | 9 | 1 | E | 0x08043644 | FUN_08043644 | enqueue_sprite_attrs_for_card_chain_list | 2 | [eval](eval/08043644.md) |
| 722 | 875 | 8 | 2 | E | 0x08044e30 | FUN_08044e30 | update_duel_field_slot_sprite_state | 1 | [eval](eval/08044e30.md) |
| 723 | 875 | 8 | 25 | C | 0x08047724 | FUN_08047724 | update_equip_target_bitmap_for_field | 2 | [eval](eval/08047724.md) |
| 724 | 875 | 7 | 5 | D | 0x0804790c | FUN_0804790c | prepare_slot_ctx_for_equip_bitmap | 1 | [eval](eval/0804790c.md) |
| 725 | 875 | 6 | 43 | C | 0x0804794c | FUN_0804794c | enqueue_equip_slot_bitmap_update | 1 | [eval](eval/0804794c.md) |
| 726 | 875 | 7 | 3 | E | 0x0805b990 | FUN_0805b990 | scan_equip_zone_candidates_with_snapshot | 2 | [eval](eval/0805b990.md) |
| 727 | 876 | 8 | 2 | E | 0x0804a334 | FUN_0804a334 | render_monster_slot_card_with_lp_bar | 2 | [eval](eval/0804a334.md) |
| 728 | 877 | 7 | 3 | E | 0x08095d84 | FUN_08095d84 | dispatch_lp_bar_animation_step | 1 | [eval](eval/08095d84.md) |
| 729 | 878 | 7 | 2 | E | 0x08095ca0 | FUN_08095ca0 | trigger_lp_bar_animation_if_ready | 2 | [eval](eval/08095ca0.md) |
| 730 | 879 | 7 | 119 | C | 0x08093390 | FUN_08093390 | trigger_card_display_op31_if_not_active | 1 | [eval](eval/08093390.md) |
| 731 | 880 | 8 | 26 | C | 0x080942dc | FUN_080942dc | get_monster_slot_entry_ptr | 1 | [eval](eval/080942dc.md) |
| 732 | 881 | 5 | 3 | E | 0x0809463c | FUN_0809463c | advance_prng_state | 1 | [eval](eval/0809463c.md) |
| 733 | 882 | 4 | 34 | C | 0x08094664 | FUN_08094664 | sample_prng_scaled | 1 | [eval](eval/08094664.md) |
| 734 | 883 | 12 | 2 | E | 0x08094564 | FUN_08094564 | read_slot_palette_index | 1 | [eval](eval/08094564.md) |
| 735 | 884 | 11 | 4 | E | 0x080ade34 | FUN_080ade34 | check_slot_palette_nonzero | 1 | [eval](eval/080ade34.md) |
| 736 | 885 | 11 | 1 | E | 0x080ade8c | FUN_080ade8c | find_random_empty_slot_excluding_card_id | 4 | [eval](eval/080ade8c.md) |
| 737 | 886 | 11 | 1 | E | 0x080adf8c | FUN_080adf8c | check_special_card_activation_eligible | 1 | [eval](eval/080adf8c.md) |
| 738 | 887 | 10 | 7 | D | 0x08032f7c | FUN_08032f7c | count_slot_card_pair_allowed_for_card | 1 | [eval](eval/08032f7c.md) |
| 739 | 888 | 10 | 4 | E | 0x080af914 | FUN_080af914 | check_any_pair_slot_available_for_card | 1 | [eval](eval/080af914.md) |
| 740 | 889 | 9 | 5 | D | 0x080eef9c | FUN_080eef9c | get_card_type_bits_by_internal_id | 1 | [eval](eval/080eef9c.md) |
| 741 | 890 | 11 | 1 | E | 0x08037b34 | FUN_08037b34 | count_monster_slots_with_field5_ge_threshold | 1 | [eval](eval/08037b34.md) |
| 742 | 891 | 9 | 7 | D | 0x080af534 | FUN_080af534 | check_card_id_in_eligible_set | 1 | [eval](eval/080af534.md) |
| 743 | 892 | 11 | 1 | E | 0x080adf40 | FUN_080adf40 | find_slot_by_card_type_and_player | 2 | [eval](eval/080adf40.md) |
| 744 | 893 | 11 | 1 | E | 0x080ade48 | FUN_080ade48 | find_first_empty_slot_for_card_type | 3 | [eval](eval/080ade48.md) |
| 745 | 894 | 11 | 7 | D | 0x08031a84 | FUN_08031a84 | count_zone_card_pair_allowed_for_card | 1 | [eval](eval/08031a84.md) |
| 746 | 895 | 10 | 3 | E | 0x080af8cc | FUN_080af8cc | check_compound_pair_activation_eligible | 1 | [eval](eval/080af8cc.md) |
| 747 | 896 | 10 | 6 | D | 0x080abf64 | FUN_080abf64 | eval_zone_slot_score_for_player | 1 | [eval](eval/080abf64.md) |
| 748 | 897 | — | — | E | 0x08033370 | FUN_08033370 | count_active_cards_in_zone_by_player | 1 | [eval](eval/08033370.md) |
| 749 | 898 | — | — | E | 0x080aec7a | FUN_080aec7a | exit_slot_search_with_result | 2 | [eval](eval/080aec7a.md) |
| 750 | 899 | — | — | D | 0x080ae050 | FUN_080ae050 | find_empty_slot_for_card_id_dispatch | 2 | [eval](eval/080ae050.md) |
| 751 | 900 | — | — | E | 0x080aece4 | FUN_080aece4 | fill_effect_slots_up_to_count | 1 | [eval](eval/080aece4.md) |
| 752 | 901 | — | — | E | 0x080aec8c | FUN_080aec8c | activate_effect_slot_for_card | 1 | [eval](eval/080aec8c.md) |
| 753 | 902 | — | — | E | 0x080aed4c | FUN_080aed4c | fill_effect_slots_up_to_count_with_equip_cap | 1 | [eval](eval/080aed4c.md) |
| 754 | 903 | — | — | D | 0x080941c4 | FUN_080941c4 | init_effect_slot_display_context | 2 | [eval](eval/080941c4.md) |
| 755 | 904 | — | — | E | 0x08097150 | FUN_08097150 | dispatch_to_effect_handler_by_card_type | 2 | [eval](eval/08097150.md) |
| 756 | 905 | — | — | E | 0x08095ec4 | FUN_08095ec4 | dispatch_effect_slot_by_display_state | 2 | [eval](eval/08095ec4.md) |
| 757 | 906 | — | — | E | 0x080933c8 | FUN_080933c8 | invoke_card_display_op_0x31_with_params | 1 | [eval](eval/080933c8.md) |
| 758 | 907 | — | — | E | 0x0804394c | FUN_0804394c | enqueue_zone_card_sprite_attr_by_slot | 2 | [eval](eval/0804394c.md) |
| 759 | 908 | — | — | E | 0x08095ba8 | FUN_08095ba8 | init_equip_card_sprite_row_entry | 1 | [eval](eval/08095ba8.md) |
| 760 | 909 | — | — | E | 0x08096988 | FUN_08096988 | write_card_display_ctx_fields | 1 | [eval](eval/08096988.md) |
| 761 | 910 | — | — | E | 0x080af940 | FUN_080af940 | check_effect_zone_available_for_player | 1 | [eval](eval/080af940.md) |
| 762 | 911 | — | — | D | 0x0805bc48 | FUN_0805bc48 | check_card_normal_summon_eligible_full | 2 | [eval](eval/0805bc48.md) |
| 763 | 912 | — | — | D | 0x08037a8c | FUN_08037a8c | find_zone_slot_idx_allowed_for_card | 1 | [eval](eval/08037a8c.md) |
| 764 | 913 | — | — | E | 0x0804c38c | FUN_0804c38c | classify_card_id_summon_category | 1 | [eval](eval/0804c38c.md) |
| 765 | 914 | — | — | E | 0x0803088c | FUN_0803088c | check_effect_slot_summon_path_eligible | 2 | [eval](eval/0803088c.md) |
| 766 | 915 | — | — | E | 0x0805bcf0 | FUN_0805bcf0 | check_card_special_summon_eligible_full | 2 | [eval](eval/0805bcf0.md) |
| 767 | 916 | — | — | E | 0x080bae6c | FUN_080bae6c | check_card_summon_eligible_by_field6 | 1 | [eval](eval/080bae6c.md) |
| 768 | 917 | 8 | 3 | E | 0x080b499c | FUN_080b499c | check_normal_summon_eligible_for_slot | 1 | [eval](eval/080b499c.md) |
| 769 | 918 | 8 | 1 | E | 0x080bb3dc | FUN_080bb3dc | check_normal_summon_eligible_for_any_effect_zone | 1 | [eval](eval/080bb3dc.md) |
| 770 | 919 | 7 | 1 | E | 0x080b4ba8 | FUN_080b4ba8 | check_normal_summon_eligible_any_slot | 1 | [eval](eval/080b4ba8.md) |
| 771 | 920 | 7 | 1 | E | 0x08085430 | FUN_08085430 | build_sprite_row_from_zone_state | 1 | [eval](eval/08085430.md) |
| 772 | 921 | 7 | 3 | E | 0x0801f238 | FUN_0801f238 | copy_game_text_if_raw | 2 | [eval](eval/0801f238.md) |
| 773 | 923 | 7 | 6 | D | 0x0801f25c | FUN_0801f25c | append_game_text_if_raw | 2 | [eval](eval/0801f25c.md) |
| 774 | 924 | 7 | 1 | E | 0x08085a50 | FUN_08085a50 | build_field_action_text_by_zone_type | 1 | [eval](eval/08085a50.md) |
| 775 | 925 | 7 | 1 | E | 0x08094800 | FUN_08094800 | check_all_equip_target_slots_available | 1 | [eval](eval/08094800.md) |
| 776 | 926 | 7 | 1 | E | 0x080947a0 | FUN_080947a0 | check_all_fusion_pair_slots_available | 1 | [eval](eval/080947a0.md) |
| 777 | 927 | 6 | 1 | E | 0x08094864 | FUN_08094864 | query_summon_eligibility_code | 1 | [eval](eval/08094864.md) |
| 778 | 928 | 5 | 2 | E | 0x0809495c | FUN_0809495c | check_normal_summon_eligibility | 1 | [eval](eval/0809495c.md) |
| 779 | 929 | 8 | 1 | E | 0x080854b8 | FUN_080854b8 | scan_equip_target_slots_for_card | 1 | [eval](eval/080854b8.md) |
| 780 | 930 | 7 | 1 | E | 0x08085838 | FUN_08085838 | scan_all_zones_for_equip_target | 1 | [eval](eval/08085838.md) |
| 781 | 931 | 6 | 1 | E | 0x08085d4c | FUN_08085d4c | dispatch_field_display_state_by_type | 1 | [eval](eval/08085d4c.md) |
| 782 | 932 | 7 | 1 | E | 0x0804f0c2 | FUN_0804f0c2 | clear_sprite_row_queue_overflow_flag | 1 | [eval](eval/0804f0c2.md) |
| 783 | 933 | 6 | 2 | E | 0x0804db50 | FUN_0804db50 | dispatch_sprite_row_queue_by_state | 2 | [eval](eval/0804db50.md) |
| 784 | 934 | 7 | 2 | E | 0x0808e600 | FUN_0808e600 | enqueue_equip_chain_sprites_for_zones | 1 | [eval](eval/0808e600.md) |
| 785 | 935 | 7 | 1 | E | 0x0808fe84 | FUN_0808fe84 | apply_equip_activation_from_zone_scan | 1 | [eval](eval/0808fe84.md) |
| 786 | 936 | 7 | 7 | D | 0x08094f20 | FUN_08094f20 | write_card_display_index_if_above_bit | 1 | [eval](eval/08094f20.md) |
| 787 | 937 | 7 | 1 | E | 0x08095084 | FUN_08095084 | write_monster_zone_display_indices | 1 | [eval](eval/08095084.md) |
| 788 | 938 | 7 | 1 | E | 0x0808ec08 | FUN_0808ec08 | scan_field_slots_for_graveyard_equip_activation | 2 | [eval](eval/0808ec08.md) |
| 789 | 939 | 7 | 17 | D | 0x080486e4 | FUN_080486e4 | enqueue_equip_zone_sprite_by_side | 1 | [eval](eval/080486e4.md) |
| 790 | 940 | 9 | 3 | E | 0x08049e44 | FUN_08049e44 | enqueue_equip_slot_sprite_with_card_check | 2 | [eval](eval/08049e44.md) |
| 791 | 941 | 8 | 6 | D | 0x0804a2c8 | FUN_0804a2c8 | submit_equip_slot_sprite_zone11 | 2 | [eval](eval/0804a2c8.md) |
| 792 | 942 | 7 | 1 | E | 0x0808f608 | FUN_0808f608 | scan_chain_nodes_for_equip_zone_sprite | 1 | [eval](eval/0808f608.md) |
| 793 | 943 | 8 | 1 | E | 0x08043274 | FUN_08043274 | enqueue_equip_chain_sprite_by_side | 1 | [eval](eval/08043274.md) |
| 794 | 944 | 7 | 1 | E | 0x0804348c | FUN_0804348c | scan_equip_chain_list_for_sprite_update | 1 | [eval](eval/0804348c.md) |
| 795 | 945 | 9 | 6 | D | 0x080325dc | FUN_080325dc | check_card_equip_eligibility_in_field | 1 | [eval](eval/080325dc.md) |
| 796 | 946 | 8 | 2 | E | 0x08032960 | FUN_08032960 | count_equip_eligible_slots_for_player | 1 | [eval](eval/08032960.md) |
| 797 | 947 | 8 | 1 | E | 0x08032a6c | FUN_08032a6c | count_equip_eligible_slots_both_players | 1 | [eval](eval/08032a6c.md) |
| 798 | 948 | 8 | 2 | E | 0x080454c0 | FUN_080454c0 | enqueue_effect_zone_pair_sprite_scan | 1 | [eval](eval/080454c0.md) |
| 799 | 949 | 7 | 1 | E | 0x0808db90 | FUN_0808db90 | dispatch_equip_pair_sprites_by_state | 1 | [eval](eval/0808db90.md) |
| 800 | 950 | 9 | 1 | E | 0x0808ee80 | FUN_0808ee80 | enqueue_active_card_shape_sprites_in_zone | 1 | [eval](eval/0808ee80.md) |
| 801 | 951 | 8 | 13 | D | 0x08049014 | FUN_08049014 | submit_effect_zone_lp_and_shape_sprites | 1 | [eval](eval/08049014.md) |
| 802 | 952 | 7 | 1 | E | 0x0808ed98 | FUN_0808ed98 | scan_field_slots_for_card_pair_sprite_update | 1 | [eval](eval/0808ed98.md) |
| 803 | 953 | 7 | 1 | E | 0x0808f57c | FUN_0808f57c | scan_equip_chain_slots_for_bitmap_update | 1 | [eval](eval/0808f57c.md) |
| 804 | 954 | 7 | 1 | E | 0x0809011c | FUN_0809011c | scan_slots_for_equip_activation_by_field5 | 1 | [eval](eval/0809011c.md) |
| 805 | 955 | 9 | 2 | E | 0x08043d20 | FUN_08043d20 | enqueue_equip_chain_pair_sprite_validated | 1 | [eval](eval/08043d20.md) |
| 806 | 956 | 7 | 8 | D | 0x08045298 | FUN_08045298 | enqueue_equip_set_slot_sprite_by_zone_col | 1 | [eval](eval/08045298.md) |
| 807 | 957 | 9 | 2 | E | 0x08043d90 | FUN_08043d90 | scan_equip_chain_list_for_activation_sprite | 1 | [eval](eval/08043d90.md) |
| 808 | 958 | 8 | 5 | D | 0x08043ea4 | FUN_08043ea4 | enqueue_equip_chain_pair_sprite_if_eligible | 1 | [eval](eval/08043ea4.md) |
| 809 | 959 | 8 | 7 | D | 0x08036014 | FUN_08036014 | check_slot_equip_eligibility_by_type | 1 | [eval](eval/08036014.md) |
| 810 | 960 | 9 | 1 | E | 0x0804c140 | FUN_0804c140 | check_card_id_is_field_zone_special | 1 | [eval](eval/0804c140.md) |
| 811 | 961 | 10 | 1 | E | 0x08032f00 | FUN_08032f00 | count_eligible_zone_slots_for_player | 1 | [eval](eval/08032f00.md) |
| 812 | 962 | 9 | 6 | D | 0x08032f6c | FUN_08032f6c | count_eligible_zone_slots_all_flags | 1 | [eval](eval/08032f6c.md) |
| 813 | 963 | 8 | 2 | E | 0x080363bc | FUN_080363bc | check_slot_field_zone_card_eligible | 1 | [eval](eval/080363bc.md) |
| 814 | 964 | 7 | 1 | E | 0x08042b24 | FUN_08042b24 | resolve_equip_target_slot_for_enqueue | 1 | [eval](eval/08042b24.md) |
| 815 | 965 | 8 | 6 | D | 0x08047e20 | FUN_08047e20 | prepare_equip_slot_ctx_for_bitmap_update | 2 | [eval](eval/08047e20.md) |
| 816 | 966 | 9 | 29 | C | 0x080478fc | FUN_080478fc | query_equip_target_bitmap_default | 1 | [eval](eval/080478fc.md) |
| 817 | 967 | 8 | 19 | D | 0x08047970 | FUN_08047970 | test_equip_target_slot_in_bitmap | 1 | [eval](eval/08047970.md) |
| 818 | 968 | 8 | 4 | E | 0x08047f1c | FUN_08047f1c | update_equip_bitmap_with_cross_side_flag | 2 | [eval](eval/08047f1c.md) |
| 819 | 969 | 7 | 1 | E | 0x0808efa8 | FUN_0808efa8 | scan_field_for_whitelist_equip_sprite_and_lp | 2 | [eval](eval/0808efa8.md) |
| 820 | 970 | 7 | 1 | E | 0x0808f9f8 | FUN_0808f9f8 | scan_field_slots_for_equip_bitmap_update | 1 | [eval](eval/0808f9f8.md) |
| 821 | 971 | 7 | 1 | E | 0x0808eeb0 | FUN_0808eeb0 | scan_field_slots_for_chain_sprite_enqueue | 2 | [eval](eval/0808eeb0.md) |
| 822 | 972 | 7 | 1 | E | 0x0808f230 | FUN_0808f230 | scan_field_for_equip_priority_slot_update | 1 | [eval](eval/0808f230.md) |
| 823 | 973 | 7 | 2 | E | 0x08037bb4 | FUN_08037bb4 | check_field_effect_zone_activation_eligible | 1 | [eval](eval/08037bb4.md) |
| 824 | 974 | 7 | 1 | E | 0x0808ffb4 | FUN_0808ffb4 | scan_field_slots_for_equip_sprite_by_chain | 1 | [eval](eval/0808ffb4.md) |
| 825 | 975 | 8 | 2 | E | 0x0808eb68 | FUN_0808eb68 | find_first_eligible_zone_slot_for_player | 1 | [eval](eval/0808eb68.md) |
| 826 | 976 | 7 | 1 | E | 0x0808ebb8 | FUN_0808ebb8 | scan_field_slots_for_zone_equip_bitmap_update | 1 | [eval](eval/0808ebb8.md) |
| 827 | 977 | 9 | 4 | E | 0x080439e0 | FUN_080439e0 | apply_slot_equip_activation_with_sprite | 1 | [eval](eval/080439e0.md) |
| 828 | 978 | 9 | 5 | D | 0x080439a0 | FUN_080439a0 | invoke_equip_activation_with_zero_flag | 2 | [eval](eval/080439a0.md) |
| 829 | 979 | 8 | 1 | E | 0x0808df3c | FUN_0808df3c | scan_all_slots_for_max_equip_match | 2 | [eval](eval/0808df3c.md) |
| 830 | 980 | 8 | 2 | E | 0x0808daf0 | FUN_0808daf0 | find_matching_slot_by_player_zone_card | 2 | [eval](eval/0808daf0.md) |
| 831 | 981 | 9 | 10 | D | 0x080316b8 | FUN_080316b8 | find_card_pair_in_player_deck_list | 2 | [eval](eval/080316b8.md) |
| 832 | 982 | 8 | 1 | E | 0x0808fc78 | FUN_0808fc78 | scan_card_placement_for_activation | 1 | [eval](eval/0808fc78.md) |
| 833 | 983 | 7 | 1 | E | 0x0804a5a0 | FUN_0804a5a0 | enqueue_sprite_attr_for_card_slot | 2 | [eval](eval/0804a5a0.md) |
| 834 | 984 | 7 | 1 | E | 0x0808f7c0 | FUN_0808f7c0 | enqueue_sprite_by_field_copy_count | 1 | [eval](eval/0808f7c0.md) |
| 835 | 985 | 7 | 1 | E | 0x0808fdc0 | FUN_0808fdc0 | scan_effect_zone_slots_for_equip_activation | 1 | [eval](eval/0808fdc0.md) |
| 836 | 986 | 7 | 1 | E | 0x0808ff44 | FUN_0808ff44 | scan_slots_for_field_bit4_sprite_update | 1 | [eval](eval/0808ff44.md) |
| 837 | 987 | 8 | 8 | D | 0x0804a4cc | FUN_0804a4cc | check_zone_eligible_with_deck_flag | 2 | [eval](eval/0804a4cc.md) |
| 838 | 988 | 7 | 1 | E | 0x0808f1cc | FUN_0808f1cc | scan_field_for_unpaired_equip_slot_update | 1 | [eval](eval/0808f1cc.md) |
| 839 | 989 | 7 | 1 | E | 0x0808fa4c | FUN_0808fa4c | scan_field_for_extra_deck_equip_slot_update | 1 | [eval](eval/0808fa4c.md) |
| 840 | 990 | 8 | 2 | E | 0x0804345c | FUN_0804345c | enqueue_equip_chain_attrs_for_slot_range | 1 | [eval](eval/0804345c.md) |
| 841 | 991 | 9 | 1 | E | 0x080435c4 | FUN_080435c4 | scan_equip_chain_list_by_player_slot | 1 | [eval](eval/080435c4.md) |
| 842 | 992 | 10 | 1 | E | 0x0804ff9a | FUN_0804ff9a | check_card_state_code_eq_11 | 2 | [eval](eval/0804ff9a.md) |
| 843 | 993 | 9 | 3 | E | 0x0804b09c | FUN_0804b09c | check_card_id_in_special_set | 2 | [eval](eval/0804b09c.md) |
| 844 | 994 | 10 | 1 | E | 0x0804ffa4 | FUN_0804ffa4 | check_card_state_code_eq_3 | 2 | [eval](eval/0804ffa4.md) |
| 845 | 995 | 10 | 1 | E | 0x0804ffba | FUN_0804ffba | check_slot_zone_bit3_eligible | 2 | [eval](eval/0804ffba.md) |
| 846 | 996 | 9 | 14 | D | 0x08036450 | FUN_08036450 | check_slot_equip_whitelist_with_monster_space | 1 | [eval](eval/08036450.md) |
| 847 | 997 | 10 | 1 | E | 0x0804ffd2 | FUN_0804ffd2 | check_slot_zone_bit1_eligible | 2 | [eval](eval/0804ffd2.md) |
| 848 | 998 | 9 | 1 | E | 0x0804ff54 | FUN_0804ff54 | check_card_state_code_eq_15 | 1 | [eval](eval/0804ff54.md) |
| 849 | 999 | 9 | 1 | E | 0x0804fed6 | FUN_0804fed6 | return_zero_unconditional | 1 | [eval](eval/0804fed6.md) |
| 850 | 1000 | 9 | 1 | E | 0x0804ffea | FUN_0804ffea | check_slot_zone_bit2_eligible | 1 | [eval](eval/0804ffea.md) |
| 851 | 1001 | 9 | 1 | E | 0x0804fffc | FUN_0804fffc | return_true_unconditional | 1 | [eval](eval/0804fffc.md) |
| 852 | 1002 | 9 | 1 | E | 0x0804ff72 | FUN_0804ff72 | check_card_state_code_eq_16 | 1 | [eval](eval/0804ff72.md) |
| 853 | 1003 | 9 | 1 | E | 0x0804ff7c | FUN_0804ff7c | check_card_state_code_eq_13 | 1 | [eval](eval/0804ff7c.md) |
| 854 | 1004 | 8 | 8 | D | 0x0804f6c4 | FUN_0804f6c4 | check_slot_card_eligible_by_card_id | 2 | [eval](eval/0804f6c4.md) |
| 855 | 1005 | 8 | 1 | E | 0x0802f768 | FUN_0802f768 | find_card_slot_by_zone_card_id | 2 | [eval](eval/0802f768.md) |
| 856 | 1006 | 8 | 11 | D | 0x08044dcc | FUN_08044dcc | enqueue_field_slot_sprite_with_state_update | 1 | [eval](eval/08044dcc.md) |
| 857 | 1007 | 8 | 1 | E | 0x0802f81c | FUN_0802f81c | find_equip_slot_by_zone_card_id_with_flag | 2 | [eval](eval/0802f81c.md) |
| 858 | 1008 | 7 | 1 | E | 0x08042bd0 | FUN_08042bd0 | dispatch_equip_chain_slot_scan_by_player | 2 | [eval](eval/08042bd0.md) |
| 859 | 1009 | 7 | 1 | E | 0x0808f450 | FUN_0808f450 | scan_field_slots_for_lp_change_sprite_update | 1 | [eval](eval/0808f450.md) |
| 860 | 1010 | 7 | 1 | E | 0x0808fbd0 | FUN_0808fbd0 | scan_field_slots_for_archfiend_equip_bitmap_update | 1 | [eval](eval/0808fbd0.md) |
| 861 | 1011 | 7 | 1 | E | 0x0808e4d8 | FUN_0808e4d8 | scan_field_slots_for_lp_zone_sprite_with_equip | 1 | [eval](eval/0808e4d8.md) |
| 862 | 1012 | 7 | 3 | E | 0x0808dd5c | FUN_0808dd5c | scan_field_for_equip_set_slot_sprite_update | 1 | [eval](eval/0808dd5c.md) |
| 863 | 1013 | 7 | 1 | E | 0x0808f6e4 | FUN_0808f6e4 | scan_chain_nodes_for_equip_zone11_sprite | 2 | [eval](eval/0808f6e4.md) |
| 864 | 1014 | 7 | 1 | E | 0x0808fae4 | FUN_0808fae4 | scan_field_slots_for_inactive_equip_bitmap_clear | 1 | [eval](eval/0808fae4.md) |
| 865 | 1015 | 7 | 2 | E | 0x0808f86c | FUN_0808f86c | scan_field_slots_for_equip_chain_node_bitmap_update | 1 | [eval](eval/0808f86c.md) |
| 866 | 1016 | 7 | 1 | E | 0x0804a570 | FUN_0804a570 | enqueue_duel_field_card_slot_sprite | 1 | [eval](eval/0804a570.md) |
| 867 | 1017 | 7 | 1 | E | 0x0808e370 | FUN_0808e370 | scan_field_for_fieldspell_eligible_slot_sprite | 1 | [eval](eval/0808e370.md) |
| 868 | 1018 | — | 1 | E | 0x0809007c | FUN_0809007c | scan_equip_set_slot_sprite_by_counter | 1 | [eval](eval/0809007c.md) |
| 869 | 1019 | — | 1 | E | 0x0808f174 | FUN_0808f174 | scan_field_for_paired_equip_slot_bitmap_update | 1 | [eval](eval/0808f174.md) |
| 870 | 1020 | — | 1 | E | 0x0808e8fc | FUN_0808e8fc | scan_all_zone_slots_for_lp_change_indicator | 1 | [eval](eval/0808e8fc.md) |
| 871 | 1021 | — | 1 | E | 0x08090218 | FUN_08090218 | dispatch_equip_field_scan_sequence | 1 | [eval](eval/08090218.md) |
| 872 | 1022 | — | 1 | E | 0x0804f2e0 | FUN_0804f2e0 | dispatch_equip_field_update_by_anim_state | 1 | [eval](eval/0804f2e0.md) |
| 873 | 1023 | — | 17 | D | 0x0809e9e0 | FUN_0809e9e0 | scan_trap_zone_for_equip_activation_by_card | 2 | [eval](eval/0809e9e0.md) |
| 874 | 1024 | — | 2 | E | 0x0809f000 | FUN_0809f000 | scan_trap_zone_for_equip_activation_the_eye_of_truth | 2 | [eval](eval/0809f000.md) |
| 875 | 1025 | — | 20 | C | 0x0809e920 | FUN_0809e920 | scan_monster_zone_for_equip_activation_by_card | 2 | [eval](eval/0809e920.md) |
| 876 | 1026 | — | 2 | E | 0x0809ec04 | FUN_0809ec04 | scan_monster_zone_for_equip_activation_spirit_of_the_breeze | 2 | [eval](eval/0809ec04.md) |
| 877 | 1027 | — | 2 | E | 0x0809f808 | FUN_0809f808 | scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand | 2 | [eval](eval/0809f808.md) |
| 878 | 1028 | — | 2 | E | 0x0809f158 | FUN_0809f158 | scan_monster_zone_chain_for_equip_activation | 2 | [eval](eval/0809f158.md) |
| 879 | 1029 | — | 2 | E | 0x0809f20c | FUN_0809f20c | scan_monster_zone_chain_for_equip_activation_treeborn_frog | 2 | [eval](eval/0809f20c.md) |
| 880 | 1030 | — | 2 | E | 0x0809f40c | FUN_0809f40c | scan_monster_zone_for_equip_activation_legendary_fiend | 2 | [eval](eval/0809f40c.md) |
| 881 | 1031 | — | 2 | E | 0x0809ec14 | FUN_0809ec14 | scan_monster_zone_for_equip_activation_dancing_fairy | 2 | [eval](eval/0809ec14.md) |
| 882 | 1032 | — | 2 | E | 0x0809ee14 | FUN_0809ee14 | scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution | 2 | [eval](eval/0809ee14.md) |
| 883 | 1033 | — | 2 | E | 0x0809f018 | FUN_0809f018 | scan_trap_zone_for_equip_activation_minor_goblin_official | 2 | [eval](eval/0809f018.md) |
| 884 | 1034 | — | 2 | E | 0x0809f21c | FUN_0809f21c | scan_equip_zone_for_special_summon_activation_return_zombie | 2 | [eval](eval/0809f21c.md) |
| 885 | 1035 | — | 2 | E | 0x0809f41c | FUN_0809f41c | scan_monster_zone_for_equip_activation_exodia_necross | 2 | [eval](eval/0809f41c.md) |
| 886 | 1036 | — | 1 | E | 0x0808e45c | FUN_0808e45c | scan_trap_zone_slots_for_equip_shape_sprite | 1 | [eval](eval/0808e45c.md) |
| 887 | 1037 | — | 1 | E | 0x0808e770 | FUN_0808e770 | scan_effect_zones_for_equip_activation_forced_requisition | 1 | [eval](eval/0808e770.md) |

---

## 历史里程碑

- 2026-05-14: **batch #49 PASSED (campaign-49 落地)** — equip activation chain + zone card id node pool + sprite attr enqueue cluster (scan_equip_set_slot_sprite_by_counter counter_trigger=7 gP1LifePoints+0x1cf4 4-slot scan bit4 equip-activation + scan_field_for_paired_equip_slot_bitmap_update 2px5 card_id=0x147a test_active+card_id=0x146f count_paired==0 enqueue_bitmap + scan_all_zone_slots_for_lp_change_indicator 2px10 card_id=0x1361 bit5/bit1 equip-lock bitmap+submit_lp_change_indicator x2 dual-side + dispatch_equip_field_scan_sequence ~30-callee sequential chain any-hit-early-exit duel_field master controller + dispatch_equip_field_update_by_anim_state 3-way priority: anim_state/queue_state/field_scan + scan_trap_zone_for_equip_activation_by_card D_shared_mid indeg=17 slot+5 offset trap-zone counter_offset=0x1d24 + scan_trap_zone_for_equip_activation_the_eye_of_truth 5-instr player-invert stub card_id=0x137b + scan_monster_zone_for_equip_activation_by_card C_util_high indeg=20 slot+0 monster-zone counter loop + scan_monster_zone_for_equip_activation_spirit_of_the_breeze 4-instr stub card_id=0x1450 + scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand slot 5..9 card_id=0x1540 enqueue_bitmap + scan_monster_zone_chain_for_equip_activation check_value_in_slot_chain zone=0xb guard + apply activation gDuelFieldSlots=0x0201c8f8 + scan_monster_zone_chain_for_equip_activation_treeborn_frog 4-instr stub card_id=0x19cb + scan_monster_zone_for_equip_activation_legendary_fiend 4-instr stub card_id=0x154d + scan_monster_zone_for_equip_activation_dancing_fairy 4-instr stub card_id=0x1451 + scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution slot0..9 per-frame card_id=0x1491 count_zone_slots_with_card_field5(opponent)*100 LP indicator + scan_trap_zone_for_equip_activation_minor_goblin_official 5-instr player-invert stub card_id=0x1355 + scan_equip_zone_for_special_summon_activation_return_zombie card_id=0x1775 MASK=0x201fff memset(0x18) check_card_special_summon_eligible_full gate + scan_monster_zone_for_equip_activation_exodia_necross 4-instr stub card_id=0x1645 + scan_trap_zone_slots_for_equip_shape_sprite slot 5..9 opponent-side state_mask=0x98300000 enqueue_sprite_attr_with_shape + scan_effect_zones_for_equip_activation_forced_requisition slot 5..10 card_id=0x1354 count_available_effect_zones gate bit4/bit5/bit1 3-flag check); first-shot 20/20, rev=1 (8 fns), rev=2 (12 fns); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (887/1526 = 58.13%)
- 2026-05-14: **batch #48 PASSED (campaign-48 落地)** — equip activation chain + zone card id node pool + sprite attr enqueue cluster (check_card_state_code_eq_15 cmp r3,#0xf beq r0=1 dispatch stub + return_zero_unconditional 2-instr movs r0,0+b-shared-tail unified-false-exit + check_slot_zone_bit2_eligible non-APCS r4/r7 fixed r2=2 check_slot_zone_bit_eligible wrapper + return_true_unconditional 1-instr movs r0,1 fallthrough shared-tail unified-true-exit + check_card_state_code_eq_16 cmp r3,#0x10 sibling + check_card_state_code_eq_13 cmp r3,#0xd sibling + check_slot_card_eligible_by_card_id indeg=8 BST dispatch hub gDuelFieldSlots 40+ branches query_slot_card_state_code r3 card_ptr[0] halfword dispatch + find_card_slot_by_zone_card_id ldrh[+0xa] chain head traverse nodes stride=8 card_id lsrs#0x10 match return 0xffff + enqueue_field_slot_sprite_with_state_update indeg=11 bits[22:16] display_type+bit18 side_flag combined OAM 0x43/0x8043 enqueue + find_equip_slot_by_zone_card_id_with_flag symmetric+bit4 flag_mask r8 extra filter 0xffff no_result + dispatch_equip_chain_slot_scan_by_player ldrh[+0x8] chain-head 0->scan_equip_chain_list_by_player_slot/nonzero->complex path return 0/1 + scan_field_slots_for_lp_change_sprite_update 2x9 loop state_mask=0xa5f80000 enqueue_xy_split+equip_bitmap+submit_lp_change_indicator_with_chain_check x2 + scan_field_slots_for_archfiend_equip_bitmap_update 2x5 card_id=0x16bf test_active+10-subslot archfiend-count=0->enqueue_bitmap + scan_field_slots_for_lp_zone_sprite_with_equip 2x9 opponent_side=1-r6 flip sibling of lp_change + scan_field_for_equip_set_slot_sprite_update 2x5 card_id=0x1009 count_paired_slots+set_slot_bit+enqueue_set_sprite + scan_chain_nodes_for_equip_zone11_sprite 2x check_node zone=0xb 0x0201d9c0 traverse AND=0x0002188c find_slot+enqueue_zone11 + scan_field_slots_for_inactive_equip_bitmap_clear 2x5 bit5==0 inactive+no-archfiend->enqueue_bitmap + scan_field_slots_for_equip_chain_node_bitmap_update bit0 gate+phase_threshold>8 2x5 card_id={0x1596/0x1598}+find_equip_chain_node_by_pred+enqueue_bitmap + enqueue_duel_field_card_slot_sprite gP1LifePoints+0x1ce0 dword P1=0x4d/P2=0x804d OAM enqueue + scan_field_for_fieldspell_eligible_slot_sprite count_field_copies=0x12fb gate 2x5 check_value_in_slot_chain+count_available_effect_zones+check_fieldspell_eligible hit_bitmap enqueue_sprite_attr_by_sign); first-shot 15/20, rev=2: 0x0804f6c4/0x0802f768/0x0802f81c/0x08042bd0/0x0808f6e4; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (867/1526 = 56.81%)
- 2026-05-14: **batch #47 PASSED (campaign-47 落地)** — equip activation chain + zone card scan cluster + sprite attr enqueue + state code checkers + zone eligibility stubs (invoke_equip_activation_with_zero_flag sp+0=0 wrapper flag=0 apply_slot_equip_activation_with_sprite + scan_all_slots_for_max_equip_match 2px[0..9] sp+4 init-template max-ATK compare r7-hit-count + find_matching_slot_by_player_zone_card gDuelFieldSlots [+2] bit0=player bits[5:3]=zone_type [+4] bits[14:8]=card_id + find_card_pair_in_player_deck_list gP1LifePoints+player*0x868+0x10 lsls/lsrs#0x13 13-bit card_id check_card_pair_allowed + scan_card_placement_for_activation byte[+0]=0x1b bit15 type_A=0x17c7/type_B=0x17c8 find_zone+find_pair+find_slot+apply_activation chain + enqueue_sprite_attr_for_card_slot low16 tile_idx attr0=0x58 enqueue_sprite_attr_record + enqueue_sprite_by_field_copy_count card_id=0x1510 count>0 flag compare [gP1LifePoints+0x10d0] bit2 enqueue_sprite_attr_for_card_slot + scan_effect_zone_slots_for_equip_activation 2px5 bits[19:13] card_type=0x16da bit31 [+8]/[+c] nonzero OAM attr build apply_equip_activation+enqueue_xy_split r12-hitcount + scan_slots_for_field_bit4_sprite_update 2px5 low13 mask=0xba200000 set_field_slot_bit_with_sprite_update(r2=4,r3=0) + check_zone_eligible_with_deck_flag r1==0->call_check_field_effect_zone OR r4=r1 get_player_deck_flag_bit1 compare enqueue OAM=0x51/0x8051 + scan_field_for_unpaired_equip_slot_update card_id=0x1914 count_equipped_paired_slots_for_player(0)==0&&(1)==0 enqueue_equip_slot_bitmap_update + scan_field_for_extra_deck_equip_slot_update card_id=0x1645 5x count_extra_deck_cards_by_id(0x0fb7..0x0fbb) any==0 enqueue_bitmap + enqueue_equip_chain_attrs_for_slot_range 2px5=10-call batch enqueue_equip_chain_slot_sprite_attr r3=1 + scan_equip_chain_list_by_player_slot [slot+0xa] chain head: 0->batch-enqueue / nonzero->chain-traverse type[0xa..0xd] node[0]/[1]/[6] enqueue+bitmap + check_card_state_code_eq_11 movs r0,0 cmp r3,#0xb beq r0=1 dispatch-stub + check_card_id_in_special_set leaf BST {0x117b/0x16b9/0x17df/0x18be} 4-ID whitelist + check_card_state_code_eq_3 symmetric sibling cmp r3,#0x3 + check_slot_zone_bit3_eligible non-APCS r4/r7 fixed r2=3 check_slot_zone_bit_eligible stub + check_slot_equip_whitelist_with_monster_space indeg=14 5-step has_card+[+0x8]+field_zone+whitelist+monster_slot chain + check_slot_zone_bit1_eligible non-APCS r4/r7 fixed r2=1 sibling); first-shot 10/20, rev=2: 0x080439a0/0x0808daf0/0x080316b8/0x0804a5a0/0x0804a4cc/0x0804ff9a/0x0804b09c/0x0804ffa4/0x0804ffba/0x0804ffd2; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (847/1526 = 55.50%)
- 2026-05-14: **batch #46 PASSED (campaign-46 落地)** — equip chain pair sprite enqueue + equip slot eligibility/bitmap cluster + field zone card eligibility chain + scan-field dispatcher cluster (enqueue_equip_chain_pair_sprite_if_eligible bit12 dual-activation check then enqueue_equip_chain_pair_sprite_validated+enqueue_sprite_attr_record+scan_equip_chain_list + check_slot_equip_eligibility_by_type 7-caller composite check_slot_card_effect_eligibility+count_zones_by_card_and_mode type=[1/5/6/0xa] dispatch + check_card_id_is_field_zone_special leaf 3-cmp [0x170a/0x1652/0x17d2] + count_eligible_zone_slots_for_player bit12+[+0x8]+zone_bit 5-slot scan + count_eligible_zone_slots_all_flags thin wrapper r2=-1 all-flags tail-call + check_slot_field_zone_card_eligible bit12/bit5/bit1 multi-guard + check_card_id_is_field_zone_special + [0x1826/0x17e4/0x1860] + count_eligible_zone_slots_all_flags + resolve_equip_target_slot_for_enqueue 7-callee chain: field_zone_eligible+equip_type+whitelist+monster_slot+bitmap_update+chain_sprite + prepare_equip_slot_ctx_for_bitmap_update memset(0x18) + [r2+2] bit1 + bitmap 1<<(player*16+slot) zone_flags=0xe + query_equip_target_bitmap_default indeg=29 fixed-param (zone=0xe,side=2) thin wrapper + test_equip_target_slot_in_bitmap indeg=19 1<<(r1*16+r2) slot_mask AND test + update_equip_bitmap_with_cross_side_flag eors/rsbs/orrs/asrs cross-side detect bit17=0x20000 inject + scan_field_for_whitelist_equip_sprite_and_lp 2px5 whitelist+bit5/bit1+enqueue_zone_sprite+submit_lp_change + scan_field_slots_for_equip_bitmap_update 2px(slot5..9) card_id=0x1624 test_active+get_effect_val==0+enqueue_bitmap + scan_field_slots_for_chain_sprite_enqueue 2px5 bit12+[slot+0xc]=0xa2680000 enqueue_xy_split + scan_field_for_equip_priority_slot_update 2px5 card_id=0x160f [slot+4] min-select enqueue_bitmap + check_field_effect_zone_activation_eligible 4-OR chain: count_effect_zones(0x137b)+count_field_copies+count_effect_zones(0x17e7)+active_player_match(0x135e) + scan_field_slots_for_equip_sprite_by_chain 2px5 card_id=0x1817 count_chain_nodes bit5->effect_sprite+equip_sprite + find_first_eligible_zone_slot_for_player early-exit 5-slot bit12+[+8]+zone_bit(r2=1) + scan_field_slots_for_zone_equip_bitmap_update 2px5 card_id=0x13a4 test_active+find_first_eligible+enqueue_bitmap + apply_slot_equip_activation_with_sprite OAM attr 7-mask build + enqueue_sprite_attr_record + set_field_slot_bit + card_id=[0x1005/0x1048/0x101e/0x1197/0x1868] apply_equip_activation + submit_lp_bar_sprite_row); first-shot 16/20, rev=2: 0x08047e20/0x08047f1c/0x0808efa8/0x0808eeb0; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (827/1526 = 54.19%)
- 2026-05-14: **batch #45 PASSED (campaign-45 落地)** — equip activation chain scan cluster + equip zone sprite enqueue cluster + equip eligibility checker chain + equip-pair sprite dispatcher + effect zone LP/shape sprite submitter (scan_field_slots_for_graveyard_equip_activation gP1LifePoints+0x1ce8 2px10 loop card_id=0x1403 Graveyard apply_equip_activation_with_id_lookup + enqueue_equip_zone_sprite_by_side indeg=17 OAM_P1=0x2f/OAM_P2=0x802f H-flip + enqueue_equip_slot_sprite_with_card_check count_field_copies+check_field8_is_9 OAM attr build scan_field_slots_for_equip_sprite + submit_equip_slot_sprite_zone11 indeg=6 fixed r1=0xb zone11 wrapper + scan_chain_nodes_for_equip_zone_sprite 2px11 loop check_node_in_slot_chain(0x123b,zone=0xb,type=2) find_slot_idx enqueue_equip_zone_sprite+submit_zone11+match_sprite + enqueue_equip_chain_sprite_by_side OAM_P1=0x38/OAM_P2=0x8038 row/col byte merge + scan_equip_chain_list_for_sprite_update 0x0201d9c0 chain traversal [node+0x6] next / [node+0x2] type_mask 0xa/0x6 + check_card_equip_eligibility_in_field indeg=6 6-layer check: field8_is_normal/[+0x34]/0x166c/0x12bf(zone=0xb)/summon_restriction/0x148e+0x14da/targeted_by_spell + count_equip_eligible_slots_for_player gDuelFieldSlots+player*0x868+0x10a4 5-slot scan mov r8,r1=card_id check_equip_eligibility + count_equip_eligible_slots_both_players P1+P2 sum wrapper + enqueue_effect_zone_pair_sprite_scan type=0x14 base sprite + check_matches+check_pair inner loop pair sprites + dispatch_equip_pair_sprites_by_state base=0x0201c5d8 stride=0x868 count_equip_eligible_slots_both_players>0 gate classify_card_effect_category enqueue_effect_zone_pair_sprite_scan + enqueue_active_card_shape_sprites_in_zone card_id=0x144d slot 0..4 test_slot_has_active_card enqueue_sprite_attr_with_shape(mode=1) + submit_effect_zone_lp_and_shape_sprites indeg=13 effect_count==0 guard opponent_side count_available_effect_zones(0x1256) OAM=0x24/0x8024 LP_row_type=0x11 + scan_field_slots_for_card_pair_sprite_update 2px10 cmp=0x28a0 enqueue_xy_split+zone_lookup+submit_lp_shape + scan_equip_chain_slots_for_bitmap_update 2px5 card_id=0x14fc base=0x0201e1c8 find_equip_chain_pair_across_field!=0xffff enqueue_equip_slot_bitmap_update + scan_slots_for_equip_activation_by_field5 r9=card_id(0x1762) field5 dispatch monster/trap zone range apply_equip_activation+set_field_slot_bit + enqueue_equip_chain_pair_sprite_validated src/dst encoded params self-ref guard 0x12ab type mask find_equip_chain_pair enqueue_equip_chain_slot_sprite_attr + enqueue_equip_set_slot_sprite_by_zone_col indeg=8 OAM=0x3b/0x803b check_card_id_is_equip_set_a zone_col==0 direct / zone_col!=0 get_set_code + scan_equip_chain_list_for_activation_sprite sibling of enqueue_equip_chain_pair_sprite_validated 0x0201d9c0 chain 0x118a..0x11c9 card_id range enqueue_equip_set_slot_sprite+apply_equip_activation+enqueue_xy_split); first-shot 17/20, rev=2: 0x0808ec08/0x08049e44/0x0804a2c8; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (807/1526 = 52.88%)
- 2026-05-14: **batch #44 PASSED (campaign-44 落地)** — normal summon eligibility chain + sprite row dispatch cluster + field display state dispatcher + equip chain sprite enqueue + zone display index writers (check_normal_summon_eligible_for_slot r0/r1/r2 player/slot_ptr/mode_flag gDuelCardMain search path A/B + check_normal_summon_eligible_for_any_effect_zone 0xce effect_zone_base=0x09e48918 stride=8 scan + check_normal_summon_eligible_any_slot [0x0201afe0] player_ptr write + 0xdd slot gDuelCardMain=0x09e478d0 scan + build_sprite_row_from_zone_state gP1LifePoints+0x1d08 guard byte+word pack submit_sprite_row_data + copy_game_text_if_raw RAW_ID_MASK=0xFFFE0000 high-15-bit check resolve_game_str_ptr+strcpy + append_game_text_if_raw strcat variant + build_field_action_text_by_zone_type gDuelCardBase+0x4d4 type_byte switchD 30-case tail_id=0x10d + check_all_equip_target_slots_available effect_zone_id=0x1468 + 4x find_equip_slot_by_card_id 0x1497..0x149a + check_all_fusion_pair_slots_available 5x count_valid_monster_pair_slots 0x0fb7..0x0fbb + query_summon_eligibility_code priority-9 code [0..9] fusion/equip/chain states + check_normal_summon_eligibility gDuelSettings XOR guard + dual player query_summon_eligibility_code write [+0x2c] + scan_equip_target_slots_for_card gDuelCardBase+0x4d4 byte-1 switchD_080854da 30-case + scan_all_zones_for_equip_target gDuelCardSlots+gDuelEffectZones dual-phase 2-player 11-slot + dispatch_field_display_state_by_type gDuelCardBase+0x578 type_code switchD_08085d70 51-entry + clear_sprite_row_queue_overflow_flag gSpriteRowBase+0x498 zero+return_1 shared frame exit + dispatch_sprite_row_queue_by_state gSpriteRowBase+0x49c state_code PTR_DAT_0804dbb8 dispatch_limit=0x67 + enqueue_equip_chain_sprites_for_zones gP1LifePoints+0x10d0 cooldown gDuelActivation 5-slot scan enqueue_sprite_attr_with_mode(mode=0x9) + apply_equip_activation_from_zone_scan gDuelEffectZones card_type=0x18b2 filter apply_equip_activation_with_id_lookup + enqueue_sprite_attr_with_xy_split + write_card_display_index_if_above_bit indeg=7 get_card_data_bit_by_index+cmp+write_card_display_index_entry + write_monster_zone_display_indices gDuelEffectZones 5-slot field5 scan pair-check write index=0x3b/0x3c/0x3d); first-shot 17/20, rev=2: 0x0801f238/0x0801f25c/0x0804db50; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (787/1526 = 51.57%)
- 2026-05-13: **batch #43 PASSED (campaign-43 落地) — ~50% MILESTONE** — effect slot init/dispatch hub cluster + equip card sprite init + summon eligibility checker chain (count_active_cards_in_zone_by_player 4-slot active-bit9 counter + exit_slot_search_with_result shared epilogue thunk + find_empty_slot_for_card_id_dispatch BST card_id slot finder [0x0201afe0] side-effect + fill_effect_slots_up_to_count type[7..37] loop filler [gP1LifePoints+0x1d40] counter + activate_effect_slot_for_card single-slot type==6/0x49 activator + fill_effect_slots_up_to_count_with_equip_cap type[0x28..0x47] equip-cap variant 0x18e0 special ID + init_effect_slot_display_context indeg=39 hub gEffectDisplayCtx 0x0201e4f0 zero+dispatch + dispatch_to_effect_handler_by_card_type 17-entry ROM table 0x09e47560 stride=0x10 linear scan + dispatch_effect_slot_by_display_state state[0/1/2] 3-way [gP1LifePoints+0x1d60] + invoke_card_display_op_0x31_with_params 4-instr thunk op=0x31/sub=0x2 + enqueue_zone_card_sprite_attr_by_slot gDuelFieldSlots bit9 OAM_ATTR0_BASE=0x8035 enqueue + init_equip_card_sprite_row_entry gP1LifePoints+0x1d68/6c/70 slot_a+slot_b sprite init + write_card_display_ctx_fields leaf 5-field batch write 0x1d4c/7c/58/54/64 + check_effect_zone_available_for_player zone_count>6 || count_available_effect_zones==0 gate + check_card_normal_summon_eligible_full multi-condition BST field6/9/5 chain + find_zone_slot_idx_allowed_for_card indeg=8 check_card_pair_allowed scanner + classify_card_id_summon_category 3-way BST return [0..2] + check_effect_slot_summon_path_eligible type==0xe early-exit + classify loop + check_card_special_summon_eligible_full multi-layer field5/8/zone_type chain + check_card_summon_eligible_by_field6 field6=0x16/0x17 zone_id dispatch fallback); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (767/1526 = 50.26% — half closure reached!)
- 2026-05-13: **batch #42 PASSED (campaign-42 落地)** — LP bar animation state machine dispatch cluster + monster slot entry ptr + LCG PRNG pair (advance_prng_state + sample_prng_scaled) + palette slot scanner pair (read_slot_palette_index + check_slot_palette_nonzero) + slot scan cluster (find_random_empty_slot_excluding_card_id 2-phase prng + check_special_card_activation_eligible {0x1366,0x137d,0x15e6} special IDs + find_slot_by_card_type_and_player bits[18..0]+bit[13] + find_first_empty_slot_for_card_type no-player variant) + card trigger/gate pair (trigger_card_display_op31_if_not_active indeg=119 + trigger_lp_bar_animation_if_ready 0x0fee sentinel) + pair activation checker cluster (count_slot_card_pair_allowed_for_card 0..10 slot loop + check_any_pair_slot_available_for_card dual OR gate + count_zone_card_pair_allowed_for_card zone-based loop + check_compound_pair_activation_eligible 4-fold OR gate) + card type bits reader (get_card_type_bits_by_internal_id ands#3 low-2-bit type enum) + monster field5 threshold counter (count_monster_slots_with_field5_ge_threshold r8 non-APCS threshold) + card ID whitelist checker (check_card_id_in_eligible_set 18+ ID BST leaf) + zone slot scorer (eval_zone_slot_score_for_player 0x0201c510 zone_table r8/r12 high-reg); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (747/1526 = 48.95%)
- 2026-05-13: **batch #41 PASSED (campaign-41 落地)** — equip slot sprite attr enqueue cluster + equip chain all-slots pair enqueue + best-slot ATK scanner pair + effect node snapshot populator + slot card type eligibility query (indeg=74) + equip placement valid check chain + equip target eligibility check + card chain list sprite enqueue + duel field slot sprite state update hub + equip target bitmap updater (indeg=25) + slot ctx preparer + equip slot bitmap update (indeg=43) + equip zone candidate scanner + monster slot card LP bar renderer (enqueue_equip_slot_sprite_attr indeg=35 OAM_BASE=0x8037 + enqueue_paired_slot_sprite_attrs_for_player player*2 row scan mode=3 + enqueue_equip_card_sprite_attr_for_slot equip_set_b 0x3c/0x803c + enqueue_effect_card_slot_sprite_attr effect_category compare + enqueue_equip_chain_slot_sprite_attr find_chain_node 0xa000 OAM + enqueue_equip_chain_all_slots_for_pair double-loop player[0..1]xslot[0..10] + find_best_slot_for_card_by_player field5-dispatch monster/trap zone ATK max + find_best_slot_atk_across_players dual-player max wrapper + populate_effect_node_snapshot 12-field batch fill [r7+0x0..0x2c] + query_slot_card_type_eligibility field6=0x17/0x16/other 3-way dispatch + check_slot_equip_placement_valid 6-step comprehensive check + build_equip_placement_valid_bitmap full-field bitmap build 1<<(player*16+slot) + check_slot_equip_target_eligibility find_equip_target gate + enqueue_sprite_attrs_for_card_chain_list chain list walk [slot+0xa] + update_duel_field_slot_sprite_state bit5 gate + full enqueue dispatch + update_equip_target_bitmap_for_field 2-phase gP1LifePoints+0x10d4 writer + prepare_slot_ctx_for_equip_bitmap memset+bit1-merge + enqueue_equip_slot_bitmap_update player*16+slot bitmask gate + scan_equip_zone_candidates_with_snapshot snapshot+double-loop candidate filter + render_monster_slot_card_with_lp_bar field6/field9 check + LP bar submit); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (727/1526 = 47.64%)
- 2026-05-10: **batch #40 PASSED (campaign-40 落地)** — duel field equip dispatch + zone chain query + sprite attr enqueue cluster (check_equip_eligibility_via_request_buf 24-byte stack equip request constructor + check_zone_card_special_state_by_field5 field5 [6..9]/[0xa..0xd] dispatch + check_card_field8_is_9 indeg=44 5-instr leaf wrapper + scan_field_slots_for_attached_sprite_by_id 0x14bf double-loop + find_node_packed_by_card_id_in_dual_lists 0xffff sentinel + apply_equip_activation_via_packed_attr 8-bit-field record builder + apply_equip_activation_with_id_lookup indeg=61 lookup wrapper + refresh_opponent_field_slots_for_card_attached opp side scan + submit_lp_change_indicator_with_chain_check triple chain gate + check_zone_card_id_in_node_pool 7-instr leaf + enqueue_sprite_attr_for_zone_card_id_lookup indeg=40 0x10e0 zone table + find_zone_node_by_card_id_match FUN_0810e5e4 predicate + dispatch_card_effect_sprite_render_by_card_id 50+ card_id BST + dispatch_card_effect_zone_action_by_card_id 30+ card_id BST sibling dispatcher + handle_card_effect_zone_eligibility_by_field6 0x16/0x17/<=4/[0xe..0xf] field6 dispatch + check_slot_card_eligible_for_special_action 5-card whitelist 0x13ea/0x1231/0x1238/0x1514/0x1980 + find_zone_chain_node_by_card_id_pair zone_type>9 + find_chain_node_by_dual_halfword zone_type<=5 dual chain finder pair + enqueue_sprite_attr_for_chain_node_match 0x38/0x8038 OAM + enqueue_sprite_attr_with_xy_split 0x3a/0x803a OAM xy-pack); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (707/1526 = 46.33%)
- 2026-05-10: **batch #39 PASSED (campaign-39 落地)** — prng anim queue dequeue + per-frame anim step (dequeue_prng_anim_entry gPrng+0x592 frame counter type-mask 0x90/0xA0/0xB0 dispatch + step_prng_anim_frame busy_flag bit0 game-loop-step) + sprite row queue flush/reset/dispatch trio (flush_sprite_row_queue_partial 0x0201b290+0x488 count compact + reset_sprite_row_queue_tail multi-offset zero/set + dispatch_sprite_row_anim_by_state state[0..0xe] 15-case jump table) + card sprite row entry init pair (init_card_sprite_row_entry + init_card_sprite_row_entry_alt symmetric variant via sp[0x18] vs r10) + OAM sprite attr enqueue 5-fn cluster (enqueue_sprite_attr_with_mode indeg=74 core primitive 5-param packing + enqueue_sprite_attr_type11 indeg=81 type=0xb wrapper + enqueue_sprite_attr_by_sign sign-determined palette 0x30/0x8030 + enqueue_sprite_attr_clamped count clamp [0..0xffff] + enqueue_sprite_attr_with_shape r0/r3 shape selection 0x3a/0x803a) + render_field_card_copy_count count+marker+loop pipeline + check_card_type_is_spell map_field8==3 indeg=25 + scan_field_slots_for_equip_sprite gDuelFieldSlots two-side 9-slot active_mask 0x9b080000 + find_equip_target_for_card_slot stat_field8 0xa/0xb equip_chain pair lookup + count_equip_slots_matching_whitelist + count_equip_slots_active_only fixed-arg wrapper + map_card_id_to_anim_type 6-label binary-search dispatch tree NO_ANIM=0/DEFAULT=1/EXTRA=2/SPELL=4/EQUIP=6 + check_card_equip_eligible_for_slot indeg=37 C_util_high TYPE_A=0x150c/TYPE_B=0x1645 multi-phase eligibility eval; first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (687/1526 = 45.02%)
- 2026-05-10: **batch #38 PASSED (campaign-38 落地)** — sprite attr record cluster + LP bar display counter cluster + LP display state/commit pair + field slot bit writer pair + card display index cluster + misc callee util (reset_sprite_attr_record_flags struct@0x0201e4d0 AND-mask bit0/clear-bit1/OR-0x30-done + submit_lp_bar_sprite_row_by_type indeg=32 path-A LP ptr match + path-B gDuelCtx+0x4d0 count=0 submit_sprite_row_data(type=0x9,count=6) + check_card_effect_node_active find_node+rsbs+orrs+lsrs#0x1f bool + dispatch_card_effect_by_stat_type bit1-processed/bit2-alt/field9[2..3]/card_id=0x1909 pure-read + read_prng_entry_flag_clear gPrng+0x1c0[+0x584] bics#1 flag-clear bool + commit_lp_display_row_to_sprite gP1LifePoints+0x1d88/0x1d94/0x1d84 active-zero-done copy+submit(type=0x1e,count=0x12) + setup_lp_display_row_with_data r0/r1->+0x1d6c/+0x1d70 copy+commit chain + get_lp_display_state_word 4-insn leaf gP1LifePoints+0x1d0c + write_sprite_attr_record_entry gSpriteAttrBuf@0x0201b870 4x strh[0x304/0x306/0x308/0x30a] OR-filled-bit-0x4 at[0x300] clear-pad[0x30c] + increment_lp_bar_display_counter indeg=64 C_util_high gDuelCtx+0x4c4 +1 first-1 init 0x4cc/0x580/0x4c8 + find_slot_idx_in_dual_list_by_id dual-loop base=0x10e0 127-entries lsls#0x13/lsrs#0x13 13-bit-id + write_field_slot_bit_by_player indeg=11 player*0x868+slot*0x14+0x40 OR/BIC + set_field_slot_bit_with_sprite_update indeg=29 change-guard write_field_slot+enqueue_sprite_attr OAM_y=0x2a/0x802a + submit_slot_card_sprite_row_entry find_slot_idx+sp-6strh submit(type=0x14,count=0xc)/alt zero_fill+pack+active_count++ + decrement_lp_bar_display_counter indeg=67 C_util_high gDuelCtx+0x4c4 -1 symmetric + write_card_display_index_entry indeg=10 dual-path direct<=0x34/bitfield-0xd4+OR-BIC + write_card_display_index_with_bit_offset indeg=27 get_bit+base_offset wrapper + update_card_display_index_by_type_rules field6=0x17/0x16 write_index[0x3a/0x39/0x21/0x1f/0x20/0x22] player_id XOR guard + increment_lp_bar_counter_no_player indeg=4 no-player-param halfword=2 variant + check_prng_anim_frame_slot_occupied gPrng+0x1c0[+0x5a0+player*14] OAM-attr circular-scan[&0x3f] hit=1/miss=0); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (667/1526 = 43.71%)
- 2026-05-10: **batch #37 PASSED (campaign-37 落地)** — card display op dispatcher cluster (dispatch_card_display_op indeg=114 op_range=[1..0x3d] 61-entry jump table 0x0801ecc4 + pack_sprite_row_attr_words r0[15:0]|r1[15:0]<<16 first attr + sp[4] AND mask pair second attr submit_sprite_row_data(count=6) + init_field_slot_aob_ctx_a cases 0x01/0x21 zero_len=0xd8 base=DAT_080bc7d4 r8=r2 via mov + init_field_slot_aob_ctx_b case 0x0b base=0x0201fe60 palette<<3 bit[10:3] init_aob_ctx_from_ptnsect + write_zone_oam_entry_with_flip case 0x0c sub_idx<<5|zone_type key->flip selection [base+0x14/0x18] ctrl=0x02023345 + write_field_slot_activation_mask case 0x09 zero_len=0xb8 r0[4:0]<<3->[base+3] r0[21:19]->[base+4] + init_field_slot_aob_ctx_c case 0x19 zero_len=0x38 init_flag=0x2 bit1 + init_field_slot_aob_ctx_d case 0x18 zero_len=0x38 init_flag=0x1 bit0 r8=r2 via mov + init_field_slot_ctx_zoom case 0x1a zero_fill 0x38 bytes ctx_src/ctx_dst + render_field_slot_card_tile_by_id case 0x1b slot_descriptor decode get_field_slot_tile_vram_addr +0x120 cache ensure+render + init_card_effect_aob_ctx case 0x06 classify_card_effect_category<<1->gDuelActivation[2:1] init_aob_ctx_from_ptnsect[+0x38] + zero_card_name_vram_buf 32KB VRAM clear ctrl_val=0x0b + copy_game_text_to_card_name_vram case 0x31 zero+resolve_game_str_ptr x2+copy_cstr_to_buf vram_base+1 + get_duel_activation_zone_id 3-instruction leaf ldr+ldr[+0xc]+bx lr + build_field_zone_display_state case 0x32 zero gDuelZoneState 0x5eb8 bytes zone_id<<13 into [+0x2f50] slot loop ensure+find+eval card_stats ldmia/stmia + refresh_all_zone_slot_tile_display case 0x24 final step outer[0..1] inner[0..4]+[5..10] get_zone_slot_entity_ref+update_field_slot_tile_display + update_zone_activation_display_state case 0x03 [0..1]x[0..10] dispatch_zone_activation_by_state FLAG_ACTIVATABLE=0x800 gDuelZoneCtrl=0x020230c0 + get_player_lp_by_field_type case 0x14 gP1LifePoints+player*0x868 type[0xc..0xf]->[+0x18/+0x10/+0x14/+0x1c] + invoke_card_display_op_0x31 4-movs thunk op=0x31 sub_param=0x0b + process_card_play_ok_sequence play_card_ok_ui_effect+enqueue_sprite_attr_record 0x8006/0x8007/0x8008+pack_sprite_row_attr_words+invoke_card_display_op_0x31 phase_counter+1); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (647/1526 = 42.40%)
- 2026-05-10: **batch #36 PASSED (campaign-36 落地)** — zone slot comparator cluster + zone sort insertion/quicksort + zone slot sorted view setup + zone card list state machine/view + zone display frame tick + zone detail render/panel + zone field info panel + invert zone tick result + play card ok UI effect + return void noop stub + sprite attr queue enqueue + sprite row VRAM write + sprite row dispatch by type + sprite row data submit (compare_zone_slot_visibility_pair gDuelCtx+0x02020160 stride=0x28 compare_table=0x09832604 invisible->1/-1 + compare_zone_slot_stat_with_type_alt type_0x16->-2/type_0x17->-3 + compare_zone_slot_card_stat_with_atk ATK/DEF tables 0x09e4f310/0x09e4f32c/0x09e4f2ac + compare_zone_slot_card_stat_with_level same tables different ptr@080d3f94 invisible=0x27 + sort_zone_slots_by_stat_insertion base-case count<=6 FUN_0810e5d0 comparator ldrh/strh halfword swap + sort_zone_slots_by_stat_quicksort recursive pivot=arr[count/2+count%2] threshold=6 self-recursive + setup_zone_slot_sorted_view gDuelCtx+0x2f52 bits[12:5] VRAM 0x0601f000 zero + dispatch_zone_card_anim_by_type + render_zone_slot_card_icon_tile loop + load_card_list_small_image + dispatch_zone_card_display_by_mode + tick_zone_card_list_state_machine state=0/1/2 gDuelCtx+0x2f4d gPrng+0x148 bit6/7/5 fixed_return=1 + tick_zone_card_list_view type_combined gDuelCtx+0x2f53/0x2f54 bits[7:5]<<3|bits[4:0] type=[1..5]/4/5/6/else full dispatch + invert_zone_tick_result bool-invert wrapper 3-instruction push/bl/cmp/beq/movs/b + tick_zone_detail_render_step render_zone_card_detail_panel+state+1 fixed_return=1 + tick_zone_detail_panel_by_anim_state sub_state [0..6] apply_palette_offset_to_tile_row x2 VRAM=0x0600f00a + tick_zone_field_info_panel sub_state=0 zero VRAM / 1..6 palette / 7 render_duel_field_zone_info+copy_bytes OBJ_PAL=0x050002e0 + tick_zone_display_frame gDuelCtx+0x2f4c selector LP_alive gPrng_rand/60>179 flag + 4 sub-system dispatch + play_card_ok_ui_effect movs r0,#0x31=49 bl play_ui_effect single-instruction wrapper + return_void_noop_stub bx lr release-stub + enqueue_sprite_attr_record indeg=135 queue_base=0x0201bcc0+0x808 capacity=0xff 4-strh x/y/w/h + write_sprite_row_to_vram_buffer r7=(r1+1)/2 <=6 single-ch/>6 dual-ch IME toggle gPrng+0x464/0x584 + dispatch_sprite_row_write_by_type subs#2/cmp#0x1d switch_table=0x080953dc 30-entry bits[18:15] 0x0201b870 + submit_sprite_row_data 256-byte stack buf r1=-1 skip-header copy_bytes+dispatch+write 3-step); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (627/1526 = 41.09%)
- 2026-05-10: **batch #35 PASSED (campaign-35 落地)** — zone card anim OAM render cluster + equip eligibility check chain + hand slot search pair + effect ctx slot writer (render_zone_card_anim_oam_frame gDuelCtx+0x2f53/0x2f54 type_combined 4-branch OAM write + render_zone_card_anim_oam_frame_alt subs#5 multi-col variant + check_zone_anim_id_in_table linear-scan gDuelCtx+0x2e00/0x2e40 halfword array + check_card_stat_field8_is_7 field8==7 bool wrapper sibling cluster + check_card_is_equip_target_eligible BST exclusion + special_group 2/4 filter + eval_equip_placement_full_check 5-step toon-world chain + check_zone_slot_equip_eligible_alt alt zone_base=0x0201cab0 + find_hand_slot_idx_by_set_code_alt count_offset=0x1c/array=0x5d0 + count_slots_equippable_by_state_code guard_0x13f2 + 2-player slot sweep + check_zone_slot_equip_eligible indeg=21 C_util_high zone_base=0x0201c8f8 + find_hand_slot_idx_by_set_code indeg=43 C_util_high count_offset=0x14/array=0x418 + dispatch_effect_ctx_slot_by_zone_type zone_type[0xb..0xf] 5-entry jump table + render_zone_card_anim_oam_with_base r9=gDuelCtx internal + check_zone_anim_id_in_table + strh-clear + render_zone_card_anim_dual_pass active_flag gDuelCtx+0x2f51 bit4 guard + 2-pass OAM + write_effect_ctx_slot_index 3-instruction leaf gEffectContext+0x8 + dispatch_zone_card_anim_by_subtype gDuelCtx+0x2f4e subtype [0..6] 7-entry table + update_zone_anim_queue_entry clear/shift mode queue gDuelCtx+0x2dfe + compare_zone_slot_card_stat_pair/alt/win three-sibling -2/-3 vs -1/-2 vs +9 ldmia/stmia 24-byte card_stats batch); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (607/1526 = 39.78%)
- 2026-05-10: **batch #34 PASSED (campaign-34 落地)** — duel zone card anim dispatch cluster (dispatch_zone_card_anim_by_type 7-case bx-r8 jump-table gDuelCtx+0x2f53 bits[7:5] | gDuelCtx+0x2f54 bits[4:0]<<3 type_combined [0..6] + tick_zone_card_anim_state 3-phase state-machine [0x020230ad] idle/loading/active gPrng+0x148 flag-check + advance_zone_card_anim 2-instruction bl+b call-then-exit stub + signal_zone_tick_done 1-instruction movs r0,#1 fallthrough stub + dispatch_zone_card_anim_by_type_alt symmetric partner attr-code=6 gDuelCtx+0x2f56 row-offset variant + exit_zone_tick_frame shared pop+bx frame exit 3-instruction stub); first-shot 6/6; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (587/1526 = 38.47%)
- 2026-05-10: **batch #33 PASSED (campaign-33 落地)** — card-list display master + face tile row render pair + card frame tile copy + card-list scene frame tick + tile palette buf writer + tile row clamped reader + field scroll phase checker + zone slot visibility checker + zone slot card icon tile render + zone card detail panel (8-step full render) + zone card JP text panel + zone card display mode dispatcher + zone card detail view 4-state machine (tick_card_list_display_master 2-level mode dispatch + render_card_list_face_row_by_mode/alt lsls#0xf/lsrs#0x18 mode extract 3-variant strh VRAM + copy_card_frame_tiles_by_type copy+computed-goto 14-case + tick_card_list_scene_frame PRNG/60 threshold + set_tile_palette_index_in_buf halfword bit[15:8] write + get_clamped_tile_row_count 3-range clamp + check_field_scroll_phase_ready 4-range phase check + check_zone_slot_attr_visible slot*0x28 stride attr_type=0xf + render_zone_slot_card_icon_tile slot%5 VRAM row + render_zone_card_detail_panel 8-step BG+OBJ+JP pipeline + render_zone_card_jp_text_panel zero+copy+JP render 2-line + dispatch_zone_card_display_by_mode r1=[0..1] mode + tick_zone_card_detail_view 4-state fadein+card_info+rebuild+fadeout); first-shot 14/14; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (581/1526 = 38.07%)
- 2026-05-10: **batch #32 PASSED (campaign-32 落地)** — card-list OAM row render cluster + dispatch hub + slot search pair (dispatch_card_list_oam_row_by_card_type 10-case jump-table gFontState[0x0a01]-1 [0..9] + render_card_list_oam_row_by_jp_type JP row count/state 4-way dispatch + render_card_list_oam_row_by_pack_slot case1 slot-state [0..1] + render_card_list_oam_row_by_dual_slot case4 __divsi3 x2 divisor=0xc8 OAM_Y+0x1c + render_card_list_oam_row_by_cursor_slot case3 cursor active/max check attr0=0x88 + render_card_list_oam_row_by_anim_frame case10 6-strip loop PRNG delta [0..3] + render_card_list_oam_row_by_rarity_flag case5 rarity 0x200/0x400 20-iter mod/div-10 + render_card_list_oam_row_by_pack_column case7 pack_col_count [0..2] __divsi3 divisor=2-N + render_card_list_oam_row_by_type_icon case6 slot_count icon loop + render_card_list_oam_row_by_single_slot case9 divisor=0xb8 OAM_Y+0x2a sibling-pair + render_card_list_oam_row_by_cost_bar case8 near-byte-identical to pack_slot + render_card_list_oam_row_by_stat_state 4-state stat machine find_fwd/bwd + find_next_occupied_slot_forward circular bit-search r2++ + find_next_occupied_slot_backward r2-- symmetric sibling); first-shot 14/14; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (567/1526 = 37.16%)
- 2026-05-10: **batch #31 PASSED (campaign-31 落地)** — card list OAM row writer hub + display state dispatcher + card name JP render + card info init cluster + 8 sibling OAM row state-machine variants + 2 slot search helpers (write_card_list_oam_row_strip indeg=10 7-slot inner loop + dispatch_card_display_state_by_mode switchD 7-case + render_card_name_jp_to_bg_tile_vram 8-step render pipeline + init_card_info_display_with_jp_label 9-callee init sequence + render_card_list_oam_row_by_lp_counter gPrng+0x148 mask=0xc0 + render_card_list_oam_row_by_nibble_rotate 0x0a0e nibble-dec rotate + render_card_list_oam_row_by_flag_check shortest sibling bit0/bit1 + render_card_list_oam_row_by_lp_nibble nibble-to-LP write + find_next_occupied_slot_in_main_list modsi3-6 + find_next_occupied_slot_in_secondary_list symmetric reverse-search + render_card_list_oam_row_by_slot_advance extra Y-offset + 5 cursor sprites + render_card_list_oam_row_by_stat_display render_card_numeric_stat_to_bg callee + render_card_list_oam_row_by_lp_init mask=0x30 + render_card_list_oam_row_by_slot_nibble nibble_B OR bit1); first-shot 14/14; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (553/1526 = 36.24%)
- 2026-05-09: **batch #30 PASSED (campaign-30 落地)** — blend control reset (reset_blend_control_regs BLDCNT/BLDCOEF/BLDALPHA clear) + banner display state machine (tick_banner_display_state_machine 9-case switch gBannerState+0x10) + card play condition check (check_card_play_condition_eligible 0x0201bcc0 precond + LP check) + card view LP time render (render_card_view_scene_by_lp_time __divsi3 0x3c=60) + field BG tile VRAM init (init_field_bg_tile_vram_layout packed_params r0 hi/lo split + 3x tile_2d_row_copy) + card entry JP label render (render_card_entry_jp_labels_to_bg loop [0..3] card entries) + stat tiles render (render_card_stat_tiles_to_vram stat_value ATK/DEF modsi3/divsi3 10 cols) + field slot tile attrs (init_field_slot_tile_attrs 15-bit palette + 7-bit tile_offset STATE_DONE=7) + duel zone card detail (render_duel_zone_card_detail_to_vram 8-step card+zone+JP+small+large render) + 2-line JP text pair (render_jp_two_line_text_to_bg_vram + render_jp_two_line_text_to_bg_vram_alt symmetric siblings loop [0..1] FONT_SIZE=0x200) + LP zone OAM digits (render_lp_zone_digit_oam_row slot.id==0 loop + 3x write_decimal_digits_to_oam) + JP label row pair (render_jp_label_row_with_tile_count nibble-loop + render_jp_label_row_with_tile_pos direct tile_row calc, symmetric siblings) + card label VRAM zero-fill guard (zero_fill_card_label_vram_if_ready dual-flag check + resolve_game_str_ptr conditional render); first-shot 15/15; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (539/1526 = 35.32%)
- 2026-05-09: **batch #29 PASSED (campaign-29 落地)** — zone slot entity ref reader (get_zone_slot_entity_ref_by_type indeg=11 switch-5-cases + default) + pack banner 3D state machine pair (tick_pack_banner_3d_state_machine 7-phase + tick_pack_banner_3d_state_machine_alt alt-resource-path) + OAM slot-check writer (write_oam_entry_with_slot_check sentinel=0x80) + card zoom OAM grid (render_card_zoom_oam_sprite_grid __divsi3/__modsi3 折行) + zone pair OAM (write_zone_pair_oam_with_coords gDuelActivation flip-dispatch) + pack banner state machine A/B sibling pair (tick_pack_banner_state_machine_a pal_init=0x098cc0a4 + tick_pack_banner_state_machine_b pal_init=0x098c9064) + zone slot OAM descriptor (write_zone_slot_oam_descriptor 16-case switch) + UI effect flag clear (clear_ui_effect_state_flags bit1/bit0-bit2) + UI effect card-type dispatcher (dispatch_ui_effect_by_card_type 5-case) + card pair state machine (run_ui_effect_card_pair_state_machine resolve+load+build) + duel puzzle banner state machine (tick_duel_puzzle_banner_state_machine sin-wave OAM 9-phase) + campaign banner init+tick pair (init_window_regs_for_campaign_banner WIN0H/WININ/BLDCNT + tick_campaign_banner_slide_state_machine WIN0V slide 4-phase); first-shot 15/15; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (524/1526 = 34.34%)
- 2026-05-09: **batch #28 PASSED (campaign-28 落地)** — LP digit OAM renderer + release noop pair (return_void_noop + suppress_display_output) + blend EVY pair (start_blend_fade_with_evy + advance_blend_evy_step) + OBJ affine cluster (write_obj_affine_scale_diagonal pure-diagonal + write_obj_affine_rot_scale sin-table) + write_obj_attr_256color_affine (bit13 mode) + pack OBJ attr by_dir trio (write_pack_obj_attr_by_dir + write_pack_obj_attr_by_dir_split r3-hi16 + write_pack_obj_attr_by_dir_stacked r3-both-stacked) + banner dual-state-machine (dispatch_banner_anim_tick_by_state gBannerState[+0x11] + dispatch_banner_scene_tick_by_state gBannerState[+0x10]) + compute_duel_zone_dir_for_player zone-direction pure-read + update_zone_oam_card_count_tag zone-deck OAM tag update + draw_number_digits_to_oam LP digit loop; first-shot 15/15; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (509/1526 = 33.36%)
- 2026-05-09: **batch #27 PASSED (campaign-27 落地)** — card-data bit query + result_screen card name render pipeline + duel puzzle search + zone OAM decode/LP threshold/coord/sort cluster + LP anim counter + OAM sprite attr write pair (get_card_data_bit_by_index indeg=6 + render_game_text_decimal_to_line + get_duel_puzzle_count indeg=7 leaf + find_puzzle_slot_by_id linear scan + render_card_name_escape_to_line switchD tail + init_card_name_result_screen full screen init + decode_zone_oam_word_to_cursor_fields 16-case + check_lp_threshold_for_zone_slot 3-way + decode_zone_oam_word_to_slot_fields 16-case + check_zone_card_id_cache_valid + sort_zone_oam_entries_to_vram qsort+writeBack + set_zone_oam_coords_by_player + get_lp_display_anim_counter leaf + write_oam_entry_attr_pairs 4-strh + write_oam_sprite_entry_by_flip_mode 16-flip-case); first-shot 15/15; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (494/1526 = 32.37%)
- 2026-05-09: **batch=19 #26 PASSED (单 call 落地)** — duel field card sprite OAM phase dispatch cluster + result_screen blend fade + LP display counter clear + pack VRAM upload + card name format render pipeline (dispatch_duel_field_zone_oam_by_type + init_duel_field_card_sprite_vram + tick_card_sprite_oam_step_b/c 兄弟对 + tick_card_sprite_oam_phase_dispatch 4-phase state machine + resolve_zone_data_ptr_by_oam_word indeg=6 + dispatch_duel_zone_pair_to_oam + setup_zone_oam_entry_by_field_slot + zero_duel_lp_display_counters leaf + tick_scene_blend_fadeout_step + tick_scene_blend_fadein_step 对称对 + tick_scene_blend_fade_sequence state machine + init_zone_oam_ctx_by_type + init_jp_font_linebuf_for_render + commit_glyph_linebuf_to_sprite_vram_with_index + upload_pack_vram_and_palette indeg=13 + find_lp_entry_by_flag_and_type + render_card_name_format_to_line + expand_card_name_escape_to_buf); first-shot 19/19; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (479/1526 = 31.39%)
- 2026-05-09: **batch=20 #25 PASSED (单 call 落地)** — card frame nibble/OAM + blend counter + AOB frame tick/render + duel field slot OAM grid + OAM zone coord resolver cluster (write_nibble_row_pair_to_bg_tiles + copy_card_frame_nibbles_to_palette_vram + render_card_display_with_type_gfx + clamp_blend_counter_to_target + blit_card_frame_tile_row_to_vram + build_slot_activation_mask_for_player + push_oam_entry_to_aob_slot + render_aob_frame_to_oam indeg=11 + tick_aob_frame_counter indeg=11 + write_digit_oam_column_with_scroll + render_decimal_number_to_oam + render_card_number_oam_by_player + render_dual_card_number_oam_columns + init_duel_zone_target_slot_refs indeg=11 + transform_zone_oam_coords_by_player + resolve_zone_oam_base_coords_by_type indeg=11 + render_duel_field_slot_oam_grid + compute_card_sprite_oam_coords_by_zone + tick_card_sprite_oam_step_a + write_tile_rows_to_vram_by_mode); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (460/1526 = 30.14%)
- 2026-05-09: **batch=20 #24 PASSED (单 call 落地)** — duel field VRAM init + AOB ctx cluster + card image/name/atkdef render pipeline (write_lp_digit_tiles_to_vram + init_duel_field_tile_indices + resolve_aob_pattern_entry_ptr + init_aob_ctx_with_anm_entry indeg=14 + init_aob_ctx_from_ptnsect indeg=14 + init_duel_field_lp_aob_ctx + init_duel_field_vram_layout indeg=8 hub + tick_duel_field_fadeout_step indeg=8 + tick_duel_field_fadein_step indeg=10 + blend_palette_entry_toward_target indeg=8 + tick_banner_pack_state_machine + write_card_image_oam_grid + tick_blend_step_with_bldcnt + init_line_buf_with_jp_font_flag + draw_card_atkdef_label_to_vram + repack_nibbles_with_palette_offset + render_card_image_to_vram + draw_card_name_to_bg_tile_vram + write_nibble_to_bg_tile_cell + write_nibble_sequence_to_bg_tiles); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (440/1526 = 28.83%)
- 2026-05-08: **batch=20 #23 PASSED (单 call 落地)** — duel field zone activation dispatch + field slot tile render cluster (eval_slot_activation_eligibility_full indeg=11 + check_any_slot_fieldspell_zone_eligible + count_slots_with_chain_field_match + eval_slot_fieldspell_activation_full + eval_slot_activation_guard_full indeg=9 + setup_equip_slot_activation_entry + dispatch_zone_effect_by_slot + eval_zone_activation_flags_by_type + build_zone_activation_entry_blocked/equip 兄弟对 + setup_equip_slot_activation_entry_alt + dispatch_zone_activation_by_state indeg=5 hub + query_player_slot_activation_bitmask + render_field_slot_card_tile indeg=5 + refresh_player_field_slot_tiles indeg=6 + render_field_zone_card_tile_by_type + redraw_all_field_slot_tiles + write_palette_tile_row_to_vram + apply_palette_offset_to_tile_row indeg=5 + upload_player_icon_gfx_to_vram); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (420/1526 = 27.52%)
- 2026-05-08: **batch=20 #22 PASSED** — duel slot activation/eligibility eval cluster (eval_slot_score_entry_full callee cluster + check_slot_*_activatable/eligible sibling cluster + Last Warrior/Archfiend/Amazoness card_id anchored cluster + count_slots_matching_card_pair) + check_player_has_equip_type_in_slots; 1 fix iter (8 NEEDS_FIX: 6 R3 non-APCS misclassified (mov rN,APCS) -> delete param rows + 2 R7 self-reference + 1 R7 indeg=41 caller count insufficient); first-shot 12/20; crossed 25% milestone (400/1526 = 26.21%); byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b.
- 2026-05-08: **batch=21 PASSED (单 call 模式)** — duel field equip activation eval cluster (check_equip_slot_pair_can_activate_full + check_equip_slot_can_activate_with_context count-list variant + scan_equip_activation_for_player + scan_equip_activation_with_mode card_id mode init + get_equip_activation_mode_by_card_id leaf + find_slot_idx_by_card_id_in_player_zones indeg=21 + check_banisher_pair_activation_allowed med + eval_equip_target_slot_flags + eval_spell_activation_flags_by_zone indeg=1 large hub + check_card_stat_field8_is_8/6 sibling pair + check_card_has_activatable_effect_node + check_card_id_is_equip_blocker whitelist + eval_equip_activation_for_slot + setup_equip_context_for_slot_activation + setup_equip_context_for_zone_activation + read_player_field_slot_word_by_zone jump-table + check_zone_slot_card_activatable + eval_zone_activation_flags_for_player + count_equip_set_activatable_slots_for_player r8/r9/r10 non-APCS); first-shot 20/20; byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b. (380/1526 = 24.90%)
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
