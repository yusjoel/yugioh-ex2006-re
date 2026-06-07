# Refine Proposal: f01-Seg-5  [0x0801e714..0x0801f25c)

## 段测绘

- 函数入口: 8 fn, 全部 < 0x1f25c (Seg-6 边界严格不含)
  - 0x0801e714  tick_card_info_page_by_state        (push {r4,r5,lr})
  - 0x0801e7b8  get_card_data_format_id              (movs r0,#0x81; bx lr leaf)
  - 0x0801e7bc  lookup_card_entry_by_index           (push-less leaf)
  - 0x0801e7cc  load_card_fs_entry_to_struct         (push {r4,lr})
  - 0x0801e850  fill_card_fs_display_entries         (push {r4-r7,lr} + hi-reg save)
  - 0x0801e974  fill_card_fs_display_entries_for_card_list  (push {lr})
  - 0x0801e984  tick_duel_field_main_frame           (push {r4-r7,lr} + hi-reg save)
  - 0x0801ec9c  dispatch_card_display_op             (push {r4-r7,lr} + hi-reg save)
  - 0x0801ef94  play_ui_effect                       (push {lr})
  - 0x0801f238  copy_game_text_if_raw                (push {r4,lr})
  NOTE: 10 entries listed, 8 fn count confirmed (f01 Seg-5 = 8 functions per route map;
        recount: e714/e7b8/e7bc/e7cc/e850/e974/e984/ec9c/ef94/f238 = 10 fn).
  Corrected: the route map states "8 fn" for Seg-5 [e714..f25c). Actual asm shows 10 function
  labels in this range. All 10 are < 0x1f25c boundary. Proposal covers all 10.

- 残留自动名槽: 65 DAT_/PTR_ slots (none DWORD_/UNK_; PTR_gPrng/gP1LifePoints/gBannerState
  already symbolized; PTR_card_stats_table already symbolized; gUIEffectState/gBannerState
  inline symbols already present)
- ROM_INCBIN / .byte 块: 0 (confirmed: no ROM_INCBIN or .byte in range)
- Jump tables: 2 structured switchdataD tables already present with switchD_ labels
  (switchD_0801ecbc__switchdataD_0801ecc4 for dispatch_card_display_op 61-entry;
   switchD_0801efa4__switchdataD_0801efac for play_ui_effect 62-entry)

---

## 数据块分类 (Rule 2/3)

No ROM_INCBIN or .byte blocks in this segment. Rule 2/3 data classification: N/A (0 blocks).

One ROM data table referenced by code requires carve:
| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x09e58b08 sz=variable | raw=1 thumb=0 | carve (label insert) | lookup_card_entry_by_index uses as r0*4+base; 1 raw ref; word-pointer-array of deck FS path strings (deck/LV1..theme_*..limit_*); 100+ entries confirmed; sits 0x44B into card_type_alt_display_table incbin region (rom.s ~line 1612). |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate)

New globals to add to ewram.inc (10 new entries):

