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
| 6 | 0x4394c..0x44674 | 20 | 69 | — | ✅ | (see §四.4.06) |
| 7 | 0x44674..0x44e30 | 19 | 35 | — | ✅ | (see §四.4.07) |
| 8a | 0x44e30..0x4640c | 9 | 143 | — | ✅ | (see §四.4.08a) |
| 8b | 0x4640c..0x47990 | 10 | 132 | — | ✅ | (see §四.4.08b) |
| 9 | 0x47990..0x47ec0 | 20 | 14 | — | ✅ | (see §四.4.09) |
| 10 | 0x47ec0..0x49014 | 19 | 112 | — | ✅ | (see §四.4.10) |

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

### 4.06 Seg-6 完成记录 (0x0804394c..0x08044674)

**函数列表 (20)**:
enqueue_zone_card_sprite_attr_by_slot / invoke_equip_activation_with_zero_flag /
apply_slot_equip_activation_with_eligibility_check / apply_slot_equip_activation_with_sprite /
dispatch_slot_equip_sprite_by_field6_type / enqueue_equip_chain_pair_sprite_validated /
scan_equip_chain_list_for_activation_sprite / enqueue_equip_chain_pair_sprite_if_eligible /
enqueue_equip_chain_dual_slot_sprite_with_activation_scan / enqueue_face_down_slot_sprite_attr /
enqueue_hand_card_sprite_by_spell_type / dispatch_equip_zone_sprite_and_activation /
dispatch_equip_zone_sprite_banisher_of_the_light / dispatch_equip_zone_sprite_banisher_lp_row2 /
dispatch_equip_zone_sprite_banisher_with_count_check / dispatch_equip_zone_sprite_banisher_with_spell_check /
enqueue_equip_zone_sprite_direct / dispatch_equip_zone_sprite_banisher_by_field_count /
dispatch_equip_zone_sprite_banisher_lp_row1 / render_equip_zone_sprite_with_chain_lp

**符号化统计**: EQ=68 (reuse+new) / REF=1 / RENAME=0 / PLATE=8 fn (17 entries) / carve=0 / disasm=0 / §5.1=0

**新建常量 (27 项)**:
- oam_attr.inc x5:
  - OAM_EQUIP_SLOT_SPRITE_P1=0x8034 (equip slot activation; 19 ROM refs)
  - OAM_EQUIP_ZONE_SPRITE_P1=0x8033 (equip zone sprite; 40 ROM refs)
  - OAM_EQUIP_CHAIN_PAIR_SPRITE_P1=0x803d (equip chain pair; 76 ROM refs)
  - OAM_EQUIP_CHAIN_DUAL_SPRITE_P1=0x803e (equip chain dual-slot; 121 ROM refs)
  - OAM_ZONE_EQUIP_SPRITE_P1=0x8045 (zone equip shape; 166 ROM refs)
- card_info.inc x22 (新建):
  - BANISHER_OF_THE_LIGHT_CID=0x1332 (6 slots)
  - GRAVEROBBER_CID=0x1379 (2 slots)
  - SUPER_REJUVENATION_CID=0x14e2 (2 slots)
  - SAMSARA_CID=0x19da / CRASS_CLOWN_CID=0x1005 / BLADE_RABBIT_CID=0x1868 / AMEBA_CID=0x118a /
    MANTICORE_OF_DARKNESS_CID=0x16f9 / ARCHFIEND_OF_GILFER_CID=0x13e3 / MINAR_CID=0x11bc /
    SKULL_MARK_LADYBUG_CID=0x12a2 / MAKYURA_THE_DESTRUCTOR_CID=0x14a5 / DESPAIR_FROM_THE_DARK_CID=0x1653 /
    FEAR_FROM_THE_DARK_CID=0x1655 / OUTSTANDING_DOG_MARRON_CID=0x1687 / ROC_FROM_THE_VALLEY_OF_HAZE_CID=0x1828 /
    NIGHT_ASSAILANT_CID=0x179a / BROWW_HUNTSMAN_OF_DARK_WORLD_CID=0x1966 /
    SILLVA_WARLORD_OF_DARK_WORLD_CID=0x1968 / EKIBYO_DRAKMORD_CID_SHIFTED=0xa4e80000 /
    act_cid_1048_08043b48=0x1048 (low conf) / act_cid_1197_08043be8=0x1197 (low conf)
