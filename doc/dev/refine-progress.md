# refine-progress — asm/ 25 模块细化总进度

> **总目标**: `asm/` 下 25 个反汇编模块 (`NN_*.s`, 覆盖 ROM 0x080000c0..0x084c7637) **全部内部细化完成**——
> 消灭 `DAT_/DWORD_/UNK_/PTR_DAT_` 自动名 + `ROM_INCBIN`/`.byte` 未分化块, 立即数符号化, 注释订正,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> **驱动**: skill `refine-loop` + 3 sub-agent (`refine-{executor,reviewer,fixer}`)。方法论
> `doc/dev/methodology/refine-loop.md`。这是 refine-loop 的**跨文件状态镜像** (类比 analysis-loop 的
> `eval/PROGRESS.md`)。
>
> **当前文件**: `00_system_str_vija.s` (进行中, ~7/10 段)。
> **下一任务**: **Seg-7** (00 文件, 0x18774..0x19a58, ~28 fn, ROM_INCBIN 0x19640/0x20)。

---

## 一、25 文件总表

| # | 文件 | 地址区间 | 段(~10/文件) | 状态 | 活动 doc |
|---|------|----------|------|------|---------|
| 00 | system_str_vija | 0x080000c0..0x0801cb00 | Seg-1..10 已拆 | 🟡 进行中 (1..6b ✅, 7→) | `doc/dev/p5-refine-00-system-str-vija.md` |
| 01 | vija_scene_text | 0x0801cb00..0x0802c238 | 未拆 | ⬜ | (待建) |
| 02 | text_lp_fieldspell | 0x0802c238..0x08035f54 | 未拆 | ⬜ | |
| 03 | equip_chain_hand | 0x08035f54..0x0804020c | 未拆 | ⬜ | |
| 04 | card_zone_sprite | 0x0804020c..0x08049014 | 未拆 | ⬜ | |
| 05 | equip_eligibility_a | 0x08049014..0x080537c0 | 未拆 | ⬜ | |
| 06 | equip_eligibility_b | 0x080537c0..0x0805c2f0 | 未拆 | ⬜ | |
| 07 | equip_effect_chain | 0x0805c2f0..0x080643e0 | 未拆 | ⬜ | |
| 08 | equip_oam_neodaed | 0x080643e0..0x0806e76c | 未拆 | ⬜ | |
| 09 | equip_lp_display | 0x0806e76c..0x08079e60 | 未拆 | ⬜ | |
| 10 | equip_effect_dispatch | 0x08079e60..0x080850d8 | 未拆 | ⬜ | |
| 11 | effect_slot_puzzletext | 0x080850d8..0x080941c4 | 未拆 | ⬜ | |
| 12 | equip_activation_scan | 0x080941c4..0x0809d718 | 未拆 | ⬜ | |
| 13 | equip_placement | 0x0809d718..0x080a78dc | 未拆 | ⬜ | |
| 14 | equip_ai_scoring | 0x080a78dc..0x080b5348 | 未拆 | ⬜ | |
| 15 | equip_target_summon_zoom | 0x080b5348..0x080c1448 | 未拆 | ⬜ | |
| 16 | duelfield_zone | 0x080c1448..0x080cbf0c | 未拆 | ⬜ | |
| 17 | duelfield_pack_frame | 0x080cbf0c..0x080d5e84 | 未拆 | ⬜ | |
| 18 | pack_card_info | 0x080d5e84..0x080df368 | 未拆 | ⬜ | |
| 19 | pack_eligibility_anim | 0x080df368..0x080e90a0 | 未拆 | ⬜ | |
| 20 | anim_jp_tileblit | 0x080e90a0..0x080f413c | 未拆 | ⬜ | |
| 21 | font_title_scene | 0x080f413c..0x080fdd3c | 未拆 | ⬜ | |
| 22 | cardlist_scene | 0x080fdd3c..0x081078d4 | 未拆 | ⬜ | |
| 23 | sound_cardlist_libc | 0x081078d4..0x08110dc8 | 未拆 | ⬜ | |
| 24 | libc_runtime | 0x08110dc8..0x084c7637 | 未拆 | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 二、当前文件 (00) 段进度

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1a | b1 残留 3 defer | ✅ | da7eb99 |
| 1b | 0x14398..0x14600 (7 fn) | ✅ | f37d2ed |
| 2 | 0x14838..0x14fa8 (§5.1 only) | ✅ | 39b3dfd |
| 3a | fs_load (carve fs 关键字表) | ✅ | ea54718 |
| 3b | 0x1510a..0x1571c | ✅ | 0421491 |
| 4 | 0x1571c..0x16218 | ✅ | 9626e06 |
| 5a | write_tile_region | ✅ | b177f9a |
| 5b | apply_bgdt/objd | ✅ | (committed) |
| 5c | apply_gfx_resource_list + R4 disasm 63 SJIS stubs | ✅ | (committed) |
| 5d | 0x171ec..0x1794c (15 fn + 2 carve + §5.1 0x17424/0x40) | ✅ | 8c4ec5a |
| 6a | 0x1794c..0x17e48 (5 fn, kana carve A+B+pool+I) | ✅ | baabb9a |
| 6b | 0x17e48..0x18774 (23 fn, carve F/G/H, §5.1 0x186ce/0x22) | ✅ | (pending commit) |
| **7** | **0x18774..0x19a58 (~28 fn, incbin 0x19640/0x20)** | **⬜ 下一步** | |
| 8 | 0x19a58..0x1a794 | ⬜ | |
| 9 | 0x1a794..0x1b850 (incbin 0x1a89c, 0x1ad18/0xec) | ⬜ | |
| 10 | 0x1b850..0x1cb00 | ⬜ | |

