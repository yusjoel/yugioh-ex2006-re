# Refine Review: F03-Seg-6

范围: `asm/03_equip_chain_hand.s` 0x0803b3a8..0x0803bba4  
reviewer: 独立复核 (不信 executor 结论，自主 ref-scan + ROM 字节核对)  
review iteration: 2 (post fix-iter-1)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 活动 doc §三 Seg-6=0x3b3a8..0x3bba4 完全吻合; Seg-7 从 eval_equip_placement_full_check@0x3bba4 (push 0x70b5) 开始; 无越界 |
| C2 Rule2 | 无 ROM_INCBIN/.byte 块残留 | ✅ | grep 独立确认 asm lines 11741..12835 内无 ROM_INCBIN 或 .incbin; 段内全为 literal-pool words |
| C3 Rule3 | §5.1 块 0 引用 | ✅ N/A | 本段无 §5.1 块; 无 inter-function 数据块 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | ✅ | 独立 python 核对 39 个关键槽 (含全部 9 新 CID + 4 switch-table ptr + 2 EFFECT_ZONE_BITMASK_OFF + PARASITE + 多组 PLAYER_BLOCK_STRIDE/gP1LifePoints): 0 mismatch |
| C5 R1 复用 | 新建常量前无现有同值 | ✅ | grep constants/card_info.inc 确认 0x132c/0x1679/0x135d/0x15ad/0x1578/0x1972/0x13ff/0x12b1/0x147f 均缺席; 其他 18 个 constants/*.inc 同样无命中; PARASITE_PARACIDE_CID=0x12a1 已在 card_info.inc 确认复用 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | fix-iter-1 已将 4 个 RENAME new_label 中的 `switchD` 改为 `switch`: entity_ref_switch_table_ptr / card_ref_switch_table_ptr / zone_attr_switch_table_ptr / field_word_switch_table_ptr。独立 regex 验证全部通过；EOL 文本中 switchD=False，无大写字母 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | ✅ N/A | 本段无 carve; 37 个 REF 槽各有 slot_label + 对应全局名 |
| C8 R5 现名 | plate 引用全用现名 | ✅ | 独立 grep lines 11741..12835: FUN_ 出现 2 次 (lines 11883/12357); proposal PLATE 表两条 substring replace 均正确映射: FUN_0803b5c0→get_zone_slot_field6_by_type, FUN_08040144→tick_hand_sort_display_init_seq |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | fix-iter-1 在 PLATE 更新表增加 2 个 setPlateComment 全文改写条目 (get_zone_slot_entity_ref_by_type line 11741 + set_player_state_bit line 12390); 独立 python 核对两段 ASCII 板文本: 0 non-ASCII chars; proposal 内其他 CJK 仅在 doc/ 节头/表头 (允许)，非 Ghidra plate/EOL 内容 |
| C10 carve | 指针表 `+1` (THUMB) | ✅ N/A | 段内无函数指针表; 4 个 switch-table ptr 均指向同一 ROM 段内数据 (非 THUMB fn-ptr) |
| C11 误名 | 函数体全局 vs 函数名无矛盾 | ✅ | 抽查 read_player_field_slot_word_by_zone / check_field_spell_last_warrior_placeable / write_slot_occupy_flag_bit: 全部与函数名语义一致; 无 FUNC_RENAME 需求 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | ✅ | 9 个新 CID 均提供 data/card-stats.s 行号 + 卡名 + passcode + slot_id，置信度标 high; 无零容忍词; EFFECT_ZONE_BITMASK_OFF 地址等式验证有记录 |
| C13 残留 | 所有残留自动名槽均已覆盖 | ✅ | EQ(54)+REF(37)+RENAME(4)=95; 独立扫描 lines 11741..12835 的 DAT_/PTR_ 定义总数=95，一一对应 |

---

## 独立复核记录 (iter-2 新增核验)

### C6 RENAME label 修复验证

fix-iter-1 将 4 个 RENAME 标签从 `switchD` 改为 `switch` 后:

| new_label | regex ^[a-z][a-z0-9_]+$ | EOL 含 switchD | EOL 含非 ASCII |
|---|---|---|---|
| entity_ref_switch_table_ptr | OK | No | No |
| card_ref_switch_table_ptr | OK | No | No |
| zone_attr_switch_table_ptr | OK | No | No |
| field_word_switch_table_ptr | OK | No | No |

`switchD` 仅出现在 §Fix iteration 1 历史记录表（文档叙述），非 new_label 实际值。

### C9 CJK plate 修复验证

PLATE 更新表 (proposal line 437-447) 列出 5 个动作:
1. get_zone_slot_card_ref_by_type — substring replace FUN_0803b5c0
2. write_slot_occupy_flag_bit — substring replace FUN_08040144
3. check_lp_exceeds_spell_copy_threshold — substring replace scale=132→scale=500
4. get_zone_slot_entity_ref_by_type — setPlateComment full rewrite (CJK→ASCII)
5. set_player_state_bit — setPlateComment full rewrite (CJK→ASCII)

ASCII plate text 独立核对:

**get_zone_slot_entity_ref_by_type (line 11741):** 10 行纯 ASCII 技术描述，涵盖 params/switch 覆盖范围/sibling reference/bases/indeg。python `[c for c in text if ord(c)>0x7F]` = []。

**set_player_state_bit (line 12390):** 7 行纯 ASCII 技术描述，涵盖 OR/BIC 语义/params/sibling/side effects/offsets。python `[c for c in text if ord(c)>0x7F]` = []。

内容忠实度: 两段均准确传达原 CJK 板注释的技术要点（语义一致），无信息丢失或歪曲。

### 无回归确认

- **C1**: 段边界未改动，仍为 0x0803b3a8..0x0803bba4。
- **C5**: 9 个新 CID 常量未添加新项，未触碰 constants/*.inc 已有内容。
- **C8**: 两条 stale-FUN_ 映射保持正确；PLATE 表条目 1-2 不受 fix-iter-1 影响。
- **C13**: 95/95 覆盖不变 (EQ54+REF37+RENAME4=95)。

---

## 状态: PASS

---

## 修改清单

无。fix-iter-1 已解决全部 2 项问题，C1-C13 全部 ✅。
