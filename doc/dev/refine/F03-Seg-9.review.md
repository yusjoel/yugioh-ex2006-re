# Refine Review: F03-Seg-9

Seg range: `[0x0803d91c, 0x0803efcc)`, file `asm/03_equip_chain_hand.s`, 13 functions.
Review iteration: 1 (initial review).

## 核验结果 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五路线图一致 | PASS | 0x3d91c..0x3efcc 与 p5-refine-03-equip-chain-hand.md §三 表格 Seg-9 完全一致; 第一fn tick_zone_slot_transition_display_seq @ 0x0803d91c (asm 行 16737); 最后 fn tick_equip_node_chain_link_display_seq 末尾 DAT_0803efc8 @ 0x0803efc8, 下一fn tick_zone_desc_card_move_display_seq @ 0x0803efcc (asm 行 19811). 不回头不跳号. |
| C2 Rule2 | ROM_INCBIN/.byte 块 | PASS | 独立 awk 扫 asm 行 16737..19810: incbin/\.byte 计数 = 0. 段内无函数间裸 incbin. |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无 §5.1 登记块. |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立 python 核对 25 个关键槽 (PLAYER_BLOCK_STRIDE/DISPLAY_SEQ_STEP_LOCK_OFF/SLOT_BIT21_CLR/UNHAPPY_GIRL_CID_SHIFTED/DISPLAY_CTX_SLOT_DATA_MASK/BACKFIRE_CID/SOUL_ABSORPTION_CID/HUMAN_WAVE_TACTICS_CID/DUEL_FIELD_OAM_TILE_IDX_A/gDuelDisplaySeqState/gDuelChainStepCounter/gDuelFieldSlots/A_DEAL_WITH_DARK_RULER_CID/BOSS_RUSH_CID 等), 全部与 ROM 一致. |
| C5 R1 复用 | 新建前确无同值 | PASS | 5 个新建常量: UNHAPPY_GIRL_CID_SHIFTED(0xba180000)/BACKFIRE_CID(0x1762)/SOUL_ABSORPTION_CID(0x16da)/HUMAN_WAVE_TACTICS_CID(0x17b2)/DISPLAY_CTX_SLOT_DATA_MASK(0x7fff) 均独立 grep 全 20 个 constants/*.inc 确认无重复. DUEL_FIELD_OAM_TILE_IDX_A(0x814) 复用正确. 注: 三处复用常量的"所在 inc"列有文档误标 (见 NOTES). |
| C6 R2 名 | 槽名格式合规无碰撞 | PASS | RENAME labels: zone_card_place_switch_table_ptr / equip_node_chain_switch_table_ptr 均符合 ^[a-z][a-z0-9_]+$; 全局无碰撞. EQ slot labels (如 player_block_stride_d990) 格式合规. |
| C7 R3 接通 | carve/全局槽有 USER-label | PASS | 无 carve 块. 8 个 REF 全局均已在 ewram.inc 有 .equ 定义且 ROM 值核对一致; gP1LifePoints 5 个 PTR_ slots 已 Ghidra 自动命名. |
| C8 R5 现名 | plate 无残留 FUN_ | PASS | 独立扫 asm 行 16728..19810: 12 处 FUN_ substring 覆盖 10 个函数. 三个 stale 名均可查证现名: FUN_0803be4c→dispatch_duel_event_display_seq (asm 行 13193); FUN_0802f0d8→clear_zone_slot_card_ref_bits (asm/02 行 6400); FUN_0802ec3c→replace_chain_node_ref_by_zone_match (asm/02 行 5725). |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | 独立 python 扫 asm 行 16737..19810 全字符: non-ASCII = 0. |
| C10 carve | 指针表条目 +1 核对 | PASS | 两个 RENAME slots: DAT_0803e634=0x0803e638 (ROM 核对 OK, 偶地址 data table ptr, 不需 +1); DAT_0803eb7c=0x0803eb80 (ROM 核对 OK, 同理). |
| C11 误名 | 函数名无矛盾 | PASS | 13 个函数名与函数体操作交叉核查: 无矛盾信号. FUNC_RENAME=0 正确. |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | 消费者证据表对 8 个关键常量/全局各给出 asm 函数名/行号/指令序列/置信度; 卡牌 ID 均经 data/card-stats.s 坐实. BACKFIRE_CID 证据中 passcode 有一处笔误 (82705373 应为 82705573), 但槽值 0x1762 与 card-stats.s 一致. 无零容忍词. |
| C13 残留 | 所有 DAT_/PTR_ 均被覆盖 | PASS | 独立 grep 段内: DAT_ 定义 = 143, PTR_ 定义 = 5, 总计 148. EQ(70)+REF(76)+RENAME(2)=148. 100% 覆盖. 注: 提案页眉写"146 DAT_ + 2 PTR_"误, 应为 143+5, 但总量和覆盖率正确. |

---

## 自主复核要点

**C4 ROM 字节核对 (python 独立读)**

全部 25 个抽查槽与 ROM 小端值完全一致. 关键确认:
- 0x0803de78 = 0xba180000 = 0x1743<<19 (UNHAPPY_GIRL_CID_SHIFTED) OK
- 0x0803e0f8 = 0x00007fff (DISPLAY_CTX_SLOT_DATA_MASK) OK
- 0x0803ebcc = 0x00000814 (DUEL_FIELD_OAM_TILE_IDX_A reuse) OK

**C5 新常量验证**

- UNHAPPY_GIRL_CID_SHIFTED = 0xba180000: card_info.inc 现有 SANCTUARY_CID_SHIFTED=0xbaf00000 等, 0xba180000 未重复. lsls r0,r0,#0x13 + cmp 于 0x0803ddb2-0x0803ddb6 确认.
- BACKFIRE_CID = 0x1762: card-stats.s card_1547 slot=0x1762 pw=82705573. ROM 核对 0x0803e9f8/0x0803ee10 均为 0x00001762.
- SOUL_ABSORPTION_CID = 0x16da: card-stats.s card_1435 slot=0x16DA pw=68073522. ROM 核对 0x0803ea00/0x0803ee18 均为 0x000016da.
- HUMAN_WAVE_TACTICS_CID = 0x17b2: card-stats.s card_1606 slot=0x17B2 pw=30353551. ROM 核对 0x0803ee20 = 0x000017b2.
- DISPLAY_CTX_SLOT_DATA_MASK = 0x7fff: 全 20 constants/*.inc grep 无重复.

**C8 FUN_ 板注订正**

独立 awk 行范围 16728..19810 (含函数前置 plate 行): 12 处 FUN_ 均有对应现名. dispatch_duel_event_display_seq (FUN_0803be4c) 已在同文件 asm 行 13193. 另两处跨文件 FUN_ 已在 asm/02_text_lp_fieldspell.s 坐实.

**C13 槽计数**

独立 grep 确认 DAT_=143 / PTR_=5 / 总=148 = EQ(70)+REF(76)+RENAME(2) = 148.
ROM python 计数核对全部 REF 全局: gDuelDisplaySeqState=34 / gDuelFieldSlots=17 / gDuelChainStepCounter=2 / gDuelChainDescBase=7 / gDuelCardCtxBase=6 / gEquipChainSlotRefs=2 / gDuelEffectChainSlots=1 / gDuelFieldSlotState=2 / gP1LifePoints=5 = 76 REF 全部核对通过.

---

## NOTES (非阻断, fixer 落地时留意)

**N1 — "所在 inc" 列文档误标 (21 处, 非 C5 失败)**

下列复用常量在提案 EQ 表中"所在 inc"列写错:

| 常量名 | 提案写 | 实际位置 | 影响槽数 |
|--------|--------|----------|---------|
| PLAYER_BLOCK_STRIDE | constants/duel_field.inc | constants/ewram.inc | 18 |
| P1LP_BLOCK2_OFF_1CE8 | constants/duel_field.inc | constants/ewram.inc | 2 |
| SLOT_CARD_SET_CODE_MASK | constants/duel_field.inc | constants/card_info.inc | 1 |

均为 REUSE (复用), 非新建. GAS 全局符号解析不受影响, 但 fixer 生成 Ghidra 脚本时参考 inc 文件应以实际位置为准.

**N2 — 提案页眉槽计数文字有误**

"146 DAT_ + 2 PTR_ = 148 slots" 应为 "143 DAT_ + 5 PTR_ = 148 slots". 总量 148 正确, 覆盖率 100% 正确.

**N3 — BACKFIRE_CID R6 证据 passcode 笔误**

R6 表第一行写 "82705373" 应为 "82705573" (card_1547 pw=82705573). 槽值 0x1762 和卡名 Backfire 均正确.

---

## 状态: PASS

所有 C1-C13 均通过. 三处 NOTES 为非阻断文档问题, 不影响落地正确性.

---

## Reviewer Verdict: F03-Seg-9 = PASS