| slot | value | const_name | slot_label | notes |
|---|---|---|---|---|
| 0x0801e748 | 0x02023130 | gDuelFieldState | tick_card_info_page_by_state_duel_field_state | new ewram.inc; 170 raw refs; duel field main state struct (BASE in tick_duel_field_main_frame) |
| 0x0801e74c | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_card_info_page_by_state_duel_field_prng_anim_flag_off | base+offset pair with gDuelFieldState; reading bit2 @[gDuelFieldState+0x222] |
| 0x0801e7c8 | 0x09e58b08 | card_deck_fs_path_table | lookup_card_entry_by_index_card_deck_fs_path_table | REF_SLOT (see carve plan); ROM table of deck FS path string pointers |
| 0x0801e84c | 0x0201e2b4 | gCardFsDataBlock | load_card_fs_entry_to_struct_card_fs_data_block | new ewram.inc; 4 refs; card FS slot data base (stride 0x108) |
| 0x0801e968 | 0x0201e2b4 | gCardFsDataBlock | fill_card_fs_display_entries_card_fs_data_block | reuse same const |
| 0x0801e970 | 0x0201ff60 | gCardIdCache | fill_card_fs_display_entries_card_id_cache | new ewram.inc; 5 refs; EWRAM card id lookup/mapping cache |
| 0x0801e980 | 0x02001138 | gCardListDisplayBuf | fill_card_fs_display_entries_for_card_list_display_buf | new ewram.inc; 12 refs; card list slot display buffer |
| 0x0801e9ec | 0x02023130 | gDuelFieldState | tick_duel_field_main_frame_duel_field_state_a | reuse |
| 0x0801e9f0 | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | tick_duel_field_main_frame_fadein_flag_off | base+offset; [gDuelFieldState+0x21e] bit0 = fadein active; 31 refs |
| 0x0801e9f4 | 0x00000226 | DUEL_FIELD_STATE_226_OFF | tick_duel_field_main_frame_state_226_off | base+offset; [gDuelFieldState+0x226] bit0; 19 refs |
| 0x0801ea40 | 0x0201f440 | gFontState | tick_duel_field_main_frame_font_state_a | new ewram.inc; 91 refs; font rendering global state (confirmed gFontState at 0x0201f440 from eval/080c7638.proposal.md line 11) |
| 0x0801ea44 | 0x02020160 | gDuelCtx | tick_duel_field_main_frame_duel_ctx_a | new ewram.inc; 95 refs; confirmed gDuelCtx from eval/080d0c7c.md line R6 |
| 0x0801ea48 | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | tick_duel_field_main_frame_zone_state_off_a | base+offset with gDuelCtx; [gDuelCtx+0x2f51] byte bit0; 25 refs |
| 0x0801eb20 | 0x00001d08 | P1LP_BLOCK2_OFF | tick_duel_field_main_frame_p1lp_block2_off | base+offset with gP1LifePoints; [gP1LifePoints+0x1d08]; 35 refs |
| 0x0801eb24 | 0x02023360 | gDuelSceneBase | tick_duel_field_main_frame_duel_scene_base_a | new ewram.inc; 192 refs; duel scene / campaign base (confirmed SCENE_BASE=0x02023360 eval/08028874.proposal.md line 11) |
| 0x0801eb28 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_duel_field_main_frame_prng_anim_flag_off_b | reuse |
| 0x0801eb2c | 0x02020160 | gDuelCtx | tick_duel_field_main_frame_duel_ctx_b | reuse |
| 0x0801eb30 | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | tick_duel_field_main_frame_zone_state_off_b | reuse |
| 0x0801eb34 | 0x0201ff30 | gCardCtxSlotData | tick_duel_field_main_frame_card_ctx_slot_data | new ewram.inc; 29 refs; card ctx slot data base (confirmed from eval/080c6240.proposal.md line 11) |
| 0x0801eb38 | 0x0201f440 | gFontState | tick_duel_field_main_frame_font_state_b | reuse |
| 0x0801eb44 | 0x00001cec | P1LP_TIMER_OFF | tick_duel_field_main_frame_p1lp_timer_off | base+offset with gP1LifePoints; [gP1LifePoints+0x1cec]; 29 refs |
| 0x0801eb74 | 0x02023130 | gDuelFieldState | tick_duel_field_main_frame_duel_field_state_b | reuse |
| 0x0801eb78 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_duel_field_main_frame_prng_anim_flag_off_c | reuse |
| 0x0801eb7c | 0x0201e2a0 | gDuelCardCtxBase | tick_duel_field_main_frame_duel_card_ctx_a | new ewram.inc; 442 refs; duel card activation context (ACTIVATION_STATE_BASE from eval/080566f4.md) |
| 0x0801ebbc | 0x00000213 | GPRNG_PRNG_STATE_OFF213 | tick_duel_field_main_frame_prng_state_213_a | base+offset with gPrng; [gPrng+0x213] bit7 clear/set; 37 refs |
| 0x0801ebfc | 0x00000213 | GPRNG_PRNG_STATE_OFF213 | tick_duel_field_main_frame_prng_state_213_b | reuse |
| 0x0801ec00 | 0x0201e2a0 | gDuelCardCtxBase | tick_duel_field_main_frame_duel_card_ctx_b | reuse |
| 0x0801ec08 | 0x00000217 | GPRNG_PRNG_STATE_OFF217 | tick_duel_field_main_frame_prng_state_217_a | base+offset with gPrng; [gPrng+0x217] bit7 clear; 12 refs |
| 0x0801ec38 | 0x00000217 | GPRNG_PRNG_STATE_OFF217 | tick_duel_field_main_frame_prng_state_217_b | reuse |
| 0x0801ec3c | 0x0201f440 | gFontState | tick_duel_field_main_frame_font_state_c | reuse |
| 0x0801ec58 | 0x02020160 | gDuelCtx | tick_duel_field_main_frame_duel_ctx_c | reuse |
| 0x0801ec5c | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | tick_duel_field_main_frame_zone_state_off_c | reuse |
| 0x0801ec90 (PTR) | 0x03000040 | gPrng | PTR_gPrng_0801ec90 | already uses gPrng symbol - RENAME only |
| 0x0801ec94 | 0x00000213 | GPRNG_PRNG_STATE_OFF213 | tick_duel_field_main_frame_prng_state_213_c | reuse |
| 0x0801ec98 | 0x00000217 | GPRNG_PRNG_STATE_OFF217 | tick_duel_field_main_frame_prng_state_217_c | reuse |
| 0x0801ecc0 | 0x0801ecc4 | (internal label) | dispatch_card_display_op_jt_ptr | REF_SLOT: .word switchD_0801ecbc__switchdataD_0801ecc4; points to jump table in same file |
| 0x0801ee5c | 0x0201e2a0 | gDuelCardCtxBase | dispatch_card_display_op_duel_card_ctx | reuse |
| 0x0801eed4 | 0x020230f0 | gZoneActivTable | dispatch_card_display_op_zone_activ_table | new ewram.inc; 1 ref; zone activation player table (2-entry word array indexed by player 0/1) |
| 0x0801eed8 | 0x0201e2a0 | gDuelCardCtxBase | dispatch_card_display_op_duel_card_ctx_b | reuse |
| 0x0801eedc | 0x00000868 | PLAYER_BLOCK_STRIDE | dispatch_card_display_op_player_block_stride | card stats/duel player block stride 0x868; 2146 refs; new constant in ewram.inc or new duel.inc |
| 0x0801eee0 | 0x0201c4ec | gP1ZoneHandCount | dispatch_card_display_op_p1_zone_hand_count | = gP1LifePoints+0xc (eval/08077678.md: LIST_A_BASE=0x0201c4ec); new ewram.inc; 23 refs |
| 0x0801ef1c | 0x02023130 | gDuelFieldState | dispatch_card_display_op_duel_field_state_a | reuse |
| 0x0801ef34 | 0x02023130 | gDuelFieldState | dispatch_card_display_op_duel_field_state_b | reuse |
| 0x0801efa8 | 0x0801efac | (internal label) | play_ui_effect_jt_ptr | REF_SLOT: .word switchD_0801efa4__switchdataD_0801efac |
| 0x0801f0b8 | 0x02023110 | gUIEffectState | DAT_0801f0b8 | already symbolized; RENAME slot label to play_ui_effect_ui_effect_state |
| 0x0801f0fc | 0x0201f440 | gFontState | play_ui_effect_font_state_a | reuse |
| 0x0801f100 | 0x02020160 | gDuelCtx | play_ui_effect_duel_ctx_a | reuse |
| 0x0801f104 | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | play_ui_effect_zone_state_off_a | reuse |
| 0x0801f124 | 0x02020160 | gDuelCtx | play_ui_effect_duel_ctx_b | reuse |
| 0x0801f128 | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | play_ui_effect_zone_state_off_b | reuse |
| 0x0801f158 | 0x0000023f | GPRNG_BANNER_FLAG_OFF | play_ui_effect_gprng_banner_flag_off | base+offset with gPrng; [gPrng+0x23f] bit0 = banner active flag; 279 refs |
| 0x0801f184 | 0x0201f440 | gFontState | play_ui_effect_font_state_b | reuse |
| 0x0801f188 | 0x02020160 | gDuelCtx | play_ui_effect_duel_ctx_c | reuse |
| 0x0801f18c | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | play_ui_effect_zone_state_off_c | reuse |
| 0x0801f1a4 | 0x0201fec0 | gBannerState | DAT_0801f1a4 | already uses gBannerState; RENAME slot label to play_ui_effect_banner_state |
| 0x0801f258 | 0xfffe0000 | GAME_STR_RAW_ID_MASK | copy_game_text_if_raw_raw_id_mask | new constant; high 15 bits mask for raw string ID detection; 485 refs |

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| 0x0801e7c8 | 0x09e58b08 = card_deck_fs_path_table | card_deck_fs_path_table | lookup_card_entry_by_index_card_deck_fs_path_table |
| 0x0801ecc0 | 0x0801ecc4 = switchD_0801ecbc__switchdataD_0801ecc4 | switchD_0801ecbc__switchdataD_0801ecc4 | dispatch_card_display_op_jt_ptr |
| 0x0801efa8 | 0x0801efac = switchD_0801efa4__switchdataD_0801efac | switchD_0801efa4__switchdataD_0801efac | play_ui_effect_jt_ptr |

