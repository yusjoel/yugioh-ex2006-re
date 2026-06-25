# Refine Review: F11-Seg-9

Source: `asm/11_effect_slot_puzzletext.s` lines 26885-30887  
Range: `[0x08091888, 0x08093598)` -- 18 functions, 184 residual slots (180 DAT_ + 4 DWORD_)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | PASS | §五: Seg-9 [0x8091888..0x8093598); 前段 Seg-8 已完成; 无跳号/回头 |
| C2 | ROM_INCBIN/.byte 块全有归宿 | PASS | 段内 0 ROM_INCBIN, 0 .byte 行; python 扫描确认 |
| C3 | §5.1 块确 0 引用 | N/A | 无 ROM_INCBIN/byte 块, 无 §5.1 条目 |
| C4 | EQ value == ROM 4 字节小端 | PASS | 40 个 slot 全部 python 实读验证一致 |
| C5 | 新建前确无同值现有常量 | **FAIL (2 items)** | 见下方 #1/#2 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | 正则合规; python grep 无同名定义碰撞 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | gEquipActivationSlotBase(2 raw ref): slot 0x08091d98 在 Seg-9; gDuelFieldSlotState_ec(1 raw ref): slot 0x08091da0 在 Seg-9 |
| C8 | plate 引用全用现名, 无残留旧 FUN_ | **FAIL (1 item)** | flush_field_spell_equip_slot_sprites 重写 plate 741 chars >500 limit; 见 #3 |
| C9 | plate/EOL 文本纯 ASCII | PASS (待落地) | 2 条 CJK 行 (line 30340, 30586) 已在 proposal 中规划 ASCII 重写; plate 2 为 499 chars OK |
| C10 | 指针表条目 +1 THUMB | N/A | 无 carve |
| C11 | 全局 vs 函数名矛盾 | PASS | 无 FUNC_RENAME 信号 |
| C12 | 关键槽语义有 file:line + 置信度证据 | PASS | 6 个关键槽有 asm line + conf; gDuelFieldSlotState_ec conf:med 可接受 |
| C13 | 段内全部残留自动名槽被覆盖 | PASS | python 枚举: 180 DAT_ + 4 DWORD_ = 184; group 并集 unique = 184, 无漏槽 |

---

## 状态: NEEDS_FIX (3 items)

---

## 修改清单

### #1 -- C5 -- SANCTUARY_IN_THE_SKY_CID 标为 NEW, 应为 REUSE

**问题**: 提案将 `SANCTUARY_IN_THE_SKY_CID = 0x0000175e` 标注为 NEW, 但 `constants/card_info.inc:1234` 已有完全相同的定义:

```
.equ SANCTUARY_IN_THE_SKY_CID,  0x0000175e  @ The Sanctuary in the Sky ... Seg-7 DAT_08061b90
```

**影响槽**: 以下 3 个 slot 将 `SANCTUARY_IN_THE_SKY_CID` 标为 NEW, 实为 REUSE:
- `0x08091dac` (Group E, cid_sanctuary_1dac)

以及 Group I 中的分析结论也说 "NEW: `SANCTUARY_IN_THE_SKY_CID`".

**修复**: 将 `0x08091dac` 状态从 NEW 改为 `REUSE card_info.inc:1234`. 无需新增 `.equ` 行. 在 `新增 constants / 全局` 节删除该条目.

---

### #2 -- C5 -- EMISSARY_OF_THE_OASIS_CID 标为 NEW, 实为不同名但同值的 REUSE

**问题**: 提案将 `EMISSARY_OF_THE_OASIS_CID = 0x0000179d` 标为 NEW. 但 `constants/card_info.inc:194` 已有:

```
.equ EMISSARY_OF_OASIS_CID,  0x0000179d  @ Emissary of the Oasis; activation elig BST; 7 raw refs
```

现有名是 `EMISSARY_OF_OASIS_CID` (无 `_THE_`). 提案名 `EMISSARY_OF_THE_OASIS_CID` 与现有名不同但值相同, 若新建将产生同值重复 `.equ`.

**影响槽**: Group E `0x08091e40` (cid_emissary_1e40) 和 Group G `0x08091ee8` (cid_emissary_28e8 或 cid_emissary_2* -- 视具体 dup 行).  

实际影响: Group E 中 `0x08091e40 = 0x0000179d` 和 Group G 中对应 dup 槽.

**修复**: 
- 将这些槽的 const_name 改为现有名 `EMISSARY_OF_OASIS_CID` (REUSE card_info.inc:194).
- 在 `新增 constants / 全局` 节删除 `EMISSARY_OF_THE_OASIS_CID` 条目.
- 不新建该常量.

---

