# 函数/数据细化计划 — `asm/06_equip_eligibility_b.s`

> 阶段目标: 把 `asm/06_equip_eligibility_b.s` (ROM `0x080537C0 ~ 0x0805C2F0`, 装备资格按 slot flag
> 派发 `check_equip_slot_eligible_*` 簇尾 + Neo Daedalus 效果 + equip activation LP/score display seq +
> switch 派发) **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **7** 个文件 (file 00 / 01 / 02 / 03 / 04 / 05 已全 10 段完成, 见对应
> `p5-refine-0N-*.md`)。方法论 + R1-R9 细化清单 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..05 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**R1-R9 详版**见 `doc/dev/p5-refine-00-system-str-vija.md` §一。

**跨文件踩坑沿用** (file 00..05 沉淀, 务必遵守):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式) — memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
  **file 05 Seg-10 教训**: 段内可能残留命名期遗留的 **CJK mojibake plate**, executor 测绘时须 grep 段内
  非 ASCII plate 一并 ASCII 整段重写 (substring 替换对 CJK plate 静默 no-op)。
- **槽地址精确性**: 每个 DAT_/PTR_ 槽地址必须用 python `struct.unpack_from('<I', rom, rom_addr-0x08000000)`
  核对 ROM 字节值; executor 自报地址常有错, fixer 物化前 dry-run 暴露 WARN 即修正地址再实跑。