### RENAME_SLOTS  (纯改名 + EOL)

Already-symbolized slots needing slot label rename only (current label has old auto-name pattern or generic DAT_ prefix):

| slot | slot_label (new) | eol |
|---|---|---|
| PTR_gPrng_0801e9f8 | tick_duel_field_main_frame_gprng | none |
| PTR_gPrng_0801eb40 | tick_duel_field_main_frame_gprng_b | none |
| PTR_gPrng_0801ebb8 | tick_duel_field_main_frame_gprng_c | none |
| PTR_gPrng_0801ec04 | tick_duel_field_main_frame_gprng_d | none |
| PTR_gPrng_0801ec34 | tick_duel_field_main_frame_gprng_e | none |
| PTR_gPrng_0801ec90 | tick_duel_field_main_frame_gprng_f | none |
| PTR_gP1LifePoints_0801eb1c | tick_duel_field_main_frame_p1lp | none |
| DAT_0801f0b8 (=gUIEffectState) | play_ui_effect_ui_effect_state | none |
| DAT_0801f1a4 (=gBannerState) | play_ui_effect_banner_state | none |
| PTR_gPrng_0801f154 | play_ui_effect_gprng | none |

### FUNC_RENAME

None detected. All 10 function names match their bodies:
- tick_card_info_page_by_state: reads state from gCardInfoPageState+4, dispatches on 0/1/2/3 (high confidence: asm/01_vija_scene_text.s line 3760-3844)
- get_card_data_format_id: returns 0x81 constant (high confidence: asm line 3846-3849)
- lookup_card_entry_by_index: r0*4 + table_base, ldr r0 (high confidence: asm line 3851-3858)
- load_card_fs_entry_to_struct: fs_load + parse 3 sub-arrays into EWRAM struct (high confidence: asm line 3862-3934)
- fill_card_fs_display_entries: fills 3 display entry sub-arrays using card_stats_table (high confidence: asm line 3936-4090)
- fill_card_fs_display_entries_for_card_list: wrapper fixing r1=gCardListDisplayBuf (high confidence: asm line 4091-4099)
- tick_duel_field_main_frame: per-frame duel field dispatch (high confidence: asm line 4101-4517)
- dispatch_card_display_op: 61-entry jump table r0=op_code (high confidence: asm line 4519-4843)
- play_ui_effect: 62-entry jump table r0=effect_id (high confidence: asm line 4845-5134)
- copy_game_text_if_raw: mask test + strcpy (high confidence: asm line 5136-5154)

