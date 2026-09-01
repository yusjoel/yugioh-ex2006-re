# Refine Proposal: F13-Seg-4 [0x080a0840..0x080a1658)

## 冻结输入与范围

- 严格范围: `[0x080a0840,0x080a1658)`, `3608` bytes (`0xe18`).
- 当前汇编: `asm/13_equip_placement.s`, SHA256 `121004fdbfcc154d2677d5e04263e6f2e6039c9e59f56e31a07f9242923fd42b`.
- 原 ROM: `roms/2343.gba`, SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`.
- Ghidra 前态通过一次 `-noanalysis -readOnly` 合并查询取得；`f13-seg4-preflight2-db-before.json` 与 `...after.json` 的 15/15 文件哈希逐项相同。第一次命令行过长的未启动尝试保留在 `f13-seg4-preflight.log`，没有打开项目。
- 本提案不分析 0x080a1658 起的 Seg-5。

## 段测绘

### 函数入口

| 入口 | 当前名 | Ghidra ID/source | body | incoming |
|---|---|---|---|---|
| 0x080a0840 | `update_equip_sprite_state_by_slot_status` | `6136` / `USER_DEFINED` | `[[080a0840, 080a0873] [080a0880, 080a08d1] [080a08e4, 080a08f9]]`; 156 B; SHA256 `1d292dff44efe342d90423b233ef822b3f1e78b9565013a4ab1cd6b2d5ea9a5c` | 080a0a9c UNCONDITIONAL_CALL/DEFAULT |
| 0x080a08fc | `dispatch_equip_effect_by_slot_state` | `16935` / `USER_DEFINED` | `[[080a08fc, 080a093b] [080a0948, 080a099b] [080a09b0, 080a09c5]]`; 170 B; SHA256 `0893b29c409a1c37f603154e0ce80efe8e84f4d5d67991eda2a1bfe583557d91` | 080a0abe UNCONDITIONAL_CALL/DEFAULT |
| 0x080a09c8 | `dispatch_equip_lp_delta_by_slot_status` | `16719` / `USER_DEFINED` | `[[080a09c8, 080a09fb] [080a0a08, 080a0a57] [080a0a68, 080a0a89]]`; 166 B; SHA256 `b1d785ece5f4fb614452cd37f5ab94060330b3adc38ecc43cc02d486afb7cf44` | 080a0af4 UNCONDITIONAL_CALL/DEFAULT |
| 0x080a0a8c | `route_equip_slot_tick_by_flag` | `16720` / `USER_DEFINED` | `[[080a0a8c, 080a0aad] [080a0ab8, 080a0b11]]`; 124 B; SHA256 `eb12f28ba4205c1d7e45c63355e9ee495052cfce822acbb1c992082c16f70e8f` | 080a0b16 UNCONDITIONAL_CALL/DEFAULT |
| 0x080a0b14 | `tick_equip_slot_activation_step` | `16721` / `USER_DEFINED` | `[[080a0b14, 080a0b1f]]`; 12 B; SHA256 `a663bf8c01ecdd8f61a6f68e8ccdc05c7bfff97d971e18dd75b97bbb7965e9cf` | 08094d96 UNCONDITIONAL_CALL/DEFAULT |
| 0x080a1338 | `tick_equip_zone_sprite_phase_a` | `16722` / `USER_DEFINED` | `[[080a1338, 080a1375] [080a1388, 080a1401] [080a1414, 080a1465] [080a1474, 080a1489] [080a1498, 080a14bf] [080a14c4, 080a14fb] [080a1508, 080a1521]]`; 410 B; SHA256 `3b41c6f026ceba1bf0728355dbb91cae91a2b9e3ea9b61f8e408a6c2a169b6cd` | none |
| 0x080a1524 | `tick_equip_zone_sprite_phase_b` | `16723` / `USER_DEFINED` | `[[080a1524, 080a1551] [080a1568, 080a159f] [080a15b0, 080a15f7] [080a1604, 080a161b] [080a1624, 080a164b] [080a1650, 080a1657]]`; 246 B; SHA256 `bdf1d0f1f29bc94f2a91dd9d6d58e12401f7dd8f6e16f62d76c94e743945913c` | none |

- 实测 7 个 Function objects；7 个均以 `push` 开始，无额外非-push Function entry。
- 0x080a1338 与 0x080a1524 的 Ghidra incoming 均为空；全 ROM 对其偶地址/THUMB|1 扫描没有形成可验证的函数指针引用。

### 残留自动名槽

- 57 个 4-byte 槽，当前类型为 14 `DAT_` + 43 `DWORD_`; 57/57 均为 DefinedData `/undefined4`。
- 59 个消费者均由 Thumb literal-LDR 编码重算命中槽地址；0x080a099c 与 0x080a1404 各有两个真实 LDR，其余各一个。
- 动作按地址唯一覆盖: EQ=34, REF=16, RENAME=7。所有现有槽标签均为 DEFAULT 自动标签。

### ROM_INCBIN / .byte 块

| 块 | 大小 | 当前投影 |
|---|---:|---|
| 0x080a0b20..0x080a1338 | 0x818 (2072 B) | `ROM_INCBIN 0xa0b20, 0x818` |

除此块外，本段没有 `ROM_INCBIN` 或 `.byte` 块；函数间 `.zero 2` 是对齐填充，不是裸块。

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|---|---|---|---|
| 0x080a0b20..0x080a1338 | entry 0 / 0; exhaustive interior sliding scan raw=391, thumb=367, verified refs=0 | §5.1 | 入口 0x080a0b20 的 raw 与 odd 值在全 ROM 均为 0。递归 Thumb 解码从唯一入口覆盖 822 条指令/1754 B、71 个 literal words/284 B、17 个 2-byte zero padding/34 B，合计 2072 B。758 个逐半字滑窗命中没有一个源地址等于当前 asm 的真实机器行或结构化数据行；它们来自 module24 内嵌数据/后代码资产或未对齐代码窗口。0x09d34758 是编码资产字节；0x09ea37b4 指向 literal word 0x080a1330，不是入口。Ghidra 前态 2072/2072 均为 undefined DataDB1，无 Function/Instruction/DefinedData/ref。 |

块有 55 个静态 BL 出边，指向 18 个去重已命名 callee，并在 0x080a131c 使用块内共享退出；这些是出边，不构成块入口引用。根据 Rule 3 保留原 `ROM_INCBIN` 并登记 §5.1，不执行 R4/R7。完整碰撞证据见 `f13-seg4-block-refscan-filtered.json`。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

四元组为 `(slot, value, const_name, slot_label)`。

| slot | value | const_name | slot_label | 定义 | 真实消费者 | EOL |
|---|---|---|---|---|---|---|
| 0x080a087c | 0x0000030d | `SPRITE_ROW_ENTRY_30D_OFF` | `sprite_row_entry_30d_off_080a087c` | REUSE `constants/ewram.inc:618` | 0x080a0860 (asm/13_equip_placement.s:6668) | `SPRITE_ROW_ENTRY_30D_OFF: gSpriteAttrBuf control byte for status path A.` |
| 0x080a08d8 | 0x00000484 | `EQUIP_ACTIVE_CTX_OFF` | `equip_active_ctx_off_080a08d8` | REUSE `constants/duel_field.inc:365` | 0x080a089c (asm/13_equip_placement.s:6701) | `EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.` |
| 0x080a08e0 | 0x0000030d | `SPRITE_ROW_ENTRY_30D_OFF` | `sprite_row_entry_30d_off_080a08e0` | REUSE `constants/ewram.inc:618` | 0x080a08c4 (asm/13_equip_placement.s:6721) | `SPRITE_ROW_ENTRY_30D_OFF: gSpriteAttrBuf control byte for status path A.` |
| 0x080a0944 | 0x0000030e | `SPRITE_ROW_ENTRY_30E_OFF` | `sprite_row_entry_30e_off_080a0944` | REUSE `constants/ewram.inc:619` | 0x080a0928 (asm/13_equip_placement.s:6783) | `SPRITE_ROW_ENTRY_30E_OFF: gSpriteAttrBuf control byte for status path B.` |
| 0x080a09a0 | 0x000004b4 | `EQUIP_ACTIVATION_AUX_OFF` | `equip_activation_aux_off_080a09a0` | REUSE `constants/duel_field.inc:358` | 0x080a0958 (asm/13_equip_placement.s:6809) | `EQUIP_ACTIVATION_AUX_OFF: gDuelPhaseFlags equip activation auxiliary field.` |
| 0x080a09a4 | 0x00000484 | `EQUIP_ACTIVE_CTX_OFF` | `equip_active_ctx_off_080a09a4` | REUSE `constants/duel_field.inc:365` | 0x080a0966 (asm/13_equip_placement.s:6817) | `EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.` |
| 0x080a09ac | 0x0000030e | `SPRITE_ROW_ENTRY_30E_OFF` | `sprite_row_entry_30e_off_080a09ac` | REUSE `constants/ewram.inc:619` | 0x080a098e (asm/13_equip_placement.s:6837) | `SPRITE_ROW_ENTRY_30E_OFF: gSpriteAttrBuf control byte for status path B.` |
| 0x080a0a04 | 0x0000030f | `SPRITE_ROW_ENTRY_30F_OFF` | `sprite_row_entry_30f_off_080a0a04` | REUSE `constants/ewram.inc:620` | 0x080a09e8 (asm/13_equip_placement.s:6891) | `SPRITE_ROW_ENTRY_30F_OFF: gSpriteAttrBuf control byte for LP-delta path.` |
| 0x080a0a5c | 0x00000484 | `EQUIP_ACTIVE_CTX_OFF` | `equip_active_ctx_off_080a0a5c` | REUSE `constants/duel_field.inc:365` | 0x080a0a2e (asm/13_equip_placement.s:6929) | `EQUIP_ACTIVE_CTX_OFF: gDuelPhaseFlags current effect-entry pointer.` |
| 0x080a0a64 | 0x0000030f | `SPRITE_ROW_ENTRY_30F_OFF` | `sprite_row_entry_30f_off_080a0a64` | REUSE `constants/ewram.inc:620` | 0x080a0a4a (asm/13_equip_placement.s:6942) | `SPRITE_ROW_ENTRY_30F_OFF: gSpriteAttrBuf control byte for LP-delta path.` |
| 0x080a0ab4 | 0x00000301 | `SPRITE_ROW_BUSY_BYTE_OFF` | `sprite_row_busy_byte_off_080a0ab4` | REUSE `constants/ewram.inc:617` | 0x080a0a90 (asm/13_equip_placement.s:6987) | `SPRITE_ROW_BUSY_BYTE_OFF: gSpriteAttrBuf busy and route flag byte.` |
| 0x080a137c | 0x00001d8c | `EQUIP_CONTEXT_PLAYER_OFF` | `equip_context_player_off_080a137c` | NEW `constants/duel_field.inc` | 0x080a1346 (asm/13_equip_placement.s:7093) | `EQUIP_CONTEXT_PLAYER_OFF: gP1LifePoints-relative equip context player field.` |
| 0x080a1380 | 0x00001d98 | `EQUIP_REROLL_SPRITE_PARAM_OFF` | `equip_reroll_sprite_param_off_080a1380` | NEW `constants/duel_field.inc` | 0x080a134c (asm/13_equip_placement.s:7096) | `EQUIP_REROLL_SPRITE_PARAM_OFF: gP1LifePoints-relative coin/dice sprite parameter hword.` |
| 0x080a1384 | 0x00001d9a | `EQUIP_REROLL_COUNT_TARGET_OFF` | `equip_reroll_count_target_off_080a1384` | NEW `constants/duel_field.inc` | 0x080a1352 (asm/13_equip_placement.s:7099) | `EQUIP_REROLL_COUNT_TARGET_OFF: gP1LifePoints-relative packed reroll count/target hword.` |
| 0x080a1404 | 0x00001da8 | `LP_CARD_TRACK_BASE_OFF` | `lp_card_track_base_off_080a1404` | REUSE `constants/ewram.inc:247` | 0x080a1388 (asm/13_equip_placement.s:7128), 0x080a13e8 (asm/13_equip_placement.s:7179) | `LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.` |
| 0x080a1408 | 0x0000805b | `OAM_COIN_REROLL_SPRITE_P2_5B` | `oam_coin_reroll_sprite_p2_5b_080a1408` | NEW `constants/oam_attr.inc` | 0x080a13d6 (asm/13_equip_placement.s:7169) | `OAM_COIN_REROLL_SPRITE_P2_5B: P2-side coin-reroll sprite code; P1 uses inline 0x5b.` |
| 0x080a1410 | 0x00001d94 | `EQUIP_PHASE_DISPLAY_STATE_OFF` | `equip_phase_display_state_off_080a1410` | REUSE `constants/duel_field.inc:599` | 0x080a13f4 (asm/13_equip_placement.s:7184) | `EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.` |
| 0x080a1468 | 0x0000150f | `SECOND_COIN_TOSS_CID` | `second_coin_toss_cid_080a1468` | NEW `constants/card_info.inc` | 0x080a1414 (asm/13_equip_placement.s:7201) | `SECOND_COIN_TOSS_CID: Second Coin Toss internal CID.` |
| 0x080a1470 | 0x00001daa | `LP_CARD_TRACK_NEXT_OFF` | `lp_card_track_next_off_080a1470` | REUSE `constants/ewram.inc:248` | 0x080a1444 (asm/13_equip_placement.s:7223) | `LP_CARD_TRACK_NEXT_OFF: adjacent gP1LifePoints scratch hword.` |
| 0x080a148c | 0x0000011f | `GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID` | `game_str_perform_coin_toss_again_id_080a148c` | NEW `constants/duel_field.inc` | 0x080a1474 (asm/13_equip_placement.s:7250) | `GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID: game string 287: Perform coin toss again?.` |
| 0x080a1494 | 0x00001d94 | `EQUIP_PHASE_DISPLAY_STATE_OFF` | `equip_phase_display_state_off_080a1494` | REUSE `constants/duel_field.inc:599` | 0x080a147c (asm/13_equip_placement.s:7254) | `EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.` |
| 0x080a14c0 | 0x0000150f | `SECOND_COIN_TOSS_CID` | `second_coin_toss_cid_080a14c0` | NEW `constants/card_info.inc` | 0x080a14a4 (asm/13_equip_placement.s:7275) | `SECOND_COIN_TOSS_CID: Second Coin Toss internal CID.` |
| 0x080a1504 | 0x00001daa | `LP_CARD_TRACK_NEXT_OFF` | `lp_card_track_next_off_080a1504` | REUSE `constants/ewram.inc:248` | 0x080a14d0 (asm/13_equip_placement.s:7296) | `LP_CARD_TRACK_NEXT_OFF: adjacent gP1LifePoints scratch hword.` |
| 0x080a1558 | 0x00001d8c | `EQUIP_CONTEXT_PLAYER_OFF` | `equip_context_player_off_080a1558` | NEW `constants/duel_field.inc` | 0x080a1528 (asm/13_equip_placement.s:7358) | `EQUIP_CONTEXT_PLAYER_OFF: gP1LifePoints-relative equip context player field.` |
| 0x080a155c | 0x00001d98 | `EQUIP_REROLL_SPRITE_PARAM_OFF` | `equip_reroll_sprite_param_off_080a155c` | NEW `constants/duel_field.inc` | 0x080a152e (asm/13_equip_placement.s:7361) | `EQUIP_REROLL_SPRITE_PARAM_OFF: gP1LifePoints-relative coin/dice sprite parameter hword.` |
| 0x080a1560 | 0x00001d9a | `EQUIP_REROLL_COUNT_TARGET_OFF` | `equip_reroll_count_target_off_080a1560` | NEW `constants/duel_field.inc` | 0x080a1534 (asm/13_equip_placement.s:7364) | `EQUIP_REROLL_COUNT_TARGET_OFF: gP1LifePoints-relative packed reroll count/target hword.` |
| 0x080a1564 | 0x00001d94 | `EQUIP_PHASE_DISPLAY_STATE_OFF` | `equip_phase_display_state_off_080a1564` | REUSE `constants/duel_field.inc:599` | 0x080a153c (asm/13_equip_placement.s:7368) | `EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.` |
| 0x080a15a0 | 0x00001da8 | `LP_CARD_TRACK_BASE_OFF` | `lp_card_track_base_off_080a15a0` | REUSE `constants/ewram.inc:247` | 0x080a156c (asm/13_equip_placement.s:7393) | `LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.` |
| 0x080a15a4 | 0x0000805c | `OAM_DICE_REROLL_SPRITE_P2_5C` | `oam_dice_reroll_sprite_p2_5c_080a15a4` | NEW `constants/oam_attr.inc` | 0x080a1584 (asm/13_equip_placement.s:7405) | `OAM_DICE_REROLL_SPRITE_P2_5C: P2-side dice-reroll sprite code; P1 uses inline 0x5c.` |
| 0x080a15ac | 0x00001d94 | `EQUIP_PHASE_DISPLAY_STATE_OFF` | `equip_phase_display_state_off_080a15ac` | REUSE `constants/duel_field.inc:599` | 0x080a159a (asm/13_equip_placement.s:7417) | `EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.` |
| 0x080a15f8 | 0x000016a5 | `DICE_RE_ROLL_CID` | `dice_re_roll_cid_080a15f8` | NEW `constants/card_info.inc` | 0x080a15b0 (asm/13_equip_placement.s:7429) | `DICE_RE_ROLL_CID: Dice Re-Roll internal CID.` |
| 0x080a1600 | 0x00001da8 | `LP_CARD_TRACK_BASE_OFF` | `lp_card_track_base_off_080a1600` | REUSE `constants/ewram.inc:247` | 0x080a15e8 (asm/13_equip_placement.s:7455) | `LP_CARD_TRACK_BASE_OFF: gP1LifePoints scratch hword base reused by reroll animation.` |
| 0x080a1620 | 0x00001d94 | `EQUIP_PHASE_DISPLAY_STATE_OFF` | `equip_phase_display_state_off_080a1620` | REUSE `constants/duel_field.inc:599` | 0x080a160e (asm/13_equip_placement.s:7476) | `EQUIP_PHASE_DISPLAY_STATE_OFF: gP1LifePoints equip display phase state word.` |
| 0x080a164c | 0x000016a5 | `DICE_RE_ROLL_CID` | `dice_re_roll_cid_080a164c` | NEW `constants/card_info.inc` | 0x080a1630 (asm/13_equip_placement.s:7495) | `DICE_RE_ROLL_CID: Dice Re-Roll internal CID.` |

### REF_SLOTS

四元组为 `(slot, target, gas_label, slot_label)`。每项保留槽的 Data4 与 incoming READ；在 operand 0 建 DATA/USER_DEFINED 引用。

| slot | target | gas_label | slot_label | 真实消费者 | EOL |
|---|---|---|---|---|---|
| 0x080a0874 | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a0874` | 0x080a0842 (asm/13_equip_placement.s:6652) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0878 | 0x0201b590 | `gEffectEntryArray` | `effect_entry_array_ref_080a0878` | 0x080a0852 (asm/13_equip_placement.s:6660) | `gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a08d4 | 0x0201b290 | `gDuelPhaseFlags` | `duel_phase_flags_ref_080a08d4` | 0x080a089a (asm/13_equip_placement.s:6700) | `gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a08dc | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a08dc` | 0x080a08c2 (asm/13_equip_placement.s:6720) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a093c | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a093c` | 0x080a08fe (asm/13_equip_placement.s:6758) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0940 | 0x0201b590 | `gEffectEntryArray` | `effect_entry_array_ref_080a0940` | 0x080a090e (asm/13_equip_placement.s:6768) | `gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a099c | 0x0201b290 | `gDuelPhaseFlags` | `duel_phase_flags_ref_080a099c` | 0x080a094e (asm/13_equip_placement.s:6804), 0x080a0964 (asm/13_equip_placement.s:6816) | `gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a09a8 | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a09a8` | 0x080a098c (asm/13_equip_placement.s:6836) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a09fc | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a09fc` | 0x080a09ca (asm/13_equip_placement.s:6875) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0a00 | 0x0201b590 | `gEffectEntryArray` | `effect_entry_array_ref_080a0a00` | 0x080a09da (asm/13_equip_placement.s:6883) | `gEffectEntryArray: 0x18-byte effect entry array base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0a58 | 0x0201b290 | `gDuelPhaseFlags` | `duel_phase_flags_ref_080a0a58` | 0x080a0a2c (asm/13_equip_placement.s:6928) | `gDuelPhaseFlags: duel phase and equip activation state base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0a60 | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a0a60` | 0x080a0a48 (asm/13_equip_placement.s:6941) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a0ab0 | 0x0201b870 | `gSpriteAttrBuf` | `sprite_attr_buf_ref_080a0ab0` | 0x080a0a8e (asm/13_equip_placement.s:6986) | `gSpriteAttrBuf: sprite attribute buffer base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a146c | 0x0201e2a0 | `gDuelCardCtxBase` | `duel_card_ctx_ref_080a146c` | 0x080a1434 (asm/13_equip_placement.s:7215) | `gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a14fc | 0x0201e2a0 | `gDuelCardCtxBase` | `duel_card_ctx_ref_080a14fc` | 0x080a14c4 (asm/13_equip_placement.s:7290) | `gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.` |
| 0x080a15fc | 0x0201e2a0 | `gDuelCardCtxBase` | `duel_card_ctx_ref_080a15fc` | 0x080a15d2 (asm/13_equip_placement.s:7444) | `gDuelCardCtxBase: duel card activation context base; add operand-0 DATA/USER_DEFINED reference.` |

目标对象前态与实施约束:

- `gDuelPhaseFlags` 0x0201b290: LABEL/USER_DEFINED/primary ID 25230, `/undefined2`.
- `gEffectEntryArray` 0x0201b590: 当前 DEFAULT dynamic `DAT_0201b590`, ID 4611686018461054352, `/undefined2`; 将同一主对象规范为全局 USER_DEFINED `gEffectEntryArray`，不得新建同址 alias，不得创建 RAM Data。
- `gSpriteAttrBuf` 0x0201b870: LABEL/USER_DEFINED/primary ID 21747, `/undefined2`.
- `gDuelCardCtxBase` 0x0201e2a0: LABEL/USER_DEFINED/primary ID 18879, `/undefined4`.
- REF 槽前态没有 operand-0 outgoing refs；精确新增目标 DATA/USER_DEFINED ref，保留所有非目标引用与 Data4。

### RENAME_SLOTS

三元组为 `(slot, slot_label, eol_ascii)`。这些槽已有正确 operand-0 DATA/USER_DEFINED 引用，禁止删除或重建。

| slot | old -> new | EOL | 真实消费者 |
|---|---|---|---|
| 0x080a1378 | `DWORD_080a1378` -> `gp1lp_ptr_080a1378` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a1344 (asm/13_equip_placement.s:7092) |
| 0x080a140c | `DWORD_080a140c` -> `gp1lp_ptr_080a140c` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a13e6 (asm/13_equip_placement.s:7178) |
| 0x080a1490 | `DWORD_080a1490` -> `gp1lp_ptr_080a1490` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a147a (asm/13_equip_placement.s:7253) |
| 0x080a1500 | `DWORD_080a1500` -> `gp1lp_ptr_080a1500` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a14ce (asm/13_equip_placement.s:7295) |
| 0x080a1554 | `DWORD_080a1554` -> `gp1lp_ptr_080a1554` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a1526 (asm/13_equip_placement.s:7357) |
| 0x080a15a8 | `DWORD_080a15a8` -> `gp1lp_ptr_080a15a8` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a1598 (asm/13_equip_placement.s:7416) |
| 0x080a161c | `DWORD_080a161c` -> `gp1lp_ptr_080a161c` | `gP1LifePoints base; preserve existing operand-0 DATA/USER_DEFINED reference.` | 0x080a160c (asm/13_equip_placement.s:7475) |

- 7 项引用均指向 `gP1LifePoints` 0x0201c4e0，目标 LABEL/USER_DEFINED/primary ID 15545，`/undefined4`。现有引用均为 operand0 DATA/USER_DEFINED/primary。

### FUNC_RENAME

- 无。7 个当前函数名与实测职责一致。

### PLATE

全部执行 full replace。文本为 ASCII，最长 461 chars；函数 ID/body/incoming 保持前态。

#### 0x080a0840 `update_equip_sprite_state_by_slot_status`

- Guard: Function ID `6136`, body SHA256 `1d292dff44efe342d90423b233ef822b3f1e78b9565013a4ab1cd6b2d5ea9a5c`, old PLATE SHA256 `c3ca9fd4c72c7057227e833d124c64a02d7f10221e8ecb3f705a6c74bb293ce6` (728 chars).
- New PLATE:

```text
No arguments. Uses gSpriteAttrBuf+0x310 as the effect-entry count and gEffectEntryArray stride 0x18. Control byte +0x30d selects initialization, handler, or sprite-row paths. The handler stores the current entry at gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF, calls invoke_card_effect_node_handler(current, previous), records the result sign, and advances the control byte. Returns 0 only after the handler path; otherwise 1. Caller: route_equip_slot_tick_by_flag.
```

#### 0x080a08fc `dispatch_equip_effect_by_slot_state`

- Guard: Function ID `16935`, body SHA256 `0893b29c409a1c37f603154e0ce80efe8e84f4d5d67991eda2a1bfe583557d91`, old PLATE SHA256 `05fc115a4d52010c4416579efabca6cf221a8cc7ec571891ae0d2faa47b769d1` (572 chars).
- New PLATE:

```text
No arguments. Uses gSpriteAttrBuf+0x310 and gEffectEntryArray stride 0x18. Control byte +0x30e selects initialization, invoke_effect_node_action_if_found, or sprite-row 0x1b. Initialization clears two gDuelPhaseFlags fields. The handler stores the current entry at +EQUIP_ACTIVE_CTX_OFF, updates entry byte +4 bit 0, and advances the control byte. Returns 0 after the handler path; otherwise 1. Caller: route_equip_slot_tick_by_flag.
```

#### 0x080a09c8 `dispatch_equip_lp_delta_by_slot_status`

- Guard: Function ID `16719`, body SHA256 `b1d785ece5f4fb614452cd37f5ab94060330b3adc38ecc43cc02d486afb7cf44`, old PLATE SHA256 `c211f02e211462571e62e4f5229f8b4f47ab8cccce7211ce4b0c153b5af0059e` (708 chars).
- New PLATE:

```text
No arguments. Uses gSpriteAttrBuf+0x310 and gEffectEntryArray stride 0x18. Control byte +0x30f selects initialization, LP-delta handling, or sprite-row 0x19. The handler stores the current entry at gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF, calls apply_equip_lp_delta_by_node_flag(current, previous), stores the result at +0x4a0, and advances only when the result is zero. Returns 0 after the handler path; otherwise 1.
```

#### 0x080a0a8c `route_equip_slot_tick_by_flag`

- Guard: Function ID `16720`, body SHA256 `eb12f28ba4205c1d7e45c63355e9ee495052cfce822acbb1c992082c16f70e8f`, old PLATE SHA256 `f6a70a0bfcfd704972e78e05c59543a28363de525652148951f5d77e9cc27581` (679 chars).
- New PLATE:

```text
No arguments. Reads gSpriteAttrBuf+SPRITE_ROW_BUSY_BYTE_OFF. In order, it services flag 0x10 with update_equip_sprite_state_by_slot_status, flag 0x20 with dispatch_equip_effect_by_slot_state, gSpriteAttrBuf+0x300 flag 0x10 with dispatch_equip_slot_state_by_index, and flag 0x40 with dispatch_equip_lp_delta_by_slot_status. Completed handlers clear their flag. Returns 1 after a selected handler and 0 when no relevant flag is set.
```

#### 0x080a0b14 `tick_equip_slot_activation_step`

- Guard: Function ID `16721`, body SHA256 `a663bf8c01ecdd8f61a6f68e8ccdc05c7bfff97d971e18dd75b97bbb7965e9cf`, old PLATE SHA256 `ae6f59578b7d30e02fc0dc25d49ad19bb7bbd49e06919168827969e7f765113b` (385 chars).
- New PLATE:

```text
No arguments. Calls route_equip_slot_tick_by_flag, discards its return value, and always returns 0. Called once from tick_equip_activation_main_sequence at 0x08094d96.
```

#### 0x080a1338 `tick_equip_zone_sprite_phase_a`

- Guard: Function ID `16722`, body SHA256 `3b41c6f026ceba1bf0728355dbb91cae91a2b9e3ea9b61f8e408a6c2a169b6cd`, old PLATE SHA256 `e0b8117f89f7797ca8fc48f4b9243f6a7b8bd9b56db6ae904ac52cf97e351a64` (1367 chars).
- New PLATE:

```text
No APCS arguments; r8-r10 are inherited context. Drives the three-state Second Coin Toss reroll display at gP1LifePoints+0x1d94. State 0 builds coin sprite records from the packed parameters at +0x1d98/+0x1d9a. State 1 checks CID 0x150f, issues game string 287 when confirmation is needed, and advances. State 2 enqueues the zone sprite and resets the display phase state. Other states return 1. No incoming call or pointer reference is defined in the current image.
```

#### 0x080a1524 `tick_equip_zone_sprite_phase_b`

- Guard: Function ID `16723`, body SHA256 `bdf1d0f1f29bc94f2a91dd9d6d58e12401f7dd8f6e16f62d76c94e743945913c`, old PLATE SHA256 `1874e99d8c40bf2c8cb9dfc22afb9c9ca39c7795912b75ad8bcc2fefd522c052` (1293 chars).
- New PLATE:

```text
No APCS arguments; r8-r10 are inherited context. Drives the three-state Dice Re-Roll display at gP1LifePoints+0x1d94. State 0 builds die sprite records from +0x1d98/+0x1d9a. State 1 checks CID 0x16a5 in zone 11 for modes 1 and 2, issues game string 288 when confirmation is needed, and advances. State 2 enqueues the equip-zone sprite and resets the display phase state. Other states return 1. No incoming call or pointer reference is defined in the current image.
```

## carve 计划 (R7)

- 无。

## disasm 计划 (R4)

- 无。0x080a0b20 块按 Rule 3 登记 §5.1。

## 新增 constants / 全局

### 新增 constants

| value | name | 目标文件 | 证据 / C5 |
|---|---|---|---|
| 0x0000011f | `GAME_STR_PERFORM_COIN_TOSS_AGAIN_ID` | `constants/duel_field.inc` | game string 287: Perform coin toss again?. text/game-strings/en.txt:874-875 maps index 287 (0x11f) to the exact prompt. |
| 0x0000150f | `SECOND_COIN_TOSS_CID` | `constants/card_info.inc` | Second Coin Toss internal CID. data.md:1067 logical CID column; card-stats.s:14081-14083; card-passcodes.s:1104. |
| 0x000016a5 | `DICE_RE_ROLL_CID` | `constants/card_info.inc` | Dice Re-Roll internal CID. data.md:1372 logical CID column; card-stats.s:18111-18113; card-passcodes.s:1414. |
| 0x00001d8c | `EQUIP_CONTEXT_PLAYER_OFF` | `constants/duel_field.inc` | gP1LifePoints-relative equip context player field. 现有同值 `NAME_INPUT_BG1CNT_INIT` 属 GBA BG 控制寄存器域；本槽以 gP1LifePoints 为基址并作为 player 参数，域不同。 |
| 0x00001d98 | `EQUIP_REROLL_SPRITE_PARAM_OFF` | `constants/duel_field.inc` | gP1LifePoints-relative coin/dice sprite parameter hword. 当前 6039-definition value-first scan has no same-domain reusable definition. |
| 0x00001d9a | `EQUIP_REROLL_COUNT_TARGET_OFF` | `constants/duel_field.inc` | gP1LifePoints-relative packed reroll count/target hword. 当前 6039-definition value-first scan has no same-domain reusable definition. |
| 0x0000805b | `OAM_COIN_REROLL_SPRITE_P2_5B` | `constants/oam_attr.inc` | P2-side coin-reroll sprite code; P1 uses inline 0x5b. 当前 6039-definition value-first scan has no same-domain reusable definition. |
| 0x0000805c | `OAM_DICE_REROLL_SPRITE_P2_5C` | `constants/oam_attr.inc` | P2-side dice-reroll sprite code; P1 uses inline 0x5c. 当前 6039-definition value-first scan has no same-domain reusable definition. |

### 复用 definitions / globals

- `gSpriteAttrBuf`, `gEffectEntryArray`, `gDuelPhaseFlags`, `gP1LifePoints`, `gDuelCardCtxBase`.
- `SPRITE_ROW_ENTRY_30D_OFF`, `SPRITE_ROW_ENTRY_30E_OFF`, `SPRITE_ROW_ENTRY_30F_OFF`, `SPRITE_ROW_BUSY_BYTE_OFF`.
- `EQUIP_ACTIVE_CTX_OFF`, `EQUIP_ACTIVATION_AUX_OFF`, `EQUIP_PHASE_DISPLAY_STATE_OFF`, `LP_CARD_TRACK_BASE_OFF`, `LP_CARD_TRACK_NEXT_OFF`.

### NEW global

- 无新地址 global。0x0201b590 仅把既有 DEFAULT 主对象规范为已存在于 `constants/ewram.inc:358` 的 `gEffectEntryArray`。

## §5.1 登记 (Rule 3)

| block | bytes | refs | 分类 | 后续条件 |
|---|---:|---|---|---|
| 0x080a0b20..0x080a1338 | 2072 | entry raw=0, thumb=0; verified interior entry refs=0 | orphan Thumb body with pools and padding | 仅在后续发现真实外部入口引用时重新进入 R4；本次保留原 ROM_INCBIN。 |

## 消费者证据 (R6)

| 证据 | 结论 | 置信度 |
|---|---|---|
| asm/13_equip_placement.s:6652-6737 | 0x30d 状态函数用 gSpriteAttrBuf count/control、gEffectEntryArray stride 0x18 与 gDuelPhaseFlags+0x484。 | high |
| asm/13_equip_placement.s:6758-6854 | 0x30e 状态函数用相同 entry array，并写 +0x4b4 auxiliary state。 | high |
| asm/13_equip_placement.s:6875-6957 | 0x30f 状态函数把 apply_equip_lp_delta_by_node_flag 结果写 gDuelPhaseFlags+0x4a0。 | high |
| asm/13_equip_placement.s:6986-7055 | router 实测四个 flag 路径，包含旧 PLATE 漏记的 gSpriteAttrBuf+0x300 / dispatch_equip_slot_state_by_index 路径。 | high |
| asm/13_equip_placement.s:7092-7321 | phase A 从 +0x1d8c 取 player，从 +0x1d98/+0x1d9a 取 reroll sprite 参数；CID 0x150f 与 game string 0x11f 分属卡与文本域。 | high |
| asm/13_equip_placement.s:7357-7508 | phase B 使用同一 context fields、CID 0x16a5、P2 sprite code 0x805c，并以内联 0x120 触发 game string 288。 | high |
| doc/um06-deck-modification-tool/data.md:1067,1372 + card-stats/passcodes | ICID 0x150f=Second Coin Toss, 0x16a5=Dice Re-Roll；逻辑 CID、名字和 password 三方一致。 | high |

## 落地与守卫

1. 对 34 EQ 槽保留 Data4，添加单一 equate、USER_DEFINED slot label 与指定 EOL；ROM word 不变。
2. 对 16 REF 槽添加 USER_DEFINED slot label 和 operand0 DATA/USER_DEFINED ref；`gEffectEntryArray` 复用同一目标 symbol object。不得读取 RAM 值或重建 RAM Data。
3. 对 7 RENAME 槽只改 slot label/EOL；现有 gP1LifePoints DATA/USER_DEFINED ref 必须保持同一目标 ID/source/type。
4. 全量替换 7 个 PLATE；Function ID/name/body/ranges/incoming 保持。所有 EOL/PLATE 必须逐字 ASCII。
5. 0x080a0b20..0x080a1338 的 2072 个 Ghidra code units、symbols、refs、TMode 与原 `ROM_INCBIN` 投影全部保持。
6. 重导后静态投影必须与 `f13-seg4-static-projection.json` 的 57 项一致；本提案不要求 CSV/registry/function inventory 变化。

## 自检

- `f13-seg4-selfcheck.json`: `PASS`, 47 checks, 0 errors.
- 已实跑: 57/57 ROM words、59/59 LDR decoded targets、57 unique action coverage、34/16/7 counts、label regex/uniqueness、ASCII EOL/PLATE、PLATE <=500、Ghidra Data4/ref guards、C5 reuse/new checks、block SHA/flow coverage/refscan/Ghidra undefined state、15 DB read-only hashes。
- 可复跑入口: `Get-Content output/refine-run-20260831-194634/f13-seg4-generate-plan.txt -Raw | python -`。proposal 渲染入口为 `f13-seg4-render-proposal.txt`。

## 求助

- 无。
