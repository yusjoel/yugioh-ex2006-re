# refine-progress — asm/ 25 模块细化总进度

> **总目标**: `asm/` 下 25 个反汇编模块 (`NN_*.s`, 覆盖 ROM 0x080000c0..0x084c7637) **全部内部细化完成**——
> 消灭 `DAT_/DWORD_/UNK_/PTR_DAT_` 自动名 + `ROM_INCBIN`/`.byte` 未分化块, 立即数符号化, 注释订正,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> **驱动**: skill `refine-loop` + 3 sub-agent (`refine-{executor,reviewer,fixer}`)。方法论
> `doc/dev/methodology/refine-loop.md`。这是 refine-loop 的**跨文件状态镜像** (类比 analysis-loop 的
> `eval/PROGRESS.md`)。
>
> **当前文件**: `07_equip_effect_chain.s` (0x0805c2f0..0x080643e0; 已拆 Seg-1..10 (339 named fn / ~516 槽 / 35 ROM_INCBIN / 0 switchD), 见活动 doc §五)。
> **下一任务**: file 07 Seg-2 0x5cfec..0x5e358 (~34 fn, ~83 槽; 2 ROM_INCBIN 0x5dd3e/1a 0x5ddda/d2; check_spell_zone_effect_activatable + spell/zone 效果谓词簇)。