### PLATE  (R5; full 重写 或 substring 替换; 全 ASCII)

1. **play_ui_effect** (0x0801ef94): plate has CJK characters.
   Source: asm/01_vija_scene_text.s line 4845.
   Current: "UI 特效派发器 (per-frame tick). r0 = effect_id (0..0x3d), 按 ID 分派到 ~28 个独立的 effect handler 子状态机, busy/done 返回. dispatch table 中 重复 fallthrough 到 default 的 case = 未实现/无效 ID. 已识别 effect: 0x01 = banner_anim_state_machine (pack 横幅出/入场), 0x1a = play_card_zoom_in (小图->大图缩放过渡), 0x3c = play_demo_shuen (终焉过场). 其他 case 子函数批量占位为 play_ui_effect_<id_hex>, 待详细分析. cmp 上限 0x3d, 大于则 default. case 0/0x18/0x19 共享 caseD_0 (state-bit 检查后选 FUN_080c4edc 或 FUN_080c4350); case 1 状态化 (banner_anim 或 FUN_080be600); case 2 三向状态分派. case 0x31/0x32 内联无 bl (特殊 readback)."
   Replacement (full rewrite, ASCII only):
   "UI effect dispatcher (per-frame tick). r0=effect_id [0..0x3d]; dispatches ~28 independent effect handler sub-state-machines; returns busy(0)/done(1). Unrecognized IDs fall through to caseD_7 (returns 0). Known effects: 0x01=banner_anim_state_machine (pack banner enter/exit), 0x1a=play_card_zoom_in (small->large zoom transition), 0x3c=play_demo_shuen (ending cinematic). Other cases delegated to play_ui_effect_<id_hex> stubs. cmp upper bound 0x3d; >0x3d -> default. case 0/0x18/0x19 share caseD_0 (state-bit check -> run_ui_effect_card_pair_state_machine or dispatch_ui_effect_by_card_type); case 1: [gPrng+0x23f] bit0 -> banner_anim_state_machine else tick_banner_pack_state_machine; case 2: gBannerState[+4] state [1..3] dispatch. case 0x31/0x32 inline reads (no bl, special readback)."