- card_info.inc x1 (复用): LIGHT_OF_INTERVENTION_CID=0x135d (card_info.inc:401)

**REF**: PTR_gP1LifePoints_080440ac -> gP1LifePoints=0x0201c4e0 (ewram.inc:79)

**PLATE**: 8 functions, 17 substr replacements (21 logical token replacements):
- invoke_equip_activation_with_zero_flag: 5 FUN_ tokens
- enqueue_equip_chain_pair_sprite_validated: 2 FUN_ tokens
- scan_equip_chain_list_for_activation_sprite: 4 FUN_ tokens
- dispatch_equip_zone_sprite_and_activation: 1 FUN_ token
- dispatch_equip_zone_sprite_banisher_with_count_check: 1 FUN_ token
- dispatch_equip_zone_sprite_banisher_with_spell_check: 2 FUN_ tokens
- enqueue_equip_zone_sprite_direct: 1 FUN_ token
- render_equip_zone_sprite_with_chain_lp: 1 FUN_ token

**踩坑**: Proposal 中 5 处 DAT_ 地址错误 (ROM 验证发现):
- OAM_EQUIP_SLOT_SPRITE_P1: proposal 0x08043b44 -> 正确 0x08043af8
- CRASS_CLOWN_CID: proposal 0x08043b04 -> 正确 0x08043b30
- BLADE_RABBIT_CID: proposal 0x08043c14 -> 正确 0x08043bec
- OAM_ZONE_EQUIP_SPRITE_P1: proposal 0x0804416c -> 正确 0x08044148 (0x0804416c=OAM_EQUIP_ZONE_SPRITE_P1)
- SAMSARA_CID: proposal 0x08044540 -> 正确 0x08044530 (0x08044540 是函数入口)
- CID BST cluster: proposal 0x080440dc..0x08044108 -> 正确 0x080441e0..0x0804428c
fn-ptr +1 再次补回 (0x37884/0x389dc/0x389f8/0x3aa74 in asm/03; 0x08040ab4 +7*16 in asm/04)

**落地后验收**:
- plate FUN_ grep in Seg-6 [lines 7927..9800]: 0 hits
- non-ASCII grep in Seg-6 range: 0 hits
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

---

### 4.07 Seg-7 完成记录 (0x08044674..0x08044e30)

**函数列表 (19)**:
enqueue_graveyard_spell_sprite_and_lp / enqueue_graveyard_spell_sprite_with_zone_ref /
enqueue_hand_card_sprite_alt_by_zone_slot / enqueue_graveyard_spell_sprite_with_player_xor /
enqueue_equip_zone_sprite_by_slot_ptr / enqueue_equip_zone_sprite_with_attr_u16 /
enqueue_equip_zone_sprite_attr_shape_a / enqueue_equip_zone_sprite_attr_shape_b /
enqueue_hand_sprite_with_flip_flag_set / enqueue_hand_sprite_by_zone_set_code /
enqueue_sprite_attr_for_zone_slot_packed / enqueue_equip_chain_sprite_attrs_for_slot /
enqueue_equip_slot_sprite_by_player / enqueue_sprite_attr_row_0x29_by_player /
enqueue_sprite_attr_row_0x29_with_flag2 / enqueue_equip_slot_sprite_with_display_code /
enqueue_equip_zone_sprite_for_player / enqueue_equip_multi_slot_marker_sprite /
enqueue_field_slot_sprite_with_state_update

**符号化统计**: EQ=35 (25 reuse + 10 new) / REF=0 / RENAME=0 / FUNC_RENAME=0 / PLATE=14 fn (26 token: 13 substr + 1 full-ASCII-rewrite) / carve=0 / disasm=0 / §5.1=0

**新建常量 (7 项)**:
- card_info.inc x3:
  - WATAPON_CID=0x17cc (pw=87774234; card_1626; enqueue_hand_sprite_by_zone_set_code Watapon-path; 10 raw refs)
  - WATAPON_EQUIP_ACTIVATION_MASK=0x34500000 (activation flag mask ORed into attr2 arg for Watapon path; 24 raw refs)
  - DARK_MIMIC_LV1_CID=0x17d5 (pw=74713516; card_1635; enqueue_equip_chain_sprite_attrs_for_slot card_type filter A; 16 raw refs)