上次更新: 2026-06-14 **file 07 Seg-1 完成** (EQ=54/REF=3/RENAME=9/PLATE=0; disasm=4 blocks/5 new fn; card_info.inc +11 CID (SANGA_OF_THUNDER/SCAPEGOAT/GRACEFUL_CHARITY/GREENKAPPA/REAPER_OF_CARDS/HARPIES_FEATHER_DUSTER/DRIVING_SNOW/NOBLEMAN_EXTERMINATION/BAIT_DOLL/cid_131c/cid_12fb); CSV +5 rows; §5.1 +1 (0x5c4aa/0x2a); byte-identical 9689337d; 下一任务 Seg-2 0x5cfec..0x5e358). **file 06 Seg-9 完成** (EQ=140/REF=1/RENAME=5/PLATE=7; disasm=2 blocks/6 new fn (tick_bonding_or_photon_activation_seq + 5 state handlers); card_info.inc +23 (SPECIAL_EQUIP_SENTINEL_ID/ZONE_STATUS_MASK/SPECIAL_EQUIP_TARGET_CID_A + 20 CID); CSV +6 rows; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d; 下一任务 file 06 Seg-10 0x5b480..0x5c2f0). **file 06 Seg-8 完成** (EQ=93/REF=21/RENAME=17/PLATE=3; disasm=4 blocks/13 new fn; card_info.inc +1 ABYSS_SOLDIER_CID / duel_field.inc +1 OP31_EFFECT_NODE_COUNT_CODE; CSV +13 rows + 2 updates; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; byte-identical 9689337d). **file 06 Seg-7 完成** (EQ=53/REF=5/PLATE=4; card_info.inc +1 CRIMSON_NINJA_CID / ewram.inc +1 LP_BANISHER_CTX_OFF / duel_field.inc +1 EQUIP_ACTIVE_CTX_OFF; 4 CJK plate 全段 ASCII 重写 + 1 stale FUN_ 订正; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-6 完成** (disasm=3 ranges/6 new fn; EQ=86/REF=5/RENAME=28/FUNC_RENAME=1/PLATE_SET=2; duel_field.inc +2 / card_info.inc +2; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; CSV +6 rows + 1 update; byte-identical 9689337d). **file 06 Seg-5 完成** (EQ=94/REF=23/PLATE_SET=5/PLATE_SUB=1; card_info.inc +7 CID / duel_field.inc +3 scalar; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-4 完成** (EQ=145/REF=5/RENAME=3/PLATE_SUBS=2/PLATE_SET=2; card_info.inc +55 CID; duel_field.inc +4 structural+22 score labels; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-3 完成** (disasm=1 ROM_INCBIN 0x55188/0x34 -> check_zone_slot_occupied_with_clear_equip_flag; EQ=44/REF=1; 0 new constants (全复用 ewram.inc); fn-ptr fix asm/03 x4 + asm/04 x3 + asm/05 x6 + asm/06 x1; CSV +1; byte-identical 9689337d). **file 06 Seg-2 完成** (disasm=1 ROM_INCBIN 0x54614/0x48 -> check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight; EQ=52/PLATE=1; card_info.inc +5 CID+pattern / duel_field.inc +1 offset; CSV +1; fn-ptr fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 06 Seg-1 完成** (EQ=45/REF=1/RENAME=1/PLATE=3; card_info.inc +1 GRAVEKEEPERS_CANNONHOLDER_CID; ewram.inc +2 EQUIP_CTX_PLAYER_OFF/SLOT_REF_OFF; fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d, commit f3bb6a9). **file 05 Seg-10 完成 (file 05 全 10 段完成 ✅)** (EQ=51/EOL=10/PLATE=2rewrites; card_info.inc +2 (BOTTOMLESS_TRAP_HOLE_CID/FIELD5_SCORE_THRESHOLD_1499); fn-ptr periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 05 Seg-9 完成** (EQ=112/RENAME=5/PLATE=2subs; card_info.inc +27 CID (SUMMONED_SKULL/RED_EYES_B_DRAGON/MULTIPLY/GRACEFUL_DICE/SHADOW_TAMER/DRAGON_MANIPULATOR/WINGBEAT_GIANT_DRAGON/INSECT_IMITATION/LIMITER_REMOVAL/CATHEDRAL_OF_NOBLES/PYRAMID_ENERGY/METAMORPHOSIS/FORMATION_UNION/KNIGHTS_TITLE/TERRORKING_ARCHFIEND/ULTRA_EVOLUTION_PILL/ORDER_TO_CHARGE/ORDER_TO_SMASH/BIG_WAVE_SMALL_WAVE/DOUBLE_ATTACK/KAMINOTE_BLOW/MINEFIELD_ERUPTION/TRANSCENDENT_WINGS/SPIRITUAL_EARTH_ART/ELEMENTAL_HERO_TEMPEST/HERO_HEART/PHOTON_GENERATOR_UNIT); fn-ptr periodic fix asm/03 x4 + asm/04 x4; byte-identical 9689337d). **file 05 Seg-8 完成** (EQ=75/REF=1/FNPTR=6/RENAME=1/PLATE=4subs; card_info.inc +11 CID+1 threshold / ewram.inc +1 / duel_field.inc +3; §5.1 +1; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/05 x6; byte-identical 9689337d). **file 05 Seg-7 完成** (EQ=69/REF=0/RENAME=3/PLATE=4subs; card_info.inc +22 CID (18 named + 4 unallocated); fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3; byte-identical 9689337d). **file 05 Seg-6 完成** (EQ=129/REF=2/RENAME=2/PLATE=13; ewram.inc +8 / card_info.inc +36 CID+1 / 5 disasm regions (Block1 13 stubs + Block2 12 stubs + RegA 3 + RegC 4 + RegD 2) / 138 literal pool DWORD fixes; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-5 完成** (EQ=67/REF=0/RENAME=8/PLATE=0; card_info.inc +7 CID / oam_attr.inc +2 / ewram.inc +9; §5.1 +3 orphan blocks (0x4c734/0x38, 0x4cca2/0xea, 0x4cdac/0x2c); byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-4b 完成** (EQ=89/RENAME=10/FUNC_RENAME=0/PLATE=1; card_info.inc +57 new CID; §5.1 +1 orphan 0x4becc/0x54; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3; Seg-4 全完成 4a+4b). **file 05 Seg-4a 完成** (EQ=95/RENAME=6/SCALAR_EQ=5; card_info.inc +68 (63 B-class CID + 3 inline CID + 2 field6 type); byte-identical 9689337d; no carve/disasm; commit 3155175). **file 05 Seg-3 完成** (EQ=87/REF=2/RENAME=3/FUNC_RENAME=1/PLATE=7; card_info.inc +50 CID; 3 disasm blocks → 5 new THUMB fn; FixF05Seg3SplitLiteralPools (20 DWORD forced) + FixF05Seg3BlockCStubTable (switch table + inline stub); byte-identical 9689337d; fn-ptr +1 periodic fix asm/04 x3; commit bd9ce13). **file 05 Seg-2 完成** (EQ=33/REF=1/card_id_EQ=34/PLATE=4subs; ewram.inc +2 + duel_field.inc +2 + oam_attr.inc +2 + card_info.inc +5; §5.1 +1 orphan 0x4aa5e/0xee; byte-identical 9689337d; fn-ptr +1 periodic fix asm/03 x4 + asm/04 x3). **file 05 Seg-1 完成** (EQ=99/REF=14/RENAME=39/PLATE=33; card_info.inc +16 CID + oam_attr.inc +21; byte-identical 9689337d; fn-ptr +1 periodic fix 7 slots). file 04 全 10 段完成 ✅ (Seg-10: EQ=87/REF=25/PLATE=8fn; 新建 oam_attr x10 + card_info x26 + duel_field x2; byte-identical 9689337d, commit cb54638)。

---

## 一、25 文件总表

| # | 文件 | 地址区间 | 段(~10/文件) | 状态 | 活动 doc |
|---|------|----------|------|------|---------|
| 00 | system_str_vija | 0x080000c0..0x0801cb00 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-00-system-str-vija.md` |
| 01 | vija_scene_text | 0x0801cb00..0x0802c238 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-01-vija-scene-text.md` |
| 02 | text_lp_fieldspell | 0x0802c238..0x08035f54 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-02-text-lp-fieldspell.md` |
| 03 | equip_chain_hand | 0x08035f54..0x0804020c | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-03-equip-chain-hand.md` |
| 04 | card_zone_sprite | 0x0804020c..0x08049014 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-04-card-zone-sprite.md` |
| 05 | equip_eligibility_a | 0x08049014..0x080537c0 | Seg-1..10 全完成 | ✅ 全 10 段完成 | `doc/dev/p5-refine-05-equip-eligibility-a.md` |
| 06 | equip_eligibility_b | 0x080537c0..0x0805c2f0 | Seg-1..10 已拆 | ✅ 全 10 段完成 | `doc/dev/p5-refine-06-equip-eligibility-b.md` |
| 07 | equip_effect_chain | 0x0805c2f0..0x080643e0 | Seg-1..10 已拆 | 🟡 进行中 (1/10) | `doc/dev/p5-refine-07-equip-effect-chain.md` |
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
| 6b | 0x17e48..0x18774 (23 fn, carve F/G/H, §5.1 0x186ce/0x22) | ✅ | 67862bf |
| 7 | 0x18774..0x19a58 (28 fn, carve J/K + §5.1 0x19640/0x20) | ✅ | (this session) |
| **8** | **0x19a58..0x1a794 (28 fn, banlist password 渲染簇)** | **✅** | (this session) |
| **9** | **0x1a794..0x1b850 (banlist/shuen 28fn + carve 1/2/3 + disasm block B + §5.1 block A)** | **✅** | (this session) |
| **10** | **0x1b850..0x1cb00 (vija/shuen 场景 tick, 32fn)** | **✅** | (see active doc §四.4.0ab) |

00 文件完整路线图 (段范围 / ROM_INCBIN / 旧覆盖) 见其活动 doc §五。
00 文件 §5.1 未引用登记: 0x14e54 / 0x14f9c / 0x1547e / 0x1550a / 0x156ec / 0x15d18 / 0x15fe8 /
0x16074 / 0x169d6+0x16a20 / 0x17424 / 0x186ce / 0x19640 / **0x1a89c** (孤儿 dead-code, 引用到时再 R4 disasm)。

### file 06 段进度 (equip_eligibility_b, 进行中)

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| 1 | 0x537c0..0x541cc (22 fn, 47 槽) | ✅ | f3bb6a9 |
| 2 | 0x541cc..0x54ba0 (22 fn, 50 槽, ROM_INCBIN 0x54614/0x48) | ✅ | 6c90482 |
| 3 | 0x54ba0..0x55440 (22 fn, 43 槽, ROM_INCBIN 0x55188/0x34) | ✅ | aee415f |
| 4 | 0x55440..0x565e8 (22 fn, 149 槽) | ✅ | fd8e6b6 |
| 5 | 0x565e8..0x57458 (22 fn, 101 槽) | ✅ | 3177750 |
| 6 | 0x57458..0x58550 (22 fn, 99 槽, ROM_INCBIN x2) | ✅ | 51ebd37 |
| 7 | 0x58550..0x58cec (22 fn, 58 槽) | ✅ | 8fd1210 |
| 8 | 0x58cec..0x59de0 (22 fn+13 new, 107 槽, ROM_INCBIN x2 + switchD) | ✅ | 11c409d |
| 9 | 0x59de0..0x5b480 (22 fn+6 new, 140 槽, ROM_INCBIN x2) | ✅ | 8c4bd9a |
| 10 | 0x5b480..0x5c2f0 (15 fn, 69 槽, switchD x2) | ✅ | c71149a |

**Seg-10 完成**: vija/shuen 32fn 全符号化, gVijaState 新全局, BG3HOFS plate 订正, CJK plate/EOL ASCII 转换; DWORD_SLOTS 永久修复 literal pool label 丢失问题; byte-identical 9689337d; file 00 全 10 段完成 ✅。

**Seg-9 完成**: Seg-8 executor proposal 越界预析已复用, Seg-9 全部落地:
- Block A (0x1a89c/0x20): §5.1 候选 (thumb=0; raw=1 偶合 0x08af5768 压缩 FS 资产)
- Block B (0x1ad18/0xec): R4 disasm 5 stubs (dispatch_banlist_cursor_action MOV PC,R0 跳转表目标)
- banlist_pass_ext_char_group carve (@0x09e3be3c, 代码引用 DWORD_0801abb0 in Seg-9)
- 越界 EQ 4槽: advance/retreat_banlist_password_cursor_slot_ewram_base/gsettings_offset
- 越界 RENAME 18槽: advance/retreat_banlist_password_cursor_slot_dir_field_off + load_banlist_char_by_cursor_slot_*/get_banlist_scroll_pixel_offset_*/get_banlist_password_entry_ptr_*/render_banlist_*/advance/retreat_banlist_pw_char_and_render_* 族
- 越界 REF 10槽: 7x gBanlistPasswordBuffer (Seg-9 fn) + 3x carve (char_candidate_str/alt_char/ext_char_group)

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

**上次更新**: 2026-06-14 (file 06 Seg-10 完成: EQ=56/REF=12/RENAME=13/PLATE_SUB=5; carve=0/disasm=0; card_info.inc +7 CID + duel_field.inc +1 scalar; fn-ptr periodic fix asm/03 x4 + asm/04 x3 + asm/06 x1; byte-identical 9689337d; **file 06 全 10 段完成 ✅**; 下一任务 file 07 bootstrap 0x0805c2f0..0x080643e0)。