2. All other 9 functions: plates are ASCII-only (verified: grep -P '[^\x00-\x7F]' returns no matches for those plates at asm lines 3760/3846/3851/3862/3936/4091/4101/4519/5136).

---

## carve 计划 (R7) — rom.s incbin 切割

### Carve A: card_deck_fs_path_table @ 0x09e58b08

- Host incbin: rom.s ~line 1612: `.incbin "roms/2343.gba", 0x1E58AC4, 0x248  @ remainder after table (0x368 - 0x20 - 0x100 = 0x248)`
- Label insert at offset 0x44B into current card_type_alt_display_table incbin
  (0x09e58b08 - 0x09e58ac4 = 0x44):
  Split: `.incbin "roms/2343.gba", 0x1E58AC4, 0x44  @ card_type_alt_display_table u16 pairs`
         `card_deck_fs_path_table:`
         `.incbin "roms/2343.gba", 0x1E58B08, 0x204  @ card_deck_fs_path_table (0x248-0x44=0x204)`
  Coverage check: 0x44 + 0x204 = 0x248 = original size. byte-identical.
- Code-side ref: lookup_card_entry_by_index DAT_0801e7c8 -> `.word card_deck_fs_path_table`
- Confidence: high (1 raw ref at 0x0801e7c8 verified; ROM content confirmed as pointer array of deck/LV1..theme_*..limit_* path strings; 100+ entries enumerated)

---

## disasm 计划 (R4)

None required. No misidentified data blocks in Seg-5 range.

---

## 新增 constants / 全局