- oam_attr.inc x3:
  - OAM_EQUIP_SLOT_SPRITE_P2=0x8029 (P2 equip slot sprite attr0; 5 slots; 121 raw refs)
  - OAM_MULTI_SLOT_MARKER_P2=0x8048 (P2 multi-slot selection marker; 12 raw refs)
  - OAM_FIELD_SLOT_SPRITE_P2=0x8043 (P2 duel field slot sprite attr0; 35 raw refs)
- duel_field.inc x1:
  - EQUIP_MULTI_SLOT_CTL_OFF=0x1ce0 ([gP1LifePoints+0x1ce0] equip multi-slot control word; 1 raw ref)

**PLATE**: 14 functions total:
- 13 substr replacements (26 FUN_ tokens total across 13 functions, 0 WARN)
- 1 full ASCII rewrite: enqueue_sprite_attr_for_zone_slot_packed (0x08044b5c) — CJK plate replaced with ASCII (len=891)
- Post-land Seg-7 lines [9720..10822]: FUN_ count = 0 (line 10822 is Seg-8 first function plate, excluded) / CJK = 0

**踩坑**: fn-ptr +1 再次需要补 (4 slots in asm/03: 0x37884/0x389dc/0x389f8/0x3aa74; zone_monster_field_bonus_table+7*16 at 0x08040ab4 in asm/04); 补完后 SHA1 match.

**byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.08a Seg-8a 完成记录 (0x08044e30..0x0804640c)

**函数列表 (9)**:
update_duel_field_slot_sprite_state / enqueue_sprite_attr_with_xy_split /
enqueue_sprite_attr_with_shape / enqueue_equip_set_slot_sprite_by_zone_col /
enqueue_effect_card_slot_sprite_attr / enqueue_equip_card_sprite_attr_for_slot /
enqueue_effect_zone_pair_sprite_scan / apply_nitro_unit_equip_activation /
dispatch_card_effect_sprite_render_by_card_id

**符号化统计**: EQ=116 / REF=18 / RENAME=9 / FUNC_RENAME=0 / PLATE=6 fn (20 FUN_ tokens) / carve=0 / disasm=0 / §5.1=0

**新建常量**:
- oam_attr.inc x7: OAM_XY_SPLIT_SPRITE_P1/P2 (0x3a/0x803a) + OAM_EQUIP_SET_SLOT_P1/P2 (0x3b/0x803b) + OAM_EFFECT_CARD_SLOT_P1/P2 (0x3c/0x803c) + EQUIP_PAIR_SPRITE_EXTRA (0x101)
- ewram.inc x2: P1LP_EQUIP_BITMAP_CTR_OFF=0x1d3c + gEquipZoneCountTable=0x0201e1c8
- duel_field.inc x1: EQUIP_CHAIN_SENTINEL=0xffff0000
- card_info.inc x62: 56 named CIDs + PANDEMONIUM_CID (0x169f) + CENTRIFUGAL_FIELD_CID (0x187f) + 4 gap stubs (upd_cid_10c6/120e/13e9/1672); 4 REUSEs (UMI_CARD_ID/ZOMBYRA_THE_DARK_CID/RAGING_FLAME_SPRITE_CID/SPELL_ZONE_TARGET_CARD_ID)

**REF highlights**: gDuelFieldSlots x6 + gDuelFieldSlots_p2_base x2 + gEquipChainSlotRefs x7 + gEquipZoneCountTable x1 + gEquipNodePool x1 + apply_nitro_unit_equip_activation+1 (THUMB fn-ptr) x1

**PLATE**: 6 functions, 20 FUN_ tokens total; 0 WARN (all patterns found); 0 FUN_ remaining in lines 10822..13947

**踩坑**: fn-ptr +1 再次需要补 (4 slots in asm/03: 0x37884/0x389dc/0x389f8/0x3aa74; zone_monster_field_bonus_table+7*16 at 0x08040ab4 in asm/04); 新增 THUMB fn-ptr 0x08045efc -> apply_nitro_unit_equip_activation+1 (Ghidra 导出偶地址需手补 +1)。Dry run: A=116 B=18 C=9 D=6 fails=0 (0 WARN). 补完后 SHA1 match.

