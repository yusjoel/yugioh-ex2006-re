# Refine Review: 04-Seg-8a

Segment: `asm/04_card_zone_sprite.s` [0x08044e30, 0x0804640c)
Proposal: `doc/dev/refine/04-Seg-8a.proposal.md`
Reviewer date: 2026-06-13 (iter 1: NEEDS_FIX(4); iter 2: final)

## 复核方法

- ROM 字节: `struct.unpack_from('<I', rom, addr-0x08000000)` 独立读取
- CID 坐实: 解析 `data/card-stats.s` `card_NNNN: @ Name  slot=0xXXXX` pattern 建索引
- constants 碰撞: 遍历 `constants/*.inc` 所有 `.equ` 建值→名映射 (4641 条)
- DAT_ 计数: regex 扫 asm 文件段内 `DAT_|DWORD_|PTR_DAT_|UNK_` label 去重
- FUN_ plate: 遍历行范围内所有 `FUN_` token, 验证映射名在 asm 文件中存在
- gap CID: 确认 card-stats.s 中无对应 slot 条目

---

## 核验矩阵 (C1-C13) — 迭代 2 终核

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | Seg-8a = Seg-8 [0x44e30..0x47990] 有效子拆分; 上界 0x0804640c 处 hword=0xb5f0 (PUSH) = 函数入口确认 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS (N/A) | 段内无 ROM_INCBIN/.byte 块 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS (N/A) | 无数据块, §5.1=0 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立核对: 4 个 fix 槽 (0x08045524=0x10f4 / 0x080451c4=0x1368 / 0x08044f60=0x147d / 0x08045028=0x182d); OAM/offset/sentinel/REF/RENAME/fn-ptr 各类代表槽全验; 所有 43 抽查点匹配 |
| C5 R1 复用 | 新建 constants 前无现有同值 | PASS | 迭代 2 修复: 4 处碰撞全改 REUSE (UMI_CARD_ID/SPELL_ZONE_TARGET_CARD_ID/ZOMBYRA_THE_DARK_CID/RAGING_FLAME_SPRITE_CID); 剩余 62 新 .equ 无名称碰撞、无值碰撞 (全量扫描 constants/*.inc 4641 条) |
| C6 R2 名 | 槽名合规, 无碰撞 | PASS | 所有 RENAME slot_label (`nitro_unit_*/archfiend_*/pandemonium_*/centrifugal_*/spell_path_*`) 符合 `^[a-z][a-z0-9_]+$`; EQ 名合规; 无碰撞 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | gEquipZoneCountTable 新全局 high-conf + file:line; REF x18 全有 USER-label; fn-ptr THUMB+1 正确 |
| C8 R5 现名 | plate 引用全用现名 | PASS | 20 unique FUN_ token; 所有映射目标已在对应 asm 文件以现名存在 (file 04/06/08/11 跨模块确认) |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | RENAME 表 11 行 EOL 全 ASCII; PLATE 块 0 非 ASCII 字节; proposal doc 节标题含 CJK 属 doc/ 正常用法, 不影响 Ghidra 内容 |
| C10 carve | 指针表 `.word <fn>+1` 正确 | PASS | 0x08045efc=0x08045531=apply_nitro_unit_equip_activation(0x08045530)+1; fn 首 hword=0xb530 (PUSH) |
| C11 误名 | 函数名与函数体无矛盾 | PASS | 9 fn 名字与主体一致; proposal 无 FUNC_RENAME |
| C12 R6 | 关键槽语义有 file:line + 置信度, 无零容忍词 | PASS | med-conf 槽 (0x080454bc / composite packed vals) 均有 L: 证据 + 置信度标注; 无零容忍词 |
| C13 残留 | 段内所有自动名槽全覆盖 | PASS | 独立 grep: 143 unique DAT_/DWORD_/PTR_ 地址; proposal 处理 143; 差集空 |

---

## 附加观察 (不影响 PASS)

- **card_info.inc 新建计数**: proposal 正文声称 61, 实际 .equ 块有 62 条 (56 regular + 2 bare-CID + 4 gap)。内部描述 "57 named + 2 bare + 4 gap" 也与实际 56 regular 差 1。属 proposal 内部统计笔误, 不影响内容正确性 (所有 62 条无碰撞, 4 REUSE 注释正确)。fixer 落地时按实际 .equ 列表操作即可, 无需纠正数字。

---

## 状态: PASS

迭代 2 全部 C1-C13 通过。4 处 C5 碰撞已在 iter 1 修改清单要求下全部改为 REUSE。
无新回归。可进入落地阶段。
