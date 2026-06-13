# Refine Review: F06-Seg-6

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | Seg-5 (0x565e8..0x57458) 已 COMPLETE, Seg-6 (0x57458..0x58550) 当前段, Seg-7 下一段; 无跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | PASS | block1 (0x57d0a/0x2a) R4 disasm; block2 (0x57d4c/0x15c) R4 disasm; 均有引用证据, 无静默保留 |
| C3 Rule3 | §5.1 块 0 引用确认 | N/A | 本段无 §5.1 登记块; 两块均有引用故不进 §5.1 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 抽查 15 槽全部 OK: gDuelPhaseFlags/STEP_OFF/AUX_OFF/PLAYER_BLOCK_STRIDE/gDuelFieldSlots/gDuelCardCtxBase/OAM_ATTR0_HIDDEN/ELIGIB_SPRITE_CTRL_OFF/P1LP_BLOCK2_OFF_1CE8/FIELD_STATE_OFF/OTOHIME_CID/CLIFF_CID/SPRITE_ATTR_MODE1/EQUIP_ACT_SCORE_MODE_103/gP1LP x28 |
| C5 R1 复用 | 新建 constants 前无现有同值 | PASS | 4 新建 (EQUIP_ACTIVATION_AUX_OFF=0x4b4 / CLIFF_THE_TRAP_REMOVER_CID=0x161e / OTOHIME_CID=0x1503 / EQUIP_ZONE_SPRITE_ATTR_MODE1=0x152a) 扫 constants/*.inc 全无碰撞; 0x152a 仅 rom_data.inc 有 0x0983152A (不同值) |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$, 无碰撞 | PASS | 检查 68 个 slot_label + 7 个 fn 名, 全 OK; 多同类有 _a/_b/.._j 后缀 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | PASS | 4 fn-ptr REF 有具名目标; PTR_DAT_08057d38 为 ptr_table 入口, 有计划; 6 block2 sub-fn labels 在 disasm 后接通 |
| C8 R5 现名 | plate 无残留 FUN_[0-9a-f]{8} | PASS | 全段 (L9462..L11806) grep FUN_ = 0 hits |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | 现有 2 CJK mojibake lines (L10933/L11806) 已识别; 提案的 PLATE P1/P2 替换文本全 ASCII (641/468 chars 验证) |
| C10 carve | ptr_table 条目为 raw 地址 (非 THUMB+1) | PASS | 5 条目 (0x57d38..0x57d48) 全为偶数 raw 地址; 正确 (dispatch via mov pc,r0, 非 bl, 故不需 +1) |
| C11 误名 | 函数名与体语义一致 | PASS | FUNC_RENAME 订正 tick_equip_activation_if_not_dd_assailant -> tick_equip_activation_if_not_otohime: 分发表 0x09e43d44=0x1503 (Otohime CID) 直接毗邻 fn-ptr 0x09e43d54=0x08057f99, 且 card-stats.s L13925 确认 slot=0x1503=Otohime; D.D.Assailant slot=0x172c (L19554), 旧名混淆了 card record# 与 slot_id |
| C12 R6 | 关键槽有 file:line + 置信度 | PASS | 8 个关键槽均有具体 file:line 证据及 high/med 置信度; 无零容忍词 |
| C13 残留 | 段内所有自动名槽全覆盖 | PASS | 实测 120 个 DAT_/DWORD_/PTR_ 自动名 label (L9462..L11806); 精确交叉比对 EQ(86)+fn-ptr REF(4)+PTR_DAT REF(1)+RENAME gP1LP(28)+disasm DAT_08057d4c(1) = 120; 0 遗漏 |

---

## ref-scan 独立复核结果

独立穷举 2B-step scan (raw + THUMB|1), 结果如下:

| 块 | 地址 | raw refs | THUMB+1 refs | 判定 |
|----|------|----------|--------------|------|
| block1 dispatch fn | 0x08057d0c | 0 | 1 @ 0x09e40e8c | R4 disasm; 0x09e40e7c=CID 0x14e6 (Emergency Provisions), fn-ptr slot 4 |
| block2 sub-fn A | 0x08057d4c | 1 @ 0x08057d38 | 0 | raw (ptr_table, mov pc,r0) |
| block2 sub-fn B | 0x08057df8 | 1 @ 0x08057d40 | 0 | raw (ptr_table) |
| block2 sub-fn C | 0x08057e40 | 2 @ 0x08057d3c+0x57d48 | 0 | raw (ptr_table, states 1+4) |
| block2 return stub | 0x08057ea0 | 1 @ 0x08057d44 | 0 | raw (ptr_table, state 3) |
| unlabeled fn | 0x08057678 | 0 | 2 @ 0x08057778+0x57b88 | R4 disasm; 两个 DAT_ 槽 = THUMB fn-ptr |

block2 总字节: 0xac+0x48+0x60+0x8 = 0x15c, 与 ROM_INCBIN 声明一致。

---

## 附记

1. **proposal 头部 EQ=96 计数偏差**: 实际 distinct EQ slot (纯数值常量) = 86 (17 gDuelPhaseFlags + 17 STEP_OFF + 8 AUX_OFF + 13 PLAYER_BLOCK_STRIDE + 3 gDuelFieldSlots + 4 gDuelCardCtxBase + 4 ELIGIB_SPRITE_CTRL_OFF + 1+1+1 三个小偏移 + 3 OAM_ATTR0_HIDDEN + 14 CID 类). 96 与 86 差 10 -- 推测 proposal 将 fn-ptr REF (2) + gP1LP (8 个 DWORD_ 而非 PTR_) 混入了统计。**此为 proposal 文档计数不精确; 实际覆盖全无遗漏 (120 全覆盖已验证), 不影响落地正确性。**

2. **block1 literal pool 位置**: 0x57d2a = 2 zero bytes; 0x57d2c = 0x0201b290 (gDuelPhaseFlags); 0x57d30 = 0x000004ac (STEP_OFF). clearListing(0x57d0a, 0x57d34) exclusive end 正确不含 0x57d34 的 ptr-to-table .word.

3. **FUNC_RENAME indeg**: bl refs = 0; fn-ptr THUMB+1 ref = 1 @ 0x09e43d54. 提案说 "indeg=1 (only one bl ref in asm/06)" 表述有误 (不是 bl 而是 fn-ptr), 但 indeg=1 数量正确, 不影响 RENAME 有效性。

4. **EOL 数学核验**: 0x8a<<5=0x1140 PASS; 0xfc<<4=0xfc0 PASS; 0xf0<<2=0x3c0 PASS.

5. **C9 scope**: L11806 的 CJK plate 属于 tick_equip_activation_neo_daedalus_gate (Seg-7 第一个函数), 但该行仍在 Seg-6 行范围内 (L9462..L11806 inclusive), 故 PLATE_SET P2 覆盖此行为正确; L11830 的 dispatch_equip_zone_sprite_by_slot_group CJK plate 在 Seg-6 范围外, 正确标记为 out of scope.

---

## 状态: PASS

## 修改清单

无需修改。所有 C1-C13 检查通过。

---

*Reviewer: claude-sonnet-4-6, 2026-06-14*
