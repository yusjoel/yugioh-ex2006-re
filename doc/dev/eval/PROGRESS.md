# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> **每完成 1 个 batch (默认 15 函数), fixer 一次性更新本文档** (PROGRESS 字段 + N 行函数列表)

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=15 全自动模式。

python tools/ad-hoc/pick_batch.py --max 15 --out temp/batch.json   # ← 改 15 调整 batch 大小

启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,
单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。

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
| **当前步骤** | Step 1 — executor (batch=15 模式, campaign-6) |
| **下一步** | `python tools/ad-hoc/pick_batch.py --max 15 --out temp/batch.json` → 启动 4-agent loop (campaign-6) |
| **上次更新** | 2026-05-06 (campaign-5 batch, 75/1526) |
| **上次 callgraph 刷新** | 2026-05-05 (含 +50 新反汇 fns, +131 callgraph 边, +26 manual dispatch 边) |
| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |

## 进度

**75 / 1526 已分析** (campaign_scene_handler 闭包: 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过, 待命名 1526)

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

---

## 历史里程碑

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