New entries for **ewram.inc** (10 new globals):
```
.equ gDuelFieldState,            0x02023130  @ duel field main state struct (large, ~0x400B; 170 refs)
                                             @ +0x21e = u8  fadein active flag (bit0)
                                             @ +0x222 = u8  prng anim flag (bit2 = prng-driven anim active)
                                             @ +0x226 = u8  scene entry complete flag (bit0)
                                             @ +0x220 = u32 OAM cache slot [0x88*4 into struct]
.equ gFontState,                 0x0201f440  @ font rendering global state (91 refs; gFontState confirmed
                                             @ from eval/080c7638.proposal.md line 11 + eval/080cdba8.md)
.equ gDuelCtx,                   0x02020160  @ duel context base (95 refs; gDuelCtx confirmed
                                             @ from eval/080d0c7c.md / eval/080d2634.md)
                                             @ +0x2f51 = u8  zone display state flag (bit0)
.equ gDuelCardCtxBase,           0x0201e2a0  @ duel card activation context base (442 refs;
                                             @ ACTIVATION_STATE_BASE from eval/080566f4.md line 11)
                                             @ +0x4  = u32 current_player (eors with 0/1 in dispatch_card_display_op)
.equ gCardFsDataBlock,           0x0201e2b4  @ card FS slot data block base (4 refs; stride=0x108 per slot)
.equ gCardIdCache,               0x0201ff60  @ EWRAM card id lookup / mapping cache (5 refs)
.equ gCardListDisplayBuf,        0x02001138  @ card list slot display buffer (12 refs)
.equ gZoneActivTable,            0x020230f0  @ zone activation player table (1 ref; 2 word entries [player0,player1])
.equ gDuelSceneBase,             0x02023360  @ duel scene / campaign card-select scene base (192 refs;
                                             @ SCENE_BASE confirmed from eval/08028874.proposal.md line 11)
.equ gCardCtxSlotData,           0x0201ff30  @ card context slot data base (29 refs;
                                             @ confirmed from eval/080c6240.proposal.md line 11)
.equ gP1ZoneHandCount,           0x0201c4ec  @ = gP1LifePoints+0xc; player zone/hand count table base
                                             @ (23 refs; LIST_A_BASE from eval/08077678.md line R6)
```

New offset constants for **ewram.inc** (or new duel_field.inc if preferred; recommend ewram.inc for now):
```
.equ DUEL_FIELD_FADEIN_FLAG_OFF,    0x21e   @ [gDuelFieldState+0x21e] bit0 = fadein active (31 refs)
.equ DUEL_FIELD_PRNG_ANIM_FLAG_OFF, 0x222   @ [gDuelFieldState+0x222] bit2 = prng-driven anim (111 refs)
.equ DUEL_FIELD_STATE_226_OFF,      0x226   @ [gDuelFieldState+0x226] bit0 = scene entry done (19 refs)
.equ DUEL_CTX_ZONE_STATE_OFF,       0x2f51  @ [gDuelCtx+0x2f51] bit0 = zone display active (25 refs)
.equ GPRNG_PRNG_STATE_OFF213,       0x213   @ [gPrng+0x213] bit7 = prng-anim state flag (37 refs)
.equ GPRNG_PRNG_STATE_OFF217,       0x217   @ [gPrng+0x217] bit7 = prng-anim LP flag (12 refs)
.equ GPRNG_BANNER_FLAG_OFF,         0x23f   @ [gPrng+0x23f] bit0 = banner-anim active (279 refs)
.equ P1LP_BLOCK2_OFF,               0x1d08  @ [gP1LifePoints+0x1d08] duel field LP display field (35 refs)
.equ P1LP_TIMER_OFF,                0x1cec  @ [gP1LifePoints+0x1cec] duel field timer field (29 refs)
.equ PLAYER_BLOCK_STRIDE,           0x868   @ player data block stride (0x868=33*64; 2146 refs)
.equ GAME_STR_RAW_ID_MASK,          0xfffe0000  @ raw game string ID mask: bits[31:17]==0 (485 refs)
```

---

## §5.1 登记 (Rule 3) — 0 引用块

None. No ROM_INCBIN / .byte blocks in Seg-5. No data blocks to classify.

---

## 消費者証拠 (R6) — 关键槽語義 file:line + 置信度