### #3 -- C8 -- flush_field_spell_equip_slot_sprites plate 重写超过 500 字符上限

**问题**: 提案为 `flush_field_spell_equip_slot_sprites` (0x080931de) 给出的 ASCII plate 重写长度为 **741 chars**, 超过 500 字符上限. Ghidra 设 plate 超 500 字符会截断或其他副作用; 工程标准硬限 500 chars.

**有问题的文本** (741 chars):
```
Called by eval_field_equip_activation_candidates (indeg=6+). Checks gEquipChainSlotRefs[+0x8] (busy flag) and sp[0x8] (context_flag); if either nonzero, returns immediately. Then checks [r4+0x2c] (activation_pending bit); if set and r7==0: compares [r4+0x10] to GYROID_CID(0x18f1) via check_value_in_slot_chain(chain_ref=TIME_WIZARD_CID=0x0fb6, 5 entries); on miss: clears [r4+0x2c], if sp[0x4] nonzero calls enqueue_sprite_attr_for_zone_card_id_lookup + enqueue_sprite_attr_with_mode(2) + enqueue_sprite_attr_with_mode(4); on hit: enqueue_sprite_attr_with_mode(4). Symmetric P2 side at sp[0x10]. Side effects: clears activation bit; up to 3 OAM enqueue calls. Constants: GYROID_CID=0x18f1, TIME_WIZARD_CID=0x0fb6, PLAYER_BLOCK_STRIDE=0x868.
```

**修复**: 将 plate 重写削减到 <=500 chars 并保持纯 ASCII. 建议保留核心语义, 削去冗余细节. 示例 (479 chars):

```
Clears equip-activation flag and enqueues OAM sprites. Callee of eval_field_equip_activation_candidates (indeg=6+). Guards: checks gEquipChainSlotRefs[+0x8] (busy) and sp[0x8] (ctx_flag); returns immediately if either set. Then: if [r4+0x2c] (activation_pending) set and r7==0, tests [r4+0x10] via check_value_in_slot_chain(chain=TIME_WIZARD_CID,5); on miss: clears pending, enqueues up to 3 OAM calls; on hit: 1 OAM call. P2 mirror at sp[0x10]. Side effects: write [r4+0x2c]=0; up to 3 enqueue_sprite_attr calls.
```

Length of example: 479 chars -- verify before applying.

---

## 附加说明 (非 FAIL, 供 fixer 参考)

### gEquipActivationSlotBase slot 标签不一致

Group A 表中 slot 0x08091d98 的标签名为 `ptr_gEquipActivationSlotBase_1d98`, REF_SLOTS 节中标签名为 `ptr_equip_act_slot_base_1d98`. 两处指向同一槽, fixer 落地时应统一为一个标签名. 推荐按 REF 节命名规范使用 `ptr_equip_act_slot_base_1d98`.

### EQUIP_ACTIVATION_CNT_CAP = 0xffff -- 4 个现有 0xffff 等值常量

`constants/duel_field.inc:395` 已有 `LP_ROW_TYPE8_ALL_SLOTS_MASK = 0x0000ffff`; `oam_attr.inc:156` 有 `EQUIP_SLOT_SCORE_CAP = 0x0000ffff`; `card_info.inc:386` 有 `SLOT_CARD_EMPTY = 0x0000ffff`; `oam_attr.inc:13` 有 `OAM_ATTR0_HIDDEN = 0x0000ffff`. 新建 `EQUIP_ACTIVATION_CNT_CAP` (激活次数饱和上限) 语义确实与上述四者不同 (score cap / LP display mask / card sentinel / OAM hidden), 属良性碰撞, 新建 **合规** (C5 OK). 但 fixer 脚本中须指定目标文件为 `duel_field.inc`.

### C8 stale FUN_ 其余项

提案列举的 FUN_0803c708 / FUN_0803c8e0 / FUN_08099314 等均在外部文件且已有 naming-proposals.csv 名称 (如 tick_equip_candidate_scan_with_display 等). 按惯例, 外部文件未命名引用 plate 保留 FUN_ 不改. 提案明确说明 "only fixing CJK plates and the one FUN_08091888" -- 合规.

### Group E 计数与 C13 arithmetic

提案 C13 arithmetic 写 "groups A:30 + B:8 + C:12 + D:26 + E:18 + F:23 + G:40 + H:19 + DWORD rename:4 = 180" -- Group A 实际有 40 行 (30 gEquipChainSlotRefs + 10 其他全局), Group E 有 16 行, 数字不精确. 但 python 枚举 unique addrs = 184 精确验证全覆盖, arithmetic 表述有误但结论正确. 不影响落地.

---

## Reviewer Verdict: F11-Seg-9 = NEEDS_FIX(3 items)