**落地后验收**:
- plate FUN_ grep in Seg-8a [lines 10822..13947]: 0 hits
- non-ASCII grep in Seg-8a range: 0 hits
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.08b Seg-8b 完成记录 (0x0804640c..0x08047990)

**函数列表 (10)**:
check_slot_equip_placement_valid / build_equip_placement_valid_bitmap /
check_slot_equip_target_eligibility / dispatch_card_effect_zone_action_by_card_id /
handle_card_effect_zone_eligibility_by_field6 / update_equip_target_bitmap_for_field /
query_equip_target_bitmap_default / prepare_slot_ctx_for_equip_bitmap /
enqueue_equip_slot_bitmap_update / test_equip_target_slot_in_bitmap

**符号化统计**: EQ=117 (116 via equate + 1 EOL-only) / REF=6 / RENAME=23 / PLATE=4 fn (15 FUN_ tokens) / carve=0 / disasm=0 / §5.1=0

**新建常量 (23 项)**:
- card_info.inc x19:
  PANDEMONIUM_WATCHBEAR_CID(0x1683) / HEAVY_MECH_SUPPORT_PLATFORM_CID(0x1825) /
  AUTONOMOUS_ACTION_UNIT_CID(0x15e6) / CALL_OF_THE_HAUNTED_CID(0x137d) /
  PREMATURE_BURIAL_CID(0x1366) / SPIRIT_MESSAGE_L_CID(0x149a) /
  SPIRITUAL_ENERGY_SETTLE_CID(0x150e) / THE_FIRST_SARCOPHAGUS_CID(0x17af) /
  THE_THIRD_SARCOPHAGUS_CID(0x17ad) / BATTLE_SCARRED_CID(0x16a2) /
  NINJITSU_ART_OF_TRANSFORMATION_CID(0x1768) / RE_FUSION_CID(0x1881) /
  SYMBOL_OF_HERITAGE_CID(0x19d7) / BIG_BANG_SHOT_CID(0x1625) /
  DESTINY_BOARD_CID(0x1468) / AMPLIFIER_CID(0x12d3) /
  SOUL_RESURRECTION_CID(0x17b7) / FIBER_JAR_CID(0x14fb) /
  GOBLIN_OUT_OF_FRYING_PAN_CID(0x19e1)
- duel_field.inc x1: EQUIP_BITMAP_CTRL_OFF(0x10d4)
- oam_attr.inc x3: OAM_SPRITE_ATTR_CLR_BIT18(0xfffbffff) / OAM_SPRITE_ATTR_CLR_BITS22_19(0xff87ffff) / OAM_EFFECT_ZONE_SPRITE_P1(0x8031)

**REF**: 5x PTR_gP1LifePoints (0x0201c4e0) + 1x compound (.word gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF = 0x0201d5b4)

**PLATE**: 4 functions, 15 FUN_ tokens total (2+8+4+1); 0 WARN (all patterns found)

**踩坑**: compound REF 槽 0x080478f0 Ghidra 导出为 `.word gDuelFieldSlots` (平坦地址); 需手改为 `.word gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF`; build 验证发现 2 字节偏差 @ 0x080478f0 后手补修正。fn-ptr +1 再次需要补 (slots 0x37884/0x389dc/0x389f8/0x3aa74 in asm/03; zone_monster_field_bonus_table+7*16 @ 0x08040ab4 + apply_nitro_unit_equip_activation+1 @ 0x08045efc in asm/04)。

**落地后验收**:
- plate FUN_ grep in Seg-8b [lines 13947..16863]: 0 hits
- non-ASCII grep in Seg-8b range: 0 hits
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅

---

### 4.09 Seg-9 完成记录 (0x08047990..0x08047ec0)

