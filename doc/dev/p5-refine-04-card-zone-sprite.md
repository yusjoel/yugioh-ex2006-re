# 函数/数据细化计划 — `asm/04_card_zone_sprite.s`

> 阶段目标: 把 `asm/04_card_zone_sprite.s` (ROM `0x0804020C ~ 0x08049014`, 卡牌显示序列
> tick 簇 + 区域卡 sprite attr 入队 + 装备 slot/链 sprite + equip target bitmap 计算)
> **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **5** 个文件 (file 00 / 01 / 02 / 03 已全 10 段完成, 见对应
> `p5-refine-00-system-str-vija.md` / `p5-refine-01-vija-scene-text.md` /
> `p5-refine-02-text-lp-fieldspell.md` / `p5-refine-03-equip-chain-hand.md`)。方法论 +
> R1-R9 细化清单 + 三条硬规则见 `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00/01/02/03 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**R1-R9 详版**见 `doc/dev/p5-refine-00-system-str-vija.md` §一。

**跨文件踩坑沿用** (file 00/01/02/03 沉淀):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式; 否则 GAS PC-relative
  "value too big") — 见 memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
  (proposal/review markdown 文档可中文, 仅写入 Ghidra .rep 的 plate/EOL 须 ASCII)
- carve byte-identical: host incbin 覆盖等式 `sum(spans)==原 size`; THUMB fn-ptr 表 `.word <fn>+1`,
  数据指针/slot-index 表不 +1; `.asciz` 须含 NUL+对齐 pad; .hword RGB15 注意 bit15。
- **executor 严守段上界** (reviewer C1 逐槽地址裁定)。
- **C5 按值去重不分语义域**: 新建常量前必扫全 constants/*.inc 确认无同值常量;
  REF/RENAME 不得绕过已存在常量值; 不建孤儿常量 (段内无槽持该值)。
- **C13 残留 100% 覆盖**: 段内 incbin 块外所有 DAT_/DWORD_/PTR_ 净数须被 EQ+REF+RENAME 去重全覆盖,
  勿留"低优先级不处理"。
- **C8 stale 函数名**: plate 中 `FUN_xxxx`/`PTR_FUN_xxxx` **完整字符串**匹配替换现名 (禁子串匹配);
  整段 setPlateComment 重写, 落地后 grep 段范围 FUN_ == 0 验收。
- **R4 大块 disasm** (file 04 当前测绘无 ROM_INCBIN, 但若 re-export 暴露误标代码沿用): flow-disasm
  会把 literal pool 当 THUMB 解码 → reference-manager 扫 PC-relative ldr 目标 createDWord 一次性全覆盖;
  mov pc,r0 派发表存裸 THUMB 地址; 重跑前 clearListing 整 range 再 setTMode (避 ContextChangeException)。
- **卡牌 ID 常量 (file 02/03 教训)**: 命名前必查 `data/card-stats.s` passcode→slot_id 坐实
  card_id→卡名映射 (file 02 Seg-8 Yami/Sanctuary 误判, file 03 Seg-4b GOBLIN_KING/Solar Flare 边界
  经 card-stats.s 订正)。无对应卡 → 降级 `<func>_cid_<hex>` 低置信 RENAME, 勿臆造卡名 (触发红线 3)。
- **fn-ptr +1 永久踩坑 (file 03 沉淀, 跨文件)**: Ghidra 把 THUMB fn-ptr 数据 ref 导出为偶地址,
  build diff 差 1 字节; 手动改 `.word <fn>+1`。file 03 受影响槽 0x37884 / 0x3aa74 / 0x389dc / 0x389f8,
  每次 re-export 后须重补。file 04 若出现新 fn-ptr 槽同样处理。
- 复用 file 00/01/02/03 已建 constants/*.inc 与 carve label (见 §一末尾资产清单)。

**file 02/03 已建可复用资产** (新建前必 grep 确认无同值):
- `ewram.inc`: gDuelFieldSlots=0x0201c510 / gEquipNodePool / gEquipChainSlotRefs / gDuelFieldSlotState /
  gDuelEffectChainSlots=0x0201bc54 / PLAYER_BLOCK_STRIDE=0x868 / ZONE_CHAIN_CARD_ID_OFF=0x10e2 /
  gP1SlotCountBase / gP1SlotSetCodeArray / gP1HandCountBase / gP1HandSlotArray / gP1ChainZoneCountBase /
  gP1ChainZoneArray / gP1AltHandCountBase / gP1AltHandSlotArray / gP1ZoneHandCount /
  gDuelFieldSlots_p2_base=0x0201c5d8 / gDuelFieldSpellZoneBase=0x0201c5ec / gP1FieldArrayCBase=0x0201c600 /
  gEffectEntryArray=0x0201b590 / gDuelDisplaySeqState=0x0201bcc0 / gSpriteAttrBuf=0x0201b870 /
  gDuelChainStepCounter=0x0201c4d0 / gDuelChainDescBase=0x0201c4d8 / gDuelDisplaySeqStateAlt=0x0201bcc2 /
  gP1FieldState
- `duel_field.inc`: FIELD_SLOT_PHASE_MASK / EQUIP_NODE_BASE_OFFSET / NODE_POOL_NEG_OFFSET /
  EQUIP_CHAIN_LINK_OFFSET / FIELD_SLOT_COUNT_OFF=0x1cb4 / SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 /
  FIELD_SPELL_CARD_REF_OFF=0x1390 / DUEL_ACTIVE_PLAYER_OFF=0x1cb8 / EQUIP_SLOT_ACTIVE_TAG=0xa5600000 /
  EFFECT_ZONE_PARTITION_OFF=0x10a4 / EFFECT_ZONE_BITMASK_OFF=0x10d0 / ACTIVATION_STATE_A_OFF=0x1d48 /
  ACTIVATION_STATE_B_OFF=0x1d78 / ACTIVE_EFFECT_CATEGORY_OFF=0x10d8 / DISPLAY_SEQ_SLOT_IDX_OFF=0x808 /
  DISPLAY_SEQ_STEP_LOCK_OFF=0x80c / DISPLAY_SEQ_ACTIVE_PLAYER_OFF=0x1d10 / DISPATCH_ACTIVE_FLAG_OFF=0x1d38 /
  ACTIVATION_STATE_C_OFF=0x1d4c / SPRITE_ATTR_FIELD1_OFF=0x306 / SPRITE_ATTR_FIELD3_OFF=0x30a /
  EQUIP_CHAIN_STEP_OFF=0x1d28 / EQUIP_CHAIN_ACTIVE_OFF=0x1d2c / 众多 SLOT_*_CLR 位清除掩码 /
  DISP_SEQ_STEP_LOCK_A_OFF=0x80a / DISP_SEQ_ALT_CTR_OFF=0x80e / DISP_SEQ_CARD_SET_CTR_OFF=0x818 /
  DISPLAY_CTX_SLOT_DATA_MASK=0x7fff / SLOT_CHAIN_CTR_CLR=0xc03fffff / SLOT_BIT20_CLR=0xffefffff
- `card_info.inc`: SLOT_CARD_SET_CODE_MASK=0x00001fff / FIELD_SPELL_B_EFFECT_ID=0x1407 + file 01/02/03 已建
  众多 *_CARD_ID / *_CID / *_CID_SHIFTED (复用前必 grep card_info.inc; ~150+ CID 常量已沉淀)
- `oam_attr.inc`: OAM_ATTR0_HIDDEN / OAM_ATTR2_TILE_CLEAR=0xffffe000 / OAM_ATTR2_TILE_CLEAR (file 03 sprite 簇引用)
- `bitops.inc`: 8 POPCOUNT_MASK_*
- `field_spell_bonus.inc`: FIELD_SPELL_TABLE_IDX_BIAS / ZONE_EFFECT_ATK_PENALTY_500
- 全局: gVijaState=0x02029eb0 / gDemoState=0x02029ec0 / gDuelSceneBase=0x02023360 /
  gDuelCardCtxBase=0x0201e2a0 / gDuelDispCtx=0x0203eeb0
- 跨文件 caller hub: `dispatch_duel_event_display_seq` (0x0803be4c, file 03 Seg-7) — file 04 几乎所有
  tick_*_display_seq 函数都 bl 它且 plate 引用它; stale `FUN_0803be4c` → 此名 (C8 主战场, 参照 file 03
  Seg-7..10 PLATE breakdown)。

---

## 二、落地工作流 (pipeline)

同 file 00/01/02/03 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF04Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。

---

## 三、当前进度 (04_card_zone_sprite.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN | 状态 | commit |
|-----|------|-----|--------|-----------------|------|--------|
| 1 | 0x4020c..0x407fc | 19 | 64 | — | ✅ | (see §四.4.01) |
| 2 | 0x407fc..0x40c88 | 20 | 46 | — | ✅ | (see §四.4.02) |
| 3 | 0x40c88..0x417f0 | 19 | 98 | — | ✅ | (see §四.4.03) |
| 4 | 0x417f0..0x4308c | 19 | 159 | — | ✅ | (see §四.4.04) |
| 5 | 0x4308c..0x4394c | 19 | 48 | — | ✅ | (see §四.4.05) |
| 6 | 0x4394c..0x44674 | 20 | 69 | — | ⬜ | — |
| 7 | 0x44674..0x44e30 | 19 | 35 | — | ⬜ | — |
| 8 | 0x44e30..0x47990 | 19 | 275 | — | ⬜ | — |
| 9 | 0x47990..0x47ec0 | 20 | 14 | — | ⬜ | — |
| 10 | 0x47ec0..0x49014 | 19 | 112 | — | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
重段提示: Seg-8 (275 槽, dispatch_card_effect_sprite_render_by_card_id 等大型 card_id 分发 + equip
target bitmap 计算) / Seg-4 (159 槽, trigger_display_op36_seq 等大型 tick 簇) / Seg-10 (112 槽,
render_slot_card_sprite_* 描述符渲染) 较重, 必要时拆 Seg-Na/Nb (地址序边界=函数结束处, 不回头)。

---

## 四、逐段完成记录

(各段落地后由 fixer 追加 4.0N 小节: 函数列表 / 符号化统计 / 新建 constants / carve / 踩坑 / commit)

### 4.01 Seg-1 完成记录 (0x0804020c..0x080407fc)

**函数列表 (19)**:
tick_card_display_seq_op15 / tick_equip_preview_display_sequence / tick_set_display_mode_seq /
tick_lp_compare_init_display_seq / invoke_card_display_op_by_equip_mode /
invoke_card_display_op_equip_mode0..5 (6fn) /
commit_display_index_on_effect5 / tick_display_slot_flag_clear_seq /
advance_card_display_seq_counter / set_slot_facedown_bit_by_flag /
apply_card_flags_to_zone_bitmap / commit_field_slot_bit_with_display_op24 /
tick_card_effect_category_display_seq / tick_display_op40_seq

**符号化统计**: EQ=33 (28 reuse + 5 new) / REF=22 / RENAME=9 / PLATE=17 / carve=0 / disasm=0 / §5.1=0

**新建常量 (5, constants/duel_field.inc)**:
- DISP_SET_VARIANT_OFF=0x1cfc
- SET_DISPLAY_STATE_SLOT_OFF=0x894
- EQUIP_MAIN_PHASE_OFF=0x1d18
- HAND_SLOT_FACE_ARRAY_OFF=0x41a
- ALT_HAND_SLOT_FACE_ARRAY_OFF=0x5d2

**踩坑**: file 03 fn-ptr +1 再次需要补 (4 槽: 0x37884/0x389dc/0x389f8/0x3aa74;
check_level_conv_lab_node_match+1 x2, check_card_is_amazoness_type+1 x2)。
每次 re-export 必补，已固化到 asm/03_equip_chain_hand.s。

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.02 Seg-2 完成记录 (0x080407fc..0x08040c88)

**函数列表 (20)**:
tick_card_normal_summon_display_state / tick_flip_attack_display_state /
tick_random_draw_display_seq / tick_prng_advance_display_op38_seq /
tick_card_display_op3a_seq / tick_display_op39_seq / tick_card_display_seq_op3b /
tick_equip_slot_scan_display_sequence / tick_ui_effect_op3c_display_seq /
tick_card_display_op0b_seq / trigger_display_op36_seq /
clear_display_step_lock_i / clear_display_step_lock_j / clear_display_step_lock_k /
reset_card_display_seq_state / clear_match_state_field_at_80c /
clear_match_state_field_at_80c_alt / clear_display_step_counter_a /
clear_display_step_counter_b / clear_display_step_lock_a

**符号化统计**: EQ=44 (43 reuse + 1 new) / REF=1 / RENAME=1 / PLATE=15 / carve=0 / disasm=0 / §5.1=0

**新建常量 (1, constants/ewram.inc)**:
- P1LP_BACKUP_DST_OFF=0x1cf0 (after P1LP_TIMER_OFF line 244)

**REF 槽**:
- DAT_08040ab4 -> zone_monster_field_bonus_table+7*16 (0x09e3f104): Destiny Board + Spirit Message I/N/A/L card_id 表; 已 carved, 非新 carve

**PLATE**: 15 函数 plate 中 FUN_0803be4c/(0x0803be4c) -> dispatch_duel_event_display_seq; 含 2 种变体 (FUN_xxx 和 (0xxx)); 0 WARN (全命中)

**踩坑**: fn-ptr +1 槽 (0x37884/0x389dc/0x389f8/0x3aa74) 本次 re-export 后 SHA1 仍一致; GAS 已正确输出奇地址, 无需手补

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.03 Seg-3 完成记录 (0x08040c88..0x080417f0)

**函数列表 (19)**:
clear_display_step_lock_b/c/d/e/f/g/h (7) /
clear_card_display_state_flag /
tick_zone_slot_spell_remove_display_seq /
tick_field_clear_display_sequence /
tick_player_hand_shuffle_display_seq /
tick_card_lp_change_cycle_display_seq /
tick_find_slot_by_card_id_display_seq /
tick_card_change_position_display_state /
tick_zone_card_place_by_id_seq /
tick_card_id_zone_find_display_seq /
tick_spell_equip_zone_display_seq /
tick_card_display_op28_clear_seq /
tick_card_display_op2b_lp_clear_seq

**符号化统计**: EQ=87 (84 reuse + 3 new) / REF=0 / RENAME=0 / PLATE=18 / carve=0 / disasm=0 / §5.1=0

**新建常量 (3, constants/ewram.inc)** (inserted after P1LP_BACKUP_DST_OFF):
- LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card-ref tracking array base; 109 raw ROM refs
- LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] 5-entry hword clear loop base; 44 raw ROM refs
- LP_CARD_TRACK_AUX_OFF=0x1db2: [gP1LifePoints+0x1db2] auxiliary LP track field; 1 raw ROM ref

**PLATE**: 18 functions — 17x FUN_0803be4c -> dispatch_duel_event_display_seq;
1x (0x0803be4c) -> (dispatch_duel_event_display_seq) at tick_card_change_position_display_state.
Post-land grep: FUN_0803be4c=0, 0x0803be4c=0 in Seg-3 lines 1689-3366. Verified 0 WARNs.

**踩坑**: fn-ptr +1 再次需要补 (slots 0x37884/0x389dc/0x389f8/0x3aa74 in asm/03_*).
Re-export also lost zone_monster_field_bonus_table+7*16 offset at 0x08040ab4 (became plain base label);
補 +7*16 suffix 进 asm/04 line 1360.

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.04 Seg-4 完成记录 (0x080417f0..0x0804308c)

**函数列表 (19)**:
tick_zone_slot_ref_track_display_seq / tick_equip_attach_display_sequence /
tick_card_display_op3e_seq / tick_equip_zone_shuffle_display_seq /
tick_card_display_op43_seq / tick_zone_equip_link_placement_seq /
tick_card_flip_reveal_display_seq / tick_zone_card_relocate_display_seq /
tick_normal_summon_zone_placement_seq / tick_equip_chain_count_check_sequence /
tick_card_discard_display_seq / tick_draw_card_display_seq /
invoke_draw_display_seq_forward / invoke_draw_display_seq_reverse /
tick_display_op0d_with_lp_update_seq / reset_equip_chain_entry_by_player /
resolve_equip_target_slot_for_enqueue / dispatch_equip_chain_slot_scan_by_player /
enqueue_sprite_attr_with_mode

**符号化统计**: EQ=142 / REF=15 / RENAME=3 / PLATE=9 / carve=0 / disasm=0 / §5.1=0

**新建常量 (10 项)**:
- card_info.inc x6: POLYMERIZATION_CID(0x12e5) / RYU_SENSHI_CID(0x14c7) / FRONTIER_WISEMAN_CID(0x14ca) / VICTORY_D_CID(0x16ec) / BLUE_EYES_SHINING_DRAGON_CID(0x17c2) / RARE_METALMORPH_CID(0x184b)
- duel_field.inc x1: EQUIP_CHAIN_STEP_BASE_OFF(0x1130)
- ewram.inc x2: LP_DISCARD_ZONE_OFF(0x10dc) / gEquipChainEntryBase(0x0201e288)
- oam_attr.inc x1: OAM_SPRITE_PAL_P1(0x8036)

**复用 (无重建)**: TYRANT_DRAGON_CARD_ID / FIEND_SKULL_DRAGON_CID / SKULL_SERVANT_CID / SLOT_CARD_EMPTY / A_DEAL_WITH_DARK_RULER_CID / SOUL_ABSORPTION_CID / COST_DOWN_CID / EQUIP_SLOT_CARD_ID_RANGE_MAX / DISP_SET_VARIANT_OFF / SCROLLBAR_CLEAR_BITS_14_6 等

**BLOCKED 标签 (3)**: nsummon_cid_1672_080423e0 / draw_seq_cid_1729_08042780 / draw_seq_cid_1986_08042794 (not in card-stats.s; 中性形式)

**REF**: DAT_08042638 -> tick_draw_card_switch_table (0x0804263c, even addr, not THUMB+1); gEquipChainEntryBase NEW global; 12x PTR_gP1LifePoints

**PLATE**: 9 functions FUN_0803be4c -> dispatch_duel_event_display_seq; all [PFX] (0 WARN)

**踩坑**: fn-ptr +1 再次需要补 (slots 0x37884/0x389dc/0x389f8/0x3aa74 in asm/03, zone_monster_field_bonus_table+7*16 at 0x08040ab4 in asm/04); 补完后 SHA1 match.
Dry run found 2 address mismatches (0x08042e98/0x08042e9c swapped, 0x08042468 code not data, 0x08042828 code not data, 0x08042864/68 ptr+stride -> fixed to 0x0804286c).

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

**commit**: a62d2e2

---

### 4.05 Seg-5 完成记录 (0x0804308c..0x0804394c)

**函数列表 (19)**:
enqueue_slot_card_sprite_if_eligible / enqueue_equip_zone_sprite_attr_by_player /
enqueue_equip_chain_slot_sprite_attr / enqueue_sprite_attr_for_chain_node_check /
enqueue_equip_chain_all_slots_for_pair / enqueue_sprite_attr_for_chain_node_match /
enqueue_equip_chain_sprite_by_side / enqueue_zone_slot_sprite_attr_by_card_type /
enqueue_equip_set_slot_sprite_by_zone_col / enqueue_equip_slot_sprite_attr_by_state /
scan_equip_chain_list_for_sprite_update / enqueue_equip_chain_attrs_for_slot_range /
scan_equip_chain_list_by_player_slot / scan_equip_chain_by_slot_for_update /
enqueue_sprite_attrs_for_card_chain_list / enqueue_slot_bitmap_type_d_for_equip /
enqueue_slot_sprite_by_state_and_type / enqueue_slot_sprite_attr_by_card_type_and_state /
enqueue_zone_slot_sprite_attr_if_occupied

**符号化统计**: EQ=45 (31 reuse + 14 new) / REF=0 / RENAME=3 / PLATE=9 函数 (16 PLATE entries: 2 full ASCII rewrite + 14 substr) / carve=0 / disasm=0 / §5.1=0

**新建常量 (10)**:
- oam_attr.inc x8:
  - OAM_EQUIP_CHAIN_SPRITE_P1=0x8037 (equip chain node OAM attr0 P1; 11 ROM refs)
  - OAM_CHAIN_MATCH_SPRITE_P1=0x8038 (chain match OAM attr0 P1; 82 ROM refs)
  - OAM_ZONE_TYPE_SPRITE_P1=0x8042 (zone card-type OAM attr0 P1; 48 ROM refs)
  - OAM_ZONE_CARD_SPRITE_P1=0x8035 (zone occupied card OAM attr0 P1; 8 ROM refs)
  - OAM_SPRITE_ATTR_CLR_BIT9=0xfffffdff (clears bit9 player_side; 480 ROM refs)
  - OAM_SPRITE_ATTR_CLR_BITS13_10=0xffffc3ff (clears bits[13:10] slot_idx field; 27 ROM refs)
  - OAM_SPRITE_ATTR_CLR_BIT16=0xfffeffff (clears bit16 flip flag; 1475 ROM refs)
  - OAM_SPRITE_ATTR_CLR_BIT17=0xfffdffff (clears bit17 composite sprite flag; 448 ROM refs)
- card_info.inc x2:
  - GEARFRIED_IRON_KNIGHT_CID=0x13c3 (pw=00423705; card_0839; 10 ROM refs)
  - GEARFRIED_SWORDMASTER_CID=0x186b (pw=57046845; card_1772; 8 ROM refs)

**PLATE 关键**:
- enqueue_sprite_attr_for_chain_node_check (0x080431f4): CJK plate → full ASCII rewrite via setComment(PLATE_COMMENT, ...)
- enqueue_zone_slot_sprite_attr_by_card_type (0x080432bc): CJK plate → full ASCII rewrite (corrects 3 stale FUN_ refs)
- 7 函数: FUN_ substring replace (16 total token replacements)
- Proposal 地址 0x08043100/0x08043190 对应 LAB_/mid-code; 落地时自动校正为实际函数入口 0x080430e4/0x0804317c

**踩坑**: fn-ptr +1 再次需要补 (0x37884/0x389dc/0x389f8/0x3aa74 in asm/03; zone_monster_field_bonus_table+7*16 at 0x08040ab4 in asm/04); 补完后 SHA1 match.

**落地后验收**:
- plate FUN_ grep in Seg-5 [lines 6685..7928]: 0 hits ✅
- non-ASCII grep in Seg-5 range: 0 hits ✅
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 04 范围 `[0x0804020c, 0x08049014)` (193 named fn = 176 push-prologue + 17 leaf
> `clear_display_step_lock_*` 簇, 920 DAT_/DWORD_/PTR_ 槽, **0 ROM_INCBIN/inter-function 数据块** —
> 文件全为代码 + 函数内 literal pool, 无 `.incbin`/`.byte`/`ROM_INCBIN`; `.zero 0x2` 均为 THUMB
> literal-pool 字对齐 pad) 按**函数数**均分 10 段 (~19 fn/段, 边界=函数结束处=下一函数起点)。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x4020c..0x407fc | 19 | 64 | — | 卡牌显示序列 tick (op15/equip preview/set display/lp compare) + invoke_card_display_op_equip_mode 簇 |
| Seg-2 | 0x407fc..0x40c88 | 20 | 46 | — | normal-summon/flip/random-draw/prng display tick + op3a/39/3b/3c/0b 簇 (含部分 clear_display_step_lock 叶) |
| Seg-3 | 0x40c88..0x417f0 | 19 | 98 | — | clear_display_step_lock 叶簇尾 + zone-slot-spell-remove / field-clear / hand-shuffle / lp-change tick |
| Seg-4 | 0x417f0..0x4308c | 19 | 159 | — | 重: zone-slot-ref-track / equip-attach / op3e / zone-equip-link / card-flip-reveal / zone-card-relocate / draw-card 大型 tick 簇 |
| Seg-5 | 0x4308c..0x4394c | 19 | 48 | — | equip chain entry reset / target slot resolve / chain-slot-scan dispatch + enqueue_sprite_attr 簇头 |
| Seg-6 | 0x4394c..0x44674 | 20 | 69 | — | enqueue zone/equip slot sprite attr 簇 + scan_equip_chain_list + activation sprite render |
| Seg-7 | 0x44674..0x44e30 | 19 | 35 | — | graveyard spell sprite + hand-card sprite + equip-zone sprite dispatch (banisher 系列) |
| Seg-8 | 0x44e30..0x47990 | 19 | 275 | — | 重: update_duel_field_slot_sprite_state + dispatch_card_effect_sprite_render_by_card_id (大型 card_id 分发) + equip target bitmap 计算/查询簇 |
| Seg-9 | 0x47990..0x47ec0 | 20 | 14 | — | equip target bitmap zone-test/update 谓词小簇 (zone11/13/14/15 + cross-side flag) |
| Seg-10 | 0x47ec0..0x49014 | 19 | 112 | — | render_slot_card_sprite 描述符渲染 + zone sprite effect dispatch + lp indicator + setup_equip_slot_sprite_attr_by_card (文件末) |

执行约定同 file 00/01/02/03: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-01-vija-scene-text.md` (file 01 完整记录)
- `doc/dev/p5-refine-02-text-lp-fieldspell.md` (file 02 完整记录, equip chain / card_id 常量与 carve label)
- `doc/dev/p5-refine-03-equip-chain-hand.md` (file 03 完整记录, dispatch_duel_event_display_seq hub /
  tick_*_display_seq 簇 / card_info.inc CID 常量批量沉淀 / fn-ptr +1 踩坑)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
