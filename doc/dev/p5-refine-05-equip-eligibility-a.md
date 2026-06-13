# 函数/数据细化计划 — `asm/05_equip_eligibility_a.s`

> 阶段目标: 把 `asm/05_equip_eligibility_a.s` (ROM `0x08049014 ~ 0x080537C0`, 装备槽资格检查
> `check_equip_slot_eligible_*` 簇 + 效果区 LP/shape sprite 提交 + 卡字段查询 + switch 派发)
> **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **6** 个文件 (file 00 / 01 / 02 / 03 / 04 已全 10 段完成, 见对应
> `p5-refine-0N-*.md`)。方法论 + R1-R9 细化清单 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..04 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**R1-R9 详版**见 `doc/dev/p5-refine-00-system-str-vija.md` §一。

**跨文件踩坑沿用** (file 00..04 沉淀, 务必遵守):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式) — memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
- **槽地址精确性 (file 04 Seg-6/8 教训)**: 每个 DAT_/PTR_ 槽地址必须用 python
  `struct.unpack_from('<I', rom, rom_addr-0x08000000)` 核对 ROM 字节值; executor 自报地址常有错,
  fixer 物化前 dry-run 暴露 WARN 即修正地址再实跑。
- **C5 按值去重不分语义域**: 新建常量前必扫全 constants/*.inc 确认无同值常量
  (file 04 反复抓到 UMI/ZOMBYRA/SPELL_ZONE_TARGET/RAGING_FLAME/TYRANT_DRAGON 等碰撞);
  REF/RENAME 不绕过已存在常量值; 不建孤儿常量 (段内无槽持该值)。
- **C13 残留 100% 覆盖**: 段内所有 DAT_/DWORD_/PTR_ 须被 EQ+REF+RENAME 去重全覆盖; executor 必
  python 精确清点段内 .word 槽总数 (file 04 反复漏数), 勿留"低优先级不处理"。
- **C8 stale 函数名**: plate 中 `FUN_xxxx`/`PTR_FUN_xxxx` **完整字符串**匹配替换现名 (禁子串);
  **含 CJK 全文的旧 plate 必须整段 ASCII 重写** (substring 替换对 CJK plate 静默 no-op, file 04 Seg-5/6 踩坑);
  整段 setPlateComment 重写, 落地后 grep 段范围 FUN_ == 0 + 无 CJK 验收。
- **卡牌 ID 常量 (file 02/03/04 教训)**: 命名前必查 `data/card-stats.s` 坐实 passcode→slot_id→卡名;
  slot_id 范围内未分配的值 → 中性 `<func>_cid_<hex>` 低置信 RENAME, 勿臆造卡名 (红线 3); pw 注释取正确 passcode;
  plate 卡名与 card-stats.s 矛盾即**命名期误名信号** (file 04 Seg-9 订正 0x1814 All-Seeing→Silent Swordsman LV5)。
- **packed/bitfield 值部分解码**: 单个 packed 32-bit 值语义不明 → 中性 RENAME 标签 + med/low-conf EOL
  记录字节分解 (high16/low16), **不臆造完整位域语义, 不 BLOCK 整段** (file 04 Seg-8a/10 范式)。
- **switch 跳转表 (file 05 新特征)**: 段内 `switchD_*`/`switchdataD_*` Ghidra 自动名是 switch 派发数据块;
  jump table 目标存裸 THUMB 地址 (R4 disasm 跳转表逐 stub) 或字节偏移表; carve/disasm 处理参 file 00 Seg-5c。
- **fn-ptr +1 永久踩坑**: Ghidra 把 THUMB fn-ptr 数据 ref 导出为偶地址, build diff 差 1 字节; 手改 `.word <fn>+1`。
  每次 re-export 后须重补。已知周期性修复槽 (跨文件累积):
  asm/03: 0x37884 / 0x389dc / 0x389f8 / 0x3aa74;
  asm/04: 0x40ab4 (zone_monster_field_bonus_table+7*16) / 0x42638 (tick_draw_card_switch_table) /
          0x45efc (apply_nitro_unit_equip_activation+1) / 0x478f0 (gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF)。
  file 05 若出现新 fn-ptr 槽同样处理。
- 复用 file 00..04 已建 constants/*.inc 与 carve label (见下方资产清单)。

**file 02/03/04 已建可复用资产** (新建前必 grep 确认无同值):
- `ewram.inc`: gDuelFieldSlots=0x0201c510 / gEquipNodePool=0x0201d9c0 / gEquipChainSlotRefs /
  gDuelFieldSlotState / gDuelEffectChainSlots=0x0201bcc0 / PLAYER_BLOCK_STRIDE=0x868 /
  gP1SlotCountBase / gP1SlotSetCodeArray / gP1HandCountBase / gP1HandSlotArray /
  gDuelFieldSlots_p2_base=0x0201c5d8 / gDuelFieldSpellZoneBase=0x0201c5ec / gP1FieldArrayCBase=0x0201c600 /
  gEffectEntryArray=0x0201b590 / gDuelDisplaySeqState=0x0201bcc0 / gSpriteAttrBuf=0x0201b870 /
  gDuelChainStepCounter=0x0201c4d0 / gDuelChainDescBase=0x0201c4d8 / gDuelCardCtxBase=0x0201e2a0 /
  gEquipChainEntryBase=0x0201e288 / gEquipZoneCountTable=0x0201e1c8 / P1LP_BACKUP_DST_OFF=0x1cf0 /
  LP_CARD_TRACK_BASE_OFF=0x1da8 / LP_CARD_TRACK_NEXT_OFF=0x1daa / LP_CARD_TRACK_AUX_OFF=0x1db2 /
  P1LP_EQUIP_BITMAP_CTR_OFF=0x1d3c / LP_DISCARD_ZONE_OFF
- `duel_field.inc`: 众多 *_OFF 字段偏移 + SLOT_*_CLR 位清除掩码 (file 02/03/04 累积 ~80+ 项);
  EQUIP_MAIN_PHASE_OFF=0x1d18 / DISP_SET_VARIANT_OFF=0x1cfc / SET_DISPLAY_STATE_SLOT_OFF=0x894 /
  HAND_SLOT_FACE_ARRAY_OFF=0x41a / ALT_HAND_SLOT_FACE_ARRAY_OFF=0x5d2 / EQUIP_CHAIN_STEP_BASE_OFF /
  EQUIP_MULTI_SLOT_CTL_OFF=0x1ce0 / EQUIP_CHAIN_SENTINEL=0xffff0000 / EQUIP_BITMAP_CTRL_OFF /
  FIELD_COPY_COUNT_FLAG=0x10002 / EQUIP_ZONE_EFFECT_ATTR_OR=0x1e501511 (file 04 Seg-10 low-conf) /
  EQUIP_SLOT_ACTIVE_TAG=0xa5600000 / FIELD_SLOT_COUNT_OFF=0x1cb4 / SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 等
- `card_info.inc`: SLOT_CARD_SET_CODE_MASK=0x00001fff + file 01..04 已建 **~250+ CID 常量**
  (复用前必 grep card_info.inc; file 04 单文件新增 ~130 CID)
- `oam_attr.inc`: OAM_ATTR0_HIDDEN=0x0000ffff / OAM_ATTR1_X_CLEAR / OAM_ATTR2_TILE_CLEAR=0xffffe000 /
  众多 OAM_*_SPRITE_P1/P2 调色板选择子 (0x80xx 系列, file 04 累积 ~30 项) /
  OAM_SPRITE_ATTR_CLR_BIT* / OAM_SPRITE_ATTR_CLR_BITS* 位清除掩码 (file 04 累积)
- `bitops.inc`: 8 POPCOUNT_MASK_*
- 全局: gVijaState=0x02029eb0 / gDemoState=0x02029ec0 / gDuelSceneBase=0x02023360 /
  gDuelCardCtxBase=0x0201e2a0 / gDuelDispCtx=0x0203eeb0
- 跨文件 caller hub: `dispatch_duel_event_display_seq` (0x0803be4c, file 03 Seg-7) — tick_*_display_seq 的 bl 目标 + plate 引用 (C8 高频)。

---

## 二、落地工作流 (pipeline)

同 file 00..04 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF05Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。
重段 (>~150 槽) 按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (05_equip_eligibility_a.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------------|------|--------|
| 1 | 0x49014..0x4a5b8 | 24 | 152 | — | ✅ | 6dd6fec |
| 2 | 0x4a5b8..0x4ad48 | 24 | 68 | — | ✅ | 68c1e28 |
| 3 | 0x4ad48..0x4b4f4 | 24 | 73 | — | ⬜ | — |
| 4 | 0x4b4f4..0x4c6e8 | 24 | 200 | — | ⬜ | — |
| 5 | 0x4c6e8..0x4d124 | 24 | 65 | — | ⬜ | — |
| 6 | 0x4d124..0x4ffba | 24 | 128 | — | ⬜ | — |
| 7 | 0x4ffba..0x50e40 | 24 | 73 | — | ⬜ | — |
| 8 | 0x50e40..0x51cc4 | 24 | 83 | — | ⬜ | — |
| 9 | 0x51cc4..0x52df8 | 24 | 117 | — | ⬜ | — |
| 10 | 0x52df8..0x537c0 | 23 | 51 | — | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
重段提示: Seg-4 (200 槽, switch 派发 + check_card_is_equip_set 簇) / Seg-1 (152 槽, sprite 提交簇) /
Seg-6 (128 槽) / Seg-9 (117 槽) 较重, 必要时拆 Seg-Na/Nb (地址序边界=函数结束处, 不回头)。
switchD_/switchdataD_ 自动名 (Seg-2/4/5/6 含) 是 switch 派发数据块, 按 file 00 Seg-5c R4 disasm 范式处理。

---

## 四、逐段完成记录

(各段落地后由 fixer 追加 4.0N 小节: 函数列表 / 符号化统计 / 新建 constants / carve / 踩坑 / commit)

### 4.01 Seg-1 完成记录 (0x08049014..0x0804a5b8, 24 fn, 152 slots)

**函数列表 (24)**:
submit_effect_zone_lp_and_shape_sprites / tick_duel_field_zone_sprite_update_pipeline /
tick_zone_sprite_pipeline_with_update_flag / enqueue_slot_sprite_attr_by_player /
enqueue_equip_zone_sprite_attr_full / render_spell_zone_card_sprite_with_id_tree /
render_pair_zone_sprites_if_field_card_present / render_spell_zone_sprite_with_field_copy_check /
render_matched_pair_zone_sprites / enqueue_equip_zone_sprite_with_mode /
enqueue_pair_zone_sprite_attr_by_card_id / enqueue_effect_slot_sprites_descending /
enqueue_equip_slot_sprite_with_card_check / submit_equip_slot_sprite_zone11 /
enqueue_equip_slot_sprite_zone13 / enqueue_equip_slot_sprite_zone12 /
render_monster_slot_card_with_lp_bar / enqueue_sprite_attr_type11 /
enqueue_sprite_attr_with_type_select / check_zone_eligible_with_deck_flag /
enqueue_lp_field_state_sprite_by_player / enqueue_lp_counter_sprite_by_player /
enqueue_duel_field_card_slot_sprite / enqueue_sprite_attr_for_card_slot

**符号化统计**: EQ=99 / REF=14 / RENAME=39 / FUNC_RENAME=0 / PLATE=33 fn_subs

**新建 constants**:
- card_info.inc +16 CID (PENGUIN_KNIGHT / BAD_REACTION_TO_SIMOCHI / HIROS_SHADOW_SCOUT /
  CRUSH_CARD / APPROPRIATE / PROTECTOR_OF_THE_SANCTUARY / HEART_OF_THE_UNDERDOG /
  REGENERATING_MUMMY / GREED / PETEN_THE_DARK_CLOWN / DECK_DEVASTATION_VIRUS /
  PIKERU_SECOND_SIGHT / CYBER_ARCHFIEND / BUBBLE_ILLUSION / DANDYLION / KAISER_GLIDER)
- oam_attr.inc +21 (10 P1/P2 tile attr0 pairs + OAM_CARD_SLOT_SPRITE + 3 CLR masks + 4 ATTR2_OR)

**carve**: 0 (no ROM_INCBIN in this segment)

**踩坑**: fn-ptr +1 periodic fix (7 slots in asm/03 x4 + asm/04 x3) after re-export; all recovered

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**plate FUN_ residual**: 4 instances remain in plates; all are cross-references to functions in
other segments (0x08073d84, 0x0806d960, 0x08049e44, 0x080718c4) not in Seg-1 mapping list;
will be resolved when those segments are refined.

**commit**: 6dd6fec

### 4.02 Seg-2 完成记录 (0x0804a5b8..0x0804ad48, 12 fn, 68 slots)

**函数列表 (12)**:
enqueue_monster_zone_equip_sprites_and_lp_counters /
enqueue_sprite_attr_type10_halfword /
increment_lp_bar_display_counter /
increment_lp_bar_counter_no_player /
decrement_lp_bar_display_counter /
set_slot_occupy_bit_with_sprite_update /
set_player_state_bit_with_sprite_update /
set_field_slot_bit_with_sprite_update /
map_field8_to_card_type_category (contains switchD_0804a9ee) /
check_card_pair_allowed /
map_card_id_to_banlist_canonical /
check_card_ids_banlist_compatible

**符号化统计**: EQ=33 / REF=1 / card_id_EQ=34 / FUNC_RENAME=0 / PLATE=4 subs (3 fn)

**新建 constants**:
- ewram.inc +2 (LP_BAR_DISPLAY_CTR_OFF=0x4c4 / LP_BAR_ANIM_STATE_OFF=0x4cc)
- duel_field.inc +2 (EQUIP_SPRITE_X_DELTA_A=0xffffe730 / EQUIP_SPRITE_X_DELTA_B=0xffffe32c)
- oam_attr.inc +2 (OAM_PLAYER_STATE_BIT_SPRITE_P1=0x8022 / OAM_FIELD_SLOT_BIT_SPRITE_P1=0x802a)
- card_info.inc +5 (POLYMERIZATION_CID_1303 / CYBER_HARPIE_LADY_CID / HARPIE_LADY_1_CID / HARPIE_LADY_3_CID / BEWD_RANGE_CHECK_BIAS)

**carve**: 0 (no fn-ptr ROM_INCBIN in this segment; §5.1 orphan block 0x4aa5e/0xee)

**plate FUN_ residual after landing**: 0 stale FUN_ in Seg-2 range (grep confirmed)

**踩坑**: fn-ptr +1 periodic fix -- asm/03 x4 (eval_equip_bonus_for_slot_pred_fn / eval_amazoness_fnptr_a / eval_amazoness_fnptr_b / eval_equip_chain_pred_fnptr) + asm/04 x3 (tick_equip_scan_destiny_chain_table now +7*16 / dat_08045efc_fnptr +1 / upd_equip_bitmap_effect_zone gP1LifePoints+EQUIP_BITMAP_CTRL_OFF fix) after re-export

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**commit**: 68c1e28

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 05 范围 `[0x08049014, 0x080537c0)` (239 named fn, 1010 DAT_/DWORD_/PTR_ 槽,
> **0 ROM_INCBIN/inter-function 数据块** — 文件全为代码 + 函数内 literal pool +
> switchD/switchdataD 函数内跳转表) 按**函数数**均分 10 段 (~24 fn/段, 边界=函数结束处=下一函数起点)。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x49014..0x4a5b8 | 24 | 152 | — | 效果区 LP/shape sprite 提交 + equip slot sprite + monster zone equip sprite/lp counter 簇 |
| Seg-2 | 0x4a5b8..0x4ad48 | 24 | 68 | — | monster zone equip sprite 尾 + switchD_0804a9ee 派发 + card field5 查询簇头 |
| Seg-3 | 0x4ad48..0x4b4f4 | 24 | 73 | — | card 字段查询 (field5/field8/stat) 谓词簇 + summon restriction 查询头 |
| Seg-4 | 0x4b4f4..0x4c6e8 | 24 | 200 | — | 重: get_card_field_summon_restriction + check_card_is_equip_set 簇 + switchD_0804c6dc 大型派发表 |
| Seg-5 | 0x4c6e8..0x4d124 | 24 | 65 | — | switchdataD_0804c6e8 跳转表 + slot card sprite row packed 提交簇 |
| Seg-6 | 0x4d124..0x4ffba | 24 | 128 | — | switchD_0804ce98 派发 + check_equip_slot_eligible_with_owner_and_type 资格检查簇头 |
| Seg-7 | 0x4ffba..0x50e40 | 24 | 73 | — | check_slot_zone_bit3 + eligible_type_and_card_match 资格检查簇 |
| Seg-8 | 0x50e40..0x51cc4 | 24 | 83 | — | eligible_with_whitelist_prereqs + by_opposite_side_and_prereqs 资格检查簇 |
| Seg-9 | 0x51cc4..0x52df8 | 24 | 117 | — | eligible_by_card_id_bst_and_pairs + dispatch_alt 大型 card_id 资格分发簇 |
| Seg-10 | 0x52df8..0x537c0 | 23 | 51 | — | eligible_by_prereqs_and_active_player_match + by_owner_mismatch 资格检查簇 (文件末) |

执行约定同 file 00..04: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |
| 0x0804aa5e | 0xee (238B) | Seg-2 | 孤立 THUMB 代码块 (BST 比较器形态, 与 check_card_pair_allowed 结构相似但独立); 全 ROM raw=0 fn-ptr 及 THUMB+1=0 (2B step exhaustive scan, reviewer 独立确认) | defer |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-04-card-zone-sprite.md` (file 04 完整记录, card_info.inc CID 批量沉淀 / oam_attr P1/P2 / packed 值 / 重段 8a/8b 拆分 / fn-ptr +1 踩坑)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