**函数列表 (20)**:
check_equip_slot_eligible_in_target_bitmap / update_equip_target_bitmap_by_card_type /
update_equip_target_bitmap_zone14 / query_equip_target_bitmap_with_zone_struct /
update_equip_target_bitmap_zone15 / render_equip_zone_bitmap_sprite_by_chain /
forward_equip_bitmap_update_with_full_mask / test_equip_target_slot_zone11 /
query_equip_zone_slot_target_bit / forward_equip_bitmap_update_zone11 /
test_equip_target_slot_zone13 / test_equip_target_slot_zone13_crossside /
update_equip_target_bitmap_zone_d_no_flag / reset_equip_slot_ctx_with_bitmap_update_zone_d /
test_equip_target_zone13_with_slot_parity_flag / submit_equip_sprite_if_slot_eligible /
submit_equip_sprite_samsara_zone_select / prepare_equip_slot_ctx_for_bitmap_update /
test_equip_target_slot_zone14 / test_equip_target_slot_zone14_with_flags

**符号化统计**: EQ=14 (0 new, 全复用) / REF=0 / RENAME=0 / PLATE=6 fn / carve=0 / disasm=0 / §5.1=0

**新建常量**: 0 (全 7 个唯一值复用 ewram.inc + card_info.inc 已建常量)

**PLATE 订正内容**:
- update_equip_target_bitmap_by_card_type: FUN_0807a9c8 -> dispatch_equip_banisher_activation_by_state
- update_equip_target_bitmap_zone14: FUN_08065698/FUN_0806a334/FUN_0806ecb0 -> 现名 (3 tokens)
- update_equip_target_bitmap_zone15: FUN_080576b0 -> tick_equip_chain_sprite_and_spell_zone_seq
- render_equip_zone_bitmap_sprite_by_chain: gDuelFieldSlots_A->gDuelFieldSlots / gDuelFieldSlots_B->gEquipNodePool / "CARD_ID_B=0x1814 (The All-Seeing White Tiger)"->"SILENT_SWORDSMAN_LV5_CID=0x1814"
- test_equip_target_zone13_with_slot_parity_flag: gDuelFieldSlots_A -> gDuelFieldSlots
- submit_equip_sprite_if_slot_eligible: DAT_08047d8c=0x14e2 -> SUPER_REJUVENATION_CID=0x14e2

**落地后验收**:
- plate FUN_ grep in Seg-9 [lines 16862..17597]: 0 hits
- non-ASCII (CJK) grep in Seg-9 range: 0 hits
- "All-Seeing White Tiger" grep in Seg-9 range: 0 hits
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**踩坑**: fn-ptr +1 再次补回 (0x37884/0x3aa74 check_level_conv_lab_node_match+1 in asm/03;
0x389dc/0x389f8 check_card_is_amazoness_type+1 in asm/03;
zone_monster_field_bonus_table+7*16 @ 0x08040ab4 in asm/04;
apply_nitro_unit_equip_activation+1 @ 0x08045efc in asm/04;
gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF @ 0x080478f0 in asm/04).
All 7 slots re-patched after re-export; SHA1 match restored.

---

### 4.10 Seg-10 完成记录 (0x08047ec0..0x08049014)

**函数列表 (19)**:
test_equip_target_zone14_with_ctx_clear / update_equip_target_bitmap_zone_e_no_flag /
update_equip_bitmap_zone_e_with_slot_save / update_equip_bitmap_with_cross_side_flag /
render_slot_card_sprite_from_descriptor / render_slot_card_sprite_and_effects /
render_zone_sprite_with_effect_dispatch_by_slot / render_slot_card_sprite_with_chaos_equip_check /
render_zone_sprite_with_effect_dispatch_alt / enqueue_sprite_attr_for_zone_card_id_lookup /
enqueue_sprite_attr_by_sign / enqueue_equip_zone_sprite_by_side /
enqueue_sprite_attr_for_slot_indicator / enqueue_sprite_attr_position_by_player /
enqueue_sprite_attr_clamped / enqueue_sprite_attr_record_with_cap /
submit_lp_indicator_with_slot_xor_flag / submit_lp_change_indicator_with_chain_check /
setup_equip_slot_sprite_attr_by_card

**符号化统计**: EQ=87 (49 reuse + 10 new oam_attr.inc + 26 new card_info.inc + 2 new duel_field.inc) / REF=25 / RENAME=0 / FUNC_RENAME=0 / PLATE=8 fn (16+2=18 FUN_ tokens + 5 C9 wrong-global corrections) / carve=0 / disasm=0 / §5.1=0