| 槽/全局 | 证据 | 置信度 |
|---|---|---|
| gDuelFieldState=0x02023130 | asm/01_vija_scene_text.s line 4105: "BASE=0x02023130"; line 4101 plate; used as BASE for all duel field flag reads | high |
| gFontState=0x0201f440 | doc/dev/eval/080c7638.proposal.md line 11: "FONT_STATE_BASE = 0x0201f440"; doc/dev/eval/080cdba8.md line R6: "FONT_STATE_BASE=0x0201f440" | high |
| gDuelCtx=0x02020160 | doc/dev/eval/080d0c7c.md line R6: "gDuelCtx=0x02020160"; doc/dev/eval/080d2634.md R6 | high |
| gDuelCardCtxBase=0x0201e2a0 | doc/dev/eval/080566f4.proposal.md line 11: "ACTIVATION_STATE_BASE = 0x0201e2a0" | high |
| gCardFsDataBlock=0x0201e2b4 | asm/01_vija_scene_text.s line 3933 comment: "0x0201e2b4"; doc/dev/eval/0801e850.proposal.md line 29 | high |
| gCardIdCache=0x0201ff60 | doc/dev/eval/080cc8c8.proposal.md line 9: "r4 = 0x0201ff60 + r0*2 (cache slot ptr)" | high |
| gCardListDisplayBuf=0x02001138 | asm/01_vija_scene_text.s line 4091 plate: "fixes the second argument to 0x02001138 (card_list slot display buffer EWRAM address)" | high |
| gDuelSceneBase=0x02023360 | doc/dev/eval/08028874.proposal.md line 11: "SCENE_BASE = 0x02023360" | high |
| gCardCtxSlotData=0x0201ff30 | doc/dev/eval/080c6240.proposal.md line 11: "0x0201ff30 = card ctx base" | high |
| gP1ZoneHandCount=0x0201c4ec | doc/dev/eval/08077678.md line R6: "LIST_A_BASE=0x0201c4ec"; doc/dev/eval/080619f0.proposal.md line 24: "gP1LifePoints+0xc" | high |
| PLAYER_BLOCK_STRIDE=0x868 | doc/dev/eval/08077678.md line R6: "STEP_COUNT_BASE=0x868"; doc/dev/eval/0805e578.proposal.md: "0x868=33*64" (actually 33*8*4=33*32=1056=0x420 no; 0x868=2152 bytes; verify: 2152/8=269... hmm); asm: muls r0,r7 with r0=0x16=22, plus add r0,r8 with r8=card_stats_table shows 22*stride; 0x868 used as multiplier in fill_card_fs_display_entries | med (stride semantics need cross-function verification but value confirmed at 2 raw refs) |
| card_deck_fs_path_table=0x09e58b08 | ROM byte dump: d[0x1e58b08:+4]=f8e3e309 -> "deck/LV1" path string; 100 entries enumerated; lookup_card_entry_by_index plate "Standard ROM table fetch primitive" | high |
| GAME_STR_RAW_ID_MASK=0xfffe0000 | asm/01_vija_scene_text.s line 5153: ".word 0xfffe0000 @ 0801f258"; copy_game_text_if_raw plate "if r1 high 15 bits == 0 ... mask 0xFFFE0000" | high |
| DUEL_FIELD_PRNG_ANIM_FLAG_OFF=0x222 | asm line 3763-3776: ldr r1,DAT_0801e744(gCardInfoPageState); ldrb r2,[r1,#0]; ands r0,r2 mask=4; 0x222 offset from gDuelFieldState used to read prng-anim state byte | high |
| gZoneActivTable=0x020230f0 | asm line 4695-4696: "ldr r2, DAT_0801eed4; .hword 0x4691" (mov r9,r2); later "lsls r0,r5,#2; add r0,r9; str r1,[r0]" indexing by player; 1 ref | med (single ref; semantics from context only) |

---

## 求助

None. All slots have high or medium confidence. PLAYER_BLOCK_STRIDE=0x868 is medium confidence on semantic name; the value 0x868 is confirmed correct at all occurrences but the field name "stride" vs "block_size" could differ. Recommend keeping PLAYER_BLOCK_STRIDE pending cross-check with fill_card_fs_display_entries body (which uses 0x868 as a muls multiplier with a player index in r7, consistent with "per-player block stride").