00 文件完整路线图 (段范围 / ROM_INCBIN / 旧覆盖) 见其活动 doc §五。
00 文件 §5.1 未引用登记: 0x14e54 / 0x14f9c / 0x1547e / 0x1550a / 0x156ec / 0x15d18 / 0x15fe8 /
0x16074 / 0x169d6+0x16a20 / 0x17424 / 0x186ce (孤儿 dead-code, 引用到时再 R4 disasm)。

---

## 三、自动推进协议 (refine-loop 跨文件)

```
当前段完成 → 同文件下一段 (地址序, 不跳号)
当前文件全段 ✅ → 在本表标 ✅ → 自动跳下一文件 (NN+1):
   1) 为新文件建活动 doc doc/dev/refine/<NN_name>.md (含 §一 R1-R9 引用 / §二 pipeline /
      §三 进度 / §四 逐段记录 / §五 路线图 / §5.1 登记) —— 模板抄 00 文件 doc
   2) **先按地址拆分**: push-prologue 抽函数入口, 地址序均分 ~10 段 (边界=函数结束处),
      写入新 doc §五 路线图 (每段地址范围 + 内含 ROM_INCBIN + 旧覆盖列留空)
   3) **再逐批处理**: 从 Seg-1 起, executor → reviewer → fixer 逐段推进
   4) 更新本表该文件 doc 列 + 状态, 更新顶部"当前文件/下一任务"
全 25 文件 ✅ → refine 总目标达成
```

> 跨文件注意: 符号化时**优先复用**已建的 `constants/*.inc` (gSettings / OBJ_PALRAM_BASE / FourCC tag /
> ROM_REGION_CODE_ADDR / gFsDecompBuf / gTextEncodingOverride / GFX_ATTR_CLEAR_BITS_* 等)。
> 同一 ROM 数据被多文件引用时, 谁先 carve 谁建 label, 后者直接 `.word <label>` 引用。

---

## 四、关键路径

| 文件 | 用途 |
|------|------|
| `.claude/skills/refine-loop/SKILL.md` | 驱动器 (3-agent 编排 + 三条硬规则) |
| `.claude/agents/refine-{executor,reviewer,fixer}.md` | 3 sub-agent |
| `doc/dev/methodology/refine-loop.md` | 完整方法论 |
| `doc/dev/refine/<Seg>.{proposal,review}.md` | 每段留痕 |
| `tools/asm-regen/split_manifest.tsv` | 25 文件地址边界 (本表来源) |
| `output/2343.gba` SHA1 == 9689337d… | byte-identical 红线 |

**上次更新**: 2026-06-07 (00 文件 Seg-6b 完成: 23 fn render/cursor/load_assets + carve F/G/H + 10 EQ + 31 REF + 23 RENAME + §5.1 0x186ce/0x22; byte-identical 9689337d)。
