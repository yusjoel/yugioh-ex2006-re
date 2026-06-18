# Refine Review: F09-Seg-7

File 09 `asm/09_equip_lp_display.s`, range `[0x080752cc, 0x0807629c)`.
Reviewer: independent, self-ran ref-scan + ROM byte checks. Does NOT trust proposal conclusions.

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | PASS | 路线图: Seg-7 0x752cc..0x7629c, 19fn, 46 slots, 6 inc. Proposal 完全一致. |
| C2 | 每个 ROM_INCBIN 块都有归宿 | PASS | 6 块全部进入 R4 disasm (B1..B6); asm 中精确核查 6 条 ROM_INCBIN 与 §五 路线图列表 byte-exact 匹配. §5.1=0. |
| C3 | §5.1 块确 0 引用 | PASS | §5.1=0 块, 无相关性. 6 块全部有引用 (见 C2). |
| C4 | EQ value == ROM 4 字节小端 | PASS | 自主 python 读全部 42 个 EQ 槽 ROM bytes, 无一不符. 详见下方 ref-scan 附表. |
| C5 | 新建 constants 前无现有可复用 | PASS | EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629: grep card_info.inc 0 命中 -> NEW 正确. MAGICAL_DIMENSION_CID=0x1678: 0 命中 -> NEW 正确. FRIENDSHIP_CID=0x167a: 1 命中 (card_info.inc line 1071) -> REUSE 正确. 14 个 REUSE 常量全部按 VALUE 确认存在. |
| C6 | 槽名有 file:line + 置信度证据 | PASS | 6 个关键槽全部有 asm file:line 引用 + conf:high. DWORD_08075c24 语义 (FS ROM ptr 到 CID data, mask 0x1fff) 在 asm 中核实. |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS (N/A) | carve=0. RENAME 槽 dispatch_eff_act_card_id_ptr_5c24 是 0x09e3fXXX FS ROM 地址, Ruling A RENAME_ONLY. 无需 rom.s 改动. |
| C8 | plate 引用全用现名, 无残留 FUN_/DAT_/DWORD_ | PASS | grep asm lines 14656..16265 for `FUN_[0-9a-f]{8}` -> 0 命中. PLATE=0 正确. 注: 现有 plate (enqueue_effect_slot_sprites_all_players) 含旧非正式名 "gEffectSlots"/"gSlotData" (非 FUN_/DAT_/DWORD_, 不违反 C8), 但需 fixer 落地时一并更新 -- 见修改建议. |
| C9 | ASCII: plate/EOL 文本纯 ASCII | PASS | EOL for DWORD_08075c24 ("FS ROM ptr: ...") 纯 ASCII. Seg-7 asm lines 14656..16265 全部 ASCII (python 逐字节核验). Proposal .md 文件中 CJK 仅存在于文档解释段落 (doc/ 中允许). |
| C10 | 指针表条目 +1 (THUMB), .word fn+1 == ROM raw 值 | PASS | B1/B3/B5 FS table THUMB+1 自主核验: B1@0x09e41678=0x08075379 (=0x08075378|1) OK; B3@0x09e41948=0x08075d0d (=0x08075d0c|1) OK; B5@0x09e41978=0x08075f91 (=0x08075f90|1) OK. B2/B4/B6 dispatch table 全 raw (非 THUMB+1) 核验: 表末项均为对应块起始地址 raw 值, 无 +1 混淆. |
| C11 | 函数体全局 vs 函数名矛盾 -> FUNC_RENAME | PASS | FUNC_RENAME=0. 抽查 enqueue_graveyard_spell_for_hand_set_code / dispatch_effect_activation_with_lp_counter / set_field_bit_by_slot_match_equip_dir -- 函数体逻辑与命名一致, 无矛盾信号. |
| C12 | 关键槽语义有 file:line + 置信度, 无零容忍词 | PASS | 全部 6 个 R6 槽均 conf:high + file:line. 无"似乎/大概/可能是"等零容忍词. |
| C13 | 段内所有残留自动名槽均被覆盖 | PASS | 自主 awk 精确清点: 27 DAT_ + 19 DWORD_ = 46. Proposal: EQ=42 + RENAME=4 = 46. Set 级精确匹配 (python 集合差集 = 空集). PTR_gP1LifePoints_* (4 个) 非 DAT_/DWORD_/UNK_ 前缀, 不计入, 正确. |