**新建常量 (38 项)**:
- oam_attr.inc x10:
  OAM_SLOT_SPRITE_P2(0x8032) / OAM_ZONE_CARD_ID_SPRITE_P2(0x802e) / OAM_SIGN_SPRITE_P2(0x8030) /
  OAM_EQUIP_ZONE_SIDE_P2(0x802f) / OAM_SLOT_INDICATOR_P2(0x802b) / OAM_POSITION_ATTR_P2(0x8026) /
  OAM_SPRITE_COUNT_P2(0x8025) / OAM_SPRITE_ATTR_CLR_BITS20_17(0xffe1ffff) /
  OAM_SPRITE_ATTR_CLR_BITS25_22(0xfc3fffff) / OAM_SPRITE_ATTR_CLR_BIT26(0xfbffffff)
- card_info.inc x26: WHITE_MAGICAL_HAT / MASKED_SORCERER / BISTRO_BUTCHER / RELINQUISHED /
  DRILL_BUG / ROBBINS_GOBLIN / CESTUS_OF_DAGLA / SECRET_OF_THE_BANDIT / DON_ZALOOG /
  TOON_MASKED_SORCERER / DARK_ROOM_OF_NIGHTMARE / FREEZING_BEAST / equip_cid_15de_08048a68(low-conf) /
  MEFIST_THE_INFERNAL_GENERAL / SASUKE_SAMURAI_3 / VAMPIRE_LADY / DES_COUNTERBLOW /
  HALLOWED_LIFE_BARRIER / DARK_BLADE_THE_DRAGON_KNIGHT / PIKERUS_CIRCLE_OF_ENCHANTMENT /
  POISON_FANGS / SPIRAL_SPEAR_STRIKE / DES_WOMBAT / BRRON_MAD_KING_OF_DARK_WORLD /
  DOOM_DOZER / BEGONE_KNAVE
- duel_field.inc x2: FIELD_COPY_COUNT_FLAG(0x00010002) / EQUIP_ZONE_EFFECT_ATTR_OR(0x1e501511, low-conf)

**PLATE 订正内容**:
- update_equip_target_bitmap_zone_e_no_flag: FUN_080584cc/FUN_080777d8/FUN_0807c474 -> addr literals
- update_equip_bitmap_zone_e_with_slot_save: FUN_08059068 -> addr literal
- render_zone_sprite_with_effect_dispatch_alt: FUN_08048268 -> render_zone_sprite_with_effect_dispatch_by_slot
- enqueue_sprite_attr_by_sign: FUN_08049014 -> addr, FUN_080490b4 -> duel_field_080490b4, FUN_0808e5c4 -> addr
- enqueue_equip_zone_sprite_by_side: 5 FUN_ -> addr literals
- enqueue_sprite_attr_clamped: FUN_0805635c -> addr, FUN_080572b8 -> duel_field_080572b8, FUN_0808e5c4 -> addr
- enqueue_sprite_attr_record_with_cap: FUN_08098264 -> addr
- submit_lp_change_indicator_with_chain_check: FUN_0808f938 -> refresh_opponent_field_slots_for_card_attached
- C9 corrections: gDuelFieldSlots=0x0201bc54 -> gDuelEffectChainSlots + gDuelTurnStruct -> gEquipChainSlotRefs
  (render_slot_card_sprite_from_descriptor + render_slot_card_sprite_and_effects)

**落地后验收**:
- plate FUN_ grep in Seg-10 [lines 17597..19930]: 0 hits
- non-ASCII grep in Seg-10 range: 0 hits
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b

**踩坑**: fn-ptr +1 再次补回 (同 Seg-9 - 7 slots total: 4 in asm/03 + 3 in asm/04);
RefineF04Seg10PlateFix.py 补修 FUN_0808e5c4 x2 (proposal PLATE 清单遗漏但 grep 发现)。

**file 04 全 10 段完成!**

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
| Seg-8a | 0x44e30..0x4640c | 9 | 143 | — | update_duel_field_slot_sprite_state + enqueue_sprite_attr_* 簇 + dispatch_card_effect_sprite_render_by_card_id 前半 ✅ |
| Seg-8b | 0x4640c..0x47990 | 10 | 132 | — | dispatch_card_effect_sprite_render_by_card_id 后半 + equip target bitmap 计算/查询簇 |
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