- **C5 按值去重**: 新建常量前必扫全 constants/*.inc 确认无同值常量。
  **偏移放宽 (用户裁定 file 05 Seg-5)**: 结构体字段偏移 `*_OFF` 与现有常量数值碰撞但属**不同 base 寄存器/不同结构体**
  → 良性碰撞各建独立常量 (如 ELIGIB_RESULT_OFF=0x584 vs GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF); 仅疑似同字段 (同 base) 才复用/问用户。
  **卡 ID / 掩码 / 位域 / 阈值等非偏移标量严格去重不变** (值碰撞必复用现有常量, 除非语义=不同实体如 state_code 碰 CID 才 RENAME-only)。
  (file 05 Seg-6/8/9 反复抓到已存在却重列: HARPIE_LADY_SISTERS_CID / SLOT_CARD_EMPTY / CARD_STAT_LP_THRESHOLD_999 等。)
- **C13 残留 100% 覆盖**: 段内所有 DAT_/DWORD_/PTR_ 须被 EQ+REF+RENAME 去重全覆盖; executor 必 python
  精确清点段内 .word 槽总数 (file 05 Seg-9 抓到 8 槽边界泄漏多计 125 实 117); **严防越界吃下一段/下一文件**。
- **C8 stale 函数名**: plate 中 stale `FUN_` 用**穷举 pattern** `FUN_[0-9a-f]{8}` 扫段内 asm 行范围
  (含跨模块指向其它已命名函数的, file 05 Seg-6 反复漏跨模块 FUN_), 完整字符串匹配替换现名 (禁子串);
  整段 setPlateComment 重写, 落地后 grep 段范围穷举 `FUN_[0-9a-f]{8}` == 0 + 无 CJK 验收。
- **卡牌 ID 常量**: 命名前必查 `data/card-stats.s` 坐实 passcode→slot_id→卡名; **passcode 注释逐一 python 核对**
  (file 05 Seg-9 抓到 3 处 pw= 错误, Seg-10 抓到 3 处卡名错); slot_id 未分配 → 中性 `<func>_cid_<hex>` 低置信, 勿臆造 (红线 3)。
- **packed/bitfield**: 语义不明单 packed 32-bit 值 → 中性 RENAME 标签 + med/low-conf EOL 记字节分解,
  **不臆造完整位域语义, 不 BLOCK 整段**。
- **EOL 数学自检**: 任何移位/算术/分支方向等式 EOL 必须 python 实算 + 对机器码核验
  (file 05 Seg-7 抓到 0x1840<<19 错误等式; Seg-10 抓到 ble 分支方向写反); 算不准 → 中性 "exact semantics not decoded"。
- **switch 跳转表 (file 06 含 3 表 0x80598fa/0x805b498/0x805b54e)**: `switchD_*` jump table 目标存裸 THUMB 地址
  → R4 disasm 逐 stub (file 00 Seg-5c 范式: clearListing 整 range → setTMode → 逐 stub DisassembleCommand);
  **file 05 Seg-6 教训**: case stub 可 bl 调用 secondary ROM_INCBIN 区 helper (级联发现), 这些 secondary 区表面 0-ref
  实为 case-stub 调用目标, 必须一并 disasm, 勿误判 §5.1 孤儿。
- **fn-ptr +1 永久踩坑**: Ghidra 把 THUMB fn-ptr 数据 ref 导出为偶地址, build diff 差 1 字节; 手改 `.word <fn>+1`。
  每次 re-export 后须重补。已知周期性修复槽 (跨文件累积):
  asm/03: 0x37884 / 0x389dc / 0x389f8 / 0x3aa74;
  asm/04: 0x40ab4 / 0x42638 / 0x45efc / 0x478f0;
  asm/05: Seg-8 的 6 fn-ptr 树槽。file 06 若出现新 fn-ptr 槽同样处理。
- 复用 file 00..05 已建 constants/*.inc 与 carve label (见 file 05 doc §一 资产清单)。

**file 02/03/04/05 已建可复用资产** (新建前必 grep 确认无同值): 见 `doc/dev/p5-refine-05-equip-eligibility-a.md` §一
(ewram.inc / duel_field.inc / card_info.inc ~310+ CID / oam_attr.inc / bitops.inc / 全局 / caller hub)。

---

## 二、落地工作流 (pipeline)

同 file 00..05 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineF06Seg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。
重段 (>~120 槽) 按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (06_equip_eligibility_b.s)

| Seg | 范围 | ~fn | ~slots | 内含 ROM_INCBIN/switch | 状态 | commit |
|-----|------|-----|--------|------------------------|------|--------|
| 1 | 0x537c0..0x541cc | 22 | 47 | — | ✅ | f3bb6a9 |
| 2 | 0x541cc..0x54ba0 | 22 | 50 | ROM_INCBIN 0x54614/0x48 | ✅ | 6c90482 |
| 3 | 0x54ba0..0x55440 | 22 | 43 | ROM_INCBIN 0x55188/0x34 | ✅ | aee415f |
| 4 | 0x55440..0x565e8 | 22 | 149 | — (重) | ✅ | pending |
| 5 | 0x565e8..0x57458 | 22 | 101 | — | ⬜ | — |
| 6 | 0x57458..0x58550 | 22 | 99 | ROM_INCBIN 0x57d0a/0x2a + 0x57d4c/0x15c | ⬜ | — |
| 7 | 0x58550..0x58cec | 22 | 54 | — | ⬜ | — |
| 8 | 0x58cec..0x59de0 | 22 | 107 | ROM_INCBIN 0x5953a/0x2a + 0x59588/0x164 + switchD_080598fa | ⬜ | — |
| 9 | 0x59de0..0x5b480 | 22 | 146 | ROM_INCBIN 0x59cc8/0x28 + 0x59d14/0xcc + 0x5a0aa/0x36 + 0x5a0f8/0xe4 (重) | ⬜ | — |
| 10 | 0x5b480..0x5c2f0 | 15 | 69 | switchD_0805b498 + switchD_0805b54e | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
重段提示: Seg-4 (149 槽) / Seg-9 (146 槽, 4 ROM_INCBIN) / Seg-8 (107 槽, switch) 较重, 必要时拆 Seg-Na/Nb
(地址序边界=函数结束处, 不回头)。3 switch 表 (0x80598fa Seg-8 / 0x805b498+0x805b54e Seg-10) 按 file 00 Seg-5c R4 范式处理。
10 个 ROM_INCBIN 块须 ref-scan 分类 (被引用代码→R4 disasm / 被引用数据→carve / 全 ROM 0 引用→§5.1)。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录 (2026-06-14, commit f3bb6a9)

- **段范围**: 0x080537c0..0x080541cc, 22 fn
- **EQ=45**: 19x PLAYER_BLOCK_STRIDE + 19x gDuelFieldSlots (ewram.inc 复用)
  + 2x SCROLLBAR_CLEAR_BITS_14_6 (gl_scrollbar.inc 复用; setcode-A bits[14:6] 清位)
  + 1x gEquipChainSlotRefs + 1x GRAVEKEEPERS_CANNONHOLDER_CID (card_info.inc 新建 0x158c)
  + 1x gDuelPhaseFlags + 1x LP_BAR_ANIM_STATE_OFF + 1x CHAIN_NODE_CARD_ARR_OFF
- **REF=1**: 0x08053e08 fn-ptr -> check_equip_slot_eligible_triple_predicate+1
- **RENAME=1**: DWORD_08054138 -> dispatch_equip_slot_eligible_by_type_prereqs_or_setcode_flag_a (equip_flag=0x1706 鉴别码; med-conf; 非 TORPEDO_FISH_CID)
- **PLATE=3**: P1 dispatch_equip_slot_eligible_by_type_prereqs_or_setcode ASCII 全段重写 (旧 CJK mojibake); P2 FUN_08054e5c->check_equip_slot_eligible_by_setcode_prereqs_all_slots (line 1024); P3 同上 (line 1482, 跨段 0x080541cc 提前修订)
- **新建 constants**: card_info.inc +1 (GRAVEKEEPERS_CANNONHOLDER_CID=0x158c); ewram.inc +2 (EQUIP_CTX_PLAYER_OFF=0x0, EQUIP_CTX_SLOT_REF_OFF=0x1c)
- **carve=0, disasm=0, §5.1=0**
- **fn-ptr periodic fix**: asm/03 x4 (check_level_conv_lab_node_match+1 x2, check_card_is_amazoness_type+1 x2) + asm/04 x3 (zone_monster_field_bonus_table+7*16, apply_nitro_unit_equip_activation+1, gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- **commit**: f3bb6a9

### 4.02 Seg-2 完成记录 (2026-06-14, commit pending)

- **段范围**: 0x080541cc..0x08054ba0, 23 fn (22 pre-existing + 1 new from disasm)
- **disasm=1**: ROM_INCBIN 0x08054614/0x48 -> check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight (Desert Sunlight CID 0x17B4 equip predicate #2; fn-ptr2 @ 0x09e421d4; leaf fn; clearListing->setTMode->DisassembleCommand->createFunction+setName+plate)
- **EQ=52**: 21x PLAYER_BLOCK_STRIDE + 22x gDuelFieldSlots (ewram.inc 复用) + 2x SCROLLBAR_KEEP_BITS_8_0 + 2x SCROLLBAR_CLEAR_BITS_14_6 (gl_scrollbar.inc 复用) + 5 new (TRICKYS_MAGIC_4_CID/GILFORD_THE_LEGEND_CID/THE_TRICKY_TARGET_SLOT_PATTERN [card_info.inc] + EQUIP_FLAG_TARGET_ICID_TABLE_OFF [duel_field.inc] + SERIAL_SPELL_CID [card_info.inc])
- **PLATE=1**: FUN_0809077c -> invoke_count_zone_pair_hits_full_range (0x0809077c, callback iterator) @ check_equip_slot_eligible_by_same_side_and_prereqs
- **carve=0, §5.1=0**
- **新建 constants**: card_info.inc +5 (ULTIMATE_BASEBALL_KID_CID=0x17e1 + TRICKYS_MAGIC_4_CID=0x180e + GILFORD_THE_LEGEND_CID=0x1938 + SERIAL_SPELL_CID=0x183e + THE_TRICKY_TARGET_SLOT_PATTERN=0xc0300000); duel_field.inc +1 (EQUIP_FLAG_TARGET_ICID_TABLE_OFF=0x10b0)
- **CSV sync**: naming-proposals.csv +1 行 (0x08054614 check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight)
- **fn-ptr periodic fix**: asm/03 x4 (check_level_conv_lab_node_match+1 x2 @ 0x37884/0x3aa74; check_card_is_amazoness_type+1 x2 @ 0x389dc/0x389f8) + asm/04 x3 (zone_monster_field_bonus_table+7*16 @ 0x40ab4; apply_nitro_unit_equip_activation+1 @ 0x45efc; gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF @ 0x478f0)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- **验收**: FUN_残留=0; CJK=0; ROM_INCBIN 0x54614 无残留; disasm fn check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight @ line 2140 出现
- **commit**: 6c90482

### 4.03 Seg-3 完成记录 (2026-06-14, commit pending)

- **段范围**: 0x08054ba0..0x08055440, 22 fn + 1 disasm'd (check_zone_slot_occupied_with_clear_equip_flag)
- **disasm=1**: ROM_INCBIN 0x08055188/0x34 -> check_zone_slot_occupied_with_clear_equip_flag (R4 disasm; fn-ptr2 @ dispatch_table 0x09e4365c CID 0x130f + 0x09e43b84 CID 0x14b4 Byser Shock; leaf fn bx lr; THUMB decode verified; clearListing->setTMode->DisassembleCommand->createFunction+setName+plate; lit pool 0x080551b0/0x080551b4 createDWord'd)
- **EQ=44**: 21x PLAYER_BLOCK_STRIDE + 21x gDuelFieldSlots (ewram.inc 复用) + 2x pool slots in disasm'd fn (check_zone_slot_clear_equip_stride / check_zone_slot_clear_equip_slots)
- **REF=1**: 0x08054c44 -> gEquipChainSlotRefs=0x0201bb90 (ewram.inc 复用; slot_label=check_equip_slot_eligible_by_prereqs_and_effect_ctx_ctx)
- **PLATE=1**: disasm'd fn plate (ASCII; 669 chars; dispatch table + predicate semantics)
- **FUNC_RENAME=0, PLATE_SUBS=0** (Seg-3 内所有 22 现有函数 plate 已 ASCII 无 stale FUN_)
- **carve=0, §5.1=0**
- **新建 constants/全局**: none (全复用 ewram.inc)
- **fn-ptr periodic fix**: asm/03 x4 (check_level_conv_lab_node_match+1 @ 0x37884/0x3aa74; check_card_is_amazoness_type+1 @ 0x389dc/0x389f8) + asm/04 x2 (zone_monster_field_bonus_table+7*16 @ 0x40ab4; apply_nitro_unit_equip_activation+1 @ 0x45efc) + asm/04 x1 (gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF @ 0x478f0) + asm/05 Seg-8 x6 (eval_equip_slot_score_by_card_state/check_equip_slot_eligible_by_card_id_bst/check_equip_slot_eligible_by_card_id_dispatch_b/check_equip_slot_eligible_by_type_then_prereqs/check_equip_slot_eligible_by_setcode_and_prereqs x2) + asm/06 x1 (check_equip_slot_eligible_triple_predicate+1 @ 0x53e08)
- **CSV sync**: naming-proposals.csv +1 行 (0x08055188 check_zone_slot_occupied_with_clear_equip_flag)
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- **验收**: FUN_残留=0; CJK=0; ROM_INCBIN 0x55188 无残留; disasm fn @ asm/06 line 3971
- **commit**: aee415f

### 4.04 Seg-4 完成记录 (2026-06-14, commit pending)

- **段范围**: 0x08055440..0x080565e8, 22 fn
- **EQ=145**: 10x PLAYER_BLOCK_STRIDE (ewram.inc) + 9x gDuelFieldSlots (ewram.inc) + 5x gDuelPhaseFlags (ewram.inc) + 2x PHASE_LOCK_FLAG_OFF (duel_field.inc) + 4x EQUIP_ACTIVATION_STEP_OFF (duel_field.inc 新建) + 55 CID (50 named + 5 gap; card_info.inc 新建) + 1x UMI_CARD_ID + 1x cid_12c6 (card_info.inc 复用) + 2x LP_COST_1500/3000 (duel_field.inc 复用) + 1x LP_COST_5000 (duel_field.inc 新建) + 1x TRIGGER_OP_PARAM_107 (duel_field.inc 新建) + 1x EQUIP_ZONE_SPRITE_ATTR (duel_field.inc 新建) + 3x Mooyan/A_Rival score labels (duel_field.inc 新建) + 19x BST score labels (duel_field.inc 新建) + 1x gDuelCardCtxBase + 1x ELIGIB_SPRITE_CTRL_OFF + 17x CID reuse (STAUNCH_DEFENDER/BUBBLE_SHUFFLE/LEGENDARY_FISHERMAN 等)
- **REF=5**: 1x fn-ptr check_equip_slot_eligible_by_type_and_card_id_pair+1 @ 0x08055770 + 4x gP1LifePoints @ 0x08055c6c/0x08056454/0x080564e8/0x08056570
- **RENAME=3**: tick_lp_row_type8_entry_duel_state/step_off/all_slots_mask (DWORD_ slots in tick_equip_activation_with_lp_row_type8_entry)
- **PLATE_SUBS=2**: P4 trigger_lp_row_type2_if_equip_tier_nonzero: FUN_0805715c->tick_equip_activation_state_by_phase + FUN_08059be0->enqueue_equip_zone_sprite_with_lp_tier
- **PLATE_SET=2**: P1 tick_equip_activation_state_machine (1047 chars, CJK mojibake 全段重写); P2 tick_equip_activation_with_lp_row_type8_entry (507 chars, CJK mojibake 全段重写)
- **新建 constants**: card_info.inc +55 CID; duel_field.inc +4 structural (EQUIP_ACTIVATION_STEP_OFF/TRIGGER_OP_PARAM_107/LP_COST_5000/EQUIP_ZONE_SPRITE_ATTR) + 22 score labels (3 named + 19 BST b_0x*)
- **carve=0, disasm=0, §5.1=0, FUNC_RENAME=0**
- **fn-ptr periodic fix**: asm/03 x4 (check_level_conv_lab_node_match+1 @ 0x37884/0x3aa74; check_card_is_amazoness_type+1 @ 0x389dc/0x389f8) + asm/04 x3 (zone_monster_field_bonus_table+7*16 @ 0x40ab4; apply_nitro_unit_equip_activation+1 @ 0x45efc; gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF @ 0x478f0)
- **验收**: FUN_ 残留=0 (lines 4427-7216); CJK=0; fn-ptr+1 all fixed
- **byte-identical**: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b
- **commit**: pending

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 06 范围 `[0x080537c0, 0x0805c2f0)` (213 named fn, 865 DAT_/DWORD_/PTR_ 槽, 10 ROM_INCBIN 块,
> 3 switchD 跳转表) 按**函数数**均分 10 段 (~22 fn/段, 边界=函数结束处=下一函数起点)。

| Seg | 地址范围 | ~fn | ~slots | 内含 ROM_INCBIN/switch | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x537c0..0x541cc | 22 | 47 | — | equip eligibility by slot equip flag dispatch + side/setcode/type 资格检查簇头 |
| Seg-2 | 0x541cc..0x54ba0 | 22 | 50 | ROM_INCBIN 0x54614/0x48 | side+setcode+prereqs+type 资格检查簇 |
| Seg-3 | 0x54ba0..0x55440 | 22+1 | 43 | ROM_INCBIN 0x55188/0x34 | equip_type+occupied 资格检查簇 ✅ |
| Seg-4 | 0x55440..0x565e8 | 22 | 149 | — | 重: same_player_type_mismatch + card_id BST/pairs 大型分发簇 ✅ |
| Seg-5 | 0x565e8..0x57458 | 22 | 101 | — | tick_equip_activation_with_lp_cost_sprite + LP cost display 簇头 |
| Seg-6 | 0x57458..0x58550 | 22 | 99 | ROM_INCBIN 0x57d0a/0x2a + 0x57d4c/0x15c | set_lp_row_type2 + equip activation LP display seq |
| Seg-7 | 0x58550..0x58cec | 22 | 54 | — | tick_equip_activation_neo_daedalus_gate + Neo Daedalus 效果簇 |
| Seg-8 | 0x58cec..0x59de0 | 22 | 107 | ROM_INCBIN 0x5953a/0x2a + 0x59588/0x164 + switchD_080598fa | tick_equip_score_lp_display_seq + switch 派发 |
| Seg-9 | 0x59de0..0x5b480 | 22 | 146 | ROM_INCBIN 0x59cc8/0x28 + 0x59d14/0xcc + 0x5a0aa/0x36 + 0x5a0f8/0xe4 | 重: tick_equip_zone14_activation_display_seq + 4 ROM_INCBIN 数据块 |
| Seg-10 | 0x5b480..0x5c2f0 | 15 | 69 | switchD_0805b498 + switchD_0805b54e | find_zone_slot_match_by_type_in_node_list + switch 派发 (文件末) |

执行约定同 file 00..05: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-05-equip-eligibility-a.md` (file 05 完整记录, §一 复用资产清单 / C5 偏移放宽 / fn-ptr +1 踩坑 / switch R4 范式 / CJK plate 重写)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