---

## 自主 ref-scan 结果 (C3 重核)

自主运行, 不信 proposal 数值:

| Block | GBA addr | sz | raw | thumb | B-addr+2 thumb | 判定 |
|-------|----------|----|-----|-------|----------------|------|
| B1 | 0x08075378 | 0x28 | 0 | 1 | - | R4 disasm fn_eligible |
| B2 | 0x08075414 | 0xa4 | 1 | 0 | - | R4 disasm sub-stubs |
| B3 | 0x08075d0c | 0x2c | 0 | 1 | - | R4 disasm fn_eligible |
| B4 | 0x08075d5c | 0x214 | 1 | 0 | - | R4 disasm sub-stubs |
| B5 | 0x08075f8e | 0x2e | 0 | 0 | 1 (addr+2=0x08075f90) | R4 disasm fn_eligible (2B pad) |
| B6 | 0x08075fe0 | 0x17c | 1 | 0 | - | R4 disasm sub-stubs |

B4 exhaustive scan 附记: python 对 B4 range [0x08075d5c, 0x08075f70) 全 ROM 穷扫发现 2 个额外命中:
- @ROM 0x772790 -> 0x08075d76 (raw): 周围字节 (0x4975d75d / 0xdb6db5c1) 为非指针数据, 判断为压缩数据中偶合字节; 非真实函数指针引用.
- @ROM 0xc26970 -> 0x08075e7b (THUMB+1): ROM offset 0xc26970 (~12.7MB 处, 卡图/图形数据区), 周围字节亦为非代码数据; 偶合.

结论: B4 无外部 FS handler table 引用 (THUMB+1=0), 全部真实引用来自同段内 dispatch table (0x75d38..0x75d58, 9 raw ptr). B4 -> R4 disasm 分类正确.

---

## CID 核验 (C4 + card-stats.s)

| 常量 | 值 | FS table @ | ROM 读回 CID | card-stats.s 确认 | passcode |
|------|----|-----------|------------|---------------------|---------|
| EMBLEM_OF_DRAGON_DESTROYER_CID | 0x1629 | 0x09e41674 | 0x00001629 | card_1292 slot=0x1629 | 06390406 |
| MAGICAL_DIMENSION_CID | 0x1678 | 0x09e41944 | 0x00001678 | card_1349 slot=0x1678 | 28553439 |
| FRIENDSHIP_CID (REUSE) | 0x167a | 0x09e41974 | 0x0000167a | card_1351 slot=0x167A | 81332143 |

---

## 注意事项 (不阻止 PASS, fixer 落地时处理)

### PLATE 旧非正式名 (非 C8 违规, 建议落地时一并修正)

enqueue_effect_slot_sprites_all_players 的 Ghidra plate 含旧非正式名:
- `gEffectSlots=0x0201e1c8` -> 应更新为 `gEquipZoneCountTable=0x0201e1c8`
- `gSlotData=0x0201c510` -> 应更新为 `gDuelFieldSlots=0x0201c510`

这两处不是 FUN_/DAT_/DWORD_ 残留 (C8 定义), 不构成 NEEDS_FIX 阻断条件. 但 proposal 将 PLATE=0, 而 R6 证据章节已隐式指出该 plate 与 canonical 常量名不一致. Fixer 落地时应把这两处旧名替换为现名, 并在 PLATE 计数中记录 (+1 update).

### B5 proc 细节

B5 clearListing 范围从 0x08075f90 (fn code start), 不含 0x75f8e 处 2B pad. pool 2 DWords 在 0x08075fb4 / 0x08075fb8 (均 python 核实正确). Fixer 应对 2B pad (0x0000) 保留为 `.zero 0x2` 或 createWord.

---

## 状态: PASS

所有 C1-C13 项均通过. 无硬规则违反. 2 个非阻断注意事项 (plate 旧非正式名) 已记录供 fixer 参考.

---

## 修改清单

无强制修改项 (PASS). Fixer 落地时可选处理:

- (建议) 更新 enqueue_effect_slot_sprites_all_players plate: `gEffectSlots` -> `gEquipZoneCountTable`, `gSlotData` -> `gDuelFieldSlots`. 不影响 byte-identical 验证结果.
